#!/usr/bin/env python3
"""Portable, data-driven FSM task adapter runtime.

This file is copied into a generated Nested task skill.  Task semantics live in
the adjacent e2e-adapter.json descriptor and ora-resource rule plan.  The
runtime performs offline package work only; it never connects to Fusion.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path, PurePosixPath
from typing import Any
from xml.etree import ElementTree


SCHEMA_VERSION = "fscr-fsm-task-adapter-v1"
MAX_MEMBER_BYTES = 10 * 1024 * 1024
MAX_TOTAL_BYTES = 100 * 1024 * 1024
MAX_COMPRESSION_RATIO = 100
SUCCESS_STATUS = re.compile(r"COMPLETE|SUCCESS|SUCCEED", re.IGNORECASE)
SOURCE_DATE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d")
CANDIDATE_DATE_FORMAT = "%Y-%m-%d"

# Task-specific clarification policy retained across the no-ship descriptor
# split.  The shipping descriptor remains schema-pure; this offline runtime
# enforces the task's evidenced mandatory business choices before preview.
TASK_CREATE_REQUIREMENTS = {
    "AR_RECEIPT_CLASS": {
        "group": "Receipt class",
        "valueFields": [
            "CreationMethodCode",
            "ConfirmFlag",
            "RemitFlag",
            "ClearFlag",
        ],
        "labels": {
            "CreationMethodCode": "creation method",
            "ConfirmFlag": "confirmation behavior",
            "RemitFlag": "remittance behavior",
            "ClearFlag": "clearance behavior",
        },
    },
    "AR_RECEIPT_METHOD": {
        "group": "Receipt method",
        "valueFields": ["StartDate", "PaymentTypeCode"],
        "labels": {
            "StartDate": "effective start date",
            "PaymentTypeCode": "intended receipt use or payment type",
        },
    },
    "AR_RECEIPT_METHOD_ACCOUNT": {
        "group": "Remittance bank account",
        "valueFields": ["PrimaryFlag", "OverrideRemitAccountFlag"],
        "evidenceFields": [
            "BuName",
            "BankAccountName",
            "CurrencyCode",
            "AccountingCombinations",
        ],
        "labels": {
            "PrimaryFlag": "primary-account choice",
            "OverrideRemitAccountFlag": "remittance-account override behavior",
            "BuName": "target-valid active business unit evidence",
            "BankAccountName": "eligible bank, branch, and bank-account evidence",
            "CurrencyCode": "supported currency evidence",
            "AccountingCombinations": (
                "applicable accounting combinations or an evidence-backed "
                "not-applicable decision"
            ),
        },
    },
}


class AdapterError(ValueError):
    """A safe, user-correctable adapter failure."""


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
    entities = _entity_map(contract)
    if len(entities) != len(package["entities"]):
        raise AdapterError("Adapter contract contains duplicate entity names.")
    for entity in entities.values():
        for field in entity["keyFields"]:
            _key_comparison_mode(entity, field)
        field_constraints = entity.get("fieldConstraints", {})
        if not isinstance(field_constraints, dict):
            raise AdapterError(
                f"Entity {entity['name']} fieldConstraints must be an object."
            )
        unknown_length_fields = set(field_constraints) - set(entity["headers"])
        if unknown_length_fields:
            raise AdapterError(
                f"Entity {entity['name']} declares maximum lengths for unknown fields: "
                f"{sorted(unknown_length_fields)}."
            )
        for field, constraint in field_constraints.items():
            maximum = constraint.get("maxLength") if isinstance(constraint, dict) else None
            if not isinstance(maximum, int) or isinstance(maximum, bool) or maximum <= 0:
                raise AdapterError(
                    f"Entity {entity['name']} field {field} has invalid maximum length "
                    f"{maximum!r}."
                )
            expected = entity["types"].get(field, "string") or "string"
            if expected != "string":
                raise AdapterError(
                    f"Entity {entity['name']} field {field} declares maximum length "
                    f"but has non-string type {expected!r}."
                )
    _relationship_specs(contract, entities)
    return contract


def _entity_map(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {entity["name"]: entity for entity in contract["package"]["entities"]}


def _key_comparison_mode(entity: dict[str, Any], field: str) -> str:
    if field not in entity.get("keyFields", []):
        raise AdapterError(
            f"Entity {entity['name']} comparison requested for non-key field {field}."
        )
    return "exact"


def _parse_source_date(value: str) -> datetime:
    for pattern in SOURCE_DATE_FORMATS:
        try:
            return datetime.strptime(value, pattern)
        except ValueError:
            continue
    raise ValueError(value)


def _canonical_date_text(value: Any, *, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AdapterError(
            f"{context} must be a nonblank date in YYYY-MM-DD or YYYY/MM/DD format."
        )
    candidate = value.strip()
    try:
        parsed = _parse_source_date(candidate)
    except ValueError as exc:
        raise AdapterError(
            f"{context} has invalid date {value!r}; expected YYYY-MM-DD or "
            "source-export YYYY/MM/DD."
        ) from exc
    return parsed.strftime(CANDIDATE_DATE_FORMAT)


def _normalized_key_component(entity: dict[str, Any], field: str, value: Any) -> str:
    text = "" if value is None else str(value)
    if entity["types"].get(field) == "date" and text.strip():
        text = _canonical_date_text(
            text,
            context=f"Entity {entity['name']} key field {field}",
        )
    if _key_comparison_mode(entity, field) == "casefold":
        return text.casefold()
    return text


def _relationship_specs(
    contract: dict[str, Any], entities: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    semantic_model = contract.get("semanticModel", {})
    relationships = semantic_model.get("relationships", [])
    if not isinstance(relationships, list):
        raise AdapterError("semanticModel.relationships must be a list.")
    result: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for position, relationship in enumerate(relationships, start=1):
        if not isinstance(relationship, dict):
            raise AdapterError(f"Relationship {position} must be an object.")
        child_name = relationship.get("childEntity")
        parent_name = relationship.get("parentEntity")
        if child_name not in entities or parent_name not in entities:
            raise AdapterError(
                f"Relationship {position} names unknown child/parent entities "
                f"{child_name!r}/{parent_name!r}."
            )
        identity = (str(child_name), str(parent_name))
        if identity in seen:
            raise AdapterError(
                f"More than one relationship maps {child_name} to {parent_name}."
            )
        seen.add(identity)
        parent_fields = relationship.get("parentFields")
        child_fields = relationship.get("childFields")
        if (
            not isinstance(parent_fields, list)
            or not isinstance(child_fields, list)
            or not parent_fields
            or len(parent_fields) != len(child_fields)
        ):
            raise AdapterError(
                f"Relationship {position} must map equally sized childFields and "
                "parentFields arrays."
            )
        field_map = dict(zip(child_fields, parent_fields, strict=True))
        child = entities[str(child_name)]
        parent = entities[str(parent_name)]
        unknown_child = set(field_map) - set(child["keyFields"])
        if unknown_child:
            raise AdapterError(
                f"Relationship {position} maps non-key child fields: "
                f"{sorted(unknown_child)}."
            )
        if len(set(field_map.values())) != len(field_map):
            raise AdapterError(f"Relationship {position} repeats a parent key field.")
        if set(field_map.values()) != set(parent["keyFields"]):
            raise AdapterError(
                f"Relationship {position} must resolve every parent key field "
                f"{parent['keyFields']}."
            )
        try:
            parent_sequence = int(parent["nodeSequence"])
            child_sequence = int(child["nodeSequence"])
        except (KeyError, TypeError, ValueError) as exc:
            raise AdapterError(
                f"Relationship {position} requires numeric parent/child nodeSequence values."
            ) from exc
        if parent_sequence >= child_sequence:
            raise AdapterError(
                f"Relationship {position} violates package dependency order: "
                f"{parent_name} must precede {child_name}."
            )
        normalized_relationship = dict(relationship)
        normalized_relationship["fieldMap"] = field_map
        result.append(normalized_relationship)
    coverage = semantic_model.get("coverage", {})
    if isinstance(coverage, dict) and "relationshipCount" in coverage:
        if coverage["relationshipCount"] != len(result):
            raise AdapterError(
                "semanticModel.coverage.relationshipCount differs from the "
                "declared relationship graph."
            )
    return result


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
    reader = csv.DictReader(io.StringIO(text, newline=""))
    headers = reader.fieldnames or []
    if not headers or len(set(headers)) != len(headers):
        raise AdapterError(f"{member} has blank or duplicate headers.")
    rows = []
    for number, row in enumerate(reader, start=2):
        if None in row:
            raise AdapterError(f"{member} row {number} has extra values.")
        rows.append({header: row.get(header, "") for header in headers})
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
        writer.writerow({header: str(row.get(header, "")) for header in headers})
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
    node_sequences: list[int] = []
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
        try:
            node_sequence = int(actual["nodeSequence"])
        except (TypeError, ValueError) as exc:
            raise AdapterError(
                f"Metadata node sequence for {entity['name']} must be a positive integer."
            ) from exc
        if node_sequence <= 0:
            raise AdapterError(
                f"Metadata node sequence for {entity['name']} must be a positive integer."
            )
        node_sequences.append(node_sequence)
        for field, actual_type in actual["types"].items():
            if field not in entity["headers"]:
                raise AdapterError(
                    f"Metadata object {entity['name']} contains non-CSV attribute {field}."
                )
            if entity["types"].get(field, "") != actual_type:
                raise AdapterError(
                    f"Metadata type for {entity['name']}.{field} is {actual_type!r}, expected {entity['types'].get(field, '')!r}."
                )
    if len(set(node_sequences)) != len(node_sequences):
        raise AdapterError("Metadata business-object node sequences must be unique.")

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
                # Current-data exports can reorder business-object metadata.
                # Fingerprint the canonical descriptor order so a harmless
                # runtime ordering variation does not look like schema drift.
                "nodeSequence": entity["nodeSequence"],
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


def _validate_template_node_sequences(
    contract: dict[str, Any], template: PackageData
) -> None:
    """Require the build template to preserve the canonical parent-first order.

    Current-data exports can legitimately vary their business-object sequence,
    so their sequence is identity evidence rather than a fixed schema value.
    The template is different: its metadata is copied byte-for-byte into the
    candidate and therefore must keep the descriptor's parent-before-child
    import order.
    """
    for entity in contract["package"]["entities"]:
        actual = template.object_contracts[entity["name"]]["nodeSequence"]
        if actual != entity["nodeSequence"]:
            raise AdapterError(
                f"Build template node sequence for {entity['name']} is {actual!r}, "
                f"expected canonical value {entity['nodeSequence']!r}."
            )


def _validate_source_pair(
    contract: dict[str, Any], template: PackageData, baseline: PackageData
) -> None:
    if any(template.rows[entity["name"]] for entity in contract["package"]["entities"]):
        raise AdapterError("Build template must be template-only and contain no data rows.")
    _validate_template_node_sequences(contract, template)
    for field in ("ProcessEnv", "ProcessRelease"):
        if template.metadata[field] != baseline.metadata[field]:
            raise AdapterError(
                f"Template and baseline {field} differ: {template.metadata[field]!r} versus {baseline.metadata[field]!r}."
            )
    # evidenceRelease records the release used to author and qualify the
    # descriptor; it is provenance, not a target-release allowlist.  A later
    # target release is safe only when its template and baseline are from the
    # same release and both still match the descriptor's exact task schema.
    expected_fingerprint = contract["package"].get("schemaFingerprint", "")
    if expected_fingerprint:
        for label, source in (("Template", template), ("Baseline", baseline)):
            actual_fingerprint = _schema_fingerprint(contract, source)
            if actual_fingerprint != expected_fingerprint:
                raise AdapterError(
                    f"{label} schema fingerprint {actual_fingerprint!r} differs "
                    f"from descriptor schema fingerprint {expected_fingerprint!r}."
                )


def _row_key(entity: dict[str, Any], row: dict[str, str]) -> tuple[str, ...]:
    return tuple(
        _normalized_key_component(entity, field, row.get(field, ""))
        for field in entity["keyFields"]
    )


def _target_tuple(entity: dict[str, Any], target: dict[str, Any]) -> tuple[str, ...]:
    return tuple(
        _normalized_key_component(entity, field, target.get(field, ""))
        for field in entity["keyFields"]
    )


def _field_values_equal(
    entity: dict[str, Any], field: str, left: Any, right: Any
) -> bool:
    """Compare source values without treating harmless CSV formatting as a change."""
    if field.endswith("CcidSegments"):
        try:
            return _account_segment_display(left) == _account_segment_display(right)
        except AdapterError:
            return False
    left_text = "" if left is None else str(left).strip()
    right_text = "" if right is None else str(right).strip()
    if left_text == right_text:
        return True
    if not left_text or not right_text:
        return False

    expected = entity["types"].get(field, "string") or "string"
    try:
        if expected in {"int", "long"}:
            return int(left_text) == int(right_text)
        if expected == "decimal":
            return Decimal(left_text) == Decimal(right_text)
        if expected == "date":
            return _parse_source_date(left_text) == _parse_source_date(right_text)
        if expected == "dateTime":
            def parse_datetime(value: str) -> datetime:
                normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
                return datetime.fromisoformat(normalized)

            return parse_datetime(left_text) == parse_datetime(right_text)
    except (InvalidOperation, ValueError):
        return False
    return False


def _validate_field_value(
    entity: dict[str, Any], field: str, value: Any, operation_id: str
) -> None:
    expected = entity["types"].get(field, "string") or "string"
    valid = False
    if expected == "string":
        valid = isinstance(value, str)
    elif expected in {"int", "long"}:
        valid = (
            isinstance(value, int)
            and not isinstance(value, bool)
        ) or (
            isinstance(value, str)
            and re.fullmatch(r"[+-]?\d+", value.strip()) is not None
        )
    elif expected == "decimal":
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
    elif expected == "date":
        if isinstance(value, str) and value.strip():
            try:
                _parse_source_date(value.strip())
                valid = True
            except ValueError:
                valid = False
    elif expected == "dateTime":
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
    constraint = entity.get("fieldConstraints", {}).get(field, {})
    maximum = constraint.get("maxLength") if isinstance(constraint, dict) else None
    if maximum is not None and isinstance(value, str) and len(value) > maximum:
        raise AdapterError(
            f"Operation {operation_id} field {entity['name']}.{field} exceeds "
            f"maximum length {maximum}: received {len(value)} characters."
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


def _satisfied_prerequisites(blueprint: dict[str, Any]) -> set[tuple[str, str]]:
    satisfied: set[tuple[str, str]] = set()
    for item in blueprint.get("prerequisites", []):
        if not isinstance(item, dict) or item.get("status") != "satisfied":
            continue
        entity = str(item.get("entity", ""))
        field = str(item.get("field", ""))
        if entity and field and item.get("evidence"):
            satisfied.add((entity, field))
    return satisfied


def _validate_clarification_requirements(
    contract: dict[str, Any], blueprint: dict[str, Any]
) -> None:
    """Block incomplete creates with one consolidated business follow-up."""
    requirements = TASK_CREATE_REQUIREMENTS
    if not isinstance(requirements, dict) or not requirements:
        return

    evidenced: set[tuple[str, str]] = set()
    for item in blueprint.get("prerequisites", []):
        if not isinstance(item, dict) or item.get("status") not in {
            "satisfied",
            "not_applicable",
        }:
            continue
        entity = str(item.get("entity", ""))
        field = str(item.get("field", ""))
        if entity and field and item.get("evidence"):
            evidenced.add((entity, field))
    findings: list[str] = []
    for operation in blueprint.get("operations", []):
        if not isinstance(operation, dict) or operation.get("action") != "create":
            continue
        entity_name = str(operation.get("entity", ""))
        rule = requirements.get(entity_name)
        if not isinstance(rule, dict):
            continue
        values = operation.get("values")
        values = values if isinstance(values, dict) else {}
        labels = rule.get("labels")
        labels = labels if isinstance(labels, dict) else {}
        missing: list[str] = []
        for field in rule.get("valueFields", []):
            value = values.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                missing.append(str(labels.get(field, field)))
        for field in rule.get("evidenceFields", []):
            if (entity_name, str(field)) not in evidenced:
                missing.append(str(labels.get(field, field)))
        if missing:
            group = str(rule.get("group") or entity_name)
            operation_id = str(operation.get("id") or "unnamed operation")
            findings.append(f"{group} {operation_id}: {', '.join(missing)}")

    if findings:
        raise AdapterError(
            "FOLLOW_UP_REQUIRED: Ask one consolidated business-language question "
            "covering every unresolved hierarchy choice before creating a blueprint "
            "or ZIP. Do not ask one level at a time and do not choose the first "
            "observed option. Unresolved choices: " + " | ".join(findings)
        )


def _validate_create_parents(
    contract: dict[str, Any],
    blueprint: dict[str, Any],
    baseline_indexes: dict[str, dict[tuple[str, ...], dict[str, str]]],
    entities: dict[str, dict[str, Any]],
) -> None:
    relationships_by_child: dict[str, list[dict[str, Any]]] = {}
    for relationship in _relationship_specs(contract, entities):
        relationships_by_child.setdefault(relationship["childEntity"], []).append(
            relationship
        )

    candidate_creates: dict[
        tuple[str, tuple[str, ...]], tuple[int, dict[str, Any]]
    ] = {}
    for position, operation in enumerate(blueprint["operations"], start=1):
        if operation["action"] != "create":
            continue
        entity = entities[operation["entity"]]
        identity = (entity["name"], _target_tuple(entity, operation["targetKey"]))
        candidate_creates[identity] = (position, operation)

    for child_position, operation in enumerate(blueprint["operations"], start=1):
        if operation["action"] != "create":
            continue
        child_name = operation["entity"]
        for relationship in relationships_by_child.get(child_name, []):
            parent_name = relationship["parentEntity"]
            parent = entities[parent_name]
            parent_target = {
                parent_field: operation["targetKey"][child_field]
                for child_field, parent_field in relationship["fieldMap"].items()
            }
            parent_key = _target_tuple(parent, parent_target)
            if parent_key in baseline_indexes[parent_name]:
                continue
            candidate_parent = candidate_creates.get((parent_name, parent_key))
            if candidate_parent is None:
                raise AdapterError(
                    f"Operation {operation['id']} parent {parent_name} {parent_key!r} "
                    "is absent from both the fresh current export and the same "
                    "candidate create graph."
                )
            parent_position, parent_operation = candidate_parent
            if parent_position >= child_position:
                raise AdapterError(
                    f"Operation {parent_operation['id']} must precede child operation "
                    f"{operation['id']} to preserve candidate dependency order."
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
    entities = _entity_map(contract)
    for index, raw in enumerate(operations, start=1):
        if not isinstance(raw, dict):
            raise AdapterError(f"Operation {index} must be an object.")
        operation = dict(raw)
        operation.setdefault("id", f"OP-{index:03d}")
        operation.setdefault("action", "update")
        operation.setdefault("preserveOtherValues", True)
        operation.setdefault("preserveUnspecifiedRows", True)
        entity = entities.get(str(operation.get("entity", "")))
        if entity is not None:
            for group_name in ("targetKey", "values"):
                group = operation.get(group_name)
                if not isinstance(group, dict):
                    continue
                normalized_group = dict(group)
                for field, value in group.items():
                    if entity["types"].get(field) == "date":
                        normalized_group[field] = _canonical_date_text(
                            value,
                            context=(
                                f"Operation {operation['id']} field "
                                f"{entity['name']}.{field}"
                            ),
                        )
                operation[group_name] = normalized_group
        normalized_ops.append(operation)
    blueprint = {
        "task": {
            "name": contract["task"]["name"],
            "code": contract["task"]["code"],
        },
        "operations": normalized_ops,
        "resolvedScope": design.get("resolvedScope", {}),
        "explicitDefaults": design.get("explicitDefaults", []),
        "preservedValues": design.get("preservedValues", []),
        "prerequisites": design.get("prerequisites", []),
        "warnings": design.get("warnings", []),
    }
    return blueprint


def _business_design_projection(blueprint: dict[str, Any]) -> dict[str, Any]:
    """Return the stable business intent that a user's confirmation binds.

    Source archives, process identifiers, prerequisite lookup evidence, and
    generated candidate bytes are deliberately absent.  Those values are
    execution evidence and may change between sequential phases without
    changing the business decision.  Resolved business values must be carried
    by operations, resolvedScope, explicitDefaults, or preservedValues.
    """
    return {
        "task": blueprint["task"],
        "operations": blueprint["operations"],
        "resolvedScope": blueprint.get("resolvedScope", {}),
        "explicitDefaults": blueprint.get("explicitDefaults", []),
        "preservedValues": blueprint.get("preservedValues", []),
    }


def business_design_sha256(blueprint: dict[str, Any]) -> str:
    return _sha256_bytes(_canonical_bytes(_business_design_projection(blueprint)))


def _phase_blueprint(
    blueprint: dict[str, Any], operations: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        "task": blueprint["task"],
        "operations": operations,
        "resolvedScope": blueprint.get("resolvedScope", {}),
        "explicitDefaults": blueprint.get("explicitDefaults", []),
        "preservedValues": blueprint.get("preservedValues", []),
        "prerequisites": blueprint.get("prerequisites", []),
        "warnings": blueprint.get("warnings", []),
    }


def _flow_phase_dependencies(
    contract: dict[str, Any], phase_operations: list[list[dict[str, Any]]]
) -> list[list[str]]:
    entities = _entity_map(contract)
    relationships_by_child: dict[str, list[dict[str, Any]]] = {}
    for relationship in _relationship_specs(contract, entities):
        relationships_by_child.setdefault(relationship["childEntity"], []).append(
            relationship
        )
    last_target_phase: dict[tuple[str, tuple[str, ...]], int] = {}
    created_target_phase: dict[tuple[str, tuple[str, ...]], int] = {}
    result: list[list[str]] = []
    for phase_index, operations in enumerate(phase_operations, start=1):
        dependencies: set[int] = set()
        for operation in operations:
            entity = entities[operation["entity"]]
            identity = (entity["name"], _target_tuple(entity, operation["targetKey"]))
            if identity in last_target_phase:
                dependencies.add(last_target_phase[identity])
            for relationship in relationships_by_child.get(entity["name"], []):
                parent = entities[relationship["parentEntity"]]
                parent_target = {
                    parent_field: operation["targetKey"][child_field]
                    for child_field, parent_field in relationship["fieldMap"].items()
                }
                parent_identity = (
                    parent["name"],
                    _target_tuple(parent, parent_target),
                )
                if parent_identity in created_target_phase:
                    dependencies.add(created_target_phase[parent_identity])
        result.append([f"PHASE-{item:03d}" for item in sorted(dependencies)])
        for operation in operations:
            entity = entities[operation["entity"]]
            identity = (entity["name"], _target_tuple(entity, operation["targetKey"]))
            last_target_phase[identity] = phase_index
            if operation["action"] == "create":
                created_target_phase[identity] = phase_index
    return result


def plan_flow(contract: dict[str, Any], design_path: Path) -> dict[str, Any]:
    """Plan one business request into the fewest semantically required phases.

    This is an offline planning operation.  Each phase is still normalized
    against the then-current export before build, so the planner never treats
    an earlier phase's expected result as persisted Fusion state.
    """
    blueprint = _normalized_blueprint(contract, _read_json(design_path))
    operation_ids = [str(item.get("id", "")) for item in blueprint["operations"]]
    if len(operation_ids) != len(set(operation_ids)):
        raise AdapterError("Flow operations must have globally unique stable ids.")
    entities = _entity_map(contract)
    create_targets: set[tuple[str, tuple[str, ...]]] = set()
    for operation in blueprint["operations"]:
        # Singleton validation below produces the precise unknown-entity/key
        # error; duplicate-create detection only runs for structurally usable
        # identities.
        entity = entities.get(str(operation.get("entity", "")))
        target = operation.get("targetKey")
        if (
            operation.get("action") != "create"
            or entity is None
            or not isinstance(target, dict)
        ):
            continue
        if set(target) != set(entity["keyFields"]):
            continue
        identity = (entity["name"], _target_tuple(entity, target))
        if identity in create_targets:
            raise AdapterError(
                f"Flow contains more than one create for {entity['name']} "
                f"{identity[1]!r}."
            )
        create_targets.add(identity)

    phase_operations: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    for operation in blueprint["operations"]:
        proposed = current + [operation]
        try:
            _validate_blueprint(contract, _phase_blueprint(blueprint, proposed))
            current = proposed
        except AdapterError:
            if current:
                phase_operations.append(current)
            current = [operation]
            # Re-run for the singleton so semantic errors are reported rather
            # than being mistaken for a batch-shape boundary.
            _validate_blueprint(contract, _phase_blueprint(blueprint, current))
    if current:
        phase_operations.append(current)

    phase_dependencies = _flow_phase_dependencies(contract, phase_operations)
    phases = []
    for index, operations in enumerate(phase_operations, start=1):
        phase = _phase_blueprint(blueprint, operations)
        phases.append(
            {
                "id": f"PHASE-{index:03d}",
                "sequence": index,
                "dependsOn": phase_dependencies[index - 1],
                "operationIds": [operation["id"] for operation in operations],
                "operationCount": len(operations),
                "blueprint": phase,
                "phaseDesignSha256": _sha256_bytes(_canonical_bytes(phase)),
                "baselinePolicy": (
                    "fresh-current-export"
                    if index == 1
                    else "latest-successfully-reconciled-export"
                ),
            }
        )
    return {
        "schemaVersion": SCHEMA_VERSION,
        "status": "PASS",
        "task": blueprint["task"],
        "businessDesignSha256": business_design_sha256(blueprint),
        "operationCount": len(blueprint["operations"]),
        "phaseCount": len(phases),
        "phases": phases,
        "executionPolicy": {
            "interaction": "one consolidated clarification and design confirmation",
            "liveMutationConcurrency": 1,
            "candidateApprovalOwner": "core.data-loader",
            "verificationExportReuse": True,
            "continueAfterFailure": "continue only with phases unblocked by fresh reconciled state",
        },
    }


def _validate_blueprint(
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
    satisfied = _satisfied_prerequisites(blueprint)
    seen_ids: set[str] = set()
    seen_targets: set[tuple[str, tuple[str, ...]]] = set()
    baseline_indexes = (
        {name: _row_index(baseline, entity) for name, entity in entities.items()}
        if baseline is not None
        else {}
    )
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
        target = operation.get("targetKey")
        if not isinstance(target, dict) or set(target) != set(entity["keyFields"]):
            raise AdapterError(
                f"Operation {operation_id} targetKey must contain exactly "
                f"{entity['keyFields']}."
            )
        target_tuple = _target_tuple(entity, target)
        if any(value == "" for value in target_tuple):
            raise AdapterError(f"Operation {operation_id} has a blank target key.")
        for field, value in target.items():
            _validate_field_value(entity, field, value, operation_id)
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
        blocked = {
            item["field"]: item
            for item in entity.get("conditionallyBlockedFields", [])
        }
        operation_fields = set(
            entity.get("createFields" if action == "create" else "updateFields", {})
        )
        for field in values:
            if field in blocked and (entity_name, field) not in satisfied:
                raise AdapterError(
                    f"Operation {operation_id} changes conditionally blocked field "
                    f"{entity_name}.{field}: {blocked[field]['reason']}"
                )
            if field not in operation_fields:
                raise AdapterError(
                    f"Operation {operation_id} has no source-backed {action} contract "
                    f"for {entity_name}.{field}. Ask for a supported business change "
                    "and do not generate a candidate ZIP."
                )
            _validate_field_value(entity, field, values[field], operation_id)
        if baseline is not None:
            matches = baseline_indexes[entity_name]
            if action == "create" and target_tuple in matches:
                raise AdapterError(
                    f"Operation {operation_id} create target {entity_name} "
                    f"{target_tuple!r} already exists in the fresh current export."
                )
            if action == "update" and target_tuple not in matches:
                raise AdapterError(
                    f"Operation {operation_id} target {target_tuple!r} does not exist "
                    "exactly once in the fresh current export."
                )
            if action == "update" and all(
                _field_values_equal(entity, field, matches[target_tuple].get(field, ""), value)
                for field, value in values.items()
            ):
                raise AdapterError(
                    f"Operation {operation_id} is a no-op: every requested value already "
                    "matches the fresh current export. No candidate ZIP is needed."
                )
    if baseline is not None:
        _validate_create_parents(
            contract, blueprint, baseline_indexes, entities
        )
    _validate_clarification_requirements(contract, blueprint)


def _requirements(
    contract: dict[str, Any], blueprint: dict[str, Any]
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    number = 1
    for operation in blueprint["operations"]:
        target_display = json.dumps(
            operation["targetKey"], ensure_ascii=False, sort_keys=True
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
                    f"identified by {target_display}"
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
        if operation.get("preserveOtherValues", True):
            if operation["action"] == "create":
                requirement_kind = "unset_target"
                requirement_text = (
                    "Leave every unrequested non-key, non-audit value unset on "
                    "the created record"
                )
            else:
                requirement_kind = "preserve_target"
                requirement_text = (
                    "Preserve every other non-audit value on the target record"
                )
            result.append(
                {
                    "id": f"REQ-{number:03d}",
                    "kind": requirement_kind,
                    "requirement": requirement_text,
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
    requirements = _requirements(contract, blueprint)
    design_sha = _sha256_bytes(_canonical_bytes(blueprint))
    preview = {
        "schemaVersion": SCHEMA_VERSION,
        "task": blueprint["task"],
        "requestSha256": _sha256_path(request_path),
        "designSha256": design_sha,
        "businessDesignSha256": business_design_sha256(blueprint),
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
        "preservedValues": blueprint["preservedValues"],
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
        else:
            raise AdapterError(f"Unsupported action {operation['action']!r}.")
        row.update({field: str(value) for field, value in operation["values"].items()})
        for field in entity["auditFields"]:
            row[field] = ""
        output[entity["name"]].append(row)
    context = _candidate_context_rows(contract, baseline, blueprint, entities)
    for entity_name, rows_by_key in context.items():
        existing = {
            _row_key(entities[entity_name], row) for row in output[entity_name]
        }
        for key, row in rows_by_key.items():
            if key not in existing:
                output[entity_name].append(row)
    for entity_name, rows in output.items():
        entity = entities[entity_name]
        rows.sort(key=lambda row: _row_key(entity, row))
    return output


def _candidate_context_rows(
    contract: dict[str, Any],
    baseline: PackageData,
    blueprint: dict[str, Any],
    entities: dict[str, dict[str, Any]] | None = None,
) -> dict[str, dict[tuple[str, ...], dict[str, str]]]:
    """Return baseline ancestor rows required by Fusion's hierarchical loader.

    Fusion skips a child row when its parent CSV has no matching row, even when
    that parent already exists in the target environment. Candidate packages
    therefore carry each existing ancestor as read-only context, with all
    service-owned audit columns blanked. Ancestors explicitly created or
    updated by the same blueprint are already candidate operation rows.
    """
    entities = entities or _entity_map(contract)
    relationships_by_child: dict[str, list[dict[str, Any]]] = {}
    for relationship in _relationship_specs(contract, entities):
        relationships_by_child.setdefault(relationship["childEntity"], []).append(
            relationship
        )
    baseline_indexes = {
        name: _row_index(baseline, entity) for name, entity in entities.items()
    }
    operations: dict[tuple[str, tuple[str, ...]], dict[str, Any]] = {}
    for operation in blueprint["operations"]:
        entity = entities[operation["entity"]]
        operations[(entity["name"], _target_tuple(entity, operation["targetKey"]))] = operation
    context: dict[str, dict[tuple[str, ...], dict[str, str]]] = {
        name: {} for name in entities
    }
    visited: set[tuple[str, tuple[str, ...]]] = set()

    def add_ancestors(child_name: str, child_values: dict[str, Any]) -> None:
        for relationship in relationships_by_child.get(child_name, []):
            parent_name = relationship["parentEntity"]
            parent = entities[parent_name]
            parent_target = {
                parent_field: child_values.get(child_field, "")
                for child_field, parent_field in relationship["fieldMap"].items()
            }
            parent_key = _target_tuple(parent, parent_target)
            identity = (parent_name, parent_key)
            if identity in visited:
                continue
            visited.add(identity)
            parent_operation = operations.get(identity)
            if parent_operation is not None:
                parent_values = dict(parent_operation["targetKey"])
                parent_values.update(parent_operation["values"])
                add_ancestors(parent_name, parent_values)
                continue
            baseline_row = baseline_indexes[parent_name].get(parent_key)
            if baseline_row is None:
                continue
            row = dict(baseline_row)
            for field in parent["auditFields"]:
                row[field] = ""
            context[parent_name][parent_key] = row
            add_ancestors(parent_name, baseline_row)

    for operation in blueprint["operations"]:
        child_values = dict(operation["targetKey"])
        child_values.update(operation["values"])
        add_ancestors(operation["entity"], child_values)
    return context


def _write_candidate(
    template: PackageData,
    baseline: PackageData,
    contract: dict[str, Any],
    rows: dict[str, list[dict[str, str]]],
    output_path: Path,
) -> None:
    rows = _canonicalize_candidate_account_segments(contract, baseline, rows)
    rows = _canonicalize_candidate_dates(contract, rows)
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
                content = template.member_bytes[member]
                member_info = template.member_infos[member]
            else:
                content = template.member_bytes[member]
                member_info = template.member_infos[member]
            archive.writestr(member_info, content)


def _canonical_account_segment_vector(value: Any, *, context: str) -> str:
    """Validate and normalize Fusion's 30-slot LF-delimited CCID vector."""
    text = "" if value is None else str(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text:
        return ""
    if not text.endswith("\n"):
        raise AdapterError(
            f"{context} must be a target-native LF-delimited account vector "
            "with a terminal LF."
        )
    segments = text[:-1].split("\n")
    if len(segments) != 30:
        raise AdapterError(
            f"{context} has {len(segments)} account slots; Fusion requires exactly 30."
        )
    populated = list(segments)
    while populated and populated[-1] == "":
        populated.pop()
    if not populated:
        raise AdapterError(
            f"{context} does not contain any populated account segments."
        )
    return "\n".join(segments) + "\n"


def _account_segment_display(value: Any) -> str:
    """Return a comparable display value for native or hyphenated input."""
    text = "" if value is None else str(value)
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if "\n" not in normalized:
        return normalized.strip()
    canonical = _canonical_account_segment_vector(
        normalized, context="Account segment value"
    )
    segments = canonical[:-1].split("\n")
    while segments and segments[-1] == "":
        segments.pop()
    return "-".join(segments)


def _canonicalize_candidate_account_segments(
    contract: dict[str, Any],
    baseline: PackageData,
    rows: dict[str, list[dict[str, str]]],
) -> dict[str, list[dict[str, str]]]:
    """Resolve display accounts to exact target-native vectors before ZIP creation.

    Business input commonly uses a concatenated display value such as
    ``01-000-1110-0000-000``. The task CSV does not accept that representation:
    it requires 30 LF-delimited slots with a terminal LF. Only combinations
    already observed in the fresh target export are eligible for conversion.
    """
    native_by_display: dict[str, set[str]] = {}
    for entity in contract["package"]["entities"]:
        entity_name = entity["name"]
        for row_number, row in enumerate(baseline.rows[entity_name], start=2):
            for field in entity["headers"]:
                if not field.endswith("CcidSegments") or not row.get(field):
                    continue
                canonical = _canonical_account_segment_vector(
                    row[field],
                    context=f"Baseline {entity_name} row {row_number} field {field}",
                )
                native_by_display.setdefault(
                    _account_segment_display(canonical), set()
                ).add(canonical)

    normalized: dict[str, list[dict[str, str]]] = {}
    entities = _entity_map(contract)
    for entity_name, source_rows in rows.items():
        entity = entities[entity_name]
        normalized_rows = []
        for row_number, source_row in enumerate(source_rows, start=2):
            row = dict(source_row)
            for field in entity["headers"]:
                if not field.endswith("CcidSegments"):
                    continue
                value = row.get(field, "")
                if value is None or str(value) == "":
                    row[field] = ""
                    continue
                context = f"Candidate {entity_name} row {row_number} field {field}"
                text = str(value).replace("\r\n", "\n").replace("\r", "\n")
                if "\n" in text:
                    row[field] = _canonical_account_segment_vector(
                        text, context=context
                    )
                    continue
                display = text.strip()
                matches = native_by_display.get(display, set())
                if not matches:
                    raise AdapterError(
                        f"{context} value {display!r} has no exact target-native "
                        "account vector in the fresh current export."
                    )
                if len(matches) != 1:
                    raise AdapterError(
                        f"{context} value {display!r} maps to multiple target-native "
                        "account vectors."
                    )
                row[field] = next(iter(matches))
            normalized_rows.append(row)
        normalized[entity_name] = normalized_rows
    return normalized


def _canonicalize_candidate_dates(
    contract: dict[str, Any],
    rows: dict[str, list[dict[str, str]]],
) -> dict[str, list[dict[str, str]]]:
    """Return import rows with every populated source date serialized as ISO.

    Fusion current-data exports can contain YYYY/MM/DD, while the CSV import
    path requires YYYY-MM-DD. This preflight runs before the output ZIP is
    opened so an unparseable date cannot leave behind a candidate archive.
    """
    entities = _entity_map(contract)
    normalized: dict[str, list[dict[str, str]]] = {}
    for entity_name, source_rows in rows.items():
        entity = entities[entity_name]
        normalized_rows = []
        for row_number, source_row in enumerate(source_rows, start=2):
            row = dict(source_row)
            for field in entity["headers"]:
                if entity["types"].get(field) != "date":
                    continue
                value = row.get(field, "")
                if value is None or str(value).strip() == "":
                    row[field] = ""
                    continue
                row[field] = _canonical_date_text(
                    value,
                    context=f"Candidate {entity_name} row {row_number} field {field}",
                )
            normalized_rows.append(row)
        normalized[entity_name] = normalized_rows
    return normalized


def _semantic_issues(
    contract: dict[str, Any],
    candidate: PackageData,
    baseline: PackageData,
    blueprint: dict[str, Any],
    requirements: list[dict[str, Any]],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    entities = _entity_map(contract)
    for entity in contract["package"]["entities"]:
        for row_number, row in enumerate(candidate.rows[entity["name"]], start=2):
            for field in entity["headers"]:
                if field.endswith("CcidSegments") and row.get(field):
                    try:
                        _canonical_account_segment_vector(
                            row[field],
                            context=(
                                f"Candidate {entity['name']} row {row_number} "
                                f"field {field}"
                            ),
                        )
                    except AdapterError as exc:
                        issues.append(
                            {
                                "code": "NONCANONICAL_ACCOUNT_SEGMENTS",
                                "message": str(exc),
                            }
                        )
                if entity["types"].get(field) != "date":
                    continue
                value = row.get(field, "")
                if not value:
                    continue
                try:
                    canonical = _canonical_date_text(
                        value,
                        context=(
                            f"Candidate {entity['name']} row {row_number} field {field}"
                        ),
                    )
                except AdapterError as exc:
                    issues.append({"code": "INVALID_DATE", "message": str(exc)})
                    continue
                if value != canonical:
                    issues.append(
                        {
                            "code": "NONCANONICAL_DATE",
                            "message": (
                                f"Candidate {entity['name']} row {row_number} field "
                                f"{field} is {value!r}; import ZIPs require {canonical!r}."
                            ),
                        }
                    )
    context_rows = _candidate_context_rows(contract, baseline, blueprint, entities)
    expected_context = {
        (entity_name, key)
        for entity_name, rows_by_key in context_rows.items()
        for key in rows_by_key
    }
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
            if not _field_values_equal(entity, field, row[field], value):
                issues.append(
                    {"code": "VALUE_MISMATCH", "message": f"{entity['name']} {key!r} {field} is {row[field]!r}, expected {str(value)!r}."}
                )
        if operation.get("preserveOtherValues", True):
            if operation["action"] == "update":
                allowed = set(operation["values"]) | set(entity["auditFields"])
                for field in entity["headers"]:
                    if field not in allowed and not _field_values_equal(
                        entity, field, row[field], before[field]
                    ):
                        issues.append(
                            {"code": "UNEXPECTED_CHANGE", "message": f"{entity['name']} {key!r} changed preserved field {field}."}
                        )
            else:
                allowed = (
                    set(operation["values"])
                    | set(entity["keyFields"])
                    | set(entity["auditFields"])
                )
                for field in entity["headers"]:
                    if field not in allowed and row[field] != "":
                        issues.append(
                            {"code": "UNEXPECTED_CREATE_VALUE", "message": f"{entity['name']} {key!r} populated unrequested create field {field}."}
                        )
        for field in entity["auditFields"]:
            if row[field] != "":
                issues.append(
                    {"code": "AUDIT_FIELD_POPULATED", "message": f"{entity['name']} {key!r} audit field {field} is not blank."}
                )
    for entity_name, rows_by_key in context_rows.items():
        entity = entities[entity_name]
        candidate_rows = _row_index(candidate, entity)
        for key, expected in rows_by_key.items():
            row = candidate_rows.get(key)
            if row is None:
                issues.append(
                    {
                        "code": "MISSING_PARENT_CONTEXT",
                        "message": f"Candidate lacks required ancestor context row {entity_name} {key!r}.",
                    }
                )
                continue
            for field in entity["headers"]:
                expected_value = "" if field in entity["auditFields"] else expected[field]
                if not _field_values_equal(entity, field, row[field], expected_value):
                    issues.append(
                        {
                            "code": "PARENT_CONTEXT_CHANGED",
                            "message": (
                                f"Ancestor context {entity_name} {key!r} changed {field}; "
                                "only blank service-owned audit fields are allowed."
                            ),
                        }
                    )
    for entity in contract["package"]["entities"]:
        for row in candidate.rows[entity["name"]]:
            identity = (entity["name"], _row_key(entity, row))
            if identity not in expected_targets and identity not in expected_context:
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
    if candidate.member_bytes[metadata_member] != template.member_bytes[metadata_member]:
        issues.append(
            {
                "code": "METADATA_PROVENANCE",
                "message": (
                    f"{metadata_member} must be preserved byte-for-byte from the genuine "
                    "template-only export, not the current-data baseline."
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
            passed = (
                candidate_row is not None
                and persisted_row is not None
                and _field_values_equal(entity, field, candidate_value, requested)
                and _field_values_equal(entity, field, persisted_value, requested)
            )
        elif kind in {"preserve_target", "unset_target"}:
            operation = operation_map[requirement["operationId"]]
            differences = []
            if kind == "unset_target":
                if operation["action"] != "create":
                    differences.append("requirement/action mismatch")
                allowed = (
                    set(operation["values"])
                    | set(entity["keyFields"])
                    | set(entity["auditFields"])
                )
                if candidate_row is None or persisted_row is None:
                    differences.append("target row unavailable")
                else:
                    for field in entity["headers"]:
                        if field not in allowed and candidate_row[field] != "":
                            differences.append(field)
                requested = "not explicitly set"
                candidate_value = "unset" if not differences else differences
                persisted_value = (
                    "present; service defaults allowed" if persisted_row is not None else "missing"
                )
                passed = not differences
                detail = (
                    "Create candidate left every non-requested, non-key, non-audit field "
                    "unset; persisted service defaults are allowed."
                )
            else:
                allowed = set(operation["values"]) | set(entity["auditFields"])
                if before is None or candidate_row is None or persisted_row is None:
                    differences.append("target row unavailable")
                else:
                    for field in entity["headers"]:
                        if field not in allowed and (
                            not _field_values_equal(entity, field, candidate_row[field], before[field])
                            or not _field_values_equal(entity, field, persisted_row[field], before[field])
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
                for row_key in sorted(set(baseline_rows) | set(persisted_rows)):
                    if (entity_name, row_key) in touched:
                        continue
                    left = baseline_rows.get(row_key)
                    right = persisted_rows.get(row_key)
                    if left is None or right is None:
                        differences.append(f"{entity_name}:{row_key}:row")
                        continue
                    for field in current_entity["headers"]:
                        if field not in current_entity["auditFields"] and not _field_values_equal(
                            current_entity, field, left[field], right[field]
                        ):
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
    if template_only:
        _validate_template_node_sequences(contract, package)
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
