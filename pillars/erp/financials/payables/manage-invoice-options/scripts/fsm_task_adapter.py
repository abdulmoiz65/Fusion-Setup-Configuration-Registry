#!/usr/bin/env python3
"""Portable, data-driven FSM task adapter runtime.

This file is copied into a generated Nested task skill.  Task semantics live in
the adjacent e2e-adapter.json descriptor and ora-resource rule plan.  The
runtime performs offline package work only; it never connects to Fusion.

Reading guide: the helpers verify the JSON contract and FSM ZIP, normalize a
requested design, validate task rules, build a candidate ZIP, and reconcile a
later export. The CLI at the end only joins those offline steps; it does not
submit an import.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
import re
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path, PurePosixPath
from typing import Any
from xml.etree import ElementTree


SCHEMA_VERSION = "fscr-fsm-task-adapter-v1"
MAX_MEMBER_BYTES = 10 * 1024 * 1024
MAX_TOTAL_BYTES = 100 * 1024 * 1024
MAX_COMPRESSION_RATIO = 100
SUCCESS_STATUS = re.compile(r"COMPLETE|SUCCESS|SUCCEED", re.IGNORECASE)

# Source-backed import validation: both priority fields are non-null numbers
# and accept values from 1 through 99.
PRIORITY_RANGES: dict[tuple[str, str], tuple[int, int]] = {
    ("AP_SYSTEM_PARAMETER", "PaymentPriority"): (1, 99),
    ("AP_SYSTEM_PARAMETER", "EmployeePaymentPriority"): (1, 99),
}

# ApprovalTiming is the exported AP_SYSTEM_PARAMETER code, not the UI lookup
# type or a prefixed lookup identifier.
APPROVAL_TIMING_CODES = {"A", "N", "Y"}


class AdapterError(ValueError):
    """A safe, user-correctable adapter failure."""


class BatchValidationError(AdapterError):
    """One or more independent operation validations failed in a batch."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = tuple(errors)
        super().__init__(
            "Batch validation failed:\n" + "\n".join(f"- {error}" for error in errors)
        )


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_path(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AdapterError(f"Cannot read valid JSON from {path}: {exc}") from exc


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _default_contract_path() -> Path:
    return Path(__file__).resolve().parents[1] / "e2e-adapter.json"


# Validate the descriptor before using it so every later operation has a
# trustworthy task identity, entity list, and schema version.
def _load_contract(path: Path) -> dict[str, Any]:
    contract = _read_json(path)
    if not isinstance(contract, dict):
        raise AdapterError("Adapter contract must be a JSON object.")
    if contract.get("schemaVersion") not in (SCHEMA_VERSION, "fscr-fsm-task-adapter-v2"):
        raise AdapterError(
            f"Unsupported adapter schema: {contract.get('schemaVersion')!r}."
        )
    task = contract.get("task")
    package = contract.get("package")
    if not isinstance(task, dict) or not task.get("name") or not task.get("code"):
        raise AdapterError("Adapter contract lacks exact task identity.")
    if not isinstance(package, dict) or not package.get("entities"):
        raise AdapterError("Adapter contract lacks package entities.")
    return contract


def _entity_map(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {entity["name"]: entity for entity in contract["package"]["entities"]}


def merge_shared_row_transaction(
    contract: dict[str, Any],
    baseline_row: dict[str, Any],
    bu_name: str,
    invoice_values: dict[str, Any],
    payment_values: dict[str, Any],
) -> dict[str, Any]:
    """Create the sole canonical AP_SYSTEM_PARAMETER update for one BU.

    A multi-task request must never create competing full-row packages.  This
    function merges the two page intents once, validates the resulting row with
    both task contracts, and selects Invoice Options as the single writer.
    """
    entity = _entity_map(contract).get("AP_SYSTEM_PARAMETER")
    if entity is None:
        raise AdapterError("Invoice Options lacks AP_SYSTEM_PARAMETER.")
    if not isinstance(bu_name, str) or not bu_name.strip():
        raise AdapterError("Shared-row transaction requires one nonblank BuName.")
    if baseline_row.get("BuName") != bu_name:
        raise AdapterError("Shared-row transaction baseline does not match BuName.")
    if not isinstance(invoice_values, dict) or not isinstance(payment_values, dict):
        raise AdapterError("Shared-row transaction values must be objects.")
    overlap = {
        field for field in set(invoice_values) & set(payment_values)
        if invoice_values[field] != payment_values[field]
    }
    if overlap:
        raise AdapterError(
            "Shared-row transaction has conflicting values for "
            + ", ".join(sorted(overlap)) + "."
        )
    changes = dict(invoice_values)
    changes.update(payment_values)
    if not changes:
        raise AdapterError("Shared-row transaction requires at least one change.")
    prohibited = set(entity["keyFields"]) | set(entity["auditFields"])
    unknown = set(changes) - set(entity["headers"])
    if unknown or set(changes) & prohibited:
        raise AdapterError("Shared-row transaction contains unsupported field changes.")
    resulting_row = dict(baseline_row)
    resulting_row.update(changes)
    _validate_invoice_ui_values(entity, changes, "shared-row-transaction")
    _validate_invoice_ui_dependencies(resulting_row, "shared-row-transaction")
    _validate_payment_owned_values(
        entity, "update", resulting_row, "shared-row-transaction"
    )
    return {
        "schemaVersion": SCHEMA_VERSION,
        "entity": "AP_SYSTEM_PARAMETER",
        "targetKey": {"BuName": bu_name},
        "values": changes,
        "resultingRow": resulting_row,
        "writerTask": contract["task"],
        "validatedContracts": [
            "Manage Invoice Options",
            "Manage Payment Options",
        ],
    }


def _validate_payment_owned_values(
    invoice_entity: dict[str, Any], action: str, values: dict[str, Any], operation_id: str
) -> None:
    """Apply Payment Options validation to Payment-owned shared-row fields.

    This deliberately calls only the Payment field contract, never its full
    normalization routine: Invoice -> Payment full-adapter calls would recurse
    through the reciprocal AP_SYSTEM_PARAMETER dependency.
    """
    payment_root = Path(__file__).resolve().parents[2] / "manage-payment-options"
    descriptor_path = payment_root / "e2e-adapter.json"
    runtime_path = payment_root / "scripts" / "fsm_task_adapter.py"
    if not descriptor_path.is_file() or not runtime_path.is_file():
        raise AdapterError(
            "Payment-owned AP_SYSTEM_PARAMETER fields require the sibling Manage "
            "Payment Options adapter and runtime at pillars/erp/financials/payables/"
            "manage-payment-options/."
        )
    spec = importlib.util.spec_from_file_location(
        "fscr_manage_payment_options_field_contract", runtime_path
    )
    if spec is None or spec.loader is None:
        raise AdapterError("Cannot load the sibling Manage Payment Options runtime.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(spec.name, None)
        raise
    payment_contract = module._load_contract(descriptor_path)
    payment_entity = module._entity_map(payment_contract).get("AP_SYSTEM_PARAMETER")
    if payment_entity is None:
        raise AdapterError("Payment Options lacks an AP_SYSTEM_PARAMETER field contract.")
    for key in ("headers", "keyFields", "auditFields", "nodePath", "nodeSequence"):
        if invoice_entity.get(key) != payment_entity.get(key):
            raise AdapterError(
                "Invoice Options and Payment Options AP_SYSTEM_PARAMETER contracts "
                f"differ at {key}; refresh task evidence before building a candidate."
            )
    payment_fields = set(module.PAYMENT_OWNED_FIELDS)
    supplied_payment_fields = set(values) & payment_fields
    if not supplied_payment_fields:
        return
    if action != "update":
        # The Invoice task owns the complete shared-row create contract.  Use
        # that already-loaded, source-backed contract instead of reopening the
        # sibling descriptor from disk: during a Payment Options regeneration
        # that file can legitimately still be the prior promoted revision.
        # Payment's runtime below still applies its task-owned UI/value rules.
        create_fields = set(invoice_entity.get("createFields", {}))
        unsupported = supplied_payment_fields - create_fields
        if unsupported:
            raise AdapterError(
                f"Operation {operation_id} supplies Payment-owned create fields without "
                f"a source-backed Payment Options create contract: {sorted(unsupported)}."
            )
    try:
        module.validate_payment_owned_row(payment_entity, values, operation_id)
    except Exception as exc:
        raise AdapterError(
            "Payment Options field validation failed for shared "
            f"AP_SYSTEM_PARAMETER row: {exc}"
        ) from exc


def _safe_member_name(name: str) -> None:
    normalized = name.replace("\\", "/")
    pure = PurePosixPath(normalized)
    if pure.is_absolute() or ".." in pure.parts or normalized.startswith("/"):
        raise AdapterError(f"Unsafe ZIP member name: {name!r}.")


def _decode_csv(raw: bytes, member: str) -> tuple[list[str], list[dict[str, str]]]:
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise AdapterError(f"{member} is not UTF-8 CSV: {exc}") from exc
    try:
        reader = csv.reader(io.StringIO(text, newline=""))
        headers = next(reader, [])
        if (
            not headers
            or any(not str(header).strip() for header in headers)
            or len(set(headers)) != len(headers)
        ):
            raise AdapterError(f"{member} has blank or duplicate headers.")
        rows = []
        for number, values in enumerate(reader, start=2):
            if len(values) != len(headers):
                raise AdapterError(
                    f"{member} row {number} has {len(values)} CSV fields but the "
                    f"template header has {len(headers)}. Every row must serialize "
                    "one field per exact template header; trailing blanks require "
                    "explicit empty CSV fields."
                )
            rows.append(dict(zip(headers, values)))
    except csv.Error as exc:
        raise AdapterError(f"{member} is not valid CSV: {exc}") from exc
    return headers, rows


def _csv_bytes(headers: list[str], rows: list[dict[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=headers,
        extrasaction="raise",
        quoting=csv.QUOTE_ALL,
        lineterminator="\n",
    )
    writer.writeheader()
    for row in rows:
        writer.writerow(
            {
                header: "" if row.get(header, "") is None else str(row.get(header, ""))
                for header in headers
            }
        )
    return stream.getvalue().encode("utf-8")


def _first_xml_text(root: ElementTree.Element, local_name: str) -> str:
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1] == local_name:
            return "" if node.text is None else node.text.strip()
    return ""


@dataclass
class PackageData:
    path: Path
    archive_sha256: str
    member_names: list[str]
    member_bytes: dict[str, bytes]
    member_infos: dict[str, zipfile.ZipInfo]
    headers: dict[str, list[str]]
    rows: dict[str, list[dict[str, str]]]
    metadata: dict[str, str]
    object_contracts: dict[str, dict[str, Any]]


def _metadata_object_contracts(root: ElementTree.Element) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1] != "MigrationProcessBusinessObjectCSVMetadataVORow":
            continue
        name = _first_xml_text(node, "BusinessObjectShortName")
        if not name:
            continue
        if name in result:
            raise AdapterError(f"Metadata contains duplicate business object {name}.")
        attributes = [
            value.strip()
            for value in _first_xml_text(node, "XmlAttributeList").split(",")
            if value.strip()
        ]
        types = [
            value.strip()
            for value in _first_xml_text(node, "XmlAttributeTypeList").split(",")
        ]
        if len(attributes) != len(types):
            raise AdapterError(
                f"Metadata object {name} has {len(attributes)} attributes and {len(types)} types."
            )
        result[name] = {
            "nodePath": _first_xml_text(node, "XmlNodePath"),
            "nodeSequence": _first_xml_text(node, "NodeSequence"),
            "types": dict(zip(attributes, types)),
        }
    return result


def _read_package(path: Path, contract: dict[str, Any]) -> PackageData:
    try:
        archive_bytes = path.read_bytes()
        with zipfile.ZipFile(io.BytesIO(archive_bytes), "r") as archive:
            infos = archive.infolist()
            names = [info.filename for info in infos]
            total_size = 0
            for info in infos:
                _safe_member_name(info.filename)
                if info.is_dir():
                    raise AdapterError(f"Directory ZIP members are not allowed: {info.filename!r}.")
                if info.flag_bits & 0x1:
                    raise AdapterError(f"Encrypted ZIP members are not allowed: {info.filename!r}.")
                if info.file_size > MAX_MEMBER_BYTES:
                    raise AdapterError(f"ZIP member is too large: {info.filename!r}.")
                total_size += info.file_size
                if total_size > MAX_TOTAL_BYTES:
                    raise AdapterError("FSM ZIP expands beyond the allowed total size.")
                if info.file_size and info.file_size / max(info.compress_size, 1) > MAX_COMPRESSION_RATIO:
                    raise AdapterError(f"ZIP member compression ratio is unsafe: {info.filename!r}.")
            if len(names) != len(set(names)):
                raise AdapterError(f"{path.name} contains duplicate ZIP members.")
            member_bytes = {name: archive.read(name) for name in names}
            member_infos = {info.filename: info for info in infos}
    except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
        if isinstance(exc, AdapterError):
            raise
        raise AdapterError(f"Cannot read FSM ZIP {path}: {exc}") from exc

    expected = [contract["package"]["metadataMember"]] + [
        entity["member"] for entity in contract["package"]["entities"]
    ]
    if sorted(names) != sorted(expected):
        raise AdapterError(
            f"{path.name} members differ from the exact task contract; "
            f"expected {sorted(expected)}, found {sorted(names)}."
        )

    headers: dict[str, list[str]] = {}
    rows: dict[str, list[dict[str, str]]] = {}
    for entity in contract["package"]["entities"]:
        actual_headers, actual_rows = _decode_csv(
            member_bytes[entity["member"]], entity["member"]
        )
        if actual_headers != entity["headers"]:
            raise AdapterError(
                f"{entity['member']} header order differs from e2e-adapter.json."
            )
        headers[entity["name"]] = actual_headers
        rows[entity["name"]] = actual_rows

    metadata_member = contract["package"]["metadataMember"]
    try:
        root = ElementTree.fromstring(member_bytes[metadata_member])
    except ElementTree.ParseError as exc:
        raise AdapterError(f"Invalid {metadata_member}: {exc}") from exc
    metadata = {
        name: _first_xml_text(root, name)
        for name in (
            "ProcessName",
            "ProcessStatus",
            "ProcessEnv",
            "ProcessRelease",
            "ESSRequestId",
            "ObjectShortName",
        )
    }
    if metadata["ObjectShortName"] != contract["package"]["objectShortName"]:
        raise AdapterError(
            "Package ObjectShortName does not match the adapter task identity: "
            f"{metadata['ObjectShortName']!r}."
        )
    if not SUCCESS_STATUS.search(metadata["ProcessStatus"]):
        raise AdapterError(
            f"Package process status is not successful: {metadata['ProcessStatus']!r}."
        )
    if not metadata["ProcessEnv"] or not metadata["ProcessRelease"]:
        raise AdapterError("Package metadata must declare ProcessEnv and ProcessRelease.")
    object_contracts = _metadata_object_contracts(root)
    for entity in contract["package"]["entities"]:
        actual = object_contracts.get(entity["name"])
        if actual is None:
            raise AdapterError(
                f"Metadata lacks business object contract for {entity['name']}."
            )
        if actual["nodePath"] != entity["nodePath"]:
            raise AdapterError(
                f"Metadata node path for {entity['name']} is {actual['nodePath']!r}, expected {entity['nodePath']!r}."
            )
        expected_node_sequence = str(entity["nodeSequence"]).strip()
        actual_node_sequence = str(actual["nodeSequence"]).strip()
        if not re.fullmatch(r"[1-9][0-9]*", expected_node_sequence):
            raise AdapterError(
                f"Adapter node sequence for {entity['name']} must be a positive integer; "
                f"found {expected_node_sequence!r}."
            )
        if not re.fullmatch(r"[1-9][0-9]*", actual_node_sequence):
            raise AdapterError(
                f"Metadata node sequence for {entity['name']} must be a positive integer; "
                f"found {actual_node_sequence!r}."
            )
        if actual_node_sequence != expected_node_sequence:
            raise AdapterError(
                f"Metadata node sequence for {entity['name']} is {actual_node_sequence!r}, "
                f"expected {expected_node_sequence!r} from e2e-adapter.json."
            )
        for field, actual_type in actual["types"].items():
            if field not in entity["headers"]:
                raise AdapterError(
                    f"Metadata object {entity['name']} contains non-CSV attribute {field}."
                )
            if entity["types"].get(field, "") != actual_type:
                raise AdapterError(
                    f"Metadata type for {entity['name']}.{field} is {actual_type!r}, expected {entity['types'].get(field, '')!r}."
                )
    return PackageData(
        path=path,
        archive_sha256=_sha256_bytes(archive_bytes),
        member_names=names,
        member_bytes=member_bytes,
        member_infos=member_infos,
        headers=headers,
        rows=rows,
        metadata=metadata,
        object_contracts=object_contracts,
    )


def _schema_fingerprint(contract: dict[str, Any], package: PackageData) -> str:
    normalized = {
        "taskCode": contract["task"]["code"],
        "objectShortName": contract["package"]["objectShortName"],
        "metadataMember": contract["package"]["metadataMember"],
        "entities": [
            {
                "name": entity["name"],
                "member": entity["member"],
                "nodePath": package.object_contracts[entity["name"]]["nodePath"],
                "headers": package.headers[entity["name"]],
                "types": [
                    package.object_contracts[entity["name"]]["types"].get(field, "")
                    for field in package.headers[entity["name"]]
                ],
            }
            for entity in sorted(
                contract["package"]["entities"], key=lambda item: item["member"]
            )
        ],
    }
    return _sha256_bytes(_canonical_bytes(normalized))


def _validate_new_outputs(outputs: list[Path], inputs: list[Path]) -> None:
    resolved_outputs = [path.resolve() for path in outputs]
    resolved_inputs = {path.resolve() for path in inputs}
    if len(resolved_outputs) != len(set(resolved_outputs)):
        raise AdapterError("Output paths must be distinct.")
    for path in resolved_outputs:
        if path in resolved_inputs:
            raise AdapterError(f"Output path overlaps an input: {path}.")
        if path.exists():
            raise AdapterError(f"Refusing to overwrite existing output: {path}.")


def _validate_source_pair(
    contract: dict[str, Any], template: PackageData, baseline: PackageData
) -> None:
    if any(template.rows[entity["name"]] for entity in contract["package"]["entities"]):
        raise AdapterError("Build template must be template-only and contain no data rows.")
    for field in ("ProcessEnv", "ProcessRelease"):
        if template.metadata[field] != baseline.metadata[field]:
            raise AdapterError(
                f"Template and baseline {field} differ: {template.metadata[field]!r} versus {baseline.metadata[field]!r}."
            )
    # evidenceRelease records authoring provenance. Runtime compatibility is
    # established by the exact task identity, matching live source releases,
    # and the stable member/path/header/type fingerprint below. A compatible
    # environment release must not require regenerating an otherwise identical
    # task adapter.


def _row_key(entity: dict[str, Any], row: dict[str, str]) -> tuple[str, ...]:
    return tuple(row.get(field, "") for field in entity["keyFields"])


def _target_tuple(entity: dict[str, Any], target: dict[str, Any]) -> tuple[str, ...]:
    return tuple(str(target.get(field, "")) for field in entity["keyFields"])


def _validate_field_value(
    entity: dict[str, Any], field: str, value: Any, operation_id: str
) -> None:
    # BankChargeBearer is owned by the extensible IBY_BANK_CHARGE_BEARER
    # lookup.  Its value is deliberately passed through to FSM Import without
    # local validation in either shared-row task.
    if entity["name"] == "AP_SYSTEM_PARAMETER" and field == "BankChargeBearer":
        return
    expected = entity["types"].get(field, "string") or "string"
    lowered = expected.lower()
    if lowered in {"datetime", "timestamp"} or "timestamp" in lowered:
        normalized_type = "dateTime"
    elif lowered == "date" or ("date" in lowered and "time" not in lowered):
        normalized_type = "date"
    elif lowered in {"integer", "short"}:
        normalized_type = "int"
    elif lowered in {"number", "float", "double", "bigdecimal"}:
        normalized_type = "decimal"
    else:
        normalized_type = expected
    valid = False
    if normalized_type == "string":
        valid = isinstance(value, str)
    elif normalized_type in {"int", "long"}:
        valid = (
            isinstance(value, int)
            and not isinstance(value, bool)
        ) or (
            isinstance(value, str)
            and re.fullmatch(r"[+-]?\d+", value.strip()) is not None
        )
    elif normalized_type == "decimal":
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            candidate = str(value)
        elif isinstance(value, str):
            candidate = value.strip()
        else:
            candidate = ""
        if candidate:
            try:
                valid = Decimal(candidate).is_finite()
            except InvalidOperation:
                valid = False
    elif normalized_type == "date":
        if isinstance(value, str) and value.strip():
            try:
                date.fromisoformat(value.strip())
                valid = True
            except ValueError:
                valid = False
    elif normalized_type == "dateTime":
        if isinstance(value, str) and value.strip():
            candidate = value.strip()
            if candidate.endswith("Z"):
                candidate = candidate[:-1] + "+00:00"
            try:
                datetime.fromisoformat(candidate)
                valid = True
            except ValueError:
                valid = False
    else:
        valid = isinstance(value, str)
    if not valid:
        raise AdapterError(
            f"Operation {operation_id} field {entity['name']}.{field} expects "
            f"a source-compatible {expected} value; received {type(value).__name__}."
        )
    priority_range = PRIORITY_RANGES.get((entity["name"], field))
    if priority_range:
        minimum, maximum = priority_range
        numeric_value = int(str(value).strip())
        if not minimum <= numeric_value <= maximum:
            raise AdapterError(
                f"Operation {operation_id} field {entity['name']}.{field} must be "
                f"within the source-backed range {minimum} through {maximum}; "
                f"received {numeric_value}."
            )


def _row_index(
    package: PackageData, entity: dict[str, Any]
) -> dict[tuple[str, ...], dict[str, str]]:
    if not entity["keyFields"]:
        raise AdapterError(f"Entity {entity['name']} has no source-backed key.")
    result: dict[tuple[str, ...], dict[str, str]] = {}
    for number, row in enumerate(package.rows[entity["name"]], start=2):
        key = _row_key(entity, row)
        if any(value == "" for value in key):
            raise AdapterError(
                f"{entity['member']} row {number} has a blank key component."
            )
        if key in result:
            raise AdapterError(
                f"{entity['member']} contains duplicate key {key!r}."
            )
        result[key] = row
    return result


def _satisfied_prerequisites(
    blueprint: dict[str, Any], contract: dict[str, Any]
) -> set[tuple[str, str, str]]:
    declared = {
        (entity["name"], blocker["field"]): blocker["resolver"]
        for entity in contract["package"]["entities"]
        for blocker in entity.get("conditionallyBlockedFields", [])
    }
    satisfied: set[tuple[str, str, str]] = set()
    for item in blueprint.get("prerequisites", []):
        if not isinstance(item, dict) or item.get("status") != "satisfied":
            continue
        entity = str(item.get("entity", ""))
        field = str(item.get("field", ""))
        resolver = str(item.get("resolver", ""))
        if (
            entity
            and field
            and resolver
            and item.get("evidence")
            and declared.get((entity, field)) == resolver
        ):
            satisfied.add((entity, field, resolver))
    return satisfied


LOOKUP_RECEIPT_CONTRACTS: dict[str, tuple[str, str, bool]] = {
    "TermsDateBasis": ("resolve_terms_date_basis", "TERMS DATE BASIS", False),
    "GlDateFromReceiptFlag": ("resolve_accounting_date_basis", "ACCOUNTING DATE BASIS", False),
    "PayDateBasisLookupCode": ("resolve_pay_date_basis", "DATE RANGE", False),
    "DiscountDistributionMethod": (
        "resolve_discount_distribution_method", "DISCOUNT_DIST_OPTIONS", True
    ),
    "ProrateIntInvAcrossDists": (
        "resolve_interest_proration_method", "INTEREST_ALLOCATION_OPTIONS", True
    ),
    "SsUpriceChangeForQtymatch": (
        "resolve_ss_unit_price_change", "UNITPRICE CHANGES QTY MATCH", True
    ),
    "AccountDefaultBasisCodeDes": (
        "resolve_account_derivation_method", "ACCOUNT DERIVATION METHOD", True
    ),
}

# These lookup types are system-owned and cannot be extended in Fusion.  Keep
# their exact supported codes in the task adapter so candidate validation is
# deterministic and does not depend on a REST privilege that an implementor
# may not have.  Customer-extensible and user-controlled lookup types remain
# receipt-based and are resolved by the live preflight helper.
SYSTEM_LOOKUP_CODES: dict[str, frozenset[str]] = {
    "ACCOUNTING DATE BASIS": frozenset({
        "INVOICE",
        "GOODS RECEIVED/CURRENT",
        "CURRENT",
        "GOODS RECEIVED/INVOICE",
    }),
    "DATE RANGE": frozenset({"DISCOUNT", "DUE"}),
    "DISCOUNT_DIST_OPTIONS": frozenset({"TAX", "EXPENSE", "SYSTEM"}),
    "INTEREST_ALLOCATION_OPTIONS": frozenset({"N", "Y"}),
    "TERMS DATE BASIS": frozenset({
        "Invoice Received",
        "Goods Received",
        "Current",
        "Invoice",
    }),
    "UNITPRICE CHANGES QTY MATCH": frozenset({
        "PRICE INCREASE ONLY",
        "PRICE INCREASE OR DECREASE",
        "NO",
        "PRICE DECREASE ONLY",
    }),
    "ACCOUNT DERIVATION METHOD": frozenset({
        "Transaction Account Builder",
    }),
}

CURRENCY_RECEIPT_CONTRACTS: dict[str, str] = {
    "InvoiceCurrencyCode": "resolve_invoice_currency",
    "PaymentCurrencyCode": "resolve_payment_currency",
}


def _canonical_currency_code(value: object) -> object:
    """Return the task-owned canonical spelling for a supplied currency code."""
    return value.strip().upper() if isinstance(value, str) else value

PAYMENT_TERM_RECEIPT_FIELDS = {
    "TermName",
    "PrepaymentTermName",
    "EmployeeTermName",
}

# A new AP system-options row must contain values for these non-null flags.
# The Payables System Option entity declares their create default as "N".
# Apply the defaults only to creates and only when the requester did not
# supply a value; updates continue to preserve the exported row unchanged.
CREATE_FLAG_DEFAULTS: dict[str, str] = {
    "DisallowAttachmentDelFlag": "N",
    "AttachmentMandatorySsFlag": "N",
    "ValidateBeforeApprovalFlag": "N",
    "AllowForceApprovalFlag": "N",
    "ApprovalWorkflowFlag": "N",
    "AutoCalculateInterestFlag": "N",
    "RecalcPayScheduleFlag": "N",
}

# UI-required date controls have source-proven entity initialization defaults.
# Apply them to creates only; updates retain the fresh exported baseline.
CREATE_UI_DEFAULTS: dict[str, str] = {
    "TermsDateBasis": "Invoice",
    "GlDateFromReceiptFlag": "INVOICE",
    "PayDateBasisLookupCode": "DISCOUNT",
    "BudgetDateBasis": "ACC",
}

# These UI-required controls have no safe task-owned default: their valid
# value is business-context dependent, so a create request must supply them.
CREATE_UI_REQUIRED_REQUEST_FIELDS = frozenset({
    "InvoiceCurrencyCode",
    "PaymentCurrencyCode",
    "PaymentPriority",
    "TermName",
    "WhenToAccountPmt",
})

# Page-backed fields with a closed Y/N package contract.  Do not infer this
# from a name ending in Flag; the set is limited to the UI controls confirmed
# in the task-owned input-validation resource.
UI_BOOLEAN_FIELDS = frozenset({
    "AlwaysTakeDiscFlag",
    "DiscIsInvLessTaxFlag",
    "AllowFinalMatchFlag",
    "AllowFlexOverrideFlag",
    "AllowPaidInvoiceAdjust",
    "InvDocCategoryOverride",
    "TransferDescFlexFlag",
    "ApprovalWorkflowFlag",
    "AllowForceApprovalFlag",
    "ValidateBeforeApprovalFlag",
    "BuildPrepaymentAccountsFlag",
    "ExcludeFreightFromDiscount",
    "AutoCalculateInterestFlag",
    "RequireInvoiceGroupFlag",
    "SsInvoiceBackdatingFlag",
    "SsLimitToSinglePoFlag",
    "PrepaymentAvailableMesgFlag",
    "RecalcPayScheduleFlag",
    "RouteInterfaceRejectionFlag",
    "AllowInvThirdPartyOvrd",
    "RoutingFlag",
    "AttachmentMandatorySsFlag",
    "DisallowAttachmentDelFlag",
    "ReleaseDupInvoiceHoldFlag",
})


def _nonnegative_integer(value: Any) -> int | None:
    try:
        result = int(str(value).strip())
    except (TypeError, ValueError):
        return None
    return result


def _validate_invoice_ui_values(
    entity: dict[str, Any], values: dict[str, Any], operation_id: str
) -> None:
    """Validate source-backed Invoice Options UI controls supplied by a row."""
    if entity["name"] != "AP_SYSTEM_PARAMETER":
        return
    for field in sorted(UI_BOOLEAN_FIELDS & set(values)):
        value = values[field]
        if not isinstance(value, str) or value.strip().upper() not in {"Y", "N"}:
            raise AdapterError(
                f"Operation {operation_id} field {entity['name']}.{field} must be Y or N "
                "for its Manage Invoice Options checkbox."
            )
    if "ReceiptAcceptanceDays" in values:
        number = _nonnegative_integer(values["ReceiptAcceptanceDays"])
        if number is None or number < 0:
            raise AdapterError(
                f"Operation {operation_id} field {entity['name']}.ReceiptAcceptanceDays "
                "must be a nonnegative integer."
            )
    if "AddDaysSettlementDate" in values:
        number = _nonnegative_integer(values["AddDaysSettlementDate"])
        if number is None or not 0 <= number <= 999:
            raise AdapterError(
                f"Operation {operation_id} field {entity['name']}.AddDaysSettlementDate "
                "must be an integer from 0 through 999."
            )
    if "InterestToleranceAmount" in values:
        try:
            tolerance = Decimal(str(values["InterestToleranceAmount"]).strip())
        except (InvalidOperation, ValueError):
            tolerance = Decimal("0")
        if not tolerance.is_finite() or tolerance <= 0:
            raise AdapterError(
                f"Operation {operation_id} field {entity['name']}.InterestToleranceAmount "
                "must be greater than 0."
            )
    _validate_invoice_ui_dependencies(values, operation_id)


def _validate_invoice_ui_dependencies(values: dict[str, Any], operation_id: str) -> None:
    """Validate cross-field Invoice Options rules on a proposed complete row."""
    if values.get("DiscIsInvLessTaxFlag") == "Y" and values.get("DiscountDistributionMethod") == "TAX":
        raise AdapterError(
            f"Operation {operation_id} cannot use DiscIsInvLessTaxFlag=Y with "
            "DiscountDistributionMethod=TAX."
        )
    if values.get("ApprovalWorkflowFlag") == "N":
        dependent = [
            field
            for field in ("AllowForceApprovalFlag", "ValidateBeforeApprovalFlag")
            if values.get(field) == "Y"
        ]
        if dependent:
            raise AdapterError(
                f"Operation {operation_id} requires ApprovalWorkflowFlag=Y when "
                f"{', '.join(dependent)} is Y."
            )
    approval_timing = values.get("ApprovalTiming")
    if approval_timing not in (None, ""):
        if not isinstance(approval_timing, str) or approval_timing.strip().upper() not in APPROVAL_TIMING_CODES:
            raise AdapterError(
                f"Operation {operation_id} field AP_SYSTEM_PARAMETER.ApprovalTiming "
                "must be A, N, or Y."
            )
        if (
            values.get("ApprovalWorkflowFlag") == "N"
            and approval_timing.strip().upper() in {"A", "Y"}
        ):
            raise AdapterError(
                f"Operation {operation_id} cannot set ApprovalTiming to "
                f"{approval_timing.strip().upper()} unless ApprovalWorkflowFlag=Y."
            )
    if values.get("AutoCalculateInterestFlag") == "Y":
        missing = [
            field
            for field in ("InterestToleranceAmount", "InterestSegments", "SOBName")
            if not str(values.get(field, "")).strip()
        ]
        if missing:
            raise AdapterError(
                f"Operation {operation_id} requires {missing} when "
                "AutoCalculateInterestFlag=Y."
            )
    # Fusion clears the interest account and tolerance when interest invoices
    # are disabled. Reject contradictory input rather than silently building
    # a candidate whose requested values will vanish during import.
    if values.get("AutoCalculateInterestFlag") == "N":
        incompatible = [
            field
            for field in ("InterestSegments", "InterestToleranceAmount")
            if str(values.get(field, "")).strip()
        ]
        if values.get("ProrateIntInvAcrossDists") == "Y":
            incompatible.append("ProrateIntInvAcrossDists=Y")
        if incompatible:
            raise AdapterError(
                f"Operation {operation_id} cannot supply {incompatible} when "
                "AutoCalculateInterestFlag=N."
            )

def _validate_lookup_receipt(
    blueprint: dict[str, Any],
    entity_name: str,
    field: str,
    requested_code: object,
    operation_id: str,
) -> None:
    """Require one exact, current receipt for a page-bound Payables lookup.

    The task adapter is deliberately offline. A live workflow obtains the
    lookup result, and this function verifies the normalized receipt before a
    candidate package can carry the requested code. If the read-only Financials
    lookup endpoint is unavailable to the caller, the live preflight emits one
    explicit advisory receipt; Fusion import remains authoritative in that case.
    """
    resolver, lookup_type, allow_blank = LOOKUP_RECEIPT_CONTRACTS[field]
    code = str(requested_code).strip()
    if allow_blank and not code:
        return
    allowed_codes = SYSTEM_LOOKUP_CODES.get(lookup_type)
    if allowed_codes is not None:
        if code not in allowed_codes:
            raise AdapterError(
                f"Operation {operation_id} {field} must use one of the supported "
                f"system {lookup_type} codes: {', '.join(sorted(allowed_codes))}."
            )
        return
    matches = [
        item
        for item in blueprint.get("prerequisites", [])
        if isinstance(item, dict)
        and item.get("entity") == entity_name
        and item.get("field") == field
        and item.get("resolver") == resolver
    ]
    if len(matches) != 1:
        raise AdapterError(
            f"Operation {operation_id} changes {field} and requires exactly one "
            f"{resolver} receipt."
        )
    prerequisite = matches[0]
    receipt = prerequisite.get("evidence")
    if not isinstance(receipt, dict):
        raise AdapterError(
            f"Operation {operation_id} {field} resolver evidence must be an object."
        )
    if receipt.get("lookupType") != lookup_type or receipt.get("lookupCode") != code:
        raise AdapterError(
            f"Operation {operation_id} {field} receipt must attest one exact, "
            f"{lookup_type} lookup code."
        )
    if prerequisite.get("status") == "validation_skipped":
        if (
            receipt.get("availability") == "unavailable"
            and receipt.get("preflightPolicy") == "advisory_on_unavailable"
        ):
            return
        raise AdapterError(
            f"Operation {operation_id} {field} skipped lookup validation must "
            "attest advisory unavailable access."
        )
    if prerequisite.get("status") != "satisfied":
        raise AdapterError(
            f"Operation {operation_id} {field} lookup receipt has unsupported "
            f"status {prerequisite.get('status')!r}."
        )
    if (
        not isinstance(receipt.get("resultCount"), int)
        or receipt["resultCount"] < 1
    ):
        raise AdapterError(
            f"Operation {operation_id} {field} receipt must attest at least one "
            "readable exact lookup match."
        )


def _validate_currency_receipt(
    blueprint: dict[str, Any],
    entity_name: str,
    field: str,
    requested_code: object,
    operation_id: str,
) -> None:
    """Require a corroborating `currenciesLOV` receipt."""
    resolver = CURRENCY_RECEIPT_CONTRACTS[field]
    code = str(requested_code).strip()
    matches = [
        item
        for item in blueprint.get("prerequisites", [])
        if isinstance(item, dict)
        and item.get("entity") == entity_name
        and item.get("field") == field
        and item.get("resolver") == resolver
    ]
    if len(matches) != 1:
        raise AdapterError(
            f"Operation {operation_id} changes {field} and requires exactly one "
            f"{resolver} receipt."
        )
    prerequisite = matches[0]
    receipt = prerequisite.get("evidence")
    if not isinstance(receipt, dict):
        raise AdapterError(
            f"Operation {operation_id} {field} resolver evidence must be an object."
        )
    if prerequisite.get("status") == "validation_skipped":
        if receipt.get("availability") in {"unavailable", "multiple_results"} and receipt.get("preflightPolicy") in {"advisory_on_unavailable", "advisory_on_multiple_results"}:
            return
        raise AdapterError(f"Operation {operation_id} {field} skipped currency validation must attest an advisory preflight outcome.")
    if prerequisite.get("status") != "satisfied":
        raise AdapterError(f"Operation {operation_id} {field} currency receipt has unsupported status {prerequisite.get('status')!r}.")
    if receipt.get("currencyCode") != code or not isinstance(receipt.get("resultCount"), int) or receipt["resultCount"] < 1:
        raise AdapterError(f"Operation {operation_id} {field} receipt must attest at least one currency record.")


def _validate_payment_term_receipt(
    blueprint: dict[str, Any],
    entity_name: str,
    field: str,
    requested_name: object,
    operation_id: str,
) -> None:
    """Require a corroborating `payablesPaymentTerms` preflight receipt."""
    matches = [
        item
        for item in blueprint.get("prerequisites", [])
        if isinstance(item, dict)
        and item.get("entity") == entity_name
        and item.get("field") == field
        and item.get("resolver") == "resolve_payment_term_from_name"
    ]
    if len(matches) != 1:
        raise AdapterError(
            f"Operation {operation_id} changes {field} and requires exactly one "
            "resolve_payment_term_from_name receipt."
        )
    prerequisite = matches[0]
    receipt = prerequisite.get("evidence")
    if not isinstance(receipt, dict):
        raise AdapterError(
            f"Operation {operation_id} {field} resolver evidence must be an object."
        )
    name = str(requested_name).strip()
    if prerequisite.get("status") == "validation_skipped":
        if receipt.get("name") == name and receipt.get("availability") in {"unavailable", "multiple_results"} and receipt.get("preflightPolicy") in {"advisory_on_unavailable", "advisory_on_multiple_results"}:
            return
        raise AdapterError(f"Operation {operation_id} {field} skipped payment-term validation must attest an advisory preflight outcome.")
    if prerequisite.get("status") != "satisfied":
        raise AdapterError(f"Operation {operation_id} {field} payment-term receipt has unsupported status {prerequisite.get('status')!r}.")
    if receipt.get("name") != name or not isinstance(receipt.get("resultCount"), int) or receipt["resultCount"] < 1:
        raise AdapterError(
            f"Operation {operation_id} {field} receipt must attest at least one returned payment-term record."
        )


def _validate_create_ui_required_fields(
    values: dict[str, Any], operation_id: str,
) -> None:
    """Block incomplete UI-equivalent creates before package generation."""
    missing = sorted(
        field for field in CREATE_UI_REQUIRED_REQUEST_FIELDS
        if not str(values.get(field, "")).strip()
    )
    if missing:
        raise AdapterError(
            f"Operation {operation_id} create is missing UI-required fields: {missing}."
        )


def _normalized_blueprint(
    contract: dict[str, Any], design: dict[str, Any]
) -> dict[str, Any]:
    if not isinstance(design, dict):
        raise AdapterError("Normalized design input must be a JSON object.")
    operations = design.get("operations")
    if not isinstance(operations, list) or not operations:
        raise AdapterError("Design must contain at least one operation.")
    normalized_ops = []
    for index, raw in enumerate(operations, start=1):
        if not isinstance(raw, dict):
            raise AdapterError(f"Operation {index} must be an object.")
        operation = dict(raw)
        operation.setdefault("id", f"OP-{index:03d}")
        operation.setdefault("action", "update")
        operation.setdefault("preserveOtherValues", True)
        operation.setdefault("preserveUnspecifiedRows", True)
        if operation["action"] == "create":
            values = operation.get("values")
            if isinstance(values, dict):
                operation["values"] = {
                    **CREATE_FLAG_DEFAULTS,
                    **CREATE_UI_DEFAULTS,
                    **values,
                }
        values = operation.get("values")
        if isinstance(values, dict):
            operation["values"] = {
                field: (_canonical_currency_code(value)
                        if field in CURRENCY_RECEIPT_CONTRACTS else value)
                for field, value in values.items()
            }
        normalized_ops.append(operation)
    blueprint = {
        "task": {
            "name": contract["task"]["name"],
            "code": contract["task"]["code"],
        },
        "operations": normalized_ops,
        "resolvedScope": design.get("resolvedScope", {}),
        "enterpriseIdResolution": {},
        "explicitDefaults": design.get("explicitDefaults", []),
        "preservedValues": design.get("preservedValues", []),
        "prerequisites": design.get("prerequisites", []),
        "warnings": design.get("warnings", []),
    }
    return blueprint


def _business_unit_preflight_entry(
    blueprint: dict[str, Any],
    entity: dict[str, Any],
    target: dict[str, Any],
    operation_id: str,
) -> dict[str, Any]:
    """Return the one persisted, exact-match BU preflight result for a create."""
    scope = blueprint.get("resolvedScope")
    entries = scope.get("businessUnits") if isinstance(scope, dict) else None
    if not isinstance(entries, list):
        raise AdapterError(
            f"Operation {operation_id} creates {entity['name']} and requires one "
            "resolvedScope.businessUnits preflight result for its BuName."
        )
    matches = [
        item
        for item in entries
        if isinstance(item, dict)
        and item.get("entity") == entity["name"]
        and item.get("targetKey") == target
    ]
    if len(matches) != 1:
        raise AdapterError(
            f"Operation {operation_id} requires exactly one matching business-unit "
            "preflight result; zero or multiple matches are unsafe."
        )
    return matches[0]


# Local EnterpriseId portion of `resolve_business_unit_by_name_and_enterprise`.
# It combines an explicit row value, a run-level default, or one unambiguous
# value from the fresh baseline; it does not perform a BU-to-enterprise lookup.
def _create_enterprise_resolution(
    contract: dict[str, Any],
    blueprint: dict[str, Any],
    baseline: PackageData | None,
) -> dict[str, Any]:
    """Resolve EnterpriseId for create rows without CRM or BU-to-enterprise calls.

    The resolution deliberately has a narrow precedence: an explicit create-row
    value wins for that row; the first explicit value becomes the current-run
    default; and a fresh FSM baseline supplies a default only when it contains
    exactly one nonblank EnterpriseId.  A later conflicting explicit value is
    valid for its own row but makes subsequent blank create rows ambiguous.
    """
    entities = _entity_map(contract)
    baseline_ids: set[str] = set()
    if baseline is not None:
        for entity in entities.values():
            if "EnterpriseId" not in entity["headers"]:
                continue
            baseline_ids.update(
                str(row.get("EnterpriseId", "")).strip()
                for row in baseline.rows.get(entity["name"], [])
                if str(row.get("EnterpriseId", "")).strip()
            )

    default = next(iter(baseline_ids)) if len(baseline_ids) == 1 else None
    default_source = "baseline" if default is not None else None
    ambiguous = False
    operation_values: dict[str, str] = {}
    operation_sources: dict[str, str] = {}

    for operation in blueprint["operations"]:
        entity = entities[operation["entity"]]
        if operation["action"] != "create" or "EnterpriseId" not in entity["headers"]:
            continue
        operation_id = operation["id"]
        supplied = operation["values"].get("EnterpriseId")
        if supplied is not None:
            value = str(supplied).strip()
            if not value:
                raise AdapterError(
                    f"Operation {operation_id} supplies a blank EnterpriseId."
                )
            _validate_field_value(entity, "EnterpriseId", value, operation_id)
            operation_values[operation_id] = value
            operation_sources[operation_id] = "requester"
            if default is None and not ambiguous:
                default = value
                default_source = "requester"
            elif default is not None and value != default:
                # The explicit row remains valid; only a later omitted value is
                # unsafe because there is no longer one unambiguous run default.
                default = None
                default_source = None
                ambiguous = True
            continue
        if default is None:
            reason = (
                "a prior create supplied a different EnterpriseId"
                if ambiguous
                else "the fresh FSM export has no single nonblank EnterpriseId"
            )
            raise AdapterError(
                f"Operation {operation_id} omits EnterpriseId and {reason}. "
                "Ask the requester which EnterpriseId to use for this and later blank create rows."
            )
        operation_values[operation_id] = default
        operation_sources[operation_id] = f"current-run-default:{default_source}"

    return {
        "baselineDistinctEnterpriseIds": sorted(baseline_ids),
        "currentRunDefaultEnterpriseId": default,
        "state": "ambiguous" if ambiguous else "resolved",
        "operations": [
            {
                "operationId": operation_id,
                "enterpriseId": operation_values[operation_id],
                "source": operation_sources[operation_id],
            }
            for operation_id in sorted(operation_values)
        ],
    }


def _resolved_enterprise_id(
    contract: dict[str, Any],
    blueprint: dict[str, Any],
    baseline: PackageData | None,
    operation_id: str,
) -> str:
    """Return the persisted deterministic EnterpriseId for one create operation."""
    resolution = _create_enterprise_resolution(contract, blueprint, baseline)
    matches = [item for item in resolution["operations"] if item["operationId"] == operation_id]
    if len(matches) != 1:
        raise AdapterError(f"Operation {operation_id} has no resolved EnterpriseId.")
    return matches[0]["enterpriseId"]


def _resolved_sob_name(
    blueprint: dict[str, Any],
    entity: dict[str, Any],
    target: dict[str, Any],
    operation_id: str,
) -> str:
    """Resolve the primary-ledger name for a new BU without guessing it.

    The live preflight calls finBusinessUnitsLOV by exact BuName and then
    ledgersLOV by the returned PrimaryLedgerId. This offline adapter verifies
    the normalized two-stage evidence and injects the returned ledger name.
    """
    entry = _business_unit_preflight_entry(blueprint, entity, target, operation_id)
    resolved = entry.get("resolvedValues")
    evidence = entry.get("evidence")
    sob_name = resolved.get("SOBName") if isinstance(resolved, dict) else None
    if not isinstance(sob_name, str) or not sob_name.strip():
        raise AdapterError(
            f"Operation {operation_id} business-unit preflight result lacks SOBName."
        )
    if not isinstance(evidence, dict):
        raise AdapterError(
            f"Operation {operation_id} business-unit preflight must retain evidence."
        )
    business_unit = evidence.get("finBusinessUnitsLOV")
    ledger = evidence.get("ledgersLOV")
    if not isinstance(business_unit, dict) or not isinstance(ledger, dict):
        raise AdapterError(
            f"Operation {operation_id} business-unit preflight requires both "
            "finBusinessUnitsLOV and ledgersLOV receipts."
        )
    primary_ledger_id = business_unit.get("primaryLedgerId")
    if (
        business_unit.get("source") != "finBusinessUnitsLOV"
        or not isinstance(business_unit.get("resultCount"), int)
        or business_unit["resultCount"] < 1
        or business_unit.get("matchedBuName") != target.get("BuName")
        or not str(primary_ledger_id or "").strip()
        or ledger.get("source") != "ledgersLOV"
        or str(ledger.get("ledgerId")) != str(primary_ledger_id)
        or ledger.get("name") != sob_name
    ):
        raise AdapterError(
            f"Operation {operation_id} BU-to-ledger receipts must attest the exact "
            "BuName, its PrimaryLedgerId, and the returned ledger Name."
        )
    return sob_name.strip()


def _resolved_base_currency_code(
    blueprint: dict[str, Any],
    entity: dict[str, Any],
    target: dict[str, Any],
    operation_id: str,
) -> str:
    """Return the exact primary-ledger currency for a new BU.

    The primary-ledger receipt is the source of truth used to validate a
    supplied BaseCurrencyCode or to provide one when the requester omitted it.
    """
    entry = _business_unit_preflight_entry(blueprint, entity, target, operation_id)
    resolved = entry.get("resolvedValues")
    evidence = entry.get("evidence")
    currency = resolved.get("BaseCurrencyCode") if isinstance(resolved, dict) else None
    if not isinstance(currency, str) or not currency.strip():
        raise AdapterError(
            f"Operation {operation_id} business-unit preflight result lacks BaseCurrencyCode."
        )
    if not isinstance(evidence, dict):
        raise AdapterError(
            f"Operation {operation_id} business-unit preflight must retain evidence."
        )
    business_unit = evidence.get("finBusinessUnitsLOV")
    ledger = evidence.get("ledgersLOV")
    primary_ledger_id = business_unit.get("primaryLedgerId") if isinstance(business_unit, dict) else None
    if (
        not isinstance(business_unit, dict)
        or not isinstance(ledger, dict)
        or business_unit.get("source") != "finBusinessUnitsLOV"
        or business_unit.get("matchedBuName") != target.get("BuName")
        or str(ledger.get("ledgerId")) != str(primary_ledger_id)
        or ledger.get("source") != "ledgersLOV"
        or ledger.get("currencyCode") != currency.strip()
    ):
        raise AdapterError(
            f"Operation {operation_id} BU-to-ledger receipt must attest the exact "
            "PrimaryLedgerId and returned CurrencyCode."
        )
    return currency.strip()


def _validate_blueprint_failfast(
    contract: dict[str, Any],
    blueprint: dict[str, Any],
    baseline: PackageData | None = None,
) -> None:
    task = blueprint.get("task")
    if task != {"name": contract["task"]["name"], "code": contract["task"]["code"]}:
        raise AdapterError("Blueprint task identity differs from the adapter contract.")
    operations = blueprint.get("operations")
    if not isinstance(operations, list) or not operations:
        raise AdapterError("Blueprint must contain at least one operation.")
    entities = _entity_map(contract)
    allowed = set(contract["normalization"]["supportedOperations"])
    satisfied = _satisfied_prerequisites(blueprint, contract)
    seen_ids: set[str] = set()
    seen_targets: set[tuple[str, tuple[str, ...]]] = set()
    for position, operation in enumerate(operations, start=1):
        if not isinstance(operation, dict):
            raise AdapterError(f"Operation {position} must be an object.")
        operation_id = operation.get("id")
        if not isinstance(operation_id, str) or not operation_id:
            raise AdapterError(f"Operation {position} has no stable id.")
        if operation_id in seen_ids:
            raise AdapterError(f"Duplicate operation id {operation_id!r}.")
        seen_ids.add(operation_id)
        action = operation.get("action")
        if action not in allowed:
            raise AdapterError(f"Operation {operation_id} uses unsupported action {action!r}.")
        entity_name = operation.get("entity")
        if entity_name not in entities:
            raise AdapterError(f"Operation {operation_id} names unknown entity {entity_name!r}.")
        entity = entities[entity_name]
        blocked = {
            item["field"]: item
            for item in entity.get("conditionallyBlockedFields", [])
        }
        target = operation.get("targetKey")
        if not isinstance(target, dict) or set(target) != set(entity["keyFields"]):
            raise AdapterError(
                f"Operation {operation_id} targetKey must contain exactly "
                f"{entity['keyFields']}."
            )
        for field in entity["keyFields"]:
            _validate_field_value(entity, field, target[field], operation_id)
            if (
                action == "create"
                and field in blocked
                and (entity_name, field, blocked[field]["resolver"]) not in satisfied
            ):
                raise AdapterError(
                    f"Operation {operation_id} creates conditionally blocked key field "
                    f"{entity_name}.{field}: {blocked[field]['reason']}"
                )
        target_tuple = _target_tuple(entity, target)
        if any(value == "" for value in target_tuple):
            raise AdapterError(f"Operation {operation_id} has a blank target key.")
        target_identity = (entity_name, target_tuple)
        if target_identity in seen_targets:
            raise AdapterError(
                f"More than one operation targets {entity_name} {target_tuple!r}."
            )
        seen_targets.add(target_identity)
        values = operation.get("values")
        if not isinstance(values, dict) or not values:
            raise AdapterError(f"Operation {operation_id} must supply values.")
        prohibited = set(entity["keyFields"]) | set(entity["auditFields"])
        unknown = set(values) - set(entity["headers"])
        if unknown:
            raise AdapterError(
                f"Operation {operation_id} supplies unknown fields: {sorted(unknown)}."
            )
        invalid = set(values) & prohibited
        if invalid:
            raise AdapterError(
                f"Operation {operation_id} cannot change key/audit fields: {sorted(invalid)}."
            )
        field_contract = entity.get(
            "createFields" if action == "create" else "updateFields", {}
        )
        if isinstance(field_contract, dict):
            unsupported = set(values) - set(field_contract)
            if unsupported:
                raise AdapterError(
                    f"Operation {operation_id} supplies fields outside the "
                    f"source-backed {action} contract: {sorted(unsupported)}."
                )
        if action == "create":
            _validate_create_ui_required_fields(values, operation_id)
        # EnterpriseId is required by the FSM create row.  It can be supplied
        # explicitly by the requester, inherited from the current-run default,
        # or defaulted only from one distinct nonblank value in the baseline.
        # Updates retain the value already present in the fresh export.
        if action == "create" and "EnterpriseId" in entity["headers"]:
            if "EnterpriseId" in values:
                _validate_field_value(entity, "EnterpriseId", values["EnterpriseId"], operation_id)
        elif action == "update" and "EnterpriseId" in values:
            raise AdapterError(
                f"Operation {operation_id} must retain EnterpriseId from the uniquely "
                "matched exported row; it cannot be changed in an update."
            )
        if action == "create" and "SOBName" in entity["headers"]:
            if "SOBName" in values:
                raise AdapterError(
                    f"Operation {operation_id} must not supply SOBName; "
                    "resolve it from the exact business-unit primary-ledger result."
                )
            sob_name = _resolved_sob_name(blueprint, entity, target, operation_id)
            _validate_field_value(entity, "SOBName", sob_name, operation_id)
        if action == "create" and "BaseCurrencyCode" in entity["headers"]:
            derived_base_currency = _resolved_base_currency_code(
                blueprint, entity, target, operation_id
            )
            supplied_base_currency = values.get("BaseCurrencyCode")
            if supplied_base_currency is not None and str(supplied_base_currency).strip() != derived_base_currency:
                raise AdapterError(
                    f"Operation {operation_id} supplies BaseCurrencyCode "
                    f"{str(supplied_base_currency).strip()!r}, but the target BU's "
                    f"primary ledger resolves to {derived_base_currency!r}."
                )
            _validate_field_value(
                entity,
                "BaseCurrencyCode",
                supplied_base_currency if supplied_base_currency is not None else derived_base_currency,
                operation_id,
            )
        _validate_payment_owned_values(entity, action, values, operation_id)
        for field in values:
            if (
                field in PAYMENT_TERM_RECEIPT_FIELDS
                and blocked.get(field, {}).get("resolver")
                == "resolve_payment_term_from_name"
            ):
                _validate_payment_term_receipt(
                    blueprint, entity_name, field, values[field], operation_id
                )
                _validate_field_value(entity, field, values[field], operation_id)
                continue
            if (
                field in LOOKUP_RECEIPT_CONTRACTS
                and blocked.get(field, {}).get("resolver")
                == LOOKUP_RECEIPT_CONTRACTS[field][0]
            ):
                _validate_lookup_receipt(
                    blueprint, entity_name, field, values[field], operation_id
                )
                _validate_field_value(entity, field, values[field], operation_id)
                continue
            if (
                field in CURRENCY_RECEIPT_CONTRACTS
                and blocked.get(field, {}).get("resolver")
                == CURRENCY_RECEIPT_CONTRACTS[field]
            ):
                _validate_currency_receipt(
                    blueprint, entity_name, field, values[field], operation_id
                )
                _validate_field_value(entity, field, values[field], operation_id)
                continue
            if field in blocked and (
                entity_name, field, blocked[field]["resolver"]
            ) not in satisfied:
                raise AdapterError(
                    f"Operation {operation_id} changes conditionally blocked field "
                    f"{entity_name}.{field}: {blocked[field]['reason']}"
                )
            _validate_field_value(entity, field, values[field], operation_id)
        _validate_invoice_ui_values(entity, values, operation_id)
        if baseline is not None:
            matches = _row_index(baseline, entity)
            if action == "update" and target_tuple not in matches:
                raise AdapterError(
                    f"Operation {operation_id} target {target_tuple!r} does not exist "
                    "exactly once in the fresh current export."
                )
            if action == "create" and target_tuple in matches:
                raise AdapterError(
                    f"Operation {operation_id} create target {target_tuple!r} already "
                    "exists in the fresh current export."
                )
            if action == "update":
                # Validate the complete resulting shared row, not merely the
                # field delta.  This catches a Payment-owned value that was
                # already present in the exact baseline or is supplied beside
                # an Invoice-owned change.
                resulting_row = dict(matches[target_tuple])
                resulting_row.update(values)
                _validate_invoice_ui_dependencies(resulting_row, operation_id)
                _validate_payment_owned_values(
                    entity, action, resulting_row, operation_id
                )
    # Resolve all creates together because an explicit EnterpriseId on one row
    # establishes (or conflicts with) the current-run default for later rows.
    resolution = _create_enterprise_resolution(contract, blueprint, baseline)
    persisted = blueprint.get("enterpriseIdResolution")
    if persisted is not None and persisted not in ({}, resolution):
        raise AdapterError(
            "EnterpriseId resolution in the blueprint differs from the deterministic "
            "current baseline and create operations. Re-normalize the design."
        )


def _validate_blueprint(
    contract: dict[str, Any],
    blueprint: dict[str, Any],
    baseline: PackageData | None = None,
) -> None:
    """Collect independent operation errors, then retain fail-safe batch rejection.

    Package and task identity errors remain immediately blocking.  For a valid
    batch envelope, each operation is first validated in isolation so a caller
    can correct all independent row errors in one pass.  No candidate is
    generated while any collected error exists.
    """
    operations = blueprint.get("operations") if isinstance(blueprint, dict) else None
    if not isinstance(operations, list) or not operations:
        _validate_blueprint_failfast(contract, blueprint, baseline)
        return
    errors: list[str] = []
    for position, operation in enumerate(operations, start=1):
        isolated = dict(blueprint)
        isolated["operations"] = [operation]
        isolated["enterpriseIdResolution"] = {}
        try:
            _validate_blueprint_failfast(contract, isolated, baseline)
        except AdapterError as exc:
            error = str(exc)
            if error not in errors:
                errors.append(error)
    if errors:
        raise BatchValidationError(errors)
    # Once every operation is individually valid, retain the existing
    # cross-row checks (duplicate targets, EnterpriseId precedence, etc.).
    _validate_blueprint_failfast(contract, blueprint, baseline)


def _requirements(
    contract: dict[str, Any], blueprint: dict[str, Any]
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    number = 1
    for operation in blueprint["operations"]:
        target_key_text = json.dumps(
            operation["targetKey"],
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        base = {
            "operationId": operation["id"],
            "entity": operation["entity"],
            "targetKey": operation["targetKey"],
        }
        result.append(
            {
                "id": f"REQ-{number:03d}",
                "kind": "target",
                "requirement": (
                    f"{operation['action']} exactly one {operation['entity']} record "
                    f"identified by {target_key_text}"
                ),
                **base,
            }
        )
        number += 1
        for field in sorted(operation["values"]):
            value = str(operation["values"][field])
            result.append(
                {
                    "id": f"REQ-{number:03d}",
                    "kind": "value",
                    "requirement": f"Persist {operation['entity']}.{field}={value}",
                    "field": field,
                    "requestedValue": value,
                    **base,
                }
            )
            number += 1
        # A create has no pre-existing target row whose values can be preserved.
        # Unspecified fields are governed by the explicit create values and the
        # package schema; only updates need a target-level preservation check.
        if (
            operation["action"] == "update"
            and operation.get("preserveOtherValues", True)
        ):
            result.append(
                {
                    "id": f"REQ-{number:03d}",
                    "kind": "preserve_target",
                    "requirement": "Preserve every other non-audit value on the target record",
                    **base,
                }
            )
            number += 1
        if operation.get("preserveUnspecifiedRows", True):
            result.append(
                {
                    "id": f"REQ-{number:03d}",
                    "kind": "preserve_rows",
                    "requirement": "Preserve every unspecified record and non-audit value",
                    **base,
                }
            )
            number += 1
    return result


def _requirement_contract(
    contract: dict[str, Any], blueprint: dict[str, Any], requirements: list[Any]
) -> list[dict[str, Any]]:
    expected = _requirements(contract, blueprint)
    if requirements != expected:
        raise AdapterError(
            "Requirements JSON is stale or differs from the deterministic blueprint requirements."
        )
    return expected


def normalize_design(
    contract: dict[str, Any],
    baseline_path: Path,
    request_path: Path,
    design_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    baseline = _read_package(baseline_path, contract)
    design = _read_json(design_path)
    blueprint = _normalized_blueprint(contract, design)
    _validate_blueprint(contract, blueprint, baseline)
    blueprint["enterpriseIdResolution"] = _create_enterprise_resolution(
        contract, blueprint, baseline
    )
    requirements = _requirements(contract, blueprint)
    design_sha = _sha256_bytes(_canonical_bytes(blueprint))
    preview = {
        "schemaVersion": SCHEMA_VERSION,
        "task": blueprint["task"],
        "requestSha256": _sha256_path(request_path),
        "designSha256": design_sha,
        "baselineSha256": baseline.archive_sha256,
        "operations": [
            {
                "id": operation["id"],
                "action": operation["action"],
                "entity": operation["entity"],
                "targetKey": operation["targetKey"],
                "requestedValues": operation["values"],
                "preserveOtherValues": operation.get("preserveOtherValues", True),
                "preserveUnspecifiedRows": operation.get("preserveUnspecifiedRows", True),
            }
            for operation in blueprint["operations"]
        ],
        "explicitDefaults": blueprint["explicitDefaults"],
        "prerequisites": blueprint["prerequisites"],
        "warnings": blueprint["warnings"],
        "requirementCount": len(requirements),
    }
    return blueprint, preview, requirements


def _candidate_rows(
    contract: dict[str, Any],
    baseline: PackageData,
    blueprint: dict[str, Any],
) -> dict[str, list[dict[str, str]]]:
    entities = _entity_map(contract)
    output: dict[str, list[dict[str, str]]] = {name: [] for name in entities}
    for operation in blueprint["operations"]:
        entity = entities[operation["entity"]]
        key = _target_tuple(entity, operation["targetKey"])
        if operation["action"] == "update":
            row = dict(_row_index(baseline, entity)[key])
        elif operation["action"] == "create":
            row = {header: "" for header in entity["headers"]}
            row.update({field: str(value) for field, value in operation["targetKey"].items()})
            if "EnterpriseId" in entity["headers"]:
                row["EnterpriseId"] = _resolved_enterprise_id(
                    contract, blueprint, baseline, operation["id"]
                )
            if "SOBName" in entity["headers"]:
                row["SOBName"] = _resolved_sob_name(
                    blueprint, entity, operation["targetKey"], operation["id"]
                )
            if "BaseCurrencyCode" in entity["headers"]:
                supplied_base_currency = operation["values"].get("BaseCurrencyCode")
                row["BaseCurrencyCode"] = (
                    str(supplied_base_currency)
                    if supplied_base_currency is not None
                    else _resolved_base_currency_code(
                        blueprint, entity, operation["targetKey"], operation["id"]
                    )
                )
        else:
            raise AdapterError(f"Unsupported action {operation['action']!r}.")
        row.update({field: str(value) for field, value in operation["values"].items()})
        for field in entity["auditFields"]:
            row[field] = ""
        output[entity["name"]].append(row)
    for entity_name, rows in output.items():
        entity = entities[entity_name]
        rows.sort(key=lambda row: _row_key(entity, row))
    return output


def _write_candidate(
    template: PackageData,
    baseline: PackageData,
    contract: dict[str, Any],
    rows: dict[str, list[dict[str, str]]],
    output_path: Path,
) -> None:
    entity_by_member = {
        entity["member"]: entity for entity in contract["package"]["entities"]
    }
    metadata_member = contract["package"]["metadataMember"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w") as archive:
        for member in template.member_names:
            if member in entity_by_member:
                entity = entity_by_member[member]
                content = _csv_bytes(entity["headers"], rows[entity["name"]])
                member_info = template.member_infos[member]
            elif member == metadata_member:
                content = baseline.member_bytes[member]
                member_info = baseline.member_infos[member]
            else:
                content = template.member_bytes[member]
                member_info = template.member_infos[member]
            archive.writestr(member_info, content)


def _semantic_issues(
    contract: dict[str, Any],
    candidate: PackageData,
    baseline: PackageData,
    blueprint: dict[str, Any],
    requirements: list[dict[str, Any]],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    entities = _entity_map(contract)
    expected_targets: set[tuple[str, tuple[str, ...]]] = set()
    for operation in blueprint["operations"]:
        entity = entities[operation["entity"]]
        key = _target_tuple(entity, operation["targetKey"])
        expected_targets.add((entity["name"], key))
        candidate_rows = _row_index(candidate, entity)
        baseline_rows = _row_index(baseline, entity)
        row = candidate_rows.get(key)
        if row is None:
            issues.append(
                {"code": "MISSING_TARGET", "message": f"Candidate lacks {entity['name']} {key!r}."}
            )
            continue
        before = baseline_rows.get(key, {header: "" for header in entity["headers"]})
        for field, value in operation["values"].items():
            if row[field] != str(value):
                issues.append(
                    {"code": "VALUE_MISMATCH", "message": f"{entity['name']} {key!r} {field} is {row[field]!r}, expected {str(value)!r}."}
                )
        if operation.get("preserveOtherValues", True) and operation["action"] == "update":
            allowed = set(operation["values"]) | set(entity["auditFields"])
            for field in entity["headers"]:
                if field not in allowed and row[field] != before[field]:
                    issues.append(
                        {"code": "UNEXPECTED_CHANGE", "message": f"{entity['name']} {key!r} changed preserved field {field}."}
                    )
        for field in entity["auditFields"]:
            if row[field] != "":
                issues.append(
                    {"code": "AUDIT_FIELD_POPULATED", "message": f"{entity['name']} {key!r} audit field {field} is not blank."}
                )
    for entity in contract["package"]["entities"]:
        for row in candidate.rows[entity["name"]]:
            identity = (entity["name"], _row_key(entity, row))
            if identity not in expected_targets:
                issues.append(
                    {"code": "UNEXPECTED_ROW", "message": f"Candidate contains unrequested {entity['name']} row {identity[1]!r}."}
                )
    if {item["id"] for item in requirements} != {
        item["id"] for item in _requirements(contract, blueprint)
    }:
        issues.append(
            {"code": "REQUIREMENT_COVERAGE", "message": "Requirement IDs do not cover the normalized blueprint."}
        )
    return issues


def validate_candidate(
    contract: dict[str, Any],
    template_path: Path,
    baseline_path: Path,
    blueprint_path: Path,
    requirements_path: Path,
    candidate_path: Path,
) -> dict[str, Any]:
    template = _read_package(template_path, contract)
    baseline = _read_package(baseline_path, contract)
    candidate = _read_package(candidate_path, contract)
    _validate_source_pair(contract, template, baseline)
    blueprint = _read_json(blueprint_path)
    requirements = _read_json(requirements_path)
    _validate_blueprint(contract, blueprint, baseline)
    if not isinstance(requirements, list):
        raise AdapterError("Requirements file must contain a JSON array.")
    _requirement_contract(contract, blueprint, requirements)
    expected_fingerprint = contract["package"]["schemaFingerprint"]
    fingerprints = {
        "template": _schema_fingerprint(contract, template),
        "baseline": _schema_fingerprint(contract, baseline),
        "candidate": _schema_fingerprint(contract, candidate),
    }
    issues = _semantic_issues(contract, candidate, baseline, blueprint, requirements)
    metadata_member = contract["package"]["metadataMember"]
    if candidate.member_bytes[metadata_member] != baseline.member_bytes[metadata_member]:
        issues.append(
            {
                "code": "METADATA_PROVENANCE",
                "message": (
                    f"{metadata_member} must be preserved byte-for-byte from the fresh "
                    "current-data baseline, not the template-only export."
                ),
            }
        )
    for label, fingerprint in fingerprints.items():
        if fingerprint != expected_fingerprint:
            issues.append(
                {"code": "SCHEMA_FINGERPRINT", "message": f"{label} schema fingerprint {fingerprint} differs from {expected_fingerprint}."}
            )
    return {
        "schemaVersion": SCHEMA_VERSION,
        "status": "PASS" if not issues else "FAIL",
        "task": contract["task"],
        "candidateSha256": candidate.archive_sha256,
        "templateSha256": template.archive_sha256,
        "baselineSha256": baseline.archive_sha256,
        "designSha256": _sha256_bytes(_canonical_bytes(blueprint)),
        "schemaFingerprint": expected_fingerprint,
        "memberInventory": candidate.member_names,
        "rowCounts": {
            entity["member"]: len(candidate.rows[entity["name"]])
            for entity in contract["package"]["entities"]
        },
        "requirementIds": [item["id"] for item in requirements],
        "errors": issues,
        "warnings": blueprint.get("warnings", []),
        "unresolvedWarnings": blueprint.get("warnings", []),
    }


def validate_uploaded_package(
    contract: dict[str, Any], baseline_path: Path, package_path: Path,
) -> dict[str, Any]:
    """Validate a user-uploaded exact-task FSM ZIP without importing it.

    Existing baseline keys are interpreted as updates; absent keys as creates.
    The uploaded row supplies only nonblank values.  Every row is evaluated and
    a batch with any blocking error is rejected as a whole.
    """
    baseline = _read_package(baseline_path, contract)
    uploaded = _read_package(package_path, contract)
    expected_fingerprint = _schema_fingerprint(contract, baseline)
    upload_fingerprint = _schema_fingerprint(contract, uploaded)
    if upload_fingerprint != expected_fingerprint:
        raise AdapterError(
            f"Uploaded package schema fingerprint {upload_fingerprint} differs from "
            f"the fresh baseline {expected_fingerprint}."
        )
    entities = _entity_map(contract)
    operations: list[dict[str, Any]] = []
    row_descriptions: list[dict[str, Any]] = []
    raw_row_errors: dict[str, list[str]] = {}
    for entity in contract["package"]["entities"]:
        baseline_rows = _row_index(baseline, entity)
        uploaded_keys: dict[tuple[str, ...], list[tuple[int, str]]] = {}
        for row_number, row in enumerate(uploaded.rows[entity["name"]], start=1):
            target = {field: row[field] for field in entity["keyFields"]}
            key = _target_tuple(entity, target)
            action = "update" if key in baseline_rows else "create"
            if action == "update":
                values = {
                    field: row[field]
                    for field in entity["headers"]
                    if field not in set(entity["keyFields"]) | set(entity["auditFields"])
                    and row[field] != ""
                    and row[field] != baseline_rows[key][field]
                }
            else:
                values = {
                    field: row[field]
                    for field in entity["headers"]
                    if field not in set(entity["keyFields"]) | set(entity["auditFields"])
                    and row[field] != ""
                }
            operation_id = f"UPLOAD-{entity['name']}-{row_number:03d}"
            uploaded_keys.setdefault(key, []).append((row_number, operation_id))
            populated_audits = [
                field for field in entity["auditFields"] if row.get(field, "").strip()
            ]
            if populated_audits:
                raw_row_errors.setdefault(operation_id, []).append(
                    f"Operation {operation_id} uploaded row must leave audit fields blank: "
                    f"{populated_audits}."
                )
            operations.append({
                "id": operation_id,
                "action": action,
                "entity": entity["name"],
                "targetKey": target,
                "values": values,
                "preserveOtherValues": True,
                "preserveUnspecifiedRows": True,
            })
            row_descriptions.append({
                "row": row_number,
                "operationId": operation_id,
                "entity": entity["name"],
                "action": action,
                "targetKey": target,
            })
        for key, occurrences in uploaded_keys.items():
            if len(occurrences) > 1:
                rows = [number for number, _ in occurrences]
                for _, operation_id in occurrences:
                    raw_row_errors.setdefault(operation_id, []).append(
                        f"Operation {operation_id} uploaded row has duplicate target key "
                        f"{key!r} in AP_SYSTEM_PARAMETER rows {rows}."
                    )
    if not operations:
        raise AdapterError("Uploaded package contains no task rows to validate.")
    blueprint = _normalized_blueprint(contract, {
        "operations": operations,
        "resolvedScope": {},
        "prerequisites": [],
        "warnings": [],
    })
    errors: list[str] = [
        error for operation_errors in raw_row_errors.values() for error in operation_errors
    ]
    try:
        _validate_blueprint(contract, blueprint, baseline)
    except BatchValidationError as exc:
        errors.extend(exc.errors)
    except AdapterError as exc:
        errors.append(str(exc))
    for item in row_descriptions:
        item["errors"] = [
            error for error in errors if item["operationId"] in error
        ]
        item["status"] = "FAIL" if item["errors"] else "PASS"
    return {
        "schemaVersion": SCHEMA_VERSION,
        "status": "PASS" if not errors else "FAIL",
        "task": contract["task"],
        "uploadedPackageSha256": uploaded.archive_sha256,
        "baselineSha256": baseline.archive_sha256,
        "notImported": True,
        "candidateCreated": False,
        "rowResults": row_descriptions,
        "errors": errors,
    }


def build_candidate(
    contract: dict[str, Any],
    template_path: Path,
    baseline_path: Path,
    blueprint_path: Path,
    requirements_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    _validate_new_outputs(
        [output_path],
        [template_path, baseline_path, blueprint_path, requirements_path],
    )
    template = _read_package(template_path, contract)
    baseline = _read_package(baseline_path, contract)
    _validate_source_pair(contract, template, baseline)
    blueprint = _read_json(blueprint_path)
    requirements = _read_json(requirements_path)
    _validate_blueprint(contract, blueprint, baseline)
    if not isinstance(requirements, list):
        raise AdapterError("Requirements file must contain a JSON array.")
    _requirement_contract(contract, blueprint, requirements)
    rows = _candidate_rows(contract, baseline, blueprint)
    _write_candidate(template, baseline, contract, rows, output_path)
    result = validate_candidate(
        contract,
        template_path,
        baseline_path,
        blueprint_path,
        requirements_path,
        output_path,
    )
    if result["status"] != "PASS":
        raise AdapterError(
            "Generated candidate failed semantic validation: "
            + "; ".join(issue["message"] for issue in result["errors"])
        )
    result["businessSummary"] = [
        {
            "operationId": operation["id"],
            "action": operation["action"],
            "entity": operation["entity"],
            "targetKey": operation["targetKey"],
            "values": operation["values"],
        }
        for operation in blueprint["operations"]
    ]
    result["structuralValidator"] = "fsm_task_adapter.py exact-task package reader"
    result["semanticValidator"] = "fsm_task_adapter.py blueprint/baseline validator"
    result["notImported"] = True
    return result


def determinism_check(
    contract: dict[str, Any],
    template_path: Path,
    baseline_path: Path,
    blueprint_path: Path,
    requirements_path: Path,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="fscr-adapter-") as directory:
        first = Path(directory) / "candidate-a.zip"
        second = Path(directory) / "candidate-b.zip"
        build_candidate(
            contract, template_path, baseline_path, blueprint_path, requirements_path, first
        )
        build_candidate(
            contract, template_path, baseline_path, blueprint_path, requirements_path, second
        )
        first_sha = _sha256_path(first)
        second_sha = _sha256_path(second)
    return {
        "schemaVersion": SCHEMA_VERSION,
        "status": "PASS" if first_sha == second_sha else "FAIL",
        "firstSha256": first_sha,
        "secondSha256": second_sha,
        "identicalBytes": first_sha == second_sha,
    }


def reconcile(
    contract: dict[str, Any],
    baseline_path: Path,
    candidate_path: Path,
    blueprint_path: Path,
    requirements_path: Path,
    export_path: Path,
) -> dict[str, Any]:
    baseline = _read_package(baseline_path, contract)
    candidate = _read_package(candidate_path, contract)
    persisted = _read_package(export_path, contract)
    blueprint = _read_json(blueprint_path)
    requirements = _read_json(requirements_path)
    _validate_blueprint(contract, blueprint, baseline)
    if not isinstance(requirements, list):
        raise AdapterError("Requirements file must contain a JSON array.")
    _requirement_contract(contract, blueprint, requirements)
    entities = _entity_map(contract)
    operation_map = {operation["id"]: operation for operation in blueprint["operations"]}
    indexes = {
        name: {
            "baseline": _row_index(baseline, entity),
            "candidate": _row_index(candidate, entity),
            "persisted": _row_index(persisted, entity),
        }
        for name, entity in entities.items()
    }
    matrix = []
    for requirement in requirements:
        entity = entities[requirement["entity"]]
        key = _target_tuple(entity, requirement["targetKey"])
        rows = indexes[entity["name"]]
        before = rows["baseline"].get(key)
        candidate_row = rows["candidate"].get(key)
        persisted_row = rows["persisted"].get(key)
        kind = requirement["kind"]
        passed = True
        requested: Any = requirement.get("requestedValue", "record present")
        candidate_value: Any = "present" if candidate_row is not None else "missing"
        persisted_value: Any = "present" if persisted_row is not None else "missing"
        detail = ""
        if kind == "target":
            passed = candidate_row is not None and persisted_row is not None
        elif kind == "value":
            field = requirement["field"]
            requested = str(requirement["requestedValue"])
            candidate_value = "" if candidate_row is None else candidate_row[field]
            persisted_value = "" if persisted_row is None else persisted_row[field]
            passed = candidate_value == requested and persisted_value == requested
        elif kind == "preserve_target":
            operation = operation_map[requirement["operationId"]]
            allowed = set(operation["values"]) | set(entity["auditFields"])
            differences = []
            if before is None or candidate_row is None or persisted_row is None:
                differences.append("target row unavailable")
            else:
                for field in entity["headers"]:
                    if field not in allowed and (
                        candidate_row[field] != before[field]
                        or persisted_row[field] != before[field]
                    ):
                        differences.append(field)
            requested = "unchanged"
            candidate_value = "unchanged" if not differences else differences
            persisted_value = "unchanged" if not differences else differences
            passed = not differences
            detail = "Preserved all non-requested, non-audit target fields."
        elif kind == "preserve_rows":
            touched = {
                (
                    op["entity"],
                    _target_tuple(entities[op["entity"]], op["targetKey"]),
                )
                for op in blueprint["operations"]
            }
            differences = []
            for entity_name, current_entity in entities.items():
                baseline_rows = indexes[entity_name]["baseline"]
                persisted_rows = indexes[entity_name]["persisted"]
                # Protect every confirmed baseline row, but do not fail solely
                # because another actor created an unrelated row after this
                # candidate's captured baseline. Requested targets remain covered by the
                # target/value requirements above and duplicate keys are
                # rejected while indexing the package.
                for row_key in sorted(baseline_rows):
                    if (entity_name, row_key) in touched:
                        continue
                    left = baseline_rows.get(row_key)
                    right = persisted_rows.get(row_key)
                    if right is None:
                        differences.append(f"{entity_name}:{row_key}:row")
                        continue
                    for field in current_entity["headers"]:
                        if field not in current_entity["auditFields"] and left[field] != right[field]:
                            differences.append(f"{entity_name}:{row_key}:{field}")
            requested = "unchanged"
            candidate_value = "not populated by design"
            persisted_value = "unchanged" if not differences else differences[:25]
            passed = not differences
            detail = f"Unexpected difference count: {len(differences)}."
        matrix.append(
            {
                "requirementId": requirement["id"],
                "requirement": requirement["requirement"],
                "requested": requested,
                "candidate": candidate_value,
                "persisted": persisted_value,
                "passed": passed,
                "detail": detail,
            }
        )
    return {
        "schemaVersion": SCHEMA_VERSION,
        "status": "PASS" if all(row["passed"] for row in matrix) else "FAIL",
        "task": contract["task"],
        "baselineSha256": baseline.archive_sha256,
        "candidateSha256": candidate.archive_sha256,
        "exportSha256": persisted.archive_sha256,
        "requirementMatrix": matrix,
        "mismatchCount": sum(not row["passed"] for row in matrix),
    }


def make_rollback(
    contract: dict[str, Any],
    template_path: Path,
    before_path: Path,
    current_path: Path,
    forward_blueprint_path: Path,
    rollback_blueprint_path: Path,
    rollback_requirements_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    _validate_new_outputs(
        [rollback_blueprint_path, rollback_requirements_path, output_path],
        [template_path, before_path, current_path, forward_blueprint_path],
    )
    before = _read_package(before_path, contract)
    current = _read_package(current_path, contract)
    if before.metadata["ProcessEnv"] != current.metadata["ProcessEnv"]:
        raise AdapterError("Before and current rollback exports come from different environments.")
    if before.metadata["ProcessRelease"] != current.metadata["ProcessRelease"]:
        raise AdapterError("Before and current rollback exports come from different releases.")
    forward = _read_json(forward_blueprint_path)
    _validate_blueprint(contract, forward, before)
    entities = _entity_map(contract)
    operations = []
    for index, operation in enumerate(forward["operations"], start=1):
        if operation["action"] != "update":
            raise AdapterError("Automatic rollback currently supports update operations only.")
        entity = entities[operation["entity"]]
        key = _target_tuple(entity, operation["targetKey"])
        original_row = _row_index(before, entity).get(key)
        current_row = _row_index(current, entity).get(key)
        if original_row is None or current_row is None:
            raise AdapterError(f"Rollback target {entity['name']} {key!r} is missing.")
        values = {field: original_row[field] for field in operation["values"]}
        operations.append(
            {
                "id": f"RB-OP-{index:03d}",
                "action": "update",
                "entity": entity["name"],
                "targetKey": operation["targetKey"],
                "values": values,
                "preserveOtherValues": True,
                "preserveUnspecifiedRows": True,
            }
        )
    design = {
        "operations": operations,
        "resolvedScope": forward.get("resolvedScope", {}),
        "explicitDefaults": [],
        "preservedValues": [],
        "prerequisites": forward.get("prerequisites", []),
        "warnings": [],
    }
    rollback = _normalized_blueprint(contract, design)
    _validate_blueprint(contract, rollback, current)
    requirements = _requirements(contract, rollback)
    _write_json(rollback_blueprint_path, rollback)
    _write_json(rollback_requirements_path, requirements)
    report = build_candidate(
        contract,
        template_path,
        current_path,
        rollback_blueprint_path,
        rollback_requirements_path,
        output_path,
    )
    report["rollbackOfDesignSha256"] = _sha256_bytes(_canonical_bytes(forward))
    report["rollbackScope"] = "Restore only fields changed by the forward blueprint."
    return report


def normalized_manifest(
    contract: dict[str, Any],
    package_path: Path,
    environment: str,
    base_url: str,
    template_only: bool,
) -> dict[str, Any]:
    package = _read_package(package_path, contract)
    populated = [
        entity["member"]
        for entity in contract["package"]["entities"]
        if package.rows[entity["name"]]
    ]
    return {
        "environment": environment,
        "baseUrl": base_url,
        "taskName": contract["task"]["name"],
        "taskCode": contract["task"]["code"],
        "status": package.metadata["ProcessStatus"],
        "templateOnly": template_only,
        "release": package.metadata["ProcessRelease"],
        "processId": package.metadata["ESSRequestId"],
        "schemaFingerprint": _schema_fingerprint(contract, package),
        "selectedTaskCodes": [contract["task"]["code"]],
        "definedTaskCodes": [contract["task"]["code"]],
        "members": package.member_names,
        "headers": {
            entity["member"]: package.headers[entity["name"]]
            for entity in contract["package"]["entities"]
        },
        "populatedMembers": populated,
        "unrelatedPopulatedMembers": [],
    }


def _bool_arg(value: str) -> bool:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    raise argparse.ArgumentTypeError("Expected true or false.")


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, default=_default_contract_path())
    parser.add_argument("--report", type=Path)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    manifest = sub.add_parser("manifest", help="Normalize one exact-task source ZIP.")
    _add_common(manifest)
    manifest.add_argument("--package", type=Path, required=True)
    manifest.add_argument("--environment", required=True)
    manifest.add_argument("--base-url", required=True)
    manifest.add_argument("--template-only", type=_bool_arg, required=True)

    normalize = sub.add_parser("normalize", help="Validate a Codex-normalized business design.")
    _add_common(normalize)
    normalize.add_argument("--baseline", type=Path, required=True)
    normalize.add_argument("--request", type=Path, required=True)
    normalize.add_argument("--design", type=Path, required=True)
    normalize.add_argument("--blueprint-output", type=Path, required=True)
    normalize.add_argument("--preview-output", type=Path, required=True)
    normalize.add_argument("--requirements-output", type=Path, required=True)

    merge_shared = sub.add_parser(
        "merge-shared-row",
        help="Merge same-BU Invoice and Payment Options values into one canonical writer row.",
    )
    _add_common(merge_shared)
    merge_shared.add_argument("--baseline-row", type=Path, required=True)
    merge_shared.add_argument("--invoice-values", type=Path, required=True)
    merge_shared.add_argument("--payment-values", type=Path, required=True)
    merge_shared.add_argument("--bu-name", required=True)
    merge_shared.add_argument("--output", type=Path, required=True)

    for name in ("build", "validate", "determinism"):
        command = sub.add_parser(name)
        _add_common(command)
        command.add_argument("--template", type=Path, required=True)
        command.add_argument("--baseline", type=Path, required=True)
        command.add_argument("--blueprint", type=Path, required=True)
        command.add_argument("--requirements", type=Path, required=True)
        if name == "build":
            command.add_argument("--output", type=Path, required=True)
        elif name == "validate":
            command.add_argument("--package", type=Path, required=True)

    upload_validate = sub.add_parser(
        "validate-upload", help="Validate an uploaded FSM ZIP without importing it."
    )
    _add_common(upload_validate)
    upload_validate.add_argument("--baseline", type=Path, required=True)
    upload_validate.add_argument("--package", type=Path, required=True)

    rollback = sub.add_parser("rollback", help="Build a narrow rollback for a validated update.")
    _add_common(rollback)
    rollback.add_argument("--template", type=Path, required=True)
    rollback.add_argument("--before", type=Path, required=True)
    rollback.add_argument("--current", type=Path, required=True)
    rollback.add_argument("--forward-blueprint", type=Path, required=True)
    rollback.add_argument("--blueprint-output", type=Path, required=True)
    rollback.add_argument("--requirements-output", type=Path, required=True)
    rollback.add_argument("--output", type=Path, required=True)

    reconcile_parser = sub.add_parser("reconcile")
    _add_common(reconcile_parser)
    reconcile_parser.add_argument("--baseline", type=Path, required=True)
    reconcile_parser.add_argument("--candidate", type=Path, required=True)
    reconcile_parser.add_argument("--blueprint", type=Path, required=True)
    reconcile_parser.add_argument("--requirements", type=Path, required=True)
    reconcile_parser.add_argument("--export", type=Path, required=True)
    return parser.parse_args(argv)


def _command_succeeded(command: str, result: dict[str, Any]) -> bool:
    if command == "manifest":
        return result.get("status") == "COMPLETED"
    return result.get("status", "PASS") == "PASS"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        contract = _load_contract(args.contract)
        if args.command == "manifest":
            result = normalized_manifest(
                contract,
                args.package,
                args.environment,
                args.base_url,
                args.template_only,
            )
        elif args.command == "normalize":
            blueprint, preview, requirements = normalize_design(
                contract, args.baseline, args.request, args.design
            )
            _write_json(args.blueprint_output, blueprint)
            _write_json(args.preview_output, preview)
            _write_json(args.requirements_output, requirements)
            result = preview
        elif args.command == "merge-shared-row":
            result = merge_shared_row_transaction(
                contract,
                _read_json(args.baseline_row),
                args.bu_name,
                _read_json(args.invoice_values),
                _read_json(args.payment_values),
            )
            _write_json(args.output, result)
        elif args.command == "build":
            result = build_candidate(
                contract,
                args.template,
                args.baseline,
                args.blueprint,
                args.requirements,
                args.output,
            )
        elif args.command == "validate":
            result = validate_candidate(
                contract,
                args.template,
                args.baseline,
                args.blueprint,
                args.requirements,
                args.package,
            )
        elif args.command == "validate-upload":
            result = validate_uploaded_package(contract, args.baseline, args.package)
        elif args.command == "determinism":
            result = determinism_check(
                contract,
                args.template,
                args.baseline,
                args.blueprint,
                args.requirements,
            )
        elif args.command == "rollback":
            result = make_rollback(
                contract,
                args.template,
                args.before,
                args.current,
                args.forward_blueprint,
                args.blueprint_output,
                args.requirements_output,
                args.output,
            )
        elif args.command == "reconcile":
            result = reconcile(
                contract,
                args.baseline,
                args.candidate,
                args.blueprint,
                args.requirements,
                args.export,
            )
        else:
            raise AdapterError(f"Unknown command {args.command!r}.")
        if args.report:
            _write_json(args.report, result)
        print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
        return 0 if _command_succeeded(args.command, result) else 2
    except AdapterError as exc:
        failure = {
            "schemaVersion": SCHEMA_VERSION,
            "status": "FAIL",
            "errors": [{"code": "ADAPTER_ERROR", "message": str(exc)}],
        }
        if getattr(args, "report", None):
            _write_json(args.report, failure)
        print(json.dumps(failure, indent=2, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
