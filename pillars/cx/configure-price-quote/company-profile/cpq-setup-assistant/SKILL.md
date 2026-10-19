---
skill_id: "cx.configure-price-quote.company-profile.cpq-setup-assistant"
name: "CPQ Setup Assistant Setup Task Guidance"
description: "Validates CPQ Setup Assistant state and routes approved CPQ mutations through Fusion Data Loader under the Company Profile functional area."
layer: "pillar"
pillar: "CX"
offering: "Configure Price Quote"
functional_area: "Company Profile"
functional_area_code: "ORA_SVC_COMPANY_PROFILE"
task_code: "ORA_CPQ_SETUP_ASSISTANT"
task_name: "CPQ Setup Assistant"
parent_skill_id: "cx.configure-price-quote.company-profile"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "hybrid"
owner_team: "CX configure price quote pillar team"
version: "0.4.36"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "cpq_stage_proposal_and_core_preflight"
  - "cpq_task_hook_preview_input"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "cpq_setup_assistant_execution_result"
  - "cpq_data_loader_handoff"
  - "sanitized_diagnostics"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
uses_core:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
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
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/configure-price-quote/company-profile/cpq-setup-assistant/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/configure-price-quote/company-profile/cpq-setup-assistant/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/pillars/cx/configure-price-quote/company-profile/cpq-setup-assistant/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/pillars/cx/configure-price-quote/company-profile/cpq-setup-assistant/diagnostics/"
    versioning_policy: "append-only"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Retains exact recovery snapshots in owner-private local storage outside the repository and project before approval consumption; historical commands reverify ledger fingerprints."
  - "Records approval fingerprints, expiry, and consumed nonces in the project CPQ approval ledger."
  - "Validates live registration, Task Hook readiness, current CPQ state and LOVs at routed preview and pre-upload steps."
  - "Reconciles exact completed initialization/child jobs and complete approved child outcomes; retains unresolved-stage markers."
  - "Locks the target before submission, rechecks current Fusion state, and permits explicit pre-handoff recovery through a read-only check."
  - "Reads CPQ Setup Assistant state through approved read-only Fusion lookups."
  - "Initializes, configures, and submits CPQ Setup Assistant through approved Fusion Data Loader imports after explicit approval."
required_privileges:
  - "Valid Fusion OAuth access for the selected CPQ Setup Assistant environment."
---

# CPQ Setup Assistant Setup Task Guidance

## Purpose

Provides task-specific planning, readiness validation, and controlled Data Loader execution guidance for `CPQ Setup Assistant` under `Company Profile`.

## Setup Task Skill Contract

- task_code: `ORA_CPQ_SETUP_ASSISTANT`
- task_name: `CPQ Setup Assistant`
- parent_skill_id: `cx.configure-price-quote.company-profile`
- pillar: `CX`
- offering: `Configure Price Quote`
- functional_area: `Company Profile`
- functional_area_code: `ORA_SVC_COMPANY_PROFILE`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, validating, and executing `CPQ Setup Assistant` under `Company Profile`. Use direct REST only for the declared read-only deployment, status, discovery, reconciliation, and LOV checks. Route every initialization, Company Profile update, CPQ user creation, and submission mutation through `core.data-loader`.

Use it directly when the objective explicitly concerns CPQ Setup Assistant, CPQ
onboarding or initial setup, CPQ company profile setup, or CPQ administrator
setup. These signals resolve to the following scope:

- Pillar: `CX`
- Offering: `Configure Price Quote`
- Functional area: `Company Profile`
- Setup task: `CPQ Setup Assistant`

If company or administrator setup is requested without CPQ or Configure Price
Quote in scope, do not assume this skill applies; resolve the offering first.
For a matching CPQ objective, use this task skill as the next action and follow
its discovery, deployment-validation, and approval gates before any mutation.

## Setup Task Metadata

- Task name: `CPQ Setup Assistant`
- Task code: `ORA_CPQ_SETUP_ASSISTANT`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## Data Loader Execution Model

