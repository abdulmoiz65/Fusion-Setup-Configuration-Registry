#!/usr/bin/env python3
"""Verify retained new-catalog FSM lifecycle evidence locally; never submit or poll."""
from __future__ import annotations

import argparse
import copy
from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import re
import sys

import item_catalog_set_contract as binding
import prepare_profile_content_library_fsm_package as packages
from build_profile_content_library_preview import contains_sensitive
from profile_content_library_fsm_evidence import inspect_fsm_evidence, verify_item_catalog_set_readback

REPOSITORY = Path(__file__).resolve().parents[5]
REST_REGISTRY = Path(__file__).resolve().parents[1] / "content-items/references/content-item-rest-provider-registry.json"


class LifecycleError(ValueError):
    """Retained evidence is incomplete or inconsistent, not authority for a retry."""


def require(condition, message):
    if not condition:
        raise LifecycleError(message)


def timestamp(value):
    return packages.parse_rfc3339(value, "lifecycle timestamp")


def local_path(root, relative):
    require(isinstance(relative, str) and relative.strip(), "Missing project-relative evidence path")
    path = Path(relative)
    require(not path.is_absolute() and not any(p.startswith(".") for p in path.parts), "Unsafe evidence path")
    candidate = root / path
    require(not any(p.is_symlink() for p in (candidate, *candidate.parents) if p != root.parent), "Symlink evidence is not accepted")
    resolved = candidate.resolve(strict=True)
    require(root in resolved.parents and resolved.is_file(), "Evidence must be a file inside the selected project")
    require(resolved.suffix.lower() in {".json", ".zip", ".md", ".txt", ".log"}, "Unsupported evidence file type")
    require(resolved.stat().st_size <= 64 * 1024 * 1024, "Evidence file exceeds local verification limit")
    return resolved


def document(root, relative):
    path = local_path(root, relative)
    require(path.suffix == ".json", "Expected a JSON evidence document")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict) and not contains_sensitive(value), "Invalid or sensitive evidence document")
    return value


def source_file(root, reference):
    require(isinstance(reference, dict) and set(reference) == {"path", "sha256"}, "Evidence reference requires path and SHA-256")
    path = local_path(root, reference["path"])
    require(packages.sha256_file(path) == reference["sha256"], "Referenced evidence bytes changed")
    if path.suffix != ".zip":
        require(not contains_sensitive(path.read_text(encoding="utf-8")), "Sensitive source evidence is not accepted")
    return path


