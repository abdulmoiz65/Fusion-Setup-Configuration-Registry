#!/usr/bin/env python3
"""Build self-contained TCA template and field contracts from Oracle artifacts."""

from __future__ import annotations

import argparse
import csv
import datetime
import hashlib
import io
import json
import zipfile
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
PROFILE_PATH = SKILL_DIR / "references" / "object-profiles.json"
TEMPLATE_DIR = SKILL_DIR / "assets" / "templates"
COLUMN_CONTRACT_PATH = SKILL_DIR / "references" / "column-contracts.json"
FIELD_CONTRACT_PATH = SKILL_DIR / "references" / "field-contracts.json"


CREATE_REQUIRED_FIELDS: dict[str, list[str]] = {
    "Account": ["OrganizationName"],
    "AccountContact": ["AccountPartyNumber", "ContactPartyNumber"],
    "Assets": ["AssetNumber"],
    "AssetContact": [],
    "AssetResource": [],
    "AdditionalIdentifier": ["PartyIdentifierType", "PartyIdentifierValue"],
    "AdditionalName": ["NameType"],
    "Address": ["Country", "Address1"],
    "AddressLocale": ["TransliterationLanguage"],
    "AddressPurpose": ["Purpose"],
    "Classification": ["ClassCategory", "ClassCode"],
    "ClassCode": ["ClassCategory", "ClassCode", "Meaning"],
    "Contact": ["FirstName", "LastName"],
    "ContactPoint": ["ContactPointType"],
    "Hierarchy": ["TreeStructureCode", "TreeCode", "TreeName", "TreeVersionName", "LangCode"],
    "HierarchyNode": ["TreeStructureCode", "TreeCode"],
    "GenericSourceSystemReference": [
        "SourceSystem", "SourceSystemReferenceValue", "OwnerEntityObject", "OwnerEntityId"
    ],
    "LinkedParty": ["LinkType"],
    "Organization": ["OrganizationName", "PartyUsageCode"],
    "Person": ["FirstName", "LastName", "PartyUsageCode"],
    "Relationship": ["RelationshipType", "RelationshipCode"],
    "DedupLink": ["PartyType", "LinkName"],
    "LinkMember": ["LinkNumber", "PartyNumber"],
    "SalesTeamMember": ["PartyNumber", "ResourcePartyNumber"],
    "PartySourceSystemReference": ["SourceSystem", "SourceSystemReferenceValue"],
}


REST_SCHEMA_PATHS: dict[str, tuple[str, ...]] = {
    "Account": ("accounts",),
    "AccountContact": ("accounts", "children", "AccountContact"),
    "Assets": ("assets",),
    "AssetContact": ("assets", "children", "assetContacts"),
    "AssetResource": ("assets", "children", "assetResources"),
    "AdditionalIdentifier": ("accounts", "children", "AdditionalIdentifier"),
    "AdditionalName": ("accounts", "children", "AdditionalName"),
    "Address": ("accounts", "children", "Address"),
    "AddressLocale": ("accounts", "children", "Address", "children", "AddressLocale"),
    "AddressPurpose": ("accounts", "children", "Address", "children", "AddressPurpose"),
    "Classification": ("accounts", "children", "CustomerClassification"),
    "ClassCode": ("classCodes",),
    "Contact": ("contacts",),
    "ContactPoint": ("accounts", "children", "ContactPoint"),
    "GenericSourceSystemReference": ("hubSourceSystemReferences",),
    "LinkedParty": ("hubOrganizations", "children", "LinkedParty"),
    "Organization": ("hubOrganizations",),
    "Person": ("hubPersons",),
    "Relationship": ("accounts", "children", "Relationship"),
    "DedupLink": ("resolutionLinks",),
    "LinkMember": ("resolutionLinks", "children", "LinkMember"),
    "SalesTeamMember": ("accounts", "children", "SalesTeamMember"),
    "PartySourceSystemReference": ("accounts", "children", "SourceSystemReference"),
}


