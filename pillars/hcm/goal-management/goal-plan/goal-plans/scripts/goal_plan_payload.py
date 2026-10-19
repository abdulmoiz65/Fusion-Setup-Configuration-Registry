"""Pure payload builders for governed Goal Plan operations.

Runtime routes, revisions, hosts, ETags, and tokens deliberately never enter
these builders. Callers resolve those volatile values immediately before an
approved write.
"""

from __future__ import annotations

from datetime import date
from copy import deepcopy
from pathlib import Path
import base64
import sys
import hashlib
import json
from typing import Any, Mapping

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "goal-management-common/scripts"))
from goal_business_rules import validate_goal_plan_rules, validate_goal_setting_rules


class PayloadValidationError(ValueError):
    """Raised before a mutation payload is created."""


GOAL_PLAN_ELIGIBILITY_PROFILE_CHILD = "perfGoalEligibilityProfiles"
GOAL_PLAN_ELIGIBILITY_PROFILE_TALENT_OBJECT_TYPE = "GOAL"
ASSIGN_GOAL_PLANS_JOB_DEFINITION_ID = "JobDefinition://oracle/apps/ess/hcm/goals/core/ScheduleProcessJobDef"
ASSIGN_GOAL_PLANS_APPLICATION = "EarHcmEss"
ASSIGN_GOAL_PLANS_PRODUCT = "HRG"
ASSIGN_GOAL_PLANS_MODE = "ASSIGN_GOAL_PLANS"
ASSIGN_GOAL_PLANS_PROCESS_TYPE_DISPLAY = "Assign goal plans"
ASSIGN_GOAL_PLANS_OPTION_FLAG = "1"
PERFORMANCE_GOAL_DEFAULT_STATUS = "NOT_STARTED"
PERFORMANCE_GOAL_DEFAULT_PRIVATE_FLAG = False
_PERFORMANCE_GOAL_LOB_FIELDS = ("Comments", "SuccessCriteria", "LongDescription")

_CREATE_ONLY_RUNTIME_FIELDS = frozenset(
    {
        "MassRequestId",
        "PersonId",
        "AssignmentId",
        "AssignedByPersonId",
        "GoalVersionTypeCode",
        "RequestContext",
        "GoalSourceCode",
    }
)
_CREATE_DEFAULT_INPUT_FIELDS = frozenset({"ReviewPeriodStartDate", "ReviewPeriodEndDate"})
_GOAL_PLAN_MINIMUM_CREATE_FIELDS = (
    "GoalPlanName",
    "PrimaryGoalPlanFlag",
    "GoalPlanActiveCode",
    "StartDate",
    "EndDate",
)
_REQUIRED_PROFILE_TRUE_PHRASES = (
    "required",
    "mandatory",
    "must be enforced",
)
_REQUIRED_PROFILE_NEGATIONS = (
    "not required",
    "isn't required",
    "is not required",
    "no required",
    "not mandatory",
)
_MAXIMUM_ENFORCEMENT_TRUE_PHRASES = (
    "must not exceed",
    "cannot exceed",
    "can't exceed",
    "no more than",
    "enforce maximum",
    "enforce the maximum",
)
_MAXIMUM_ENFORCEMENT_FALSE_PHRASES = (
    "do not enforce",
    "don't enforce",
    "not enforced",
    "informational only",
)


def _required(source: Mapping[str, Any], *names: str) -> None:
    missing = [name for name in names if source.get(name) in (None, "")]
    if missing:
        raise PayloadValidationError("missing required field(s): " + ", ".join(missing))


def _encode_performance_goal_lobs(payload: dict[str, Any]) -> None:
    """Encode supplied Goal REST LOB text using the advertised ``byte`` format.

    The Goal Plan Performance Goals create schema represents Comments,
    SuccessCriteria, and LongDescription as ``string(byte)``. Source text may
    contain harmless HTML markup, but it must be encoded before it is placed in
    the normal JSON create body. Content is never inferred or fabricated.
    """
    for field in _PERFORMANCE_GOAL_LOB_FIELDS:
        if field not in payload or payload[field] in (None, ""):
            continue
        value = payload[field]
        if not isinstance(value, str):
            raise PayloadValidationError(f"{field} must be supplied as text before byte encoding")
        payload[field] = base64.b64encode(value.encode("utf-8")).decode("ascii")


