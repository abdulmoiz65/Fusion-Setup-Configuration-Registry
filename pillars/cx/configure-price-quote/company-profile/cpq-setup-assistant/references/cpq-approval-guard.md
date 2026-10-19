# CPQ approval guard

Use `scripts/cpq_data_loader_guard.py` for every mutation handoff. Core Data
Loader still owns metadata validation, artifact preparation, authentication,
upload, initiation, and reporting. This wrapper adds CPQ approval enforcement;
it does not restore the retired direct-REST executor or change the read-only
registry. Direct invocation of generic Core upload bypasses this pillar guard
and is outside this skill's supported execution path.

## Capability gate and explicit local approval

Run `python3 scripts/cpq_data_loader_guard.py capabilities` without project or
manifest arguments to inspect the implemented guarantees. This command is
local and performs no authentication or Fusion requests.

Repository contract inspection found no trusted approving-session identity
verifier, no server-side conditional-version parameter in the prepared Data
Loader route, and no status field proving that an uncertain asynchronous load
can never apply later. Do not infer any of these guarantees from OAuth login,
generic success/error statuses, ETags on unrelated REST resources, or a local
actor string.

**Current behavior:** the guard supports explicit local approval and reports
`liveApprovalAvailable=true` with `authenticated-actor=false`. After the user's
explicit approval of the exact preview, the workflow records `--confirmed`,
`--reviewed-binding`, and a nonempty `--actor` audit attribution. The actor is
caller-supplied and is not independently verified. An actor alone cannot
approve or execute; exact manifest/record integrity, expiry, one-time nonce
consumption, live checks, reconciliation, and locks remain mandatory.

This removes the unconditional identity-verifier blocker from the supported
pillar route. It changes the approval trust model to rely on the local workflow
operator obtaining actual consent. ATEAM-1461 recommendation 3 (authenticated
approval and independent approval-ID verification in Core Data Loader) remains
unmet; no formal exemption is implied. This mode neither verifies the approving
session nor proves that the attributed actor is the person who approved.

The proposal may declare `requiredGuarantees`, an array of capability names.
`checkout-target-locking` is implemented. `authenticated-actor`,
`server-side-conditional-write`, `cross-host-locking`, and
`non-bypassable-execution` are unavailable in the current route; requesting any
unsupported or unknown guarantee blocks manifest construction. The absence of
a requirement does not turn an unavailable guarantee into a supported one.
Never fall back to generic Core upload when a capability gate blocks.

Follow [live-validation.md](live-validation.md) for the opt-in integration
procedure. No live-validation success is implied by the offline tests.

## Inputs and preparation

Task Hook readiness is a preapproval check. Build the immutable artifact, evaluate
its applicable rules with current-stage approval pending, build the Task Hook
preview, then create the guard manifest. Only after presenting that exact preview
obtain and record one stage approval. Do not supply a fictitious approval to make
readiness pass or require the manifest before the preview that creates it.
Prior-stage completion/reconciliation requirements remain in force. Missing
current-stage approval blocks `execute`, not readiness or `preview`.

Complete the existing deployment, status, initialization-load completion,
discovery, live-registration, and Task Validator checks before mutation.
Prepare the immutable ZIP and preflight envelope through Core Data Loader's
existing preapproval workflow. Do not approve or execute that generic handoff
separately. Supply its Task Validator envelope containing `preview`, including
`finalData.archiveSha256`; the CPQ guard adapts the same user approval to Core's
approval format only at execution.

Create an internal proposal JSON with:

| Field | Contract |
|---|---|
| `stage` | Exactly `INITIALIZE`, `IMPORT_COMPANY_AND_ADMINS`, or `SUBMIT`. |
| `host`, `environment` | Values identifying the prepared Core preflight target, compared using the normalization rules below. |
| `target` | For child import and submission, the same discovered `assistantName` and `companyProfileId` object. For initialization, explicitly use `{"scope":"environment","businessObject":"cpqSetupAssistantInitialize"}`: the initialization action targets the selected environment before a configuration record is available. An empty target is rejected. |
| `rediscovery` | Required for submission as described below. |

The guard creates one canonical manifest with these explicit fields:

