"""Submit one explicitly approved, frozen CAP create through shared Data Loader.

Python 3.11+. No network implementation or live revalidation belongs here.
Consent must be the later user approval of the exact retained preview; this CLI
does not obtain consent and must never manufacture it from an earlier plan.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys

import cap_create_handoff as handoff


class SubmissionBlocked(ValueError):
    """Stop before shared submission; never select an alternate write route."""


def _require(condition, message):
    if not condition:
        raise SubmissionBlocked(message)


def attempt_key(final_data):
    """Same target and ZIP cannot be replayed by copying/reissuing a preview."""
    return handoff._digest({"environment": final_data["environment"],
                           "archiveSha256": final_data["archiveSha256"],
                           "operation": "create"})


def _save_exclusive(path, value):
    content = (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    # Claim the filename exclusively and retain it even on interrupted writes.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
    directory_fd = os.open(Path(path).parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
    _require(Path(path).read_bytes() == content, "Submission state could not be verified")


def _safe_external_id(value):
    if isinstance(value, int) and not isinstance(value, bool) and value > 0:
        return value
    if isinstance(value, str) and re.fullmatch(r"(?:[0-9]+|UCMFA[0-9]+)", value):
        return value
    return None


def _frozen_preview(preview_path, project, approved_digest, loader):
    path = Path(preview_path).resolve(strict=True)
    _require(handoff._inside(path, project), "Preview must belong to the selected project")
    retained = handoff._json(path)
    preview = retained.get("preview")
    _require(isinstance(preview, dict) and re.fullmatch(r"[0-9a-f]{64}", approved_digest or "")
             and handoff._digest(preview) == retained.get("previewSha256") == approved_digest,
             "Explicit approval must match the exact retained CAP preview digest")
    _require(preview.get("taskCode") == handoff.cap_workflow.CODE
             and preview.get("taskName") == handoff.cap_workflow.TASK
             and preview.get("executionRoute") == "data-loader",
             "Only the canonical CAP Data Loader task can be submitted")
    final = preview.get("finalData", {})
    evidence = final.get("createEvidence", {})
    prepared = retained.get("prepared", {})
    binding = prepared.get("binding", {})
    _require(final.get("validationPurpose") == "create_preparation_only"
             and final.get("writeEligible") is False
             and final.get("operation") == evidence.get("operation") == "create"
             and evidence.get("businessObject") == "learningCatalogProfiles"
             and evidence.get("restContext") == "ORA_HCM_REST",
             "Retrieval readiness or an unsupported operation cannot authorize creation")
    expected = {key: final.get(key) for key in (
        "operation", "archiveSha256", "environment", "runbook", "inputs",
        "sourceFingerprint", "evidenceSha256")}
    _require(binding == expected and handoff._digest(binding) == prepared.get("bindingSha256")
             == final.get("bindingSha256")
             and prepared.get("validation_purpose") == "create_preparation_only"
             and prepared.get("write_eligible") is False
             and final.get("inputs") == evidence.get("intendedFields")
             and final.get("environment") == evidence.get("environment")
             and final.get("runbook") == evidence.get("runbook")
             and final.get("sourceFingerprint") == evidence.get("sourceFingerprint")
             and final.get("evidenceSha256") == handoff._digest(evidence),
             "Frozen CAP inputs, evidence, target or preparation binding changed")
    results = preview.get("ruleResults", [])
    _require(isinstance(results, list) and results
             and all(isinstance(row, dict) and row.get("status") in {"passed", "not_applicable"}
                     for row in results) and any(row["status"] == "passed" for row in results),
             "CAP requires successful preparation without rule overrides")
    # Integrity only: do not reopen original DAT/evidence/context or rerun rules,
    # expiration/duplicate checks, metadata, source compilation or ZIP generation.
    preflight_path = Path(retained.get("sharedPreflightPath", "")).resolve(strict=True)
    archive = Path(retained.get("archivePath", "")).resolve(strict=True)
    _require(handoff._inside(preflight_path, path.parent) and handoff._inside(archive, path.parent)
             and preflight_path != archive
             and handoff._file_digest(preflight_path) == final.get("sharedPreflightSha256")
             and handoff._file_digest(archive) == final.get("archiveSha256"),
             "Retained shared preflight or immutable ZIP changed")
    preflight = loader.load_preflight_envelope(preflight_path)
    _require(preflight.get("taskRouted") is True and preflight.get("mappingComplete") is True
             and preflight.get("sourceType") is None
             and Path(preflight.get("approvedArtifactPath", "")).resolve() == archive
             and preflight.get("archiveSha256") == final["archiveSha256"]
             and preflight.get("host") == final["environment"]["host"]
             and preflight.get("environment") == final["environment"]["name"]
             and preflight.get("runID") == final["runbook"]["runID"],
             "Shared preflight differs from the approved CAP route or context")
    run_config = handoff.project_run_config(project)
    _, _, current_binding = handoff._project_context(project, evidence, loader, run_config_path=run_config)
    _require(current_binding == final.get("projectBinding"), "Project Run Book binding changed")
    return retained, final, archive, preflight_path


def submit_create(*, preview_path, project_root, approved_preview_sha256,
                  approve_upload=False):
    """One genuine approved attempt; shared services own all external traffic.

    Returns initiation only, never created/processed success. No automatic poll,
    retry, token/host override, replacement artifact or direct REST alternative.
    """
    _require(approve_upload is True, "Explicit exact-load approval is required before submission")
    project = Path(project_root).resolve(strict=True)
    _require(handoff._inside(project, handoff.REPO / "project"), "Invalid project workspace")
    loader, hook = handoff.shared_loader(), handoff.shared_hook()
    retained, final, archive, preflight_path = _frozen_preview(
        preview_path, project, approved_preview_sha256, loader)
    run_dir = project / "state/runs/cap-create-submissions"
    _require(handoff._inside(run_dir, project), "Submission state must remain in the project")
    run_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    key = attempt_key(final)
    attempt = run_dir / (key + ".attempt.json")
    receipt = run_dir / (key + ".result.json")
    _require(not attempt.exists() and not receipt.exists(),
             "An attempt already exists for this target and ZIP; reconcile it before any retry")
    approved = hook.approve_data_load_preview({"preview": retained["preview"]})
    checked = hook.verify_approved_data_load_archive(approved, archive)
    envelope = Path(preview_path).resolve().parent / "cap-approved-task-envelope.json"
    _require(not envelope.exists(), "A retained approval envelope already exists; reconcile before retry")
    handoff._save_new(envelope, checked["taskValidationEnvelope"])
    # Verify the frozen state on both sides of shared approval. This is not
    # another task-validation pass, and original source files are never read.
    _frozen_preview(preview_path, project, approved_preview_sha256, loader)
    _require(handoff._json(envelope) == checked["taskValidationEnvelope"], "Approved task envelope changed")
    try:
        _save_exclusive(attempt, {"status": "attempt_started", "operation": "create",
            "previewSha256": approved_preview_sha256, "bindingSha256": final["bindingSha256"],
            "environment": final["environment"], "archiveSha256": final["archiveSha256"],
            "recordedAt": datetime.now(timezone.utc).isoformat(),
            "retryAllowed": False})
    except FileExistsError as exc:
        raise SubmissionBlocked("An attempt already exists; automatic retry is forbidden") from exc
    try:
        result = loader.upload_approved_preflight(
            preflight_path, task_validation_envelope=envelope,
            run_config_path=handoff.project_run_config(project),
            auth_options={"token_cache": str(Path("auto"))})
    except BaseException as exc:
        # Preserve attempt/envelopes even on Ctrl-C; never store raw responses,
        # auth errors, exception text, URLs, rosters or credential material.
        stage = getattr(exc, "stage", None)
        safe_stage = stage if stage in {"approval", "task-validation", "ucm-upload", "data-load-initiation", "authentication"} else "shared-submission"
        record = {"status": "failed_or_uncertain", "stage": safe_stage, "retryAllowed": False,
                  "ContentId": _safe_external_id(getattr(exc, "content_id", None))}
        try:
            _save_exclusive(receipt, record)
        except (OSError, SubmissionBlocked):
            pass  # The durable attempt marker still forbids blind replay.
        raise
    # Shared uploader verifies accepted initiation. Never infer CAP completion.
    warnings = []
    try:
        _save_exclusive(receipt, {"status": "submitted", "processingVerified": False,
            "RequestId": _safe_external_id(result.get("RequestId")),
            "ContentId": _safe_external_id(result.get("ContentId")), "retryAllowed": False})
    except (OSError, SubmissionBlocked):
        warnings.append("Fusion accepted submission, but its local receipt could not be verified; retain the returned request ID and do not resubmit")
        return {"status": "submitted", "result": result, "attemptPath": str(attempt),
                "receiptPath": None, "warnings": warnings}
    # Shared lifecycle retires only internal envelopes on accepted initiation.
    # Keep the approved ZIP, CAP preview, anti-repeat state and result receipt.
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
        result = submit_create(preview_path=args.preview, project_root=args.project_root,
                               approved_preview_sha256=args.approved_preview_sha256,
                               approve_upload=args.approve_upload)
    except Exception as exc:
        # Shared DataLoadError is not a ValueError. Never leak its raw response
        # or auth details in a traceback, and do not mislabel uncertainty as no-op.
        blocked = isinstance(exc, (SubmissionBlocked, handoff.PreparationBlocked))
        message = str(exc) if blocked else "Submission did not complete; effects may be uncertain. Inspect retained state before any retry"
        status = "Blocked" if blocked else "Failed or uncertain"
        print("| Stage | Result | Details |\n|---|---|---|\n| CAP submission | " + status + " | " + message + " |")
        return 2
    for warning in result["warnings"]:
        print("Warning: " + warning, file=sys.stderr)
    loader = handoff.shared_loader()
    print(loader.data_loader_report.render_initiation_report(result["result"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