def core_hook():
    path = REPOSITORY / "core/data-loader/task-hook/scripts/task_hook.py"
    spec = importlib.util.spec_from_file_location("catalog_set_core_task_hook", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def same_operation(record, proposal, package_sha, set_sha):
    require(isinstance(record, dict), "Missing lifecycle operation record")
    expected = {"task_code": binding.TASK, "target_environment": proposal["target_environment"],
                "package_sha256": package_sha, "catalog_set_fingerprint": set_sha}
    require(all(record.get(k) == v for k, v in expected.items()), "Lifecycle target/task/package/set differs")
    for field in ("request_id", "process_id"):
        require(isinstance(record.get(field), str) and re.fullmatch(r"[1-9][0-9]*", record[field]), "Missing accepted request/process identifier")


def child_observations(root, paths, proposal, completed_at, as_of, evidence):
    """Join exact registered observations by provider key; never join by row order."""
    require(isinstance(paths, list), "child_evidence must be an array")
    if not paths:
        return evidence, []
    parent = proposal["rows"][binding.PARENT][0]
    children = proposal["rows"][binding.CHILD]
    require(len(paths) == len(children) and len(set(paths)) == len(paths), "Independent child evidence must cover the complete set")
    registry = json.loads(REST_REGISTRY.read_text(encoding="utf-8"))
    contexts = [c for c in registry["contexts"] if c["context_name"] == parent["ContextName"]]
    require(len(contexts) == 1, "Missing registered child context")
    context = contexts[0]
    require(context["catalog_selector"]["status"] == "registered" and context["read_certification"]["status"] != "unsupported", "Unregistered child evidence route")
    expected = {r["ContentItemCode"]: r for r in children}
    records = copy.deepcopy(dict(evidence.records_by_member)) if evidence is not None else None
    observed_rows = [dict(r) for r in records[binding.CHILD]] if records is not None else []
    verified_fields = set(registry["common_comparable_fields"])
    seen, hashes = set(), []
    for path in paths:
        item = document(root, path)
        digest = item.pop("evidence_sha256", None)
        require(digest == binding.fingerprint(item), "Child evidence fingerprint differs")
        require(item.get("status") == "complete" and item.get("coverage") == "complete"
                and item.get("provider") == "CATALOG_REST" and item.get("operation") == "read-only-exact-code-check"
                and item.get("profile_mode") == "enhanced", "Incomplete registered child evidence")
        require(item.get("target_environment") == proposal["target_environment"]
                and item.get("context_name") == parent["ContextName"]
                and item.get("child_relation") == context["child_relation"], "Child evidence target/context/relation differs")
        captured, expiry = timestamp(item.get("captured_at")), timestamp(item.get("valid_through"))
        require(completed_at <= captured <= as_of <= expiry, "Child evidence is stale or predates process completion")
        code = item.get("exact_provider_key", {}).get("ContentItemCode")
        require(item.get("exact_provider_key", {}).get("ContextName") == parent["ContextName"], "Child evidence key context differs")
        require(code in expected and code not in seen and item.get("classification") == "exact"
                and type(item.get("match_count")) is int and item["match_count"] == 1
                and len(item.get("matches", [])) == 1, "Child identity is missing, duplicate or foreign")
        catalogs = item.get("catalogs")
        require(isinstance(catalogs, list) and type(item.get("catalog_count")) is int
                and item["catalog_count"] == len(catalogs) and catalogs, "Incomplete owning-catalog coverage")
        require(all(type(c.get("match_count")) is int and c["match_count"] >= 0 for c in catalogs)
                and sum(c["match_count"] for c in catalogs) == 1, "Ambiguous owning catalog")
        owner = next(c for c in catalogs if c["match_count"] == 1)
        require(owner.get("catalog_code") == parent["ContentValueSetCode"]
                and owner.get("catalog_name") == parent["ValueSetName"]
                and owner.get("template_id") == context["catalog_selector"]["template_id"], "Child belongs to another catalog")
        template_name = context["catalog_selector"].get("template_name")
        require(template_name is None or owner.get("template_name") == template_name, "Child catalog template differs")
        identity = {k: owner.get(k) for k in ("catalog_code", "catalog_name", "template_id", "template_name")}
        require(owner.get("catalog_identity_sha256") == binding.fingerprint(identity), "Catalog identity fingerprint differs")
        actual, approved = item["matches"][0], expected[code]
        for field in ("ContentItemCode", "Name", "DateFrom", "DateTo"):
            require(field in actual, "Registered readback omits a required child field")
        for field in registry["common_comparable_fields"]:
            if field not in actual:
                verified_fields.discard(field)
                continue
            actual_value, expected_value = actual[field], approved[field]
            if field in ("DateFrom", "DateTo"):
                actual_value = str(actual_value or "").replace("/", "-")
                expected_value = expected_value.replace("/", "-")
            require((actual_value or "") == expected_value, "Registered child value differs: " + field)
        if records is not None:
            candidates = [r for r in observed_rows if (r["ContextName"], r["Name"], r["ContentValueSetCode"])
                          == (parent["ContextName"], actual["Name"], parent["ContentValueSetCode"])]
            require(len(candidates) == 1, "Full export does not contain exactly one independently observed child")
            require(candidates[0]["ContentItemCode"] in ("", actual["ContentItemCode"]), "Export and registered child code conflict")
            candidates[0]["ContentItemCode"] = actual["ContentItemCode"]
        seen.add(code)
        hashes.append(digest)
    require(seen == set(expected), "Independent child evidence is incomplete")
    if records is None:
        return {"provider": "CATALOG_REST", "observed_child_count": len(seen),
                "verified_child_fields": sorted(verified_fields),
                "verified_parent_fields": ["ContextName", "ContentValueSetCode", "ValueSetName"],
                "unverified_checks": ["parent_description_and_other_business_fields", "complete_scoped_row_counts",
                                      "rating_description_rows", "child_fields_outside_registered_REST_coverage"]}, hashes
    records[binding.CHILD] = tuple(observed_rows)
    return replace(evidence, records_by_member=records), hashes


def verify(args):
    root = Path(args.project_root).resolve(strict=True)
    require((root / "state/project-state.json").is_file(), "Existing implementation project is required")
    proposal = document(root, args.proposal)
    report = document(root, args.readiness)
    lifecycle = document(root, args.lifecycle)
    envelope = document(root, args.task_envelope)
    require(set(lifecycle) == {"schema_version", "submission", "process", "readback", "child_evidence"}
            and lifecycle["schema_version"] == "1.0", "Invalid lifecycle contract")
    archive = local_path(root, args.archive)
    package_sha = packages.sha256_file(archive)
    set_sha = binding.validate_binding(proposal)
    require(report.get("status") == "package_ready_for_core_data_loader_preview"
            and report.get("package_sha256") == package_sha
            and report.get("catalog_set_fingerprint") == set_sha
            and report.get("proposal_input_sha256") == packages.sha256_file(local_path(root, args.proposal)), "Readiness no longer binds the complete proposal/archive")
    require(report.get("catalog_set_capability") == binding.CAPABILITY
            and report.get("catalog_set_registry_sha256") == binding.registry()[1]
            and report.get("catalog_set_lifecycle") == "certification-only"
            and report.get("runtime_verified") is False, "Invalid new-set readiness lifecycle")
    submission, process = lifecycle["submission"], lifecycle["process"]
    for record in (submission, process):
        same_operation(record, proposal, package_sha, set_sha)
        source_file(root, record.get("evidence"))
    require(submission.get("route") == "core.data-loader" and submission.get("status") == "accepted", "No accepted Core submission evidence")
    require(submission.get("task_envelope_sha256") == packages.sha256_file(local_path(root, args.task_envelope)), "Submission approval envelope changed")
    require(all(process[k] == submission[k] for k in ("request_id", "process_id")), "Process IDs differ from accepted submission")
    as_of, submitted = timestamp(args.as_of), timestamp(submission.get("submitted_at"))
    checked = timestamp(process.get("captured_at"))
    require(timestamp(report["as_of"]) <= submitted <= checked <= as_of, "Lifecycle chronology is inconsistent")
    hook = core_hook()
    hook.verify_approved_data_load_archive(envelope, archive)
    task_context = local_path(root, args.task_context)
    require(submission.get("task_context_sha256") == packages.sha256_file(task_context), "Submitted task context changed")
    requirements = report["data_loader_handoff"]["task_context_requirements"]
    checked_preview = hook.build_data_load_preview({"taskContextPath": str(task_context),
        "taskName": requirements["task_name"], "sequence": args.sequence,
        "finalData": envelope["preview"].get("finalData"), "ruleResults": envelope["preview"].get("ruleResults")})
    require(checked_preview["preview"]["taskCode"] == binding.TASK
            and envelope["preview"].get("taskName") == checked_preview["preview"]["taskName"], "Persisted task context differs")
    require(timestamp(envelope["preview"].get("generatedAt")) <= timestamp(envelope["approval"].get("approvedAt")) <= submitted,
            "Core approval must precede accepted submission")
    require(envelope["preview"].get("taskCode") == binding.TASK
            and envelope["preview"].get("executionRoute") == "data-loader", "Core preview has another task or route")
    final_data = envelope["preview"].get("finalData")
    require(final_data == report["data_loader_handoff"]["task_hook_final_data"], "Core approval differs from complete package readiness")
    require(final_data.get("catalogSetFingerprint") == set_sha and final_data.get("catalogSetCapability") == binding.CAPABILITY
            and final_data.get("catalogSetRegistrySha256") == binding.registry()[1]
            and final_data.get("providerRowsFingerprint") == packages.provider_rows_fingerprint(proposal), "Core approval lacks exact new-set binding")
    contract = packages.PACKAGE_CONTRACTS[binding.TASK]
    current_path = local_path(root, args.current_state) if args.current_state else None
    baseline_path = local_path(root, args.baseline)
    current_sha = packages.sha256_file(current_path) if current_path is not None else None
    require(report["current_state_sha256"] == current_sha, "Original current-state binding differs")
    current_records = {member: () for member in contract.headers}
    if current_path is not None:
        current = inspect_fsm_evidence(current_path, task_code=binding.TASK,
            source_environment_alias=proposal["target_environment"], target_environment_alias=proposal["target_environment"],
            fusion_release="unknown", purpose="current-state", unfiltered_task_export=True)
        require(current.usable_for_duplicate_comparison, "Original current-state evidence is incomplete")
        current_records = current.records_by_member
    _, approved_rows = packages.validate_proposal(copy.deepcopy(proposal), contract=contract,
        supplied_fingerprint=proposal["proposal_fingerprint"], supplied_provider_rows_fingerprint=proposal["provider_rows_fingerprint"],
        current_sha256=current_sha, baseline_sha256=packages.sha256_file(baseline_path),
        as_of=submitted, current_records=current_records,
        candidate_new_catalog_set=True, complete_new_catalog_set=True)
    packaged, baseline = packages.inspect_archive(archive, contract), packages.inspect_archive(baseline_path, contract)
    require(packaged.raw_by_member[packages.METADATA_MEMBER] == baseline.raw_by_member[packages.METADATA_MEMBER]
            and [i.filename for i in packaged.infos] == [i.filename for i in baseline.infos], "Archive metadata/member binding differs")
    require(all(packaged.csv_by_member[m].rows == approved_rows[m] for m in approved_rows), "Archive does not contain every approved row")
    require(report["row_counts"] == {m: len(rows) for m, rows in approved_rows.items()}, "Readiness row counts differ")
    state = process.get("status")
    require(state in {"succeeded", "failed", "pending", "timeout"}, "Unrecognized process state")
    result = {"schema_version": "1.0", "status": "readback_pending", "task_code": binding.TASK,
              "target_environment": proposal["target_environment"], "catalog_set_fingerprint": set_sha,
              "package_sha256": package_sha, "request_id": submission["request_id"], "process_id": submission["process_id"],
              "process_status": state, "runtime_verified": False, "submission_authorized": False,
              "automatic_correction": False, "retry_performed": False, "evidence_basis": "retained owning-workflow evidence",
              "lifecycle_evidence_sha256": binding.fingerprint(lifecycle), "errors": []}
    if state in {"pending", "timeout"}:
        result["failure_class"] = "process_timeout" if state == "timeout" else None
        return result
    completed = timestamp(process.get("completed_at"))
    require(submitted <= completed <= checked, "Terminal completion chronology differs")
    if state == "failed":
        result.update(status="process_failed", failure_class="process_failed",
                      errors=[{"stage": "import", "message": "Terminal failure retained; partial saves may exist. Do not replay or clean up."}])
    try:
        source_file(root, process.get("process_log"))
    except (ValueError, KeyError, TypeError, OSError, AttributeError):
        if state != "failed":
            raise
        result["errors"].append({"stage": "process_log", "failure_class": "artifact_persistence",
                                 "message": "Terminal failure retained, but ProcessLog evidence is missing or invalid."})
    try:
        return compare_retained_readback(root, proposal, lifecycle, submission, package_sha, set_sha,
                                         completed, as_of, archive, current_path, baseline_path, result)
    except (ValueError, KeyError, TypeError, OSError, AttributeError):
        if state != "failed":
            raise
        result["errors"].append({"stage": "readback", "failure_class": "input_validation",
                                 "message": "Terminal failure retained; incomplete or invalid partial readback cannot prove saved rows."})
        return result


def compare_retained_readback(root, proposal, lifecycle, submission, package_sha, set_sha,
                              completed, as_of, archive, current_path, baseline_path, result):
    """Compare terminal evidence without converting an import failure into success."""
    state = result["process_status"]
    readback = lifecycle.get("readback")
    if readback is None:
        if state == "failed":
            return result
        return compare_rest_fallback(root, proposal, lifecycle, completed, as_of, result, "not_provided")
    same_operation(readback, proposal, package_sha, set_sha)
    require(all(readback[k] == submission[k] for k in ("request_id", "process_id")), "Readback process binding differs")
    if readback.get("status") in {"failed", "skipped"}:
        require(readback.get("origin") == "fsm-export", "Unexpected optional export origin")
        if readback["status"] == "failed":
            source_file(root, readback.get("evidence"))
        return compare_rest_fallback(root, proposal, lifecycle, completed, as_of, result, readback["status"])
    require(readback.get("origin") == "fsm-export" and readback.get("unfiltered_task_export") is True,
            "Readback must be a complete unfiltered FSM export")
    require(completed <= timestamp(readback.get("captured_at")) <= as_of <= timestamp(readback.get("valid_through")), "Readback is stale or predates completion")
    readback_path = source_file(root, readback.get("evidence"))
    require(readback_path not in {archive, current_path, baseline_path}, "Readback must be independently obtained after import")
    observed = inspect_fsm_evidence(readback_path, task_code=binding.TASK,
        source_environment_alias=proposal["target_environment"], target_environment_alias=proposal["target_environment"],
        fusion_release="unknown", purpose="readback", unfiltered_task_export=True)
    enriched, child_hashes = child_observations(root, lifecycle["child_evidence"], proposal, completed, as_of, observed)
    # Archive comparison uses provider serialization; business readback expects
    # the original ISO-date proposal and normalizes observed export dates itself.
    comparison = verify_item_catalog_set_readback(enriched, proposal["rows"])
    result.update(readback=comparison, readback_sha256=observed.archive_sha256, child_evidence_sha256=child_hashes)
    if state == "succeeded":
        result.update(status="verified" if comparison["status"] == "verified" else "readback_mismatch",
                      runtime_verified=comparison["status"] == "verified")
    return result


def compare_rest_fallback(root, proposal, lifecycle, completed, as_of, result, export_status):
    """Use registered observations without pretending they cover a full export."""
    result["post_import_export"] = export_status
    result["errors"].append({"stage": "export", "message": "Post-import export unavailable; use registered read-only verification."})
    if result["process_status"] == "succeeded":
        result["status"] = "verification_incomplete"
    result["next_action"] = (
        "Use the Content Items registered talent_content_item_catalog_adapter.py check route for each exact child code; "
        "retain complete same-target post-completion observations. Report unsupported fields; do not resubmit the import."
    )
    if not lifecycle["child_evidence"]:
        return result
    try:
        comparison, hashes = child_observations(root, lifecycle["child_evidence"], proposal, completed, as_of, None)
    except (ValueError, KeyError, TypeError, OSError, AttributeError) as error:
        result["errors"].append({"stage": "rest_readback", "failure_class": "input_validation",
                                 "message": str(error) if isinstance(error, LifecycleError) else "REST readback evidence is invalid or unavailable."})
        return result
    result.update(readback=comparison, child_evidence_sha256=hashes)
    if result["process_status"] == "succeeded":
        result["status"] = "partially_verified"
    result["next_action"] = "Report verified REST fields and remaining coverage gaps; use a supported read for remaining fields if available. Do not resubmit."
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("project-root", "proposal", "readiness", "archive", "baseline", "task-envelope", "task-context", "lifecycle", "as-of"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--current-state", help="Omit when the approved package records a skipped/failed pre-import export")
    parser.add_argument("--sequence", required=True, type=int)
    args = parser.parse_args(argv)
    try:
        result = verify(args)
    except (ValueError, KeyError, TypeError, OSError, AttributeError) as error:
        # Do not print raw untrusted fields, file contents or exception paths.
        result = {"status": "blocked", "failure_class": "input_validation", "runtime_verified": False,
                  "message": str(error) if isinstance(error, LifecycleError) else "Lifecycle evidence validation failed",
                  "error_type": type(error).__name__,
                  "submission_authorized": False, "retry_performed": False}
    print(json.dumps(result, indent=2, sort_keys=True))
    return {"verified": 0, "readback_pending": 3, "process_failed": 4}.get(result["status"], 2)


if __name__ == "__main__":
    raise SystemExit(main())
