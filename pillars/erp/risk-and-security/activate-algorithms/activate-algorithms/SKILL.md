---
skill_id: "erp.risk-and-security.activate-algorithms.activate-algorithms"
name: "Activate Algorithms"
description: "Identifies active Risk Management processes, previews or publishes algorithms from the approved Reference Code workbook for the confirmed process subset, and lists environment-wide published algorithms through an explicit read-only inventory mode."
layer: "pillar"
pillar: "ERP"
offering: "Risk and Security"
functional_area: "Activate Algorithms"
functional_area_code: "ORA_GTG_ACTIVATE_ALGORITHMS"
task_code: "ORA_GTG_ACTIVATE_ALGORITHMS"
task_name: "Activate Algorithms"
parent_skill_id: "erp.risk-and-security.activate-algorithms"
available_flag: "Y"
export_import_supported_flag: "UNKNOWN"
csv_export_import_supported_flag: "UNKNOWN"
dataloader_import_mode: "REST"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "Risk Management implementation"
version: "0.3.1"
inputs:
  - "confirmed active-process handoff produced by this skill's internal Identify Active Modules phase (mock permitted only for preview development)"
  - "approved Reference Code allow-list workbook"
  - "explicit customer approval of the previewed target changes for live publication"
outputs:
  - "readable publication preview or live result"
  - "selected, published, already-published, skipped, and failed algorithms"
  - "internal immutable approval record and durable audit report"
  - "runbook_lifecycle_result"
  - "durable project run and token-usage records"
uses_core:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
depends_on:
  - "erp.risk-and-security.assign-initial-users.assign-default-process-owners"
  - "erp.risk-and-security.activate-algorithms.activate-audit-policies"
  - "shared.implementation-planning.fsm-set-optin.fsm-set-optin-offerings"
  - "shared.implementation-planning.fsm-set-optin.fsm-set-optin"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run_and_artifact"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
state_updates:
  - "validation_results"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/erp/risk-and-security/activate-algorithms/activate-algorithms/current/"
    versioning_policy: "append-only"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
side_effects:
  - "Preview — GET-only BOSS reads and project artifact writes."
  - "Live — ordered, approval-gated BOSS context bulk POSTs, followed by bounded verification reads."
required_privileges:
  - "BOSS read access to provided algorithms and algorithm contexts"
  - "BOSS create/update access to algorithm contexts for live publication"
---

# Activate Algorithms

## Purpose

First identify the active Risk Management processes, then select **provided
algorithms** whose exact reference code is in the approved allow-list and
whose process association is in the confirmed process values, and
publish them with **Export File** as the required result action. Process
identification is an internal, read-only phase of this catalog task. It is not a separate
Fusion Setup task, and no local Python implementation is invoked for it.

## Usage

Use this skill when planning, sequencing, or validating the **Activate
Algorithms** setup task under **Activate Algorithms**.

### List published algorithms

Use the explicit read-only inventory mode to list every currently published
Risk Management algorithm in the selected environment. This inventory is not
limited to the confirmed activation-process scope or the reference-code allow-list, and
it never prepares or performs an algorithm update.

```text
python pillars/erp/risk-and-security/activate-algorithms/activate-algorithms/scripts/execute.py \
  --project-id <project> --environment <environment> --published-inventory \
  --request-plan-output <next-core-request.json>
```

The local planner retrieves all paginated pages through the Core BOSS client,
then renders all results inline when there are at most 25. For a larger result,
it returns a link to the readable inventory register. Persist the internal
audit record and token-usage record in either case.

## Audit policy prerequisite

Strongly recommend completing and verifying
[Activate Audit Policies](../activate-audit-policies/SKILL.md) for the same
environment before beginning this skill. A planned backend validation is
expected to reject an algorithm activation when the required audit policies are
disabled.

This is a sequencing recommendation, not a claim that the backend validation
already exists. A developer may still perform the read-only identification and
preview phases to diagnose the environment, but must not describe the
environment as ready for algorithm publication while Audit Policy verification
is absent.

## Core execution delegation

