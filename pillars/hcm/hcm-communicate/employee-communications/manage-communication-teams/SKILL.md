---
skill_id: "hcm.hcm-communicate.employee-communications.manage-communication-teams"
name: "Manage Communication Teams Setup Task Guidance"
description: "Provides task-specific setup-data import, validation, and lifecycle guidance for Manage Communication Teams under the Employee Communications functional area."
layer: "pillar"
pillar: "HCM"
offering: "HCM Communicate"
functional_area: "Employee Communications"
functional_area_code: "ORA_IRC_EMPLOYEE_CAMPAIGNS"
task_code: "ORA_IRC_EMP_CAMP_COMM_TEAMS"
task_name: "Manage Communication Teams"
parent_skill_id: "hcm.hcm-communicate.employee-communications"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObjects:
  - "communicateUICommTeams"
  - "communicateUICommTeams_updateTeamDetails"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "HCM hcm communicate pillar team"
version: "0.5.15"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "lifecycle_action"
  - "target_environment"
  - "environment_version_details"
  - "team_name"
  - "current_status_evidence"
  - "campaign_status_evidence"
  - "execution_intent"
  - "approval"
  - "requested_operation"
  - "team_type"
  - "team_creator_membership_intent"
  - "team_creator_member_evidence"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "resolved_import_route"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
  - "current_team_state"
  - "lifecycle_change_preview"
  - "execution_authorization"
  - "lifecycle_execution_result"
  - "post_action_verification"
  - "team_creator_membership_verification"
depends_on:
  - "shared.baseline-assessment.topology-manager.environment-info"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "core.fusion-api.apps-common.profile-options"
  - "hcm.hcm-communicate.employee-communications.manage-communicate-lookups"
uses_core:
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-communicate/employee-communications/manage-communication-teams/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-communicate/employee-communications/manage-communication-teams/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
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
  - "After an exact preview and fresh explicit approval, may activate one exact Draft Communication Team only through the confirmed REST Data Loader communicateUICommTeams_updateTeamDetails action."
required_privileges:
  - "Authenticated access to Manage Communication Teams and the selected task import route"
---

# Manage Communication Teams Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, validation, and lifecycle-action guidance for `Manage Communication Teams` under `Employee Communications`.

## Setup Task Skill Contract

