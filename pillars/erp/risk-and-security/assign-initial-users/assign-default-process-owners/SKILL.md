---
skill_id: "erp.risk-and-security.assign-initial-users.assign-default-process-owners"
name: "Assign Default Process Owners"
description: "Proposes Risk Management process owners from verified functional and organizational evidence, then bulk-creates missing owners, selectively bulk-replaces explicitly requested owners, or bulk-resets explicitly requested Level 2 scopes."
layer: "pillar"
pillar: "ERP"
offering: "Risk and Security"
functional_area: "Assign Initial Users"
functional_area_code: "ORA_GTG_RM_INITIAL_USERS"
task_code: "ORA_GTG_ASSIGN_DEFAULT_PROCESS_OWNERS"
task_name: "Assign Default Process Owners"
parent_skill_id: "erp.risk-and-security.assign-initial-users"
available_flag: "Y"
export_import_supported_flag: "UNKNOWN"
csv_export_import_supported_flag: "UNKNOWN"
dataloader_import_mode: "REST"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "ERP Risk Management pillar team"
version: "0.6.7"
inputs:
  - "project_id"
  - "fusion_environment_context"
  - "customer_mapping_documents (optional supporting evidence)"
  - "derived_business_unit_to_process_suggestions (optional supporting evidence)"
  - "process_function_evidence (optional)"
  - "hierarchy_search_parameters"
  - "candidate_role_enrichment_request (optional)"
  - "customer-approved_process_relevant_role_codes (optional)"
  - "approved_owner_decisions (CREATE assigns only unassigned Level 2 scope members; UPDATE or RESET only when explicitly requested per Level 2 process)"
outputs:
  - "customer_owner_candidate_review"
  - "redacted_preview_summary"
  - "risk_management_search_prerequisite_result"
  - "default_process_owner_exceptions"
  - "default_process_owner_operation_receipt"
  - "runbook_lifecycle_result"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "erp.risk-and-security.assign-initial-users"
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.fusion-api.apps-common.profile-options"
  - "core.project-mgmt.project-state-manager"
  - "core.project-mgmt.artifact-registry-manager"
uses_core:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.fusion-api.apps-common.profile-options"
  - "core.project-mgmt.project-state-manager"
  - "core.project-mgmt.artifact-registry-manager"
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
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/risk-and-security/assign-initial-users/assign-default-process-owners/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
applicability:
  industries: ["All"]
  countries: ["All"]
  fusion_releases: ["Current Oracle Fusion Cloud release"]
side_effects:
  - "Reads the Core-managed Risk Management search setting before owner coverage retrieval."
  - "Reads BOSS process, hierarchy, user, and property data, plus bounded Core-managed HCM department and functional-worker evidence."
  - "Optionally reads BOSS Business Unit and worker-assignment data when customer material supplies supporting context."
  - "Optionally reads Fusion HCM candidate details and user-account roles when a consultant requests them."
  - "Writes only redacted project artifacts and a customer-controlled review file in preview mode."
  - "In live apply mode, uses one verified BOSS bulk request per changed root or Level 3 member; CREATE fills only unassigned members, UPDATE replaces only the explicitly named source owner, and RESET removes every existing owner in an explicitly approved Level 2 scope."
required_privileges:
  - "Core-managed search-setting change requires the profile-option value management privilege."
  - "BOSS read access to BusinessUnit, workerAssignmentExtracts, managerHierarchy, User, Worker, seeded Risk process extraction, and ReferenceDataValueProperty."
  - "Future live execution requires the ReferenceDataValueProperty privilege required for the approved BOSS bulk CREATE, DELETE/CREATE, or DELETE operation."
---

# Assign Default Process Owners

## Purpose and strict scope

Execute **Assign Default Process Owners** in the Risk and Security deployment
plan. The normal assignment flow generates customer-reviewable default-owner
proposals for selected Level 2 processes, using functional workforce evidence
first and Business Unit information only as optional supporting context. It
fills only unassigned members in the selected Level 2 scope. A configured
owner remains informational unless the consultant explicitly requests UPDATE
or RESET for that named Level 2 process. The customer approves, rejects, or
edits every proposal before a later live run applies any decision.

## Consultant-facing review and decisions

Follow the offering [Consultant Interaction Contract](../../references/consultant-interaction-contract.md).
Use a compact Markdown table for every owner-coverage and owner decision. The
initial coverage review contains **Business process**, **Current default
owner**, **Current result**, and **Work on this process?**. The candidate review contains **Business process**,
**Proposed owner**, **Recommendation basis**, and **Decision**. The final
approval table contains **Business process**, **Operation**, **Approved owner**,
**Current result**, and **Approval**. RESET rows show **No assigned owner** in
the approved-owner column.

For coverage, a Level 2 row is an aggregate, never a root-row result. Before
showing or refreshing the table, derive its owner names, unassigned members,
and current result from every member in that Level 2 scope. A table that uses
only a root owner, including when a consultant asks to update or re-read the
list, is invalid and must be re-read and re-rendered.

Do not ask the consultant to open, edit, or approve a JSON review file. Their
chat or table confirmation is recorded internally. For an unavailable lookup,
state the business impact, confirm that no owner was proposed or assigned, and
give one safe next action.

## Usage

Use this skill when planning, sequencing, or validating the **Assign Default
Process Owners** setup task under **Assign Initial Users**.

## Required upstream skill

