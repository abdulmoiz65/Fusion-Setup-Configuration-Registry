"""Prepare PROJECT create controls locally; never connect to or mutate Fusion.

The calling workflow owns same-target provenance, freshness, native package
validation and Data Loader approval. This helper verifies identities and resolves
controls, but its output alone is neither an import package nor an import gate.
Output must use a new artifact path; existing files are never replaced.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path


TASK_ROOT = Path(__file__).resolve().parents[1]
REFERENCE = TASK_ROOT / "ora-resource" / "ora_reference_lookups.md"
POLICIES = ("prefer-current-else-standard", "exact-inheritance")


class ControlEvidenceError(ValueError):
    """A valid control request cannot be resolved from the supplied evidence."""

    def __init__(self, message, blocker_type="evidence_conflict"):
        super().__init__(message)
        self.blocker_type = blocker_type


def yn(value):
    if value is True or isinstance(value, str) and value.strip().lower() in {"y", "yes", "true"}:
        return "Y"
    if value is False or isinstance(value, str) and value.strip().lower() in {"n", "no", "false"}:
        return "N"
    raise ValueError("Allow must be a boolean or Yes/No, Y/N, true/false")


def requested_allow_changes(status, known_actions, classification):
    changes = status.get("ActionControls", [])
    if not isinstance(changes, list):
        raise ValueError("ActionControls must be a list of ActionCode/Allow requests")
    overrides = {}
    for change in changes:
        if not isinstance(change, dict) or set(change) != {"ActionCode", "Allow"}:
            raise ValueError("Only ActionCode and Allow may be supplied; internal inherited fields are protected")
        action = change["ActionCode"]
        if action not in known_actions or action in overrides:
            raise ValueError("Requested control is unsupported or duplicated")
        overrides[action] = yn(change["Allow"])
    if classification == "CLOSED" and (changes or "AllActionsAllow" in status):
        raise ValueError("CLOSED Allow controls are protected")
    all_allow = yn(status["AllActionsAllow"]) if "AllActionsAllow" in status else None
    if all_allow is not None and overrides:
        raise ValueError("Supply AllActionsAllow or individual controls, not both")
    return overrides, all_allow


def standard_controls(classification):
    """Read the one maintained default matrix rather than duplicating its values."""
    columns = {
        "ACTIVE": 3, "DRAFT": 4, "CLOSED": 4,
        "SUBMITTED": 5, "PENDING_CLOSE": 6,
    }
    if classification not in columns:
        raise ValueError("Standard create controls support only the five PROJECT classifications")
    section = REFERENCE.read_text().split("## Project Classification Control Defaults\n", 1)[1]
    section = section.split("\n## ", 1)[0]
    rows = []
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 7 or cells[0] == "Action Code" or set(cells[0]) <= {"-", ":"}:
            continue
        enabled = cells[columns[classification]]
        if enabled not in {"Y", "N"}:
            raise ValueError("Invalid standard EnabledFlag matrix")
        rows.append({"ActionCode": cells[0], "SortOrder": str(int(cells[2])),
                     "StatusType": "PROJECT", "EnabledFlag": enabled})
    if len(rows) != 7 or len({r["ActionCode"] for r in rows}) != 7:
        raise ValueError("Standard control matrix must contain seven distinct actions")
    return rows


def native_rows(package, member, required):
    names = package.namelist()
    if names.count(member) != 1:
        raise ValueError(f"Native export must contain exactly one {member}")
    reader = csv.DictReader(io.StringIO(package.read(member).decode("utf-8-sig")))
    if not set(required).issubset(reader.fieldnames or []) or len(reader.fieldnames) != len(set(reader.fieldnames)):
        raise ValueError(f"Missing native headers in {member}")
    rows = list(reader)
    if any(None in r or any(v is None for v in r.values()) for r in rows):
        raise ValueError(f"Malformed CSV rows in {member}")
    return rows


def validate_identities(response):
    if not isinstance(response, dict):
        raise ValueError("Identity response must be an object")
    offset = response.get("offset")
    if response.get("hasMore") is not False or type(offset) is not int or offset != 0:
        raise ValueError("Complete unfiltered identity coverage must start at offset zero and end with hasMore=false")
    items = response.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("Identity collection is missing or empty")
    if "count" in response:
        count = response["count"]
        if type(count) is not int or count != len(items):
            raise ValueError("Identity count must equal the complete supplied item count; aggregate all pages before resolving controls")
    codes, names = set(), set()
    for row in items:
        required = ("ProjectStatusCode", "ProjectStatusName", "StatusObjectCode", "StatusClassificationCode")
        if not isinstance(row, dict) or any(not isinstance(row.get(k), str) or not row[k].strip() for k in required):
            raise ValueError("Identity response is missing required string fields")
        code = row["ProjectStatusCode"]
        name = (row["StatusObjectCode"], row["ProjectStatusName"])
        if code in codes or name in names:
            raise ValueError("Ambiguous stored code or object/name identity")
        codes.add(code)
        names.add(name)
    return items


def resolve(request, identities, parents, controls, *, policy, environment):
    if policy not in POLICIES:
        raise ValueError("Unsupported controls policy")
    if not isinstance(request, dict) or request.get("operation") != "create" or not isinstance(request.get("statuses"), list) or not request["statuses"]:
        raise ValueError("This helper accepts only a nonempty create request")
    identities = validate_identities(identities)
    results, errors, requested_names = [], [], set()
    for status in request["statuses"]:
        name = status.get("ProjectStatusName") if isinstance(status, dict) else None
        try:
            if not isinstance(status, dict):
                raise ValueError("Every status must be an object")
            if status.get("StatusType") != "PROJECT" or not isinstance(name, str) or not name.strip():
                raise ValueError("A named PROJECT create is required; other objects and updates have no standard fallback")
            if name in requested_names or any(r["StatusObjectCode"] == "PROJECT" and r["ProjectStatusName"] == name for r in identities):
                raise ValueError("Requested PROJECT name already exists or is duplicated in this request")
            requested_names.add(name)
            classification = status.get("ProjectSystemStatusCode")
            defaults = standard_controls(classification)
            known_actions = {r["ActionCode"] for r in defaults}
            overrides, all_allow = requested_allow_changes(status, known_actions, classification)
            source = [r for r in identities if r["ProjectStatusCode"] == classification]
            if len(source) != 1 or source[0]["StatusObjectCode"] != "PROJECT" or source[0]["StatusClassificationCode"] != classification:
                raise ControlEvidenceError("Exact classification source identity is unavailable or incompatible")
            source_name = source[0]["ProjectStatusName"]
            parent = [r for r in parents if r["StatusType"] == "PROJECT" and r["ProjectStatusName"] == source_name]
            source_rows = [r for r in controls if r["PJF_STATUS_LIST.StatusType"] == "PROJECT" and r["PJF_STATUS_LIST.ProjectStatusName"] == source_name]
            if len(parent) > 1 or source_rows and not parent:
                raise ControlEvidenceError("Ambiguous source parent or orphan source controls")
            if parent:
                if parent[0]["ProjectSystemStatusCode"] != classification or not source_rows:
                    raise ControlEvidenceError("Exported classification source has inconsistent or missing controls; do not mask this with standard defaults")
                selected, seen = [], set()
                for row in source_rows:
                    action = row["ActionCode"]
                    if action not in known_actions or action in seen or row["EnabledFlag"] not in {"Y", "N"} or row["StatusType"] != "PROJECT" or row["ProjectSystemStatusCode"] != classification:
                        raise ControlEvidenceError("Invalid, duplicate or unsupported current classification control")
                    seen.add(action)
                    order = row["SortOrder"]
                    try:
                        int(order)
                    except (ValueError, TypeError) as exc:
                        raise ControlEvidenceError("Current classification control has invalid SortOrder") from exc
                    selected.append({"ActionCode": action, "SortOrder": order,
                                     "StatusType": "PROJECT", "EnabledFlag": row["EnabledFlag"]})
                if seen != known_actions:
                    raise ControlEvidenceError("Current classification controls do not cover the complete supported PROJECT action set; do not mask partial evidence with standard defaults")
                basis, verified = "current_classification", True
            else:
                if policy == "exact-inheritance":
                    raise ControlEvidenceError("Current classification controls are unavailable under exact-inheritance policy", "workflow_gap")
                selected, basis, verified = defaults, "standard_source", False
            available = {r["ActionCode"] for r in selected}
            if not set(overrides).issubset(available):
                raise ControlEvidenceError("Requested action is absent from the current classification controls")
            for row in selected:
                row.update({
                    "PJF_STATUS_LIST.ProjectStatusName": name,
                    "PJF_STATUS_LIST.StatusType": "PROJECT",
                    "ProjectSystemStatusCode": classification,
                    "CopyToUserStatusFlag": "N",
                    "AllowOverridesFlag": overrides.get(row["ActionCode"], all_allow if all_allow is not None else "N" if classification in {"DRAFT", "CLOSED"} else "Y"),
                })
            results.append({"ProjectStatusName": name, "ProjectSystemStatusCode": classification,
                            "controls_basis": basis, "inheritance_verified": verified,
                            "classification_source_code": classification,
                            "classification_source_name": source_name,
                            "controls": sorted(selected, key=lambda r: (int(r["SortOrder"]), r["ActionCode"]))})
        except (ValueError, KeyError, TypeError) as exc:
            evidence_error = isinstance(exc, ControlEvidenceError)
            errors.append({"ProjectStatusName": name, "message": str(exc),
                           "stage": "controls_resolution",
                           "failure_class": "catalog_or_metadata_mismatch" if evidence_error else "input_validation",
                           "blocker_type": exc.blocker_type if evidence_error else "invalid_control_request",
                           "controls_request_validation": "passed" if evidence_error else "failed",
                           "recommended_action": "Resolve the named current evidence gap; retain the valid control request" if evidence_error else "Correct the named control input"})
    standard = [r["ProjectStatusName"] for r in results if not r["inheritance_verified"]]
    return {"operation_status": "blocked" if errors else "prepared", "operation": "create",
            "environment": environment, "controls_policy": policy, "statuses": results,
            "errors": errors, "standard_default_statuses": standard,
            "controls_request_validation": "failed" if any(e["controls_request_validation"] == "failed" for e in errors) else "passed",
            "blocker_type": (errors[0]["blocker_type"] if len({e["blocker_type"] for e in errors}) == 1 else "multiple_blockers") if errors else None,
            "required_preview_disclosures": (["Standard Oracle source defaults are explicit proposed configuration; current target inheritance is unverified for: " + ", ".join(standard)] if standard else []),
            "import_authorized": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("requests-file", "identities-json", "current-export", "environment", "output"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--policy", choices=POLICIES, default=POLICIES[0])
    args = parser.parse_args()
    try:
        request_path, identities_path, export_path = map(Path, (args.requests_file, args.identities_json, args.current_export))
        paths = [request_path, identities_path, export_path, REFERENCE]
        output = Path(args.output)
        if output.exists() or output.is_symlink():
            raise FileExistsError("Controls output already exists")
        if output.resolve() in {p.resolve() for p in paths}:
            raise ValueError("Output must not overwrite an input")
        if not args.environment.strip():
            raise ValueError("Target environment is required")
        with zipfile.ZipFile(export_path) as package:
            parents = native_rows(package, "PJF_STATUS_LIST.csv", ("ProjectStatusName", "StatusType", "ProjectSystemStatusCode"))
            controls = native_rows(package, "PJF_PROJECT_STATUS_CONTROLS.csv", ("PJF_STATUS_LIST.ProjectStatusName", "PJF_STATUS_LIST.StatusType", "StatusType", "ProjectSystemStatusCode", "ActionCode", "EnabledFlag", "SortOrder"))
        result = resolve(json.loads(request_path.read_text()), json.loads(identities_path.read_text()), parents, controls, policy=args.policy, environment=args.environment)
        result["input_sha256"] = {role: hashlib.sha256(p.read_bytes()).hexdigest()
                                  for role, p in zip(("request", "identities", "current_export", "standard_reference"), paths)}
        result["resolved_at"] = datetime.now(timezone.utc).isoformat()
        output.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation also protects an artifact created after preflight.
        with output.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(result, indent=2) + "\n")
        print(json.dumps({"operation_status": result["operation_status"], "statuses": len(result["statuses"]), "standard_default_statuses": len(result["standard_default_statuses"]), "errors": len(result["errors"]), "output": str(output)}))
        return 2 if result["errors"] else 0
    except FileExistsError:
        print("Controls preparation failed: approval_blocker: output already exists; "
              "preserve it and select a new versioned output path.", file=sys.stderr)
        return 2
    except (ValueError, KeyError, OSError, zipfile.BadZipFile) as exc:
        print(f"Controls preparation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