- task_code: `ORA_IRC_EMP_CAMP_COMM_TEAMS`
- task_name: `Manage Communication Teams`
- parent_skill_id: `hcm.hcm-communicate.employee-communications`
- pillar: `HCM`
- offering: `HCM Communicate`
- functional_area: `Employee Communications`
- functional_area_code: `ORA_IRC_EMPLOYEE_CAMPAIGNS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST` for 27A and later; `FSM` for releases before 27A
- businessObjects: `communicateUICommTeams` for setup-data import; `communicateUICommTeams_updateTeamDetails` for lifecycle updates
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `communicateUICommTeams` is the exact registered Data Loader business object for setup-data import. Confirm `communicateUICommTeams_updateTeamDetails` separately for lifecycle updates.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "communicateUICommTeams" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Communication Teams` under `Employee Communications`. Before selecting a create route, retrieve `environment_version_details` through `shared.baseline-assessment.topology-manager.environment-info`. For a release before `27A`, select the FSM task-CSV route without resolving or preparing a REST setup-data archive. For `27A` and later, or when release details are unavailable, resolve the target's live Data Loader capability: use REST only when `communicateUICommTeams` is registered with usable current metadata; otherwise use the FSM task-CSV fallback. Lifecycle updates additionally require the separately registered `communicateUICommTeams_updateTeamDetails` business object with usable `POST` metadata.

Use the governed Data Loader lifecycle route below only when the user explicitly requests `Activate` or `Inactivate`. Use it only when the current registration exposes the exact `communicateUICommTeams_updateTeamDetails` action with usable `POST` metadata. Merely reading, planning, validating, exporting, importing, or authoring the skill does not authorize a Fusion change.

## Capabilities

- Create a Communication Team or Express Communication Team.
- Validate the requested team name before preparing it: require a meaningful name without extra spaces or unsupported characters, apply the environment's length limit when available, and check for an existing or confusingly similar name.
- Check whether a team with the same name already exists.
- Confirm that a newly created team appears correctly.
- For a release before `27A`, create only the top-level team through the current FSM task-CSV archive; do not prepare REST setup-data samples or child associations.
- When the REST capability is unavailable, create only the top-level team through the current FSM task-CSV archive. Child associations are out of scope for that route.
- When the REST capability is confirmed, create the parent team through a first REST Data Loader archive, obtain its generated `TeamId` and recorded creator from fresh readback, then add the recorded creator and any requested child associations through a second REST Data Loader archive. Resolve the creator to exactly one active worker and primary assignment; do not substitute the current OAuth user or a similarly named worker.
- For a child-only REST archive, use `scripts/build_child_association_archive.py` after standard Data Loader validation. It prepends the exact root `communicateUICommTeams` metadata header from the current generated workbook while retaining no parent data row. Use it only for a validated child-only archive; do not hand-edit a DAT file or add a parent update row.
- When the REST capability is confirmed, after the parent succeeds, automatically continue through read-only Team ID and creator resolution, and prepare a Team Members child row for the recorded creator in addition to requested child rows. Pause only when the exact child load is ready for its required approval. If the creator cannot be resolved exactly once, stop the child load rather than omitting or guessing the membership.
- When the REST capability is confirmed, add requested Campaign Purposes, Eligibility Profiles, HCM Lists, Microsoft Teams bots, Sender Profiles, Slack apps, Team Members, and Templates through their matching child worksheets. Add Contact Preferences only after the exact effective `ORA_IRC_COMMUNICATE_CONTACT_PREFERENCE` profile value resolves to `Y` through `profileValues`; resolve each channel through Manage Communicate Lookups from `ORA_HCO_CHANNEL_TYPE`, then resolve its channel-specific contact type through `EMAIL_TYPE` or `PHONE_TYPE` before preparing the child row. This check does not apply to lifecycle activation.
- When the REST capability is confirmed, when requested, list up to five current candidate values from the HCM List, Eligibility Profile, and Sender Profile LOVs; preserve service response order, state when fewer than five values exist, and require a fresh exact lookup before selection.
- When the REST capability is confirmed, before creating a new team, enumerate every applicable supported LOV: team type, status, campaign purposes, team members, sender profiles, eligibility profiles, HCM lists, email and SMS contact types, templates, Slack apps, and Microsoft Teams bots. Present returned values as suggestions only. When Campaign Purposes are omitted, default only to `ORA_GENERAL` and `ORA_GET_RESPONSE`; resolve both exact enabled values through Manage Communicate Lookups from Common Lookup type `ORA_IRC_EMP_CAMP_PURPOSE`. When Templates are omitted for a first REST create, default only to one exact active `Blank` template for each HTML, Advanced, and Basic editor type; resolve and prepare those child rows after the parent load. An explicit Templates list, including an explicit empty selection, replaces this default. The resulting child archive remains subject to its own exact-artifact approval before submission.
- Activate a Draft team only through the confirmed REST Data Loader `communicateUICommTeams_updateTeamDetails` lifecycle route. Use `POST`, `action=activate`, and an `attributes` JSON array containing only the exact `TeamId`. Confirm `ORA_ACTIVE` by fresh readback after one approved submission.
- Inactivate an Active team only through the REST Data Loader `communicateUICommTeams_updateTeamDetails` lifecycle route. Use `POST`, `action=inactivate`, and an `attributes` JSON array containing only the exact `TeamId`. Confirm `ORA_INACTIVE` by fresh readback after one approved submission. If Fusion returns an inactivation error, report its actual response and stop.

The FSM task-CSV route uses the current export package, including `ASM_SETUP_CSV_METADATA.xml`, and supports only the top-level fields TeamName, StatusCode, TeamId, DownloadFlag, SubscriberCode, and TypeCode. The REST service and current generated Data Loader workbook expose child sections for members, sender profiles, eligibility profiles, HCM lists, templates, contact preferences, campaign purposes, Microsoft Teams bots, and Slack apps. Use the REST workbook's exact headers and the persisted parent `TeamId`. A successful import status verifies row processing, but does not by itself provide a child-association readback.

Use the selected route's standard Data Loader workflow: for FSM, begin with the current task-export archive; for REST, generate a fresh workbook from the live registration. For every REST parent create, capture the request intent `include_persisted_creator` before preparing the parent archive. This records that the requester wants Fusion's persisted creator added as a Team Member after identity resolution; it is not approval of an unknown future child archive. Validate and submit only the exact approved immutable archive.

## Capability-Based Import Routing

1. For every create request, retrieve the exact target's `environment_version_details` through `shared.baseline-assessment.topology-manager.environment-info`. Record the returned release name/version and selected route in `setup_data_routing` and the task skill-run record.
2. When the returned release is before `27A`, select FSM setup-data import. Require the current task-export package with `ASM_SETUP_CSV_METADATA.xml`; preserve its metadata and use only `ORA_IRC_EMP_CAMP_COMM_TEAMS_DATA.csv` with the documented six top-level fields. Do not resolve REST setup-data metadata, prepare REST samples, or prepare child-association rows.
3. When the returned release is `27A` or later, use `core.data-loader` to resolve the exact target's registered `communicateUICommTeams` business object and generate or validate its current metadata workbook before source preparation. Select REST setup-data import only when one exact registration is available and usable for the requested scope; otherwise select FSM fallback and record the capability evidence and reason.
4. When the release name/version is absent or cannot be compared to `27A`, use `core.data-loader` to resolve the exact target's registered `communicateUICommTeams` capability. Select REST only when that metadata is usable; otherwise select FSM fallback and record that release details were unavailable.
5. When REST is selected, use the existing parent/child REST Data Loader flow. When FSM is selected by the release gate or capability fallback, support only top-level team creation.
6. Activation and inactivation use only the confirmed REST Data Loader `communicateUICommTeams_updateTeamDetails` route. The FSM route supports creation only and must not prepare a lifecycle archive.

## User-Facing Communication

Use business language by default. Do not expose REST field names, internal IDs, endpoints, archive hashes, workbook mechanics, or registration details unless the requester asks for technical information.

When explaining capability, say: "Capability means whether your Fusion environment is ready and allowed to complete a specific action." Use this example: "You can create a communication team. Before it can be activated, Fusion checks that the team is ready. If the check can't be completed, the team isn't changed and we explain what needs to be reviewed." If Fusion can't confirm the action, explain that the issue should be reviewed with an administrator or Oracle Support.

When a requester asks what the skill can do, use this customer-friendly summary and avoid internal implementation terms unless technical detail is requested:

- Create communication teams.
- Add people, audiences, sender profiles, templates, and contact preferences.
- Activate or deactivate a team when Fusion confirms the action is available.
- Check names, required setup, and campaign conditions.
- Stop safely and provide next steps when an action can't be confirmed.
- Explain that available options can vary by Fusion environment.

Translate internal values into these labels:

| Internal value | User-facing label |
|---|---|
| ORA_CAMP_COMM_TEAM | Communication Team |
| ORA_BU_COMM_TEAM | Express Communication Team |
| ORA_DRAFT | Draft |
| ORA_ACTIVE | Active |
| ORA_INACTIVE | Inactive |

For invalid names, explain the correction plainly: “Enter a team name,” “Remove spaces at the beginning or end,” “Remove line breaks or the `|` character,” “That team name already exists,” or “That name is longer than this environment allows.” Do not show a stack trace or metadata rule to an end user.

## Child Association Examples

Examples are parameterized and must not contain names or IDs copied from a particular environment. Resolve every selected value through a fresh documented lookup before creating an immutable load archive.

When a requester asks for available or suggested child-association values, return at most five values per supported LOV. Do not invent values or imply that returned candidates are already selected.

| Example request | Resulting behavior |
|---|---|
| “Use all available campaign purposes.” | Resolve the Campaign Purpose LOV and include every current returned value. |
| “Use `<hcm-list-name>`.” | Resolve exactly one current HCM list and populate its returned identifier and display fields. |
| “Use `<eligibility-profile-name>`.” | Resolve exactly one current eligibility profile and populate its returned identifier and display fields. |
| “Use `<sender-profile-name>`.” | Resolve exactly one current sender profile and populate its returned identifier and display fields. |
| “Add `<member-name>`, `<template-name>`, and `<messaging-application-name>`.” | Resolve each requested association independently and populate only the selected child sections. |

For a REST-capable team, record the request intent `include_persisted_creator` before preparing the parent archive; do not attempt a single Data Loader archive because child sheets require the persisted parent `TeamId`. After parent verification, automatically resolve the persisted `CreatedBy` / `CreatedByDisplayName` to one active worker and primary assignment and prepare one Team Members row for that creator. Also resolve and prepare the default `ORA_GENERAL`, `ORA_GET_RESPONSE`, and one active `Blank` template each for HTML, Advanced, and Basic when they were omitted. An explicit Templates list, including an explicit empty selection, replaces the template default but never removes the creator-membership requirement. The initial intent does not approve the final child archive: use the two-load sequence and obtain a separate immutable approval for each upload. When REST capability is unavailable, stop and explain that the FSM task-CSV route supports top-level teams only.

## Example Requests

These are workflow examples, not reusable payloads. Resolve names and IDs from fresh environment lookups before authoring a load.

- “Create a standard Communication Team named `<team-name>` and include the persisted creator as a team member.” Defaults are draft status, standard type, a parent-only first load, then a REST child load that adds the persisted creator as a team member and adds one active `Blank` template each for HTML, Advanced, and Basic when templates were not specified.
- “Create an Express Communication Team for employee events.” Use the explicitly requested Express team type; do not replace it with the standard-team default.
- “For `<team-name>`, add all available campaign purposes.” This creates a second child load containing every current Campaign Purpose LOV value.
- “For `<team-name>`, add only `<purpose-code-1>` and `<purpose-code-2>`.” An explicit purpose list overrides the `ORA_GENERAL` and `ORA_GET_RESPONSE` default.
- “Create `<team-name>`, then add `<hcm-list-name>`, `<eligibility-profile-name>`, `<sender-profile-name>`, selected templates, members, and external messaging applications.” Resolve each selection freshly, create the parent first, and use its returned `TeamId` in the child load.
- “Activate `<team-name>` after the child load succeeds.” Confirm the team is Draft, confirm the current registration exposes `communicateUICommTeams_updateTeamDetails` with `POST`, preview `action=activate` and the exact `TeamId` in `attributes`, and obtain a separate exact-artifact approval.
- “Inactivate `<team-name>`.” Confirm that the team is Active. Preview `action=inactivate` with the exact `TeamId`, then obtain separate exact-artifact approval.

## Setup Task Metadata

- Task name: `Manage Communication Teams`
- Task code: `ORA_IRC_EMP_CAMP_COMM_TEAMS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Create-route release gate: before `27A` use FSM; `27A` and later use capability-based REST with FSM fallback
- Business Objects: `communicateUICommTeams` for setup-data import; `communicateUICommTeams_updateTeamDetails` for lifecycle updates