def _validate_template_goal_execution_context(context: Mapping[str, Any]) -> None:
    """Reject a batch payload until the caller has bound the Goal Plan contract."""
    _required(context, "ObjectContext", "PayloadContract", "AdfBatchRootResolved")
    if context["ObjectContext"] != "goal_plan_template_goal":
        raise PayloadValidationError("template goal requires goal_plan_template_goal context")
    if context["PayloadContract"] != "performanceGoalsV2_batch":
        raise PayloadValidationError("template goal requires performanceGoalsV2_batch contract")
    if context["AdfBatchRootResolved"] is not True:
        raise PayloadValidationError("template goal requires a fresh resolved ADF batch root")
    forbidden = {"libraryGoals", "LibraryGoalId", "LibraryGoalKey", "PerfCategoryCode", "LibraryGoalETag"} & set(context)
    if forbidden:
        raise PayloadValidationError(
            "template goal context includes Library Goal state: " + ", ".join(sorted(forbidden))
        )


def _validate_goal_setting_info(payload: Mapping[str, Any]) -> None:
    """Validate worker-only Goal Setting Info before a Goal Plan create payload."""
    try:
        validate_goal_setting_rules(payload)
    except (KeyError, TypeError, ValueError) as exc:
        raise PayloadValidationError(str(exc)) from exc


def derive_required_profile_flag(requirement_text: str | None) -> bool:
    """Return whether a Goal Plan Eligibility Profile is explicitly required."""
    if not requirement_text:
        return False
    normalized = " ".join(str(requirement_text).lower().split())
    if any(phrase in normalized for phrase in _REQUIRED_PROFILE_NEGATIONS):
        return False
    return any(phrase in normalized for phrase in _REQUIRED_PROFILE_TRUE_PHRASES)


def derive_maximum_goal_enforcement(requirement_text: str | None) -> bool | None:
    """Resolve explicit maximum-enforcement intent without inventing a default.

    Goal Plans contain performance goals.  The returned value is deliberately
    tri-state: ``True`` for restrictive language, ``False`` only for an
    explicit no-enforcement instruction, and ``None`` when enforcement is not
    stated.  Callers omit the REST field for ``None``.
    """
    if not requirement_text:
        return None
    normalized = " ".join(str(requirement_text).lower().split())
    if any(phrase in normalized for phrase in _MAXIMUM_ENFORCEMENT_FALSE_PHRASES):
        return False
    if any(phrase in normalized for phrase in _MAXIMUM_ENFORCEMENT_TRUE_PHRASES):
        return True
    if "prevent" in normalized and ("more than" in normalized or "exceed" in normalized):
        return True
    return None


def _validate_maximum_goal_fields(payload: dict[str, Any], *, allow_enforcement: bool) -> None:
    maximum = payload.get("MaximumGoalsNumberInGoalPlan")
    if maximum is not None and (
        isinstance(maximum, bool) or not isinstance(maximum, int) or maximum < 1
    ):
        raise PayloadValidationError("MaximumGoalsNumberInGoalPlan must be a positive integer")

    if "EnforceMaximumGoalsInGpFlag" not in payload:
        return
    enforcement = payload["EnforceMaximumGoalsInGpFlag"]
    if enforcement is None:
        payload.pop("EnforceMaximumGoalsInGpFlag")
        return
    if not isinstance(enforcement, bool):
        raise PayloadValidationError("EnforceMaximumGoalsInGpFlag must be true, false, or omitted")
    if enforcement is True and maximum is None:
        raise PayloadValidationError("maximum enforcement requires MaximumGoalsNumberInGoalPlan")
    if enforcement is True and not allow_enforcement:
        raise PayloadValidationError(
            "new Goal Plan enforcement requires the staged create execution plan"
        )


