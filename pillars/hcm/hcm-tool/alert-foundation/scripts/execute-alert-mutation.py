#!/usr/bin/env python3
"""Execute exactly one validated Alert Foundation REST mutation.

This module is an isolated mutation adapter. It obtains authentication before
submission and calls the shared REST transport exactly once. It does not retry
a mutation after an HTTP, transport, or uncertain response failure. Ordinary
mutations remain pending independent read-back; an inline Template Body PATCH
uses the provider's versioned HTTP 200 response-acceptance contract.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import SplitResult, urlsplit


FDOS_ROOT = Path(__file__).resolve().parents[5]
AUTH_SCRIPTS_PATH = FDOS_ROOT / "core" / "auth" / "fusion-oauth-authentication" / "scripts"
REST_CLIENT_SCRIPTS_PATH = FDOS_ROOT / "core" / "fusion-api" / "rest-api-client" / "scripts"
sys.path.insert(0, str(AUTH_SCRIPTS_PATH))
sys.path.insert(0, str(REST_CLIENT_SCRIPTS_PATH))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import alert_batch  # noqa: E402
import execution_receipt  # noqa: E402

from fusion_auth import (  # noqa: E402
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    FusionHttpError,
    get_access_token,
    load_cached_access_token,
    token_cache_path,
    read_properties,
    require_props,
)
from rest_client_common import DEFAULT_PROPERTIES_PATH, build_url, request_bytes  # noqa: E402


RESOURCE_PATH = "/hcmRestApi/resources/11.13.18.05/eventAlerts"
DEFAULT_TOKEN_CACHE = "auto"
REST_FRAMEWORK_VERSION = "9"
ALLOWED_METHODS = {"POST", "PATCH", "DELETE"}
BODY_METHODS = {"POST", "PATCH"}
MAX_RESPONSE_TEXT_CHARS = 4000

_KEY_SEGMENT = r"[^/]+"
_POST_PATHS = (
    re.compile(rf"^{re.escape(RESOURCE_PATH)}$"),
    re.compile(rf"^{re.escape(RESOURCE_PATH)}/{_KEY_SEGMENT}/child/templates$"),
    re.compile(
        rf"^{re.escape(RESOURCE_PATH)}/{_KEY_SEGMENT}/child/templates/"
        rf"{_KEY_SEGMENT}/child/recipients$"
    ),
    re.compile(rf"^{re.escape(RESOURCE_PATH)}/{_KEY_SEGMENT}/action/copyAlert$"),
)
_ITEM_PATHS = (
    re.compile(rf"^{re.escape(RESOURCE_PATH)}/{_KEY_SEGMENT}$"),
    re.compile(
        rf"^{re.escape(RESOURCE_PATH)}/{_KEY_SEGMENT}/child/templates/{_KEY_SEGMENT}$"
    ),
    re.compile(
        rf"^{re.escape(RESOURCE_PATH)}/{_KEY_SEGMENT}/child/templates/"
        rf"{_KEY_SEGMENT}/child/recipients/{_KEY_SEGMENT}$"
    ),
)
_SENSITIVE_FIELD_NAMES = {
    "accesstoken",
    "authorization",
    "body",
    "clientsecret",
    "codeverifier",
    "documentcontent",
    "password",
    "refreshtoken",
    "token",
}


class MutationValidationError(ValueError):
    """A caller-correctable operation or environment validation error."""


def canonical_sha256(value: Any) -> str:
    """Return the Alert contract's canonical JSON SHA-256 digest."""
    canonical = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _origin_parts(value: str, *, label: str) -> tuple[str, str, int]:
    parsed = urlsplit(value)
    if parsed.scheme.lower() != "https" or not parsed.hostname:
        raise MutationValidationError(f"{label} must be an absolute HTTPS URL")
    if parsed.username or parsed.password:
        raise MutationValidationError(f"{label} must not contain user information")
    try:
        port = parsed.port or 443
    except ValueError as exc:
        raise MutationValidationError(f"{label} contains an invalid port") from exc
    return parsed.scheme.lower(), parsed.hostname.lower(), port


def _path_is_allowed(method: str, path: str) -> bool:
    patterns = _POST_PATHS if method == "POST" else _ITEM_PATHS
    return any(pattern.fullmatch(path) for pattern in patterns)


