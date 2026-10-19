"""Business duplicate identity, independent of transport and Fusion key constraints."""

FIELDS = {
    "PERFORMANCE": ("GoalName",),
    "DEVELOPMENT": ("GoalName",),
    "review_period": ("ReviewPeriodName",),
    "goal_plan": ("GoalPlanName", "ReviewPeriodName"),
}
LIBRARY_GOAL_KINDS = {"PERFORMANCE", "DEVELOPMENT"}


def _normalized(value):
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized or None


def identity(row, kind):
    """Return the Fusion business duplicate key; dates are not key fields."""
    name = FIELDS[kind][0]
    if not isinstance(row.get(name), str) or not row[name].strip():
        raise ValueError("Missing name")
    if kind in LIBRARY_GOAL_KINDS:
        return (kind, row[name].strip())
    if kind == "review_period":
        return (kind, row[name].strip())
    if kind == "goal_plan":
        period_id = _normalized(row.get("ReviewPeriodId"))
        if period_id is not None:
            return (kind, row[name].strip(), "id", period_id)
        period_name = row.get("ReviewPeriodName")
        if isinstance(period_name, str) and period_name.strip():
            return (kind, row[name].strip(), "name", period_name.strip())
        raise ValueError("Missing associated Review Period")
    raise ValueError("Unsupported duplicate identity kind")


def compare_goal_plan_review_period(expected, candidate):
    """Return match, different, or unresolved for two associated Review Periods."""
    for field in ("ReviewPeriodId", "ReviewPeriodName"):
        left, right = _normalized(expected.get(field)), _normalized(candidate.get(field))
        if left is None or right is None:
            continue
        return "match" if left == right else "different"
    return "unresolved"


def assess_duplicates(expected, rows, *, kind, pagination_complete, environment,
                      expected_environment):
    if pagination_complete is not True or not environment or environment != expected_environment:
        return {"status": "unresolved", "reason": "Incomplete pagination or environment evidence"}
    try:
        key = identity(expected, kind)
    except (ValueError, TypeError):
        return {"status": "unresolved", "reason": "Expected identity is incomplete"}
    matches, unresolved = [], False
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get(FIELDS[kind][0]), str):
            unresolved = True
            continue
        if row[FIELDS[kind][0]].strip() != key[1]:
            continue
        if kind in LIBRARY_GOAL_KINDS:
            if row.get("TypeCode") not in ("PERFORMANCE", "DEVELOPMENT"):
                unresolved = True
                continue
            if row["TypeCode"] != kind:
                continue
        if kind == "goal_plan":
            comparison = compare_goal_plan_review_period(expected, row)
            if comparison == "match":
                matches.append(row)
            elif comparison == "unresolved":
                unresolved = True
            continue
        try:
            if identity(row, kind) == key:
                matches.append(row)
        except (ValueError, TypeError):
            unresolved = True
    return {"status": "unresolved" if unresolved else "duplicate" if matches else "clear",
            "count": len(matches), "can_skip_create": False,
            "requires_item_verification": bool(matches) or unresolved}


def validate_incoming(rows, kind):
    if kind == "goal_plan":
        validated = []
        for row in rows:
            identity(row, kind)
            for previous in validated:
                if row["GoalPlanName"].strip() != previous["GoalPlanName"].strip():
                    continue
                comparison = compare_goal_plan_review_period(previous, row)
                if comparison == "match":
                    raise ValueError(
                        "DUPLICATE_BUSINESS_IDENTITY: Goal Plan name and associated Review Period match"
                    )
                if comparison == "unresolved":
                    raise ValueError(
                        "UNRESOLVED_BUSINESS_IDENTITY: Goal Plan rows have no comparable associated Review Period"
                    )
            validated.append(row)
        return
    seen = set()
    for row in rows:
        key = identity(row, kind)
        if key in seen:
            if kind in LIBRARY_GOAL_KINDS:
                rule = "name and type match"
            elif kind == "review_period":
                rule = "Review Period name matches"
            else:
                rule = "Goal Plan name and associated Review Period match"
            raise ValueError("DUPLICATE_BUSINESS_IDENTITY: " + rule)
        seen.add(key)
