#!/usr/bin/env python3
"""Prepare one offline FSM CSV package for observed new planning-RBS creates.

This is a serializer, not a Fusion lookup, eligibility check, or import client.
The caller supplies a fresh complete target export and already resolved,
source-attributed reference context. Unsupported or ambiguous data fails closed.
"""

from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
import hashlib
import io
import json
from pathlib import Path
import sys
from typing import Any
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZIP_DEFLATED, ZipFile, ZipInfo


TASK_CODE = "PJF_MANAGE_PLANNING_BILLING_RESOURCE_BREAKDOWN_STRUCTURES"
METADATA = "ASM_SETUP_CSV_METADATA.xml"
HEADER = "ORA_PJF_RBS_HEADER.csv"
VERSION = "ORA_PJF_RBS_VERSION.csv"
HEADER_TRANSLATION = "ORA_PJF_RBS_HEADER_TRANSLATION.csv"
FORMAT = "ORA_PJF_RBS_FORMAT.csv"
VERSION_TRANSLATION = "ORA_PJF_RBS_VERSION_TRANSLATION.csv"
ELEMENT = "ORA_PJF_RBS_ELEMENT.csv"
CSV_MEMBERS = (HEADER, VERSION, HEADER_TRANSLATION, FORMAT, VERSION_TRANSLATION, ELEMENT)
MEMBERS = (*CSV_MEMBERS, METADATA)
REPO_ROOT = Path(__file__).resolve().parents[6]
WORKSPACE_OUTPUT = Path("artifacts/pillars/erp/project-financial-management/project-foundation/"
                        "manage-planning-and-billing-resource-breakdown-structures/current")

# Exact headers of the successful seven-member task export/import/readback.
# Any changed schema needs a new observed contract, not a best-effort rewrite.
FIELDS = {
    HEADER: ("Name", "AttributeNumber5", "CentrallyControlFlag", "Description",
             "EndDateActive", "RbsType", "StartDateActive", "UseForAllocFlag",
             "UseForCmtCtrlFlag", "UseForIcBillingFlag", "ClassificationCode",
             "OrgEffectiveStartDate", "OrgEffectiveEndDate", "OrgName",
             "AutoAddResFlag", "LaborDisabledFlag", "EquipmentDisabledFlag",
             "MaterialDisabledFlag"),
    VERSION: ("ORA_PJF_RBS_HEADER.Name", "VersionNumber", "CurrentReportingFlag",
              "Description", "EndDateActive", "Name", "StartDateActive", "StatusCode", "SetCode"),
    HEADER_TRANSLATION: ("ORA_PJF_RBS_HEADER.Name", "Description", "Language", "Name", "SourceLang"),
    FORMAT: ("ORA_PJF_RBS_HEADER.Name", "ORA_PJF_RBS_VERSION.VersionNumber", "ResFormatId"),
    VERSION_TRANSLATION: ("ORA_PJF_RBS_HEADER.Name", "ORA_PJF_RBS_VERSION.VersionNumber",
                          "Description", "Language", "Name", "SourceLang"),
    ELEMENT: ("OutlineNumber", "NlrName", "ExpenditureCategoryName", "ExpenditureTypeName",
              "JobCode", "SetCode", "Name5", "ClassificationCode1", "EmailAddress",
              "ResourceClassId", "RbsHeaderName", "VersionNumber", "Alias", "OrderNumber",
              "ResourceTypeId", "EnabledFlag", "ResFormatId", "ResourceClassCode", "RuleFlag",
              "RbsLevel", "LeafNodeFlag", "UserCreatedFlag", "MarkedFor", "Attribute30",
              "PersonNumber", "EffectiveStartDate", "EffectiveEndDate", "EffectiveStartDate1",
              "EffectiveEndDate1", "Name3", "EffectiveStartDate4", "EffectiveEndDate4", "Name4",
              "EffectiveStartDate5", "EffectiveEndDate5", "Name6", "EffectiveStartDate7",
              "EffectiveEndDate7", "usedResourceFlag"),
}

