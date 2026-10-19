#!/usr/bin/env python3
"""Run one explicitly authorized, test-only Item Catalog FSM batch.

The runner is pillar-local orchestration. It never implements OAuth, UCM upload,
Data Loader initiation, or Data Loader status REST itself. It invokes the public
Core Data Loader CLIs as separate steps, persists sanitized project-local state,
and advances only after the Item Catalog skill supplies an exact verification
receipt for the preceding load.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import time
from typing import Any, Callable, Mapping, Sequence
import zipfile


SCHEMA_VERSION = "1.0"
MODE = "test-only-item-catalog-fsm-composite"
TASK_CODE = "ORA_MANAGE_PROFILE_ITEM_CATALOG"
VERIFICATION_ROUTE = (
    "hcm.hcm-tool.profile-management-content-library-configuration.item-catalogs"
)
PROVIDER_REGISTRY_PATH = (
    Path(__file__).resolve().parents[1]
    / "item-catalogs/references/catalog-content-item-fsm-provider.json"
)
FSM_METADATA_MEMBER = "ASM_SETUP_CSV_METADATA.xml"
ITEM_CATALOG_MEMBERS = {
    FSM_METADATA_MEMBER,
    "ORA_TALENT_PROFILE_ITEM_CATALOG.csv",
    "ORA_TALENT_CATALOG_CONTENT_ITEM.csv",
    "ORA_TALENT_CATALOG_CONTENT_ITEM_RDESC.csv",
}
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
SAFE_ID_PATTERN = re.compile(r"[a-z0-9][a-z0-9-]{2,79}")
SAFE_CODE_PATTERN = re.compile(r"[A-Z][A-Z0-9_]{1,127}")
RELEASE_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._ -]{0,63}")
REQUEST_ID_PATTERN = re.compile(
    r"^\|\s*Request ID\s*\|\s*([1-9][0-9]*)\s*\|\s*$", re.MULTILINE
)
STATUS_ROW_PATTERN = re.compile(
    r"^\|\s*(?!Data Set\s*\|)([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*"
    r"([0-9]+)\s*\|\s*([0-9]+)\s*\|\s*([0-9]+)\s*\|\s*$",
    re.MULTILINE,
)
FAILURE_STATUS_MARKERS = ("ERROR", "FAIL", "CANCEL", "REJECT")
SUCCESS_STATUS_MARKERS = ("SUCCESS", "SUCCEEDED", "COMPLETE", "COMPLETED")
FAILURE_CLASSES = {
    "input_validation",
    "catalog_mismatch",
    "auth_authz",
    "transport_environment",
    "fusion_api",
    "process_timeout",
    "process_failed",
    "artifact_persistence",
    "approval_blocker",
}
REQUIRED_AUTHORIZATION = {
    "auto_approve": True,
    "monitor_to_terminal": True,
    "domain_verification_required": True,
    "fail_fast": True,
    "retry_mutations": False,
    "auto_correct": False,
    "provider_promotion": False,
}
EXPECTED_COUNTS = {"total": 1, "loaded": 1, "failed": 0}
PROJECT_STATUSES = {"initialized", "in_progress", "blocked", "ready_for_review"}
LOAD_BASE_FIELDS = (
    "sequence",
    "load_id",
    "context_name",
    "proposal_fingerprint",
    "provider_rows_fingerprint",
    "expected_counts",
)
LOAD_EXECUTION_FIELDS = (
    "source_path",
    "source_sha256",
    "task_validation_envelope_path",
    "task_validation_envelope_sha256",
)
MANIFEST_BASE_FIELDS = (
    "schema_version",
    "mode",
    "batch_id",
    "target_environment",
    "environment_classification",
    "fusion_release",
    "operation",
    "source_type",
    "task_code",
    "provider_registry_sha256",
    "authorization",
    "polling",
    "state_path",
    "diagnostic_output_dir",
)


class TestBatchError(ValueError):
    """The guarded test-batch contract was not satisfied."""

    def __init__(self, failure_class: str, message: str) -> None:
        super().__init__(message)
        self.failure_class = failure_class
        self.message = message


CommandRunner = Callable[[Sequence[str], Path, int], subprocess.CompletedProcess[str]]
Clock = Callable[[], float]
Sleeper = Callable[[float], None]


def _repository_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "core/data-loader/scripts/upload_and_initiate.py").is_file():
            return candidate
    raise TestBatchError("input_validation", "Repository root could not be resolved.")


def _resolve_repository_token_cache(
    supplied_path: Path | None, repository_root: Path
) -> Path:
    """Defer managed profile resolution to shared auth; disallow checkout caches."""
    if supplied_path is None or str(supplied_path) == "auto":
        return Path("auto")
    selected = Path(os.path.abspath(supplied_path.expanduser()))
    if selected.is_relative_to(repository_root.resolve()) or selected.resolve().is_relative_to(repository_root.resolve()):
        raise TestBatchError("input_validation", "Token caches must be outside the repository.")
    # Shared authentication checks owner, mode and every component without following links.
    return selected


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _canonical_json(value: Any) -> bytes:
    try:
        rendered = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as error:
        raise TestBatchError(
            "input_validation", "Batch data must be finite JSON-compatible data."
        ) from error
    return rendered.encode("utf-8")


def _sha256_value(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as source:
            for block in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as error:
        raise TestBatchError("artifact_persistence", f"File could not be read: {path}") from error
    return digest.hexdigest()


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise TestBatchError("artifact_persistence", f"{label} could not be read: {path}") from error
    except json.JSONDecodeError as error:
        raise TestBatchError("input_validation", f"{label} is not valid JSON: {error.msg}.") from error
    if not isinstance(value, dict):
        raise TestBatchError("input_validation", f"{label} must be a JSON object.")
    return value


def _require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TestBatchError("input_validation", f"{label} must be non-empty text.")
    return value.strip()


def _require_sha256(value: Any, label: str) -> str:
    rendered = _require_text(value, label).lower()
    if not SHA256_PATTERN.fullmatch(rendered):
        raise TestBatchError("input_validation", f"{label} must be a lowercase SHA-256 value.")
    return rendered


def _require_integer(value: Any, label: str, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
        raise TestBatchError(
            "input_validation", f"{label} must be an integer from {minimum} through {maximum}."
        )
    return value


def _inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _project_root(path: Path) -> Path:
    try:
        root = path.resolve(strict=True)
    except OSError as error:
        raise TestBatchError("artifact_persistence", f"Project root is unavailable: {path}") from error
    state_path = root / "state/project-state.json"
    state = _read_json(state_path, "project state")
    if state.get("status") not in PROJECT_STATUSES:
        raise TestBatchError("input_validation", "Project workspace is not initialized.")
    return root


def _project_path(
    root: Path, supplied: Any, label: str, *, must_exist: bool = False, directory: bool = False
) -> Path:
    raw = Path(_require_text(supplied, label))
    if raw.is_absolute():
        raise TestBatchError("input_validation", f"{label} must be relative to project root.")
    resolved = (root / raw).resolve()
    if not _inside(resolved, root):
        raise TestBatchError("input_validation", f"{label} resolves outside project root.")
    if must_exist and (not resolved.is_dir() if directory else not resolved.is_file()):
        kind = "directory" if directory else "file"
        raise TestBatchError("artifact_persistence", f"{label} does not identify an existing {kind}.")
    return resolved


def _validate_exact_keys(value: Mapping[str, Any], allowed: set[str], label: str) -> None:
    extra = sorted(set(value) - allowed)
    if extra:
        raise TestBatchError("input_validation", f"{label} contains unsupported fields: {', '.join(extra)}.")


NON_PRODUCTION_ENVIRONMENT_MARKERS = frozenset(
    {"BRONZE", "DEV", "DEVELOPMENT", "QA", "SANDBOX", "STAGE", "STAGING", "TEST", "TESTING", "UAT"}
)
PRODUCTION_ENVIRONMENT_MARKERS = frozenset({"LIVE", "PRD", "PROD", "PRODUCTION"})


def _environment_markers(environment: str) -> set[str]:
    return set(re.findall(r"[A-Z]+", environment.upper()))


def _is_explicit_test_environment(environment: str) -> bool:
    markers = _environment_markers(environment)
    return bool(markers & NON_PRODUCTION_ENVIRONMENT_MARKERS) and not bool(
        markers & PRODUCTION_ENVIRONMENT_MARKERS
    )


def _authorization_material(manifest: Mapping[str, Any]) -> dict[str, Any]:
    material = {field: manifest.get(field) for field in MANIFEST_BASE_FIELDS}
    material["loads"] = [
        {field: load.get(field) for field in LOAD_BASE_FIELDS}
        for load in manifest.get("loads", [])
        if isinstance(load, Mapping)
    ]
    return material


def _execution_material(manifest: Mapping[str, Any]) -> dict[str, Any]:
    material = _authorization_material(manifest)
    material["loads"] = [
        {field: load.get(field) for field in LOAD_BASE_FIELDS + LOAD_EXECUTION_FIELDS}
        for load in manifest.get("loads", [])
        if isinstance(load, Mapping)
    ]
    return material


def authorization_fingerprint(manifest: Mapping[str, Any]) -> str:
    return _sha256_value(_authorization_material(manifest))


def execution_fingerprint(manifest: Mapping[str, Any]) -> str:
    return _sha256_value(_execution_material(manifest))


def _validate_fsm_archive(path: Path) -> None:
    try:
        with zipfile.ZipFile(path) as archive:
            basenames = [Path(name).name for name in archive.namelist() if not name.endswith("/")]
            if basenames.count(FSM_METADATA_MEMBER) != 1 or set(basenames) != ITEM_CATALOG_MEMBERS:
                raise TestBatchError(
                    "catalog_mismatch",
                    f"{path.name} must contain exactly the four Item Catalog FSM members.",
                )
            if len(basenames) != len(set(basenames)):
                raise TestBatchError("catalog_mismatch", f"{path.name} contains duplicate member basenames.")
    except (OSError, zipfile.BadZipFile) as error:
        raise TestBatchError("catalog_mismatch", f"{path.name} is not a valid FSM ZIP.") from error


def _validate_task_envelope(
    path: Path,
    source_sha256: str,
    task_code: str,
    proposal_fingerprint: str,
    provider_rows_fingerprint: str,
) -> None:
    envelope = _read_json(path, "Task Validation envelope")
    _validate_exact_keys(envelope, {"preview", "approval"}, "Task Validation envelope")
    preview = envelope.get("preview")
    approval = envelope.get("approval")
    if not isinstance(preview, dict) or not isinstance(approval, dict):
        raise TestBatchError("approval_blocker", "Task Validation envelope is incomplete.")
    final_data = preview.get("finalData")
    if (
        preview.get("executionRoute") != "data-loader"
        or preview.get("taskCode") != task_code
        or not isinstance(final_data, dict)
        or str(final_data.get("archiveSha256") or "").lower() != source_sha256
        or final_data.get("proposalFingerprint") != proposal_fingerprint
        or final_data.get("providerRowsFingerprint") != provider_rows_fingerprint
        or final_data.get("sourceType") != "FSM"
        or final_data.get("operation") != "create"
    ):
        raise TestBatchError(
            "approval_blocker",
            "Task Validation preview does not bind the exact approved FSM package inputs.",
        )
    if (
        approval.get("approved") is not True
        or approval.get("executionRoute") != "data-loader"
        or approval.get("taskCode") != task_code
    ):
        raise TestBatchError("approval_blocker", "Task Validation approval does not match the preview.")


def _registered_contexts(expected_sha256: str, fusion_release: str) -> set[str]:
    if _sha256_file(PROVIDER_REGISTRY_PATH) != expected_sha256:
        raise TestBatchError("approval_blocker", "Item Catalog FSM provider registry SHA-256 changed.")
    registry = _read_json(PROVIDER_REGISTRY_PATH, "Item Catalog FSM provider registry")
    if (
        registry.get("schema_version") != SCHEMA_VERSION
        or registry.get("task_code") != TASK_CODE
    ):
        raise TestBatchError(
            "catalog_mismatch",
            "Item Catalog FSM provider registry does not match the task.",
        )
    providers = registry.get("providers")
    if not isinstance(providers, list) or not providers:
        raise TestBatchError("catalog_mismatch", "Item Catalog FSM provider registry is empty.")
    contexts: set[str] = set()
    for provider in providers:
        if not isinstance(provider, dict):
            raise TestBatchError("catalog_mismatch", "Item Catalog FSM provider entry is invalid.")
        context = _require_text(provider.get("context_name"), "provider context_name").upper()
        if (
            not SAFE_CODE_PATTERN.fullmatch(context)
            or context in contexts
            or provider.get("lifecycle") not in {"certification-only", "verified"}
        ):
            raise TestBatchError(
                "catalog_mismatch", "Item Catalog FSM provider registry has an ineligible entry."
            )
        contexts.add(context)
    return contexts


def validate_manifest(
    manifest: Mapping[str, Any],
    project_root: Path,
    *,
    require_execution: bool,
    verify_fingerprints: bool = True,
) -> dict[str, Any]:
    allowed_top = set(MANIFEST_BASE_FIELDS) | {
        "manifest_stage",
        "loads",
        "authorization_fingerprint",
        "execution_fingerprint",
    }
    _validate_exact_keys(manifest, allowed_top, "batch manifest")
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise TestBatchError("input_validation", "Unsupported batch schema_version.")
    if manifest.get("manifest_stage") not in {"authorization", "execution"}:
        raise TestBatchError("input_validation", "manifest_stage must be authorization or execution.")
    if require_execution and manifest.get("manifest_stage") != "execution":
        raise TestBatchError("input_validation", "Execution requires an execution-stage manifest.")
    if manifest.get("mode") != MODE:
        raise TestBatchError("input_validation", "The manifest is not a test-only Item Catalog FSM batch.")
    batch_id = _require_text(manifest.get("batch_id"), "batch_id")
    if not SAFE_ID_PATTERN.fullmatch(batch_id):
        raise TestBatchError("input_validation", "batch_id must use lowercase kebab-case.")
    target = _require_text(manifest.get("target_environment"), "target_environment").upper()
    if not SAFE_CODE_PATTERN.fullmatch(target) or not _is_explicit_test_environment(target):
        raise TestBatchError(
            "input_validation",
            "Target must be an exact environment alias with an approved non-production marker.",
        )
    if manifest.get("environment_classification") != "test":
        raise TestBatchError("input_validation", "Only a target explicitly classified as test is supported.")
    release = _require_text(manifest.get("fusion_release"), "fusion_release")
    if not RELEASE_PATTERN.fullmatch(release):
        raise TestBatchError("input_validation", "fusion_release must be safe informational text or unknown.")
    if manifest.get("operation") != "create" or manifest.get("source_type") != "FSM":
        raise TestBatchError("input_validation", "Only create-only FSM loads are supported.")
    if manifest.get("task_code") != TASK_CODE:
        raise TestBatchError("input_validation", f"Only task {TASK_CODE} is supported.")
    provider_registry_sha256 = _require_sha256(
        manifest.get("provider_registry_sha256"), "provider_registry_sha256"
    )
    registered_contexts = _registered_contexts(provider_registry_sha256, release)
    authorization = manifest.get("authorization")
    if not isinstance(authorization, dict) or authorization != REQUIRED_AUTHORIZATION:
        raise TestBatchError("approval_blocker", "The test-batch safety authorization is incomplete or changed.")
    polling = manifest.get("polling")
    if not isinstance(polling, dict):
        raise TestBatchError("input_validation", "polling must be an object.")
    _validate_exact_keys(
        polling,
        {"interval_seconds", "load_timeout_seconds", "helper_timeout_seconds"},
        "polling",
    )
    interval = _require_integer(polling.get("interval_seconds"), "interval_seconds", 1, 300)
    timeout = _require_integer(polling.get("load_timeout_seconds"), "load_timeout_seconds", 1, 86400)
    helper_timeout = _require_integer(
        polling.get("helper_timeout_seconds"), "helper_timeout_seconds", 30, 1800
    )
    if timeout < interval:
        raise TestBatchError("input_validation", "load_timeout_seconds must not be shorter than the poll interval.")
    state_path = _project_path(project_root, manifest.get("state_path"), "state_path")
    diagnostic_dir = _project_path(
        project_root, manifest.get("diagnostic_output_dir"), "diagnostic_output_dir"
    )
    loads = manifest.get("loads")
    if not isinstance(loads, list) or not 1 <= len(loads) <= 50:
        raise TestBatchError("input_validation", "loads must contain from one through fifty entries.")
    allowed_load = set(LOAD_BASE_FIELDS + LOAD_EXECUTION_FIELDS)
    normalized_loads: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_contexts: set[str] = set()
    for expected_sequence, raw_load in enumerate(loads, start=1):
        if not isinstance(raw_load, dict):
            raise TestBatchError("input_validation", "Every load must be an object.")
        _validate_exact_keys(raw_load, allowed_load, f"load {expected_sequence}")
        if raw_load.get("sequence") != expected_sequence:
            raise TestBatchError("input_validation", "Load sequences must be consecutive and ordered from one.")
        load_id = _require_text(raw_load.get("load_id"), "load_id")
        if not SAFE_ID_PATTERN.fullmatch(load_id) or load_id in seen_ids:
            raise TestBatchError("input_validation", "load_id values must be unique lowercase kebab-case.")
        seen_ids.add(load_id)
        context = _require_text(raw_load.get("context_name"), "context_name").upper()
        if not SAFE_CODE_PATTERN.fullmatch(context) or context in seen_contexts:
            raise TestBatchError("input_validation", "context_name values must be unique uppercase codes.")
        if context not in registered_contexts:
            raise TestBatchError(
                "catalog_mismatch",
                f"{context} is not registered for Item Catalog FSM controlled certification.",
            )
        seen_contexts.add(context)
        proposal = _require_sha256(raw_load.get("proposal_fingerprint"), "proposal_fingerprint")
        provider = _require_sha256(
            raw_load.get("provider_rows_fingerprint"), "provider_rows_fingerprint"
        )
        if raw_load.get("expected_counts") != EXPECTED_COUNTS:
            raise TestBatchError(
                "input_validation",
                "Every canary must expect exactly one created business child and zero failed rows.",
            )
        normalized: dict[str, Any] = {
            "sequence": expected_sequence,
            "load_id": load_id,
            "context_name": context,
            "proposal_fingerprint": proposal,
            "provider_rows_fingerprint": provider,
            "expected_counts": dict(EXPECTED_COUNTS),
        }
        execution_fields_present = any(field in raw_load for field in LOAD_EXECUTION_FIELDS)
        if require_execution or manifest.get("manifest_stage") == "execution" or execution_fields_present:
            if not all(field in raw_load for field in LOAD_EXECUTION_FIELDS):
                raise TestBatchError("input_validation", f"{load_id} is missing execution artifact fields.")
            source_path = _project_path(
                project_root, raw_load.get("source_path"), f"{load_id}.source_path", must_exist=True
            )
            if source_path.suffix.lower() != ".zip":
                raise TestBatchError("input_validation", f"{load_id} source must be a ZIP.")
            source_sha = _require_sha256(raw_load.get("source_sha256"), f"{load_id}.source_sha256")
            if _sha256_file(source_path) != source_sha:
                raise TestBatchError("approval_blocker", f"{load_id} source SHA-256 changed.")
            _validate_fsm_archive(source_path)
            envelope_path = _project_path(
                project_root,
                raw_load.get("task_validation_envelope_path"),
                f"{load_id}.task_validation_envelope_path",
                must_exist=True,
            )
            envelope_sha = _require_sha256(
                raw_load.get("task_validation_envelope_sha256"),
                f"{load_id}.task_validation_envelope_sha256",
            )
            if _sha256_file(envelope_path) != envelope_sha:
                raise TestBatchError("approval_blocker", f"{load_id} Task Validation envelope changed.")
            _validate_task_envelope(
                envelope_path,
                source_sha,
                TASK_CODE,
                proposal,
                provider,
            )
            normalized.update(
                {
                    "source_path": str(source_path),
                    "source_relative": str(source_path.relative_to(project_root)),
                    "source_sha256": source_sha,
                    "task_validation_envelope_path": str(envelope_path),
                    "task_validation_envelope_relative": str(envelope_path.relative_to(project_root)),
                    "task_validation_envelope_sha256": envelope_sha,
                }
            )
        normalized_loads.append(normalized)
    expected_authorization = authorization_fingerprint(manifest)
    if verify_fingerprints:
        supplied_authorization = _require_sha256(
            manifest.get("authorization_fingerprint"), "authorization_fingerprint"
        )
        if supplied_authorization != expected_authorization:
            raise TestBatchError("approval_blocker", "authorization_fingerprint does not match the exact batch inputs.")
    expected_execution: str | None = None
    if require_execution or manifest.get("manifest_stage") == "execution":
        expected_execution = execution_fingerprint(manifest)
        if verify_fingerprints:
            supplied_execution = _require_sha256(
                manifest.get("execution_fingerprint"), "execution_fingerprint"
            )
            if supplied_execution != expected_execution:
                raise TestBatchError("approval_blocker", "execution_fingerprint does not match the exact package inputs.")
    return {
        "batch_id": batch_id,
        "target_environment": target,
        "fusion_release": release,
        "provider_registry_sha256": provider_registry_sha256,
        "authorization_fingerprint": expected_authorization,
        "execution_fingerprint": expected_execution,
        "polling": {
            "interval_seconds": interval,
            "load_timeout_seconds": timeout,
            "helper_timeout_seconds": helper_timeout,
        },
        "state_path": state_path,
        "diagnostic_output_dir": diagnostic_dir,
        "loads": normalized_loads,
    }


def _read_configured_environment(properties_path: Path) -> str:
    try:
        lines = properties_path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise TestBatchError("artifact_persistence", "Fusion properties file could not be read.") from error
    values: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", ";")) or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key.strip() == "environment" and value.strip():
            values.append(value.strip().upper())
    if len(values) != 1:
        raise TestBatchError("input_validation", "Fusion properties must contain one exact environment alias.")
    return values[0]


def _atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp-{os.getpid()}")
    if temporary.exists():
        raise TestBatchError("artifact_persistence", f"Temporary state path already exists: {temporary}")
    try:
        with temporary.open("xb") as destination:
            destination.write(json.dumps(value, indent=2, sort_keys=True).encode("utf-8") + b"\n")
        os.chmod(temporary, 0o600)
        temporary.replace(path)
    except OSError as error:
        raise TestBatchError("artifact_persistence", f"State could not be persisted: {path}") from error


def _atomic_write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp-{os.getpid()}")
    if temporary.exists():
        raise TestBatchError("artifact_persistence", f"Temporary report path already exists: {temporary}")
    try:
        with temporary.open("x", encoding="utf-8") as destination:
            destination.write(value)
        os.chmod(temporary, 0o600)
        temporary.replace(path)
    except OSError as error:
        raise TestBatchError("artifact_persistence", f"Report could not be persisted: {path}") from error


def _new_state(batch: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "ready",
        "batch_id": batch["batch_id"],
        "target_environment": batch["target_environment"],
        "fusion_release": batch["fusion_release"],
        "task_code": TASK_CODE,
        "authorization_fingerprint": batch["authorization_fingerprint"],
        "execution_fingerprint": batch["execution_fingerprint"],
        "loads": [
            {
                "sequence": load["sequence"],
                "load_id": load["load_id"],
                "context_name": load["context_name"],
                "source_sha256": load["source_sha256"],
                "status": "pending",
            }
            for load in batch["loads"]
        ],
        "errors": [],
        "updated_at": _utc_now(),
    }


def _load_or_create_state(batch: Mapping[str, Any]) -> dict[str, Any]:
    path = batch["state_path"]
    if not path.exists():
        state = _new_state(batch)
        _atomic_write_json(path, state)
        return state
    state = _read_json(path, "batch state")
    for field in (
        "batch_id",
        "target_environment",
        "fusion_release",
        "authorization_fingerprint",
        "execution_fingerprint",
    ):
        if state.get(field) != batch.get(field):
            raise TestBatchError("approval_blocker", f"Existing batch state has a different {field}.")
    state_loads = state.get("loads")
    if not isinstance(state_loads, list) or len(state_loads) != len(batch["loads"]):
        raise TestBatchError("approval_blocker", "Existing batch state has a different load set.")
    for expected, actual in zip(batch["loads"], state_loads):
        if not isinstance(actual, dict) or any(
            actual.get(field) != expected.get(field)
            for field in ("sequence", "load_id", "context_name", "source_sha256")
        ):
            raise TestBatchError("approval_blocker", "Existing batch state does not match the execution manifest.")
    return state


def _save_state(batch: Mapping[str, Any], state: dict[str, Any]) -> None:
    state["updated_at"] = _utc_now()
    _atomic_write_json(batch["state_path"], state)


def _default_command_runner(command: Sequence[str], cwd: Path, timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command),
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )


def _combined_output(result: subprocess.CompletedProcess[str]) -> str:
    parts = [value.strip() for value in (result.stdout, result.stderr) if value and value.strip()]
    return "\n\n".join(parts) + ("\n" if parts else "")


def _sanitize_core_output(output: str, token_cache_path: Path) -> str:
    """Prevent the local cache location from entering project diagnostics."""
    if str(token_cache_path) == "auto":
        return re.sub(r"Saved access token cache in [^\n]+", "Saved access token cache in <managed-token-cache>", output)
    candidates = {str(token_cache_path), os.path.abspath(token_cache_path)}
    sanitized = output
    for candidate in sorted(candidates, key=len, reverse=True):
        if candidate:
            sanitized = sanitized.replace(candidate, "<repository-token-cache>")
    return sanitized


def _failure_class_from_output(output: str) -> str:
    normalized = output.casefold()
    if any(token in normalized for token in ("approval", "task validation", "fingerprint", "sha-256")):
        return "approval_blocker"
    if any(token in normalized for token in ("oauth", "unauthorized", "forbidden", "401", "403")):
        return "auth_authz"
    if any(token in normalized for token in ("timeout", "connection", "transport", "certificate", "tls")):
        return "transport_environment"
    if any(token in normalized for token in ("metadata", "catalog", "member", "header")):
        return "catalog_mismatch"
    return "fusion_api"


def _add_error(state: dict[str, Any], load: Mapping[str, Any], failure_class: str, message: str) -> None:
    state.setdefault("errors", []).append(
        {
            "load_id": load["load_id"],
            "context_name": load["context_name"],
            "failure_class": failure_class,
            "message": message,
            "recorded_at": _utc_now(),
        }
    )
    state["status"] = "blocked"


def _status_outcome(markdown: str, expected: Mapping[str, int]) -> dict[str, Any]:
    rows = STATUS_ROW_PATTERN.findall(markdown)
    if not rows:
        if "Not available yet" in markdown:
            return {"state": "active", "status": "Not available yet"}
        raise TestBatchError("fusion_api", "Core Data Loader status output did not contain a recognized status table.")
    parsed = []
    for data_set, status, total, loaded, failed in rows:
        parsed.append(
            {
                "data_set": data_set.strip(),
                "status": status.strip(),
                "total": int(total),
                "loaded": int(loaded),
                "failed": int(failed),
            }
        )
    statuses = [row["status"].upper() for row in parsed]
    if any(any(marker in status for marker in FAILURE_STATUS_MARKERS) for status in statuses):
        return {"state": "failed", "rows": parsed}
    if all(any(marker in status for marker in SUCCESS_STATUS_MARKERS) for status in statuses):
        counts = {
            "total": sum(row["total"] for row in parsed),
            "loaded": sum(row["loaded"] for row in parsed),
            "failed": sum(row["failed"] for row in parsed),
        }
        complete_object_counts = all(
            row["total"] > 0
            and row["loaded"] == row["total"]
            and row["failed"] == 0
            for row in parsed
        )
        return {
            "state": "succeeded" if complete_object_counts else "count_mismatch",
            "rows": parsed,
            "counts": counts,
            "expected_business_counts": dict(expected),
        }
    return {"state": "active", "rows": parsed, "status": ", ".join(row["status"] for row in parsed)}


def _core_command_paths(repository_root: Path) -> tuple[Path, Path]:
    upload = repository_root / "core/data-loader/scripts/upload_and_initiate.py"
    status = repository_root / "core/data-loader/scripts/get_data_load_info.py"
    if not upload.is_file() or not status.is_file():
        raise TestBatchError("input_validation", "Core Data Loader CLI paths are unavailable.")
    return upload, status


def _relative_to_project(path: Path, project_root: Path) -> str:
    return str(path.relative_to(project_root))


def _apply_verification_receipt(
    batch: Mapping[str, Any], state: dict[str, Any], receipt_path: Path
) -> None:
    pending = next((item for item in state["loads"] if item.get("status") == "awaiting_verification"), None)
    if pending is None:
        raise TestBatchError("input_validation", "No load is awaiting an Item Catalog verification receipt.")
    receipt = _read_json(receipt_path, "verification receipt")
    allowed = {
        "schema_version",
        "status",
        "verification_route",
        "target_environment",
        "fusion_release",
        "task_code",
        "load_id",
        "context_name",
        "authorization_fingerprint",
        "execution_fingerprint",
        "source_sha256",
        "checks",
        "failure_class",
        "message",
    }
    _validate_exact_keys(receipt, allowed, "verification receipt")
    exact = {
        "schema_version": SCHEMA_VERSION,
        "verification_route": VERIFICATION_ROUTE,
        "target_environment": batch["target_environment"],
        "task_code": TASK_CODE,
        "load_id": pending["load_id"],
        "context_name": pending["context_name"],
        "authorization_fingerprint": batch["authorization_fingerprint"],
        "execution_fingerprint": batch["execution_fingerprint"],
        "source_sha256": pending["source_sha256"],
    }
    if any(receipt.get(field) != value for field, value in exact.items()):
        raise TestBatchError("approval_blocker", "Verification receipt does not match the active load.")
    status = receipt.get("status")
    if status == "verified":
        expected_checks = {
            "direct_child_readback": "passed",
            "parent_no_drift": "passed",
            "full_item_catalog_export": "passed",
            "duplicate_rerun_block": "passed",
        }
        if receipt.get("checks") != expected_checks:
            raise TestBatchError("catalog_mismatch", "Verification receipt is missing a required passed check.")
        pending["status"] = "verified"
        pending["verification_receipt_path"] = _relative_to_project(receipt_path, batch["project_root"])
        state["status"] = "running"
        _save_state(batch, state)
        return
    if status == "blocked":
        failure_class = receipt.get("failure_class")
        message = receipt.get("message")
        if failure_class not in FAILURE_CLASSES or not isinstance(message, str) or not message.strip():
            raise TestBatchError("input_validation", "Blocked verification receipt is incomplete.")
        pending["status"] = "blocked"
        pending["verification_receipt_path"] = _relative_to_project(receipt_path, batch["project_root"])
        _add_error(state, pending, failure_class, message.strip())
        _save_state(batch, state)
        return
    raise TestBatchError("input_validation", "Verification receipt status must be verified or blocked.")


def execute_next(
    batch: dict[str, Any],
    *,
    approved_authorization_fingerprint: str,
    properties_path: Path,
    token_cache_path: Path,
    run_config_path: Path | None = None,
    verification_receipt: Path | None = None,
    command_runner: CommandRunner = _default_command_runner,
    clock: Clock = time.monotonic,
    sleeper: Sleeper = time.sleep,
) -> tuple[dict[str, Any], int]:
    approved = _require_sha256(
        approved_authorization_fingerprint, "approved_authorization_fingerprint"
    )
    if approved != batch["authorization_fingerprint"]:
        raise TestBatchError("approval_blocker", "Execution authorization does not match this exact batch.")
    configured_environment = _read_configured_environment(properties_path)
    if configured_environment != batch["target_environment"]:
        raise TestBatchError(
            "transport_environment",
            "Configured Fusion environment does not match the approved test target.",
        )
    state = _load_or_create_state(batch)
    if verification_receipt is not None:
        receipt_path = _project_path(
            batch["project_root"],
            str(verification_receipt),
            "verification_receipt",
            must_exist=True,
        )
        _apply_verification_receipt(batch, state, receipt_path)
    if state.get("status") == "blocked":
        return state, 1
    awaiting = next((item for item in state["loads"] if item.get("status") == "awaiting_verification"), None)
    if awaiting is not None:
        state["status"] = "awaiting_verification"
        _save_state(batch, state)
        return state, 2
    current = next((item for item in state["loads"] if item.get("status") != "verified"), None)
    if current is None:
        state["status"] = "completed"
        _save_state(batch, state)
        return state, 0
    if current.get("status") in {"submitting", "submission_unknown"}:
        current["status"] = "submission_unknown"
        _add_error(
            state,
            current,
            "fusion_api",
            "A prior submission did not persist an accepted Request ID; reconcile it before any retry.",
        )
        _save_state(batch, state)
        return state, 1
    manifest_load = next(load for load in batch["loads"] if load["load_id"] == current["load_id"])
    repository_root = _repository_root()
    upload_cli, status_cli = _core_command_paths(repository_root)
    diagnostic_dir = batch["diagnostic_output_dir"] / current["load_id"]
    diagnostic_dir.mkdir(parents=True, exist_ok=True)
    helper_timeout = batch["polling"]["helper_timeout_seconds"]
    if current.get("status") == "pending":
        current["status"] = "submitting"
        state["status"] = "running"
        _save_state(batch, state)
        command = [
            sys.executable,
            str(upload_cli),
            manifest_load["source_path"],
            "--properties",
            str(properties_path),
            "--token-cache",
            str(token_cache_path),
            "--project-root",
            str(batch["project_root"]),
            "--task-routed",
            "--task-validation-envelope",
            manifest_load["task_validation_envelope_path"],
            "--approve-upload",
        ]
        if run_config_path is not None:
            command.extend(("--run-config", str(run_config_path)))
        try:
            result = command_runner(command, repository_root, helper_timeout)
        except subprocess.TimeoutExpired:
            current["status"] = "submission_unknown"
            _add_error(
                state,
                current,
                "transport_environment",
                "Core Data Loader initiation timed out with an unknown remote outcome; no retry was made.",
            )
            _save_state(batch, state)
            return state, 1
        output = _combined_output(result)
        report_path = diagnostic_dir / "initiation.md"
        _atomic_write_text(
            report_path,
            _sanitize_core_output(output, token_cache_path)
            or "Core Data Loader returned no report.\n",
        )
        request_match = REQUEST_ID_PATTERN.search(output)
        if request_match is None:
            current["status"] = "submission_unknown" if result.returncode == 0 else "blocked"
            _add_error(
                state,
                current,
                _failure_class_from_output(output),
                "Core Data Loader did not return an accepted Request ID; no retry was made.",
            )
            current["initiation_report_path"] = _relative_to_project(report_path, batch["project_root"])
            _save_state(batch, state)
            return state, 1
        current["request_id"] = request_match.group(1)
        current["initiation_report_path"] = _relative_to_project(report_path, batch["project_root"])
        current["status"] = "monitoring"
        _save_state(batch, state)
    if current.get("status") != "monitoring" or not current.get("request_id"):
        raise TestBatchError("input_validation", "Active load state cannot safely continue.")
    start = clock()
    timeout = batch["polling"]["load_timeout_seconds"]
    interval = batch["polling"]["interval_seconds"]
    while True:
        status_command = [
            sys.executable,
            str(status_cli),
            str(current["request_id"]),
            "--status-only",
            "--properties",
            str(properties_path),
            "--token-cache",
            str(token_cache_path),
            "--diagnostic-log-output-dir",
            str(diagnostic_dir),
        ]
        try:
            result = command_runner(status_command, repository_root, helper_timeout)
        except subprocess.TimeoutExpired:
            current["status"] = "blocked"
            _add_error(state, current, "transport_environment", "A read-only status request timed out.")
            _save_state(batch, state)
            return state, 1
        output = _combined_output(result)
        status_report = diagnostic_dir / "status-latest.md"
        _atomic_write_text(
            status_report,
            _sanitize_core_output(output, token_cache_path)
            or "Core Data Loader returned no status report.\n",
        )
        if result.returncode != 0:
            current["status"] = "blocked"
            _add_error(state, current, _failure_class_from_output(output), "Data Loader status inspection failed.")
            current["status_report_path"] = _relative_to_project(status_report, batch["project_root"])
            _save_state(batch, state)
            return state, 1
        try:
            outcome = _status_outcome(output, manifest_load["expected_counts"])
        except TestBatchError as error:
            current["status"] = "blocked"
            _add_error(state, current, error.failure_class, error.message)
            current["status_report_path"] = _relative_to_project(status_report, batch["project_root"])
            _save_state(batch, state)
            return state, 1
        current["last_status"] = outcome.get("status") or outcome.get("state")
        current["status_report_path"] = _relative_to_project(status_report, batch["project_root"])
        if outcome["state"] == "succeeded":
            current["status"] = "awaiting_verification"
            current["counts"] = outcome["counts"]
            state["status"] = "awaiting_verification"
            _save_state(batch, state)
            return state, 2
        if outcome["state"] in {"failed", "count_mismatch"}:
            current["status"] = "failed"
            if "counts" in outcome:
                current["counts"] = outcome["counts"]
            _add_error(
                state,
                current,
                "process_failed",
                "Data Loader failed or returned zero, incomplete, or error-bearing FSM object counts.",
            )
            _save_state(batch, state)
            return state, 1
        elapsed = clock() - start
        current["elapsed_seconds"] = int(elapsed)
        _save_state(batch, state)
        if elapsed >= timeout:
            current["status"] = "timed_out"
            _add_error(
                state,
                current,
                "process_timeout",
                "Data Loader did not reach a terminal status within the approved polling window; no retry was made.",
            )
            _save_state(batch, state)
            return state, 1
        sleeper(interval)


def _render_result(state: Mapping[str, Any], state_path: Path) -> str:
    lines = ["## Item Catalog FSM test batch", "", f"Batch status: `{state.get('status')}`", ""]
    lines.extend(
        [
            "| Order | Context | State | Request ID |",
            "|---:|---|---|---|",
        ]
    )
    for load in state.get("loads", []):
        if not isinstance(load, dict):
            continue
        lines.append(
            "| {sequence} | {context} | {status} | {request_id} |".format(
                sequence=load.get("sequence", ""),
                context=load.get("context_name", ""),
                status=load.get("status", ""),
                request_id=load.get("request_id", "—"),
            )
        )
    lines.extend(("", f"State file: `{state_path}`"))
    errors = [item for item in state.get("errors", []) if isinstance(item, dict)]
    if errors:
        latest = errors[-1]
        lines.extend(
            (
                "",
                "| Failure class | Details |",
                "|---|---|",
                f"| {latest.get('failure_class')} | {latest.get('message')} |",
            )
        )
    elif state.get("status") == "awaiting_verification":
        lines.extend(
            (
                "",
                "Next action: run the routed Item Catalog child readback, parent no-drift, fresh full export, and duplicate-rerun checks; then supply their bound verification receipt. No new user approval is required.",
            )
        )
    return "\n".join(lines) + "\n"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--expected-test-environment", required=True)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--print-authorization-fingerprint", action="store_true")
    action.add_argument("--print-execution-fingerprint", action="store_true")
    action.add_argument("--dry-run", action="store_true")
    action.add_argument("--execute", action="store_true")
    parser.add_argument("--approved-authorization-fingerprint")
    parser.add_argument("--properties", type=Path)
    parser.add_argument(
        "--token-cache",
        type=Path,
        help=(
            "External private OAuth cache; default: managed ~/.fusionaim/<profile>_token.json."
        ),
    )
    parser.add_argument("--run-config", type=Path)
    parser.add_argument(
        "--verification-receipt",
        type=Path,
        help="Project-relative Item Catalog verification receipt for the load awaiting verification.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        root = _project_root(args.project_root)
        manifest_path = args.manifest
        if not manifest_path.is_absolute():
            manifest_path = root / manifest_path
        manifest_path = manifest_path.resolve(strict=True)
        if not _inside(manifest_path, root):
            raise TestBatchError("input_validation", "Manifest must resolve inside the project workspace.")
        manifest = _read_json(manifest_path, "batch manifest")
        require_execution = args.print_execution_fingerprint or args.dry_run or args.execute
        batch = validate_manifest(
            manifest,
            root,
            require_execution=require_execution,
            verify_fingerprints=not (
                args.print_authorization_fingerprint or args.print_execution_fingerprint
            ),
        )
        batch["project_root"] = root
        expected = _require_text(args.expected_test_environment, "expected_test_environment").upper()
        if expected != batch["target_environment"] or not _is_explicit_test_environment(expected):
            raise TestBatchError("approval_blocker", "Expected test environment does not match the exact manifest target.")
        if args.print_authorization_fingerprint:
            print("## Item Catalog FSM test-batch authorization")
            print()
            print(f"Authorization fingerprint: `{batch['authorization_fingerprint']}`")
            print(f"Target: `{batch['target_environment']}`")
            print(f"Loads: `{len(batch['loads'])}`")
            return 0
        if args.print_execution_fingerprint:
            print("## Item Catalog FSM test-batch execution")
            print()
            print(f"Authorization fingerprint: `{batch['authorization_fingerprint']}`")
            print(f"Execution fingerprint: `{batch['execution_fingerprint']}`")
            print(f"Target: `{batch['target_environment']}`")
            print(f"Loads: `{len(batch['loads'])}`")
            return 0
        if args.dry_run:
            print("## Item Catalog FSM test-batch dry run")
            print()
            print("All local manifest, target, archive, SHA-256, and Task Validation envelope checks passed.")
            print("No OAuth login, Fusion request, upload, initiation, status check, or provider change was performed.")
            return 0
        if not args.approved_authorization_fingerprint:
            raise TestBatchError("approval_blocker", "Execution requires the exact approved authorization fingerprint.")
        if args.properties is None:
            raise TestBatchError("input_validation", "Execution requires an explicit Fusion properties path.")
        properties = args.properties.expanduser().resolve(strict=True)
        token_cache = _resolve_repository_token_cache(args.token_cache, _repository_root())
        state, exit_code = execute_next(
            batch,
            approved_authorization_fingerprint=args.approved_authorization_fingerprint,
            properties_path=properties,
            token_cache_path=token_cache,
            run_config_path=args.run_config.expanduser().resolve(strict=True) if args.run_config else None,
            verification_receipt=args.verification_receipt,
        )
        print(_render_result(state, batch["state_path"]), end="")
        return exit_code
    except (TestBatchError, OSError) as error:
        if isinstance(error, TestBatchError):
            failure_class, message = error.failure_class, error.message
        else:
            failure_class, message = "artifact_persistence", str(error)
        print("## Item Catalog FSM test batch blocked", file=sys.stderr)
        print(file=sys.stderr)
        print(f"| Failure class | Details |", file=sys.stderr)
        print("|---|---|", file=sys.stderr)
        print(f"| {failure_class} | {message} |", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
