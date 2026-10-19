#!/usr/bin/env python3
"""Call Oracle Fusion UCM HTTP IdcService APIs with the shared OAuth cache."""

from __future__ import annotations

import argparse
import base64
import getpass
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
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
    require_authorized_rest_url,
    get_access_token,
    read_properties,
    require_props,
)


DEFAULT_IDC_SERVICE_PATH = "/cs/idcplg"
DEFAULT_SECURITY_GROUP = "FAFusionImportExport"
DEFAULT_DOCUMENT_TYPE = "Document"
SUPPORTED_METHODS = {"GET", "POST"}
SUPPORTED_AUTH_MODES = {"oauth", "basic"}


def parse_key_value(value: str, *, separator_hint: str = "Name=value") -> tuple[str, str]:
    if "=" in value:
        key, parsed_value = value.split("=", 1)
    elif ":" in value:
        key, parsed_value = value.split(":", 1)
    else:
        raise ValueError(f"Expected {separator_hint}: {value}")
    key = key.strip()
    if not key:
        raise ValueError(f"Missing key in {value}")
    return key, parsed_value.strip()


def parse_repeated_key_values(values: list[str] | None) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values or []:
        key, parsed_value = parse_key_value(value)
        parsed[key] = parsed_value
    return parsed


def build_idc_url(props: dict[str, str], args: argparse.Namespace, fields: dict[str, str] | None = None) -> str:
    endpoint = args.idc_service_path
    url = rest_url(props, endpoint)

    if not fields:
        return url

    separator = "&" if urllib.parse.urlparse(url).query else "?"
    return f"{url}{separator}{urllib.parse.urlencode(fields)}"


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


def get_basic_auth_header(props: dict[str, str], args: argparse.Namespace) -> str:
    username = args.username or props.get("user") or os.environ.get("FUSION_USERNAME")
    if not username:
        raise ValueError("Basic auth requires --username, FUSION_USERNAME, or user in fusionEnv.properties")

    password = args.password
    if args.password_env:
        password = os.environ.get(args.password_env)
        if password is None:
            raise ValueError(f"Environment variable {args.password_env} is not set")
    if password is None and args.prompt_password:
        password = getpass.getpass(f"Fusion password for {username}: ")
    if not password:
        raise ValueError("Basic auth requires --password, --password-env, or --prompt-password")

    credentials = f"{username}:{password}".encode("utf-8")
    return "Basic " + base64.b64encode(credentials).decode("ascii")


def get_authorization_header(props: dict[str, str], args: argparse.Namespace, *, force_login: bool = False) -> str:
    if args.auth_mode == "basic":
        return BoundAccessToken(get_basic_auth_header(props, args), request_context(props))
    token = get_token(props, args, force_login=force_login)
    return BoundAccessToken("Bearer " + token, request_context(props, token))


def request_bytes(
    props: dict[str, str],
    url: str,
    *,
    method: str,
    authorization: str,
    body: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: int,
) -> tuple[bytes, dict[str, str], int]:
    request_headers = dict(headers or {})
    request_headers["Authorization"] = authorization
    request = urllib.request.Request(url, data=body, headers=request_headers, method=method)

    try:
        with authorized_urlopen(props, request, timeout=timeout, access_token=authorization) as response:
            return response.read(), dict(response.headers.items()), response.status
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise FusionHttpError(exc.code, url, error_body) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed calling {url}: {exc.reason}") from exc


