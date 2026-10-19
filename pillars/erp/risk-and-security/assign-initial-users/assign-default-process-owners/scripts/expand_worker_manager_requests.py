#!/usr/bin/env python3
"""Expand verified workforce candidates into the next deterministic Core read batch.

This helper has no Fusion, OAuth, HTTP, approval, or owner-selection logic.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable


ASSIGNMENTS = "/api/boss/data/objects/ora/hcmHrCore/employment/v1/workerAssignmentExtracts"
HIERARCHY = "/api/boss/data/objects/ora/hcmHrCore/employment/v1/managerHierarchy"
USERS = "/api/boss/data/objects/ora/hcmHrCore/userRoleProvisioning/v1/users"
PAGE_SIZE = 500
DEFAULT_MANAGER_LEVELS = (1, 2, 3)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def collection_items(payload: Any, request_id: str) -> list[dict[str, Any]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise ValueError(f"Core response {request_id!r} must contain an items array")
    if not all(isinstance(row, dict) for row in payload["items"]):
        raise ValueError(f"Core response {request_id!r} contains a non-object item")
    return payload["items"]


def paged_items(payload: Any, request_id: str, page_size: int = PAGE_SIZE) -> tuple[list[dict[str, Any]], bool]:
    items = collection_items(payload, request_id)
    has_more = payload.get("hasMore") if isinstance(payload, dict) else None
    if has_more is None and items and len(items) < page_size:
        # Some terminal collection responses omit continuation metadata. A short,
        # non-empty final page is the narrow compatibility evidence accepted here.
        return items, False
    if not isinstance(has_more, bool):
        raise ValueError(f"Core response {request_id!r} does not establish page completion")
    if has_more and not items:
        raise ValueError(f"Core response {request_id!r} hasMore=true with an empty items array")
    return items, has_more


def request(request_id: str, service: str, endpoint: str, query: dict[str, str]) -> dict[str, Any]:
    return {"id": request_id, "service": service, "method": "GET", "endpoint": endpoint, "query": query}


def page_id(kind: str, entity_id: str, offset: int) -> str:
    return f"{kind}:{entity_id}:offset:{offset}"


def boss_string_literal(value: Any) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def confirmed_business_unit_ids(document: dict[str, Any]) -> list[str]:
    mappings = document.get("mappings")
    if not isinstance(mappings, list) or not mappings:
        raise ValueError("Confirmed mappings require a non-empty mappings array")
    business_unit_ids: set[str] = set()
    for index, mapping in enumerate(mappings):
        business_unit_id = mapping.get("business_unit_id") if isinstance(mapping, dict) else None
        if isinstance(business_unit_id, bool) or not isinstance(business_unit_id, (str, int)) or not str(business_unit_id).strip():
            raise ValueError(f"mappings[{index}] requires business_unit_id")
        business_unit_ids.add(str(business_unit_id).strip())
    return sorted(business_unit_ids)


def candidate_worker_ids(values: list[str]) -> list[str]:
    """Normalize worker identities returned by the functional candidate lookup.

    These are internal identifiers from an already-completed Core HCM result,
    not consultant-supplied values.  Keeping this route separate from Business
    Unit mappings lets functional discovery continue when no mapping exists.
    """
    if not values:
        raise ValueError("At least one candidate worker identifier is required")
    return sorted({numeric_identifier(value, "candidate_worker_id") for value in values})


def load_core_results(args: argparse.Namespace) -> tuple[str, dict[str, Any]]:
    responses: dict[str, Any] = {}
    environment: str | None = args.environment
    if args.core_results:
        bundle = read_json(Path(args.core_results))
        bundled_responses = bundle.get("responses")
        bundle_environment = bundle.get("environment")
        if not isinstance(bundled_responses, dict) or not isinstance(bundle_environment, str) or not bundle_environment:
            raise ValueError("Core-result bundle requires environment and responses")
        if environment and environment != bundle_environment:
            raise ValueError("--environment does not match the Core-result bundle")
        environment, responses = bundle_environment, dict(bundled_responses)
    for specification in args.core_response:
        request_id, separator, response_path = specification.partition("=")
        if not separator or not request_id or not response_path:
            raise ValueError("--core-response must be request_id=Core-output.json")
        if request_id in responses:
            raise ValueError(f"Duplicate Core response id: {request_id}")
        responses[request_id] = read_json(Path(response_path))
    if not environment:
        raise ValueError("--environment is required when Core responses are supplied individually")
    return environment, responses


def collect_pages(kind: str, entity_id: str, responses: dict[str, Any], needed: dict[str, dict[str, Any]], build_request: Callable[[str, int], dict[str, Any]]) -> list[dict[str, Any]] | None:
    offset = 0
    all_items: list[dict[str, Any]] = []
    while True:
        request_id = page_id(kind, entity_id, offset)
        if request_id not in responses:
            needed[request_id] = build_request(request_id, offset)
            return None
        items, has_more = paged_items(responses[request_id], request_id)
        all_items.extend(items)
        if not has_more:
            return all_items
        offset += len(items)


def assignment_request(business_unit_id: str, request_id: str, offset: int) -> dict[str, Any]:
    return request(request_id, "boss", ASSIGNMENTS, {"$fields": "personDetail.id,businessUnit.id,businessUnit.name", "$filter": f"businessUnit.id={business_unit_id}", "$limit": str(PAGE_SIZE), "$offset": str(offset)})


def numeric_identifier(value: Any, field: str) -> str:
    identifier = str(value).strip()
    if not identifier.isascii() or not identifier.isdecimal():
        raise ValueError(f"{field} must be a numeric BOSS identifier")
    return identifier


def hierarchy_entity_id(worker_id: str, manager_level: int | None) -> str:
    return worker_id if manager_level is None else f"{worker_id}:level:{manager_level}"


def hierarchy_request(worker_id: str, manager_level: int | None, request_id: str, offset: int) -> dict[str, Any]:
    worker_id = numeric_identifier(worker_id, "worker_id")
    filter_value = f"personId={worker_id}"
    if manager_level is not None:
        if isinstance(manager_level, bool) or not isinstance(manager_level, int) or manager_level <= 0:
            raise ValueError("manager_level must be a positive integer")
        filter_value += f" and managerLevel={manager_level}"
    return request(request_id, "boss", HIERARCHY, {"$fields": "personId,managerId,managerLevel", "$filter": filter_value, "$limit": str(PAGE_SIZE), "$offset": str(offset)})


def hierarchy_manager_levels(document: dict[str, Any]) -> list[int] | None:
    """Return the requested manager levels, or None when TOP needs full rows."""
    hierarchy = document.get("hierarchy")
    if hierarchy is None:
        return [1, 2, 3]
    if not isinstance(hierarchy, dict):
        raise ValueError("hierarchy must be an object when supplied")
    selection = hierarchy.get("selection", "LOWEST_RESOLVABLE")
    levels_to_inspect = hierarchy.get("levels_to_inspect", 3)
    if isinstance(levels_to_inspect, bool) or not isinstance(levels_to_inspect, int) or levels_to_inspect <= 0:
        raise ValueError("hierarchy.levels_to_inspect must be a positive integer")
    if selection == "LOWEST_RESOLVABLE":
        return list(range(1, levels_to_inspect + 1))
    if selection == "FROM_LEVEL":
        starting_level = hierarchy.get("starting_manager_level")
        if isinstance(starting_level, bool) or not isinstance(starting_level, int) or starting_level <= 0:
            raise ValueError("hierarchy.starting_manager_level must be a positive integer for FROM_LEVEL")
        return list(range(starting_level, starting_level + levels_to_inspect))
    if selection == "TOP":
        return None
    raise ValueError("hierarchy.selection must be LOWEST_RESOLVABLE, FROM_LEVEL, or TOP")


def supplied_owner_usernames(values: list[str]) -> list[str]:
    usernames = {value.strip() for value in values if isinstance(value, str) and value.strip()}
    if len(usernames) != len(values):
        raise ValueError("Every proposed owner username must be a non-empty string")
    return sorted(usernames)


def supplied_owner_request(username: str) -> dict[str, Any]:
    request_id = f"supplied-owner:{username}"
    return request(request_id, "boss", USERS, {"$fields": "name,guid,personId", "$filter": f"name={boss_string_literal(username)}", "$limit": "2", "$offset": "0"})


def supplied_owner_next_requests(usernames: list[str], responses: dict[str, Any]) -> list[dict[str, Any]]:
    """Resolve consultant-supplied exact usernames before hierarchy analysis."""
    needed: dict[str, dict[str, Any]] = {}
    for username in usernames:
        request_id = f"supplied-owner:{username}"
        if request_id not in responses:
            needed[request_id] = supplied_owner_request(username)
            continue
        rows, has_more = paged_items(responses[request_id], request_id, page_size=2)
        if has_more or len(rows) != 1:
            raise ValueError(f"Proposed owner username {username!r} did not resolve uniquely")
        owner = rows[0]
        if owner.get("name") != username or not isinstance(owner.get("guid"), str) or not owner["guid"].strip():
            raise ValueError(f"Proposed owner username {username!r} did not return a usable BOSS identity")
    return [needed[request_id] for request_id in sorted(needed)]


def next_requests(business_unit_ids: list[str], responses: dict[str, Any], proposed_owner_usernames: list[str] | None = None, manager_levels: tuple[int, ...] | list[int] | None = DEFAULT_MANAGER_LEVELS, functional_candidate_worker_ids: list[str] | None = None) -> list[dict[str, Any]]:
    if proposed_owner_usernames:
        return supplied_owner_next_requests(supplied_owner_usernames(proposed_owner_usernames), responses)
    needed: dict[str, dict[str, Any]] = {}
    if functional_candidate_worker_ids:
        worker_ids = set(candidate_worker_ids(functional_candidate_worker_ids))
    else:
        assignment_rows: list[dict[str, Any]] = []
        assignments_complete = True
        for business_unit_id in business_unit_ids:
            rows = collect_pages("assignments", business_unit_id, responses, needed, lambda request_id, offset, bu=business_unit_id: assignment_request(bu, request_id, offset))
            if rows is None:
                assignments_complete = False
            else:
                assignment_rows.extend(rows)
        if not assignments_complete:
            return [needed[request_id] for request_id in sorted(needed)]
        worker_ids = {numeric_identifier(row["personDetail"]["id"], "personDetail.id") for row in assignment_rows if isinstance(row.get("personDetail"), dict) and row["personDetail"].get("id") is not None}
    requested_levels = manager_levels
    if requested_levels is not None:
        if not requested_levels:
            raise ValueError("manager_levels must not be empty")
        if any(isinstance(level, bool) or not isinstance(level, int) or level <= 0 for level in requested_levels):
            raise ValueError("manager_levels must contain positive integers")
        requested_levels = sorted(set(requested_levels))
    hierarchy_targets = [(worker_id, manager_level) for worker_id in sorted(worker_ids) for manager_level in (requested_levels if requested_levels is not None else [None])]
    hierarchy_request_ids = [request_id for request_id in responses if request_id.startswith("hierarchy:")]
    if hierarchy_targets and not hierarchy_request_ids:
        # Confirm that reporting information is available for one worker before
        # scheduling a potentially large hierarchy batch. If Core cannot perform
        # this read, no result is returned and the workflow stops without fan-out.
        worker_id, manager_level = hierarchy_targets[0]
        request_id = page_id("hierarchy", hierarchy_entity_id(worker_id, manager_level), 0)
        return [hierarchy_request(worker_id, manager_level, request_id, 0)]

    hierarchy_rows: list[dict[str, Any]] = []
    hierarchies_complete = True
    for worker_id, manager_level in hierarchy_targets:
        entity_id = hierarchy_entity_id(worker_id, manager_level)
        rows = collect_pages("hierarchy", entity_id, responses, needed, lambda request_id, offset, worker=worker_id, level=manager_level: hierarchy_request(worker, level, request_id, offset))
        if rows is None:
            hierarchies_complete = False
        else:
            hierarchy_rows.extend(rows)
    if not hierarchies_complete:
        return [needed[request_id] for request_id in sorted(needed)]

    # Functional candidates themselves need a verified user identity even when
    # their reporting hierarchy is empty. The optional Business Unit route
    # preserves its existing behavior: it resolves only returned managers.
    identity_ids = {numeric_identifier(row["managerId"], "managerId") for row in hierarchy_rows if row.get("managerId") is not None}
    if functional_candidate_worker_ids:
        identity_ids |= worker_ids
    for identity_id in sorted(identity_ids):
        request_id = f"user:{identity_id}"
        if request_id not in responses:
            needed[request_id] = request(request_id, "boss", USERS, {"$fields": "name,guid,personId", "$filter": f"personId={identity_id}", "$limit": "10"})

    return [needed[request_id] for request_id in sorted(needed)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--confirmed-mappings", help="Internally retained Business Unit/process mapping JSON for the optional Business Unit evidence route.")
    parser.add_argument("--candidate-worker-id", action="append", default=[], help="Verified numeric worker identifier retained by the Core department-bounded worker assessment. Repeat for each candidate.")
    parser.add_argument("--core-results", help="Customer-controlled Core-result bundle JSON.")
    parser.add_argument("--core-response", action="append", default=[], help="Repeat as request_id=Core-output.json.")
    parser.add_argument("--environment", help="Required with --core-response; must match a bundle environment when both are supplied.")
    parser.add_argument("--proposed-owner-username", action="append", default=[], help="Exact consultant-supplied username to resolve before hierarchy analysis.")
    parser.add_argument("--request-plan-output", required=True, help="Output path for the next Core request manifest.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    environment, responses = load_core_results(args)
    if args.proposed_owner_username:
        if args.confirmed_mappings or args.candidate_worker_id:
            raise ValueError("Direct owner validation cannot be combined with candidate discovery input")
        requests = next_requests([], responses, args.proposed_owner_username)
    else:
        if bool(args.confirmed_mappings) == bool(args.candidate_worker_id):
            raise ValueError("Provide exactly one of --confirmed-mappings or --candidate-worker-id for candidate discovery")
        mappings = read_json(Path(args.confirmed_mappings)) if args.confirmed_mappings else {}
        requests = next_requests(
            confirmed_business_unit_ids(mappings) if args.confirmed_mappings else [],
            responses,
            manager_levels=hierarchy_manager_levels(mappings),
            functional_candidate_worker_ids=args.candidate_worker_id or None,
        )
    write_json(Path(args.request_plan_output), {"environment": environment, "requests": requests})
    if requests:
        print("I’m checking the current setup. I’ll return with a complete review or a clear next action.")
    else:
        print("Owner analysis is complete. Review the consultant decision table before approving any owner assignment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
