---
skill_id: "hcm.hcm-tool.profile-types-and-content-section-configuration"
name: "Profile Types and Content Section Configuration Implementation Guidance"
description: "Provides guidance and fillable templates for HCM Profile Types and Content Section configuration, lists configured sections and verifies named-section setup through GET-only Fusion REST reads, prepares review-only FSM ZIPs from runtime template metadata, and exports current Profile Types or Content Subscribers setup data."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Profile Types and Content Section Configuration"
functional_area_code: "CUSTOM_PROFILE_TYPES_AND_CONTENT_SECTION"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "HCM hcm tool pillar team"
version: "0.2.19"
inputs:
  - "project_id"
  - "implementation_objective"
  - "project_context"
  - "profile_types_and_content_section_configuration_scope"
  - "profile_types_and_content_section_configuration_requirements"
  - "fusion_environment_context"
  - "requested_operation"
  - "read_only_verification_request"
  - "export_scope"
  - "export_options"
  - "completed_export_request_template"
  - "fsm_import_zip"
  - "fsm_source_template_zip"
  - "profile_type_parent_template_lookup"
  - "rest_template_sections_response"
  - "rest_section_properties_response"
  - "rest_person_section_properties_response"
  - "rest_target_content_sections_response"
  - "rest_profile_types_response"
  - "rest_person_content_sections_response"
  - "rest_subscriber_catalog_response"
  - "fsm_profile_type_section_request"
  - "execution_approval"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "fillable_export_request_template"
  - "setup_task_export_zip"
  - "export_execution_result"
  - "export_diagnostics"
  - "export_audit_summary"
  - "fsm_import_preflight"
  - "fsm_parent_anchor_validation"
  - "fsm_candidate_profile_type_section_zip"
  - "fsm_candidate_preparation_result"
  - "fsm_import_execution_result"
  - "read_only_verification_result"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
  - "shared.setup-export.task-level-export"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
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
  - "exports"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-types-and-content-section-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-types-and-content-section-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-types-and-content-section-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_export"
    default_location: "project/{project_id}/exports/hcm-tool/profile-types-and-content-section-configuration/"
    versioning_policy: "append-only"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "HRT_MANAGE_CONTENT_SUBSCRIBERS"
  - "HRT_MANAGE_PROFILE_TYPES"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "For an explicit current-state verification request, performs only GET calls against allowlisted HCM REST resources and writes no Fusion configuration."
  - "After explicit approval, invokes shared.setup-export.task-level-export to create, poll, and download one or more current-instance FSM setup-task CSV exports."
  - "Writes the unchanged exported ZIP, or the process log on failure, under project/{project_id}/exports/hcm-tool/profile-types-and-content-section-configuration/."
  - "After Core Data Loader's authoritative approval gate, may submit one validated, immutable HRT_MANAGE_PROFILE_TYPES FSM ZIP through the authorized task-level adapter and poll its ProcessId."
  - "For an approved local preparation request, writes one new review-only HRT_MANAGE_PROFILE_TYPES candidate ZIP from complete GET metadata and a validated native source archive; it never overwrites an existing file or changes Fusion."
required_privileges:
  - "For read-only verification, Use REST Service - Talent Profile Types Read Only and the GET privileges required for the referenced profile-section, subscriber, content-type, or content-item LOV resources."
  - "Export Import Functional Setups User (ORA_ASM_FUNCTIONAL_SETUPS_USER_ABSTRACT) and the task-specific privileges required to export the selected setup task."
  - "For import, the target-environment Functional Setups import role and task-specific privileges required by HRT_MANAGE_PROFILE_TYPES."
  - "Write access to the selected local project workspace."
---

# Profile Types and Content Section Configuration Skill

## Purpose

Prepare a business-first, review-only proposal for enabling profile capability,
verify whether a requested content section and related setup already exist by
using GET-only Fusion REST reads, prepare a review-only FSM candidate ZIP from
complete runtime template metadata, or export the current task-owned setup data
from an authorized Fusion instance as an unchanged FSM CSV ZIP. For
configuration planning, start
from the workforce or process outcome, who is affected, when it takes effect,
and explicit constraints. Resolve setup terminology only after the business
proposal has been reviewed. This skill covers configuration of the seeded
profile types visible in Profiles V2, Person content-section creation from
predefined templates, non-Person content sections sourced from corresponding
Person sections, content-section properties, and content subscribers. It does not
create custom parent profile types because Profiles V2 doesn't display them.
The global subscriber catalog is configured through the
`Content Subscribers` task; subscriber-specific section-property assignments
are configured through the `Profile Types` task. It does not load individual workers' profile data or
configure content-section access, which is separately owned outside this
catalog node.

## When to Use

Use this skill when someone asks, in business language, to enable, structure, or
govern profile information for a workforce population or process. Examples
include making qualifications visible to a workforce, enabling a profile section
for a job family, defining the content subscribers used by a profile process, or
checking the exact current section, properties, catalog, subscriber, and model
parent configuration. It also applies when capturing the current Profile Types
or Content Subscribers configuration from a Fusion instance for review, backup,
comparison, or migration preparation.

Do not use it for loading existing worker profile history, qualifications, or
other profile instances; route that work to the authorized data-loading workflow.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `HCM Tool` (`CUSTOM_HCM_TOOL`)
- Functional area / Setup Object: `Profile Types and Content Section Configuration` (`CUSTOM_PROFILE_TYPES_AND_CONTENT_SECTION`)

