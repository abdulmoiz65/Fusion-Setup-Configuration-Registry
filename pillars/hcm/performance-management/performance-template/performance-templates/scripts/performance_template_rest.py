#!/usr/bin/env python3
"""Preview and execute one approval-bound Performance Templates REST request."""

from __future__ import annotations

import argparse
from datetime import date
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Sequence
from urllib.parse import quote, urlparse


TASK_ROOT = Path(__file__).resolve().parents[1]
FSCR_ROOT = Path(__file__).resolve().parents[6]
CONTRACT_PATH = TASK_ROOT / "ora-resource" / "ora_rest_execution.json"
REST_SCRIPTS = FSCR_ROOT / "core" / "fusion-api" / "rest-api-client" / "scripts"
AUTH_SCRIPTS = FSCR_ROOT / "core" / "auth" / "fusion-oauth-authentication" / "scripts"
sys.path.insert(0, str(REST_SCRIPTS))
sys.path.insert(0, str(AUTH_SCRIPTS))

from fusion_auth import FusionHttpError, get_access_token, read_properties, require_props  # noqa: E402
from rest_client_common import build_url, request_bytes  # noqa: E402


class ContractError(ValueError):
    """The requested operation is outside the declared safe contract."""


def read_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ContractError(f"{label} is unavailable or invalid JSON: {path}") from error
    if not isinstance(value, dict):
        raise ContractError(f"{label} must be a JSON object: {path}")
    return value


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_digest(path: Path) -> str:
    try:
        return digest_bytes(path.read_bytes())
    except OSError as error:
        raise ContractError(f"Required file could not be read: {path}") from error


def stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def preview_digest(preview: dict[str, Any]) -> str:
    material = dict(preview)
    material.pop("preview_sha256", None)
    return digest_bytes(stable_bytes(material))


def describe_root(describe: dict[str, Any]) -> dict[str, Any]:
    if "metadata" in describe:
        metadata = describe.get("metadata")
        if (
            describe.get("classification") != "read_only_metadata"
            or describe.get("route") != "template_describe"
            or not isinstance(metadata, dict)
            or describe.get("response_sha256") != digest_bytes(stable_bytes(metadata))
        ):
            raise ContractError("Wrapped Describe metadata record is invalid or not the declared template route.")
        describe = metadata
    try:
        root = describe["Resources"]["talentPerformanceTemplates"]
    except (KeyError, TypeError) as error:
        raise ContractError("Describe does not contain Resources.talentPerformanceTemplates.") from error
    if not isinstance(root, dict):
        raise ContractError("Performance Templates Describe root must be an object.")
    return root


def describe_node(root: dict[str, Any], scope: str) -> dict[str, Any]:
    parts = scope.split("/")
    if not parts or parts[0] != "template":
        raise ContractError(f"Unsupported scope: {scope}")
    node = root
    for part in parts[1:]:
        children = node.get("children", {})
        if not isinstance(children, dict) or not isinstance(children.get(part), dict):
            raise ContractError(f"Describe is missing scope: {scope}")
        node = children[part]
    return node


def target_action(node: dict[str, Any], level: str, name: str) -> dict[str, Any]:
    container = node.get(level, {})
    actions = container.get("actions", []) if isinstance(container, dict) else []
    matches = [item for item in actions if isinstance(item, dict) and item.get("name") == name]
    if len(matches) != 1:
        raise ContractError(f"Target Describe does not declare exactly one {level} action {name}.")
    return matches[0]


