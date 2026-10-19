#!/usr/bin/env python3
"""Generate and validate deterministic Trading Community CX Import CSV files."""

from __future__ import annotations

import argparse
import csv
import decimal
import hashlib
import io
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any, Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
REPOSITORY_ROOT = SCRIPT_DIR.parents[6]
PROJECT_ROOT = REPOSITORY_ROOT / "project"
PROFILE_PATH = SKILL_DIR / "references" / "object-profiles.json"
CONTRACT_PATH = SKILL_DIR / "references" / "column-contracts.json"
FIELD_CONTRACT_PATH = SKILL_DIR / "references" / "field-contracts.json"
ROW_LIMITS = {"low": 50_000, "high": 500_000}
MAX_FILE_BYTES = 250 * 1024 * 1024
PROSPECT_TYPE_CODE = "ZCA_PROSPECT"
CUSTOMER_TYPE_CODE = "ZCA_CUSTOMER"
ACCOUNT_TYPE_DISPLAY_MEANINGS = {
    "PROSPECT": PROSPECT_TYPE_CODE,
    "CUSTOMER": CUSTOMER_TYPE_CODE,
}
ACCOUNT_ADDRESS_FIELDS = ("AddressLine1", "City", "Country")

class CsvContractError(ValueError):
    """Raised when source data cannot safely become a CX Import CSV."""


def load_catalogs() -> tuple[
    dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]
]:
    profiles_payload = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    contracts_payload = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    field_contracts_payload = json.loads(FIELD_CONTRACT_PATH.read_text(encoding="utf-8"))
    profiles = {item["object_code"]: item for item in profiles_payload["objects"]}
    contracts = contracts_payload["contracts"]
    field_contracts = field_contracts_payload["objects"]
    if not (set(profiles) == set(contracts) == set(field_contracts)):
        missing_profiles = sorted((set(contracts) | set(field_contracts)) - set(profiles))
        missing_contracts = sorted(set(profiles) - set(contracts))
        missing_field_contracts = sorted(set(profiles) - set(field_contracts))
        raise CsvContractError(
            "Profile/contract mismatch; "
            f"missing profiles={missing_profiles}, missing contracts={missing_contracts}, "
            f"missing field contracts={missing_field_contracts}."
        )
    for code, contract in contracts.items():
        field_names = [field["column_name"] for field in field_contracts[code]["fields"]]
        if contract["full_headers"] != field_names:
            raise CsvContractError(f"Column and field contract order differs for {code}.")
    return profiles, contracts, field_contracts


PROFILES, CONTRACTS, FIELD_CONTRACTS = load_catalogs()


def resolve_object(value: str) -> tuple[dict[str, Any], dict[str, Any]]:
    normalized = value.strip().casefold()
    matches = [
        profile for profile in PROFILES.values()
        if normalized in {profile["object_code"].casefold(), profile["display_name"].casefold()}
    ]
    if len(matches) != 1:
        choices = ", ".join(profile["display_name"] for profile in PROFILES.values())
        raise CsvContractError(
            f"Select one exact import object; {value!r} is not an unambiguous object. Supported: {choices}."
        )
    profile = matches[0]
    return profile, CONTRACTS[profile["object_code"]]


def is_within(path: Path, parent: Path) -> bool:
    resolved = path.resolve()
    resolved_parent = parent.resolve()
    return resolved == resolved_parent or resolved_parent in resolved.parents


def require_safe_data_path(path: Path, *, label: str) -> None:
    if is_within(path, PROJECT_ROOT):
        raise CsvContractError(
            f"{label} must not be stored under project/ because it may contain customer data."
        )


def validate_csv_filename(path: Path) -> None:
    if path.suffix.lower() != ".csv":
        raise CsvContractError("CSV output must use a .csv extension.")
    if len(path.name) > 40:
        raise CsvContractError("CSV filename must be 40 characters or fewer.")
    if path.name in {".csv", "..csv"}:
        raise CsvContractError("CSV output filename is invalid.")


def normalise_value(value: Any, *, row_number: int, field: str) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        raise CsvContractError(
            f"Row {row_number} field {field} must be a string or null; preserve identifiers as strings."
        )
    if "\x00" in value:
        raise CsvContractError(f"Row {row_number} field {field} contains a NUL byte.")
    if "\r" in value or "\n" in value:
        raise CsvContractError(f"Row {row_number} field {field} contains an unsupported line break.")
    return value


