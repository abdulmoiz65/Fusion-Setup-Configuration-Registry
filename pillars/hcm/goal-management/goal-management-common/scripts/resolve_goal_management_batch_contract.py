#!/usr/bin/env python3
"""Resolve maintained Goal Management ADF batch capability without side effects.

The resolver is deliberately dormant unless the route selector returns the
explicit ``adf_batch`` transport intent.  Standard REST, HDL, FSM, and intake
routes are returned unchanged and never receive batch contracts.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlsplit, unquote

from goal_management_route_selector import select_route


DEFAULT_REGISTRY = (
    Path(__file__).resolve().parents[1]
    / "ora-resource"
    / "ora_rest_batch_capabilities.json"
)
_ROOT_PATH = re.compile(r"/hcmRestApi/resources/(?:latest|\d+(?:\.\d+)*)/?")
_PARENT_RESOURCES = {"reviewPeriods", "libraryGoals", "goalPlans"}


class BatchContractResolutionError(ValueError):
    """Raised when an explicitly selected REST batch has no safe contract."""


def _batch_root(value: str) -> str:
    parsed = urlsplit(value)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or not _ROOT_PATH.fullmatch(parsed.path)
    ):
        raise BatchContractResolutionError(
            "A verified same-host HCM resources root is required for REST batch"
        )
    return value.rstrip("/")


def _operation_shape(path: Any, operation: Any) -> tuple[str, str]:
    if not isinstance(path, str) or not path.startswith("/") or path.startswith("//"):
        raise BatchContractResolutionError("A safe relative operation path is required")
    decoded = unquote(path)
    if decoded != path or any(value in decoded for value in ("\\", "?", "#", "{", "}")):
        raise BatchContractResolutionError("Encoded, templated, or qualified paths are not supported")
    segments = decoded.strip("/").split("/")
    if not segments or segments[0] not in _PARENT_RESOURCES:
        raise BatchContractResolutionError("No maintained parent-resource batch capability")
    if operation == "create" and len(segments) == 1:
        return segments[0], "collection"
    if operation in {"update", "delete"} and len(segments) == 2 and segments[1] not in {".", "..", ""}:
        return segments[0], "item"
    raise BatchContractResolutionError("No maintained capability for this path and operation shape")


def _load_registry() -> tuple[dict[str, Any], str]:
    raw = DEFAULT_REGISTRY.read_bytes()
    registry = json.loads(raw)
    if (
        registry.get("schema_version") != "1.0"
        or registry.get("transport_intent") != "adf_batch"
        or not isinstance(registry.get("capabilities"), list)
        or not registry.get("registry_id")
        or not registry.get("transaction_context")
        or not registry.get("evidence")
    ):
        raise BatchContractResolutionError("Goal Management batch capability registry is invalid")
    return registry, hashlib.sha256(raw).hexdigest()


def _resource(metadata: Any, resource_name: str) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise BatchContractResolutionError(f"Current {resource_name} metadata is required")
    resources = metadata.get("Resources")
    if isinstance(resources, dict):
        metadata = resources.get(resource_name)
    if not isinstance(metadata, dict):
        raise BatchContractResolutionError(f"Current metadata does not describe {resource_name}")
    return metadata


def _advertises(resource: dict[str, Any], *, path_kind: str, action: str, method: str) -> bool:
    owner = resource.get("collection") if path_kind == "collection" else resource.get("item")
    actions = owner.get("actions", []) if isinstance(owner, dict) else []
    return any(
        isinstance(candidate, dict)
        and candidate.get("name") == action
        and str(candidate.get("method", "")).upper() == method
        for candidate in actions
    )


def resolve_batch_contracts(
    *,
    intent: str,
    batch_root: str,
    operations: list[dict[str, Any]],
    runtime_metadata: dict[str, Any],
) -> dict[str, Any]:
    """Resolve parent CRUD contracts for one explicitly selected batch stage."""
    route = select_route([], intent)
    if route.get("transportIntent") != "adf_batch":
        return {
            "selected": False,
            "route": route,
            "operations": deepcopy(operations),
            "combination_contract": None,
        }
    if not isinstance(operations, list) or not operations:
        raise BatchContractResolutionError("An explicit REST batch requires operations")
    if not isinstance(runtime_metadata, dict):
        raise BatchContractResolutionError("Current runtime metadata is required")

    root = _batch_root(batch_root)
    registry, registry_sha256 = _load_registry()
    resolved: list[dict[str, Any]] = []
    capabilities = registry["capabilities"]
    context = registry["transaction_context"]

    for source in deepcopy(operations):
        if not isinstance(source, dict):
            raise BatchContractResolutionError("Every operation must be an object")
        resource_name, path_kind = _operation_shape(source.get("path"), source.get("operation"))
        matches = [
            capability
            for capability in capabilities
            if capability.get("resource") == resource_name
            and capability.get("operation") == source.get("operation")
            and capability.get("path_kind") == path_kind
            and capability.get("pattern") == "independent_setup"
        ]
        if len(matches) != 1:
            raise BatchContractResolutionError(
                f"Expected one maintained batch capability for {resource_name} {source.get('operation')}"
            )
        capability = matches[0]
        current = _resource(runtime_metadata.get(resource_name), resource_name)
        if not _advertises(
            current,
            path_kind=path_kind,
            action=capability["runtime_action"],
            method=capability["runtime_method"],
        ):
            raise BatchContractResolutionError(
                f"Current {resource_name} metadata does not advertise "
                f"{capability['runtime_action']} {capability['runtime_method']}"
            )
        source["contract"] = {
            **deepcopy(source.get("contract", {})),
            "batch_root": root,
            "batch_enabled": True,
            "transaction_context": context,
            "evidence": {
                "resolver": "goal-management-maintained-capability-plus-current-describe",
                "registry_id": registry["registry_id"],
                "registry_sha256": registry_sha256,
                "capability_id": capability["capability_id"],
                "runtime_action": capability["runtime_action"],
                "runtime_method": capability["runtime_method"],
            },
            "path": source["path"],
            "operation": source["operation"],
        }
        resolved.append(source)

    parts = [{key: operation.get(key) for key in ("id", "path", "operation")} for operation in resolved]
    combination_contract = {
        "batch_root": root,
        "pattern": "independent_setup",
        "transaction_context": context,
        "evidence": {
            "resolver": "goal-management-maintained-combination",
            "registry_id": registry["registry_id"],
            "registry_sha256": registry_sha256,
            "capability_ids": [operation["contract"]["evidence"]["capability_id"] for operation in resolved],
        },
        "parts": parts,
    }
    return {
        "selected": True,
        "route": route,
        "batch_root": root,
        "operations": resolved,
        "combination_contract": combination_contract,
    }