| Manifest field | Source |
|---|---|
| `stage` | Validated proposal mutation type. |
| `target` | Normalized HTTPS origin, environment identifier, and stage-appropriate target identity. |
| `taskCode`, `taskName` | Exactly `ORA_CPQ_SETUP_ASSISTANT` and `CPQ Setup Assistant`; both are required and validated. |
| `executionSettings` | Explicit prepared-DAT execution contract described below. |
| `operations` | All DAT rows in their original archive order, with complete values. |
| `archiveSha256` | Immutable prepared ZIP digest, matching Core preflight and `finalData`. |
| `administratorSet` | Complete `CPQUsers` rows derived from those operations, in order; empty for initialization/submission. |
| `redactedBusinessSummary` | Automatically generated stage description and record counts, excluding names, emails, and business values. |
| `createdAt`, `expiresAt` | Preview time and expiry, expressed as UTC Unix seconds. |
| `nonce` | UUID generated once during preview. |

The manifest also includes schema version `cpq-approval-manifest/3`, entire proposal, entire Task
Validator preview (including all `finalData`), entire Core preflight, and
`liveValidation`: the independently resolved registration fingerprints, complete
pre-import state, rebuilt Task Hook evidence, private Task Hook input path and
exact effective upload/initiation settings. These raw business records remain
in private temporary storage, never the project ledger.
Canonical JSON uses sorted object keys and compact separators while retaining
array order. Its SHA-256 is returned as `bindingSha256`. All fields, including
the summary, expiry, and nonce, are inside that fingerprint. Required fields
and consistency with the proposal/actual archive are checked at approval and
execution. Any change requires fresh validation, preview, and approval.

Normalize the HTTPS origin by lowercasing/IDNA-encoding the DNS host, removing
a trailing DNS dot, omitting default port 443, and removing the sole trailing
slash. Preserve a nondefault port. Reject credentials, non-HTTPS schemes,
non-root paths, queries, fragments, whitespace, and invalid DNS origins.
Normalize the environment identifier using Unicode NFC and trim surrounding
whitespace; preserve case so distinct environment names cannot be conflated.
The original Core preflight is also fingerprinted and passed unchanged to Core,
which still checks its configured host/environment exactly. Equivalent normalized
targets do not permit changing the approved raw preflight after preview.

`executionSettings` explicitly contains `executionRoute=data-loader`,
`fileAction=IMPORT_AND_LOAD`, `sourceType=null`, `taskRouted=true`, the exact
`runID`, `supportsRunBookTaskCode`, `uploadFileName`,
`ucmAccount=hcm$/dataloader$/import$`, `wrapperAttempts=1`, and
`adapterPolicy=core.data-loader`, and every fixed `initiationOptions` value.
`runID` must be nonempty. These are the supported non-secret CPQ
prepared-DAT settings, not an unrestricted options dictionary. Reject missing
required settings, alternate FSM/FBDI/CX routing options, or execution-time
mismatches. Core continues to own authentication, transport, and its documented
adapter behavior. Credentials and OAuth configuration contents are never added
to the approval record. Core rechecks the actual selected environment and Run
Book configuration before uploading.

The guard accepts the registered `cpqSetupAssistantInitialize`,
`setupAssistants`, `CompanyProfiles`, and `CPQUsers` DAT sections only. It
rejects mixed stages, unrelated sections, unsupported directives, generated
administrator identities, unresolved placeholders, and child rows in a final
submission. Parent final submission allows only `Status=SUBMITTED`, discovered
`Name`, and the registered transport fields `RestAction`,
`REST-Framework-Version`, and `Content-Type`. Company Profile updates require
the discovered `CompanyProfileId`. Current Core metadata remains authoritative:
if its validated layout cannot satisfy these guards, stop with a catalog or
metadata blocker; do not guess fields or bypass the wrapper.

## Preview, approve, execute

The `preview`, `approve`, and `execute` commands take the same `--proposal`, `--preflight`, `--task-envelope`,
`--manifest`, and `--project` arguments. The manifest path must be in system
temporary storage outside the repository and project; its parent directory
must already exist. The project must already exist at `project/{project_id}`.
Use the normal routed project workflow to create it if needed.

1. At the routed read-only preparation step, run `preview --task-input
   <private-task-hook-input.json> --properties <selected-properties>
   --run-config <selected-runbook-config>`. It validates live registration,
   complete current state/LOVs and recomputed Task Hook readiness before it exclusively creates the
   `--manifest` file with mode `0600`; an existing path is rejected. It returns
   `bindingSha256`, `archiveSha256`, nonce, expiry, and redacted summary without
   printing the full manifest. Present the existing Data Loader approval preview with
   the exact environment, stage, business changes, administrator set, and
   immutable artifact. Associate that preview with this binding fingerprint.
