#!/usr/bin/env python3
"""Build a validated Goal Management HDL handoff for core.data-loader."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from hdl_dat_validator import HdlDatValidationError, validate_bundle
from hdl_dat_enricher import enrich_bundle
from hdl_manifest_builder import build_manifest


SENSITIVE_METADATA_FIELDS = {
    "ReqSubmittedByPersonNumber", "AssignedByPersonNumber", "PersonId", "AssignmentId",
    "WorkerPersonNumber", "WorkerAssignmentNumber", "GoalWorkerPersonNumber",
    "GoalWorkerAssignmentNumber", "ObjectId",
    "GoalPersonNumber", "GoalAssignmentNumber",
}


def redacted_audit_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    """Remove runtime identity values from the durable validation evidence."""
    durable = copy.deepcopy(manifest)
    for section in ("rowOperations", "targetEvidence", "reviewPeriodBounds"):
        if isinstance(durable.get(section), dict):
            durable[section] = {_audit_key(key): value for key, value in durable[section].items()}
    # Runtime bindings contain worker keys and population identities. They are
    # needed for validation, not for the durable audit or a second execution.
    for field in ("rowBindings", "resolvedSemanticValues", "existingRows"):
        durable.pop(field, None)
    for evidence in durable.get("targetEvidence", {}).values():
        if isinstance(evidence, dict):
            for field in set(evidence) - {"confirmed", "environment", "verifiedAt", "source"}:
                evidence.pop(field)
    components = durable.get("fieldMetadata")
    if not isinstance(components, dict):
        return durable
    for fields in components.values():
        if not isinstance(fields, dict):
            continue
        for field, contract in fields.items():
            if field in SENSITIVE_METADATA_FIELDS and isinstance(contract, dict):
                contract.pop("allowedValues", None)
                contract.pop("valueMap", None)
    return durable


def _audit_key(value: str) -> str:
    if any(field + "=" in value for field in SENSITIVE_METADATA_FIELDS):
        return "identity-sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()
    return value


def require_passed_report(report: dict[str, Any]) -> dict[str, Any]:
    """Reject reports that are incomplete, blocked, or carry any issue."""
    if report.get("status") != "passed":
        raise HdlDatValidationError("Goal Management HDL DAT preflight requires a passed validation report.")
    if report.get("validationScope") != "execution":
        raise HdlDatValidationError("Structural-only validation cannot authorize a Data Loader handoff.")
    if report.get("issues") not in ([], None):
        raise HdlDatValidationError("Goal Management HDL DAT preflight report must contain no issues.")
    if not isinstance(report.get("rows"), list) or not report["rows"]:
        raise HdlDatValidationError("Goal Management HDL DAT preflight report must identify validated rows.")
    return report


def build_final_data_fragment(source: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Validate an exact DAT, ZIP, or directory and return the Data Loader fragment."""
    report = require_passed_report(validate_bundle(source, manifest, execution_validation=True))
    for row in report["rows"]:
        for field in ("sourceIdentity", "rowKey"):
            row[field] = _audit_key(row[field])
    return {"format": "goal-management-hdl-dat", "hdlValidation": report}


def prepare_final_data_fragment(
    source: Path,
    profile: str,
    runtime_context: dict[str, Any],
    prepared_output: Path,
) -> dict[str, Any]:
    """Enrich an immutable copy, generate its internal manifest, and validate it."""
    preparation = enrich_bundle(source, profile, runtime_context, prepared_output)
    manifest = build_manifest(prepared_output, profile, runtime_context)
    fragment = build_final_data_fragment(prepared_output, manifest)
    fragment["hdlPreparation"] = preparation
    fragment["hdlManifest"] = redacted_audit_manifest(manifest)
    fragment["preparedSource"] = str(prepared_output)
    return fragment


