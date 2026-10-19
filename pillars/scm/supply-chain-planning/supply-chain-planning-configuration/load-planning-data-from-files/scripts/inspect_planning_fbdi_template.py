#!/usr/bin/env python3
"""Extract compact, same-run Planning XLSM/CTL contracts; never execute macros."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"m": MAIN, "r": REL, "p": PKG_REL}
SKILL = Path(__file__).resolve().parents[1] / "SKILL.md"
TABLE_NAME = re.compile(r"INTO\s+TABLE\s+([A-Z0-9_]+)", re.I)
CSV_FIELD = re.compile(r"^\s*,?\s*([A-Z][A-Z0-9_]*)\b(.*)$")


class ContractError(ValueError):
    """Input or template does not satisfy the documented contract."""


def supported_members() -> dict[str, tuple[str, str]]:
    """Read the single maintained route table in SKILL.md, not a second list."""
    text = SKILL.read_text(encoding="utf-8")
    if text.count("## Supported files\n") != 1:
        raise ContractError("Missing or ambiguous supported-file table in SKILL.md.")
    section = text.split("## Supported files\n", 1)[1].split("\n## ", 1)[0]
    rows = re.findall(
        r"^\| [^|\n]+ \| ([A-Za-z0-9]+\.csv) \| ([A-Za-z0-9]+\.xlsm) \| (MSC_ST_[A-Z_]+) \|$",
        section, re.M)
    if not rows or len({row[0].casefold() for row in rows}) != len(rows):
        raise ContractError("Missing or duplicate supported-file routes in SKILL.md.")
    return {member: (workbook, table) for member, workbook, table in rows}


def validate_members(names: list[str]) -> list[str]:
    routes = supported_members()
    canonical = {name.casefold(): name for name in routes}
    if not names:
        raise ContractError("At least one supported CSV member is required.")
    result = []
    for name in names:
        if not isinstance(name, str) or name.casefold() not in canonical:
            raise ContractError(f"Unsupported CSV member: {name!r}; see SKILL.md.")
        member = canonical[name.casefold()]
        if member in result:
            raise ContractError(f"Duplicate CSV member: {name}")
        result.append(member)
    return result


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def normalized_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def worksheet_matches_control_name(worksheet: str, control_file: str) -> bool:
    # Oracle's trailing "_" tab naming maps directly to the CTL file prefix.
    return normalized_name(worksheet).rstrip("s") == normalized_name(Path(control_file).stem).rstrip("s")


def column_index(cell_ref: str) -> int:
    value = 0
    for char in re.match(r"[A-Z]+", cell_ref).group():
        value = value * 26 + ord(char) - ord("A") + 1
    return value


def row_values(row: ET.Element, strings: list[str]) -> list[str]:
    values = {}
    for cell in row.findall("m:c", NS):
        node = cell.find("m:v", NS)
        value = "" if node is None else node.text or ""
        if cell.get("t") == "s":
            value = strings[int(value)]
        elif cell.get("t") == "inlineStr":
            value = "".join(cell.find("m:is", NS).itertext())
        values[column_index(cell.attrib["r"])] = value
    return [values.get(index, "") for index in range(1, max(values, default=0) + 1)]


def control_contract(path: Path, append_end_marker: bool = True) -> dict:
    member = validate_members([path.with_suffix(".csv").name])[0]
    content = path.read_bytes()
    text = content.decode("utf-8-sig")
    table = TABLE_NAME.search(text)
    if table is None or table.group(1).upper() != supported_members()[member][1]:
        raise ContractError(f"{path.name} targets an unexpected table for {member}.")
    start = text.find("(", table.end())
    fields = []
    for line in text[start + 1:].splitlines():
        match = CSV_FIELD.match(line)
        if match is None:
            continue
        name, expression = match.groups()
        if re.search(r"\b(constant|expression)\b", expression, re.I):
            break
        fields.append(name)
    if start < 0 or not fields or len(set(fields)) != len(fields):
        raise ContractError(f"{path.name} has no unique source-field contract.")
    delimiter = "," if re.search(r'FIELDS\s+TERMINATED\s+BY\s+","', text, re.I) else None
    quote = '"' if re.search(r"""OPTIONALLY\s+ENCLOSED\s+BY\s+'"'""", text, re.I) else None
    if delimiter is None or quote is None:
        raise ContractError(f"{path.name}: unsupported delimiter/quoting contract.")
    return {
        "control_file": path.name, "control_file_path": str(path.resolve()),
        "control_file_sha256": sha256(content), "csv_member": member,
        "target_table": table.group(1).upper(),
        "header_required": bool(re.search(r"\bSKIP\s*=\s*1\b", text, re.I)),
        "delimiter": delimiter, "optionally_enclosed_by": quote,
        "trailing_null_columns": bool(re.search(r"\bTRAILING\s+NULLCOLS\b", text, re.I)),
        "ordered_headers": fields + (["END"] if append_end_marker else []),
        "legacy_end_marker": append_end_marker,
    }


def metadata_fields(row: list[str]) -> list[str]:
    # Trim workbook styling beyond the schema, never holes inside its columns.
    fields = [value.strip() for value in row[1:]]
    while fields and not fields[-1]:
        fields.pop()
    return fields


def bind_worksheet(name: str, rows: list[list[str]], contract: dict) -> dict:
    metadata = {}
    requirements = {}
    for row in rows:
        if not row:
            continue
        key = row[0].strip().casefold()
        if key in {"name", "description", "data type", "technical name"}:
            if key in metadata:
                raise ContractError(f"{name}: duplicate metadata row {key}.")
            metadata[key] = metadata_fields(row)
        elif any(value.strip().casefold() in {"required", "conditional"} for value in row[1:]):
            requirements[row[0].strip()] = row[1:]
    technical = metadata.get("technical name", [])
    labels = metadata.get("name", [])
    fields = contract["ordered_headers"][:-1] if contract["legacy_end_marker"] else contract["ordered_headers"]
    if len(technical) != len(fields) or len(labels) != len(fields):
        raise ContractError(f"{name}: XLSM/CTL column count mismatch.")
    mapping = []
    for index, header in enumerate(fields):
        mapping.append({
            "position": index + 1, "csv_header": header,
            "worksheet_label": labels[index], "worksheet_technical_name": technical[index],
            "data_type": (metadata.get("data type", []) + [""] * len(fields))[index],
            "description": (metadata.get("description", []) + [""] * len(fields))[index],
            "application_requirements": {
                application: values[index].strip()
                for application, values in requirements.items()
                if index < len(values) and values[index].strip()
            },
        })
    return {
        **contract, "worksheet": name,
        "match_type": "exact" if technical == fields else "position",
        "field_mapping": mapping,
    }


def inspect_template(template: Path, controls: list[Path], append_end_marker: bool = True) -> dict:
    members = validate_members([path.with_suffix(".csv").name for path in controls])
    routes = supported_members()
    for member in members:
        if routes[member][0] != template.name:
            raise ContractError(f"{member} requires {routes[member][0]}, not {template.name}.")
    contracts = [control_contract(path, append_end_marker) for path in controls]
    content = template.read_bytes()
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        strings = []
        if "xl/sharedStrings.xml" in archive.namelist():
            shared = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            strings = ["".join(node.itertext()) for node in shared.findall("m:si", NS)]
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {node.attrib["Id"]: node.attrib for node in relationships.findall("p:Relationship", NS)}
        sheets = workbook.findall("m:sheets/m:sheet", NS)
        bound = []
        for contract in contracts:
            candidates = [sheet for sheet in sheets if worksheet_matches_control_name(
                sheet.attrib["name"], contract["control_file"])]
            if len(candidates) != 1:
                raise ContractError(f'{contract["csv_member"]}: expected one CTL-prefix data tab.')
            sheet = candidates[0]
            relationship = targets[sheet.attrib[f"{{{REL}}}id"]]
            target = relationship["Target"].lstrip("/")
            xml_path = target if target.startswith("xl/") else f"xl/{target}"
            if relationship.get("TargetMode") == "External" or ".." in target.split("/"):
                raise ContractError("Unsafe workbook relationship.")
            worksheet = ET.fromstring(archive.read(xml_path))
            rows = []
            # Only metadata preceding/including Technical Name is needed, not sample data.
            for row in worksheet.findall("m:sheetData/m:row", NS):
                values = row_values(row, strings)
                rows.append(values)
                if values and values[0].strip().casefold() == "technical name":
                    break
            bound.append(bind_worksheet(sheet.attrib["name"], rows, contract))
    return {
        "template": template.name, "template_path": str(template.resolve()),
        "sha256": sha256(content), "csv_contracts": bound,
    }


def inspect_templates(templates: list[Path], controls: list[Path]) -> list[dict]:
    members = validate_members([path.with_suffix(".csv").name for path in controls])
    routes = supported_members()
    expected = {routes[member][0] for member in members}
    if len({path.name for path in templates}) != len(templates) or {p.name for p in templates} != expected:
        raise ContractError("Provide each requested workbook exactly once and no unrelated workbooks.")
    return [inspect_template(template, [
        path for path, member in zip(controls, members) if routes[member][0] == template.name
    ]) for template in templates]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template", nargs="+", type=Path)
    parser.add_argument("--control-file", action="append", type=Path, required=True)
    parser.add_argument("--provenance", type=Path, required=True,
                        help="same-run public download provenance JSON; see references/csv-preparation.md")
    parser.add_argument("--output", type=Path, required=True, help="new transient contract JSON path")
    args = parser.parse_args(argv)
    try:
        provenance = json.loads(args.provenance.read_text(encoding="utf-8-sig"))
        for key in ("run_id", "release", "source_system", "source_system_type", "catalog_url", "retrieved_at", "files"):
            if not provenance.get(key):
                raise ContractError(f"Missing download provenance: {key}")
        templates = inspect_templates(args.template, args.control_file)
        for template in templates:
            files = [(template["template"], template["sha256"])] + [
                (c["control_file"], c["control_file_sha256"]) for c in template["csv_contracts"]]
            for name, digest in files:
                source = provenance["files"].get(name, {})
                if source.get("sha256") != digest or not source.get("url"):
                    raise ContractError(f"Missing or mismatched download provenance for {name}.")
        result = {"status": "passed", "schema_version": 1, "provenance": provenance, "templates": templates}
        # Exclusive create: evidence from an earlier preparation is never silently replaced.
        with args.output.open("x", encoding="utf-8", newline="\n") as output:
            output.write(json.dumps(result, indent=2) + "\n")
        print(json.dumps({"status": "passed", "contract_path": str(args.output.resolve()),
                          "members": [c["csv_member"] for t in templates for c in t["csv_contracts"]]}))
        return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, ET.ParseError, zipfile.BadZipFile) as error:
        print(json.dumps({"status": "blocked", "failure_class": "input_validation", "message": str(error)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