## Supported Lifecycle Transitions

| Requested action | Required current status | Expected status after success | Supported execution route |
|---|---|---|---|
| Activate | `ORA_DRAFT` | `ORA_ACTIVE` | Confirmed REST Data Loader `communicateUICommTeams_updateTeamDetails` route only; use `POST` with `action=activate` and the exact `TeamId` in `attributes` |
| Inactivate | `ORA_ACTIVE` | `ORA_INACTIVE` | Confirmed REST Data Loader `communicateUICommTeams_updateTeamDetails` route only; use `POST` with `action=inactivate` and the exact `TeamId` in `attributes` |

Reject every other current-status/action combination. Both lifecycle actions require current generated metadata and the exact `communicateUICommTeams_updateTeamDetails` action with `POST`; do not substitute the setup-data `communicateUICommTeams` create action.

For either lifecycle action, the current registered workbook controls column order. Populate `RestAction=POST`, `action=activate` or `action=inactivate` as requested, and `attributes` as a serialized JSON array containing one object with the exact persisted `TeamId`, for example `[{"TeamId":"100000000000001"}]`. The inactivation shape and expected `ORA_INACTIVE` result were supplied by the user; the example ID is not a target. When the workbook exposes a top-level `TeamId` column, populate it with the same resolved ID. Keep optional `Content-Type` and `REST-Framework-Version` blank unless current metadata requires values. Reject `SAMPLE_VALUE` placeholders. The action changes only the team's lifecycle status; it does not carry parent create fields or child associations. Validate the archive against the live Data Loader schema before approval.

