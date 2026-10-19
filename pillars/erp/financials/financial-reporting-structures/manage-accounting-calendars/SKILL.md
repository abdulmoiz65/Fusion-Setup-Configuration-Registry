---
skill_id: "erp.financials.financial-reporting-structures.manage-accounting-calendars"
name: "Manage Accounting Calendars Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Accounting Calendars under the Financial Reporting Structures functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Financial Reporting Structures"
functional_area_code: "ORA_ASK_FIN_REPORTING_STRUCT"
task_code: "GL_MANAGE_ACCOUNTING_CALENDARS"
task_name: "Manage Accounting Calendars"
parent_skill_id: "erp.financials.financial-reporting-structures"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/financial-reporting-structures/manage-accounting-calendars/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/financial-reporting-structures/manage-accounting-calendars/current/"
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
side_effects: []
required_privileges: []
---

# Manage Accounting Calendars Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, import, and validation guidance for `Manage Accounting Calendars` under `Financial Reporting Structures`.

## Setup Task Skill Contract

- task_code: `GL_MANAGE_ACCOUNTING_CALENDARS`
- task_name: `Manage Accounting Calendars`
- parent_skill_id: `erp.financials.financial-reporting-structures`
- pillar: `ERP`
- offering: `Financials`
- functional_area: `Financial Reporting Structures`
- functional_area_code: `ORA_ASK_FIN_REPORTING_STRUCT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, importing, or validating setup data for `Manage Accounting Calendars` under `Financial Reporting Structures`.

## Definition Source Boundary

For a project's first accounting-calendar run, obtain the same-environment,
same-release task template through the approved **template-only** route owned by
`shared.setup-export.task-level-export`. Validate the template package and
persist its metadata XML, member names, headers, column order, task identity,
environment, release, and fingerprint as that project's reusable technical
baseline. A later run for the same project may reuse the baseline only while
those compatibility checks still pass; otherwise obtain and persist a fresh
template-only package before authoring.

For calendar creation, derive the package definition only from that validated template baseline,
documented calendar rules, and the requested calendar definition. A
template-only fetch is not a Data Only Export: it must use
`setupTaskCSVTemplateExports`, never `setupTaskCSVExports`, and must contain no
current setup rows. Do not copy attribute values, period rows, naming choices,
or defaults from exported setup data or an existing calendar. Read-only
exact-name lookup is permitted solely to prevent a duplicate; it is not a
definition source.

Never request, initiate, or depend on an FSM **Data Only Export** for calendar
creation, general lookup, or failed-import troubleshooting. A permitted
existing-calendar update has one narrow exception for obtaining the complete
current parent carrier that Fusion requires:

1. Reuse the final FSCR-authored calendar package only when the calendar was
   created successfully in the current project/session and the retained package,
   successful load result, and post-load verification prove the exact task,
   environment, release, `UserPeriodSetName`, `PeriodSetName`, complete parent
   header, and current period rows. Treat any later external change or missing
   evidence as making this source unusable.
2. Otherwise automatically run one full current-data task export through
   `shared.setup-export.task-level-export` and `setupTaskCSVExports` as read-only
   update preflight. Do not ask for separate export approval; authentication may
   still pause for login. Do not use export criteria for this task because the
   tested calendar-name criteria were ignored by Fusion.
3. From that package, require exactly one `GL_PERIOD_SET.csv` row whose
   `UserPeriodSetName` and `PeriodSetName` match the identity resolved through
   `accountingCalendarsLOV`, and retain only that calendar's child rows as update
   evidence. If the exact target is absent, duplicated, ambiguous, or linked to
   inconsistent child rows, stop. Never substitute a similar calendar or derive
   defaults from unrelated exported rows.

Use current-data export values only to preserve and validate the exact existing
calendar in the requested update. They are not defaults for creation or another
calendar. Data Loader/FSM import remains the authoritative final product
validation, and an import failure is not a reason to run another Data Only
Export.

Treat deletion as unsupported. Existing-calendar updates use the controlled
update path below; never convert one into a duplicate create or a generic FSM
submission attempt. The permitted update scope is deliberately narrow:

- The description may be edited only by an FSM package submitted through the
  mandatory Data Loader workflow after exact identity resolution. Both the
  display name (`UserPeriodSetName`) and `PeriodSetName` are immutable; do not
  rename a calendar or rewrite child-row parent keys.
- A period-name format may change only while adding a new fiscal year. Select
  only a format allowed for the calendar frequency, generate the added year's
  rows using that format, and leave every existing/historical period row, name,
  date, and boundary unchanged. Before generating the added year, verify that
  the complete existing calendar has its expected rows, continuous standard
  dates, sequential numbering, valid quarters and adjustments, reconciled
  counts, and a complete immediately preceding fiscal year. The added year
  therefore has the newly requested format while prior years retain their
  prior format.
- An existing period's supported FSM/Data Loader fields are `PeriodNum`,
  `QuarterNum`, `StartDate`, `EndDate`, and `AdjustmentPeriodFlag`. Every
  changed row is affected and must be eligible. Block an existing-period name
  change through this task's FSM CSV route: `PeriodName` is the matching key
  and changing it causes Fusion to treat the row as a new period, while an
  `EnteredPeriodName`-only change does not update the displayed period name.
  Do not use a period-name prefix/header value as a workaround for existing
  rows.
  When associated ledgers exist, prove **Never Opened** (`ClosingStatus=N`)
  across every ledger and every returned application-specific status row.
  A per-ledger `accountingPeriodStatusLOV` response normally contains the
  ledger's full period history; this is not a blocker and requires no user
  follow-up. Retrieve every page, then automatically project the response onto
  the immutable affected `PeriodNameId` set, retain every matching
  `ApplicationId` row, and build the affected-period x associated-ledger
  coverage matrix. Ignore unrelated history rows. Use the original composite
  period identity only to cross-check the ID match, or as an exact fallback
  when `PeriodNameId` is unavailable; never use fuzzy name or date matching.
  Call this LOV with the cached OAuth bearer token and
  `REST-Framework-Version: 9`. A convenience-client call that returns no
  captured HTTP status or response body is a transport/client failure, not an
  empty result; retry the explicit GET with that header before blocking.
  For each successfully completed per-ledger query, matching rows must all be
  `N`. If the complete response has no matching row for an affected period--or
  no rows for that ledger at all--record `NO_STATUS_INSTANTIATED` for that
  ledger/period and allow it to pass without synthesizing an `N` row. This rule
  applies independently per ledger, so one empty ledger result may coexist with
  other ledgers whose matching rows are all `N`.
  Continue directly from successful retrieval through reduction and eligibility
  evaluation without asking the user to request another check or isolate rows.
  When a complete exact `ledgersLOV` query
  proves that the calendar has zero associated ledgers, query
  `accountingPeriodStatusLOV` directly for every affected period using its
  original name, year, number, and dates; resolve every returned `LedgerId`, and
  require that no returned status belongs to the target calendar. This
  zero-ledger/no-status branch is eligible because no ledger/application period
  status is instantiated for the calendar; an empty result is not mislabeled as
  `N`. Repeat the applicable complete check immediately before submission.
  Treat an inaccessible/truncated page, ambiguous identity, a target-calendar non-`N`
  row, or an evidence change as a blocker. Persist pagination receipts and the
  compact filtered matrix with period, ledger, application, status, dates, and
  retrieval time. A date change that requires
  an adjacent period boundary change makes that adjacent period affected and
  subject to the same rule.
  Preserve the original `PeriodNameId` in eligibility evidence. Preserve
  `PeriodName`, `EnteredPeriodName`, `PeriodYear`, calendar identity, frequencies, header
  counts, and header dates. Period numbers and quarters must still start and
  progress according to the calendar rules; adjustment-flag changes must retain
  the existing adjustment policy and reconciled counts. If the requested edit
  cannot preserve full-calendar continuity, uniqueness, numbering, quarter
  assignment, adjustment geometry, and those protected fields, stop. Treat the
  UI Additional Information region as DFF data, not a core calendar field; edit
  it only through a separately validated context/segment contract.

Changes to an existing calendar's start date, non-adjusting frequency,
adjustment policy, `UserPeriodSetName`, `PeriodSetName`, parent linkage, or
any period field outside the conditionally permitted UI-editable core fields
remain blocked. Require an explicit update approval before any permitted
existing-calendar update.

Budgetary-control-only calendars are a separate mode. They use the
budgetary-control calendar type, `OTHER` frequency, an explicit number of
budget periods, no user-selectable adjustment policy, and the budget-period
naming generated by the approved template. Do not apply normal accounting
calendar frequency, adjustment, or naming defaults to this mode.

Weekly (`WEEK`) is the finest-grain supported standard calendar frequency.
Reject Daily or any finer-grain generated or manual calendar design, including
an attempt to express daily periods through `OTHER`.

## Read Order

1. Read `ora-resource/ora_input_intake.md`.
2. Read `ora-resource/ora_input_validation.md`.
3. Read `ora-resource/ora_dependency_readiness.md`.
4. Read `ora-resource/ora_reference_lookups.md`.
5. Read `ora-resource/ora_defaulting_rules.md`.
6. Read `ora-resource/ora_design_advisory.md`.
7. Read `ora-resource/ora_design_enforcement.md`.
8. Read `ora-resource/ora_bulk_intake.md`.
9. Read `ora-resource/ora_rest_execution.md`.
10. Read `ora-resource/ora_error_handling.md`.

## Setup Task Metadata

- Task name: `Manage Accounting Calendars`
- Task code: `GL_MANAGE_ACCOUNTING_CALENDARS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## Template Acquisition, Import, and Validation Workflow

