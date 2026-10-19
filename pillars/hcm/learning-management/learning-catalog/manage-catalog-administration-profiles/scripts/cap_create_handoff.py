"""Preparation-only CAP handoff to unchanged shared Data Loader and Task Hook.

Python 3.11+. No approval, upload or submission API is exposed. Evidence must
already have been established by a reviewer using the declared read contracts;
this module checks its completeness, provenance and binding, not its truth.
"""
from __future__ import annotations
import cap_visibility

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit

import cap_create_validation as validation
import cap_workflow

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
from cap_paths import repository_root
REPO = repository_root(SKILL)
CREATE_NODES = ("CAP-SELECT", "CAP-CREATE-VALIDATE", "CAP-CREATE-EVIDENCE",
                "CAP-CREATE-ARTIFACT", "CAP-CREATE-READY")


class PreparationBlocked(ValueError):
    """A missing or changed prerequisite; never authorizes a fallback route."""


def _require(condition, message):
    if not condition:
        raise PreparationBlocked(message)


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def _file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _json(path):
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    _require(isinstance(value, dict), "Expected a JSON object")
    return value


def _inside(path, directory):
    try:
        Path(path).resolve().relative_to(Path(directory).resolve())
        return True
    except ValueError:
        return False


def _shared_module(name, relative):
    path = REPO / relative
    scripts = str(path.parent)
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def shared_loader():
    return _shared_module("cap_preparation_shared_loader", "core/data-loader/scripts/upload_and_initiate.py")


def shared_hook():
    return _shared_module("cap_preparation_shared_hook", "core/data-loader/task-hook/scripts/task_hook.py")


def source_fingerprint():
    """Bind the real compiled graph and pillar implementations, not caller text."""
    cap_workflow.shared_plan()
    paths = sorted(set(SKILL.glob("scripts/*.py")) | set(SKILL.glob("ora-resource/*.md"))
                   | {SKILL / "ora-resource/ora_rule_registry.json"})
    return _digest({str(path.relative_to(SKILL)): _file_digest(path) for path in paths})


def project_run_config(project_root, *, create=False):
    """Materialize only the active project identity; never edit shared defaults."""
    root = Path(project_root).resolve(strict=True)
    _require(_inside(root, REPO / "project"), "Invalid project workspace")
    guard = _shared_module("cap_shared_runbook_guard", "core/runbook/scripts/runbook_guard.py")
    binding = guard.require_project_runbook(root)
    run_id = binding["workerJourneyId"]
    _require(isinstance(run_id, str) and run_id.isascii() and run_id.isdecimal()
             and int(run_id) > 0, "Project Run Book identity must be a positive decimal")
    directory = root / "config"
    path = directory / "cap-data-loader.properties"
    _require(not directory.is_symlink() and not path.is_symlink()
             and _inside(path, root), "Project run configuration must not be redirected")
    expected = ("# CAP project Run Book; no authentication values.\nrunID=" + run_id + "\n").encode()
    if create and not path.exists():
        directory.mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as stream:
            stream.write(expected)
            stream.flush()
            os.fsync(stream.fileno())
    _require(path.is_file() and path.read_bytes() == expected,
             "Project run configuration is missing or differs from its active binding; do not overwrite it")
    return path


