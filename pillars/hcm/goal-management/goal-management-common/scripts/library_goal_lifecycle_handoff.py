"""Validate the lifecycle follow-up record before a Library Goal task handoff.

This is a local, read-only guard. It does not authorize or perform activation.
"""

import argparse
import json
from pathlib import Path


def validate_handoff(record):
    if record.get("source_status_intent") not in {"omitted", "active", "inactive"}:
        raise ValueError("source_status_intent must be omitted, active, or inactive")
    goals = record.get("verified_creates")
    if not isinstance(goals, list) or not goals:
        raise ValueError("verified_creates must contain at least one newly created goal")
    expected_type = record.get("type_code")
    if expected_type not in {"PERFORMANCE", "DEVELOPMENT"}:
        raise ValueError("type_code must be PERFORMANCE or DEVELOPMENT")
    identities = set()
    for goal in goals:
        if goal.get("TypeCode") != expected_type:
            raise ValueError("verified goal type does not match the task")
        if goal.get("StatusCode") not in {"I", "A"}:
            raise ValueError("each created goal needs a verified lifecycle status")
        if goal.get("verification_result") != "passed" or not goal.get("created_in_this_run"):
            raise ValueError("only verified successful creates from this run are eligible")
        if not goal.get("GoalName") or not goal.get("verification_ref"):
            raise ValueError("goal name and verification evidence are required")
        identity = (goal["TypeCode"], goal["GoalName"])
        if identity in identities:
            raise ValueError("duplicate exact goal identity")
        identities.add(identity)

    inactive = [goal for goal in goals if goal["StatusCode"] == "I"]
    intent = record["source_status_intent"]
    required_active = intent == "active" or bool(record.get("downstream_requires_active"))
    if intent == "inactive" and record.get("downstream_requires_active"):
        raise ValueError("explicit inactive intent conflicts with active dependency")
    if inactive and intent == "omitted":
        if record.get("activation_choice") not in {"pending", "activate", "retain_inactive"}:
            raise ValueError("omitted status requires an explicit activation-choice record")
        if not record.get("handoff_choice_text"):
            raise ValueError("handoff must offer activation or retaining inactive")
        if record["activation_choice"] == "pending" and not all(
            term in record["handoff_choice_text"].lower() for term in ("activate", "inactive")
        ):
            raise ValueError("pending choice must present both lifecycle options")
    if required_active and inactive and record.get("activation_choice") == "retain_inactive":
        raise ValueError("required active outcome cannot be retained inactive")
    unresolved_optional_choice = bool(
        inactive and intent == "omitted"
        and record.get("activation_choice") != "retain_inactive"
    )
    return {
        "creation_complete": True,
        "lifecycle_ready": not (required_active and inactive or unresolved_optional_choice),
        "activation_follow_up": unresolved_optional_choice,
        "verified_goal_count": len(goals),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path, help="Persisted task lifecycle follow-up JSON")
    args = parser.parse_args()
    result = validate_handoff(json.loads(args.record.read_text(encoding="utf-8")))
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
