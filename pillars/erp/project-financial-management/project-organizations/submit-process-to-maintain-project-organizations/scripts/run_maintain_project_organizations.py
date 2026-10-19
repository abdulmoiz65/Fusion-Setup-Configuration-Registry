#!/usr/bin/env python3
"""Run only approved parameterless OrgDenormJob; save acceptance before polling."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

FIXED_PAYLOAD = {
    "jobDefinitionId": "JobDefinition://oracle/apps/ess/projects/foundation/setup/system/OrgDenormJob",
    "application": "FscmEss",
    "product": "PJF",
}


def payload_digest(payload):
    """Bind approval to the complete JSON object, independent of formatting."""
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate_payload(args, adapter):
    supplied = adapter.load_payload(args)
    if "requestParameters" in supplied or args.parameter:
        raise ValueError("Maintain Project Organizations rejects all user-supplied request parameters.")
    if any(key not in FIXED_PAYLOAD or value != FIXED_PAYLOAD[key] for key, value in supplied.items()):
        raise ValueError("Only the fixed parameterless OrgDenormJob payload is supported.")
    return dict(FIXED_PAYLOAD)


def verify_approval(args, props, payload):
    if not getattr(args, "approval_file", None):
        raise ValueError("Explicit approval of the exact target and payload is required.")
    if Path(str(args.approval_file) + ".attempted.json").exists():
        raise ValueError("This approval already has a submission attempt; resume or reconcile it.")
    approval = json.loads(Path(args.approval_file).read_text(encoding="utf-8"))
    if (approval.get("approved") is not True or approval.get("operation") != "submit"
            or approval.get("environment") != props["environment"]
            or approval.get("restBaseUrl") != props["restBaseUrl"]
            or approval.get("payload_sha256") != payload_digest(payload)):
        raise ValueError("Approval is declined, incomplete, or does not match the exact target and payload.")


def load_adapter():
    source = Path(__file__).resolve().parents[6] / "core/fusion-api/ess-job-submitter/scripts/ess_job_submitter.py"
    spec = importlib.util.spec_from_file_location("project_organizations_core_ess", source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_receipt(adapter, result, output, props):
    """Keep known recovery identity visible even when receipt storage fails."""
    try:
        adapter.write_result(result, str(output))
        return True
    except Exception:
        # Whitelist recovery fields, never the exception, response body or token.
        try:
            target_host = urlsplit(props.get("restBaseUrl", "")).hostname
        except ValueError:
            target_host = None
        request_id = result.get("execution_result", {}).get("requestId")
        if isinstance(request_id, bool) or not isinstance(request_id, int) or request_id <= 0:
            request_id = None
        print(json.dumps({
            "failure_class": "artifact_persistence",
            "stage": "receipt_persistence",
            "environment": props.get("environment"),
            "target_host": target_host,
            "jobDefinitionId": FIXED_PAYLOAD["jobDefinitionId"],
            "requestId": request_id,
            "next_action": "Repair receipt storage and resume this request ID; do not resubmit."
                           if request_id else "Repair receipt storage and reconcile any uncertain submission; do not resubmit.",
        }), file=sys.stderr)
        return False


def execute(args, adapter):
    """Persist acceptance before monitoring; never call the retrying core main()."""
    if not args.output or args.find_recent_job_definition:
        raise ValueError("A distinct --output receipt is required; recent-request lookup is not this execution route.")
    if args.request_id is not None and (isinstance(args.request_id, bool)
                                       or not isinstance(args.request_id, int) or args.request_id <= 0):
        raise ValueError("--request-id must be positive.")
    operation = getattr(args, "operation", None)
    if (operation not in (None, "submit", "resume")
            or (operation == "submit" and args.request_id is not None)
            or (operation == "resume" and args.request_id is None)):
        raise ValueError("Use submit without request ID or resume with the saved request ID.")
    payload = validate_payload(args, adapter)
    if args.wait_seconds <= 0 or args.poll_interval <= 0:
        raise ValueError("Polling requires positive wait seconds and interval.")
    output = Path(args.output)
    accepted_path = Path(str(output) + ".accepted.json")
    for path in (output, accepted_path):
        if path.exists():
            raise ValueError("Receipt already exists; use a new output path and resume the known request ID.")
        path.parent.mkdir(parents=True, exist_ok=True)
        # Check actual file creation/writes before authentication or submission.
        # Storage can still fail later; write_receipt preserves recovery identity.
        with path.open("x", encoding="utf-8") as receipt:
            receipt.write("{}\n")
        path.unlink()
    props = {}
    accepted = None
    stage = "preflight"
    try:
        props = adapter.read_properties(Path(args.properties))
        adapter.require_props(props, ["environment", "restBaseUrl"])
        if args.request_id is None:
            stage = "approval"
            verify_approval(args, props, payload)
        # Acquire credentials once through core; never refresh and replay a POST.
        token = adapter.get_token(props, args)
        if args.request_id is None:
            # Consume this approval before POST. An uncertain attempt cannot reuse it.
            stage = "attempt_persistence"
            attempt_path = Path(str(args.approval_file) + ".attempted.json")
            with attempt_path.open("x", encoding="utf-8") as receipt:
                json.dump({"environment": props["environment"], "restBaseUrl": props["restBaseUrl"],
                           "payload_sha256": payload_digest(payload), "output": str(output),
                           "submission_state": "attempt_recorded_reconcile_before_new_submission"}, receipt)
        stage = "submission" if args.request_id is None else "resume"
        submit_args = copy.copy(args)
        # Freeze the approved object in memory; core must not reread a mutable file.
        submit_args.payload_file = None
        submit_args.payload = json.dumps(payload)
        submit_args.submit_only = True
        accepted = adapter.run_with_token(props, token, submit_args)
        request_id = accepted["execution_result"]["requestId"]
        if isinstance(request_id, bool) or not isinstance(request_id, int) or request_id <= 0:
            raise ValueError("Core returned no positive ESS request ID; reconcile before any new submission.")
        stage = "acceptance_persistence"
        accepted["audit_summary"].update(
            fixed_payload=payload,
            approval_bound=args.request_id is None,
            payload_sha256=payload_digest(payload),
            environment=props["environment"],
            restBaseUrl=props["restBaseUrl"],
        )
        adapter.write_result(accepted, str(accepted_path))
        saved = json.loads(accepted_path.read_text(encoding="utf-8"))
        if saved != accepted:
            raise ValueError("Accepted receipt could not be verified; stop before polling.")
        if args.submit_only:
            result = accepted
        else:
            stage = "tracking"
            track_args = copy.copy(args)
            track_args.request_id = request_id
            track_args.submit_only = False
            result = adapter.run_with_token(props, token, track_args)
            status = result["execution_result"].get("status") or {}
            if (status.get("requestId") not in (None, request_id)
                    or status.get("jobDefinitionId") not in (None, FIXED_PAYLOAD["jobDefinitionId"])):
                raise ValueError("Returned status belongs to another ESS request or job.")
            # Keep submission evidence alongside the latest status from core.
            result["execution_result"].update(
                submitted=accepted["execution_result"]["submitted"],
                submit_response=accepted["execution_result"]["submit_response"],
                location=accepted["execution_result"]["location"],
            )
            result["audit_summary"].update(accepted["audit_summary"])
    except Exception as exc:
        result = copy.deepcopy(accepted) if accepted else adapter.build_failure_result(props, exc)
        result["diagnostics"].update(
            failure_class=("artifact_persistence" if stage in {"acceptance_persistence", "attempt_persistence"} else
                           "auth_authz" if isinstance(exc, adapter.FusionHttpError) and exc.status_code in {401, 403}
                           else "fusion_api_error" if isinstance(exc, adapter.FusionHttpError)
                           else "approval_blocker" if stage == "approval"
                           else "transport_or_environment"),
            stage=stage,
            message=f"Organization-maintenance {stage} failed ({type(exc).__name__}); no automatic resubmission.",
            submission_state="accepted" if accepted and accepted["execution_result"].get("requestId") else
                             "indeterminate" if stage == "submission" else "not_submitted",
            next_action="Resume the preserved request ID; reconcile an unknown submission before seeking new approval.",
        )
        write_receipt(adapter, result, output, props)
        return 1
    if not write_receipt(adapter, result, output, props):
        return 1
    execution = result["execution_result"]
    if execution["terminal"] and execution["success"] is False:
        return 4
    if result["diagnostics"]["timed_out_waiting"]:
        return 3
    return 0


def main():
    adapter = load_adapter()
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--approval-file", help="Explicit target/payload approval JSON receipt.")
    parser.add_argument("--operation", choices=("submit", "resume"))
    parser.add_argument("--dry-run", action="store_true", help="Show the fixed payload without authentication or submission.")
    local, remaining = parser.parse_known_args()
    if "--help" in remaining or "-h" in remaining:
        print("Task options: --dry-run; --approval-file <explicit approval JSON>. Only fixed OrgDenormJob is permitted.")
    sys.argv = [sys.argv[0], *remaining]
    args = adapter.parse_args()
    args.approval_file = local.approval_file
    args.operation = local.operation
    if local.dry_run:
        print(json.dumps(validate_payload(args, adapter), indent=2))
        return 0
    return execute(args, adapter)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        # Exception messages may contain tenant payloads or credentials.
        print(f"Organization-maintenance execution stopped ({type(exc).__name__}); preserve existing receipts.", file=sys.stderr)
        raise SystemExit(1)