# IDs were observed in the target export and in the 16-case successful import.
# Each requested ID must also be present in the supplied current-target export.
FORMATS = {
    "Resource Class": "323", "Named Person": "195", "Project Nonlabor Resource": "306",
    "Organization": "205", "Job": "166", "Expenditure Type": "80",
    "Expenditure Category": "35", "Job: Expenditure Category": "170",
    "Organization: Inventory Item": "231",
}
FORMAT_ONLY = set(FORMATS)
RESOURCE_TYPES = {
    "Named Person": "3", "Project Nonlabor Resource": "12", "Organization": "10",
    "Job": "9", "Expenditure Type": "6", "Expenditure Category": "5",
    "Job: Expenditure Category": "5",
}
RESOURCE_KEYS = {
    "Named Person": {"format", "person"},
    "Project Nonlabor Resource": {"format", "nonlabor_resource_name"},
    "Organization": {"format", "organization", "resource_class", "spread_curve"},
    "Job": {"format", "alias", "job"},
    "Expenditure Type": {"format", "expenditure_type_name", "resource_class", "spread_curve"},
    "Expenditure Category": {"format", "alias", "expenditure_category_name", "resource_class", "spread_curve"},
    "Job: Expenditure Category": {"format", "alias", "job", "expenditure_category_name"},
}
CLASS = {"Labor": ("PEOPLE", "1"), "Equipment": ("EQUIPMENT", "2")}
TESTED_PAIR = {
    "Named Person": ("Labor", "Prorated Even"),
    "Project Nonlabor Resource": ("Equipment", "Back Loaded"),
    "Organization": ("Equipment", "Back Loaded"),
    "Job": ("Labor", "Prorated Even"),
    "Expenditure Type": ("Labor", "Prorated Even"),
    "Expenditure Category": ("Labor", "Prorated Even"),
    "Job: Expenditure Category": ("Labor", "Prorated Even"),
}
DEFAULT_CLASS_ROWS = {
    "1": ("Labor", "PEOPLE", "1", "Prorated Even"),
    "2": ("Equipment", "EQUIPMENT", "2", "Back Loaded"),
    "3": ("Material Items", "MATERIAL_ITEMS", "3", "S Curve"),
    "4": ("Financial Resources", "FINANCIAL_ELEMENTS", "4", "Prorated Even"),
}


class ContractError(ValueError):
    """The input or source export cannot safely support this projection."""


def require(test: bool, message: str) -> None:
    if not test:
        raise ContractError(message)