`scripts/execute.py` is a local request planner and Core-result interpreter.
It never performs HTTP, OAuth, token-cache, retry, or Core-client work. When a
required BOSS result is absent, it writes one Core request manifest for every
independent GET available in the current read phase and stops. Execute every
manifest request through `core.fusion-api.rest-api-client`, then rerun the
planner with each saved result as `--core-response <request-id>=<result.json>`.
Additional pages and later read phases remain dependency-ordered. Live
publication may contain up to three approval-gated, resource-specific BOSS
`$bulk` POSTs for the complete approved set: create missing Access contexts,
publish Transaction contexts, then publish Access parent contexts. Execute only
the next request emitted by the planner; do not split a resource batch into one
write per algorithm or retry a bulk POST. For an existing algorithm context,
read `$context.etag` from the Core GET body and place it unchanged in that
item's `$context.etag` field. After the first two batches, obtain fresh Access
and parent context evidence before preparing the Access parent batch. When the
planner emits a mutation request, it also writes an adjacent `*-body.json` file
containing only that request's body. The Core client must use that body file for
the mutation; the request manifest remains orchestration evidence and is never
an HTTP body. The mutation manifest also contains `core_client_request`; invoke
the BOSS client with its explicit `method` (`POST`), `endpoint`, and `body_file`.
Never rely on the client's default method for a mutation.

## Customer-facing behavior

The skill publishes only algorithms that are both in the approved Snapshot
workbook and associated with an active process. It presents a grouped preview
of algorithms to publish and labels an unconfirmed setup as not published. It
does not publish anything until the customer approves the complete proposed set.

Follow the offering [Consultant Interaction Contract](../../references/consultant-interaction-contract.md).
In the publication chat preview, group only proposed publications by business
process. For each process, show one heading naming the process and its full
proposed count, followed by a Markdown table with exactly two columns:
`Algorithm | Reference`. Show the first **10 algorithms per process** in that
table, regardless of the total number of processes or proposed algorithms.
When a process has more than 10, follow its table with `… N more to publish in
<process>.`, where N is that process's remaining count. Do not add Business
process, Status, or Action columns to these tables; the process heading and
section title supply that context. Do not show a Business summary table.
Use this table shape for each process:

```markdown
### <Business process> — <total> algorithm(s) to publish
| Algorithm | Reference |
| --- | --- |
| <Readable algorithm name> | <AL.#####.ORA> |
```

Keep a complete, uncapped actionable list in the same process-grouped format
available on request before approval; when asked for a named process, return
all proposed algorithms for that process. An algorithm associated with multiple
processes appears under each process, but counts only once in the approval
total. Label algorithms whose current state cannot be confirmed as **Not published**.

Complete all internal retrieval batches before showing the consultant any
algorithm-preview status. Never expose page counts, offsets, continuation
signals, request manifests, Core-result prompts, or other collection mechanics.
An incomplete internal retrieval is not a consultant decision point. Continue
the declared read-only work internally; if it cannot be completed, explain the
business impact and safe next action without technical detail.

When the runner returns the completed preview, return its complete
customer-facing Markdown output in chat without omissions or replacing it with
a summary. Include every per-process heading and table,
all “N more” indicators, and the approval question. Do not present an interim
collection message as the completed preview.

Present only readable information to the customer: process name, algorithm name
and reference code, intended business outcome, current state, and clear
exceptions. A requested large complete register may link only to its
consultant-facing Markdown table. Do not show report JSON, diagnostic paths,
checksums, plan digests, HTTP terminology such as POST or PATCH, payloads,
endpoints, or other implementation controls in the customer-facing response.
Persist those details internally for audit and approval integrity.

When the preview contains proposed publications, ask plainly: **"Do you approve
publishing these [count] algorithms in [environment]?"** On explicit approval,
the workflow supplies the internally retained plan digest to live mode. Never
ask the customer to copy, provide, compare, or approve a digest. Ask for further
details only when an algorithm mapping is ambiguous, a required input is missing,
or an execution exception needs a customer decision.

