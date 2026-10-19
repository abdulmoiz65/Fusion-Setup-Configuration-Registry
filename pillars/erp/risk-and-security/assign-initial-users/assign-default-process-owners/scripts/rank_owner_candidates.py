#!/usr/bin/env python3
"""Rank verified default-owner candidates from Core-returned evidence.

This helper is deliberately local-only.  It does not make Fusion, BOSS, SCIM,
OAuth, HTTP, or Core-client calls.  Candidate evidence is restricted input from
the completed Core-result bundle; its output is an internal decision record.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


FIT_SCORES = {
    "direct_responsibility": 5,
    "functional_department": 4,
    "job_or_position": 3,
    "organizational_context": 2,
    "business_unit_context": 1,
    "none": 0,
}


@dataclass(frozen=True)
class Candidate:
    username: str
    owner_code: str
    function_match: str
    active: bool | None
    effective: bool | None
    manager_level: int | None
    direct_report_count: int | None
    represented_assignments: int
    job_name: str | None
    department_name: str | None
    position_name: str | None
    manager_name: str | None
    evidence: str | None

    @property
    def fit_score(self) -> int:
        return FIT_SCORES[self.function_match]

    @property
    def fit_rating(self) -> str:
        if self.fit_score >= 4:
            return "High"
        if self.fit_score >= 2:
            return "Medium"
        return "Low"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def optional_bool(value: Any, field: str) -> bool | None:
    if value is None:
        return None
    if not isinstance(value, bool):
        raise ValueError(f"{field} must be true, false, or omitted")
    return value


def optional_nonnegative_int(value: Any, field: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field} must be a non-negative integer or omitted")
    return value


def optional_positive_int(value: Any, field: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field} must be a positive integer or omitted")
    return value


def optional_text(value: Any, field: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string or omitted")
    return value.strip()


def required_text(value: Any, field: str) -> str:
    text = optional_text(value, field)
    if text is None:
        raise ValueError(f"{field} is required")
    return text


def parse_candidate(row: Any, index: int) -> Candidate:
    if not isinstance(row, dict):
        raise ValueError(f"candidates[{index}] must be an object")
    function_match = row.get("function_match")
    if function_match is None and row.get("manager_level") is not None:
        # A resolved reporting relationship is evidence of organizational context,
        # not a claimed functional match.
        function_match = "organizational_context"
    if function_match is None:
        function_match = "none"
    if function_match not in FIT_SCORES:
        raise ValueError(f"candidates[{index}].function_match is unsupported")
    return Candidate(
        username=required_text(row.get("username"), f"candidates[{index}].username"),
        owner_code=required_text(row.get("owner_code"), f"candidates[{index}].owner_code"),
        function_match=function_match,
        active=optional_bool(row.get("active"), f"candidates[{index}].active"),
        effective=optional_bool(row.get("effective"), f"candidates[{index}].effective"),
        manager_level=optional_positive_int(row.get("manager_level"), f"candidates[{index}].manager_level"),
        direct_report_count=optional_nonnegative_int(row.get("direct_report_count"), f"candidates[{index}].direct_report_count"),
        represented_assignments=optional_nonnegative_int(row.get("represented_assignments"), f"candidates[{index}].represented_assignments") or 0,
        job_name=optional_text(row.get("job_name"), f"candidates[{index}].job_name"),
        department_name=optional_text(row.get("department_name"), f"candidates[{index}].department_name"),
        position_name=optional_text(row.get("position_name"), f"candidates[{index}].position_name"),
        manager_name=optional_text(row.get("manager_name"), f"candidates[{index}].manager_name"),
        evidence=optional_text(row.get("evidence"), f"candidates[{index}].evidence"),
    )


def eligibility(candidate: Candidate) -> bool:
    """Exclude only explicitly inactive or ineffective candidates.

    Absent HCM fields are unknown, not a reason to remove a verified user.
    """
    return candidate.active is not False and candidate.effective is not False


def sort_key(candidate: Candidate) -> tuple[int, int, int, int, int, int, str]:
    return (
        -candidate.fit_score,
        -(candidate.active is True),
        -(candidate.effective is True),
        candidate.manager_level if candidate.manager_level is not None else 10**9,
        -(candidate.direct_report_count if candidate.direct_report_count is not None else -1),
        -candidate.represented_assignments,
        candidate.username.casefold(),
    )


def confidence(candidates: list[Candidate]) -> str:
    if not candidates:
        return "Low"
    top = candidates[0]
    same_tier = sum(candidate.fit_score == top.fit_score for candidate in candidates) > 1
    if same_tier:
        return "Low"
    if top.fit_score >= 4 and top.active is True and top.effective is not False:
        return "High"
    if top.fit_score >= 2:
        return "Medium"
    return "Low"


def reason(candidate: Candidate) -> str:
    labels = {
        "direct_responsibility": "Direct responsibility supports this process",
        "functional_department": "The candidate leads the matching functional department",
        "job_or_position": "The candidate's job or position supports the process function",
        "organizational_context": "The candidate is supported by the verified reporting relationship",
        "business_unit_context": "The candidate is supported by the Business Unit context",
        "none": "Only a verified user identity is available",
    }
    return candidate.evidence or labels[candidate.function_match]


def candidate_record(candidate: Candidate, status: str) -> dict[str, Any]:
    return {
        "username": candidate.username,
        "owner_code": candidate.owner_code,
        "job_name": candidate.job_name,
        "department_name": candidate.department_name,
        "position_name": candidate.position_name,
        "manager_name": candidate.manager_name,
        "fit_rating": candidate.fit_rating,
        "function_match": candidate.function_match,
        "reason": reason(candidate),
        "recommendation_status": status,
    }


def rank_process(process: Any) -> dict[str, Any]:
    if not isinstance(process, dict):
        raise ValueError("processes entries must be objects")
    process_name = required_text(process.get("process_name"), "process_name")
    raw_candidates = process.get("candidates")
    if not isinstance(raw_candidates, list):
        raise ValueError(f"{process_name}.candidates must be an array")
    parsed = [parse_candidate(row, index) for index, row in enumerate(raw_candidates)]
    eligible = sorted((candidate for candidate in parsed if eligibility(candidate)), key=sort_key)
    if not eligible:
        return {
            "process_name": process_name,
            "recommendation_status": "NoCandidate",
            "confidence": "Low",
            "requires_consultant_selection": False,
            "candidates": [],
        }
    top_score = eligible[0].fit_score
    leading = [candidate for candidate in eligible if candidate.fit_score == top_score]
    requires_selection = len(leading) > 1
    records = [candidate_record(candidate, "Candidate") for candidate in eligible]
    records[0]["recommendation_status"] = "TopCandidate" if not requires_selection else "EquivalentCandidate"
    if requires_selection:
        for record in records[1:len(leading)]:
            record["recommendation_status"] = "EquivalentCandidate"
    elif len(records) > 1:
        records[1]["recommendation_status"] = "Alternate"
    return {
        "process_name": process_name,
        "recommendation_status": "ConsultantSelectionRequired" if requires_selection else "TopCandidate",
        "confidence": confidence(eligible),
        "requires_consultant_selection": requires_selection,
        "candidates": records,
    }


def rank_candidates(document: dict[str, Any]) -> dict[str, Any]:
    processes = document.get("processes")
    if not isinstance(processes, list) or not processes:
        raise ValueError("processes must be a non-empty array")
    return {"recommendations": [rank_process(process) for process in processes]}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-evidence", required=True, help="Restricted candidate evidence JSON assembled from completed Core results.")
    parser.add_argument("--decision-record-output", required=True, help="Restricted internal decision-record output path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    write_json(Path(args.decision_record_output), rank_candidates(read_json(Path(args.candidate_evidence))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
