#!/usr/bin/env python3
"""Resolve Goal Management profile-option intent using a local semantic catalog."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CATALOG = SCRIPT_DIR.parents[1] / "manage-profile-options/ora-resource/profile-option-semantic-catalog.json"


class ProfileResolutionError(ValueError):
    """The semantic-resolution input or catalog is invalid."""


def _text(value: Any, field: str, required: bool = True) -> str | None:
    if value is None and not required:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ProfileResolutionError(f"{field} must be non-empty text")
    return " ".join(value.split())


def _key(value: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", value.casefold()).split())


def _tokens(value: str) -> tuple[str, ...]:
    return tuple(_key(value).split())


def _phrase_positions(value: str, phrase: str) -> list[int]:
    value_tokens = _tokens(value)
    phrase_tokens = _tokens(phrase)
    if not phrase_tokens or len(phrase_tokens) > len(value_tokens):
        return []
    width = len(phrase_tokens)
    return [
        index
        for index in range(len(value_tokens) - width + 1)
        if value_tokens[index:index + width] == phrase_tokens
    ]


def _contains_intent(statement: str, alias: str) -> bool:
    return bool(_phrase_positions(statement, alias))


def _is_negated(tokens: tuple[str, ...], position: int) -> bool:
    preceding = tokens[max(0, position - 2):position]
    return (
        bool(preceding)
        and preceding[-1] in {"not", "never"}
    ) or tuple(preceding[-2:]) in {
        ("do", "not"),
        ("does", "not"),
        ("must", "not"),
        ("should", "not"),
        ("no", "longer"),
    }


def _has_uncertain_language(statement: str) -> bool:
    if "?" in statement:
        return True
    uncertainty_phrases = (
        "whether",
        "not sure",
        "unsure",
        "uncertain",
        "to be determined",
        "tbd",
        "needs review",
        "for review",
        "consider enabling",
        "consider disabling",
    )
    return any(_contains_intent(statement, phrase) for phrase in uncertainty_phrases)


def _catalog(path: Path) -> list[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProfileResolutionError(f"Cannot read profile semantic catalog: {exc}") from exc
    profiles = payload.get("profiles") if isinstance(payload, Mapping) else None
    if not isinstance(profiles, list) or not profiles:
        raise ProfileResolutionError("profile semantic catalog must contain a non-empty profiles array")
    return profiles


def _matches(requirement: Mapping[str, Any], profiles: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    code = _text(requirement.get("profile_option_name"), "profile_option_name", required=False)
    statement = _text(requirement.get("statement"), "statement")
    if code:
        return [profile for profile in profiles if profile.get("profile_option_name", "").casefold() == code.casefold()]
    return [profile for profile in profiles if any(_contains_intent(statement, alias) for alias in profile.get("intent_aliases", []))]


def _requested_value(requirement: Mapping[str, Any], profile: Mapping[str, Any]) -> dict[str, Any] | None:
    values = profile.get("value_mappings", [])
    explicit_value = _text(requirement.get("requested_value"), "requested_value", required=False)
    if explicit_value:
        candidate_key = _key(explicit_value)
        matches = []
        for value in values:
            aliases = [value.get("meaning", ""), *value.get("aliases", [])]
            if any(_key(alias) == candidate_key for alias in aliases if isinstance(alias, str)):
                matches.append(value)
        return matches[0] if len(matches) == 1 else None

    statement = _text(requirement.get("statement"), "statement")
    if _has_uncertain_language(statement):
        return None
    statement_tokens = _tokens(statement)
    values_by_meaning = {
        value.get("meaning"): value
        for value in values
        if isinstance(value.get("meaning"), str)
    }
    evidence: set[str] = set()
    for value in values:
        meaning = value.get("meaning")
        aliases = [meaning or "", *value.get("aliases", [])]
        for alias in aliases:
            if not isinstance(alias, str):
                continue
            for position in _phrase_positions(statement, alias):
                inferred_meaning = meaning
                if _is_negated(statement_tokens, position):
                    if meaning == "enabled":
                        inferred_meaning = "disabled"
                    elif meaning == "disabled":
                        inferred_meaning = "enabled"
                    else:
                        return None
                if isinstance(inferred_meaning, str):
                    evidence.add(inferred_meaning)
    if len(evidence) != 1:
        return None
    return values_by_meaning.get(evidence.pop())


def _question(requirement_id: str, statement: str, reason: str) -> dict[str, str]:
    return {
        "requirement_id": requirement_id,
        "status": "consultant_confirmation_required",
        "question": reason,
        "source_statement": statement,
    }


def resolve(payload: Mapping[str, Any], catalog_path: Path = DEFAULT_CATALOG) -> dict[str, Any]:
    requirements = payload.get("requirements") if isinstance(payload, Mapping) else None
    if not isinstance(requirements, list) or not requirements:
        raise ProfileResolutionError("input must contain a non-empty requirements array")
    profiles = _catalog(catalog_path)
    resolutions = []
    for index, requirement in enumerate(requirements, start=1):
        if not isinstance(requirement, Mapping):
            raise ProfileResolutionError("requirements entries must be objects")
        requirement_id = _text(requirement.get("requirement_id"), "requirement_id", required=False) or f"profile-requirement-{index}"
        statement = _text(requirement.get("statement"), "statement")
        matches = _matches(requirement, profiles)
        if len(matches) != 1:
            reason = "Specify the exact profile option code or a more specific behavior; the skill found no unique Goal Management profile match."
            if len(matches) > 1:
                reason = "Clarify the intended profile option; more than one Goal Management profile matches this behavior."
            resolutions.append(_question(requirement_id, statement, reason))
            continue
        profile = matches[0]
        supplied_product = _text(requirement.get("product_code"), "product_code", required=False)
        if supplied_product and supplied_product.casefold() != str(profile["product_code"]).casefold():
            resolutions.append(_question(requirement_id, statement, f"Confirm product ownership: this profile is cataloged as {profile['product_code']} ({profile['product_name']}), not {supplied_product}."))
            continue
        value = _requested_value(requirement, profile)
        if value is None:
            resolutions.append(_question(requirement_id, statement, "State the desired profile value using one of the profile's supported meanings; the requested value could not be resolved."))
            continue
        supplied_level = _text(requirement.get("level_code"), "level_code", required=False)
        level = supplied_level or profile.get("default_level_code")
        if not isinstance(level, str) or not level.strip():
            resolutions.append(_question(requirement_id, statement, "Provide the profile level; this profile has no declared safe default level."))
            continue
        resolutions.append({
            "requirement_id": requirement_id,
            "status": "resolved",
            "source_statement": statement,
            "source_reference": _text(requirement.get("source_reference"), "source_reference", required=False),
            "profile_option_name": profile["profile_option_name"],
            "product_code": profile["product_code"],
            "product_name": profile["product_name"],
            "level_code": level,
            "level_provenance": "source_supplied" if supplied_level else "catalog_default",
            "requested_meaning": value["meaning"],
            "proposed_stored_value": value["stored_value"],
            "value_provenance": "profile_specific_catalog_mapping",
            "catalog_source": profile.get("source"),
            "execution_preflight": [
                "Read the target-tenant profile definition.",
                "Confirm product ownership, permitted level, and allowed stored value.",
                "Read the current effective value before presenting the immutable update preview."
            ],
        })
    needs_review = any(item["status"] != "resolved" for item in resolutions)
    return {
        "schema_version": "1.0",
        "status": "review_required" if needs_review else "draft",
        "task_mapping_candidate": {
            "Matched Task Name": "Manage Administrator Profile Values",
            "Matched Task Code": "FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES",
            "Offering": "Goal Management",
            "Functional Area": "Goal Management Common",
            "operation_intent": "update"
        },
        "resolutions": resolutions
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        result = resolve(payload, args.catalog)
    except (OSError, json.JSONDecodeError, ProfileResolutionError) as exc:
        parser.error(str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
