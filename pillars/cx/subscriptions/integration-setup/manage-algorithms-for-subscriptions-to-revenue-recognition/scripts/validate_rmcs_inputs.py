#!/usr/bin/env python3
"""Read-only RMCS attachment identity gates; no writes or live calls.

The structural summary identifies candidates, not an approved action or import.
Default limits: 20 MiB per input and 5 MiB per XML.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any
import xml.etree.ElementTree as ET


ALGORITHM_NAME = "Subscription Management and RMCS Integration"
ALGORITHM_FILENAME = "Algorithm_BO.xml"
MIB = 1024 * 1024
DEFAULT_MAX_XML_BYTES = 5 * MIB


class InputError(ValueError):
    """A safe, static diagnostic without attachment contents or local paths."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _error(code: str, message: str) -> None:
    raise InputError(code, message)


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _children(element: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in element if _local_name(child.tag) == name]


def _one(element: ET.Element, name: str, code: str) -> ET.Element:
    matches = _children(element, name)
    if len(matches) != 1:
        _error(code, "A required XML element is missing or duplicated.")
    return matches[0]


def _scalar(element: ET.Element, name: str, code: str) -> str:
    child = _one(element, name, code)
    if len(child) or child.get("null") == "true":
        _error(code, "A required XML scalar is nested or explicitly null.")
    return child.text or ""


def _optional_scalar(element: ET.Element, name: str) -> str | None:
    matches = _children(element, name)
    if len(matches) != 1 or len(matches[0]) or matches[0].get("null") == "true":
        return None
    return matches[0].text or ""


def _parse_xml(data: bytes, label: str, max_xml_bytes: int) -> ET.Element:
    if not data or len(data) > max_xml_bytes:
        _error(label + "_size", "XML is empty or exceeds the configured size limit.")
    # Removing NULs also catches declarations in UTF-16/UTF-32 encoded XML.
    if re.search(br"<!\s*(?:DOCTYPE|ENTITY)\b", data.replace(b"\x00", b""), re.I):
        _error(label + "_unsafe_xml", "DOCTYPE and ENTITY declarations are prohibited.")
    try:
        return ET.fromstring(data)
    except (ET.ParseError, ValueError, LookupError):
        _error(label + "_malformed_xml", "The attachment is not well-formed XML.")


def _step_summary(version: ET.Element) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "header_candidates": 0,
        "line_candidates": 0,
        "subline_candidates": 0,
        "unknown_steps": 0,
    }
    groups = _children(version, "StepSetup")
    if len(groups) != 1:
        summary["structure_requires_review"] = True
        return summary
    steps = _children(groups[0], "StepSetupVORow")
    for step in steps:
        sets = _children(step, "StepSetSetup")
        if len(sets) != 1:
            summary["unknown_steps"] += 1
            continue
        rows = _children(sets[0], "StepSetSetupVORow")
        primary = [row for row in rows if _optional_scalar(row, "PrimarySetFlag") == "Y"]
        if len(primary) != 1:
            summary["unknown_steps"] += 1
            continue
        alias = _optional_scalar(primary[0], "SetAlias")
        path = _optional_scalar(primary[0], "SetName")
        target = _optional_scalar(step, "TargetLookupSet")
        sublines = [row for row in rows if (
            _optional_scalar(row, "SetAlias") == "RmcsDocSublines"
            and _optional_scalar(row, "SetName") == "RMCSInterface.RmcsDocSublines"
        )]
        if alias == "RmcsDoc" and path == "RMCSInterface.RmcsDoc" and target == "Subscription":
            summary["header_candidates"] += 1
        elif alias == "RmcsDocLines" and path == "RMCSInterface.RmcsDocLines":
            if target == "RmcsDocSublines" and len(sublines) == 1 and (
                _optional_scalar(sublines[0], "PrimarySetFlag") == "N"
                and _optional_scalar(sublines[0], "Cardinality") == "MANY"
            ):
                summary["subline_candidates"] += 1
            elif target == "Products" and not sublines:
                summary["line_candidates"] += 1
            else:
                summary["unknown_steps"] += 1
        else:
            summary["unknown_steps"] += 1
    summary["step_count"] = len(steps)
    summary["structure_requires_review"] = bool(
        summary["unknown_steps"] or summary["header_candidates"] != 1
        or summary["line_candidates"] != 1 or summary["subline_candidates"] > 1
    )
    return summary


