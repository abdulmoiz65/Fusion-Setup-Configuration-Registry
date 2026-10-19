"""Continue an exact approved, frozen CAP PATCH through shared Data Loader.

Python 3.11+. This module neither obtains consent nor performs live revalidation.
The approval arguments represent the user's later approval of this exact retained
preview, not approval of a plan, retrieval, create, or a different artifact.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import sys

import cap_create_handoff as common
from cap_create_submission import _safe_external_id, _save_exclusive
import cap_update_validation as validation


class SubmissionBlocked(ValueError):
    """Stop without selecting a direct REST or other alternate write route."""


def _require(condition, message):
    if not condition:
        raise SubmissionBlocked(message)


def attempt_key(final_data):
    """A reissued preview cannot replay the same target, ZIP and operation."""
    return common._digest({"environment": final_data["environment"],
                           "archiveSha256": final_data["archiveSha256"],
                           "operation": "update"})


def _frozen_preview(preview_path, project, approved_digest, loader):
    path = Path(preview_path).resolve(strict=True)
    _require(common._inside(path, project), "Preview must belong to the selected project")
    retained = common._json(path)
    preview = retained.get("preview")
    _require(isinstance(preview, dict) and re.fullmatch(r"[0-9a-f]{64}", approved_digest or "")
             and common._digest(preview) == retained.get("previewSha256") == approved_digest,
             "Explicit approval must match the exact retained CAP update preview digest")
    _require(preview.get("taskCode") == common.cap_workflow.CODE
             and preview.get("taskName") == common.cap_workflow.TASK
             and preview.get("executionRoute") == "data-loader",
             "Only the canonical CAP Data Loader task can be submitted")
    final = preview.get("finalData", {})
    evidence = final.get("updateEvidence", {})
    prepared = retained.get("prepared", {})
    binding = prepared.get("binding", {})
    _require(final.get("validationPurpose") == "update_preparation_only"
             and final.get("writeEligible") is False
             and final.get("operation") == evidence.get("operation") == "update"
             and evidence.get("businessObject") == "learningCatalogProfiles"
             and evidence.get("restContext") == "ORA_HCM_REST",
             "Retrieval, create readiness or another operation cannot authorize an update")
    expected = {key: final.get(key) for key in (
        "operation", "archiveSha256", "environment", "runbook", "profileNumber", "inputs",
        "baseline", "sourceFingerprint", "evidenceSha256", "conflictModel")}
    baseline = evidence.get("baseline", {})
    _require(binding == expected and common._digest(binding) == prepared.get("bindingSha256")
             == final.get("bindingSha256")
             and prepared.get("validation_purpose") == "update_preparation_only"
             and prepared.get("write_eligible") is False
             and final.get("inputs") == evidence.get("intendedFields")
             and final.get("baseline") == baseline
             and final.get("profileNumber") == baseline.get("learningCatalogProfileNumber")
             and final.get("conflictModel") == "sparse_last_writer_wins"
             and final.get("environment") == evidence.get("environment")
             and final.get("runbook") == evidence.get("runbook")
             and final.get("sourceFingerprint") == evidence.get("sourceFingerprint")
             and final.get("evidenceSha256") == common._digest(evidence),
             "Frozen update identity, baseline, diff, conflict model, evidence or target changed")
    results = preview.get("ruleResults", [])
    _require(isinstance(results, list) and results
             and all(isinstance(row, dict) and row.get("status") in {"passed", "not_applicable"}
                     for row in results) and any(row["status"] == "passed" for row in results),
             "CAP update requires successful preparation without rule overrides")
    # Integrity only. The evidence digest binds the verified key/effective
    # mapping. Never reread original DAT/evidence/context, reevaluate expiration
    # or rules, refresh a baseline, rebuild the ZIP or substitute a new date.
    preflight_path = Path(retained.get("sharedPreflightPath", "")).resolve(strict=True)
    archive = Path(retained.get("archivePath", "")).resolve(strict=True)
    _require(common._inside(preflight_path, path.parent) and common._inside(archive, path.parent)
             and preflight_path != archive
             and common._file_digest(preflight_path) == final.get("sharedPreflightSha256")
             and common._file_digest(archive) == final.get("archiveSha256"),
             "Retained shared preflight or immutable update ZIP changed")
    # JSON hashes alone cannot establish that the presented diff describes the
    # ZIP's business row. Compare the retained bytes to their frozen evidence;
    # this is pure artifact integrity, not fresh evidence/rule/time validation.
    try:
        archive_summary = validation.validate_archive(archive.read_bytes(), evidence)
    except ValueError as exc:
        raise SubmissionBlocked("Frozen update ZIP does not match its approved fields, identity or mapping") from exc
    _require(archive_summary["archiveSha256"] == final["archiveSha256"],
             "Immutable update ZIP changed during frozen integrity verification")
    preflight = loader.load_preflight_envelope(preflight_path)
    _require(preflight.get("taskRouted") is True and preflight.get("mappingComplete") is True
             and preflight.get("sourceType") is None
             and Path(preflight.get("approvedArtifactPath", "")).resolve() == archive
             and preflight.get("archiveSha256") == final["archiveSha256"]
             and preflight.get("host") == final["environment"]["host"]
             and preflight.get("environment") == final["environment"]["name"]
             and preflight.get("runID") == final["runbook"]["runID"],
             "Shared preflight differs from the approved CAP update route or context")
    _, _, current_binding = common._project_context(project, evidence, loader)
    _require(current_binding == final.get("projectBinding"), "Project Run Book binding changed")
    return retained, final, archive, preflight_path


def submit_update(*, preview_path, project_root, approved_preview_sha256,
                  approve_upload=False):
    """Make one genuine approved attempt through shared services, never retry.

    Returns initiation only. Loader completion, business readback and CAP
    processing require their separately selected shared read workflows.
    """
    _require(approve_upload is True, "Explicit exact-load approval is required before submission")
    project = Path(project_root).resolve(strict=True)
    _require(common._inside(project, common.REPO / "project"), "Invalid project workspace")
    loader, hook = common.shared_loader(), common.shared_hook()
    retained, final, archive, preflight_path = _frozen_preview(
        preview_path, project, approved_preview_sha256, loader)
    run_dir = project / "state/runs/cap-update-submissions"
    _require(common._inside(run_dir, project), "Submission state must remain in the project")
    run_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    key = attempt_key(final)
    attempt = run_dir / (key + ".attempt.json")
    receipt = run_dir / (key + ".result.json")
    _require(not attempt.exists() and not receipt.exists(),
             "An attempt already exists for this target and ZIP; reconcile it before any retry")
    approved = hook.approve_data_load_preview({"preview": retained["preview"]})
    checked = hook.verify_approved_data_load_archive(approved, archive)
    envelope = Path(preview_path).resolve().parent / "cap-update-approved-task-envelope.json"
    _require(not envelope.exists(), "A retained approval envelope already exists; reconcile before retry")
    common._save_new(envelope, checked["taskValidationEnvelope"])
    # Frozen-state integrity on both sides of shared approval, not a second
    # Task Hook validation pass and not a time-sensitive preparation rerun.
    _frozen_preview(preview_path, project, approved_preview_sha256, loader)
    _require(common._json(envelope) == checked["taskValidationEnvelope"], "Approved task envelope changed")
    try:
        _save_exclusive(attempt, {"status": "attempt_started", "operation": "update",
            "previewSha256": approved_preview_sha256, "bindingSha256": final["bindingSha256"],
            "environment": final["environment"], "archiveSha256": final["archiveSha256"],
            "profileNumber": final["profileNumber"],
            "recordedAt": datetime.now(timezone.utc).isoformat(), "retryAllowed": False})
    except FileExistsError as exc:
        raise SubmissionBlocked("An attempt already exists; automatic retry is forbidden") from exc
    try:
        result = loader.upload_approved_preflight(
            preflight_path, task_validation_envelope=envelope,
            auth_options={"token_cache": str(Path("auto"))})
    except BaseException as exc:
        # Preserve uncertain state, including interruptions, without persisting
        # raw exception text, auth diagnostics, responses or sensitive inputs.
        stage = getattr(exc, "stage", None)
        safe_stage = stage if stage in {"approval", "task-validation", "ucm-upload", "data-load-initiation", "authentication"} else "shared-submission"
        record = {"status": "failed_or_uncertain", "stage": safe_stage, "retryAllowed": False,
                  "ContentId": _safe_external_id(getattr(exc, "content_id", None))}
        try:
            _save_exclusive(receipt, record)
        except (OSError, ValueError):
            pass  # The durable attempt marker still prevents blind replay.
        raise
    warnings = []
    try:
        _save_exclusive(receipt, {"status": "submitted", "operation": "update",
            "readbackVerified": False, "processingVerified": False,
            "RequestId": _safe_external_id(result.get("RequestId")),
            "ContentId": _safe_external_id(result.get("ContentId")), "retryAllowed": False})
    except (OSError, ValueError):
        warnings.append("Fusion accepted submission, but its local receipt could not be verified; retain the returned request ID and do not resubmit")
        return {"status": "submitted", "result": result, "attemptPath": str(attempt),
                "receiptPath": None, "warnings": warnings}
    # Retire only internal envelopes after accepted initiation. Keep ZIP,
    # preview, durable anti-repeat marker and the honest submission receipt.
    for internal in (preflight_path, envelope):
        try:
            internal.unlink()
        except OSError:
            warnings.append("Internal envelope retirement failed; do not resubmit")
    return {"status": "submitted", "result": result, "attemptPath": str(attempt),
            "receiptPath": str(receipt), "warnings": warnings}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--approved-preview-sha256", required=True)
    parser.add_argument("--approve-upload", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = submit_update(preview_path=args.preview, project_root=args.project_root,
                               approved_preview_sha256=args.approved_preview_sha256,
                               approve_upload=args.approve_upload)
    except Exception as exc:
        blocked = isinstance(exc, (SubmissionBlocked, common.PreparationBlocked))
        message = str(exc) if blocked else "Submission did not complete; effects may be uncertain. Inspect retained state before any retry"
        status = "Blocked" if blocked else "Failed or uncertain"
        print("| Stage | Result | Details |\n|---|---|---|\n| CAP update submission | " + status + " | " + message + " |")
        return 2
    for warning in result["warnings"]:
        print("Warning: " + warning, file=sys.stderr)
    print(common.shared_loader().data_loader_report.render_initiation_report(result["result"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
