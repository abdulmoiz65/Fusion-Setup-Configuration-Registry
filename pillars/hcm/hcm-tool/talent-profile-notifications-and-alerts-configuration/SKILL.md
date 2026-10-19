---
skill_id: "hcm.hcm-tool.talent-profile-notifications-and-alerts-configuration"
name: "Talent Profile Notifications and Alerts Configuration Implementation Guidance"
description: "Provides no-Fusion guidance, the checked-in blank template, or an unvalidated draft questionnaire, and implements explicitly requested FSM-supported Profile Management notification changes with export readback."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Talent Profile Notifications and Alerts Configuration"
functional_area_code: "CUSTOM_TALENT_PROFILE_NOTIFICATIONS_AND_ALERTS"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM hcm tool pillar team"
version: "0.4.1"
inputs:
  - "request_intent"
  - "implementation_objective"
  - "project_context"
  - "talent_profile_notifications_and_alerts_scope"
  - "talent_profile_notifications_and_alerts_requirements"
outputs:
  - "request_mode_result"
  - "blank_template_reference"
  - "draft_questionnaire"
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "core.data-loader"
uses_core:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
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
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/talent-profile-notifications-and-alerts-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/talent-profile-notifications-and-alerts-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/talent-profile-notifications-and-alerts-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "HRT_MANAGE_TALENT_NOTIFICATIONS"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "For an explicit implementation request only, performs one bounded read-only Talent Notifications REST capability check before FSM processing."
required_privileges:
  - "For implementation only, Manage Talent Notifications (HRT_MANAGE_TALENT_NOTIFICATIONS_PRIV)"
---

# Talent Profile Notifications and Alerts Configuration Implementation Guidance

## Purpose

Answer guidance questions, return the checked-in blank intake template, prepare
an unvalidated questionnaire from user-supplied values, or enable and disable
existing delivered Profile Management notifications when implementation is
explicitly requested.

For implementation, a fresh validated FSM export identifies eligible
notifications. A user may provide an exact notification identity or describe
the business event and recipient. Business intent can discover eligible
candidates, but it never selects a notification or authorizes persistence
without user confirmation.

The skill uses a fresh target-environment `Talent Notifications` FSM export as
the candidate, identity, current-state, package, and readback authority. It
changes only `NotifEnabled`, submits one minimal upsert package through
`core.data-loader`, and withholds success until fresh-export readback matches.

## When to Use

Use this skill for Talent Notifications guidance, requirements intake, or
delivered Profile Management notification enablement. Examples include:

```text
How does Talent Notifications configuration work?

Give me the blank Talent Profile Notifications requirements template.

Help me draft a questionnaire for worker feedback notifications.

Notification Identifier, Label, or Business Intent: Stop notifying workers when they receive feedback
Notification Enabled: No
Implement this change.
```

Direct conversation, XLSX, CSV, DOCX, PDF, and plain-text files are accepted.
The checked-in [requirements workbook](assets/talent-profile-notifications-requirements.xlsx)
is the default reusable blank intake template, not a generated output and not
an FSM prerequisite. Preserve every uploaded file unchanged and do not convert
non-XLSX input into XLSX.

Do not use this skill for Goal Management, Performance Management, or Talent
Review notifications; Profile Management notifications absent from the current
FSM provider; profile-update nudges; Touchpoints-specific notifications;
notification-policy recommendations; or direct Alerts Composer administration.

## Request Modes

Classify the user's requested outcome before resolving a project, checking
authentication, calling REST, requesting an FSM export, or invoking Data
Loader. Retain the selected `request_mode` in the response.

### `guidance_only`

Use when the user asks for explanations, examples, supported scope, input
formats, or process guidance without asking to inspect or change a target
environment. Answer from the checked-in skill, task metadata, and cited
guidance. Do not require `project_id`, authentication, notification rows, or a
complete enabled-state decision. Do not call Fusion or request persistence
approval. Return `guidance_provided`.

### `blank_template`

Use when the user asks for the blank or fillable requirements template. Return
the existing checked-in
[requirements workbook](assets/talent-profile-notifications-requirements.xlsx)
unchanged. Do not copy, regenerate, populate, rename, or validate it against
Fusion at runtime. Do not require `project_id`, authentication, configuration
rows, complete requirements, or persistence approval. Return
`blank_template_provided`.