Require the verified coverage result from the parent [Risk Administrator
Assignment Verification](../SKILL.md#risk-administrator-assignment-verification), which **Assign
Initial Users** invokes first for the selected project and environment. It
verifies both that organization coverage exists and that the authenticated user
is ready through Risk Administrator or IT Security Manager access. If the
authenticated user needs access, the parent prepares and verifies the one
explicitly approved Risk Administrator assignment before routing here.

This nested skill is never an independent entry point. When a consultant asks
to run **Assign Default Process Owners** directly, route the request back to
**Assign Initial Users** in `prerequisite` mode. Before any process, owner,
Business Unit, worker, hierarchy, or user read, require current parent evidence
for the same project and environment that records both
`organization_coverage=true` and `runner_access_ready=true`. A pending,
blocked, stale, cross-environment, or incomplete prerequisite result is not
evidence. Keep the parent gate active until it reaches its decision or verified
result; do not start owner discovery in parallel or disclose the internal reason
for the hold. After verification, resume this child as the sole active
workflow.

## Stage 0 — Risk Management search prerequisite

After the parent gate and before any owner-coverage inventory, delegate the
Risk Management search prerequisite to
`core.fusion-api.apps-common.profile-options`. Read the exact profile
definition, its Site capability metadata, and its Site value through that Core
skill. Read [the task-local lookup contract](ora-resource/ora_reference_lookups.md)
before preparing the Core request.

The Site capability is usable only when exactly one Site metadata row reports
that it is both enabled and updatable. The child-level Site metadata is the
capability source for this task; do not infer capability from missing
parent-level flags. Treat a missing Site value or a value other than the
required enabled value as disabled.

When the setting is already enabled, retain only redacted evidence—the
environment, prerequisite outcome, Core request references, and verification
outcome—and continue directly to Stage 1 without a consultant message. Do not
persist the profile code, raw value, endpoint, privileges, or response body in
the project record.

When it is disabled, show only this approval table and wait for a fresh
confirmation:

| Setting | Business impact | Proposed change | Approval |
| --- | --- | --- | --- |
| Risk Management search | Default-owner recommendations cannot begin | Enable the setting for the environment | Pending approval |

Ask: **“Approve enabling Risk Management search for this environment?”** On
approval, have the Profile Options Core skill re-read the Site capability and
current Site value, then create a missing Site value or update an existing
disabled value through its supported route. The Core skill owns the change
selection and execution. This child must not construct, submit, or retry a
profile-option request. Re-read through Core and require the enabled Site
value before beginning Stage 1.

If the profile cannot be read, the Site capability is missing or not
updatable, approval is withheld, the Core change fails, or final verification
does not confirm the enabled setting, stop before owner coverage. State that
Risk Management search could not be confirmed for this environment, that no
default-owner review or assignment was started, and ask the consultant to have
an administrator enable the setting and then resume this task. Do not expose
profile codes, values, endpoints, or privilege mechanics.

## Core execution delegation

Delegate the Stage 0 profile-definition, Site-capability, Site-value, and any
approved Site-value change exclusively to
`core.fusion-api.apps-common.profile-options`. That Core skill owns its
supported create/update choice, its REST client, OAuth, token cache,
transport, and no-retry behavior. This child records only redacted phase
evidence and never imports, launches, or emulates an HTTP or OAuth client for
the prerequisite.

Prepare the exact Business Unit, worker, hierarchy, user, process-property,
and approved owner-assignment requests here, then defer every Fusion and BOSS
execution to `core.fusion-api.rest-api-client`. The Core skill owns selection
and execution of its Python client, OAuth, token caches, transport, retry, and
response handling. This skill and its helpers must not import, launch, or
emulate that client.

Use returned Core results for matching, candidate scoring, approval-plan
construction, verification, and redacted project reporting.

The [Consultant Interaction Contract](../../references/consultant-interaction-contract.md)
governs every consultant-visible message, including commentary. Internal
collection progress is never a consultant outcome. Complete it silently; before
a coverage table, required decision, approval, or genuine business blocker is
ready, do not explain why internal work is continuing. When a progress update
is unavoidable, use the contract's neutral sentence verbatim.

This rule also applies when a read must be retried or cannot continue. Never
explain session setup, service scope, authorization mechanics, query or filter
construction, shell quoting, request plans, or collection mechanics to a
consultant. Return only the contract's neutral progress sentence until a
complete business review, required decision, or genuine business-facing
exception is ready.

Use `scripts/expand_worker_manager_requests.py` only to expand confirmed
Business Units into the next deterministic batch of worker-assignment,
manager-hierarchy, user, and public-worker requests. It does not match
Business Units, select owners, interpret customer decisions, prepare creates,
or verify assignments. It has no HTTP, OAuth, Core-client, or Fusion imports.
Read [the Core-result-bundle contract](references/core-result-bundle.md)
before using it. Core performs every external request.

Worker-assignment and manager-hierarchy requests are paginated reads. The
helper emits `$limit=500` and `$offset=0` for the first page, then advances the
offset by the non-empty returned page size while `hasMore=true`. A nonempty
page shorter than the requested page size may be treated as final when the
continuation flag is absent; every other missing or malformed continuation
signal, or an empty continuing page, blocks the affected stage. The helper does
not prepare hierarchy reads until every confirmed Business Unit assignment page
is complete, and does not prepare manager/user reads until every hierarchy page
is complete.

The matching and proposal stages are preview-only. The separate apply stage may
create approved default owners only after a current-state preflight and a
fresh, exact-plan approval. It must not provision Risk Power Users or perform
work owned by another deployment skill.

## Stage 1 — Review current default-owner coverage

Begin only after Stage 0 records a current verified prerequisite result for the
same project and environment. Before asking which business processes to work
on, retrieve the complete seeded Level 2
process inventory and the complete current default-owner inventory through
`core.fusion-api.rest-api-client`. Do not request Business Unit, worker, or
hierarchy information yet. If either inventory is incomplete, unavailable, or
ambiguous after the declared reads, stop with a business-facing exception; do
not present a partial coverage table or expose the internal reason that a
complete review could not be produced.

Start both collection streams at `$offset=0` with `$limit=100`. For either
stream, when `hasMore=true`, advance the offset by the nonempty returned page
size and request the next page with the same filter, fields, and sort order.
Continue until the Boolean value `hasMore=false`. A literal Boolean `false` is
a completed final page; do not treat it as absent when displaying or evaluating
the result. A missing or malformed continuation signal, an empty page with
`hasMore=true`, or a repeated/unstable page blocks the coverage review; do not
infer that the remaining inventory is empty.

Inspect the continuation value with a Boolean-safe check. In particular, do
not use a fallback expression such as `jq '.hasMore // "missing"'`: that
operator replaces a valid `false` with the fallback value. Test the field's
type and value separately, or read the Boolean directly. A returned Boolean
`false` completes the inventory and requires the complete coverage table next.

Prepare these reads as an internal Core request manifest, retaining the exact
query property names `$filter`, `$limit`, `$offset`, and `$sortBy`. Before the
first request, validate that `$limit` is `100` and `$offset` is `0`; do not
construct a separate shell command whose quoting could alter those names.

```http
GET /api/boss/data/objects/ora/riskMgmtRisk/core/v1/referenceDataValues
  ?$filter=referenceCode!='SOURCE.ORA.ORA' AND referenceCode!='SOLUTION.FND.ORA' AND attributeCode='PROCESSES.ORA'
  &$fields=valueCode,referenceCode,attributeCode,levelOne,levelTwo,levelThree,description
  &$limit=100
  &$offset=0
  &$sortBy=levelTwo:asc,referenceCode:asc
```

```http
GET /api/boss/data/objects/ora/riskMgmtRisk/core/v1/referenceDataValueProperties/$views/detailed
  ?$limit=100
  &$offset=0
  &$sortBy=valueCode:asc
```

`referenceDataValues` is the provided `ReferenceDataValue` business object;
it does not include user-defined reference data. Do not substitute the
`allReferenceDataValues` extraction, which unions provided and user-defined
records. Form the consultant inventory only from its distinct `levelTwo`
values and establish the corresponding Level 2 scope using the documented
seeded Common-process rule. For each Level 2 row, first collect every catalog
record with the same validated `levelTwo` into one exact-`valueCode` set. A
repeated `valueCode`, a missing canonical member name, or any other nonunique
member identity blocks that row and requires a fresh catalog read; do not
silently collapse it. Identify any self-named member whose normalized canonical
process name equals the normalized Level 2 name. Exactly one such member is an
optional root marker for display and is not added again. No self-named member
means the scope has no root marker and remains valid; more than one is
ambiguous and blocks the row. Join every unique scope member to its current
owner record by
`valueCode`, using only the completed owner-properties inventory from the same
coverage run. A member is assigned only when exactly one matching property has
`defaultOwnerType` `USER` or `GROUP` and a nonblank `defaultOwnerCode`. No
property, or a property with a blank/null owner code, is unassigned. Treat
duplicate properties, an unsupported type with a nonblank code, or incomplete
evidence as ambiguous; block the coverage row rather than inferring its state.
Never expose a member `valueCode` or `defaultOwnerCode`.

For an assigned USER owner, use the owner-properties view's readable
`defaultOwnerUser.name`; for an assigned GROUP owner, use
`defaultOwnerGroup.name`. Otherwise use the returned readable owner label or
**Configured owner** only when no readable name is returned. The
**Current default owner** cell aggregates distinct assigned readable owners from
all scope members in stable sorted, comma-separated order. The root owner alone
must never determine the row's current owner or current result. If any scope
members are unassigned, append `Unassigned (<reference codes>)`. Use each
unassigned member's nonblank catalog `referenceCode`, including for an optional
marked root, sorted by normalized value. The root marker remains internal scope
metadata and has no special display suffix. Do not remove distinct members
because their displayed Reference Codes match. If an unassigned member has no
usable Reference Code, block the coverage row and require a fresh catalog read;
do not fall back to a process name, hierarchy/category value, or `valueCode`.

Every consultant-facing table is Level 2 process-level only. Use only the
fields declared for that table type in [Consultant-facing review and
decisions](#consultant-facing-review-and-decisions). The initial coverage
table's **Current default owner** cell may show the allowed unassigned reference
codes above. Do not add member identities, counts, states, action results, or
any other member-derived column or cell.

Render one complete consultant table **in the chat response** before asking for
a process selection. Persisting the table as an artifact, or describing it in
prose, does not satisfy this gate. Include every considered process, including
the ones already configured, and do not replace the table with a count, bullet
list, or missing-owner summary. Do not start Audit Policies, active-module
identification, algorithm publication, or Risk Power User work while this table
awaits a selection:

| Business process | Current default owner | Current result | Work on this process? |
| --- | --- | --- | --- |
| `<Level 2 process>` | `<comma-separated assigned owner names or usernames; Unassigned (<reference codes>) when applicable>` | `Already configured`, `Default owner needed`, or `Partially assigned` | `Not applicable`, `Pending selection`, or explicitly requested `UPDATE` / `RESET` |

A process with an existing owner is informative only in the normal assignment
flow. Do not offer replacement or reset choices merely because an owner is
present. The normal CREATE operation may be selected for a Level 2 row that
has one or more unassigned scope members; it creates owners only for those
members and preserves all configured members. Accept replacement or reset only
when the consultant explicitly requests one of these individually named actions:

- **UPDATE**, **CHANGE**, **MODIFY** or **REPLACE**: name the source owner and a separately validated,
  approved replacement owner. Replace only scope members whose exact internal
  owner type and owner code still match that source owner. Leave unassigned and
  differently owned members unchanged.
- **RESET**, **REMOVE** or **DELETE**: delete every existing default-owner
  property in the Level 2 scope; already-unassigned members remain unchanged.

Record the requested operation alongside the exact selected Level 2 process. A
missing, blank, or unrecognized operation means no change to configured
members. Internally, every approved decision records the selected Level 2
process, operation, reviewed per-member state, and hidden member action plan;
the plan contains each exact member identity once. Before approval and again
before the first write, reject a plan that repeats a member identity rather
than issuing duplicate bulk requests.
CREATE and UPDATE also record the replacement owner and UPDATE records the
exact source owner. RESET records no replacement owner. The customer approval
table remains Level 2-only and uses only its declared approval fields. Retain
created, updated, preserved, reset, and unchanged counts only in the hidden
action plan and redacted receipt.

For the normal assignment flow, ask plainly: **“Which processes with one or
more unassigned members would you like to work on?”** If no such process or
explicit existing-owner operation is selected, report that no changes are
needed and stop. Do not request more input at this point: begin functional
candidate discovery only for CREATE and explicit UPDATE targets. Do not ask for
mapping documents, permission to generate a mapping, or a Business Unit.

If the consultant later asks which processes are available or still need an
owner, re-render the same Markdown table filtered to **Default owner needed**
or **Partially assigned** rows. Do not answer with a count-labelled bullet list. The filtered table still
uses **Business process**, **Current default owner**, **Current result**, and
**Work on this process?** columns, with no process-record count.

## Stage 2 — Build a candidate population for selected processes

For selected unassigned CREATE processes and explicitly requested UPDATE
processes only, build a read-only candidate population. RESET requires no
candidate population. A Business Unit is useful evidence about a workforce
population; it is not, by itself, evidence that a person owns the selected
process.

Start the default route immediately from the selected process, without asking
the consultant for a Business Unit or a Business Unit-to-process mapping. Use
`core.fusion-api.rest-api-client` to first obtain the active-department catalog
defined in `ora-resource/ora_reference_lookups.md`. Reuse that completed
catalog for every selected process in the same unchanged workflow; do not read
it again for each process.

Assess department name and available department context semantically against
the selected process's business purpose, product domain, and any explicit
customer process-function evidence. This is a fuzzy business comparison, not
an exact-title or keyword search: customer job titles and department names vary
and must not be treated as a fixed catalog. Retain only direct functional
department matches. A senior title, a Business Unit name, location, or an
adjacent function alone is not a direct functional match.

For each retained department, use its exact returned department name in the
bounded primary-worker finder defined in the lookup reference. Read only those
worker results in stable 100-row pages to completion. Do not retrieve the
unfiltered `publicWorkers` collection and do not expand every worker into
hierarchy or identity reads. If direct functional departments produce no viable
candidate, evaluate adjacent departments only as a separate, lower-confidence
fallback and record why they are adjacent rather than direct.

The semantic assessment must consider the full functional context, not only
shared words. A customer-specific department may be relevant to a selected
process even when it does not contain a predefined title. Record the business
rationale for every retained department and candidate, and classify its support
using the existing functional fit tiers before ranking.

Customer mapping material remains optional supporting evidence. If it is
available, resolve supplied Business Unit names against the authoritative
catalog using exact then normalized names only, and retain a unique effective
match with workers as supporting evidence. Do not ask the consultant to approve
or provide a mapping, and do not use a Business Unit as the primary discovery
route. Exclude a matched Business Unit that has no workers unless the
consultant explicitly asks to inspect it.

If the department-bounded worker lookup and optional supporting evidence
produce no eligible worker, present a concise exception table. Offer an exact
Fusion username or an HCM-administrator validation of the relevant worker
function; do **not** ask for a Business Unit mapping. Do not claim that a
Business Unit has no owner; only state that the available workforce information
did not support a recommendation.

Retain the returned worker identities, any resolved Business Unit context, and
process-function evidence internally. Do not present a Business Unit decision
table unless the consultant explicitly asks to compare an ambiguity. The first
normal consultant output after process selection is the completed
owner-candidate review.

The completed `process_catalog` remains the directly provided
`referenceDataValues` result and resolves each selected L2 name to one row.
Reconfirm through the completed `process_owner_properties` inventory that each
CREATE target remains unassigned and each explicit UPDATE or RESET target has
one current owner property. Candidate discovery applies only to CREATE and
UPDATE. Never use the `allReferenceDataValues` union extraction as an alternate
match source.

## Stage 3 — Propose owners from functional and organizational evidence

Use the resolved candidate population to identify active, eligible owner
candidates. The default discovery route obtains workforce and reporting evidence
through Core, then ranks only verified candidates. It does not ask a consultant
to choose a management tier before the initial review.

If the consultant identifies an intended owner by an exact Fusion username,
first validate the exact account is active through the Fusion SCIM Users read.
That completes the account-active check. Do **not** use the HCM `userAccounts`
resource to validate a direct owner. Then resolve that exact username through
the BOSS user collection before requesting worker or reporting information. A
single BOSS result with the same `name` and a `guid` is a
supported direct owner candidate: use its `guid` as the internally retained
owner code and the exact supplied username as the consultant decision-table
label. A public-worker display-name lookup is not required for this direct
candidate route. This route replaces hierarchy analysis for that proposed
owner; it does not require a person, manager, department, or assignment record
and does not authorize an assignment. Zero, multiple, inactive, or
incomplete matches require correction and never fall back to a guessed
identity.

Use verified reporting relationships as organizational evidence, not as a proxy
for functional accountability. The default request scope remains the existing
closest-resolvable-manager review through three levels; it supplies a bounded
candidate population and does not itself choose the owner. A consultant may
request another supported hierarchy strategy only as a later refinement.

Pass the verified worker identifiers from the department-bounded worker lookup to
`scripts/expand_worker_manager_requests.py` with one
`--candidate-worker-id` per candidate to produce the next deterministic Core
request batch. Do not supply `--confirmed-mappings` for this default route.
Rerun it after every returned Core batch until it produces no further requests.
It obtains the bounded manager-hierarchy evidence and BOSS user identities only
for the department-bounded candidates and any returned managers. Use a
uniquely resolved BOSS username as the initial candidate label. The optional
Business Unit evidence route may continue to use `--confirmed-mappings`; it is
never a consultant-facing prerequisite.

From that completed set, build a small deterministic shortlist for each selected
process and deduplicate it across processes. Retain any candidate with explicit
process-function evidence first, then retain up to three additional verified
organizational candidates ordered by nearer reporting context, represented
worker assignments, and stable username; include candidates tied at the cutoff.
This is an enrichment limit only, not the final owner ranking. Ask
`core.fusion-api.rest-api-client` to enrich only those shortlisted candidates
with the documented HCM assignment fields. The Core skill performs every HCM
request; this skill does not construct an HTTP client or make a request. Use
returned job, department, position, manager, and direct-report evidence only
when it is present and verified. Retain the corresponding restricted decision
evidence internally.

For a consultant-supplied exact username, pass each name through
`--proposed-owner-username` without `--confirmed-mappings`. The helper requests
only the bounded BOSS identity lookup. Use the exact supplied username as the
readable label after the active-SCIM and BOSS-identity checks succeed. Do not
request HCM `userAccounts`, public-worker profiles, worker assignments, or
reporting hierarchy for that direct-candidate path.

### Candidate-analysis completion barrier

Do not present owner proposals, candidate choices, an approval request, or a
statement that hierarchy analysis is complete while any request produced by the
helper remains outstanding. Complete the entire read sequence first: worker
assignments, every returned worker's hierarchy, every candidate manager's BOSS
user identity. A
direct exact-username candidate completes after its active-SCIM and unique BOSS
identity checks. Also read current process-owner properties before reporting a
proposal.
Only after evaluating the complete result set may the skill present one of:

- a supported owner proposal for an unconfigured process;
- an explicit customer-choice tie; or
- an already-configured or no-candidate exception.

After the Business Unit selection, keep the skill execution active while Core
request batches are running. Begin with one deterministic level-one reporting
read before requesting the remaining workers and requested levels. An
authorization, transport, malformed-result, or other Core failure stops before
the larger batch and produces the corresponding business-facing exception.

A successful empty final hierarchy result is completed data for that worker,
not evidence that access is unavailable. Continue through all requested
workers and levels. If no reporting relationships are returned after the full
set completes, present this exception table and no owner proposal:

| Item | Business impact | Current result | Next action |
| --- | --- | --- | --- |
| `<selected business process>` | No supported default-owner recommendation is available | No reporting relationships were returned | Provide an exact Fusion username or ask the HCM administrator to validate reporting relationships and functional worker information |

Continue from each returned batch to the next dependent batch without yielding
a final response that merely says analysis is in progress. Return to the
consultant only for a completed review, a non-recoverable read/authentication
blocker, or a required decision.

`hierarchy.selection` defaults to `LOWEST_RESOLVABLE`, which requests levels 1
through `levels_to_inspect` (three by default). `FROM_LEVEL` requires a positive
`starting_manager_level`; `TOP` omits it and retrieves full hierarchy rows to
evaluate the requested number of highest levels.

After the shortlisted candidate enrichment is complete, build the restricted
evidence record and run `scripts/rank_owner_candidates.py`. It ranks candidates
in these orderable evidence tiers:

1. direct responsibility for the selected process or function;
2. leadership of the matching functional department;
3. matching job or position evidence;
4. verified organizational reporting context; then
5. verified Business Unit context.

Within a tier, prefer explicit active/effective evidence, management
responsibility, nearer reporting context, greater direct-report context when
available, and finally stable username ordering. Stable ordering is only for
repeatability: when multiple candidates share the strongest evidence tier, show
them as equivalent alternatives and require the consultant to select one.

Do not infer a direct functional match from an absent field, a Business Unit
name, or seniority alone. Process-specific functional evidence must come from
customer material, an explicit customer correction, or returned workforce data
that supports the stated match. When only organizational or Business Unit
evidence is available, present a Low-confidence proposal or alternatives rather
than claiming confirmed ownership.

Present the completed candidate review in this table. Omit an unavailable job
or department value instead of treating it as an error:

| Business process | Candidate | Job / department | Fit | Confidence | Why this person | Decision |
| --- | --- | --- | --- | --- | --- | --- |

The review can show one top candidate and an alternate, or equivalent candidates
when a consultant choice is required. A recommendation remains a proposal; it
does not assign an owner.

### Candidate review refinement

When the consultant requests the next likely candidate, a lower organizational
level, or a comparison, preserve the selected process and completed evidence.
Exclude only the prior candidate when requested and rerun the same local ranking
rule. Reuse the retained department catalog, shortlist, and enrichment evidence;
do not repeat unrelated Business Unit, worker, or hierarchy reads. If the
consultant asks for additional candidate detail, enrich only the newly
shortlisted verified candidate through Core. The exact-username route remains
available at every point and validates the specified person without
recommendation ranking.

The review files cannot be in `project/`, because they contain customer
identity data. Project artifacts retain only redacted counts, status, and
exceptions. `mapping_basis.mode` is `FUNCTIONAL_DISCOVERY` for the normal
selected-process route; it can also be `CUSTOMER_DOCUMENTS` when optional
customer material supplied supporting context.

## GET-only candidate analysis

The Core-managed preview reads the following BOSS and Fusion HCM resources. The process and
current-owner inventories use the same ordered 100-row coverage pages completed
in Stage 1; do not re-read or re-paginate them until apply preflight. The UI
process catalog is authoritative for the L2 target: it must be the direct
provided `referenceDataValues` result. Match the confirmed process name to
`levelTwo`, then resolve its complete Level 2 scope. Its owner display and
current result must aggregate every scope member. Treat an ambiguous scope as
an ambiguity for customer review rather than excluding the UI process.

1. The paginated `process_catalog` and `process_owner_properties` results
   defined in Stage 1. Expand each selected Level 2 target from the same
   validated unique-`valueCode` set used for its coverage row. If exactly one
   self-named root exists, mark it within that set; never append it separately.
   A scope with no self-named root remains valid. A duplicate member identity
   or multiple roots stops the scope before candidate review or mutation
   selection.
   Before selecting a mutation, classify each member from the current property
   inventory as `ABSENT_PROPERTY` (no row), `EMPTY_PROPERTY` (exactly one
   supported USER/GROUP row with a blank/null owner code), or
   `ASSIGNED_PROPERTY` (exactly one supported USER/GROUP row with a nonblank
   owner code). Treat duplicate rows, an unsupported nonblank owner type, a
   missing required identity, incomplete evidence, or any other shape that
   cannot establish one of those states as ambiguous and not mutable. A normal
   CREATE action targets only `ABSENT_PROPERTY` and `EMPTY_PROPERTY` members.
   An explicit UPDATE targets
   only members whose exact internal owner type/code matches the reviewed source
   owner. An explicit RESET targets every member with a valid assigned owner
   tuple; empty properties are already unassigned and remain unchanged. All
   remaining members are preserved.
2. The active HCM department catalog, using `departmentsLov` with
   `q=Status='A'`, `fields=OrganizationId,Name,EffectiveStartDate,EffectiveEndDate,Status`,
   `onlyData=true`, `limit=100`, `orderBy=Name:asc`, and a stable offset
   sequence. Complete it once and semantically select direct functional
   departments for each requested process. Do not use a fixed title list or a
   consultant-supplied Business Unit filter.
3. The primary-worker `publicWorkers` finder for each retained department,
   using the exact returned `DepartmentName` and
   `OnlyPrimaryAssignmentFlag=true`, with `limit=100` and stable offsets. This
   is the only normal worker-population read. Do not retrieve the unfiltered
   worker collection. Deduplicate returned numeric `PersonId` values before
   hierarchy expansion.
4. `managerHierarchy` for every department-bounded worker and every requested manager level. For
   a level-based review, `personId` and `managerLevel` are numeric BOSS values:
   use `personId=<PersonId> and managerLevel=<level>`. The `TOP` review may
   request full hierarchy rows with `personId=<PersonId>`.
5. BOSS `users` to resolve each department-bounded worker and hierarchy candidate to
   the stable BOSS user GUID and verified username. Use that username as the
   reviewable candidate label.
6. For only the unique shortlisted candidate identities, read the documented
   public-worker and primary-assignment fields through
   `core.fusion-api.rest-api-client`. Retain available display name, job,
   department, position, manager, and direct-report evidence. Do not expand this
   enrichment to every worker in a Business Unit, and do not exclude a verified
   candidate whose optional HCM data is unavailable.
7. When the operator requests candidate role enrichment, enrich candidates from
   the Fusion user-account resource in small batches, using `GET
   /hcmRestApi/resources/11.13.18.05/userAccounts` with a batched
   `q=Username='...' OR ...` filter and `expand=userAccountRoles`. Use the
   normal Fusion OAuth audience and report unavailable or unmapped
   accounts without blocking the hierarchy preview. This is optional role
   enrichment only; it is never part of exact-owner validation and cannot block
   a direct-owner proposal.

Role counts and broad administration never establish functional responsibility
or break a functional-evidence tie.

The same owner may be recommended for more than one Level 2 process. Each
Level 2 target receives its own proposal and customer decision; candidates are
not deduplicated across Level 2 targets.

The review output shows the process context, supported candidate set, functional
and organizational evidence, recommendation or equivalent alternatives, and a
pending customer decision for every proposal. Print every candidate option in
the consultant table defined above. A candidate table is decision-support output
only; the customer still selects or approves the owner explicitly. Keep request
bodies and internal owner identifiers out of this table.

## Candidate evidence enrichment

The default preview enriches only the bounded shortlist, not every returned
worker. Delegate the following GET-only Fusion HCM reads to
`core.fusion-api.rest-api-client`; the Core skill performs them and returns the
restricted result. First read the candidate's public-worker identity, then the
candidate's assignments:

```http
GET /hcmRestApi/resources/11.13.18.05/publicWorkers/{PersonId}/child/assignments
    ?fields=AssignmentId,PrimaryAssignmentFlag,JobName,DepartmentName,ManagerName
    &onlyData=true
```

Use the assignment with `PrimaryAssignmentFlag=true` when returned. To retrieve
manager display context when it is needed for a shortlisted candidate, delegate:

```http
GET /hcmRestApi/resources/11.13.18.05/publicWorkers/{PersonId}/child/assignments/{AssignmentId}/child/managers
```

Use only returned and relevant details as ranking evidence. An unavailable
manager, assignment, department, position, or person-detail response is not a
reason to discard an otherwise verified candidate; it lowers confidence and is
shown as unavailable. Store candidate details only in restricted decision
evidence, not under `project/`; they never replace customer approval.

## Approval and live execution

Record an explicit table or chat approval for each reviewed Level 2 proposal
and each explicit Level 2 existing-owner operation. For a customer-resolved
tie, retain the reviewed candidate list and selected internal owner identity.
Validate that selection here before continuing. The apply preview re-reads the
whole selected scope, rebuilds the hidden member action plan from its unique
member set, and shows one business-labelled Level 2 row using the declared
approval-table fields. A repeated member identity or multiple roots cancels the
scope. A live apply may use only that unchanged approved plan.

Every owner-property mutation uses the documented BOSS bulk endpoint. Do not
use collection POST, PATCH, an item endpoint, or an inferred multi-member bulk
contract. The recorded contract supports one changed unique scope member per
request:

```http
POST /api/boss/data/objects/ora/riskMgmtRisk/core/v1/referenceDataValueProperties/$bulk

{
  "items": [
    {"$operation": "CREATE", "valueCode": "<member_value_code>", "defaultOwnerType": "USER|GROUP", "defaultOwnerCode": "<approved_owner_code>"}
  ]
}
```

Use that CREATE payload only for a member that has no current owner property.
For an unassigned member with exactly one empty property, Core must instead
verify its `$id` equals its `valueCode` and that its owner code is still
blank/null, then use the documented DELETE/CREATE request below to replace the
empty property. If the property gained a nonblank code, is missing a matching
`$id`, or is nonunique, cancel that member and require a new review and
approval. For an explicit UPDATE, Core must verify exactly one current property whose
`$id` equals its `valueCode`, and whose internal owner type/code exactly
matches the reviewed source owner. The replacement request uses that identity:

```http
POST /api/boss/data/objects/ora/riskMgmtRisk/core/v1/referenceDataValueProperties/$bulk

{
  "items": [
    {"$operation": "DELETE", "$id": "<member_value_code>"},
    {"$operation": "CREATE", "valueCode": "<member_value_code>", "defaultOwnerType": "USER|GROUP", "defaultOwnerCode": "<approved_owner_code>"}
  ]
}
```

An explicit UPDATE changes only members that still match its reviewed source
owner; an unassigned member, including one with an empty property, or a member
owned by anyone else is preserved. An explicit RESET needs the same verified
`$id` for every member with a valid assigned owner tuple and submits one
one-item bulk request containing only
`{"$operation":"DELETE","$id":"<member_value_code>"}`. An absent RESET
member or an empty-property RESET member is unchanged. A nonmatching `$id`,
nonunique property, or any changed member state cancels that member and
requires a new review and approval.

Before the customer approves application, re-read the full Level 2 scope and
rebuild the aggregate action counts. If its summarized operation differs from
the reviewed table, cancel that scope and require a new review and approval.
Immediately before every planned member request, confirm its identity has not
already appeared in the approved plan, then re-read that member and
record its safe physical state and selected path in the redacted operation
receipt: `ABSENT_PROPERTY` with `CREATE_ABSENT`, `EMPTY_PROPERTY` with
`REPLACE_EMPTY_PROPERTY`, or `ASSIGNED_PROPERTY` with the applicable
preserve, update, or reset path. Do not include member codes, property `$id`
values, raw payloads, or authorization data. After fresh approval, execute the
one-member bulk requests in scope order without automatic retries. Re-read the
changed member afterwards: verify CREATE and UPDATE by matching `valueCode`,
`defaultOwnerType`, and `defaultOwnerCode`; verify RESET by confirming the
matching property is absent. The detailed response does not reliably return
`administratorFlag`. Write the customer-controlled receipt and redacted
project run report from Core results.

Do not automatically retry a bulk POST. If a member is stale, the write fails,
or verification is uncertain or mismatched, stop the remaining member requests
for that Level 2 scope. Do not compensate an earlier member. Report the Level 2
process, operation, verified result, and safe next action. Retain created,
updated, preserved, reset, unchanged, failed, and unresolved counts only in the
redacted run report.

After every operation in which all planned member changes verify successfully,
re-read the complete process and owner-property inventories and render the full
Level 2 coverage table again. If any Level 2 scope still has unassigned members,
remain in this skill and ask the normal assignment-selection question. If no
members remain unassigned, return `completed_verified` to the parent workflow;
the parent alone evaluates and proposes any
eligible next task. Do not select or start another skill here. If the consultant
explicitly defers this skill while members remain unassigned, record the
deferral, return `deferred` control to the parent, and do not report this skill
as complete. The offering coordinator handles the requested task switch. A
stale, failed, partial, uncertain, or verification-mismatched operation is not
a handoff result and retains the stop behavior above.

## Exceptions

Report unknown/ambiguous or ineffective Business Units, unknown processes,
no workers, unresolved hierarchy candidates, equal top candidates, an existing
process property without an explicit operation request, and any missing
operation contract. Never choose a replacement owner or reset a property
silently.

## Failure handling and safe recovery

Read [task-local error handling](ora-resource/ora_error_handling.md) before a
preview or live apply. It owns task-specific disclosure and stop-before-retry
rules; the Core REST skill continues to own token refresh, HTTP transport, and
raw-response handling.

Before any create, update, or reset, verify the target environment, required
BOSS bulk-operation privilege, approved review decisions, immutable Level 2
scope plan, and writable redacted artifact destination. UPDATE and RESET also
require exactly one current owner-property `$id` equal to every changed
member's valueCode. A missing or ambiguous result stops with the documented
failure class; never substitute an unresolved Business Unit, process, owner,
property state, or property identity.

On an authentication or authorization failure, refresh only as permitted by the
Core REST skill, then stop and record the redacted Core diagnostic. On a
transport, malformed Core-result, or lookup failure, stop the affected stage
and do not treat incomplete reads as complete. On a create, update, or reset
failure or uncertain outcome, do not replay that write automatically: retain
its redacted status, safe pre-write property state, selected mutation path,
endpoint path, request identifier or ECID when provided, and reconcile it with
the documented read-only property query. Stop remaining members in that Level
2 scope. Persist redacted status, stage, failure class, recommended action,
environment, and artifact references in the project run record.

## Synthetic validation scenarios

Validate with synthetic Core-result bundles before a live run:

1. Search prerequisite: exactly one enabled and updatable Site capability row
   with an enabled Site value records redacted evidence and proceeds silently.
   A missing or disabled Site value shows the approval table, refreshes the
   Core evidence after approval, delegates the one Core-managed create or
   update, and requires final enabled-value verification before any process or
   owner read. An unavailable, unsupported, withheld, failed, or unverified
   prerequisite blocks before coverage without a retry.
2. Initial coverage review: the process and current-owner inventories are each
   retrieved in stable 100-row pages until the Boolean `hasMore=false`, then
   produce one table covering every Level 2 process and every existing readable
   owner. Each row scopes one exact-`valueCode` set of all matching Level 2
   catalog records. Exactly one self-named root is marked within that set when
   present; no root marker is valid, while multiple roots block the row. A
   duplicate member identity also blocks the row. The normal selection accepts
   a row with one or more unassigned members;
   configured members remain preserved. An UPDATE or
   RESET is mutable only after an explicit individually named Level 2 request.
   After a CREATE or explicit UPDATE selection, functional discovery begins
   without a Business Unit or mapping question; RESET skips candidate discovery,
   and no other offering workflow begins while a selection is pending.
   A list that reports only one member's owner for a Level 2 row is invalid and
   must be re-read before it is shown or refreshed.
3. Aggregated owner display: a Level 2 scope with distinct assigned owners and
   unassigned records displays the distinct owner labels followed by
   `Unassigned (<reference codes>)`. These are the nonblank catalog Reference
   Codes of the unassigned records, including an optional marked root, sorted
   by normalized code. A root has no special display suffix. Assigned child
   names and member counts are never displayed.
   When the root and one or more children have different owners, with no
   unassigned members, display all distinct owner labels and `Already
   configured`; do not display only the root owner.
4. Candidate population: after a CREATE or explicit UPDATE process is selected,
   the bounded functional worker lookup begins without a Business Unit mapping.
   A returned Business Unit is supporting context only. If no eligible worker
   is found, offer exact username selection or HCM validation of functional
   worker information; do not request a Business Unit or mapping.
5. Empty-property CREATE selection: for a selected Level 2 scope containing
   assigned and unassigned members, no property resolves to
   `ABSENT_PROPERTY` and selects one one-item BOSS bulk `CREATE` request. One
   supported GROUP property with null owner code/group resolves to
   `EMPTY_PROPERTY`; with a verified `$id`, it selects one bulk
   `REPLACE_EMPTY_PROPERTY` DELETE/CREATE request, never CREATE-only. Valid
   USER and GROUP owner tuples resolve to `ASSIGNED_PROPERTY` and are
   preserved. An unreadable owner name does not change a valid tuple's state.
6. Functional ranking: direct process responsibility outranks a nearer generic
   manager. Returned job, department, position, and organization evidence may
   raise fit; missing optional person, assignment, manager, or department data
   cannot exclude a verified user or be invented as a match.
7. Equivalent candidates: multiple candidates in the strongest functional tier
   are shown as alternatives for consultant selection. Stable username ordering
   does not become a business recommendation.
8. Empty final hierarchy rows: complete every requested worker/level read, make
   no user lookup, and render the no-reporting-relationships exception rather
   than an access-failure diagnosis.
9. Refinement: excluding a prior candidate produces the next deterministic
   recommendation from retained restricted evidence without re-reading unrelated
   Business Unit, workforce, or hierarchy data.
10. Explicit update: for a Level 2 scope with source owner X, owner Z, and an
    unassigned member, UPDATE from X to Y submits one BOSS bulk DELETE/CREATE
    request only for each X-owned member with a matching `$id`; Z-owned and
    unassigned members remain unchanged. Each changed member's post-request
    reread must match Y.
11. Explicit reset: RESET submits one BOSS bulk DELETE request for every
    valid assigned owner-property member in the Level 2 scope, each with a
    matching `$id`; absent and empty-property members remain unchanged. Each
    changed member's post-request reread must have no matching property.
12. Contract and preflight safety: an empty property without a matching `$id`,
    a nonunique current property, or an `EMPTY_PROPERTY` member that becomes
    `ASSIGNED_PROPERTY` cancels that member. A changed aggregate Level 2 plan
    before approval requires new review and approval.
13. Partial live outcome: a constraint failure, stale member, failed bulk
    request, uncertain write, or verification mismatch stops remaining members
    in that Level 2 scope, never retries or compensates, reports aggregate
    operation-specific counts, and records the safe property-state/mutation
    path pair for diagnosis.
14. Bulk-create contract: every CREATE uses the documented one-item `$bulk`
    payload. No multi-member bulk semantics or atomicity is assumed unless
    authoritative UI/API evidence later establishes it.
15. Scope identity and child labels: a synthetic Level 2 catalog with one
    self-named root and multiple children produces one unique member per
    `valueCode`. When all are unassigned, the coverage table contains each
    nonblank Reference Code once, including the root, with no root suffix. It
    never displays a canonical process name or shared hierarchy/category value
    for an unassigned record. A valid unique-member scope with no self-named
    root displays all unassigned Reference Codes and remains reviewable and
    mutable. A missing usable Reference Code for an unassigned member, duplicate
    `valueCode`, or multiple roots blocks the coverage row; duplicate planned
    member identities block CREATE before any bulk request.