## Oracle Resource Read Order

For setup-data import, lookup, default, lifecycle, validation, and error decisions, read the applicable files in `ora-resource/` in this order:

1. `ora_input_validation.md`
2. `ora_dependency_readiness.md`
3. `ora_reference_lookups.md`
4. `ora_defaulting_rules.md`
5. `ora_design_enforcement.md`
6. `ora_error_handling.md`

The compiled `ora_rule_registry.json` is a planning artifact. It does not override an unresolved TBD or authorize a live action.

## Lifecycle Action Workflow

1. Select this route only for an explicit `Activate` or `Inactivate` request.
2. Establish the requested expected status: `ORA_DRAFT` to `ORA_ACTIVE` for Activate, or `ORA_ACTIVE` to `ORA_INACTIVE` for Inactivate.
3. Establish the exact target Fusion environment through the approved environment configuration without reading, copying, logging, or exposing credentials or tokens.
4. Resolve confirmed REST `communicateUICommTeams` capability, current metadata, and exact `communicateUICommTeams_updateTeamDetails` action with usable `POST` metadata, then obtain a fresh task-level CSV export. Stop when the REST capability or lifecycle action is unavailable; do not select FSM fallback.
5. Match `Team Name` exactly and require exactly one result. Stop on zero or multiple matches.
6. Read the current status from the exported row. For Activate, require `ORA_DRAFT` and prepare only the `activate` action for that exact `TeamId`. For Inactivate, require `ORA_ACTIVE` and prepare only the `inactivate` action for that exact `TeamId`.
7. Present an exact preview containing environment, task, team name, current status, requested action, expected status, and post-action verification method.
8. Prepare an immutable REST lifecycle archive with the current generated header order, `RestAction=POST`, the requested `action=activate` or `action=inactivate`, and a one-object `attributes` JSON array containing the exact `TeamId`. Set the top-level `TeamId` to that same value when exposed. Keep optional header fields blank unless required by current metadata, reject placeholders, and include no create or child fields. Do not prepare an FSM lifecycle archive.
9. Obtain fresh explicit approval bound to that exact archive immediately before the Data Loader submission. Prior approval for creation, another import, another environment, another team, or another action does not apply.
10. Submit the approved archive once. If the result is uncertain, do not submit it again.
11. Export again and verify the exact expected status for the exact team. Report success only after verification; otherwise return the visible diagnostic and stop.

