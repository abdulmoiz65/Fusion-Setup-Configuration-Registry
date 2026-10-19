"""Runtime-only resolvers for governed Goal Plan template-goal operations.

No resolver result from this module may be written to a project artifact.  The
values are volatile request context used only to construct a freshly approved
request.  A public child-create contract is preferred over an ADF batch
fallback whenever current Goal Plans metadata advertises it.
"""

from __future__ import annotations

import re
from typing import Any, Iterable, Mapping
from urllib.parse import urlparse


class RuntimeContractGap(RuntimeError):
    """Raised when the skill, not the consultant, lacks an executable route."""


TEMPLATE_GOAL_PLAN_FIELDS = (
    "GoalPlanId,GoalPlanName,ReviewPeriodId,PrimaryGoalPlanFlag,"
    "StartDate,EndDate,MassRequestId"
)


def resolve_goal_plan_mass_request_id(
    plan: Mapping[str, Any], *, expected_goal_plan_id: int | str
) -> int:
    """Validate an exact, explicitly projected plan read for template-goal work.

    A compact GET that omits ``MassRequestId`` is incomplete evidence, not a
    returned null. This is runtime request context, not a Goal Plan create input.
    """
    if str(plan.get("GoalPlanId")) != str(expected_goal_plan_id):
        raise RuntimeContractGap(
            "GOAL_PLAN_IDENTITY_MISMATCH: projected item does not match the selected GoalPlanId"
        )
    if plan.get("PrimaryGoalPlanFlag") is not False or plan.get("ReviewPeriodId") in (None, ""):
        raise RuntimeContractGap(
            "GOAL_PLAN_TEMPLATE_GOAL_INELIGIBLE: target must be a regular plan with a Review Period"
        )
    if "MassRequestId" not in plan:
        raise RuntimeContractGap(
            "GOAL_PLAN_PROJECTION_INCOMPLETE: re-read the exact item with MassRequestId in fields"
        )
    value = plan["MassRequestId"]
    if value in (None, ""):
        raise RuntimeContractGap(
            "GOAL_PLAN_MASS_REQUEST_MISSING: projected item explicitly returned no MassRequestId"
        )
    if isinstance(value, bool) or not str(value).isdigit() or int(value) <= 0:
        raise RuntimeContractGap(
            "GOAL_PLAN_MASS_REQUEST_INVALID: projected MassRequestId must be a positive integer"
        )
    return int(value)


def resolve_current_lov_value(value: str, allowed_values: Iterable[str]) -> str:
    """Return one current LOV display value or fail closed on no/ambiguous match."""
    matches = [candidate for candidate in allowed_values if str(candidate).casefold() == str(value).casefold()]
    if len(matches) != 1:
        raise RuntimeContractGap("GOAL_PLAN_LOV_VALIDATION_GAP: requirement did not match one current allowed value")
    return str(matches[0])


