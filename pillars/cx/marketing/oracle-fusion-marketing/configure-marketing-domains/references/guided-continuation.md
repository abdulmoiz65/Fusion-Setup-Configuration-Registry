# Guided Marketing Domain Continuation

Use this caller contract when a domain update spans Run Book setup, a running
helper, a read-only follow-up, or another conversation turn. It supplements the
task's Custom Execution Workflow; core.runbook and core.data-loader remain the
only owners of their declared operations. This is assisted guidance, not a new
executor, authentication broker, or automatically persisted state machine.

## Stages and the next actor

Advance only on confirmed evidence. Retain the selected domain and supplied
changes in available conversation context while completing prerequisites.

| Phase | Evidence required to leave this phase | Next actor and action |
|---|---|---|
| `awaiting_selection` | One exact domain selected from the completed list | User selects; caller reads and displays the complete selected record. |
| `awaiting_changes` | Supported, nonblank changes for the displayed record | User supplies missing changes; caller validates them. |
| `runbook_pending` | Existing core binding is active and complete returned dashboard has been delivered | Core completes its declared prerequisite; caller continues preparation in the same turn. |
| `preparing_source` | Registered object and live headers resolved; fresh sparse source verified | Caller follows the task source-preparation route through core.data-loader. |
| `validating` | Immutable archive/preflight exists and Task Hook checks passed for those exact bytes | Core builds its immutable approval preview. |
| `preview_running` | Original helper has returned a verified stage result, including the documented approval-required exit; source/core preflight and Task Hook validation have passed for the final bytes | Caller polls that same helper; deliver the approval preview only after all validation, never preliminary helper approval text. |
| `awaiting_approval` | Exact preview delivered and contextual approval received under core's contract | User approves or revises; caller invokes core's immutable approved-artifact path. |
| `submitting` | Verified accepted initiation result, or classified failed/uncertain result | Core submits once; caller records the confirmed outcome. |
| `verifying` | Fresh unambiguous domain read-back and comparison of every approved changed field | Caller completes the task's bounded read-back and final response. |
| `blocked` | Recorded blocker resolved with evidence | Caller resumes the recorded next action; ask only for missing user input. |
| `paused` | User explicitly resumes | Caller restores the prior phase and checks its evidence. |
| `cancelled` | A new explicit update request | Caller starts only the newly requested work; no automatic continuation. |
| `complete` | Final initiation report and verification outcome delivered | No further action unless requested. |

Run Book creation and its dashboard complete a prerequisite, not the domain
update. Deliver the complete sanitized dashboard before downstream operations,
then continue the already requested preparation in the same turn. Do not ask
again for changes that remain available. Never recreate an active Run Book or
initialize another project merely because a conversation resumes. Pending,
failed, or unknown Run Book states retain the core workflow's blocking rules.

## Follow-ups, pauses, and visible handoffs

Interpret “check again” according to the object the user asked to inspect. A
request to check the domain means a fresh paginated read-only Domains GET and
the complete selected-record display after the normal read preflight. It is a
side trip: retain the pending changes, original preparation authority, and
next action. After reporting that read, continue pending preparation when its
prerequisites are satisfied. Do not replace the update with a status-only task
or restart the change-selection interaction. Ask for clarification only when
the requested inspection target cannot be resolved from context.

Neither “check again” nor “resume” approves an upload. A read-only request does
not create a new mutation approval, revoke an existing scoped preparation
request, or permit replay of an upload. An explicit pause, cancellation, or
instruction to perform only the read takes precedence; preserve that intent.
An accepted load still follows the existing verification contract, while an
explicit request for Data Loader job status routes to core's status workflow.

At every genuine stop, make three facts clear in ordinary language: **Completed**
(confirmed work only), **Next** (the pending action), and **Your action** (the
specific missing input/approval, or “none” while the caller is still working).
For a pause or recoverable blocker, say that ordinary “resume” wording is
accepted. Do not end at a dashboard or empty helper output when authorized work
can continue. Never call preparation, preview, or Run Book creation a completed
domain update; verified field values also do not prove asynchronous job success.

