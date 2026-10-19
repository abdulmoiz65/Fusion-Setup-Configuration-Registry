#!/usr/bin/env python3
"""Read mandatory root attributes from live Fusion Data Loader metadata."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import data_loader_metadata as metadata
    import data_loader_report
except ModuleNotFoundError:
    from scripts import data_loader_metadata as metadata
    from scripts import data_loader_report


def get_mandatory_attributes(
    business_object: str,
    config_path: Path,
    *,
    auth_options: dict[str, object] | None = None,
) -> dict[str, object]:
    config = metadata.read_config(config_path, **(auth_options or {}))
    schema = metadata.load_business_object_schema(
        business_object,
        config,
        allow_aliases=True,
        sample_attribute_lookup=True,
        allow_attribute_schema_fallback=True,
    )
    attributes = [
        str(attribute.get("AttributeName"))
        for attribute in schema.attributes.get(schema.discriminator, ())
        if metadata.is_mandatory(attribute) and attribute.get("AttributeName")
    ]
    return {
        "BusObjTopDiscriminator": schema.discriminator,
        "UIName": schema.ui_name,
        "attributes": attributes,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List mandatory root attributes from live Fusion Data Loader metadata."
    )
    parser.add_argument("business_object", help="Business-object discriminator, UI name, or template filename.")
    metadata.add_oauth_arguments(parser)
    parser.add_argument(
        "--inline-output",
        type=Path,
        help="Deprecated compatibility option; inline HTML rendering is disabled.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = get_mandatory_attributes(
            args.business_object,
            args.properties,
            auth_options=metadata.oauth_kwargs(args),
        )
    except metadata.DataLoadError as exc:
        data_loader_report.emit_inline_or_markdown(
            exc,
            "error",
            args.inline_output,
            data_loader_report.render_error_report,
            stream=sys.stderr,
        )
        return 1
    data_loader_report.emit_inline_or_markdown(
        result,
        "mandatory-attributes",
        args.inline_output,
        data_loader_report.render_mandatory_attributes_report,
        stream=sys.stdout,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