2. After the user's explicit approval for that preview, run `approve
   --confirmed --reviewed-binding <bindingSha256> --actor <approval-attribution>
   --approval-record <private-temporary-path>`. This is the single approval
   interaction for the stage. `--confirmed` records authorization already
   received; it must never be inferred from readiness, an earlier stage, or an
   unqualified prior approval. A changed binding is rejected. The manifest expires
   900 seconds after preview; preview-only `--ttl` can shorten that period.
   Approval preserves the preview's nonce and expiry; it never extends validity.
   Retain the returned nonce
   and binding fingerprint, not raw proposal data, in the durable handoff.
   Supply a nonempty actor attribution from the approving interaction; do not
   invent a default or claim the value is independently authenticated. The
   guard validates the attribution's shape and binds it to the approval record,
   but relies on the workflow operator to record actual consent. Fusion
   credentials, OS identity, and an actor value alone are not approval.
3. Optionally run `execute --nonce <nonce> --approval-record <same-path> --dry-run`. It checks binding, expiry,
   prior use, reconciliation, and any existing target lock locally without
   consuming approval, acquiring a lock, or calling Fusion. It does not perform
   the live final-state check, validate credentials, or replace Core preflight.
4. Run `execute --nonce <nonce> --approval-record <same-path>`. Pass `--properties` and `--run-config` only
   for the already selected Core configuration. Core rechecks the configured
   environment and Run Book context. The wrapper snapshots the checked artifact
   and envelopes into a private temporary directory and commits consumption of
   the nonce. For `SUBMIT`, this same transaction also acquires the target lock;
   the live final-state check below must pass before calling Core
   `upload_approved_preflight` once. The original
   approved artifact/envelopes remain available for reconciliation.

Approval creates a separate canonical payload with schema version
`cpq-approval/1`: `manifestSha256`, exact `taskCode`/`taskName`, `archiveSha256`,
full `finalData`, normalized `target`, ordered `operations`, `executionSettings`,
`actor`, actual `approvedAt`, and the manifest's unchanged `expiresAt` and
`nonce`. `approvedAt` is captured when approval is recorded; it is not preview
`createdAt`. The full record is written exclusively with mode `0600` to the
private temporary `--approval-record` path. Its SHA-256 is persisted alongside
the existing approval ledger and returned as `approvalSha256`; actor and raw
payload values are not stored in the project ledger or printed by the CLI.

Before execution, verify that payload against the manifest, ledger fingerprint,
actual approval timestamp, expiry, and nonce. Missing or modified records stop
before handoff without consuming approval. If record persistence fails after
approval was recorded, stop and create a fresh preview and approval; do not
delete the ledger entry or regenerate a record with a different approval time.

For example, from this skill directory, with synthetic paths:

```sh
python3 scripts/cpq_data_loader_guard.py preview \
  --proposal /private/tmp/cpq/proposal.json \
  --preflight /private/tmp/cpq/preflight.json \
  --task-envelope /private/tmp/cpq/task.json \
  --task-input /private/tmp/cpq/task-input.json \
  --manifest /private/tmp/cpq/manifest.json \
  --project /path/to/FDOS/project/example
