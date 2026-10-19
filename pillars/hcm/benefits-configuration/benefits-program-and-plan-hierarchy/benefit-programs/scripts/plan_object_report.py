"""Compare Benefits Plan Copy object inventories from export and import logs."""

from __future__ import annotations

import hashlib
import re
from typing import Any


REPORT_HEADING = re.compile(r"^\s*Plan Copy Report\s*$", re.IGNORECASE)
OBJECT_HEADING = re.compile(
    r"^\s*Object Name\s*-\s*No\.?\s+of\s+rows\s*$", re.IGNORECASE
)
OBJECT_ROW = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_ ]*)\s*-\s*(\d+)\s*$")
SEPARATOR = re.compile(r"^[-\s]*$")
SUPPORT_OBJECTS = frozenset({"PlanCopyMap", "BenIntegrationKeyMap"})


def import_log_objects(log_text: str) -> tuple[dict[str, int], str]:
    """Read only the Plan Copy Report table, never unrelated warning tables."""
    lines = log_text.splitlines()
    sections = [index for index, line in enumerate(lines) if REPORT_HEADING.fullmatch(line)]
    if len(sections) != 1:
        return {}, "missing_or_ambiguous_report"
    start = sections[0] + 1
    header = next(
        (index for index in range(start, min(start + 8, len(lines)))
         if OBJECT_HEADING.fullmatch(lines[index])),
        None,
    )
    if header is None:
        return {}, "missing_object_header"

    counts: dict[str, int] = {}
    for line in lines[header + 1:]:
        if SEPARATOR.fullmatch(line):
            continue
        row = OBJECT_ROW.fullmatch(line)
        if row is None:
            break
        name = row.group(1).strip()
        if name not in SUPPORT_OBJECTS:
            counts[name] = counts.get(name, 0) + int(row.group(2))
    return counts, "reported" if counts else "no_object_rows"


def build_object_report(
    export_summary: dict[str, Any],
    import_log_text: str,
    *,
    import_status: str,
) -> dict[str, Any]:
    """Keep source counts separate and never infer unreported imported counts."""
    before = {
        name: count
        for name, count in export_summary["reportedObjectCounts"].items()
        if name not in SUPPORT_OBJECTS
    }
    after, log_status = import_log_objects(import_log_text)
    names = sorted(set(before) | set(after))
    rows = [
        {
            "objectType": name,
            "beforeCount": before.get(name),
            "afterCount": after.get(name),
        }
        for name in names
    ]
    if not after:
        verification = "NOT_REPORTED"
    elif set(after) != set(before):
        verification = "INCOMPLETE"
    elif before == after:
        verification = "MATCHED"
    else:
        verification = "DIFFERENT"
    return {
        "planNames": export_summary["planNames"],
        "importStatus": import_status,
        "objectVerification": verification,
        "beforeSource": export_summary["objectCountSource"],
        "afterSource": "RequestLogs / Plan Copy Report",
        "afterLogStatus": log_status,
        "importLogSha256": hashlib.sha256(import_log_text.encode("utf-8")).hexdigest(),
        "beforeTotal": sum(before.values()),
        "afterReportedTotal": sum(after.values()) if after else None,
        "objects": rows,
    }


def render_markdown(report: dict[str, Any]) -> str:
    """Show only setup-object counts actually reported by RequestLogs."""
    plan = ", ".join(report["planNames"])
    lines = [
        "# Benefits plan import object report",
        "",
        f"Plan: {plan}",
        f"Import process status: {report['importStatus']}",
        f"Count source: {report['afterSource']}",
        "",
    ]
    reported_rows = [
        row for row in report["objects"]
        if row["afterCount"] is not None and row["objectType"] not in SUPPORT_OBJECTS
    ]
    if not reported_rows:
        lines.extend(["The import log did not report object counts.", ""])
        return "\n".join(lines)
    lines.extend([
        "| Object | Count |",
        "| --- | ---: |",
    ])
    for row in reported_rows:
        lines.append(f"| {row['objectType']} | {row['afterCount']} |")
    lines.extend([
        f"| **Total reported rows** | **{sum(row['afterCount'] for row in reported_rows)}** |",
        "",
    ])
    return "\n".join(lines)
