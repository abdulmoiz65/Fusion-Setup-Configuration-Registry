#!/usr/bin/env python3
"""Format extracted OpenAPI REST-operation JSON for DI object creation.

Read the JSON produced by the task-local OpenAPI extraction workflow from
standard input and write the Data Integrator payload to standard output.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
import time
from typing import Any


RESPONSE_OBJECT_CODE_OVERRIDES = {
    "/interop/rest/security/v2/report/roleassignmentreport/user": "RoleAssignmentList",
    "/interop/rest/security/v2/role/getavailableroles": "RoleList",
}


def _json_string(value: Any) -> str:
    """Match JavaScript JSON.stringify's compact representation."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _validate_object(raw_object: dict[str, Any]) -> None:
    """Reject an object tree that cannot be represented by DI attributes."""
    structure = raw_object.get("objectStructure")
    attributes = raw_object.get("dataExtractionObjectAttributes")
    attribute_items = attributes.get("items") if isinstance(attributes, dict) else None

    if not isinstance(structure, dict):
        raise ValueError("Each request and response object must contain an objectStructure object.")
    if not isinstance(attribute_items, list):
        raise ValueError(
            "Each request and response object must contain dataExtractionObjectAttributes.items."
        )
    if structure and not attribute_items:
        raise ValueError(
            "A nonempty objectStructure requires flattened dataExtractionObjectAttributes.items."
        )

    attribute_codes: set[str] = set()
    for attribute in attribute_items:
        if not isinstance(attribute, dict):
            raise ValueError("Each flattened attribute must be an object.")
        attribute_code = attribute.get("attributeCode")
        if not isinstance(attribute_code, str) or not attribute_code or attribute_code == "_":
            raise ValueError(
                "Each flattened attribute requires a nonempty attributeCode other than '_'."
            )
        if attribute_code in attribute_codes:
            raise ValueError("Flattened attributeCodes must be unique within an object.")
        attribute_codes.add(attribute_code)


def convert_to_extraction_objects(api_spec: Any, base_id: int = 10000) -> dict[str, Any]:
    """Convert OpenAPI extraction output into DI extraction objects/endpoints."""
    items: list[dict[str, Any]] = []
    endpoints: list[dict[str, Any]] = []
    next_reference_code = base_id

    if not isinstance(api_spec, dict) or not isinstance(api_spec.get("REST Operations"), list):
        raise ValueError("Input must contain a REST Operations array.")

    def prepare_object(raw_object: dict[str, Any]) -> dict[str, Any]:
        nonlocal next_reference_code
        _validate_object(raw_object)
        prepared = copy.deepcopy(raw_object)
        prepared["selectedFlag"] = True
        prepared["baseObjectReferenceCode"] = next_reference_code
        next_reference_code += 1
        return prepared

    for operation in api_spec["REST Operations"]:
        if not isinstance(operation, dict):
            continue

        request_reference_code = None
        response_reference_code = None
        request_key = None
        response_key = None

        request_object = operation.get("requestObject")
        if isinstance(request_object, dict):
            prepared_request = prepare_object(request_object)
            request_reference_code = prepared_request["baseObjectReferenceCode"]
            request_key = prepared_request.get("objectCode")
            items.append(prepared_request)

        response_object = operation.get("responseObject")
        if isinstance(response_object, dict):
            prepared_response = prepare_object(response_object)
            override_code = RESPONSE_OBJECT_CODE_OVERRIDES.get(operation.get("resourcePath"))
            if override_code is not None:
                prepared_response["objectCode"] = override_code
            response_reference_code = prepared_response["baseObjectReferenceCode"]
            response_key = prepared_response.get("objectCode")
            items.append(prepared_response)

        request_parameters = operation.get("requestParameters")
        endpoint = {
            "selectedFlag": True,
            "resourcePath": operation.get("resourcePath"),
            "operationType": operation.get("operationType"),
            "requestObjectCode": request_reference_code,
            "requestKey": request_key,
            "responseObjectCode": response_reference_code,
            "responseKey": response_key,
            "baseSourceEndPointReferenceCode": next_reference_code,
            "requestParameters": request_parameters,
            "responseContentType": operation.get("responseContentType"),
            "description": operation.get("name"),
            "name": operation.get("name"),
        }
        if operation.get("requestContentType") is not None:
            endpoint["requestContentType"] = operation["requestContentType"]
        endpoints.append(endpoint)
        next_reference_code += 1

    return {
        "dataExtractionObjects": {"items": items},
        "sourceEndPoints": {"items": endpoints},
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Format OpenAPI extraction JSON as DI object-definition JSON."
    )
    parser.add_argument(
        "--base-id",
        type=int,
        default=None,
        help="First reference code to assign (default: current Unix time in milliseconds).",
    )
    args = parser.parse_args()

    try:
        api_spec = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Input must be valid JSON: {error}", file=sys.stderr)
        return 2

    try:
        base_id = args.base_id if args.base_id is not None else int(time.time() * 1000)
        output = json.dumps(
            convert_to_extraction_objects(api_spec, base_id), ensure_ascii=False, indent=2
        ) + "\n"
    except (TypeError, ValueError, OSError) as error:
        print(f"Unable to format extraction output: {error}", file=sys.stderr)
        return 3

    try:
        sys.stdout.write(output)
        sys.stdout.flush()
    except OSError as error:
        print(f"Unable to write extraction output: {error}", file=sys.stderr)
        return 4

    return 0


if __name__ == "__main__":
    raise SystemExit(main())