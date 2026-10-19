#!/usr/bin/env python3
"""Read-only prerequisite check for Profile Management child-object loads.

Only registered Data Loader business-object schemas are queried. DFF and
attachment routes remain explicit blockers until their owning adapters provide
a documented preflight and execution contract.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable


DATA_LOADER_SCRIPTS = Path(__file__).resolve().parents[5] / "core" / "data-loader" / "scripts"
sys.path.insert(0, str(DATA_LOADER_SCRIPTS))

import data_loader_metadata as metadata  # noqa: E402


CHILD_OBJECTS = {
    "talent-profile-translation": "TalentProfileTranslation",
    "content-item-translation": "ContentItemTranslation",
    "content-item-rating-description-translation": "ContentItemRatingDescriptionTranslation",
    "talent-model-profile-extra-information-translation": "TalentModelProfileExtraInformationTranslation",
}
ROOT_TEMPLATE_SECTIONS = {
    "content-item": "ProfileItem",
    "content-item-relationship": "ProfileRelation",
    "talent-model-profile-extra-information": "ModelProfileExtraInfo",
    "dff": "ProfileItem",
    "attachment": "ProfileAttachment",
}
REFRESH_REQUIRED = {
    "content-item-translation": {
        "owner": "Fusion HCM integration administrator",
        "navigation": "My Client Groups > Data Exchange > HCM Data Loader > View Business Objects",
        "product_area": "Talent Management",
        "business_object": "Content Item Translation",
        "action": "Search Product Area Talent Management and Business Object Content Item Translation, refresh the returned object, then rerun this preflight.",
        "post_refresh_failure_action": "If the exact preflight still returns HTTP 500 after refresh, record a Fusion provider defect with the sanitized status, product area, business object, and refresh timestamp. Do not generate or upload this route.",
    },
}


def preflight(
    config: dict[str, Any], selection: str, *, loader: Callable[..., Any] = metadata.load_business_object_schema
) -> dict[str, Any]:
    root_section = ROOT_TEMPLATE_SECTIONS.get(selection)
    discriminator = "TalentProfile" if root_section else CHILD_OBJECTS[selection]
    try:
        schema = loader(discriminator, config, allow_aliases=False)
    except metadata.DataLoadError as exc:
        result = {"status": "blocked", "selection": selection, "businessObject": discriminator, "stage": exc.stage, "message": str(exc)}
        if selection in REFRESH_REQUIRED:
            result.update({"remediation": REFRESH_REQUIRED[selection], "nextAction": "Do not prepare or upload this route until preflight resolves the exact schema. A repeated HTTP 500 after refresh is a provider blocker, not a reason to guess an HDL layout."})
        return result
    sections = schema.sections
    if root_section:
        sections = tuple(section for section in schema.sections if section.discriminator == root_section)
        if not sections:
            return {
                "status": "blocked",
                "selection": selection,
                "businessObject": schema.discriminator,
                "stage": "template-section-validation",
                "message": f"TalentProfile did not declare expected section {root_section}.",
            }
    return {
        "status": "resolved",
        "selection": selection,
        "businessObject": schema.discriminator,
        **({"templateSection": root_section} if root_section else {}),
        "schemaFingerprint": metadata.schema_fingerprint(schema),
        "sections": [
            {"discriminator": section.discriminator, "attributes": list(section.attribute_names)}
            for section in sections
        ],
        "nextAction": "Confirm parent keys and required fields against this exact schema before creating an immutable artifact.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", required=True, choices=sorted((*CHILD_OBJECTS, *ROOT_TEMPLATE_SECTIONS)))
    parser.add_argument("--properties", default="core/auth/fusionEnv.properties")
    parser.add_argument("--token-cache")
    parser.add_argument("--no-open-browser", action="store_true")
    parser.add_argument(
        "--bypass-proxy",
        action="store_true",
        help="Use the approved direct route for this read-only Fusion request.",
    )
    args = parser.parse_args()
    if args.bypass_proxy:
        for proxy_variable in ("ALL_PROXY", "HTTP_PROXY", "HTTPS_PROXY", "all_proxy", "http_proxy", "https_proxy"):
            os.environ.pop(proxy_variable, None)
    try:
        config = metadata.read_config(Path(args.properties), token_cache=args.token_cache, open_browser=not args.no_open_browser)
        result = preflight(config, args.selection)
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "resolved" else 2
    except metadata.DataLoadError as exc:
        print(json.dumps({"status": "failed", "stage": exc.stage, "message": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