def call_with_retry(
    props: dict[str, str],
    args: argparse.Namespace,
    *,
    url: str,
    method: str,
    body: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[bytes, dict[str, str], int]:
    require_authorized_rest_url(props, url)
    authorization = get_authorization_header(props, args)
    try:
        return request_bytes(
            props,
            url,
            method=method,
            authorization=authorization,
            body=body,
            headers=headers,
            timeout=args.timeout,
        )
    except FusionHttpError as exc:
        if args.auth_mode != "oauth" or exc.status_code not in {401, 403} or args.access_token:
            raise
        print("Cached access token was rejected by Fusion. Running login flow again.", file=sys.stderr)
        authorization = get_authorization_header(props, args, force_login=True)
        return request_bytes(
            props,
            url,
            method=method,
            authorization=authorization,
            body=body,
            headers=headers,
            timeout=args.timeout,
        )


def strip_json_prefix(text: str) -> str:
    stripped = text.strip()
    for prefix in ("for(;;);", ")]}',"):
        if stripped.startswith(prefix):
            return stripped[len(prefix) :].strip()
    return stripped


def looks_like_login_page(text: str) -> bool:
    lowered = text.lower()
    return (
        "webcenter content sign in" in lowered
        or "<!--loginform-->" in lowered
        or "idcclientloginform" in lowered
        or "/ui/v1/signin" in lowered
    )


def parse_json_response(content: bytes, url: str) -> dict[str, Any]:
    text = content.decode("utf-8", errors="replace")
    if not text.strip():
        return {}
    if looks_like_login_page(text):
        raise RuntimeError(
            "UCM returned the WebCenter/IDCS sign-in page instead of an IdcService JSON response. "
            "The endpoint is reachable, but this pod is not accepting the supplied Authorization header "
            "for /cs/idcplg."
        )
    try:
        parsed = json.loads(strip_json_prefix(text))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Expected JSON from {url}, got: {text[:1000]}") from exc
    if not isinstance(parsed, dict):
        raise RuntimeError(f"Expected a JSON object from {url}")
    return parsed


def write_json(args: argparse.Namespace, response: dict[str, Any]) -> None:
    rendered = json.dumps(response, indent=2, sort_keys=True)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")
        print(f"Wrote {output_path}")
    else:
        print(rendered)


def encode_multipart(
    fields: dict[str, str],
    file_field: str,
    file_path: Path,
    *,
    file_name: str,
    content_type: str,
) -> tuple[bytes, str]:
    boundary = f"----fdos-ucm-{uuid.uuid4().hex}"
    chunks: list[bytes] = []

    for key, value in fields.items():
        chunks.append(f"--{boundary}\r\n".encode("ascii"))
        chunks.append(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8"))
        chunks.append(str(value).encode("utf-8"))
        chunks.append(b"\r\n")

    chunks.append(f"--{boundary}\r\n".encode("ascii"))
    chunks.append(
        (
            f'Content-Disposition: form-data; name="{file_field}"; filename="{file_name}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode("utf-8")
    )
    chunks.append(file_path.read_bytes())
    chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode("ascii"))
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def extract_local_data(response: dict[str, Any]) -> dict[str, Any]:
    local_data = response.get("LocalData")
    return local_data if isinstance(local_data, dict) else {}


def extract_result_rows(response: dict[str, Any]) -> list[dict[str, Any]]:
    result_sets = response.get("ResultSets")
    if not isinstance(result_sets, dict):
        return []

    rows: list[dict[str, Any]] = []
    for result_set in result_sets.values():
        if not isinstance(result_set, dict):
            continue
        fields = result_set.get("fields")
        raw_rows = result_set.get("rows")
        if not isinstance(fields, list) or not isinstance(raw_rows, list):
            continue
        for raw_row in raw_rows:
            if isinstance(raw_row, list):
                rows.append({str(field): raw_row[index] if index < len(raw_row) else None for index, field in enumerate(fields)})
            elif isinstance(raw_row, dict):
                rows.append(raw_row)
    return rows


def summarize_ucm_response(response: dict[str, Any]) -> dict[str, Any]:
    local_data = extract_local_data(response)
    rows = extract_result_rows(response)
    summary: dict[str, Any] = {
        "localData": {
            key: local_data[key]
            for key in (
                "IdcService",
                "StatusCode",
                "StatusMessage",
                "dID",
                "dDocName",
                "dDocTitle",
                "dDocType",
                "dSecurityGroup",
                "dDocAccount",
                "dOriginalName",
                "DocUrl",
            )
            if key in local_data
        }
    }
    if rows:
        summary["rowCount"] = len(rows)
        summary["firstRows"] = rows[:10]
    return summary


def idc_json_call(
    props: dict[str, str],
    args: argparse.Namespace,
    *,
    fields: dict[str, str],
    method: str = "GET",
    body: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    fields_with_json = dict(fields)
    fields_with_json.setdefault("IsJson", "1")
    if method == "GET":
        url = build_idc_url(props, args, fields_with_json)
    else:
        url = build_idc_url(props, args)
        if body is None:
            body = urllib.parse.urlencode(fields_with_json).encode("utf-8")
            headers = {"Content-Type": "application/x-www-form-urlencoded", **dict(headers or {})}

    content, response_headers, status = call_with_retry(
        props,
        args,
        url=url,
        method=method,
        body=body,
        headers={"Accept": "application/json", **dict(headers or {})},
    )
    response = parse_json_response(content, url)
    if args.include_http:
        response["_http"] = {"status": status, "headers": response_headers}
    return response


def command_ping(props: dict[str, str], args: argparse.Namespace) -> dict[str, Any]:
    response = idc_json_call(props, args, fields={"IdcService": "PING_SERVER"})
    if args.summary:
        return summarize_ucm_response(response)
    return response


def command_info(props: dict[str, str], args: argparse.Namespace) -> dict[str, Any]:
    if args.ddoc_name:
        fields = {"IdcService": "DOC_INFO_BY_NAME", "dDocName": args.ddoc_name}
    elif args.did:
        fields = {"IdcService": "DOC_INFO", "dID": args.did}
    else:
        raise ValueError("Provide --ddoc-name or --did")
    response = idc_json_call(props, args, fields=fields)
    if args.summary:
        return summarize_ucm_response(response)
    return response


def command_search(props: dict[str, str], args: argparse.Namespace) -> dict[str, Any]:
    fields = {
        "IdcService": "GET_SEARCH_RESULTS",
        "QueryText": args.query_text,
        "ResultCount": str(args.result_count),
    }
    if args.sort_field:
        fields["SortField"] = args.sort_field
        fields["SortOrder"] = args.sort_order
    response = idc_json_call(props, args, fields=fields)
    if args.summary:
        return summarize_ucm_response(response)
    return response


def command_upload(props: dict[str, str], args: argparse.Namespace) -> dict[str, Any]:
    file_path = Path(args.file).expanduser()
    if not file_path.exists() or not file_path.is_file():
        raise ValueError(f"Upload file does not exist: {file_path}")
    if not args.document_account:
        raise ValueError("--document-account is required for UCM check-in")

    file_name = args.file_name or file_path.name
    content_type = args.content_type or mimetypes.guess_type(file_name)[0] or "application/octet-stream"
    fields = {
        "IdcService": "CHECKIN_UNIVERSAL",
        "IsJson": "1",
        "dDocTitle": args.title or file_name,
        "dDocType": args.document_type,
        "dSecurityGroup": args.security_group,
        "dDocAccount": args.document_account,
    }
    if args.author:
        fields["dDocAuthor"] = args.author
    if args.comments:
        fields["xComments"] = args.comments
    fields.update(parse_repeated_key_values(args.field))

    if not args.execute:
        return {
            "dryRun": True,
            "method": "POST",
            "endpoint": build_idc_url(props, args),
            "service": "CHECKIN_UNIVERSAL",
            "file": str(file_path),
            "fileName": file_name,
            "contentType": content_type,
            "fileField": args.file_field,
            "fields": fields,
            "message": "No file was uploaded. Re-run with --execute to check in the file to UCM.",
        }

    body, multipart_content_type = encode_multipart(
        fields,
        args.file_field,
        file_path,
        file_name=file_name,
        content_type=content_type,
    )
    response = idc_json_call(
        props,
        args,
        fields={},
        method="POST",
        body=body,
        headers={"Content-Type": multipart_content_type},
    )
    if args.summary:
        return summarize_ucm_response(response)
    return response


def command_download(props: dict[str, str], args: argparse.Namespace) -> dict[str, Any]:
    if not args.output:
        raise ValueError("download requires --output")
    fields = {
        "IdcService": "GET_FILE",
        "Rendition": args.rendition,
    }
    if args.ddoc_name:
        fields["dDocName"] = args.ddoc_name
    elif args.did:
        fields["dID"] = args.did
    else:
        raise ValueError("Provide --ddoc-name or --did")

    url = build_idc_url(props, args, fields)
    content, response_headers, status = call_with_retry(
        props,
        args,
        url=url,
        method="GET",
        headers={"Accept": "application/octet-stream,*/*"},
    )
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(content)
    return {
        "downloaded": True,
        "path": str(output_path),
        "bytes": len(content),
        "httpStatus": status,
        "contentType": response_headers.get("Content-Type", response_headers.get("content-type")),
    }


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument("--idc-service-path", default=DEFAULT_IDC_SERVICE_PATH)
    parser.add_argument("--auth-mode", choices=sorted(SUPPORTED_AUTH_MODES), default="oauth")
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--auth-code")
    parser.add_argument("--redirect-url")
    parser.add_argument("--callback-timeout", type=int, default=DEFAULT_CALLBACK_TIMEOUT_SECONDS)
    parser.add_argument("--force-login", action="store_true")
    parser.add_argument("--access-token")
    parser.add_argument("--username")
    parser.add_argument("--password")
    parser.add_argument("--password-env")
    parser.add_argument("--prompt-password", action="store_true")
    parser.add_argument("--open-browser", action="store_true", default=True)
    parser.add_argument("--no-open-browser", action="store_false", dest="open_browser")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--output")
    parser.add_argument("--include-http", action="store_true")
    parser.add_argument("--summary", action="store_true", help="Print a compact UCM summary instead of the full response.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Call Oracle Fusion UCM HTTP IdcService APIs.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ping = subparsers.add_parser("ping", help="Call PING_SERVER against UCM.")
    add_common_args(ping)

    info = subparsers.add_parser("info", help="Fetch UCM document metadata by dDocName or dID.")
    add_common_args(info)
    info.add_argument("--ddoc-name")
    info.add_argument("--did")

    search = subparsers.add_parser("search", help="Search UCM documents with GET_SEARCH_RESULTS.")
    add_common_args(search)
    search.add_argument("--query-text", required=True)
    search.add_argument("--result-count", type=int, default=20)
    search.add_argument("--sort-field")
    search.add_argument("--sort-order", choices=["Asc", "Desc"], default="Desc")

    upload = subparsers.add_parser("upload", help="Upload/check in a local file to UCM with CHECKIN_UNIVERSAL.")
    add_common_args(upload)
    upload.add_argument("--file", required=True)
    upload.add_argument("--file-name")
    upload.add_argument("--file-field", default="primaryFile")
    upload.add_argument("--content-type")
    upload.add_argument("--title")
    upload.add_argument("--document-type", default=DEFAULT_DOCUMENT_TYPE)
    upload.add_argument("--security-group", default=DEFAULT_SECURITY_GROUP)
    upload.add_argument("--document-account", required=True)
    upload.add_argument("--author")
    upload.add_argument("--comments")
    upload.add_argument("--field", action="append", help="Additional UCM metadata field as Name=value.")
    upload.add_argument("--execute", action="store_true", help="Check in the file. Omit for dry run.")

    download = subparsers.add_parser("download", help="Download a UCM document's primary file with GET_FILE.")
    add_common_args(download)
    download.add_argument("--ddoc-name")
    download.add_argument("--did")
    download.add_argument("--rendition", default="Primary")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    props = read_properties(Path(args.properties))
    require_props(props, ["environment", "restBaseUrl"])
    started_at = time.time()

    if args.command == "ping":
        response = command_ping(props, args)
    elif args.command == "info":
        response = command_info(props, args)
    elif args.command == "search":
        response = command_search(props, args)
    elif args.command == "upload":
        response = command_upload(props, args)
    elif args.command == "download":
        response = command_download(props, args)
    else:
        raise ValueError(f"Unsupported command: {args.command}")

    if args.include_http and isinstance(response, dict):
        response.setdefault("_client", {})["elapsedSeconds"] = round(time.time() - started_at, 3)
    write_json(args, response)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FusionHttpError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
    except (RuntimeError, ValueError, TimeoutError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