### `draft_questionnaire`

Use when the user asks to collect, organize, or draft requirements without an
explicit request to implement them, including when they supply notification
values without a change instruction. Preserve only the values and context the
user supplied. Missing target or enabled-state values become open questions,
not validation failures. Do not infer delivered identities, enabled states,
scope, current values, technical fields, or recommendations. Clearly label the
result `UNVALIDATED DRAFT - no Fusion lookup or implementation has been
performed`. Return the draft in the conversation unless the user separately
requests an authored artifact. Do not convert conversation, CSV, DOCX, PDF, or
text into XLSX automatically. Do not call Fusion or request persistence
approval. Return `draft_questionnaire_provided`.

### `implementation`

Enter this mode only when the user explicitly asks to configure, enable,
disable, turn on, turn off, stop or start a notification, apply a change, or
otherwise implement the supplied requirements. Then follow the authenticated
preflight, FSM resolution, validation, packaging, approval, and readback
workflow below. A question, blank-template request, draft request, uploaded
file, or supplied row without change intent is not implementation authority.
An informational question such as "How can I disable a notification?" remains
guidance; a direct request such as "Can you disable this notification?" is
explicit implementation intent.
When intent remains ambiguous, remain side-effect-free, treat supplied values
as a draft, and ask whether the user wants implementation.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `HCM Tool` (`CUSTOM_HCM_TOOL`)
- Functional area / Setup Object: `Talent Profile Notifications and Alerts Configuration` (`CUSTOM_TALENT_PROFILE_NOTIFICATIONS_AND_ALERTS`)

## Setup Tasks

1. [Talent Notifications](talent-notifications.md) (`HRT_MANAGE_TALENT_NOTIFICATIONS`)

## Inputs

- `request_intent`: required only to classify the request mode; never default
  an ambiguous request to implementation.
- `guidance_only` and `blank_template` require no project, environment, release,
  authentication, or notification row.
- `draft_questionnaire` accepts partial direct conversation or an XLSX, CSV,
  DOCX, PDF, or plain-text source. Preserve uploaded files unchanged.
- `implementation` requires:
  - `project_id`: initialized durable FDOS project workspace;
  - `authenticated_fusion_environment`: `environment` and `restBaseUrl`
    resolved from the active FDOS Fusion authentication context, never
    requested as quarterly-release input;
  - `configuration_source`: direct conversation or one XLSX, CSV, DOCX, PDF,
    or plain-text file;
  - one or more complete rows containing `Notification Identifier, Label, or
    Business Intent` and `Notification Enabled`;
  - `run_id` to resume a clarification, approval, or readback state;
  - optional `alerts_composer_requirements`, retained only when explicitly
    supplied.

Accept `Notification Identifier or Label` as a backward-compatible header.
Also recognize `Business Intent` and `Desired Workforce Outcome` as source
aliases for the first logical field.

`Notification Enabled` accepts `Yes`, `No`, `Y`, `N`, `true`, `false`,
`Enabled`, `Disabled`, `On`, or `Off`, case-insensitively. Normalize the
explicit value to `Y` or `N`; never derive enablement solely from business
intent. Legacy files with separate Worklist and Email values fail with
migration guidance because they cannot safely map to one `NotifEnabled` value.

## Authenticated Preflight

Run this section only after `request_mode=implementation`. Guidance, blank
template, and draft-questionnaire requests must never reach this section.

Resolve the target only from the active
`core.auth.fusion-oauth-authentication` context. Use its `environment` and
`restBaseUrl` values together; do not select a host from user content, an
uploaded file, documentation, prior conversation, or a project artifact. If
the authenticated context is missing, malformed, or conflicts with the
selected project, stop with login or environment-configuration guidance.

Before requesting any FSM export, route exactly one capability check through
`core.fusion-api.rest-api-client`:

```text
GET /hcmRestApi/resources/11.13.18.05/talentNotifications
    ?onlyData=true
    &limit=1
timeout: 60 seconds
```