An algorithm configured for a review task is preserved. Publish Snapshot
Algorithms never replaces `REVIEW`; the later Review Task Configuration
workflow owns those changes. A newly created context uses **Export File**; an
existing context retains its current result action while its publication mode
is updated. An already published provided algorithm or context is excluded from
the proposed publication tables and is not changed by this workflow.

## Inputs

### Internal phase: Identify Active Modules

This is the first, read-only assisted phase of **Activate Algorithms**. Complete
it for the selected project and environment before evaluating an algorithm. It
owns process discovery, semantic inference, user agreement, and the confirmed
active-process handoff. Do not ask the customer to provide a Level 2 process
list or a process-to-capability mapping.

This phase is intentionally runner-free: it orchestrates the declared Core and
Shared skills and must not add a pillar-local executable, HTTP transport, OAuth,
token handling, or retries. Do not start `scripts/execute.py` to initiate this
phase; that publisher consumes the confirmed handoff produced here.

#### Preflight

Require an initialized `project/{project_id}` workspace and an explicitly
selected Fusion environment. Every delegated result must identify that same
environment. Preview gathers evidence and creates an unconfirmed proposal;
confirmation reviews that one preview without repeating reads. This phase never
modifies Fusion setup, offerings, features, process ownership, or algorithms.

After this preflight, the canonical process-catalog inventory and root-offering
inventory may run concurrently because they are independent GET-only Core
operations. Complete the root-offering inventory before requesting any
selected-choice evidence.

Do not automatically invoke **Activate Audit Policies** during this phase. Its
verified same-environment result is a readiness fact for publication, not a
reason to create extra Audit Setup inventory, status, or update calls. This
phase may still run its own GET-only discovery while audit-policy readiness is
pending.

#### Resolve the canonical process catalog

Delegate this paginated BOSS read to `core.fusion-api.rest-api-client`:

```text
GET /api/boss/data/objects/ora/riskMgmtRisk/core/v1/referenceDataValues
```

Start with:

```text
$filter=referenceCode!='SOURCE.ORA.ORA' AND referenceCode!='SOLUTION.FND.ORA' AND attributeCode='PROCESSES.ORA'
$fields=valueCode,referenceCode,attributeCode,orderNumber,levelOne,levelTwo,levelThree,description
$limit=200
$offset=0
$sortBy=levelTwo:asc,referenceCode:asc
```

Continue with the same filter, fields, and stable ordering while `hasMore=true`.
Advance `$offset` by the non-empty page size and stop with a
`catalog_or_metadata_mismatch` diagnostic if a page is malformed, an empty page
has `hasMore=true`, or pagination cannot complete. Persist a sanitized complete
source snapshot. `referenceDataValues` is the direct provided
`ReferenceDataValue` business object; do not replace it with the
`allReferenceDataValues` union extraction. Build one canonical process for
each non-empty normalized `levelTwo`: ignore `All Processes`;
retain its `MUL_*` `valueCode`; and, for duplicates, retain only the row whose
normalized `levelOne` equals `levelTwo`. Stop if that selection is ambiguous
or lacks a `MUL_*` code.

#### Obtain selected-capability evidence

Use `core.fusion-api.rest-api-client` for the complete selected-offering
inventory. Retrieve every root-offering page from:

```text
GET /api/boss/data/objects/ora/commonSetup/features/v1/features/$views/availableOfferings
```

Request `featureShortName`, `featureName`, and `enabledFlag` with stable
pagination. For every returned root offering with `enabledFlag=true`, retrieve
every page of:

```text
GET /api/boss/extraction/queries/ora/commonSetup/features/v1/featureSelectedChoices
```

Pass the offering's `featureShortName` and a bounded page size such as
`$limit=200`. A root offering is selected only when its own `enabledFlag` is
true **and** its choices contain the `Yes` choice with `checkedFlag=true`.
`choiceEnabledFlag` means available or selectable; it is not selection
evidence. Stop when any page is malformed, empty while `hasMore=true`,
unauthorized, for another environment, or cannot complete. Preserve offering
names, short names, complete-page evidence, and checked-Yes evidence in the
project artifact. Do not limit the inventory to Risk Management-named entities
or exact process-name matches.

