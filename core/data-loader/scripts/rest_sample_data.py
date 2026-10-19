#!/usr/bin/env python3
"""Read one safe sample record from an explicit Fusion FSCM REST collection."""

from __future__ import annotations

import math
import re
import urllib.parse
from datetime import date
from dataclasses import dataclass
from typing import Any

if __package__ == "scripts":
    from scripts import data_loader_metadata as metadata
else:
    import data_loader_metadata as metadata


REST_API_VERSION = "11.13.18.05"


@dataclass(frozen=True)
class RestSampleResult:
    discriminator: str
    enriched: bool
    values: dict[str, str]
    reason: str | None = None
    http_status: int | None = None
    item_key: str | None = None


def _resource_from_describe(response: Any, discriminator: str) -> dict[str, Any] | None:
    if not isinstance(response, dict):
        return None
    resources = response.get("Resources")
    if resources is None:
        resources = response.get("resources")
    if isinstance(resources, dict):
        resource = resources.get(discriminator)
        return resource if isinstance(resource, dict) else None
    if isinstance(resources, list):
        for candidate in resources:
            if not isinstance(candidate, dict):
                continue
            candidate_name = next(
                (
                    candidate.get(key)
                    for key in ("name", "resourceName", "collectionName", "discriminator")
                    if candidate.get(key) not in (None, "")
                ),
                None,
            )
            if candidate_name == discriminator:
                return candidate
    return None


def _resource_attributes(response: Any, discriminator: str) -> set[str] | None:
    resource = _resource_from_describe(response, discriminator)
    if resource is None:
        return None

    attributes = resource.get("attributes")
    if attributes is None:
        attributes = resource.get("Attributes")
    if isinstance(attributes, dict):
        return {str(name) for name in attributes}
    if not isinstance(attributes, list):
        return set()

    names: set[str] = set()
    for attribute in attributes:
        if isinstance(attribute, str):
            names.add(attribute)
        elif isinstance(attribute, dict):
            name = attribute.get("name") or attribute.get("Name")
            if name not in (None, ""):
                names.add(str(name))
    return names


def product_attribute_metadata(
    config: dict[str, str],
    top_discriminator: str,
    section_discriminators: tuple[str, ...],
    *,
    getter: metadata.Getter = metadata.get_json,
) -> dict[str, dict[str, dict[str, str]]]:
    """Read product REST titles and descriptions without affecting sample generation."""
    encoded = urllib.parse.quote(top_discriminator, safe="")
    try:
        response = getter(
            config["host"]
            + f"/fscmRestApi/resources/{REST_API_VERSION}/{encoded}/describe",
            config["auth"],
            stage="attribute-details-enrichment",
        )
    except metadata.DataLoadError:
        return {}

    root = _resource_from_describe(response, top_discriminator)
    if root is None:
        return {}

    requested = set(section_discriminators)
    result: dict[str, dict[str, dict[str, str]]] = {}

    def collect(discriminator: str, resource: Any) -> None:
        if not isinstance(resource, dict):
            return
        attributes = resource.get("attributes")
        if discriminator in requested and isinstance(attributes, list):
            section_details: dict[str, dict[str, str]] = {}
            for attribute in attributes:
                if not isinstance(attribute, dict):
                    continue
                raw_name = attribute.get("name") or attribute.get("Name")
                if raw_name in (None, ""):
                    continue
                annotations = attribute.get("annotations")
                description = (
                    annotations.get("description")
                    if isinstance(annotations, dict)
                    else None
                )
                section_details[str(raw_name)] = {
                    "label": str(attribute.get("title") or ""),
                    "description": str(description or ""),
                }
            result[discriminator] = section_details
        children = resource.get("children")
        if isinstance(children, dict):
            for child_discriminator, child_resource in children.items():
                collect(str(child_discriminator), child_resource)

    collect(top_discriminator, root)
    return result


def _data_length(detail: dict[str, Any] | None) -> int | None:
    raw = (detail or {}).get("DataLength")
    try:
        length = int(raw) if raw not in (None, "") else None
    except (TypeError, ValueError):
        return None
    return length if length and length > 0 else None


def _is_date_attribute(detail: dict[str, Any] | None) -> bool:
    data_type = (detail or {}).get("DataType") or (detail or {}).get(
        "AttributeDatatype"
    )
    return str(data_type or "").strip().lower() == "date"


