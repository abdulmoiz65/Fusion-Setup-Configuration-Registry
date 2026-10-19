#!/usr/bin/env python3
"""Plan and prove promotion of catalog-bound Content Item HDL providers.

This local-only coordinator standardizes the evidence and lifecycle gates for
the catalog contexts that remain ``certification-only``.  It never authenticates,
calls Fusion, uploads a package, starts a Data Loader request, or edits the
checked-in provider contract.  Existing routed skills continue to own those
operations.  The coordinator instead creates a durable plan, records a local
duplicate-lock probe, and emits a review-only promotion proposal once the
required receipts are supplied.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
from types import SimpleNamespace
from typing import Any, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
PROVIDER_CONTRACT_PATH = (
    SCRIPT_DIR.parent / "content-items" / "references" / "content-item-catalog-hdl-provider.json"
)
CATALOG_BUILDER_PATH = SCRIPT_DIR / "prepare_catalog_content_item_hdl_package.py"
CONTENT_ITEMS_TASK_CODE = "HRT_MANAGE_PROFILE_CONTENT_ITEMS"
ITEM_CATALOG_TASK_CODE = "ORA_MANAGE_PROFILE_ITEM_CATALOG"
ITEM_CATALOG_REQUIRED_MEMBERS = (
    "ORA_TALENT_PROFILE_ITEM_CATALOG.csv",
    "ORA_TALENT_CATALOG_CONTENT_ITEM.csv",
    "ORA_TALENT_CATALOG_CONTENT_ITEM_RDESC.csv",
)
SCHEMA_VERSION = "1.0"
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}", re.IGNORECASE)
CODE_PATTERN = re.compile(r"[A-Z][A-Z0-9_]*")
RELEASE_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._ -]{0,63}")


class CertificationAutomationError(ValueError):
    """The local certification automation contract was not satisfied."""


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CertificationAutomationError(f"{label} must be a non-empty string")
    return value.strip()


def _require_code(value: Any, label: str) -> str:
    rendered = _require_text(value, label)
    if not CODE_PATTERN.fullmatch(rendered):
        raise CertificationAutomationError(f"{label} must be an uppercase code")
    return rendered


def _require_release(value: Any, label: str) -> str:
    rendered = _require_text(value, label)
    if not RELEASE_PATTERN.fullmatch(rendered):
        raise CertificationAutomationError(f"{label} must be safe informational text or unknown")
    return rendered


def _require_sha256(value: Any, label: str) -> str:
    rendered = _require_text(value, label)
    if not SHA256_PATTERN.fullmatch(rendered):
        raise CertificationAutomationError(f"{label} must be a SHA-256 hex value")
    return rendered.lower()


def _require_count(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise CertificationAutomationError(f"{label} must be a non-negative integer")
    return value


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise CertificationAutomationError(f"{label} could not be read: {path}") from error
    except json.JSONDecodeError as error:
        raise CertificationAutomationError(f"{label} is not valid JSON: {error.msg}") from error
    if not isinstance(value, dict):
        raise CertificationAutomationError(f"{label} must contain a JSON object")
    return value


def _project_path(project_root: Path, supplied: str, label: str, *, must_exist: bool = False) -> Path:
    root = project_root.resolve(strict=True)
    candidate = Path(_require_text(supplied, label))
    if candidate.is_absolute():
        raise CertificationAutomationError(f"{label} must be relative to project_root")
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise CertificationAutomationError(f"{label} resolves outside project_root") from error
    if must_exist and not resolved.is_file():
        raise CertificationAutomationError(f"{label} does not identify an existing file")
    return resolved


def _atomic_create(path: Path, content: bytes) -> None:
    if path.exists():
        raise CertificationAutomationError(f"output already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as destination:
            destination.write(content)
    except OSError as error:
        raise CertificationAutomationError(f"output could not be created: {path}") from error


def _load_provider_contract() -> tuple[dict[str, Any], str]:
    provider = _read_json(PROVIDER_CONTRACT_PATH, "catalog HDL provider contract")
    if provider.get("provider") != "CATALOG_CONTENT_ITEM_V2_HDL":
        raise CertificationAutomationError("catalog HDL provider contract has an unexpected provider")
    if provider.get("task_code") != CONTENT_ITEMS_TASK_CODE:
        raise CertificationAutomationError("catalog HDL provider contract has an unexpected task code")
    contexts = provider.get("contexts")
    if not isinstance(contexts, list) or not contexts:
        raise CertificationAutomationError("catalog HDL provider contract has no contexts")
    names: set[str] = set()
    for context in contexts:
        if not isinstance(context, dict):
            raise CertificationAutomationError("catalog HDL provider contract has an invalid context")
        name = _require_code(context.get("context_name"), "context_name")
        if name in names:
            raise CertificationAutomationError("catalog HDL provider contract has duplicate contexts")
        names.add(name)
        lifecycle = context.get("lifecycle")
        if not isinstance(lifecycle, dict) or lifecycle.get("status") not in {
            "blocked",
            "certification-only",
            "verified",
        }:
            raise CertificationAutomationError(f"catalog HDL provider has an invalid lifecycle for {name}")
    return provider, _sha256_file(PROVIDER_CONTRACT_PATH)


def _context_by_name(provider: dict[str, Any], name: str) -> dict[str, Any]:
    matches = [entry for entry in provider["contexts"] if entry["context_name"] == name]
    if len(matches) != 1:
        raise CertificationAutomationError(f"provider context is not registered exactly once: {name}")
    return matches[0]


def _plan_stages(context: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "id": "preflight",
            "mode": "read-only",
            "owner": "content-items",
            "required_output": "fresh dual-key catalog receipt with zero exact code and name matches",
        },
        {
            "id": "package",
            "mode": "local-create-only",
            "owner": "prepare_catalog_content_item_hdl_package.py",
            "approval": "explicit package-preparation approval",
        },
        {
            "id": "task_hook_preview",
            "mode": "local-validation",
            "owner": "core.data-loader.task-hook",
            "required_output": "archive-bound Task Hook preview",
        },
        {
            "id": "upload",
            "mode": "external-write",
            "owner": "core.data-loader",
            "approval": "explicit approval for the immutable archive SHA-256",
            "automatic_retry": False,
        },
        {
            "id": "load_status",
            "mode": "read-only",
            "owner": "core.data-loader",
            "required_output": "one-row succeeded load receipt with zero failures",
        },
        {
            "id": "catalog_rest_readback",
            "mode": "read-only",
            "owner": "content-items",
            "required_output": "one exact code and one exact name match",
        },
        {
            "id": "item_catalog_export_readback",
            "mode": "read-only-export",
            "owner": "shared.setup-export.task-level-export",
            "task_code": ITEM_CATALOG_TASK_CODE,
            "required_members": list(ITEM_CATALOG_REQUIRED_MEMBERS),
            "unfiltered": True,
        },
        {
            "id": "duplicate_lock",
            "mode": "local-create-blocker",
            "owner": "prepare_catalog_content_item_hdl_package.py",
            "required_output": "blocked before package creation for the exact existing key",
        },
        {
            "id": "promotion_proposal",
            "mode": "local-review-only",
            "owner": "catalog_content_item_certification.py",
            "required_output": "review-only lifecycle promotion proposal",
        },
        {
            "id": "provider_promotion",
            "mode": "reviewed-source-change",
            "owner": "provider contract reviewer",
            "approval": "review and approval before changing certification-only to verified",
        },
    ]


def create_plan(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root)
    provider, provider_sha256 = _load_provider_contract()
    target = _require_code(args.target_environment, "target_environment")
    release = _require_release(args.fusion_release, "fusion_release")
    if args.all_pending:
        selected = [entry for entry in provider["contexts"] if entry["lifecycle"]["status"] == "certification-only"]
    else:
        selected = [_context_by_name(provider, _require_code(args.context, "context"))]
    if not selected:
        raise CertificationAutomationError("no certification-only catalog providers are available")
    for entry in selected:
        if entry["lifecycle"]["status"] != "certification-only":
            raise CertificationAutomationError(
                f"{entry['context_name']} is not certification-only and does not need a certification plan"
            )
    output_path = _project_path(project_root, args.output_json, "output_json")
    if output_path.exists():
        raise CertificationAutomationError("output_json already exists; refusing to overwrite")
    planned = []
    for entry in selected:
        planned.append(
            {
                "context_name": entry["context_name"],
                "template_id": entry["template_id"],
                "child_relation": entry["child_relation"],
                "lifecycle": entry["lifecycle"]["status"],
                "required_fields": entry["required_fields"],
                "fixed_values": entry["fixed_values"],
                "stages": _plan_stages(entry),
            }
        )
    material = {
        "schema_version": SCHEMA_VERSION,
        "status": "certification_automation_plan",
        "provider": provider["provider"],
        "provider_contract_sha256": provider_sha256,
        "target_environment": target,
        "fusion_release": release,
        "content_items_task_code": CONTENT_ITEMS_TASK_CODE,
        "item_catalog_export_task_code": ITEM_CATALOG_TASK_CODE,
        "item_catalog_required_members": list(ITEM_CATALOG_REQUIRED_MEMBERS),
        "providers": planned,
        "safety_controls": {
            "no_automatic_fusion_calls": True,
            "no_automatic_upload": True,
            "no_automatic_retry": True,
            "no_automatic_provider_promotion": True,
        },
        "created_at": _utc_now(),
    }
    result = {**material, "plan_fingerprint": _sha256_bytes(_canonical_json(material))}
    _atomic_create(output_path, json.dumps(result, indent=2, sort_keys=True).encode("utf-8") + b"\n")
    return result


def _load_catalog_builder() -> Any:
    spec = importlib.util.spec_from_file_location("catalog_content_item_hdl_builder", CATALOG_BUILDER_PATH)
    if spec is None or spec.loader is None:
        raise CertificationAutomationError("catalog HDL package builder could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def build_duplicate_lock_receipt(args: argparse.Namespace) -> dict[str, Any]:
    """Derive one fresh builder-compatible collision receipt from exact REST readback."""
    project_root = Path(args.project_root)
    input_path = _project_path(project_root, args.input_json, "input_json", must_exist=True)
    rest_path = _project_path(project_root, args.rest_readback_json, "rest_readback_json", must_exist=True)
    output_path = _project_path(project_root, args.output_json, "output_json")
    if output_path.exists():
        raise CertificationAutomationError("output_json already exists; refusing to overwrite")
    payload = _read_json(input_path, "input_json")
    row = payload.get("row")
    if not isinstance(row, dict):
        raise CertificationAutomationError("input_json must contain a provider row")
    context = _require_code(row.get("ContextName"), "row.ContextName")
    original_receipt_value = payload.get("current_state_receipt_path")
    original_receipt_path = _project_path(
        project_root, _require_text(original_receipt_value, "current_state_receipt_path"), "current_state_receipt_path", must_exist=True
    )
    original = _read_json(original_receipt_path, "current_state_receipt")
    rest = _read_json(rest_path, "rest_readback_json")
    if rest.get("status") != "complete" or rest.get("coverage") != "complete":
        raise CertificationAutomationError("REST readback must be complete")
    if rest.get("target_environment") != payload.get("target_environment"):
        raise CertificationAutomationError("REST readback must use the approved target")
    if rest.get("context_name") != context:
        raise CertificationAutomationError("REST readback context does not match the package input")
    if rest.get("exact_code_match_count") != 1 or rest.get("exact_name_match_count") != 1:
        raise CertificationAutomationError("REST readback must contain one exact code and name match")
    expected_code = row.get("ContentItemCode")
    expected_name = row.get("Name")
    for field in ("code_matches", "name_matches"):
        matches = rest.get(field)
        if not isinstance(matches, list) or len(matches) != 1:
            raise CertificationAutomationError(f"REST readback {field} must contain one exact row")
        if matches[0].get("ContentItemCode") != expected_code or matches[0].get("Name") != expected_name:
            raise CertificationAutomationError("REST readback exact identity does not match the package input")
    intended = [
        item
        for item in rest.get("catalogs", [])
        if isinstance(item, dict)
        and item.get("catalog_code") == original.get("catalog_code")
        and item.get("catalog_name") == original.get("catalog_name")
        and item.get("exact_code_match_count") == 1
        and item.get("exact_name_match_count") == 1
    ]
    if len(intended) != 1:
        raise CertificationAutomationError("REST readback did not locate the exact item in the original catalog")
    builder = _load_catalog_builder()
    try:
        body = {key: original[key] for key in builder.RECEIPT_KEYS - {"evidence_sha256"}}
    except KeyError as error:
        raise CertificationAutomationError("original current-state receipt is incomplete") from error
    body.update(
        {
            "captured_at": rest.get("captured_at"),
            "valid_through": rest.get("valid_through"),
            "complete": True,
            "exact_content_item_code_matches": 1,
            "exact_content_item_name_matches": 1,
        }
    )
    if not isinstance(body["captured_at"], str) or not isinstance(body["valid_through"], str):
        raise CertificationAutomationError("REST readback is missing freshness timestamps")
    result = {**body, "evidence_sha256": _sha256_bytes(_canonical_json(body))}
    _atomic_create(output_path, json.dumps(result, indent=2, sort_keys=True).encode("utf-8") + b"\n")
    return result


def verify_duplicate_lock(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root)
    input_path = _project_path(project_root, args.input_json, "input_json", must_exist=True)
    receipt_path = _project_path(
        project_root, args.current_state_receipt_json, "current_state_receipt_json", must_exist=True
    )
    probe_input_path = _project_path(project_root, args.probe_input_json, "probe_input_json")
    probe_zip_path = _project_path(project_root, args.probe_output_zip, "probe_output_zip")
    probe_readiness_path = _project_path(project_root, args.probe_readiness_report, "probe_readiness_report")
    output_path = _project_path(project_root, args.output_json, "output_json")
    if any(path.exists() for path in (probe_input_path, probe_zip_path, probe_readiness_path, output_path)):
        raise CertificationAutomationError("duplicate-lock outputs must not already exist")
    payload = _read_json(input_path, "input_json")
    row = payload.get("row")
    if not isinstance(row, dict):
        raise CertificationAutomationError("input_json must contain a provider row")
    context = _require_code(row.get("ContextName"), "row.ContextName")
    receipt = _read_json(receipt_path, "current_state_receipt_json")
    if receipt.get("target_environment") != payload.get("target_environment"):
        raise CertificationAutomationError("duplicate-lock receipt must use the approved target environment")
    if receipt.get("content_type_context") != context:
        raise CertificationAutomationError("duplicate-lock receipt context does not match the package input")
    if receipt.get("exact_content_item_code_matches", 0) < 1 or receipt.get("exact_content_item_name_matches", 0) < 1:
        raise CertificationAutomationError("duplicate-lock receipt does not prove an exact code and name collision")
    exact_key = receipt.get("exact_key")
    if not isinstance(exact_key, dict) or exact_key.get("ContentItemCode") != row.get("ContentItemCode") or exact_key.get("Name") != row.get("Name"):
        raise CertificationAutomationError("duplicate-lock receipt identity does not match the package input")
    probe_payload = dict(payload)
    probe_payload["current_state_receipt_path"] = str(receipt_path.relative_to(project_root.resolve()))
    probe_payload["current_state_receipt_sha256"] = _sha256_file(receipt_path)
    _atomic_create(probe_input_path, json.dumps(probe_payload, indent=2, sort_keys=True).encode("utf-8") + b"\n")
    builder = _load_catalog_builder()
    try:
        builder.prepare(
            SimpleNamespace(
                project_root=str(project_root),
                input_json=str(probe_input_path.relative_to(project_root.resolve())),
                output_zip=str(probe_zip_path.relative_to(project_root.resolve())),
                readiness_report=str(probe_readiness_path.relative_to(project_root.resolve())),
                as_of=args.as_of,
            )
        )
    except Exception as error:  # Builder owns its exact refusal taxonomy.
        if probe_zip_path.exists() or probe_readiness_path.exists():
            raise CertificationAutomationError("duplicate probe wrote a package or readiness receipt") from error
        if "zero exact code and name matches" not in str(error):
            raise CertificationAutomationError(
                "duplicate probe was blocked for a reason other than the exact existing key"
            ) from error
        material = {
            "schema_version": SCHEMA_VERSION,
            "status": "blocked",
            "stage": "duplicate_lock",
            "failure_class": "duplicate_existing_key",
            "blocked_before_package_creation": True,
            "target_environment": payload["target_environment"],
            "fusion_release": payload["fusion_release"],
            "context_name": context,
            "content_item_code": row["ContentItemCode"],
            "content_item_name": row["Name"],
            "current_state_receipt_sha256": probe_payload["current_state_receipt_sha256"],
            "probe_input_path": str(probe_input_path.relative_to(project_root.resolve())),
            "message": str(error),
            "captured_at": _utc_now(),
        }
        result = {**material, "evidence_fingerprint": _sha256_bytes(_canonical_json(material))}
        _atomic_create(output_path, json.dumps(result, indent=2, sort_keys=True).encode("utf-8") + b"\n")
        return result
    raise CertificationAutomationError("duplicate probe was not blocked before package creation")


def _require_selected_plan(plan: dict[str, Any], context: str, provider_sha256: str) -> dict[str, Any]:
    if plan.get("schema_version") != SCHEMA_VERSION or plan.get("status") != "certification_automation_plan":
        raise CertificationAutomationError("plan_json is not a certification automation plan")
    if _require_sha256(plan.get("provider_contract_sha256"), "plan.provider_contract_sha256") != provider_sha256:
        raise CertificationAutomationError("provider contract changed after the certification plan was created")
    providers = plan.get("providers")
    if not isinstance(providers, list):
        raise CertificationAutomationError("plan_json does not contain providers")
    matches = [entry for entry in providers if isinstance(entry, dict) and entry.get("context_name") == context]
    if len(matches) != 1:
        raise CertificationAutomationError("plan_json does not select the requested provider context")
    return matches[0]


def _validate_load_receipt(receipt: dict[str, Any], *, context: str, target: str, release: str) -> None:
    if receipt.get("schema_version") != SCHEMA_VERSION or receipt.get("status") != "complete":
        raise CertificationAutomationError("data-load receipt is not complete")
    if receipt.get("load_status") != "Succeeded":
        raise CertificationAutomationError("data-load receipt is not successful")
    if receipt.get("context_name") != context or receipt.get("target_environment") != target:
        raise CertificationAutomationError("data-load receipt does not match the selected provider")
    request_id = _require_text(receipt.get("request_id"), "data-load receipt request_id")
    if not request_id.isdigit() or int(request_id) < 1:
        raise CertificationAutomationError("data-load receipt request_id must be a positive integer")
    total = _require_count(receipt.get("total"), "data-load receipt total")
    loaded = _require_count(receipt.get("loaded"), "data-load receipt loaded")
    failed = _require_count(receipt.get("failed"), "data-load receipt failed")
    if total != 1 or loaded != 1 or failed != 0:
        raise CertificationAutomationError("data-load receipt must prove exactly one successful row and zero failures")


def _validate_readback(receipt: dict[str, Any], *, context: str, target: str, release: str, provider_sha256: str) -> None:
    if receipt.get("schema_version") != SCHEMA_VERSION or receipt.get("status") != "verified":
        raise CertificationAutomationError("catalog readback receipt is not verified")
    if receipt.get("context_name") != context or receipt.get("target_environment") != target:
        raise CertificationAutomationError("catalog readback receipt does not match the selected provider")
    if _require_sha256(receipt.get("provider_contract_sha256"), "catalog readback provider_contract_sha256") != provider_sha256:
        raise CertificationAutomationError("catalog readback receipt was created against a different provider contract")
    required_counts = ("exact_rest_code_matches", "exact_rest_name_matches", "exact_export_catalog_matches", "exact_export_item_matches")
    if any(receipt.get(field) != 1 for field in required_counts):
        raise CertificationAutomationError("catalog readback receipt does not contain exact dual-provider matches")
    if receipt.get("differing_fields") != []:
        raise CertificationAutomationError("catalog readback receipt contains field differences")


def _validate_duplicate_lock(receipt: dict[str, Any], *, context: str, target: str, release: str) -> None:
    if receipt.get("schema_version") != SCHEMA_VERSION or receipt.get("status") != "blocked":
        raise CertificationAutomationError("duplicate-lock receipt is not blocked")
    if receipt.get("stage") != "duplicate_lock" or receipt.get("failure_class") != "duplicate_existing_key":
        raise CertificationAutomationError("duplicate-lock receipt does not prove an existing key")
    if receipt.get("blocked_before_package_creation") is not True:
        raise CertificationAutomationError("duplicate-lock receipt did not block before package creation")
    if receipt.get("context_name") != context or receipt.get("target_environment") != target:
        raise CertificationAutomationError("duplicate-lock receipt does not match the selected provider")


def create_promotion_proposal(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root)
    plan_path = _project_path(project_root, args.plan_json, "plan_json", must_exist=True)
    load_path = _project_path(project_root, args.data_load_receipt_json, "data_load_receipt_json", must_exist=True)
    readback_path = _project_path(project_root, args.catalog_readback_json, "catalog_readback_json", must_exist=True)
    duplicate_path = _project_path(project_root, args.duplicate_lock_json, "duplicate_lock_json", must_exist=True)
    output_path = _project_path(project_root, args.output_json, "output_json")
    if output_path.exists():
        raise CertificationAutomationError("output_json already exists; refusing to overwrite")
    context = _require_code(args.context, "context")
    provider, provider_sha256 = _load_provider_contract()
    provider_context = _context_by_name(provider, context)
    if provider_context["lifecycle"]["status"] != "certification-only":
        raise CertificationAutomationError("only certification-only contexts can produce a promotion proposal")
    plan = _read_json(plan_path, "plan_json")
    selected = _require_selected_plan(plan, context, provider_sha256)
    target = _require_code(plan.get("target_environment"), "plan.target_environment")
    release = _require_release(plan.get("fusion_release"), "plan.fusion_release")
    _validate_load_receipt(_read_json(load_path, "data_load_receipt_json"), context=context, target=target, release=release)
    _validate_readback(
        _read_json(readback_path, "catalog_readback_json"),
        context=context,
        target=target,
        release=release,
        provider_sha256=provider_sha256,
    )
    _validate_duplicate_lock(
        _read_json(duplicate_path, "duplicate_lock_json"), context=context, target=target, release=release
    )
    material = {
        "schema_version": SCHEMA_VERSION,
        "status": "promotion_proposed",
        "provider": provider["provider"],
        "context_name": context,
        "target_environment": target,
        "fusion_release": release,
        "provider_contract_sha256": provider_sha256,
        "current_lifecycle": "certification-only",
        "proposed_lifecycle": "verified",
        "requires_human_review": True,
        "requires_provider_contract_change": True,
        "provider_contract_path": str(PROVIDER_CONTRACT_PATH.relative_to(SCRIPT_DIR.parents[4])),
        "evidence": {
            "data_load_receipt_sha256": _sha256_file(load_path),
            "catalog_readback_sha256": _sha256_file(readback_path),
            "duplicate_lock_sha256": _sha256_file(duplicate_path),
        },
        "selected_provider": {
            "template_id": selected["template_id"],
            "child_relation": selected["child_relation"],
            "required_fields": selected["required_fields"],
        },
        "review_instruction": "Review evidence, update the checked-in lifecycle with an evidence-backed reason, run focused tests, and obtain source-change approval. This proposal does not change provider lifecycle.",
        "created_at": _utc_now(),
    }
    result = {**material, "proposal_fingerprint": _sha256_bytes(_canonical_json(material))}
    _atomic_create(output_path, json.dumps(result, indent=2, sort_keys=True).encode("utf-8") + b"\n")
    return result


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    plan = commands.add_parser("plan", help="Create a local plan for one or all pending catalog providers.")
    plan.add_argument("--project-root", required=True)
    plan.add_argument("--target-environment", required=True)
    plan.add_argument("--fusion-release", default="unknown", help="Optional informational metadata; not an eligibility gate.")
    selection = plan.add_mutually_exclusive_group(required=True)
    selection.add_argument("--context")
    selection.add_argument("--all-pending", action="store_true")
    plan.add_argument("--output-json", required=True)

    collision = commands.add_parser("build-duplicate-lock-receipt", help="Derive a fresh collision receipt from exact REST readback.")
    collision.add_argument("--project-root", required=True)
    collision.add_argument("--input-json", required=True)
    collision.add_argument("--rest-readback-json", required=True)
    collision.add_argument("--output-json", required=True)

    duplicate = commands.add_parser("verify-duplicate-lock", help="Prove a fresh exact collision blocks package creation.")
    duplicate.add_argument("--project-root", required=True)
    duplicate.add_argument("--input-json", required=True)
    duplicate.add_argument("--current-state-receipt-json", required=True)
    duplicate.add_argument("--probe-input-json", required=True)
    duplicate.add_argument("--probe-output-zip", required=True)
    duplicate.add_argument("--probe-readiness-report", required=True)
    duplicate.add_argument("--output-json", required=True)
    duplicate.add_argument("--as-of")

    promotion = commands.add_parser("promotion-proposal", help="Create a review-only provider lifecycle promotion proposal.")
    promotion.add_argument("--project-root", required=True)
    promotion.add_argument("--context", required=True)
    promotion.add_argument("--plan-json", required=True)
    promotion.add_argument("--data-load-receipt-json", required=True)
    promotion.add_argument("--catalog-readback-json", required=True)
    promotion.add_argument("--duplicate-lock-json", required=True)
    promotion.add_argument("--output-json", required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "plan":
            result = create_plan(args)
        elif args.command == "build-duplicate-lock-receipt":
            result = build_duplicate_lock_receipt(args)
        elif args.command == "verify-duplicate-lock":
            result = verify_duplicate_lock(args)
        else:
            result = create_promotion_proposal(args)
    except CertificationAutomationError as error:
        print(json.dumps({"status": "blocked", "failure_class": "input_validation", "message": str(error)}))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
