#!/usr/bin/env python3
"""Resolve GROW-8164 AC2 intake prompts without contacting Fusion.

This small, local contract is deliberately separate from validation and HDL
generation.  It classifies a user's intake request and returns a predictable
response object that a conversational skill can render or a caller can test.
No response from this module authorizes or initiates a Fusion operation.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_XLSX_TEMPLATE = SKILL_DIR / "templates" / "profile-management-data-load-intake.xlsx"
CSV_COLUMNS = (
    "target_environment", "requested_operation", "root_record_type", "target_check_status",
    "object", "identifier", "parent_identifier", "language", "values_json",
)
SUPPORTED_EXECUTION_OBJECTS = ("Talent Profile", "Talent Profile Translation")
PROVIDER_BLOCKED_OBJECTS = (
    "Content Item", "Content Item Relationship", "Content Item Translation",
    "Content Item Rating Description Translation", "Talent Model Profile Extra Information",
    "Talent Model Profile Extra Information Translation", "Profile Attachment",
)


def _data_set_module() -> Any:
    """Load the local intake module without relying on the caller's sys.path."""
    module_path = SCRIPT_DIR / "profile_management_data_set.py"
    spec = importlib.util.spec_from_file_location("profile_management_data_set_for_ac2", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Profile Management intake module is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _extract(prompt: str, pattern: str) -> str:
    match = re.search(pattern, prompt, flags=re.IGNORECASE)
    return match.group(1).strip().strip(".,;:") if match else ""


def _prefilled_form(prompt: str) -> tuple[dict[str, Any], list[str]]:
    """Extract only explicitly stated values; every inference stays outstanding."""
    target = _extract(prompt, r"\b(?:in|target(?:\s+environment)?\s*(?:is|:)?)\s+([A-Za-z0-9_-]+)")
    operation = _extract(prompt, r"\b(?:operation\s*(?:is|:)?\s*)?(create(?:/load)?|update|migration|mass[- ]maintenance|translation)\b")
    operation = {"create/load": "create", "mass maintenance": "mass-maintenance", "mass-maintenance": "mass-maintenance"}.get(operation.casefold(), operation.casefold())
    root_type = ""
    lowered = prompt.casefold()
    if "model profile" in lowered or "model-profile" in lowered:
        root_type = "model-profile"
    elif "person profile" in lowered or "person-profile" in lowered:
        root_type = "person-profile"
    elif "content library" in lowered or "content-library" in lowered:
        root_type = "content-library"
    identifier = _extract(prompt, r"\b(?:identifier|profile\s*code)\s*(?:is|:)?\s*([A-Za-z0-9_-]+)")
    record: dict[str, Any] = {"object": "Talent Profile", "identifier": identifier, "values": {}}
    form = {
        "target_environment": target,
        "requested_operation": operation,
        "root_record_type": root_type,
        "target_check": {"status": ""},
        "records": [record],
    }
    required = []
    labels = (
        ("target environment", target),
        ("operation", operation),
        ("root record type", root_type),
        ("ProfileCode / identifier", identifier),
        ("exact target check", ""),
    )
    required.extend(label for label, value in labels if not value)
    if root_type == "model-profile":
        required.extend(("Profile Type code and ID evidence", "Profile status code", "Profile usage code"))
    return form, required


def classify_prompt(prompt: str, source: Path | None = None) -> str:
    """Return a stable AC2 intake mode, without interpreting a request as approval."""
    text = prompt.casefold()
    if source is not None and source.suffix.casefold() == ".csv":
        return "csv-import-mapping-review"
    if re.search(r"\b(import|validate|map|mapping review)\b.*\bcsv\b|\bcsv\b.*\b(import|validate|map)", text):
        return "csv-import-mapping-review"
    if re.search(r"\b(export|generate|create|give)\b.*\bcsv\b|\bcsv\s+template\b", text):
        return "csv-export"
    if any(term in text for term in ("spreadsheet", "excel", "xlsx", "workbook", "template", "guideline", "guidance")):
        return "template-guidance"
    if any(term in text for term in ("direct entry", "profile file", "create profile", "model profile", "person profile", "profile data")):
        return "direct-entry"
    return "clarification-required"


def _base_response(mode: str) -> dict[str, Any]:
    return {
        "acceptance_criterion": "AC2",
        "intake_mode": mode,
        "execution": "not-authorized",
        "fusion_activity": "none",
        "supported_execution_scope": list(SUPPORTED_EXECUTION_OBJECTS),
        "provider_blocked_objects": list(PROVIDER_BLOCKED_OBJECTS),
        "load_status": "no load initiated",
    }


def resolve_ac2_prompt(prompt: str, source: Path | None = None, preserve_source_dir: Path | None = None) -> dict[str, Any]:
    """Resolve an AC2 prompt into a safe, machine-readable response."""
    mode = classify_prompt(prompt, source)
    response = _base_response(mode)
    if mode == "template-guidance":
        response.update({
            "template": {"format": "xlsx", "path": str(DEFAULT_XLSX_TEMPLATE), "delivery": "attach-default-template"},
            "guidance": [
                "Complete target environment, operation, root record type, and exact target-check status on Request.",
                "Enter each parent and child record on Records; repeat rows for translations and relationships.",
                "Use Language only for translations. Do not invent flexfield, attachment, or blocked-child attributes.",
                "This workbook is intake only, not an HDL payload or load approval.",
            ],
            "next_safe_action": "Complete the workbook and request a local validation and mapping review.",
            "outstanding_inputs": ["completed intake values"],
        })
    elif mode == "csv-export":
        response.update({
            "csv_columns": list(CSV_COLUMNS),
            "csv_contract": "local interchange only; it is not an HDL payload or load approval",
            "next_safe_action": "Populate the CSV, then provide it for local import and mapping review.",
            "outstanding_inputs": ["completed CSV intake rows"],
        })
    elif mode == "csv-import-mapping-review":
        if source is None:
            response.update({
                "outstanding_inputs": ["CSV file to import"],
                "next_safe_action": "Attach the CSV; it will be mapped and validated locally before any preview.",
            })
        else:
            intake = _data_set_module()
            try:
                request = intake.request_from_source(source, preserve_source_dir)
                errors = intake.validate_request(request)
                response.update({
                    "request": request,
                    "mapping_review": intake.mapping_review(request),
                    "validation_errors": errors,
                    "outstanding_inputs": [] if not errors else errors,
                    "next_safe_action": "Correct every mapping or validation issue, then request a new local validation.",
                })
            except (OSError, ValueError, json.JSONDecodeError) as error:
                response.update({
                    "validation_errors": [str(error)],
                    "outstanding_inputs": ["a readable CSV in the documented intake format"],
                    "next_safe_action": "Correct the CSV without adding inferred mappings, then import it again.",
                })
    elif mode == "direct-entry":
        form, missing = _prefilled_form(prompt)
        response.update({
            "intake_form": form,
            "outstanding_inputs": missing,
            "next_safe_action": "Complete only the missing intake fields; child rows stay with their parent ProfileCode.",
        })
    else:
        response.update({
            "outstanding_inputs": ["intake mode: direct entry, spreadsheet template, CSV export, or CSV import"],
            "next_safe_action": "State the desired intake mode and, if known, target environment, operation, root type, and identifier.",
        })
    return response


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", help="User-authored AC2 intake request")
    parser.add_argument("--source", type=Path, help="Optional supplied intake source, read locally")
    parser.add_argument("--preserve-source-dir", type=Path, help="Optional local evidence directory")
    args = parser.parse_args()
    print(json.dumps(resolve_ac2_prompt(args.prompt, args.source, args.preserve_source_dir), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