def resolve_goal_eligibility_profile(
    profiles: Iterable[Mapping[str, Any]],
    *,
    pagination_complete: bool,
    exact_name: str | None = None,
    verified_criteria_match_ids: Iterable[Any] = (),
) -> dict[str, Any]:
    """Resolve an existing Goal Management Eligibility Profile deterministically.

    ``profiles`` must contain the rows from every ``eligibilityProfilesLOV``
    page and the caller must prove that with ``pagination_complete=True``.
    Semantic population criteria are resolved only from IDs produced by an
    authoritative criteria-read capability; this helper never treats a
    similar-looking profile name as proof of its stored criteria.
    """

    if pagination_complete is not True:
        raise RuntimeContractGap(
            "ELIGIBILITY_PROFILE_LOOKUP_INCOMPLETE: every eligibilityProfilesLOV page must be read before resolution"
        )

    def normalized_profile(row: Mapping[str, Any]) -> dict[str, Any] | None:
        profile_id = _mapping_value(row, "EligyPrflId", "EligibilityProfileId")
        name = _mapping_value(row, "Name", "EligibilityProfileName")
        status = str(_mapping_value(row, "StatCd", "StatusCode") or "").upper()
        usage = str(_mapping_value(row, "BnftCagrPrtnCd", "ProfileUsageCode") or "").upper()
        profile_type = str(_mapping_value(row, "ProfileType") or "").upper()
        if profile_id in (None, "") or name in (None, ""):
            return None
        if status != "A" or usage != "GOAL" or profile_type != "PRTP":
            return None
        return {
            "EligibilityProfileId": profile_id,
            "Name": str(name),
            "Description": str(_mapping_value(row, "Description") or ""),
            "StatusCode": status,
            "ProfileUsageCode": usage,
            "ProfileType": profile_type,
        }

    compatible = [
        normalized
        for row in profiles
        if isinstance(row, Mapping)
        for normalized in [normalized_profile(row)]
        if normalized is not None
    ]
    compatible.sort(key=lambda row: (row["Name"].casefold(), str(row["EligibilityProfileId"])))

    supplied_name = str(exact_name or "").strip()
    if supplied_name:
        matches = [row for row in compatible if row["Name"].casefold() == supplied_name.casefold()]
        match_basis = "exact_name"
    else:
        verified_ids = {str(value) for value in verified_criteria_match_ids if value not in (None, "")}
        if not verified_ids:
            return {
                "Outcome": "SELECTION_REQUIRED",
                "MatchBasis": "unverified_semantic_criteria",
                "Candidates": compatible,
            }
        matches = [row for row in compatible if str(row["EligibilityProfileId"]) in verified_ids]
        match_basis = "verified_profile_criteria"

    if len(matches) == 1:
        return {"Outcome": "RESOLVED", "MatchBasis": match_basis, "Profile": matches[0]}
    if not matches:
        return {"Outcome": "MISSING", "MatchBasis": match_basis, "Candidates": []}
    return {"Outcome": "MULTIPLE_MATCHES", "MatchBasis": match_basis, "Candidates": matches}


_ADF_ROOT = re.compile(r"^(https://[^/]+/hcmRestApi/rest/rv:[^/]+/[A-Za-z][A-Za-z0-9_-]*/[^/]+)(?:/|$)")
_DEFAULT_ACTIVE_ASSIGNMENT_STATUS_CODES = frozenset({"A", "ACTIVE", "ACTIVE_PROCESS"})


def resolve_adf_batch_root(rest_base_url: str, runtime_urls: Iterable[str]) -> str:
    """Return one same-host ADF root from current returned metadata/links.

    Captured URLs from another environment are intentionally rejected.  A
    caller must collect ``runtime_urls`` only from the current authenticated
    response/OpenAPI contract; this function never synthesizes a revision.
    """
    expected_host = urlparse(rest_base_url).netloc.lower()
    roots = {
        match.group(1).rstrip("/")
        for value in runtime_urls
        if isinstance(value, str)
        for match in [_ADF_ROOT.match(value)]
        if match and urlparse(match.group(1)).netloc.lower() == expected_host
    }
    if len(roots) != 1:
        raise RuntimeContractGap(
            "GOAL_PLAN_RUNTIME_CONTRACT_GAP: current tenant metadata did not yield one same-host ADF batch root"
        )
    return roots.pop()


def collect_runtime_urls(document: Any) -> list[str]:
    """Collect current URL strings from a metadata/response document."""
    urls: list[str] = []
    if isinstance(document, Mapping):
        for value in document.values():
            urls.extend(collect_runtime_urls(value))
    elif isinstance(document, list):
        for value in document:
            urls.extend(collect_runtime_urls(value))
    elif isinstance(document, str) and document.startswith("https://"):
        urls.append(document)
    return urls


def _values_as_upper_strings(values: Iterable[Any]) -> frozenset[str]:
    return frozenset(str(value).upper() for value in values if value not in (None, ""))


def _iter_mappings(document: Any) -> Iterable[Mapping[str, Any]]:
    if isinstance(document, Mapping):
        yield document
        for value in document.values():
            yield from _iter_mappings(value)
    elif isinstance(document, list):
        for value in document:
            yield from _iter_mappings(value)