def build_eligibility_profile_association_payload(
    fields: Mapping[str, Any], *, child_collection: str = GOAL_PLAN_ELIGIBILITY_PROFILE_CHILD
) -> dict[str, Any]:
    """Build one Goal Plan Eligibility Profile child-association payload.

    Tenant-validated runtime evidence confirms that Goal Management Goal Plan
    associations use ``TalentObjectType="GOAL"`` for the
    ``perfGoalEligibilityProfiles`` child only. The caller still resolves the
    exact Goal Plan, child collection support, and Eligibility Profile from the
    current tenant before preview.
    """
    if child_collection != GOAL_PLAN_ELIGIBILITY_PROFILE_CHILD:
        raise PayloadValidationError("TalentObjectType=GOAL is only valid for perfGoalEligibilityProfiles")
    if "TalentObjectType" in fields:
        raise PayloadValidationError("TalentObjectType is skill-derived for Goal Plan Eligibility Profile associations")
    _required(fields, "EligibilityProfileId")
    if fields.get("StatCd") not in (None, "", "A"):
        raise PayloadValidationError("Eligibility Profile must be active")
    if fields.get("StatusCode") not in (None, "", "A"):
        raise PayloadValidationError("Eligibility Profile must be active")
    usage = fields.get("ProfileUsageCode", fields.get("BnftCagrPrtnCd"))
    if usage not in (None, "", "GOAL"):
        raise PayloadValidationError("Eligibility Profile usage must be compatible with Goal Management")
    if fields.get("ProfileType") not in (None, "", "PRTP"):
        raise PayloadValidationError("Eligibility Profile must be a participant profile")

    if "RequiredFlag" in fields:
        if not isinstance(fields["RequiredFlag"], bool):
            raise PayloadValidationError("RequiredFlag must be a boolean when supplied by an internal resolver")
        required_flag = fields["RequiredFlag"]
    else:
        required_flag = derive_required_profile_flag(fields.get("RequirementText"))

    return {
        "EligibilityProfileId": fields["EligibilityProfileId"],
        "RequiredFlag": required_flag,
        "TalentObjectType": GOAL_PLAN_ELIGIBILITY_PROFILE_TALENT_OBJECT_TYPE,
    }


def _validate_goal_plan_create_contract(
    fields: Mapping[str, Any], writable_fields: set[str] | frozenset[str] | None
) -> None:
    """Reject fields that a new Goal Plan create must never send.

    ``writable_fields`` is the exact current create-field set resolved from
    ``goalPlans/describe``.  It is supplied by the caller immediately before
    preview; this helper deliberately does not preserve a tenant field list.
    """
    forbidden = _CREATE_ONLY_RUNTIME_FIELDS & set(fields)
    if forbidden:
        raise PayloadValidationError(
            "new Goal Plan create must not contain runtime template-goal field(s): "
            + ", ".join(sorted(forbidden))
        )
    if "GoalAccessLevel" in fields:
        raise PayloadValidationError("GoalAccessLevel is unsupported; use current metadata field GoalAccessLevelCode")
    if writable_fields is None:
        return
    allowed = set(writable_fields) | _CREATE_DEFAULT_INPUT_FIELDS
    unsupported = set(fields) - allowed
    if unsupported:
        raise PayloadValidationError(
            "Goal Plan create contains field(s) not writable in current metadata: " + ", ".join(sorted(unsupported))
        )


