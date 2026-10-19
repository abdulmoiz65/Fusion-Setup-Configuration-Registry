#!/usr/bin/env python3
"""Preview and execute an existing Document Type attachment create via Fusion REST."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


TASK_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = TASK_ROOT.parents[4]
REST_CLIENT = REPO_ROOT / "core/fusion-api/rest-api-client/scripts/fusion_rest_client.py"
PROPERTIES = REPO_ROOT / "core/auth/fusionEnv.properties"
API_VERSION = "11.13.18.05"
RESOURCE = f"/hcmRestApi/resources/{API_VERSION}/hrDocumentTypes"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def read_properties(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def safe_basename(path: Path) -> str:
    name = path.name
    if not name or name in {".", ".."} or "/" in name or "\\" in name:
        raise ValueError("Attachment must have a safe file basename")
    return name


def file_facts(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"Attachment file does not exist: {path}")
    content = path.read_bytes()
    if not content:
        raise ValueError("Attachment file is empty")
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return {
        "basename": safe_basename(path),
        "mime_type": mime_type,
        "size_bytes": len(content),
        "sha256": sha256_bytes(content),
        "content": content,
    }


def attachment_payload(facts: dict[str, Any], *, title: str) -> dict[str, Any]:
    return {
        "DatatypeCode": "FILE",
        "FileName": facts["basename"],
        "Title": title,
        "UploadedFileName": facts["basename"],
        "UploadedFileContentType": facts["mime_type"],
        "FileContents": base64.b64encode(facts["content"]).decode("ascii"),
    }


def run_rest(
    endpoint: str,
    *,
    method: str = "GET",
    query: list[str] | None = None,
    body: dict[str, Any] | None = None,
) -> Any:
    with tempfile.TemporaryDirectory(prefix="doctype-attachment-") as temp_dir:
        response_path = Path(temp_dir) / "response.json"
        command = [
            sys.executable,
            str(REST_CLIENT),
            endpoint,
            "--method",
            method,
            "--output",
            str(response_path),
            "--no-open-browser",
        ]
        for value in query or []:
            command.extend(["--query", value])
        if body is not None:
            body_path = Path(temp_dir) / "request.json"
            body_path.write_bytes(canonical_json(body))
            command.extend(["--body-file", str(body_path)])
        completed = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True)
        if completed.returncode:
            message = (completed.stderr or completed.stdout).strip().splitlines()
            raise RuntimeError(message[-1] if message else "Fusion REST request failed")
        if not response_path.exists():
            raise RuntimeError("Fusion REST client returned no response artifact")
        raw = response_path.read_text(encoding="utf-8")
        return json.loads(raw) if raw.strip() else {}


def resolve_parent(document_type: str) -> dict[str, Any]:
    escaped_document_type = document_type.replace("'", "''")
    response = run_rest(
        RESOURCE,
        query=[f"q=DocumentType='{escaped_document_type}'", "onlyData=true", "limit=2"],
    )
    items = [item for item in response.get("items", []) if item.get("DocumentType") == document_type]
    if len(items) != 1:
        raise ValueError(f"Expected exactly one current Document Type named {document_type!r}; found {len(items)}")
    return items[0]


def validate_contract(description: dict[str, Any]) -> None:
    resource = description.get("Resources", {}).get("attachments", {})
    actions = resource.get("collection", {}).get("actions", [])
    supports_post = any(action.get("name") == "create" and action.get("method") == "POST" for action in actions)
    attributes = {attribute.get("name"): attribute for attribute in resource.get("attributes", [])}
    if not supports_post:
        raise ValueError("Live Document Type attachments collection does not advertise POST create")
    if attributes.get("FileContents", {}).get("type") != "attachment":
        raise ValueError("Live attachment contract does not expose FileContents as an attachment")
    if attributes.get("AttachedDocumentId", {}).get("hasDefaultValueExpression") is not True:
        raise ValueError("Live attachment contract does not generate AttachedDocumentId")


def assert_no_duplicate(items: list[dict[str, Any]], basename: str) -> None:
    matches = [item for item in items if item.get("FileName") == basename or item.get("UploadedFileName") == basename]
    if matches:
        raise ValueError(f"An attachment named {basename!r} already exists; use a separately reviewed replace operation")


def build_preview(document_type: str, file_path: Path, title: str | None) -> dict[str, Any]:
    parent = resolve_parent(document_type)
    parent_id = parent["DocumentTypeId"]
    endpoint = f"{RESOURCE}/{parent_id}/child/attachments"
    description = run_rest(f"{endpoint}/describe")
    validate_contract(description)
    current = run_rest(endpoint, query=["onlyData=true", "limit=100"])
    facts = file_facts(file_path)
    assert_no_duplicate(current.get("items", []), facts["basename"])
    resolved_title = title or facts["basename"]
    payload = attachment_payload(facts, title=resolved_title)
    properties = read_properties(PROPERTIES)
    return {
        "schema_version": "1.0",
        "operation": "create_document_type_attachment",
        "approval_required": True,
        "adapter_sha256": sha256_bytes(Path(__file__).read_bytes()),
        "environment": properties.get("environment"),
        "target_base_url": properties.get("restBaseUrl"),
        "document_type": document_type,
        "technical_target": {
            "document_type_id": parent_id,
            "endpoint": endpoint,
        },
        "attachment": {
            "source_path": str(file_path.resolve()),
            "basename": facts["basename"],
            "mime_type": facts["mime_type"],
            "size_bytes": facts["size_bytes"],
            "sha256": facts["sha256"],
            "title": resolved_title,
        },
        "payload_fields": sorted(payload),
        "payload_sha256": sha256_bytes(canonical_json(payload)),
        "contract_evidence": {
            "collection_create_method": "POST",
            "file_contents_type": "attachment",
            "attached_document_id_generated": True,
        },
        "current_attachment_count": len(current.get("items", [])),
    }


def preview_digest(preview: dict[str, Any]) -> str:
    return sha256_bytes(canonical_json(preview))


def execute_preview(preview_path: Path, approved_sha256: str, result_path: Path) -> dict[str, Any]:
    preview = json.loads(preview_path.read_text(encoding="utf-8"))
    actual_preview_sha = preview_digest(preview)
    if actual_preview_sha != approved_sha256:
        raise ValueError("Approved preview fingerprint does not match the current preview")
    if preview.get("operation") != "create_document_type_attachment":
        raise ValueError("Preview operation is not supported")
    if preview.get("adapter_sha256") != sha256_bytes(Path(__file__).read_bytes()):
        raise ValueError("Attachment adapter changed after preview; rebuild and reapprove")

    parent = resolve_parent(preview["document_type"])
    if parent["DocumentTypeId"] != preview["technical_target"]["document_type_id"]:
        raise ValueError("The resolved Document Type changed after preview; rebuild and reapprove")
    endpoint = preview["technical_target"]["endpoint"]
    description = run_rest(f"{endpoint}/describe")
    validate_contract(description)
    current = run_rest(endpoint, query=["onlyData=true", "limit=100"])
    assert_no_duplicate(current.get("items", []), preview["attachment"]["basename"])

    file_path = Path(preview["attachment"]["source_path"])
    facts = file_facts(file_path)
    if facts["sha256"] != preview["attachment"]["sha256"] or facts["size_bytes"] != preview["attachment"]["size_bytes"]:
        raise ValueError("Attachment bytes changed after preview; rebuild and reapprove")
    payload = attachment_payload(facts, title=preview["attachment"]["title"])
    if sha256_bytes(canonical_json(payload)) != preview["payload_sha256"]:
        raise ValueError("Attachment payload changed after preview; rebuild and reapprove")

    response = run_rest(endpoint, method="POST", body=payload)
    created_id = response.get("AttachedDocumentId")
    verified = run_rest(endpoint, query=["onlyData=true", "limit=100"])
    if created_id is not None:
        matches = [item for item in verified.get("items", []) if item.get("AttachedDocumentId") == created_id]
    else:
        matches = [
            item for item in verified.get("items", [])
            if item.get("FileName") == facts["basename"] or item.get("UploadedFileName") == facts["basename"]
        ]
    status = "verified" if len(matches) == 1 else "unverified"
    result = {
        "status": status,
        "operation": preview["operation"],
        "environment": preview["environment"],
        "document_type": preview["document_type"],
        "attachment": {
            "basename": facts["basename"],
            "mime_type": facts["mime_type"],
            "size_bytes": facts["size_bytes"],
            "sha256": facts["sha256"],
        },
        "created_attachment_id": created_id,
        "response_file_name": response.get("FileName") or response.get("UploadedFileName"),
        "verification_match_count": len(matches),
    }
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if status != "verified":
        raise RuntimeError(f"Fusion accepted the POST but verification found {len(matches)} matching attachments; do not retry")
    return result


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("preview", help="Build an immutable approval preview without changing Fusion")
    plan.add_argument("--document-type", required=True)
    plan.add_argument("--file", required=True, type=Path)
    plan.add_argument("--title")
    plan.add_argument("--output", required=True, type=Path)
    execute = commands.add_parser("execute", help="Execute an exactly approved preview")
    execute.add_argument("--preview", required=True, type=Path)
    execute.add_argument("--approved-preview-sha256", required=True)
    execute.add_argument("--result", required=True, type=Path)
    return root


def main() -> int:
    args = parser().parse_args()
    if args.command == "preview":
        value = build_preview(args.document_type, args.file, args.title)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"preview": str(args.output), "preview_sha256": preview_digest(value)}, indent=2))
        return 0
    result = execute_preview(args.preview, args.approved_preview_sha256, args.result)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