REST_TYPE_MAP = {
    "string": "String",
    "integer": "Long",
    "number": "BigDecimal",
    "boolean": "Boolean",
    "date": "Date",
    "datetime": "Timestamp",
    "attachment": "Attachment",
}

OBJECT_METADATA_TYPE_MAP = {
    "java.lang.String": "String",
    "java.lang.Boolean": "Boolean",
    "java.lang.Integer": "Integer",
    "java.lang.Long": "Long",
    "java.math.BigDecimal": "BigDecimal",
    "java.sql.Date": "Date",
    "java.sql.Timestamp": "Timestamp",
    "oracle.jbo.domain.ClobDomain": "Clob",
}


# Fields absent from the CRM REST describe are backed by the Oracle interface
# table sources listed in each entry. These are data contracts, not guesses.
AUTHORITATIVE_OVERRIDES: dict[tuple[str, str], dict[str, Any]] = {
    ("ClassCode", "ClassCategory"): {"data_type": "String", "length": 30},
    ("ClassCode", "ClassCode"): {"data_type": "String", "length": 30},
    ("ClassCode", "Meaning"): {"data_type": "String", "length": 80},
    ("ClassCode", "Description"): {"data_type": "String", "length": 240},
    ("ClassCode", "ParentClassCode"): {"data_type": "String", "length": 30},
    ("ClassCode", "ModifyHierarchy"): {"data_type": "String", "length": 1, "default_value": "N"},
    ("Hierarchy", "SourceLangFlag"): {"data_type": "String", "length": 1},
    ("Hierarchy", "TreeStructureCode"): {"data_type": "String", "length": 30},
    ("Hierarchy", "TreeCode"): {"data_type": "String", "length": 30},
    ("Hierarchy", "TreeName"): {"data_type": "String", "length": 80},
    ("Hierarchy", "IconName"): {"data_type": "String", "length": 4000},
    ("Hierarchy", "TreeDescription"): {"data_type": "String", "length": 240},
    ("Hierarchy", "TreeVersionName"): {"data_type": "String", "length": 80},
    ("Hierarchy", "TreeVersionDesc"): {"data_type": "String", "length": 240},
    ("Hierarchy", "TreeVersionComment"): {"data_type": "String", "length": 4000},
    ("Hierarchy", "AsOfDate"): {"data_type": "Date"},
    ("Hierarchy", "EffectiveStartDate"): {"data_type": "Date"},
    ("Hierarchy", "EffectiveEndDate"): {"data_type": "Date"},
    ("Hierarchy", "LangCode"): {"data_type": "String", "length": 4},
    ("HierarchyNode", "AsOfDate"): {"data_type": "Date"},
    ("HierarchyNode", "LabelShortName"): {"data_type": "String", "length": 80},
    ("HierarchyNode", "ParentPartyId"): {"data_type": "Long", "precision": 18},
    ("HierarchyNode", "ParentPartyNumber"): {"data_type": "String", "length": 30},
    ("HierarchyNode", "ParentPartyOrigSysRef"): {"data_type": "String", "length": 240},
    ("HierarchyNode", "ParentPartyOrigSystem"): {"data_type": "String", "length": 30},
    ("HierarchyNode", "PartyId"): {"data_type": "Long", "precision": 18},
    ("HierarchyNode", "PartyNumber"): {"data_type": "String", "length": 30},
    ("HierarchyNode", "PartyOrigSysRef"): {"data_type": "String", "length": 240},
    ("HierarchyNode", "PartyOrigSystem"): {"data_type": "String", "length": 30},
    ("HierarchyNode", "TreeCode"): {"data_type": "String", "length": 30},
    ("HierarchyNode", "TreeStructureCode"): {"data_type": "String", "length": 30},
    ("LinkMember", "DedupLinkMemberId"): {"data_type": "Long", "precision": 18},
}