```

Use the same arguments for `approve` and `execute`, adding the flags above.
Both commands reload the same manifest and compare its prepared inputs with
the current proposal, preflight, Task Validator preview, and ZIP operations.
Existing approvals from earlier manifest or approval-record versions cannot authorize
this path; create a new manifest and obtain fresh approval without deleting
the existing ledger or its consumed-nonce history.
Approval/nonces are held in the fixed project ledger
`state/cpq-setup-assistant/approvals.sqlite3`, rather than a caller-selected
ledger file. Atomic SQLite consumption prevents concurrent or later reuse.
Never delete or replace the ledger to recover an approval. A failure or crash
after consumption leaves that approval spent, even if no upload was completed.
There is no automatic mutation retry. The CPQ callback adapter blocks Core's
routing-changing fallback; a new attempt requires reconciliation and fresh approval.

## Final-submission reconciliation

After initialization is accepted, retain its private manifest/approval and run
`reconcile-initialization --project <project> --manifest <initial-manifest>
--approval-record <initial-approval> --properties <selected-properties>` only
on the explicit completion continuation. This verifies its exact recorded job,
zero errors/pending records, eligible assistant status and one Company Profile.
An unresolved initialization blocks later mutations.

After the child import was attempted, run the guard's `reconcile` command.
It first verifies the exact recorded request ID, UCM content ID and approved
upload name completed successfully with zero errors and pending records. It
then compares the full expected company business state and administrator set
against the pre-import baseline plus approved changes. Unexpected users,
changed existing identities, missing users and changed retained company values
block reconciliation. A successful receipt clears only that earlier-stage
pending marker; it never releases a final-submission lock.
This is the declared post-import read-only step. It uses Core's standard Fusion
REST client and OAuth helpers to GET the existing `resolve_cpq_setup_assistant_record`
lookup from `ora_reference_lookups.md` using its declared complete-child
verification path: read the fixed assistant identity, page CompanyProfiles and
CPQUsers, then recheck assistant identity/status. Each GET uses `onlyData=true`,
`REST-Framework-Version: 9`, and a 30-second timeout. It uses
standard Fusion scope/cache, not the CPQ service-specific client. The configured
environment must match the approved child target before authentication or GET.
Permit only the standard client's one cached-token refresh on 401/403; do not
poll or retry transport failures. No arbitrary endpoint or mutation is accepted.

Use the approved child manifest and its approval record, even if their original
execution approval has since expired. Reconciliation verifies the historical
approval and requires its nonce to have been consumed by the latest child-import
attempt for this target. It does not authorize another upload.

```sh
python3 scripts/cpq_data_loader_guard.py reconcile \
  --project /path/to/FDOS/project/example \
  --manifest /private/tmp/cpq/child-manifest.json \
  --approval-record /private/tmp/cpq/child-approval.json \
  --reconciliation /private/tmp/cpq/reconciliation.json
