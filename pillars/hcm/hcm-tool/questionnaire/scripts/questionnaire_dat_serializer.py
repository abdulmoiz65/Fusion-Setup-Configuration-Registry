#!/usr/bin/env python3
"""Render Questionnaire-family HDL DAT files from a structured build specification."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

try:
    from questionnaire_dat_validator import (
        ALLOWED_OPERATION,
        DatValidationError,
        _atomic_write_new,
        is_nonportable_attribute,
        parse_template,
        sha256_bytes,
        validate_candidate_bytes,
    )
except ModuleNotFoundError:
    from scripts.questionnaire_dat_validator import (  # type: ignore[no-redef]
        ALLOWED_OPERATION,
        DatValidationError,
        _atomic_write_new,
        is_nonportable_attribute,
        parse_template,
        sha256_bytes,
        validate_candidate_bytes,
    )


SUPPORTED_TASK_FILES = {
    "question-library": {"Question.dat", "QuestionTranslation.dat"},
    "questionnaire-templates": {"QuestionnaireTemplate.dat"},
    "questionnaires": {"Questionnaire.dat", "QuestionnaireTranslation.dat"},
}


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DatValidationError(f"unable to read JSON build specification {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise DatValidationError("build specification root must be an object")
    return value


def _string_value(value: Any, *, field_path: str) -> str:
    if value is None:
        raise DatValidationError(f"{field_path} cannot be JSON null; omit it for a blank DAT cell")
    if isinstance(value, bool):
        raise DatValidationError(f"{field_path} cannot be a JSON boolean; use Y or N")
    if isinstance(value, (dict, list, float)):
        raise DatValidationError(f"{field_path} must be a string or integer")
    text = str(value)
    if "|" in text or "\r" in text or "\n" in text:
        raise DatValidationError(
            f"{field_path} contains a DAT delimiter or line break that has no approved representation"
        )
    if text in {"#NULL", "null"}:
        raise DatValidationError(f"{field_path} uses an unsupported null token")
    return text


def _component_contract(spec: dict[str, Any]) -> dict[str, Any]:
    evidence = spec.get("validation_evidence")
    if not isinstance(evidence, dict):
        raise DatValidationError("validation_evidence must be an object")
    contract = evidence.get("component_contract")
    if not isinstance(contract, dict) or not contract:
        raise DatValidationError("validation_evidence.component_contract must be a non-empty object")
    return contract


def evidence_bundle_sha256(spec: dict[str, Any]) -> str:
    canonical = copy.deepcopy(spec)
    evidence = canonical.get("validation_evidence")
    if not isinstance(evidence, dict):
        raise DatValidationError("validation_evidence must be an object")
    supplied = evidence.pop("evidence_bundle_sha256", None)
    if not isinstance(supplied, str) or len(supplied) != 64 or any(
        character not in "0123456789abcdef" for character in supplied
    ):
        raise DatValidationError(
            "validation_evidence.evidence_bundle_sha256 must be a lowercase SHA-256"
        )
    try:
        serialized = json.dumps(
            canonical, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise DatValidationError(
            f"build specification is not canonical JSON: {exc}"
        ) from exc
    actual = sha256_bytes(serialized)
    if supplied != actual:
        raise DatValidationError(
            "validation_evidence.evidence_bundle_sha256 does not bind the complete build specification"
        )
    return actual


def normalize_render_rows(
    spec: dict[str, Any], template_attributes: dict[str, tuple[str, ...]], section_order: tuple[str, ...]
) -> list[tuple[str, dict[str, str]]]:
    render_sections = spec.get("render_sections")
    if not isinstance(render_sections, list) or not render_sections:
        raise DatValidationError(
            "render_sections must be a non-empty normalized row plan; do not freehand DAT rows"
        )
    component_contract = _component_contract(spec)
    order_index = {component: index for index, component in enumerate(section_order)}
    seen_components: set[str] = set()
    prior_order = -1
    normalized_rows: list[tuple[str, dict[str, str]]] = []

    for section_index, section in enumerate(render_sections):
        path = f"render_sections[{section_index}]"
        if not isinstance(section, dict):
            raise DatValidationError(f"{path} must be an object")
        component = section.get("component")
        rows = section.get("rows")
        if not isinstance(component, str) or not component:
            raise DatValidationError(f"{path}.component must be a non-empty string")
        if component not in template_attributes:
            raise DatValidationError(f"{path}.component {component!r} is absent from the live template")
        if component not in component_contract:
            raise DatValidationError(
                f"{path}.component {component!r} is absent from the evidence-bound component contract"
            )
        component_evidence = component_contract[component]
        if not isinstance(component_evidence, dict) or component_evidence.get(
            "merge_registered"
        ) is not True:
            raise DatValidationError(
                f"{path}.component {component!r} is not evidence-bound to a registered MERGE operation"
            )
        if component in seen_components:
            raise DatValidationError(f"{path}.component {component!r} is repeated")
        current_order = order_index[component]
        if current_order <= prior_order:
            raise DatValidationError("render_sections must follow live template parent-before-child order")
        prior_order = current_order
        seen_components.add(component)
        if not isinstance(rows, list) or not rows:
            raise DatValidationError(f"{path}.rows must be a non-empty array")

        metadata_attributes = template_attributes[component]
        allowed = set(metadata_attributes)
        for row_index, row in enumerate(rows):
            row_path = f"{path}.rows[{row_index}]"
            if not isinstance(row, dict) or set(row) != {"attributes"}:
                raise DatValidationError(f"{row_path} must contain only an attributes object")
            source_attributes = row.get("attributes")
            if not isinstance(source_attributes, dict):
                raise DatValidationError(f"{row_path}.attributes must be an object")
            unknown = sorted(set(source_attributes) - allowed)
            if unknown:
                raise DatValidationError(
                    f"{row_path} contains attribute(s) absent from the live template: {', '.join(unknown)}"
                )
            normalized: dict[str, str] = {}
            for attribute in metadata_attributes:
                raw_value = source_attributes.get(attribute, "")
                value = _string_value(raw_value, field_path=f"{row_path}.attributes.{attribute}")
                if value and is_nonportable_attribute(attribute):
                    raise DatValidationError(
                        f"{row_path}.attributes.{attribute} is not portable and must remain blank"
                    )
                normalized[attribute] = value
            normalized_rows.append((component, normalized))
    return normalized_rows


def serialize(spec: dict[str, Any], template: bytes, *, template_name: str) -> tuple[bytes, dict[str, Any]]:
    if spec.get("contract_version") != 1:
        raise DatValidationError("contract_version must be 1")
    task = spec.get("task")
    if not isinstance(task, str) or task not in SUPPORTED_TASK_FILES:
        raise DatValidationError(
            "task must be question-library, questionnaire-templates, or questionnaires"
        )
    intent = spec.get("intent")
    if intent not in {"create", "update"}:
        raise DatValidationError("intent must be create or update")
    if intent == "update" and not isinstance(spec.get("update_contract"), dict):
        raise DatValidationError("update intent requires an update_contract object")
    if spec.get("operation") != ALLOWED_OPERATION:
        raise DatValidationError("operation must be MERGE")
    evidence_sha = evidence_bundle_sha256(spec)

    evidence = spec.get("validation_evidence")
    if not isinstance(evidence, dict):
        raise DatValidationError("validation_evidence must be an object")
    main_template = evidence.get("main_template")
    if not isinstance(main_template, dict):
        raise DatValidationError("validation_evidence.main_template must be an object")
    file_name = main_template.get("file_name")
    expected_file_names = SUPPORTED_TASK_FILES[task]
    if file_name not in expected_file_names:
        raise DatValidationError(
            f"task {task!r} requires main_template.file_name to be one of "
            + ", ".join(repr(name) for name in sorted(expected_file_names))
        )
    if Path(template_name).name != file_name:
        raise DatValidationError(
            f"live template path must use the exact registered filename {file_name!r}"
        )
    expected_template_sha = main_template.get("sha256")
    actual_template_sha = sha256_bytes(template)
    if expected_template_sha != actual_template_sha:
        raise DatValidationError(
            "live template SHA-256 differs from validation_evidence.main_template.sha256"
        )
    if main_template.get("merge_registered") is not True:
        raise DatValidationError("main_template.merge_registered must be true")

    contract = parse_template(template, source_name=template_name)
    rows = normalize_render_rows(spec, contract.attributes, contract.section_order)
    output_lines = list(contract.lines)
    for component, mapping in rows:
        output_lines.append(
            ALLOWED_OPERATION
            + "|"
            + component
            + "|"
            + "|".join(mapping[attribute] for attribute in contract.attributes[component])
        )
    content = ("\n".join(output_lines) + "\n").encode("utf-8")
    report = validate_candidate_bytes(
        content,
        template,
        candidate_name=file_name,
        template_name=template_name,
        expected_filename=file_name,
        spec=spec,
        expected_rows=rows,
    )
    report.update(
        {
            "task": task,
            "operation": ALLOWED_OPERATION,
            "evidence_bundle_sha256": evidence_sha,
            "boundary": "CALLER_ATTESTED_CANDIDATE_AWAITING_CORE_REVALIDATION",
        }
    )
    return content, report


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render and validate a Questionnaire-family HDL DAT from a normalized JSON specification."
    )
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument(
        "--receipt-name", default="hdl-dat-validation-receipt.json"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        spec = _read_json(args.spec)
        template = args.template.read_bytes()
        content, report = serialize(spec, template, template_name=str(args.template))
        output_name = report["file_name"]
        if Path(args.receipt_name).name != args.receipt_name or not args.receipt_name.endswith(
            ".json"
        ):
            raise DatValidationError(
                "--receipt-name must be a plain JSON filename inside --output-dir"
            )
        output_path = args.output_dir / output_name
        receipt_path = args.output_dir / args.receipt_name
        if output_path.exists() or receipt_path.exists():
            raise DatValidationError(
                "refusing to overwrite an existing DAT or validation receipt; use a new versioned run directory"
            )
        _atomic_write_new(output_path, content)
        try:
            _atomic_write_new(
                receipt_path,
                (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8"),
            )
        except Exception:
            output_path.unlink(missing_ok=True)
            raise
        result = dict(report)
        result["output_path"] = str(output_path)
        result["receipt_path"] = str(receipt_path)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (OSError, DatValidationError) as exc:
        failure = {
            "status": "blocked",
            "stage": "questionnaire-dat-serialization",
            "failure_class": "input_validation",
            "message": str(exc),
            "recommended_action": "Correct the normalized build specification or live template; do not freehand, publish, or upload a DAT.",
        }
        print(json.dumps(failure, indent=2, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