OVERRIDE_SOURCES = {
    "ClassCode": "https://docs.oracle.com/en/cloud/saas/sales/oedms/hzclasscodesint-21868.html",
    "Hierarchy": "https://docs.oracle.com/en/cloud/saas/sales/oedms/hzhierarchiesint-16283.html",
    "HierarchyNode": "https://docs.oracle.com/en/cloud/saas/sales/oedms/hzhierarchynodesint-9474.html",
    "LinkMember": "https://docs.oracle.com/en/cloud/saas/sales/oedms/zchdeduplinkmembers-20890.html",
}


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_node(resources: dict[str, Any], path: tuple[str, ...]) -> dict[str, Any]:
    node: Any = resources
    for part in path:
        node = node[part]
    if not isinstance(node, dict):
        raise ValueError(f"REST schema path did not resolve to an object: {'/'.join(path)}")
    return node


def latest_template_zip(downloads_dir: Path, display_name: str) -> Path:
    matches = list(downloads_dir.glob(f"{display_name}_Templates_*.zip"))
    if not matches:
        raise ValueError(f"No downloaded template ZIP found for {display_name}")
    return max(matches, key=lambda path: (path.stat().st_mtime_ns, path.name))


def read_template(zip_path: Path, template_filename: str) -> tuple[bytes, list[str], list[str]]:
    with zipfile.ZipFile(zip_path) as archive:
        csv_names = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if csv_names != [template_filename]:
            raise ValueError(
                f"{zip_path.name} must contain exactly {template_filename}; found {csv_names}"
            )
        content = archive.read(template_filename)
    try:
        rows = list(csv.reader(io.StringIO(content.decode("utf-8-sig"), newline="")))
    except UnicodeDecodeError as exc:
        raise ValueError(f"{zip_path.name}/{template_filename} is not UTF-8") from exc
    if len(rows) != 2 or not rows[0] or len(rows[0]) != len(rows[1]):
        raise ValueError(f"{zip_path.name}/{template_filename} must contain two equal-width rows")
    if len(set(rows[0])) != len(rows[0]) or any(not header for header in rows[0]):
        raise ValueError(f"{zip_path.name}/{template_filename} has blank or duplicate headers")
    return content, rows[0], rows[1]


def object_metadata(path: Path | None) -> dict[str, dict[str, Any]]:
    if not path:
        return {}
    payload = load_json(path)
    return {item["AttributeCode"]: item for item in payload.get("items", [])}


def ui_metadata(path: Path | None) -> dict[str, dict[str, Any]]:
    if not path or not path.exists():
        return {}
    payload = load_json(path)
    return {item["attributeName"]: item for item in payload}


