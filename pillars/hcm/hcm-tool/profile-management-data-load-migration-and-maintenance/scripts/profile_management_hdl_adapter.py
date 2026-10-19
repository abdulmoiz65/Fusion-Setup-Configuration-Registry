#!/usr/bin/env python3
"""Build a deterministic, local-only TalentProfile HDL ZIP from a validated request.

The adapter deliberately supports only sections confirmed by the configured
non-production TalentProfile template.  It never calls Fusion and it refuses
provider-blocked translation routes rather than guessing a discriminator.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Any


SECTION_BY_OBJECT = {
    "Talent Profile": ("TalentProfile", "TalentProfile.dat"),
    "Talent Profile Translation": ("TalentProfileTranslation", "TalentProfileTranslation.dat"),
}
PROVIDER_BLOCKED_OBJECTS = {
    "Content Item": "Content Item is a separate HDL root family; download and validate the target Content Item template with Value Set ID and Value Set Name before enabling a route.",
    "Content Item Relationship": "Content Item Relationship is a child of the separate Content Item HDL family; the target template and exact parent contract are not yet confirmed.",
    "Content Item Translation": "Fusion metadata detail returned HTTP 500 for ContentItemTranslation.",
    "Content Item Rating Description Translation": "No exact live discriminator is registered.",
    "Talent Model Profile Extra Information": "The public contract identifies Talent Model Profile Extra Information Translation; the standalone ModelProfileExtraInfo section is not confirmed by target metadata.",
    "Talent Model Profile Extra Information Translation": "No exact live discriminator is registered.",
    "Profile Attachment": "Oracle confirms attachments use the Talent Profile file, but the exact target attachment section and attribute contract have not been downloaded and validated.",
}
PARENT_SECTIONS = {"TalentProfileTranslation"}
FIELD_ALIASES = {
    "TalentProfile": {"ProfileName": "Description"},
    "TalentProfileTranslation": {"ProfileName": "Description"},
}
DEPENDENCIES_BY_OBJECT = {
    "Talent Profile Translation": ("installed-language",),
}


def _cell(value: Any) -> str:
    text = str(value if value is not None else "")
    if "|" in text or "\n" in text or "\r" in text:
        raise ValueError("HDL values must not contain a pipe or line break")
    return text


def _section_row(record: dict[str, Any]) -> tuple[str, str, dict[str, str]]:
    object_name = str(record.get("object") or "")
    if object_name in PROVIDER_BLOCKED_OBJECTS:
        raise ValueError(f"{object_name} is provider-blocked: {PROVIDER_BLOCKED_OBJECTS[object_name]}")
    try:
        section, filename = SECTION_BY_OBJECT[object_name]
    except KeyError as exc:
        raise ValueError(f"{object_name} has no live-confirmed AC2 HDL route") from exc
    values = record.get("values")
    if not isinstance(values, dict):
        raise ValueError(f"{object_name} values must be an object")
    aliases = FIELD_ALIASES.get(section, {})
    row = {aliases.get(str(key), str(key)): _cell(value) for key, value in values.items()}
    identifier = _cell(record.get("identifier"))
    parent = _cell(record.get("parent_identifier")) if record.get("parent_identifier") else ""
    if section == "TalentProfile":
        row.setdefault("ProfileCode", identifier)
    elif section in PARENT_SECTIONS:
        row.setdefault("ProfileCode", parent)
    if section == "TalentProfileTranslation":
        row.setdefault("Language", _cell(record.get("language")))
    return filename, section, row


def _ordered_fields(section: str, rows: list[dict[str, str]]) -> list[str]:
    preferred = {
        "TalentProfile": ["ProfileCode", "ProfileTypeCode", "ProfileTypeId", "Description", "Summary"],
        "TalentProfileTranslation": ["ProfileCode", "Language", "Description", "Summary"],
    }.get(section, [])
    available = {field for row in rows for field in row}
    return [field for field in preferred if field in available] + sorted(available.difference(preferred))


def _render_dat(sections: list[tuple[str, dict[str, str]]]) -> str:
    lines: list[str] = []
    by_section: dict[str, list[dict[str, str]]] = defaultdict(list)
    order: list[str] = []
    for section, row in sections:
        if section not in by_section:
            order.append(section)
        by_section[section].append(row)
    for section in order:
        rows = by_section[section]
        fields = _ordered_fields(section, rows)
        lines.append("METADATA|" + section + "|" + "|".join(fields))
        for row in rows:
            lines.append("MERGE|" + section + "|" + "|".join(row.get(field, "") for field in fields))
    return "\n".join(lines) + "\n"


def _configuration_sha256(configuration: Any) -> str:
    return hashlib.sha256(
        json.dumps(configuration, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    ).hexdigest()


def _validated_model_profile_configuration(request: dict[str, Any], root: dict[str, str]) -> dict[str, str]:
    """Bind a resolved owning-configuration result to this exact root profile."""
    result = request.get("model_profile_configuration")
    if not isinstance(result, dict) or result.get("status") != "resolved":
        raise ValueError("a resolved model_profile_configuration result is required for a model-profile artifact")
    match = result.get("match")
    configuration = result.get("configuration")
    supplied_hash = str(result.get("configuration_sha256") or "")
    if not isinstance(match, dict) or not isinstance(configuration, dict) or not supplied_hash:
        raise ValueError("model_profile_configuration must include match, configuration, and configuration_sha256")
    if _configuration_sha256(configuration) != supplied_hash:
        raise ValueError("model_profile_configuration SHA-256 does not match its configuration evidence")
    profile_type_code = str(match.get("ProfileTypeCode") or "").strip().upper()
    profile_type_id = str(match.get("ProfileTypeId") or "").strip()
    if not profile_type_code or not profile_type_id:
        raise ValueError("model_profile_configuration must include an exact Profile Type code and ID")
    if root.get("ProfileTypeCode", "").strip().upper() != profile_type_code:
        raise ValueError("model_profile_configuration Profile Type code does not match the TalentProfile root")
    supplied_id = root.get("ProfileTypeId", "").strip()
    if supplied_id and supplied_id != profile_type_id:
        raise ValueError("model_profile_configuration Profile Type ID does not match the TalentProfile root")
    source = configuration.get("source")
    if not isinstance(source, dict) or not str(source.get("reference") or "").strip():
        raise ValueError("model_profile_configuration requires a source reference")
    return {
        "record_identifier": root["ProfileCode"],
        "dependency": "model-profile-configuration",
        "expected_value": profile_type_code,
        "status": "exactly-one",
        "evidence_sha256": supplied_hash,
        "evidence_reference": str(source["reference"]),
    }


def _validated_dependencies(request: dict[str, Any], roots: list[dict[str, str]]) -> list[dict[str, str]]:
    """Require immutable, exact read-only evidence for every non-root dependency."""
    supplied = request.get("dependency_checks")
    if not isinstance(supplied, list):
        raise ValueError("dependency_checks is required before child-object artifact preparation")
    normalized: dict[tuple[str, str], dict[str, str]] = {}
    for check in supplied:
        if not isinstance(check, dict):
            raise ValueError("every dependency check must be an object")
        record_identifier = _cell(check.get("record_identifier"))
        dependency = _cell(check.get("dependency"))
        expected_value = _cell(check.get("expected_value"))
        status = _cell(check.get("status"))
        if not record_identifier or not dependency or not expected_value:
            raise ValueError("dependency checks require record_identifier, dependency, and expected_value")
        if status != "exactly-one":
            raise ValueError(f"dependency {dependency} for {record_identifier} must have status exactly-one")
        normalized[(record_identifier, dependency)] = {
            "record_identifier": record_identifier,
            "dependency": dependency,
            "expected_value": expected_value,
            "status": status,
        }
    required: list[dict[str, str]] = []
    for record in request.get("records") or []:
        object_name = str(record.get("object") or "")
        identifier = _cell(record.get("identifier"))
        if object_name == "Talent Profile":
            continue
        dependencies = ("parent-profile", *DEPENDENCIES_BY_OBJECT.get(object_name, ()))
        for dependency in dependencies:
            check = normalized.get((identifier, dependency))
            if check is None:
                raise ValueError(f"missing exact dependency check {dependency} for {identifier}")
            required.append(check)
    if request.get("root_record_type") == "model-profile":
        for root in roots:
            required.append(_validated_model_profile_configuration(request, root))
    return required


def _write_immutable_archive(destination: Path, grouped: dict[str, list[tuple[str, dict[str, str]]]]) -> None:
    """Create a byte-stable ZIP without ever overwriting an existing artifact."""
    if destination.exists():
        raise ValueError(f"immutable artifact destination already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent)
    os.close(fd)
    temporary = Path(temporary_name)
    created_destination = False
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for filename in sorted(grouped):
                payload = _render_dat(grouped[filename]).encode("utf-8")
                info = zipfile.ZipInfo(filename, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, payload)
        with destination.open("xb") as output, temporary.open("rb") as source:
            created_destination = True
            shutil.copyfileobj(source, output)
    except Exception:
        if created_destination:
            destination.unlink(missing_ok=True)
        raise
    finally:
        temporary.unlink(missing_ok=True)


def build_archive(request: dict[str, Any], destination: Path) -> dict[str, Any]:
    if request.get("requested_operation") not in {"create", "update", "migration", "mass-maintenance", "translation"}:
        raise ValueError("request operation is not eligible for HDL artifact preparation")
    target_status = (request.get("target_check") or {}).get("status")
    expected = "not-found" if request.get("requested_operation") == "create" else "exactly-one"
    if target_status != expected:
        raise ValueError(f"target_check.status must be {expected} before artifact preparation")
    for record in request.get("records") or []:
        object_name = str(record.get("object") or "")
        if object_name in PROVIDER_BLOCKED_OBJECTS:
            raise ValueError(f"{object_name} is provider-blocked: {PROVIDER_BLOCKED_OBJECTS[object_name]}")
    grouped: dict[str, list[tuple[str, dict[str, str]]]] = defaultdict(list)
    for record in request.get("records") or []:
        filename, section, row = _section_row(record)
        grouped[filename].append((section, row))
    if not grouped:
        raise ValueError("request contains no artifact-eligible records")
    if "TalentProfile.dat" in grouped and not any(section == "TalentProfile" for section, _ in grouped["TalentProfile.dat"]):
        raise ValueError("TalentProfile.dat requires one TalentProfile root record before child sections")
    if request.get("root_record_type") == "model-profile":
        roots = [row for section, row in grouped.get("TalentProfile.dat", []) if section == "TalentProfile"]
        for root in roots:
            missing = [field for field in ("ProfileStatusCode", "ProfileUsageCode") if not root.get(field)]
            if missing:
                raise ValueError("model-profile TalentProfile is missing required supplied fields: " + ", ".join(missing))
            if root["ProfileUsageCode"] != "M":
                raise ValueError("model-profile TalentProfile.ProfileUsageCode must be M")
    dependencies = _validated_dependencies(request, roots if request.get("root_record_type") == "model-profile" else [])
    _write_immutable_archive(destination, grouped)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    with zipfile.ZipFile(destination) as archive:
        members = [{"name": info.filename, "size": info.file_size} for info in archive.infolist()]
    return {
        "status": "prepared",
        "path": str(destination),
        "sha256": digest,
        "members": members,
        "target_check": {"status": target_status},
        "dependency_checks": dependencies,
        "execution": "not-authorized",
    }


def build_execution_preview(request: dict[str, Any], archive_result: dict[str, Any]) -> dict[str, Any]:
    """Build the AC5 review object bound to the exact immutable ZIP hash."""
    if archive_result.get("status") != "prepared" or not archive_result.get("sha256"):
        raise ValueError("a prepared immutable archive is required for execution preview")
    return {
        "status": "approval-required",
        "artifact_sha256": archive_result["sha256"],
        "artifact_members": archive_result["members"],
        "target_environment": request.get("target_environment", ""),
        "requested_operation": request.get("requested_operation", ""),
        "target_check": archive_result["target_check"],
        "dependency_checks": archive_result["dependency_checks"],
        "execution": "not-authorized",
        "approval_instruction": "Obtain a separate explicit approval that names this exact artifact SHA-256 before invoking core.data-loader.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path)
    parser.add_argument("--output-zip", required=True, type=Path)
    parser.add_argument("--preview-json", type=Path)
    args = parser.parse_args()
    try:
        request = json.loads(args.request.read_text(encoding="utf-8"))
        result = build_archive(request, args.output_zip)
        if args.preview_json:
            args.preview_json.parent.mkdir(parents=True, exist_ok=True)
            args.preview_json.write_text(json.dumps(build_execution_preview(request, result), indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "blocked", "stage": "artifact-preparation", "message": str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
