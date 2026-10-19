"""Authenticated read-only CPQ registration, state and load-completion checks."""

from __future__ import annotations

import re
import urllib.parse
from typing import Any, Mapping

import sys
from pathlib import Path
import cpq_approval_contract as contract

CORE_ROOT = Path(__file__).resolve().parents[6] / "core"
sys.path.insert(0, str(CORE_ROOT / "data-loader/scripts"))
import upload_and_initiate as loader
metadata = loader.metadata


ASSISTANT_NAME = "SA_SETUP_ASSISTANT"
ASSISTANT_PATH = "/crmRestApi/resources/latest/setupAssistants/" + ASSISTANT_NAME
DATA_SETS_PATH = "/hcmRestApi/resources/latest/dataLoaderDataSets"
COMPANY_LOV_PATH = "/crmRestApi/resources/latest/setupAssistantsLOV"
_COMPANY_LOV_TYPES = {
    "Country": "CompanyProfilesCountry", "CorporateCurrency": "CompanyProfilesCurrency",
    "LegalEntity": "LegalEntity", "BusinessUnit": "BusinessUnit",
}
_CHILDREN = ("CompanyProfiles", "CPQUsers", "CPQRoleMappings", "CPQStarterDataImport", "SetupProgress")
_MAX_ITEMS = 10000
_PAGE_SIZE = 500
_COMPANY_FIELDS = {
    "DOESNT_EXIST": frozenset({"EnterpriseName", "CompanyName", "Addressline", "Country", "CorporateCurrency", "TaxRegNumber"}),
    "EXISTS": frozenset({"CompanyName", "LegalEntity", "BusinessUnit", "CorporateCurrency"}),
    "EXISTS_WITH_BU": frozenset({"CompanyName", "LegalEntity", "CorporateCurrency"}),
}
_EXISTING_LEGAL_ENTITY_DERIVED_FIELDS = frozenset({"Addressline", "Country", "TaxRegNumber"})
_COMPANY_ROUTING = frozenset({"Id", "CompanyProfileId", "Name", "RestAction", "Content-Type", "REST-Framework-Version"})
_PROGRESS_TASKS = {
    "SA_COMPANY_INFORMATION": "Company Information",
    "SA_CPQ_ADMIN_USERS": "Application Administrators",
    "SA_CPQ_REFDATA_IMPORT": "Import of Starter Data",
    "SA_CPQ_RESOURCE_ROLES": "Resource Roles and Role Mappings",
}


def _clean(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _clean(item) for key, item in value.items() if key not in {"links", "@context"}}
    if isinstance(value, list):
        return [_clean(item) for item in value]
    return value


def collection(
    path: str, config: Mapping[str, Any], *, query: Mapping[str, Any] | None = None,
    getter=metadata.get_json,
) -> list[dict[str, Any]]:
    """Read every page through a fixed same-host path; never follow response URLs."""
    records: list[dict[str, Any]] = []
    page_digests: set[str] = set()
    while True:
        params = {**(query or {}), "onlyData": "true", "limit": _PAGE_SIZE, "offset": len(records)}
        response = getter(
            config["host"] + path + "?" + urllib.parse.urlencode(params), config["auth"],
            stage="cpq-state-validation",
        )
        if not isinstance(response, dict) or not isinstance(response.get("items"), list) or type(response.get("hasMore")) is not bool:
            raise contract.ContractError("CPQ discovery requires a complete, paginated collection response.")
        items = response["items"]
        if any(not isinstance(item, dict) for item in items):
            raise contract.ContractError("CPQ discovery returned an invalid collection record.")
        fingerprint = contract.digest(items)
        if items and fingerprint in page_digests:
            raise contract.ContractError("CPQ discovery repeated a page; completeness is unproven.")
        page_digests.add(fingerprint)
        records.extend(_clean(items))
        if len(records) > _MAX_ITEMS:
            raise contract.ContractError("CPQ discovery exceeds the supported complete-collection limit.")
        if not response["hasMore"]:
            return records
        if not items:
            raise contract.ContractError("CPQ discovery pagination did not advance.")


