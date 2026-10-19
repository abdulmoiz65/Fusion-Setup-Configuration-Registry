#!/usr/bin/env python3
"""Deterministically select the Goal Management REST, intake, or HDL route.

REST is the normal-volume default. Goal Plan and Library Goal work can use
HDL when explicitly requested or when root-row volume reaches the configured
bulk threshold. A missing DAT/ZIP selects source generation instead of a
blocker. Review Period remains REST-only.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable


UNSTRUCTURED_SUFFIXES = {
    ".doc", ".docx", ".pdf", ".ppt", ".pptx", ".xls", ".xlsx", ".csv", ".tsv", ".txt", ".md",
    ".png", ".jpg", ".jpeg", ".webp", ".tiff"
}
DEFAULT_HIGH_VOLUME_THRESHOLD = 25
REVIEW_PERIOD_OBJECTS = {"review period", "review periods", "reviewperiod"}
GOAL_PLAN_OBJECTS = {"goal plan", "goal plans", "goalplan"}
LIBRARY_GOAL_OBJECTS = {
    "library goal", "library goals", "performance library goal", "performance library goals",
    "development library goal", "development library goals", "content item", "content items", "contentitem",
}


def resolve_approval_intent(intent: str, *, operation_count: int | None = None) -> dict[str, Any]:
    """Classify approval grouping without selecting an HTTP transport.

    A consultant's request for one approval over several changes says nothing
    about whether Fusion supports one batch request.  Transport is resolved
    later from the operation-specific current contract.
    """
    if operation_count is not None and (
        isinstance(operation_count, bool) or not isinstance(operation_count, int) or operation_count < 1
    ):
        raise ValueError("operation_count must be a positive integer when supplied")
    normalized = _positive_intent(intent)
    grouped = any(
        phrase in normalized
        for phrase in (
            "one approval",
            "single approval",
            "one approval gate",
            "single approval gate",
            "approve all",
            "approve them all",
        )
    )
    separate = any(
        phrase in normalized
        for phrase in ("separate approval", "approve separately", "one by one approval")
    )
    if grouped and separate:
        return {
            "approvalMode": "blocked",
            "status": "APPROVAL_INTENT_CONFLICT",
            "transportSelected": False,
        }
    mode = "single_group" if grouped else "per_operation" if separate else "unspecified"
    if operation_count == 1 and mode == "unspecified":
        mode = "single_group"
    return {
        "approvalMode": mode,
        "status": "READY",
        "operationCount": operation_count,
        "transportSelected": False,
    }


def _normalized(value: str) -> str:
    return " ".join(value.casefold().replace("_", " ").replace("-", " ").split())


def _explicit_hdl_intent(intent: str) -> bool:
    normalized = _positive_intent(intent)
    return any(phrase in normalized for phrase in ("hdl", "hcm data loader", "use data loader", "data load"))


def _explicit_rest_intent(intent: str) -> bool:
    normalized = _positive_intent(intent)
    return explicit_rest_batch_intent(intent) or any(phrase in normalized for phrase in ("use rest", "via rest", "through rest", "rest api", "rest route"))


def explicit_rest_batch_intent(intent: str) -> bool:
    """Require REST and batch in the same positive clause; bulk alone is not batch."""
    positive = re.sub(r"\b(?:without|not)\b.*?(?=[;.!]|\bbut\b|\binstead\b|$)",
                      "", _positive_intent(intent))
    return any(
        re.search(r"\brest\b", clause) and re.search(r"\bbatch(?:ed|ing)?\b", clause)
        for clause in re.split(r"[;.!]|\bbut\b|\binstead\b", positive)
    )


def _declared_high_volume(intent: str) -> bool:
    normalized = _positive_intent(intent)
    return any(
        phrase in normalized
        for phrase in ("high volume", "large volume", "bulk load", "bulk import", "mass load", "mass upload")
    )


def _positive_intent(intent: str) -> str:
    """Remove explicitly negated clauses, not individual transport names."""
    value = _normalized(intent).replace("’", "'")
    return re.sub(r"\b(?:do not|don't|never|no)\b.*?(?=[;.!]|\bbut\b|\binstead\b|$)", "", value)


def select_route(
    sources: Iterable[str | Path],
    intent: str,
    object_name: str | None = None,
    *,
    root_record_count: int | None = None,
    high_volume_threshold: int = DEFAULT_HIGH_VOLUME_THRESHOLD,
    source_normalized: bool = False,
) -> dict[str, Any]:
    if high_volume_threshold <= 0:
        raise ValueError("high_volume_threshold must be greater than zero")
    if root_record_count is not None and root_record_count < 0:
        raise ValueError("root_record_count cannot be negative")

    paths = [Path(value) for value in sources]
    has_hdl_source = any(path.suffix.casefold() in {".dat", ".zip"} for path in paths)
    explicit_hdl = _explicit_hdl_intent(intent)
    explicit_rest = _explicit_rest_intent(intent)
    rest_batch = explicit_rest_batch_intent(intent)
    normalized_object = _normalized(object_name or "")
    is_review_period = normalized_object in REVIEW_PERIOD_OBJECTS
    is_hdl_object = normalized_object in GOAL_PLAN_OBJECTS | LIBRARY_GOAL_OBJECTS
    count_selects_hdl = root_record_count is not None and root_record_count >= high_volume_threshold
    declared_high_volume = _declared_high_volume(intent)
    common = {
        "defaultExecutionRoute": "rest",
        "highVolumeThreshold": high_volume_threshold,
        "rootRecordCount": root_record_count,
        "sourceNormalized": source_normalized,
        "approvalIntent": resolve_approval_intent(intent),
    }

    positive = _positive_intent(intent)
    wants_export = bool(re.search(r"\bexport\b", positive))
    wants_import = bool(re.search(r"\bimport\b", positive))
    fsm = bool(re.search(r"\bfsm\b|\bsetup (?:data|csv|package)\b", positive))
    if wants_export and wants_import:
        return {**common, "route": "blocked", "status": "NEEDS_OPERATION_SPLIT",
                "reason": "Preview export and import as separate explicitly requested operations."}
    if wants_export or (wants_import and fsm):
        if explicit_hdl or explicit_rest:
            return {**common, "route": "blocked", "status": "NEEDS_ROUTE_CONFIRMATION",
                    "reason": "Resolve the requested setup transfer versus REST/HDL operation."}
        return {**common, "route": "csv_export" if wants_export else "csv_import", "status": "PREFLIGHT_REQUIRED",
                "owner": "shared.setup-export.task-level-export" if wants_export else "core.data-loader",
                "selectionReason": "explicit_setup_transfer", "requiresCatalogSupport": True,
                "requiresExplicitApproval": True}
    if wants_import and not explicit_hdl and not explicit_rest:
        return {**common, "route": "blocked", "status": "NEEDS_ROUTE_CONFIRMATION",
                "reason": "Specify FSM setup import or HDL data loading; import alone is ambiguous."}

    if explicit_hdl and explicit_rest:
        return {
            **common, "route": "blocked", "status": "BLOCKED", "code": "TRANSPORT_INTENT_CONFLICT",
            "reason": "The request explicitly selects both REST and HDL. Confirm one execution route.",
        }
    if explicit_hdl and is_review_period:
        return {
            **common, "route": "blocked", "status": "BLOCKED", "code": "HDL_OBJECT_UNSUPPORTED",
            "reason": "Review Period HDL is not supported by Goal Management; use REST.", "supportedRoute": "rest",
        }
    # Unknown formats and folders also require intake, never a silent REST fall-through.
    has_functional_input = bool(paths)
    if has_functional_input and not source_normalized and not explicit_hdl:
        return {
            **common,
            "route": "implementation_intake",
            "status": "READY",
            "next": "normalize-source-and-reselect",
            "selectionReason": "functional_input_requires_intake",
            "reason": "Normalize the supplied functional input once, then reselect the object execution route with source_normalized=true.",
        }
    if is_review_period:
        if rest_batch:
            return {**common, "route": "rest", "status": "PREFLIGHT_REQUIRED",
                    "transportIntent": "adf_batch", "selectionReason": "explicit_rest_batch",
                    "next": "goal-management-common/rest-batch.md"}
        return {**common, "route": "rest", "status": "READY", "selectionReason": "review_period_rest_only"}
    if explicit_rest:
        if rest_batch:
            return {**common, "route": "rest", "status": "PREFLIGHT_REQUIRED",
                    "transportIntent": "adf_batch", "selectionReason": "explicit_rest_batch",
                    "next": "goal-management-common/rest-batch.md"}
        return {**common, "route": "rest", "status": "READY", "selectionReason": "explicit_rest"}

    negative_clauses = re.findall(r"\b(?:do not|don't|never|no)\b.*?(?=[;.!]|\bbut\b|\binstead\b|$)", _normalized(intent).replace("’", "'"))
    hdl_denied = any(re.search(r"\bhdl\b|\bhcm data loader\b|\bdata load\b", clause) for clause in negative_clauses)
    hdl_selected = explicit_hdl or ((count_selects_hdl or declared_high_volume) and not hdl_denied)
    if hdl_selected and not is_hdl_object:
        return {
            **common, "route": "implementation_intake", "status": "NEEDS_OBJECT_CLASSIFICATION",
            "code": "HDL_OBJECT_REQUIRED",
            "reason": "Classify the request as Goal Plan, Library Goal, or Review Period before selecting HDL.",
        }

    selection_reason = (
        "explicit_hdl" if explicit_hdl else "root_record_threshold" if count_selects_hdl else "declared_high_volume"
    )
    if hdl_selected and has_hdl_source:
        return {
            **common, "route": "hdl_dat_preflight", "status": "READY", "sourceMode": "supplied",
            "selectionReason": selection_reason,
            "next": "Validate the supplied artifact and business values, then hand off to core.data-loader.",
        }
    if hdl_selected:
        return {
            **common, "route": "hdl_generate", "status": "READY", "sourceMode": "generated",
            "selectionReason": selection_reason, "generationOwner": "core.data-loader",
            "next": "Resolve and validate business rows, then have core.data-loader generate the live-metadata source and immutable ZIP.",
        }
    return {**common, "route": "rest", "status": "READY", "selectionReason": "normal_volume_default"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Select the Goal Management execution route without side effects.")
    parser.add_argument("--intent", required=True)
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--object")
    parser.add_argument("--root-record-count", type=int)
    parser.add_argument(
        "--source-normalized",
        action="store_true",
        help="The supplied source has already completed Goal Management implementation intake.",
    )
    parser.add_argument(
        "--high-volume-threshold", type=int, default=DEFAULT_HIGH_VOLUME_THRESHOLD,
        help=f"Root-row count that selects HDL automatically (default: {DEFAULT_HIGH_VOLUME_THRESHOLD})",
    )
    args = parser.parse_args()
    print(json.dumps(select_route(
        args.source, args.intent, args.object, root_record_count=args.root_record_count,
        high_volume_threshold=args.high_volume_threshold, source_normalized=args.source_normalized,
    ), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