def read_json_records(path: Path) -> list[dict[str, str]]:
    require_safe_data_path(path, label="Source record file")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        payload = payload.get("records")
    if not isinstance(payload, list) or not payload:
        raise CsvContractError("Records JSON must be a nonempty array or contain a nonempty records array.")
    records: list[dict[str, str]] = []
    for row_number, record in enumerate(payload, start=2):
        if not isinstance(record, dict):
            raise CsvContractError(f"Row {row_number} must be a JSON object.")
        normalized: dict[str, str] = {}
        for field, value in record.items():
            if not isinstance(field, str) or not field:
                raise CsvContractError(f"Row {row_number} contains an invalid field name.")
            normalized[field] = normalise_value(value, row_number=row_number, field=field)
        records.append(normalized)
    return records


def read_target_values(path: Path | None, *, object_code: str) -> dict[str, set[str]]:
    if path is None:
        return {}
    require_safe_data_path(path, label="Target-values file")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise CsvContractError("Target-values file must contain a JSON object.")
    if payload.get("objectCode") != object_code:
        raise CsvContractError(
            f"Target-values objectCode must be {object_code}; received {payload.get('objectCode')!r}."
        )
    if payload.get("source") != "fusion-runtime":
        raise CsvContractError("Target-values source must be fusion-runtime.")
    fields = payload.get("fields")
    if not isinstance(fields, dict) or not fields:
        raise CsvContractError("Target-values file must contain a nonempty fields object.")
    allowed_fields = set(CONTRACTS[object_code]["full_headers"])
    unknown_fields = sorted(set(fields) - allowed_fields)
    if unknown_fields:
        raise CsvContractError("Target-values file contains unknown fields: " + ", ".join(unknown_fields))
    resolved: dict[str, set[str]] = {}
    for field, values in fields.items():
        if not isinstance(values, list) or not values or not all(
            isinstance(value, str) and value.strip() for value in values
        ):
            raise CsvContractError(
                f"Target-values field {field} must contain a nonempty array of nonblank strings."
            )
        if len(values) != len(set(values)):
            raise CsvContractError(f"Target-values field {field} contains duplicate values.")
        resolved[field] = set(values)
    return resolved


def parse_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    require_safe_data_path(path, label="Source CSV")
    content = path.read_bytes()
    if not content:
        raise CsvContractError("Source CSV is empty.")
    if len(content) > MAX_FILE_BYTES:
        raise CsvContractError("Source CSV exceeds the 250 MB file-size limit.")
    if b"\x00" in content:
        raise CsvContractError("Source CSV contains a NUL byte.")
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise CsvContractError("Source CSV must contain valid UTF-8 text.") from exc
    try:
        rows = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error as exc:
        raise CsvContractError(f"Source CSV has malformed quoting: {exc}.") from exc
    if not rows or not rows[0]:
        raise CsvContractError("Source CSV must contain a header row.")
    headers = rows[0]
    if any(not header or header != header.strip() for header in headers):
        raise CsvContractError("CSV headers must be nonblank and must not have surrounding whitespace.")
    if len(set(headers)) != len(headers):
        raise CsvContractError("CSV headers must be unique.")
    if len(rows) == 1:
        raise CsvContractError("Source CSV must contain at least one data row.")
    records: list[dict[str, str]] = []
    for row_number, row in enumerate(rows[1:], start=2):
        if not row or all(not cell.strip() for cell in row):
            raise CsvContractError(f"Row {row_number} is blank.")
        if len(row) != len(headers):
            raise CsvContractError(
                f"Row {row_number} has {len(row)} columns but the header has {len(headers)}."
            )
        records.append({
            header: normalise_value(value, row_number=row_number, field=header)
            for header, value in zip(headers, row)
        })
    return headers, records


def resolve_volume(profile: dict[str, Any], requested: str | None) -> str:
    volume = requested or profile["default_volume"]
    policy = profile["volume_policy"]
    if policy == "fixed-high" and volume != "high":
        raise CsvContractError(f'{profile["display_name"]} requires high-volume mode.')
    if policy == "fixed-low" and volume != "low":
        raise CsvContractError(f'{profile["display_name"]} requires standard (low) volume mode.')
    return volume


