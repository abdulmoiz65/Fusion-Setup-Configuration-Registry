#!/usr/bin/env python3
"""Render local CREATE evidence as business and per-Alert technical Markdown.

No REST/auth imports, payload construction, or execution side effects.
Input is sanitized evidence assembled by the assisted Alert provider.
"""
import argparse
import html
import json
import sys
from pathlib import Path
from urllib.parse import quote


STAGES = {"awaiting_approval", "not_submitted", "submitted", "failed", "uncertain"}
ENTITIES = {"alert", "template", "recipient"}


def escaped(value):
    """Untrusted data must not introduce Markdown links, rows or HTML."""
    text = str(value).replace("\r", " ").replace("\n", " ")
    return "".join(f"&#{ord(char)};" if char in "\\`*_{}[]()#!|"
                   else html.escape(char, quote=True) for char in text)


def identity(obj):
    return obj["entity"], obj.get("parent_key", ""), obj["code"]


def status_for(row):
    stage = row["stage"]
    if stage == "uncertain":
        return "Outcome uncertain"
    if stage == "awaiting_approval":
        return "Awaiting approval"
    if stage == "not_submitted":
        return "Not submitted"
    expected = {identity(o) for o in row["expected_objects"]}
    observed = {identity(o): o for o in row.get("objects", [])}
    verified = {k for k, o in observed.items() if o["status"] == "verified"}
    failed = stage == "failed" or any(o["status"] == "verification_failed" for o in observed.values())
    if failed:
        return "Partially completed" if verified else "Needs attention"
    if row.get("response_matched") and row.get("http_status") is not None and expected == verified and expected == set(observed):
        return "Created and verified"
    return "Submitted; verification pending"


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("Reporting input must be an object")
    if data.get("schema_version") != 1 or data.get("execution_mode") not in {"batch-create", "sequential"}:
        raise ValueError("Unsupported reporting schema or execution mode")
    if not isinstance(data.get("alerts"), list) or not data["alerts"]:
        raise ValueError("At least one Alert is required")
    seen = set()
    for row in data["alerts"]:
        if not isinstance(row, dict):
            raise ValueError("Each Alert must be an object")
        for field in ("code", "name"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ValueError(f"Missing Alert {field}")
        if row["code"] in seen:
            raise ValueError("Duplicate Alert code")
        seen.add(row["code"])
        if row.get("stage") not in STAGES:
            raise ValueError("Unknown Alert stage")
        http = row.get("http_status")
        if http is not None and (type(http) is not int or not 100 <= http <= 599):
            raise ValueError("Invalid HTTP status")
        if row["stage"] in {"awaiting_approval", "not_submitted"} and (http is not None or row.get("objects") or row.get("response_matched")):
            raise ValueError("Unsubmitted Alert cannot contain submission/verification evidence")
        if type(row.get("response_matched", False)) is not bool:
            raise ValueError("response_matched must be boolean")
        for collection in ("expected_objects", "objects"):
            values = row.get(collection, [])
            if not isinstance(values, list) or (collection == "expected_objects" and not values):
                raise ValueError("Missing expected hierarchy")
            keys = set()
            for obj in values:
                if not isinstance(obj, dict):
                    raise ValueError("Object evidence must be an object")
                if obj.get("entity") not in ENTITIES or not isinstance(obj.get("code"), str) or not obj["code"]:
                    raise ValueError("Invalid object identity")
                if not isinstance(obj.get("parent_key", ""), str):
                    raise ValueError("Invalid parent key")
                key = identity(obj)
                if key in keys:
                    raise ValueError("Duplicate object identity; supply parent_key where needed")
                keys.add(key)
                if collection == "objects":
                    if obj.get("status") not in {"verified", "verification_failed", "pending"}:
                        raise ValueError("Unknown object verification status")
                    if obj["status"] == "verified" and (type(obj.get("id")) is not int or obj["id"] <= 0 or obj.get("http_status") != 200):
                        raise ValueError("Verified object requires internal ID and GET HTTP 200")
            if collection == "expected_objects":
                parents = [o for o in values if o["entity"] == "alert"]
                if len(parents) != 1 or parents[0]["code"] != row["code"]:
                    raise ValueError("Expected hierarchy must contain exactly this Alert")
        if not {identity(o) for o in row.get("objects", [])} <= {identity(o) for o in row["expected_objects"]}:
            raise ValueError("Unexpected object evidence")
        if row.get("response_matched") and http is not None and not 200 <= http < 300:
            raise ValueError("Successful response evidence contradicts HTTP status")
    for ref in data.get("evidence_files", []):
        if not isinstance(ref, str) or not Path(ref).is_absolute() or not Path(ref).is_file():
            raise ValueError("Evidence links must target existing absolute local files")


def render(data):
    validate(data)
    rows = data["alerts"]
    statuses = [status_for(r) for r in rows]
    if all(s == "Created and verified" for s in statuses):
        heading = "Your Event Alerts were created successfully."
    elif all(s == "Awaiting approval" for s in statuses):
        heading = "Your Alerts are ready for review. Nothing has been submitted."
    elif all(s == "Not submitted" for s in statuses):
        heading = "Your Alerts have not been submitted."
    else:
        heading = "Your Event Alert request needs attention. Review each Alert's status below."
    summary = [heading, "", "| Alert code | Alert name | Status | HTTP status | Technical details |", "| --- | --- | --- | --- | --- |"]
    details = ["# Event Alert technical details", "", f"Environment: {escaped(data.get('environment', 'Not bound'))}", "", f"Execution mode: {escaped(data['execution_mode'])}", "", f"Work unit / run reference: {escaped(data.get('work_unit_sha256', 'Not available'))}", ""]
    actions = []
    for index, (row, status) in enumerate(zip(rows, statuses), 1):
        anchor = f"alert-{index}"
        http = row.get("http_status")
        scope = "batch" if data["execution_mode"] == "batch-create" else "Alert POST"
        http_text = f"{http} ({scope})" if http is not None else ("Not submitted" if row["stage"] in {"awaiting_approval", "not_submitted"} else "Unavailable")
        summary.append(f"| {escaped(row['code'])} | {escaped(row['name'])} | {status} | {http_text} | [View details](technical-details.md#{anchor}) |")
        details += [f"## Alert {index}", "", f"Code: {escaped(row['code'])}", "", f"Name: {escaped(row['name'])}", "", f"Status: {status}", "", f"HTTP status: {http_text}", "", f"Response matched: {row.get('response_matched', False)}", ""]
        counts = {e: sum(o["entity"] == e for o in row["expected_objects"]) for e in ENTITIES}
        details += [f"Expected: {counts['alert']} Alert, {counts['template']} Templates, {counts['recipient']} Recipients.", "", "| Object | Code | Parent key | Internal ID | Verification | GET HTTP status |", "| --- | --- | --- | --- | --- | --- |"]
        actual = {identity(o): o for o in row.get("objects", [])}
        for expected in row["expected_objects"]:
            obj = actual.get(identity(expected), {})
            details.append("| " + " | ".join(escaped(v) for v in (expected["entity"], expected["code"], expected.get("parent_key", ""), obj.get("id", "Unavailable"), obj.get("status", "Not performed"), obj.get("http_status", "Unavailable"))) + " |")
        details.append("")
        action = row.get("action")
        if not action and status == "Outcome uncertain":
            action = "Do not resubmit. Reconcile the existing request before recovery."
        elif not action and status in {"Needs attention", "Partially completed"}:
            action = "Review the failed items and existing creations before approving recovery."
        elif not action and status == "Submitted; verification pending":
            action = "Complete read-back verification. Do not repeat the create request."
        if action:
            actions.append(f"- {escaped(row['code'])}: {escaped(action)}")
            details += [f"Action: {escaped(action)}", ""]
    if data["execution_mode"] == "batch-create":
        summary += ["", "HTTP status is the shared batch response; each Alert's status reflects its own evidence."]
    if actions:
        summary += ["", "Required action:", "", *actions]
    if data.get("body_verification") == "deferred":
        note = "Stored message Body verification remains deferred. Review message bodies in Alerts Composer."
        summary += ["", note]
        details += ["## Verification limitation", "", note, ""]
    details += ["Configuration results do not establish notification delivery.", ""]
    if data.get("evidence_files"):
        details += ["## Evidence", ""]
        for i, ref in enumerate(data["evidence_files"], 1):
            target = quote(Path(ref).as_posix(), safe="/:")
            details.append(f"- [Evidence {i}: {escaped(Path(ref).name)}](<{target}>)")
    return "\n".join(summary) + "\n", "\n".join(details) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        summary, details = render(data)
        directory = Path(args.output_dir).resolve()
        paths = [directory / "business-summary.md", directory / "technical-details.md"]
        if any(p.exists() for p in paths):
            raise FileExistsError("Report exists; select a new output directory")
        if not args.dry_run:
            directory.mkdir(parents=True, exist_ok=True)
            for path, content in zip(paths, (summary, details)):
                with path.open("x", encoding="utf-8") as stream:
                    stream.write(content)
        print(json.dumps({"status": "validated" if args.dry_run else "reported", "alerts": len(data["alerts"]), "artifacts": [str(p) for p in paths]}))
        return 0
    except (ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "failed", "failure_class": "input_validation", "message": str(exc)}))
        return 2
    except OSError as exc:
        print(json.dumps({"status": "failed", "failure_class": "artifact_persistence", "error_type": type(exc).__name__}))
        return 3


if __name__ == "__main__":
    sys.exit(main())