def _mapping_value(mapping: Mapping[str, Any], *names: str) -> Any:
    """Read a metadata field without depending on its source casing."""
    normalized = {str(key).lower(): value for key, value in mapping.items()}
    for name in names:
        if name.lower() in normalized:
            return normalized[name.lower()]
    return None


def _public_child_create_action(goal_plan_describe: Mapping[str, Any]) -> Mapping[str, Any] | None:
    """Find an advertised POST create action under a performanceGoals child.

    Goal Plans describe/OpenAPI documents vary in how they nest collection and
    action metadata.  This deliberately inspects only a ``performanceGoals``
    child node supplied from the Goal Plans describe response, never a Library
    Goal response or a remembered tenant capture.
    """
    for parent in _iter_mappings(goal_plan_describe):
        for key, child in parent.items():
            if str(key).lower() != "performancegoals" or not isinstance(child, Mapping):
                continue
            for node in _iter_mappings(child):
                actions = _mapping_value(node, "actions", "operations")
                if not isinstance(actions, list):
                    continue
                for action in actions:
                    if not isinstance(action, Mapping):
                        continue
                    method = str(_mapping_value(action, "method", "httpMethod") or "").upper()
                    name = str(_mapping_value(action, "name", "operation", "operationName") or "").lower()
                    if method == "POST" and name in {"create", "post"}:
                        return action
    return None


def resolve_template_goal_create_contract(
    goal_plan_describe: Mapping[str, Any],
    *,
    rest_base_url: str | None = None,
    runtime_urls: Iterable[str] = (),
) -> dict[str, Any]:
    """Resolve the one current contract for adding a regular-plan goal.

    The public child POST is authoritative when advertised.  ADF batch is a
    fallback only if that POST is absent and a same-host runtime batch root is
    independently available.  This resolver must be called from the selected
    Goal Plans workflow before preview; it is not a browser-discovery route.
    """
    if not isinstance(goal_plan_describe, Mapping):
        raise RuntimeContractGap(
            "GOAL_PLAN_CREATE_CONTRACT_GAP: current Goal Plans metadata is unavailable or malformed"
        )
    action = _public_child_create_action(goal_plan_describe)
    if action is not None:
        content_types = _mapping_value(action, "requestContentTypes", "consumes", "contentTypes")
        if isinstance(content_types, str):
            content_types = [content_types]
        if not isinstance(content_types, list):
            content_types = []
        return {
            "ObjectContext": "goal_plan_template_goal",
            "PayloadContract": "goalPlans_performanceGoals_child_create",
            "PublicChildCreateAdvertised": True,
            "RequestContentTypes": [str(value) for value in content_types],
        }
    if rest_base_url not in (None, ""):
        try:
            root = resolve_adf_batch_root(rest_base_url, runtime_urls)
        except RuntimeContractGap:
            root = None
        if root is not None:
            return {
                "ObjectContext": "goal_plan_template_goal",
                "PayloadContract": "performanceGoalsV2_batch",
                "AdfBatchRootResolved": True,
                "AdfBatchRoot": root,
            }
    raise RuntimeContractGap(
        "GOAL_PLAN_CREATE_CONTRACT_GAP: current Goal Plans metadata advertises no child create and no current ADF batch fallback"
    )


def verify_assignment_outcome(*, job_status: str, expected: Mapping[str, Any],
                              actual: Mapping[str, Any]) -> dict[str, Any]:
    """Consume normalized assignee evidence from the core read adapter.

    Count is the observed final population, not a forecast or inferred delta.
    Reconciliation must verify identities and scope against the configured selector.
    """
    if job_status != "SUCCEEDED":
        return {"status": "job_not_succeeded", "can_complete": False}
    keys = ("environment", "GoalPlanId", "request_id", "population_evidence_ref")
    if (any(not expected.get(key) or actual.get(key) != expected[key] for key in keys)
            or actual.get("pagination_complete") is not True
            or actual.get("fresh_read") is not True
            or actual.get("identities_and_scope_match") is not True):
        return {"status": "verification_pending", "can_complete": False}
    count = actual.get("count")
    if type(count) is not int or count < 0:
        return {"status": "verification_pending", "can_complete": False}
    return {"status": "verified", "can_complete": True, "actual_count": count}


