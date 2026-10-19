#!/usr/bin/env python3
"""Submit and monitor Oracle CX Import Management and Export Management jobs."""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape


CORE_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROPERTIES_PATH = CORE_ROOT / "auth" / "fusionEnv.properties"
AUTH_SCRIPTS_PATH = CORE_ROOT / "auth" / "fusion-oauth-authentication" / "scripts"
sys.path.insert(0, str(AUTH_SCRIPTS_PATH))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import cx_import_approval as approval  # noqa: E402

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


IMPORT_ENDPOINT = "/crmRestApi/resources/11.13.18.05/importActivities"
EXPORT_ENDPOINT = "/crmRestApi/resources/11.13.18.05/bulkExportActivities"
IMPORT_MAPPING_ENDPOINT = "/crmRestApi/resources/11.13.18.05/importMappings"
ERP_INTEGRATIONS_REST_ENDPOINT = "/fscmRestApi/resources/11.13.18.05/erpintegrations"
ERP_INTEGRATION_SERVICE_PATH = "/fscmService/ErpIntegrationService"
UCM_GENERIC_SOAP_PATH = "/idcws/GenericSoapPort"
DEFAULT_UCM_SECURITY_GROUP = "FAFusionImportExport"
ERP_INTEGRATION_NAMESPACE = "http://xmlns.oracle.com/apps/financials/commonModules/shared/model/erpIntegrationService"
DEFAULT_UCM_REST_OPERATION = "uploadFileToUCM"
DEFAULT_UCM_SOAP_OPERATION = "uploadFileToUcm"
CX_IMPORT_UCM_DOCNAME_PREFIX = "UCM"
TERMINAL_STATUS_VALUES = {
    "COMPLETE",
    "COMPLETE_WITH_ERRORS",
    "COMPLETE_WITH_WARNINGS",
    "COMPLETED",
    "COMPLETED_WITH_ERRORS",
    "COMPLETED_WITH_WARNINGS",
    "ERROR",
    "ERRORS",
    "FAILED",
    "CANCELED",
    "CANCELLED",
    "SUCCESS",
    "WARNING",
}


def first_text_match(patterns: list[str], text: str) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            value = match.group(1).strip()
            if value:
                return value
    return None


def looks_like_cx_import_content_id(value: str) -> bool:
    """CX Import Management expects the UCM document name, for example UCMFA06213998."""
    return value.strip().upper().startswith(CX_IMPORT_UCM_DOCNAME_PREFIX)