def library_requirements_from_source(request, source):
    """Preserve supplied create values/keys; never ask the consultant to retype them."""
    from library_goal_hdl_resolver import guard_route, load_catalog
    from hdl_dat_validator import _read_source
    guard_route(request)
    if request["route"] != "hdl_dat_preflight":
        raise HdlDatValidationError("HDL_ROUTE_REQUIRED: supplied source requires hdl_dat_preflight.")
    request = copy.deepcopy(request)
    catalog = load_catalog()
    reverse = {v["field"]: k for k, v in catalog["fields"].items()}
    files, issues, _ = _read_source(source)
    if issues or set(files) != {"ContentItem.dat"}:
        raise HdlDatValidationError("SIMPLE_LIBRARY_SOURCE_REQUIRED: component bundles retain the existing resolved-context preflight.")
    try:
        lines = files["ContentItem.dat"].decode("utf-8-sig").splitlines()
    except UnicodeDecodeError as exc:
        raise HdlDatValidationError("SOURCE_ENCODING_INVALID: UTF-8 required.") from exc
    header, supplied_rows = None, []
    for raw in lines:
        parts = raw.split("|")
        if not raw.strip() or raw.startswith("COMMENT|"):
            continue
        if parts[:2] == ["METADATA", "ContentItem"]:
            header = parts[2:]
            if len(header) != len(set(header)):
                raise HdlDatValidationError("SOURCE_ROW_MISMATCH: duplicate attributes.")
        elif parts[:2] == ["MERGE", "ContentItem"] and header and len(header) == len(parts) - 2:
            row = {}
            for field, value in zip(header, parts[2:]):
                if not value:
                    continue
                if field == "ContextName":
                    if value != "GOAL":
                        raise HdlDatValidationError("SOURCE_ROW_MISMATCH: only GOAL context supported.")
                    continue
                # Keep additional physical HDL headers for the live template and
                # VO crosswalk resolver to validate; never discard a supplied value.
                semantic = reverse.get(field, field)
                kind = catalog["fields"].get(semantic, {}).get("type")
                if kind == "date" or field == "DateFrom":
                    value = value.replace("/", "-")
                if kind == "integer":
                    if not value.isdigit():
                        raise HdlDatValidationError(f"REFERENCE_INVALID: {field} must be a positive integer.")
                    value = int(value)
                row[semantic] = value
            supplied_rows.append(row)
        else:
            raise HdlDatValidationError("SOURCE_ROW_MISMATCH: expected root ContentItem MERGE rows.")
    if len(supplied_rows) != len(request.get("rows", [])):
        raise HdlDatValidationError("SOURCE_ROW_MISMATCH: source and requirements counts differ.")
    for row, supplied in zip(request["rows"], supplied_rows):
        for key, value in supplied.items():
            if key in row and row[key] != value:
                raise HdlDatValidationError(f"SOURCE_ROW_MISMATCH: supplied {key} conflicts with requirements.")
            row[key] = value
    return request