def _validate_uri(uri: str, props: dict[str, str], method: str) -> SplitResult:
    parsed = urlsplit(uri)
    _origin_parts(uri, label="operation uri")
    if parsed.query or parsed.fragment:
        raise MutationValidationError("operation uri must not contain a query or fragment")
    if _origin_parts(uri, label="operation uri") != _origin_parts(
        props["restBaseUrl"],
        label="configured restBaseUrl",
    ):
        raise MutationValidationError(
            "operation uri origin does not match the configured Fusion environment"
        )
    if not _path_is_allowed(method, parsed.path):
        raise MutationValidationError(
            f"{method} is not allowed for Alert Foundation path {parsed.path}"
        )
    return parsed


def validate_operation(
    operation: dict[str, Any],
    props: dict[str, str],
) -> tuple[str, str, dict[str, Any] | None]:
    """Validate one immutable Alert mutation operation before authentication."""
    method_value = operation.get("method")
    if not isinstance(method_value, str) or method_value not in ALLOWED_METHODS:
        raise MutationValidationError(
            "operation method must be exactly POST, PATCH, or DELETE"
        )

    uri_value = operation.get("uri")
    if not isinstance(uri_value, str) or not uri_value:
        raise MutationValidationError("operation uri must be a non-empty string")
    _validate_uri(uri_value, props, method_value)

    payload = operation.get("payload")
    payload_sha256 = operation.get("payload_sha256")
    if method_value in BODY_METHODS:
        if not isinstance(payload, dict):
            raise MutationValidationError(f"{method_value} payload must be a JSON object")
        if not isinstance(payload_sha256, str) or not re.fullmatch(
            r"[0-9A-Fa-f]{64}",
            payload_sha256,
        ):
            raise MutationValidationError(
                f"{method_value} payload_sha256 must be a SHA-256 digest"
            )
        actual_digest = canonical_sha256(payload)
        if actual_digest.lower() != payload_sha256.lower():
            raise MutationValidationError(
                "operation payload does not match the approved payload_sha256"
            )
    else:
        if payload is not None:
            raise MutationValidationError("DELETE must not contain a payload")
        if payload_sha256 not in {None, ""}:
            raise MutationValidationError("DELETE must not contain payload_sha256")
        payload = None

    return method_value, build_url(props, uri_value, {}), payload


def _normalized_field_name(value: str) -> str:
    return "".join(character for character in value.lower() if character.isalnum())