def _project_context(project_root, evidence, loader, *, run_config_path=None):
    root = Path(project_root).resolve(strict=True)
    _require(_inside(root, REPO / "project"), "Selected project must be inside the repository project workspace")
    state_path = root / "state/project-state.json"
    state = _json(state_path)
    control = state.get("runbook_control", {})
    _require(control.get("status") == "active", "Project Run Book is not active")
    guard = _shared_module("cap_shared_runbook_guard", "core/runbook/scripts/runbook_guard.py")
    shared_binding = guard.require_project_runbook(root)
    # CAP evidence stays in the established project artifact, not an extension
    # of the centrally owned runbook_control schema.
    binding_path = (root / "artifacts/core/runbook/current/active-runbook-binding.json").resolve()
    _require(_inside(binding_path, root), "Run Book binding must belong to the selected project")
    binding = _json(binding_path)
    config = loader.read_config(REPO / "core/auth/fusionEnv.properties")
    selected_run_config = run_config_path or REPO / "core/data-loader/config/env.properties"
    if run_config_path is not None:
        _require(Path(run_config_path) == project_run_config(root), "Unexpected project run configuration")
    run_id = loader.metadata.read_run_id(selected_run_config)
    _require(shared_binding["workerJourneyId"] == run_id
             and shared_binding["serverUrl"] == guard.server_identity(config.get("host")),
             "Shared Run Book identity or server differs from the configured target")
    validation.verify_environment(evidence, config, run_id)
    _require(binding.get("status") == "active" and binding.get("returned_identity_matches_runID") is True,
             "Active Run Book identity has not been verified")
    _require(isinstance(run_id, str) and binding.get("identity_sha256") == hashlib.sha256(run_id.encode()).hexdigest(),
             "Configured Run Book identity differs from the project binding")
    _require(config.get("environment") == binding.get("environment")
             and binding.get("host") == urlsplit(config["host"]).hostname,
             "Run Book environment differs from the configured target")
    _require(binding.get("task_name") == cap_workflow.TASK
             and binding.get("task_type") == "ORA_CHK_DATA_LOADER" and binding.get("task_count") == 1,
             "Run Book does not bind the one selected CAP Data Loader task")
    ref = evidence["runbook"].get("projectStateRef")
    _require(isinstance(ref, str) and (REPO / ref).resolve() == state_path,
             "Create evidence references a different project state")
    integrity = {"projectStateSha256": _file_digest(state_path),
                 "runbookBindingSha256": _file_digest(binding_path)}
    if run_config_path is not None:
        integrity.update(runConfigPath=str(Path(run_config_path).relative_to(root)),
                         runConfigSha256=_file_digest(run_config_path))
    return config, run_id, integrity


def _verify_evidence_refs(evidence, project_root):
    """Evidence status alone is insufficient: retain target-bound source bytes."""
    sources = {}
    for name, check in evidence["checks"].items():
        ref = check.get("evidenceRef", {})
        _require(isinstance(ref, dict) and isinstance(ref.get("path"), str),
                 name + " needs a saved evidence reference")
        path = (REPO / ref["path"]).resolve()
        _require(_inside(path, project_root) and path.is_file() and path.stat().st_size > 0,
                 name + " evidence must be a nonempty file in the selected project")
        _require(ref.get("sha256") == _file_digest(path), name + " evidence file changed")
        _require(ref.get("environment") == evidence["environment"]["name"]
                 and ref.get("host") == evidence["environment"]["host"],
                 name + " evidence target differs")
        sources[name] = ref
    return sources


def _create_trace(task, passed):
    """Follow the source graph, not the retrieval graph or resource ordering."""
    nodes = {node["id"]: node for node in task["nodes"]}
    current = task["start_node"]
    trace = []
    for expected in CREATE_NODES:
        _require(current == expected and current in nodes, "Source graph does not declare the bounded create-preparation route")
        node = nodes[current]
        _require(all(item in passed for item in node.get("prerequisites", [])), "Create node prerequisite was not evaluated")
        outcome = "prepare" if current == "CAP-SELECT" else "passed"
        trace.append({"node": current, "outcome": "stop_for_approval" if current == CREATE_NODES[-1] else outcome})
        if current == CREATE_NODES[-1]:
            _require(node["action_type"] == "terminal", "Create preparation must end at a terminal node")
            break
        _require(current in passed, "Create node was not evaluated")
        current = node["transitions"].get(outcome)
    return trace