def build_goal_plan_create_payload(
    fields: Mapping[str, Any], *, writable_fields: set[str] | frozenset[str] | None = None
) -> dict[str, Any]:
    """Build a new regular-plan payload with resolved Review Period date defaults.

    Callers must pass the current ``goalPlans/describe`` writable create-field
    set before an approval preview.  The optional argument remains available
    for local composition tests that do not have live metadata.
    """
    _validate_goal_plan_create_contract(fields, writable_fields)
    payload = dict(fields)
    review_bounds = None
    if fields.get("ReviewPeriodStartDate") and fields.get("ReviewPeriodEndDate"):
        review_bounds = {"StartDate": fields["ReviewPeriodStartDate"], "EndDate": fields["ReviewPeriodEndDate"]}
    payload.setdefault("PrimaryGoalPlanFlag", False)
    payload.setdefault("GoalPlanActiveCode", "I")
    if not isinstance(payload["PrimaryGoalPlanFlag"], bool):
        raise PayloadValidationError("PrimaryGoalPlanFlag must be true or false")
    if payload["GoalPlanActiveCode"] != "I":
        raise PayloadValidationError("new Goal Plans must be created inactive with GoalPlanActiveCode=I")
    if payload.get("PrimaryGoalPlanFlag") is not True:
        _required(payload, "ReviewPeriodId")
        has_start = payload.get("StartDate") not in (None, "")
        has_end = payload.get("EndDate") not in (None, "")
        if has_start != has_end:
            raise PayloadValidationError("regular Goal Plan dates must be supplied together or both defaulted from the Review Period")
        if not has_start:
            _required(payload, "ReviewPeriodStartDate", "ReviewPeriodEndDate")
            payload["StartDate"] = payload["ReviewPeriodStartDate"]
            payload["EndDate"] = payload["ReviewPeriodEndDate"]
    payload.pop("ReviewPeriodStartDate", None)
    payload.pop("ReviewPeriodEndDate", None)
    _required(payload, *_GOAL_PLAN_MINIMUM_CREATE_FIELDS)
    if writable_fields is not None:
        unsupported_final = set(payload) - set(writable_fields)
        if unsupported_final:
            raise PayloadValidationError(
                "Goal Plan create contains defaulted field(s) not writable in current metadata: "
                + ", ".join(sorted(unsupported_final))
            )
    try:
        plan_start = date.fromisoformat(str(payload["StartDate"]))
        plan_end = date.fromisoformat(str(payload["EndDate"]))
    except (TypeError, ValueError) as exc:
        raise PayloadValidationError("Goal Plan dates must be ISO YYYY-MM-DD values") from exc
    if plan_start > plan_end:
        raise PayloadValidationError("Goal Plan start date must be on or before its end date")
    _validate_goal_setting_info(payload)
    _validate_maximum_goal_fields(payload, allow_enforcement=False)
    try:
        validate_goal_plan_rules(payload, review_period=review_bounds)
    except (ValueError, TypeError, KeyError) as exc:
        raise PayloadValidationError(str(exc)) from exc
    return payload