def keys(value: Any, allowed: set[str], required: set[str], where: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{where} must be an object")
    extra = set(value) - allowed
    missing = required - set(value)
    require(not extra and not missing, f"{where}: unexpected {sorted(extra)}; missing {sorted(missing)}")
    return value


def string(value: Any, where: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{where} must be nonblank text")
    require(value == value.strip(), f"{where} has leading or trailing whitespace")
    return value


def csv_date(value: Any, where: str) -> str:
    raw = string(value, where)
    try:
        parsed = date.fromisoformat(raw) if "-" in raw else datetime.strptime(raw, "%Y/%m/%d").date()
    except ValueError as error:
        raise ContractError(f"{where} must be a real ISO yyyy-mm-dd date") from error
    return parsed.strftime("%Y/%m/%d")


def evidence(value: Any, environment: str, where: str) -> None:
    item = keys(value, {"source", "environment", "match_count", "reference"},
                {"source", "environment", "match_count"}, where)
    source = string(item["source"], f"{where}.source")
    require("rbs_export" not in source.casefold() and "fixture" not in source.casefold(),
            f"{where} cannot cite an RBS export or fixture as lookup authority")
    require(string(item["environment"], f"{where}.environment").casefold() == environment.casefold(),
            f"{where} is bound to another environment")
    require(type(item["match_count"]) is int and item["match_count"] == 1,
            f"{where} needs exactly one validated match")
    if "reference" in item:
        string(item["reference"], f"{where}.reference")


def context_evidence(value: Any, environment: str, where: str) -> None:
    """Bind supplied CSV context to the target without judging reference eligibility."""
    item = keys(value, {"source", "environment", "match_count", "reference"},
                {"source", "environment"}, where)
    source = string(item["source"], f"{where}.source")
    require("rbs_export" not in source.casefold() and "fixture" not in source.casefold(),
            f"{where} cannot cite an RBS export or fixture as context authority")
    require(string(item["environment"], f"{where}.environment").casefold() == environment.casefold(),
            f"{where} is bound to another environment")
    if "match_count" in item:
        require(type(item["match_count"]) is int and item["match_count"] == 1,
                f"{where}.match_count must describe one selected context row")
    if "reference" in item:
        string(item["reference"], f"{where}.reference")


def read_csv(raw: bytes, member: str) -> list[dict[str, str]]:
    require(b"\x00" not in raw, f"{member} contains NUL bytes")
    try:
        source = io.StringIO(raw.decode("utf-8-sig"), newline="")
    except UnicodeDecodeError as error:
        raise ContractError(f"{member} is not UTF-8") from error
    reader = csv.DictReader(source)
    require(tuple(reader.fieldnames or ()) == FIELDS[member], f"{member} header differs from observed contract")
    rows = list(reader)
    require(all(None not in row and all(value is not None for value in row.values())
                for row in rows), f"{member} has a malformed row")
    return rows


def write_csv(member: str, rows: list[dict[str, str]]) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=FIELDS[member], lineterminator="\r\n", quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def read_export(path: Path, environment: str, digest: str, max_age_days: int) -> tuple[dict[str, list[dict[str, str]]], bytes, str]:
    require(path.is_file(), f"source export not found: {path}")
    require(path.stat().st_size <= 200_000_000, "source export exceeds archive size limit")
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == digest, "source export SHA-256 does not match the validated input")
    try:
        with ZipFile(io.BytesIO(raw)) as archive:
            infos = archive.infolist()
            require(len(infos) == 7 and set(i.filename for i in infos) == set(MEMBERS),
                    "source export must contain exactly seven flat task members")
            require(all(i.file_size <= 100_000_000 for i in infos) and
                    sum(i.file_size for i in infos) <= 200_000_000,
                    "source export uncompressed members exceed size limit")
            require(archive.testzip() is None, "source export ZIP has a corrupt member")
            members = {name: archive.read(name) for name in MEMBERS}
    except (BadZipFile, OSError, RuntimeError, ValueError) as error:
        raise ContractError("source export is not a readable task ZIP") from error
    metadata = members[METADATA]
    require(b"<!DOCTYPE" not in metadata.upper() and b"<!ENTITY" not in metadata.upper(),
            "source export metadata contains unsupported XML entities")
    try:
        root = ET.fromstring(metadata)
    except ET.ParseError as error:
        raise ContractError("source export metadata is invalid XML") from error
    require(root.tag == "MigrationProcessCSVMetadataVO", "unexpected source-export metadata root")
    row = root.find("MigrationProcessCSVMetadataVORow")
    require(row is not None, "source export has no process metadata")
    field = lambda name: (row.findtext(name) or "").strip()
    require(field("ObjectShortName") == TASK_CODE and field("ObjectType") == "TASK" and
            field("ProcessType") == "EXPORT" and field("ProcessStatus") == "COMPLETED",
            "source export is not a completed export for this setup task")
    require(field("ProcessEnv").casefold() == environment.casefold(), "source export belongs to another environment")
    try:
        process_day = date.fromisoformat(field("ProcessDate")[:10])
    except ValueError as error:
        raise ContractError("source export process date is missing or invalid") from error
    days_old = (date.today() - process_day).days
    require(-1 <= days_old <= max_age_days, "source export is stale or future-dated for this preparation")
    objects = {element.text for element in root.findall(".//BusinessObjectShortName")}
    require({name.removesuffix(".csv") for name in CSV_MEMBERS} <= objects,
            "source export metadata does not describe all six CSV members")
    return {name: read_csv(members[name], name) for name in CSV_MEMBERS}, metadata, field("ProcessDate")


def one(rows: list[dict[str, str]], where: str) -> dict[str, str]:
    require(len(rows) == 1, f"{where} must match exactly one row; found {len(rows)}")
    return rows[0]


def select_minimal_template(source: dict[str, list[dict[str, str]]], name: str) -> tuple[dict[str, str], dict[str, str], dict[str, list[dict[str, str]]]]:
    header = one([r for r in source[HEADER] if r["Name"] == name], "minimal template header")
    version = one([r for r in source[VERSION] if r["ORA_PJF_RBS_HEADER.Name"] == name], "minimal template version")
    require(header["RbsType"] == "PLANNING" and not header["EndDateActive"] and
            version["VersionNumber"] == "1" and version["Name"] == name and
            version["StartDateActive"] == header["StartDateActive"] and
            version["StatusCode"] == "FROZEN" and
            version["CurrentReportingFlag"] == "Y" and not version["SetCode"],
            "template must be a tested new-planning-style version 1 without a Job Set")
    expected_header = {"CentrallyControlFlag": "Y", "UseForAllocFlag": "N", "UseForCmtCtrlFlag": "N",
                       "UseForIcBillingFlag": "N", "AutoAddResFlag": "N", "LaborDisabledFlag": "N",
                       "EquipmentDisabledFlag": "N", "MaterialDisabledFlag": "N"}
    require(all(header[k] == v for k, v in expected_header.items()), "template header flags differ from observed UI profile")
    fmt = [r for r in source[FORMAT] if r["ORA_PJF_RBS_HEADER.Name"] == name]
    require(len(fmt) == 1 and fmt[0]["ResFormatId"] == "323" and
            fmt[0]["ORA_PJF_RBS_VERSION.VersionNumber"] == "1",
            "template must contain only the Resource Class format")
    elements = [r for r in source[ELEMENT] if r["RbsHeaderName"] == name]
    require(len(elements) == 5 and {r["OutlineNumber"] for r in elements} == {"0", "1", "2", "3", "4"},
            "template must have the root and exactly four default class elements")
    by_outline = {r["OutlineNumber"]: r for r in elements}
    root = by_outline["0"]
    require((root["Alias"], root["RbsHeaderName"], root["VersionNumber"],
             root["OrderNumber"], root["ResourceTypeId"], root["EnabledFlag"],
             root["RuleFlag"], root["RbsLevel"], root["LeafNodeFlag"],
             root["UserCreatedFlag"]) ==
            (name, name, "1", "0", "-1", "Y", "N", "1", "N", "Y"),
            "template root shape differs")
    root_fields = {"OutlineNumber", "RbsHeaderName", "VersionNumber", "Alias", "OrderNumber",
                   "ResourceTypeId", "EnabledFlag", "RuleFlag", "RbsLevel", "LeafNodeFlag",
                   "UserCreatedFlag"}
    class_fields = root_fields | {"ResourceClassId", "ResFormatId", "ResourceClassCode", "Name3"}
    require({key for key, value in root.items() if value} <= root_fields,
            "template root has unreviewed populated fields")
    for outline, (alias, code, class_id, curve) in DEFAULT_CLASS_ROWS.items():
        r = by_outline[outline]
        require({key for key, value in r.items() if value} <= class_fields,
                f"template Resource Class element {outline} has unreviewed populated fields")
        require((r["Alias"], r["RbsHeaderName"], r["VersionNumber"], r["OrderNumber"],
                 r["ResourceClassCode"], r["ResourceClassId"], r["Name3"],
                 r["ResourceTypeId"], r["EnabledFlag"], r["RuleFlag"], r["ResFormatId"],
                 r["RbsLevel"], r["LeafNodeFlag"], r["UserCreatedFlag"])
                == (alias, name, "1", outline, code, class_id, curve,
                    "13", "Y", "N", "323", "2", "Y", "Y"),
                f"template Resource Class element {outline} differs from observed default")
    trans: dict[str, list[dict[str, str]]] = {}
    for member in (HEADER_TRANSLATION, VERSION_TRANSLATION):
        rows = [r for r in source[member] if r["ORA_PJF_RBS_HEADER.Name"] == name]
        require(rows and len({r["Language"] for r in rows}) == len(rows) and
                all(r["Name"] == name and r["Language"] and
                    r["SourceLang"] in {x["Language"] for x in rows} and
                    (member != VERSION_TRANSLATION or
                     r["ORA_PJF_RBS_VERSION.VersionNumber"] == "1")
                    for r in rows),
                f"{member} translation template is incomplete or inconsistent")
        trans[member] = rows
    require({r["Language"] for r in trans[HEADER_TRANSLATION]} ==
            {r["Language"] for r in trans[VERSION_TRANSLATION]},
            "header and version translation languages disagree")
    return header, version, {**trans, ELEMENT: [by_outline[str(i)] for i in range(5)]}


def resolved_job(value: Any, set_code: str, environment: str, where: str) -> dict[str, str]:
    item = keys(value, {"display_name", "code", "set_code", "effective_start_date",
                        "effective_end_date", "evidence"},
                {"display_name", "code", "set_code", "effective_start_date", "effective_end_date", "evidence"}, where)
    evidence(item["evidence"], environment, f"{where}.evidence")
    require(string(item["set_code"], f"{where}.set_code") == set_code,
            f"{where} belongs to a different Job Set")
    return {"display_name": string(item["display_name"], f"{where}.display_name"),
            "code": string(item["code"], f"{where}.code"),
            "start": csv_date(item["effective_start_date"], f"{where}.effective_start_date"),
            "end": csv_date(item["effective_end_date"], f"{where}.effective_end_date")}


def format_path(label: str) -> list[str]:
    if label == "Job: Expenditure Category":
        return ["Job", label]
    if label == "Organization: Inventory Item":
        return ["Organization", label]
    return [label]


def validate_and_project(request: dict[str, Any], source: dict[str, list[dict[str, str]]],
                         environment: str, template_name: str,
                         format_map: dict[str, str]) -> tuple[dict[str, list[dict[str, str]]], list[dict[str, Any]]]:
    template_header, template_version, template = select_minimal_template(source, template_name)
    structures = request["structures"]
    require(isinstance(structures, list) and structures, "structures must contain at least one create request")
    require(len(structures) <= 1000, "batch exceeds 1000 structures")
    existing = {r["Name"].casefold() for r in source[HEADER]}
    requested: set[str] = set()
    available_formats = {r["ResFormatId"] for r in source[FORMAT]}
    available_types = {(r["ResFormatId"], r["ResourceTypeId"]) for r in source[ELEMENT]}
    projected = {member: [] for member in CSV_MEMBERS}
    preview: list[dict[str, Any]] = []
    for index, raw in enumerate(structures, start=1):
        where = f"structures[{index}]"
        item = keys(raw, {"name", "project_unit", "from_date", "description", "job_set", "formats", "resources"},
                    {"name", "project_unit", "from_date"}, where)
        name = string(item["name"], f"{where}.name")
        require(name.casefold() not in existing and name.casefold() not in requested,
                f"{where}.name already exists in source export or batch")
        requested.add(name.casefold())
        start = csv_date(item["from_date"], f"{where}.from_date")
        description = item.get("description", "")
        require(isinstance(description, str), f"{where}.description must be text")
        pu = keys(item["project_unit"], {"name", "classification_code", "effective_start_date",
                                         "effective_end_date", "evidence"},
                  {"name", "classification_code", "effective_start_date", "effective_end_date", "evidence"},
                  f"{where}.project_unit")
        context_evidence(pu["evidence"], environment, f"{where}.project_unit.evidence")
        pu_name = string(pu["name"], f"{where}.project_unit.name")
        pu_classification = string(pu["classification_code"], f"{where}.project_unit.classification_code")
        pu_start = csv_date(pu["effective_start_date"], f"{where}.project_unit.effective_start_date")
        pu_end = csv_date(pu["effective_end_date"], f"{where}.project_unit.effective_end_date")
        set_code = ""
        if "job_set" in item:
            job_set = keys(item["job_set"], {"name", "code", "evidence"},
                           {"name", "code", "evidence"}, f"{where}.job_set")
            evidence(job_set["evidence"], environment, f"{where}.job_set.evidence")
            string(job_set["name"], f"{where}.job_set.name")
            set_code = string(job_set["code"], f"{where}.job_set.code")
        raw_formats = item.get("formats", [])
        raw_resources = item.get("resources", [])
        require(isinstance(raw_formats, list) and isinstance(raw_resources, list),
                f"{where}.formats and resources must be arrays")
        selected: list[str] = ["Resource Class"]
        for label in raw_formats:
            require(isinstance(label, str) and label in FORMAT_ONLY,
                    f"{where} contains an unobserved format: {label!r}")
            for part in format_path(label):
                if part not in selected:
                    selected.append(part)
        resources: list[dict[str, Any]] = []
        for rindex, raw_resource in enumerate(raw_resources, start=1):
            rwhere = f"{where}.resources[{rindex}]"
            require(isinstance(raw_resource, dict), f"{rwhere} must be an object")
            label = raw_resource.get("format")
            require(isinstance(label, str) and label in RESOURCE_KEYS,
                    f"{rwhere} is an untested actual resource format: {label!r}")
            keys(raw_resource, RESOURCE_KEYS[label], RESOURCE_KEYS[label], rwhere)
            for part in format_path(label):
                if part not in selected:
                    selected.append(part)
            resources.append(raw_resource)
        require(all(FORMATS[label] in available_formats for label in selected),
                f"{where}: current-target export does not evidence every requested format ID")
        require(all(format_map.get(label) == FORMATS[label] for label in selected),
                f"{where}: same-target label-to-format-ID provenance is missing or conflicts")
        require(all((FORMATS[r["format"]], RESOURCE_TYPES[r["format"]]) in available_types for r in resources),
                f"{where}: current-target export does not evidence every requested resource type")
        header = {key: "" for key in FIELDS[HEADER]}
        header.update({"Name": name, "CentrallyControlFlag": "Y", "Description": description,
                       "RbsType": "PLANNING", "StartDateActive": start, "UseForAllocFlag": "N",
                       "UseForCmtCtrlFlag": "N", "UseForIcBillingFlag": "N", "ClassificationCode": pu_classification,
                       "OrgEffectiveStartDate": pu_start, "OrgEffectiveEndDate": pu_end, "OrgName": pu_name,
                       "AutoAddResFlag": "N", "LaborDisabledFlag": "N", "EquipmentDisabledFlag": "N",
                       "MaterialDisabledFlag": "N"})
        # Compare only the observed invariant values; no source unit identity is reused.
        require(all(header[k] == template_header[k] for k in
                    ("RbsType", "CentrallyControlFlag", "UseForAllocFlag", "UseForCmtCtrlFlag",
                     "UseForIcBillingFlag", "AutoAddResFlag", "LaborDisabledFlag",
                     "EquipmentDisabledFlag", "MaterialDisabledFlag")), "template header invariant mismatch")
        projected[HEADER].append(header)
        version = {key: "" for key in FIELDS[VERSION]}
        version.update({"ORA_PJF_RBS_HEADER.Name": name, "VersionNumber": "1",
                        "CurrentReportingFlag": "Y", "Description": description,
                        "Name": name, "StartDateActive": start, "StatusCode": "FROZEN", "SetCode": set_code})
        require(version["StatusCode"] == template_version["StatusCode"], "template version invariant mismatch")
        projected[VERSION].append(version)
        for member in (HEADER_TRANSLATION, VERSION_TRANSLATION):
            for old in template[member]:
                translated = dict(old)
                translated["ORA_PJF_RBS_HEADER.Name"] = name
                translated["Name"] = name
                translated["Description"] = description
                projected[member].append(translated)
        for label in selected:
            projected[FORMAT].append({"ORA_PJF_RBS_HEADER.Name": name,
                                      "ORA_PJF_RBS_VERSION.VersionNumber": "1",
                                      "ResFormatId": FORMATS[label]})
        elements = []
        for old in template[ELEMENT]:
            row = dict(old)
            row["RbsHeaderName"] = name
            if row["OutlineNumber"] == "0":
                row["Alias"] = name
            elements.append(row)
        next_outline = 5
        job_parents: set[str] = set()
        job_children: set[str] = set()
        for rindex, resource in enumerate(resources, start=1):
            label = resource["format"]
            rwhere = f"{where}.resources[{rindex}]"
            class_name, curve = TESTED_PAIR[label]
            if label in {"Organization", "Expenditure Type", "Expenditure Category"}:
                require(resource["resource_class"] == class_name and resource["spread_curve"] == curve,
                        f"{rwhere} class/curve pair was not tested; only {class_name}/{curve} is supported")
            class_code, class_id = CLASS[class_name]
            row = {key: "" for key in FIELDS[ELEMENT]}
            row.update({"OutlineNumber": str(next_outline), "RbsHeaderName": name, "VersionNumber": "1",
                        "OrderNumber": str(next_outline), "ResourceTypeId": RESOURCE_TYPES[label],
                        "EnabledFlag": "Y", "ResFormatId": FORMATS[label],
                        "ResourceClassCode": class_code, "ResourceClassId": class_id,
                        "RuleFlag": "N", "RbsLevel": "2", "LeafNodeFlag": "Y",
                        "UserCreatedFlag": "Y", "Name3": curve})
            if label in {"Job", "Job: Expenditure Category"}:
                require(set_code, f"{rwhere} needs a resolved Job Set")
                job = resolved_job(resource["job"], set_code, environment, f"{rwhere}.job")
                row.update({"JobCode": job["code"], "SetCode": set_code,
                            "EffectiveStartDate1": job["start"], "EffectiveEndDate1": job["end"]})
                if label == "Job":
                    require(job["code"] not in job_children, f"{rwhere}: standalone Job and child for same Job not tested")
                    require(job["code"] not in job_parents, f"{rwhere}: duplicate Job resource not tested")
                    job_parents.add(job["code"])
                    row["Alias"] = string(resource["alias"], f"{rwhere}.alias")
                else:
                    require(job["code"] not in job_parents and job["code"] not in job_children,
                            f"{rwhere}: duplicate Job parent or child for same Job not tested")
                    job_children.add(job["code"])
                    row["Alias"] = job["display_name"]
                    row["ResFormatId"] = FORMATS["Job"]
                    row["ResourceTypeId"] = RESOURCE_TYPES["Job"]
                    row["LeafNodeFlag"] = "N"
                    child = dict(row)
                    child.update({"OutlineNumber": f"{next_outline}.1", "OrderNumber": "1",
                                  "ResFormatId": FORMATS[label], "ResourceTypeId": RESOURCE_TYPES[label],
                                  "RbsLevel": "3", "LeafNodeFlag": "Y",
                                  "Alias": string(resource["alias"], f"{rwhere}.alias"),
                                  "ExpenditureCategoryName": string(resource["expenditure_category_name"],
                                                                    f"{rwhere}.expenditure_category_name")})
                    elements.append(row)
                    elements.append(child)
                    next_outline += 1
                    continue
            elif label == "Named Person":
                person = keys(resource["person"], {"display_name", "list_name", "person_number",
                                                   "email_address", "effective_start_date", "effective_end_date",
                                                   "enterprise_name", "enterprise_effective_start_date",
                                                   "enterprise_effective_end_date", "evidence"},
                              {"person_number", "email_address", "effective_start_date", "effective_end_date",
                               "enterprise_name", "enterprise_effective_start_date",
                               "enterprise_effective_end_date", "evidence"}, f"{rwhere}.person")
                evidence(person["evidence"], environment, f"{rwhere}.person.evidence")
                selected_name = person.get("display_name") or person.get("list_name")
                row.update({"Alias": string(selected_name, f"{rwhere}.person display/list name"),
                            "PersonNumber": string(person["person_number"], f"{rwhere}.person.person_number"),
                            "EmailAddress": string(person["email_address"], f"{rwhere}.person.email_address"),
                            "EffectiveStartDate": csv_date(person["effective_start_date"], f"{rwhere}.person.effective_start_date"),
                            "EffectiveEndDate": csv_date(person["effective_end_date"], f"{rwhere}.person.effective_end_date"),
                            "Name6": string(person["enterprise_name"], f"{rwhere}.person.enterprise_name"),
                            "EffectiveStartDate7": csv_date(person["enterprise_effective_start_date"], f"{rwhere}.person.enterprise_effective_start_date"),
                            "EffectiveEndDate7": csv_date(person["enterprise_effective_end_date"], f"{rwhere}.person.enterprise_effective_end_date")})
            elif label == "Project Nonlabor Resource":
                name_value = string(resource["nonlabor_resource_name"], f"{rwhere}.nonlabor_resource_name")
                row.update({"Alias": name_value, "NlrName": name_value})
            elif label == "Organization":
                org = keys(resource["organization"], {"name", "classification_code", "effective_start_date",
                                                        "effective_end_date", "enterprise_name",
                                                        "enterprise_effective_start_date", "enterprise_effective_end_date",
                                                        "evidence"},
                           {"name", "classification_code", "effective_start_date", "effective_end_date",
                            "enterprise_name", "enterprise_effective_start_date", "enterprise_effective_end_date",
                            "evidence"}, f"{rwhere}.organization")
                context_evidence(org["evidence"], environment, f"{rwhere}.organization.evidence")
                org_classification = string(org["classification_code"], f"{rwhere}.organization.classification_code")
                org_name = string(org["name"], f"{rwhere}.organization.name")
                row.update({"Alias": org_name, "Name5": org_name, "ClassificationCode1": org_classification,
                            "EffectiveStartDate4": csv_date(org["effective_start_date"], f"{rwhere}.organization.effective_start_date"),
                            "EffectiveEndDate4": csv_date(org["effective_end_date"], f"{rwhere}.organization.effective_end_date"),
                            "Name4": string(org["enterprise_name"], f"{rwhere}.organization.enterprise_name"),
                            "EffectiveStartDate5": csv_date(org["enterprise_effective_start_date"], f"{rwhere}.organization.enterprise_effective_start_date"),
                            "EffectiveEndDate5": csv_date(org["enterprise_effective_end_date"], f"{rwhere}.organization.enterprise_effective_end_date")})
            elif label == "Expenditure Type":
                type_name = string(resource["expenditure_type_name"], f"{rwhere}.expenditure_type_name")
                row.update({"Alias": type_name, "ExpenditureTypeName": type_name})
            elif label == "Expenditure Category":
                row.update({"Alias": string(resource["alias"], f"{rwhere}.alias"),
                            "ExpenditureCategoryName": string(resource["expenditure_category_name"],
                                                              f"{rwhere}.expenditure_category_name")})
            elements.append(row)
            next_outline += 1
        projected[ELEMENT].extend(elements)
        preview.append({"name": name, "project_unit": pu_name, "from_date": start,
                        "formats": selected, "resource_rows": len(resources),
                        "element_rows": len(elements), "root_alias": elements[0]["Alias"]})
    return projected, preview


def build(request: dict[str, Any], export_path: Path, max_age_days: int = 1) -> tuple[bytes, dict[str, Any]]:
    keys(request, {"target_environment", "source_export_sha256", "template_rbs_name",
                   "format_map", "structures"},
         {"target_environment", "source_export_sha256", "template_rbs_name",
          "format_map", "structures"}, "request")
    environment = string(request["target_environment"], "target_environment")
    digest = string(request["source_export_sha256"], "source_export_sha256")
    require(len(digest) == 64 and all(c in "0123456789abcdef" for c in digest),
            "source_export_sha256 must be a lowercase SHA-256 digest")
    require(type(max_age_days) is int and 0 <= max_age_days <= 30, "max_age_days must be 0-30")
    map_input = keys(request["format_map"], {"values", "evidence"}, {"values", "evidence"}, "format_map")
    evidence(map_input["evidence"], environment, "format_map.evidence")
    require(isinstance(map_input["values"], dict) and
            all(isinstance(label, str) and isinstance(identifier, str)
                for label, identifier in map_input["values"].items()),
            "format_map.values must map format labels to IDs")
    require(all(label in FORMATS for label in map_input["values"]),
            "format_map includes an unobserved format label")
    source, metadata, process_date = read_export(export_path, environment, digest, max_age_days)
    rows, structures = validate_and_project(request, source, environment,
                                            string(request["template_rbs_name"], "template_rbs_name"),
                                            map_input["values"])
    output = io.BytesIO()
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for member in MEMBERS:
            info = ZipInfo(member, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            archive.writestr(info, metadata if member == METADATA else write_csv(member, rows[member]))
    data = output.getvalue()
    with ZipFile(io.BytesIO(data)) as check:
        require(check.namelist() == list(MEMBERS) and check.testzip() is None,
                "generated task ZIP failed integrity validation")
    report = {"task_code": TASK_CODE, "target_environment": environment,
              "source_export_sha256": digest, "source_export_process_date": process_date,
              "archive_sha256": hashlib.sha256(data).hexdigest(),
              "row_counts": {member: len(rows[member]) for member in CSV_MEMBERS},
              "structures": structures,
              "warning": "Offline serialization only. Lookup provenance is caller-supplied, not rechecked here; Data Loader preflight and approval remain required."}
    return data, report


def workspace_paths(workspace_root: Path, input_path: Path, source_export: Path,
                    output_path: Path, preview_path: Path) -> None:
    """Require one real project workspace and its task-owned output directory."""
    projects = (REPO_ROOT / "project").resolve()
    require(workspace_root.is_dir() and not workspace_root.is_symlink() and
            workspace_root.resolve().parent == projects,
            "workspace root must be a direct project/<project_id> directory")
    root = workspace_root.resolve()
    target = root / WORKSPACE_OUTPUT
    require(target.is_dir() and target.resolve() == target and
            not any(part.is_symlink() for part in [workspace_root, *target.parents] if part != projects),
            "task artifact destination is missing or contains a symlink")
    require(output_path.parent.resolve() == target and preview_path.parent.resolve() == target,
            "ZIP and preview must be in the PRBS task artifact directory")
    require(output_path.suffix.lower() == ".zip" and preview_path.suffix.lower() == ".json",
            "task outputs must be one ZIP and one JSON preview")
    require(not output_path.is_symlink() and not preview_path.is_symlink(),
            "task output paths may not be symlinks")
    require(input_path.resolve().is_relative_to(root) and source_export.resolve().is_relative_to(root),
            "input and source export must belong to the same project workspace")
    require(source_export.resolve().is_relative_to(root / "exports"),
            "source export must be under the selected project workspace exports directory")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Validated create-batch JSON")
    parser.add_argument("--source-export", required=True, type=Path, help="Fresh complete same-target task export ZIP")
    parser.add_argument("--workspace-root", type=Path, help="Required project/<project_id> workspace for writes")
    parser.add_argument("--output", type=Path, help="New immutable seven-member task ZIP")
    parser.add_argument("--preview", type=Path, help="New JSON preview/checksum record")
    parser.add_argument("--max-export-age-days", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true", help="Validate/project without writing files")
    args = parser.parse_args(argv)
    try:
        require(args.input.is_file(), "input JSON does not exist")
        request = json.loads(args.input.read_text(encoding="utf-8"))
        require(args.dry_run or (args.output is not None and args.preview is not None),
                "--output and --preview are both required unless --dry-run is set")
        if not args.dry_run:
            require(args.workspace_root is not None, "--workspace-root is required for package writes")
            workspace_paths(args.workspace_root, args.input, args.source_export, args.output, args.preview)
            require(args.output != args.preview and args.output != args.input and args.preview != args.input,
                    "output, preview and input must be distinct")
            require(args.output != args.source_export and args.preview != args.source_export,
                    "never overwrite the source export")
            for path in (args.output, args.preview):
                require(path.parent.is_dir() and not path.exists(), f"destination must be a new file in an existing folder: {path}")
        data, report = build(request, args.source_export, args.max_export_age_days)
        if args.dry_run:
            report["status"] = "dry_run_only"
        else:
            created_output = False
            created_preview = False
            try:
                with args.output.open("xb") as handle:
                    created_output = True
                    handle.write(data)
                with args.preview.open("x", encoding="utf-8") as handle:
                    created_preview = True
                    handle.write(json.dumps(report, indent=2) + "\n")
            except BaseException:
                if created_output:
                    args.output.unlink(missing_ok=True)
                if created_preview:
                    args.preview.unlink(missing_ok=True)
                raise
            report["archive_path"] = str(args.output)
            report["preview_path"] = str(args.preview)
        print(json.dumps(report, indent=2))
        return 0
    except (ContractError, OSError, json.JSONDecodeError) as error:
        print(f"PRBS package blocked: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
