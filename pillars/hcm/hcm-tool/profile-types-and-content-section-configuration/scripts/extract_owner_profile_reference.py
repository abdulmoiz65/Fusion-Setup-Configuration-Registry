#!/usr/bin/env python3
"""Extract one immutable owning-profile reference from a current FSM export.

The input archive is evidence only: this utility never changes, repackages, or
submits it. Its small JSON output can supply owner metadata to the separate
empty-template candidate builder when the documented REST owner provider is unavailable.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path


TASK_MARKER = "HRT_MANAGE_PROFILE_TYPES"
METADATA_MEMBER = "ASM_SETUP_CSV_METADATA.xml"
PROFILE_MEMBER = "HRT_PROFILE_TYPES_B.csv"
PROFILE_TYPES = {1: "PERSON", 2: "JOB", 3: "POSITION", 4: "ORGANIZATION", 5: "TEMPLATE",
                 10: "REQUISITION", 11: "PREREQUISITE", 12: "GUIDE"}
REQUIRED_OWNER_FIELDS = {"Description", "Summary", "ProfileStatusCode", "DateFrom", "DateTo",
                         "PidApprovalFlag", "ModuleId"}


class ReferenceError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReferenceError(message)


def _safe_archive(path: Path) -> zipfile.ZipFile:
    require(path.is_file() and zipfile.is_zipfile(path), "Reference export must be a readable ZIP file.")
    archive = zipfile.ZipFile(path)
    names = archive.namelist()
    require(len(names) == len(set(names)), "Reference export contains duplicate member names.")
    for name in names:
        member = Path(name)
        require(not member.is_absolute() and ".." not in member.parts, f"Unsafe ZIP member: {name}")
    require(archive.testzip() is None, "Reference export failed its CRC check.")
    require(names.count(METADATA_MEMBER) == 1, "Reference export must contain exactly one metadata marker.")
    require(names.count(PROFILE_MEMBER) == 1, "Reference export must contain exactly one HRT_PROFILE_TYPES_B.csv member.")
    require(TASK_MARKER.encode("utf-8") in archive.read(METADATA_MEMBER),
            "Reference export metadata marker is not for HRT_MANAGE_PROFILE_TYPES.")
    return archive


def extract(archive_path: Path, profile_type_id: int, profile_type_code: str) -> dict:
    require(PROFILE_TYPES.get(profile_type_id) == profile_type_code,
            "Profile type ID and code are not an exact seeded pair.")
    with _safe_archive(archive_path) as archive:
        try:
            text = archive.read(PROFILE_MEMBER).decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ReferenceError("HRT_PROFILE_TYPES_B.csv is not UTF-8 CSV.") from exc
        reader = csv.DictReader(io.StringIO(text))
        require(reader.fieldnames is not None and len(reader.fieldnames) == len(set(reader.fieldnames)),
                "HRT_PROFILE_TYPES_B.csv has an invalid header.")
        rows = list(reader)
        matches = [row for row in rows if (row.get("ProfileTypeCode") or "").strip().upper() == profile_type_code]
        require(len(matches) == 1,
                f"Reference export must contain exactly one {profile_type_code} owning profile row; found {len(matches)}.")
        row = {key: value.strip() if isinstance(value, str) else value for key, value in matches[0].items()}
        supplied_id = (row.get("ProfileTypeId") or "").strip()
        require(not supplied_id or supplied_id == str(profile_type_id),
                "Reference export profile type ID conflicts with the requested seeded profile type.")
        required = set(REQUIRED_OWNER_FIELDS)
        if profile_type_id == 1:
            required.add("AutoCreateFlag")
        missing = sorted(field for field in required if not (row.get(field) or "").strip())
        require(not missing, "Reference export owning profile row is incomplete: " + ", ".join(missing))
        row["ProfileTypeId"] = profile_type_id
        row["ProfileTypeCode"] = profile_type_code
        return {
            "count": 1,
            "hasMore": False,
            "items": [row],
            "provenance": {
                "kind": "approved_unchanged_fsm_current_data_export_reference",
                "source_archive_sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(),
                "source_member": PROFILE_MEMBER,
                "source_profile_type_code": profile_type_code,
            },
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-export", required=True, type=Path)
    parser.add_argument("--profile-type-id", required=True, type=int)
    parser.add_argument("--profile-type-code", required=True, choices=sorted(set(PROFILE_TYPES.values())))
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        result = extract(args.reference_export, args.profile_type_id, args.profile_type_code)
        result["status"] = "planned" if args.dry_run else "prepared"
        result["reference_export"] = str(args.reference_export)
        result["output"] = str(args.output)
        if not args.dry_run:
            require(not args.output.exists(), f"Output already exists: {args.output}")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (OSError, ReferenceError) as exc:
        print(json.dumps({"status": "blocked", "failure_class": "catalog_or_metadata_mismatch", "message": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
