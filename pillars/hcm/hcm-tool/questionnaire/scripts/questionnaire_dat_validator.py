#!/usr/bin/env python3
"""Validate Questionnaire-family HDL DAT artifacts without contacting Fusion."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ALLOWED_OPERATION = "MERGE"
GENERATED_ID_ATTRIBUTES = {
    "AnswerId",
    "AttachmentId",
    "OwnerPersonId",
    "QuestionId",
    "QuestionAnswerId",
    "QuestionContextId",
    "QuestionnaireId",
    "QuestionnaireSectionId",
    "QuestionnaireTemplateId",
    "QstnrSectionId",
    "QstnrTemplateId",
    "RatingModelId",
    "SectionId",
}
AUDIT_ATTRIBUTES = {
    "CreatedBy",
    "CreationDate",
    "LastUpdateDate",
    "LastUpdatedBy",
    "LastUpdateLogin",
}
BOOLEAN_ATTRIBUTES = {
    "AdhocQstn",
    "AllowAdhoc",
    "AllowFormatChg",
    "AllowIntroChg",
    "AllowQstnOrderChg",
    "AllowRespOrderChg",
    "AllowSectionChg",
    "EnableComments",
    "InUse",
    "Mandatory",
    "NewPage",
    "RandomAnswers",
    "RandomQstns",
}
CONTEXT_DIMENSIONS = (
    "LocationName",
    "OrganizationName",
    "JobFunction",
    "JobFamilyName",
)


class DatValidationError(ValueError):
    """A fail-closed local Questionnaire DAT validation error."""

    def __init__(self, message: str, *, line_number: int | None = None) -> None:
        self.line_number = line_number
        prefix = f"Line {line_number}: " if line_number is not None else ""
        super().__init__(prefix + message)


@dataclass(frozen=True)
class TemplateContract:
    source_name: str
    lines: tuple[str, ...]
    section_order: tuple[str, ...]
    attributes: dict[str, tuple[str, ...]]


@dataclass(frozen=True)
class DataRow:
    line_number: int
    operation: str
    component: str
    attributes: dict[str, str]


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _decode_utf8(content: bytes, source_name: str) -> str:
    try:
        return content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise DatValidationError(f"{source_name} must contain valid UTF-8 text") from exc


def _normalized_attribute_name(raw_name: str) -> str:
    return raw_name.split("=", 1)[0]


def is_nonportable_attribute(attribute: str) -> bool:
    return (
        attribute in GENERATED_ID_ATTRIBUTES
        or attribute.endswith("Id")
        or attribute in AUDIT_ATTRIBUTES
        or attribute == "SourceRefTableName"
        or attribute.startswith("SourceRef")
    )


def parse_template(content: bytes, *, source_name: str) -> TemplateContract:
    text = _decode_utf8(content, source_name)
    lines = tuple(text.splitlines())
    section_order: list[str] = []
    attributes: dict[str, tuple[str, ...]] = {}

    for line_number, line in enumerate(lines, start=1):
        if not line:
            continue
        parts = line.split("|")
        directive = parts[0]
        if line == "COMMENT" or line.startswith("COMMENT ") or directive == "COMMENT":
            continue
        if directive != "METADATA":
            raise DatValidationError(
                "the live template must contain only COMMENT, METADATA, and blank lines",
                line_number=line_number,
            )
        if len(parts) < 3 or not parts[1]:
            raise DatValidationError("malformed METADATA line", line_number=line_number)
        component = parts[1]
        if component in attributes:
            raise DatValidationError(
                f"duplicate METADATA component {component!r}", line_number=line_number
            )
        raw_attributes = tuple(parts[2:])
        if any(not value for value in raw_attributes):
            raise DatValidationError(
                f"METADATA component {component!r} contains an empty attribute",
                line_number=line_number,
            )
        normalized = tuple(_normalized_attribute_name(value) for value in raw_attributes)
        if len(normalized) != len(set(normalized)):
            raise DatValidationError(
                f"METADATA component {component!r} repeats an attribute",
                line_number=line_number,
            )
        section_order.append(component)
        attributes[component] = normalized

    if not section_order:
        raise DatValidationError("the live template contains no METADATA sections")
    return TemplateContract(source_name, lines, tuple(section_order), attributes)


def _validate_portable_values(row: DataRow) -> None:
    for attribute, value in row.attributes.items():
        if not value:
            continue
        if attribute in GENERATED_ID_ATTRIBUTES or attribute.endswith("Id"):
            raise DatValidationError(
                f"{row.component}.{attribute} is a generated identifier and must remain blank",
                line_number=row.line_number,
            )
        if attribute in AUDIT_ATTRIBUTES:
            raise DatValidationError(
                f"{row.component}.{attribute} is an audit attribute and must remain blank",
                line_number=row.line_number,
            )
        if attribute == "SourceRefTableName" or attribute.startswith("SourceRef"):
            raise DatValidationError(
                f"{row.component}.{attribute} is a source reference and must remain blank",
                line_number=row.line_number,
            )
        if attribute.endswith("Flag") or attribute in BOOLEAN_ATTRIBUTES:
            if value not in {"Y", "N"}:
                raise DatValidationError(
                    f"{row.component}.{attribute} must be Y or N, not {value!r}",
                    line_number=row.line_number,
                )


def _response_type_pairs_from_spec(
    spec: dict[str, Any] | None,
) -> frozenset[tuple[str, str]] | None:
    """Return exact target-proven HDL response pairs bound to the specification."""
    if spec is None:
        return None
    evidence = spec.get("validation_evidence")
    if not isinstance(evidence, dict):
        raise DatValidationError("spec.validation_evidence must be an object")
    raw_evidence_ids = evidence.get("evidence_ids")
    if not isinstance(raw_evidence_ids, list) or any(
        not isinstance(value, str) or not value for value in raw_evidence_ids
    ):
        raise DatValidationError(
            "spec.validation_evidence.evidence_ids must be an array of non-empty strings"
        )
    evidence_ids = set(raw_evidence_ids)
    raw_pairs = evidence.get("response_type_pairs")
    if raw_pairs is None:
        return frozenset()
    if not isinstance(raw_pairs, list) or not raw_pairs:
        raise DatValidationError(
            "spec.validation_evidence.response_type_pairs must be a non-empty array when supplied"
        )

    pairs: set[tuple[str, str]] = set()
    for index, raw_pair in enumerate(raw_pairs):
        path = f"spec.validation_evidence.response_type_pairs[{index}]"
        if not isinstance(raw_pair, dict):
            raise DatValidationError(f"{path} must be an object")
        question_type = raw_pair.get("question_type")
        response_type_name = raw_pair.get("response_type_name")
        resolver = raw_pair.get("resolver")
        evidence_id = raw_pair.get("evidence_id")
        for field_name, value in (
            ("question_type", question_type),
            ("response_type_name", response_type_name),
            ("resolver", resolver),
            ("evidence_id", evidence_id),
        ):
            if not isinstance(value, str) or not value:
                raise DatValidationError(f"{path}.{field_name} must be a non-empty string")
        if evidence_id not in evidence_ids:
            raise DatValidationError(
                f"{path}.evidence_id is not listed in validation_evidence.evidence_ids"
            )
        pair = (question_type, response_type_name)
        if pair in pairs:
            raise DatValidationError(
                f"{path} duplicates QuestionType/ResponseTypeName pair {pair!r}"
            )
        pairs.add(pair)
    return frozenset(pairs)


def _recruiting_organization_contexts_from_spec(
    spec: dict[str, Any] | None,
) -> dict[tuple[str, str, str, str], dict[str, str]] | None:
    """Return canonical Recruiting organization evidence keyed to a QuestionContext row.

    ``recruitingOrganizationsLOV`` is a discovery view: its Name can be a hierarchy
    label and is therefore not portable for ``QuestionContext.OrganizationName``.
    A build specification that emits an organization context must bind the emitted
    leaf name to a successful canonical ``organizationsLOV`` lookup. Internal IDs
    are deliberately transient and must not be persisted in the specification.
    """
    if spec is None:
        return None
    evidence = spec.get("validation_evidence")
    if not isinstance(evidence, dict):
        raise DatValidationError("spec.validation_evidence must be an object")
    raw_evidence_ids = evidence.get("evidence_ids")
    if not isinstance(raw_evidence_ids, list) or any(
        not isinstance(value, str) or not value for value in raw_evidence_ids
    ):
        raise DatValidationError(
            "spec.validation_evidence.evidence_ids must be an array of non-empty strings"
        )
    evidence_ids = set(raw_evidence_ids)
    raw_contexts = evidence.get("recruiting_organization_contexts")
    if raw_contexts is None:
        return {}
    if not isinstance(raw_contexts, list):
        raise DatValidationError(
            "spec.validation_evidence.recruiting_organization_contexts must be an array"
        )

    contexts: dict[tuple[str, str, str, str], dict[str, str]] = {}
    for index, raw_context in enumerate(raw_contexts):
        path = f"spec.validation_evidence.recruiting_organization_contexts[{index}]"
        if not isinstance(raw_context, dict):
            raise DatValidationError(f"{path} must be an object")
        if any("organizationid" in key.lower() for key in raw_context if isinstance(key, str)):
            raise DatValidationError(
                f"{path} must not persist OrganizationId; it is transient lookup state"
            )
        row_key = raw_context.get("row_key")
        if not isinstance(row_key, dict):
            raise DatValidationError(f"{path}.row_key must be an object")
        values: dict[str, str] = {}
        for field_name in (
            "SubscriberName",
            "QuestionCode",
            "QstnVersionNum",
            "OrganizationName",
        ):
            value = row_key.get(field_name)
            if not isinstance(value, str) or not value:
                raise DatValidationError(
                    f"{path}.row_key.{field_name} must be a non-empty string"
                )
            values[field_name] = value
        for field_name, expected in (
            ("resolver", "resolve_live_recruiting_question_context"),
            ("canonical_source", "organizationsLOV"),
            ("status", "passed"),
        ):
            if raw_context.get(field_name) != expected:
                raise DatValidationError(f"{path}.{field_name} must be {expected!r}")
        evidence_id = raw_context.get("evidence_id")
        if not isinstance(evidence_id, str) or evidence_id not in evidence_ids:
            raise DatValidationError(
                f"{path}.evidence_id must reference validation_evidence.evidence_ids"
            )
        key = tuple(
            values[field_name]
            for field_name in (
                "SubscriberName",
                "QuestionCode",
                "QstnVersionNum",
                "OrganizationName",
            )
        )
        if key in contexts:
            raise DatValidationError(f"{path} duplicates Recruiting organization context {key!r}")
        contexts[key] = {"evidence_id": evidence_id}
    return contexts


def _validate_recruiting_organization_context(
    row: DataRow,
    *,
    canonical_contexts: dict[tuple[str, str, str, str], dict[str, str]] | None,
) -> None:
    """Require a canonical leaf lookup for every emitted organization context."""
    if row.component != "QuestionContext" or not row.attributes.get("OrganizationName"):
        return
    if canonical_contexts is None:
        return
    key = tuple(
        row.attributes.get(field_name, "")
        for field_name in (
            "SubscriberName",
            "QuestionCode",
            "QstnVersionNum",
            "OrganizationName",
        )
    )
    if key not in canonical_contexts:
        raise DatValidationError(
            "QuestionContext.OrganizationName must exactly match one passed canonical "
            "organizationsLOV evidence entry; do not emit a recruitingOrganizationsLOV "
            "hierarchy display name",
            line_number=row.line_number,
        )


def _validate_component_semantics(
    row: DataRow,
    *,
    response_type_pairs: frozenset[tuple[str, str]] | None,
) -> None:
    values = row.attributes
    if row.component == "QuestionContext":
        populated = [name for name in CONTEXT_DIMENSIONS if values.get(name)]
        if len(populated) != 1:
            raise DatValidationError(
                "QuestionContext must populate exactly one of LocationName, "
                "OrganizationName, JobFunction, or JobFamilyName",
                line_number=row.line_number,
            )
        missing_parent = [
            name
            for name in ("SubscriberName", "QuestionCode", "QstnVersionNum")
            if not values.get(name)
        ]
        if missing_parent:
            raise DatValidationError(
                "QuestionContext is missing parent key attribute(s): "
                + ", ".join(missing_parent),
                line_number=row.line_number,
            )

    if row.component == "Question" and "ConditionDisplay" in values:
        condition_display = values.get("ConditionDisplay", "")
        condition_fields = (
            "ConditionQuestionCode",
            "ConditionQstnVersionNum",
            "ConditionAnswerCode",
        )
        populated = [name for name in condition_fields if values.get(name)]
        if condition_display == "Y" and len(populated) != len(condition_fields):
            raise DatValidationError(
                "ConditionDisplay=Y requires ConditionQuestionCode, "
                "ConditionQstnVersionNum, and ConditionAnswerCode",
                line_number=row.line_number,
            )
        if condition_display not in {"", "Y", "N"}:
            raise DatValidationError(
                f"Question.ConditionDisplay must be Y or N, not {condition_display!r}",
                line_number=row.line_number,
            )
        if condition_display != "Y" and populated:
            raise DatValidationError(
                "conditional reference fields require ConditionDisplay=Y",
                line_number=row.line_number,
            )

    if row.component == "Question" and (
        "QuestionType" in values or "ResponseTypeName" in values
    ):
        question_type = values.get("QuestionType", "")
        response_type_name = values.get("ResponseTypeName", "")
        if bool(question_type) != bool(response_type_name):
            raise DatValidationError(
                "QuestionType and ResponseTypeName must be supplied together",
                line_number=row.line_number,
            )
        if question_type and response_type_name and response_type_pairs is not None:
            pair = (question_type, response_type_name)
            if pair not in response_type_pairs:
                raise DatValidationError(
                    "QuestionType/ResponseTypeName pair "
                    f"{pair!r} is absent from the exact target-proven "
                    "validation_evidence.response_type_pairs catalog; "
                    "ResponseTypeName must be the HDL display Name and never an FSM "
                    "ResponseTypeCode",
                    line_number=row.line_number,
                )


def _required_attributes_from_spec(spec: dict[str, Any] | None) -> dict[str, tuple[str, ...]]:
    if spec is None:
        return {}
    evidence = spec.get("validation_evidence")
    if not isinstance(evidence, dict):
        raise DatValidationError("spec.validation_evidence must be an object")
    component_contract = evidence.get("component_contract")
    if not isinstance(component_contract, dict):
        raise DatValidationError(
            "spec.validation_evidence.component_contract must be an object"
        )
    result: dict[str, tuple[str, ...]] = {}
    for component, contract in component_contract.items():
        if not isinstance(component, str) or not isinstance(contract, dict):
            raise DatValidationError("each component contract must be an object")
        required = contract.get("required_attributes", [])
        if not isinstance(required, list) or any(not isinstance(item, str) for item in required):
            raise DatValidationError(
                f"component contract {component!r} has invalid required_attributes"
            )
        result[component] = tuple(required)
    return result


def validate_candidate_bytes(
    candidate: bytes,
    template: bytes,
    *,
    candidate_name: str,
    template_name: str,
    expected_filename: str | None = None,
    spec: dict[str, Any] | None = None,
    expected_rows: Iterable[tuple[str, dict[str, str]]] | None = None,
) -> dict[str, Any]:
    if expected_filename and Path(candidate_name).name != expected_filename:
        raise DatValidationError(
            f"candidate filename must be exactly {expected_filename!r}, not {Path(candidate_name).name!r}"
        )

    contract = parse_template(template, source_name=template_name)
    candidate_text = _decode_utf8(candidate, candidate_name)
    candidate_lines = tuple(candidate_text.splitlines())
    if len(candidate_lines) < len(contract.lines) or candidate_lines[: len(contract.lines)] != contract.lines:
        raise DatValidationError(
            "candidate must preserve the exact live template COMMENT, METADATA, and blank lines"
        )

    required_by_component = _required_attributes_from_spec(spec)
    response_type_pairs = _response_type_pairs_from_spec(spec)
    recruiting_organization_contexts = _recruiting_organization_contexts_from_spec(spec)
    rows: list[DataRow] = []
    section_counts = {component: 0 for component in contract.section_order}
    for line_number, line in enumerate(
        candidate_lines[len(contract.lines) :], start=len(contract.lines) + 1
    ):
        if not line:
            raise DatValidationError(
                "blank lines are not allowed after the first data row", line_number=line_number
            )
        parts = line.split("|")
        if len(parts) < 2:
            raise DatValidationError("malformed data row", line_number=line_number)
        operation, component = parts[0], parts[1]
        if operation != ALLOWED_OPERATION:
            raise DatValidationError(
                f"unsupported data instruction {operation!r}; only MERGE is permitted",
                line_number=line_number,
            )
        attributes = contract.attributes.get(component)
        if attributes is None:
            raise DatValidationError(
                f"data row uses unknown component {component!r}", line_number=line_number
            )
        values = parts[2:]
        if len(values) != len(attributes):
            raise DatValidationError(
                f"{component} has {len(values)} values but its METADATA declares "
                f"{len(attributes)} attributes",
                line_number=line_number,
            )
        mapping = dict(zip(attributes, values, strict=True))
        row = DataRow(line_number, operation, component, mapping)
        _validate_portable_values(row)
        _validate_component_semantics(
            row, response_type_pairs=response_type_pairs
        )
        _validate_recruiting_organization_context(
            row, canonical_contexts=recruiting_organization_contexts
        )
        missing = [name for name in required_by_component.get(component, ()) if not mapping.get(name)]
        if missing:
            raise DatValidationError(
                f"{component} is missing required attribute(s): {', '.join(missing)}",
                line_number=line_number,
            )
        rows.append(row)
        section_counts[component] += 1

    if not rows:
        raise DatValidationError("candidate contains no MERGE data rows")
    if rows[0].component != contract.section_order[0]:
        raise DatValidationError(
            f"candidate must begin with live root component {contract.section_order[0]!r}"
        )

    populated_components = [component for component in contract.section_order if section_counts[component]]
    actual_component_order: list[str] = []
    for row in rows:
        if not actual_component_order or actual_component_order[-1] != row.component:
            actual_component_order.append(row.component)
    if actual_component_order != populated_components:
        raise DatValidationError(
            "data components must be contiguous and follow live template parent-before-child order"
        )

    if expected_rows is not None:
        expected = list(expected_rows)
        actual = [(row.component, row.attributes) for row in rows]
        if actual != expected:
            raise DatValidationError(
                "round-trip validation failed: parsed DAT rows differ from the build specification"
            )

    return {
        "status": "passed",
        "failure_class": None,
        "file_name": Path(candidate_name).name,
        "sha256": sha256_bytes(candidate),
        "template_sha256": sha256_bytes(template),
        "row_count": len(rows),
        "section_row_counts": {
            component: count for component, count in section_counts.items() if count
        },
        "checks": [
            "utf8",
            "exact_filename",
            "exact_template_preamble",
            "registered_component",
            "registered_operation",
            "metadata_value_parity",
            "portable_attribute_boundary",
            "questionnaire_semantics",
            "canonical_recruiting_organization_context",
            "required_attributes",
            "parent_before_child_order",
            "round_trip" if expected_rows is not None else "round_trip_not_requested",
        ],
    }


def _atomic_write_new(path: Path, content: bytes) -> None:
    if path.exists():
        raise DatValidationError(f"refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError as exc:
            raise DatValidationError(f"refusing to overwrite existing file: {path}") from exc
    finally:
        temporary.unlink(missing_ok=True)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DatValidationError(f"unable to read JSON specification {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise DatValidationError("JSON specification root must be an object")
    return value


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a Questionnaire-family HDL DAT against its exact live template."
    )
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--spec", type=Path)
    parser.add_argument("--expected-filename")
    parser.add_argument("--report", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        spec = _read_json(args.spec) if args.spec else None
        template_bytes = args.template.read_bytes()
        expected_rows = None
        evidence_sha = None
        expected_filename = args.expected_filename
        if spec is not None:
            try:
                from questionnaire_dat_serializer import (
                    evidence_bundle_sha256,
                    normalize_render_rows,
                )
            except ModuleNotFoundError:
                from scripts.questionnaire_dat_serializer import (  # type: ignore[no-redef]
                    evidence_bundle_sha256,
                    normalize_render_rows,
                )
            evidence_sha = evidence_bundle_sha256(spec)
            evidence = spec.get("validation_evidence")
            main_template = evidence.get("main_template") if isinstance(evidence, dict) else None
            if not isinstance(main_template, dict):
                raise DatValidationError(
                    "validation_evidence.main_template must be an object"
                )
            registered_filename = main_template.get("file_name")
            if not isinstance(registered_filename, str) or not registered_filename:
                raise DatValidationError(
                    "validation_evidence.main_template.file_name must be a non-empty string"
                )
            if expected_filename and expected_filename != registered_filename:
                raise DatValidationError(
                    "--expected-filename conflicts with validation_evidence.main_template.file_name"
                )
            expected_filename = registered_filename
            if Path(args.template).name != registered_filename:
                raise DatValidationError(
                    f"live template path must use the exact registered filename {registered_filename!r}"
                )
            if main_template.get("sha256") != sha256_bytes(template_bytes):
                raise DatValidationError(
                    "live template SHA-256 differs from validation_evidence.main_template.sha256"
                )
            template_contract = parse_template(
                template_bytes, source_name=str(args.template)
            )
            expected_rows = normalize_render_rows(
                spec,
                template_contract.attributes,
                template_contract.section_order,
            )
        report = validate_candidate_bytes(
            args.candidate.read_bytes(),
            template_bytes,
            candidate_name=str(args.candidate),
            template_name=str(args.template),
            expected_filename=expected_filename,
            spec=spec,
            expected_rows=expected_rows,
        )
        if evidence_sha is not None:
            report["evidence_bundle_sha256"] = evidence_sha
        output = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.report:
            _atomic_write_new(args.report, output.encode("utf-8"))
        print(output, end="")
        return 0
    except (OSError, ValueError) as exc:
        failure = {
            "status": "blocked",
            "stage": "questionnaire-dat-validation",
            "failure_class": "input_validation",
            "message": str(exc),
            "recommended_action": "Correct the build specification or live template; do not publish or upload the DAT.",
        }
        print(json.dumps(failure, indent=2, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