Use the authenticated context's `restBaseUrl`; never hard-code or accept a
different host. HTTP 200 with a JSON collection whose `items` value is an
array proves read capability, including when that array is empty. The bounded
response may contain zero or one item. It must not supply candidates, provider
identities, current state, package rows, or readback evidence.

The owning REST client may refresh rejected cached authentication once. A
blocked preflight retains one distinct reason code:

- final HTTP 401: `rest_capability_unauthenticated`;
- final HTTP 403: `rest_capability_forbidden`;
- HTTP 404: `rest_capability_unavailable`;
- request timeout: `rest_capability_timeout`;
- transport failure: `rest_capability_transport_failure`;
- any other non-200 response: `rest_capability_http_failure`;
- invalid JSON or collection shape: `rest_capability_malformed_response`.

Do not substitute a browser, direct HTTP client, another endpoint, or a
different environment.

`11.13.18.05` is an Oracle REST API resource version, not a Fusion quarterly
release. Never derive a quarterly release such as `26C` from that version, a
hostname, documentation, the current date, a catalog path, or prior
conversation. Quarterly release is optional audit metadata. Record it only
when an explicit quarterly-release field is already supplied by the
authenticated FDOS context or validated same-environment FSM metadata; retain
its source and timestamp. Omit both the value and its source when unavailable.
Conflicting trusted values are an evidence mismatch and must not be resolved
by asking the user for a release.

## Normalized Request Row

Persist for every accepted row:

- source file or direct-conversation reference and row/page location;
- original supplied identity or business-intent text;
- source kind: `identifier`, `label`, or `business_intent`;
- explicit requested `NotifEnabled` as `Y` or `N`;
- resolved provider identifier, identifier field, and `NotifLabel`;
- provider key status;
- mapping or candidate-confirmation evidence;
- FSM scope disposition and exact exported product-scope evidence;
- current value, changed/no-change disposition, and export fingerprint.

Identical duplicates consolidate with all source locations. Conflicting
duplicates block the complete set. A corrected row resumes the same run and
does not discard unrelated confirmed rows.

## Profile Management FSM Scope

Before identity or semantic resolution, partition every row in the fresh
validated current export by the row's exact `ProductCode` value:

- `ProductCode=HRT`: eligible Profile Management FSM row;
- any other nonblank product code: exported but out of scope;
- missing or ambiguous product scope for a selected row: invalid evidence.

Apply matching, candidate discovery, comparison, packaging, and readback only
to the eligible partition. This is a dynamic provider rule: do not embed the
currently observed names or count, and automatically admit a future exported
row when its exact `ProductCode` is `HRT`.

Never infer scope from a notification-code prefix, label, description,
business intent, or user-supplied tab name. The unfiltered export may be used
only after eligible resolution fails to diagnose an exact identity that exists
solely under another product code; it must never supply a candidate or package
row.

Return `validation_failed` with:

- `reason=out_of_scope_notification` when an exact identity matches only an
  exported non-HRT row, including HRA or HRR rows;
- `reason=unsupported_by_current_fsm_provider` when no row in the current FSM
  export establishes the requested identity;
- an evidence error when a selected row has blank, conflicting, or ambiguous
  product scope.

If any requested row is unsupported, out of scope, or has invalid scope
evidence, fail the complete configuration set before preview or package
preparation. Do not partially process otherwise eligible rows.

## Target Resolution

Use only the eligible `ProductCode=HRT` partition from the fresh current
export.

1. Resolve one unique exact case-sensitive `NotifId`, `NotifName`, or
   `NotifLabel` automatically.
2. A unique case/whitespace-only correction requires explicit mapping
   confirmation and returns `mapping_confirmation_required` until confirmed.
3. When the supplied value is business intent or has no direct match, discover
   candidates using only eligible rows and their exported `NotifLabel`,
   `NotifName`, `Description`, `GroupingKey`, `ViewInstanceName`, and
   `ProductCode`.
4. Every semantic result, including one strong result, requires confirmation.
   Present up to five meaningful candidates with the delivered label, provider
   identifier, current state, plain-language event/recipient context, and a
   short match rationale. Return `candidate_selection_required` without side
   effects.
5. Allow selection of one or more eligible candidates, rejection of all
   candidates, or
   refinement of the original intent. If no meaningful candidate exists,
   request more event or recipient context instead of guessing.