## Evidence and durable continuation

The Marketing caller must use the existing project state, artifact registry,
and run-record managers to persist a redacted continuation checkpoint in the
already initialized project, and record prescribed token usage. This document
does not write checkpoints itself. Record confirmed transitions and the pending
next action before a handoff, pause, or blocker; never invent completed evidence
to make a resumed workflow advance.

Persist only an allow-listed checkpoint: phase, next action, requested field
names (for example, `senderName` and `replyToName`), nonsecret environment and
task-context references, safe artifact/envelope references, their integrity
digests when available, evidence/process statuses and timestamps, explicit pause/cancel
state, and blocker class. Use generic artifact names that reveal no domain or
header values. Reference the authoritative core Run Book binding without
copying server identifiers. Record an approval evidence reference/status only
when core has bound it to the exact preview; a checkpoint is never approval.

Write append-only checkpoint versions under the task's declared
`continuation/` artifact directory; register the latest version with the
existing project managers. Do not write new arbitrary fields into the shared
project-state schema. Record prerequisite completion and supplied field names
as well as the following evidence checkpoints: verified sparse source; immutable archive
and preflight; Task Hook result for those bytes; delivered preview and its
approval state; accepted, failed, or uncertain initiation; and read-back result.
Distinguish “started” from “passed” and “accepted” from “unknown.” Keep the
original mutation-attempt state so recovery cannot silently resubmit.

Never persist primary domains, sender/reply-to names or addresses, bounceback
addresses, current record values, customer payloads, record IDs, self links,
ETags, credentials, token-cache contents, OAuth codes/state, or tool session
handles in the project. This includes checkpoint text, diagnostic messages,
filenames, token logs, and run records. Keep process handles and available
customer values transient. Existing core-owned private artifacts containing
payloads must remain outside the project and tracked repository; reference
them only with safe generic paths. Do not copy them into a project checkpoint
or invent a new customer-data cache to support resume.

On a fresh session, read the existing project and checkpoint, confirm the
environment/task context, then recover only evidence and values actually
available from conversation or the existing permitted core artifact. If the
workspace predates this checkpoint contract, reconstruct only confirmed stages
from its existing Run Book binding and core artifacts. An absent preview or
checkpoint is not proof that no mutation was attempted; reconcile an unknown
attempt before any retry. Retain usable conversation intent and request only
what cannot be recovered. If the
selection or requested values cannot be recovered safely, ask for only those
missing inputs; field names, digests, or stale record views cannot reconstruct
them. Do not create another project or rerun completed prerequisites.

For an intact preview still awaiting approval, retain its exact archive,
preflight, and Task Hook preview; re-present the existing report and request
approval without regenerating its source. For an approved immutable artifact, use core's approved-preflight/envelope
verification path. Do not rebuild the source, refresh live schema, or repeat
Task Hook validation merely because time passed. Missing/changed artifacts,
invalid envelopes, or changed environment/Run Book context require fresh
preparation, validation, preview, and approval through core. A failed or
uncertain mutation requires reconciliation of existing evidence through the
declared core route; never replay it automatically. If that route cannot
resolve the outcome, record the blocker and the precise next action.

## OAuth and running helper discipline

For every standard Run Book or Data Loader invocation, explicitly pass
`--token-cache` with the absolute checkout-root `.fusionaim_token.json` path.
For the BOSS client, explicitly pass the absolute checkout-root
`.fusionaim_boss_token.json` path and retain its configured `boss_scope` route.
Resolve the checkout root once; do not depend on the command's working
directory or copy tokens between the standard and BOSS caches. Delegate cache
inspection, reuse, and refresh to the existing core OAuth client.

Run commands from the working directory required by the owning core skill.
For example, use this sample-generation command from the repository root only
after the active Run Book gate passes. Replace both placeholders with verified
absolute paths; the private destination must be fresh and outside `project/`
and the tracked repository:

