#!/usr/bin/env python3
"""Preview and execute a Document Type REST create with an optional file attachment."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from document_type_attachment import (  # noqa: E402
    PROPERTIES,
    RESOURCE,
    assert_no_duplicate,
    attachment_payload,
    canonical_json,
    file_facts,
    read_properties,
    run_rest,
    sha256_bytes,
    validate_contract as validate_attachment_contract,
)


def validate_parent_contract(description: dict[str, Any]) -> None:
    resource = description.get("Resources", {}).get("hrDocumentTypes", {})
    actions = resource.get("collection", {}).get("actions", [])
    supports_post = any(action.get("name") == "create" and action.get("method") == "POST" for action in actions)
    attributes = {attribute.get("name"): attribute for attribute in resource.get("attributes", [])}
    if not supports_post:
        raise ValueError("Live Document Types collection does not advertise POST create")
    for name in ("DocumentType", "CategoryCode"):
        attribute = attributes.get(name, {})
        if attribute.get("mandatory") is not True or attribute.get("inputRequired") is not True:
            raise ValueError(f"Live Document Type create contract is incompatible for {name}")
    if attributes.get("HierarchyCode", {}).get("mandatory") is True:
        raise ValueError("Live Document Type REST contract unexpectedly requires HierarchyCode")
    validate_attachment_contract({"Resources": {"attachments": resource.get("children", {}).get("attachments", {})}})


def resolve_exact(document_type: str) -> list[dict[str, Any]]:
    escaped = document_type.replace("'", "''")
    response = run_rest(
        RESOURCE,
        query=[f"q=DocumentType='{escaped}'", "onlyData=true", "limit=2"],
    )
    return [item for item in response.get("items", []) if item.get("DocumentType") == document_type]


def parent_payload(document_type: str, category_code: str) -> dict[str, Any]:
    return {"DocumentType": document_type, "CategoryCode": category_code}


def preview_digest(preview: dict[str, Any]) -> str:
    return sha256_bytes(canonical_json(preview))


def build_preview(
    document_type: str,
    category_code: str,
    file_path: Path | None,
    title: str | None,
) -> dict[str, Any]:
    if resolve_exact(document_type):
        raise ValueError(f"A Document Type named {document_type!r} already exists")
    description = run_rest(f"{RESOURCE}/describe")
    validate_parent_contract(description)
    create_payload = parent_payload(document_type, category_code)
    attachment: dict[str, Any] | None = None
    attachment_payload_sha: str | None = None
    if file_path is not None:
        facts = file_facts(file_path)
        resolved_title = title or facts["basename"]
        child_payload = attachment_payload(facts, title=resolved_title)
        attachment = {
            "source_path": str(file_path.resolve()),
            "basename": facts["basename"],
            "mime_type": facts["mime_type"],
            "size_bytes": facts["size_bytes"],
            "sha256": facts["sha256"],
            "title": resolved_title,
        }
        attachment_payload_sha = sha256_bytes(canonical_json(child_payload))
    properties = read_properties(PROPERTIES)
    return {
        "schema_version": "1.0",
        "operation": "create_document_type",
        "approval_required": True,
        "adapter_sha256": sha256_bytes(Path(__file__).read_bytes()),
        "environment": properties.get("environment"),
        "target_base_url": properties.get("restBaseUrl"),
        "document_type": document_type,
        "category_code": category_code,
        "hierarchy_code": None,
        "delivery_preferences": "not requested",
        "parent_endpoint": RESOURCE,
        "parent_payload_fields": sorted(create_payload),
        "parent_payload_sha256": sha256_bytes(canonical_json(create_payload)),
        "attachment": attachment,
        "attachment_payload_sha256": attachment_payload_sha,
        "contract_evidence": {
            "parent_create_method": "POST",
            "hierarchy_code_mandatory": False,
            "attachment_create_method": "POST",
            "attached_document_id_generated": True,
        },
    }


def _write_result(path: Path, result: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


def execute_preview(preview_path: Path, approved_sha256: str, result_path: Path) -> dict[str, Any]:
    preview = json.loads(preview_path.read_text(encoding="utf-8"))
    if preview_digest(preview) != approved_sha256:
        raise ValueError("Approved preview fingerprint does not match the current preview")
    if preview.get("operation") != "create_document_type":
        raise ValueError("Preview operation is not supported")
    if preview.get("adapter_sha256") != sha256_bytes(Path(__file__).read_bytes()):
        raise ValueError("Document Type create adapter changed after preview; rebuild and reapprove")
    if preview.get("hierarchy_code") is not None or preview.get("delivery_preferences") != "not requested":
        raise ValueError("Preview is not a hierarchy-free Document Type create")
    if resolve_exact(preview["document_type"]):
        raise ValueError("The Document Type now exists; rebuild the preview instead of retrying")

    description = run_rest(f"{RESOURCE}/describe")
    validate_parent_contract(description)
    create_payload = parent_payload(preview["document_type"], preview["category_code"])
    if sha256_bytes(canonical_json(create_payload)) != preview["parent_payload_sha256"]:
        raise ValueError("Parent payload changed after preview; rebuild and reapprove")

    attachment_preview = preview.get("attachment")
    facts: dict[str, Any] | None = None
    child_payload: dict[str, Any] | None = None
    if attachment_preview is not None:
        facts = file_facts(Path(attachment_preview["source_path"]))
        if facts["sha256"] != attachment_preview["sha256"] or facts["size_bytes"] != attachment_preview["size_bytes"]:
            raise ValueError("Attachment bytes changed after preview; rebuild and reapprove")
        child_payload = attachment_payload(facts, title=attachment_preview["title"])
        if sha256_bytes(canonical_json(child_payload)) != preview["attachment_payload_sha256"]:
            raise ValueError("Attachment payload changed after preview; rebuild and reapprove")

    parent_response = run_rest(RESOURCE, method="POST", body=create_payload)
    parent_id = parent_response.get("DocumentTypeId")
    if parent_id is None:
        raise RuntimeError("Fusion accepted the parent POST without returning DocumentTypeId; do not retry")
    result: dict[str, Any] = {
        "status": "parent_created",
        "operation": preview["operation"],
        "environment": preview["environment"],
        "document_type": preview["document_type"],
        "category_code": preview["category_code"],
        "hierarchy_code_requested": False,
        "attachment": None,
    }
    _write_result(result_path, result)

    try:
        if child_payload is not None and facts is not None:
            endpoint = f"{RESOURCE}/{parent_id}/child/attachments"
            child_description = run_rest(f"{endpoint}/describe")
            validate_attachment_contract(child_description)
            current = run_rest(endpoint, query=["onlyData=true", "limit=100"])
            assert_no_duplicate(current.get("items", []), facts["basename"])
            child_response = run_rest(endpoint, method="POST", body=child_payload)
            child_id = child_response.get("AttachedDocumentId")
            verified_children = run_rest(endpoint, query=["onlyData=true", "limit=100"])
            if child_id is not None:
                child_matches = [item for item in verified_children.get("items", []) if item.get("AttachedDocumentId") == child_id]
            else:
                child_matches = [item for item in verified_children.get("items", []) if item.get("FileName") == facts["basename"]]
            if len(child_matches) != 1:
                raise RuntimeError(f"Attachment verification found {len(child_matches)} matches; do not retry")
            result["attachment"] = {
                "basename": facts["basename"],
                "mime_type": facts["mime_type"],
                "size_bytes": facts["size_bytes"],
                "sha256": facts["sha256"],
                "verification_match_count": 1,
            }

        parents = resolve_exact(preview["document_type"])
        if len(parents) != 1 or parents[0].get("CategoryCode") != preview["category_code"]:
            raise RuntimeError("Parent verification did not return the approved business state; do not retry")
        result["status"] = "verified"
        result["hierarchy_code_returned"] = parents[0].get("HierarchyCode")
        _write_result(result_path, result)
        return result
    except Exception as exc:
        result["status"] = "partial_parent_created"
        result["error"] = str(exc)
        _write_result(result_path, result)
        raise


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("preview", help="Build an immutable approval preview without changing Fusion")
    plan.add_argument("--document-type", required=True)
    plan.add_argument("--category-code", required=True)
    plan.add_argument("--file", type=Path)
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
        value = build_preview(args.document_type, args.category_code, args.file, args.title)
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
