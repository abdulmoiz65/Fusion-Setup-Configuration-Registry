"""Feedback SITE baseline and profile-provider handoff; never grants write access."""
from copy import deepcopy
from datetime import datetime, timezone

CODES = ("HRA_REQUEST_FEEDBACK_ENABLED", "ORA_HRA_REQ_FEEDBACK_REDWOOD_ENABLED")
KEY = "feedback_profile_prerequisites"
PROVIDER = "core.fusion-api.apps-common.profile-options"
SOURCE = "pillars/hcm/performance-management/requested-feedback-template/ora-resource/ora_request_feedback_profile_options.md"
BASE = "/fscmRestApi/resources/11.13.18.05/profileOptions/"


def profile_baseline(state, attested):
    record = state.get("feedback_profile_evidence", {})
    if not isinstance(record, dict):
        record = {}
    verified = (attested(record, state) and record.get("provider") == PROVIDER
                and record.get("level") == "SITE"
                and isinstance(record.get("verification_reference"), str)
                and bool(record["verification_reference"].strip()))
    values = record.get("values", {}) if isinstance(record, dict) else {}
    if not isinstance(values, dict):
        values = {}
    verified = bool(verified and all(isinstance(values.get(code), str) and values[code].strip() for code in CODES))
    satisfied = verified and all(values[code] == "Y" for code in CODES)
    return {"verified": verified, "satisfied": satisfied,
            "current_values": {code: values.get(code) if verified else None for code in CODES},
            "evidence": record if verified else {}, "provider": PROVIDER,
            "user_action_required": False, "template_post_capability_proven": False,
            "template_privilege_proven": False}


def prerequisite(state, attested):
    baseline = profile_baseline(state, attested)
    bound = KEY in state.get("runbook", {}).get("bindings", {})
    if baseline["satisfied"] and not bound:
        return None
    return {"key": KEY, "name": "Manage Administrator Profile Values",
            "owner_skill_id": PROVIDER, "execution_route": "profile-provider",
            "source_reference": SOURCE, "required_by": ["feedback"],
            "disposition": "completed" if baseline["satisfied"] else "configure",
            "evidence": baseline["evidence"] if baseline["satisfied"] else {},
            "catalog_identity": {"task_code": "FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES",
                                 "task_name": "Manage Administrator Profile Values",
                                 "offering": "Performance Management", "functional_area": "Performance Management Common"},
            "requirements": {"level": "SITE", "desired_values": {code: "Y" for code in CODES},
                             "current_values": baseline["current_values"], "evidence": baseline["evidence"],
                             "read_before_preview": True, "mutate_only_non_y": True,
                             "exact_write_approval_required": True, "readback_required": True,
                             "read_handoff": [{"profile_code": code, "method": "GET",
                                               "definition_path": BASE + code,
                                               "site_path": BASE + code + "/child/siteProfileOptionValues"}
                                              for code in CODES]}}


def refresh_profiles(state, client, reference):
    """Consume the declared provider's authenticated client; GETs only.

    Invocation is an execution step, not intake. Client must enforce configured
    host identity and the routed authentication policy. No token/login logic here.
    """
    if state.get("run_status") in ("stopped", "paused", "abandoned"):
        raise ValueError("Stopped run cannot refresh tenant profile evidence")
    if not isinstance(reference, str) or not reference.strip():
        raise ValueError("Provider verification reference is required")
    values = {}
    for code in CODES:
        definition = client.request("GET", BASE + code)
        if not isinstance(definition, dict) or definition.get("ProfileOptionName") != code:
            raise ValueError("Profile definition identity mismatch")
        page = client.request("GET", BASE + code + "/child/siteProfileOptionValues")
        if not isinstance(page, dict) or not isinstance(page.get("items"), list) or page.get("hasMore") is not False:
            raise ValueError("SITE profile read incomplete")
        rows = page["items"]
        if len(rows) > 1 or any(not isinstance(row, dict) or "ProfileOptionValue" not in row for row in rows):
            raise ValueError("SITE profile value ambiguous or not returned")
        values[code] = rows[0]["ProfileOptionValue"] if rows else "absent"
    result = deepcopy(state)
    result["feedback_profile_evidence"] = {
        **{key: state[key] for key in ("project_id", "environment", "configuration_revision")},
        "actor": "profile-provider", "provider": PROVIDER, "level": "SITE", "values": values,
        "reference": reference, "verification_reference": reference,
        "recorded_at": datetime.now(timezone.utc).isoformat()}
    return result


class ProfileReadClient:
    """Declared profile provider's core transport, cached authentication only."""
    def __init__(self, base_url):
        import sys
        from pathlib import Path
        root = Path(__file__).resolve().parents[5]
        sys.path.insert(0, str(root / "core/fusion-api/rest-api-client/scripts"))
        import rest_client_common as core
        import fusion_auth
        self.core = core
        self.props = core.read_properties(core.DEFAULT_PROPERTIES_PATH)
        if self.props.get("restBaseUrl", "").rstrip("/") != base_url.rstrip("/"):
            raise ValueError("Configured Fusion environment differs from requested target")
        self.token = fusion_auth.load_cached_access_token(self.props, root / ".fusionaim_token.json")
        if not self.token:
            raise ValueError("Authentication handoff required through the routed Chrome session")

    def request(self, method, path):
        import json
        if method != "GET" or not any(path in (BASE + code, BASE + code + "/child/siteProfileOptionValues") for code in CODES):
            raise ValueError("Profile baseline adapter permits exact declared GETs only")
        raw, _, status = self.core.request_bytes(
            self.props, self.core.build_url(self.props, path, {}), method="GET",
            access_token=self.token, headers={"REST-Framework-Version": "9"}, timeout=60)
        if not 200 <= status < 300:
            raise ValueError("Profile provider GET failed; HTTP " + str(status))
        return json.loads(raw)


def main():
    import argparse
    import json
    from pathlib import Path
    from touchpoints_workflow import evaluate
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--dry-run", action="store_true")
    modes.add_argument("--live-read", action="store_true", help="Declared profile-provider GET execution step; no writes")
    parser.add_argument("--base-url", help="Must equal state environment and configured Fusion host")
    parser.add_argument("--reference", help="Provider read evidence reference")
    args = parser.parse_args()
    try:
        state = json.loads(args.input.read_text())
        plan = evaluate(state)
        if "feedback" not in plan["scope"]["selected_tasks"]:
            raise ValueError("Feedback is outside selected scope")
        if args.live_read:
            if state.get("run_status") in ("stopped", "paused", "abandoned"):
                raise ValueError("Stopped run cannot access tenant")
            if not args.base_url or state["environment"].rstrip("/") != args.base_url.rstrip("/"):
                raise ValueError("Profile read requires exact state environment URL")
            if not args.reference:
                raise ValueError("Provider verification reference is required")
            state = refresh_profiles(state, ProfileReadClient(args.base_url), args.reference)
            plan = evaluate(state)
        print(json.dumps({"state": state, "plan": plan, "external_writes": False}, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError):
        print(json.dumps({"status": "technical_failure", "user_action_required": False,
                          "message": "Profile baseline check failed; reconcile provider identity, authentication and read evidence"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