def _run_preflight(source, envelope, timeout, *, run_config_path=None):
    command = [sys.executable, str(REPO / "core/data-loader/scripts/upload_and_initiate.py"),
               str(source), "--task-routed", "--preflight-envelope-output", str(envelope),
               "--token-cache", str(Path("auto"))]
    if run_config_path is not None:
        command.extend(["--run-config", str(run_config_path)])
    try:
        result = subprocess.run(command, cwd=REPO, capture_output=True, text=True,
                                timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise PreparationBlocked("Shared read-only Data Loader preflight timed out; no approval or submission requested") from exc
    # Core's normal approval-required preflight exits 1. Do not parse untrusted
    # stdout as readiness or echo potentially sensitive helper diagnostics.
    _require(result.returncode == 1 and envelope.is_file(),
             "Shared source/schema preflight did not produce its immutable envelope; inspect shared read-only diagnostics")


def _save_new(path, value):
    encoded = (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    with Path(path).open("xb") as stream:
        os.chmod(path, 0o600)
        stream.write(encoded)
    _require(Path(path).read_bytes() == encoded, "Preparation artifact readback failed")


def prepare_create(*, source_path, evidence_path, task_context_path, project_root,
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
    validation.validate_evidence(evidence, validation.CONTRACT, fingerprint)
    references = _verify_evidence_refs(evidence, project)
    loader, hook = shared_loader(), shared_hook()
    run_config = project_run_config(project, create=True)
    config, run_id, project_binding = _project_context(project, evidence, loader, run_config_path=run_config)
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
    context_digest, evidence_digest, source_digest = map(_file_digest, (context, evidence_path, source))
    # Reject wrong operations/extra rows/children before even read-only metadata.
    validation.validate_archive(loader.prepare_archive(source).content, validation.CONTRACT, evidence)
    source_plan = cap_workflow.shared_plan()
    _create_trace(source_plan["task"], set(CREATE_NODES[:-1]))
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
    _run_preflight(staged_source, envelope, timeout, run_config_path=run_config)
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
    trace = _create_trace(source_plan["task"], set(CREATE_NODES[:-1]))
    executed = set(CREATE_NODES[:-1])
    results = []
    privilege_notice = ("Write grants are not independently verified. Shared authenticated "
                        "read-only preflight completed; Fusion enforces UCM upload and loader "
                        "authorization during the exact approved load. Stop on rejection; no permission probe.")
    assessed_privileges = evidence["checks"]["privileges"]["status"] == "assessed"
    for resource in plan["taskValidation"]["ruleResources"]:
        covered = [node["id"] for node in resource["nodes"] if node["id"] in executed]
        issues = ([{"severity": "info", "message": "Evaluated create nodes: " + ", ".join(covered)}]
                  if covered else [])
        if assessed_privileges and "CAP-CREATE-EVIDENCE" in covered:
            issues.append({"severity": "warning", "message": privilege_notice})
        results.append({"source": resource["file"], "status": "passed" if covered else "not_applicable",
                        "issues": issues, "changes": []})
    final_data = {**prepared["binding"], "validationPurpose": "create_preparation_only",
                  "visibilityReview": cap_visibility.review(evidence["intendedFields"]["visibility"]),
                  "writeEligible": False, "createEvidence": evidence, "evidenceReferences": references,
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
        new_config, new_run_id, new_binding = _project_context(project, evidence, loader, run_config_path=run_config)
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
    preview_path = destination / "cap-create-preview.json"
    _save_new(preview_path, retained)
    return {"status": "awaiting_exact_load_approval", "write_eligible": False,
            "operation": "create", "archiveSha256": preflight["archiveSha256"],
            "archivePath": str(artifact), "previewPath": str(preview_path),
            "sharedPreflightPath": str(envelope), "previewSha256": retained["previewSha256"],
            "warnings": [privilege_notice] if assessed_privileges else [],
            "rowCount": 1, "side_effects": ["local preparation artifacts", "shared read-only metadata checks"]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source", "evidence", "task-context", "project-root", "output-dir"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args(argv)
    try:
        result = prepare_create(source_path=args.source, evidence_path=args.evidence,
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