def _assistant(config: Mapping[str, Any], getter) -> dict[str, Any]:
    result = getter(config["host"] + ASSISTANT_PATH + "?onlyData=true", config["auth"], stage="cpq-state-validation")
    return _assistant_identity(result)


def _assistant_identity(result: Any) -> dict[str, Any]:
    if not isinstance(result, dict) or result.get("Name") != ASSISTANT_NAME or not result.get("Id"):
        raise contract.ContractError("CPQ Setup Assistant identity is missing or ambiguous.")
    if not isinstance(result.get("Status"), str):
        raise contract.ContractError("CPQ Setup Assistant status is indeterminate.")
    return {key: result[key] for key in ("Id", "Name", "Status")}


def discover_state(config: Mapping[str, Any], *, getter=metadata.get_json) -> dict[str, Any]:
    """Snapshot complete child collections and bracket them with parent reads."""
    before = _assistant(config, getter)
    state: dict[str, Any] = {"assistant": before}
    for child in _CHILDREN:
        rows = collection(ASSISTANT_PATH + "/child/" + child, config, getter=getter)
        state[child] = sorted(rows, key=contract.canonical_bytes)
    state["CompanyLOV"] = sorted(
        (row for row in collection(COMPANY_LOV_PATH, config, getter=getter)
         if row.get("LookupType") in _COMPANY_LOV_TYPES.values()),
        key=contract.canonical_bytes,
    )
    if _assistant(config, getter) != before:
        raise contract.ContractError("CPQ Setup Assistant changed during discovery; start a fresh review.")
    return state


def parse_registered_archive(
    content: bytes, config: Mapping[str, Any], *, getter=metadata.get_json,
    byte_getter=metadata.get_bytes,
) -> contract.ParsedArchive:
    registrations = {}
    schemas = {}
    member_schemas = {}
    for name, payload in contract.archive_members(content):
        sections = metadata.parse_source_sections(payload, source_name="CPQ prepared member")
        section_names = {section.discriminator for section in sections}
        if section_names == {contract.INITIALIZE}:
            root = contract.INITIALIZE
        elif section_names and section_names <= {contract.ASSISTANT, contract.COMPANY, contract.ADMIN}:
            root = contract.ASSISTANT
        else:
            raise contract.ContractError("CPQ archive has unknown, mixed or retired registration sections.")
        if root not in schemas:
            schemas[root] = metadata.load_business_object_schema(
                root, config, allow_aliases=False, getter=getter, byte_getter=byte_getter,
            )
        schema = schemas[root]
        if schema.discriminator != root:
            raise contract.ContractError("CPQ authoritative registration does not match the intended root.")
        metadata.validate_source_sections(sections, schema)
        registrations[name] = contract.Registration.from_schema(schema)
        member_schemas[name] = schema
    parsed = contract.parse_archive(content, registrations)
    for operation in parsed.operations:
        values = dict(operation.fields)
        attributes = member_schemas[operation.member].attributes.get(operation.section, ())
        for attribute in attributes:
            name = metadata.normalize_attribute_name(attribute.get("AttributeName", ""))
            if name in {"Content-Type", "REST-Framework-Version"}:
                required = metadata.is_mandatory(attribute) or (values.get("RestAction") == "POST" and metadata.is_required_for_create(attribute))
                if required and not values.get(name, "").strip():
                    raise contract.ContractError("CPQ row omits a registered required transport value; do not infer a default.")
        if operation.section == contract.INITIALIZE:
            _validate_initialization_metadata(operation, member_schemas[operation.member])
        elif operation.section == contract.ADMIN:
            _validate_admin_create_metadata(operation, member_schemas[operation.member])
    return parsed


