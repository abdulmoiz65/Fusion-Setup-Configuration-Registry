"""Deterministic task identities, dependency order and execution checkpoints.

This module plans owner handoffs. It never authorizes or performs a Fusion write.
"""
from __future__ import annotations
from touchpoints_feedback_profiles import KEY as FEEDBACK_PROFILES, prerequisite, profile_baseline

BUILTINS = ("profiles", "checkins", "feedback", "surveys", "nudges", "readiness", "full", "daily")
ROUTES = {"profiles": "profile-provider", "checkins": "data-loader", "feedback": "rest",
          "surveys": "manual-ui", "nudges": "manual-ui", "readiness": "confirmation",
          "full": "ess", "daily": "ess"}
IDENTITIES = {
    "checkins": ("ORA_MANAGE_CHECK_IN_TEMPLATES", "Check-In Templates", "Performance Management", "Check-in Template"),
    "feedback": ("ORA_HRA_FEEDBACK_TEMPLATES", "Feedback Templates", "Performance Management", "Requested Feedback Template"),
    "full": ("CUSTOM_AGGREGATE_ORACLE_TOUCHPOINTS_DATA", "Aggregate Oracle Touchpoints Data", "HCM Tool", "Touchpoints Aggregate Data Process"),
}
OWNERS = {
    "profiles": "core.fusion-api.apps-common.profile-options",
    "checkins": "hcm.performance-management.check-in-template.check-in-templates",
    "feedback": "hcm.performance-management.requested-feedback-template.feedback-templates",
    "full": "hcm.hcm-tool.touchpoints-aggregate-data-process.aggregate-oracle-touchpoints-data",
    "daily": "hcm.hcm-tool.touchpoints-aggregate-data-process.aggregate-oracle-touchpoints-data",
}
ROUTE_VALUES = {"profile-provider", "data-loader", "rest", "manual-ui"}


