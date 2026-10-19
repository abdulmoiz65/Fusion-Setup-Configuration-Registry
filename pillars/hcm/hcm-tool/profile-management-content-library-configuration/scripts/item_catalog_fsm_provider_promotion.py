#!/usr/bin/env python3
"""Validate Item Catalog FSM canary evidence and bind a lifecycle promotion.

This helper is deliberately local-only. It reads project evidence, produces a
review-only promotion proposal, and can verify that a later checked-in provider
registry matches that proposal. It never authenticates, calls Fusion, edits a
registry, uploads a package, or starts a Data Loader request.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REGISTRY = (
    SCRIPT_DIR.parent
    / "item-catalogs"
    / "references"
    / "catalog-content-item-fsm-provider.json"
)
TASK_CODE = "ORA_MANAGE_PROFILE_ITEM_CATALOG"
EXPECTED_CONTEXTS = (
    "BEHAVIOR",
    "CERTIFICATION",
    "COMPETENCY",
    "DEGREE",
    "EDUCATION_LEVEL",
    "HONOR",
    "LANGUAGE",
    "MEMBERSHIP",
    "PROJECT",
)
PROMOTION_EVIDENCE_SUMMARY = (
    "All nine registered contexts passed a controlled 26C non-production FSM "
    "create, successful Data Loader and ProcessLog checks, exact child and full "
    "Item Catalog export readback, parent no-drift comparison, and duplicate-create "
    "lock; immutable evidence paths and hashes remain in the project promotion record."
)
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")


class PromotionError(ValueError):
    """The provider-promotion evidence contract was not satisfied."""


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise PromotionError(f"{label} could not be read: {path}") from error
    except json.JSONDecodeError as error:
        raise PromotionError(f"{label} is not valid JSON: {error.msg}") from error
    if not isinstance(value, dict):
        raise PromotionError(f"{label} must contain a JSON object")
    return value


def _require_exact_keys(value: Any, expected: set[str], label: str) -> Mapping[str, Any]:
    if not isinstance(value, dict) or set(value) != expected:
        raise PromotionError(f"{label} has an invalid field contract")
    return value


def _require_sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SHA256_PATTERN.fullmatch(value):
        raise PromotionError(f"{label} must be a lowercase SHA-256 value")
    return value


def _project_file(project_root: Path, supplied: Any, label: str) -> Path:
    if not isinstance(supplied, str) or not supplied:
        raise PromotionError(f"{label} must be a non-empty project-relative path")
    candidate = Path(supplied)
    if candidate.is_absolute():
        raise PromotionError(f"{label} must be relative to project_root")
    root = project_root.resolve(strict=True)
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise PromotionError(f"{label} resolves outside project_root") from error
    if not resolved.is_file():
        raise PromotionError(f"{label} does not identify an existing file")
    return resolved


def _bound_json(
    project_root: Path, reference: Mapping[str, Any], label: str
) -> tuple[dict[str, Any], Path]:
    _require_exact_keys(reference, {"path", "sha256"}, label)
    path = _project_file(project_root, reference["path"], f"{label}.path")
    expected_sha = _require_sha256(reference["sha256"], f"{label}.sha256")
    if _sha256_file(path) != expected_sha:
        raise PromotionError(f"{label} SHA-256 does not match the referenced file")
    return _read_json(path, label), path


def _require_counts(value: Any, label: str) -> None:
    expected = {"total": 3, "loaded": 3, "failed": 0}
    if not isinstance(value, dict) or any(
        value.get(key) != count for key, count in expected.items()
    ):
        raise PromotionError(f"{label} must prove the FSM object counts 3/3/0")


def _require_nonempty_export_counts(value: Any, label: str) -> None:
    if not isinstance(value, dict) or len(value) != 3:
        raise PromotionError(f"{label} must contain all three Item Catalog members")
    if any(
        isinstance(count, bool) or not isinstance(count, int) or count < 1
        for count in value.values()
    ):
        raise PromotionError(f"{label} must prove a populated full Item Catalog export")


def _validate_request_receipt(
    receipt: Mapping[str, Any], expected: Mapping[str, str]
) -> None:
    if (
        receipt.get("schemaVersion") != "1.0"
        or receipt.get("status") != "verified"
        or receipt.get("environment") != expected["target_environment"]
        or receipt.get("taskCode") != TASK_CODE
    ):
        raise PromotionError(
            f"{expected['context_name']} request receipt identity is invalid"
        )
    load = receipt.get("dataLoad")
    if not isinstance(load, dict) or (
        load.get("requestId") != expected["data_loader_request_id"]
        or load.get("sourceType") != "FSM"
        or load.get("terminalStatus") != "Succeeded"
        or load.get("diagnosticCount") != 0
        or load.get("dataSetErrorsQueried") is not True
    ):
        raise PromotionError(
            f"{expected['context_name']} Data Loader result is invalid"
        )
    _require_counts(
        load.get("objectCounts"), f"{expected['context_name']} objectCounts"
    )
    log = load.get("processLog")
    if not isinstance(log, dict) or any(
        log.get(key) != value
        for key, value in {
            "downloaded": True,
            "totalObjectsProcessed": 3,
            "totalObjectsSucceeded": 3,
            "totalObjectsFailed": 0,
            "totalObjectsWithWarnings": 0,
        }.items()
    ):
        raise PromotionError(
            f"{expected['context_name']} ProcessLog result is invalid"
        )
    child = receipt.get("childVerification")
    if not isinstance(child, dict) or any(
        child.get(key) != value
        for key, value in {
            "contextName": expected["context_name"],
            "contentValueSetCode": expected["parent_catalog_code"],
            "contentItemCode": expected["content_item_code"],
            "exactProviderKeyMatches": 1,
            "differingPortableFields": [],
            "verification": "verified-with-parent-no-drift",
        }.items()
    ):
        raise PromotionError(
            f"{expected['context_name']} child readback is invalid"
        )
    parent = receipt.get("parentVerification")
    if not isinstance(parent, dict) or any(
        parent.get(key) != value
        for key, value in {
            "contextName": expected["context_name"],
            "contentValueSetCode": expected["parent_catalog_code"],
            "exactMatches": 1,
            "differingPortableFields": [],
        }.items()
    ):
        raise PromotionError(
            f"{expected['context_name']} parent no-drift result is invalid"
        )
    export = receipt.get("freshReadback")
    if (
        not isinstance(export, dict)
        or export.get("complete") is not True
        or export.get("retrieved") != "FileContent"
    ):
        raise PromotionError(
            f"{expected['context_name']} full export result is invalid"
        )
    _require_sha256(
        export.get("archiveSha256"),
        f"{expected['context_name']} export SHA-256",
    )
    _require_nonempty_export_counts(
        export.get("rowCounts"), f"{expected['context_name']} export counts"
    )
    guard = receipt.get("repeatCreateGuard")
    if not isinstance(guard, dict) or any(
        guard.get(key) != value
        for key, value in {
            "classification": "exact",
            "matchCount": 1,
            "parentMatchCount": 1,
            "differingPortableFields": [],
            "wouldCreateAgain": False,
        }.items()
    ):
        raise PromotionError(
            f"{expected['context_name']} duplicate-create lock is invalid"
        )
    side_effects = receipt.get("sideEffectsDuringVerification")
    if not isinstance(side_effects, dict) or any(
        side_effects.get(key) != value
        for key, value in {
            "uploadPerformed": False,
            "dataLoadInitiated": False,
            "retryPerformed": False,
            "rollbackPerformed": False,
            "providerPromoted": False,
            "commonCodeOrConfigurationChanged": False,
        }.items()
    ):
        raise PromotionError(
            f"{expected['context_name']} verification side-effect boundary is invalid"
        )


def _validate_modern_verification_receipt(
    receipt: Mapping[str, Any], expected: Mapping[str, str]
) -> None:
    if any(
        receipt.get(key) != value
        for key, value in {
            "schema_version": "1.0",
            "status": "verified",
            "verification_route": (
                "hcm.hcm-tool.profile-management-content-library-configuration."
                "item-catalogs"
            ),
            "target_environment": expected["target_environment"],
            "fusion_release": expected["fusion_release"],
            "task_code": TASK_CODE,
            "context_name": expected["context_name"],
        }.items()
    ):
        raise PromotionError(
            f"{expected['context_name']} verification receipt identity is invalid"
        )
    for key in (
        "authorization_fingerprint",
        "execution_fingerprint",
        "source_sha256",
    ):
        _require_sha256(receipt.get(key), f"{expected['context_name']} {key}")
    if receipt.get("checks") != {
        "direct_child_readback": "passed",
        "parent_no_drift": "passed",
        "full_item_catalog_export": "passed",
        "duplicate_rerun_block": "passed",
    }:
        raise PromotionError(
            f"{expected['context_name']} verification checks are incomplete"
        )


def _validate_domain_details(
    receipt: Mapping[str, Any], expected: Mapping[str, str]
) -> None:
    if any(
        receipt.get(key) != value
        for key, value in {
            "schema_version": "1.0",
            "status": "verified",
            "target_environment": expected["target_environment"],
            "task_code": TASK_CODE,
            "context_name": expected["context_name"],
            "content_item_code": expected["content_item_code"],
            "parent_catalog_code": expected["parent_catalog_code"],
            "data_loader_request_id": expected["data_loader_request_id"],
            "data_loader_status": "Succeeded",
            "mutation_retry_performed": False,
            "rollback_performed": False,
            "provider_promotion_performed": False,
        }.items()
    ):
        raise PromotionError(
            f"{expected['context_name']} domain verification identity is invalid"
        )
    _require_counts(
        receipt.get("data_loader_counts"),
        f"{expected['context_name']} data_loader_counts",
    )
    if receipt.get("data_set_errors") != {
        "queried": True,
        "diagnostic_count": 0,
    }:
        raise PromotionError(
            f"{expected['context_name']} Data Loader diagnostics are invalid"
        )
    log = receipt.get("process_log")
    if not isinstance(log, dict) or any(
        log.get(key) != value
        for key, value in {
            "total_objects_processed": 3,
            "total_objects_succeeded": 3,
            "total_objects_failed": 0,
            "total_objects_with_warnings": 0,
        }.items()
    ):
        raise PromotionError(
            f"{expected['context_name']} ProcessLog result is invalid"
        )
    for field in ("child_readback", "parent_no_drift"):
        check = receipt.get(field)
        if (
            not isinstance(check, dict)
            or check.get("status") != "verified"
            or check.get("match_count") != 1
            or check.get("differing_fields") != []
        ):
            raise PromotionError(
                f"{expected['context_name']} {field} result is invalid"
            )
    export = receipt.get("fresh_export")
    if not isinstance(export, dict):
        raise PromotionError(
            f"{expected['context_name']} full export result is missing"
        )
    _require_sha256(
        export.get("archive_sha256"),
        f"{expected['context_name']} export SHA-256",
    )
    _require_nonempty_export_counts(
        export.get("row_counts"), f"{expected['context_name']} export counts"
    )
    guard = receipt.get("repeat_create_guard")
    if not isinstance(guard, dict) or any(
        guard.get(key) != value
        for key, value in {
            "status": "ready",
            "classification": "exact",
            "match_count": 1,
            "parent_match_count": 1,
            "differing_fields": [],
        }.items()
    ):
        raise PromotionError(
            f"{expected['context_name']} duplicate-create lock is invalid"
        )


def _validate_test_batch_domain(
    project_root: Path, receipt: Mapping[str, Any], expected: Mapping[str, str]
) -> None:
    if any(
        receipt.get(key) != value
        for key, value in {
            "schema_version": "1.0",
            "status": "verified",
            "target_environment": expected["target_environment"],
            "fusion_release": expected["fusion_release"],
            "task_code": TASK_CODE,
            "context_name": expected["context_name"],
            "data_loader_request_id": expected["data_loader_request_id"],
        }.items()
    ):
        raise PromotionError(
            f"{expected['context_name']} test-batch verification identity is invalid"
        )
    _require_counts(
        receipt.get("data_loader_reported_counts"),
        f"{expected['context_name']} data_loader_reported_counts",
    )
    if receipt.get("data_loader_dataset_status") != "succeeded":
        raise PromotionError(
            f"{expected['context_name']} Data Loader status is invalid"
        )
    child_reference = receipt.get("direct_child_readback")
    if not isinstance(child_reference, dict):
        raise PromotionError(
            f"{expected['context_name']} direct child readback is missing"
        )
    child_path = _project_file(
        project_root, child_reference.get("path"), "direct_child_readback.path"
    )
    if _sha256_file(child_path) != _require_sha256(
        child_reference.get("sha256"), "direct_child_readback.sha256"
    ):
        raise PromotionError(
            f"{expected['context_name']} direct child readback SHA-256 is invalid"
        )
    child = _read_json(child_path, "direct_child_readback")
    key = child.get("exact_provider_key")
    if (
        not isinstance(key, dict)
        or any(
            key.get(field) != value
            for field, value in {
                "ContextName": expected["context_name"],
                "ContentItemCode": expected["content_item_code"],
            }.items()
        )
        or child.get("target_environment") != expected["target_environment"]
        or child.get("fusion_release") != expected["fusion_release"]
    ):
        raise PromotionError(
            f"{expected['context_name']} direct child identity is invalid"
        )
    export = receipt.get("full_item_catalog_export")
    if not isinstance(export, dict) or export.get("complete") is not True:
        raise PromotionError(
            f"{expected['context_name']} full export result is invalid"
        )
    _require_sha256(
        export.get("sha256"), f"{expected['context_name']} export SHA-256"
    )
    _require_nonempty_export_counts(
        export.get("row_counts"), f"{expected['context_name']} export counts"
    )
    readback = receipt.get("export_readback")
    parent = readback.get("parent_readback") if isinstance(readback, dict) else None
    if (
        not isinstance(readback, dict)
        or readback.get("status") != "verified"
        or readback.get("differing_fields") != []
        or not isinstance(parent, dict)
        or parent.get("status") != "verified"
        or parent.get("differing_fields") != []
    ):
        raise PromotionError(
            f"{expected['context_name']} export or parent readback is invalid"
        )
    guard = receipt.get("duplicate_rerun_lock")
    if not isinstance(guard, dict) or any(
        guard.get(key) != value
        for key, value in {
            "status": "passed",
            "classification": "exact",
            "match_count": 1,
            "parent_match_count": 1,
            "differing_fields": [],
        }.items()
    ):
        raise PromotionError(
            f"{expected['context_name']} duplicate-create lock is invalid"
        )


def _validate_registry(registry: Mapping[str, Any], lifecycle: str) -> None:
    if set(registry) - {"source_product_releases"} != {
        "schema_version",
        "task_code",
        "task_name",
        "fusion_release",
        "provider",
        "parent_catalog_strategy",
        "supported_child_scope",
        "providers",
        "source_evidence",
    }:
        raise PromotionError(
            "the Item Catalog FSM provider registry schema is invalid"
        )
    if "source_product_releases" in registry and registry["source_product_releases"] != ["11.13.26.10.0"]:
        raise PromotionError("the separately documented product-release contract has changed")
    if (
        registry.get("schema_version") != "1.0"
        or registry.get("task_code") != TASK_CODE
        or registry.get("task_name") != "Item Catalogs"
        or registry.get("fusion_release") != "26C"
        or registry.get("provider")
        != (
            "oracle.apps.hcm.profiles.contentLibrary.itemCatalogMigrationService."
            "ItemCatalogMigrationService"
        )
        or registry.get("parent_catalog_strategy") != "existing-catalog-anchor"
    ):
        raise PromotionError(
            "the Item Catalog FSM provider registry identity is invalid"
        )
    scope = registry.get("supported_child_scope")
    if scope != {
        "content_item": "one create-only row per package",
        "rating_description": "blocked",
        "translations": "blocked",
        "relationships": "blocked",
        "dynamic_fields": "blocked",
        "updates_deletes_end_dates": "blocked",
    }:
        raise PromotionError("the Item Catalog FSM supported scope has changed")
    providers = registry.get("providers")
    if not isinstance(providers, list) or len(providers) != len(EXPECTED_CONTEXTS):
        raise PromotionError("the Item Catalog FSM provider context set is invalid")
    context_names = [
        item.get("context_name") for item in providers if isinstance(item, dict)
    ]
    if (
        len(context_names) != len(EXPECTED_CONTEXTS)
        or any(not isinstance(name, str) for name in context_names)
        or tuple(sorted(context_names)) != EXPECTED_CONTEXTS
    ):
        raise PromotionError("the Item Catalog FSM provider context set is invalid")
    for provider in providers:
        if (
            set(provider)
            != {"context_name", "lifecycle", "allowed_supplier_codes"}
            or provider.get("lifecycle") != lifecycle
            or provider.get("allowed_supplier_codes") != ["C"]
        ):
            raise PromotionError(
                "the Item Catalog FSM provider lifecycle or supplier scope is invalid"
            )


def _validate_index(
    project_root: Path, index: Mapping[str, Any], registry_path: Path
) -> list[dict[str, str]]:
    _require_exact_keys(
        index,
        {
            "schema_version",
            "status",
            "target_environment",
            "fusion_release",
            "task_code",
            "provider_contract_sha256",
            "final_decision",
            "contexts",
        },
        "evidence index",
    )
    if (
        index.get("schema_version") != "1.0"
        or index.get("status") != "promotion-evidence-complete"
        or index.get("fusion_release") != "26C"
        or index.get("task_code") != TASK_CODE
    ):
        raise PromotionError("the evidence index identity is invalid")
    target = index.get("target_environment")
    if not isinstance(target, str) or not target:
        raise PromotionError("target_environment must be non-empty")
    if _sha256_file(registry_path) != _require_sha256(
        index.get("provider_contract_sha256"), "provider_contract_sha256"
    ):
        raise PromotionError(
            "the evidence index is not bound to the current provider registry"
        )
    decision, _ = _bound_json(
        project_root, index.get("final_decision"), "final_decision"
    )
    if (
        decision.get("status") != "complete"
        or decision.get("target_environment") != target
        or decision.get("fusion_release") != "26C"
        or decision.get("task_code") != TASK_CODE
    ):
        raise PromotionError("the final decision identity is invalid")
    proofs = decision.get("fsm_proofs")
    if not isinstance(proofs, list) or len(proofs) != len(EXPECTED_CONTEXTS):
        raise PromotionError("the final decision has no FSM proofs")
    proof_names = [
        item.get("context_name") for item in proofs if isinstance(item, dict)
    ]
    if (
        len(proof_names) != len(EXPECTED_CONTEXTS)
        or any(not isinstance(name, str) for name in proof_names)
        or tuple(sorted(proof_names)) != EXPECTED_CONTEXTS
    ):
        raise PromotionError("the final decision FSM proof set is invalid")
    proof_by_context = {
        item.get("context_name"): item for item in proofs if isinstance(item, dict)
    }
    entries = index.get("contexts")
    if (
        not isinstance(entries, list)
        or tuple(
            sorted(
                item.get("context_name")
                for item in entries
                if isinstance(item, dict)
            )
        )
        != EXPECTED_CONTEXTS
    ):
        raise PromotionError(
            "the evidence index must contain each registered context exactly once"
        )
    normalized: list[dict[str, str]] = []
    for position, entry in enumerate(entries, start=1):
        _require_exact_keys(
            entry,
            {
                "context_name",
                "parent_catalog_code",
                "content_item_code",
                "data_loader_request_id",
                "evidence_format",
                "evidence",
                "verification_receipt",
            },
            f"contexts[{position}]",
        )
        expected = {
            "context_name": entry["context_name"],
            "parent_catalog_code": entry["parent_catalog_code"],
            "content_item_code": entry["content_item_code"],
            "data_loader_request_id": entry["data_loader_request_id"],
            "target_environment": target,
            "fusion_release": "26C",
        }
        if any(
            not isinstance(expected[key], str) or not expected[key]
            for key in (
                "context_name",
                "parent_catalog_code",
                "content_item_code",
                "data_loader_request_id",
            )
        ):
            raise PromotionError(f"contexts[{position}] contains an empty identity")
        proof = proof_by_context.get(expected["context_name"])
        if not isinstance(proof, dict) or any(
            proof.get(key) != value
            for key, value in {
                "parent_catalog_code": expected["parent_catalog_code"],
                "proof_content_item_code": expected["content_item_code"],
                "data_loader_request_id": expected["data_loader_request_id"],
            }.items()
        ):
            raise PromotionError(
                f"{expected['context_name']} does not match the final decision proof"
            )
        evidence, _ = _bound_json(
            project_root,
            entry["evidence"],
            f"{expected['context_name']} evidence",
        )
        evidence_format = entry.get("evidence_format")
        if evidence_format == "request-verification-v1":
            if entry.get("verification_receipt") is not None:
                raise PromotionError(
                    f"{expected['context_name']} has an unexpected secondary receipt"
                )
            _validate_request_receipt(evidence, expected)
        elif evidence_format == "domain-details-v1":
            _validate_domain_details(evidence, expected)
            secondary, _ = _bound_json(
                project_root,
                entry.get("verification_receipt"),
                f"{expected['context_name']} verification_receipt",
            )
            _validate_modern_verification_receipt(secondary, expected)
        elif evidence_format == "test-batch-domain-v1":
            if entry.get("verification_receipt") is not None:
                raise PromotionError(
                    f"{expected['context_name']} has an unexpected secondary receipt"
                )
            _validate_test_batch_domain(project_root, evidence, expected)
        else:
            raise PromotionError(
                f"{expected['context_name']} evidence_format is unsupported"
            )
        normalized.append(
            {
                **expected,
                "evidence_format": evidence_format,
                "evidence_sha256": entry["evidence"]["sha256"],
                "verification_receipt_sha256": (
                    entry["verification_receipt"]["sha256"]
                    if isinstance(entry.get("verification_receipt"), dict)
                    else "not-applicable"
                ),
            }
        )
    return sorted(normalized, key=lambda value: value["context_name"])


def propose(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root)
    registry_path = Path(args.registry).resolve(strict=True)
    registry = _read_json(registry_path, "provider registry")
    _validate_registry(registry, "certification-only")
    index_path = _project_file(
        project_root, args.evidence_index, "evidence_index"
    )
    index = _read_json(index_path, "evidence_index")
    contexts = _validate_index(project_root, index, registry_path)
    proposed_registry = copy.deepcopy(registry)
    for provider in proposed_registry["providers"]:
        provider["lifecycle"] = "verified"
    if PROMOTION_EVIDENCE_SUMMARY not in proposed_registry["source_evidence"]:
        proposed_registry["source_evidence"].append(PROMOTION_EVIDENCE_SUMMARY)
    material = {
        "schema_version": "1.0",
        "status": "ready-for-reviewed-source-change",
        "task_code": TASK_CODE,
        "fusion_release": "26C",
        "target_environment": index["target_environment"],
        "provider_contract_sha256": _sha256_file(registry_path),
        "evidence_index_sha256": _sha256_file(index_path),
        "evidence_fingerprint": _sha256_bytes(_canonical_json(contexts)),
        "proposed_provider_contract_fingerprint": _sha256_bytes(
            _canonical_json(proposed_registry)
        ),
        "promotion_evidence_summary": PROMOTION_EVIDENCE_SUMMARY,
        "contexts": contexts,
        "preserved_boundary": {
            "operation": "create-only",
            "package_cardinality": "one exact existing parent and one new child",
            "supplier_codes": ["C"],
            "rating_model_code": "blank",
            "rating_descriptions": "zero rows",
            "translations_relationships_dynamic_generated_fields": "blocked",
            "updates_deletes_end_dates_multi_child_multi_context": "blocked",
            "fresh_target_specific_evidence_per_future_row": True,
            "core_data_loader_approval_per_future_package": True,
        },
        "required_reviewers_before_merge": [
            "HCM Pillar Development Lead or delegated Profile Management SME",
            "FSCR A-Team/core reviewer",
            "QA reviewer",
        ],
    }
    result = {
        **material,
        "proposal_fingerprint": _sha256_bytes(_canonical_json(material)),
    }
    output_path = project_root.resolve(strict=True) / args.output_json
    try:
        output_path.resolve().relative_to(project_root.resolve())
    except ValueError as error:
        raise PromotionError("output_json resolves outside project_root") from error
    if output_path.exists():
        raise PromotionError("output_json already exists; refusing to overwrite")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("xb") as destination:
        destination.write(
            json.dumps(result, indent=2, sort_keys=True).encode("utf-8") + b"\n"
        )
    return result


def verify_applied(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root)
    proposal_path = _project_file(
        project_root, args.proposal_json, "proposal_json"
    )
    proposal = _read_json(proposal_path, "proposal_json")
    if (
        proposal.get("status") != "ready-for-reviewed-source-change"
        or proposal.get("task_code") != TASK_CODE
    ):
        raise PromotionError("the promotion proposal identity is invalid")
    material = dict(proposal)
    supplied_fingerprint = material.pop("proposal_fingerprint", None)
    if supplied_fingerprint != _sha256_bytes(_canonical_json(material)):
        raise PromotionError("the promotion proposal fingerprint is invalid")
    registry_path = Path(args.registry).resolve(strict=True)
    registry = _read_json(registry_path, "provider registry")
    _validate_registry(registry, "verified")
    if PROMOTION_EVIDENCE_SUMMARY not in registry.get("source_evidence", []):
        raise PromotionError(
            "the provider registry is missing the promotion evidence summary"
        )
    actual = _sha256_bytes(_canonical_json(registry))
    if actual != proposal.get("proposed_provider_contract_fingerprint"):
        raise PromotionError(
            "the applied provider registry differs from the reviewed proposal"
        )
    return {
        "schema_version": "1.0",
        "status": "promotion-applied-and-bound",
        "task_code": TASK_CODE,
        "fusion_release": "26C",
        "provider_contract_sha256": _sha256_file(registry_path),
        "proposal_fingerprint": proposal.get("proposal_fingerprint"),
        "verified_contexts": list(EXPECTED_CONTEXTS),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate and bind the local Item Catalog FSM provider lifecycle "
            "promotion."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    propose_parser = subparsers.add_parser(
        "propose",
        help="Validate evidence and write a review-only promotion proposal.",
    )
    propose_parser.add_argument("--project-root", required=True)
    propose_parser.add_argument("--evidence-index", required=True)
    propose_parser.add_argument("--output-json", required=True)
    propose_parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    propose_parser.set_defaults(handler=propose)
    verify_parser = subparsers.add_parser(
        "verify-applied",
        help="Verify the checked-in registry matches the bound proposal.",
    )
    verify_parser.add_argument("--project-root", required=True)
    verify_parser.add_argument("--proposal-json", required=True)
    verify_parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    verify_parser.set_defaults(handler=verify_applied)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = args.handler(args)
    except PromotionError as error:
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "failure_class": "input_validation",
                    "message": str(error),
                },
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
