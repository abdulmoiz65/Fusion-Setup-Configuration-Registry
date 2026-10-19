#!/usr/bin/env python3
"""Normalize and validate non-Person content-section parent anchors.

The utility is intentionally local: it reads a candidate Profile Types FSM ZIP,
the source-template FSM ZIP, and a previously captured complete read-only
``findByProfileTypeId`` response for Person.  It never calls Fusion and never
overwrites an input archive.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path
from typing import Any, Iterable, Mapping


SECTION_MEMBER = "ORA_HRT_PROFILE_TYPE_SECTIONS.csv"
METADATA_MEMBER = "ASM_SETUP_CSV_METADATA.xml"
PERSON_PROFILE_TYPE_CODE = "PERSON"
SUPPORTED_NON_PERSON_PROFILE_TYPE_CODES = frozenset(
    {
        "JOB",
        "POSITION",
        "ORGANIZATION",
        "TEMPLATE",
        "REQUISITION",
        "PREREQUISITE",
        "GUIDE",
    }
)
PARENT_BUSINESS_KEY_FIELDS = (
    "ParentSectionProfileTypeCode",
    "ParentSectionContextName",
    "ParentSectionSectionContext",
)
PARENT_SURROGATE_FIELDS = (
    "ParentSectionId",
    "ParentSectionContentTypeId",
)
REQUIRED_SECTION_FIELDS = (
    "ProfileTypeCode",
    "ContentTypeContextName",
    "SectionContext",
    "ActiveFlag",
    "TemplateBasedSectionFlag",
    *PARENT_BUSINESS_KEY_FIELDS,
    *PARENT_SURROGATE_FIELDS,
)


class ParentAnchorError(ValueError):
    """Raised when parent-template evidence is missing or ambiguous."""


def _is_true(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().upper() in {"1", "TRUE", "Y", "YES"}


def _archive_member(archive: zipfile.ZipFile, basename: str) -> str:
    matches = [name for name in archive.namelist() if Path(name).name == basename]
    if len(matches) != 1:
        raise ParentAnchorError(
            f"FSM archive must contain exactly one {basename}; found {len(matches)}."
        )
    return matches[0]


def _decode_csv(raw: bytes) -> tuple[str, bool]:
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    try:
        return raw.decode("utf-8-sig"), has_bom
    except UnicodeDecodeError as error:
        raise ParentAnchorError(f"{SECTION_MEMBER} must be UTF-8 encoded.") from error


def _read_sections(
    archive_path: Path,
) -> tuple[list[str], list[dict[str, str]], str, bool]:
    try:
        with zipfile.ZipFile(archive_path) as archive:
            member = _archive_member(archive, SECTION_MEMBER)
            text, has_bom = _decode_csv(archive.read(member))
    except (OSError, zipfile.BadZipFile) as error:
        raise ParentAnchorError(f"Unable to read FSM ZIP {archive_path}: {error}") from error

    reader = csv.DictReader(io.StringIO(text, newline=""))
    if reader.fieldnames is None:
        raise ParentAnchorError(f"{SECTION_MEMBER} has no header row.")
    missing = [name for name in REQUIRED_SECTION_FIELDS if name not in reader.fieldnames]
    if missing:
        raise ParentAnchorError(
            f"{SECTION_MEMBER} is missing required column(s): {', '.join(missing)}."
        )
    return list(reader.fieldnames), list(reader), member, has_bom


def _read_metadata(archive_path: Path) -> tuple[str, bytes]:
    try:
        with zipfile.ZipFile(archive_path) as archive:
            member = _archive_member(archive, METADATA_MEMBER)
            return member, archive.read(member)
    except (OSError, zipfile.BadZipFile) as error:
        raise ParentAnchorError(f"Unable to read FSM ZIP {archive_path}: {error}") from error


def _validate_metadata_matches_source(
    archive_path: Path, source_archive_path: Path
) -> bytes:
    _candidate_member, candidate_metadata = _read_metadata(archive_path)
    _source_member, source_metadata = _read_metadata(source_archive_path)
    if candidate_metadata != source_metadata:
        raise ParentAnchorError(
            f"{METADATA_MEMBER} must remain byte-for-byte identical to the source "
            "FSM package-shape template."
        )
    return source_metadata


def _source_template_for(
    candidate: Mapping[str, str],
    source_rows: Iterable[Mapping[str, str]],
    source_section_context: str | None = None,
) -> Mapping[str, str]:
    profile_type_code = str(candidate.get("ProfileTypeCode") or "").strip()
    if profile_type_code not in SUPPORTED_NON_PERSON_PROFILE_TYPE_CODES:
        raise ParentAnchorError(
            "Parent-anchor validation supports only seeded non-Person profile "
            f"types; found {profile_type_code or '<blank>'!r}."
        )
    matches = [
        row
        for row in source_rows
        if row.get("ProfileTypeCode") == profile_type_code
        and row.get("ContentTypeContextName")
        == candidate.get("ContentTypeContextName")
        and (
            source_section_context is None
            or row.get("SectionContext") == source_section_context
        )
        and _is_true(row.get("ActiveFlag"))
        and _is_true(row.get("TemplateBasedSectionFlag"))
        and bool(str(row.get("ParentSectionSectionContext") or "").strip())
    ]
    if len(matches) != 1:
        section_context = candidate.get("SectionContext") or "<blank>"
        content_context = candidate.get("ContentTypeContextName") or "<blank>"
        selector = (
            f" and source SectionContext {source_section_context!r}"
            if source_section_context
            else ""
        )
        raise ParentAnchorError(
            f"Template-based {profile_type_code} section "
            f"{section_context!r} requires exactly one active source template for "
            f"content context {content_context!r}{selector}; found {len(matches)}."
        )
    return matches[0]


def _lookup_items(parent_lookup: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    if parent_lookup.get("hasMore") is not False:
        raise ParentAnchorError(
            "Person-section lookup must be complete and report hasMore=false."
        )
    items = parent_lookup.get("items")
    if not isinstance(items, list) or not all(isinstance(item, Mapping) for item in items):
        raise ParentAnchorError("Person-section lookup must contain an items array.")
    return items


def resolve_parent_anchor(
    candidate: Mapping[str, str],
    source_rows: Iterable[Mapping[str, str]],
    parent_lookup: Mapping[str, Any],
    source_section_context: str | None = None,
) -> dict[str, str]:
    """Return the exact Person business-key anchor for one non-Person row."""

    source_template = _source_template_for(
        candidate, source_rows, source_section_context
    )
    profile_type_code = str(candidate.get("ProfileTypeCode") or "").strip()
    parent_context_name = str(
        source_template.get("ContentTypeContextName") or ""
    ).strip()
    if not parent_context_name:
        raise ParentAnchorError(
            f"Resolved {profile_type_code} source template has a blank "
            "ContentTypeContextName."
        )
    parent_section_context = str(
        source_template.get("ParentSectionSectionContext") or ""
    ).strip()
    matches = [
        item
        for item in _lookup_items(parent_lookup)
        if str(item.get("ProfileTypeId")) == "1"
        and item.get("SectionContext") == parent_section_context
        and (
            "ActiveFlag" not in item
            or _is_true(item.get("ActiveFlag"))
        )
    ]
    if len(matches) != 1:
        raise ParentAnchorError(
            "Parent section "
            f"{parent_section_context!r} must resolve to exactly one matching "
            f"Person section; found {len(matches)}."
        )

    parent = matches[0]
    return {
        "ParentSectionProfileTypeCode": PERSON_PROFILE_TYPE_CODE,
        "ParentSectionContextName": parent_context_name,
        "ParentSectionSectionContext": str(parent.get("SectionContext") or "").strip(),
        "ParentSectionContentTypeId": "",
        "ParentSectionId": "",
        "TemplateBasedSectionFlag": "Y",
    }


def normalize_rows(
    candidate_rows: Iterable[Mapping[str, str]],
    source_rows: Iterable[Mapping[str, str]],
    parent_lookup: Mapping[str, Any],
    source_section_context: str | None = None,
) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    """Normalize every non-Person row and return rows plus a change summary."""

    source_rows = list(source_rows)
    normalized: list[dict[str, str]] = []
    changes: list[dict[str, Any]] = []
    non_person_count = 0
    for row_number, original in enumerate(candidate_rows, start=2):
        row = dict(original)
        profile_type_code = str(row.get("ProfileTypeCode") or "").strip()
        if profile_type_code != PERSON_PROFILE_TYPE_CODE:
            non_person_count += 1
            expected = resolve_parent_anchor(
                row, source_rows, parent_lookup, source_section_context
            )
            for field, value in expected.items():
                before = row.get(field, "")
                if before != value:
                    changes.append(
                        {
                            "row": row_number,
                            "profileTypeCode": profile_type_code,
                            "sectionContext": row.get("SectionContext", ""),
                            "field": field,
                            "before": before,
                            "after": value,
                        }
                    )
                row[field] = value
        normalized.append(row)
    if non_person_count == 0:
        raise ParentAnchorError(
            "Candidate archive contains no non-Person content-section row."
        )
    return normalized, changes


def validate_rows(
    candidate_rows: Iterable[Mapping[str, str]],
    source_rows: Iterable[Mapping[str, str]],
    parent_lookup: Mapping[str, Any],
    source_section_context: str | None = None,
) -> list[dict[str, Any]]:
    """Validate parent keys and return the resolved anchors."""

    source_rows = list(source_rows)
    validations: list[dict[str, Any]] = []
    non_person_count = 0
    for row_number, row in enumerate(candidate_rows, start=2):
        profile_type_code = str(row.get("ProfileTypeCode") or "").strip()
        if profile_type_code == PERSON_PROFILE_TYPE_CODE:
            continue
        non_person_count += 1
        expected = resolve_parent_anchor(
            row, source_rows, parent_lookup, source_section_context
        )
        differences = {
            field: {"actual": row.get(field, ""), "expected": value}
            for field, value in expected.items()
            if row.get(field, "") != value
        }
        if differences:
            section_context = row.get("SectionContext") or "<blank>"
            fields = ", ".join(sorted(differences))
            raise ParentAnchorError(
                f"Template-based {profile_type_code} section {section_context!r} "
                f"has an invalid parent anchor in: {fields}."
            )
        validations.append(
            {
                "row": row_number,
                "profileTypeCode": profile_type_code,
                "sectionContext": row.get("SectionContext", ""),
                "parentAnchor": {
                    field: expected[field]
                    for field in (*PARENT_BUSINESS_KEY_FIELDS, "TemplateBasedSectionFlag")
                },
            }
        )
    if non_person_count == 0:
        raise ParentAnchorError(
            "Candidate archive contains no non-Person content-section row."
        )
    return validations


def _serialize_sections(
    header: list[str], rows: Iterable[Mapping[str, str]], has_bom: bool
) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=header, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    payload = stream.getvalue().encode("utf-8")
    return (b"\xef\xbb\xbf" + payload) if has_bom else payload


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalize_archive(
    archive_path: Path,
    source_archive_path: Path,
    parent_lookup: Mapping[str, Any],
    output_path: Path,
    source_section_context: str | None = None,
) -> dict[str, Any]:
    """Write one new normalized archive without changing either input archive."""

    if output_path.exists():
        raise ParentAnchorError(f"Output already exists: {output_path}")
    if output_path.resolve() in {archive_path.resolve(), source_archive_path.resolve()}:
        raise ParentAnchorError("Output archive must differ from both input archives.")

    header, candidate_rows, section_member, has_bom = _read_sections(archive_path)
    _source_header, source_rows, _source_member, _source_bom = _read_sections(
        source_archive_path
    )
    normalized_rows, changes = normalize_rows(
        candidate_rows, source_rows, parent_lookup, source_section_context
    )
    section_payload = _serialize_sections(header, normalized_rows, has_bom)

    _source_metadata_member, source_metadata = _read_metadata(source_archive_path)
    try:
        with zipfile.ZipFile(archive_path) as source_archive:
            metadata_member = _archive_member(source_archive, METADATA_MEMBER)
            with zipfile.ZipFile(output_path, "x") as output_archive:
                for info in source_archive.infolist():
                    if info.filename == section_member:
                        payload = section_payload
                    elif info.filename == metadata_member:
                        payload = source_metadata
                    else:
                        payload = source_archive.read(info.filename)
                    output_archive.writestr(info, payload)
        with zipfile.ZipFile(output_path) as normalized_archive:
            metadata_after = normalized_archive.read(metadata_member)
    except (OSError, zipfile.BadZipFile) as error:
        raise ParentAnchorError(f"Unable to write normalized FSM ZIP: {error}") from error

    if source_metadata != metadata_after:
        raise ParentAnchorError(
            f"Normalization failed to preserve source {METADATA_MEMBER} bytes; "
            "discard the output archive."
        )

    _header, output_rows, _member, _bom = _read_sections(output_path)
    validations = validate_rows(
        output_rows, source_rows, parent_lookup, source_section_context
    )
    return {
        "status": "normalized",
        "output": str(output_path),
        "sha256": _sha256(output_path),
        "metadataBytesPreservedFromSource": True,
        "changes": changes,
        "validations": validations,
    }


def validate_archive(
    archive_path: Path,
    source_archive_path: Path,
    parent_lookup: Mapping[str, Any],
    source_section_context: str | None = None,
) -> dict[str, Any]:
    """Validate the final candidate archive without modifying it."""

    _header, candidate_rows, _member, _bom = _read_sections(archive_path)
    _source_header, source_rows, _source_member, _source_bom = _read_sections(
        source_archive_path
    )
    validations = validate_rows(
        candidate_rows, source_rows, parent_lookup, source_section_context
    )
    _validate_metadata_matches_source(archive_path, source_archive_path)
    return {
        "status": "passed",
        "archive": str(archive_path),
        "sha256": _sha256(archive_path),
        "validations": validations,
    }


def validate_rest_rows(candidate_rows, parent_lookup, evidence):
    """Validate portable model anchors against independently captured REST evidence."""
    if str(evidence.get("parent_profile_type_id")) != "1":
        raise ParentAnchorError("REST evidence must identify the Person collection owner.")
    requests = evidence.get("sections")
    if not isinstance(requests, list) or not requests:
        raise ParentAnchorError("REST evidence requires explicit section selections.")
    parents = _lookup_items(parent_lookup)
    content_types = _lookup_items(evidence.get("content_types", {}))
    targets = _lookup_items(evidence.get("target_sections", {}))
    profile_ids = {"JOB": "2", "POSITION": "3", "ORGANIZATION": "4", "TEMPLATE": "5",
                   "REQUISITION": "10", "PREREQUISITE": "11", "GUIDE": "12"}
    target_id = str(evidence.get("target_profile_type_id"))
    if profile_ids.get(evidence.get("target_profile_type_code")) != target_id:
        raise ParentAnchorError("REST target profile ID/code pair is invalid.")
    if any(str(t.get("ProfileTypeId", target_id)) != target_id for t in targets):
        raise ParentAnchorError("REST target collection contains another profile type.")
    validations = []
    model_rows = [r for r in candidate_rows if r.get("ProfileTypeCode") != "PERSON"]
    if (not model_rows or len(requests) != len(model_rows) or
            len({r.get("SectionContext") for r in model_rows}) != len(model_rows)):
        raise ParentAnchorError("REST evidence must cover every model section exactly once.")
    for row in model_rows:
        code = row.get("ProfileTypeCode")
        if code not in SUPPORTED_NON_PERSON_PROFILE_TYPE_CODES or code != evidence.get("target_profile_type_code"):
            raise ParentAnchorError("REST target profile does not match the candidate.")
        selections = [r for r in requests if r.get("section_context") == row.get("SectionContext")]
        if len(selections) != 1 or not selections[0].get("person_section_context"):
            raise ParentAnchorError("An exact independent Person section selection is required.")
        selection = selections[0]
        matches = [p for p in parents if p.get("SectionContext") == selection["person_section_context"]]
        if len(matches) != 1:
            raise ParentAnchorError("REST Person parent must resolve exactly once.")
        parent = matches[0]
        if not _is_true(parent.get("ActiveFlag")) or str(parent.get("ProfileTypeId", "1")) != "1":
            raise ParentAnchorError("REST parent must be active and owned by Person.")
        if not str(parent.get("SectionId", "")).isdigit():
            raise ParentAnchorError("REST parent lacks a valid SectionId.")
        types = [t for t in content_types if str(t.get("ContentTypeId")) == str(parent.get("ContentTypeId"))]
        if len(types) != 1 or not types[0].get("ContextName") or types[0]["ContextName"] != row.get("ContentTypeContextName"):
            raise ParentAnchorError("REST parent content type/context does not match the candidate.")
        if any(t.get("SectionContext") == row.get("SectionContext") or
               str(t.get("ParentSectionId")) == str(parent["SectionId"]) or
               t.get("ParentSectionContext", t.get("ParentSectionSectionContext")) == parent["SectionContext"]
               for t in targets):
            raise ParentAnchorError("The model section or its Person parent is already represented in the target.")
        expected = {"ParentSectionProfileTypeCode": "PERSON",
                    "ParentSectionContextName": types[0]["ContextName"],
                    "ParentSectionSectionContext": parent["SectionContext"],
                    "ParentSectionId": "", "ParentSectionContentTypeId": "",
                    "TemplateBasedSectionFlag": "Y"}
        if any(row.get(k, "") != v for k, v in expected.items()):
            raise ParentAnchorError("Candidate has an invalid REST-derived parent anchor.")
        validations.append({"profileTypeCode": code, "sectionContext": row["SectionContext"], "parentAnchor": expected})
    return validations


def validate_rest_archive(archive_path, source_archive_path, parent_lookup, evidence):
    _validate_metadata_matches_source(archive_path, source_archive_path)
    _header, rows, _member, _bom = _read_sections(archive_path)
    return {"status": "passed", "archive": str(archive_path), "sha256": _sha256(archive_path),
            "evidenceMode": "rest", "validations": validate_rest_rows(rows, parent_lookup, evidence)}


def _read_json(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ParentAnchorError(f"Unable to read parent lookup JSON {path}: {error}") from error
    if not isinstance(value, Mapping):
        raise ParentAnchorError("Parent lookup JSON must contain one object.")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate or normalize parent anchors for every seeded non-Person "
            "content section in a Profile Types FSM ZIP."
        )
    )
    parser.add_argument("archive", type=Path, help="Candidate Profile Types FSM ZIP")
    parser.add_argument("--rest-parent-evidence", type=Path,
                        help="Independent REST parent selections, content types, and target sections; validation only")
    parser.add_argument(
        "--source-template-archive",
        required=True,
        type=Path,
        help=(
            "Current source FSM ZIP containing the selected active template row "
            "for each non-Person target"
        ),
    )
    parser.add_argument(
        "--parent-lookup-json",
        required=True,
        type=Path,
        help=(
            "Complete read-only findByProfileTypeId response for Person captured "
            "as JSON"
        ),
    )
    parser.add_argument(
        "--source-section-context",
        help=(
            "Exact active source-template SectionContext; required when content "
            "type alone matches more than one source row"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write a new normalized ZIP; omit to validate the candidate only",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        parent_lookup = _read_json(args.parent_lookup_json)
        if args.rest_parent_evidence:
            if args.output or args.source_section_context:
                raise ParentAnchorError("REST evidence mode is validation-only; do not combine with output or source-section-context.")
            result = validate_rest_archive(args.archive, args.source_template_archive,
                                           parent_lookup, _read_json(args.rest_parent_evidence))
        elif args.output:
            result = normalize_archive(
                args.archive,
                args.source_template_archive,
                parent_lookup,
                args.output,
                args.source_section_context,
            )
        else:
            result = validate_archive(
                args.archive,
                args.source_template_archive,
                parent_lookup,
                args.source_section_context,
            )
    except ParentAnchorError as error:
        print(json.dumps({"status": "blocked", "error": str(error)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