def redact(value: Any, *, field_name: str = "") -> Any:
    """Remove credential and sensitive body fields from structured diagnostics."""
    if _normalized_field_name(field_name) in _SENSITIVE_FIELD_NAMES:
        return "***REDACTED***"
    if isinstance(value, dict):
        return {str(key): redact(item, field_name=str(key)) for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


def response_summary(content: bytes | str) -> dict[str, Any]:
    """Return a bounded, redacted response representation for diagnostics."""
    text = content if isinstance(content, str) else content.decode("utf-8", errors="replace")
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return {
            "text": text[:MAX_RESPONSE_TEXT_CHARS],
            "truncated": len(text) > MAX_RESPONSE_TEXT_CHARS,
        }
    return {"json": redact(parsed)}


def is_inline_template_body_patch(
    method: str,
    url: str,
    payload: dict[str, Any] | None,
) -> bool:
    if method != "PATCH" or not isinstance(payload, dict) or set(payload) != {"Body"}:
        return False
    return bool(_ITEM_PATHS[1].fullmatch(urlsplit(url).path))


def _authentication_failure(exc: Exception) -> dict[str, Any]:
    result: dict[str, Any] = {
        "status": "authentication_failed",
        "classification": "not_submitted",
        "failure_class": "auth_or_authz",
        "stage": "authentication",
        "message": "Authentication failed before the mutation was submitted.",
        "request_attempts": 0,
        "automatic_write_retry": False,
        "outcome_uncertain": False,
    }
    if isinstance(exc, FusionHttpError):
        result["http_status"] = exc.status_code
        result["response"] = response_summary(exc.body)
    return result


def _request_failure(
    exc: Exception,
    *,
    method: str,
    url: str,
) -> dict[str, Any]:
    if isinstance(exc, FusionHttpError):
        failure_class = "auth_or_authz" if exc.status_code in {401, 403} else "fusion_api_error"
        return {
            "status": "external_operation_failed",
            "failure_class": failure_class,
            "stage": "mutation",
            "method": method,
            "uri": url,
            "http_status": exc.status_code,
            "response": response_summary(exc.body),
            "request_attempts": 1,
            "automatic_write_retry": False,
            "outcome_uncertain": False,
        }
    return {
        "status": "external_operation_failed",
        "classification": "outcome_unknown",
        "failure_class": "transport_or_environment",
        "stage": "mutation",
        "method": method,
        "uri": url,
        "message": "The mutation did not receive a definitive HTTP response.",
        "request_attempts": 1,
        "automatic_write_retry": False,
        "outcome_uncertain": True,
    }


def execute_alert_mutation(
    operation: dict[str, Any],
    *,
    properties_path: Path = DEFAULT_PROPERTIES_PATH,
    token_cache: str = DEFAULT_TOKEN_CACHE,
    timeout: int = 60,
    redirect_url: str | None = None,
    auth_code: str | None = None,
    open_browser: bool = True,
    callback_timeout: int = DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    force_login: bool = False,
    execution_mode: str = "sequential",
    approval_phrase: str | None = None,
    source_workbook: str | None = None,
    gate_evidence: dict[str, Any] | None = None,
    cached_token_only: bool = False,
    receipt_output: str | Path | None = None,
) -> dict[str, Any]:
    """Authenticate first, then submit one Alert mutation without REST retry."""
    if timeout <= 0:
        raise MutationValidationError("timeout must be greater than zero")
    if callback_timeout <= 0:
        raise MutationValidationError("callback_timeout must be greater than zero")

    props = read_properties(properties_path)
    require_props(props, ["environment", "restBaseUrl", "scope"])
    receipt: execution_receipt.Receipt | None = None

    def transition(stage: str) -> None:
        if receipt is not None:
            receipt.transition(stage)

    def approved_receipt_path(document: dict[str, Any]) -> Path:
        reference = document["execution_receipt_reference"]
        expected = alert_batch.receipt_reference(document["project_id"], document["attempt_id"])
        if reference != expected:
            raise MutationValidationError("approved receipt reference does not match project and attempt")
        root = FDOS_ROOT.resolve()
        receipt_root = (root / "project" / document["project_id"] / "state" / "runs" / "alert-receipts").resolve()
        resolved = (root / reference).resolve()
        try:
            resolved.relative_to(receipt_root)
        except ValueError as exc:
            raise MutationValidationError("approved receipt resolves outside its project receipt root") from exc
        if resolved != receipt_root / f"{document['attempt_id']}.json":
            raise MutationValidationError("approved receipt path is not the attempt receipt")
        return resolved

    if execution_mode == "batch-create":
        approved = alert_batch.validate_submission(
            operation, approval_phrase=approval_phrase, source_workbook=source_workbook,
            gate_evidence=gate_evidence, configured_origin=props["restBaseUrl"],
        )
        method, url, payload = approved["method"], approved["uri"], approved["payload"]
        request_headers = dict(alert_batch.HEADERS)
        if not cached_token_only:
            return {"status": "not_submitted", "classification": "not_submitted", "failure_class": "approval_blocker",
                    "stage": "authentication_readiness", "message": "batch-create requires --cached-token-only before authentication.",
                    "request_attempts": 0, "automatic_write_retry": False, "outcome_uncertain": False}
        if receipt_output is None:
            raise MutationValidationError("batch-create requires --receipt-output before authentication or dispatch")
        try:
            supplied_receipt = receipt_output.as_posix() if isinstance(receipt_output, Path) else str(receipt_output)
        except ValueError as exc:
            raise MutationValidationError("--receipt-output must be the approved safe relative receipt reference") from exc
        if supplied_receipt != operation["approval_document"]["execution_receipt_reference"]:
            return {"status": "not_submitted", "classification": "not_submitted", "failure_class": "approval_blocker",
                    "stage": "receipt_binding", "message": "--receipt-output does not match the approved receipt reference.",
                    "request_attempts": 0, "automatic_write_retry": False, "outcome_uncertain": False}
        receipt = execution_receipt.Receipt(approved_receipt_path(operation["approval_document"]), operation["approval_document"]["attempt_id"], operation["work_unit_sha256"])
        try:
            receipt.reserve()
            transition("approval_validated")
        except (OSError, ValueError) as exc:
            return {"status": "not_submitted", "classification": "not_submitted", "failure_class": "artifact_persistence",
                    "stage": "receipt_reservation", "message": "Batch receipt could not be reserved before authentication.",
                    "request_attempts": 0, "automatic_write_retry": False, "outcome_uncertain": False}
    elif execution_mode == "sequential":
        method, url, payload = validate_operation(operation, props)
        request_headers = {"REST-Framework-Version": REST_FRAMEWORK_VERSION}
    else:
        raise MutationValidationError("Unsupported execution mode")

    try:
        if cached_token_only:
            if force_login or auth_code or redirect_url:
                raise MutationValidationError("cached-token-only mode is noninteractive and cannot accept login inputs")
            access_token = load_cached_access_token(props, token_cache_path(props, token_cache))
            if not access_token:
                raise RuntimeError("No valid cached token is available for noninteractive mutation")
        else:
            access_token = get_access_token(
                props, redirect_url=redirect_url, auth_code=auth_code, open_browser=open_browser,
                callback_timeout=callback_timeout, token_cache=token_cache, force_login=force_login,
            )
    except (FusionHttpError, OSError, RuntimeError, TimeoutError, ValueError) as exc:
        failure = _authentication_failure(exc)
        if execution_mode == "batch-create":
            failure.pop("response", None)
        return failure

    try:
        transition("authentication_ready")
    except (OSError, ValueError):
        return {"status": "not_submitted", "classification": "not_submitted", "failure_class": "artifact_persistence",
                "stage": "authentication_readiness", "message": "Authentication was ready but its receipt transition failed before dispatch.",
                "request_attempts": 0, "automatic_write_retry": False, "outcome_uncertain": False}

    try:
        # This fsynced transition is deliberately outside the request exception
        # handler: interruption in request_bytes leaves durable unknown outcome.
        try:
            transition("request_started")
        except (OSError, ValueError):
            return {"status": "not_submitted", "classification": "not_submitted", "failure_class": "artifact_persistence",
                    "stage": "request_reservation", "message": "Request-start receipt transition failed before dispatch.",
                    "request_attempts": 0, "automatic_write_retry": False, "outcome_uncertain": False}
        content, response_headers, http_status = request_bytes(
            props,
            url,
            method=method,
            access_token=access_token,
            headers=request_headers,
            json_body=payload,
            timeout=timeout,
        )
    except (FusionHttpError, OSError, RuntimeError, TimeoutError) as exc:
        if isinstance(exc, FusionHttpError):
            try:
                transition("response_received")
            except (OSError, ValueError):
                return {"status": "external_operation_failed", "classification": "response_received",
                        "failure_class": "artifact_persistence", "artifact_persistence_error": "response receipt transition failed after HTTP response",
                        "stage": "response_receipt", "method": method, "uri": url, "http_status": exc.status_code,
                        "request_attempts": 1, "automatic_write_retry": False, "outcome_uncertain": False}
        failure = _request_failure(exc, method=method, url=url)
        if execution_mode == "batch-create":
            # Batch error text may echo the entire payload, including encoded Body.
            failure.pop("response", None)
            definitive = isinstance(exc, FusionHttpError)
            failure.update({"execution_mode": execution_mode, "classification": "response_received" if definitive else "outcome_unknown",
                            "outcome_uncertain": not definitive,
                            "message": "Fusion returned a definitive batch response; reconcile it before recovery." if definitive else "Fusion did not confirm the batch. Reconcile all Alert codes before proposing recovery; do not resubmit."})
        return failure

    try:
        transition("response_received")
    except (OSError, ValueError):
        return {"status": "external_operation_failed", "classification": "response_received",
                "failure_class": "artifact_persistence", "artifact_persistence_error": "response receipt transition failed after HTTP response",
                "stage": "response_receipt", "method": method, "uri": url, "http_status": http_status,
                "request_attempts": 1, "automatic_write_retry": False, "outcome_uncertain": False}

    request_id_headers = {
        name: value
        for name, value in response_headers.items()
        if name.lower() in {"ecid", "opc-request-id", "x-oracle-dms-ecid"}
    }
    if execution_mode == "batch-create":
        try:
            response = json.loads(content)
        except (json.JSONDecodeError, UnicodeError):
            response = None
        verification = alert_batch.inspect_response(payload, response, approved["uri"].removesuffix(alert_batch.ENDPOINT))
        if http_status != 200:
            verification["errors"].append({"message": "Batch did not return the required HTTP 200 response."})
        failed = bool(verification["errors"])
        return {
            "status": "external_operation_failed" if failed else "submitted_pending_verification",
            "classification": "response_received",
            "execution_mode": execution_mode,
            "validation_mode": operation["approval_document"]["validation_mode"],
            "work_unit_sha256": operation["work_unit_sha256"],
            "failure_class": "verification_failed" if failed else None,
            "stage": "batch_response_verification", "method": method, "uri": url,
            "http_status": http_status, "request_attempts": 1,
            "automatic_write_retry": False, "automatic_rollback": False,
            "outcome_uncertain": failed, "request_identifiers": request_id_headers,
            "verification": verification,
            "message": ("Batch needs reconciliation. Review every part before recovery; do not resubmit."
                        if failed else "All batch response parts matched. Independent read-back is still required; stored Body verification is deferred."),
        }
    body_patch = is_inline_template_body_patch(method, url, payload)
    body_patch_accepted = body_patch and http_status == 200
    result: dict[str, Any] = {
        "status": (
            "accepted_response_verified"
            if body_patch_accepted
            else "submitted_pending_verification"
        ),
        "failure_class": None,
        "stage": "verification" if body_patch_accepted else "mutation",
        "method": method,
        "uri": url,
        "http_status": http_status,
        "response": response_summary(content),
        "request_attempts": 1,
        "automatic_write_retry": False,
        "outcome_uncertain": False,
    }
    if request_id_headers:
        result["request_identifiers"] = request_id_headers
    if body_patch:
        result["verification"] = {
            "mode": "mutation_response",
            "accepted_http_statuses": [200],
            "independent_read_back": False,
            "deferred_enhancement": (
                "Verify stored Body content through a supported Body/enclosure read route"
            ),
        }
        if not body_patch_accepted:
            result.update(
                {
                    "status": "external_operation_failed",
                    "failure_class": "fusion_api_error",
                    "stage": "mutation_response_verification",
                    "message": "Template Body PATCH did not return the required HTTP 200 response.",
                }
            )
    return result


def load_operation(path: Path) -> dict[str, Any]:
    """Load one JSON operation object from disk."""
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise MutationValidationError(f"operation file is not valid JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise MutationValidationError("operation file must contain one JSON object")
    return parsed


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Submit one validated Alert Foundation mutation without automatic REST retry."
    )
    result.add_argument("operation_file", help="JSON file containing one approved operation object")
    result.add_argument("--execution-mode", choices=("sequential", "batch-create"), default="sequential")
    result.add_argument("--approval-phrase", help="Exact Confirm Alert Batch phrase; required for batch-create")
    result.add_argument("--source-workbook", help="Original XLSX, rehashed before batch authentication")
    result.add_argument("--gate-evidence", help="JSON evidence required for deep batch-create only; simple uses local gates")
    result.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    result.add_argument("--token-cache", default=DEFAULT_TOKEN_CACHE)
    result.add_argument("--cached-token-only", action="store_true", help="Use only an unexpired cached token; never open login or refresh authentication.")
    result.add_argument("--receipt-output", help="New path for the sanitized immutable batch execution receipt")
    result.add_argument("--timeout", type=int, default=60)
    result.add_argument("--auth-code", help="OAuth authorization code used only before submission")
    result.add_argument("--redirect-url", help="OAuth redirect URI used only before submission")
    result.add_argument("--callback-timeout", type=int, default=DEFAULT_CALLBACK_TIMEOUT_SECONDS)
    result.add_argument(
        "--force-login",
        action="store_true",
        help="Authenticate before submission without using an existing cached token.",
    )
    browser = result.add_mutually_exclusive_group()
    browser.add_argument("--open-browser", action="store_true", dest="open_browser")
    browser.add_argument("--no-open-browser", action="store_false", dest="open_browser")
    result.set_defaults(open_browser=True)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        operation = load_operation(Path(args.operation_file))
        result = execute_alert_mutation(
            operation,
            properties_path=Path(args.properties),
            token_cache=args.token_cache,
            timeout=args.timeout,
            redirect_url=args.redirect_url,
            auth_code=args.auth_code,
            open_browser=args.open_browser,
            callback_timeout=args.callback_timeout,
            force_login=args.force_login,
            execution_mode=args.execution_mode,
            approval_phrase=args.approval_phrase,
            source_workbook=args.source_workbook,
            gate_evidence=load_operation(Path(args.gate_evidence)) if args.gate_evidence else None,
            cached_token_only=args.cached_token_only,
            receipt_output=args.receipt_output,
        )
        exit_code = (
            0
            if result["status"]
            in {"submitted_pending_verification", "accepted_response_verified"}
            else 3
        )
    except (MutationValidationError, OSError, ValueError) as exc:
        result = {
            "status": "validation_failed",
            "failure_class": "approval_blocker" if isinstance(exc, alert_batch.BatchApprovalError) else "input_validation",
            "stage": "preflight",
            "message": str(exc),
            "request_attempts": 0,
            "automatic_write_retry": False,
            "outcome_uncertain": False,
        }
        exit_code = 2
    sys.stdout.write(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