def prepare_library_goal(request, evidence, prepared_output, *, source=None):
    """HDL-only business-input entry. Core renders the source; existing gates validate it."""
    from library_goal_hdl_resolver import resolve_context, ROOT
    if (request.get("route") == "hdl_dat_preflight") != (source is not None):
        raise HdlDatValidationError("HDL_ROUTE_REQUIRED: source presence must match the selected HDL route.")
    if source is not None:
        request = library_requirements_from_source(request, source)
    context = resolve_context(request, evidence)
    if source is not None:
        # A supplied DAT is never rewritten. Canonical requirements must describe each root row.
        from hdl_dat_validator import _read_source
        files, issues, _ = _read_source(source)
        if issues or set(files) != {"ContentItem.dat"}:
            raise HdlDatValidationError("SIMPLE_LIBRARY_SOURCE_REQUIRED: component bundles use the existing resolved-context preflight.")
        header, count = None, 0
        locations = []
        for line, raw in enumerate(files["ContentItem.dat"].decode("utf-8-sig").splitlines(), 1):
            parts = raw.split("|")
            if parts[:2] == ["METADATA", "ContentItem"]:
                header = parts[2:]
            elif parts[:2] == ["MERGE", "ContentItem"]:
                if header is None or len(header) != len(parts) - 2 or count >= len(request["rows"]):
                    raise HdlDatValidationError("SOURCE_ROW_MISMATCH: source and requirements differ.")
                row = dict(zip(header, parts[2:]))
                original = f"ContentItem.dat|ContentItem|line:{count + 2}"
                resolved = context["derivedValues"][original]
                for field, value in row.items():
                    if value and (field not in resolved or value != resolved[field]):
                        raise HdlDatValidationError(f"SOURCE_ROW_MISMATCH: preserve and resolve supplied {field} before preparation.")
                locations.append((original, f"ContentItem.dat|ContentItem|line:{line}"))
                count += 1
            elif raw.strip() and not raw.startswith("COMMENT|"):
                raise HdlDatValidationError("SOURCE_ROW_MISMATCH: only ContentItem create rows are supported by this entry.")
        if count != len(request["rows"]):
            raise HdlDatValidationError("SOURCE_ROW_MISMATCH: source and requirements counts differ.")
        for key in ("derivedValues", "resolvedSemanticValues"):
            context[key] = {new: context[key][old] for old, new in locations if old in context[key]}
        context["createRows"] = [new for _, new in locations]
        return prepare_final_data_fragment(source, request["profile"], context, prepared_output)
    # Core's deterministic DAT renderer owns encoding/serialization; no sample placeholder rows.
    import sys
    sys.path.insert(0, str(ROOT / "core/data-loader/scripts"))
    import data_loader_metadata as core
    from generate_sample_dat import render_dat
    section = core.TemplateSection("ContentItem", (core.TemplateAttribute("Name", "Name"),))
    schema = core.BusinessObjectSchema("", "ContentItem", "Content Item", "", "ContentItem.dat", (section,), {}, {})
    with tempfile.TemporaryDirectory(prefix="library-goal-hdl-") as directory:
        path = Path(directory) / "ContentItem.dat"
        chunks = [render_dat(schema, {"ContentItem": (("Name",), (row["GoalName"],))}).splitlines() for row in request["rows"]]
        path.write_text("\n".join([chunks[0][0], *(chunk[1] for chunk in chunks)]) + "\n", encoding="utf-8")
        return prepare_final_data_fragment(path, request["profile"], context, prepared_output)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Goal Management HDL DAT/ZIP input for Data Loader handoff.")
    parser.add_argument("--source", "--bundle", dest="source", type=Path)
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--manifest", type=Path, help="Prebuilt internal manifest for compatibility/testing.")
    source_group.add_argument("--runtime-context", type=Path, help="Internal routed-workflow context; not consultant input.")
    source_group.add_argument("--requirements", type=Path, help="Library Goal HDL canonical business requirements; resolves technical context automatically.")
    reads = parser.add_mutually_exclusive_group()
    reads.add_argument("--read-evidence", type=Path, help="Full metadata and raw read responses for deterministic replay; no network.")
    reads.add_argument("--live-control", type=Path, help="Fresh allowed owning-task control selecting Core read services.")
    parser.add_argument("--profile", choices=("goal_plan", "performance_library_goal", "development_library_goal"))
    parser.add_argument("--prepared-output", type=Path)
    parser.add_argument("--output", type=Path, help="Optional JSON output path for the finalData fragment.")
    args = parser.parse_args()
    if args.requirements:
        if not args.prepared_output or not (args.read_evidence or args.live_control):
            parser.error("--requirements requires --prepared-output and --read-evidence or --live-control")
        request = json.loads(args.requirements.read_text(encoding="utf-8"))
        from library_goal_hdl_resolver import guard_route, read_live_evidence
        guard_route(request)
        if (request["route"] == "hdl_dat_preflight") != (args.source is not None):
            parser.error("hdl_dat_preflight requires --source; hdl_generate must not supply --source")
        if args.source:
            request = library_requirements_from_source(request, args.source)
        evidence = (json.loads(args.read_evidence.read_text(encoding="utf-8")) if args.read_evidence else
                    read_live_evidence(request, json.loads(args.live_control.read_text(encoding="utf-8"))))
        fragment = prepare_library_goal(request, evidence, args.prepared_output, source=args.source)
    elif args.runtime_context:
        if args.read_evidence or args.live_control:
            parser.error("read options require --requirements")
        if not args.source or not args.profile or not args.prepared_output:
            parser.error("--runtime-context requires --profile and --prepared-output")
        context = json.loads(args.runtime_context.read_text(encoding="utf-8"))
        fragment = prepare_final_data_fragment(args.source, args.profile, context, args.prepared_output)
    else:
        if not args.source or args.read_evidence or args.live_control:
            parser.error("--manifest requires --source and no read options")
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        fragment = build_final_data_fragment(args.source, manifest)
    content = json.dumps(fragment, indent=2) + "\n"
    if args.output:
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (HdlDatValidationError, json.JSONDecodeError, OSError) as exc:
        raise SystemExit(f"Error: {exc}")