def validate_selection(
    profile: dict[str, Any], operation: str, parent_object: str | None, volume: str | None
) -> str:
    if operation not in profile["operations"]:
        supported = ", ".join(profile["operations"])
        raise CsvContractError(
            f'{profile["display_name"]} does not support {operation}; supported: {supported}.'
        )
    parents = profile["parents"]
    if parents:
        if not parent_object:
            raise CsvContractError(
                f'{profile["display_name"]} requires --parent-object; choose one of: {", ".join(parents)}.'
            )
        if parent_object not in parents:
            raise CsvContractError(
                f'Parent {parent_object!r} is invalid for {profile["display_name"]}; choose: {", ".join(parents)}.'
            )
    elif parent_object:
        raise CsvContractError(f'{profile["display_name"]} is top-level and does not accept --parent-object.')
    return resolve_volume(profile, volume)


def normalize_operation(operation: str) -> str:
    """Map the user-facing update alias to CX Import Management create-or-update."""
    return "create-or-update" if operation == "update" else operation


def select_headers(
    profile: dict[str, Any], contract: dict[str, Any], operation: str,
    records: Iterable[dict[str, str]] = (), *, full: bool = False,
    requested: Iterable[str] = (), include_defaults: bool = True,
) -> list[str]:
    full_headers = contract["full_headers"]
    allowed = set(full_headers)
    requested_set = set(requested)
    record_keys = {key for record in records for key in record}
    unknown = sorted((requested_set | record_keys) - allowed)
    if unknown:
        raise CsvContractError("Unknown columns: " + ", ".join(unknown))
    selected = set(full_headers if full else profile["default_headers"].get(operation, []) if include_defaults else [])
    selected.update(requested_set)
    selected.update(record_keys)
    return [header for header in full_headers if header in selected]


def has_value(record: dict[str, str], field: str) -> bool:
    return bool(record.get(field, "").strip())


def complete_identity(record: dict[str, str], identity_set: list[str]) -> bool:
    return all(has_value(record, field) for field in identity_set)


def validate_field_shape(
    field_contract: dict[str, Any], value: str, *, row_number: int
) -> str | None:
    if not value:
        return None
    field = field_contract["column_name"]
    data_type = field_contract["data_type"]
    length = field_contract.get("length")
    if data_type == "String" and isinstance(length, int) and len(value) > length:
        return f"Row {row_number}: {field} exceeds its maximum length of {length} characters."
    if data_type in {"Integer", "Long"} and not re.fullmatch(r"[+-]?\d+", value):
        return f"Row {row_number}: {field} must be an integer value for data type {data_type}."
    if data_type in {"BigDecimal", "Double"}:
        try:
            parsed = decimal.Decimal(value)
        except decimal.InvalidOperation:
            return f"Row {row_number}: {field} must be numeric for data type {data_type}."
        if not parsed.is_finite():
            return f"Row {row_number}: {field} must be a finite numeric value."
    allowed_values = field_contract.get("allowed_values")
    if allowed_values and value not in allowed_values:
        return (
            f"Row {row_number}: {field} must be one of the stored allowed values: "
            + ", ".join(allowed_values) + "."
        )
    return None


def is_destructive(profile: dict[str, Any], operation: str, records: list[dict[str, str]]) -> bool:
    if operation == "delete":
        return True
    semantic_marker = {
        "Assets": ("DeleteFlag", "Y"),
        "DedupLink": ("LinkStatus", "I"),
        "LinkMember": ("MemberStatus", "I"),
        "PartySourceSystemReference": ("Status", "I"),
    }.get(profile["object_code"])
    return bool(
        semantic_marker and any(
            record.get(semantic_marker[0], "").strip().upper() == semantic_marker[1]
            for record in records
        )
    )


