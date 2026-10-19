# Opt-in CPQ integration validation

Offline tests prove local behavior with explicit local approval and synthetic Fusion fixtures.
They do not verify the current live registration, response completeness, or
server execution semantics. Never describe them as a successful live test.

## Prerequisites and blockers

1. Run the guard's `capabilities` command. Explicit local approval reports
   `liveApprovalAvailable=true` and `authenticated-actor=false`. This supports
   the guarded route using actual user consent, exact `--reviewed-binding`,
   `--confirmed`, and a nonempty caller-supplied `--actor` attribution. It does
   not verify who approved; ATEAM-1461 recommendation 3 remains unmet. If the
   workflow requires authenticated approval, declare `authenticated-actor`
   in `requiredGuarantees` and stop when that capability is unavailable.
   Never manufacture identity evidence or call Core directly.
2. Obtain an explicit request for testing in a named non-production Fusion
   environment with a disposable CPQ setup. Use the implementation router,
   selected project, current registration, authentication, and privilege checks.
   Do not infer authorization from this developer change request.
3. Record the required guarantees. If the test requires conditional writes,
   cross-host exclusion, or enforcement against direct Core callers, stop:
   the current route cannot provide them. Do not substitute a REST mutation.
4. Keep synthetic test names/addresses and raw artifacts in protected temporary
   storage; retain only permitted fingerprints, results, and external IDs in
   the project. Record the run and token usage through the project workflow.

## Read-only preparation

When the routed implementation workflow reaches its declared preparation steps,
run guard `preview` with the private `--task-input`, prepared task envelope,
selected properties and Run Book configuration. The version 3 manifest records
the live business-object registration, rebuilt Task Hook evidence and complete
CPQ discovery baseline. Core preflight `eligible` is a nonempty source/object
list, not a boolean; the guard validates the list against the selected stage. Confirm
that the response exposes the actual company fields, administrator first name,
last name and email, identities, and complete child collections. Missing fields,
ambiguous IDs, incomplete pagination, or unsupported layouts are blockers. Do not mark
live compatibility passed based on synthetic responses.

## Mutation tests, only after the prerequisites pass

1. Prepare initialization through Core, build the guard preview, obtain the
   stage's actual user approval of that exact preview, record explicit local
   approval with the matching binding and actor attribution, and execute once
   through the guard. On the explicit continuation, confirm the
   identified initialization load completed without errors through
   `reconcile-initialization` before proceeding.
2. Prepare one synthetic Company Profile/admin child import with current
   metadata. Approve its exact manifest and execute once. Record external IDs;
   never reuse the approval after error or timeout.
3. Run `reconcile` on that child manifest/approval. Check successful completion of its exact job and that actual current
   records match the baseline plus every approved change, with no extra admins
   or changed retained company values. Build a new final manifest and obtain
   its separate approval. Verify that stale or altered evidence blocks before
   submission.
4. Submit once. Confirm the final state check passed, the approval was consumed,
   and the shared target lock remains. On an explicit status request, use the
   recorded job's status workflow. Do not retry as part of validation.
5. Exercise tampering, replay, competing approvals/projects, crash, timeout,
   and recovery failure cases using the offline tests. Do not deliberately
   launch competing live mutations or induce an uncertain production outcome.

## Evidence and completion

Report each check as passed, failed, or blocked, with sanitized environment,
stage, artifact/manifest/approval fingerprints, request IDs, and observed status.
An accepted import is not proof that all business changes completed. Do not
mark the end-to-end test passed until the declared result and reconciliation
checks succeed. Do not unlock a post-handoff attempt merely to repeat a test;
the existing status contract lacks proof that a retry is safe.

All test executions must use the pillar guard. Source review should confirm
that `SKILL.md` and `api-flow.md` route mutations through it. This validates the
declared skill path; preventing unrelated callers from bypassing the guard
requires enforcement outside this pillar and remains unsupported.


