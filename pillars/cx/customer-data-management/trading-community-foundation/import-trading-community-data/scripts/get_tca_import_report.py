#!/usr/bin/env python3
"""Retrieve and summarize a Trading Community Import Management error report."""

from __future__ import annotations

import argparse
import base64
import binascii
import csv
from email import policy
from email.parser import BytesParser
from html import escape
import importlib.util
import io
import json
from pathlib import Path
import re
import sys
from types import ModuleType
from typing import Any, Sequence
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
import zipfile


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = SKILL_ROOT.parents[4]
CORE_ADAPTER_PATH = REPOSITORY_ROOT / "core" / "fusion-api" / "cx-import-export-management" / "scripts" / "cx_import_export_job.py"
DEFAULT_PROPERTIES = REPOSITORY_ROOT / "core" / "auth" / "fusionEnv.properties"
CONTENT_REFERENCE_PATTERN = re.compile(r"^UCMFA[0-9]+$")


class ReportError(RuntimeError):
    """A safe Trading Community report-retrieval error."""


def load_core_adapter() -> ModuleType:
    spec = importlib.util.spec_from_file_location("tca_import_report_core", CORE_ADAPTER_PATH)
    if spec is None or spec.loader is None:
        raise ReportError("The authenticated Fusion client could not be loaded.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE_ADAPTER = load_core_adapter()


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content-id", required=True)
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES))
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def report_request_body(reference: str) -> bytes:
    if not CONTENT_REFERENCE_PATTERN.fullmatch(reference):
        raise ReportError("The Fusion report content ID is invalid.")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ucm="http://www.oracle.com/UCM">
  <soapenv:Header/>
  <soapenv:Body>
    <ucm:GenericRequest webKey="cs">
      <ucm:Service IdcService="GET_FILE">
        <ucm:Document>
          <ucm:Field name="dDocName">{escape(reference)}</ucm:Field>
          <ucm:Field name="RevisionSelectionMethod">Latest</ucm:Field>
        </ucm:Document>
      </ucm:Service>
    </ucm:GenericRequest>
  </soapenv:Body>
</soapenv:Envelope>""".encode("utf-8")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def embedded_xml_report(body: bytes) -> bytes | None:
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return None
    if any(local_name(element.tag) == "Fault" for element in root.iter()):
        raise ReportError("Fusion rejected the import report retrieval request.")
    for element in root.iter():
        if local_name(element.tag) not in {"File", "FileContent", "Content", "primaryFile"}:
            continue
        value = (element.text or "").strip()
        if not value:
            continue
        try:
            decoded = base64.b64decode(value, validate=True)
        except (ValueError, binascii.Error):
            continue
        if decoded:
            return decoded
    return None


def extract_report_bytes(body: bytes, content_type: str) -> bytes:
    lowered_type = content_type.lower()
    if "multipart/" in lowered_type:
        envelope = f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n".encode("utf-8") + body
        message = BytesParser(policy=policy.default).parsebytes(envelope)
        candidates = []
        for part in message.walk():
            if part.is_multipart():
                continue
            payload = part.get_payload(decode=True)
            if payload and part.get_content_type().lower() not in {"text/xml", "application/xop+xml", "application/soap+xml"}:
                candidates.append(payload)
        if candidates:
            return max(candidates, key=len)
    if any(marker in lowered_type for marker in ("application/zip", "application/octet-stream", "text/csv")) and body:
        return body
    embedded = embedded_xml_report(body)
    if embedded:
        return embedded
    raise ReportError("Fusion returned no downloadable report content.")


def fetch_report(reference: str, args: argparse.Namespace) -> bytes:
    properties = CORE_ADAPTER.read_properties(Path(args.properties).expanduser().resolve())
    CORE_ADAPTER.require_props(properties, ["environment", "restBaseUrl"])
    url = CORE_ADAPTER.build_url(properties, CORE_ADAPTER.UCM_GENERIC_SOAP_PATH)
    token_args = argparse.Namespace(
        access_token=None,
        auth_code=None,
        callback_timeout=120,
        force_login=False,
        open_browser=False,
        redirect_url=None,
        timeout=args.timeout,
        token_cache=str(args.token_cache),
    )
    token = CORE_ADAPTER.get_token(properties, token_args)
    request = urllib.request.Request(
        url,
        data=report_request_body(reference),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "multipart/related, application/xop+xml, application/octet-stream, text/xml",
            "Content-Type": "text/xml; charset=UTF-8",
            "SOAPAction": "urn:GenericSoap/GenericSoapOperation",
        },
        method="POST",
    )
    try:
        with CORE_ADAPTER.authorized_urlopen(properties, request, timeout=args.timeout, access_token=token) as response:
            return extract_report_bytes(response.read(), response.headers.get("Content-Type", ""))
    except urllib.error.HTTPError as error:
        error.read()
        raise ReportError(f"Fusion report retrieval returned HTTP {error.code}.") from error
    except urllib.error.URLError as error:
        raise ReportError("The Fusion report endpoint could not be reached.") from error


def csv_payload(report: bytes) -> bytes:
    if not zipfile.is_zipfile(io.BytesIO(report)):
        return report
    with zipfile.ZipFile(io.BytesIO(report)) as archive:
        candidates = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if len(candidates) != 1:
            raise ReportError("The Fusion error report ZIP must contain exactly one CSV file.")
        return archive.read(candidates[0])


def summarize_errors(report: bytes) -> list[dict[str, str]]:
    try:
        text = csv_payload(report).decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ReportError("The Fusion error report is not valid UTF-8 CSV.") from error
    reader = csv.DictReader(io.StringIO(text, newline=""))
    required = {"Error Type", "Error Message", "Comments"}
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise ReportError("The Fusion error report is missing its diagnostic columns.")
    results: list[dict[str, str]] = []
    seen = set()
    for row in reader:
        item = {
            "error_type": str(row.get("Error Type") or "").strip(),
            "message": str(row.get("Error Message") or "").strip(),
            "comments": str(row.get("Comments") or "").strip(),
        }
        key = tuple(item.values())
        if item["message"] and key not in seen:
            seen.add(key)
            results.append(item)
    if not results:
        raise ReportError("The Fusion error report contained no actionable diagnostics.")
    return results


def safe_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def render_markdown(content_id: str, errors: list[dict[str, str]]) -> str:
    lines = [
        "# Trading Community import errors",
        "",
        f"Fusion report: `{content_id}`",
        "",
        "| Type | Error | Diagnostic |",
        "|---|---|---|",
    ]
    lines.extend(
        f"| {safe_cell(item['error_type'])} | {safe_cell(item['message'])} | {safe_cell(item['comments'])} |"
        for item in errors
    )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        content_id = args.content_id.strip()
        errors = summarize_errors(fetch_report(content_id, args))
    except (OSError, ValueError, ReportError) as error:
        print(f"Report retrieval failed: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({"content_id": content_id, "errors": errors}, indent=2))
    else:
        print(render_markdown(content_id, errors))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
