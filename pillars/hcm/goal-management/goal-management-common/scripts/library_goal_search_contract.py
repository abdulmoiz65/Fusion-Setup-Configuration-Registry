"""Pure Library Goal search contract; transport and pagination remain core-owned."""
from __future__ import annotations

from typing import Any
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from duplicate_identity import assess_duplicates


def build_search_payload(*, query: str = "", status_code: str | None = None,
                         limit: int = 25, offset: int = 0,
                         supported_filter_fields=()) -> dict[str, Any]:
    if type(limit) is not int or limit < 1 or type(offset) is not int or offset < 0:
        raise ValueError("limit must be positive and offset nonnegative integers")
    if not isinstance(query, str):
        raise ValueError("query must be text")
    filters = []
    if status_code is not None:
        if "StatusCode" not in supported_filter_fields or not isinstance(status_code, str) or not status_code:
            raise ValueError("StatusCode filter requires current action-field evidence")
        filters.append({"StatusCode": [status_code]})
    # TypeCode is not an advertised filter. Hydrate and discriminate candidates
    # locally; resource attributes alone do not establish action filter support.
    return {"query": query, "searchFields": ["GoalName"], "filters": filters,
            "displayFields": ["GoalId", "GoalName", "TypeMeaning", "StatusMeaning",
                              "AvailableTo", "LastUpdateDate"],
            "sort": [{"name": "LastUpdateDate", "direction": "desc"}],
            "limit": limit, "offset": offset}


def assess_duplicate_evidence(*, rows: list[dict], goal_name: str, variant: str,
                              pagination_complete: bool, environment: str,
                              expected_environment: str, type_meanings: dict[str, str] | None = None,
                              start_date: str | None = None, end_date: str | None = None) -> dict:
    """Consume complete, core-normalized search results, not a search count."""
    if variant not in {"PERFORMANCE", "DEVELOPMENT"}:
        raise ValueError("unsupported Library Goal variant")
    if not environment or environment != expected_environment or pagination_complete is not True:
        return {"status": "unresolved", "reason": "environment or pagination evidence incomplete"}
    matches = []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("GoalName"), str):
            return {"status": "unresolved", "reason": "malformed candidate"}
        if row["GoalName"] != goal_name:
            continue
        code = row.get("TypeCode") or (type_meanings or {}).get(row.get("TypeMeaning"))
        if code not in {"PERFORMANCE", "DEVELOPMENT"}:
            return {"status": "unresolved", "reason": "hydrate candidate type before duplicate decision"}
        if code == variant:
            matches.append(row)
    return assess_duplicates(
        {"GoalName": goal_name, "StartDate": start_date, "TargetCompletionDate": end_date},
        [dict(row, TypeCode=variant) for row in matches], kind=variant,
        pagination_complete=pagination_complete, environment=environment,
        expected_environment=expected_environment)