## Setup Tasks

1. [Content Subscribers](content-subscribers.md) (`HRT_MANAGE_CONTENT_SUBSCRIBERS`)
2. [Profile Types](profile-types.md) (`HRT_MANAGE_PROFILE_TYPES`)

## Inputs

- Business outcome.
- Workforce, organization, population, or business-process context.
- Effective date.
- Explicit constraints and exceptions.
- Optional project context, approved decisions, and existing evidence.
- Optional expert input: complete JSON, workbook, CSV, Markdown, text, or
  another already-supported technical source. Preserve it unchanged and use it
  only after the business-intent capture.

## Guidance and Fillable Templates

For a request for guidance, a questionnaire, or a fillable template, use the
local no-Fusion template-only workflow and select one of its two modes. Both
accept incomplete requirements, make no
authenticated call, perform no implementation validation, and never authorize
or submit a live export.

- Configuration intake:
  `scripts/generate_blank_template.py --mode configuration --output <path>`
- Instance export request:
  `scripts/generate_blank_template.py --mode export --output <path>`

Omitting `--mode` preserves the existing configuration-intake behavior. Give
the generated file to the user to fill out, then treat the completed file as
untrusted request input. Never ask the user to enter a password, OAuth token,
client secret, token-cache content, or customer configuration rows in either
template.

Treat a populated workbook or template as later expert input. Populate it only
after the user supplies requirements; run technical validation, duplicate
checks, environment preflight, and any implementation workflow only as separate
later stages.

## Read-Only Current-State Verification

Select this route when the user asks which sections are configured for a seeded
profile type, or whether a desired content section or its related setup exists
in a Fusion instance. This is distinct from configuration
proposal, export, and import. Read
[Read-Only REST Verification](references/read-only-rest-verification.md) before
making any request in this route.

The route has a hard HTTP-method allowlist: every Fusion business-resource call
must be `GET`. Reject `POST`, `PUT`, `PATCH`, `DELETE`, request bodies, and action
endpoints before authentication or network execution. Do not create, update,
delete, export, import, submit, or synchronize anything, and do not switch to
browser automation or another write-capable route when a read is unavailable.
Use `core.fusion-api.rest-api-client` with explicit `--method GET` and only the
stable logical paths listed in the reference. Never hardcode the browser HAR's
host, cookies, authorization data, or opaque `/rest/rv:<value>/...` route.

This is the standalone `ptcs.read-only-verification` diagnostic workflow, not
the `HRT_MANAGE_PROFILE_TYPES` configuration/import Task Hook graph. Run
`scripts/verify_content_section.py --input-stdin --dry-run` first with the
exact verification request described in the reference. Require `status=planned`
before running the same input without `--dry-run`. The helper performs input,
environment-alias, cached-authentication, runtime-capability, pagination, and
comparison checks and returns a terminal sanitized report. It delegates all
HTTP transport to the shared core client with explicit `--method GET`.
The public `profileTypeSectionsLOV` finder `findByProfileTypeId` is its primary
existence/approval read; richer property/subscriber reads remain runtime-gated.

Do not enter `PTCS.DISCOVERY`, invoke Core Data Loader, or override registry
readiness for this diagnostic operation. The configuration/import graph remains
independently fail-closed; a diagnostic plan/report neither satisfies its
validation rules nor supplies its execution approval. This is an explicitly
selected workflow, never an automatic fallback after a failed import check.
Unsupported comparison inputs must stop before authentication; do not replace
the helper with hand-written REST or browser calls.

Require one exact seeded profile type ID/key pair. For a section inventory, use
`operation=list_profile_content_sections` with just the environment and profile
identity (for Job, `profile_type_id=2`, `profile_type_key=JOB`). Do not ask for a
section name/context first. The helper lists all sections visible to the
authenticated user after complete pagination, returning business names/contexts
and documented approval/default flags; null flags mean unknown, not false.
This is `section_inventory_only`, not a complete editable configuration snapshot:
properties, active state and assignments remain outside this read's coverage.
Do not substitute an empty template or a document filled with unretrieved values
for a requested current-state snapshot. Explain any missing coverage and route
an explicitly requested populated export through Instance Data Export below.

For `operation=verify_profile_content_section`, prefer exact
`SectionContext`; when it is unavailable, require exact `SectionName` plus
`ContentTypeId`. Follow every collection page through `hasMore=false` before
classifying the section as `exists`, `not_found`, `ambiguous`, or `blocked`.
When it exists, compare only the requested template and the section flags
exposed by the public LOV. Properties, subscriber assignments, model parents,
and the owning profile-type row require a supported metadata provider and are
blocked before authentication; do not infer them from browser or HAR traffic.

Return `read_only=true`, `methods_used=["GET"]`, `writes_performed=false`, the
section existence state, pagination completeness, per-component comparison
results, differences, unverifiable items, and one safe next action. Effective
date is not exposed by the observed setup reads and must be reported as
unverifiable. Persist only a sanitized validation result when project
continuity requires it; never persist raw responses, secrets, session material,
opaque route values, or customer-sensitive rows. End the route after the
verification report. A later configuration, export, or import request is a new
routed operation with separate prerequisites and approvals.

## Instance Data Export

