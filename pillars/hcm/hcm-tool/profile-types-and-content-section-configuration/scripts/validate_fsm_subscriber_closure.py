#!/usr/bin/env python3
"""Validate content-subscriber dependency closure in a Profile Types FSM ZIP.

The validator is local and read-only. It verifies that every subscriber-scoped
section-property row has exactly one matching content-source relationship and
that every subscriber-property translation has a matching base property row.
Explicitly requested subscribers can also be required by exact business key.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Iterable, Mapping, Sequence


CONTENT_SOURCE_MEMBER = "ORA_HRT_PROFILE_TYPE_CONTENT_SOURCE.csv"
SUBSCRIBER_PROPERTY_MEMBER = (
    "ORA_HRT_PROFILE_TYPE_SUBSCRIBER_PROFILE_TYPE_SECTION_PROP.csv"
)
SUBSCRIBER_PROPERTY_TRANSLATION_MEMBER = (
    "ORA_HRT_PROFILE_TYPE_SUBSCRIBER_PROFILE_TYPE_SECTION_PROP_TRANSLATION.csv"
)

RELATIONSHIP_FIELDS = (
    "ORA_HRT_PROFILE_TYPE_SECTIONS.ProfileTypeCode",
    "ORA_HRT_PROFILE_TYPE_SECTIONS.ContentTypeContextName",
    "ORA_HRT_PROFILE_TYPE_SECTIONS.SectionContext",
    "SourceCode",
)
SUBSCRIBER_FIELDS = (
    "ProfileTypeCode",
    "ContextName",
    "SectionContext",
    "SourceCode",
)
SUBSCRIBER_PROPERTY_FIELDS = (*SUBSCRIBER_FIELDS, "FieldName")


class SubscriberClosureError(ValueError):
    """Raised when an FSM subscriber dependency is missing or ambiguous."""


def _archive_member(
    archive: zipfile.ZipFile, basename: str
) -> str | None:
    matches = [name for name in archive.namelist() if Path(name).name == basename]
    if len(matches) > 1:
        raise SubscriberClosureError(
            f"FSM archive must contain at most one {basename}; found {len(matches)}."
        )
    return matches[0] if matches else None


def _read_optional_csv(
    archive: zipfile.ZipFile,
    basename: str,
    required_fields: Sequence[str],
) -> list[dict[str, str]]:
    member = _archive_member(archive, basename)
    if member is None:
        return []
    try:
        text = archive.read(member).decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise SubscriberClosureError(f"{basename} must be UTF-8 encoded.") from error
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if reader.fieldnames is None:
        raise SubscriberClosureError(f"{basename} has no header row.")
    missing = [field for field in required_fields if field not in reader.fieldnames]
    if missing:
        raise SubscriberClosureError(
            f"{basename} is missing required column(s): {', '.join(missing)}."
        )
    return [
        {key: str(value or "").strip() for key, value in row.items()}
        for row in reader
        if any(str(value or "").strip() for value in row.values())
    ]


def _relationship_key(row: Mapping[str, str]) -> tuple[str, str, str, str]:
    values = [str(row.get(field) or "").strip() for field in RELATIONSHIP_FIELDS]
    return values[0], values[1], values[2], values[3]


def _subscriber_property_key(
    row: Mapping[str, str],
) -> tuple[str, str, str, str, str]:
    values = [
        str(row.get(field) or "").strip() for field in SUBSCRIBER_PROPERTY_FIELDS
    ]
    return values[0], values[1], values[2], values[3], values[4]


def _display_key(key: Iterable[str]) -> str:
    profile_type, context, section, source = list(key)
    return (
        f"ProfileTypeCode={profile_type or '<blank>'}, "
        f"ContextName={context or '<blank>'}, "
        f"SectionContext={section or '<blank>'}, "
        f"SourceCode={source or '<blank>'}"
    )


def _require_complete_key(
    key: tuple[str, ...], member: str, row_number: int
) -> None:
    if any(not value for value in key):
        raise SubscriberClosureError(
            f"{member} row {row_number} has a blank subscriber business-key field."
        )


def parse_expected_subscriber(value: str) -> tuple[str, str, str, str]:
    """Parse PROFILE_TYPE_CODE,CONTEXT_NAME,SECTION_CONTEXT,SOURCE_CODE."""

    parts = tuple(part.strip() for part in value.split(","))
    if len(parts) != 4 or any(not part for part in parts):
        raise argparse.ArgumentTypeError(
            "expected PROFILE_TYPE_CODE,CONTEXT_NAME,SECTION_CONTEXT,SOURCE_CODE"
        )
    return parts[0], parts[1], parts[2], parts[3]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_archive(
    archive_path: Path,
    expected_subscribers: Sequence[tuple[str, str, str, str]] = (),
) -> dict[str, object]:
    """Validate subscriber relationships and return a sanitized result."""

    try:
        with zipfile.ZipFile(archive_path) as archive:
            content_source_member = _archive_member(archive, CONTENT_SOURCE_MEMBER)
            relationship_rows = _read_optional_csv(
                archive, CONTENT_SOURCE_MEMBER, RELATIONSHIP_FIELDS
            )
            property_rows = _read_optional_csv(
                archive, SUBSCRIBER_PROPERTY_MEMBER, SUBSCRIBER_PROPERTY_FIELDS
            )
            translation_rows = _read_optional_csv(
                archive,
                SUBSCRIBER_PROPERTY_TRANSLATION_MEMBER,
                SUBSCRIBER_PROPERTY_FIELDS,
            )
    except (OSError, zipfile.BadZipFile) as error:
        raise SubscriberClosureError(
            f"Unable to read FSM ZIP {archive_path}: {error}"
        ) from error

    if (
        property_rows or translation_rows or expected_subscribers
    ) and content_source_member is None:
        raise SubscriberClosureError(
            f"{CONTENT_SOURCE_MEMBER} is required when a subscriber is requested "
            "or subscriber-property rows are present."
        )

    relationship_keys: list[tuple[str, str, str, str]] = []
    for row_number, row in enumerate(relationship_rows, start=2):
        key = _relationship_key(row)
        _require_complete_key(key, CONTENT_SOURCE_MEMBER, row_number)
        if row.get("SectionContext") and row["SectionContext"] != key[2]:
            raise SubscriberClosureError(
                f"{CONTENT_SOURCE_MEMBER} row {row_number} has inconsistent "
                "SectionContext values."
            )
        relationship_keys.append(key)

    relationship_counts = Counter(relationship_keys)
    duplicates = [key for key, count in relationship_counts.items() if count > 1]
    if duplicates:
        raise SubscriberClosureError(
            "Duplicate content-source relationship for " + _display_key(duplicates[0]) + "."
        )

    property_keys: list[tuple[str, str, str, str, str]] = []
    for row_number, row in enumerate(property_rows, start=2):
        property_key = _subscriber_property_key(row)
        _require_complete_key(property_key, SUBSCRIBER_PROPERTY_MEMBER, row_number)
        relation_key = property_key[:4]
        if relationship_counts[relation_key] != 1:
            raise SubscriberClosureError(
                f"{SUBSCRIBER_PROPERTY_MEMBER} row {row_number} has no matching "
                f"content-source relationship: {_display_key(relation_key)}."
            )
        property_keys.append(property_key)

    property_counts = Counter(property_keys)
    duplicate_properties = [
        key for key, count in property_counts.items() if count > 1
    ]
    if duplicate_properties:
        relation_key = duplicate_properties[0][:4]
        raise SubscriberClosureError(
            "Duplicate subscriber-property row for "
            f"{_display_key(relation_key)}, "
            f"FieldName={duplicate_properties[0][4]}."
        )

    for row_number, row in enumerate(translation_rows, start=2):
        translation_key = _subscriber_property_key(row)
        _require_complete_key(
            translation_key, SUBSCRIBER_PROPERTY_TRANSLATION_MEMBER, row_number
        )
        if property_counts[translation_key] != 1:
            raise SubscriberClosureError(
                f"{SUBSCRIBER_PROPERTY_TRANSLATION_MEMBER} row {row_number} has "
                "no single matching subscriber-property row."
            )

    for expected in expected_subscribers:
        if relationship_counts[expected] != 1:
            raise SubscriberClosureError(
                "Expected subscriber must resolve to exactly one content-source "
                f"relationship; found {relationship_counts[expected]} for "
                f"{_display_key(expected)}."
            )

    return {
        "status": "valid",
        "archive": str(archive_path),
        "sha256": _sha256(archive_path),
        "relationshipRows": len(relationship_rows),
        "subscriberPropertyRows": len(property_rows),
        "subscriberPropertyTranslationRows": len(translation_rows),
        "expectedSubscribers": [
            {
                "profileTypeCode": key[0],
                "contextName": key[1],
                "sectionContext": key[2],
                "sourceCode": key[3],
            }
            for key in expected_subscribers
        ],
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate content-subscriber closure in a Profile Types FSM ZIP."
    )
    parser.add_argument("archive", type=Path, help="Candidate Profile Types FSM ZIP")
    parser.add_argument(
        "--expected-subscriber",
        action="append",
        default=[],
        type=parse_expected_subscriber,
        metavar="PROFILE_TYPE_CODE,CONTEXT_NAME,SECTION_CONTEXT,SOURCE_CODE",
        help=(
            "Require one exact section-to-subscriber relationship; repeat for "
            "each explicitly supplied subscriber."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        result = validate_archive(args.archive, args.expected_subscriber)
    except SubscriberClosureError as error:
        print(json.dumps({"status": "blocked", "error": str(error)}, indent=2))
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