def _validate_initialization_metadata(operation: contract.Operation, schema: Any) -> None:
    """Require independently registered values, never invented transport inputs.

    Core's metadata projection has no default-value/derivation contract. A
    required value therefore must be explicit; a claimed default cannot waive it.
    """
    attributes = schema.attributes.get(contract.INITIALIZE)
    if not attributes:
        raise contract.ContractError("CPQ initialization requires complete live attribute metadata.")
    values = dict(operation.fields)
    by_name = {}
    for attribute in attributes:
        if not isinstance(attribute, dict) or not isinstance(attribute.get("AttributeName"), str):
            raise contract.ContractError("CPQ initialization attribute metadata is malformed.")
        name = metadata.normalize_attribute_name(attribute["AttributeName"])
        if not name or name in by_name:
            raise contract.ContractError("CPQ initialization attribute metadata is ambiguous.")
        code = attribute.get("MandatoryStatusCode")
        label = str(attribute.get("MandatoryStatus") or "").strip().lower()
        expected_labels = {"ORA_Y": "yes", "ORA_W": "for new records", "ORA_N": "no"}
        if (code is not None and code not in expected_labels) or (code is None and label not in expected_labels.values()):
            raise contract.ContractError("CPQ initialization attribute requirement is unknown.")
        if code in expected_labels and label and label != expected_labels[code]:
            raise contract.ContractError("CPQ initialization attribute requirements are contradictory.")
        by_name[name] = attribute
        if (metadata.is_mandatory(attribute) or metadata.is_required_for_create(attribute)) and not values.get(name, "").strip():
            raise contract.ContractError("CPQ initialization omits a live registration-required value; do not infer a default.")
    if "RestAction" not in by_name or any(name not in by_name for name in values):
        raise contract.ContractError("CPQ initialization header is not supported by complete live attribute metadata.")


def _is_admin_create_required(attribute: Mapping[str, Any]) -> bool:
    """Accept fields required for every operation or specifically for create."""
    return metadata.is_mandatory(attribute) or metadata.is_required_for_create(attribute)


def _validate_admin_create_metadata(operation: contract.Operation, schema: Any) -> None:
    """Do not let a compact DAT header weaken the live create contract."""
    attributes = schema.attributes.get(contract.ADMIN)
    if not attributes:
        raise contract.ContractError("CPQ administrator creation requires complete live attribute metadata.")
    by_name = {}
    for attribute in attributes:
        if not isinstance(attribute, dict) or not isinstance(attribute.get("AttributeName"), str):
            raise contract.ContractError("CPQ administrator attribute metadata is malformed.")
        name = metadata.normalize_attribute_name(attribute["AttributeName"])
        if name in by_name:
            raise contract.ContractError("CPQ administrator attribute metadata is ambiguous.")
        by_name[name] = attribute
    for name in ("FirstName", "LastName", "Email"):
        if name not in by_name or not _is_admin_create_required(by_name[name]):
            raise contract.ContractError("CPQ administrator registration is missing a required create-field designation.")
    values = dict(operation.fields)
    for name, attribute in by_name.items():
        if name in {"CPQUserId", "Id", "PartyNumber", "UserName"}:
            # The CPQ-specific create contract owns these generated identities.
            # A generic required designation does not make them caller input.
            if values.get(name):
                raise contract.ContractError("New CPQ administrators must not supply generated identities.")
            continue
        if _is_admin_create_required(attribute) and not values.get(name, "").strip():
            raise contract.ContractError("A CPQ administrator row omits a registered create-required value.")


def _identity(value: Any) -> str:
    if isinstance(value, bool) or not isinstance(value, (str, int)) or not str(value).strip():
        raise contract.ContractError("CPQ discovery did not supply a usable record identity.")
    return str(value)


