"""Pure requirement-to-field resolution for Goal Management planning."""
from __future__ import annotations
from datetime import date
import re
from typing import Any, Iterable, Mapping

class FieldResolutionError(ValueError):
    pass

def classify_statement(statement: str) -> str:
    if re.search(r"\b(?:do not|don't|never)\s+(?:assign|include|exclude|populate)\b", statement.casefold()):
        return "explicit_no_assignment"
    value = " ".join(statement.casefold().split())
    if any(word in value for word in ("eligibility profile", "eligible worker", "populate", "assign worker", "include worker", "exclude worker")):
        return "population_or_assignment_intent"
    # Match action plus population nouns without depending on their adjacency.
    # This covers prose, table cells, and extracted document rows such as
    # "Assign US employees working with Legal Entity ..." while preserving
    # descriptive wording such as "supports employees working in ...".
    if re.search(r"\b(assign|include|exclude)\b", value) and re.search(
        r"\b(employee|employees|worker|workers|person|people)\b", value
    ):
        return "population_or_assignment_intent"
    if any(word in value for word in ("supports employees", "intended for", "purpose", "audience", "working in")):
        return "business_context"
    return "configuration_intent"

def resolve_lov_value(value: str, allowed_values: Iterable[str]) -> str:
    matches = [candidate for candidate in allowed_values if candidate.casefold() == value.casefold()]
    if len(matches) != 1:
        raise FieldResolutionError("requirement does not resolve to one current LOV value")
    return matches[0]