def build_goal_plan_create_execution_plan(
    fields: Mapping[str, Any], *, environment: str,
    writable_fields: set[str] | frozenset[str] | None = None,
    request_path: str = "/goalPlans",
) -> dict[str, Any]:
    """Build one approval-bound create plan with optional staged enforcement.

    The maximum count belongs to the performance goals in the Goal Plan.  When
    enforcement is explicitly true, create the plan with the maximum but omit
    the enforcement flag, verify that the maximum persisted, and only then
    patch enforcement.  The generated GoalPlanId is resolved from the verified
    create and does not change the approved business target.
    """
    if not isinstance(environment, str) or not environment.strip():
        raise PayloadValidationError("environment must be non-empty for approval binding")
    if writable_fields is None:
        raise PayloadValidationError("Execution preview requires current writable metadata")
    if not fields.get("PrimaryGoalPlanFlag") and not all(fields.get(k) for k in ("ReviewPeriodStartDate", "ReviewPeriodEndDate")):
        raise PayloadValidationError("Execution preview requires resolved Review Period bounds")
    requested = deepcopy(dict(fields))
    enforcement = requested.get("EnforceMaximumGoalsInGpFlag")
    if enforcement is not None and not isinstance(enforcement, bool):
        raise PayloadValidationError("EnforceMaximumGoalsInGpFlag must be true, false, or omitted")
    if enforcement is True and requested.get("MaximumGoalsNumberInGoalPlan") is None:
        raise PayloadValidationError("maximum enforcement requires MaximumGoalsNumberInGoalPlan")
    if (
        enforcement is True
        and writable_fields is not None
        and "EnforceMaximumGoalsInGpFlag" not in writable_fields
    ):
        raise PayloadValidationError(
            "EnforceMaximumGoalsInGpFlag is not writable in current metadata"
        )

    create_fields = dict(requested)
    if enforcement is True:
        create_fields.pop("EnforceMaximumGoalsInGpFlag", None)
    create_payload = build_goal_plan_create_payload(create_fields, writable_fields=writable_fields)
    _required(create_payload, "GoalPlanName")

    target = {
        "GoalPlanName": create_payload["GoalPlanName"],
        "ReviewPeriodId": create_payload.get("ReviewPeriodId"),
        "PrimaryGoalPlanFlag": create_payload.get("PrimaryGoalPlanFlag", False),
    }
    maximum = create_payload.get("MaximumGoalsNumberInGoalPlan")
    steps: list[dict[str, Any]] = [
        {
            "sequence": 1,
            "operation": "create",
            "method": "POST",
            "target": "goalPlans",
            "payload": create_payload,
        },
        {
            "sequence": 2,
            "operation": "verify_create",
            "business_key": target,
            "expected": dict(create_payload),
        },
    ]
    if enforcement is True:
        steps.extend(
            [
                {
                    "sequence": 3,
                    "operation": "enable_maximum_enforcement",
                    "method": "PATCH",
                    "target": "verified_create_item",
                    "precondition": {"MaximumGoalsNumberInGoalPlan": maximum},
                    "payload": {"EnforceMaximumGoalsInGpFlag": True},
                },
                {
                    "sequence": 4,
                    "operation": "verify_enforcement",
                    "business_key": target,
                    "expected": {
                        "MaximumGoalsNumberInGoalPlan": maximum,
                        "EnforceMaximumGoalsInGpFlag": True,
                    },
                },
            ]
        )

    result = {
        "approval_scope": "goal_plan_create_configuration",
        "environment": environment,
        "request_path": request_path,
        "business_target": target,
        "single_approval_for_exact_sequence": True,
        "stop_without_retry_on_failed_or_uncertain_step": True,
        "steps": steps,
    }
    approval_envelope = {
        "environment": environment.strip().casefold(),
        "operation": "Create Goal Plan configuration",
        "request_path": request_path,
        "identity": target,
        "steps": steps,
    }
    result["approval_envelope"] = approval_envelope
    result["sha256"] = hashlib.sha256(
        json.dumps(approval_envelope, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    result["approval"] = {
        "required": "Reply Approve, Yes, or Go ahead to continue.",
        "fingerprint_is_internal": True,
        "payload_change_requires_fresh_approval": True,
    }
    return result


def approval_is_current(approved_fingerprint: str, preview: Mapping[str, Any]) -> bool:
    try:
        envelope = {"environment": preview["environment"].strip().casefold(),
                    "operation": "Create Goal Plan configuration", "request_path": preview["request_path"],
                    "identity": preview["business_target"], "steps": preview["steps"]}
        digest = hashlib.sha256(json.dumps(envelope, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        return digest == preview["sha256"] == approved_fingerprint
    except (KeyError, TypeError, AttributeError):
        return False


def build_included_worker_payload(fields: Mapping[str, Any]) -> dict[str, Any]:
    """Build the public included-worker child payload without assignee filters."""
    _required(fields, "PersonId", "AssignmentId", "CascadingLevel")
    forbidden = {"ManagerAssignmentId", "EssAssignmentId", "AssignmentIntent"} & set(fields)
    if forbidden:
        raise PayloadValidationError(
            "included-worker payload must not contain: " + ", ".join(sorted(forbidden))
        )
    return {key: fields[key] for key in ("PersonId", "AssignmentId", "CascadingLevel")}


def _default_template_goal_priority(payload, execution_context, addition_kind):
    """Preserve explicit/copied priority; default only an omitted create field."""
    if "PriorityCode" in payload:
        return
    source = execution_context.get("SourceLibraryGoal") if addition_kind == "library" else None
    if source is not None:
        if not isinstance(source, Mapping) or str(source.get("GoalId")) != str(payload.get("ReferenceContentItemId")):
            raise PayloadValidationError("source Library Goal does not match ReferenceContentItemId")
        if source.get("PriorityCode") not in (None, ""):
            payload["PriorityCode"] = source["PriorityCode"]
            return
    payload["PriorityCode"] = "MEDIUM"


def build_template_goal_batch(
    existing_plan: Mapping[str, Any],
    admin_context: Mapping[str, Any],
    goal_fields: Mapping[str, Any],
    execution_context: Mapping[str, Any],
    *,
    addition_kind: str = "library",
) -> dict[str, Any]:
    """Build one ADF batch part for a library or independent regular-plan goal."""
    _validate_template_goal_execution_context(execution_context)
    _required(existing_plan, "GoalPlanId", "ReviewPeriodId", "MassRequestId")
    if existing_plan.get("PrimaryGoalPlanFlag") is not False:
        raise PayloadValidationError("template goals require an existing regular Goal Plan")
    _required(admin_context, "PersonId", "AssignmentId")
    if admin_context.get("AssignmentIsActivePrimary") is not True:
        raise PayloadValidationError("admin AssignmentId must be the confirmed active primary assignment")
    _required(goal_fields, "GoalName")
    if addition_kind not in {"library", "non_library"}:
        raise PayloadValidationError("addition_kind must be library or non_library")

    forbidden = {"ManagerAssignmentId", "adfBatchRoot", "host", "revision", "ETag"} & set(goal_fields)
    if forbidden:
        raise PayloadValidationError("goal fields include forbidden runtime/filter data")
    if "Weighting" in goal_fields and not isinstance(goal_fields["Weighting"], (int, float)):
        raise PayloadValidationError("template goal Weighting must use the numeric performanceGoalsV2 schema")

    payload = dict(goal_fields)
    reference_id = payload.get("ReferenceContentItemId")
    if addition_kind == "library" and reference_id in (None, ""):
        raise PayloadValidationError("library Goal Plan additions require ReferenceContentItemId")
    if addition_kind == "non_library" and reference_id not in (None, ""):
        raise PayloadValidationError("non-library Goal Plan additions must not reference a Library Goal")
    _default_template_goal_priority(payload, execution_context, addition_kind)
    has_start = payload.get("StartDate") not in (None, "")
    has_target = payload.get("TargetCompletionDate") not in (None, "")
    if has_start != has_target:
        raise PayloadValidationError("template goal dates must be supplied together or both defaulted from the Goal Plan")
    if not has_start:
        _required(existing_plan, "StartDate", "EndDate")
        payload["StartDate"] = existing_plan["StartDate"]
        payload["TargetCompletionDate"] = existing_plan["EndDate"]
    payload.update(
        {
            "PersonId": admin_context["PersonId"],
            "AssignmentId": admin_context["AssignmentId"],
            "GoalPlanId": existing_plan["GoalPlanId"],
            "ReviewPeriodId": existing_plan["ReviewPeriodId"],
            "MassRequestId": existing_plan["MassRequestId"],
            "GoalVersionTypeCode": "MASS_REQ",
            "RequestContext": "AdminUI",
            "GoalSourceCode": "HR",
        }
    )
    return {"parts": [{"id": "Create-goal-1", "path": "/performanceGoalsV2", "operation": "create", "payload": payload}]}


def build_template_goal_child_create(
    existing_plan: Mapping[str, Any],
    admin_context: Mapping[str, Any],
    goal_fields: Mapping[str, Any],
    execution_context: Mapping[str, Any],
    *,
    addition_kind: str = "library",
) -> dict[str, Any]:
    """Build an advertised public child-create body for a regular-plan goal.

    This is separate from ``build_template_goal_batch`` and is valid only when
    current Goal Plans metadata advertises POST on the selected plan's
    ``performanceGoals`` child collection.
    """
    _required(execution_context, "ObjectContext", "PayloadContract", "PublicChildCreateAdvertised")
    if execution_context["ObjectContext"] != "goal_plan_template_goal":
        raise PayloadValidationError("template goal requires goal_plan_template_goal context")
    if execution_context["PayloadContract"] != "goalPlans_performanceGoals_child_create":
        raise PayloadValidationError("template goal requires public performanceGoals child-create contract")
    if execution_context["PublicChildCreateAdvertised"] is not True:
        raise PayloadValidationError("template goal requires a currently advertised public child-create operation")
    _required(existing_plan, "GoalPlanId", "ReviewPeriodId", "MassRequestId", "StartDate", "EndDate")
    if existing_plan.get("PrimaryGoalPlanFlag") is not False:
        raise PayloadValidationError("template goals require an existing regular Goal Plan")
    _required(admin_context, "PersonId", "AssignmentId")
    if admin_context.get("AssignmentIsActivePrimary") is not True:
        raise PayloadValidationError("admin AssignmentId must be the confirmed active primary assignment")
    _required(goal_fields, "GoalName")
    if addition_kind not in {"library", "non_library"}:
        raise PayloadValidationError("addition_kind must be library or non_library")
    payload = dict(goal_fields)
    reference_id = payload.get("ReferenceContentItemId")
    if addition_kind == "library" and reference_id in (None, ""):
        raise PayloadValidationError("library Goal Plan additions require ReferenceContentItemId")
    if addition_kind == "non_library" and reference_id not in (None, ""):
        raise PayloadValidationError("non-library Goal Plan additions must not reference a Library Goal")
    _default_template_goal_priority(payload, execution_context, addition_kind)
    forbidden = {"ManagerAssignmentId", "adfBatchRoot", "host", "revision", "ETag", "PerfCategoryCode"} & set(payload)
    if forbidden:
        raise PayloadValidationError("goal fields include forbidden runtime/filter data")
    has_start = payload.get("StartDate") not in (None, "")
    has_target = payload.get("TargetCompletionDate") not in (None, "")
    if has_start != has_target:
        raise PayloadValidationError("template goal dates must be supplied together or both defaulted from the Goal Plan")
    if not has_start:
        payload["StartDate"] = existing_plan["StartDate"]
        payload["TargetCompletionDate"] = existing_plan["EndDate"]
    _encode_performance_goal_lobs(payload)
    payload.update(
        {
            "PersonId": admin_context["PersonId"],
            "AssignmentId": admin_context["AssignmentId"],
            "AssignedByPersonId": admin_context["PersonId"],
            "GoalPlanId": existing_plan["GoalPlanId"],
            "ReviewPeriodId": existing_plan["ReviewPeriodId"],
            "MassRequestId": existing_plan["MassRequestId"],
            "GoalVersionTypeCode": "MASS_REQ",
            "RequestContext": "AdminUI",
            "GoalSourceCode": "HR",
        }
    )
    payload.setdefault("StatusCode", PERFORMANCE_GOAL_DEFAULT_STATUS)
    payload.setdefault("PrivateFlag", PERFORMANCE_GOAL_DEFAULT_PRIVATE_FLAG)
    return payload


def build_template_goal_create(
    existing_plan: Mapping[str, Any],
    admin_context: Mapping[str, Any],
    goal_fields: Mapping[str, Any],
    execution_context: Mapping[str, Any],
    *,
    addition_kind: str = "library",
) -> dict[str, Any]:
    """Build only the body selected by the current Goal Plans create contract.

    The caller submits ``payload`` to the endpoint selected by its current
    resolver output.  Keeping the selected contract with the payload prevents
    an ADF envelope from being sent to an advertised ordinary child POST (or
    the reverse) after the approval preview was generated.
    """
    contract = execution_context.get("PayloadContract")
    if contract == "goalPlans_performanceGoals_child_create":
        payload = build_template_goal_child_create(
            existing_plan, admin_context, goal_fields, execution_context, addition_kind=addition_kind
        )
    elif contract == "performanceGoalsV2_batch":
        payload = build_template_goal_batch(
            existing_plan, admin_context, goal_fields, execution_context, addition_kind=addition_kind
        )
    else:
        raise PayloadValidationError("template goal requires a resolved supported create contract")
    return {"PayloadContract": contract, "payload": payload}


def _ess_param(name: str, value: Any = None) -> dict[str, Any]:
    parameter = {"name": name, "paramType": "STRING"}
    if value is not _OMITTED:
        parameter["value"] = value
    return parameter


class _Omitted:
    pass


_OMITTED = _Omitted()


def validate_assignment_impact(goal_plan: Mapping[str, Any], *, effective_date: str,
                               environment: str | None, evidence: Mapping[str, Any] | None) -> None:
    """Validate domain impact before the core submitter receives an ESS body.

    Evidence describes the configured population selector and execution approval.
    ESS determines eligible employees; no advance count or employee list is required.
    """
    if not isinstance(evidence, Mapping):
        raise PayloadValidationError("verified assignment impact evidence is required")
    if (not environment or evidence.get("environment") != environment
            or evidence.get("GoalPlanName") != goal_plan.get("GoalPlanName")
            or str(evidence.get("MassRequestId")) != str(goal_plan.get("MassRequestId"))
            or evidence.get("effective_date") != effective_date):
        raise PayloadValidationError("assignment impact evidence does not match the current target")
    for flag in ("population_verified", "fresh_read"):
        if evidence.get(flag) is not True:
            raise PayloadValidationError(f"assignment impact requires {flag} for the configured population selector")
    if not evidence.get("population_evidence_ref") or not evidence.get("approval_ref"):
        raise PayloadValidationError("assignment impact requires population and approval evidence references")


def resolve_assignment_effective_date(effective_date: str | None = None) -> str:
    """Resolve the ESS-only default at preview time; retain it through approval.

    Callers with a user/project timezone pass that context's current ISO date.
    Otherwise today is the execution host's local calendar date. This default
    does not apply to worker lookup or any other date field.
    """
    if effective_date is None or effective_date == "":
        return date.today().isoformat()
    try:
        if not isinstance(effective_date, str) or date.fromisoformat(effective_date).isoformat() != effective_date:
            raise ValueError()
    except (ValueError, TypeError):
        raise PayloadValidationError("effective_date must be an ISO YYYY-MM-DD calendar date") from None
    return effective_date


def build_assign_goal_plan_ess_payload(
    goal_plan: Mapping[str, Any],
    *,
    effective_date: str | None = None,
    description: str = "Assign goal plan",
    impact_evidence: Mapping[str, Any] | None = None,
    environment: str | None = None,
) -> dict[str, Any]:
    """Build the verified ESS payload for one Goal Plan assignment request.

    The contract is scoped to Goal Management's Manage Goal Scheduled Process
    only.  It uses the verified ``ASSIGN_GOAL_PLANS`` mode and a single current
    regular Goal Plan's name, dates, and MassRequestId.  The numeric option flag
    is preserved from successful Assign Goal Plans Scheduler evidence; it is not
    interpreted as a purge value or reused by any other scheduled process.
    """
    _required(goal_plan, "GoalPlanName", "StartDate", "EndDate", "MassRequestId")
    if goal_plan.get("PrimaryGoalPlanFlag") is not False:
        raise PayloadValidationError("Assign Goal Plans requires an existing regular Goal Plan")
    if goal_plan.get("GoalPlanActiveCode") != "A":
        raise PayloadValidationError("Assign Goal Plans requires an active Goal Plan")
    effective_date = resolve_assignment_effective_date(effective_date)
    validate_assignment_impact(goal_plan, effective_date=effective_date,
                               environment=environment, evidence=impact_evidence)

    return {
        "description": description,
        "jobDefinitionId": ASSIGN_GOAL_PLANS_JOB_DEFINITION_ID,
        "application": ASSIGN_GOAL_PLANS_APPLICATION,
        "product": ASSIGN_GOAL_PLANS_PRODUCT,
        "requestParameters": [
            _ess_param("submit.argument1", ASSIGN_GOAL_PLANS_MODE),
            _ess_param("submit.argument2", goal_plan["GoalPlanName"]),
            _ess_param("submit.argument3", None),
            _ess_param("submit.argument4", goal_plan["StartDate"]),
            _ess_param("submit.argument5", goal_plan["EndDate"]),
            _ess_param("submit.argument6", str(goal_plan["MassRequestId"])),
            _ess_param("submit.argument7", None),
            _ess_param("submit.argument8", None),
            _ess_param("submit.argument9", _OMITTED),
            _ess_param("submit.argument10", _OMITTED),
            _ess_param("submit.argument11", _OMITTED),
            _ess_param("submit.argument12", effective_date),
            _ess_param("submit.argument13", ASSIGN_GOAL_PLANS_PROCESS_TYPE_DISPLAY),
            _ess_param("submit.argument14", None),
            _ess_param("submit.argument15", None),
            _ess_param("submit.argument16", _OMITTED),
            _ess_param("submit.argument17", ASSIGN_GOAL_PLANS_OPTION_FLAG),
            _ess_param("display.attribute2.label", "Goal Plan Name"),
            _ess_param("display.attribute2.value", goal_plan["GoalPlanName"]),
            _ess_param("display.attribute4.label", "Goal Plan Start Date"),
            _ess_param("display.attribute4.value", goal_plan["StartDate"]),
            _ess_param("display.attribute5.label", "Goal Plan End Date"),
            _ess_param("display.attribute5.value", goal_plan["EndDate"]),
            _ess_param("display.attribute6.label", "Purge Start Days"),
            _ess_param("display.attribute6.value", None),
            _ess_param("display.attribute7.label", "Mass Assignment ID"),
            _ess_param("display.attribute7.value", str(goal_plan["MassRequestId"])),
            _ess_param("display.attribute12.label", "Effective Date"),
            _ess_param("display.attribute12.value", effective_date),
            _ess_param("display.attribute13.label", "Process Type"),
            _ess_param("display.attribute13.value", ASSIGN_GOAL_PLANS_PROCESS_TYPE_DISPLAY),
            _ess_param("display.attribute16.label", "Person Numbers"),
            _ess_param("display.attribute16.value", None),
        ],
    }