def validate_operations(parsed: contract.ParsedArchive, state: Mapping[str, Any]) -> None:
    """Bind row targets to discovery and preserve the existing CPQ branch rules."""
    assistant = state.get("assistant", {})
    if assistant.get("Name") != ASSISTANT_NAME or assistant.get("Status") != "SETUP_NOT_DONE":
        raise contract.ContractError("CPQ mutation requires the discovered, not-yet-submitted Setup Assistant.")
    if parsed.stage == "initialize":
        return
    profiles = state.get("CompanyProfiles")
    users = state.get("CPQUsers")
    if not isinstance(profiles, list) or len(profiles) != 1 or not isinstance(users, list):
        raise contract.ContractError("CPQ configuration requires one discovered Company Profile and complete administrator state.")
    profile = profiles[0]
    profile_id = _identity(profile.get("CompanyProfileId") or profile.get("Id"))
    branch = profile.get("IsDataExisting")
    if branch not in _COMPANY_FIELDS:
        raise contract.ContractError("CPQ company state is incomplete or processing; no mutation is permitted.")
    known_emails: set[str] = set()
    for user in users:
        email = user.get("Email")
        if not isinstance(email, str) or not email.strip() or email.casefold() in known_emails:
            raise contract.ContractError("CPQ administrator discovery is incomplete or ambiguous.")
        known_emails.add(email.casefold())
    proposed_admins = 0
    for operation in parsed.operations:
        values = dict(operation.fields)
        if "Name" in values and values["Name"] != ASSISTANT_NAME:
            raise contract.ContractError("CPQ parent routing does not match the discovered Setup Assistant.")
        if operation.section == contract.COMPANY:
            if values.get("CompanyProfileId") != profile_id:
                raise contract.ContractError("Company Profile routing must match the discovered profile identity.")
            if values.get("Id") and values["Id"] != profile_id:
                raise contract.ContractError("Company Profile identity differs from discovery.")
            allowed = _COMPANY_FIELDS[branch] | _COMPANY_ROUTING
            if any(value and key not in allowed for key, value in operation.fields):
                raise contract.ContractError("Company Profile changes exceed the discovered business branch.")
        elif operation.section == contract.ADMIN:
            email = values["Email"]
            if not re.fullmatch(r"[^\s@|]+@[^\s@|]+\.[^\s@|]+", email) or email.casefold() in known_emails:
                raise contract.ContractError("CPQ administrator email is invalid or already exists.")
            if any(value and key not in {"FirstName", "LastName", "Email", "Name", "RestAction", "Content-Type", "REST-Framework-Version"} for key, value in operation.fields):
                raise contract.ContractError("CPQ administrator creation contains unsupported additional values.")
            proposed_admins += 1
    if not known_emails and not proposed_admins:
        raise contract.ContractError("CPQ configuration requires at least one existing or approved new administrator.")
    _validate_company_readiness(parsed, profile, state)
    if parsed.stage == "submit":
        _validate_starter_readiness(state)


def _validate_company_readiness(
    parsed: contract.ParsedArchive, profile: Mapping[str, Any], state: Mapping[str, Any],
) -> None:
    """Validate retained and proposed business values against complete live LOVs."""
    branch = profile["IsDataExisting"]
    effective = dict(profile)
    for operation in parsed.operations:
        if operation.section == contract.COMPANY:
            effective.update({key: value for key, value in operation.fields if value and key in _COMPANY_FIELDS[branch]})
    required = {"CompanyName", "CorporateCurrency"}
    choices = {"CorporateCurrency"}
    if branch == "DOESNT_EXIST":
        required.update({"EnterpriseName", "Addressline", "Country"})
        choices.add("Country")
        if effective.get("Country") == "BR":
            required.add("TaxRegNumber")
    else:
        required.update({"LegalEntity", "BusinessUnit"})
        choices.add("LegalEntity")
        if branch == "EXISTS":
            choices.add("BusinessUnit")
    if any(not isinstance(effective.get(key), str) or not effective[key].strip() for key in required):
        raise contract.ContractError("CPQ company proposal lacks required values for the discovered branch.")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,79}", effective["CompanyName"]):
        raise contract.ContractError("CPQ company identifier must use 1–80 ASCII letters, digits or hyphens and start with a letter or digit.")
    # Source: CompanyProfileVO updatable-field contract. No address parsing or
    # UI-only company-name semantics are inferred from these length limits.
    for key in required | _COMPANY_FIELDS[branch]:
        value = effective.get(key)
        maximum = 100 if key in {"Addressline", "EnterpriseName"} else 80
        if value is not None and (not isinstance(value, str) or len(value) > maximum):
            raise contract.ContractError("CPQ company value exceeds the documented field contract.")
    lovs = state.get("CompanyLOV")
    if not isinstance(lovs, list) or any(not isinstance(row, dict) for row in lovs):
        raise contract.ContractError("CPQ company validation requires complete current LOV discovery.")
    for key in choices:
        matches = [row for row in lovs if row.get("LookupType") == _COMPANY_LOV_TYPES[key]
                   and row.get("LookupCode") == effective[key]]
        if len(matches) != 1:
            raise contract.ContractError("A retained or proposed CPQ company selection is missing or ambiguous in current LOVs.")