The catalog's `CSVExportImportSupportedFlag` remains `Y`. Creation uses only the
template route; a permitted update may use the controlled current-value source
rule above. Route acquisition, package validation, and import through:

1. On the project's first run, or when its persisted template baseline is
   incompatible, automatically fetch the header-only task template with
   `shared.setup-export.task-level-export` in template-only mode. Treat this as
   normal non-business-data preflight under the user's calendar request; do not
   ask for a separate conversational approval. Authentication may still pause
   for user login when the token is stale.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

For a permitted update, resolve its complete current parent and period baseline
before step 2: reuse the verified current-session FSCR creation package when
eligible; otherwise automatically obtain one full task data export and isolate
the exact target. The full export is required for description-only updates,
period-name-format changes that add a fiscal year, and eligible existing-period
field edits whenever the verified current-session source is unavailable.

`core.data-loader` is the mandatory execution owner for every calendar import.
It must perform the task validation, immutable-preview, approval, and submission
workflow for the FSM ZIP, including the adapter handoff and invocation.
`shared.setup-import.task-level-import` may be used only as the Data
Loader-invoked FSM adapter; never call that adapter directly after a chat
approval, a locally approved preview, or a Data Loader authorization record.

Use this task metadata when invoking those skills:

- Offering: `Financials`
- Functional area / Setup Object: `Financial Reporting Structures`
- Setup task name: `Manage Accounting Calendars`
- Setup task code: `GL_MANAGE_ACCOUNTING_CALENDARS`


## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `erp.financials.financial-reporting-structures` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Runtime Verification and Result Reporting

1. Never access Fusion setup UI for discovery, duplicate checks, validation or verification, including through delegates or user-supplied screenshots. Use the declared endpoints and FSCR framework; authentication through core.auth is the sole user-completed browser handoff. Follow [endpoint-only verification](ora-resource/ora_reference_lookups.md#endpoint-only-verification).
2. Inspect the actual matching process logs before reporting any submitted import as successful or failed. For lookups or pre-submission checks, inspect their actual response or diagnostics. Follow [result reporting](ora-resource/ora_error_handling.md#mandatory-log-review-before-outcome-reporting).