After Core establishes a named selected offering, optional read-only enrichment
may invoke
`shared.implementation-planning.fsm-set-optin.fsm-set-optin-offerings` for that
offering with `--action opt-in --dry-run`. Its declared
`shared.implementation-planning.fsm-set-optin.fsm-set-optin` engine remains a
dependency for target-specific selection interpretation. This enrichment may
preserve additional feature or parent context and refine confidence, but it must
not add, remove, or override the complete Core selection inventory. Missing,
partial, unauthorized, or otherwise unavailable enrichment is a warning only;
Core inventory failure remains blocking.

#### Assess and confirm processes

For every canonical Level 2 process, first assess exact selected offering or
feature matches. Then assess every selected capability semantically: use its
business purpose, product domain, parent context, and Oracle Fusion business
knowledge. Do not rely on shared words alone and do not maintain a static
process-to-offering mapping.

Recommend a process as enabled when at least one selected capability materially
supports the process or a material part of its lifecycle. Record the best
candidate, selection evidence, `direct` or `inferred` basis, `high`, `medium`,
or `low` confidence, and a concise process-specific explanation. Recommend
false only when no selected capability supportably relates to the process.

For calibration, a selected Help Desk capability can support Information
Technology Processes, and Project Execution Management or Project Financial
Management can support Project Management. These are reasoning examples, not a
closed mapping catalog.

Present one review table before confirmation:

| Process | Recommended enabled | Basis | Selected capability evidence | Confidence | Why | User decision |
|---|---:|---|---|---|---|---|
| `<process>` | `true` or `false` | `direct` or `inferred` | `<selected offering/feature, or none>` | `high`, `medium`, or `low` | `<process-specific reasoning>` | `pending` |

This table must include every canonical process and its process-specific
justification. A bullet list, process count, or an unqualified statement that
the selected capabilities support a process does not satisfy the confirmation
gate. Do not request confirmation until this table is visible.

Ask the user only to accept all recommendations or identify rows to change; do
not ask for an offering, feature, or replacement mapping. Record every decision.
After agreement, persist the preview, source snapshots/checksums, decisions,
unconfirmed handoff, confirmed handoff, artifact registration, token usage, and
skill run under this task's current artifact directory. Redact credentials,
tokens, authorization headers, and sensitive errors.

The confirmed handoff is internal, not customer-facing:

```json
{
  "source": "ACTIVE_MODULES_IDENTIFICATION",
  "confirmed": true,
  "environment": "<environment>",
  "active_process_level_twos": ["Order to Cash", "Record to Report"]
}
```

Provide it to the local runner as `--active-modules-handoff`. The runner may
reuse only the newest same-environment confirmed handoff in this task's current
artifact path; it never reads the retired `risk-management` layout. If this
phase cannot create a confirmed handoff, stop before algorithm evaluation.

For development only, `"source": "MOCK_ACTIVE_MODULES"` is accepted for a
preview. The runner refuses mock input in live mode.

### Reference Code allow-list workbook

The skill reads the checked-in [Reference Code allow-list workbook](reference-data/algorithms.xlsx)
directly at runtime. Its `Reference Code` column contains eligible exact
`AL.#####.ORA` values. The runner ignores non-exact cells and fails closed
when the column is missing, duplicated, or contains duplicate exact codes.
A replacement workbook may be supplied with
`--reference-code-workbook <file.xlsx>` when it contains that column.

## Execution

Only after the internal phase creates its confirmed handoff, run the local
publisher from repository root:

```text
python pillars/erp/risk-and-security/activate-algorithms/activate-algorithms/scripts/execute.py \
  --project-id draft_impl_project_2026-08-19 --environment DEV3 --mode preview \
  --active-modules-handoff <confirmed-active-modules-handoff.json> \
  --request-plan-output <next-core-request.json>
```

For a resumed Publisher run only, the runner may reuse its newest matching confirmed
handoff when `--active-modules-handoff` is omitted.