```bash
python3 core/data-loader/scripts/generate_sample_dat.py domains \
  --operation update \
  --token-cache "<absolute-repository-root>/.fusionaim_token.json" \
  --output-dir "<approved-private-working-directory>"
```

Never run `fusion_login.py` as a generic preflight: it always uses
`force_login=True`, bypassing reusable-cache behavior. Invoke the routed helper
with its pinned cache and let the shared client decide whether login is needed.
Before launching another authentication-capable command, establish that no
prior workflow command is running and inspect the configured loopback callback
port for an existing listener. If a listener is present, resolve its ownership
as described below before launching. Missing tools or permission-denied output
are unknown readiness, not a free port. Serialize all authentication-capable
commands, including read-only helpers; only one may own a possible callback
flow at a time. Do not background, use
`nohup`, or relaunch an operation while its original process is active.

Preserve the complete execution result internally, including `session_id`,
`exit_code`, output, and elapsed time. A yielded `exec_command` session must be
resumed with `write_stdin` using that session ID. `functions.wait` applies only
to a yielded `functions.exec` cell ID; it does not poll an `exec_command`
process. Keep these handles transient, outside durable project checkpoints.
When orchestrating tools, retain the whole result rather than only printing
`result.output`: otherwise the process session ID is lost. Once the outer cell
finishes, inspect the inner result; a nonempty inner `session_id` still needs
`write_stdin` even though the outer cell says completed.
Empty stdout or an output file that does not yet exist is not evidence of
failure while the process is running. Await exit and inspect the complete
result before declaring success, failure, or an absent preview.

Poll in bounded intervals that permit concise progress updates; preserve the
owning helper's timeout. Interpret exit codes using the owning helper's contract:
`upload_and_initiate.py` normally returns **1** for its preapproval
**approval-required** result. Inspect its complete report and verify the
persisted immutable archive/preflight with `mappingComplete=true`,
`taskRouted=true`, and a matching digest. That result is a prepared preflight,
not a process failure or completed Task Hook validation. Continue with pending
Task Hook checks and build its preview; only then present the unchanged core
approval report. Never treat an arbitrary exit 1 or an old artifact as success.

Classify actual failures from the core report (for example authentication,
mapping, or artifact persistence), using `process_failed` only for otherwise
unclassified execution failures and `process_timeout` for confirmed timeout.
Retain sanitized evidence and pending intent and report the concrete recovery
action. A timeout never authorizes an
upload/initiation retry. If an old session handle is unavailable after resume,
do not infer that its process stopped or start a duplicate; reconcile ownership
and outcome first.

`--no-open-browser` suppresses automatic browser opening; it still starts the
loopback callback listener. Inspect only the configured callback port with a
read-only `lsof -nP -a -iTCP:<configured-port> -sTCP:LISTEN` check before a new
authentication-capable command and when resolving a port conflict. `lsof`
returns **1** for no matching listener: empty stdout with no error/warning
diagnostics and that documented no-match status means no visible listener at
that instant, not proof against a race. A listener listing requires ownership
resolution; permission errors, warnings, or an unavailable tool mean unknown
readiness. If inspection needs additional local permission, use the host tool's
normal escalation for that same read-only check; if unavailable, stop and ask
for the specific listener-ownership check rather than another login. Do not send an
HTTP request to the callback as a health probe: it can consume the OAuth flow.
An unknown listener owner is a blocker. Cancel only this workflow's positively
identified owned session through its execution tool, verify its exit and port
release, and then follow the declared recovery route. Never kill by port,
terminate unrelated processes, or choose a random redirect/port.

The current shared OAuth implementation opens the browser before binding its
callback server. Serialization and ownership checks reduce collisions but do
not remove that race. This Marketing reference cannot fix it; if the race
occurs, report the actual failure and use the bounded owned-session recovery
above without claiming listener readiness or inventing a new authentication
route.