The CPQ Setup Assistant is a customer-impacting configuration action. The
validated Data Loader objects are `cpqSetupAssistantInitialize` and
`setupAssistants`. The `setupAssistants` object contains the parent `Status`
field plus the `CompanyProfiles` and `CPQUsers` child sections. The compiled
registry and REST client remain read-only; they must not perform a CPQ POST or
PATCH mutation.

## Data Loader Handoff

### Approval ordering for every stage

For `INITIALIZE`, `IMPORT_COMPANY_AND_ADMINS`, and `SUBMIT`, use this order:
prepare the metadata-backed immutable archive through Core Data Loader; evaluate
Task Hook readiness; build the Task Hook preview and CPQ guard manifest; present
the exact stage preview; obtain one explicit approval; record that approval and
execute once through the guard. Complete deployment/status checks before
initialization preparation, and stage-specific discovery and reconciliation
before preparing later stages.

Readiness is eligibility to build an approval preview, not authorization to
execute. Approval remains pending during Task Hook validation and manifest
construction. Missing approval alone must not block those read-only steps or be
recorded as a passed approval check. The current stage's manifest, reviewed
binding, actor attribution, approval record, expiry and nonce are produced or
checked at their prescribed preview/approve/execute steps, not required as inputs
to readiness. Prior-stage completion and reconciliation evidence remain required
where applicable. Missing data, unsafe state, unsupported capabilities, or invalid
artifacts still block preview; no waiver or fabricated approval is implied.