Select this route when the requested operation is to export current setup data
from a Fusion instance. This is separate from configuration proposal and create
work: it doesn't require the unresolved Profile Types write-provider contract,
and it must not enter the create/import workflow. Delegate the live operation to
`shared.setup-export.task-level-export`; do not implement OAuth, REST process
creation, polling, download, or retry mechanics in this pillar skill.

### Export Scope

| Requested scope | Task name | Task code | Result |
|---|---|---|---|
| Profile types, content sections, section properties, task-owned subscriber assignments, and translations | Profile Types | `HRT_MANAGE_PROFILE_TYPES` | One unchanged FSM CSV export ZIP |
| Global content-subscriber catalog | Content Subscribers | `HRT_MANAGE_CONTENT_SUBSCRIBERS` | One unchanged FSM CSV export ZIP |
| Both scopes | Both tasks above | Both task codes above | Two independently traceable ZIPs; never merge or repackage them |

Default an unqualified profile/content-section export request to `Profile Types`.
Select `Content Subscribers` only when the user explicitly requests the global
subscriber catalog. The Profile Types export can contain subscriber-specific
section-property rows, but that does not replace the separate global Content
Subscribers task export. Do not claim that the ZIP contains Oracle-seeded rows:
FSM excludes seeded data from CSV export/import, so report only the exportable
task data actually returned by the source instance.

### Export Request Guidelines

Use the fillable export-request template when the source environment, scope, or
output preferences aren't already clear. Help the user complete it in business
language using these rules:

1. **Purpose:** record why the export is needed: review, backup, comparison, or
   migration preparation. The purpose doesn't grant permission for an import.
2. **Source:** enter only the configured FDOS environment name or alias. Never
   place credentials, tokens, cookies, or client secrets in the template.
3. **Scope:** choose exactly one of `Profile Types`, `Content Subscribers`, or
   `Both`. Choose `Profile Types` for profile types, content sections, section
   properties, translations, and task-owned subscriber assignments. Choose
   `Content Subscribers` only for the global subscriber catalog.
4. **Coverage:** choose `Full task` unless a smaller business scope is required.
   For `Filtered`, describe the intended seeded profile type or subset in
   business terms; do not invent technical export criteria. The skill validates
   whether the instance exposes a safe FSM criterion before execution.
5. **Artifact:** retain the default unchanged ZIP and project export location.
   Requesting a file listing or SHA-256 is safe; extraction is optional and must
   remain under the selected project workspace. Never request silent overwrite.
6. **Timing:** use the standard bounded wait and polling defaults unless the
   environment requires a documented alternative. A timeout is not permission
   to submit another export.
7. **Approval:** leave the approval field as `Pending`. A completed template is
   not approval. After validating it, present the exact environment, task,
   scope, criteria, and output path, then request approval immediately before
   the live export call.

If required information is missing, ask only for the missing business-facing
value. Do not require the user to know a task code, REST resource, business-
object code, attribute set, or OAuth detail; resolve those through the declared
workflow.

### Export Preflight and Execution

Read `references/local-export-gate.md`. All new exports from this skill must
pass `scripts/export_profile_setup.py` plan and explicit approval validation.
It delegates once to the unchanged shared task-level orchestration script.
Direct invocation of another creation entry point is not this skill's route.

These approval rules belong to this Profile Types skill; do not modify shared
or core services to enforce them. Before delegating an export, record genuine
user approval bound to the exact environment/base URL, task, template-only or
current-data mode, filters, and destination. A preparation request or import
approval never supplies export approval. Use only the shared service's supported
arguments; do not pass a custom `--export-authorization` option.

Do not retry export creation automatically or replay it after a polling error.
If a shared entry point can replay a create POST during authentication recovery,
do not use that path for this skill unless its supported options prevent replay.
Report the workflow gap to the shared owner rather than editing shared code or
bypassing the declared route. Once a ProcessId is returned, resume only that
process through the declared polling operation.

1. Resolve `project_id`, the authenticated source environment identity, and the
   exact requested scope. An export is a source-instance operation; do not ask
   for or infer a target environment or quarterly release.
2. Resolve the task only from this skill's task metadata and have
   `shared.setup-export.task-level-export` confirm the live task identity and
   `CSVExportImportSupportedFlag=Y`. Stop on ambiguity, unsupported status, or
   missing export privilege.
3. Treat a request for current data as data-export mode. Never substitute a
   CSV template/spec export, which contains structure rather than current setup
   values.
4. A request limited to one seeded Profiles V2 type is a filtered-export
   request, not permission to export the full task. Pass
   `SetupTaskCSVExportCriteria` only when the live task/provider metadata
   confirms the exact business-object code, attribute set, attribute name, and
   attribute value. Never translate the seeded ID/key mapping into
   `ProfileTypeCode` or `ProfileUsageCode`. If a safe criterion cannot be
   confirmed, stop and offer an explicitly approved full `Profile Types` task
   export instead of silently broadening the scope.
5. Before the live export call, show the exact source environment, operation,
   task name/code, full-versus-filtered scope, criteria when present, and output
   directory. Obtain explicit approval immediately before invoking the shared
   exporter. Approval for configuration, import, a prior export, or a different
   environment doesn't authorize this call.
6. Invoke the local export guard, which delegates to `shared.setup-export.task-level-export` with the selected task code,
   `HCM Tool`, `Profile Types and Content Section Configuration`, `project_id`,
   the authenticated token cache, bounded wait/poll options, and only the
   approved criteria. Let it create the export, poll by `ProcessId`, and retrieve
   `FileContent` on success or `ProcessLog` on failure.
