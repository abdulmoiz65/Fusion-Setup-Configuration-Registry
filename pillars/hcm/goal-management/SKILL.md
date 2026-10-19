---
skill_id: "hcm.goal-management"
name: "Goal Management"
description: "Coordinates HCM Goal Management implementation guidance and routes work to developer-created functional-area skills."
layer: "pillar"
pillar: "HCM"
offering: "Goal Management"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM Goal Management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "hcm_scope"
  - "goal_management_requirements"
outputs:
  - "goal_management_scope"
  - "functional_area_skill_plan"
  - "goal_management_work_products"
  - "token_usage_record"
depends_on:
  - "shared.project-intake.scope-definition"
  - "shared.implementation-planning.offering-task-map-builder"
uses_core:
  - "core.fusion-dev.pillar-skill-gen"
  - "core.project-mgmt.project-state-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.artifact-version-manager"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
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
  - "scope"
  - "skill_path"
  - "setup_task_sequence"
  - "design_decisions"
  - "configuration_blueprints"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "scope"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects: []
required_privileges: []
---

# Goal Management Implementation Guidance

## Purpose and ownership

This Goal Management branch entry point owns consultant workflow for the
approved Common, Review Period, Goal Plan, Performance Library Goals, and
Development Library Goals functional areas under the catalog-backed Goal
Management offering (`ORA_GOAL_MANAGEMENT`). Task-local skills own object
behavior.

## Best-practice reference consultation

For every Goal Management implementation query, consult the canonical
[HCM Goal Management best-practice reference](goal-management-common/best-practice-rules/hcm-goal-management/README.md)
before forming consultant guidance. Use its topic map to select the applicable
sections, disclose material tenant or release assumptions, and return the
relevant recommendation with the owning task route.

The reference is advisory. Target-tenant behavior, current Oracle
documentation, and the owning task skill's current contract take precedence,
in that order, over the reference when they differ. Never use the reference to
infer tenant metadata, hard-code IDs or codes, bypass a declared dependency,
or perform an external operation without the task skill's required validation
and approval gates. For general design, security, notifications, Transaction
Design Studio, Visual Builder Studio, diagnostics, testing, migration, or
cutover questions that do not name a setup object, use the reference to frame
an advisory response and route any concrete setup operation to its declared
owner.

## Deterministic routing

For explicit REST batch intent, read [REST batch workflow](goal-management-common/rest-batch.md).
The selector returns `transportIntent=adf_batch` after intake/conflict checks.
Preserve default REST, HDL batch upload, FSM, and existing specialized batching.
Only that explicit transport intent may invoke the maintained batch-capability
resolver; standard REST and loader routes must bypass it unchanged. This selects
preparation, not approval to execute.

Evaluate `goal-management-common/scripts/goal_management_route_selector.py` before selecting
an execution route. REST is the default for normal-volume object execution.
Classify explicit FSM setup export/import first: `csv_export` delegates to
`shared.setup-export.task-level-export`; `csv_import` delegates to
`core.data-loader` using its FSM route. Both require current catalog support,
exact task identity, package/operation preflight and the owner's approval gate.
Do not export as a prerequisite or recovery shortcut without explicit intent.
An ambiguous import request needs route clarification. Negated HDL instructions
are not HDL requests. Screenshots, TSV, folders and unknown source formats
require intake, not an automatic REST operation.
Select HDL for Goal Plan or Library Goal only when the consultant explicitly
requests HDL/HCM Data Loader/data load, or when the resolved root-record count
is at least 25 (the configurable Goal Management high-volume threshold).
Explicit REST overrides automatic volume routing. A supplied DAT/ZIP alone
does not imply HDL. When HDL is selected without a DAT/ZIP, return
`hdl_generate`: the object task resolves and validates the business rows and
`core.data-loader` generates the live-metadata source and immutable ZIP. When
HDL is selected with a DAT/ZIP, return `hdl_dat_preflight`. Review Period is
REST-only; an explicit Review Period HDL request returns
`HDL_OBJECT_UNSUPPORTED` and offers REST. Follow
[Goal Management HDL Source Generation](goal-management-common/hdl-source-generation.md) for
both generated and supplied-source modes.