def _validate_starter_readiness(state: Mapping[str, Any]) -> None:
    """The starter child is presence-only; progress supplies processing state."""
    progress = state.get("SetupProgress")
    if not isinstance(progress, list) or any(not isinstance(row, dict) for row in progress):
        raise contract.ContractError("CPQ final submission requires current starter-data progress.")
    rows = [row for row in progress if row.get("TaskCode") == "SA_CPQ_REFDATA_IMPORT"]
    if (len(rows) != 1 or rows[0].get("TaskStatusCode") not in {"SETUP_NOT_DONE", "COMPLETED"}
            or rows[0].get("ErrorMessage")):
        raise contract.ContractError("CPQ starter data is running, failed or indeterminate; do not submit.")


def business_notices(state: Mapping[str, Any]) -> dict[str, Any]:
    """Project only the read-only role mappings and starter-data business state."""
    mappings = state.get("CPQRoleMappings")
    starter = state.get("CPQStarterDataImport")
    progress = state.get("SetupProgress")
    if any(not isinstance(rows, list) for rows in (mappings, starter, progress)):
        raise contract.ContractError("CPQ approval requires discovered role and starter-data notices.")
    roles = []
    for row in mappings:
        if not isinstance(row, dict) or any(not isinstance(row.get(key), str) or not row[key].strip() for key in ("ResourceRoleName", "RoleCommonNameCode")):
            raise contract.ContractError("CPQ discovered role mappings are incomplete; do not invent a notice.")
        roles.append({"resourceRole": row["ResourceRoleName"], "applicationRole": row["RoleCommonNameCode"]})
    rows = [row for row in progress if isinstance(row, dict) and row.get("TaskCode") == "SA_CPQ_REFDATA_IMPORT"]
    status = "indeterminate"
    if len(rows) == 1:
        status = {"SETUP_NOT_DONE": "ready", "IN_PROGRESS": "running", "COMPLETED": "complete", "ERROR": "failed"}.get(rows[0].get("TaskStatusCode"), "indeterminate")
        if rows[0].get("ErrorMessage"):
            status = "failed"
    return {
        "roleMappings": roles, "roleMappingAvailability": "available" if roles else "unavailable",
        "starterDataAvailability": "available" if starter else "unavailable",
        "starterDataState": status, "readOnly": True,
    }


def require_load_complete(
    result: Mapping[str, Any], config: Mapping[str, Any], *, getter=metadata.get_json,
) -> dict[str, Any]:
    """One read-only reconciliation; initiation SUCCESS alone never advances a stage."""
    request_id = str(result.get("RequestId", ""))
    if not re.fullmatch(r"[1-9][0-9]*", request_id):
        raise contract.ContractError("CPQ stage has no valid initiation request to reconcile.")
    rows = collection(DATA_SETS_PATH, config, query={"q": "DataSetRequestId=" + request_id}, getter=getter)
    if len(rows) != 1:
        raise contract.ContractError("CPQ load outcome is pending or ambiguous; no next-stage mutation is permitted.")
    row = rows[0]
    if (
        str(row.get("DataSetRequestId")) != request_id
        or row.get("UcmContentId") != result.get("ContentId")
        or row.get("DataSetName") != result.get("dataSetName")
    ):
        raise contract.ContractError("CPQ load completion does not identify the approved stage request.")
    if not (
        row.get("DataSetStatus") == "ORA_SUCCESS"
        and row.get("ImportedStatus") == "SUCCESS"
        and row.get("LoadedStatus") == "SUCCESS"
    ):
        raise contract.ContractError("CPQ load has not completed successfully; reconcile before proceeding.")
    for key in ("FileLineImportErrorCount", "ImportErrorCount", "LineErrorCount", "ObjectErrorCount", "UnprocessedCount", "PendingObjects"):
        if str(row.get(key)) != "0":
            raise contract.ContractError("CPQ load has errors, pending records or incomplete completion evidence.")
    return {key: row.get(key) for key in ("DataSetId", "DataSetRequestId", "UcmContentId", "DataSetStatus", "ImportedStatus", "LoadedStatus")}