def integer_or_none(value: Any) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def build_field(
    *,
    object_code: str,
    column_name: str,
    display_name: str,
    rest_attribute: dict[str, Any] | None,
    object_attribute: dict[str, Any] | None,
    ui_attribute: dict[str, Any] | None,
    create_required: set[str],
    identity_sets: list[list[str]],
) -> dict[str, Any]:
    data_type = None
    type_source = None
    length = None
    precision = None
    mandatory = None
    mandatory_source = None
    default_value = None
    description = None
    updatable = None

    if rest_attribute:
        data_type = REST_TYPE_MAP.get(rest_attribute.get("type"), rest_attribute.get("type"))
        type_source = "oracle_crm_rest_describe"
        length = integer_or_none(rest_attribute.get("maxLength"))
        precision = integer_or_none(rest_attribute.get("precision"))
        mandatory = rest_attribute.get("mandatory") if isinstance(rest_attribute.get("mandatory"), bool) else None
        mandatory_source = "oracle_crm_rest_describe" if mandatory is not None else None
        default_value = rest_attribute.get("defaultValue")
        description = rest_attribute.get("description")
        updatable = rest_attribute.get("updatable") if isinstance(rest_attribute.get("updatable"), bool) else None

    if object_attribute:
        object_type = object_attribute.get("AttributeType")
        data_type = OBJECT_METADATA_TYPE_MAP.get(object_type, object_type) or data_type
        type_source = "oracle_import_object_metadata"
        flag = object_attribute.get("MandatoryFlag")
        mandatory = flag == "Y" if flag in {"Y", "N"} else mandatory
        mandatory_source = "oracle_import_object_metadata" if flag in {"Y", "N"} else mandatory_source
        update_flag = object_attribute.get("IsUpdatableFlag")
        updatable = update_flag == "Y" if update_flag in {"Y", "N"} else updatable
        description = object_attribute.get("Description") or description

    if ui_attribute:
        data_type = ui_attribute.get("dataType") or data_type
        type_source = "fusion_manage_import_objects_ui"
        length = integer_or_none(ui_attribute.get("length")) or length
        mandatory = ui_attribute.get("required") if isinstance(ui_attribute.get("required"), bool) else mandatory
        mandatory_source = "fusion_manage_import_objects_ui" if isinstance(ui_attribute.get("required"), bool) else mandatory_source
        default_value = ui_attribute.get("defaultValue") or default_value
        description = ui_attribute.get("description") or description

    override = AUTHORITATIVE_OVERRIDES.get((object_code, column_name))
    if override:
        data_type = override["data_type"]
        length = override.get("length", length)
        precision = override.get("precision", precision)
        default_value = override.get("default_value", default_value)
        type_source = "oracle_interface_table_documentation"

    if not data_type:
        raise ValueError(f"No authoritative data type resolved for {object_code}.{column_name}")

    identity_membership = [identity for identity in identity_sets if column_name in identity]
    return {
        "column_name": column_name,
        "display_name": display_name,
        "data_type": data_type,
        "length": length,
        "precision": precision,
        "default_value": default_value,
        "description": description,
        "metadata_required": mandatory,
        "metadata_required_source": mandatory_source,
        "updatable": updatable,
        "required_for_create_by_skill": column_name in create_required,
        "identity_set_membership": identity_membership,
        "type_source": type_source,
        "allowed_values": ui_attribute.get("allowedValues") if ui_attribute else None,
        "allowed_values_note": (
            ui_attribute.get("allowedValuesNote")
            if ui_attribute and ui_attribute.get("allowedValuesNote")
            else "Resolve target-active lookup/reference values at runtime when the field is coded."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--downloads-dir", required=True, type=Path)
    parser.add_argument("--rest-describe", type=Path)
    parser.add_argument("--account-object-metadata", type=Path)
    parser.add_argument("--contact-object-metadata", type=Path)
    parser.add_argument("--ui-metadata-dir", type=Path)
    parser.add_argument(
        "--object", dest="object_names", action="append", default=[],
        help="Regenerate only one exact display name or object code; repeat for multiple objects.",
    )
    parser.add_argument(
        "--source-date", default=datetime.date.today().isoformat(),
        help="Capture date for regenerated Oracle template and UI metadata sources.",
    )
    args = parser.parse_args()

    if not args.object_names and not args.rest_describe:
        parser.error("--rest-describe is required for a full catalog regeneration")

    all_profiles = load_json(PROFILE_PATH)["objects"]
    if args.object_names:
        requested = {value.casefold() for value in args.object_names}
        profiles = [
            profile for profile in all_profiles
            if profile["object_code"].casefold() in requested
            or profile["display_name"].casefold() in requested
        ]
        matched = {
            value.casefold() for profile in profiles
            for value in (profile["object_code"], profile["display_name"])
        }
        missing = sorted(requested - matched)
        if missing:
            raise ValueError("Unknown object selection: " + ", ".join(missing))
    else:
        profiles = all_profiles
    resources = load_json(args.rest_describe)["Resources"] if args.rest_describe else {}
    explicit_metadata = {
        "Account": object_metadata(args.account_object_metadata),
        "Contact": object_metadata(args.contact_object_metadata),
    }
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

    incremental = bool(args.object_names)
    existing_columns = load_json(COLUMN_CONTRACT_PATH) if incremental and COLUMN_CONTRACT_PATH.exists() else {}
    existing_fields = load_json(FIELD_CONTRACT_PATH) if incremental and FIELD_CONTRACT_PATH.exists() else {}
    column_contracts: dict[str, Any] = dict(existing_columns.get("contracts", {}))
    field_objects: dict[str, Any] = dict(existing_fields.get("objects", {}))
    selected_names = {profile["display_name"] for profile in profiles}
    source_artifacts: list[dict[str, Any]] = [
        item for item in existing_fields.get("sources", {}).get("templates", [])
        if item.get("display_name") not in selected_names
    ]

    for profile in profiles:
        object_code = profile["object_code"]
        display_name = profile["display_name"]
        template_filename = profile["template_filename"]
        zip_path = latest_template_zip(args.downloads_dir, display_name)
        content, headers, display_headers = read_template(zip_path, template_filename)
        destination = TEMPLATE_DIR / template_filename
        destination.write_bytes(content)

        column_contracts[object_code] = {
            "template_filename": template_filename,
            "template_asset": f"assets/templates/{template_filename}",
            "template_sha256": sha256_bytes(content),
            "full_headers": headers,
            "display_headers": display_headers,
        }
        source_artifacts.append({
            "display_name": display_name,
            "zip_filename": zip_path.name,
            "template_filename": template_filename,
            "template_sha256": sha256_bytes(content),
            "downloaded_on": args.source_date,
        })

        rest_attributes: dict[str, dict[str, Any]] = {}
        rest_path = REST_SCHEMA_PATHS.get(object_code)
        if rest_path and resources:
            rest_attributes = {
                item["name"]: item
                for item in schema_node(resources, rest_path).get("attributes", [])
                if isinstance(item, dict) and item.get("name")
            }
        object_attributes = explicit_metadata.get(object_code, {})
        ui_path = args.ui_metadata_dir / f"{object_code}.json" if args.ui_metadata_dir else None
        ui_attributes = ui_metadata(ui_path)
        create_required = set(CREATE_REQUIRED_FIELDS[object_code])
        identity_sets = profile["identity_sets"]
        delete_identity_sets = profile.get("delete_identity_sets", identity_sets)
        fields = [
            build_field(
                object_code=object_code,
                column_name=column,
                display_name=display,
                rest_attribute=rest_attributes.get(column),
                object_attribute=object_attributes.get(column),
                ui_attribute=ui_attributes.get(column),
                create_required=create_required,
                identity_sets=identity_sets,
            )
            for column, display in zip(headers, display_headers)
        ]
        field_objects[object_code] = {
            "display_name": display_name,
            "template_filename": template_filename,
            "template_asset": f"assets/templates/{template_filename}",
            "field_count": len(fields),
            "required_fields": {
                "create": CREATE_REQUIRED_FIELDS[object_code],
                "create_or_update_identity_alternatives": identity_sets,
                "delete_identity_alternatives": delete_identity_sets if "delete" in profile["operations"] else [],
                "metadata_required": [
                    field["column_name"] for field in fields if field["metadata_required"] is True
                ],
            },
            "requiredness_notes": [
                "create is enforced by the skill's minimum field list plus object-specific conditional rules",
                "create-or-update and delete require one complete supported identity set",
                "metadata_required is descriptive Oracle metadata and is not blindly enforced as a CSV rule",
            ],
            "fields": fields,
        }

    COLUMN_CONTRACT_PATH.write_text(
        json.dumps({
            "schema_version": 2,
            "source": f"Oracle Import Management templates downloaded through {args.source_date}",
            "contracts": column_contracts,
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    FIELD_CONTRACT_PATH.write_text(
        json.dumps({
            "schema_version": 1,
            "generated_on": args.source_date,
            "scope": f"All columns in the {len(field_objects)} supported Trading Community import templates",
            "sources": {
                "templates": source_artifacts,
                "rest_describe": "Oracle CRM REST describe captured from the target-family environment",
                "import_object_metadata": "Oracle objectMetadata attribute payloads for Account and Contact",
                "import_objects_ui": "Oracle Import Object Details UI metadata supplied through --ui-metadata-dir",
                "interface_table_documentation": OVERRIDE_SOURCES,
            },
            "allowed_values_policy": (
                "No environment-sensitive lookup list is frozen in this catalog. Resolve and validate active "
                "lookup/reference values against the exact target immediately before import."
            ),
            "objects": field_objects,
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(field_objects)} object contracts and {sum(x['field_count'] for x in field_objects.values())} fields")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