def validate_records(
    profile: dict[str, Any], operation: str, volume: str,
    records: list[dict[str, str]], *, allow_party_id_identity: bool,
    target_values: dict[str, set[str]] | None = None,
) -> list[str]:
    object_code = profile["object_code"]
    if len(records) > ROW_LIMITS[volume]:
        raise CsvContractError(
            f"{volume}-volume mode permits at most {ROW_LIMITS[volume]} records per CSV."
        )
    warnings: list[str] = []
    errors: list[str] = []
    identity_source = (
        profile.get("delete_identity_sets", profile["identity_sets"])
        if operation == "delete"
        else profile["identity_sets"]
    )
    identities = [list(fields) for fields in identity_source]
    field_contracts = {
        field["column_name"]: field for field in FIELD_CONTRACTS[object_code]["fields"]
    }
    create_required_fields = FIELD_CONTRACTS[object_code]["required_fields"]["create"]
    if allow_party_id_identity and "PartyId" in CONTRACTS[object_code]["full_headers"]:
        identities.append(["PartyId"])
    seen: dict[tuple[str, ...], int] = {}
    target_values = target_values or {}

    if object_code == "LinkedParty" and "LinkType" not in target_values:
        errors.append(
            "Linked Party requires target-active LinkType values from --target-values-json; "
            "resolve them from the exact Fusion environment before preview."
        )

    for row_number, record in enumerate(records, start=2):
        for field, value in record.items():
            shape_error = validate_field_shape(field_contracts[field], value, row_number=row_number)
            if shape_error:
                errors.append(shape_error)
            active_values = target_values.get(field)
            if value and active_values is not None and value not in active_values:
                errors.append(
                    f"Row {row_number}: {field} value {value!r} is not active in the exact target; "
                    "valid target values: " + ", ".join(sorted(active_values)) + "."
                )

        for left, right in (
            ("SourceSystem", "SourceSystemReferenceValue"),
            ("PartySourceSystem", "PartySourceSystemReferenceValue"),
            ("SiteSourceSystem", "SiteSourceSystemReferenceValue"),
            ("RelationshipSourceSystem", "RelationshipSourceSystemReferenceValue"),
            ("AssetOrigSystem", "AssetOrigSystemReference"),
            ("AccountSourceSystem", "AccountSourceSystemReference"),
            ("ContactSourceSystem", "ContactSourceSystemReference"),
            ("ItemSourceSystem", "ItemSourceSystemReference"),
        ):
            if (left in record or right in record) and has_value(record, left) != has_value(record, right):
                errors.append(f"Row {row_number}: {left} and {right} must be supplied together.")

        matched = [fields for fields in identities if complete_identity(record, fields)]
        if operation in {"create-or-update", "delete"} and not matched:
            readable = " or ".join(" + ".join(fields) for fields in identities)
            errors.append(f"Row {row_number}: provide a complete identity: {readable}.")
        for fields in matched:
            key = tuple(["|".join(fields)] + [record[field].strip() for field in fields])
            if key in seen:
                errors.append(f"Row {row_number}: duplicate identity already used by row {seen[key]}.")
            else:
                seen[key] = row_number

        if operation == "create":
            missing = [field for field in create_required_fields if not has_value(record, field)]
            if missing:
                errors.append(f"Row {row_number}: required create fields are missing: {', '.join(missing)}.")

        if operation == "delete":
            allowed = {field for fields in identities for field in fields}
            nonidentity = sorted(field for field, value in record.items() if value.strip() and field not in allowed)
            if nonidentity:
                errors.append(
                    f'Row {row_number}: {profile["display_name"]} deletion accepts identifier fields only; remove '
                    + ", ".join(nonidentity) + "."
                )

        if object_code == "Account" and operation in {"create", "create-or-update"}:
            account_type = record.get("Type", "").strip().upper()
            if account_type in ACCOUNT_TYPE_DISPLAY_MEANINGS:
                errors.append(
                    f"Row {row_number}: {account_type} is a display meaning; use the exact active lookup code "
                    f"{ACCOUNT_TYPE_DISPLAY_MEANINGS[account_type]}."
                )
            elif operation == "create" and account_type != PROSPECT_TYPE_CODE:
                missing = [field for field in ACCOUNT_ADDRESS_FIELDS if not has_value(record, field)]
                if missing:
                    errors.append(
                        f"Row {row_number}: a Customer or unclassified Account requires AddressLine1, City, and Country; missing: {', '.join(missing)}."
                    )
            elif operation == "create-or-update" and any(
                has_value(record, field) for field in ACCOUNT_ADDRESS_FIELDS
            ):
                missing = [field for field in ACCOUNT_ADDRESS_FIELDS if not has_value(record, field)]
                if missing:
                    errors.append(
                        f"Row {row_number}: an Account address update must supply AddressLine1, City, and Country together; missing: {', '.join(missing)}."
                    )
            if account_type == PROSPECT_TYPE_CODE and operation == "create":
                warnings.append(
                    f"Row {row_number}: Prospect address exception applied; confirm {PROSPECT_TYPE_CODE} in the target lookup."
                )
            if account_type == CUSTOMER_TYPE_CODE:
                warnings.append(
                    f"Row {row_number}: {CUSTOMER_TYPE_CODE} establishes the sales Account classification/"
                    "SALES_ACCOUNT usage; it does not establish the separate financial CUSTOMER usage."
                )
            if volume == "low" and operation == "create" and not (
                has_value(record, "OwnerPartyId") or has_value(record, "OwnerPartyNumber")
            ):
                warnings.append(f"Row {row_number}: ownerless Account create requires assignment/access review.")

        if object_code == "Assets" and operation == "create" and not (
            has_value(record, "CustomerId")
            or has_value(record, "CustomerPartyNumber")
            or (
                has_value(record, "AccountSourceSystem")
                and has_value(record, "AccountSourceSystemReference")
            )
        ):
            errors.append(
                f"Row {row_number}: Asset requires an owner identity: CustomerId, "
                "CustomerPartyNumber, or AccountSourceSystem + AccountSourceSystemReference."
            )
        if object_code == "Assets" and operation == "create" and not (
            has_value(record, "ProdGroupId")
            or (
                has_value(record, "InventoryItemId")
                and has_value(record, "InventoryOrgId")
            )
        ):
            errors.append(
                f"Row {row_number}: Asset requires a product identity: ProdGroupId, "
                "or InventoryItemId + InventoryOrgId."
            )

        if object_code == "AssetContact" and operation == "create":
            if not (has_value(record, "AssetId") or has_value(record, "AssetNumber")):
                errors.append(f"Row {row_number}: Asset Contact requires AssetId or AssetNumber.")
            if not (
                has_value(record, "ContactPartyId")
                or has_value(record, "ContactPartyNumber")
                or (
                    has_value(record, "ContactSourceSystem")
                    and has_value(record, "ContactSourceSystemReference")
                )
            ):
                errors.append(
                    f"Row {row_number}: Asset Contact requires ContactPartyId, ContactPartyNumber, "
                    "or ContactSourceSystem + ContactSourceSystemReference."
                )

        if object_code == "AssetResource" and operation == "create":
            if not (has_value(record, "AssetId") or has_value(record, "AssetNumber")):
                errors.append(f"Row {row_number}: Asset Team Member requires AssetId or AssetNumber.")
            if not (has_value(record, "ResourceId") or has_value(record, "ResourcePartyNumber")):
                errors.append(
                    f"Row {row_number}: Asset Team Member requires ResourceId or ResourcePartyNumber."
                )

        if object_code in {"Organization", "Person"} and (
            record.get("PartyUsageCode", "").strip().upper() == "CUSTOMER"
        ):
            errors.append(
                f"Row {row_number}: CUSTOMER is conditional financial-customer usage and cannot be "
                f"assigned unconditionally through {profile['display_name']} import; use the owning "
                "customer-account workflow."
            )

        if (
            object_code == "PartySourceSystemReference"
            and operation in {"create", "create-or-update"}
            and has_value(record, "Status")
        ):
            errors.append(
                f"Row {row_number}: omit Status for Source System Reference create/update; use "
                "DELETE_RECORD for its documented semantic inactivation path."
            )

        if object_code == "AdditionalName" and operation == "create" and not (
            has_value(record, "Name") or has_value(record, "FirstName") or has_value(record, "LastName")
        ):
            errors.append(f"Row {row_number}: provide Name or person-name fields for Additional Name.")
        if object_code == "HierarchyNode" and operation == "create" and not (
            has_value(record, "PartyId") or has_value(record, "PartyNumber")
            or (has_value(record, "PartyOrigSystem") and has_value(record, "PartyOrigSysRef"))
        ):
            errors.append(f"Row {row_number}: Hierarchy Member requires a complete party identity.")
        if object_code == "LinkedParty" and not (
            (has_value(record, "PartyId") and has_value(record, "RelatedPartyId"))
            or (has_value(record, "PartyNumber") and has_value(record, "RelatedPartyNumber"))
        ):
            errors.append(f"Row {row_number}: Linked Party requires both main and related party identities.")
        elif object_code == "LinkedParty":
            warnings.append(
                f"Row {row_number}: verify live usages before approval: the main party must have "
                "SALES_PROSPECT or SALES_ACCOUNT and the related party must have financial CUSTOMER."
            )
        if object_code == "Relationship" and not (
            (has_value(record, "SubjectPartyId") or has_value(record, "SubjectPartyNumber"))
            and (has_value(record, "ObjectPartyId") or has_value(record, "ObjectPartyNumber"))
        ):
            errors.append(f"Row {row_number}: Relationship requires subject and object party identities.")
        if volume == "high":
            null_fields = sorted(field for field, value in record.items() if value.strip() == "#NULL")
            if null_fields:
                errors.append(f"Row {row_number}: high-volume import does not accept #NULL in {', '.join(null_fields)}.")

    if object_code == "Account" and operation == "create" and not any(
        complete_identity(record, fields) for record in records for fields in identities
    ):
        warnings.append("Account CREATE_ONLY may use Fusion-generated identities; source-system keys are recommended.")
    if object_code == "LinkMember" and operation == "create":
        members_by_link: dict[str, list[tuple[int, dict[str, str]]]] = {}
        for row_number, record in enumerate(records, start=2):
            link_number = record.get("LinkNumber", "").strip()
            members_by_link.setdefault(link_number, []).append((row_number, record))
            master_flag = record.get("MasterFlag", "").strip().upper()
            if master_flag not in {"Y", "N"}:
                errors.append(f"Row {row_number}: MasterFlag must be Y or N for a new Resolution Link.")
            member_status = record.get("MemberStatus", "").strip().upper()
            if member_status != "A":
                errors.append(f"Row {row_number}: MemberStatus must be A for a new Resolution Link.")
        for link_number, members in members_by_link.items():
            master_count = sum(
                record.get("MasterFlag", "").strip().upper() == "Y"
                for _, record in members
            )
            if master_count != 1:
                label = link_number or "<missing LinkNumber>"
                errors.append(
                    f"Resolution Link {label}: exactly one member must have MasterFlag=Y; "
                    f"found {master_count}."
                )
    if allow_party_id_identity and any(has_value(record, "PartyId") for record in records):
        warnings.append("PartyId identity was explicitly enabled; confirm it against target metadata.")
    if is_destructive(profile, operation, records):
        warnings.append(f'Deletion behavior: {profile["delete_semantics"]}. Separate approval is required.')
    if profile["verification_strategy"] == "hierarchy-post-process":
        warnings.append("Run and verify Party Hierarchy Generation after the import succeeds.")
    if errors:
        preview = errors[:100]
        if len(errors) > 100:
            preview.append(f"{len(errors) - 100} additional errors omitted.")
        raise CsvContractError("\n".join(preview))
    return warnings


