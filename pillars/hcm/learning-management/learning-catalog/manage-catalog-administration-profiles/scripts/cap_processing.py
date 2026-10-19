"""Bounded, read-only CAP processing observation using the declared GET route.

Python 3.11+. This does not submit reconciliation, inspect ESS jobs, establish
contributor state or grant write readiness. Invocation requires routed read
authorization. The default is one exact-number observation, not a background job.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

import cap_workflow


# Product source, not deployment certification: CAP Redwood template lines
# 39 and 67-76 in learning-administration-ui/extension1/sources/ui/self/
# applications/learning-setup/flows/main/pages/
# catalog-administration-profile-details-page-template.html gates contributor
# export/list links on this exact success enum. The backend getter is
# learningorganizations/view/LearnOrgLearningItemVORowImpl.java:905-910.
ROOT_SUCCEEDED = "ORA_PROCESSING_SUCCEEDED"
PENDING = "ORA_NEEDS_PROCESSING"
MAX_TIMEOUT_SECONDS = 300
MAX_SAMPLES = 20


class ReadUnavailable(ValueError):
    """Sanitized read-route failure; never contains subprocess output."""


def _read_via_workflow(request, remaining_seconds):
    """Run existing readiness/GET workflow with an outer process-tree deadline.

    This is not an HTTP adapter. The child invokes cap_workflow.execute through
    its supported CLI, which retains shared graph, target, metadata, identity and
    transport checks. Kill the read process group on timeout, not only its parent.
    No child output is echoed or retained on failure.
    """
    command = [sys.executable, str(Path(__file__).with_name("cap_workflow.py")),
               "retrieve", "--request-stdin", "--execute-read"]
    timeout = min(180, remaining_seconds)
    if timeout <= 0:
        raise TimeoutError("Processing observation deadline reached")
    try:
        process = subprocess.Popen(command, cwd=cap_workflow.REPO,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True,
                                   start_new_session=True)
        try:
            stdout, _ = process.communicate(json.dumps(request), timeout=timeout)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.communicate()
            raise TimeoutError("Declared read workflow exceeded its deadline") from None
    except TimeoutError:
        raise
    except OSError:
        raise ReadUnavailable("Declared read workflow could not be started") from None
    if process.returncode != 0:
        raise ReadUnavailable("Declared read readiness or GET failed")
    try:
        result = json.loads(stdout)
    except (ValueError, TypeError):
        raise ReadUnavailable("Declared read returned invalid JSON") from None
    return result


def _validate_request(request):
    allowed = {"mode", "number", "expected_id", "environment", "host",
               "confirmed_host", "headers"}
    if (not isinstance(request, dict) or set(request) - allowed
            or request.get("mode") != "exact" or "number" not in request):
        raise ValueError("Processing observation requires an exact-number read request")
    cap_workflow.validate_read_request(request)


def _validate_bounds(max_samples, timeout_seconds, interval_seconds):
    if type(max_samples) is not int or not 1 <= max_samples <= MAX_SAMPLES:
        raise ValueError("max_samples must be an integer from 1 to 20")
    for value, lower, upper, name in (
            (timeout_seconds, 0, MAX_TIMEOUT_SECONDS, "timeout_seconds"),
            (interval_seconds, 15, MAX_TIMEOUT_SECONDS, "interval_seconds")):
        if (type(value) not in (int, float) or not math.isfinite(value)
                or value > upper or value < lower or value == 0):
            raise ValueError(name + " is outside the bounded observation contract")


def _observation(result, request, elapsed):
    """Validate envelope and identity before projecting processing evidence."""
    if not isinstance(result, dict):
        raise ReadUnavailable("Invalid read envelope")
    if (result.get("environment") != request["environment"]
            or result.get("host") != request["host"]):
        raise ReadUnavailable("Read target identity changed")
    if (result.get("validation_purpose") != "retrieval_only"
            or result.get("write_eligible") is not False
            or result.get("side_effects") != []):
        raise ReadUnavailable("Read isolation evidence is missing")
    if result.get("status") != "matched" or result.get("pagination_completed") is not True:
        raise ReadUnavailable("Unique accessible profile not established")
    matches = result.get("matches")
    if not isinstance(matches, list) or len(matches) != 1 or not isinstance(matches[0], dict):
        raise ReadUnavailable("Unique accessible profile not established")
    row = matches[0]
    if row.get("learningCatalogProfileNumber") != request["number"]:
        raise ReadUnavailable("Read profile identity changed")
    raw = row.get("processingStatus")
    if raw is not None and (not isinstance(raw, str) or not re.fullmatch(r"ORA_[A-Z0-9_]{1,76}", raw)):
        raise ReadUnavailable("Processing status violates its code contract")
    state = "pending" if raw == PENDING else "succeeded" if raw == ROOT_SUCCEEDED else "unverified"
    return {"elapsed_seconds": round(elapsed, 3), "processing_status": raw,
            "state": state, "field_available": "processingStatus" in row}


def observe_processing(request, *, max_samples=1, timeout_seconds=300,
                       interval_seconds=15, read=None, clock=None, sleep=None):
    """Observe one exact CAP number with finite count, interval and wall time.

    ``read(request, remaining_seconds)`` is injectable for offline tests only.
    The default launches the supported CAP workflow CLI under a process-group
    timeout. ``clock`` is monotonic; time spent reading and sleeping counts.
    A late response never establishes completion. Unknown codes/null stop as
    unverified rather than inferring success or triggering reconciliation.
    """
    _validate_request(request)
    _validate_bounds(max_samples, timeout_seconds, interval_seconds)
    read = _read_via_workflow if read is None else read
    clock = time.monotonic if clock is None else clock
    sleep = time.sleep if sleep is None else sleep
    started = clock()
    observations = []
    attempts = 0
    status, reason = "unverified", "not_observed"
    for index in range(max_samples):
        remaining = timeout_seconds - (clock() - started)
        if remaining <= 0:
            status, reason = "timed_out", "deadline"
            break
        attempts += 1
        try:
            result = read(copy.deepcopy(request), remaining)
            elapsed = clock() - started
            if elapsed >= timeout_seconds:
                status, reason = "timed_out", "late_read_not_used"
                break
            observation = _observation(result, request, elapsed)
        except TimeoutError:
            status, reason = "timed_out", "read_deadline"
            break
        except (ValueError, OSError):
            status, reason = "unavailable", "read_or_identity_check_failed"
            break
        observations.append(observation)
        status = observation["state"]
        if status != "pending":
            reason = "root_success_observed" if status == "succeeded" else "unknown_or_missing_processing_state"
            break
        if index == max_samples - 1:
            reason = "single_observation" if max_samples == 1 else "sample_limit"
            break
        remaining = timeout_seconds - (clock() - started)
        if remaining <= interval_seconds:
            status, reason = "timed_out", "insufficient_budget_for_next_sample"
            break
        sleep(interval_seconds)
    return {"status": status, "stop_reason": reason,
            "environment": request["environment"], "host": request["host"],
            "learningCatalogProfileNumber": request["number"],
            "attempt_count": attempts, "sample_count": len(observations),
            "observations": observations, "elapsed_seconds": round(clock() - started, 3),
            "last_processing_status": observations[-1]["processing_status"] if observations else None,
            "root_processing_completed": status == "succeeded",
            "loader_completion_verified": False, "job_completion_verified": False,
            "contributor_state_verified": False, "write_eligible": False, "side_effects": [],
            "validation_purpose": "processing_observation_only",
            "limitations": {"account": "Authenticated account-visible profile only",
                            "effective_date": "Server-current; no historical/as-of override",
                            "language": request.get("headers", {}).get("Accept-Language", "Server default"),
                            "processing": "Root status observation only; no correlated ESS job or contributor verification",
                            "consistency": "Samples are separate reads, not a transactional snapshot"},
            "next_step": "Review the recorded observations; another authorized read may be requested. No reconciliation or load was submitted."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request-stdin", action="store_true", required=True)
    parser.add_argument("--execute-read", action="store_true")
    parser.add_argument("--max-samples", type=int, default=1)
    parser.add_argument("--timeout-seconds", type=float, default=300)
    parser.add_argument("--interval-seconds", type=float, default=15)
    args = parser.parse_args(argv)
    try:
        request = json.load(sys.stdin)
        _validate_request(request)
        _validate_bounds(args.max_samples, args.timeout_seconds, args.interval_seconds)
        if not args.execute_read:
            result = cap_workflow.readiness("retrieve", request)
        else:
            result = observe_processing(request, max_samples=args.max_samples,
                                        timeout_seconds=args.timeout_seconds,
                                        interval_seconds=args.interval_seconds)
    except (ValueError, OSError):
        result = {"status": "unavailable", "write_eligible": False,
                  "message": "Processing read input, readiness or observation failed. No write occurred."}
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in {"ready_for_read_preflight", "succeeded", "pending", "unverified"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
