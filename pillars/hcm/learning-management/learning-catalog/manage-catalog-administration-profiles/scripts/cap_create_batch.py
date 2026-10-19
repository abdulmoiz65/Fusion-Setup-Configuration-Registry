"""Independent one-root CAP creates using the existing shared-loader handoff.

This is NOT a multi-root DAT, atomic transaction, mixed updater or generic write
route. Every member uses unchanged prepare_create/submit_create validation. A
later explicit approval binds the exact manifest and every retained preview/ZIP.
Stop after the first failed, uncertain or locally unverified submission; no retry.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re

import cap_create_handoff as handoff
import cap_create_submission as submission


class BatchBlocked(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise BatchBlocked(message)


def _project(project_root):
    project = Path(project_root).resolve(strict=True)
    _require(handoff._inside(project, handoff.REPO / "project"), "Use the selected repository project")
    return project


def _relative_file(base, value):
    _require(isinstance(value, str) and value and not Path(value).is_absolute()
             and ".." not in Path(value).parts, "Batch members require contained relative paths")
    path = (base / value).resolve(strict=True)
    _require(path.is_file() and handoff._inside(path, base), "Batch artifact escaped its retained directory")
    return path


def _member(prepared, row_id, destination, project, loader):
    retained, final, archive, _ = submission._frozen_preview(
        prepared["previewPath"], project, prepared["previewSha256"], loader)
    preview = Path(prepared["previewPath"]).resolve(strict=True)
    _require(handoff._inside(preview, destination) and handoff._inside(archive, destination),
             "Batch preview and archive must remain in the batch directory")
    return {"rowId": row_id, "previewPath": str(preview.relative_to(destination)),
            "previewSha256": retained["previewSha256"], "archivePath": str(archive.relative_to(destination)),
            "archiveSha256": final["archiveSha256"], "inputs": final["inputs"]}, final


def prepare_batch(*, rows, project_root, output_dir, timeout=180):
    """Prepare 1..20 independent validated roots; read-only shared preflight only.

    Each row contains row_id, source_path, evidence_path and task_context_path.
    A partially prepared batch retains its artifacts but has no approval manifest.
    """
    project = _project(project_root)
    destination = Path(output_dir).resolve()
    _require(handoff._inside(destination, project) and not destination.exists(),
             "Use a new batch directory inside the selected project")
    _require(isinstance(rows, list) and 1 <= len(rows) <= 20, "Independent batch budget is 1 to 20 roots")
    _require(type(timeout) is int and 1 <= timeout <= 600, "Per-root preflight timeout must be 1 to 600 seconds")
    normalized, row_ids = [], set()
    for row in rows:
        _require(isinstance(row, dict) and set(row) == {"row_id", "source_path", "evidence_path", "task_context_path"},
                 "Only explicit root creation inputs are accepted")
        row_id = row["row_id"]
        _require(isinstance(row_id, str) and re.fullmatch(r"[A-Za-z0-9_-]{1,100}", row_id)
                 and row_id not in row_ids, "Batch rows need distinct safe stable IDs")
        paths = {key: Path(row[key]).resolve(strict=True) for key in ("source_path", "evidence_path", "task_context_path")}
        _require(all(path.is_file() and handoff._inside(path, project) for path in paths.values()),
                 "Every input belongs to the selected project")
        normalized.append({"row_id": row_id, **paths})
        row_ids.add(row_id)
    # Reject duplicate intended names/numbers before read-only preflight. This is
    # additional batch consistency, not a substitute for each real DAT validator.
    evidence_rows = [handoff._json(row["evidence_path"]) for row in normalized]
    names = [evidence.get("intendedFields", {}).get("name") for evidence in evidence_rows]
    numbers = [evidence.get("intendedFields", {}).get("learningCatalogProfileNumber") for evidence in evidence_rows]
    _require(all(isinstance(name, str) and name for name in names) and len(names) == len(set(names)),
             "Batch creation names must be distinct")
    specified = [number for number in numbers if number is not None]
    _require(all(isinstance(number, str) and number for number in specified)
             and len(specified) == len(set(specified)), "Supplied profile numbers must be distinct")
    contexts = [{"environment": item.get("environment"), "runbook": item.get("runbook")} for item in evidence_rows]
    _require(all(context == contexts[0] for context in contexts), "Batch roots must use one target and Run Book")
    destination.mkdir(parents=True, mode=0o700)
    loader = handoff.shared_loader()
    members, outcomes, first_final = [], [], None
    for index, row in enumerate(normalized, 1):
        try:
            prepared = handoff.prepare_create(**{key: row[key] for key in ("source_path", "evidence_path", "task_context_path")},
                project_root=project, output_dir=destination / ("root-" + str(index)), timeout=timeout)
            member, final = _member(prepared, row["row_id"], destination, project, loader)
            if first_final is None:
                first_final = final
            _require(all(final[key] == first_final[key] for key in ("environment", "runbook", "projectBinding", "sourceFingerprint")),
                     "Target, Run Book, project binding or implementation changed during preparation")
            members.append(member)
            outcomes.append({"rowId": row["row_id"], "status": "prepared", "previewPath": member["previewPath"]})
        except Exception:
            outcomes.append({"rowId": row["row_id"], "status": "preparation_failed"})
            outcomes.extend({"rowId": later["row_id"], "status": "not_prepared"} for later in normalized[index:])
            report = {"status": "preparation_failed", "rows": outcomes, "write_eligible": False,
                      "message": "No batch approval manifest was created. Inspect the failed root; no upload occurred."}
            handoff._save_new(destination / "cap-create-batch-preparation-failure.json", report)
            return report
    manifest = {"schemaVersion": "1.0", "operation": "create", "mode": "independent-root-loads",
                "atomic": False, "environment": first_final["environment"], "runbook": first_final["runbook"],
                "projectBinding": first_final["projectBinding"], "rows": members,
                "approval": None, "writeEligible": False}
    retained = {"manifest": manifest, "manifestSha256": handoff._digest(manifest)}
    path = destination / "cap-create-batch-preview.json"
    handoff._save_new(path, retained)
    return {"status": "awaiting_exact_batch_approval", "manifestPath": str(path),
            "manifestSha256": retained["manifestSha256"], "rowCount": len(members),
            "mode": manifest["mode"], "atomic": False, "write_eligible": False}


def verify_batch(*, manifest_path, project_root, approved_manifest_sha256):
    """Read-only integrity verification of ALL members before the first write."""
    project = _project(project_root)
    path = Path(manifest_path).resolve(strict=True)
    _require(handoff._inside(path, project), "Batch manifest must belong to the selected project")
    retained = handoff._json(path)
    manifest = retained.get("manifest", {})
    _require(isinstance(approved_manifest_sha256, str) and re.fullmatch(r"[a-f0-9]{64}", approved_manifest_sha256)
             and retained.get("manifestSha256") == approved_manifest_sha256 == handoff._digest(manifest),
             "Approval must match the exact retained batch manifest")
    _require(set(manifest) == {"schemaVersion", "operation", "mode", "atomic", "environment", "runbook", "projectBinding", "rows", "approval", "writeEligible"}
             and manifest["schemaVersion"] == "1.0" and manifest["operation"] == "create"
             and manifest["mode"] == "independent-root-loads" and manifest["atomic"] is False
             and manifest["approval"] is None and manifest["writeEligible"] is False,
             "Only unmodified independent root-create manifests are supported")
    rows = manifest["rows"]
    _require(isinstance(rows, list) and 1 <= len(rows) <= 20, "Invalid batch size")
    loader, checked, identities, names, numbers, preview_paths = handoff.shared_loader(), [], set(), set(), set(), set()
    for row in rows:
        _require(isinstance(row, dict) and set(row) == {"rowId", "previewPath", "previewSha256", "archivePath", "archiveSha256", "inputs"}
                 and isinstance(row["rowId"], str) and re.fullmatch(r"[A-Za-z0-9_-]{1,100}", row["rowId"])
                 and row["rowId"] not in identities, "Invalid or duplicate batch row")
        identities.add(row["rowId"])
        preview = _relative_file(path.parent, row["previewPath"])
        archive = _relative_file(path.parent, row["archivePath"])
        _require(preview not in preview_paths, "A preview cannot appear twice in a batch")
        preview_paths.add(preview)
        _, final, retained_archive, _ = submission._frozen_preview(preview, project, row["previewSha256"], loader)
        _require(final["environment"] == manifest["environment"] and final["runbook"] == manifest["runbook"]
                 and final["projectBinding"] == manifest["projectBinding"] and final["inputs"] == row["inputs"]
                 and final["archiveSha256"] == row["archiveSha256"] and archive == retained_archive,
                 "A batch row differs from its frozen exact preview")
        name, number = final["inputs"].get("name"), final["inputs"].get("learningCatalogProfileNumber")
        _require(name not in names and (number is None or number not in numbers), "Duplicate batch profile identity")
        names.add(name)
        if number is not None:
            numbers.add(number)
        key = submission.attempt_key(final)
        state = project / "state/runs/cap-create-submissions"
        _require(not (state / (key + ".attempt.json")).exists() and not (state / (key + ".result.json")).exists()
                 and not (preview.parent / "cap-approved-task-envelope.json").exists(),
                 "A member already has submission state; reconcile without automatic retry")
        checked.append({"rowId": row["rowId"], "previewPath": str(preview), "previewSha256": row["previewSha256"],
                        "archiveSha256": row["archiveSha256"]})
    return manifest, checked


def submit_batch(*, manifest_path, project_root, approved_manifest_sha256, approve_upload=False):
    """Continue one explicitly approved manifest; each root is a separate load.

    All accepted rows still require loader monitoring and independent readback.
    A batch attempt is not resumable as a fresh submission after uncertainty.
    """
    _require(approve_upload is True, "Explicit approval of the exact batch is required")
    project = _project(project_root)
    manifest, checked = verify_batch(manifest_path=manifest_path, project_root=project,
                                     approved_manifest_sha256=approved_manifest_sha256)
    state = project / "state/runs/cap-create-batches"
    _require(handoff._inside(state, project), "Batch state escaped the selected project")
    state.mkdir(parents=True, exist_ok=True, mode=0o700)
    key = handoff._digest({"environment": manifest["environment"], "archives": [row["archiveSha256"] for row in checked]})
    attempt, receipt = state / (key + ".attempt.json"), state / (key + ".result.json")
    _require(not receipt.exists(), "Batch outcome already exists; do not retry")
    try:
        submission._save_exclusive(attempt, {"status": "attempt_started", "manifestSha256": approved_manifest_sha256,
            "recordedAt": datetime.now(timezone.utc).isoformat(), "retryAllowed": False})
    except FileExistsError as exc:
        raise BatchBlocked("Batch attempt already exists; do not retry") from exc
    outcomes = []
    status = "submitted"
    for index, row in enumerate(checked):
        try:
            result = submission.submit_create(preview_path=row["previewPath"], project_root=project,
                approved_preview_sha256=row["previewSha256"], approve_upload=True)
            if result.get("status") != "submitted":
                raise BatchBlocked("Member initiation outcome is uncertain")
            details = result.get("result", {})
            outcome = {"rowId": row["rowId"], "status": "submitted",
                       "RequestId": submission._safe_external_id(details.get("RequestId")),
                       "ContentId": submission._safe_external_id(details.get("ContentId")),
                       "receiptPath": result.get("receiptPath"), "processingVerified": False}
            outcomes.append(outcome)
            if result.get("warnings") or not outcome["RequestId"] or not outcome["ContentId"] or not outcome["receiptPath"]:
                status = "stopped_after_submission_warning"
        except Exception:
            outcomes.append({"rowId": row["rowId"], "status": "failed_or_uncertain", "processingVerified": False})
            status = "stopped_after_failure_or_uncertainty"
        if status != "submitted":
            outcomes.extend({"rowId": later["rowId"], "status": "not_submitted"} for later in checked[index + 1:])
            break
    report = {"status": status, "mode": "independent-root-loads", "atomic": False, "rows": outcomes,
              "processingVerified": False, "retryAllowed": False, "manifestSha256": approved_manifest_sha256,
              "attemptPath": str(attempt), "receiptPath": str(receipt)}
    try:
        submission._save_exclusive(receipt, report)
    except (OSError, ValueError):
        report["receiptPath"] = None
        report["warning"] = "Batch outcome could not be saved. Retain per-root request IDs and never resubmit."
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "submit"))
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--rows", type=Path, help="Local JSON array of explicit preparation rows")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--approved-manifest-sha256")
    parser.add_argument("--approve-upload", action="store_true")
    args = parser.parse_args()
    try:
        if args.action == "prepare":
            _require(args.rows is not None and args.output_dir is not None and not args.approve_upload,
                     "Preparation needs local rows and a new output directory, not approval")
            result = prepare_batch(rows=json.loads(args.rows.read_text()), project_root=args.project_root,
                                   output_dir=args.output_dir)
        else:
            _require(args.manifest is not None and args.rows is None and args.output_dir is None,
                     "Submit only a retained manifest")
            result = submit_batch(manifest_path=args.manifest, project_root=args.project_root,
                                  approved_manifest_sha256=args.approved_manifest_sha256,
                                  approve_upload=args.approve_upload)
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0 if result["status"] in {"awaiting_exact_batch_approval", "submitted"} else 2
    except Exception:
        print(json.dumps({"status": "blocked_or_uncertain", "retryAllowed": False,
                          "message": "Batch did not complete; inspect retained state before any further action."}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