For initialization preparation, read the
[initialization registration contract](references/data-loader-registration-contract.md#initialization)
before deciding that the live action is unsupported. Evaluate the current Core
metadata and validation result; do not require optional correlation or transport
columns, or treat fields absent from Core's metadata projection as proof that
the live action is missing. Unavailable action evidence remains indeterminate
and blocks execution; it is not permission to invent a route or payload.

Task Hook's `ready` result selects the supported assisted rule-evaluation route.
Read its execution guide and evaluate applicable CPQ registry nodes, recording
node IDs, prerequisites, outcomes and sanitized evidence through the existing
project diagnostic workflow. Aggregate the results in Task Hook's existing
ordered `ruleResults` format. A separate evaluator executable or independently
authenticated evaluator is not required by this route. Registry readiness alone
is not a passed evaluation. Keep current-stage approval pending and unrelated
stage rules `not_applicable` only when their applicability excludes them; do not
mark a missing initialization contract as passed. Build the preview through the
existing Task Hook and CPQ guard commands without constructing their outputs
manually. Include evidence references in the existing stage preview's review
context so assisted evaluation can be reviewed without claiming independent
verification or changing the approval envelope.

Only the guard's approval and execution steps authorize a mutation. They retain
exact binding, explicit confirmation, attribution, expiry, one-time consumption,
target, live-state and reconciliation checks. Never reuse approval across stages
or ask twice for the same stage. A changed or expired preview requires fresh
validation and approval under the existing guard contract.

Before live approval, inspect `cpq_data_loader_guard.py capabilities`. The
pillar uses explicit local approval: `liveApprovalAvailable` is true, while
`authenticated-actor` remains false. Obtain the user's explicit approval of
the exact stage preview, then record it with `--confirmed`, the exact
`--reviewed-binding`, and a nonempty caller-supplied `--actor` for audit
attribution. The actor is not independently authenticated; do not describe it
as a verified session identity or infer approval from OAuth/OS credentials.
ATEAM-1461 recommendation 3 remains unmet. This mode does not constitute an
exemption or add independent approval verification inside Core.
Requirements for authenticated identity, server-side conditional writes,
cross-host coordination, or non-bypassable Core enforcement remain unsupported;
declare them in proposal `requiredGuarantees` and stop with the capability
blocker. Never fall back to direct Core upload. See
[live validation](references/live-validation.md) for the opt-in test procedure.

Every mutation handoff must use [cpq_data_loader_guard.py](scripts/cpq_data_loader_guard.py)
after Core Data Loader preparation and Task Validator preview. Read
[CPQ approval guard](references/cpq-approval-guard.md) before preparing the
approval. The guard separates `INITIALIZE`, `IMPORT_COMPANY_AND_ADMINS`, and
`SUBMIT`, binds the exact preview and archive, and consumes approval before
delegating to Core's existing prepared-artifact upload. Do not invoke Core's
upload command directly for CPQ mutations. Capture the existing Data Loader
user approval through this guard; do not ask twice for the same stage.
Preview creates one canonical manifest containing the stage, exact target,
ordered operations, artifact digest, administrator set, generated redacted
business summary, expiry, and nonce. Approve and execute that unchanged
manifest; nonce and expiry are never regenerated at approval.
Preview now requires `--task-input` for the Task Hook preview input and performs
the declared live metadata/state/LOV reads before creating a version 3 manifest.
The exact effective initiation settings and discovered baseline are bound to it.
At upload, [cpq_execution.py](scripts/cpq_execution.py) rechecks that live binding
and verifies actual Core upload/initiation callbacks without allowing a
routing-changing retry or token-refresh replay. Explicit approval of the exact
manifest and the durable approval controls remain mandatory.
After accepted initialization, use `reconcile-initialization` on the explicit
completion continuation; unresolved initialization blocks further mutations.
After a child-import attempt, run the guard's `reconcile` step with its consumed
child manifest and approval record. This step invokes the already-declared
`resolve_cpq_setup_assistant_record` read through Core's standard Fusion client,
first verifies successful completion of the exact recorded child load, compares
the complete expected company/admin state against the baseline plus approved
operations, and generates a ledger-verified receipt. Unexpected administrators
and changes to retained business values block reconciliation. In the `EXISTS`
and `EXISTS_WITH_BU` branches, allow only Fusion's blank-to-populated
`Addressline`, `Country`, or `TaxRegNumber` derivation after an approved Legal
Entity selection; a replaced retained value or any other unapproved change
still blocks reconciliation. Pending earlier
stages remain recorded across process exit and block later mutations. Missing, ambiguous,
incomplete, or mismatched results stop submission. Build the final parent source
and a new final manifest only after success, pass that receipt using
`--reconciliation`, and obtain the separate final-submission approval. A manually
supplied verification flag or response fingerprint is not sufficient.
At final execution, acquire the durable target submission lock atomically with
approval consumption, then use that same declared read-only lookup to compare
current Company Profile, CPQ-user, and assistant identity/status fingerprints
with the approved receipt. Stop on changed or unreadable state; never rebuild
the manifest under the old approval. The target lock blocks competing approvals
and further mutations for this setup across projects using this checkout's
shared pillar-local registry. Retain it after
accepted or uncertain handoff. On an explicit recovery request, use
`recover-submission`; it may release only a lock that has not entered Core
handoff, after a successful read-only readiness check. Recovery invalidates the
old reconciliation and never restores the consumed approval. See the guard
reference for the external-change race and checkout-local coordination limits.

For complete company/admin reconciliation and final-state verification, use the
bounded child-collection discovery declared in `ora_reference_lookups.md`.
Read all pages and bracket them with assistant identity/status checks; reject
malformed pages, duplicate identities, incomplete reads or changed targets.
This is a finite verification step, not progress polling.

Execution retains its exact manifest/approval in protected local recovery storage
before consuming the nonce. Historical reconciliation and inspection can use
`--attempt-id <original-nonce>` after temporary files are removed. Retention does
not authorize execution or release an uncertain attempt. Preserve evidence for
outstanding and dependent workflows; use `retain-evidence` to migrate existing
consumed attempts before deleting their original files. See the approval guard
reference for storage, migration and closure requirements. Recovery storage
provides no independent approving-user authentication or Core approval-ID
verification; those ATEAM-1461 recommendation 3 guarantees remain unavailable.

The compiled registry is a readiness and authenticated-read graph. Its
`CPQ.INITIALIZATION_READY` and `CPQ.CONFIGURATION_READY` terminals hand off a
redacted, immutable readiness record to Core Data Loader; the terminals neither
execute nor authorize a mutation.

After readiness and the applicable explicit approval, hand off through the
CPQ guard to `core.data-loader`. Use `cpqSetupAssistantInitialize` for initialization,
`setupAssistants` with `CompanyProfiles` and `CPQUsers` child rows for company
and administrator changes, then a parent `setupAssistants` row for final
submission with `Status` set to `SUBMITTED`. Resolve `RestAction`, parent/child
linkage, keys, and writable fields from current Data Loader metadata; do not
infer them from retired REST payloads.
Preserve source-artifact fingerprints and approval binding, but never persist
raw mutation values, OAuth tokens, or authorization headers in project artifacts.

For the supplied registered `setupAssistants` hierarchy, apply the explicit
parent and child write contracts in
[data-loader-registration-contract.md](references/data-loader-registration-contract.md).
This registration permits a Company Profile update only through its discovered
child identity, a new CPQ administrator only with first name, last name, and
email, and final submission only through the parent patch contract. Do not
infer a child create, update, identifier, or parent-link value that the current
registration does not establish.

### CPQ user create-field rule

For an approved new `CPQUsers` row, resolve the complete current child
attribute template—not merely a compact generated DAT sample. Treat every
attribute marked **Mandatory** or **Required for new records** as required when
the registered child action resolves to create. In the registered CPQ-user
contract, this requires `FirstName`, `LastName`, and `Email` for every proposed
administrator.
Use the registered parent link and the registered create `RestAction` for each
child row. Do not supply `CPQUserId`, `Id`, `PartyNumber`, or `UserName` for a
new administrator merely because a template displays it as a key, surrogate,
or response attribute.

The CPQ-specific create contract treats generated identity attributes as
server-generated even when the generic template marks them Mandatory or
Required for new records. If separate route evidence requires a caller-supplied
generated identity, or current metadata omits a required designation for any of
the three administrator fields, stop before approval with a catalog/metadata
mismatch. Do not weaken the CPQ-user contract or substitute a direct REST
mutation.

### Loader transport-field rule

Treat `REST-Framework-Version` and `Content-Type` as registration-controlled
transport fields, not business configuration. A generated Data Loader sample
may display `SAMPLE_VALUE` for either optional string field; that value is a
generator placeholder and is never eligible for upload. Before building the
immutable archive, resolve whether each field must be omitted or populated
from the current registered business-object metadata/template. Do not copy the
client's request defaults into a loader row and do not guess a value from a
prior REST call. `RestAction` must likewise come from current metadata; for
the initialization object, use the live registered create action only when it
resolves unambiguously. If registration metadata does not establish a required
transport-field value, stop with a catalog/metadata mismatch before approval
or upload.

## Access and Approval Gates

Do not check for, request confirmation of, or persist evidence about the three
legacy initial-user roles. Authentication and authorization failures returned by a
direct HTTPS call are handled as `auth/authz` failures. The remaining user gates
are explicit approval to initialize CPQ and explicit approval of the exact
post-discovery change summary before any Company Profile update, administrator
creation, or submission.

## CPQ Deployment Preflight

Before a configuration workflow enters Setup Assistant initialization, verify that
CPQ is deployed in the selected environment. Use the documented unauthenticated
deployment-version lookup; do not attach OAuth credentials, an `Authorization`
header, or any other authentication material. A `404` result means CPQ is not
deployed: show “CPQ is not dpeloyed in this instance and hence cannot proceed with
Setups now.” and stop without initialization or any Setup Assistant call. Any other
HTTP response confirms that the deployment endpoint is present and permits the
workflow to continue directly to the separate initialization approval and initialization. Do not expose
the endpoint, HTTP status, or transport details in the customer-facing response.

## Customer-Facing API Disclosure Rule

In every API invocation flow, keep transport and request implementation details internal. Customer-facing responses must not include an API endpoint or path, HTTP method, request headers, query parameters, request body, payload field names, identifiers, or raw request/response content. This applies to success, approval, progress, validation, and error messages. Communicate the business action, affected configuration, plain-language outcome, and safe next action instead. Store any required operational diagnostics only in the approved project workspace, with sensitive values redacted.

When values are retrieved from the Setup Assistant LOV service, retain the complete response internally for validation only. Ask the customer for each required business value first. The exception is an existing-company branch: when `IsDataExisting` is `EXISTS` or `EXISTS_WITH_BU`, show the eligible Legal Entity display values before asking the customer to select one, so the selection comes from the verified list rather than an arbitrary value. For all other choices, provide possible values only if the customer explicitly asks for them, and then show only the display values for that single relevant LOV category (Country, Corporate Currency, Legal Entity, or Business Unit). Never show the complete LOV response, unrelated LOV categories, record metadata, or identifiers.

## Address Line 1 Minimum-Data Rule

For a new-company flow, `Addressline` represents required Legal Address **Address Line 1** only. Request a single street, building, premises, or locality line—not a complete postal address. Do not collect or include a city, state/province, postal or PIN code, country text, additional address lines, or other address components; country is selected separately from its LOV. If the customer provides a complete address or includes those components in the proposed line, ask them to provide Address Line 1 alone before validation and submission. Collect no additional address detail during this initial setup unless a separately approved workflow requires it.

Follow the mandatory workflow below. Do not ask for an administrator until the company-profile branch and required company details are resolved. Do not submit before reporting the discovered role mappings and starter-data state.

## Mandatory Step-by-Step Workflow

1. **Verify CPQ deployment.** Before any Setup Assistant call, use the unauthenticated deployment-version lookup for the selected environment. If it returns `404`, show “CPQ is not dpeloyed in this instance and hence cannot proceed with Setups now.” and stop. For any other HTTP response, continue with the read-only status check.
2. **Check status before initialization.** Read the CPQ Setup Assistant status once. If it is complete, in progress, reports an error, or is indeterminate, report the matching customer-facing outcome and stop without initialization. For a `COMPLETED` result, offer this ready-to-use next prompt: `Publish Adaptive Search for oraclecpqo_transaction and oraclecpqo_transactionLine.` Only `SETUP_NOT_DONE` proceeds to initialization approval.
3. **Initialize CPQ only when needed.** When the pre-initialization status is `SETUP_NOT_DONE`, prepare the immutable initialization archive, complete Task Hook readiness with approval pending, and build the guard preview. Present that exact initialization effect and obtain one explicit stage approval before initializing CPQ once. Do not assess Legal Entity, Business Unit, or other enterprise setup data before initialization. Do not repeat initialization automatically.
4. **Rediscover and classify the initialized state.** Immediately after the approved one-time initialization, read the CPQ Setup Assistant, Company Profile, CPQ Users, role mappings, starter-data child, and CPQ-owned progress. Treat `Status` and `IsDataExisting` as read-only discovery values and use them only to select the workflow branch. A post-initialization `SETUP_NOT_DONE` result proceeds to Company Profile input collection; `IN_PROGRESS`, `ERROR`, `COMPLETED`, and unknown results report their matching customer-facing outcome and stop. The sole exception is the governed final submission: after all required data, notices, and explicit approval are complete, submit exactly `Status` to `SUBMITTED`. Never include `IsDataExisting` in a payload or make any other `Status` change. Then translate the result with [observed-state-branches.md](references/observed-state-branches.md).
5. **Collect company details by existing-data branch.** Retrieve Setup Assistant LOV data internally, then ask for each required Country, Corporate Currency, Legal Entity, or Business Unit value without preemptively displaying lists, except for Legal Entity in the `EXISTS` and `EXISTS_WITH_BU` branches: show its eligible display values upfront and require the customer's explicit selection from that list. If the customer explicitly asks for possible values for another category, show only the display values for that requested category; never show the complete LOV response. Explain, when needed, that the unique CPQ Company Identifier (also called CPQ Company Name) maps to the REST `CompanyName` field, while Enterprise Name maps separately to the Fusion `EnterpriseName` field. When `IsDataExisting` is `DOESNT_EXIST`, first inspect the returned configurable Company Profile fields: enterprise name, CPQ company identifier, Address Line 1, country, corporate currency, and, when applicable, tax registration number. If any are populated, tell the user that values are already present despite the new-company state, show the current values (redacting tax registration number), and ask whether to retain them or provide updates; collect only missing required values and requested changes. A retained country or currency must still be present in the current LOV response. Otherwise, collect enterprise name, currency, country, Address Line 1 only, and CPQ company identifier. Do not collect a complete address, postal or PIN code, state/province, city, country text, or additional address lines. In either case, do not ask for Legal Entity or Business Unit because Company Profile Setup creates them. When it is `EXISTS`, keep enterprise name read-only, do not collect address or country, require the user to provide the CPQ company identifier and select Legal Entity and Business Unit, and allow currency to be updated or require it when absent. When it is `EXISTS_WITH_BU`, apply the `EXISTS` flow, including the required CPQ company identifier, but preserve the discovered Business Unit as read-only. If `IsDataExisting` reports a partial setup or an active LDAP job, stop with the task-specific customer message instead of collecting changes.
6. **Validate the company proposal.** Confirm that every selected country, currency, legal entity, and business unit exists in the current lists of values, and retain the discovered Company Profile ID. Do not prepare a Data Loader row at this stage.
7. **Collect CPQ administrators.** Only after the company details are ready, first ask whether the current logged-in user should be created as a CPQ administrator. If yes, collect that user's first name, last name, and valid email address; do not assume or expose identity values from the session. Then ask whether additional CPQ administrators should be added. If yes, collect first name, last name, and valid email address for each additional user. Reconcile every requested user against discovered CPQ users and resource records; do not create duplicates. Initial setup requires at least one valid administrator, which may be a discovered administrator or an approved, validated new administrator. If discovery already confirms one or more valid administrators and no addition is requested, do not create a user; reconcile that existing state before submission.
8. **Notify before submission.** Report the discovered CPQ role mappings as seeded read-only information and report starter-data readiness as unavailable, ready, running, complete, or failed. Do not create, delete, remap, import, or rerun either resource through this skill. If starter data is running or failed, stop submission and explain the safe next action.
9. **Validate, preview, then obtain approval.** For each stage, prepare its immutable source through Core Data Loader, complete Task Hook readiness with approval pending, and build the Task Hook preview and CPQ guard manifest. Show a redacted summary of the changed company fields, selected legal entity and business unit, every proposed administrator, target environment, role/starter-data notice, and intended submission. The customer summary must describe the business change only; never include a loader source, endpoint, request payload, or other implementation detail. Obtain explicit approval for that exact summary before each immutable Data Loader submission.
10. **Execute once in order.** Use `cpqSetupAssistantInitialize`, then one immutable pre-submission `setupAssistants` source containing the changed `CompanyProfiles` row and every approved `CPQUsers` row, then a final parent `setupAssistants` source with `Status` set to `SUBMITTED`. Apply the registered child patch/create contracts in [data-loader-registration-contract.md](references/data-loader-registration-contract.md): the combined child source must update only the discovered Company Profile and create every new administrator with `FirstName`, `LastName`, and `Email`, treating both **Mandatory** and **Required for new records** as required for that create action. Do not create a Company Profile or supply a generated CPQ-user identity. Bind the exact combined child source, ordered operation set, and redacted change summary to approval. Validate each exact metadata-backed source and immutable archive through `core.data-loader`; reject any `SAMPLE_VALUE` transport-field placeholder and resolve optional transport fields from the current business-object registration before approval; never retry an upload or initiation automatically. After the combined child import is accepted or uncertain, rediscover both Company Profile and CPQ-user state before any final submission. Once final submission is accepted, tell the user: “CPQ Setup Assistant has been submitted. It typically completes in approximately 12–15 minutes. You can track progress in the Schedule Processes UI by monitoring the Run Setup Assistant process.” This is advisory timing, not a completion guarantee. Immediately after final submission, perform exactly one read-only status and progress retrieval, translate its CPQ-owned result for the user, then end the execution. Follow [api-flow.md](references/api-flow.md).
11. **Refresh status later only on request.** After the required immediate post-submission retrieval, do not automatically poll, retry, resubmit, or make another status read. A later status refresh starts only when the user explicitly requests it: identify the target environment, perform exactly one read-only status GET with a 30-second HTTP request timeout and no retry, translate the returned CPQ-owned progress and Company Information prerequisite state using the user-facing status messages in [observed-state-branches.md](references/observed-state-branches.md), then end the request. Do not mention Adaptive Search in processing or incomplete status messages; offer its invocation prompt only for an overall successful completion. A timeout or read failure returns “CPQ setup status could not be determined safely”; retain sanitized diagnostics when available, do not infer completion, and do not mutate. Any later setup submission must independently rediscover the authoritative Fusion state before mutation.

The Data Loader path bypasses wizard-page validation. Validate required values before submission and use only IDs returned by the discovery request.

## Partial-Failure and Safe-Resume Contract

This contract applies when a company-profile update or administrator creation fails or has an uncertain outcome before submission is accepted.

1. **Stop mutations and retain the consumed approval.** Do not retry an uncertain operation, advance the stage, or submit the assistant.
2. **Inspect without replay.** Use `inspect-child-outcome` with the original consumed manifest and approval record. It verifies the recorded completion evidence when available and reads current company/admin state. Its classifications are `matches_approved`, `not_observed`, and `uncertain`. An absent record does not prove that the original job cannot apply later.
3. **Retain pending markers.** The sanitized diagnostic records observations, completion/state verification, and one next action; it never grants retry authority. Only ordinary full `reconcile` can advance a successfully completed child load after every expected result is verified.
4. **Recover proven zero-write attempts only.** `recover-prewrite` requires a durable pre-write phase, no remote identifiers, eligible unchanged assistant identity, and the execution lock. The nonce stays consumed. A released child attempt is excluded from latest-import selection; fresh reconciliation of the last actual import is required before final approval. If there was no actual child import, the verified existing-state route may be used.
5. **Escalate partial or uncertain writes.** This skill does not provide automated remaining-work retry. Resolve the original job through the supported operational process. Enabling resume requires a separately verified contract proving original-job finality and safe retry/idempotency. Fresh approval alone cannot clear uncertainty or authorize replay.

If submission was accepted or its acceptance is uncertain, do not use this pre-submission resume flow. Never submit again. Perform the one required immediate read-only status retrieval, then allow later status refresh only when user-triggered. If a retrieval reports an error, stop, retain the sanitized diagnostic, identify the affected CPQ setup step in plain language when the returned progress identifies one, and direct the user to the `Run Setup Assistant` ESS job logs in the Schedule Processes UI. If the log review does not resolve the issue, advise the user to log an Oracle Service Request (SR). If no affected step is returned, say that the affected step could not be determined safely; never infer one.

## Discovery-Driven Use Cases

Read [observed-state-branches.md](references/observed-state-branches.md) after the discovery request. Treat the returned state as authoritative for the target environment; do not infer a branch from a prior run.

| Use case | Read evidence | Allowed outcome |
|---|---|---|
| Assess an existing CPQ setup | Assistant `Status`, Company Information, and CPQ-owned setup-progress tasks | Report a customer-facing setup state from [observed-state-branches.md](references/observed-state-branches.md): Complete, Not started or incomplete, Processing, Needs attention, or Indeterminate. Do not use Sales Setup Assistant tasks as CPQ completion criteria. |
| Read and report CPQ status | User requests CPQ Setup Assistant status | Identify the target environment, perform exactly one direct read-only status GET with a 30-second HTTP request timeout and no retry, and report the returned state. When it is complete, offer this ready-to-use next prompt: `Publish Adaptive Search for oraclecpqo_transaction and oraclecpqo_transactionLine.` When it reports an error, identify the affected CPQ setup step when returned, direct the user to the `Run Setup Assistant` ESS job logs in the Schedule Processes UI, and advise logging an Oracle Service Request (SR) if log review does not resolve it. For a timeout or read failure, report the deterministic unable-to-determine result. Then end the request without initialization, submission, resubmission, or another mutation. |
| Initialize CPQ for a configuration workflow | The unauthenticated deployment-version lookup does not return `404`, the pre-initialization status is `SETUP_NOT_DONE`, and the user explicitly approves initialization | Initialize once, then immediately rediscover. Do not confirm Legal Entity, Business Unit, or other enterprise data first. |
| Reconcile existing company data | Company Profile state, discovered profile ID, and Setup Assistant LOV data | Explain the state in plain language. For `EXISTS` and `EXISTS_WITH_BU`, show the eligible Legal Entity display values upfront and require a selection from that list; ask for other required choices normally. Never expose the complete LOV response or overwrite by assumption. |
| Select existing legal entity and business unit | Setup Assistant LOV list and discovered Company Profile values | In `EXISTS` and `EXISTS_WITH_BU`, show eligible Legal Entity display values upfront and require an explicit selection from that returned list. Preselect a discovered value only where the UI permits it; if exactly one eligible value exists, retain it and show it to the customer. Preserve a discovered default business unit when the UI would lock it. |
| Configure company information | One discovered Company Profile and complete, validated values | Validate the UI-equivalent fields and PATCH only the discovered Company Profile ID. Do not send an unchanged field or a value that is absent from the applicable LOV response. |
| Provision CPQ administrators | `CPQUsers` is empty and the user supplies one or more validated administrators | Before creation, require a legal entity and business unit. On the first setup run, first ask whether the current logged-in user should be a CPQ administrator; if yes, collect their details. Then ask whether to add more administrators and collect each requested user's details. Require at least one administrator with first name, last name, and a valid, unique email address. Create only approved users, then rediscover to confirm them. If a person already exists, report whether they are already a CPQ administrator, have a different resource role, or need investigation; do not create a duplicate. |
| Review seeded CPQ roles | `CPQRoleMappings` | Report the discovered role mappings. This skill does not create, delete, or remap roles because that write contract has not been verified. |
| Assess starter-data readiness | `CPQStarterDataImport` and CPQ starter-data progress | Report whether starter-data processing is unavailable, ready, running, complete, or failed. Do not import or alter starter data through this API contract. |
| Submit and request status refresh | Required child data is present, approval covers submission, and the CPQ-specific flow is not complete | Submit once, then immediately perform exactly one bounded read-only progress request and report the customer-facing state. Later status refreshes require an explicit user request and perform exactly one bounded read-only progress request; neither path polls or retries. Any later submission independently rediscovers authoritative Fusion state before mutation. |
| Request a rerun | A CPQ-specific task has failed or must be repeated | Do not clear data or initiate a rerun through this skill. Explain that rerun eligibility is task-specific and requires an approved, separately verified API contract. |

Never expose implementation status codes to users. Translate every returned state using [observed-state-branches.md](references/observed-state-branches.md). Underlying company/business-unit data is not CPQ completion; determine completion from assistant status and only the CPQ-owned progress tasks.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `cpq_setup_assistant_execution_result`: the latest available overall Setup Assistant status and the latest available status for each individual CPQ-owned setup task.
- `cpq_data_loader_handoff`: a redacted, immutable readiness record for Core Data Loader; it contains operation IDs, source-artifact fingerprints, and digests, never mutation values or credentials.
- `sanitized_diagnostics`: internal project-workspace audit and recovery evidence only. Never include diagnostics, endpoint details, payloads, identifiers, or raw API data in customer-facing output.
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.configure-price-quote.company-profile` for functional-area sequencing and scope decisions. Before execution, load the compiled `ora_rule_registry.json`, obtain a `planned` execution plan, and use its readiness terminal only as the handoff record for Core Data Loader. Core Data Loader independently validates current metadata, source structure, immutable archive, and approval immediately before upload and initiation. Track token usage for any generated project artifact or skill-run record using the manifest policy.

Release the executable guard and complete test directory with this skill, and run the [release validation](references/cpq-approval-guard.md#release-validation) against the release candidate contents.
