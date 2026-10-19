#!/usr/bin/env python3
"""Submit and track Oracle Fusion AI Studio workflow agent requests."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
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
    authorized_urlopen, rest_url,
    get_access_token,
    read_properties,
    require_props,
)


DEFAULT_PATH_PREFIX = "/api/fusion-ai"
SUCCESS_STATUSES = {"SUCCESS", "SUCCEEDED", "COMPLETED", "COMPLETE", "DONE"}
INPUT_REQUIRED_STATUSES = {
    "INPUT_REQUIRED",
    "NEEDS_INPUT",
    "WAITING",
    "WAITING_FOR_INPUT",
    "WAITING_FOR_USER_INPUT",
}
FAILURE_STATUSES = {"ERROR", "FAILED", "FAILURE", "CANCELLED", "CANCELED", "TIMEOUT", "TIMED_OUT"}
TERMINAL_STATUSES = SUCCESS_STATUSES | INPUT_REQUIRED_STATUSES | FAILURE_STATUSES


@dataclass(frozen=True)
class AgentHttpResult:
    status: int
    headers: dict[str, str]
    body: dict[str, Any]


def build_url(
    props: dict[str, str],
    resource_path: str,
    query_params: dict[str, str] | None = None,
) -> str:
    url = rest_url(props, resource_path)
    if query_params:
        url = f"{url}?{urllib.parse.urlencode(query_params)}"
    return url


def join_resource_path(prefix: str | None, resource_path: str) -> str:
    if not prefix:
        return resource_path
    return f"/{prefix.strip('/')}/{resource_path.lstrip('/')}"


def workflow_resource_path(workflow_code: str, suffix: str, *, path_prefix: str | None = None) -> str:
    encoded_workflow_code = urllib.parse.quote(workflow_code, safe="")
    resource_path = f"/orchestrator/agent/v2/{encoded_workflow_code}/{suffix.lstrip('/')}"
    return join_resource_path(path_prefix, resource_path)


def request_json(
    url: str,
    *,
    method: str,
    access_token: str,
    props: dict[str, str] | None = None,
    json_body: dict[str, Any] | None = None,
    timeout: int = 60,
) -> AgentHttpResult:
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
    return AgentHttpResult(status=status, headers=response_headers, body=parsed)


def submit_workflow(
    props: dict[str, str],
    access_token: str,
    workflow_code: str,
    payload: dict[str, Any],
    *,
    path_prefix: str | None,
    timeout: int,
) -> AgentHttpResult:
    if not payload.get("message"):
        raise ValueError("Workflow submit payload must include message")
    return request_json(
        build_url(props, workflow_resource_path(workflow_code, "invokeAsync", path_prefix=path_prefix)),
        method="POST",
        access_token=access_token,
        props=props,
        json_body=payload,
        timeout=timeout,
    )


def get_workflow_status(
    props: dict[str, str],
    access_token: str,
    workflow_code: str,
    job_id: str,
    *,
    path_prefix: str | None,
    invocation_mode: str | None,
    timeout: int,
) -> AgentHttpResult:
    encoded_job_id = urllib.parse.quote(job_id, safe="")
    query_params = {"invocationMode": invocation_mode} if invocation_mode else None
    return request_json(
        build_url(
            props,
            workflow_resource_path(workflow_code, f"status/{encoded_job_id}", path_prefix=path_prefix),
            query_params,
        ),
        method="GET",
        access_token=access_token,
        props=props,
        timeout=timeout,
    )


def normalize_status(value: Any) -> str:
    return str(value or "").strip().upper()


def first_string(data: dict[str, Any], names: tuple[str, ...]) -> str | None:
    for name in names:
        value = data.get(name)
        if isinstance(value, str) and value:
            return value
    return None


def extract_job_id(response: dict[str, Any], headers: dict[str, str]) -> str:
    job_id = first_string(response, ("jobId", "jobID", "id", "requestId"))
    if job_id:
        return job_id

    location = headers.get("Location") or headers.get("location")
    if location:
        parsed_path = urllib.parse.urlparse(location).path.rstrip("/")
        if parsed_path:
            return parsed_path.rsplit("/", 1)[-1]

    raise RuntimeError(f"Fusion response did not include a job ID: {response}")


def status_value(payload: dict[str, Any]) -> str:
    return normalize_status(
        first_string(
            payload,
            (
                "status",
                "state",
                "jobStatus",
                "executionStatus",
                "lifecycleState",
                "phase",
            ),
        )
    )


def is_terminal_status(payload: dict[str, Any]) -> bool:
    status = status_value(payload)
    if status in TERMINAL_STATUSES:
        return True
    return any(token in status for token in TERMINAL_STATUSES)


def is_success_status(payload: dict[str, Any]) -> bool:
    status = status_value(payload)
    if status in SUCCESS_STATUSES or any(token in status for token in SUCCESS_STATUSES):
        return True
    if status in INPUT_REQUIRED_STATUSES or any(token in status for token in INPUT_REQUIRED_STATUSES):
        return True
    return False


def summarize_status(payload: dict[str, Any] | None) -> dict[str, Any] | None:
    if payload is None:
        return None
    status = status_value(payload)
    terminal = is_terminal_status(payload)
    return {
        "jobId": first_string(payload, ("jobId", "jobID", "id", "requestId")),
        "conversationId": first_string(payload, ("conversationId", "conversationID")),
        "status": status or None,
        "terminal": terminal,
        "success": is_success_status(payload) if terminal else None,
        "input_required": status in INPUT_REQUIRED_STATUSES or any(
            token in status for token in INPUT_REQUIRED_STATUSES
        ),
        "message": first_string(payload, ("message", "response", "answer", "output", "result")),
    }


def wait_for_workflow(
    props: dict[str, str],
    access_token: str,
    workflow_code: str,
    job_id: str,
    *,
    path_prefix: str | None,
    invocation_mode: str | None,
    wait_seconds: int,
    poll_interval: int,
    timeout: int,
) -> dict[str, Any]:
    deadline = time.time() + wait_seconds
    last_status: dict[str, Any] | None = None
    while True:
        last_status = get_workflow_status(
            props,
            access_token,
            workflow_code,
            job_id,
            path_prefix=path_prefix,
            invocation_mode=invocation_mode,
            timeout=timeout,
        ).body
        if is_terminal_status(last_status):
            return last_status
        if wait_seconds <= 0 or time.time() >= deadline:
            return last_status
        time.sleep(max(1, poll_interval))


def parse_json_object(value: str, *, argument_name: str) -> dict[str, Any]:
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError(f"{argument_name} must be a JSON object")
    return parsed


def load_payload_fragment(args: argparse.Namespace) -> dict[str, Any]:
    if args.payload and args.payload_file:
        raise ValueError("Provide either --payload or --payload-file, not both")
    if args.payload_file:
        return parse_json_object(Path(args.payload_file).read_text(encoding="utf-8"), argument_name="--payload-file")
    if args.payload:
        return parse_json_object(args.payload, argument_name="--payload")
    return {}


def parse_parameter(value: str) -> tuple[str, Any]:
    if "@file=" in value:
        key, file_path = value.split("@file=", 1)
        if not key:
            raise ValueError(f"Missing parameter name in {value}")
        return key, Path(file_path).read_text(encoding="utf-8")
    if ":=" in value:
        key, raw_json = value.split(":=", 1)
        if not key:
            raise ValueError(f"Missing parameter name in {value}")
        return key, json.loads(raw_json)
    if "=" in value:
        key, parsed_value = value.split("=", 1)
        if not key:
            raise ValueError(f"Missing parameter name in {value}")
        return key, parsed_value
    raise ValueError(f"Expected parameter as name=value, name:=json, or name@file=path: {value}")


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    parsed = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError(f"State file must contain a JSON object: {path}")
    return parsed


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def build_submit_payload(args: argparse.Namespace, state: dict[str, Any]) -> dict[str, Any]:
    payload = load_payload_fragment(args)
    if args.message:
        payload["message"] = args.message
    elif not payload.get("message"):
        raise ValueError("Provide --message, or provide message in --payload/--payload-file")

    if args.conversational:
        payload["conversational"] = True

    conversation_id = args.conversation_id
    if not args.new and not conversation_id:
        saved_conversation_id = state.get("conversationId")
        if isinstance(saved_conversation_id, str) and saved_conversation_id:
            conversation_id = saved_conversation_id
    if not conversation_id and args.client_generated_conversation_id:
        conversation_id = str(uuid.uuid4())
    if conversation_id:
        payload["conversationId"] = conversation_id

    scalar_fields = {
        "invocationMode": args.invocation_mode,
        "version": args.version,
        "status": args.workflow_status,
        "workflowName": args.workflow_name,
        "architecture": args.architecture,
    }
    for key, value in scalar_fields.items():
        if value is not None:
            payload[key] = value

    if args.stream_output is not None:
        payload["streamOutput"] = args.stream_output
    if args.progress_message is not None:
        payload["progressMessage"] = args.progress_message

    if args.agent_code:
        payload["agentCodes"] = args.agent_code
    if args.tool_code:
        payload["toolCodes"] = args.tool_code

    if args.parameter:
        parameters = payload.get("parameters")
        if parameters is None:
            parameters = {}
        if not isinstance(parameters, dict):
            raise ValueError("payload.parameters must be a JSON object when --parameter is used")
        for item in args.parameter:
            key, value = parse_parameter(item)
            parameters[key] = value
        payload["parameters"] = parameters

    if args.resume_node_input:
        payload["resumeNodeInput"] = parse_json_object(
            args.resume_node_input,
            argument_name="--resume-node-input",
        )
    if args.resume_node_input_file:
        payload["resumeNodeInput"] = parse_json_object(
            Path(args.resume_node_input_file).read_text(encoding="utf-8"),
            argument_name="--resume-node-input-file",
        )

    return payload


def update_state(
    *,
    path: Path | None,
    existing_state: dict[str, Any],
    workflow_code: str,
    job_id: str,
    submit_payload: dict[str, Any] | None,
    submit_response: dict[str, Any] | None,
    status_payload: dict[str, Any] | None,
) -> None:
    if path is None:
        return

    conversation_id = None
    for payload in (status_payload, submit_response, submit_payload):
        if payload:
            conversation_id = first_string(payload, ("conversationId", "conversationID"))
            if conversation_id:
                break

    state = dict(existing_state)
    state["workflowCode"] = workflow_code
    state["lastJobId"] = job_id
    state["lastUpdatedEpoch"] = int(time.time())
    if conversation_id:
        state["conversationId"] = conversation_id
    if submit_payload and submit_payload.get("message"):
        history = state.get("chatHistory")
        if not isinstance(history, list):
            history = []
        history.append(
            {
                "role": "user",
                "message": submit_payload["message"],
                "jobId": job_id,
                "epoch": int(time.time()),
            }
        )
        state["chatHistory"] = history[-50:]

    save_state(path, state)


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


def workflow_auth_properties(props: dict[str, str], scope_override: str | None = None) -> dict[str, str]:
    """Select the AI scope, retaining the generic scope as a compatibility fallback."""
    selected_scope = scope_override or props.get("ai_scope") or props.get("scope")
    if not selected_scope or not selected_scope.strip():
        raise ValueError("Missing required OAuth scope property: ai_scope or scope")
    scoped_props = dict(props)
    scoped_props["scope"] = selected_scope.strip()
    return scoped_props


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Submit and track Oracle Fusion AI workflow agent requests.")
    parser.add_argument("--workflow-code", required=True, help="AI Studio workflow code.")
    parser.add_argument("--message", help="Prompt message to submit to the workflow agent.")
    parser.add_argument("--job-id", help="Track an existing workflow job instead of submitting a new request.")
    parser.add_argument("--payload", help="Workflow submit payload JSON object.")
    parser.add_argument("--payload-file", help="Path to a workflow submit payload JSON object.")
    parser.add_argument("--parameter", action="append", help="Parameter as name=value, name:=json, or name@file=path.")
    parser.add_argument("--agent-code", action="append", help="Agent code. May be supplied more than once.")
    parser.add_argument("--tool-code", action="append", help="Tool code. May be supplied more than once.")
    parser.add_argument("--conversation-id")
    parser.add_argument("--conversational", action="store_true")
    parser.add_argument("--new", action="store_true", help="Ignore saved conversationId for this submit.")
    parser.add_argument("--client-generated-conversation-id", action="store_true")
    parser.add_argument(
        "--state-file",
        help="Optional conversation state file path. State is not persisted unless this is supplied.",
    )
    parser.add_argument("--no-state", action="store_true", help="Do not read or write conversation state.")
    parser.add_argument("--invocation-mode", default="END_USER")
    parser.add_argument("--version", type=int)
    parser.add_argument("--workflow-status", default="PUBLISHED", help="Workflow status to send in the submit payload.")
    parser.add_argument("--workflow-name")
    parser.add_argument("--architecture")
    parser.add_argument("--resume-node-input", help="resumeNodeInput JSON object.")
    parser.add_argument("--resume-node-input-file", help="Path to resumeNodeInput JSON object.")
    parser.add_argument("--stream-output", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--progress-message", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--wait-seconds", type=int, default=300)
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--submit-only", action="store_true")
    parser.add_argument("--output", help="Write the structured result JSON to this file.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument(
        "--path-prefix",
        default=DEFAULT_PATH_PREFIX,
        help=(
            "REST path prefix before /orchestrator. Defaults to /api/fusion-ai "
            "based on Oracle A-Team invokeAsync samples. Use '' for the raw OpenAPI path."
        ),
    )
    parser.add_argument("--scope", help="OAuth scope override for this invocation.")
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
    workflow_code: str,
    job_id: str,
    submitted: bool,
    submit_payload: dict[str, Any] | None,
    submit_response: dict[str, Any] | None,
    location: str | None,
    status_payload: dict[str, Any] | None,
    wait_seconds: int,
    poll_interval: int,
) -> dict[str, Any]:
    status_summary = summarize_status(status_payload)
    terminal = bool(status_summary and status_summary["terminal"])
    success = status_summary["success"] if status_summary else None
    return {
        "execution_result": {
            "submitted": submitted,
            "workflowCode": workflow_code,
            "jobId": job_id,
            "terminal": terminal,
            "success": success,
            "status": status_summary,
            "status_payload": status_payload,
            "submit_response": submit_response,
            "location": location,
        },
        "diagnostics": {
            "wait_seconds": wait_seconds,
            "poll_interval": poll_interval,
            "timed_out_waiting": bool(status_payload is not None and not terminal and wait_seconds > 0),
            "submitted_payload_fields": sorted(submit_payload.keys()) if submit_payload else [],
        },
        "audit_summary": {
            "environment": props.get("environment"),
            "rest_host": urllib.parse.urlparse(props.get("restBaseUrl", "")).netloc,
            "workflowCode": workflow_code,
            "jobId": job_id,
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


def run_with_token(props: dict[str, str], access_token: str, args: argparse.Namespace) -> dict[str, Any]:
    state_path = None if args.no_state or not args.state_file else Path(args.state_file)
    state = {} if state_path is None or args.new else load_state(state_path)
    submitted = False
    submit_payload = None
    submit_response = None
    location = None

    if args.job_id:
        job_id = args.job_id
    else:
        submit_payload = build_submit_payload(args, state)
        submit_result = submit_workflow(
            props,
            access_token,
            args.workflow_code,
            submit_payload,
            path_prefix=args.path_prefix,
            timeout=args.timeout,
        )
        job_id = extract_job_id(submit_result.body, submit_result.headers)
        submitted = True
        submit_response = submit_result.body
        location = submit_result.headers.get("Location") or submit_result.headers.get("location")

    status_payload = None
    if not args.submit_only:
        status_payload = wait_for_workflow(
            props,
            access_token,
            args.workflow_code,
            job_id,
            path_prefix=args.path_prefix,
            invocation_mode=args.invocation_mode,
            wait_seconds=args.wait_seconds,
            poll_interval=args.poll_interval,
            timeout=args.timeout,
        )

    update_state(
        path=state_path,
        existing_state=state,
        workflow_code=args.workflow_code,
        job_id=job_id,
        submit_payload=submit_payload,
        submit_response=submit_response,
        status_payload=status_payload,
    )
    return build_result(
        props=props,
        workflow_code=args.workflow_code,
        job_id=job_id,
        submitted=submitted,
        submit_payload=submit_payload,
        submit_response=submit_response,
        location=location,
        status_payload=status_payload,
        wait_seconds=0 if args.submit_only else args.wait_seconds,
        poll_interval=args.poll_interval,
    )


def main() -> int:
    args = parse_args()
    props = read_properties(Path(args.properties))
    require_props(props, ["environment", "restBaseUrl"])
    props = workflow_auth_properties(props, args.scope)
    build_url(props, workflow_resource_path(args.workflow_code, "invokeAsync", path_prefix=args.path_prefix))
    access_token = get_token(props, args)
    try:
        result = run_with_token(props, access_token, args)
    except FusionHttpError as exc:
        if exc.status_code != 401 or args.access_token:
            raise
        print("Cached access token was rejected by Fusion. Running login flow again.", file=sys.stderr)
        access_token = get_token(props, args, force_login=True)
        result = run_with_token(props, access_token, args)

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