```

The command compares actual response contents against every approved child
operation. Require the discovered assistant Name to match the approved target
and Status to remain `SETUP_NOT_DONE`. Require exactly one Company Profile
whose `Id` (or `CompanyProfileId`, when returned) matches the approved profile
identity. Compare every supplied company business field. For `EXISTS` and
`EXISTS_WITH_BU`, an approved Legal Entity selection may cause Fusion to
populate a previously blank `Addressline`, `Country`, or `TaxRegNumber`; accept
only that blank-to-populated server derivation. Reject replacement of a retained
value, derivation without an approved Legal Entity change, and every other
unapproved Company Profile change. Require at least one
current CPQ administrator, unique email identities, and exactly one matching
record for every approved administrator; compare every supplied administrator
business field, including first name, last name, and email. Existing additional
administrators are retained. Exclude only the known transport fields and the
already-checked Company Profile routing ID from business-value comparisons.
Do not assume that differently named or transformed response fields are equal.

Both expanded collections must include `items` and explicit `hasMore=false`;
any reported count must match. Missing comparison fields, truncated/paginated
results, duplicate/ambiguous identities, missing administrators, changed values,
unknown response shapes, or unreadable responses block submission. If the
existing lookup returns only user IDs rather than required verification fields,
report a catalog/lookup-contract gap and stop. Do not invent another endpoint,
accept a manual success assertion, or silently skip unverifiable values.

Only successful comparisons generate a versioned `cpq-reconciliation/1`
receipt. It contains the consumed child nonce and manifest fingerprint, target
fingerprint, actual observation time, Company Profile and CPQ-user response
fingerprints, assistant identity/status fingerprint, and verified result. The
ledger stores its fingerprint and current receipt reference. Raw response
contents remain in memory; do not persist them to the project. The receipt is
written exclusively to the protected temporary `--reconciliation` path.
Caller-supplied timestamps, response hashes, and `allOperationsVerified=true`
alone are never accepted as evidence.

A new reconciliation attempt supersedes the previous receipt immediately, even
if the new read or comparison fails. A newer child-import attempt also
invalidates an old receipt. Before recording success, recheck the latest child
attempt and ensure that another reconciliation did not supersede the read.
Receipts are usable for at most 900 seconds after observation; expiration at
preview, approval, or execution blocks submission until a new reconciliation,
final preview, and separate approval are completed. Never refresh evidence
silently under an existing final-submission approval.

After successful reconciliation, prepare the final parent source with only
`Status=SUBMITTED` as the business change and the confirmed assistant routing
identity when required. Keep its target identical to the reconciled child
target. Run final `preview`, `approve`, and `execute` with the same generated
`--reconciliation` receipt. The guard injects the verified receipt into the
final proposal's `rediscovery` field and fingerprints it in the new final
manifest; a conflicting caller-supplied value is rejected. The final manifest
must be created after observation. Request its own approval as usual; a child
approval cannot authorize final submission. These commands verify the receipt
against the ledger at every gate. Final live execution additionally performs
the explicitly declared pre-submission read below; it never updates the approved
receipt or substitutes a new manifest automatically.

Retain the child manifest and approval record in protected temporary storage
until reconciliation succeeds. They are required to compare the full approved
operation set. Clean them up after their reconciliation purpose is complete;
retain only permitted hashes, statuses, and external IDs in the project.

## Atomic target locking and final-state check

Projects in one checkout share the fixed pillar-local registry
`.runtime/submission-locks.sqlite3`. The skill's local `.gitignore` excludes
this runtime directory; it contains hashes, nonces, phases, and timestamps only.
Do not select another registry or remove it to retry. The guard attaches it to
the project approval database and requires SQLite DELETE rollback journals with
FULL synchronization. This supports atomic commits across the project ledger
and shared registry through SQLite's super-journal on a local filesystem;
unavailable or incompatible storage blocks execution rather than falling back.
During execution, one `BEGIN IMMEDIATE` transaction verifies approval, rejects an existing target
submission lock, acquires that lock for `SUBMIT`, and consumes the nonce. The
lock key is the normalized Fusion origin plus the declared assistant resource
path; changing the environment label, profile ID, or other proposal metadata
cannot evade the lock. Different approvals for the same target cannot both
proceed. Once the lock exists, other mutation stages for that target are also
blocked before handoff. Dry runs neither lock nor consume approval.

After committing the lock in phase `checking`, live submission invokes the same
Core read-only discovery adapter used by reconciliation. Validate complete
Company Profile/CPQ-user collections, the confirmed identities, and eligible
assistant status. Compare their exact canonical fingerprints and the assistant
identity/status fingerprint with the approved reconciliation receipt. Changed,
missing, incomplete, or unreadable state blocks the mutation. Do not refresh
evidence silently under that approval. Its nonce stays consumed and the lock
becomes `precheck_failed`. Obtain a fresh reconciliation, final manifest, and
separate approval after the recovery gate below.

Immediately before Core handoff, recheck manifest expiry, receipt freshness,
and receipt supersession. Atomically confirm lock ownership and change its
phase to `handoff`. A lost/recovered lock prevents the original process from
continuing. The lock remains after accepted initiation (`accepted`), an error
or timeout (`uncertain`), or a crash (last committed phase, possibly `handoff`).
Do not automatically release it on elapsed time, process exit, or a fresh nonce.

On opening a project, the guard imports retained legacy project-local locks
from this checkout before proceeding. It retires the current project's local
lock table only after import; other projects are read-only until they next open.
Conflicting legacy owners block migration. Never discard an uncertain legacy
lock. Stop older guard processes before upgrading; they do not use the shared
registry.

This guards concurrent submissions across projects using this checkout's
registry. Separate checkouts/hosts, generic Core callers, and external Fusion
clients are not coordinated by this local lock. The final read detects state drift since
approval but cannot prevent an external change between the GET and mutation;
the current Data Loader route has no server-side conditional-version contract.
Do not claim transactional protection against those external changes.

## Explicit submission recovery

On a user-requested recovery, run:

```sh
python3 scripts/cpq_data_loader_guard.py recover-submission \
  --project /path/to/FDOS/project/example \
  --manifest /private/tmp/cpq/final-manifest.json \
  --approval-record /private/tmp/cpq/final-approval.json
