"""Evidence-gated sparse CAP update preparation through unchanged shared services.

Python 3.11+. Only local preparation and shared read-only metadata occur here.
Source statuses must be independently established; fixtures are never live proof.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

import cap_create_handoff as common
import cap_update_validation as validation
import cap_workflow

SKILL, REPO = common.SKILL, common.REPO
PreparationBlocked = common.PreparationBlocked
UPDATE_NODES = ("CAP-SELECT", "CAP-UPDATE-VALIDATE", "CAP-UPDATE-EVIDENCE",
                "CAP-UPDATE-DESIGN", "CAP-UPDATE-ARTIFACT", "CAP-UPDATE-READY")

# Shared services and generic CAP-local integrity utilities remain single-owned.
_require = common._require
_digest = common._digest
_file_digest = common._file_digest
_json = common._json
_inside = common._inside
_save_new = common._save_new
_project_context = common._project_context
_verify_evidence_refs = common._verify_evidence_refs
_run_preflight = common._run_preflight
source_fingerprint = common.source_fingerprint
shared_loader = common.shared_loader
shared_hook = common.shared_hook


def _update_trace(task, passed):
    """The separate update branch cannot reuse create or retrieval readiness."""
    nodes = {node["id"]: node for node in task["nodes"]}
    current, trace = task["start_node"], []
    for expected in UPDATE_NODES:
        _require(current == expected and current in nodes,
                 "Source graph does not declare bounded update preparation")
        node = nodes[current]
        _require(all(item in passed for item in node.get("prerequisites", [])),
                 "Update prerequisite was not evaluated")
        outcome = "update_prepare" if current == "CAP-SELECT" else "passed"
        trace.append({"node": current, "outcome": "stop_for_approval"
                      if current == UPDATE_NODES[-1] else outcome})
        if current == UPDATE_NODES[-1]:
            _require(node["action_type"] == "terminal", "Update must end at its own terminal")
            break
        _require(current in passed, "Update node was not evaluated")
        current = node["transitions"].get(outcome)
    return trace


def prepare_update(*, source_path, evidence_path, task_context_path, project_root,
                   output_dir, timeout=180):
    """Run only verified-evidence preparation and retain an unapproved preview.

    Inputs are local paths. The only external route is shared loader preflight,
    which performs authentication and GET metadata; never a CAP-specific client.
    """
    source, evidence_path, context = map(lambda p: Path(p).resolve(strict=True),
                                        (source_path, evidence_path, task_context_path))
    project = Path(project_root).resolve(strict=True)
    destination = Path(output_dir).resolve()
    _require(_inside(destination, project) and not destination.exists(),
             "Use a new preparation directory within the selected project; do not overwrite retained approvals")
    _require(source.name == validation.CONTRACT["datFile"] and _inside(source, project)
             and _inside(evidence_path, project) and _inside(context, project),
             "DAT, evidence and task context must belong to the selected project")
    _require(type(timeout) is int and 1 <= timeout <= 600, "Preflight deadline must be 1 to 600 seconds")
    fingerprint = source_fingerprint()
    evidence = _json(evidence_path)
    validation.validate_evidence(evidence, fingerprint)
    references = _verify_evidence_refs(evidence, project)
    loader, hook = shared_loader(), shared_hook()
    config, run_id, project_binding = _project_context(project, evidence, loader)
    context_data = _json(context)
    tasks = [task for task in context_data.get("tasks", [])
             if task.get("task_code") == cap_workflow.CODE and task.get("task_name") == cap_workflow.TASK]
    _require(len(tasks) == 1, "Task context must select exactly one CAP task")
    task = tasks[0]
    _require((REPO / task.get("skill_path", "")).resolve() in (
                 SKILL, SKILL / "SKILL.md"),
             "Task context resolves to a different skill")
    sequence = task.get("sequence")
    _require(type(sequence) is int and sequence > 0, "Task context needs a positive sequence")
    if not evidence["intendedFields"]:
        return {"status": "no_op", "operation": "update",
                "profileNumber": evidence["baseline"][validation.CONTRACT["identityField"]],
                "write_eligible": False, "message": "No changed fields; no load prepared or submitted."}
    context_digest, evidence_digest, source_digest = map(_file_digest, (context, evidence_path, source))
    # Reject wrong operations/extra rows/children before even read-only metadata.
    validation.validate_archive(loader.prepare_archive(source).content, evidence)
    source_plan = cap_workflow.shared_plan()
    _update_trace(source_plan["task"], set(UPDATE_NODES[:-1]))
    destination.mkdir(mode=0o700, parents=True)
    # Core persists its ZIP beside the supplied DAT. Give it an exclusive copy
    # inside this new preparation directory so no prior reviewed ZIP beside the
    # original source can be overwritten, even when its semantic name repeats.
    staged_source = destination / validation.CONTRACT["datFile"]
    source_bytes = source.read_bytes()
    _require(hashlib.sha256(source_bytes).hexdigest() == source_digest,
             "Original DAT changed before staging")
    with staged_source.open("xb") as stream:
        os.chmod(staged_source, 0o600)
        stream.write(source_bytes)
    _require(staged_source.read_bytes() == source_bytes, "Staged DAT readback failed")
    envelope = destination / "shared-preflight.json"
    _run_preflight(staged_source, envelope, timeout)
    preflight = loader.load_preflight_envelope(envelope)
    _require(preflight.get("taskRouted") is True and preflight.get("mappingComplete") is True,
             "Shared preflight did not validate the task-routed source")
    _require(preflight.get("environment") == config.get("environment")
             and preflight.get("host") == config["host"] and preflight.get("runID") == run_id,
             "Shared preflight target or Run Book differs")
    artifact = Path(preflight.get("approvedArtifactPath", "")).resolve()
    _require(_inside(artifact, destination) and artifact.is_file(),
             "Shared immutable artifact is missing or outside this preparation directory")
    content = artifact.read_bytes()
    _require(hashlib.sha256(content).hexdigest() == preflight.get("archiveSha256"), "Shared artifact digest changed")
    prepared = validation.preparation_binding(content, evidence, fingerprint, config, run_id)
    plan = hook.data_load(context, cap_workflow.TASK, sequence, False)
    trace = _update_trace(source_plan["task"], set(UPDATE_NODES[:-1]))
    executed = set(UPDATE_NODES[:-1])
    results = []
    privilege_notice = ("Write grants are not independently verified. Shared authenticated "
                        "read-only preflight completed; Fusion enforces UCM upload and loader "
                        "authorization during the exact approved load. Stop on rejection; no permission probe.")
    assessed_privileges = evidence["checks"]["privileges"]["status"] == "assessed"
    if evidence["checks"]["identity"]["mapping"] == "registered_composite":
        date_notice = ("The approved item-key date is fixed at "
                       + evidence["checks"]["identity"]["dateValue"]
                       + "; it is not recomputed at submission. Item identity and effectiveOf "
                       "processing directives are separate; no transactional as-of guarantee is claimed. ")
    else:
        date_notice = "Effective context is server-current, not a frozen future as-of date. "
    conflict_notice = ("Sparse PATCH omits unrelated settings, but does not prevent a concurrent "
                       "change to the same field being overwritten. " + date_notice
                       + "Verify readback separately.")
    for resource in plan["taskValidation"]["ruleResources"]:
        covered = [node["id"] for node in resource["nodes"] if node["id"] in executed]
        issues = ([{"severity": "info", "message": "Evaluated update nodes: " + ", ".join(covered)}]
                  if covered else [])
        if assessed_privileges and "CAP-UPDATE-EVIDENCE" in covered:
            issues.append({"severity": "warning", "message": privilege_notice})
        if "CAP-UPDATE-DESIGN" in covered:
            issues.append({"severity": "warning", "message": conflict_notice})
        results.append({"source": resource["file"], "status": "passed" if covered else "not_applicable",
                        "issues": issues, "changes": []})
    final_data = {**prepared["binding"], "validationPurpose": "update_preparation_only",
                  "writeEligible": False, "updateEvidence": evidence, "evidenceReferences": references,
                  "taskContextSha256": context_digest, "taskCode": cap_workflow.CODE,
                  "taskName": cap_workflow.TASK, "sequence": sequence,
                  "originalSourceSha256": source_digest, "stagedSourceSha256": _file_digest(staged_source),
                  "sharedPreflightSha256": _file_digest(envelope), "projectBinding": project_binding,
                  "nodeTrace": trace, "bindingSha256": prepared["bindingSha256"]}
    def verify_retained_inputs():
        # Task Hook rereads context/registry; check both sides of that call.
        # This also covers source evidence files and shared envelope bytes.
        _require(source_fingerprint() == fingerprint and _file_digest(source) == source_digest
                 and _file_digest(staged_source) == source_digest
                 and _file_digest(context) == context_digest and _file_digest(evidence_path) == evidence_digest
                 and _file_digest(artifact) == preflight["archiveSha256"]
                 and _file_digest(envelope) == final_data["sharedPreflightSha256"],
                 "Preparation inputs changed; fresh validation is required")
        _verify_evidence_refs(evidence, project)
        new_config, new_run_id, new_binding = _project_context(project, evidence, loader)
        _require(new_config["host"] == config["host"] and new_run_id == run_id and new_binding == project_binding,
                 "Project or target changed during preparation")

    verify_retained_inputs()
    preview_result = hook.build_data_load_preview({"taskContextPath": str(context), "taskName": cap_workflow.TASK,
                                                   "sequence": sequence, "finalData": final_data,
                                                   "ruleResults": results})
    verify_retained_inputs()
    preview = preview_result["preview"]
    retained = {"preview": preview, "previewSha256": _digest(preview), "prepared": prepared,
                "sharedPreflightPath": str(envelope), "archivePath": str(artifact),
                "approval": None, "write_eligible": False}
    preview_path = destination / "cap-update-preview.json"
    _save_new(preview_path, retained)
    return {"status": "awaiting_exact_load_approval", "write_eligible": False,
            "operation": "update", "archiveSha256": preflight["archiveSha256"],
            "archivePath": str(artifact), "previewPath": str(preview_path),
            "sharedPreflightPath": str(envelope), "previewSha256": retained["previewSha256"],
            "warnings": ([privilege_notice] if assessed_privileges else []) + [conflict_notice],
            "rowCount": 1, "side_effects": ["local preparation artifacts", "shared read-only metadata checks"]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source", "evidence", "task-context", "project-root", "output-dir"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args(argv)
    try:
        result = prepare_update(source_path=args.source, evidence_path=args.evidence,
                                task_context_path=args.task_context, project_root=args.project_root,
                                output_dir=args.output_dir, timeout=args.timeout)
    except (ValueError, OSError, ImportError, KeyError) as exc:
        # Errors are local contract messages, never raw auth/client output.
        print(json.dumps({"status": "blocked", "write_eligible": False,
                          "message": str(exc), "approval_created": False}))
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
