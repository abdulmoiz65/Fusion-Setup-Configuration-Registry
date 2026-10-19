#!/usr/bin/env python3
"""Resolve documented Profile Management child-load prerequisites read-only.

This helper never uploads or changes Fusion.  It uses only documented LOV GET
resources, requires an exact local match, and reports unsupported dependency
types as blockers rather than guessing an endpoint or an identifier.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.parse
from pathlib import Path
from typing import Any, Callable


DATA_LOADER_SCRIPTS = Path(__file__).resolve().parents[5] / "core" / "data-loader" / "scripts"
SKILL_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(DATA_LOADER_SCRIPTS))
sys.path.insert(0, str(SKILL_SCRIPTS))

import data_loader_metadata as metadata  # noqa: E402
from profile_pagination import validated_page  # noqa: E402


BASE_PATH = "/hcmRestApi/resources/11.13.18.05"
SUPPORTED = frozenset({"profile-content-section", "content-item"})
MODEL_PROFILE_CONFIGURATION = "model-profile-configuration"
BLOCKED = {
    "dff-context-value": "No documented read-only HRT_PROFILE_ITEMS context/value contract is registered for this skill.",
    "attachment-data-type": "No documented profile-attachment data-type LOV contract is registered for this skill.",
    "profile-relationship-target": "No documented model-profile relationship-target readback contract is registered for this skill.",
}


def _collection(
    config: dict[str, Any], path: str, fields: str, *, getter: Callable[..., Any]
) -> list[dict[str, Any]]:
    """Read every documented LOV page before evaluating an exact match."""
    offset, results = 0, []
    while True:
        query = urllib.parse.urlencode(
            {"fields": fields, "limit": "500", "offset": str(offset), "onlyData": "true"}
        )
        response = getter(
            config["host"] + BASE_PATH + path + "?" + query,
            config["auth"],
            stage="profile-dependency-preflight",
        )
        items, has_more = validated_page(
            response,
            offset=offset,
            label="Profile Management dependency LOV",
            stage="profile-dependency-preflight",
            data_load_error=metadata.DataLoadError,
        )
        results.extend(item for item in items if isinstance(item, dict))
        if not has_more:
            return results
        if not items:
            raise metadata.DataLoadError(
                "profile-dependency-preflight",
                "Profile Management dependency LOV pagination did not advance.",
                response={"offset": offset},
            )
        offset += len(items)


def resolve_content_section(
    config: dict[str, Any], profile_type_id: str, section_name: str, *, getter=metadata.get_json
) -> dict[str, Any]:
    """Resolve one profile-type section by the supplied numeric profile type ID and name."""
    supplied_id, supplied_name = profile_type_id.strip(), section_name.strip()
    if not supplied_id.isdigit() or not supplied_name:
        return {"status": "blocked", "dependency": "profile-content-section", "message": "profile_type_id (numeric) and section_name are required."}
    items = _collection(
        config,
        "/profileTypeSectionsLOV",
        "ProfileTypeId,SectionId,Name,SectionContext,DffContextName,TemplateFlag",
        getter=getter,
    )
    matches = [
        item for item in items
        if str(item.get("ProfileTypeId") or "") == supplied_id
        and str(item.get("Name") or "").casefold() == supplied_name.casefold()
    ]
    return _exact("profile-content-section", {"profileTypeId": supplied_id, "sectionName": supplied_name}, matches,
                  ("ProfileTypeId", "SectionId", "Name", "SectionContext", "DffContextName", "TemplateFlag"))


def resolve_profile_type(profile_type_code: str) -> dict[str, Any]:
    """Fail closed until owning Profile Types setup returns an exact target ID."""
    supplied = profile_type_code.strip().upper()
    return {
        "status": "blocked",
        "dependency": "profile-type",
        "requested": {"profileTypeCode": supplied},
        "message": "No supported target Profile Type code-to-ID resolver is registered. Obtain exactly-one Profile Type evidence from the owning Profile Types capability and use model-profile-configuration preflight.",
    }


def resolve_content_item(
    config: dict[str, Any], content_item_id: str, content_item_name: str, *, getter=metadata.get_json
) -> dict[str, Any]:
    """Resolve one content-item LOV value by its returned ID and display name."""
    supplied_id, supplied_name = content_item_id.strip(), content_item_name.strip()
    if not supplied_id.isdigit() or not supplied_name:
        return {"status": "blocked", "dependency": "content-item", "message": "content_item_id (numeric) and content_item_name are required."}
    items = _collection(
        config,
        "/contentItemsLOV",
        "ContentItemId,Name,ContentSectionId",
        getter=getter,
    )
    matches = [
        item for item in items
        if str(item.get("ContentItemId") or "") == supplied_id
        and str(item.get("Name") or "").casefold() == supplied_name.casefold()
    ]
    return _exact("content-item", {"contentItemId": supplied_id, "contentItemName": supplied_name}, matches,
                  ("ContentItemId", "Name", "ContentSectionId"))


def validate_model_profile_configuration_evidence(evidence: Any) -> dict[str, Any]:
    """Validate owner-provided model-profile configuration evidence locally.

    Oracle documents the required configuration, but this skill has no supported
    read-only endpoint for the model-profile flags and value-set binding.  The
    evidence therefore must be returned by the owning Profile Types/Content
    Section capability; this check rejects incomplete or self-asserted values.
    """
    if not isinstance(evidence, dict):
        return {"status": "blocked", "dependency": MODEL_PROFILE_CONFIGURATION, "message": "model profile configuration evidence must be an object."}
    source = evidence.get("source")
    if not isinstance(source, dict) or not all(str(source.get(key) or "").strip() for key in ("owner", "reference", "observed_at")):
        return {"status": "blocked", "dependency": MODEL_PROFILE_CONFIGURATION, "message": "configuration evidence must name its owner, reference, and observation time."}
    profile_type = evidence.get("profile_type")
    if not isinstance(profile_type, dict) or profile_type.get("status") != "exactly-one" or not str(profile_type.get("code") or "").strip() or not str(profile_type.get("id") or "").strip():
        return {"status": "blocked", "dependency": MODEL_PROFILE_CONFIGURATION, "message": "exactly-one Profile Type evidence with code and id is required."}
    additional = evidence.get("additional_information", [])
    if not isinstance(additional, list):
        return {"status": "blocked", "dependency": MODEL_PROFILE_CONFIGURATION, "message": "additional_information must be a list."}
    for item in additional:
        if not isinstance(item, dict) or not str(item.get("name") or "").strip() or item.get("status") != "enabled":
            return {"status": "blocked", "dependency": MODEL_PROFILE_CONFIGURATION, "message": "every requested additional-information flag must have a name and enabled status."}
    sections = evidence.get("sections", [])
    if not isinstance(sections, list):
        return {"status": "blocked", "dependency": MODEL_PROFILE_CONFIGURATION, "message": "sections must be a list."}
    for section in sections:
        if not isinstance(section, dict) or section.get("status") != "exactly-one" or section.get("active") is not True or not str(section.get("section_id") or "").strip() or not str(section.get("section_name") or "").strip():
            return {"status": "blocked", "dependency": MODEL_PROFILE_CONFIGURATION, "message": "every requested section requires exactly-one active Section ID and Section Name evidence."}
        value_set = section.get("value_set")
        if value_set == "not-applicable":
            continue
        if not isinstance(value_set, dict) or value_set.get("status") != "exactly-one" or not str(value_set.get("id") or "").strip() or not str(value_set.get("name") or "").strip():
            return {"status": "blocked", "dependency": MODEL_PROFILE_CONFIGURATION, "message": "every requested section requires exactly-one Value Set evidence or an explicit not-applicable value."}
    canonical = json.dumps(evidence, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return {
        "status": "resolved",
        "dependency": MODEL_PROFILE_CONFIGURATION,
        "match": {
            "ProfileTypeCode": str(profile_type["code"]).strip().upper(),
            "ProfileTypeId": str(profile_type["id"]).strip(),
            "additionalInformation": [str(item["name"]).strip() for item in additional],
            "sectionCount": len(sections),
        },
        "evidence": "Owner-provided exact Profile Type, enabled additional-information, active section, and applicable Value Set evidence.",
        "configuration": evidence,
        "configuration_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
    }


def _exact(dependency: str, requested: dict[str, str], matches: list[dict[str, Any]], fields: tuple[str, ...]) -> dict[str, Any]:
    if len(matches) != 1:
        return {"status": "blocked", "dependency": dependency, "requested": requested, "matchCount": len(matches), "message": "Expected exactly one Fusion dependency match."}
    return {"status": "resolved", "dependency": dependency, "requested": requested,
            "match": {field: matches[0].get(field) for field in fields}}


def preflight(config: dict[str, Any], dependency: str, *, profile_type_code: str = "", profile_type_id: str = "", section_name: str = "", content_item_id: str = "", content_item_name: str = "", model_profile_evidence: Any = None, getter=metadata.get_json) -> dict[str, Any]:
    if dependency == MODEL_PROFILE_CONFIGURATION:
        return validate_model_profile_configuration_evidence(model_profile_evidence)
    if dependency == "profile-type":
        return resolve_profile_type(profile_type_code)
    if dependency == "profile-content-section":
        return resolve_content_section(config, profile_type_id, section_name, getter=getter)
    if dependency == "content-item":
        return resolve_content_item(config, content_item_id, content_item_name, getter=getter)
    return {"status": "blocked", "dependency": dependency, "message": BLOCKED[dependency]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dependency", required=True, choices=sorted((*SUPPORTED, "profile-type", MODEL_PROFILE_CONFIGURATION, *BLOCKED)))
    parser.add_argument("--profile-type-code", default="")
    parser.add_argument("--profile-type-id", default="")
    parser.add_argument("--section-name", default="")
    parser.add_argument("--content-item-id", default="")
    parser.add_argument("--content-item-name", default="")
    parser.add_argument("--model-profile-evidence-json", type=Path)
    parser.add_argument("--properties", default="core/auth/fusionEnv.properties")
    parser.add_argument("--token-cache")
    parser.add_argument("--no-open-browser", action="store_true")
    args = parser.parse_args()
    try:
        evidence = None
        if args.dependency == MODEL_PROFILE_CONFIGURATION:
            if args.model_profile_evidence_json is None:
                raise ValueError("--model-profile-evidence-json is required for model-profile-configuration")
            evidence = json.loads(args.model_profile_evidence_json.read_text(encoding="utf-8"))
            result = preflight({}, args.dependency, model_profile_evidence=evidence)
            print(json.dumps(result, indent=2))
            return 0 if result["status"] == "resolved" else 2
        config = metadata.read_config(Path(args.properties), token_cache=args.token_cache, open_browser=not args.no_open_browser)
        result = preflight(config, args.dependency, profile_type_code=args.profile_type_code, profile_type_id=args.profile_type_id, section_name=args.section_name,
                           content_item_id=args.content_item_id, content_item_name=args.content_item_name)
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "resolved" else 2
    except metadata.DataLoadError as exc:
        print(json.dumps({"status": "failed", "stage": exc.stage, "message": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