```

The guard validates the consumed historical approval, its record, and lock
ownership. Only phases `checking` and `precheck_failed` are eligible: they prove
that this attempt has not entered Core handoff. Recovery reads current Fusion
state through the declared adapter and requires matching setup identity,
`SETUP_NOT_DONE`, and complete, unambiguous Company Profile/admin state. A
second atomic check releases the lock only if its owner and eligible phase
still match. If the original process enters handoff during that read, recovery
fails and retains the lock. A suspended precheck process whose lock was released
cannot resume into handoff. The release invalidates the old reconciliation;
the old nonce remains consumed, and new reconciliation/manifest/approval are
mandatory before any new submission.

For `handoff`, `accepted`, or `uncertain`, there is no automatic release path.
Even `SETUP_NOT_DONE` alone cannot prove that an asynchronous Data Loader job
will not apply the submission later. Retain the lock and use the existing
user-requested Data Loader result/status and CPQ status workflows to investigate
the identified attempt. If safe retry cannot be established through the
declared workflow, report a blocker; never delete the lock/ledger or use another
project as a workaround. Preserve final manifest/approval records in protected
temporary storage while pre-handoff recovery is still needed.

## Read-only inspection of an uncertain submission

On an explicit user status/recovery request, use `inspect-submission` with
`--project`, the attempted final `--manifest`, and its `--approval-record`.
The guard retains returned `RequestId`/`ContentId` values after initiation and
any Core-provided `content_id` on failure. It accepts no caller-selected job ID.
Missing IDs, a missing matching lock, or invalid historical approval blocks
the lookup rather than guessing which job to inspect.

This step uses Core's Data Loader status identifier/query contract and standard
read-only client to GET the recorded `dataLoaderDataSets` request once, then
reads the declared CPQ assistant status once. Require the configured target to
match the approved target and the returned data set to match the recorded ID;
missing, ambiguous, or incomplete results block. There is no polling, mutation,
log download, or automatic retry beyond the standard cached-token refresh.
Persist only validated external IDs, bounded status codes, timestamps, and
response fingerprints in the project's `submission_status_checks` table.

The report always retains the target lock and returns `releasePermitted=false`,
even for a terminal-looking status. Current Core/Fusion contracts do not prove
that no pending side effect can still apply, so post-handoff release remains an
explicit capability blocker. The command supports investigation, not an unsafe
retry authorization.

## Persistence, failures, and trust boundary

The ledger contains only hashes, stages, timestamps, and nonce identifiers,
including the separate approval-record and reconciliation fingerprints and
submission lock target hashes, owner nonces, phases, and timestamps. Validated
external request/content IDs and sanitized status-check records are also retained.
Keep source ZIPs, raw previews/proposals, routing identities, and discovery
responses in protected temporary storage outside tracked files and project
artifacts. Before execution, retain the exact canonical manifest and approval
record (including claimed actor attribution) in the separate owner-private recovery store.
Temporary execution snapshots are deleted on normal exit; retained recovery
evidence follows the closure rules below. Persist
sanitized run results, external job identifiers, error classifications, and
token usage through the skill's existing project workflow; do not copy raw Core
errors or payloads into those records.

Local validation returns nonzero before handoff on a blocker. An execution
failure returns nonzero and never restores approval. Stop and reconcile using
the existing failure workflow before proposing remaining work. Retain the
original evidence for all outstanding workflows. Before consumption, the guard
retains the exact manifest/approval in protected local recovery storage. Only
then may temporary copies be cleaned up; accepted initiation alone never permits
deletion of the retained evidence. See Durable recovery evidence below for
attempt-ID lookup, migration of older records, and operational closure rules.

These checks enforce binding and replay prevention within the declared CPQ
workflow under explicit local approval. The actor is unverified attribution;
the workflow operator is responsible for obtaining actual user consent for the
exact manifest. These checks do not protect against a caller who can rewrite
the local ledger or bypass the wrapper. ATEAM-1461 recommendation 3 remains
unmet. The workflow agent must also invoke the declared reconciliation step.
Reconciliation evidence is generated from Core client responses, not accepted
as a caller declaration. Core files and generic Core callers are unchanged.

## Release validation

Ship all CPQ `scripts/*.py` dependencies and this reference with `SKILL.md`.
Deliver the complete focused test source/results tied to the shipped commit;
if the release excludes `tests/`, include them in the agreed Security evidence
package and verify the release source against those tests. A documentation-only distribution is incomplete.
Run this command from the repository root against the release candidate contents:

```sh
python3 -m unittest discover -s pillars/cx/configure-price-quote/company-profile/cpq-setup-assistant/tests
```

The behavioral coverage in `tests/test_cpq_data_loader_guard.py` includes:

| Requirement | Test |
| --- | --- |
| Company/admin substitution, added/removed admins, reordered source operations | `test_rebuilt_company_admin_and_reordered_archives_reject_old_approval` |
| Changed target and approval-bound fields | `test_every_binding_change_blocks_before_core` |
| Used approval and concurrent replay | `test_valid_child_handoff_uses_exact_bytes_and_core_approval`, `test_concurrent_replay_calls_core_only_once` |
| Cross-stage reuse | `test_submit_requires_fresh_complete_target_bound_reconciliation` |
| Stale rediscovery | `test_old_receipt_and_manifest_predating_observation_block_submission`, `test_changed_fusion_state_blocks_handoff_and_recovery_requires_new_approval` |
| Exact unchanged staged execution | `test_exact_unchanged_three_stage_execution` |

The unchanged sequence checks exact archive bytes at each mutation adapter call,
three distinct approvals, consumption before handoff, and refusal to execute a
stage twice. Rebuilt substitution cases regenerate the ZIP and its preflight and
preview, then verify that the old approval cannot reach the upload adapter.
Tests use explicit local approval and synthetic Fusion responses; passing them
does not establish authenticated approval or live integration success. Every
live stage must enter through the guard; never call Core directly to bypass it.

## Integrated write boundary and earlier-stage tracking

`cpq_execution.py` wraps unchanged Core upload and initiation callbacks. It checks
exact immutable bytes, filename, target, UCM account, Run Book/task routing and
all initiation options; it rejects a second initiation, including Core's fallback
that removes Run Book fields. Both writes use one frozen token and cannot refresh
or replay a mutation. The durable guard rechecks expiry, consumed approval,
registration, readiness, complete state and lock ownership at the upload boundary.
These checks preserve the single explicit approval interaction per stage and
do not independently authenticate its actor attribution.

A per-target process lock serializes all three mutation stages in this checkout.
The shared SQLite registry also records pending initialization/child attempts in
the same transaction that consumes the nonce. Their markers survive process exit
and block a later mutation, even under a new approval, until the exact job and
outcome are reconciled. Missing authoritative IDs or uncertain failure remains a
blocker; do not delete markers or replay an earlier import. Generic callers,
separate checkouts and independent hosts are outside this local coordination.

The existing `submission_jobs` table now retains validated request/content IDs
for every stage. No raw source filename, company record or administrator record
is added to the project ledger. Exact recovery evidence is stored separately in
owner-private storage outside the repository and project, as described below. Initialization reconciliation stores sanitized
fingerprints in the existing status-check table. Existing final-submission
recovery/status behavior and retained locks remain in place.

Version 3 is required for all new previews/approvals/execution. Version 2 manifests
may be used only for consumed-record status and pre-handoff recovery after their
exact ledger/approval fingerprints match; they cannot authorize a new write.
Rebuild unexecuted previews through the new live-validation step. Do not discard
old ledgers or uncertain locks during upgrade; stop older guard processes first.

The parser and live validator enforce registered fields, supported stage actions,
company branches, unique emails, exact current LOV membership and the documented
ASCII company identifier. Semantic Address Line 1 collection remains a required
Task Hook/skill validation responsibility; no heuristic postal-address parser or
new resource-provisioning endpoint is inferred by this adapter.


### Pillar functional recovery and existing configuration

The pillar guard supports these read-only commands at the declared verification/recovery step. They do not authorize any new mutation or replace the explicit approval required for each new stage:

- `recover-prewrite --project ... --manifest ... --approval-record ... --properties ...`: release only a consumed attempt with an explicit durable `checking` phase, no remote IDs, unchanged assistant identity and eligible status. It holds the same target process lock as execution. The write callback atomically changes the phase to `write_started` before upload. Missing legacy phase, any write-boundary crossing, or remote identifiers prevent release. The nonce remains consumed; rebuild evidence and obtain fresh approval. Crash after marking the write boundary remains uncertain even if no upload occurred.
- `reconcile-existing --project ... --manifest ... --proposal ... --preflight ... --task-envelope ... --task-input ... --reconciliation ... --properties ... --run-config ...`: validate an exact final-only artifact and current ready configuration when no child write has been attempted. The manifest argument reserves the later preview path; this command creates only the receipt. Supply that receipt to the usual final preview, approval and execution commands. A known child write, including a completed or partial one, requires ordinary full child reconciliation. Explicitly released zero-write attempts are eligible. Receipts bind the target, source, route, state, freshness and current receipt identity.
- `inspect-child-outcome --project ... --manifest ... --approval-record ... --properties ...`: assess the latest consumed child attempt without resubmitting anything. Each operation is reported as matching approved values, not observed, or uncertain; no business values are persisted in this diagnostic. Missing or pending completion evidence and partial state return a nonzero CLI status. The pending marker is retained even when observations match; use full reconciliation to advance. An absent administrator is not proof that the original job cannot create it later.

Registered `Content-Type` and `REST-Framework-Version` columns are accepted for final submission and child routing. Live registration must independently include them; they do not count as Company Profile business changes. Final submission still permits only the approved `SUBMITTED` status mutation.

Explicit local approval enables the guarded pillar route without independent approving-user authentication. ATEAM-1461 recommendation 3 remains unmet. These recovery commands do not clear an uncertain write or establish cross-host/non-bypassable enforcement. Safe automated retry of remaining partial work requires authoritative original-job finality and idempotency; it is not enabled by these commands.


Review corrections: latest-import selection excludes only explicitly released zero-write attempts; recovery invalidates prior child receipts so fresh reconciliation remains mandatory. Missing legacy phases and uncertain writes remain blocking. New reconciliation fingerprints normalize record order and omit REST navigation links without reordering approved operations. Older receipts with different fingerprints must be regenerated, never rewritten under an existing approval.

The supported pillar transport values for non-initialization rows are `application/json` or `application/vnd.oracle.adf.resource+json` for `Content-Type`, and `9` for `REST-Framework-Version`. Each supplied column must also exist in live registration. Required transport values must be supplied explicitly; the guard neither inserts defaults nor accepts arbitrary strings. Initialization retains its action-specific content type. Registrations requiring a different value remain blocked pending an explicit contract update.

## Durable recovery evidence

Before consuming an execution approval, the guard atomically retains the exact
manifest and approval record in the owner-private directory
`~/.local/state/fscr/cpq-setup-assistant/evidence` outside the repository and
project workspace. The directory is mode 0700 and records are mode 0600;
symlinks, unsafe permissions and conflicting records are rejected. The store
requires POSIX secure-file primitives; an unsupported or unavailable store
blocks before approval consumption or upload. Snapshots may contain business
values; never copy them into project artifacts, diagnostic output or source
control. No credential/configuration files are copied into this store.

The attempt ID is the original approval nonce. It is a locator, not an approval
credential. The following historical operations accept `--attempt-id <nonce>`
instead of `--manifest` and `--approval-record`: `reconcile`,
`reconcile-initialization`, `inspect-child-outcome`, `inspect-submission`,
`recover-prewrite`, and `recover-submission`. They recheck the consumed ledger
entry and both exact fingerprints before any external read or local recovery.
An expired execution approval can support historical verification, but neither
the snapshot nor the attempt ID grants a new mutation, restores a nonce, or
releases an uncertain write. `preview`, `approve`, and `execute` cannot use
`--attempt-id` as an alternative authorization path.

Examples at the declared completion/status step:

```sh
python3 scripts/cpq_data_loader_guard.py reconcile \
  --project <project> --attempt-id <child-nonce> \
  --reconciliation <new-private-receipt-path> --properties <selected-properties>
python3 scripts/cpq_data_loader_guard.py inspect-submission \
  --project <project> --attempt-id <submission-nonce> \
  --properties <selected-properties>
```

For attempts created before automatic retention, keep the original files and use
`retain-evidence --project <project> --manifest <original-manifest>
--approval-record <original-approval>` before removing any temporary copies.
This local command validates the consumed ledger record and persists an exact
snapshot; it performs no Fusion calls. Missing original evidence cannot be
reconstructed from hashes: stop and report the missing-evidence blocker.

Cleanup applies to private execution ZIP/task/preflight copies, not the retained
recovery snapshot. Do not delete a snapshot while its stage, dependent final
submission, status inspection, or recovery remains outstanding. A completed
child load can still need fresh reconciliation before final submission, so
reconciliation success alone is not a cleanup point. There is no automatic purge.
Manual archival/removal belongs to the operational closure process only after
all dependent verification/inspection is finished and required audit retention
is satisfied. Keep consumed nonce records, approval hashes and unresolved locks;
never delete them as a way to retry. This store provides recovery durability,
not authenticated approval authority or cross-host coordination.


`inspect-submission` reads the exact recorded load and a single fixed parent
status record. It does not depend on complete child collections or require a
stable parent status across pagination; status may legitimately change while a
job runs. This diagnostic always retains the submission lock. Complete paginated
child verification remains mandatory for reconciliation and mutation eligibility.