def validate_bytes(
    algorithm_xml: bytes,
    service_mapping_xml: bytes,
    *,
    max_xml_bytes: int = DEFAULT_MAX_XML_BYTES,
) -> dict[str, Any]:
    """Validate in-memory XML inputs; return safe JSON-compatible diagnostics.

    This API validates XML identity. It never changes either XML or validates
    executable Groovy.
    """
    result: dict[str, Any] = {
        "status": "blocked",
        "failure_class": "input_validation",
        "algorithm_xml_sha256": hashlib.sha256(algorithm_xml).hexdigest(),
        "service_mapping_xml_sha256": hashlib.sha256(service_mapping_xml).hexdigest(),
        "errors": [],
    }
    try:
        algorithm = _parse_xml(algorithm_xml, "algorithm", max_xml_bytes)
        mapping = _parse_xml(service_mapping_xml, "service_mapping", max_xml_bytes)
        if _local_name(algorithm.tag) != "AlgorithmSetupVO":
            _error("algorithm_root", "Expected an AlgorithmSetupVO document root.")
        all_algorithm_rows = [e for e in algorithm.iter() if _local_name(e.tag) == "AlgorithmSetupVORow"]
        if len(all_algorithm_rows) != 1:
            _error("algorithm_rows", "Exactly one algorithm row is required.")
        row = _one(algorithm, "AlgorithmSetupVORow", "algorithm_rows")
        if _scalar(row, "Name", "algorithm_name") != ALGORITHM_NAME:
            _error("algorithm_name", "Algorithm Name does not match the required RMCS integration.")
        if _local_name(mapping.tag) != "transformContext" or mapping.get("contextName") != "RMCSInterface":
            _error("mapping_context", "Expected transformContext with exact contextName RMCSInterface.")
        if sum(_local_name(e.tag) == "transformContext" for e in mapping.iter()) != 1:
            _error("mapping_context", "Only one transformContext is permitted.")
        versions_parent = _one(row, "VersionSetup", "algorithm_versions")
        versions = _children(versions_parent, "VersionSetupVORow")
        if not versions:
            _error("algorithm_versions", "The algorithm contains no versions.")
        numbered: dict[int, ET.Element] = {}
        for version in versions:
            raw_number = _scalar(version, "VersionNum", "version_number").strip()
            if not re.fullmatch(r"[0-9]+", raw_number) or len(raw_number) > 32:
                _error("version_number", "Every VersionNum must be a nonnegative integer.")
            number = int(raw_number)
            if number in numbered:
                _error("duplicate_version", "VersionNum values must be numerically unique.")
            numbered[number] = version
        highest = max(numbered)
        selected = numbered[highest]
        if _scalar(selected, "ActiveFlag", "highest_version_active") != "Y":
            _error("highest_version_active", "The highest overall version must have exact ActiveFlag Y; no fallback is allowed.")
        variables_parent = _one(selected, "VariableSetup", "algorithm_variables")
        variables = _children(variables_parent, "VariableSetupVORow")
        custom = [v for v in variables if _optional_scalar(v, "Name") == "CustomizationFlag"]
        if len(custom) != 1:
            _error("customization_flag", "The selected version requires exactly one CustomizationFlag variable.")
        default = _scalar(custom[0], "DefaultValue", "customization_default")
        if not default:
            _error("customization_default", "CustomizationFlag DefaultValue must not be empty.")
        interface = [v for v in variables if _optional_scalar(v, "Name") == "RMCSInterface"]
        if len(interface) != 1:
            _error("interface_variable", "The selected version requires exactly one RMCSInterface variable.")
        context = _scalar(interface[0], "Context", "interface_context")
        context_parts = context.rsplit(".", 1)
        if len(context_parts) != 2 or not all(context_parts):
            _error("interface_context", "RMCSInterface Context must identify a mapping consumer.")
        consumers = [e for e in _children(mapping, "contextConsumer") if e.get("consumerName") == context_parts[1]]
        if len(consumers) != 1:
            _error("mapping_consumer", "The selected RMCSInterface Context requires one matching mapping consumer.")
        consumer = consumers[0]
        if consumer.get("serviceType") != "Algorithm" or consumer.get("serviceName") != ALGORITHM_NAME:
            _error("mapping_consumer_algorithm", "The matching consumer must target the required RMCS Algorithm service.")
        result.update({
            "status": "passed_identity_gates",
            "failure_class": None,
            "algorithm_name": ALGORITHM_NAME,
            "version_count": len(numbered),
            "selected_version": highest,
            "selected_active_flag": "Y",
            "customization_default_is_true": default == "true",
            "step_summary": _step_summary(selected),
            "next_gate": "Review the selected action, data sets, cardinalities, business rule, and approval; identity validation is not import approval.",
        })
    except InputError as exc:
        result["errors"].append({"code": exc.code, "message": str(exc)})
    return result


def _read_input(path: Path, limit: int, label: str) -> bytes:
    try:
        if not path.is_file():
            _error(label + "_file", "A required attachment is missing or is not a regular file.")
        with path.open("rb") as stream:
            data = stream.read(limit + 1)
    except OSError:
        _error(label + "_file", "A required attachment could not be read.")
    if not data or len(data) > limit:
        _error(label + "_size", "An input is empty or exceeds the configured size limit.")
    return data


def _positive_integer(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--algorithm", required=True, type=Path, help="Raw Algorithm_BO.xml file.")
    parser.add_argument("--service-mapping", required=True, type=Path, help="One RMCS transformContext XML/text attachment.")
    parser.add_argument("--max-input-mib", type=_positive_integer, default=20)
    parser.add_argument("--max-xml-mib", type=_positive_integer, default=5)
    args = parser.parse_args(argv)
    fingerprints: dict[str, str] = {}
    try:
        algorithm_input = _read_input(args.algorithm, args.max_input_mib * MIB, "algorithm")
        if args.algorithm.name != ALGORITHM_FILENAME:
            _error("algorithm_filename", "The algorithm input must be the raw Algorithm_BO.xml file.")
        fingerprints["algorithm_input_sha256"] = hashlib.sha256(algorithm_input).hexdigest()
        mapping_input = _read_input(args.service_mapping, args.max_input_mib * MIB, "service_mapping")
        fingerprints["service_mapping_input_sha256"] = hashlib.sha256(mapping_input).hexdigest()
        result = validate_bytes(algorithm_input, mapping_input, max_xml_bytes=args.max_xml_mib * MIB)
        result["algorithm_file_name"] = ALGORITHM_FILENAME
        result.update(fingerprints)
    except InputError as exc:
        result = {
            "status": "blocked", "failure_class": "input_validation",
            "errors": [{"code": exc.code, "message": str(exc)}], **fingerprints,
        }
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["status"] == "passed_identity_gates" else 1


if __name__ == "__main__":
    raise SystemExit(main())
