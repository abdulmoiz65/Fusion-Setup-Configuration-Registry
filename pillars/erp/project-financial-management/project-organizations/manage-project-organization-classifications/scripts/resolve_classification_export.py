#!/usr/bin/env python3
"""Read a governed task FSM data-export ZIP; never import or call Fusion.

The active workflow runs shared.setup-export.task-level-export with --data.
It supplies the completed export receipt and target-proven member/header map.
This adapter projects actual exported bytes into classification evidence.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile

from validate_project_organization_classifications_hdl import (
    TASK_CODE, CONTEXT, PERMISSIONS, classification_export, dates, identity, text)


def read_export(archive, receipt, contract, target, as_of, run_id, verify_permissions=True):
    if (not isinstance(receipt, dict) or receipt.get("Status") != "SUCCESS"
            or receipt.get("Complete") is not True or receipt.get("Fresh") is not True
            or receipt.get("Mode") != "data" or receipt.get("Scope") != "task"
            or receipt.get("TaskCode") != TASK_CODE or receipt.get("TargetEnvironment") != target
            or receipt.get("AsOfDate") != as_of or not run_id or receipt.get("RunId") != run_id
            or not receipt.get("EvidenceRef") or not receipt.get("ProcessId")):
        raise ValueError("Classification export is unavailable, incomplete, stale or not a successful task-data export.")
    if (not isinstance(contract, dict) or contract.get("Verified") is not True
            or contract.get("TaskCode") != TASK_CODE or contract.get("TargetEnvironment") != target
            or not contract.get("EvidenceRef") or not isinstance(contract.get("Members"), list)
            or not contract["Members"] or len(set(contract["Members"])) != len(contract["Members"])):
        raise ValueError("One target-proven classification export member/header contract is required.")
    columns = contract.get("Columns", {})
    required = {"Name", "OrganizationId", "ClassificationCode", "Status", "EffectiveStartDate", "EffectiveEndDate"}
    if not isinstance(columns, dict) or set(columns) != required:
        raise ValueError("Complete target-export identity/classification header mapping is required.")
    permissions = contract.get("PermissionColumns", {}) if verify_permissions else {}
    if verify_permissions and (not isinstance(permissions, dict) or set(permissions) != set(PERMISSIONS)):
        raise ValueError("Target-export PTO permission header mapping is required.")
    keys = contract.get("SourceKeyColumns", {})
    key_fields = {"SourceSystemOwner", "SourceSystemId", "OrgInformationContext", "SequenceNumber"}
    if (not isinstance(keys, dict) or (keys and (set(keys) != key_fields
            or contract.get("SourceKeyComponent") != "OrgInformation"))):
        raise ValueError("Export key mapping must identify original OrgInformation keys, not classification keys.")
    all_headers = list(columns.values()) + list(permissions.values()) + list(keys.values())
    if any(not isinstance(v, str) or not v for v in all_headers) or len(set(all_headers)) != len(all_headers):
        raise ValueError("Export header mapping is incomplete or ambiguous.")
    try:
        content = Path(archive).read_bytes()
        checksum = hashlib.sha256(content).hexdigest()
        if checksum != receipt.get("ArtifactSha256"):
            raise ValueError("Classification export checksum differs from the registered completed export.")
        rows = []
        with zipfile.ZipFile(io.BytesIO(content)) as package:
            members = package.namelist()
            if len(set(members)) != len(members) or package.testzip() is not None:
                raise ValueError("Classification export ZIP is corrupt or has ambiguous members.")
            for member in contract["Members"]:
                if (member not in members or Path(member).is_absolute() or ".." in Path(member).parts
                        or "\\" in member or not member.endswith(".csv")):
                    raise ValueError("A required classification export CSV member is missing or unsafe.")
                reader = csv.DictReader(io.StringIO(package.read(member).decode("utf-8-sig")), strict=True)
                headers = reader.fieldnames or []
                if (len(headers) != len(set(headers)) or not set(columns.values()) <= set(headers)):
                    raise ValueError("Classification export identity headers are missing or ambiguous.")
                for raw in reader:
                    if None in raw or any(v is None for v in raw.values()):
                        raise ValueError("Classification export contains an incomplete CSV row.")
                    row = {key: raw[header] for key, header in columns.items()}
                    identity(row["OrganizationId"]); text(row["Name"], "Export organization name"); dates(row)
                    if row["ClassificationCode"] == "PA_PROJECT_ORG":
                        if verify_permissions and not set(permissions.values()) <= set(headers):
                            raise ValueError("Existing PTO export lacks complete current permission values.")
                        if verify_permissions:
                            row["Permissions"] = {key: raw[header] for key, header in permissions.items()}
                            if any(v not in {"Y", "N"} for v in row["Permissions"].values()):
                                raise ValueError("Existing PTO export permission values are incomplete or invalid.")
                        # Missing keys do not erase existing state or invent a new row.
                        if keys and set(keys.values()) <= set(headers) and all(raw[h] for h in keys.values()):
                            binding = {key: raw[header] for key, header in keys.items()}
                            if binding["OrgInformationContext"] != CONTEXT or binding["SequenceNumber"] != "1":
                                raise ValueError("Exported PTO information identity is conflicting.")
                            binding.update(Component="OrgInformation", SequenceNumber=1)
                            row["SourceKeyBinding"] = binding
                    rows.append(row)
    except (OSError, UnicodeError, csv.Error, zipfile.BadZipFile, RuntimeError) as exc:
        raise ValueError("Classification export is unreadable; no new setup branch or HDL artifact is allowed.") from exc
    result = {**receipt, "MetadataEvidenceRef": contract["EvidenceRef"], "Rows": rows}
    classification_export({"ClassificationsExport": result, "TargetEnvironment": target,
                           "AsOfDate": as_of, "ExportRunId": run_id}, verify_permissions=verify_permissions)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ("archive", "receipt", "contract", "output"):
        parser.add_argument("--" + flag, required=True, type=Path)
    for flag in ("target-environment", "as-of-date", "run-id"):
        parser.add_argument("--" + flag, required=True)
    parser.add_argument("--identity-only", action="store_true",
                        help="Read original HDL identity without requiring or reading PTO permission columns.")
    args = parser.parse_args()
    try:
        result = read_export(args.archive, json.loads(args.receipt.read_text()),
                             json.loads(args.contract.read_text()), args.target_environment,
                             args.as_of_date, args.run_id, verify_permissions=not args.identity_only)
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, indent=2)
        return 0
    except ValueError as exc:
        print("Classification export baseline validation failed: " + str(exc))
        return 1
    except (OSError, TypeError, KeyError):
        # Never disclose raw exported tenant rows in errors.
        print("Classification export baseline validation failed; preserve the artifact and resolve its contract.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
