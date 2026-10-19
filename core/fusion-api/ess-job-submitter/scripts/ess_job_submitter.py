#!/usr/bin/env python3
"""Submit and track Oracle Fusion ESS job requests.

This module is intentionally importable by other skills. The CLI wraps the same
functions so downstream workflows can choose either direct Python calls or a
process boundary with JSON output.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CORE_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROPERTIES_PATH = CORE_ROOT / "auth" / "fusionEnv.properties"
AUTH_SCRIPTS_PATH = CORE_ROOT / "auth" / "fusion-oauth-authentication" / "scripts"
sys.path.insert(0, str(AUTH_SCRIPTS_PATH))

from fusion_auth import (  # noqa: E402
    BoundAccessToken,
    request_context,
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    FusionHttpError,
    authorized_urlopen,
    rest_url,
    get_access_token,
    read_properties,
    require_props,
)


ESS_REQUESTS_RESOURCE = "/ess/rest/scheduler/v1/requests"
SUCCESS_CAUSES = {"PROCESS_SUCCESS"}
WARNING_CAUSE_SUFFIX = "_WARNING"
NON_TERMINAL_CAUSES = {"", "NON_TERMINAL"}
TERMINAL_STATE_TOKENS = {
    "CANCEL",
    "CANCELED",
    "CANCELLED",
    "COMPLETE",
    "COMPLETED",
    "ERROR",
    "EXPIRED",
    "FAILED",
    "FINISHED",
    "SUCCESS",
    "SUCCEEDED",
    "TIMEOUT",
    "TIMED_OUT",
    "WARNING",
}
DEFAULT_STATUS_FIELDS = (
    "requestId",
    "jobDefinitionId",
    "jobDisplayName",
    "application",
    "state",
    "stateDescription",
    "processPhase",
    "processPhaseDescription",
    "cause",
    "causeDescription",
    "errorType",
    "errorTypeDescription",
    "errorWarningMessage",
    "errorWarningDetail",
    "submissionTime",
    "scheduledTime",
    "processStartTime",
    "processEndTime",
    "completedTime",
    "elapsedTime",
    "isAsynchronous",
    "ecid",
)


@dataclass(frozen=True)
class EssHttpResult:
    status: int
    headers: dict[str, str]
    body: dict[str, Any]


def build_url(props: dict[str, str], resource_path: str, query_params: dict[str, str] | None = None) -> str:
    url = rest_url(props, resource_path)
    if query_params:
        url = f"{url}?{urllib.parse.urlencode(query_params)}"
    return url


def request_json(
    props: dict[str, str],
    url: str,
    *,
    method: str,
    access_token: str,
    json_body: dict[str, Any] | None = None,
    timeout: int = 60,
) -> EssHttpResult:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    body = None
    if json_body is not None:
        body = json.dumps(json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with authorized_urlopen(props, request, timeout=timeout, access_token=access_token) as response:
            response_body = response.read().decode("utf-8", errors="replace")
            response_headers = dict(response.headers.items())
            status = response.status
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise FusionHttpError(exc.code, url, error_body) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed calling {url}: {exc.reason}") from exc

    if not response_body.strip():
        parsed: dict[str, Any] = {}
    else:
        try:
            data = json.loads(response_body)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Expected JSON from {url}, got: {response_body[:500]}") from exc
        if not isinstance(data, dict):
            raise RuntimeError(f"Expected a JSON object from {url}")
        parsed = data
    return EssHttpResult(status=status, headers=response_headers, body=parsed)


def validate_request_payload(payload: dict[str, Any]) -> None:
    if "callbackSubscription" in payload:
        raise ValueError("callbackSubscription is not supported by this skill yet")
    if not payload.get("jobDefinitionId"):
        raise ValueError("ESS request payload must include jobDefinitionId")
    if payload.get("schedule") and payload.get("scheduleId"):
        raise ValueError("Only one of schedule and scheduleId may be specified")

    priority = payload.get("priority")
    if priority is not None and (not isinstance(priority, int) or priority < 0 or priority > 9):
        raise ValueError("priority must be an integer in the range 0..9")

    request_parameters = payload.get("requestParameters", [])
    if request_parameters is None:
        return
    if not isinstance(request_parameters, list):
        raise ValueError("requestParameters must be an array")
    for index, parameter in enumerate(request_parameters):
        if not isinstance(parameter, dict):
            raise ValueError(f"requestParameters[{index}] must be an object")
        if not parameter.get("name") or not parameter.get("paramType"):
            raise ValueError(f"requestParameters[{index}] must include name and paramType")


def extract_request_id(response: dict[str, Any], headers: dict[str, str]) -> int:
    for key in ("id", "requestId"):
        value = response.get(key)
        if value is not None:
            return int(value)

    location = headers.get("Location") or headers.get("location")
    if location:
        last_segment = urllib.parse.urlparse(location).path.rstrip("/").rsplit("/", 1)[-1]
        if last_segment.isdigit():
            return int(last_segment)

    raise RuntimeError(f"Fusion response did not include a request id: {response}")


def submit_job_request(
    props: dict[str, str],
    access_token: str,
    payload: dict[str, Any],
    *,
    timeout: int = 60,
) -> EssHttpResult:
    validate_request_payload(payload)
    return request_json(
        props,
        build_url(props, ESS_REQUESTS_RESOURCE),
        method="POST",
        access_token=access_token,
        json_body=payload,
        timeout=timeout,
    )


def get_job_request(
    props: dict[str, str],
    access_token: str,
    request_id: int | str,
    *,
    fields: list[str] | None = None,
    timeout: int = 60,
) -> EssHttpResult:
    query_params: dict[str, str] = {}
    if fields:
        query_params["fields"] = ",".join(fields)
    return request_json(
        props,
        build_url(props, f"{ESS_REQUESTS_RESOURCE}/{request_id}", query_params),
        method="GET",
        access_token=access_token,
        timeout=timeout,
    )


def terminal_by_text(value: Any) -> bool:
    if value is None:
        return False
    normalized = str(value).strip().upper()
    if not normalized:
        return False
    if normalized in TERMINAL_STATE_TOKENS:
        return True
    tokenized = "".join(ch if ch.isalnum() else "_" for ch in normalized)
    parts = {part for part in tokenized.split("_") if part}
    if parts & TERMINAL_STATE_TOKENS:
        return True
    return any(
        tokenized.startswith(f"{token}_") or tokenized.endswith(f"_{token}")
        for token in TERMINAL_STATE_TOKENS
    )


def is_terminal_status(status: dict[str, Any]) -> bool:
    cause = str(status.get("cause") or "").strip().upper()
    if cause not in NON_TERMINAL_CAUSES:
        return True
    if status.get("completedTime"):
        return True
    if terminal_by_text(status.get("state")):
        return True
    return terminal_by_text(status.get("processPhase"))


def is_success_status(status: dict[str, Any]) -> bool:
    cause = str(status.get("cause") or "").strip().upper()
    if cause in SUCCESS_CAUSES:
        return True
    if cause.endswith(WARNING_CAUSE_SUFFIX):
        return True
    if cause not in NON_TERMINAL_CAUSES:
        return False
    state = str(status.get("state") or "").strip().upper()
    error_fields = (
        status.get("errorType"),
        status.get("errorWarningMessage"),
        status.get("errorWarningDetail"),
    )
    return bool(status.get("completedTime")) and "ERROR" not in state and not any(error_fields)


def summarize_status(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "requestId": status.get("requestId"),
        "jobDefinitionId": status.get("jobDefinitionId"),
        "jobDisplayName": status.get("jobDisplayName"),
        "state": status.get("state"),
        "stateDescription": status.get("stateDescription"),
        "processPhase": status.get("processPhase"),
        "cause": status.get("cause"),
        "causeDescription": status.get("causeDescription"),
        "completedTime": status.get("completedTime"),
        "elapsedTime": status.get("elapsedTime"),
        "errorType": status.get("errorType"),
        "errorWarningMessage": status.get("errorWarningMessage"),
        "ecid": status.get("ecid"),
        "terminal": is_terminal_status(status),
        "success": is_success_status(status) if is_terminal_status(status) else None,
    }


def wait_for_job_request(
    props: dict[str, str],
    access_token: str,
    request_id: int | str,
    *,
    wait_seconds: int,
    poll_interval: int,
    fields: list[str] | None = None,
    timeout: int = 60,
) -> dict[str, Any]:
    deadline = time.time() + wait_seconds
    last_status: dict[str, Any] | None = None
    while True:
        last_status = get_job_request(
            props,
            access_token,
            request_id,
            fields=fields,
            timeout=timeout,
        ).body
        if is_terminal_status(last_status):
            return last_status
        if wait_seconds <= 0 or time.time() >= deadline:
            return last_status
        time.sleep(max(1, poll_interval))


def parse_request_parameter(value: str) -> dict[str, str]:
    parts = value.split("=", 2)
    if len(parts) == 2:
        name, parameter_value = parts
        param_type = "STRING"
    elif len(parts) == 3:
        name, param_type, parameter_value = parts
    else:
        raise ValueError(f"Expected parameter as name=value or name=TYPE=value: {value}")
    if not name:
        raise ValueError(f"Missing parameter name in {value}")
    param_type = param_type.upper()
    if param_type not in {"BOOLEAN", "LONG", "INTEGER", "DATETIME", "STRING"}:
        raise ValueError(f"Unsupported parameter type {param_type!r}")
    return {"name": name, "paramType": param_type, "value": parameter_value}


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.payload and args.payload_file:
        raise ValueError("Provide either --payload or --payload-file, not both")
    if args.payload_file:
        loaded = json.loads(Path(args.payload_file).read_text(encoding="utf-8"))
        if not isinstance(loaded, dict):
            raise ValueError("--payload-file must contain a JSON object")
        payload.update(loaded)
    if args.payload:
        loaded = json.loads(args.payload)
        if not isinstance(loaded, dict):
            raise ValueError("--payload must be a JSON object")
        payload.update(loaded)

    for field in (
        "application",
        "description",
        "endTime",
        "jobDefinitionId",
        "product",
        "requestCategory",
        "requestLogLevel",
        "scheduleId",
        "startTime",
    ):
        value = getattr(args, field, None)
        if value is not None:
            payload[field] = value

    for field in ("priority", "requestTimeout", "retries"):
        value = getattr(args, field, None)
        if value is not None:
            payload[field] = value

    if args.parameter:
        payload["requestParameters"] = [parse_request_parameter(item) for item in args.parameter]
    return payload


def get_token(props: dict[str, str], args: argparse.Namespace, *, force_login: bool = False) -> str:
    if args.access_token:
        return BoundAccessToken(str(args.access_token), request_context(props))
    return get_access_token(
        props,
        redirect_url=args.redirect_url,
        auth_code=args.auth_code,
        open_browser=args.open_browser,
        callback_timeout=args.callback_timeout,
        token_cache=args.token_cache,
        force_login=args.force_login or force_login,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Submit and track Oracle Fusion ESS job requests.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument("--request-id", type=int, help="Track an existing ESS request instead of submitting a new one.")
    parser.add_argument("--find-recent-job-definition", help="Read-only lookup for recent requests with this exact job definition.")
    parser.add_argument("--since-minutes", type=int, help="Recent lookup window in minutes; requires --find-recent-job-definition.")
    parser.add_argument("--payload", help="ESS submit request JSON object.")
    parser.add_argument("--payload-file", help="Path to an ESS submit request JSON object.")
    parser.add_argument("--job-definition-id", dest="jobDefinitionId", help="ESS job definition metadata object ID.")
    parser.add_argument("--application", help="ESS application name.")
    parser.add_argument("--description", help="Optional search tag for the request.")
    parser.add_argument("--parameter", action="append", help="Request parameter as name=value or name=TYPE=value.")
    parser.add_argument("--product")
    parser.add_argument("--request-category", dest="requestCategory")
    parser.add_argument("--request-log-level", dest="requestLogLevel")
    parser.add_argument("--priority", type=int)
    parser.add_argument("--retries", type=int)
    parser.add_argument("--request-timeout", dest="requestTimeout", type=int, help="Request timeout in minutes.")
    parser.add_argument("--start-time", dest="startTime", help="ISO 8601 requested start time.")
    parser.add_argument("--end-time", dest="endTime", help="ISO 8601 requested end time.")
    parser.add_argument("--schedule-id", dest="scheduleId")
    parser.add_argument("--wait-seconds", type=int, default=300)
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--submit-only", action="store_true", help="Return after submission without polling status.")
    parser.add_argument("--full-status", action="store_true", help="Return the full status payload while polling.")
    parser.add_argument("--output", help="Write the structured result JSON to this file.")
    parser.add_argument("--timeout", type=int, default=60, help="HTTP request timeout in seconds.")
    parser.add_argument("--auth-code")
    parser.add_argument("--redirect-url")
    parser.add_argument("--callback-timeout", type=int, default=DEFAULT_CALLBACK_TIMEOUT_SECONDS)
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--force-login", action="store_true")
    parser.add_argument("--access-token")
    parser.add_argument("--open-browser", action="store_true", default=True)
    parser.add_argument("--no-open-browser", action="store_false", dest="open_browser")
    return parser.parse_args()


def build_result(
    *,
    props: dict[str, str],
    request_id: int,
    submitted: bool,
    submit_response: dict[str, Any] | None,
    location: str | None,
    status: dict[str, Any] | None,
    wait_seconds: int,
    poll_interval: int,
) -> dict[str, Any]:
    status_summary = summarize_status(status) if status else None
    terminal = bool(status_summary and status_summary["terminal"])
    success = status_summary["success"] if status_summary else None
    return {
        "execution_result": {
            "submitted": submitted,
            "requestId": request_id,
            "terminal": terminal,
            "success": success,
            "status": status_summary,
            "status_payload": status,
            "submit_response": submit_response,
            "location": location,
        },
        "diagnostics": {
            "wait_seconds": wait_seconds,
            "poll_interval": poll_interval,
            "timed_out_waiting": bool(status is not None and not terminal and wait_seconds > 0),
        },
        "audit_summary": {
            "environment": props.get("environment"),
            "rest_host": urllib.parse.urlparse(props.get("restBaseUrl", "")).netloc,
            "requestId": request_id,
            "submitted": submitted,
        },
    }


def write_result(result: dict[str, Any], output_path: str | None) -> None:
    rendered = json.dumps(result, indent=2) + "\n"
    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
        print(f"Wrote {path}")
    else:
        print(rendered, end="")


def build_failure_result(props: dict[str, str], exc: Exception) -> dict[str, Any]:
    """Return a redacted durable result when submission cannot produce a normal result."""
    return {
        "execution_result": {
            "submitted": False,
            "requestId": None,
            "terminal": False,
            "success": False,
            "status": None,
            "status_payload": None,
            "submit_response": None,
            "location": None,
        },
        "diagnostics": {
            "failure_class": "fusion_api_error" if isinstance(exc, FusionHttpError) else "transport_or_environment",
            "message": f"ESS submitter failed before a request ID was available ({type(exc).__name__}).",
            "wait_seconds": None,
            "poll_interval": None,
            "timed_out_waiting": False,
        },
        "audit_summary": {
            "environment": props.get("environment"),
            "rest_host": urllib.parse.urlparse(props.get("restBaseUrl", "")).netloc,
            "requestId": None,
            "submitted": False,
        },
    }


def run_with_token(props: dict[str, str], access_token: str, args: argparse.Namespace) -> dict[str, Any]:
    if args.find_recent_job_definition:
        if not args.since_minutes or args.since_minutes <= 0:
            raise ValueError("--find-recent-job-definition requires a positive --since-minutes value")
        since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=args.since_minutes)).isoformat()
        query = (
            f'jobDefinitionId eq "{args.find_recent_job_definition}" and '
            f'submissionTime ge "{since}"'
        )
        lookup = request_json(
            props,
            build_url(
                props,
                ESS_REQUESTS_RESOURCE,
                {"q": query, "orderBy": "submissionTime:desc", "fields": ",".join(DEFAULT_STATUS_FIELDS)},
            ),
            method="GET",
            access_token=access_token,
            timeout=args.timeout,
        ).body
        items = lookup.get("items", [])
        if not isinstance(items, list):
            raise RuntimeError("Expected an items array from the recent ESS request lookup")
        return {
            "execution_result": {
                "submitted": False,
                "requestId": None,
                # Keep the read-only lookup result compatible with the normal
                # command exit evaluation below.  A lookup is never a terminal
                # ESS execution result in its own right.
                "terminal": False,
                "success": None,
                "status": None,
                "status_payload": None,
                "submit_response": None,
                "location": None,
                "recent_requests": [summarize_status(item) for item in items if isinstance(item, dict)],
            },
            "diagnostics": {
                "lookup_window_minutes": args.since_minutes,
                "read_only": True,
                "timed_out_waiting": False,
            },
            "audit_summary": {"environment": props.get("environment"), "submitted": False},
        }
    submitted = False
    submit_response = None
    location = None
    if args.request_id:
        request_id = args.request_id
    else:
        payload = load_payload(args)
        submit_result = submit_job_request(props, access_token, payload, timeout=args.timeout)
        request_id = extract_request_id(submit_result.body, submit_result.headers)
        submitted = True
        submit_response = submit_result.body
        location = submit_result.headers.get("Location") or submit_result.headers.get("location")

    status = None
    if not args.submit_only:
        fields = None if args.full_status else list(DEFAULT_STATUS_FIELDS)
        status = wait_for_job_request(
            props,
            access_token,
            request_id,
            wait_seconds=args.wait_seconds,
            poll_interval=args.poll_interval,
            fields=fields,
            timeout=args.timeout,
        )

    return build_result(
        props=props,
        request_id=request_id,
        submitted=submitted,
        submit_response=submit_response,
        location=location,
        status=status,
        wait_seconds=0 if args.submit_only else args.wait_seconds,
        poll_interval=args.poll_interval,
    )


def main() -> int:
    args = parse_args()
    props: dict[str, str] = {}
    try:
        props = read_properties(Path(args.properties))
        require_props(props, ["environment", "restBaseUrl"])
        access_token = get_token(props, args)
        result = run_with_token(props, access_token, args)
    except FusionHttpError as exc:
        if exc.status_code not in {401, 403} or args.access_token:
            write_result(build_failure_result(props, exc), args.output)
            return 1
        try:
            print("Cached access token was rejected by Fusion. Running login flow again.", file=sys.stderr)
            access_token = get_token(props, args, force_login=True)
            result = run_with_token(props, access_token, args)
        except Exception as retry_exc:
            write_result(build_failure_result(props, retry_exc), args.output)
            return 1
    except Exception as exc:
        write_result(build_failure_result(props, exc), args.output)
        return 1

    write_result(result, args.output)
    execution_result = result["execution_result"]
    if execution_result["terminal"] and execution_result["success"] is False:
        return 4
    if result["diagnostics"]["timed_out_waiting"]:
        return 3
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
