#!/usr/bin/env python3
"""Goal Management recovery state around the unchanged Core ESS CLI.

Invoke only after the Goal Plans workflow has verified readiness and approval.
Reuse the same run directory on every continuation; never create a new run to
recover an uncertain submission. This module does not implement an ESS client.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[6]
CORE = ROOT / "core/fusion-api/ess-job-submitter/scripts/ess_job_submitter.py"


def read_json(path):
    return json.loads(Path(path).read_text())


def save(path, value):
    """Publish a complete local record atomically, flushing before publication."""
    path = Path(path)
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        json.dump(value, stream, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    descriptor = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def handoff(*, payload, environment, run_dir, properties, token_cache,
            approved=False, wait_seconds=300, runner=subprocess.run):
    if not approved:
        raise ValueError("Explicit workflow approval is required")
    if not 0 <= wait_seconds <= 3600:
        raise ValueError("Monitoring window must be between 0 and 3600 seconds")
    if payload.get("jobDefinitionId") != "JobDefinition://oracle/apps/ess/hcm/goals/core/ScheduleProcessJobDef":
        raise ValueError("Only the Goal Management ESS job is supported")
    params = {p["name"]: p.get("value") for p in payload.get("requestParameters", [])}
    if params.get("submit.argument1") != "ASSIGN_GOAL_PLANS":
        raise ValueError("Only Assign Goal Plans is supported")
    # Include the effective CLI override in the digest and saved payload.
    payload = dict(payload, retries=0)
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    binding = {"environment": environment, "payload_sha256": digest}
    run_dir = Path(run_dir).resolve()
    if not run_dir.is_relative_to((ROOT / "project").resolve()):
        raise ValueError("Recovery artifacts must be under this repository's project directory")
    run_dir.mkdir(parents=True, exist_ok=True)
    with (run_dir / "handoff.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {"status": "LOCAL_EXECUTION_PENDING"}
        attempt = run_dir / "attempt.json"
        checkpoint = run_dir / "checkpoint.json"
        output = run_dir / "submission-result.json"
        request = run_dir / "request.json"
        base = [sys.executable, str(CORE), "--properties", str(properties),
                "--token-cache", str(token_cache), "--no-open-browser"]
        if attempt.exists():
            if read_json(attempt) != binding:
                raise ValueError("Existing attempt environment or payload differs; submission prohibited")
        else:
            if checkpoint.exists() or output.exists() or request.exists():
                raise ValueError("Orphaned recovery artifacts; submission prohibited")
            save(request, payload)
            save(attempt, binding)
            # From this point, any failure is uncertain and must never replay POST.
            runner(base + ["--payload-file", str(request), "--submit-only", "--retries", "0",
                           "--output", str(output)], check=False)
        if checkpoint.exists():
            accepted = read_json(checkpoint)
            if any(accepted.get(k) != v for k, v in binding.items()):
                raise ValueError("Checkpoint binding mismatch")
            request_id = accepted.get("request_id")
        else:
            try:
                result = read_json(output)
                request_id = result["execution_result"]["requestId"]
                if result["execution_result"].get("submitted") is not True or result["audit_summary"].get("rest_host") != environment:
                    raise ValueError("Submission result binding mismatch")
            except (OSError, ValueError, KeyError, TypeError):
                return {"status": "UNKNOWN_AFTER_SUBMISSION", **binding}
        if type(request_id) is not int or request_id <= 0:
            return {"status": "UNKNOWN_AFTER_SUBMISSION", **binding}
        save(checkpoint, {**binding, "request_id": request_id})
        execution = run_dir / "execution-result.json"
        process = runner(base + ["--request-id", str(request_id), "--wait-seconds", str(wait_seconds),
                                 "--output", str(execution)], check=False)
        # A terminal ESS result still requires the existing assignee reconciliation.
        return {"status": "ASSIGNMENT_SUBMITTED", "request_id": request_id,
                "monitor_exit_code": process.returncode, "execution_result": str(execution),
                "business_verification_required": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--payload-file", required=True, type=Path)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--environment", required=True, help="Approved Fusion REST host")
    parser.add_argument("--properties", type=Path, default=ROOT / "core/auth/fusionEnv.properties")
    parser.add_argument("--token-cache", type=Path, default=ROOT / ".fusionaim_token.json")
    parser.add_argument("--approved", action="store_true")
    parser.add_argument("--wait-seconds", type=int, default=300)
    args = parser.parse_args()
    # Reuse Core's configuration parser, without performing authentication here.
    sys.path.insert(0, str(CORE.parent))
    from ess_job_submitter import read_properties
    properties = read_properties(args.properties)
    environment = urlparse(properties["restBaseUrl"]).netloc
    if not environment or environment != args.environment:
        raise ValueError("Configured environment differs from approved environment")
    result = handoff(payload=read_json(args.payload_file), environment=environment,
                     run_dir=args.run_dir, properties=args.properties, token_cache=args.token_cache,
                     approved=args.approved, wait_seconds=args.wait_seconds)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "ASSIGNMENT_SUBMITTED" else 3


if __name__ == "__main__":
    raise SystemExit(main())