def verify_child_outcome(
    parsed: contract.ParsedArchive, before: Mapping[str, Any], after: Mapping[str, Any],
) -> None:
    """Reconcile the approved child result, not merely a successful loader job."""
    if parsed.stage != "children" or before.get("assistant") != after.get("assistant"):
        raise contract.ContractError("CPQ assistant identity or state changed during child import.")
    prior_profiles = before.get("CompanyProfiles", [])
    current_profiles = after.get("CompanyProfiles", [])
    if len(prior_profiles) != 1 or len(current_profiles) != 1:
        raise contract.ContractError("CPQ child reconciliation requires one unchanged Company Profile identity.")
    prior_profile, current_profile = prior_profiles[0], current_profiles[0]
    for key in ("Id", "CompanyProfileId", "IsDataExisting"):
        if prior_profile.get(key) != current_profile.get(key):
            raise contract.ContractError("CPQ Company Profile identity or branch changed during child import.")
    company_values = {key: prior_profile.get(key) for fields in _COMPANY_FIELDS.values() for key in fields}
    approved_company_fields: set[str] = set()
    prior_users = before.get("CPQUsers", [])
    current_users = after.get("CPQUsers", [])
    expected_users = {}
    for user in prior_users:
        email = user.get("Email")
        if not isinstance(email, str) or email.casefold() in expected_users:
            raise contract.ContractError("Prior CPQ administrator state cannot be reconciled safely.")
        expected_users[email.casefold()] = {key: user.get(key) for key in ("Id", "CPQUserId", "FirstName", "LastName", "Email")}
    for operation in parsed.operations:
        values = dict(operation.fields)
        if operation.section == contract.COMPANY:
            for key in company_values:
                if key in values and values[key] != "":
                    company_values[key] = values[key]
                    approved_company_fields.add(key)
        elif operation.section == contract.ADMIN:
            key = values["Email"].casefold()
            if key in expected_users:
                raise contract.ContractError("Approved administrator duplicates prior CPQ state.")
            expected_users[key] = {name: values[name] for name in ("FirstName", "LastName", "Email")}
    for key, expected in company_values.items():
        # REST may serialize identifiers as numbers and empty fields as null.
        actual = current_profile.get(key)
        server_derived = (
            prior_profile.get("IsDataExisting") in {"EXISTS", "EXISTS_WITH_BU"}
            and "LegalEntity" in approved_company_fields
            and key in _EXISTING_LEGAL_ENTITY_DERIVED_FIELDS
            and str(expected if expected is not None else "") == ""
            and str(actual if actual is not None else "") != ""
        )
        if server_derived:
            continue
        if str(actual if actual is not None else "") != str(expected if expected is not None else ""):
            raise contract.ContractError("Rediscovered Company Profile does not match the approved child outcome.")
    found = set()
    for user in current_users:
        email = user.get("Email")
        if not isinstance(email, str) or email.casefold() not in expected_users or email.casefold() in found:
            raise contract.ContractError("Rediscovered administrator set differs from the approved child outcome.")
        key = email.casefold()
        found.add(key)
        for name, expected in expected_users[key].items():
            actual = user.get(name)
            if name == "Email":
                actual, expected = actual.casefold(), expected.casefold()
            if actual != expected:
                raise contract.ContractError("Rediscovered administrator identity differs from the approved child outcome.")
    if found != set(expected_users):
        raise contract.ContractError("An approved administrator is missing after child import.")
