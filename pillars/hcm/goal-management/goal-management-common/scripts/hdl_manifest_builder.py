#!/usr/bin/env python3
"""Build the internal audit manifest for a prepared Goal Management HDL bundle."""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import io
import json
from pathlib import Path
from typing import Any

from hdl_dat_validator import (
    ALLOWED_OPERATIONS,
    HdlDatValidationError,
    PROFILES,
    _field_map,
    _identity,
    _read_source,
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _confirmed_evidence(context: dict[str, Any], timestamp: str) -> dict[str, dict[str, Any]]:
    environment = context.get("environment")
    if not isinstance(environment, str) or not environment.strip():
        raise HdlDatValidationError("Internal runtime context requires the configured Fusion environment identity.")
    sources = context.get("evidenceSources")
    if not isinstance(sources, dict) or not sources:
        raise HdlDatValidationError("Internal runtime context requires fresh target evidence sources.")
    result: dict[str, dict[str, Any]] = {}
    default_verified_at = context.get("verifiedAt")
    if not isinstance(default_verified_at, str) or not default_verified_at.strip():
        raise HdlDatValidationError("verifiedAt must be the actual target-read timestamp, not the preparation time.")
    for name, evidence in sources.items():
        if not isinstance(name, str) or not name:
            raise HdlDatValidationError("evidenceSources must contain nonblank names and source descriptions.")
        if isinstance(evidence, str):
            source = evidence
            verified_at = default_verified_at
            evidence_environment = environment
        elif isinstance(evidence, dict):
            source = evidence.get("source")
            verified_at = evidence.get("verifiedAt")
            evidence_environment = evidence.get("environment", environment)
        else:
            raise HdlDatValidationError("evidenceSources values must be source strings or structured evidence objects.")
        if not isinstance(source, str) or not source.strip():
            raise HdlDatValidationError("evidenceSources must contain nonblank source descriptions.")
        if not isinstance(verified_at, str) or not verified_at.strip():
            raise HdlDatValidationError("Every structured evidence source requires its actual target-read timestamp.")
        if not isinstance(evidence_environment, str) or evidence_environment.strip().casefold() != environment.strip().casefold():
            raise HdlDatValidationError("Every structured evidence source must match the configured Fusion environment.")
        result[name] = {
            **(deepcopy(evidence) if isinstance(evidence, dict) else {}),
            "confirmed": True,
            "environment": environment.strip(),
            "verifiedAt": verified_at.strip(),
            "source": source.strip(),
        }
    return result


def build_manifest(source: Path, profile: str, runtime_context: dict[str, Any]) -> dict[str, Any]:
    """Generate audit-only validation data; consultants never author this structure."""
    if profile not in PROFILES:
        raise HdlDatValidationError("profile must identify a supported Goal Management HDL bundle.")
    files, issues, _ = _read_source(source)
    if issues:
        raise HdlDatValidationError(issues[0]["message"])
    contract = PROFILES[profile]
    ordered_files = [name for name in (*contract["required"], *contract["optional"]) if name in files]
    timestamp = runtime_context.get("generatedAt", _now())
    if not isinstance(timestamp, str) or not timestamp.strip():
        raise HdlDatValidationError("generatedAt must be a timezone-aware ISO-8601 timestamp.")
    allowed = runtime_context.get("allowedOperations", [runtime_context.get("defaultOperation", "create")])
    if not isinstance(allowed, list) or not allowed or not set(allowed) <= ALLOWED_OPERATIONS:
        raise HdlDatValidationError("allowedOperations must contain only create, update, or delete.")
    default_operation = runtime_context.get("defaultOperation")
    explicit = runtime_context.get("rowOperations", {})
    if explicit and not isinstance(explicit, dict):
        raise HdlDatValidationError("rowOperations must be an internally generated object.")
    user_key_fields = runtime_context.get("userKeyFields", {})
    identity_manifest = {"userKeyFields": user_key_fields}
    row_operations: dict[str, str] = {}
    row_bindings: dict[str, Any] = {}
    semantic_values: dict[str, Any] = {}
    consumed_context = {"rowBindings": set(), "resolvedSemanticValues": set()}

    for filename in ordered_files:
        metadata: dict[str, list[str]] = {}
        try:
            text = files[filename].decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise HdlDatValidationError(f"{filename} must be valid UTF-8 text.") from exc
        for number, raw in enumerate(io.StringIO(text), start=1):
            values = raw.rstrip("\r\n").split("|")
            if len(values) >= 2 and values[0] == "METADATA":
                metadata[values[1]] = values
                continue
            if len(values) < 2 or values[0] not in {"MERGE", "DELETE"}:
                continue
            fields = metadata.get(values[1])
            if fields is None or len(fields) != len(values):
                continue
            row = _field_map(fields, values)
            identity = _identity(values[1], row, identity_manifest)
            if identity is None:
                raise HdlDatValidationError(f"{filename}:{number} cannot be assigned a source or supported user identity.")
            scoped = f"{filename}|{values[1]}|{identity}"
            location = f"{filename}|{values[1]}|line:{number}"
            operation = "delete" if values[0] == "DELETE" else explicit.get(location, explicit.get(scoped, default_operation))
            if operation not in ALLOWED_OPERATIONS:
                raise HdlDatValidationError(
                    f"{location} requires an internally resolved create/update operation before validation."
                )
            row_operations[scoped] = operation
            for name, destination in (("rowBindings", row_bindings),
                                      ("resolvedSemanticValues", semantic_values)):
                supplied = runtime_context.get(name, {})
                if not isinstance(supplied, dict):
                    raise HdlDatValidationError(f"{name} must be an object keyed by source row location.")
                if location in supplied:
                    destination[scoped] = deepcopy(supplied[location])
                    consumed_context[name].add(location)

    for name, consumed in consumed_context.items():
        if set(runtime_context.get(name, {})) != consumed:
            raise HdlDatValidationError(f"{name} contains unresolved source row locations.")

    mandatory = runtime_context.get("mandatoryFields")
    if not isinstance(mandatory, dict) or not mandatory:
        raise HdlDatValidationError("Internal runtime context requires current target-template mandatoryFields.")
    manifest: dict[str, Any] = {
        "profile": profile,
        "environment": runtime_context.get("environment"),
        "files": ordered_files,
        "allowedOperations": allowed,
        "rowOperations": row_operations,
        "mandatoryFields": mandatory,
        "validationTime": timestamp,
        "targetEvidence": _confirmed_evidence(runtime_context, timestamp),
        "generatedInternally": True,
        "rowBindings": row_bindings,
        "resolvedSemanticValues": semantic_values,
    }
    for name in (
        "evidenceMaxAgeHours", "existingParents", "userKeyFields", "variantField",
        "enabledLanguages", "baseLanguage", "translationParentReferences",
        "semanticFields", "fieldMetadata", "existingRows", "reviewPeriodBounds",
        "operationMandatoryFields", "mappingEvidence", "resolutionContract",
    ):
        if name in runtime_context:
            manifest[name] = runtime_context[name]
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an internal Goal Management HDL validation manifest.")
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--profile", required=True, choices=tuple(PROFILES))
    parser.add_argument("--runtime-context", required=True, type=Path, help="Internal routed-workflow context; not consultant input.")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    context = json.loads(args.runtime_context.read_text(encoding="utf-8"))
    args.output.write_text(json.dumps(build_manifest(args.source, args.profile, context), indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (HdlDatValidationError, json.JSONDecodeError, OSError) as exc:
        raise SystemExit(f"Error: {exc}")