7. Preserve each returned ZIP unchanged. Validate its ZIP signature and
   integrity, record SHA-256 and a file-name listing without extracting customer
   data into the reusable skill tree, and register it as a configuration export
   under the declared project path.
8. Return the source environment, task name/code, export scope, `ProcessId`,
   terminal status, ZIP or log path, SHA-256 when successful, whether
   `FileContent` or `ProcessLog` was retrieved, elapsed wait, and a safe next
   action. Redact tokens, secrets, base64 content, and sensitive row values.

On cached-token 401/403, allow the shared authentication workflow to refresh
once. Retry only bounded read-only polling for a known process. On timeout,
preserve the `ProcessId` and last status and wait for user direction before
polling again. Never automatically submit a second export after an ambiguous
response, timeout, failed process, or transport error.

Oracle references:

- [Export Setup Data for a Task](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/Task_CSV_Export.html)
- [Setup Task CSV Exports REST Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-exports.html)
- [Export and Import CSV File Packages](https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/export-and-import-csv-file-packages.html)
- [Additional Access Required for Exporting and Importing Setup Data](https://docs.oracle.com/en/cloud/saas/applications-common/26c/oafsm/additional-access-required-for-exporting-and-importing-setup.html)
- [Profile Type Sections List of Values](https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-list-values-profile-type-sections-list-values.html)

## Outputs

- Short business proposal: what will be enabled, for whom or which process,
  effective date, resolved associations/defaults, material assumptions, and
  exclusions.
- Assumption ledger with provenance and review status.
- Technically normalized configuration, technical validation result, and
  per-candidate exact duplicate decision after proposal review.
- For a current-state check: GET-only method ledger, exact section existence
  state, pagination status, requested component comparisons, differences, and
  unverifiable items, with `writes_performed=false`.
- For an approved instance export: unchanged task ZIP artifact(s), integrity
  metadata, execution result, diagnostics, and audit summary.
- For REST-metadata package preparation: one new review-only candidate ZIP,
  exact template and parent identities, normalized property/subscriber counts,
  validation checks, and SHA-256. Raw REST responses and credentials are not
  included.
- For a template request: a blank configuration-intake or instance-export
  request template, with no Fusion call or execution approval implied.
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files only after business intent has been
captured and resolved. Track token usage for any generated project artifact or
skill-run record using the manifest policy.

## Business-First Interaction Contract

Do not ask a normal user to choose a skill, setup task, consumer, object,
component, loader, REST resource, or technical field. Capture the four business
inputs above, then prepare a review-only proposal when one safe proposal is
possible. Ask exactly one concise business-language question only when competing
answers materially change behavior, scope, timing, reuse-versus-new, or a
downstream impact.

Treat a complete technical file as a backward-compatible expert route, not as a
different safety model. Technical schemas, FSM/import contracts, metadata checks,
exact-match rules, immutable preview, execution approval, readback, no-update/
delete limits, and downstream ownership boundaries remain post-proposal gates.

Read [Business Intent Contract](references/business-intent-contract.md) before
resolving business intent, defaults, comparable configurations, or proposal
review.

## Scope Boundary

Use this skill to prepare a configuration proposal for one Profiles V2
UI-visible seeded profile type: `1 PERSON`, `2 JOB`, `3 POSITION`,
`4 ORGANIZATION`, `5 TEMPLATE`, `10 REQUISITION`, `11 PREREQUISITE`, or
`12 GUIDE`. Create Person sections from predefined templates; configure every
supported non-Person section from its corresponding active Person section and
apply only its Profile Types-owned properties. Treat this list as the UI visibility
allowlist, not proof that every type supports every create, update, or import
operation. Do not create a custom parent profile type; before immutable preview
or execution, require the confirmed provider or FSM contract to authorize the
requested operation for the selected seeded type.
Every content section for a supported seeded profile type other than `PERSON`
must be based on exactly one corresponding active Person content section. The
same Person section may be used once in each supported non-Person profile type,
but it must not produce two sections in the same target profile type. For one
new section whose required Person parent already exists, the REST-metadata
candidate builder enforces the relationship and target-level uniqueness before
writing. Multi-section parent-before-target construction for a missing Person
prerequisite remains owned by the separately confirmed FSM processing contract.
The single request can include section name, description, active/default/order
choices, approvals, summary/detail/hidden attribute display, DFF-context
references, evaluator settings, talent-rating settings, delivered subscriber
assignments, subscriber attributes, automatic person-profile settings, and
conditional job-to-position synchronization settings.

For person profile types, the request may also configure Profile Talent Ratings:
delivered rating presentation/subscription and up to five new custom ratings
when an existing rating model and required access are supplied. For model types,
enforce category association: Job-to-Job, Position-to-Position, and
Organization-to-Organization only. Treat Prerequisite support as provider-
validated before proposal normalization because the confirmed task surface does
not document a creation contract for it.

Keep the seeded type identity separate from CSV fields. In particular,
`HRT_PROFILE_TYPES_B.ProfileTypeCode` is the profile-type business key and
`ProfileUsageCode` is a usage classification; neither field is the seeded
Profiles V2 ID-to-key mapping. When both a seeded ID and key are supplied, they
must be an exact pair from
[Oracle Profile Configuration Scope](references/oracle-profile-configuration-scope.md).

For the owning `HRT_PROFILE_TYPES_B` row, set `ProfileUsageCode=P` for Person
and `ProfileUsageCode=M` for Model profiles. After validating the supported
profile type ID/code pair, derive this classification when metadata omits it
or leaves it blank; do not leave it blank in a generated package. Reject a
conflicting supplied `ProfileUsageCode` or `UsageCode` instead of silently
overwriting it. This user-confirmed rule supplies only the usage code, not
dates, ModuleId, approval flags, or other missing values. It does not prove
that the owning row is otherwise safe to import or authorize another import.

For all Model profiles (`ProfileUsageCode=M`), leave the owning
`HRT_PROFILE_TYPES_B.AutoCreateFlag` empty. Do not require Y/N or copy a Person
auto-create setting or the REST alias `AutoCreatePersonProfileFlag`. Normalize
legacy nonblank model values to empty during preparation, before preview.
Person profiles retain their source-backed Y/N requirement. This exception
does not relax other owner metadata or import-approval gates.

Populate the owning profile's name in `HRT_PROFILE_TYPES_B.Description`,
start date in `DateFrom`, and end date in `DateTo`; require all three for
package preparation. These are not the section's `Name` or item dates.
Use explicit user values or a verified, applicable owning-profile reference,
not lookup-definition dates or the current date. Render valid calendar dates
as `YYYY/MM/DD` and require start date not to exceed end date. For the reviewed
PERSON reference in this workflow, the user confirmed `Description=Person`,
`DateFrom=2000/01/01`, and `DateTo=4712/12/31`; these are not universal dates
for Model profiles or other environments. Do not leave the owning name blank
because the new section already has a name. Other owner fields and import
approval gates remain independent requirements.

Do not use this skill to silently choose a business design, update or delete
existing configuration, create individual profiles, load or migrate profile
data, configure downstream product templates, or automatically run unrelated
administrative jobs.

## Source-Grounded Execution Contract

## Fusion Environment Preflight Evidence

Use the authenticated Fusion environment context and the structured checks
declared by this skill as preflight evidence. Do not require screenshots,
browser address-bar images, copied URLs, exact confirmation replies, or user
attestations. If an applicable structured environment check is unavailable,
record the preflight as blocked and identify the missing check. Retain visual
evidence only when the verification itself is inherently visual.

Resolve the environment from authenticated FDOS context. Never ask the user for
a quarterly Fusion release. Record a release only when trusted authenticated
metadata already provides it; never infer a quarterly release from
`11.13.18.05`, a hostname, documentation version, or date. Use the documented
bounded `GET /fscmRestApi/resources/11.13.18.05/setupTaskCSVImports/HRT_MANAGE_PROFILE_TYPES?onlyData=true`
capability check through the authenticated REST client.

1. Capture business intent before technical terminology: outcome, context,
   effective date, constraints, and exceptions.
2. Use only workflow-declared, source-backed, read-only discovery. Apply the
   precedence in the Business Intent Contract and log every inferred value.
   Never invent an endpoint, association, default, comparable configuration, or
   enterprise convention.
3. Present a short review-only proposal. Before an immutable execution artifact
   exists, use actions such as **Prepare configuration** and **Review
   assumptions**, never an execution action.
4. After proposal confirmation, technically normalize the request and run all
   existing technical completeness, metadata, dependency, and exact-match
   checks. Similarity is not an exact duplicate.
5. For every non-Person target, resolve the corresponding active Person content
   section before property customization. If it is absent, disclose the missing
   prerequisite and request explicit approval to add the Person section to the
   implementation scope. This is scope approval, not Core Data Loader execution
   approval. After approval, hand the normalized parent-and-target intent to the
   FSM processing layer; do not construct or import the Person section in this
   pillar skill. On workflow re-entry, a recorded matching scope approval takes
   the approved-missing branch into FSM handoff instead of asking again.
6. Perform the exact duplicate check for every candidate content section only
   after technical normalization. The duplicate gate clears only when every
   candidate returns zero exact matches. If any one section is an exact
   duplicate, disclose every duplicate found and stop the entire ZIP: do not
   import the remaining new sections, and do not offer approval to update,
   merge, overwrite, resubmit, or add child rows. Continue only with a newly
   prepared ZIP that excludes all duplicates and completes a fresh validation,
   SHA-256, preview, and approval cycle. Multiple exact rows for one candidate
   are ambiguous and also block the entire ZIP.
7. The authorized executor owns immutable preview and execution approval.
   Proposal confirmation is not live-execution approval. Persist only through a
   confirmed HCM Tool operation, then read back the saved values and compare
   them to the approved immutable preview. Do not substitute REST, HDL, browser automation, or a migration route.
8. Stop and retain a sanitized traceability record on ambiguous material intent,
   unresolved evidence, missing provider registration, failed create, partial
   persistence, or unverifiable readback.

## Configuration Workflow

1. **Business intent**
2. **Read-only context and comparable discovery**
3. **Assumption-led proposal**
4. **Genuine business clarification, if required**
5. **Technical normalization**
6. **Technical validation and Person-parent resolution**
7. **Whole-ZIP exact duplicate decision**
8. **Immutable preview and approval**
9. **Execution and read-back** through the authorized executor only

## REST-Metadata Candidate ZIP Preparation

Select this local assisted route after proposal review when the user asks for a
new Profile Types CSV ZIP and complete GET metadata can identify the template,
properties, current target sections, Person parent when applicable, and
requested subscribers. Read
[REST Metadata to FSM Candidate ZIP](references/rest-metadata-fsm-package-preparation.md)
before preparing the artifact.

Resolve the native package source before any live export. First inspect the
selected project's Profile Types export folder for an existing FSM
template/spec ZIP. Reuse it without another Fusion call only when ZIP integrity
passes, its single `ASM_SETUP_CSV_METADATA.xml` marker identifies
`HRT_MANAGE_PROFILE_TYPES`, all required CSV members are present, and every CSV
is header-only; record its SHA-256. If no valid archive exists, present the exact
source environment, Profile Types task, template-only operation, and output
directory, obtain explicit approval, and invoke
`shared.setup-export.task-level-export` with `--template-only`. Never substitute
a current-data export for this empty native source or submit another template
export merely because a reusable valid archive already exists.

Classify `prepare/create a ZIP` as local package preparation, not permission
to export current data or submit an import. A separately approved empty-template
download records approval within this skill's project workflow and uses `--template-only`;
existing template reuse requires no export. The owning Profile Type row must
have source-backed metadata for the native columns, including usage, dates,
ModuleId, and approval flags. Do not treat missing REST fields as safe blanks,
or use lookup-definition dates/ModuleId as profile values. Person section
parent fields remain empty; the owning PERSON profile row is not a parent
section. Structural ZIP validation is not proof of safe import semantics.

### Owner-Metadata Export Fallback

Use this route only after the declared exact owning-profile GET has failed or
does not expose a required owner field. It is an explicit alternative, never an
automatic retry or a replacement for the empty template/spec source.

1. Confirm whether `HRT_MANAGE_PROFILE_TYPES` supports a safe exact filter for
   the requested seeded profile type. If no exact filter is confirmed, disclose
   that a full-task export is broader and stop unless the user explicitly
   approves that broader current-data export.
2. Immediately before creating the export, present the exact source environment,
   task/code, selected profile type or full-task scope, immutable output path,
   and that the archive will be evidence only. Obtain separate explicit export
   approval; preparation or import approval never supplies it.
3. Preserve the returned current-data export byte-for-byte. Never use it as the
   empty template/spec source, add a content section to it, overwrite it,
   repackage it, or import it.
4. Run `scripts/extract_owner_profile_reference.py` first with `--dry-run`,
   then write its new JSON reference only after `status=planned`. It extracts
   exactly one owning `HRT_PROFILE_TYPES_B` row for the requested seeded profile
   type, checks the native marker, integrity, required owner fields, and source
   archive SHA-256, and injects only the verified seeded profile ID into the
   derived reference.
5. Give that JSON to the candidate builder as `--profile-types-response`, while
   continuing to give the builder the distinct validated header-only native
   template/spec ZIP as `--source-template-zip`. Any missing, duplicate, or
   conflicting owner value blocks preparation.

Keep existing Jira/task mappings and Jira approval workflow intact. Neither
preparation nor an export approval satisfies Core Data Loader's authoritative
immutable-artifact import gate. Do not submit a candidate whose profile
metadata is incomplete, even if an earlier structural check passed.

Use the stable logical resources through `core.fusion-api.rest-api-client` and
keep raw responses in a safe temporary location. Never execute or retain a
browser-captured `/rest/rv:<opaque-value>/...` URL, authorization header, or
cookie. Require full pagination and one exact template match. The template LOV
returns the template `SectionId`; use that identifier for the runtime-confirmed
template-properties child GET.

For Person output, retain only properties whose `SourceProfileTypeCode` is `P`
or `B`. For every non-Person target, resolve properties from two distinct,
fully paginated child responses after resolving the exact active Person parent:
take only `B` rows with null `SourceCode` from the selected Person section, take
only `M` rows from the template section under profile type `5`, and merge those
rows without changing their stable property identity or presentation metadata.
Never source `B` rows for a model section from the template response. Require
exactly one corresponding active Person section, and reject preparation when
that Person section is already represented in the same target profile type.
The same Person section remains independently eligible for another target type
such as Position after it is used by Job.

Run the deterministic builder in dry-run mode first:

```text
python3 scripts/build_fsm_profile_type_section_zip.py \
  --request <request.json> \
  --templates-response <complete-findTemplateSections.json> \
  --properties-response <complete-template-properties.json> \
  --target-sections-response <complete-target-sections.json> \
  --source-template-zip <native-HRT_MANAGE_PROFILE_TYPES.zip> \
  --output <new-candidate.zip> \
  --dry-run
```

Add `--person-sections-response` for a non-Person target and
`--person-properties-response` for that selected Person section's complete
`B`/null-`SourceCode` property response. Add
`--subscriber-response` when subscriber assignments are requested. Require
`status=planned`, then rerun without `--dry-run` to write one new candidate.
The builder never calls Fusion, overwrites a file, invents `AttributeLabelKey`,
accepts a source CSV data row, or substitutes REST metadata for the native FSM
headers and metadata marker. It preserves every native template member, adding
approved rows only to the applicable task CSVs.

After construction, run subscriber-closure validation when subscribers are
present and parent-anchor validation for every non-Person section. Treat the
candidate as review-only. Package preparation does not satisfy the later Task
Hook, immutable-preview, execution-approval, import, or readback gates.

## FSM Import Route

For a new Person section, first read
[Person Submission Readiness](references/person-submission-readiness.md).
It distinguishes the existing native FSM transport from the still-required
Person package semantics, activation timing, subscriber/access prerequisites,
immutable preview, and readback evidence. GET success alone clears none of
those submission gates.

Use the native FSM CSV ZIP shape exemplified by a validated Profile Types export:
exactly one `ASM_SETUP_CSV_METADATA.xml` marker whose setup object is
`HRT_MANAGE_PROFILE_TYPES`, accompanied by the task-owned parent, section,
property, qualifier, subscriber-property, and translation CSV members that are
actually needed by the approved scope. A supplied example establishes archive
shape only; its rows, codes, descriptions, translations, and section inventory
are never business defaults. Preserve the exact validated ZIP bytes and its
SHA-256 through review and execution.

For a new Person section, preserve the package's business-key relationships:
leave section and child surrogate IDs empty, leave the section `ContentTypeId`
empty rather than writing the literal `#null`, and require every property and
translation row's prefixed parent keys to match the generated section exactly.
Treat a literal-null or mismatched parent relationship as a blocker before
preview.

Use `references/fsm-profile-types-package.md` as the package-template contract.
Do not create a synthetic blank ZIP or copy example data into a new request;
obtain or build the native task archive through the confirmed FSM contract.

Before any immutable preview or import handoff, validate subscriber dependency
closure with `scripts/validate_fsm_subscriber_closure.py`. For each explicitly
supplied subscriber, pass its exact resolved `ProfileTypeCode`, `ContextName`,
`SectionContext`, and predefined `SourceCode` using `--expected-subscriber`.
The validator requires exactly one matching row in
`ORA_HRT_PROFILE_TYPE_CONTENT_SOURCE.csv`; subscriber-property rows configure
that assignment but never create it. Every subscriber-property row must resolve
to that relationship, and every subscriber-property translation must resolve to
one base subscriber-property row. A relationship without subscriber-property
rows is valid only when no subscriber attribute selections were supplied. Stop
before preview when the closure is missing or ambiguous; do not synthesize the
relationship, infer a subscriber, or treat header-only files as configuration.

```text
python3 scripts/validate_fsm_subscriber_closure.py <candidate-zip> \
  --expected-subscriber \
  <PROFILE_TYPE_CODE>,<CONTEXT_NAME>,<SECTION_CONTEXT>,<SOURCE_CODE>
```

Before an immutable preview, semantically validate every section for a seeded
profile type other than `PERSON` using either the archive-derived source row
or the independent REST-derived Person selection and content-type mapping.
Both paths require the documented complete Person-section lookup. This rule is not
limited to `JOB`; it also applies to supported Position, Organization,
Template, Requisition, Prerequisite, and Guide section operations. A generated
section must retain the resolved parent business key and template flag. For a
competency section derived from
`JOB_COMPETENCY`, the normalized relationship is
`ParentSectionProfileTypeCode=PERSON`,
`ParentSectionContextName=COMPETENCY`,
`ParentSectionSectionContext=PERSON_COMPETENCY`, and
`TemplateBasedSectionFlag=Y`; leave `ParentSectionId` and
`ParentSectionContentTypeId` empty. Never blank a source template's parent
anchor and never infer one from the new section name. Require exactly one
eligible parent result; zero, multiple, incomplete pagination, or mismatched
business keys block before preview. A zero match is also a missing business
prerequisite: the skill must disclose it and request explicit scope approval to
include the corresponding Person section. The FSM processing layer owns the
missing-parent package construction and parent-before-target ordering. If that
contract is not confirmed, stop rather than constructing the missing parent in
this pillar skill. When the parent already exists, use the REST-metadata
candidate builder and retain its uniqueness evidence.

Use the local fail-closed validator for this gate:

For a REST-derived Model section built from a native empty template, use the
alternative `--rest-parent-evidence` mode documented in
`references/fsm-profile-types-package.md`. It validates the independent Person
selection and complete REST collections without requiring a populated Job/model
source row. Do not export data, synthesize a source ZIP, or use the candidate as
its own relationship evidence. Existing archive-derived validation remains
available for packages based on a populated source. Both paths retain the
unchanged native metadata marker and independent import approval gates.

```text
python3 scripts/validate_fsm_parent_anchors.py <candidate-zip> \
  --source-template-archive <current-source-profile-types-zip> \
  --source-section-context <exact-active-source-section-context> \
  --parent-lookup-json <complete-findByProfileTypeId-person-response.json>
```

When constructing a candidate before preview, `--output <new-zip>` may create a
new normalized archive. It never overwrites either input, preserves the
source-template `ASM_SETUP_CSV_METADATA.xml` content byte-for-byte and preserves
all unrelated candidate member content, then validates the output. Validation
also rejects a candidate whose metadata marker differs from the source template.
Any normalization produces a new archive and SHA-256 that must start a fresh
validation and approval cycle. Do not normalize or repair an archive after
immutable preview.

Core Data Loader owns source inspection, immutable archive review, Task Hook
validation, final approval, submission, polling, and ProcessLog retrieval.
Before handoff, compare every parent and child row to the approved business
scope. A structurally valid ZIP is insufficient: block unrelated sections,
unexpected translations or child records, a custom parent profile type that
Profiles V2 won't display, a seeded target that cannot be resolved exactly, or
a non-Person section whose Person parent-anchor validation did not pass.
Do not require a surrogate `ProfileTypeId` merely because the CSV column exists;
use the confirmed FSM key-resolution contract.

For every candidate section whose technical normalization produces an exact
seeded `ProfileTypeId` and exact `SectionContext`, run the declared read-only
duplicate GET through `core.fusion-api.rest-api-client`. Do not use the section
lookup to infer whether a custom parent `ProfileTypeCode` exists. Only zero
exact rows for every candidate clear the duplicate gate. A same-prompt
instruction such as "if no records, submit" may satisfy Core Data Loader's
final approval gate for that exact immutable archive, but only after
environment, identity, privilege, Task Hook, archive-scope, and provider checks
all pass. If any candidate has one exact row, disclose all duplicates and stop
the entire ZIP; do not import its remaining new sections and do not accept
approval to update, merge, overwrite, resubmit, or add child rows. Require a
new ZIP that excludes every duplicate and repeat all validation and approval
gates. Multiple exact rows for any candidate are ambiguous and also block the
entire ZIP. If any exact identifier or supported GET is unavailable, do not
call a guessed endpoint and do not submit.

After all gates pass, route the approved package through `core.data-loader`'s
authoritative FSM workflow. Let Data Loader select and execute its adapter;
do not independently call UCM, initiateDataLoad, or a task import endpoint.
Return its accepted initiation report immediately. Poll and retrieve ProcessLog
only when the user requests status, using Data Loader's monitoring workflow.

## XLSX Source Selection

Before generating an XLSX workbook, detect whether worksheet names would
collide after the required business-object prefix shortening. If a collision is
found, prefer this task's valid FSM CSV export/import route. When no valid FSM
route applies, stop and require the user to explicitly request DAT preparation;
do not generate an ambiguous XLSX workbook.

## Dependencies and Known Gaps

- Create content sections and their documented properties within the selected
  profile type. Treat delivered templates as the basis for Person sections and
  corresponding Person sections as the basis for non-Person sections; do not
  invent a template or alter an existing leading attribute.
- Treat the active Person content section as mandatory related setup for every
  supported non-Person content section. When it is missing, ask for explicit
  scope approval and pass the approved parent-and-target intent to the FSM
  processing layer. Do not build the missing Person section here, and do not
  treat scope approval as the loader's final execution approval.
- Treat rating models, content-library definitions, profile options, item
  catalogs, value sets, flexfields, approvals, security, lookups, and background
  processes as separately owned dependencies. Validate their references only;
  do not create or change them here.
- A subscriber attribute can be configured only when its content-section
  property display is Summary or Detail; Hide excludes it. A leading attribute
  is immutable after section creation.
- Manager access to Skills and Qualifications or Talent Ratings requires
  read-only verification that `ORA_HCM_VBCS_PWA_ENABLED=Y` and
  `HRC_ELASTIC_SEARCH_ENABLED=Y`; do not set either profile option here.
- Do not propose job-to-position synchronization by default. When explicitly
  requested, disclose that it can add, update, or delete synced position items,
  verify its current state read-only, and never enable or run it automatically.
- Use only predefined Oracle subscriber codes. `Content Subscribers` is the
  catalog-defined task for the global subscriber catalog. The Profile Types
  task owns the section assignment in `ORA_HRT_PROFILE_TYPE_CONTENT_SOURCE`
  and any subscriber-specific section-property rows in
  `ORA_HRT_PROFILE_TYPE_SUBSCRIBER_PROFILE_TYPE_SECTION_PROP` and its
  translation table. Property rows alone are not a subscriber assignment; do
  not substitute them for the content-source relationship or a standalone
  Content Subscribers table.
- `GET /talentProfileSyncLogs` is confirmed only as a read-only reconciliation
  resource. The exact ESS job definition, application, product, parameters, and
  privilege contract for job-to-position synchronization remain unresolved.
- The create-only Person content-section transport is the native
  `HRT_MANAGE_PROFILE_TYPES` FSM CSV contract: require a validated native
  metadata marker with a registered migration service, a successful bounded
  task-import capability GET, deterministic package validation, and exact
  post-import section readback. This confirmation does not authorize direct
  REST writes, updates, deletes, or an unsupported reference type; those paths
  must remain fail-closed.

## Read Order

1. `references/business-intent-contract.md`
2. `references/oracle-profile-configuration-scope.md`
3. `references/profile-configuration-rules.md`
4. `references/read-only-rest-verification.md` when current-state verification
   is requested
5. `references/rest-metadata-fsm-package-preparation.md` when a REST-grounded
   candidate ZIP is requested
6. `references/fsm-profile-types-package.md` when FSM packaging is requested
7. `ora-resource/ora_input_validation.md`
8. `ora-resource/ora_dependency_readiness.md`
9. `ora-resource/ora_reference_lookups.md`
10. `ora-resource/ora_defaulting_rules.md`
11. `ora-resource/ora_design_enforcement.md`
12. `ora-resource/ora_error_handling.md`
13. `ora-resource/ora_rule_registry.json`

## Required Handoff Record

For each run, persist the business outcome, scope, effective date, constraints,
exceptions, requested task code and name when resolved, source identifiers,
sanitized input mapping, the assumption ledger, proposal review status,
technical-validation result, duplicate-check outcome, immutable preview
revision, execution approval, provider-operation status, readback comparison,
discrepancies, read-only verification status and method ledger when applicable,
and one safe next action. Do not persist credentials, raw REST responses,
payloads, opaque IDs, or customer-sensitive source content.