When a consultant supplies a multi-object direct implementation prompt, an
implementation source pack, or points to
unstructured inputs such as DOCX, PDF, PPT/PPTX, Excel/CSV, text, Markdown,
ZIP, screenshots, or HDL folders that still require business-object and volume classification, route first to
[Goal Management Implementation Intake](goal-management-common/implementation-intake/README.md).
That offering-owned support package defines source inventory, fact extraction, complete task
mapping, runbook readiness, and the confirmation summary before project or Run
Book creation. Do not create a Run Book or start an object mutation directly
from an unstructured-source prompt.

After intake normalizes the source into semantic facts, call the route
selector again with `source_normalized=true`. This lifecycle marker prevents
the same DOCX, PDF, spreadsheet, DAT, table, screenshot, or prompt-derived
source from looping back into intake. The second selection routes the
classified object to REST or HDL under the same volume and explicit-intent
rules.

### Goal Management project planning handoff

For every Goal Management project that requires an initial Run Book, including
direct prompts and mixed Performance/Development Library Goal requests, use
the [implementation intake task-mapping and handoff procedure](goal-management-common/implementation-intake/README.md#task-mapping).
Do not stop at Core's generated skill selection: both Library Goal variants
share the same task code and name, so its lexical fallback may select the
wrong variant even when the mapping contains the correct functional area.

Persist `Resolver Sequence` for every mapping row from the shared planning
workflow's validated `setup_task_sequence`; do not invent a local order.
After Core's `create_project_runbook.py --refresh-artifacts`, run
`goal-management-common/implementation-intake/scripts/reconcile_goal_management_runbook.py
--project-root project/{project_id}` for a local dry-run, then repeat with
`--apply` to persist the exact routes. Reconcile after every Core refresh,
before binding the plan checksum, presenting the final Run Book preview, or
dispatching Run Book creation through `core.runbook`. Use the reconciled
persisted plan for that handoff; another Core refresh invalidates it until
reconciliation runs again.

The existing Goal Management reconciler validates code, name, offering, and
functional area against the task manifests and updates `setup-task-plan.json`,
`task-context.json`, and `runbook-plan.json` together with audit evidence.
It preserves Core's executable sequence and sends no Oracle requests.
A recoverable lexical variant mismatch is handled by this declared local
step; missing sequence provenance, ambiguous identity, or inconsistent
artifacts remain blockers. Do not manually substitute a skill path or resume
a stopped implementation as part of repairing its skill instructions.

For a single-object prompt, route exactly one object per run:

1. [Review Periods](review-period/review-periods/SKILL.md) (`ORA_HRG_MANAGE_REVIEW_PERIODS`)
2. [Goal Plans](goal-plan/goal-plans/SKILL.md) (`HRG_MANAGE_GOAL_PLANS`)
3. [Performance Library Goal](performance-library-goals/goal-library/SKILL.md) (`HRG_MANAGE_GOAL_LIBRARY`)
4. [Development Library Goal](development-library-goals/goal-library/SKILL.md) (`HRG_MANAGE_GOAL_LIBRARY`)

The underlying Goal Library setup task still uses the Fusion `libraryGoals`
resource. Library Goal behavior is variant-specific: Performance routes use
`PerfCategoryCode` and `TypeCode=PERFORMANCE`; Development routes use
`DevCategoryCode` and `TypeCode=DEVELOPMENT`. Never infer, convert, or combine
the variant-specific fields in one task payload.

For unstructured requirements, use the offering-owned
[Goal Setup Field Resolution](goal-management-common/goal-setup-field-resolution/README.md) support package before asking a
consultant to map Goal Plan or Library Goal field language. Do not route a
business-purpose statement to population maintenance. Resolve dropdown and LOV
values from current metadata, disclose defaults, and ask only where there is
no unique supported field mapping.

For source packs, preserve document order as traceability only. Resolve each
setup task by exact task code, task name, offering, and functional area, then
derive its execution sequence through the shared implementation-planning
services and their validated dependency sources. Never select a Library Goal
skill by lexical path when the shared catalog task has multiple product
variants. The validated task context and shared `setup_task_sequence` remain
inputs to the common configuration-plan and Run Book workflows.

## Guided implementation continuation

When a consultant starts with no setup object or supplies too little detail to
plan the selected object, enter guided implementation mode. Ask only for the
next missing business input, then offer optional continuation choices; do not
create tasks or infer dependencies from that guidance. The recommended object
sequence, after any source-requested or selected-field dependency work, is
Performance Library Goals, Development Library Goals, Review Periods, then Goal
Plans. A consultant can start any non-Goal-Plan object in another order.

If the consultant supplies an explicit task sequence, preserve it exactly and
do not replace it with the recommendation. A regular Goal Plan is the sole
ordering prerequisite: it cannot proceed to preview until one active Review
Period is identified. At the end of a successful guided object setup, state the
available next objects in the selected order and offer `continue`, `skip`, or
`not now`. Do not re-prompt an item declined in the current implementation
conversation. Do not show this continuation guidance for a fully scoped source
pack or an explicitly isolated setup action.

### Greenfield HDL DAT routing

When routing selects `hdl_generate` or `hdl_dat_preflight` for Goal Plans or
Library Goals, classify the request as a greenfield data load, not FSM export/import.
Select the applicable object task below for object-specific
business validation and defaulting, then require `core.data-loader` for all
source generation or supplied-source validation, immutable package, preview,
approval, upload, and reconciliation stages. The task must pass resolved
business rows; Core owns the live-metadata workbook/DAT and exact ZIP. If a
supplied source is malformed but business intent is complete and unambiguous,
preserve it as evidence and rebuild a separate prepared source through Core.
Never upload the malformed file or invent an unresolved business value.
All object validation rules apply equally to REST and HDL. Follow
[Goal Management HDL Source Generation](goal-management-common/hdl-source-generation.md).

For a supplied DAT/ZIP, require `core.data-loader` for all local
preflight, immutable package, preview, approval, upload, and reconciliation
stages. The task skill must declare the allowed DAT component order and the
target-tenant reference evidence. Treat the DAT/ZIP and prompt as the complete
consultant input: resolve environment, evidence, caller context, timestamps,
operations, and safe target/Oracle defaults internally. Preserve the uploaded
bytes and create a separate prepared copy; never overwrite a supplied value or
invent an unresolved business choice. Do not combine Performance and Development
Library Goal DAT files or use REST, browser entry, or FSM CSV as a substitute
after HDL selection. REST remains the default for normal volumes. Never switch
an approved or failed REST operation to HDL automatically; recommend the
alternate route and wait for explicit consultant confirmation. Review Period
HDL remains unsupported.

### Mixed Library Goal prompts

When one consultant prompt explicitly requests both Performance and Development
Library Goal work, decompose it into two independent child routes: one for
`performance-library-goal` and one for `development-library-goal`. Return a
`split_work_plan` that preserves the request order, object identity, requested
operation, and approval state for each child. Do not send a combined
`libraryGoals` payload, reuse an approval across children, or begin a mutation
until each child has its own exact preview and explicit approval. Independent
read-only children may proceed after normal readiness checks; mutations remain
serialized and approval-gated.

## Consultant prompt detection

| Prompt intent | Owning task | Normalized operation |
|---|---|---|
| Consultant implementation source pack / DOCX / PDF / PPT / Excel / CSV / text / screenshots / DAT or ZIP without explicit HDL intent / mixed HDL folders | `hcm.goal-management` with `goal-management-common/implementation-intake/README.md` | `unstructured_input_extract`, then confirmed task mapping and REST by default; no Fusion action |
| Review Period / review cycle / period dates | `review-periods` | `get`, `list`, `search`, `create`, `update`, or `inactivate` |
| Goal Plan / Primary Goal Plan / plan population / plan assignment | `goal-plans` | `get`, `list`, `search`, `create`, `update`, `activate`, `inactivate`, `maintain_population`, or `prepare_assignment` |
| Explicit HDL/data-load intent or at least 25 resolved root rows for Goal Plan or Goal Library data, without a DAT/ZIP | Object-specific Goal Plan, Performance Library Goal, or Development Library Goal task, then `core.data-loader` | `hdl_generate`; resolve and validate business rows, generate the live-metadata source and immutable ZIP, then use the Data Loader approval workflow |
| Supported DAT/ZIP plus an HDL selection condition for Goal Plan or Goal Library data | Object-specific Goal Plan, Performance Library Goal, or Development Library Goal task, then `core.data-loader` | `hdl_dat_preflight`, then immutable preview and approval; no upload or record creation without the Data Loader workflow |
| Explicit HDL intent for Review Period | `review-periods` | Block with `HDL_OBJECT_UNSUPPORTED` and offer the supported REST route |
| Performance Library Goal / performance reusable goal | `performance-library-goal` | `get`, `list`, `search`, `create`, `update`, `activate`, `inactivate`, or guarded `delete` |
| Development Library Goal / development reusable goal / career development goal library | `development-library-goal` | `get`, `list`, `search`, `create`, `update`, `activate`, `inactivate`, or guarded `delete` |
| Exact profile option code / profile-option value / worker goal setting profile option | Goal Management Common facade for reads; `core.fusion-api.apps-common.profile-options` for maintenance | `dependency_read` or independent `dependency_mutation`; never a Goal Management REST mutation |
| Exact lookup type / lookup code / Goal Management lookup | Goal Management Common facade for reads; `core.fusion-api.apps-common.lookups` for maintenance | `dependency_read` or independent `dependency_mutation`; never a Goal Management REST mutation |
| Exact value set code / value-set value / Goal Management value set | Goal Management Common facade for reads; `core.fusion-api.apps-common.value-sets` for maintenance | `dependency_read` or independent `dependency_mutation`; never a Goal Management REST mutation |
| Exact flexfield code / context or segment | Matching Apps Common DFF, EFF, or KFF provider | `dependency_read` or independent provider-owned export/import/deployment; never a Goal Management REST mutation |
| Manage Reference Data Sets / reference-data-set request | Goal Management Common delegation facade, then the owning Common setup workflow | Read existing values or route an independent provider-owned mutation |
| Manage Currencies / currency setup | Goal Management Common delegation facade, then the owning Common/manual workflow | Read existing values or route an independent provider-owned mutation with seed-data safeguards |
| Approval Options or approval rules | `hcm.hcm-tool.approval-options` or `hcm.hcm-tool.approval-rules` | Exact-process read or independent provider-owned mutation; never embed approval plumbing in a Goal Management payload |
| Offering, functional-area, or feature opt-in | `shared.implementation-planning.fsm-set-optin` and its target-specific child skill | Independent shared setup operation |

## Profile-option routing

For any of the four Goal Management objects, route an exact profile option
code to `hcm.goal-management.goal-management-common.manage-profile-options`. That Common task
requires the external transport capability
`core.fusion-api.apps-common.profile-options`, implemented in this repository
by the declared `core.fusion-api.apps-common` dependency, using the supplied
code as `ProfileOptionName`. The shared provider owns the exact-code lookup,
definition/value read, scope validation, and any profile-value mutation. Do
not require the code to appear in this branch's known-code list before a read,
and do not infer a code from a display label or product object. If the declared
dependency cannot expose that capability, return `PROVIDER_SKILL_UNAVAILABLE`;
if the exact code cannot be confirmed, return `validation_gap`.

When the same prompt contains a Goal Management object operation and a profile
option operation, return independent child routes. The product task must not
embed a profile-value request in its HCM business-object payload. Profile
option reads proceed through the common provider after environment validation;
any profile-value write requires the provider's exact current-value preview and
explicit approval, independent of the product-object approval.

## Lookup routing

For any of the four Goal Management objects, a consultant may provide an exact
`LookupType` and an optional `LookupCode`. Route it to
`hcm.goal-management.goal-management-common.manage-common-lookups`, which requires external capability
`core.fusion-api.apps-common.lookups`, implemented in this
repository by the declared `core.fusion-api.apps-common` dependency. The shared
provider owns lookup-category selection, exact-key resolution, returned-item
identity, and any mutation. Task-local `commonLookupsLOV` calls are
prohibited: Goal Management lookup validation uses the public Apps Common
`commonLookups/{LookupType}?expand=lookupCodes` route and must not create,
update, or delete a foundation lookup. If the declared dependency cannot expose that capability, return
`PROVIDER_SKILL_UNAVAILABLE`; if the exact lookup type cannot be confirmed,
return `validation_gap`.

When a lookup category is supplied, pass it to the provider. When it is not
supplied, the provider may perform read-only discovery in its documented order:
Common, Standard, Generic, then Set-Enabled. A Generic lookup requires an exact
`ApplicationCode` before its result is authoritative. A Set-Enabled lookup
mutation requires an exact returned code-item identity and reference-data-set
context. Stop on `401` or `403`; do not treat authorization failure as evidence
that another category should be tried.

When the same prompt contains a product-object operation and a lookup operation,
return independent child routes. Do not embed a lookup mutation in an HCM
business-object payload. Lookup writes require the common provider's own exact
current-value preview and explicit approval, independent of the product-object
approval.

## Value-set routing

For any of the four Goal Management objects, route an exact value-set code to
`hcm.goal-management.goal-management-common.manage-value-sets`, which requires external capability
`core.fusion-api.apps-common.value-sets`, implemented in this
repository by the declared `core.fusion-api.apps-common` dependency. The shared
provider resolves the exact code to a returned `valueSets_Id` before reading a
definition, validation table, or values. Never derive an identifier from a
code, accept a partial/display-name match, or treat an unknown code as a Goal
Management default. If the declared dependency cannot expose that capability,
return `PROVIDER_SKILL_UNAVAILABLE`; if the exact code cannot be confirmed,
return `validation_gap`.

The provider may maintain only a returned child value record. A create, update,
or delete of the root value-set definition is unsupported unless a current
Oracle source advertises a supported route. Child-value writes require the
provider's exact current-state preview and explicit approval.

When the same prompt contains a product-object operation and a value-set
operation, return independent child routes. Do not embed a value-set mutation
in an HCM business-object payload. Library Goal Target Outcome `ValueSetName`
remains a current runtime selector for `contentItemsLov`; it is not permission
to maintain that value set through the product task.

## Flexfield routing

For any of the four Goal Management objects, route an exact Descriptive
Flexfield code to `hcm.goal-management.goal-management-common.manage-descriptive-flexfields`,
which requires external capability
`core.fusion-api.apps-common.descriptive-flexfields`, implemented in
this repository by the declared `core.fusion-api.apps-common` dependency, with
`HRG_MANAGE_WORKFORCE_GOALS_DESCRIPTIVE_FLEXFIELD` and functional area
`HRG_WORKER_GOALS`. The shared provider owns exact task resolution, eligibility
checks, export/import packaging, and DFF configuration execution. If the
declared dependency cannot expose that capability, return
`PROVIDER_SKILL_UNAVAILABLE`; if the exact code cannot be confirmed, return
`validation_gap`.

An `inspect` request requires the provider's task-level export process. It is
read-only with respect to configuration, but it is not a strict no-side-effect
operation: obtain separate authorization before launching that export.

Do not infer an entity usage, context, segment, value set, or runtime payload
attribute from the supplied DFF code. Confirm those details from current
exported setup data or current metadata before preparing a change. A supplied
code is not constrained to the known-code register; unknown or ambiguous
current configuration must return a blocker instead of a guessed mapping.

When the same prompt contains a product-object operation and a DFF operation,
return independent child routes. Product-object payload `dff_changes` is
business data only and may be used only when current runtime metadata confirms
the exact writable attribute. It cannot create, update, deploy, or otherwise
configure a DFF. DFF imports require the common provider's exact package
preview and explicit approval, independent of the product-object approval.

## Common Applications foundation routing

Manage Reference Data Sets and Manage Currencies are direct children of the
current Common functional area. Route them to their respective Common task
skills. Preserve their task-level safety and approval requirements; do not
fall back to a legacy external-provider or no-skill classification. When a
prompt includes a product object and Common work, return independent child
routes with independent approval boundaries.

Treat `show`, `fetch`, `find`, and `what was created` as reads. A read proceeds
after input and environment validation and does not require write approval.
Treat `create`, `add`, `update`, `edit`, `activate`, `inactivate`, `delete`,
population maintenance, import, and ESS submission as side effects. Validate
them and show the exact proposed change, but stop for explicit approval before
the first live mutation. A search action that uses HTTP POST solely because the
runtime API accepts its query in a body is still a read; classify approval by
business effect, not by HTTP verb.

## Source-pack execution continuation

For an approved implementation source pack or Run Book queue, retain the
ordered task queue until it is complete, the consultant stops it, or a declared
blocker occurs. Complete local intake, task-detail retrieval, metadata reads,
reference resolution, duplicate checks, and other applicable read-only
preflight in the same turn. These intermediate results are not response
boundaries. Keep control until the next exact state-changing operation or
fully resolved batch has an immutable preview.

Before any Goal Management mutation, call
`goal-management-common/scripts/plan_guided_next_actions.py` through
`resolve_controlled_next_task` with the complete resolved task list for the
current input. The list may contain one, two, or any positive number of tasks;
never substitute the common five-task example or hard-code task names. Require
an approved current plan fingerprint, created Run Book, delivered dashboard,
and an exact match between the requested task and the earliest unfinished
applicable task. A later-task instruction or approval cannot override this
control. Completed and explicitly Not Applicable tasks may advance the queue;
all other statuses remain unfinished. Missing, duplicate, stale, ambiguous, or
contradictory control evidence returns `BLOCKED` before payload preparation or
live lookup.

Pause before every unapproved state change. Approval is a temporary execution
gate, not task completion. After contextual approval of the unchanged preview,
continue through submission, terminal monitoring, fresh-state verification,
and any Run Book status update that was explicitly included in that preview.
Then present the next queued task preview without requiring the consultant to
ask for progress. Stop only for an approval gate, unresolved business input,
terminal failure, timeout, verification failure, changed preview, unsupported
route, or an explicit consultant stop or reprioritization.

One approval may cover multiple state changes only when the preview enumerates
the complete target environment, ordered operations, exact payloads or
immutable artifacts, verification, and conditional Run Book update. If a
later operation needs an identifier or state produced by an earlier operation,
prepare a new preview after that state is verified unless the owning task has a
supported stable-key contract that resolves the entire batch in advance. Never
invent an identifier, silently split an approved batch, reuse approval after a
target or payload changes, or automatically retry an uncertain mutation.
Approval cardinality never selects transport cardinality. Resolve the method,
path, media type, request count, and body shape independently for every
operation from its current supported contract. A single approval may therefore
authorize several independently verified PATCH requests without creating an
ADF batch request.

An explicit stop, discard, or do-not-continue instruction returns the
pillar-local continuation state `stopped`, clears the queued next action, and
permits no later Goal Management mutation until a fresh intake/control check.
Preserve evidence and never reinterpret discard as Run Book force-completion.

Do not report success merely because a write or process was initiated. A task
is complete only after its owning task's terminal and reconciliation rules
pass. Read-only continuation never authorizes a mutation; every Fusion Run
Book write, REST write, Data Loader submission, import, ESS submission, or
other external state change remains subject to the shared Goal Management
approval convention and the owning skill's stricter rules.

## Repository-only runtime boundary

This parent and its task skills are the complete repository entry point for
Goal Management branch requests in this functional area. During
repository-scoped QA, resolve and execute only repository manifests and their
declared dependencies. If a required provider is absent from the repository,
return the documented blocker and resume context instead of silently
substituting an external capability.

## Runtime dependency invocation

For every live Fusion REST query or operation for an approved Goal Management
functional area, invoke the owning task skill, then
`core.auth.fusion-oauth-authentication`, then `core.fusion-api.rest-api-client`.
Do not insert a Goal Management connection parser, token-cache selector, local
properties file, or other pillar-level authentication adapter between the task
skill and those core services. The core authentication and REST-client skills
own resolution of `core/auth/fusionEnv.properties`, token-cache reuse, OAuth
handoff, and authentication retry behavior.

Do not ask a consultant for connection or environment details when the core
environment properties are complete. Ask only when the core service reports
that required properties are missing or incomplete, or when a consultant
explicitly requests a conflicting environment override. Never create a custom
connection file as a fallback.

Establish authentication with one harmless serialized REST request before
starting object metadata or data calls. Do not launch first-use calls in
parallel while the token cache may be missing or expired.

Classify request media type before the first REST call. ADF batch requests use
`application/vnd.oracle.adf.batch+json`; custom action paths containing
`/action/` use `application/vnd.oracle.adf.action+json`; ordinary entity JSON
writes use `application/json`; ordinary GET uses `Accept: application/json` and
has no request content type when it has no body. Fail closed when path and
payload classification conflict.

## Current taxonomy and common-task precedence

This is the compatibility boundary for the migrated guidance above. The
current catalog and generated task hierarchy take precedence where the legacy
terminology or routing differs.

- Route foundation work to [Goal Management Common](goal-management-common/SKILL.md), not to an offering-level
  `ora-resource` folder: [profile options](goal-management-common/manage-profile-options/SKILL.md),
  [administrator profile values](goal-management-common/manage-administrator-profile-values/SKILL.md),
  [common lookups](goal-management-common/manage-common-lookups/SKILL.md), [value sets](goal-management-common/manage-value-sets/SKILL.md),
  [descriptive flexfields](goal-management-common/manage-descriptive-flexfields/SKILL.md),
  [extensible flexfields](goal-management-common/manage-extensible-flexfields/SKILL.md),
  [key flexfields](goal-management-common/manage-key-flexfields/SKILL.md),
  [reference data sets](goal-management-common/manage-reference-data-sets/SKILL.md), and
  [currencies](goal-management-common/manage-currencies/SKILL.md).
- Foundation profile-option, lookup, value-set, and descriptive-flexfield
  requests route to their generated **Common** task skills. Product task
  helpers may supply Goal Management context, but they never replace the
  Common route. Foundation REST transport remains with
  `core.fusion-api.apps-common` and its current child skills; task helpers
  must not duplicate that transport.
- `Manage Reference Data Sets` and `Manage Currencies` remain catalog-backed
  Common tasks for catalog identity, but their local Goal Management skills are delegation
  facades only. Their reads and mutations execute through the owning Common or
  manual workflow outside Goal Management; provider absence remains a blocker.
- `HRG_WORKER_GOALS` remains valid only where current Fusion runtime metadata
  requires that API functional-area value. It is not the offering identity or
  on-disk taxonomy.

## Dependent setup ownership

Read and apply [Goal Management Dependent Setup Routing](goal-management-common/dependent-setup-routing.md)
before resolving a shared or cross-product dependency. Product-local
validation may perform declared read-only dependency calls. Any dependency
create, update, delete, deployment, import, or setup maintenance becomes an
independent child route to its owner with its own preview, approval, execution,
and verification. A Goal Management-owned association to an already resolved
dependency remains with the applicable Goal Management object task.


## Standard core authentication routing

This contract applies to every approved Goal Management functional-area object
and Common dependency. Use the repository-provided core authentication and REST
services without copying or overriding their configuration logic in this
pillar.

1. Let `core.auth.fusion-oauth-authentication` read the standard repository
   environment properties and reuse its standard secure per-user token cache.
2. When Oracle SSO interaction is required, follow the repository Chrome-first
   browser policy. The browser is only the sign-in handoff; the core REST client
   remains the data transport.
3. Continue the selected read automatically after successful authentication.
4. Ask the user only if the standard environment properties are incomplete or
   the supported authentication handoff cannot complete.

Authentication does not authorize a mutation. Every state-changing operation
remains behind its owning task skill's immutable preview and explicit approval
gate.
