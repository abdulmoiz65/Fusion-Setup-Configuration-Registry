#!/usr/bin/env python3
"""Generate the deterministic blank Profile Content Library setup-intake XLSX."""

import argparse
import json
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


CONTRACT_COLUMNS = (
    "complete_set_id",
    "task_code",
    "record_type",
    "local_key",
    "parent_local_key",
    "parent_exact_reference",
    "related_local_key",
    "related_exact_reference",
    "name",
    "code",
    "description",
    "value",
    "language",
    "effective_start_date",
    "effective_end_date",
    "sequence",
    "relationship_code",
    "location",
    "country_code",
    "country_geography_code",
    "state_country_code",
    "state_geography_code",
    "free_form_flag",
    "attribute_label",
    "column_name",
    "default_value",
    "required_flag",
    "display_code",
    "view_attribute_name",
    "rating_model_code",
    "rating_level_code",
    "mandatory_flag",
    "rating_interaction_type",
    "content_supplier_code",
    "additional_values_json",
    "source_reference",
    "review_status",
)
SHEETS = (
    ("Content Types", "content_type", "HRT_MANAGE_PROFILE_CONTENT_TYPES"),
    ("Content Type Properties", "content_type_property", "HRT_MANAGE_PROFILE_CONTENT_TYPES"),
    ("Content Type Relships", "content_type_relationship", "HRT_MANAGE_PROFILE_CONTENT_TYPES"),
    ("Content Items", "content_item", "HRT_MANAGE_PROFILE_CONTENT_ITEMS"),
    ("Item Rating Descriptions", "content_item_proficiency_description", "HRT_MANAGE_PROFILE_CONTENT_ITEMS"),
    ("Content Item Relships", "content_item_relationship", "HRT_MANAGE_PROFILE_CONTENT_ITEMS"),
    ("Item Catalogs", "item_catalog", "ORA_MANAGE_PROFILE_ITEM_CATALOG"),
    ("Catalog Content Items", "item_catalog_membership", "ORA_MANAGE_PROFILE_ITEM_CATALOG"),
    ("Catalog Rating Descriptions", "item_catalog_rating_description", "ORA_MANAGE_PROFILE_ITEM_CATALOG"),
    ("Instance Qualifiers", "instance_qualifier", "HRT_MANAGE_INSTANCE_QUALIFIERS"),
    ("Instance Qualifier Sets", "instance_qualifier_set", "HRT_MANAGE_INSTANCE_QUALIFIERS"),
    ("Educational Establishments", "educational_establishment", "HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS"),
    ("Behavior Item Catalogs", "behavior_item_catalog", "ORA_MANAGE_PROFILE_ITEM_CATALOG"),
    ("Competency Behavior Relships", "competency_behavior_relationship", "HRT_MANAGE_PROFILE_CONTENT_ITEMS"),
)
FIXED_DATE_TIME = (2026, 9, 2, 0, 0, 0)


class TemplateError(ValueError):
    pass


def column_name(index):
    value = index
    result = ""
    while value:
        value, remainder = divmod(value - 1, 26)
        result = chr(65 + remainder) + result
    return result


def inline_cell(reference, value, style=None):
    style_attr = ' s="%s"' % style if style is not None else ""
    return '<c r="%s" t="inlineStr"%s><is><t>%s</t></is></c>' % (
        reference,
        style_attr,
        escape(str(value)),
    )


def worksheet(rows, widths=None, freeze=True):
    cols = ""
    if widths:
        cols = "<cols>" + "".join(
            '<col min="%d" max="%d" width="%s" customWidth="1"/>'
            % (index, index, width)
            for index, width in enumerate(widths, start=1)
        ) + "</cols>"
    pane = '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>' if freeze else '<sheetViews><sheetView workbookViewId="0"/></sheetViews>'
    row_xml = []
    for row_index, row in enumerate(rows, start=1):
        cells = []
        for column_index, value in enumerate(row, start=1):
            if value in (None, ""):
                continue
            cells.append(
                inline_cell(
                    "%s%d" % (column_name(column_index), row_index),
                    value,
                    1 if row_index == 1 else None,
                )
            )
        row_xml.append('<row r="%d">%s</row>' % (row_index, "".join(cells)))
    dimension = "A1:%s%d" % (column_name(max(len(row) for row in rows)), len(rows))
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<dimension ref="%s"/>%s%s<sheetFormatPr defaultRowHeight="15"/>%s'
        '<sheetData>%s</sheetData></worksheet>'
        % (dimension, pane, cols, "", "".join(row_xml))
    ).encode("utf-8")


def content_types(sheet_count):
    overrides = "".join(
        '<Override PartName="/xl/worksheets/sheet%d.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        % index
        for index in range(1, sheet_count + 1)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        '%s</Types>' % overrides
    ).encode("utf-8")