def render_csv(headers: list[str], records: list[dict[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\r\n", quoting=csv.QUOTE_MINIMAL)
    writer.writerow(headers)
    for record in records:
        writer.writerow([record.get(header, "") for header in headers])
    content = buffer.getvalue().encode("utf-8")
    if len(content) > MAX_FILE_BYTES:
        raise CsvContractError("Generated CSV exceeds the 250 MB file-size limit.")
    return content


def verify_round_trip(content: bytes, headers: list[str], records: list[dict[str, str]]) -> None:
    rows = list(csv.reader(io.StringIO(content.decode("utf-8"), newline=""), strict=True))
    expected = [headers] + [[record.get(header, "") for header in headers] for record in records]
    if rows != expected:
        raise CsvContractError("Generated CSV failed deterministic round-trip verification.")


def atomic_write(path: Path, content: bytes, *, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise CsvContractError(f"Output already exists: {path}. Use --overwrite only after approval.")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as temporary:
            temporary.write(content)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_name = temporary.name
        os.replace(temporary_name, path)
    finally:
        if temporary_name and Path(temporary_name).exists():
            Path(temporary_name).unlink()


def build_report(
    *, status: str, profile: dict[str, Any], parent_object: str | None, operation: str,
    volume: str, output: Path, content: bytes, headers: list[str], row_count: int,
    warnings: list[str], destructive: bool, target_validated_fields: Iterable[str] = (),
) -> dict[str, Any]:
    return {
        "status": status,
        "displayName": profile["display_name"],
        "objectCode": profile["object_code"],
        "parentObject": parent_object,
        "operation": operation,
        "importMode": {"create": "CREATE_ONLY", "create-or-update": "CREATE_RECORD", "delete": "DELETE_RECORD"}[operation],
        "volumePolicy": profile["volume_policy"],
        "highVolume": "YES" if volume == "high" else "NO",
        "activate": "YES",
        "schedule": "ONE_TIME_IMMEDIATE",
        "outputFile": str(output.resolve()),
        "fileName": output.name,
        "rowCount": row_count,
        "columnCount": len(headers),
        "headers": headers,
        "fieldContract": "references/field-contracts.json",
        "fieldContractCount": FIELD_CONTRACTS[profile["object_code"]]["field_count"],
        "bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
        "deleteSemantics": profile["delete_semantics"],
        "destructiveApprovalRequired": destructive,
        "verificationStrategy": profile["verification_strategy"],
        "targetValidatedFields": sorted(target_validated_fields),
        "warnings": warnings,
    }


def write_report(path: Path | None, report: dict[str, Any], *, overwrite: bool) -> None:
    if path:
        atomic_write(path, (json.dumps(report, indent=2, sort_keys=True) + "\n").encode(), overwrite=overwrite)


def add_contract_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--object", dest="object_name", required=True, help="Exact display name or object code.")
    parser.add_argument("--parent-object", help="Exact parent choice for a child object, including Household where listed.")
    parser.add_argument(
        "--operation", choices=["create", "update", "create-or-update", "delete"], required=True,
        help="Use update or create-or-update for ImportMode CREATE_RECORD.",
    )
    parser.add_argument("--volume", choices=["low", "high"], help="Omit to use the profile default.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate and validate Trading Community CX Import CSV files.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("profiles", help="List supported objects, operations, parents, and volume policies.")
    fields = subparsers.add_parser("fields", help="List column, type, length, and requiredness metadata.")
    fields.add_argument("--object", dest="object_name", required=True, help="Exact display name or object code.")
    fields.add_argument("--column", help="Return one exact import column.")
    fields.add_argument("--required-only", action="store_true", help="Return skill-required create fields only.")
    template = subparsers.add_parser("template", help="Generate a header-only CSV template.")
    add_contract_arguments(template)
    template.add_argument("--full", action="store_true")
    template.add_argument("--column", action="append", default=[])
    template.add_argument("--output", type=Path, required=True)
    template.add_argument("--report", type=Path)
    template.add_argument("--overwrite", action="store_true")
    prepare = subparsers.add_parser("prepare", help="Create a validated CSV from JSON or CSV records.")
    add_contract_arguments(prepare)
    source = prepare.add_mutually_exclusive_group(required=True)
    source.add_argument("--records-json", type=Path)
    source.add_argument("--input-csv", type=Path)
    prepare.add_argument("--full", action="store_true")
    prepare.add_argument("--allow-party-id-identity", action="store_true")
    prepare.add_argument(
        "--target-values-json", type=Path,
        help="Runtime Fusion allowed values keyed by exact import field; required for LinkedParty LinkType.",
    )
    prepare.add_argument("--output", type=Path, required=True)
    prepare.add_argument("--report", type=Path)
    prepare.add_argument("--overwrite", action="store_true")
    validate = subparsers.add_parser("validate", help="Validate and optionally normalize an existing CSV.")
    add_contract_arguments(validate)
    validate.add_argument("--input", type=Path, required=True)
    validate.add_argument("--allow-party-id-identity", action="store_true")
    validate.add_argument(
        "--target-values-json", type=Path,
        help="Runtime Fusion allowed values keyed by exact import field; required for LinkedParty LinkType.",
    )
    validate.add_argument("--normalized-output", type=Path)
    validate.add_argument("--report", type=Path)
    validate.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.command == "profiles":
        return {"status": "ok", "objects": [{
            key: profile[key] for key in (
                "display_name", "object_code", "parents", "operations", "volume_policy", "default_volume",
                "delete_semantics", "verification_strategy"
            )
        } | {
            "field_count": FIELD_CONTRACTS[profile["object_code"]]["field_count"],
            "required_create_fields": FIELD_CONTRACTS[profile["object_code"]]["required_fields"]["create"],
        } for profile in PROFILES.values()]}
    profile, contract = resolve_object(args.object_name)
    field_contract = FIELD_CONTRACTS[profile["object_code"]]
    if args.command == "fields":
        selected_fields = field_contract["fields"]
        if args.column:
            selected_fields = [field for field in selected_fields if field["column_name"] == args.column]
            if not selected_fields:
                raise CsvContractError(
                    f"Unknown column {args.column!r} for {profile['display_name']}."
                )
        if args.required_only:
            selected_fields = [field for field in selected_fields if field["required_for_create_by_skill"]]
        return {
            "status": "ok",
            "displayName": profile["display_name"],
            "objectCode": profile["object_code"],
            "requiredFields": field_contract["required_fields"],
            "requirednessNotes": field_contract["requiredness_notes"],
            "fields": selected_fields,
        }
    args.operation = normalize_operation(args.operation)
    volume = validate_selection(profile, args.operation, args.parent_object, args.volume)

    if args.command == "template":
        require_safe_data_path(args.output, label="CSV output")
        validate_csv_filename(args.output)
        headers = select_headers(profile, contract, args.operation, full=args.full, requested=args.column)
        content = render_csv(headers, [])
        verify_round_trip(content, headers, [])
        atomic_write(args.output, content, overwrite=args.overwrite)
        report = build_report(
            status="template_generated", profile=profile, parent_object=args.parent_object,
            operation=args.operation, volume=volume, output=args.output, content=content,
            headers=headers, row_count=0, warnings=[], destructive=args.operation == "delete",
        )
        write_report(args.report, report, overwrite=args.overwrite)
        return report

    if args.command == "prepare":
        require_safe_data_path(args.output, label="CSV output")
        validate_csv_filename(args.output)
        if args.records_json:
            source_headers: list[str] = []
            records = read_json_records(args.records_json)
        else:
            source_headers, records = parse_csv(args.input_csv)
        headers = select_headers(profile, contract, args.operation, records, full=args.full)
        if source_headers and source_headers != headers:
            raise CsvContractError("Input CSV columns must follow the downloaded template order.")
        target_values = read_target_values(args.target_values_json, object_code=profile["object_code"])
        warnings = validate_records(
            profile, args.operation, volume, records,
            allow_party_id_identity=args.allow_party_id_identity,
            target_values=target_values,
        )
        content = render_csv(headers, records)
        verify_round_trip(content, headers, records)
        atomic_write(args.output, content, overwrite=args.overwrite)
        report = build_report(
            status="validated", profile=profile, parent_object=args.parent_object,
            operation=args.operation, volume=volume, output=args.output, content=content,
            headers=headers, row_count=len(records), warnings=warnings,
            destructive=is_destructive(profile, args.operation, records),
            target_validated_fields=target_values,
        )
        write_report(args.report, report, overwrite=args.overwrite)
        return report

    source_headers, records = parse_csv(args.input)
    headers = select_headers(
        profile, contract, args.operation, records, requested=source_headers, include_defaults=False
    )
    if source_headers != headers:
        raise CsvContractError("Input CSV columns must follow the downloaded template order.")
    target_values = read_target_values(args.target_values_json, object_code=profile["object_code"])
    warnings = validate_records(
        profile, args.operation, volume, records,
        allow_party_id_identity=args.allow_party_id_identity,
        target_values=target_values,
    )
    normalized_content = render_csv(headers, records)
    verify_round_trip(normalized_content, headers, records)
    output = args.normalized_output or args.input
    if not args.normalized_output and args.input.read_bytes() != normalized_content:
        raise CsvContractError("Source is valid data but not canonical UTF-8 CRLF CSV; use --normalized-output.")
    if args.normalized_output:
        require_safe_data_path(args.normalized_output, label="Normalized CSV output")
        validate_csv_filename(args.normalized_output)
        atomic_write(args.normalized_output, normalized_content, overwrite=args.overwrite)
    content = normalized_content if args.normalized_output else args.input.read_bytes()
    report = build_report(
        status="validated", profile=profile, parent_object=args.parent_object,
        operation=args.operation, volume=volume, output=output, content=content,
        headers=headers, row_count=len(records), warnings=warnings,
        destructive=is_destructive(profile, args.operation, records),
        target_validated_fields=target_values,
    )
    write_report(args.report, report, overwrite=args.overwrite)
    return report


def main(argv: list[str] | None = None) -> int:
    try:
        report = run(parse_args(argv))
    except (CsvContractError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "failed", "failureClass": "input_validation", "message": str(exc)}))
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