When the runner produces a further internal Core request, the orchestration
continues that read-only work and reruns the publisher with the returned result.
This is not a completed preview and must not end the consultant interaction.
Continue until the runner produces the complete grouped preview table or a
business-facing exception. Do not ask the consultant to help complete internal
data collection. The runner's interim message is workflow progress only; do not
emit it as the turn's final consultant response.

The runner exits with code `2` when it has written a further internal Core
request manifest. Treat that result as `read-only` continuation in the
[Phase Evidence Handoff](../../references/phase-evidence-handoff.md), not as a
preview failure. Execute each declared request through the existing Core client,
save its result with the active run, and rerun the same publisher invocation
with those results. Do not restart active-process discovery, repeat completed
read-only work, seek another consultant decision, or begin a different child
workflow solely because this continuation code was returned.

Preview reads:

1. `providedAlgorithms` — issue one collection query whose
   process predicate is `processDataValue.levelTwo IN (...)` for the complete
   confirmed active Level 2 set. Retrieve every page with `$limit=100` and
   `$sortBy=id:asc`; this is
   one paginated collection stream, not one request per Level 2 or reference
   code. This endpoint is discovery-only: never mutate it. A 403 is an
   authorization blocker; do not retry it or prepare any write.
2. For the allow-listed candidates, read shared and type-specific customer
   contexts in grouped `id IN (...)` requests of at most 100 IDs. Read the
   corresponding provided type-specific settings only for unpublished
   candidates without a customer context. This keeps discovery
   collection-based and avoids per-algorithm reads.
3. Locally match the returned exact reference codes against the approved
   allow-list and retain only returned associations whose expanded Level 2 is
   confirmed active. Treat a provided/base record, shared parent context, or
   typed child context with `modeType: PUBLISHED` as already published and make
   no write. For an unpublished existing context, publish only its mode with
   its current ETag; preserve its configured result action, including `REVIEW`
   and `ISSUE`.

`$en/allAlgorithms` is not a discovery source for activation selection. It is a
union of provided and user-defined algorithms, whereas selection intentionally
operates only on provided algorithms. After a successful live mutation, use it
only as a bounded effective-state verification for the exact changed IDs; it
does not add algorithms to activation scope. The separate **List published
algorithms** mode is the only exception: it uses this endpoint read-only to
produce an environment-wide inventory and never prepares a publication plan.

Lead the readable publication preview with the process-grouped proposed
algorithms, not a business-process summary. Live publication remains
separately approval-gated.

## Live approval gate

Live mode requires:

- an explicitly approved, non-mock handoff returned by the Identify Active
  Modules invocation;
- explicit customer approval for the target environment and plan.

The orchestrator verifies the exact preview internally with its retained digest;
the customer never handles that value.

```text
python pillars/erp/risk-and-security/activate-algorithms/activate-algorithms/scripts/execute.py \
  --project-id <project> --environment <environment> --mode live \
  --active-modules-handoff <confirmed-active-modules-handoff.json>
```

The workflow invokes any internal approval-integrity arguments itself after the
customer approves the readable preview; they are intentionally omitted above.

For the exact BOSS request contract that the runner implements and that was
validated in ENV11, read
[the algorithm-publication API reference](references/boss-algorithm-publication-api.md)
before live execution. It defines the typed bulk payloads, ETag use, bounded
effective-state verification, and stopping condition.

## Exceptions and reporting

Report **Publish** for proposed algorithms, **Already published** for unchanged
published algorithms, and **Published** after verified publication. Report
**Not published** for a rejected algorithm or an algorithm whose setup or
publication result cannot be confirmed. An incomplete or unattributed
execution or verification failure is reported as not published without an
item-level completion outcome. Do not silently select the first result from an
ambiguous reference-code query,
publish an inactive Level 2 process, overwrite an existing result action, or
continue after a failed mutation. Persist redacted run diagnostics, preview or
live report, and token-usage record under `project/{project_id}`.
Return `completed_verified` only after the live publication result is fully
verified, including a verified no-change or already-published result. An
explicit consultant deferral records remaining work and returns `deferred`; a
failed, uncertain, or unverified run returns `blocked`.