def resolve_active_primary_admin(
    worker: Mapping[str, Any], *, active_status_codes: Iterable[str] | None = None
) -> dict[str, Any]:
    """Validate current-caller assignment context without using a UI identity.

    The owning authenticated-caller adapter supplies the current worker record
    and, when available, the target tenant's active assignment status codes.
    ``active_status_codes`` keeps status interpretation tenant-derived; the
    small default set preserves compatibility for existing direct worker
    routes that return their canonical active codes.
    """
    accepted_statuses = (
        _DEFAULT_ACTIVE_ASSIGNMENT_STATUS_CODES
        if active_status_codes is None
        else _values_as_upper_strings(active_status_codes)
    )
    if not accepted_statuses:
        raise RuntimeContractGap(
            "GOAL_PLAN_ADMIN_CONTEXT_GAP: current worker route did not provide active assignment status semantics"
        )
    person_id = worker.get("PersonId")
    is_lov = "items" in worker
    if worker.get("hasMore") in (True, "true", "True", "Y"):
        raise RuntimeContractGap("GOAL_PLAN_ADMIN_CONTEXT_GAP: finish assignment pagination before validation")
    assignments = worker if is_lov else worker.get("assignments", worker.get("Assignments", []))
    if isinstance(assignments, Mapping):
        if assignments.get("hasMore") in (True, "true", "True", "Y"):
            raise RuntimeContractGap("GOAL_PLAN_ADMIN_CONTEXT_GAP: finish assignment pagination before validation")
        assignments = assignments.get("items", [])
    if not isinstance(assignments, list):
        assignments = []
    # Normalize the authenticated findMyAssignments LOV without changing legacy callers.
    assignments = [dict(a,
                        PrimaryFlag=a.get("AssignmentPrimaryFlag", a.get("PrimaryFlag", a.get("PrimaryAssignmentFlag"))),
                        AssignmentStatusTypeCode=a.get("AssignmentStatusType", a.get("AssignmentStatusTypeCode", a.get("StatusCode"))))
                   for a in assignments if isinstance(a, Mapping)]
    primary_candidates = [a for a in assignments if isinstance(a, Mapping)
                          and a.get("PrimaryFlag", a.get("PrimaryAssignmentFlag")) in (True, "Y", "true", "True")]
    if any(not a.get("AssignmentStatusTypeCode", a.get("StatusCode")) for a in primary_candidates):
        raise RuntimeContractGap("GOAL_PLAN_ADMIN_STATUS_UNKNOWN: primary assignment status is absent, not inactive; an assumption is not verified evidence")
    primary = [
        assignment
        for assignment in assignments
        if isinstance(assignment, Mapping)
        and assignment.get("AssignmentId") not in (None, "")
        and assignment.get("PrimaryFlag", assignment.get("PrimaryAssignmentFlag")) in (True, "Y", "true", "True")
        # This is a status-code comparison, never a display-name inference.
        and str(assignment.get("AssignmentStatusTypeCode", assignment.get("StatusCode", ""))).upper()
        in accepted_statuses
    ]
    if len(primary) == 1:
        row_person = primary[0].get("PersonId")
        if person_id not in (None, "") and row_person not in (None, "") and str(person_id) != str(row_person):
            raise RuntimeContractGap("GOAL_PLAN_ADMIN_CONTEXT_GAP: person and assignment identities disagree")
        if is_lov or person_id in (None, ""):
            person_id = row_person
    if person_id in (None, "") or len(primary) != 1:
        raise RuntimeContractGap(
            "GOAL_PLAN_ADMIN_CONTEXT_GAP: current authenticated worker did not yield one active primary assignment"
        )
    return {"PersonId": person_id, "AssignmentId": primary[0]["AssignmentId"], "AssignmentIsActivePrimary": True}