6. If no eligible target is established, apply the scope diagnostics above.
   Never expose an out-of-scope row as a semantic candidate.

Mapping and candidate confirmation clarify the target; neither is persistence
approval. A materially changed export invalidates every prior mapping and
selection and requires resolution again.

## Provider Identity Contract

For each confirmed row, use a nonblank unique `NotifId` as the execution and
readback identifier when the provider supplies it. When `NotifId` is blank,
use the same row's nonblank unique `NotifName` provisionally and record
`provider_key_status=provisional_notifname`. Disclose that `NotifId` is
unavailable.

Fail closed if the selected provider identifier is blank, duplicated, missing
from a later export, changes before preview or readback, or no longer resolves
to an exact `ProductCode=HRT` row. `NotifLabel` remains the business-facing
delivered name and is not substituted for an ambiguous provider key.

## Authoritative FSM Evidence

For `HRT_MANAGE_TALENT_NOTIFICATIONS`, obtain template, current-state, and
post-import exports through `shared.setup-export.task-level-export` and validate
them with `shared.validation.setup-data-validator`.

The current export must contain this exact ordered schema:

```text
NotifName, ViewInstanceName, GroupingKey, Description, NotifEnabled,
NotifLabel, ProductCode, NotifId
```

Validate the authenticated target, task identity, catalog flags, ZIP
integrity, every required member, FSM metadata, header order, encoding, BOM
state, quoting, native line endings, export time, and fingerprint. If trusted
FSM metadata explicitly supplies a quarterly release, record it with its
source and require any other trusted release value in the run to agree. Its
absence is valid and never blocks processing.

Do not substitute direct REST, HDL, browser automation, a provider API, or a
task-local adapter. The declared bounded REST GET is preflight capability
evidence only; it is never a runtime discovery, persistence, or readback
source for this skill.

## Minimal FSM Upsert Contract

Oracle FSM setup import is additive/updating: a package record absent from the
target can be created when that setup business object supports creation;
identical records are ignored; differing records are updated; target records
omitted from the package remain unchanged and are not deleted.

This skill remains update-only for existing delivered notifications. Every
selected notification must resolve in the fresh target export; it must never
invent or create a new notification definition.

For every approved selected `ProductCode=HRT` row:

1. Preserve the complete raw eight-column export row.
2. Compare only `NotifEnabled` with the requested `Y` or `N`.
3. Keep an already-matching row in the business preview but omit it from the
   import CSV.
4. For a changed row, preserve the serialized value of the other seven fields,
   including blanks and quoting, and replace only `NotifEnabled`.

Build one minimal package from the fresh export contract:

- retain `ASM_SETUP_CSV_METADATA.xml` unchanged;
- retain every required CSV member and its exact header and column order;
- include only approved changed rows in the applicable CSV;
- keep any required unused CSV member header-only rather than deleting it;
- preserve member names, row order among included rows, encoding, BOM state,
  quoting rules, and native line endings;
- do not include unrelated export rows as transport context;
- document omitted target rows as unchanged, never disabled or deleted.

When all selected rows already match, return `exact_match_no_change` without a
package, approval request, or import. For a package, record baseline export,
member inventory, header-only members, changed identities, omitted exact-match
rows, package row counts, and the final SHA-256.

## Deterministic Workflow

1. Classify the request before any project, authentication, REST, FSM, or Data
   Loader work. Return immediately for guidance, blank-template, or
   draft-questionnaire mode.
2. For explicit implementation mode, create an append-only `run_id`; preserve
   the source and normalize all rows.
3. Validate implementation input using
   [ora_input_validation.md](ora-resource/ora_input_validation.md), resolving
   the authenticated FDOS environment without requesting quarterly-release
   information.
4. Run the declared bounded Talent Notifications GET through the shared REST
   client and persist a sanitized capability receipt.
5. Obtain and validate fresh template and current-data exports, then partition
   the current rows by exact exported product scope.
6. Resolve exact or semantic targets only within the eligible partition. Pause
   in the applicable durable
   clarification state until the user confirms.
7. Select and validate the provider key for every confirmed row.
8. Compare current and requested values. Stop on an all-match request.
9. Construct and freeze the minimal FSM upsert ZIP. Any input, mapping,
   selection, export, key, member, row, or archive change invalidates preview.