def xml_field_value(text: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", text).strip())


def result_set_rows(response_text: str, result_set_name: str) -> list[dict[str, str]]:
    result_set_pattern = (
        rf"<(?:\w+:)?ResultSet\s+name=[\"']{re.escape(result_set_name)}[\"'][^>]*>"
        rf"(.*?)</(?:\w+:)?ResultSet>"
    )
    result_set_match = re.search(result_set_pattern, response_text, flags=re.IGNORECASE | re.DOTALL)
    if not result_set_match:
        return []

    rows: list[dict[str, str]] = []
    for row_match in re.finditer(r"<(?:\w+:)?Row[^>]*>(.*?)</(?:\w+:)?Row>", result_set_match.group(1), flags=re.DOTALL):
        row: dict[str, str] = {}
        for field_match in re.finditer(
            r"<(?:\w+:)?Field\s+name=[\"']([^\"']+)[\"'][^>]*>(.*?)</(?:\w+:)?Field>",
            row_match.group(1),
            flags=re.DOTALL,
        ):
            row[field_match.group(1)] = xml_field_value(field_match.group(2))
        if row:
            rows.append(row)
    return rows


def load_json_file(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    parsed = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return parsed


def put_if_value(payload: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        payload[key] = value


def parse_mapping_column(value: str) -> dict[str, str]:
    """Parse ColumnHeader=AttributeCode[:ExampleValue] for import mapping column creation."""
    if "=" not in value:
        raise ValueError(f"Expected mapping column as ColumnHeader=AttributeCode[:ExampleValue], got: {value}")
    column_header, rest = value.split("=", 1)
    column_header = column_header.strip()
    if not column_header:
        raise ValueError(f"Missing ColumnHeader in mapping column: {value}")
    if ":" in rest:
        attribute_code, example_value = rest.split(":", 1)
    else:
        attribute_code, example_value = rest, ""
    attribute_code = attribute_code.strip()
    if not attribute_code:
        raise ValueError(f"Missing AttributeCode in mapping column: {value}")
    payload = {
        "ColumnHeader": column_header,
        "AttributeCode": attribute_code,
    }
    if example_value:
        payload["ExampleValue"] = example_value.strip()
    return payload


def build_import_mapping_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload = load_json_file(args.payload_file)
    put_if_value(payload, "Name", args.name)
    put_if_value(payload, "ObjectCode", args.object_code)
    put_if_value(payload, "Description", args.description)
    columns = [parse_mapping_column(value) for value in args.column or []]
    if columns:
        payload["ImportMappingColumns"] = columns
    if not payload.get("Name"):
        raise ValueError("Import mapping payload requires Name. Use --name or --payload-file.")
    if not payload.get("ObjectCode"):
        raise ValueError("Import mapping payload requires ObjectCode. Use --object-code or --payload-file.")
    if not payload.get("ImportMappingColumns"):
        raise ValueError("Import mapping payload requires at least one column. Use --column or --payload-file.")
    return payload


def build_import_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload = load_json_file(args.payload_file)
    put_if_value(payload, "Name", args.name)
    put_if_value(payload, "Description", args.description)
    put_if_value(payload, "ObjectCode", args.object_code)
    put_if_value(payload, "ImportMapping", args.import_mapping)
    put_if_value(payload, "ImportMode", args.import_mode)
    put_if_value(payload, "NotificationEmail", args.notification_email)
    put_if_value(payload, "Activate", args.activate)
    put_if_value(payload, "Schedule", args.schedule)
    put_if_value(payload, "HighVolume", args.high_volume)
    put_if_value(payload, "EnableCustomBusinessLogic", args.enable_custom_business_logic)

    if args.file_name or args.input_file_content_id:
        if not args.file_name or not args.input_file_content_id:
            raise ValueError("--file-name and --input-file-content-id must be supplied together")
        data_file = {
            "FileName": args.file_name,
            "InputFileContentId": args.input_file_content_id,
        }
        payload["DataFiles"] = [data_file]

    if not payload.get("Name"):
        raise ValueError("Import payload requires Name. Use --name or --payload-file.")
    if not payload.get("ObjectCode") and not payload.get("ImportMapping"):
        raise ValueError("Import payload requires ObjectCode or ImportMapping.")
    if args.execute and not payload.get("DataFiles"):
        raise ValueError("Live import submission requires DataFiles with InputFileContentId.")
    return payload


def build_export_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload = load_json_file(args.payload_file)
    put_if_value(payload, "Name", args.name)
    put_if_value(payload, "Description", args.description)
    put_if_value(payload, "ExportObject", args.export_object)
    put_if_value(payload, "ExportColumnNames", args.export_column_names)
    put_if_value(payload, "ExportFilterCriteria", args.export_filter_criteria)
    put_if_value(payload, "ExportMapping", args.export_mapping)
    put_if_value(payload, "ExportFileName", args.export_file_name)
    put_if_value(payload, "NotificationEMail", args.notification_email)
    put_if_value(payload, "Activate", args.activate)
    put_if_value(payload, "ScheduleModeCd", args.schedule_mode)
    put_if_value(payload, "ScheduleTypeCd", args.schedule_type)
    put_if_value(payload, "EnableSplit", args.enable_split)
    put_if_value(payload, "SplitSize", args.split_size)

    if not payload.get("Name"):
        raise ValueError("Export payload requires Name. Use --name or --payload-file.")
    if not payload.get("ExportObject"):
        raise ValueError("Export payload requires ExportObject. Use --export-object or --payload-file.")
    return payload


def extract_erp_rest_content_id(response: dict[str, Any]) -> str | None:
    for key in ("DocumentId", "documentId", "ContentId", "contentId", "dDocName", "result"):
        value = response.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if value is not None and not isinstance(value, (dict, list)):
            return str(value).strip()

    items = response.get("items")
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict):
                content_id = extract_erp_rest_content_id(item)
                if content_id:
                    return content_id
    return None


def upload_file_to_ucm_rest(props: dict[str, str], args: argparse.Namespace, source: approval.SourceFile) -> dict[str, Any]:
    if not args.ucm_document_account:
        raise ValueError("--ucm-document-account is required when --upload-file is used")
    file_name = args.file_name or source.member_name
    content_type = args.ucm_content_type or Path(source.member_name).suffix.lstrip(".") or "csv"
    encoded_content = base64.b64encode(source.content).decode("ascii")
    operation = args.ucm_operation_name or DEFAULT_UCM_REST_OPERATION
    payload = {
        "OperationName": operation,
        "DocumentContent": encoded_content,
        "FileName": file_name,
        "ContentType": content_type,
        "DocumentAccount": args.ucm_document_account,
        "DocumentId": None,
    }
    if args.ucm_file_type:
        payload["FileType"] = args.ucm_file_type
    if args.ucm_comments:
        payload["Comments"] = args.ucm_comments

    response = call_with_retry(
        props,
        args,
        build_url(props, ERP_INTEGRATIONS_REST_ENDPOINT),
        method="POST",
        payload=payload,
    )
    content_id = extract_erp_rest_content_id(response)
    if not content_id:
        raise RuntimeError(f"ERP Integration REST upload response did not include a recognizable content ID: {response}")
    return {
        "contentId": content_id,
        "fileName": file_name,
        "contentType": content_type,
        "fileType": args.ucm_file_type,
        "documentAccount": args.ucm_document_account,
        "documentSecurityGroup": args.ucm_security_group,
        "uploadMode": "rest",
        "operationName": operation,
        "rawResponse": response,
    }


def upload_file_to_ucm_soap(props: dict[str, str], args: argparse.Namespace, source: approval.SourceFile) -> dict[str, Any]:
    if not args.ucm_document_account:
        raise ValueError("--ucm-document-account is required when --upload-file is used")
    file_name = args.file_name or source.member_name
    content_type = args.ucm_content_type or mimetypes.guess_type(file_name)[0] or "text/csv"
    document_title = args.ucm_document_title or file_name
    encoded_content = base64.b64encode(source.content).decode("ascii")
    service_url = build_url(props, ERP_INTEGRATION_SERVICE_PATH)
    operation = args.ucm_operation_name or DEFAULT_UCM_SOAP_OPERATION
    operation_escaped = escape(operation)
    body = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:typ="http://xmlns.oracle.com/apps/financials/commonModules/shared/model/erpIntegrationService/types/" xmlns:erp="http://xmlns.oracle.com/apps/financials/commonModules/shared/model/erpIntegrationService/">
  <soapenv:Header/>
  <soapenv:Body>
    <typ:{operation_escaped}>
      <typ:document>
        <erp:Content>{encoded_content}</erp:Content>
        <erp:FileName>{escape(file_name)}</erp:FileName>
        <erp:ContentType>{escape(content_type)}</erp:ContentType>
        <erp:DocumentTitle>{escape(document_title)}</erp:DocumentTitle>
        <erp:DocumentAuthor>{escape(args.ucm_document_author or "")}</erp:DocumentAuthor>
        <erp:DocumentSecurityGroup>{escape(args.ucm_security_group)}</erp:DocumentSecurityGroup>
        <erp:DocumentAccount>{escape(args.ucm_document_account)}</erp:DocumentAccount>
      </typ:document>
    </typ:{operation_escaped}>
  </soapenv:Body>
</soapenv:Envelope>"""
    response_text = request_text(
        props,
        service_url,
        method="POST",
        access_token=get_token(props, args),
        body=body.encode("utf-8"),
        headers={
            "Content-Type": "text/xml;charset=UTF-8",
            "SOAPAction": f"{ERP_INTEGRATION_NAMESPACE}/{operation}",
        },
        timeout=args.timeout,
    )
    content_id = first_text_match(
        [
            r"<(?:\w+:)?result(?:\s[^>]*)?>(.*?)</(?:\w+:)?result>",
            r"<(?:\w+:)?ContentId(?:\s[^>]*)?>(.*?)</(?:\w+:)?ContentId>",
            r"<(?:\w+:)?DocumentId(?:\s[^>]*)?>(.*?)</(?:\w+:)?DocumentId>",
            r"<(?:\w+:)?dDocName(?:\s[^>]*)?>(.*?)</(?:\w+:)?dDocName>",
        ],
        response_text,
    )
    if not content_id:
        raise RuntimeError(f"UCM upload response did not include a recognizable content ID: {response_text[:1000]}")
    return {
        "contentId": content_id,
        "fileName": file_name,
        "contentType": content_type,
        "documentAccount": args.ucm_document_account,
        "documentSecurityGroup": args.ucm_security_group,
        "uploadMode": "soap",
        "operationName": operation,
    }


def resolve_ucm_docname_for_document_id(props: dict[str, str], args: argparse.Namespace, document_id: str) -> dict[str, Any]:
    service_url = build_url(props, UCM_GENERIC_SOAP_PATH)
    query_text = f"dID <matches> `{document_id}`"
    body = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ucm="http://www.oracle.com/UCM">
  <soapenv:Header/>
  <soapenv:Body>
    <ucm:GenericRequest webKey="cs">
      <ucm:Service IdcService="GET_SEARCH_RESULTS">
        <ucm:Document>
          <ucm:Field name="QueryText">{escape(query_text)}</ucm:Field>
          <ucm:Field name="ResultCount">20</ucm:Field>
        </ucm:Document>
      </ucm:Service>
    </ucm:GenericRequest>
  </soapenv:Body>
</soapenv:Envelope>"""
    attempts = max(1, args.ucm_resolve_attempts)
    row: dict[str, str] = {}
    doc_name = None
    for attempt in range(1, attempts + 1):
        response_text = request_text(
            props,
            service_url,
            method="POST",
            access_token=get_token(props, args),
            body=body.encode("utf-8"),
            headers={
                "Content-Type": "text/xml; charset=UTF-8",
                "SOAPAction": "urn:GenericSoap/GenericSoapOperation",
            },
            timeout=args.timeout,
        )
        rows = result_set_rows(response_text, "SearchResults")
        matching_rows = [candidate for candidate in rows if candidate.get("dID") == document_id]
        row = matching_rows[0] if len(matching_rows) == 1 else {}
        doc_name = row.get("dDocName")
        if doc_name:
            break
        if attempt < attempts:
            time.sleep(args.ucm_resolve_interval)
    if not doc_name:
        raise RuntimeError(
            f"UCM GenericSoapPort search did not return dDocName for dID {document_id} "
            f"after {attempts} attempt(s)"
        )
    return {
        "documentId": document_id,
        "documentName": doc_name,
        "searchRow": row,
        "resolver": "idcws/GenericSoapPort GET_SEARCH_RESULTS",
    }


def upload_file_to_ucm(props: dict[str, str], args: argparse.Namespace, source: approval.SourceFile) -> dict[str, Any]:
    if args.ucm_upload_mode == "rest":
        upload_summary = upload_file_to_ucm_rest(props, args, source)
    else:
        upload_summary = upload_file_to_ucm_soap(props, args, source)

    content_id = str(upload_summary["contentId"])
    if args.ucm_resolve_docname and not looks_like_cx_import_content_id(content_id):
        resolved = resolve_ucm_docname_for_document_id(props, args, content_id)
        upload_summary["originalContentId"] = content_id
        upload_summary["contentId"] = resolved["documentName"]
        upload_summary["resolvedDocument"] = resolved
    return upload_summary


def build_url(props: dict[str, str], endpoint: str) -> str:
    return rest_url(props, endpoint)


def request_text(
    props: dict[str, str],
    url: str,
    *,
    method: str,
    access_token: str,
    body: bytes | None,
    headers: dict[str, str],
    timeout: int,
) -> str:
    request_headers = dict(headers)
    request_headers["Authorization"] = f"Bearer {access_token}"
    request = urllib.request.Request(url, data=body, headers=request_headers, method=method)
    try:
        with authorized_urlopen(props, request, timeout=timeout, access_token=access_token) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise FusionHttpError(exc.code, url, error_body) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed calling {url}: {exc.reason}") from exc


def request_bytes(
    props: dict[str, str],
    url: str,
    *,
    method: str,
    access_token: str,
    timeout: int,
) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {access_token}", "Accept": "application/octet-stream,application/zip,*/*"},
        method=method,
    )
    try:
        with authorized_urlopen(props, request, timeout=timeout, access_token=access_token) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise FusionHttpError(exc.code, url, error_body) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed calling {url}: {exc.reason}") from exc


def request_json(
    props: dict[str, str],
    url: str,
    *,
    method: str,
    access_token: str,
    json_body: dict[str, Any] | None = None,
    timeout: int,
) -> dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    body = None
    if json_body is not None:
        body = json.dumps(json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with authorized_urlopen(props, request, timeout=timeout, access_token=access_token) as response:
            response_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise FusionHttpError(exc.code, url, error_body) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed calling {url}: {exc.reason}") from exc

    if not response_body.strip():
        return {}
    parsed = json.loads(response_body)
    if not isinstance(parsed, dict):
        raise RuntimeError(f"Expected a JSON object from {url}")
    return parsed


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


def call_with_retry(
    props: dict[str, str],
    args: argparse.Namespace,
    url: str,
    *,
    method: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    require_authorized_rest_url(props, url)
    access_token = get_token(props, args)
    try:
        return request_json(props, url, method=method, access_token=access_token, json_body=payload, timeout=args.timeout)
    except FusionHttpError as exc:
        if exc.status_code not in {401, 403} or args.access_token or method.upper() != "GET":
            raise
        print("Cached access token was rejected by Fusion. Running login flow again.", file=sys.stderr)
        access_token = get_token(props, args, force_login=True)
        return request_json(props, url, method=method, access_token=access_token, json_body=payload, timeout=args.timeout)


def extract_status(response: dict[str, Any]) -> str | None:
    items = response.get("items")
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict):
                item_status = extract_status(item)
                if item_status:
                    return item_status
    for key in ("Status", "status", "RequestStatus", "ProcessStatus"):
        value = response.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def is_terminal_status(status: str | None) -> bool:
    if not status:
        return False
    return status.strip().upper().replace(" ", "_") in TERMINAL_STATUS_VALUES


def poll_status(
    props: dict[str, str],
    args: argparse.Namespace,
    endpoint: str,
) -> dict[str, Any]:
    deadline = time.time() + args.wait_seconds
    last_response: dict[str, Any] = {}
    while time.time() <= deadline:
        url = build_url(props, endpoint)
        last_response = call_with_retry(props, args, url, method="GET")
        if is_terminal_status(extract_status(last_response)):
            return last_response
        time.sleep(args.poll_interval)
    return last_response


def download_enclosure(props: dict[str, str], args: argparse.Namespace, endpoint: str, output_path: Path) -> None:
    url = build_url(props, endpoint)
    require_authorized_rest_url(props, url)
    access_token = get_token(props, args)
    try:
        content = request_bytes(props, url, method="GET", access_token=access_token, timeout=args.timeout)
    except FusionHttpError as exc:
        if exc.status_code not in {401, 403} or args.access_token:
            raise
        print("Cached access token was rejected by Fusion. Running login flow again.", file=sys.stderr)
        access_token = get_token(props, args, force_login=True)
        content = request_bytes(props, url, method="GET", access_token=access_token, timeout=args.timeout)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(content)
    print(f"Wrote {output_path} ({len(content)} bytes)")


def write_response(args: argparse.Namespace, response: dict[str, Any]) -> None:
    rendered = json.dumps(response, indent=2, sort_keys=True)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")
        print(f"Wrote {output_path}")
    else:
        print(rendered)


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--auth-code")
    parser.add_argument("--redirect-url")
    parser.add_argument("--callback-timeout", type=int, default=DEFAULT_CALLBACK_TIMEOUT_SECONDS)
    parser.add_argument("--force-login", action="store_true")
    parser.add_argument("--access-token")
    parser.add_argument("--open-browser", action="store_true", default=True)
    parser.add_argument("--no-open-browser", action="store_false", dest="open_browser")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--output")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Submit and monitor Oracle CX import/export management jobs.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_import = subparsers.add_parser("create-import", help="Create a CX Import Management import activity.")
    add_common_args(create_import)
    create_import.add_argument("--payload-file", help="JSON payload file to merge with CLI values.")
    create_import.add_argument("--name")
    create_import.add_argument("--description")
    create_import.add_argument("--object-code")
    create_import.add_argument("--import-mapping")
    create_import.add_argument("--import-mode", default="CREATE_RECORD")
    create_import.add_argument("--upload-file", help="Local CSV file to upload to UCM before creating the import.")
    create_import.add_argument("--file-name")
    create_import.add_argument("--input-file-content-id")
    create_import.add_argument("--ucm-upload-mode", choices=["rest", "soap"], default="rest")
    create_import.add_argument("--ucm-document-account", help="UCM document account for uploaded import files.")
    create_import.add_argument("--ucm-security-group", default=DEFAULT_UCM_SECURITY_GROUP)
    create_import.add_argument("--ucm-content-type")
    create_import.add_argument("--ucm-file-type")
    create_import.add_argument("--ucm-document-title")
    create_import.add_argument("--ucm-document-author")
    create_import.add_argument("--ucm-comments")
    create_import.add_argument("--ucm-operation-name")
    create_import.add_argument("--ucm-resolve-docname", action="store_true", default=True)
    create_import.add_argument("--no-ucm-resolve-docname", action="store_false", dest="ucm_resolve_docname")
    create_import.add_argument("--ucm-resolve-attempts", type=int, default=6)
    create_import.add_argument("--ucm-resolve-interval", type=int, default=5)
    create_import.add_argument("--notification-email")
    create_import.add_argument("--activate", choices=["YES", "NO"], default="NO")
    create_import.add_argument("--schedule", default="ONE_TIME_IMMEDIATE")
    create_import.add_argument("--high-volume", choices=["YES", "NO"])
    create_import.add_argument("--enable-custom-business-logic", choices=["YES", "NO"])
    create_import.add_argument("--execute", action="store_true", help="Submit the import job. Omit for dry run.")
    create_import.add_argument("--wait-seconds", type=int, default=0)
    create_import.add_argument("--poll-interval", type=int, default=15)

    for command in ("prepare-import", "execute-approved-import"):
        approved = subparsers.add_parser(command, help="Preview or execute an approval-bound local CSV import.")
        add_common_args(approved)
        approved.add_argument("--name", required=True)
        approved.add_argument("--object-code", required=True)
        approved.add_argument("--import-mode", required=True, choices=["CREATE_ONLY", "CREATE_RECORD", "DELETE_RECORD"])
        approved.add_argument("--upload-file", action="append", required=True, help="Data CSV, repeat in exact upload order; mapping CSVs are unsupported.")
        approved.add_argument("--ucm-document-account", required=True)
        approved.add_argument("--activate", choices=["YES", "NO"], default="NO")
        approved.add_argument("--schedule", default="ONE_TIME_IMMEDIATE")
        if command == "execute-approved-import":
            approved.add_argument("--approval-id", required=True)
    approve = subparsers.add_parser("approve-import", help="Record explicit user approval of a protected preview; no Fusion call.")
    approve.add_argument("--approval-id", required=True)
    approve.add_argument("--review-sha256", required=True)
    approve.add_argument("--expires-in", type=int, default=900)
    approve.add_argument("--output")

    create_export = subparsers.add_parser("create-export", help="Create a CX Export Management bulk export activity.")
    add_common_args(create_export)
    create_export.add_argument("--payload-file", help="JSON payload file to merge with CLI values.")
    create_export.add_argument("--name")
    create_export.add_argument("--description")
    create_export.add_argument("--export-object")
    create_export.add_argument("--export-column-names")
    create_export.add_argument("--export-filter-criteria")
    create_export.add_argument("--export-mapping")
    create_export.add_argument("--export-file-name")
    create_export.add_argument("--notification-email")
    create_export.add_argument("--activate", choices=["YES", "NO"], default="NO")
    create_export.add_argument("--schedule-mode", default="ONETIME")
    create_export.add_argument("--schedule-type", default="IMMEDIATE")
    create_export.add_argument("--enable-split", choices=["YES", "NO"])
    create_export.add_argument("--split-size", type=int)
    create_export.add_argument("--execute", action="store_true", help="Submit the export job. Omit for dry run.")
    create_export.add_argument("--wait-seconds", type=int, default=0)
    create_export.add_argument("--poll-interval", type=int, default=15)
    create_export.add_argument("--download-output", help="Download export output here after polling.")
    create_export.add_argument("--download-file-kind", choices=["export", "error"], default="export")

    create_mapping = subparsers.add_parser("create-import-mapping", help="Create a CX import mapping with nested columns.")
    add_common_args(create_mapping)
    create_mapping.add_argument("--payload-file", help="JSON payload file to merge with CLI values.")
    create_mapping.add_argument("--name")
    create_mapping.add_argument("--description")
    create_mapping.add_argument("--object-code", required=False)
    create_mapping.add_argument(
        "--column",
        action="append",
        help="Mapping column as ColumnHeader=AttributeCode[:ExampleValue]. May be supplied more than once.",
    )
    create_mapping.add_argument("--execute", action="store_true", help="Create the import mapping. Omit for dry run.")

    get_import = subparsers.add_parser("get-import", help="Get a CX import activity by ID.")
    add_common_args(get_import)
    get_import.add_argument("--import-activity-id", required=True)

    get_export = subparsers.add_parser("get-export", help="Get a CX bulk export activity by ID.")
    add_common_args(get_export)
    get_export.add_argument("--bulk-export-job-id", required=True)

    upload_ucm = subparsers.add_parser("upload-ucm", help="Upload a local file to UCM through ERP Integration Service.")
    add_common_args(upload_ucm)
    upload_ucm.add_argument("--upload-file", required=True)
    upload_ucm.add_argument("--file-name")
    upload_ucm.add_argument("--ucm-upload-mode", choices=["rest", "soap"], default="rest")
    upload_ucm.add_argument("--ucm-document-account", required=True)
    upload_ucm.add_argument("--ucm-security-group", default=DEFAULT_UCM_SECURITY_GROUP)
    upload_ucm.add_argument("--ucm-content-type")
    upload_ucm.add_argument("--ucm-file-type")
    upload_ucm.add_argument("--ucm-document-title")
    upload_ucm.add_argument("--ucm-document-author")
    upload_ucm.add_argument("--ucm-comments")
    upload_ucm.add_argument("--ucm-operation-name")
    upload_ucm.add_argument("--ucm-resolve-docname", action="store_true", default=True)
    upload_ucm.add_argument("--no-ucm-resolve-docname", action="store_false", dest="ucm_resolve_docname")
    upload_ucm.add_argument("--ucm-resolve-attempts", type=int, default=6)
    upload_ucm.add_argument("--ucm-resolve-interval", type=int, default=5)
    upload_ucm.add_argument("--execute", action="store_true", help="Upload the file. Omit for dry run.")

    download_export = subparsers.add_parser("download-export", help="Download export output enclosure by job ID.")
    add_common_args(download_export)
    download_export.add_argument("--bulk-export-job-id", required=True)
    download_export.add_argument("--file-kind", choices=["export", "error"], default="export")
    download_export.add_argument("--download-output", required=True)

    return parser.parse_args()


def dry_run(endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "dryRun": True,
        "method": "POST",
        "endpoint": endpoint,
        "payload": payload,
        "message": "No job was submitted. Re-run with --execute to call Fusion.",
    }


def approved_properties(args: argparse.Namespace) -> dict[str, str]:
    # The trusted selected profile is fixed by repository code, not an envelope.
    if Path(args.properties).absolute() != DEFAULT_PROPERTIES_PATH.absolute():
        raise approval.ApprovalError("Approved imports require core/auth/fusionEnv.properties")
    if args.access_token or args.auth_code or args.redirect_url:
        raise approval.ApprovalError("Approved imports use managed authentication without credential overrides")
    return read_properties(DEFAULT_PROPERTIES_PATH)


def confirm_import_metadata(props: dict[str, str], args: argparse.Namespace, manifest: dict) -> None:
    code = manifest["payload"]["ObjectCode"]
    endpoint = "/crmRestApi/resources/11.13.18.05/objectMetadata/" + urllib.parse.quote(code, safe="")
    response = call_with_retry(props, args, build_url(props, endpoint + "?fields=UcmAccount&onlyData=true"), method="GET")
    if approval.normalize_account(response.get("UcmAccount")) != manifest["ucm"]["account"]:
        raise approval.ApprovalError("Current exact-object UCM account differs from the approved account")


def approved_import_command(args: argparse.Namespace) -> int:
    if args.command == "approve-import":
        write_response(args, approval.approve(args.approval_id, args.review_sha256, args.expires_in))
        return 0
    # Invalid, expired and reused approvals fail before reading sources or acquiring tokens.
    record = approval.load_approved(args.approval_id) if args.command == "execute-approved-import" else None
    props = approved_properties(args)
    files = approval.read_sources(args.upload_file)
    manifest = approval.import_manifest(props, args, files)
    if record is not None:
        approval.compare(record, manifest)
        # Reserve once before any authenticated traffic. Failure spends the approval;
        # never release it after a timeout or uncertain partial upload.
        approval.consume(args.approval_id, manifest)
    confirm_import_metadata(props, args, manifest)
    if approval.target_context(approved_properties(args)) != manifest["target"]:
        raise approval.ApprovalError("Trusted environment configuration changed during metadata confirmation")
    if record is None:
        write_response(args, approval.prepare(manifest))
        return 0

    uploads = []
    activity_id = None
    try:
        for source in files:
            if time.time() >= record["expiresAt"]:
                raise approval.ApprovalError("Approval expired before UCM upload")
            # All transport values are taken from the compared protected manifest.
            upload_args = argparse.Namespace(**vars(args))
            upload_args.file_name = source.member_name
            upload_args.ucm_upload_mode = manifest["ucm"]["uploadMode"]
            upload_args.ucm_document_account = manifest["ucm"]["account"]
            upload_args.ucm_content_type = manifest["ucm"]["contentType"]
            upload_args.ucm_operation_name = manifest["ucm"]["operation"]
            upload_args.ucm_security_group = DEFAULT_UCM_SECURITY_GROUP
            upload_args.ucm_file_type = upload_args.ucm_comments = None
            upload_args.ucm_resolve_docname = True
            upload_args.ucm_resolve_attempts = 6
            upload_args.ucm_resolve_interval = 5
            uploaded = upload_file_to_ucm(props, upload_args, source)
            content_id = str(uploaded["contentId"])
            if not looks_like_cx_import_content_id(content_id):
                raise approval.ApprovalError("Upload did not resolve to an exact UCM document name")
            uploads.append({"FileName": source.member_name, "InputFileContentId": content_id})
        payload = {**record["manifest"]["payload"], "DataFiles": uploads}
        if time.time() >= record["expiresAt"]:
            raise approval.ApprovalError("Approval expired before import submission")
        result = call_with_retry(props, args, build_url(props, IMPORT_ENDPOINT), method="POST", payload=payload)
        activity_id = result.get("ImportActivityId")
        if not activity_id:
            raise RuntimeError("Import response did not return an activity ID")
    except Exception:
        # Preserve partial-success identifiers, never server bodies or source content.
        write_response(args, {"status": "failed", "failureClass": "process_failed",
                              "approvalId": args.approval_id, "uploadedFiles": uploads,
                              "ImportActivityId": activity_id,
                              "nextAction": "Reconcile UCM/import status before requesting a new approval; do not replay."})
        raise RuntimeError("Approved import failed; approval consumed. See redacted receipt for recovery.") from None
    write_response(args, {"status": "submitted", "approvalId": args.approval_id,
                          "ImportActivityId": activity_id, "uploadedFiles": uploads,
                          "groupSha256": manifest["groupSha256"], **manifest["payload"]})
    return 0


def main() -> int:
    args = parse_args()
    if args.command in {"create-import", "upload-ucm"} and args.execute:
        raise approval.ApprovalError("Bare import/UCM execution is disabled; use execute-approved-import with an approval ID")
    if args.command in {"prepare-import", "approve-import", "execute-approved-import"}:
        try:
            return approved_import_command(args)
        except FusionHttpError:
            raise RuntimeError("Fusion metadata request failed; no server body is exposed. Reconcile the approval before retrying.") from None
    props = read_properties(Path(args.properties))
    require_props(props, ["environment", "restBaseUrl"])

    if args.command == "create-import":
        payload = build_import_payload(args)
        response = dry_run(IMPORT_ENDPOINT, payload)
        response["message"] = "Preview only. Use prepare-import, approve-import, and execute-approved-import for local CSV imports."
        write_response(args, response)
        return 0

    if args.command == "create-export":
        payload = build_export_payload(args)
        if not args.execute:
            write_response(args, dry_run(EXPORT_ENDPOINT, payload))
            return 0
        response = call_with_retry(props, args, build_url(props, EXPORT_ENDPOINT), method="POST", payload=payload)
        export_id = response.get("BulkExportJobId")
        if args.wait_seconds and export_id:
            response["lastPolledStatus"] = poll_status(props, args, f"{EXPORT_ENDPOINT}/{export_id}")
        if args.download_output and export_id:
            enclosure_name = "ExportFileContents" if args.download_file_kind == "export" else "ErrorReportFileContents"
            endpoint = f"{EXPORT_ENDPOINT}/{export_id}/enclosure/{enclosure_name}"
            download_enclosure(props, args, endpoint, Path(args.download_output))
            response["downloadOutput"] = args.download_output
        write_response(args, response)
        return 0

    if args.command == "create-import-mapping":
        payload = build_import_mapping_payload(args)
        if not args.execute:
            write_response(args, dry_run(IMPORT_MAPPING_ENDPOINT, payload))
            return 0
        response = call_with_retry(props, args, build_url(props, IMPORT_MAPPING_ENDPOINT), method="POST", payload=payload)
        write_response(args, response)
        return 0

    if args.command == "get-import":
        response = call_with_retry(props, args, build_url(props, f"{IMPORT_ENDPOINT}/{args.import_activity_id}"), method="GET")
        write_response(args, response)
        return 0

    if args.command == "get-export":
        response = call_with_retry(props, args, build_url(props, f"{EXPORT_ENDPOINT}/{args.bulk_export_job_id}"), method="GET")
        write_response(args, response)
        return 0

    if args.command == "upload-ucm":
        if not args.execute:
            response = {
                "dryRun": True,
                "method": "POST",
                "uploadMode": args.ucm_upload_mode,
                "endpoint": ERP_INTEGRATIONS_REST_ENDPOINT
                if args.ucm_upload_mode == "rest"
                else ERP_INTEGRATION_SERVICE_PATH,
                "file": args.upload_file,
                "fileName": args.file_name or Path(args.upload_file).name,
                "documentAccount": args.ucm_document_account,
                "documentSecurityGroup": args.ucm_security_group,
                "resolveDocumentName": args.ucm_resolve_docname,
                "message": "Preview only. Use the approved import workflow to stage files.",
            }
            write_response(args, response)
            return 0

    if args.command == "download-export":
        enclosure_name = "ExportFileContents" if args.file_kind == "export" else "ErrorReportFileContents"
        endpoint = f"{EXPORT_ENDPOINT}/{args.bulk_export_job_id}/enclosure/{enclosure_name}"
        download_enclosure(props, args, endpoint, Path(args.download_output))
        return 0

    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