def build_workbook_bytes(output_path):
    sheet_names = ["Instructions"] + [item[0] for item in SHEETS]
    workbook_sheets = "".join(
        '<sheet name="%s" sheetId="%d" r:id="rId%d"/>'
        % (escape(name), index, index)
        for index, name in enumerate(sheet_names, start=1)
    )
    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets>%s</sheets></workbook>' % workbook_sheets
    ).encode("utf-8")
    workbook_relationships = "".join(
        '<Relationship Id="rId%d" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
        'Target="worksheets/sheet%d.xml"/>'
        % (index, index)
        for index in range(1, len(sheet_names) + 1)
    )
    workbook_relationships += (
        '<Relationship Id="rId%d" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
        'Target="styles.xml"/>'
        % (len(sheet_names) + 1)
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">%s</Relationships>'
        % workbook_relationships
    ).encode("utf-8")
    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        '</Relationships>'
    ).encode("utf-8")
    styles = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="2"><font/><font><b/></font></fonts>'
        '<fills count="1"><fill><patternFill patternType="none"/></fill></fills>'
        '<borders count="1"><border/></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
        '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/></cellXfs>'
        '</styleSheet>'
    ).encode("utf-8")
    instructions = [
        ("Profile Management Content Library Configuration Intake", ""),
        ("Purpose", "Blank setup questionnaire and requirements input only; this workbook never authorizes HDL, HSDL, REST, FSM, DAT, or another write."),
        ("Supply the configuration", "Enter the approved records, attributes, parent/child links, and relationships. Supply dates and optional values only when applicable. Business purpose and downstream consumers are not required; Fusion task names may remain blank."),
        ("Input choices", "Enter values directly, use this blank requirements template, or provide an existing readable file. A spreadsheet is the default for repeating rows."),
        ("Complete set", "Use one complete_set_id across every related row on every sheet."),
        ("Required review status", "Retain the actual review status. inferred-pending-review and blocked allow preliminary review but stop executable preview."),
        ("Parent/related references", "Use a local key for a row in this workbook or an exact existing provider reference, never both."),
        ("Source reference", "Identify the source row/page/decision. The normalizer fills Sheet!Row when left blank in this workbook."),
        ("Task and record type", "The normalizer derives task_code and record_type from the sheet; do not repurpose sheets."),
        ("Sensitive data", "Do not enter credentials, tokens, private keys, employee data, or customer-sensitive source contents."),
        ("Provider boundary", "Provider and import-route readiness are evaluated only after populated requirements are reviewed; this blank template makes no provider claim."),
        ("Approval", "Core Data Loader owns approval for the exact immutable archive before Fusion submission. Filling or locally saving this workbook is not load approval."),
    ]
    members = {
        "[Content_Types].xml": content_types(len(sheet_names)),
        "_rels/.rels": root_rels,
        "xl/workbook.xml": workbook,
        "xl/_rels/workbook.xml.rels": rels,
        "xl/styles.xml": styles,
        "xl/worksheets/sheet1.xml": worksheet(instructions, widths=(34, 110), freeze=False),
        "docProps/core.xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>Profile Management Content Library Configuration Intake</dc:title>'
            '<dc:creator>FDOS</dc:creator>'
            '<dcterms:created xsi:type="dcterms:W3CDTF">2026-09-02T00:00:00Z</dcterms:created>'
            '</cp:coreProperties>'
        ).encode("utf-8"),
        "docProps/app.xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
            '<Application>FDOS</Application></Properties>'
        ).encode("utf-8"),
    }
    for offset, _sheet in enumerate(SHEETS, start=2):
        members["xl/worksheets/sheet%d.xml" % offset] = worksheet(
            [CONTRACT_COLUMNS], widths=tuple(24 for _ in CONTRACT_COLUMNS)
        )

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation also rejects existing and dangling symlink destinations.
    # Never replace a supplied workbook with the blank intake template.
    with zipfile.ZipFile(str(output), "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(members):
            info = zipfile.ZipInfo(name, date_time=FIXED_DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            archive.writestr(info, members[name])
    return {
        "status": "generated",
        "workflow_stage": "setup-guidance",
        "fusion_access": "not-required",
        "configuration_rows": 0,
        "output": output.name,
        "sheet_count": len(sheet_names),
        "object_sheet_count": len(SHEETS),
        "object_sheets": [
            {"sheet": name, "record_type": record_type, "task_code": task_code}
            for name, record_type, task_code in SHEETS
        ],
        "columns": list(CONTRACT_COLUMNS),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate the deterministic blank Profile Content Library setup-intake XLSX."
    )
    parser.add_argument("output_xlsx", type=Path)
    args = parser.parse_args(argv)
    if args.output_xlsx.suffix.lower() != ".xlsx":
        parser.error("output path must end in .xlsx")
    try:
        result = build_workbook_bytes(args.output_xlsx)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(json.dumps({
            "status": "blocked",
            "stage": "template_generation",
            "failure_class": "artifact_persistence" if isinstance(exc, OSError) else "input_validation",
            "message": exc.__class__.__name__,
            "recommended_action": "Choose a new safe .xlsx destination; existing files are never overwritten.",
        }, indent=2))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