### Pillar functional recovery and existing configuration

The pillar guard supports these read-only commands at the declared verification/recovery step. They do not authorize any new mutation or replace the explicit approval required for each new stage:

- `recover-prewrite --project ... --manifest ... --approval-record ... --properties ...`: release only a consumed attempt with an explicit durable `checking` phase, no remote IDs, unchanged assistant identity and eligible status. It holds the same target process lock as execution. The write callback atomically changes the phase to `write_started` before upload. Missing legacy phase, any write-boundary crossing, or remote identifiers prevent release. The nonce remains consumed; rebuild evidence and obtain fresh approval. Crash after marking the write boundary remains uncertain even if no upload occurred.
- `reconcile-existing --project ... --manifest ... --proposal ... --preflight ... --task-envelope ... --task-input ... --reconciliation ... --properties ... --run-config ...`: validate an exact final-only artifact and current ready configuration when no child write has been attempted. The manifest argument reserves the later preview path; this command creates only the receipt. Supply that receipt to the usual final preview, approval and execution commands. A known child write, including a completed or partial one, requires ordinary full child reconciliation. Explicitly released zero-write attempts are eligible. Receipts bind the target, source, route, state, freshness and current receipt identity.
- `inspect-child-outcome --project ... --manifest ... --approval-record ... --properties ...`: assess the latest consumed child attempt without resubmitting anything. Each operation is reported as matching approved values, not observed, or uncertain; no business values are persisted in this diagnostic. Missing or pending completion evidence and partial state return a nonzero CLI status. The pending marker is retained even when observations match; use full reconciliation to advance. An absent administrator is not proof that the original job cannot create it later.

Registered `Content-Type` and `REST-Framework-Version` columns are accepted for final submission and child routing. Live registration must independently include them; they do not count as Company Profile business changes. Final submission still permits only the approved `SUBMITTED` status mutation.

Explicit local approval enables the guarded pillar route without independent approving-user authentication. ATEAM-1461 recommendation 3 remains unmet. These recovery commands do not clear an uncertain write or establish cross-host/non-bypassable enforcement. Safe automated retry of remaining partial work requires authoritative original-job finality and idempotency; it is not enabled by these commands.


Review corrections: latest-import selection excludes only explicitly released zero-write attempts; recovery invalidates prior child receipts so fresh reconciliation remains mandatory. Missing legacy phases and uncertain writes remain blocking. New reconciliation fingerprints normalize record order and omit REST navigation links without reordering approved operations. Older receipts with different fingerprints must be regenerated, never rewritten under an existing approval.

The supported pillar transport values for non-initialization rows are `application/json` or `application/vnd.oracle.adf.resource+json` for `Content-Type`, and `9` for `REST-Framework-Version`. Each supplied column must also exist in live registration. Required transport values must be supplied explicitly; the guard neither inserts defaults nor accepts arbitrary strings. Initialization retains its action-specific content type. Registrations requiring a different value remain blocked pending an explicit contract update.


### Complete discovery and retained recovery checks

The guard now uses bounded paging for CompanyProfiles and CPQUsers during
reconciliation/final-state verification, with assistant identity/status checks
before and after the reads. This does not change the separate one-shot progress
status workflow. Full-set comparison still rejects extra, missing or substituted
administrators, including records found only on later pages.

Recovery snapshots are retained before approval consumption in the owner-private
local evidence store. Historical commands accept `--attempt-id` and reverify the
consumed ledger and approval fingerprints. Temporary source deletion and approval
expiry must not prevent historical reconciliation/status inspection. Storage
failure must prevent consumption/upload; altered evidence, wrong-project evidence,
and unconsumed attempts must fail before any external read. Retained evidence
must never authorize a new mutation. See `cpq-approval-guard.md` for migration,
retention and cleanup rules. Independent approving-user authentication remains
unavailable; explicit local approval does not provide that guarantee.
