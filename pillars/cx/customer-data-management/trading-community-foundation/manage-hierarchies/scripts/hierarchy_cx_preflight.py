#!/usr/bin/env python3
"""Expose Core Data Loader's structured CX preflight for Task Hook handoff."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


FDOS_ROOT = Path(__file__).resolve().parents[6]
CORE_DATA_LOADER_ROOT = FDOS_ROOT / "core" / "data-loader"
SUPPORTED_OBJECT_CODES = frozenset({"Hierarchy", "HierarchyNode"})
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class PreflightBridgeError(Exception):
    """A safe, non-mutating preflight result could not be produced."""

    def __init__(self, stage: str, message: str) -> None:
        super().__init__(message)
        self.stage = stage
        self.message = message


def _load_core_data_loader() -> ModuleType:
    root = str(CORE_DATA_LOADER_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
    from scripts import upload_and_initiate  # type: ignore

    return upload_and_initiate


def _stop_before_mutation(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
    raise PreflightBridgeError(
        "approval",
        "Core Data Loader reached a mutation callback during read-only preflight.",
    )


_stop_before_mutation.preflight_only = True  # type: ignore[attr-defined]


def _extract_preflight(error: Any, expected_object_code: str) -> dict[str, Any]:
    if getattr(error, "stage", None) != "approval":
        raise PreflightBridgeError(
            str(getattr(error, "stage", "preflight")),
            str(getattr(error, "message", "Core Data Loader preflight failed.")),
        )

    response = getattr(error, "response", None)
    preflight = response.get("preflight") if isinstance(response, dict) else None
    if not isinstance(preflight, dict):
        raise PreflightBridgeError(
            "preflight-contract",
            "Core Data Loader approval result omitted response.preflight.",
        )

    digest = str(preflight.get("archiveSha256") or "").strip().lower()
    if not SHA256_PATTERN.fullmatch(digest):
        raise PreflightBridgeError(
            "preflight-contract",
            "Core Data Loader preflight omitted a valid archiveSha256.",
        )

    object_code = str(preflight.get("cxImportObjectCode") or "").strip()
    if object_code != expected_object_code:
        raise PreflightBridgeError(
            "preflight-contract",
            "Core Data Loader returned a different CX Import object code.",
        )

    ucm_account = str(preflight.get("cxUcmAccount") or "").strip()
    if not ucm_account:
        raise PreflightBridgeError(
            "preflight-contract",
            "Core Data Loader preflight omitted the resolved CX UCM account.",
        )

    ordered_files: list[dict[str, str]] = []
    for item in preflight.get("cxFiles") or []:
        if not isinstance(item, dict):
            continue
        file_name = str(item.get("fileName") or "").strip()
        role = str(item.get("role") or "").strip()
        if file_name:
            ordered_files.append({"fileName": file_name, "role": role})
    if not ordered_files:
        raise PreflightBridgeError(
            "preflight-contract",
            "Core Data Loader preflight omitted the ordered CX Import files.",
        )

    return {
        "status": "preflight_ready",
        "sourceType": str(preflight.get("sourceType") or "").strip(),
        "objectCode": object_code,
        "ucmAccount": ucm_account,
        "orderedFiles": ordered_files,
        "archiveSha256": digest,
    }


def run_preflight(
    source: Path,
    object_code: str,
    *,
    properties: Path | None = None,
    loader: ModuleType | None = None,
) -> dict[str, Any]:
    if object_code not in SUPPORTED_OBJECT_CODES:
        raise PreflightBridgeError(
            "input-validation",
            "Object code must be exactly Hierarchy or HierarchyNode.",
        )

    loader = loader or _load_core_data_loader()
    config_path = properties or loader.DEFAULT_CONFIG
    try:
        loader.upload_and_initiate_sources(
            (source,),
            config_path,
            run_config_path=loader.DEFAULT_RUN_CONFIG,
            cx_import=True,
            cx_import_object_code=object_code,
            poster=_stop_before_mutation,
        )
    except loader.DataLoadError as error:
        return _extract_preflight(error, object_code)

    raise PreflightBridgeError(
        "preflight-contract",
        "Core Data Loader preflight returned without its required approval stop.",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the Core Data Loader read-only CX preflight and emit its "
            "structured digest for a Manage Hierarchies Task Hook preview."
        )
    )
    parser.add_argument("source", type=Path, help="Hierarchy or HierarchyNode CSV path.")
    parser.add_argument(
        "--object-code",
        required=True,
        choices=sorted(SUPPORTED_OBJECT_CODES),
        help="Exact CX Import object code selected by Manage Hierarchies.",
    )
    parser.add_argument(
        "--properties",
        type=Path,
        help="Optional explicit Fusion OAuth properties path.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = run_preflight(
            args.source,
            args.object_code,
            properties=args.properties,
        )
    except PreflightBridgeError as error:
        print(
            json.dumps(
                {"status": "error", "stage": error.stage, "message": error.message},
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
