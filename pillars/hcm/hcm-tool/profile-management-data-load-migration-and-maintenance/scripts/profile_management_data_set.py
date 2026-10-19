"""Validate a sanitized Profile Management request and create a local preview."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

SUPPORTED_OBJECTS = frozenset({
    "Content Item", "Content Item Translation",
    "Content Item Rating Description Translation", "Content Item Relationship",
    "Talent Profile", "Talent Profile Translation",
    "Talent Model Profile Extra Information", "Talent Model Profile Extra Information Translation",
    "Profile Attachment",
})
TRANSLATIONS = frozenset({
    "Content Item Translation", "Content Item Rating Description Translation",
    "Talent Profile Translation", "Talent Model Profile Extra Information Translation",
})
CHILD_OBJECTS = frozenset({
    "Content Item Translation", "Content Item Rating Description Translation",
    "Content Item Relationship", "Talent Profile Translation",
    "Talent Model Profile Extra Information", "Talent Model Profile Extra Information Translation",
    "Profile Attachment",
})
OPERATIONS = frozenset({"create", "update", "migration", "mass-maintenance", "translation", "attachment-processing", "synchronization", "validation"})
CSV_COLUMNS = (
    "target_environment", "requested_operation", "root_record_type", "target_check_status",
    "object", "identifier", "parent_identifier", "language", "values_json",
)
FRIENDLY_RECORD_COLUMNS = (
    "Object", "Identifier", "Parent identifier", "Language",
    "Profile name or label", "ATTRIBUTE_CATEGORY", "Values JSON",
    "Attachment reference", "Source row",
)
FRIENDLY_REQUEST_FIELDS = {
    "Target environment": "target_environment",
    "Requested operation": "requested_operation",
    "Root record type": "root_record_type",
    "Exact target check": "target_check_status",
}
SOURCE_SUFFIXES = frozenset({".csv", ".xlsx", ".docx", ".pdf", ".txt", ".md", ".json"})
KNOWN_CSV_COLUMNS = frozenset(CSV_COLUMNS)
OBJECT_HDL_NAMES = {
    "Talent Profile": "TalentProfile",
    "Talent Profile Translation": "TalentProfileTranslation",
}
PROVIDER_BLOCKED_OBJECTS = {
    "Content Item": "Content Item is a separate HDL root family. Download and validate the target Content Item template with Value Set ID and Value Set Name before enabling a route.",
    "Content Item Relationship": "Content Item Relationship belongs to the separate Content Item HDL family; target template and exact parent contract are not confirmed.",
    "Content Item Translation": "Fusion metadata detail returned HTTP 500; refresh the Talent Management business object and rerun schema preflight.",
    "Content Item Rating Description Translation": "No exact registered Data Loader discriminator was found in the target metadata.",
    "Talent Model Profile Extra Information": "The standalone ModelProfileExtraInfo section is not confirmed by target metadata; Oracle documentation identifies the translation business object refresh.",
    "Talent Model Profile Extra Information Translation": "No exact registered Data Loader discriminator was found in the target metadata.",
    "Profile Attachment": "Oracle documents Talent Profile file attachment support, but the exact target attachment section and attribute contract have not been downloaded and validated.",
}


def source_evidence(source: Path) -> dict[str, Any]:
    """Return immutable, secret-free source evidence without contacting Fusion."""
    if source.suffix.casefold() not in SOURCE_SUFFIXES:
        raise ValueError(f"Unsupported source format: {source.suffix or '(none)'}")
    contents = source.read_bytes()
    return {
        "source_name": source.name,
        "source_format": source.suffix.casefold().lstrip("."),
        "sha256": hashlib.sha256(contents).hexdigest(),
        "size_bytes": len(contents),
    }


def _request_from_rows(fieldnames: list[str] | None, rows: list[dict[str, str]]) -> dict[str, Any]:
    if fieldnames is None:
        raise ValueError("source must contain a header row")
    missing = [column for column in CSV_COLUMNS if column not in fieldnames]
    if missing:
        raise ValueError("source header is missing required intake columns: " + ", ".join(missing))
    if not rows:
        raise ValueError("source must contain at least one profile record")
    request = _request_from_csv_rows(rows)
    unknown_columns = [column for column in fieldnames if column not in KNOWN_CSV_COLUMNS]
    if unknown_columns:
        request["source_uncertainties"] = [
            {
                "source_field": column,
                "target_field": "",
                "status": "confirmation-required",
                "reason": "No documented Profile Management intake-to-HDL mapping exists for this source column.",
            }
            for column in unknown_columns
        ]
    return request


def _request_from_csv_rows(rows: list[dict[str, str]]) -> dict[str, Any]:
    """Normalize template rows shared by CSV and XLSX intake."""
    shared = {key: _row_value(rows[0], key) for key in CSV_COLUMNS[:4]}
    if any(value is None for value in shared.values()):
        raise ValueError("CSV requires target environment, operation, root type, and target-check status on every row")
    records: list[dict[str, Any]] = []
    for number, row in enumerate(rows, start=2):
        if any(_row_value(row, key) != shared[key] for key in CSV_COLUMNS[:4]):
            raise ValueError(f"CSV row {number} has request metadata that differs from the first row")
        try:
            values = json.loads(row.get("values_json", ""))
        except json.JSONDecodeError as error:
            raise ValueError(f"CSV row {number} has invalid values_json: {error.msg}") from error
        record = {"object": _row_value(row, "object"), "identifier": _row_value(row, "identifier"), "values": values}
        for key in ("parent_identifier", "language"):
            if _row_value(row, key) is not None:
                record[key] = _row_value(row, key)
        records.append(record)
    return {
        "target_environment": shared["target_environment"],
        "requested_operation": shared["requested_operation"],
        "root_record_type": shared["root_record_type"],
        "target_check": {"status": shared["target_check_status"]},
        "input_method": "csv-import",
        "records": records,
    }


def _row_value(row: dict[str, str], key: str) -> str | None:
    value = row.get(key, "").strip()
    return value or None


def request_from_csv(source: Path) -> dict[str, Any]:
    """Read the documented CSV interchange format without making a Fusion call."""
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    return _request_from_rows(reader.fieldnames, rows)


def request_from_xlsx(source: Path) -> dict[str, Any]:
    """Read either documented CSV-column or friendly default XLSX intake."""
    main_ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    rel_ns = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
    package_rel_ns = "{http://schemas.openxmlformats.org/package/2006/relationships}"
    with zipfile.ZipFile(source) as archive:
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            shared = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared_strings = ["".join(node.text or "" for node in item.findall(f".//{main_ns}t")) for item in shared.findall(f"{main_ns}si")]
        sheets = {sheet.get("name"): sheet for sheet in workbook.findall(f".//{main_ns}sheet")}

        def sheet_values(name: str) -> list[list[str]]:
            sheet = sheets.get(name)
            if sheet is None:
                raise ValueError(f"XLSX intake requires a {name} sheet")
            relationship_id = sheet.get(f"{rel_ns}id")
            target = next((item.get("Target") for item in relationships.findall(f"{package_rel_ns}Relationship") if item.get("Id") == relationship_id), None)
            if not target:
                raise ValueError(f"XLSX {name} sheet relationship is missing")
            member = target.lstrip("/")
            sheet_xml = ET.fromstring(archive.read(member if member.startswith("xl/") else f"xl/{member}"))
            result: list[list[str]] = []
            for row in sheet_xml.findall(f".//{main_ns}row"):
                cells: dict[int, str] = {}
                for sequential_column, cell in enumerate(row.findall(f"{main_ns}c"), start=1):
                    reference = cell.get("r")
                    if reference:
                        letters = "".join(character for character in reference if character.isalpha())
                        column = 0
                        for character in letters:
                            column = column * 26 + ord(character.upper()) - ord("A") + 1
                    else:
                        # Retain compatibility with small synthetic OOXML
                        # workbooks that omit optional cell references.
                        column = sequential_column
                    cell_type = cell.get("t")
                    if cell_type == "inlineStr":
                        value = "".join(node.text or "" for node in cell.findall(f".//{main_ns}t"))
                    else:
                        raw = cell.findtext(f"{main_ns}v", default="")
                        value = shared_strings[int(raw)] if cell_type == "s" and raw else raw
                    cells[column] = value
                values = [cells.get(index, "") for index in range(1, (max(cells) if cells else 0) + 1)]
                while values and not str(values[-1]).strip():
                    values.pop()
                result.append(values)
            return result

        values = sheet_values("Records")
        request_values = sheet_values("Request") if "Request" in sheets else []
    if not values:
        raise ValueError("XLSX Records sheet is empty")
    header_index = next((index for index, row in enumerate(values) if [str(value).strip() for value in row] == list(CSV_COLUMNS) or [str(value).strip() for value in row] == list(FRIENDLY_RECORD_COLUMNS)), None)
    if header_index is None:
        raise ValueError("XLSX Records sheet has no supported Profile Management header row")
    fieldnames = [str(value).strip() for value in values[header_index]]
    rows = [
        {fieldnames[index]: "" if value is None else str(value) for index, value in enumerate(row[:len(fieldnames)])}
        for row in values[header_index + 1:]
        if any(value is not None and str(value).strip() for value in row)
    ]
    if fieldnames == list(CSV_COLUMNS):
        return _request_from_rows(fieldnames, rows)
    request_fields = {
        row[0].strip(): row[1].strip()
        for row in request_values
        if len(row) > 1 and row[0].strip() in FRIENDLY_REQUEST_FIELDS and row[1].strip()
    }
    missing = [label for label in FRIENDLY_REQUEST_FIELDS if not request_fields.get(label)]
    if missing:
        raise ValueError("XLSX Request sheet is missing: " + ", ".join(missing))
    normalized_rows: list[dict[str, str]] = []
    for row_number, row in enumerate(rows, start=header_index + 2):
        try:
            values_json = json.loads(row.get("Values JSON", "") or "{}")
        except json.JSONDecodeError as error:
            raise ValueError(f"XLSX Records row {row_number} has invalid Values JSON: {error.msg}") from error
        if not isinstance(values_json, dict):
            raise ValueError(f"XLSX Records row {row_number} Values JSON must be an object")
        if row.get("Profile name or label", "").strip():
            values_json.setdefault("ProfileName", row["Profile name or label"].strip())
        if row.get("ATTRIBUTE_CATEGORY", "").strip():
            values_json.setdefault("ATTRIBUTE_CATEGORY", row["ATTRIBUTE_CATEGORY"].strip())
        if row.get("Attachment reference", "").strip():
            values_json.setdefault("AttachmentReference", row["Attachment reference"].strip())
        normalized_rows.append({
            "target_environment": request_fields["Target environment"],
            "requested_operation": request_fields["Requested operation"],
            "root_record_type": request_fields["Root record type"],
            "target_check_status": request_fields["Exact target check"],
            "object": row.get("Object", ""),
            "identifier": row.get("Identifier", ""),
            "parent_identifier": row.get("Parent identifier", ""),
            "language": row.get("Language", ""),
            "values_json": json.dumps(values_json, separators=(",", ":")),
        })
    return _request_from_csv_rows(normalized_rows)


def _docx_text(source: Path) -> str:
    with zipfile.ZipFile(source) as document:
        xml = document.read("word/document.xml")
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        # Retain compatibility with minimal synthetic OOXML fixtures. A real
        # DOCX must be namespace-valid; this fallback never executes code.
        return b"\n".join(re.findall(rb"<w:t[^>]*>(.*?)</w:t>", xml, flags=re.DOTALL)).decode("utf-8", errors="replace")
    paragraphs = []
    for paragraph in root.iter():
        if paragraph.tag.endswith("}p"):
            paragraphs.append("".join(node.text or "" for node in paragraph.iter() if node.tag.endswith("}t")))
    return "\n".join(paragraphs)


def _pdf_text(source: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as error:
        bundled_site_packages = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "python" / "Lib" / "site-packages"
        if bundled_site_packages.exists():
            sys.path.append(str(bundled_site_packages))
            try:
                from pypdf import PdfReader
            except ImportError as bundled_error:
                raise ValueError("PDF intake requires the pypdf runtime") from bundled_error
        else:
            raise ValueError("PDF intake requires the pypdf runtime") from error
    return "\n".join(page.extract_text() or "" for page in PdfReader(source).pages)


def request_from_text_source(source: Path) -> dict[str, Any]:
    """Accept structured JSON or a safe key/value request from readable sources."""
    suffix = source.suffix.casefold()
    if suffix == ".docx":
        text = _docx_text(source)
    elif suffix == ".pdf":
        text = _pdf_text(source)
    else:
        text = source.read_text(encoding="utf-8-sig", errors="replace")
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        try:
            request = json.loads(text[start:end + 1])
        except json.JSONDecodeError as error:
            raise ValueError(f"source contains invalid structured JSON: {error.msg}") from error
        if not isinstance(request, dict):
            raise ValueError("structured source request must be a JSON object")
        return request
    return _request_from_key_value_text(text)


def _request_from_key_value_text(text: str) -> dict[str, Any]:
    """Parse a deliberately narrow, reviewable heading-and-key/value intake form."""
    metadata_labels = {label.casefold(): field for label, field in FRIENDLY_REQUEST_FIELDS.items()}
    object_labels = {name.casefold(): name for name in SUPPORTED_OBJECTS}
    records: list[dict[str, Any]] = []
    metadata: dict[str, str] = {}
    current: dict[str, Any] | None = None
    uncertainties: list[dict[str, str]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line in {"---", "***"}:
            continue
        object_name = object_labels.get(line.casefold())
        if object_name:
            current = {"object": object_name, "values": {}}
            records.append(current)
            continue
        if ":" not in line:
            uncertainties.append({"source_field": line, "target_field": "", "status": "confirmation-required", "reason": "Expected a supported object heading or Key: Value line."})
            continue
        label, value = (part.strip() for part in line.split(":", 1))
        if not value:
            uncertainties.append({"source_field": label, "target_field": "", "status": "confirmation-required", "reason": "Source value is blank."})
            continue
        metadata_field = metadata_labels.get(label.casefold())
        if metadata_field:
            metadata[metadata_field] = value
        elif current is None:
            uncertainties.append({"source_field": label, "target_field": "", "status": "confirmation-required", "reason": "A record field appeared before a supported object heading."})
        elif label.casefold() == "identifier":
            current["identifier"] = value
        elif label.casefold() == "parent identifier":
            current["parent_identifier"] = value
        elif label.casefold() == "language":
            current["language"] = value
        else:
            current["values"][label] = value
    request = {
        "target_environment": metadata.get("target_environment", ""),
        "requested_operation": metadata.get("requested_operation", ""),
        "root_record_type": metadata.get("root_record_type", ""),
        "target_check": {"status": metadata.get("target_check_status", "")},
        "records": records,
    }
    if uncertainties:
        request["source_uncertainties"] = uncertainties
    return request


def request_from_source(source: Path, preserve_source_dir: Path | None = None) -> dict[str, Any]:
    evidence = source_evidence(source)
    if source.suffix.casefold() == ".csv":
        request = request_from_csv(source)
    elif source.suffix.casefold() == ".xlsx":
        request = request_from_xlsx(source)
    else:
        request = request_from_text_source(source)
    request["input_method"] = f"{evidence['source_format']}-import"
    request["source_evidence"] = evidence
    if preserve_source_dir is not None:
        preserve_source_dir.mkdir(parents=True, exist_ok=True)
        preserved = preserve_source_dir / f"{evidence['sha256'][:12]}-{source.name}"
        if preserved.exists():
            if hashlib.sha256(preserved.read_bytes()).hexdigest() != evidence["sha256"]:
                raise ValueError(f"preserved source collision at {preserved}")
        else:
            shutil.copy2(source, preserved)
        request["source_evidence"]["preserved_source"] = str(preserved)
    return request


def mapping_review(request: dict[str, Any]) -> list[dict[str, str]]:
    """Produce AC1 mapping evidence; never resolve opaque Fusion identifiers locally."""
    review: list[dict[str, str]] = []
    for record in request.get("records", []):
        object_name = record.get("object", "")
        if object_name in PROVIDER_BLOCKED_OBJECTS:
            review.append({"source_field": "object", "target_field": "", "status": "provider-blocked", "reason": PROVIDER_BLOCKED_OBJECTS[object_name]})
            continue
        hdl_name = OBJECT_HDL_NAMES.get(object_name, "")
        if not hdl_name:
            review.append({"source_field": "object", "target_field": "", "status": "confirmation-required", "reason": "No supported HCM Data Loader object mapping exists."})
            continue
        review.append({"source_field": "object", "target_field": hdl_name, "status": "confirmed", "reason": "Supported HCM Data Loader object."})
        if object_name == "Talent Profile":
            review.append({"source_field": "identifier", "target_field": "TalentProfile.ProfileCode", "status": "confirmed", "reason": "Documented root key."})
        else:
            review.append({"source_field": "identifier", "target_field": "", "status": "confirmation-required", "reason": "This local row identifier is not assumed to be an HDL attribute."})
        if object_name in CHILD_OBJECTS:
            review.append({"source_field": "parent_identifier", "target_field": f"{hdl_name}.ProfileCode", "status": "confirmed", "reason": "Live TalentProfile section metadata uses the parent ProfileCode."})
        if object_name in TRANSLATIONS:
            review.append({"source_field": "language", "target_field": f"{hdl_name}.Language", "status": "target-language-lookup-required", "reason": "Use only the canonical installed Fusion language."})
        for source_field in record.get("values", {}):
            if object_name == "Talent Profile" and source_field == "ProfileName":
                target_field, status, reason = "TalentProfile.Description", "confirmed", "Documented root mapping."
            elif object_name == "Talent Profile" and source_field == "ProfileCode":
                target_field, status, reason = "TalentProfile.ProfileCode", "confirmed", "Documented root key."
            elif object_name == "Talent Profile" and source_field in {"ProfileTypeCode", "ProfileTypeId"}:
                target_field, status, reason = f"TalentProfile.{source_field}", "target-lookup-required", "Do not accept an opaque target value without read-only target evidence."
            elif source_field == "ATTRIBUTE_CATEGORY":
                target_field, status, reason = "", "dff-context-validation-required", "Use the live FLEX:HRT_PROFILE_ITEMS metadata and a deployed context field; ATTRIBUTE_CATEGORY is not a confirmed template attribute."
            elif source_field == "AttachmentReference":
                target_field, status, reason = "ProfileAttachment.File", "attachment-metadata-required", "Supply File, FileName, Title, and DataTypeCode from the live attachment metadata contract."
            elif object_name == "Content Item" and source_field in {"SectionName", "SectionId", "ContentType", "ContentTypeId", "ContentItem", "ContentItemId", "FLEX:HRT_PROFILE_ITEMS"}:
                target_field, status, reason = f"TalentProfile.ProfileItem.{source_field}", "confirmed", "Live TalentProfile ProfileItem section attribute."
            elif object_name == "Content Item Relationship" and source_field in {"RelationCode", "JobCode", "PositionCode", "OrganizationName"}:
                target_field, status, reason = f"TalentProfile.ProfileRelation.{source_field}", "confirmed", "Live TalentProfile ProfileRelation section attribute."
            elif object_name == "Talent Model Profile Extra Information" and source_field in {"Description", "JobLevelCode", "Qualifications", "Responsibilities"}:
                target_field, status, reason = f"TalentProfile.ModelProfileExtraInfo.{source_field}", "confirmed", "Live TalentProfile ModelProfileExtraInfo section attribute."
            elif object_name == "Profile Attachment" and source_field in {"File", "FileName", "Title", "DataTypeCode", "MimeType", "Description"}:
                target_field, status, reason = f"TalentProfile.ProfileAttachment.{source_field}", "confirmed", "Live TalentProfile ProfileAttachment section attribute."
            else:
                target_field, status, reason = "", "confirmation-required", "No authoritative child-object HDL field mapping is registered locally."
            review.append({"source_field": source_field, "target_field": target_field, "status": status, "reason": reason})
    review.extend(request.get("source_uncertainties", []))
    return review


def write_csv_template(destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerow({
            "target_environment": "nonprod-alias", "requested_operation": "create",
            "root_record_type": "model-profile", "target_check_status": "not-found",
            "object": "Talent Profile", "identifier": "SYNTHETIC-MODEL-001",
            "parent_identifier": "", "language": "", "values_json": '{"ProfileName":"Synthetic Model Profile"}',
        })


def export_csv(request: dict[str, Any], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for record in request["records"]:
            writer.writerow({
                "target_environment": request["target_environment"],
                "requested_operation": request["requested_operation"],
                "root_record_type": request["root_record_type"],
                "target_check_status": request["target_check"]["status"],
                "object": record.get("object", ""), "identifier": record.get("identifier", ""),
                "parent_identifier": record.get("parent_identifier", ""), "language": record.get("language", ""),
                "values_json": json.dumps(record.get("values", {}), sort_keys=True, separators=(",", ":")),
            })


def validate_request(request: Any, require_final_approval: bool = False) -> list[str]:
    if not isinstance(request, dict):
        return ["request must be a JSON object"]
    errors: list[str] = []
    for field in ("target_environment", "requested_operation", "root_record_type", "records", "target_check"):
        if field not in request:
            errors.append(f"missing required field: {field}")
    if errors:
        return errors
    uncertainties = request.get("source_uncertainties", [])
    if uncertainties:
        names = [str(item.get("source_field", "unknown")) for item in uncertainties if isinstance(item, dict)]
        errors.append("source contains unmapped or ambiguous fields: " + ", ".join(names or ["unknown"]))
    if not isinstance(request["target_environment"], str) or not request["target_environment"].strip():
        errors.append("target_environment must be non-empty text")
    operation = request["requested_operation"]
    if operation not in OPERATIONS:
        errors.append("requested_operation is unsupported")
    if request["root_record_type"] not in {"person-profile", "model-profile", "content-library"}:
        errors.append("root_record_type is unsupported")
    records = request["records"]
    if not isinstance(records, list) or not records:
        errors.append("records must be a non-empty list")
    elif isinstance(records, list):
        seen: set[tuple[str, str]] = set()
        identifiers: set[str] = set()
        for index, record in enumerate(records):
            prefix = f"records[{index}]"
            if not isinstance(record, dict):
                errors.append(f"{prefix} must be an object")
                continue
            obj, identifier = record.get("object"), record.get("identifier")
            if obj not in SUPPORTED_OBJECTS:
                errors.append(f"{prefix}.object is unsupported")
            elif obj in PROVIDER_BLOCKED_OBJECTS:
                errors.append(f"{prefix}.object is provider-blocked: {PROVIDER_BLOCKED_OBJECTS[obj]}")
            if not isinstance(identifier, str) or not identifier.strip():
                errors.append(f"{prefix}.identifier must be non-empty text")
            elif (str(obj), identifier) in seen:
                errors.append(f"{prefix} duplicates an object and identifier")
            else:
                seen.add((str(obj), identifier)); identifiers.add(identifier)
            if not isinstance(record.get("values"), dict):
                errors.append(f"{prefix}.values must be an object")
            if obj in TRANSLATIONS and not isinstance(record.get("language"), str):
                errors.append(f"{prefix}.language is required for a translation")
            if obj in CHILD_OBJECTS and not isinstance(record.get("parent_identifier"), str):
                errors.append(f"{prefix}.parent_identifier is required for a child record")
        for index, record in enumerate(records):
            if isinstance(record, dict) and record.get("object") in CHILD_OBJECTS and record.get("parent_identifier") not in identifiers:
                errors.append(f"records[{index}].parent_identifier does not reference this complete request")
    target = request["target_check"]
    status = target.get("status") if isinstance(target, dict) else None
    expected = "not-found" if operation == "create" else "exactly-one"
    if operation in {"create", "update", "mass-maintenance"} and status != expected:
        errors.append(f"target_check.status must be {expected} for {operation}")
    if operation == "migration" and status != "not-found":
        errors.append("migration must stop on an existing or ambiguous target")
    if require_final_approval and request.get("final_preview_approved") is not True:
        errors.append("final_preview_approved must be true before execution")
    return errors


def build_preview(request: dict[str, Any]) -> dict[str, Any]:
    canonical = json.dumps(request, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return {
        "status": "valid",
        "fingerprint": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "target_environment": request["target_environment"],
        "requested_operation": request["requested_operation"],
        "root_record_type": request["root_record_type"],
        "input_method": request.get("input_method", "direct-entry"),
        "object_counts": {obj: sum(row.get("object") == obj for row in request["records"]) for obj in sorted({row.get("object") for row in request["records"]})},
        "records": request["records"],
        "omitted_optional_components": request.get("omitted_optional_components", []),
        "execution": "not-authorized",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate or convert a local Profile Management request; never contacts Fusion")
    parser.add_argument("request", type=Path, nargs="?")
    parser.add_argument("--require-final-approval", action="store_true")
    parser.add_argument("--create-csv-template", type=Path)
    parser.add_argument("--import-csv", type=Path)
    parser.add_argument("--import-source", type=Path, help="Import CSV, XLSX, DOCX, PDF, TXT, MD, or JSON locally")
    parser.add_argument("--preserve-source-dir", type=Path, help="Optional explicit local destination for an unchanged source copy")
    parser.add_argument("--export-csv", type=Path)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--mapping-review-json", type=Path)
    parser.add_argument("--validation-result-json", type=Path, help="Persist the local validation or preview result without contacting Fusion")
    args = parser.parse_args()
    if args.create_csv_template:
        write_csv_template(args.create_csv_template)
        print(json.dumps({"status": "template-created", "execution": "not-authorized"}))
        return 0
    try:
        if args.import_source:
            request = request_from_source(args.import_source, args.preserve_source_dir)
            if args.output_json:
                args.output_json.parent.mkdir(parents=True, exist_ok=True)
                args.output_json.write_text(json.dumps(request, indent=2) + "\n", encoding="utf-8")
        elif args.import_csv:
            request = request_from_csv(args.import_csv)
            if args.output_json:
                args.output_json.parent.mkdir(parents=True, exist_ok=True)
                args.output_json.write_text(json.dumps(request, indent=2) + "\n", encoding="utf-8")
        elif args.request:
            request = json.loads(args.request.read_text(encoding="utf-8"))
        else:
            raise ValueError("provide a JSON request, --import-csv, or --create-csv-template")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "invalid", "errors": [str(error)]}))
        return 2
    errors = validate_request(request, args.require_final_approval)
    if args.mapping_review_json:
        args.mapping_review_json.parent.mkdir(parents=True, exist_ok=True)
        args.mapping_review_json.write_text(json.dumps(mapping_review(request), indent=2) + "\n", encoding="utf-8")
    if not errors and args.export_csv:
        export_csv(request, args.export_csv)
    result = {"status": "invalid", "errors": errors} if errors else build_preview(request)
    if args.validation_result_json:
        args.validation_result_json.parent.mkdir(parents=True, exist_ok=True)
        args.validation_result_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
