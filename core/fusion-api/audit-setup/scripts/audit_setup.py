#!/usr/bin/env python3
"""Manage Oracle Fusion Audit Setup through REST APIs."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CORE_ROOT = Path(__file__).resolve().parents[3]
REPO_ROOT = CORE_ROOT.parent
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


AUDIT_BASE_PATH = "/fscmRestApi/fndAuditRESTService/audittrail"
DEFAULT_APPLICATION_METADATA_PATH = (
    REPO_ROOT / "knowledge" / "fusion-audit-metadata" / "fnd-audit-webapp-applications.json"
)
SUPPORTED_PRODUCTS = {
    "ODI": "Oracle Data Integrator",
    "ESS": "Enterprise Scheduler Service",
    "MDS": "Metadata Services",
    "SOA": "SOA infrastructure",
    "ADF": "Application Development Framework",
    "OPSS": "Oracle Platform Security Services",
}
SUPPORTED_AUDIT_LEVELS = {"High", "Medium", "Low", "None"}
SUPPORTED_ENABLE_VALUES = {"ON", "OFF"}


@dataclass(frozen=True)
class AuditHttpResult:
    status: int
    headers: dict[str, str]
    body: dict[str, Any]


def normalize_product(product: str) -> str:
    value = product.strip().upper()
    if value not in SUPPORTED_PRODUCTS:
        valid = ", ".join(SUPPORTED_PRODUCTS)
        raise ValueError(f"Unsupported product {product!r}. Valid products: {valid}")
    return value


def normalize_audit_level(audit_level: str) -> str:
    for level in SUPPORTED_AUDIT_LEVELS:
        if audit_level.strip().lower() == level.lower():
            return level
    valid = ", ".join(sorted(SUPPORTED_AUDIT_LEVELS))
    raise ValueError(f"Unsupported audit level {audit_level!r}. Valid levels: {valid}")


def normalize_enable(value: str) -> bool:
    normalized = value.strip().upper()
    if normalized not in SUPPORTED_ENABLE_VALUES:
        raise ValueError("Enable value must be ON or OFF")
    return normalized == "ON"


def require_non_empty(value: str, name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{name} must not be empty")
    return normalized


def load_application_metadata(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"applications": [], "source": {}, "applicationCount": 0}
    parsed = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError(f"Application metadata must contain a JSON object: {path}")
    applications = parsed.get("applications")
    if applications is None:
        parsed["applications"] = []
    elif not isinstance(applications, list) or not all(isinstance(item, str) for item in applications):
        raise ValueError(f"Application metadata applications must be a string array: {path}")
    return parsed


def application_catalog_summary(application: str, metadata_path: str | None) -> dict[str, Any]:
    path = Path(metadata_path) if metadata_path else DEFAULT_APPLICATION_METADATA_PATH
    metadata = load_application_metadata(path)
    applications = metadata.get("applications", [])
    if not isinstance(applications, list):
        applications = []
    return {
        "metadata_path": str(path),
        "application_count": len(applications),
        "known_application": application in applications,
        "source": metadata.get("source", {}),
    }


def build_url(
    props: dict[str, str],
    resource_path: str,
    query_params: dict[str, str] | None = None,
) -> str:
    url = rest_url(props, resource_path)
    if query_params:
        url = f"{url}?{urllib.parse.urlencode(query_params)}"
    return url


def request_json(
    props: dict[str, str],
    resource_path: str,
    *,
    access_token: str,
    payload: dict[str, Any] | None,
    query_params: dict[str, str] | None,
    timeout: int,
) -> AuditHttpResult:
    url = build_url(props, resource_path, query_params)
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    body = json.dumps(payload or {}).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
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
    return AuditHttpResult(status=status, headers=response_headers, body=parsed)


def parse_json_object(value: str, *, argument_name: str) -> dict[str, Any]:
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError(f"{argument_name} must be a JSON object")
    return parsed


def exact_payload(args: argparse.Namespace) -> dict[str, Any] | None:
    payload = getattr(args, "payload", None)
    payload_file = getattr(args, "payload_file", None)
    if payload and payload_file:
        raise ValueError("Provide either --payload or --payload-file, not both")
    if payload_file:
        return parse_json_object(Path(payload_file).read_text(encoding="utf-8"), argument_name="--payload-file")
    if payload:
        return parse_json_object(payload, argument_name="--payload")
    return None


def audit_rows_key(args: argparse.Namespace) -> str:
    if args.body_key not in {"auditData", "auditDate"}:
        raise ValueError("--body-key must be auditData or auditDate")
    return args.body_key


def endpoint_for(command: str) -> str:
    return f"{AUDIT_BASE_PATH}/{command}"


def build_operation_payload(args: argparse.Namespace) -> tuple[str, dict[str, Any] | None, dict[str, str] | None]:
    payload = exact_payload(args)
    if payload is not None:
        return endpoint_for(args.command), payload, None

    if args.command == "get-auditlevel":
        products = [normalize_product(product) for product in args.product] if args.product else list(SUPPORTED_PRODUCTS)
        return endpoint_for(args.command), {"product": products}, None

    if args.command == "set-auditlevel":
        rows = [
            {"product": normalize_product(product), "auditLevel": normalize_audit_level(args.audit_level)}
            for product in args.product
        ]
        return endpoint_for(args.command), {audit_rows_key(args): rows}, None

    if args.command == "get-auditsetup":
        application = require_non_empty(args.application, "application")
        return endpoint_for(args.command), {"application": application}, {"application": application}

    if args.command == "check-auditstatus":
        rows = [
            {
                "businessObject": args.business_object,
                "parentBusinessObject": args.parent_business_object,
            }
        ]
        return endpoint_for(args.command), {audit_rows_key(args): rows}, None

    if args.command == "update-auditstatus":
        row: dict[str, Any] = {
            "businessObject": args.business_object,
            "parentBusinessObject": args.parent_business_object,
            "enable": normalize_enable(args.enable),
        }
        if args.attribute:
            row["attributesList"] = [parse_attribute(value) for value in args.attribute]
        return endpoint_for(args.command), {audit_rows_key(args): [row]}, None

    if args.command == "getaudithistory":
        payload = {
            "fromDate": args.from_date,
            "toDate": args.to_date,
            "product": args.product,
        }
        optional_fields = {
            "user": args.user,
            "eventType": args.event_type,
            "businessObjectType": args.business_object_type,
            "includeChildObjects": args.include_child_objects,
            "includeImpersonator": args.include_impersonator,
            "includeExtendedObjectIdentiferColumns": args.include_extended_object_identifier_columns,
            "includeAttributes": args.include_attributes,
            "timeZone": args.time_zone,
            "attributeDetailMode": args.attribute_detail_mode,
        }
        for key, value in optional_fields.items():
            if value is not None:
                payload[key] = value
        query_params = {
            "fromDate": args.from_date,
            "toDate": args.to_date,
            "product": args.product,
            "pageNumber": str(args.page_number),
            "pageSize": str(args.page_size),
        }
        for key, value in optional_fields.items():
            if value is not None:
                query_params[key] = str(value)
        return endpoint_for(args.command), payload, query_params

    raise ValueError(f"Unsupported command {args.command}")


def parse_attribute(value: str) -> dict[str, Any]:
    parts = value.split("=", 1)
    if len(parts) != 2 or not parts[0]:
        raise ValueError(f"Expected attribute as attributeName=Y|N or attributeName=true|false: {value}")
    name, raw_flag = parts[0], parts[1].strip().lower()
    if raw_flag in {"y", "yes", "true", "on", "1"}:
        auditable = True
    elif raw_flag in {"n", "no", "false", "off", "0"}:
        auditable = False
    else:
        raise ValueError(f"Unsupported auditable flag for {name}: {parts[1]}")
    return {"attributeName": name, "isAuditable": auditable}


def response_rows(body: dict[str, Any]) -> Any:
    if "auditData" in body:
        return body["auditData"]
    if "auditDate" in body:
        return body["auditDate"]
    return None


def response_failed(body: dict[str, Any]) -> bool:
    status = str(body.get("status") or "").strip().upper()
    if status == "FAIL":
        return True
    rows = response_rows(body)
    if isinstance(rows, list):
        return any(isinstance(row, dict) and str(row.get("status") or "").strip().upper() == "FAIL" for row in rows)
    return False


def build_result(
    *,
    props: dict[str, str],
    endpoint: str,
    payload: dict[str, Any] | None,
    query_params: dict[str, str] | None,
    result: AuditHttpResult,
    application_catalog: dict[str, Any] | None = None,
) -> dict[str, Any]:
    normalized_rows = response_rows(result.body)
    diagnostics: dict[str, Any] = {
        "endpoint": endpoint,
        "query_params": query_params,
        "request_payload": payload,
        "response_keys": sorted(result.body.keys()),
    }
    if application_catalog is not None:
        diagnostics["application_catalog"] = application_catalog
    return {
        "execution_result": {
            "http_status": result.status,
            "actionName": result.body.get("actionName"),
            "status": result.body.get("status"),
            "auditData": normalized_rows,
            "raw_response": result.body,
        },
        "diagnostics": diagnostics,
        "audit_summary": {
            "environment": props.get("environment"),
            "rest_host": urllib.parse.urlparse(props.get("restBaseUrl", "")).netloc,
            "endpoint": endpoint,
            "actionName": result.body.get("actionName"),
            "status": result.body.get("status"),
        },
    }


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


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument("--timeout", type=int, default=60, help="HTTP request timeout in seconds.")
    parser.add_argument("--auth-code")
    parser.add_argument("--redirect-url")
    parser.add_argument("--callback-timeout", type=int, default=DEFAULT_CALLBACK_TIMEOUT_SECONDS)
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--force-login", action="store_true")
    parser.add_argument("--access-token")
    parser.add_argument("--open-browser", action="store_true", default=True)
    parser.add_argument("--no-open-browser", action="store_false", dest="open_browser")
    parser.add_argument("--output", help="Write structured result JSON to this file.")
    parser.add_argument(
        "--application-metadata",
        default=str(DEFAULT_APPLICATION_METADATA_PATH),
        help="Application/product metadata catalog used for get-setup diagnostics.",
    )


def add_payload_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--payload", help="Exact JSON payload object to send.")
    parser.add_argument("--payload-file", help="Path to exact JSON payload object to send.")


def add_body_key_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--body-key",
        default="auditData",
        choices=["auditData", "auditDate"],
        help="Array field name for audit rows. Defaults to auditData; 26B OpenAPI metadata uses auditDate.",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage Oracle Fusion Audit Setup REST APIs.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    domains = subparsers.add_parser("domains", help="Print supported audit product/domain codes.")
    domains.add_argument("--json", action="store_true", help="Print as JSON.")

    applications = subparsers.add_parser(
        "applications",
        help="Print known functional application/product names for get-setup.",
    )
    applications.add_argument("--json", action="store_true", help="Print as JSON.")
    applications.add_argument(
        "--application-metadata",
        default=str(DEFAULT_APPLICATION_METADATA_PATH),
        help="Application/product metadata catalog.",
    )

    get_level = subparsers.add_parser("get-level", help="Get audit level for products.")
    get_level.set_defaults(command="get-auditlevel")
    get_level.add_argument("--product", action="append", help="Product code. May be supplied more than once.")
    add_payload_args(get_level)
    add_common_args(get_level)

    set_level = subparsers.add_parser("set-level", help="Set audit level for products.")
    set_level.set_defaults(command="set-auditlevel")
    set_level.add_argument("--product", action="append", required=True, help="Product code. May be supplied more than once.")
    set_level.add_argument("--audit-level", required=True, help="Audit level: High, Medium, Low, or None.")
    add_body_key_arg(set_level)
    add_payload_args(set_level)
    add_common_args(set_level)

    get_setup = subparsers.add_parser("get-setup", help="Get auditable objects for a product.")
    get_setup.set_defaults(command="get-auditsetup")
    get_setup.add_argument("--application", required=True, help="Functional application name, for example Receivables.")
    add_payload_args(get_setup)
    add_common_args(get_setup)

    get_history = subparsers.add_parser(
        "get-history",
        help="Get functional-application or ESS/MDS/OPSS/SOA audit history records.",
    )
    get_history.set_defaults(command="getaudithistory")
    get_history.add_argument("--from-date", required=True)
    get_history.add_argument("--to-date", required=True)
    get_history.add_argument(
        "--product",
        required=True,
        help="Functional application name, or infrastructure domain ESS, MDS, OPSS, or SOA.",
    )
    get_history.add_argument("--user")
    get_history.add_argument("--event-type")
    get_history.add_argument(
        "--business-object-type",
        help=(
            "Required by Fusion for functional-application object history; omit for "
            "ESS, MDS, OPSS, or SOA domain history."
        ),
    )
    get_history.add_argument("--include-child-objects")
    get_history.add_argument("--include-impersonator")
    get_history.add_argument("--include-extended-object-identifier-columns")
    get_history.add_argument("--include-attributes")
    get_history.add_argument("--time-zone")
    get_history.add_argument("--attribute-detail-mode")
    get_history.add_argument("--page-number", type=int, default=1)
    get_history.add_argument("--page-size", type=int, default=50)
    add_payload_args(get_history)
    add_common_args(get_history)

    check_status = subparsers.add_parser("check-status", help="Check audit status for a business object.")
    check_status.set_defaults(command="check-auditstatus")
    check_status.add_argument("--business-object", required=True)
    check_status.add_argument("--parent-business-object", required=True)
    add_body_key_arg(check_status)
    add_payload_args(check_status)
    add_common_args(check_status)

    update_status = subparsers.add_parser("update-status", help="Update audit status for a business object.")
    update_status.set_defaults(command="update-auditstatus")
    update_status.add_argument("--business-object", required=True)
    update_status.add_argument("--parent-business-object", required=True)
    update_status.add_argument(
        "--enable",
        required=True,
        help="ON or OFF; serialized as JSON true or false.",
    )
    update_status.add_argument("--attribute", action="append", help="Attribute audit flag as attributeName=true|false.")
    add_body_key_arg(update_status)
    add_payload_args(update_status)
    add_common_args(update_status)

    return parser.parse_args()


def print_domains(as_json: bool) -> None:
    if as_json:
        print(json.dumps({"products": SUPPORTED_PRODUCTS, "auditLevels": sorted(SUPPORTED_AUDIT_LEVELS)}, indent=2))
        return
    print("Product audit domains:")
    for code, description in SUPPORTED_PRODUCTS.items():
        print(f"- {code}: {description}")
    print("Audit levels: High, Medium, Low, None")


def print_applications(as_json: bool, metadata_path: str) -> None:
    path = Path(metadata_path)
    metadata = load_application_metadata(path)
    applications = metadata.get("applications", [])
    if not isinstance(applications, list):
        applications = []
    if as_json:
        print(json.dumps(metadata, indent=2))
        return
    print(f"Functional application/product names from {path}:")
    for application in applications:
        print(f"- {application}")


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
    endpoint, payload, query_params = build_operation_payload(args)
    result = request_json(
        props,
        endpoint,
        access_token=access_token,
        payload=payload,
        query_params=query_params,
        timeout=args.timeout,
    )
    application_catalog = None
    if args.command == "get-auditsetup" and payload and isinstance(payload.get("application"), str):
        application_catalog = application_catalog_summary(payload["application"], args.application_metadata)
    return build_result(
        props=props,
        endpoint=endpoint,
        payload=payload,
        query_params=query_params,
        result=result,
        application_catalog=application_catalog,
    )


def main() -> int:
    args = parse_args()
    if args.command == "domains":
        print_domains(args.json)
        return 0
    if args.command == "applications":
        print_applications(args.json, args.application_metadata)
        return 0

    props = read_properties(Path(args.properties))
    require_props(props, ["environment", "restBaseUrl"])
    access_token = get_token(props, args)
    try:
        result = run_with_token(props, access_token, args)
    except FusionHttpError as exc:
        if exc.status_code not in {401, 403} or args.access_token:
            raise
        print("Cached access token was rejected by Fusion. Running login flow again.", file=sys.stderr)
        access_token = get_token(props, args, force_login=True)
        result = run_with_token(props, access_token, args)

    write_result(result, args.output)
    if response_failed(result["execution_result"]["raw_response"]):
        return 4
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
