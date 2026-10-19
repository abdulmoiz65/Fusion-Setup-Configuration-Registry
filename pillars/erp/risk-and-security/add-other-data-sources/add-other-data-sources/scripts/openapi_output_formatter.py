#!/usr/bin/env python3
"""Format extracted REST operations as Data Integrator connector objects."""

from __future__ import annotations

import copy
import json
import sys
import time
from typing import Any


def _validate_object(raw_object: dict[str, Any]) -> None:
    structure = raw_object.get("objectStructure")
    attributes = raw_object.get("dataExtractionObjectAttributes")
    items = attributes.get("items") if isinstance(attributes, dict) else None
    if not isinstance(structure, dict):
        raise ValueError("Each request and response object must contain an objectStructure object.")
    if not isinstance(items, list):
        raise ValueError("Each request and response object must contain dataExtractionObjectAttributes.items.")
    if structure and not items:
        raise ValueError(
            "A nonempty objectStructure requires flattened dataExtractionObjectAttributes.items."
        )
    codes: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Each flattened attribute must be an object.")
        code = item.get("attributeCode")
        if not isinstance(code, str) or not code or code == "_":
            raise ValueError("Each flattened attribute requires a nonempty attributeCode other than '_'.")
        if code in codes:
            raise ValueError("Flattened attributeCodes must be unique within an object.")
        codes.add(code)


def convert_to_extraction_objects(api_spec: Any, base_id: int | None = None) -> dict[str, Any]:
    if not isinstance(api_spec, dict) or not isinstance(api_spec.get("REST Operations"), list):
        raise ValueError("Input must contain a REST Operations array")
    next_reference_code = base_id if base_id is not None else int(time.time() * 1000)
    objects: list[dict[str, Any]] = []
    endpoints: list[dict[str, Any]] = []

    for operation in api_spec["REST Operations"]:
        if not isinstance(operation, dict):
            raise ValueError("Every REST operation must be an object")
        request_reference = response_reference = None
        request_key = response_key = None

        for field in ("requestObject", "responseObject"):
            raw_object = operation.get(field)
            if not isinstance(raw_object, dict):
                continue
            _validate_object(raw_object)
            prepared = copy.deepcopy(raw_object)
            prepared["selectedFlag"] = True
            prepared["baseObjectReferenceCode"] = next_reference_code
            objects.append(prepared)
            if field == "requestObject":
                request_reference = next_reference_code
                request_key = prepared.get("objectCode")
            else:
                response_reference = next_reference_code
                response_key = prepared.get("objectCode")
            next_reference_code += 1

        endpoint = {
            "selectedFlag": True,
            "resourcePath": operation.get("resourcePath"),
            "operationType": operation.get("operationType"),
            "requestObjectCode": request_reference,
            "requestKey": request_key,
            "responseObjectCode": response_reference,
            "responseKey": response_key,
            "baseSourceEndPointReferenceCode": next_reference_code,
            "requestParameters": operation.get("requestParameters"),
            "responseContentType": operation.get("responseContentType"),
            "description": operation.get("name"),
            "name": operation.get("name"),
        }
        if operation.get("requestContentType") is not None:
            endpoint["requestContentType"] = operation["requestContentType"]
        endpoints.append(endpoint)
        next_reference_code += 1

    return {"dataExtractionObjects": {"items": objects}, "sourceEndPoints": {"items": endpoints}}


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        json.dump(convert_to_extraction_objects(payload), sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Unable to format extraction output: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