def dependent_tasks(state):
    """Accept source-backed owner prerequisites; never infer unrelated setup."""
    values = state.get("dependent_tasks", [])
    if not isinstance(values, list):
        raise ValueError("dependent_tasks must be an array")
    result = {}
    for row in values:
        if not isinstance(row, dict):
            raise ValueError("Dependent task must be an object")
        key = row.get("key")
        if not isinstance(key, str) or not key or key in BUILTINS or key in result:
            raise ValueError("Dependent task keys must be unique and distinct from baseline tasks")
        for field in ("name", "owner_skill_id", "source_reference"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ValueError(f"{key}: {field} is required")
        if row.get("execution_route") not in ROUTE_VALUES:
            raise ValueError(f"{key}: unsupported owner execution route")
        for field in ("required_by", "depends_on"):
            links = row.get(field, [])
            if not isinstance(links, list) or any(not isinstance(x, str) or not x for x in links) or len(set(links)) != len(links):
                raise ValueError(f"{key}: {field} must contain distinct task keys")
        if not row.get("required_by"):
            raise ValueError(f"{key}: an actual consuming task is required")
        result[key] = dict(row)
    known = set(BUILTINS) | set(result)
    for key, row in result.items():
        if any(x not in known or x == key for x in row.get("required_by", []) + row.get("depends_on", [])):
            raise ValueError(f"{key}: unknown or self dependency")
    return result


def ordered_tasks(rows):
    """Stable topological order: profiles first, configuration, then ESS tail."""
    by_key = {r["key"]: r for r in rows}
    if len(by_key) != len(rows):
        raise ValueError("Duplicate plan task keys")
    order, done = [], set()
    def rank(key):
        row = by_key[key]
        if row["execution_route"] == "profile-provider":
            return (0, 0 if key == "profiles" else 1, key)
        if key == "readiness":
            return (2, key)
        if row["execution_route"] == "ess":
            return (3, BUILTINS.index(key))
        return (1, BUILTINS.index(key) if key in BUILTINS else -1, key)
    while len(order) < len(rows):
        available = [k for k, r in by_key.items() if k not in done and set(r["depends_on"]) <= done]
        if not available:
            raise ValueError("Task dependency cycle or missing prerequisite")
        key = min(available, key=rank)
        order.append(by_key[key]); done.add(key)
    return order


def enrich_plan(plan, state, attested):
    """One plan drives row presentation, provisioning and owner handoffs."""
    extras = dependent_tasks(state)
    selected = {r["key"] for r in plan["tasks"]}
    if "feedback" in selected:
        plan["feedback_profile_baseline"] = profile_baseline(state, attested)
        automatic = prerequisite(state, attested)
        if FEEDBACK_PROFILES in extras:
            raise ValueError("Feedback profile prerequisite is automatic; do not supply a duplicate task")
        if automatic:
            extras[FEEDBACK_PROFILES] = automatic
    needed = set()
    while True:
        added = {k for k, r in extras.items() if set(r["required_by"]) & (selected | needed)}
        added |= {x for k in needed for x in extras[k].get("depends_on", []) if x in extras}
        if added <= needed:
            break
        needed |= added
    rows = [dict(row) for row in plan["tasks"]]
    for key in sorted(needed):
        source = extras[key]
        disposition = source.get("disposition", "configure")
        if disposition not in ("configure", "completed", "not_applicable"):
            raise ValueError(f"{key}: unsupported prerequisite disposition")
        evidence = source.get("evidence", {})
        resolved = attested(evidence, state) and (
            disposition == "completed" and bool(evidence.get("verification_reference"))
            or disposition == "not_applicable" and bool(evidence.get("reason")))
        missing = source.get("missing_inputs", [])
        if not isinstance(missing, list) or any(not isinstance(x, str) or not x.strip() for x in missing):
            raise ValueError(f"{key}: invalid missing business inputs")
        rows.append({**source, "disposition": disposition, "resolved": bool(resolved),
                     "status": "Completed — verified" if resolved and disposition == "completed" else
                               "Not Applicable — user confirmed" if resolved else "Pending configuration",
                     "proposed_runbook_status": "completed" if resolved and disposition == "completed" else
                                                "not-applicable" if resolved else "open",
                     "missing_inputs": missing, "delegate_configuration": not resolved and not missing})
    included = {r["key"] for r in rows}
    for row in rows:
        key = row["key"]
        row["execution_route"] = ROUTES.get(key, row.get("execution_route"))
        row["owner_skill_id"] = OWNERS.get(key, row.get("owner_skill_id"))
        if key in IDENTITIES:
            code, name, offering, area = IDENTITIES[key]
            row["catalog_identity"] = {"task_code": code, "task_name": name, "offering": offering, "functional_area": area}
        edges = set(row.get("depends_on", []))
        edges |= {k for k in needed if key in extras[k]["required_by"]}
        if any(x not in included for x in edges):
            raise ValueError(f"{key}: selected prerequisite requires an absent task; resolve scope explicitly")
        if row["execution_route"] not in ("profile-provider",) and key not in ("full", "daily", "readiness"):
            edges |= {r["key"] for r in rows if r["key"] != FEEDBACK_PROFILES
                      and ROUTES.get(r["key"], r.get("execution_route")) == "profile-provider"}
        if key in ("readiness", "full"):
            edges |= {r["key"] for r in rows if r["key"] not in ("readiness", "full", "daily")}
            if key == "full" and "readiness" in included:
                edges.add("readiness")
        if key == "daily":
            edges |= included - {"daily"}
        row["depends_on"] = sorted(edges)
    plan["tasks"] = ordered_tasks(rows)
    config = [r for r in rows if r["key"] not in ("readiness", "full", "daily")]
    ready = all(r.get("resolved") for r in config)
    plan["configuration_resolved"] = ready
    plan["full_ready_for_preview"] &= ready
    plan["daily_ready_for_preview"] &= ready
    plan["standalone_ready_for_preview"] &= ready
    plan["prerequisite_tasks"] = sorted(needed)
    plan["creation_tasks"] = [
        {"key": row["key"], "catalog_identity": row["catalog_identity"],
         "execution_route": row["execution_route"], "sequence": index + 1,
         "task_type": "ORA_CHK_DATA_LOADER" if row["execution_route"] in ("data-loader", "ess") else "ORA_CHK_MANUAL"}
        for index, row in enumerate(plan["tasks"]) if row.get("catalog_identity")
    ]
    plan["manual_tracking_tasks"] = [row["key"] for row in plan["tasks"] if not row.get("catalog_identity")]
    if not ready and plan["scope"]["mode"] == "implementation":
        for row in plan["tasks"]:
            if row["key"] == "readiness": row["status"] = "Blocked — configuration unresolved"
            elif row["key"] == "full": row["status"] = "Blocked — readiness not confirmed"
            elif row["key"] == "daily": row["status"] = "Blocked — awaiting configuration and verified Full success"
    return plan


def classify_issue(issue):
    """Technical evidence is agent-owned; only business/approval gates ask users."""
    kind = issue.get("kind")
    if kind == "business_input":
        return {"state": "awaiting_business_input", "user_action_required": True}
    if kind == "write_approval":
        return {"state": "awaiting_write_approval", "user_action_required": True}
    if kind == "governance" and issue.get("explicit_policy_reference"):
        return {"state": "awaiting_business_input", "user_action_required": True}
    if kind == "unsupported_route":
        return {"state": "unsupported_route", "user_action_required": False}
    return {"state": "technical_failure", "user_action_required": False,
            "repair_action": "resolve_declared_owner_evidence" if kind in ("route_capability", "privileges") else "reconcile_local_context" if kind == "task_context" else "inspect_owner_diagnostic"}


def execution_checkpoints(plan, state):
    """Select next owner work without treating a preview as write authorization."""
    outcomes = state.get("task_outcomes", {})
    if not isinstance(outcomes, dict):
        raise ValueError("task_outcomes must be an object")
    rows, completed = [], set()
    for task in plan["tasks"]:
        key = task["key"]
        resolved = task.get("resolved", False)
        if key == "readiness": resolved = plan["full_ready_for_preview"]
        if key == "full": resolved = task.get("status") == "Succeeded"
        if key == "daily": resolved = task.get("status") == "Schedule configured and verified"
        checkpoint = {"key": key, "owner_skill_id": task.get("owner_skill_id"),
                      "execution_route": task["execution_route"], "write_authorized": False,
                      "user_action_required": False}
        result = outcomes.get(key, {})
        if not isinstance(result, dict): raise ValueError(f"{key}: invalid task outcome")
        if resolved:
            checkpoint["state"] = "not_applicable" if task.get("disposition") == "not_applicable" else "completed"
            completed.add(key)
        elif set(task["depends_on"]) - completed:
            checkpoint.update(state="awaiting_dependencies", waiting_for=sorted(set(task["depends_on"]) - completed))
        elif task.get("missing_inputs") or task.get("disposition") == "unknown":
            checkpoint.update(state="awaiting_business_input", user_action_required=True)
        elif result.get("issue"):
            if not isinstance(result["issue"], dict): raise ValueError(f"{key}: invalid owner issue")
            checkpoint.update(classify_issue(result["issue"]))
        elif key == "readiness":
            checkpoint.update(state="awaiting_business_input", user_action_required=True)
        elif key == "daily" and not plan["daily_ready_for_preview"]:
            checkpoint.update(state="awaiting_dependencies", waiting_for=["verified_full_success"])
        else:
            checkpoint["state"] = "ready"
        rows.append(checkpoint)
    runnable = [r["key"] for r in rows if r["state"] == "ready"]
    stopped = state.get("run_status") in ("stopped", "paused", "abandoned")
    if stopped or not plan.get("runbook_complete") or state.get("pending_operation"):
        runnable = []
    return {"checkpoints": rows, "next_task": runnable[0] if runnable else None,
            "independent_ready_tasks": runnable, "execution_authorized": False,
            "run_state": "stopped" if stopped else "reconcile_runbook" if not plan.get("runbook_complete") else "ready" if runnable else "awaiting_checkpoint"}
