#!/usr/bin/env python3
"""Read-only Calendar and Set Code preflight for Manage Payment Terms.

The preflight adds evidence to a copy of the requested design before the
offline adapter normalizes it. It never invents Calendar or SetCode values and
never writes to Fusion. Readable no-match and malformed responses block the
candidate; unavailable endpoints are recorded for later review.
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import sys
import urllib.parse
from pathlib import Path
from typing import Any

TASK_ROOT = Path(__file__).resolve().parents[1]
# Find the shared client instead of embedding credentials or another HTTP
# implementation in this task-local helper.
for candidate in (TASK_ROOT, *TASK_ROOT.parents):
    if (candidate / "core" / "data-loader" / "scripts" / "data_loader_metadata.py").is_file():
        ROOT = candidate
        break
else:
    raise RuntimeError("Could not locate the FSCR repository root.")
sys.path.insert(0, str(ROOT / "core" / "data-loader" / "scripts"))
import data_loader_metadata as metadata  # noqa: E402


class PreflightError(Exception):
    pass


def _items(payload: Any, required_fields: tuple[str, ...]) -> list[dict[str, Any]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise PreflightError("resolver_failure: reference response does not contain an items array.")
    items = payload["items"]
    if any(not isinstance(item, dict) for item in items):
        raise PreflightError("resolver_failure: reference response contains a non-object item.")
    if any(any(field not in item for field in required_fields) for item in items):
        raise PreflightError("resolver_failure: reference response omits a requested field.")
    return items


def _url(host: str, path: str, fields: str, query: str) -> str:
    return host + path + "?" + urllib.parse.urlencode({
        "onlyData": "true", "fields": fields, "q": query,
    })


def _unavailable(error: metadata.DataLoadError) -> bool:
    return error.http_status is None or error.http_status in {400, 401, 403, 408, 429} or error.http_status >= 500


def _error_detail(error: metadata.DataLoadError) -> dict[str, str]:
    """Return a compact, already-redacted diagnostic from a loader error."""
    result = {"message": error.message}
    response = error.response
    if not isinstance(response, dict):
        return result
    details = response.get("o:errorDetails")
    if isinstance(details, list) and details and isinstance(details[0], dict):
        detail = details[0]
        if isinstance(detail.get("o:errorCode"), str):
            result["errorCode"] = detail["o:errorCode"]
        if isinstance(detail.get("detail"), str):
            result["detail"] = detail["detail"]
    elif isinstance(response.get("detail"), str):
        result["detail"] = response["detail"]
    return result


def _append_resolver_finding(
    design: dict[str, Any], *, operation_id: str, field: str, resolver: str,
    endpoint: str, requested_value: str, query: str, error: metadata.DataLoadError,
) -> None:
    findings = design.setdefault("resolverFindings", [])
    if not isinstance(findings, list):
        raise PreflightError("Design resolverFindings must be an array.")
    finding = {
        "classification": "resolver_contract_issue",
        "severity": "maintenance_required",
        "owner": "skill_maintainer",
        "actionRequired": "fix_or_reverify",
        "operationId": operation_id,
        "field": field,
        "resolver": resolver,
        "endpoint": endpoint,
        "httpStatus": error.http_status,
        "requestedValue": requested_value,
        "querySha256": hashlib.sha256(query.encode("utf-8")).hexdigest(),
        "observedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "diagnostic": _error_detail(error),
    }
    if finding not in findings:
        findings.append(finding)


def resolve(design: dict[str, Any], config: dict[str, Any]) -> tuple[dict[str, Any], dict[str, int]]:
    resolved = copy.deepcopy(design)
    operations = resolved.get("operations")
    if not isinstance(operations, list) or not operations:
        raise PreflightError("Design must contain a nonempty operations array.")
    warnings = resolved.setdefault("warnings", [])
    if not isinstance(warnings, list):
        raise PreflightError("Design warnings must be an array.")
    summary = {"satisfied": 0, "validationSkipped": 0, "unresolved": 0, "resolverContractIssues": 0}
    checks = {
        "Calendar": (
            "validate_payables_calendar",
            "/fscmRestApi/resources/11.13.18.05/payablesCalendarTypes",
            "calendarName,calendarType", "calendarName", "PAYMENT TERMS",
        ),
        "SetCode": (
            "validate_set_code",
            "/fscmRestApi/resources/11.13.18.05/setIdSetsLOV",
            "SetCode,SetName,Description", "SetCode", None,
        ),
    }
    for operation in operations:
        if not isinstance(operation, dict) or not isinstance(operation.get("values"), dict):
            raise PreflightError("Each operation must contain a values object.")
        target_key = operation.get("targetKey", {})
        if not isinstance(target_key, dict):
            raise PreflightError("Each operation targetKey must be an object when supplied.")
        operation_id = str(operation.get("id", "<unnamed>"))
        for field, (resolver, path, fields, response_field, type_value) in checks.items():
            # Calendar is a line value, while SetCode is part of the
            # subscription's source-backed alternate key. Check both
            # locations so a requested subscription is never skipped.
            raw_value = operation["values"].get(field, target_key.get(field))
            if raw_value is None:
                continue
            value = str(raw_value).strip()
            if not value:
                continue
            query = f"{response_field}='{value}'"
            if type_value:
                query += f" and calendarType='{type_value}'"
            try:
                response = metadata.get_json(_url(config["host"], path, fields, query), config["auth"], stage=f"validate {field}")
            except metadata.DataLoadError as exc:
                if not _unavailable(exc):
                    raise PreflightError(f"resolver_failure: cannot validate {field}: {exc.message}") from exc
                if exc.http_status == 400:
                    _append_resolver_finding(
                        resolved, operation_id=operation_id, field=field, resolver=resolver,
                        endpoint=path, requested_value=value, query=query, error=exc,
                    )
                    warnings.append(
                        f"Read-only {field} validation returned HTTP 400; preserving the requested "
                        "value for Fusion import and recording a resolver_contract_issue for skill maintenance."
                    )
                    summary["resolverContractIssues"] += 1
                else:
                    warnings.append(f"Read-only {field} validation skipped because the endpoint was unavailable; Fusion import remains authoritative.")
                summary["validationSkipped"] += 1
                continue
            # This supporting GET is corroborating evidence, not the FSM
            # resolver.  The query already expresses the submitted criteria;
            # once it yields a readable record, leave any final identity or
            # case decision to FSM Import.
            required_fields = tuple(part.strip() for part in fields.split(","))
            matches = _items(response, required_fields)
            if not matches:
                raise PreflightError(
                    f"not_found: read-only {field} validation returned no rows for "
                    f"{value!r}; candidate generation is blocked."
                )
            summary["satisfied"] += 1
    return resolved, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    metadata.add_oauth_arguments(parser)
    args = parser.parse_args(argv)
    try:
        design = json.loads(args.design.read_text(encoding="utf-8"))
        config = metadata.read_config(args.properties, **metadata.oauth_kwargs(args))
        resolved, summary = resolve(design, config)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(resolved, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"status": "PASS", **summary}, sort_keys=True))
        return 0
    except (OSError, json.JSONDecodeError, PreflightError, metadata.DataLoadError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
