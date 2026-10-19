# Daily Incremental scheduling

## Sources and boundary

Use the existing `core.fusion-api.ess-job-submitter` approved-submission contract.
No direct REST, browser mutation, alternate client, or OS/Codex automation is
part of this workflow. The existing core accepts an exact payload with an inline
schedule. This contract is grounded in Oracle's accessible
[26B request schema](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-ess-rest-scheduler-v1-requests-post.html)
and [26C request readback schema](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/op-ess-rest-scheduler-v1-requests-requestid-get.html),
checked 2026-10-08. The 26C POST and 26D readback pages were unavailable,
so the accessible 26B POST contract remains the submission reference. Revalidate release compatibility
before live use when the target differs; a contract discrepancy blocks dispatch.

## Preconditions and review

Require synchronized selected task bindings and Full-run evidence for the exact
project/environment/revision. In full implementation scope also require the
parent workflow's current configuration confirmation. A selected daily-only
request does not add the five configuration tasks or readiness row.
Inspect the core result: exact job and Full parameter, request ID, terminal
`PROCESS_SUCCESS`, completion time, and no contradictory error/warning result.
The same checks apply if the Full request was submitted outside FSCR: obtain
authorized core readback and bind the exact submission/configuration evidence;
a user assertion alone is insufficient. Failure, warning, timeout, unknown or
running status keeps this last task blocked. Never submit a replacement Full
request automatically.

Collect start date, daily time, named timezone, explicit offset-bearing first
occurrence, and either an end date/time or explicit no-end selection. Validate
the offset against the named timezone on that date, reject past starts and end
before start. This limited inline contract uses the reviewed offset/UTC daily
cadence. Do not promise a constant local wall-clock time across daylight-saving
changes: disclose the effect; block if the requested timezone/DST semantics
cannot be represented and verified by this contract. Do not invent a timezone
field in the schedule object.

Show environment, job, worker count (1..20, default 4), Incremental mode,
daily recurrence, first occurrence, timezone/offset semantics, end condition,
Full-success evidence reference, exact payload, readback settings and audit
destination. Require fresh explicit approval immediately before this separate
submission. Approval for Full, configuration readiness or Run Book creation
does not approve a recurring schedule. Changed inputs invalidate approval.

## Payload construction

Start with the nested skill's fixed job/application/product/retries and two
ordered STRING parameters. Force `submit.argument2=ORA_HRE_INCREMENTAL_RUN`.
Add `executePast: false` and exactly one inline recurrence:

```json
{
  "schedule": {
    "recurrences": [{
      "icalString": "FREQ=DAILY;INTERVAL=1;",
      "startDate": "<approved ISO 8601 timestamp with offset>",
      "endDate": "<approved ISO 8601 end timestamp with offset>"
    }]
  },
  "executePast": false
}
```

This is a fragment, not an executable payload. Omit `endDate` only for an explicit
approved no-end choice. Do not add top-level `startTime`, `scheduleId`, date
business parameters, callbackSubscription, multiple recurrences, inclusions or
exclusions. Reject UNTIL/COUNT recurrence shortcuts and arbitrary schedule JSON.
The resulting single daily recurrence must be the exact one approved.

Terminate every recurrence clause, including the last, with a semicolon.
The target Fusion Scheduler rejected `FREQ=DAILY;INTERVAL=1` with HTTP 400,
ESS-09412 on 2026-10-06. Its diagnostic requires the trailing semicolon;
Oracle's POST example also terminates its recurrence with a semicolon.
Correct the payload and obtain fresh approval after such a validation failure;
never retry the rejected POST automatically.

## Dispatch and verification

Daily scheduling is an ESS operation owned by the same nested task as Full,
with a separate manual Run Book tracking row. The authoritative plan and actual
Run Book sequences put it after Full; only terminal same-context Full success
unlocks its preview. Creating that row never submits a schedule.