10. Hand the same immutable ZIP and task context to `core.data-loader`. Its Task
   Hook preview and approval are the only persistence gate. Ask exactly:

   `Do you want to proceed with submitting the reviewed archive?`

11. After affirmative approval of the latest unchanged preview, let
   `core.data-loader` revalidate and submit once. Do not invoke another import
   route or retry an uncertain result.
12. Persist `pending_readback` after accepted initiation and end that invocation
    without polling or claiming success.

## Approval Preview

The preview includes:

- source and original supplied identity or business intent;
- exact resolved `NotifLabel`, provider identifier, identifier field, and key
  status;
- mapping and candidate confirmations;
- current and requested enabled states and changed/no-change disposition;
- validation result, Profile Management FSM eligibility, excluded scope, and
  channel-model boundary;
- changed package rows, omitted exact-match rows, required header-only members,
  archive fingerprint, and mandatory Data Loader task evidence;
- delivery-testing exclusion and Alert Foundation handoff status.

File upload, mapping confirmation, candidate selection, validation, silence,
or alert-handoff approval never constitutes persistence approval.

## Resumable Readback

Continue with the same `project_id` and `run_id`; do not re-enter requirements.

1. Verify continuation and approved archive fingerprints.
2. Ask `core.data-loader` for the existing load status. If active, retain
   `pending_readback`; if failed, timed out, or uncertain, return
   `readback_failed` without replay.
3. After successful completion, obtain and validate a fresh current export and
   partition it again by exact exported product scope.
4. Resolve the same provider identifiers to exactly one `ProductCode=HRT` row
   and compare saved `NotifEnabled` with the approved values.
5. Return `verified` only when every requested row matches. Otherwise return
   `readback_failed` with discrepancies and do not auto-correct.

## Execution States

| State | Meaning | Permitted next action |
|---|---|---|
| `guidance_provided` | Local guidance was returned without target-environment access | Ask another guidance question, request the blank template, prepare a draft, or explicitly request implementation |
| `blank_template_provided` | The existing checked-in blank workbook was returned unchanged | Fill it locally or explicitly request implementation later |
| `draft_questionnaire_provided` | Only user-supplied values were organized as an unvalidated draft | Add or correct values, or explicitly request implementation later |
| `validation_failed` | Input, FSM scope, evidence, key, package, or dependency validation failed | Correct the reported issue and resume validation |
| `mapping_confirmation_required` | One unique case/whitespace correction awaits confirmation | Confirm or replace the corrected delivered identity |
| `candidate_selection_required` | Semantic candidates await selection, rejection, or refinement | Confirm candidates or refine the business intent |
| `exact_match_no_change` | Every selected notification already matches | Stop without persistence |
| `approval_required` | The immutable preview is ready and no mutation occurred | Answer the one Data Loader submission question |
| `pending_readback` | Import is accepted or active; saved values are unproven | Continue the same run |
| `verified` | Completion and fresh-export readback match | Return the verified summary |
| `readback_failed` | Completion or readback is unsuccessful or uncertain | Stop without replay |

## Outputs

Return, as applicable:

- selected request mode and its side-effect disposition;
- local guidance with no claim about target-environment state;
- the unchanged checked-in workbook reference for blank-template mode;
- the explicitly labeled unvalidated draft and its open questions, containing
  user-supplied values only;

For implementation mode, persist:

- authenticated environment identity and sanitized REST capability receipt;
- optional trusted quarterly-release value, source, and timestamp when present;
- source references, original intent, and normalized notification rows;
- exact mappings, semantic candidates, rationale, and confirmation evidence;
- eligible and out-of-scope partition evidence, row counts, scope reason codes,
  and whole-set validation disposition;
- template, current-state, and readback export references and fingerprints;
- provider identifiers, key status, preserved source rows, and comparisons;
- validation results, minimal immutable FSM package inventory and SHA-256;
- business preview, one approval record, and execution reference;
- pending continuation state, row-level readback comparison, discrepancies,
  and final summary;
- Alert Foundation handoff, append-only run traceability, and token usage.

## Business-Facing Output Contract