def _format_dat_date(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    match = re.fullmatch(
        r"(\d{4})[-/](\d{2})[-/](\d{2})(?:[T ].*)?", value.strip()
    )
    if match is None:
        return None
    try:
        parsed = date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError:
        return None
    return parsed.strftime("%Y/%m/%d")


def coerce_dat_value(
    value: Any, detail: dict[str, Any] | None, *, object_type: str = ""
) -> str | None:
    """Convert a JSON scalar to DAT-safe text or return None for fallback."""
    if value is None or isinstance(value, (dict, list, tuple)):
        return None
    if object_type == "ADF_REST" and _is_date_attribute(detail) and not isinstance(value, str):
        return None
    if object_type == "ADF_VO" and _is_date_attribute(detail):
        text = _format_dat_date(value)
        if text is None:
            return None
    elif isinstance(value, bool):
        text = "Y" if value else "N"
    elif isinstance(value, int):
        text = str(value)
    elif isinstance(value, float):
        if not math.isfinite(value):
            return None
        text = str(value)
    elif isinstance(value, str):
        text = value
    else:
        return None

    if not text or "|" in text or "\r" in text or "\n" in text:
        return None
    length = _data_length(detail)
    if length is not None and len(text) > length:
        return None
    return text


def probe_rest_sample(
    config: dict[str, str],
    discriminator: str,
    collection_path: str,
    selected_fields: tuple[str, ...],
    details: dict[str, dict[str, Any]],
    *,
    object_type: str = "",
    getter: metadata.Getter = metadata.get_json,
) -> RestSampleResult:
    """Probe one explicit collection; endpoint/data failures become local fallback."""
    base_path = collection_path.rstrip("/")
    try:
        describe = getter(
            config["host"] + base_path + "/describe",
            config["auth"],
            stage="rest-sample-enrichment",
        )
    except metadata.DataLoadError as exc:
        return RestSampleResult(
            discriminator,
            False,
            {},
            reason="describe request failed",
            http_status=exc.http_status,
        )

    available_fields = _resource_attributes(describe, discriminator)
    if available_fields is None:
        return RestSampleResult(
            discriminator, False, {}, reason="exact REST resource was not found"
        )
    if not available_fields:
        return RestSampleResult(
            discriminator, False, {}, reason="REST describe response had no attributes"
        )

    requested_fields = tuple(
        name
        for name in selected_fields
        if name in available_fields and name != "RestAction"
    )
    if not requested_fields:
        return RestSampleResult(
            discriminator, False, {}, reason="no selected DAT fields matched REST attributes"
        )

    query = urllib.parse.urlencode(
        {
            "fields": ",".join(requested_fields),
            "limit": "1",
            "onlyData": "true",
        }
    )
    try:
        response = getter(
            config["host"] + base_path + "/?" + query,
            config["auth"],
            stage="rest-sample-enrichment",
        )
    except metadata.DataLoadError as exc:
        return RestSampleResult(
            discriminator,
            False,
            {},
            reason="sample record request failed",
            http_status=exc.http_status,
        )

    if not isinstance(response, dict) or not isinstance(response.get("items"), list):
        return RestSampleResult(
            discriminator, False, {}, reason="sample record response was malformed"
        )
    items = response["items"]
    if not items:
        return RestSampleResult(
            discriminator, False, {}, reason="REST collection returned no records"
        )
    record = items[0]
    if not isinstance(record, dict):
        return RestSampleResult(
            discriminator, False, {}, reason="first REST record was malformed"
        )

    context = record.get("@context")
    raw_item_key = context.get("key") if isinstance(context, dict) else None
    item_key = (
        str(raw_item_key).strip() if raw_item_key not in (None, "") else None
    )

    values: dict[str, str] = {}
    for name in requested_fields:
        if name not in record:
            continue
        safe_value = coerce_dat_value(
            record[name], details.get(name), object_type=object_type
        )
        if safe_value is not None:
            values[name] = safe_value
    if not values:
        return RestSampleResult(
            discriminator,
            False,
            {},
            reason="first REST record had no usable selected scalar values",
            item_key=item_key,
        )
    return RestSampleResult(discriminator, True, values, item_key=item_key)