Validate the existing version 1.0 `approved_submission` envelope against
`schemas/ess-delegation-contract.schema.json`. Set execution_options to
`wait_seconds: 1`, `poll_interval_seconds: 1`. Bind audit_context to project_id,
environment, configuration_revision and the inspected approval_reference;
fusion_environment_context includes the exact configured environment and
restBaseUrl. Compute approved_payload_sha256 from UTF-8 JSON with sorted keys,
compact separators, ensure_ascii=False and allow_nan=False. Persist the immutable
review/envelope in the project before fresh immediate approval. Recheck current
identity, catalog, active Run Book, synchronized owner handoffs,
configuration readiness, Full evidence and duplicate/uncertain request records.
Fusion enforces authorization during the approved submission and monitoring;
do not add an ESS submit-privilege probe or a privilege evidence field.

Use the scoped coordination module `../../scripts/touchpoints_ess_handoff.py`:
its callable `submit_and_monitor(project_root, approved_submission, "daily",
access_token, run_id=<unique reviewed run ID>)` delegates submission once to
core.submit_job_request. Obtain the token only through the already selected core
authentication workflow and Chrome sign-in policy. There is no new HTTP client,
authentication route, direct REST fallback, or core modification. The core skill
explicitly supports imports of its bundled functions.

The helper appends a sanitized, flushed audit intent before POST and a durable
request-ID checkpoint before monitoring, under the parent skill's project
current/ess-runs/<run_id>.jsonl directory. Existing audit names fail closed. The helper also checks prior attempted
submissions, so a new run ID cannot bypass a saved or uncertain schedule.
Retain that barrier across revisions and reconcile through the selected core read
route; neither a renamed journal nor a fresh name is permission to resubmit.
It calls core.get_job_request once, using the core's existing `fields` argument
for status plus requestType, requestParameters, schedule and parent identity.
This avoids relying on the unchanged CLI's `--full-status`, which omits fields
and may receive only the target's minimal default response. Full waiting remains
core.wait_for_job_request; daily readback never waits for a recurring parent to
finish. The module never invokes core.main/run_with_token, whose auth recovery
can replay submission. A POST or subsequent GET failure cannot trigger a new POST.

Require the same request ID, fixed job/application, both reviewed business
parameters, RECUR_PARENT identity and matching recurrence/start/end, allowing
equivalent offset timestamps. Reject errors, warnings, failed/cancelled/ended
parents, duplicate parameters and changed schedule semantics. Raw system
parameters, error bodies, credentials and stack traces are never written to the
scoped journal or result. Missing fields or readback failures remain
`submitted — verification pending`, retain the checkpointed request ID and leave
the tracking task open. Never infer successful verification from HTTP/CLI success
or a non-terminal parent alone.

For explicitly selected read-only reconciliation, import core.get_job_request
with the retained request ID and the helper's same readback_fields; inspect the
result with inspect_readback and persist a new sanitized verification artifact.
Core-only read authentication recovery may refresh once; no recovery path here
may reenter submission. Missing identity requires the core's explicitly selected
recovery lookup or an ID handoff, never a replacement schedule. On audit write
failure stop as artifact_persistence; AuditPersistenceError.result preserves any
known request ID in memory for the invoking skill's safe disclosure/recovery.
If the journal cannot be made durable, do not mark governed execution successful.

Only verified schedule creation permits the proposed Run Book outcome
`completed`, with the comment `Daily Incremental schedule configured and
verified; future executions are not yet verified.` The actual task update still
requires core.runbook authorization. Store the verified helper result as daily_schedule in the same-context workflow
state (the result includes its context, approval reference, Full request ID and
verification reference); the controller recognizes this as schedule configuration
completion and will not select creation again. Agent inspection of those referenced
records remains mandatory; evidence-shape checks do not authenticate provenance.
Store sanitized approved parameters, schedule and returned identity/readback evidence; never raw protected responses.

## Resume and duplication

Before creating a schedule, inspect the bound daily task and retained request
records. Reconcile an existing or uncertain recurring request through core
readback. If the user reports an existing schedule without an unambiguous ID,
use only the core's explicitly authorized recovery lookup or ask for its ID.
Never create a second schedule to replace missing evidence. An existing matching
verified schedule can be recorded as a no-change outcome after the same Full
prerequisite and context checks. Replacing/cancelling schedules is outside this
contract and must not be inferred from approval to create one.