def required_string(mapping: dict[str, Any], key: str, label: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{label} requires a nonblank {key}.")
    return value.strip()


def render_path(template: str, identifiers: dict[str, Any], required: list[str]) -> str:
    path = template
    for key in required:
        value = required_string(identifiers, key, "Request identifiers")
        path = path.replace("{" + key + "}", quote(value, safe=""))
    if "{" in path or "}" in path:
        raise ContractError("The declared path contains an unresolved identifier.")
    return path


def validate_create_owner_binding(
    resource: dict[str, Any], identifiers: dict[str, Any], payload: dict[str, Any]
) -> None:
    owner = resource.get("create_owner_binding")
    if owner is None:
        return
    required_keys = {
        "type_field", "type_value", "id_field", "identifier", "identifier_component"
    }
    if not isinstance(owner, dict) or set(owner) != required_keys or any(
        not isinstance(owner.get(key), str) or not owner[key]
        for key in required_keys
    ):
        raise ContractError("The task contract has invalid create_owner_binding metadata.")
    identifier = required_string(
        identifiers, owner["identifier"], "Create owner request identifiers"
    )
    component = owner["identifier_component"]
    if component == "before_comma":
        expected_id = identifier.split(",", 1)[0]
    elif component == "after_comma":
        expected_id = identifier.rsplit(",", 1)[-1]
    elif component == "whole":
        expected_id = identifier
    else:
        raise ContractError("The task contract has an unsupported owner identifier component.")
    if payload.get(owner["type_field"]) != owner["type_value"]:
        raise ContractError(
            f"Create payload {owner['type_field']} must be {owner['type_value']} for this scope."
        )
    if payload.get(owner["id_field"]) != expected_id:
        raise ContractError(
            f"Create payload {owner['id_field']} must match the bound parent identity."
        )


def validate_payload(
    node: dict[str, Any], action: dict[str, Any], operation: str, payload: dict[str, Any],
    *, ignored_required: set[str] | None = None,
) -> None:
    ignored_required = ignored_required or set()
    if operation in {"list", "get", "delete"}:
        if payload:
            raise ContractError(f"{operation} does not accept a request payload.")
        return
    if operation == "action":
        parameters = {
            item.get("name"): item
            for item in action.get("parameters", [])
            if isinstance(item, dict) and isinstance(item.get("name"), str)
        }
        unknown = sorted(set(payload) - set(parameters))
        if unknown:
            raise ContractError("Custom action payload contains undeclared fields: " + ", ".join(unknown))
        missing = sorted(
            name for name, item in parameters.items() if item.get("mandatory") and name not in payload
        )
        if missing:
            raise ContractError("Custom action payload is missing required fields: " + ", ".join(missing))
        return

    attributes = {
        item.get("name"): item
        for item in node.get("attributes", [])
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }
    unknown = sorted(set(payload) - set(attributes))
    if unknown:
        raise ContractError("Payload contains fields absent from the target Describe: " + ", ".join(unknown))
    blocked = sorted(
        name
        for name in payload
        if not attributes[name].get("updatable", False)
        or attributes[name].get("allowChanges") == "never"
        or (operation == "update" and attributes[name].get("allowChanges") == "inCreate")
    )
    if blocked:
        raise ContractError("Payload contains fields that are not writable for this operation: " + ", ".join(blocked))
    invalid_types: list[str] = []
    for name, value in payload.items():
        attribute = attributes[name]
        attribute_type = attribute.get("type")
        attribute_format = attribute.get("format")
        valid = True
        if value is None:
            valid = not attribute.get("mandatory", False)
        elif attribute.get("mandatory", False) and isinstance(value, str) and not value.strip():
            valid = False
        elif attribute_type == "boolean":
            valid = isinstance(value, bool)
        elif attribute_type == "date":
            valid = isinstance(value, str)
            if valid:
                try:
                    date.fromisoformat(value)
                except ValueError:
                    valid = False
        elif attribute_type == "string":
            valid = isinstance(value, str)
            max_length = attribute.get("maxLength")
            if valid and max_length not in {None, ""}:
                try:
                    valid = len(value) <= int(max_length)
                except (TypeError, ValueError):
                    valid = False
            if valid and attribute_format == "BigInt":
                valid = value.isdigit()
            elif valid and attribute_format == "BigDecimal":
                try:
                    Decimal(value)
                except InvalidOperation:
                    valid = False
        if not valid:
            invalid_types.append(name)
    if invalid_types:
        raise ContractError(
            "Payload contains values that do not match the target Describe type or required-value contract: "
            + ", ".join(sorted(invalid_types))
        )
    if operation == "update" and not payload:
        raise ContractError("Update requires at least one changed writable field.")
    if operation == "create":
        missing = sorted(
            name
            for name, item in attributes.items()
            if item.get("mandatory")
            and not item.get("hasDefaultValueExpression")
            and item.get("allowChanges") != "never"
            and name not in ignored_required
            and name not in payload
        )
        if missing:
            raise ContractError("Create payload is missing target-required fields: " + ", ".join(missing))


def build_preview(spec: dict[str, Any], describe_path: Path) -> dict[str, Any]:
    contract = read_object(CONTRACT_PATH, "REST execution contract")
    describe = read_object(describe_path, "target Describe")
    root = describe_root(describe)
    environment = required_string(spec, "environment", "Request specification").rstrip("/")
    parsed = urlparse(environment)
    if parsed.scheme != "https" or not parsed.netloc or parsed.path not in {"", "/"}:
        raise ContractError("environment must be an HTTPS Fusion origin without a resource path.")
    scope = required_string(spec, "scope", "Request specification")
    operation = required_string(spec, "operation", "Request specification")
    resources = contract.get("resources", {})
    resource = resources.get(scope) if isinstance(resources, dict) else None
    if not isinstance(resource, dict):
        raise ContractError(f"The task contract does not declare scope: {scope}")
    node = describe_node(root, scope)
    identifiers = spec.get("identifiers", {})
    payload = spec.get("payload", {})
    query = spec.get("query", {})
    if not isinstance(identifiers, dict) or not isinstance(payload, dict) or not isinstance(query, dict):
        raise ContractError("identifiers, payload, and query must be JSON objects.")
    validation_context: dict[str, str] = {}

    operations = contract.get("operations", {})
    custom_actions = contract.get("custom_actions", {})
    action_name = spec.get("action")
    if operation in contract.get("unsupported_operations", {}):
        raise ContractError(str(contract["unsupported_operations"][operation]))
    is_batch_section_upsert = operation == "section_upsert"
    is_atomic_role_delete = operation == "atomic_role_delete"
    if is_atomic_role_delete:
        if scope != "template":
            raise ContractError("Atomic role delete is restricted to the template root scope.")
        batch = contract.get("atomic_role_delete")
        policy = operations.get(operation) if isinstance(operations, dict) else None
        parts = spec.get("parts")
        if not isinstance(batch, dict) or not isinstance(policy, dict):
            raise ContractError("The task contract does not declare atomic role delete metadata.")
        if identifiers or payload or query:
            raise ContractError("Atomic role delete accepts only its two explicitly bound delete parts.")
        if not isinstance(parts, list) or len(parts) != 2 or any(not isinstance(part, dict) for part in parts):
            raise ContractError("Atomic role delete requires exactly two delete parts.")
        required_scopes = batch.get("required_scopes")
        if not isinstance(required_scopes, list) or set(required_scopes) != {
            "template/sections/roleActions", "template/roles"
        }:
            raise ContractError("The atomic role delete scope contract is invalid.")
        if {part.get("scope") for part in parts} != set(required_scopes):
            raise ContractError("Atomic role delete requires one role-action part and one template-role part.")
        if len({part.get("id") for part in parts}) != 2:
            raise ContractError("Atomic role delete part ids must be unique.")
        prefix = required_string(batch, "part_path_prefix", "Atomic role delete contract")
        template_ids: set[str] = set()
        body_parts: list[dict[str, Any]] = []
        for part in parts:
            if set(part) != {"id", "scope", "identifiers", "if_match"}:
                raise ContractError("Atomic role delete parts contain undeclared fields.")
            part_id = required_string(part, "id", "Atomic role delete part")
            part_scope = required_string(part, "scope", "Atomic role delete part")
            part_identifiers = part.get("identifiers")
            if not isinstance(part_identifiers, dict):
                raise ContractError("Atomic role delete part identifiers must be an object.")
            part_resource = resources.get(part_scope)
            if not isinstance(part_resource, dict):
                raise ContractError(f"The task contract does not declare scope: {part_scope}")
            expected_identifiers = set(part_resource["parent_identifiers"]) | {part_resource["item_identifier"]}
            if set(part_identifiers) != expected_identifiers:
                raise ContractError("Atomic role delete part identifiers do not match the declared resource path.")
            template_ids.add(required_string(part_identifiers, "template_id", "Atomic role delete part identifiers"))
            part_node = describe_node(root, part_scope)
            part_action = target_action(part_node, "item", "delete")
            if part_action.get("method") != "DELETE":
                raise ContractError("Target Describe does not permit an atomic delete part.")
            collection_path = render_path(
                part_resource["collection_path"], part_identifiers, part_resource["parent_identifiers"]
            )
            item_path = collection_path + "/" + quote(
                required_string(part_identifiers, part_resource["item_identifier"], "Atomic role delete part identifiers"),
                safe=",",
            )
            item_path = item_path.replace("%2C", ",").replace("%2c", ",")
            if not item_path.startswith(prefix + "/"):
                raise ContractError("Atomic role delete part path is outside the declared resource root.")
            if_match = required_string(part, "if_match", "Atomic role delete part")
            if if_match == "*" or if_match.startswith('"') or if_match.endswith('"'):
                raise ContractError("Atomic role delete requires each fresh raw ETag; wildcard and HTTP quote characters are forbidden.")
            body_parts.append({
                "id": part_id,
                "path": item_path[len(prefix):],
                "operation": "delete",
                "ifMatch": [if_match],
            })
        if len(template_ids) != 1:
            raise ContractError("Atomic role delete parts must belong to the same template.")
        body_parts.sort(key=lambda item: 0 if "/roleActions/" in item["path"] else 1)
        method = policy["method"]
        relative_path = required_string(batch, "path", "Atomic role delete contract")
        body = {"parts": body_parts}
        action = None
    elif is_batch_section_upsert:
        if scope != "template":
            raise ContractError("Batch section upsert is restricted to the template root scope.")
        batch = contract.get("section_upsert")
        if not isinstance(batch, dict):
            raise ContractError("The task contract does not declare batch section upsert metadata.")
        allowed_root = batch.get("allowed_root_fields")
        required_root = batch.get("required_root_fields")
        if not isinstance(allowed_root, list) or not isinstance(required_root, list):
            raise ContractError("The batch section upsert root-field contract is invalid.")
        unknown_root = sorted(set(payload) - set(allowed_root))
        missing_root = sorted(set(required_root) - set(payload))
        if unknown_root:
            raise ContractError("Batch section upsert contains undeclared root fields: " + ", ".join(unknown_root))
        if missing_root:
            raise ContractError("Batch section upsert is missing required root fields: " + ", ".join(missing_root))
        template_defn_id = required_string(payload, "TemplateDefnId", "Batch section upsert payload")
        if template_defn_id != required_string(identifiers, "template_defn_id", "Request identifiers"):
            raise ContractError("Batch section upsert TemplateDefnId does not match the bound target identity.")
        sections = payload.get("sections")
        if not isinstance(sections, list) or len(sections) != 1 or not isinstance(sections[0], dict):
            raise ContractError("Batch section upsert requires exactly one new section object.")
        section = dict(sections[0])
        role_actions = section.pop("roleActions", None)
        if not isinstance(role_actions, list) or not role_actions or any(not isinstance(row, dict) for row in role_actions):
            raise ContractError("Batch section upsert requires one or more nested roleActions.")
        required_section_fields = batch.get("required_section_fields")
        if not isinstance(required_section_fields, list) or not required_section_fields or any(
            not isinstance(field, str) or not field for field in required_section_fields
        ):
            raise ContractError("The batch section upsert required-section-field contract is invalid.")
        missing_section_fields = sorted(set(required_section_fields) - set(section))
        if missing_section_fields:
            raise ContractError(
                "Batch section upsert is missing required materialized section fields: "
                + ", ".join(missing_section_fields)
            )
        for field in required_section_fields:
            required_string(section, field, "Batch section upsert section")
        materialized_section_fields = batch.get("required_materialized_section_fields")
        materialized_role_fields = batch.get("required_materialized_role_action_fields")
        if not isinstance(materialized_section_fields, list) or not materialized_section_fields or any(
            not isinstance(field, str) or not field for field in materialized_section_fields
        ):
            raise ContractError("The batch section upsert materialized-section-field contract is invalid.")
        if not isinstance(materialized_role_fields, list) or not materialized_role_fields or any(
            not isinstance(field, str) or not field for field in materialized_role_fields
        ):
            raise ContractError("The batch section upsert materialized-role-field contract is invalid.")
        missing_materialized = sorted(set(materialized_section_fields) - set(section))
        if missing_materialized:
            raise ContractError(
                "Batch section upsert must materialize provider-derived section defaults: "
                + ", ".join(missing_materialized)
            )
        for index, row in enumerate(role_actions):
            missing_role_defaults = sorted(set(materialized_role_fields) - set(row))
            if missing_role_defaults:
                raise ContractError(
                    f"Batch section upsert roleActions[{index}] must materialize provider-derived defaults: "
                    + ", ".join(missing_role_defaults)
                )
        questionnaire_policy = batch.get("questionnaire_role_action")
        if not isinstance(questionnaire_policy, dict):
            raise ContractError("The questionnaire section role-action contract is invalid.")
        questionnaire_type = required_string(
            questionnaire_policy, "section_type_code", "Questionnaire role-action contract"
        )
        if section.get("SectionTypeCode") == questionnaire_type:
            worker_field = required_string(
                questionnaire_policy, "spec_worker_role_field", "Questionnaire role-action contract"
            )
            worker_tmpl_role_id = required_string(
                spec, worker_field, "Questionnaire section request specification"
            )
            if worker_tmpl_role_id not in [row.get("TmplRoleId") for row in role_actions]:
                raise ContractError(
                    "Questionnaire section upsert requires the selected Worker template-role action. "
                    "Also include each template role that will own a period questionnaire association."
                )
            validation_context[worker_field] = worker_tmpl_role_id
        section_node = describe_node(root, "template/sections")
        section_action = target_action(section_node, "collection", "create")
        validate_payload(section_node, section_action, "create", section, ignored_required={"TemplateDefnId"})
        role_node = describe_node(root, "template/sections/roleActions")
        role_action = target_action(role_node, "collection", "create")
        for row in role_actions:
            validate_payload(role_node, role_action, "create", row, ignored_required={"SectionId"})
        policy = operations.get(operation)
        if not isinstance(policy, dict):
            raise ContractError("The task contract does not declare batch section upsert execution policy.")
        method = policy["method"]
        relative_path = required_string(batch, "path", "Batch section upsert contract")
        body = payload
        action = target_action(node, "collection", "upsert")
        if action.get("method") != method:
            raise ContractError("Target Describe upsert method does not match the section upsert contract.")
    elif operation == "action":
        if scope != "template" or not isinstance(action_name, str):
            raise ContractError("Custom actions require scope template and an exact action name.")
        policy = custom_actions.get(action_name) if isinstance(custom_actions, dict) else None
        if not isinstance(policy, dict):
            raise ContractError(f"The task contract does not enable custom action: {action_name}")
        action = target_action(node, "collection", action_name)
        method = policy["method"]
        relative_path = resource["collection_path"] + "/action/" + action_name
        if action_name == "findByAdvancedSearchQuery":
            validation = contract.get("custom_action_validation", {}).get(action_name, {})
            allowed_fields = validation.get("allowed_sort_fields", [])
            allowed_directions = validation.get("allowed_sort_directions", [])
            sort_rows = payload.get("sort", [])
            if not isinstance(sort_rows, list) or any(not isinstance(row, dict) for row in sort_rows):
                raise ContractError("Advanced-search sort must be an array of objects.")
            invalid_sort = [
                row for row in sort_rows
                if row.get("name") not in allowed_fields
                or row.get("direction") not in allowed_directions
                or set(row) != {"name", "direction"}
            ]
            if invalid_sort:
                raise ContractError(
                    "Advanced-search sort supports only Name, DateFrom, or DateTo with asc or desc direction."
                )
    else:
        policy = operations.get(operation) if isinstance(operations, dict) else None
        if not isinstance(policy, dict):
            raise ContractError(f"The task contract does not declare operation: {operation}")
        level = policy["level"]
        action = target_action(node, level, {"list": "get", "get": "get", "create": "create", "update": "update", "delete": "delete"}[operation])
        method = policy["method"]
        if operation in {"create", "update", "delete"} and scope != "template":
            for key in resource["parent_identifiers"]:
                value = required_string(identifiers, key, "Mutation request identifiers")
                if value.count(",") != 1 or any(not component for component in value.split(",")):
                    raise ContractError(
                        f"Nested mutation identifier {key} must be the fresh canonical two-component key."
                    )
            if level == "item":
                item_key = resource["item_identifier"]
                item_value = required_string(identifiers, item_key, "Mutation request identifiers")
                item_shape = resource.get("item_identifier_shape", "composite")
                if item_shape == "scalar":
                    if "," in item_value:
                        raise ContractError(
                            f"Nested mutation identifier {item_key} must be the fresh canonical scalar key."
                        )
                elif item_shape == "composite":
                    if item_value.count(",") != 1 or any(
                        not component for component in item_value.split(",")
                    ):
                        raise ContractError(
                            f"Nested mutation identifier {item_key} must be the fresh canonical two-component key."
                        )
                else:
                    raise ContractError(
                        f"Resource item_identifier_shape is unsupported: {item_shape}"
                    )
        relative_path = render_path(resource["collection_path"], identifiers, resource["parent_identifiers"])
        if level == "item":
            item_key = resource["item_identifier"]
            relative_path += "/" + quote(required_string(identifiers, item_key, "Request identifiers"), safe="")
    if (
        not is_batch_section_upsert
        and not is_atomic_role_delete
        and method != action.get("method")
    ) or method not in contract.get("allowed_methods", []):
        raise ContractError("Contract method and target Describe method do not match an allowed method.")
    payload_to_validate = dict(payload)
    if operation == "create":
        nested_children = resource.get("nested_create_children", [])
        if not isinstance(nested_children, list) or any(not isinstance(name, str) for name in nested_children):
            raise ContractError("The task contract has invalid nested_create_children metadata.")
        required_nested = resource.get("required_nested_create_children", [])
        if not isinstance(required_nested, list) or any(not isinstance(name, str) for name in required_nested):
            raise ContractError("The task contract has invalid required_nested_create_children metadata.")
        required_nested_fields = resource.get("required_nested_child_fields", {})
        if not isinstance(required_nested_fields, dict) or any(
            not isinstance(child_name, str)
            or not isinstance(fields, list)
            or not fields
            or any(not isinstance(field, str) or not field for field in fields)
            for child_name, fields in required_nested_fields.items()
        ):
            raise ContractError("The task contract has invalid required_nested_child_fields metadata.")
        undeclared_required_children = sorted(set(required_nested_fields) - set(nested_children))
        if undeclared_required_children:
            raise ContractError(
                "The task contract requires fields for undeclared nested children: "
                + ", ".join(undeclared_required_children)
            )
        missing_nested = sorted(name for name in required_nested if name not in payload_to_validate)
        if missing_nested:
            raise ContractError("Create payload is missing required nested children: " + ", ".join(missing_nested))
        for child_name in nested_children:
            if child_name not in payload_to_validate:
                continue
            rows = payload_to_validate.pop(child_name)
            if not isinstance(rows, list) or not rows or any(not isinstance(row, dict) for row in rows):
                raise ContractError(f"Nested create child {child_name} must be a nonempty array of objects.")
            required_fields = required_nested_fields.get(child_name, [])
            for index, row in enumerate(rows):
                missing_fields = sorted(set(required_fields) - set(row))
                if missing_fields:
                    raise ContractError(
                        f"Nested create child {child_name}[{index}] is missing required materialized fields: "
                        + ", ".join(missing_fields)
                    )
            child_scope = scope + "/" + child_name
            child_resource = resources.get(child_scope)
            if not isinstance(child_resource, dict):
                raise ContractError(f"The task contract does not declare nested child scope: {child_scope}")
            child_node = describe_node(root, child_scope)
            child_action = target_action(child_node, "collection", "create")
            if child_action.get("method") != "POST":
                raise ContractError(f"Target Describe does not permit nested create for {child_scope}.")
            ignored_required = child_resource.get("parent_managed_attributes", [])
            if not isinstance(ignored_required, list) or any(not isinstance(name, str) for name in ignored_required):
                raise ContractError("The task contract has invalid parent_managed_attributes metadata.")
            for row in rows:
                validate_payload(
                    child_node, child_action, "create", row,
                    ignored_required=set(ignored_required),
                )
    current_parent_managed = resource.get("parent_managed_attributes", []) if operation == "create" else []
    if not isinstance(current_parent_managed, list) or any(
        not isinstance(name, str) for name in current_parent_managed
    ):
        raise ContractError("The task contract has invalid parent_managed_attributes metadata.")
    if not is_batch_section_upsert and not is_atomic_role_delete:
        if operation == "create":
            validate_create_owner_binding(resource, identifiers, payload_to_validate)
        validate_payload(
            node,
            action,
            operation,
            payload_to_validate,
            ignored_required=set(current_parent_managed),
        )
    if any(not isinstance(key, str) or not isinstance(value, str) for key, value in query.items()):
        raise ContractError("query keys and values must be strings.")
    audit_attempt_id = spec.get("audit_attempt_id")
    if audit_attempt_id is not None and (
        not isinstance(audit_attempt_id, str)
        or not audit_attempt_id.strip()
        or len(audit_attempt_id) > 120
    ):
        raise ContractError("audit_attempt_id must be a nonblank string of at most 120 characters.")

    has_nested_alerts = scope == "template" and operation == "create" and "alerts" in payload
    is_alert_mutation = bool(policy["mutation"]) and (
        scope == "template/alerts" or has_nested_alerts
    )
    if is_alert_mutation:
        template_type_code = (
            payload.get("TemplateTypeCode")
            if has_nested_alerts
            else spec.get("parent_template_type_code")
        )
        if not isinstance(template_type_code, str) or not template_type_code.strip():
            raise ContractError(
                "Alert mutations require the fresh parent template type code before preview."
            )
        template_type_code = template_type_code.strip()
        if template_type_code == "ORA_ANYTIME" and operation != "delete":
            raise ContractError("Template alerts are not supported for ORA_ANYTIME templates.")
        validation_context["parent_template_type_code"] = template_type_code

    if not is_batch_section_upsert and not is_atomic_role_delete:
        body = (
            json.loads(stable_bytes(payload).decode("utf-8"))
            if payload or operation == "action"
            else None
        )
    wire_body = json.dumps(body).encode("utf-8") if body is not None else b""
    headers = dict(contract["required_headers"])
    if is_batch_section_upsert:
        batch_headers = contract["section_upsert"].get("headers")
        if not isinstance(batch_headers, dict) or any(
            not isinstance(name, str) or not isinstance(value, str)
            for name, value in batch_headers.items()
        ):
            raise ContractError("The batch section upsert header contract is invalid.")
        headers.update(batch_headers)
    if method == "GET":
        headers["Content-Type"] = "application/vnd.oracle.adf.resourceitem+json"
    elif body is not None:
        headers["Content-Type"] = (
            required_string(contract["section_upsert"], "content_type", "Batch section upsert contract")
            if is_batch_section_upsert
            else (
                required_string(contract["atomic_role_delete"], "content_type", "Atomic role delete contract")
                if is_atomic_role_delete
                else ("application/vnd.oracle.adf.action+json" if operation == "action" else "application/vnd.oracle.adf.resourceitem+json")
            )
        )
    if operation in {"update", "delete"}:
        if_match = required_string(spec, "if_match", "Item mutation request specification")
        if if_match == "*" or len(if_match) < 2 or not (
            if_match.startswith('"') and if_match.endswith('"')
        ):
            raise ContractError(
                "Item mutation if_match must preserve the fresh HTTP ETag exactly, "
                "including its enclosing double quotes; wildcard and unquoted values are forbidden."
            )
        headers["If-Match"] = if_match
    binding = {
        "environment": environment,
        "method": method,
        "relative_path": relative_path,
        "query": dict(sorted(query.items())),
        "headers": dict(sorted(headers.items())),
        "body_sha256": digest_bytes(wire_body) if body is not None else None,
        "describe_sha256": file_digest(describe_path),
        "contract_sha256": file_digest(CONTRACT_PATH),
    }
    if validation_context:
        binding["validation_context"] = dict(sorted(validation_context.items()))
    preview = {
        "schema_version": "1.0",
        "task_code": contract["task_code"],
        "route": contract["route"],
        "scope": scope,
        "operation": operation,
        "action": action_name if operation == "action" else None,
        "mutation": bool(policy["mutation"]),
        "binding": binding,
        "body": body,
        "request_binding_sha256": digest_bytes(stable_bytes(binding)),
        "approval_status": "required" if policy["mutation"] else "not_required",
        "audit_attempt_id": audit_attempt_id,
    }
    preview["preview_sha256"] = preview_digest(preview)
    return preview


def validate_preview(preview: dict[str, Any]) -> None:
    expected = preview.get("preview_sha256")
    if not isinstance(expected, str) or expected != preview_digest(preview):
        raise ContractError("Preview SHA-256 is missing or does not match the preview bytes.")
    binding = preview.get("binding")
    if not isinstance(binding, dict) or preview.get("request_binding_sha256") != digest_bytes(stable_bytes(binding)):
        raise ContractError("Preview request binding is missing or has changed.")
    if binding.get("contract_sha256") != file_digest(CONTRACT_PATH):
        raise ContractError("The REST execution contract changed after preview.")
    body = preview.get("body")
    wire_body = json.dumps(body).encode("utf-8") if body is not None else b""
    actual_body = digest_bytes(wire_body) if body is not None else None
    if binding.get("body_sha256") != actual_body:
        raise ContractError("The preview body no longer matches its bound digest.")


def validate_approval(preview: dict[str, Any], approval: dict[str, Any]) -> None:
    if approval.get("approved") is not True:
        raise ContractError("Mutation approval must contain approved: true.")
    binding = preview["binding"]
    required = {
        "preview_sha256": preview["preview_sha256"],
        "environment": binding["environment"],
        "method": binding["method"],
        "relative_path": binding["relative_path"],
    }
    changed = [key for key, value in required.items() if approval.get(key) != value]
    if changed:
        raise ContractError("Approval does not match preview fields: " + ", ".join(changed))
    if not isinstance(approval.get("approved_at"), str) or not approval["approved_at"].strip():
        raise ContractError("Mutation approval must record approved_at.")


def execute(
    preview: dict[str, Any], properties_path: Path, token_cache: Path, approval: dict[str, Any] | None
) -> dict[str, Any]:
    validate_preview(preview)
    if preview.get("mutation"):
        if approval is None:
            raise ContractError("Mutation execution requires the later exact preview approval artifact.")
        validate_approval(preview, approval)
    props = read_properties(properties_path)
    require_props(props, ["environment", "restBaseUrl", "scope"])
    binding = preview["binding"]
    configured_origin = props["restBaseUrl"].rstrip("/")
    if configured_origin != binding["environment"]:
        raise ContractError("Configured restBaseUrl does not match the approval-bound environment.")
    token = get_access_token(props, token_cache=str(token_cache), open_browser=False)
    url = build_url(props, binding["relative_path"], binding["query"])
    try:
        content, response_headers, status = request_bytes(
            props,
            url,
            method=binding["method"],
            access_token=token,
            headers=binding["headers"],
            json_body=preview.get("body"),
            timeout=60,
        )
    except FusionHttpError as error:
        try:
            error_body: Any = json.loads(error.body)
        except json.JSONDecodeError:
            error_body = error.body
        return {
            "preview_sha256": preview["preview_sha256"],
            "request_binding_sha256": preview["request_binding_sha256"],
            "request_succeeded": False,
            "http_status": error.status_code,
            "response_headers": {},
            "response": error_body,
            "write_retried": False,
            "verification_required": bool(preview.get("mutation")),
        }
    try:
        response_body: Any = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        response_body = content.decode("utf-8", errors="replace")
    retained_headers = {
        key: value
        for key, value in response_headers.items()
        if key.casefold() in {"content-type", "etag", "x-oracle-dms-ecid", "x-request-id"}
    }
    return {
        "preview_sha256": preview["preview_sha256"],
        "request_binding_sha256": preview["request_binding_sha256"],
        "request_succeeded": True,
        "http_status": status,
        "response_headers": retained_headers,
        "response": response_body,
        "write_retried": False,
        "verification_required": bool(preview.get("mutation")),
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    preview = commands.add_parser("preview", allow_abbrev=False)
    preview.add_argument("--spec", required=True, type=Path)
    preview.add_argument("--describe", required=True, type=Path)
    preview.add_argument("--output", required=True, type=Path)
    run = commands.add_parser("execute", allow_abbrev=False)
    run.add_argument("--preview", required=True, type=Path)
    run.add_argument("--approval", type=Path)
    run.add_argument("--properties", required=True, type=Path)
    run.add_argument("--token-cache", required=True, type=Path)
    run.add_argument("--output", required=True, type=Path)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "preview":
            result = build_preview(read_object(args.spec, "request specification"), args.describe)
        else:
            preview = read_object(args.preview, "request preview")
            approval = read_object(args.approval, "approval") if args.approval else None
            result = execute(preview, args.properties, args.token_cache, approval)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        request_succeeded = result.get("request_succeeded", True)
        print(json.dumps({"status": "ok" if request_succeeded else "http_error", "output": str(args.output), "preview_sha256": result.get("preview_sha256")}))
        return 0 if request_succeeded else 2
    except (ContractError, OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