### Lifecycle Preflight and Redaction

Before any inactivation side effect, preflight the environment identity, confirmed REST capability, current metadata and `POST` action, exact unique team, current status, requested live mode, and fresh approval. Redact sensitive diagnostics and never print or persist credentials, tokens, token caches, private keys, tenant secrets, or customer-sensitive payloads.

### Lifecycle Failure Boundaries

- If the REST capability or its exact `communicateUICommTeams_updateTeamDetails` `POST` metadata is unavailable for either lifecycle action, stop and report the blocker; FSM fallback is create-only.
- If environment identity, team identity, current status, route-specific update action, or approval is ambiguous, stop before mutation.
- A safe list read may be retried after a transport failure. Do not retry `Activate` or `Inactivate` automatically.
- For either lifecycle action, do not use a direct REST call, internal ADF operation, or FSM import; use only the governed REST Data Loader archive.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Retrieve the target environment's release details through `shared.baseline-assessment.topology-manager.environment-info` before resolving the create route:
   - Before `27A`, import the validated current task-CSV/FSM archive with `core.data-loader`; do not resolve REST setup-data metadata.
   - For `27A` and later, or when release details are unavailable, resolve the live `communicateUICommTeams` capability. When it is unavailable or unusable, import the validated current task-CSV/FSM archive and record the fallback reason; when it is usable, import setup data using `communicateUICommTeams` as the Business Object.
   - Use `communicateUICommTeams_updateTeamDetails` only for approved lifecycle status updates; the FSM release gate never enables lifecycle transitions.

Use this task metadata when invoking those skills:

- Offering: `HCM Communicate`
- Functional area / Setup Object: `Employee Communications`
- Setup task name: `Manage Communication Teams`
- Setup task code: `ORA_IRC_EMP_CAMP_COMM_TEAMS`




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `lifecycle_action`
- `target_environment`
- `environment_version_details`
- `team_name`
- `current_status_evidence`
- `campaign_status_evidence`
- `execution_intent`
- `approval`
- `requested_operation`
- `team_type`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`
- `current_team_state`
- `lifecycle_change_preview`
- `execution_authorization`
- `lifecycle_execution_result`
- `post_action_verification`

## Implementation Notes

Use the parent functional-area skill `hcm.hcm-communicate.employee-communications` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
