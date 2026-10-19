"""Transport-neutral business constraints; no tenant access or guessed field mappings."""
from datetime import date


def validate_goal_plan_rules(values, *, review_period=None):
    def parsed(value):
        if not isinstance(value, str):
            raise ValueError("Dates must be ISO YYYY-MM-DD strings")
        return date.fromisoformat(value)

    start, end = parsed(values["StartDate"]), parsed(values["EndDate"])
    if start > end:
        raise ValueError("Goal Plan start date must not exceed end date")
    if review_period:
        if not parsed(review_period["StartDate"]) <= start <= end <= parsed(review_period["EndDate"]):
            raise ValueError("Goal Plan dates must be within the resolved Review Period")
    minimum, maximum = (values.get(k) for k in ("MinimumGoalsNumberInGoalPlan", "MaximumGoalsNumberInGoalPlan"))
    for key, number in (("Minimum", minimum), ("Maximum", maximum)):
        if number is not None and (isinstance(number, bool) or not isinstance(number, int) or number < (0 if key == "Minimum" else 1)):
            raise ValueError(f"{key} goals must be a valid integer")
    if minimum is not None and maximum is not None and minimum > maximum:
        raise ValueError("Minimum goals cannot exceed maximum goals")
    if values.get("EnforceMaximumGoalsInGpFlag") is True and maximum is None:
        raise ValueError("Maximum enforcement requires a maximum")
    if values.get("EnforceGoalWeightFlag") is True and values.get("EnableWeightingFlag") is not True:
        raise ValueError("100-percent weight enforcement requires weighting enabled")
    for key in ("PrimaryGoalPlanFlag", "EnforceMaximumGoalsInGpFlag", "EnableWeightingFlag", "EnforceGoalWeightFlag",
                "RestrictGoalCreationFlag", "RestrictGoalUpdateFlag"):
        if values.get(key) is not None and not isinstance(values[key], bool):
            raise ValueError(f"{key} must be boolean or omitted")
    validate_goal_setting_rules(values)


def validate_goal_setting_rules(values):
    has_start = values.get("GoalSettingStartDate") not in (None, "")
    has_end = values.get("GoalSettingEndDate") not in (None, "")
    if has_start != has_end:
        raise ValueError("Goal Setting dates must be supplied together")
    if any(values.get(k) is True for k in ("RestrictGoalCreationFlag", "RestrictGoalUpdateFlag")) and not has_start:
        raise ValueError("worker Goal Setting restrictions require start and end dates")
    if not has_start:
        return
    try:
        start, end, plan_start, plan_end = [date.fromisoformat(values[key]) for key in
            ("GoalSettingStartDate", "GoalSettingEndDate", "StartDate", "EndDate")]
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Goal Setting and Goal Plan dates must be ISO YYYY-MM-DD values") from exc
    if start > end:
        raise ValueError("Goal Setting start date must be on or before its end date")
    if not plan_start <= start <= end <= plan_end:
        raise ValueError("Goal Setting dates must be within the Goal Plan date range")


def validate_library_goal_rules(values, variant):
    for key in ("GoalName", "TypeCode", "StatusCode", "Visible"):
        if not isinstance(values.get(key), str) or not values[key].strip():
            raise ValueError(f"{key} must be nonblank")
    if values["TypeCode"] != variant:
        raise ValueError("Library Goal variant mismatch")
    if values["StatusCode"] not in {"I", "A"}:
        raise ValueError("Library Goal status must be I or A")
    if "StartDate" in values:
        date.fromisoformat(values["StartDate"])