Guidance and template responses state that no Fusion lookup or implementation
occurred. Draft questionnaires display the unvalidated-draft label, supplied
values, and open questions without delivered-notification or current-state
claims.

Implementation clarifications, previews, and summaries show original intent,
delivered notification name, provider identifier, current state, requested
state, and result. An unsupported or out-of-scope request receives a
plain-language scope reason. Keep raw FSM columns, product codes, task codes,
skill IDs, and archive mechanics in the durable audit record except for
mandatory Data Loader evidence in the approval preview.

## Alerts Composer Boundary

Enablement does not imply alert customization. Record recipients, channels,
conditions, message or template content, schedules, and timing only when the
user explicitly supplies them; never infer them from notification intent.

Use these handoff states:

- `not_requested`: no Alerts Composer requirement was supplied;
- `ready_for_handoff`: `hcm.hcm-tool.alert` exists and the structured handoff
  can be routed;
- `deferred`: the requirement is retained because Alert Foundation is absent
  or unavailable.

The handoff contains Jira/source references, original intent, resolved
notification context, explicitly supplied alert requirements, notification
execution status, open questions, and evidence references. This skill never
executes Alerts Composer or reports it configured. A deferred handoff does not
block supported Talent Notifications enablement.

## Durable Project Record

Require this record only for implementation mode. Guidance-only,
blank-template, and conversational draft-questionnaire responses do not require
a project or create an implementation run.

Persist each implementation run below:

```text
project/{project_id}/artifacts/pillars/hcm/hcm-tool/
  talent-profile-notifications-and-alerts-configuration/runs/{run_id}/
```

Use immutable or append-only artifacts for run state, sources, normalized rows,
candidate and mapping evidence, provider identities, exports, validations,
comparisons, preserved rows, package manifest, preview, approval, execution,
readback, alert handoff, final summary, and token usage. Never persist secrets,
tokens, authorization headers, or unnecessary sensitive customer data.

## Error and Retry Discipline

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`,
`auth_expired_or_invalid`, `authorization_or_privilege`,
`transport_or_environment`, `fusion_api_error`, `process_timeout`,
`process_failed`, `artifact_persistence`, or `approval_blocker`.

The owning REST client may refresh rejected cached authentication once; do not
otherwise retry the preflight automatically. Never retry an import without an
idempotency guarantee and new explicit approval, and never retry an uncertain
result. Preserve sanitized evidence and one safe next step.

## XLSX Boundary

For blank-template mode, return the existing checked-in XLSX unchanged. Do not
create a runtime copy or invoke spreadsheet generation. For draft mode, do not
convert conversational or non-XLSX input into a workbook automatically.

The reusable XLSX influences FSM only through:

- `Notification Identifier, Label, or Business Intent` to target resolution;
- `Notification Enabled` to `NotifEnabled` as `Y` or `N`.

The workbook never supplies technical fields. Spreadsheet-authoring
unavailability affects only template maintenance and does not block valid
conversation, CSV, DOCX, PDF, text, or existing-XLSX input.

Maintain instructions that explain that only currently FSM-supported Profile
Management notifications are eligible, without listing tab names, product
codes, or a fixed notification inventory.

## Source Boundary

The effective task catalog, Jira `GROW-8169`, approved HCM foundation baseline,
fresh target exports, and current Oracle FSM documentation define the source
boundary. Oracle documents upsert and non-deletion behavior for omitted setup
records. The baseline still describes separate worklist/email enablement, but
the live export and revised Jira clarification establish one `NotifEnabled`
field; record this mismatch without editing the baseline.

The fresh target export is the sole runtime scope authority. The source-backed
Talent Notifications GET is authorized only as a bounded preflight capability
check. Its records, including REST-only Profile Management observations,
remain audit evidence and cannot drive discovery, execution, or readback.
Other Talent Notifications product scopes are outside V1 even when the same
setup page displays them.

## Implementation Notes

Use [talent-notifications.md](talent-notifications.md) for internal task routing.
Load all six `ora-resource` files and the compiled registry before validation.
The registry must route the three side-effect-free request modes before the
implementation path. It authorizes one read-only Fusion REST preflight on that
implementation path and no REST write; `core.data-loader` remains the sole
executor and owner of the import approval.