def resolve_qualifier(value: str, fields: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    matches = []
    for field in fields:
        try:
            if field.get("writable") is True:
                matches.append({"field": field["name"], "value": resolve_lov_value(value, field.get("allowed_values", []))})
        except (FieldResolutionError, KeyError):
            pass
    return {"status": "resolved", **matches[0]} if len(matches) == 1 else {"status": "ambiguous" if matches else "unmapped", "candidates": matches}


def resolve_library_goal_availability(
    statement: str | None,
    *,
    business_unit_id: int | str | None = None,
) -> dict[str, Any]:
    """Resolve the standard full-role Library Goal audience and optional BU scope.

    ``Visible`` is the writable role-audience code. ``AvailableTo`` is a
    read-only display meaning used only for post-create verification. Wording
    that a goal is required is retained as an assignment indicator and never
    triggers assignment from this setup task.
    """
    value = " ".join((statement or "").casefold().split())
    full_audience = any(
        phrase in value
        for phrase in (
            "all employees",
            "company-wide",
            "company wide",
            "hr specialist, manager, and worker",
        )
    )
    bu_scoped = bool(re.search(r"\bbusiness unit\b|\bbu\b", value))
    required_indicator = "required" in value
    # Explicit limitations must never become the default full-role audience.
    if (re.search(r"\b(?:except|excluding|not|never)\b|don't", value)
        or re.search(r"\b(?:department|legal employer|job family)\b", value)
        or (not bu_scoped and re.search(r"\b(?:only|restricted|specialists?|managers?|workers?)\b", value)
            and not full_audience)):
        return {"status": "unmapped", "message": "Resolve the explicit audience/scope against current metadata; do not broaden it.",
                "required_assignment_indicator": required_indicator}

    if bu_scoped and business_unit_id is None:
        return {
            "status": "resolution_required",
            "field": "BusinessUnitId",
            "message": "Business Unit availability requires one exact resolved BusinessUnitId.",
            "required_assignment_indicator": required_indicator,
        }
    if bu_scoped or full_audience or not value:
        result: dict[str, Any] = {
            "status": "resolved" if value else "defaulted",
            "Visible": "ALL",
            "AvailableToMeaning": "HR specialist, manager, and worker",
            "required_assignment_indicator": required_indicator,
            "assignment_requested": False,
        }
        if bu_scoped:
            result["BusinessUnitId"] = business_unit_id
        return result
    if value:
        return {
            "status": "unmapped",
            "message": "Audience language does not resolve to the supported full-role mapping.",
            "required_assignment_indicator": required_indicator,
        }
    return {
        "status": "defaulted",
        "Visible": "ALL",
        "AvailableToMeaning": "HR specialist, manager, and worker",
        "required_assignment_indicator": required_indicator,
        "assignment_requested": False,
    }

def propose_library_goal_name(variant: str, topic: str) -> str:
    """Return a review-only candidate name from an explicit variant and topic."""
    normalized_variant = " ".join(variant.split()).title()
    normalized_topic = " ".join(topic.split()).title()
    if normalized_variant not in {"Performance", "Development"} or not normalized_topic:
        raise FieldResolutionError("a Performance or Development variant and a non-empty topic are required")
    return f"{normalized_variant} Library Goal - {normalized_topic}"

def propose_library_goal_names(records: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Return source names unchanged and review-only candidate names."""
    result, counts = [], {}
    for record in records:
        name = record.get("GoalName")
        if isinstance(name, str) and name.strip():
            result.append({"status": "source_supplied", "GoalName": name.strip()})
            continue
        proposed = propose_library_goal_name(str(record.get("variant", "")), str(record.get("topic", "")))
        counts[proposed.casefold()] = counts.get(proposed.casefold(), 0) + 1
        result.append({"status": "proposed", "GoalName": proposed})
    for item in result:
        if item["status"] == "proposed" and counts[item["GoalName"].casefold()] > 1:
            item["status"] = "naming_decision_required"
    return result


_GOAL_SETTING_RESTRICTIONS = {
    "add_only": (True, False),
    "edit_cancel_delete_only": (False, True),
    "both": (True, True),
    "neither": (False, False),
}

_GOAL_SETTING_MARKERS = (
    "goal-setting period",
    "goal setting period",
    "goal-setting start",
    "goal setting start",
    "goal-setting end",
    "goal setting end",
    "end date for setting goals",
    "setting goals",
)


def mentions_goal_setting_info(statement: str) -> bool:
    """Return true when a statement belongs to Goal Plan Goal Setting Info."""
    value = " ".join(statement.casefold().split())
    return any(marker in value for marker in _GOAL_SETTING_MARKERS)


def resolve_goal_plan_access(statement: str) -> dict[str, Any]:
    """Route explicit all-role access language to the Goal Plan access field.

    This deliberately returns a metadata-resolution result rather than guessing
    a volatile tenant LOV code. It is separate from Goal Setting Info, whose
    post-end flags apply to workers only.
    """
    value = " ".join(statement.casefold().split())
    if re.search(r"\b(?:not|no|never|except|excluding)\b|don't|mustn't", value):
        return {"status": "clarification_required", "field": "GoalAccessLevelCode",
                "prompt": "Resolve the restricted role-access intent against current metadata; do not apply all-role access."}
    explicit_all_roles = "all roles" in value
    enumerated_all_roles = (
        "hr specialist" in value
        and "manager" in value
        and re.search(r"\bworker(s)?\b", value) is not None
    )
    if (explicit_all_roles or enumerated_all_roles) and any(
        word in value for word in ("access", "update", "maintain", "manage")
    ):
        return {
            "status": "metadata_resolution_required",
            "field": "GoalAccessLevelCode",
            "semantic_value": "all_roles_can_access_and_update",
            "independent_of": [
                "RestrictGoalCreationFlag",
                "RestrictGoalUpdateFlag",
            ],
        }
    return {"status": "not_requested"}


def resolve_goal_setting_worker_restriction(statement: str) -> dict[str, Any]:
    """Map explicit Goal Setting Info language to worker-only restriction flags.

    The Goal Plan controls affect workers after the Goal Setting end date. They
    are additive to, rather than in conflict with, the plan access-level LOV.
    """
    value = " ".join(statement.casefold().split())
    value = value.replace("’", "'")
    has_add = bool(re.search(r"\b(?:add\w*|creat\w*)\b", value))
    has_update = bool(re.search(r"\b(?:edit\w*|cancel\w*|delet\w*|updat\w*)\b", value))
    ambiguous = {"status": "clarification_required", "applies_to": "workers_only",
                 "prompt": "Confirm each worker restriction after the end date: add and edit/cancel/delete, independently."}
    if re.search(r"\b(?:but|except|unless|however)\b", value):
        return ambiguous
    unrestricted = bool(re.search(r"\b(?:do not|don't|never)\s+(?:restrict|prevent|prohibit|block)\b|\bno restrictions?\b", value))
    if unrestricted:
        remainder = re.sub(r"\b(?:do not|don't|never)\s+(?:restrict|prevent|prohibit|block)\b|\bno restrictions?\b", "", value)
        if re.search(r"\b(?:restrict\w*|prevent\w*|prohibit\w*|cannot|don't allow|do not allow)\b", remainder):
            return ambiguous
    if "during" in value and "after" not in value:
        return ambiguous
    prohibited = bool(re.search(r"\b(?:cannot|can't|must not|don't allow|do not allow|restrict\w*|prevent\w*|prohibit\w*)\b|\bno goals?\b", value))
    permitted = bool(re.search(r"\b(?:allow\w*|may|can)\b", value)) and not prohibited
    if "neither" in value:
        has_add = has_update = True
        unrestricted = True
    if not (unrestricted or prohibited or permitted):
        return ambiguous
    if has_add and has_update:
        selection = "both"
    elif has_add:
        selection = "add_only"
    elif has_update:
        selection = "edit_cancel_delete_only"
    else:
        return {
            "status": "clarification_required",
            "applies_to": "workers_only",
            "prompt": (
                "For workers after the Goal Setting end date, select add only, "
                "edit/cancel/delete only, both, or neither."
            ),
        }
    creation, update = _GOAL_SETTING_RESTRICTIONS[selection]
    if unrestricted or permitted:
        creation, update = False, False
    result = {
        "status": "resolved",
        "applies_to": "workers_only",
        "selection": selection,
        "RestrictGoalCreationFlag": creation,
        "RestrictGoalUpdateFlag": update,
    }
    # A single-checkbox instruction must not clear the other checkbox on update.
    if not has_add:
        result.pop("RestrictGoalCreationFlag")
    if not has_update:
        result.pop("RestrictGoalUpdateFlag")
    return result


def resolve_goal_plan_goal_setting_controls(
    statements: Iterable[str],
    goal_plan_start: str,
    goal_plan_end: str,
    goal_setting_start: str | None = None,
    goal_setting_end: str | None = None,
    *, object_key: str | None = None,
) -> dict[str, Any]:
    """Resolve Goal Plan Goal Setting Info before generic access lookups.

    Date-bound add/edit/cancel/delete language belongs to
    ``RestrictGoalCreationFlag`` and ``RestrictGoalUpdateFlag``. It must not be
    routed through ``CanDelHRGoal``, which controls HR-assigned-goal actions and
    is not a Goal Setting Info field.
    """
    facts = list(statements)
    if any(isinstance(fact, Mapping) for fact in facts):
        if not all(isinstance(fact, Mapping) for fact in facts):
            return {"status": "clarification_required", "prompt": "Preserve object and semantic group for every fact."}
        relevant_facts = [fact for fact in facts if fact.get("semantic_group") == "goal_setting_info"
                          and (object_key is None or fact.get("object_key") == object_key)]
        identities = {fact.get("object_key") for fact in relevant_facts}
        if not relevant_facts or None in identities or len(identities) != 1:
            return {"status": "clarification_required", "prompt": "Select exactly one Goal Plan requirement group."}
        source_statements = [str(fact.get("statement", "")) for fact in relevant_facts]
    else:
        # Legacy callers supply an already normalized single-object group.
        source_statements = [str(statement) for statement in facts]
    anchored = any(mentions_goal_setting_info(statement) for statement in source_statements)
    if not anchored:
        return {"status": "not_requested"}

    # Extractors often split a logical table row across cells: one cell names
    # the Goal Setting period while another carries the worker restriction.
    # Once the group is anchored, correlate restriction-bearing siblings.
    restriction_terms = ("restrict", "cannot", "don't allow", "do not allow", "no goals", "must not")
    relevant = [
        statement
        for statement in source_statements
        if (mentions_goal_setting_info(statement)
            or any(term in " ".join(statement.casefold().split()) for term in restriction_terms))
        and not re.search(r"\b(?:all roles|hr specialist|manager)\b", statement.casefold())
    ]

    combined = " ".join(relevant)
    restriction = resolve_goal_setting_worker_restriction(combined)
    if restriction["status"] != "resolved":
        return {
            **restriction,
            "resolver": "goal_setting_info",
            "disallowed_generic_fields": ["CanDelHRGoal"],
        }

    dates = propose_goal_setting_dates(goal_plan_start, goal_plan_end, goal_setting_start, goal_setting_end)
    return {
        "status": "resolved" if dates["status"] == "source_supplied" else "confirmation_required",
        "resolver": "goal_setting_info",
        "applies_to": "workers_only",
        **{key: restriction[key] for key in ("RestrictGoalCreationFlag", "RestrictGoalUpdateFlag") if key in restriction},
        "GoalSettingStartDate": dates["GoalSettingStartDate"],
        "GoalSettingEndDate": dates["GoalSettingEndDate"],
        "proposed_fields": dates["proposed_fields"],
        "disallowed_generic_fields": ["CanDelHRGoal"],
    }


def propose_goal_setting_dates(
    goal_plan_start: str,
    goal_plan_end: str,
    goal_setting_start: str | None = None,
    goal_setting_end: str | None = None,
) -> dict[str, Any]:
    """Preserve supplied Goal Setting dates or propose missing plan boundaries.

    Proposed dates are review-only. They become configuration values only after
    the consultant confirms them.
    """
    try:
        plan_start, plan_end = date.fromisoformat(goal_plan_start), date.fromisoformat(goal_plan_end)
    except (TypeError, ValueError) as exc:
        raise FieldResolutionError("Goal Plan start and end dates must be ISO YYYY-MM-DD values") from exc
    if plan_start > plan_end:
        raise FieldResolutionError("Goal Plan start date must be on or before its end date")

    proposed_fields: list[str] = []
    start = goal_setting_start or goal_plan_start
    end = goal_setting_end or goal_plan_end
    if not goal_setting_start:
        proposed_fields.append("GoalSettingStartDate")
    if not goal_setting_end:
        proposed_fields.append("GoalSettingEndDate")
    try:
        setting_start, setting_end = date.fromisoformat(start), date.fromisoformat(end)
    except ValueError as exc:
        raise FieldResolutionError("Goal Setting dates must be ISO YYYY-MM-DD values") from exc
    if setting_start > setting_end:
        raise FieldResolutionError("Goal Setting start date must be on or before its end date")
    if setting_start < plan_start or setting_end > plan_end:
        raise FieldResolutionError("Goal Setting dates must be within the Goal Plan date range")

    return {
        "status": "confirmation_required" if proposed_fields else "source_supplied",
        "GoalSettingStartDate": start,
        "GoalSettingEndDate": end,
        "proposed_fields": proposed_fields,
        "applies_to": "workers_only",
    }
