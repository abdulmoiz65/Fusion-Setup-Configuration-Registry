#!/usr/bin/env python3
"""Resolve one Questionnaire-family HDL registration from Fusion metadata.

The Data Loader finder can return several template-reference rows for one
business object.  This helper deliberately separates business-object identity
from template-reference history and obtains the current template only from the
selected business object's canonical detail response.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable


class ResolutionError(ValueError):
    """Raised when live metadata cannot prove one authoritative contract."""


def _text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _fingerprint(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ResolutionError(f"Cannot read valid JSON from {path}: {exc}") from exc


def _returned_links(item: dict[str, Any]) -> Iterable[tuple[str, str]]:
    containers: list[Any] = [item.get("links")]
    context = item.get("@context")
    if isinstance(context, dict):
        containers.append(context.get("links"))

    for container in containers:
        if not isinstance(container, list):
            continue
        for link in container:
            if not isinstance(link, dict):
                continue
            relation = _text(link.get("rel")).lower()
            href = _text(link.get("href"))
            if relation and href:
                yield relation, href

    links_object = item.get("_links")
    if isinstance(links_object, dict):
        for relation, link in links_object.items():
            candidates = link if isinstance(link, list) else [link]
            for candidate in candidates:
                if isinstance(candidate, dict) and _text(candidate.get("href")):
                    yield _text(relation).lower(), _text(candidate["href"])


def _collect_complete_pages(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not pages:
        raise ResolutionError("At least one metadata collection page is required")

    rows: list[dict[str, Any]] = []
    seen_page_fingerprints: set[str] = set()
    expected_offset: int | None = None

    for index, page in enumerate(pages):
        if not isinstance(page, dict):
            raise ResolutionError(f"Metadata page {index + 1} is not a JSON object")
        items = page.get("items")
        if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
            raise ResolutionError(f"Metadata page {index + 1} has malformed items")
        count = page.get("count")
        offset = page.get("offset")
        has_more = page.get("hasMore")
        if not isinstance(count, int) or isinstance(count, bool) or count != len(items):
            raise ResolutionError(f"Metadata page {index + 1} has inconsistent count evidence")
        if not isinstance(offset, int) or isinstance(offset, bool) or offset < 0:
            raise ResolutionError(f"Metadata page {index + 1} has invalid offset evidence")
        if index == 0 and offset != 0:
            raise ResolutionError(
                f"Metadata pagination is incomplete because the first supplied offset is {offset}, not 0"
            )
        if not isinstance(has_more, bool):
            raise ResolutionError(f"Metadata page {index + 1} has no boolean hasMore evidence")
        if expected_offset is not None and offset != expected_offset:
            raise ResolutionError(
                f"Metadata pagination did not advance by the prior returned row count: "
                f"expected offset {expected_offset}, got {offset}"
            )
        if index < len(pages) - 1 and not has_more:
            raise ResolutionError("A page was supplied after Fusion reported hasMore=false")
        if index < len(pages) - 1 and not items:
            raise ResolutionError("Fusion returned an empty nonterminal metadata page")

        page_fingerprint = _fingerprint(items)
        if items and page_fingerprint in seen_page_fingerprints:
            raise ResolutionError("Fusion repeated a complete metadata page")
        seen_page_fingerprints.add(page_fingerprint)
        rows.extend(items)
        expected_offset = offset + len(items)

    if pages[-1]["hasMore"]:
        raise ResolutionError("Metadata pagination is incomplete because the final page hasMore=true")

    unique_rows: list[dict[str, Any]] = []
    seen_rows: set[str] = set()
    for row in rows:
        row_fingerprint = _fingerprint(row)
        if row_fingerprint not in seen_rows:
            seen_rows.add(row_fingerprint)
            unique_rows.append(row)
    return unique_rows


def resolve_discovery(
    pages: list[dict[str, Any]], expected_discriminator: str, expected_template_file: str
) -> dict[str, Any]:
    """Resolve one business registration and one returned detail link."""

    rows = _collect_complete_pages(pages)
    exact_discriminator_rows = [
        row for row in rows if _text(row.get("BusObjTopDiscriminator")) == expected_discriminator
    ]
    if exact_discriminator_rows:
        candidates = exact_discriminator_rows
        candidate_basis = "exact_discriminator"
    else:
        candidates = [
            row for row in rows if _text(row.get("TemplateFileName")) == expected_template_file
        ]
        candidate_basis = "exact_template_file"

    if not candidates:
        raise ResolutionError(
            f"No exact {expected_discriminator} registration or {expected_template_file} candidate "
            "was returned by the completed filtered discovery"
        )

    registrations: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in candidates:
        business_object_id = _text(row.get("BusinessObjectId"))
        discriminator = _text(row.get("BusObjTopDiscriminator"))
        if not business_object_id or not discriminator:
            raise ResolutionError(
                "An exact metadata candidate has no complete BusinessObjectId/discriminator identity"
            )
        registrations.setdefault((business_object_id, discriminator), []).append(row)

    if len(registrations) != 1:
        identities = [
            {"BusinessObjectId": key[0], "BusObjTopDiscriminator": key[1]}
            for key in sorted(registrations)
        ]
        raise ResolutionError(
            "Metadata discovery returned multiple distinct business registrations: "
            + json.dumps(identities, sort_keys=True)
        )

    (business_object_id, discriminator), registration_rows = next(iter(registrations.items()))
    returned_links = list(
        dict.fromkeys(link for row in registration_rows for link in _returned_links(row))
    )
    canonical_links = sorted({href for relation, href in returned_links if relation == "canonical"})
    self_links = sorted({href for relation, href in returned_links if relation == "self"})
    preferred_links = canonical_links or self_links
    if len(preferred_links) != 1:
        if not preferred_links:
            raise ResolutionError(
                "The selected registration has no returned canonical or self detail link; "
                "repeat discovery with onlyData=false"
            )
        raise ResolutionError("The selected registration returned conflicting detail links")

    template_references = {
        (
            _text(row.get("TemplateId")),
            _text(row.get("UcmContentId")),
            _text(row.get("TemplateFileName")),
        )
        for row in registration_rows
    }
    return {
        "status": "passed",
        "phase": "discovery",
        "candidate_basis": candidate_basis,
        "BusinessObjectId": business_object_id,
        "BusObjTopDiscriminator": discriminator,
        "registration_count": 1,
        "registration_row_count": len(registration_rows),
        "template_reference_count": len(template_references),
        "detail_link_relation": "canonical" if canonical_links else "self",
        "detail_link": preferred_links[0],
        "current_template_selected": False,
    }


def verify_detail(
    selection: dict[str, Any],
    detail_document: dict[str, Any],
    expected_discriminator: str,
    expected_template_file: str,
) -> dict[str, Any]:
    """Verify identity and select the current template from canonical detail."""

    if selection.get("status") != "passed" or selection.get("phase") != "discovery":
        raise ResolutionError("The discovery selection is not a passed discovery result")

    detail: Any = detail_document
    if isinstance(detail_document, dict) and "items" in detail_document:
        items = detail_document.get("items")
        if not isinstance(items, list) or len(items) != 1 or not isinstance(items[0], dict):
            raise ResolutionError("The detail response did not contain exactly one item")
        detail = items[0]
    if not isinstance(detail, dict):
        raise ResolutionError("The detail response is not a JSON object")

    expected_business_object_id = _text(selection.get("BusinessObjectId"))
    actual_business_object_id = _text(detail.get("BusinessObjectId"))
    actual_discriminator = _text(detail.get("BusObjTopDiscriminator"))
    actual_template_file = _text(detail.get("TemplateFileName"))
    if actual_business_object_id != expected_business_object_id:
        raise ResolutionError("The canonical detail BusinessObjectId does not match discovery")
    if actual_discriminator != expected_discriminator:
        raise ResolutionError(
            f"The canonical detail discriminator is {actual_discriminator!r}, "
            f"not {expected_discriminator!r}"
        )
    if actual_template_file != expected_template_file:
        raise ResolutionError(
            f"The canonical detail template is {actual_template_file!r}, "
            f"not {expected_template_file!r}"
        )

    template_id = _text(detail.get("TemplateId"))
    ucm_content_id = _text(detail.get("UcmContentId"))
    if not template_id or not ucm_content_id:
        raise ResolutionError(
            "The canonical detail does not identify both the current TemplateId and UcmContentId"
        )

    return {
        "status": "passed",
        "phase": "detail",
        "BusinessObjectId": actual_business_object_id,
        "BusObjTopDiscriminator": actual_discriminator,
        "TemplateFileName": actual_template_file,
        "TemplateId": template_id,
        "UcmContentId": ucm_content_id,
        "LastUpdateDate": _text(detail.get("LastUpdateDate")) or None,
        "current_template_selected": True,
        "selection_source": "canonical_business_object_detail",
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Resolve one Questionnaire-family HDL metadata registration"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover = subparsers.add_parser("discover", help="Resolve a registration from collection pages")
    discover.add_argument("--page", action="append", required=True, type=Path)
    discover.add_argument("--expected-discriminator", required=True)
    discover.add_argument("--expected-template-file", required=True)

    detail = subparsers.add_parser("verify-detail", help="Verify canonical business-object detail")
    detail.add_argument("--selection", required=True, type=Path)
    detail.add_argument("--detail", required=True, type=Path)
    detail.add_argument("--expected-discriminator", required=True)
    detail.add_argument("--expected-template-file", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "discover":
            result = resolve_discovery(
                [_load_json(path) for path in args.page],
                args.expected_discriminator,
                args.expected_template_file,
            )
        else:
            result = verify_detail(
                _load_json(args.selection),
                _load_json(args.detail),
                args.expected_discriminator,
                args.expected_template_file,
            )
    except ResolutionError as exc:
        print(json.dumps({"status": "blocked", "message": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
