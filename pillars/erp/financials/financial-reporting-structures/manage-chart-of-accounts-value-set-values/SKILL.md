---
skill_id: "erp.financials.financial-reporting-structures.manage-chart-of-accounts-value-set-values"
name: "Manage Chart of Accounts Value Set Values Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Chart of Accounts Value Set Values under the Financial Reporting Structures functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Financial Reporting Structures"
functional_area_code: "ORA_ASK_FIN_REPORTING_STRUCT"
task_code: "GL_MANAGE_CHART_OF_ACCOUNTS_VALUE_SET_VALUES"
task_name: "Manage Chart of Accounts Value Set Values"
parent_skill_id: "erp.financials.financial-reporting-structures"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FBDI"
businessObject: ""
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/financial-reporting-structures/manage-chart-of-accounts-value-set-values/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/financial-reporting-structures/manage-chart-of-accounts-value-set-values/current/"
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

# Manage Chart of Accounts Value Set Values

## Purpose

Use this skill to create or update segment values in one named existing value
set. It prepares a values-only FBDI package and hands the verified package to
`core/data-loader`; Data Loader owns import selection, upload, submission,
monitoring, and returned outcome.

Use the parent Value Sets GET only to resolve the exact target and validate its
`MaximumLength`. Do not inspect requested values before or after the Data Loader
route.

Do not create or import hierarchies in this skill.

## Input Contract

Accept four import sources:

| Source | Normalization |
|---|---|
| Natural-language text | Extract one ValueSetCode and every value row in input order |
| Image | Read visible table headers and cells, preserve blank versus populated fields, and ask once for unreadable required cells |
| CSV | Parse headerless FBDI rows with 13 through 101 columns |
| ZIP | Select exactly one `GlSegmentValuesInterface.csv`; a hierarchy CSV is not required |

Before authentication for an import, require:

- Value Set Code.
- At least one nonblank Value.
- Description for every value.
- Summary Flag for every value.
- Allow Posting Flag for every value.
- Allow Budgeting Flag for every value.

After flag normalization, reject any row where `SummaryFlag=Y` and either
`AllowPostingFlag=Y` or `AllowBudgetingFlag=Y`. A summary value must have both
Allow Posting and Allow Budgeting set to `N`. Never silently replace an
explicit conflicting flag; report the row and fields so the user can correct
the input.

A clear batch-wide flag applies to every row. Ask one consolidated question for
all missing required fields. Do not infer a Value or required flag from a
description or an unreadable image cell. A Description may support an Account
Type suggestion only under the reviewed Natural Account workflow below. Default
`EnabledFlag=Y` for text input when omitted; CSV and ZIP rows must supply
Enabled Flag in column 6.

Treat an attachment without an explicit create, import, upload, or execute
instruction as preparation/preview only. An explicit import instruction requests
live execution but does not approve a generated package. Route the immutable
package through `core.data-loader`, show its exact preview, and obtain explicit
approval before upload or submission. Any source, mapping, validation, or package
change invalidates that approval and requires a new preview.

## Read-Only Value Set Preflight

After base input validation and authentication, but before package generation or
handoff, resolve the target
through the parent Value Sets collection:

```text
GET /fscmRestApi/resources/11.13.18.05/valueSets
    ?q=ValueSetCode='{ValueSetCode}'
    &fields=ValueSetId,ValueSetCode,MaximumLength,ValidationType,ValueDataType,ValueSubtype,ProtectedFlag
    &limit=2
```

URL-encode the query and safely escape the supplied code. Apply an exact,
case-sensitive comparison to returned `ValueSetCode` values even when the
server-side query is broader.

- No exact match: report that the Value Set Code doesn't exist and stop without
  child-value retrieval, ZIP creation, upload, or ESS submission.
- Exactly one exact match: retain its `ValueSetId`, `ValueSetCode`,
  `MaximumLength`, validation/data/subtype metadata, and protected state.
- More than one exact match: stop as an ambiguous catalog result.
- Missing or nonnumeric `MaximumLength`, or a value outside 1 through 150: stop
  as a catalog mismatch; never guess or default the length.

Use this parent GET only for existence and read-only metadata. Never use parent
POST/PATCH/DELETE or child Values REST mutation in this skill. If the lookup is
unauthorized or unavailable, report the auth, authorization, transport, or
Fusion API failure and stop.

## Value-Existence Handling

Never query child values or inspect existing rows before submission. This
applies equally to Natural Account and normal segments. Let the Data Loader
route determine whether supplied rows create, update, fail validation, or
produce zero new values.

Do not offer or execute a standalone value-existence lookup from this skill.
If a user asks whether values exist, explain that this task intentionally relies
on the Data Loader result for create/update processing.

Determine value-set usage without querying values:

- In an end-to-end plan, use the established Chart of Accounts Structure
  Instance context when it proves that the target value set is assigned to the
  Natural Account segment.
- For a standalone task run, treat Natural Account usage as true only when the
  user explicitly declares it. Do not infer it from the value set name, value,
  or description.
- When Natural Account usage is proved or declared, require Account Type for
  every row. Suggest a type from the Description only when the meaning is
  unambiguous, then require the user to accept or correct every suggestion.
  Ask the user for any row that cannot be safely suggested.
- When Natural Account usage is not proved or declared, leave Account Type
  blank unless the user explicitly supplies it; validate and normalize any
  supplied value.

## FBDI CSV Contract

Generate exactly 101 columns without a header. The first 13 positions are:

| Position | Field |
|---:|---|
| 1 | Value Set Code |
| 2 | Value |
| 3 | Start Date |
| 4 | End Date |
| 5 | Summary Flag |
| 6 | Enabled Flag |
| 7 | Account Type |
| 8 | Allow Posting Flag |
| 9 | Allow Budgeting Flag |
| 10 | Third Party Control Account |
| 11 | Reconcile Flag |
| 12 | Financial Category |
| 13 | Description US |

Positions 14 through 101 retain the current template order for translated
descriptions, Attribute1 through Attribute50, Data Source, the four added
translated descriptions, and the workbook-only Is Validated marker. Always
write the Is Validated position blank. Use UTF-8 without a byte-order mark.
Follow the exact ordered mapping and deterministic processing algorithm in
`ora-resource/ora_fbdi_processing.md`.

Package the CSV as:

```text
glsegmentvaluesandhierarchy.zip
└── GlSegmentValuesInterface.csv
```

Do not add `GlSegmentHierInterface.csv` for a values-only request. The 26C
template macro skips an empty hierarchy sheet, and the attached working sample
contains only the values CSV.

The loader control file supplies `STATUS_CODE=NEW`, `OBJECT_VERSION_NUMBER=1`,
`LOAD_REQUEST_ID`, and audit columns. Do not add those as CSV positions.

## Validation and Defaults

Run complete-batch local validation before ZIP generation:

- Reject blank and duplicate values, and reject a blank Description.
- Enforce `MaximumLength` returned by the exact parent Value Sets lookup.
- Normalize Y/Yes/true/1 and N/No/false/0 to Y/N.
- Accept input dates as YYYY-MM-DD or YYYY/MM/DD; write YYYY/MM/DD and require
  End Date not earlier than Start Date.
- Apply the reserved-word, restricted-character, and description rules in
  `ora-resource/ora_input_validation.md`.
- Preserve supported translated descriptions, Attribute1 through Attribute50,
  and Data Source from CSV/ZIP input.
- Reject unknown nonblank columns after position 101.

For a value set proved or declared to be Natural Account, require a reviewed
Account Type for every row. Normalize Asset/A, Liability/L, Expense/E, Owner's
Equity/O, and Revenue/R to A/L/E/O/R, then default omitted Third Party Control
Account and Reconcile Flag to N. For any other value set, preserve an explicit
valid Account Type when supplied; otherwise leave it blank.

Do not create a package when any row fails.

## Data Loader Handoff

After successful validation and package verification, produce a preview with:

- Exact environment and Value Set Code.
- Every requested value and business attribute.
- Every applied default.
- Row count, 101-column count, ZIP member list, CSV hash, and ZIP hash.
- Data Loader route and wait configuration.

Use this component split:

| Folder | Role |
|---|---|
| `core/data-loader/` | Mandatory orchestration, validation, immutable preview, and approval workflow |
| `core/data-loader/` | Validate task scope, construct the immutable preview, obtain approval, select the import route, and return the execution outcome |

Route every live create/update through `core/data-loader`. It owns the immutable
preview, approval, import selection, submission, monitoring, and returned
outcome. This task supplies only the verified values-only FBDI package and the
task-specific validation evidence. Do not add a second transport, REST, or ESS
execution path in this skill.

Treat the Data Loader result as the overall outcome. Report requested values as
submitted and mark row-level created, updated, rejected, and unchanged counts as
unavailable unless the returned result supplies them. Never run a post-handoff
value lookup to manufacture those counts.

## User-Facing Response

For create/update operations, return only the Data Loader outcome, Value Set
Code, requested values, primary request ID when returned, terminal status, and concise loader
diagnostics when applicable. State that row-level create/update/reject counts
are unavailable from this route. Don't include
documentation links, API links, local artifact links or paths, package or
UCM document IDs, or internal storage details. Continue to persist prescribed
audit artifacts internally.

## Workflow

1. Validate the create/update candidate from text, image, CSV, or ZIP input.
2. Resolve exactly one parent value set by read-only GET and retain its
   `MaximumLength`; stop on no match or ambiguity.
3. Determine Natural Account usage from established Structure Instance context
   or an explicit standalone declaration. For Natural Account values, suggest
   Account Type from Description where unambiguous and obtain user acceptance
   or correction; request any unresolved types.
4. Generate or safely reuse and reopen the 101-column values-only ZIP and
   persist the preview and hashes.
5. Hand the verified immutable package to `core/data-loader` for its preview,
   approval, import selection, submission, monitoring, and outcome handling.
6. Do not issue separate REST, ESS, process-tree, child-job, LOG, OUT, or
   post-handoff value requests.

## Markdown Processing Contract

This skill contains no local executable code. Read
`ora-resource/ora_fbdi_processing.md` before parsing a file, classifying segment
usage, validating rows, or constructing an FBDI package. Apply its algorithms
directly with the runtime's available file and archive capabilities. Never
continue to package generation without a successful classified prepared
candidate.

## Read Order

1. `ora-resource/ora_input_intake.md`
2. `ora-resource/ora_input_validation.md`
3. `ora-resource/ora_dependency_readiness.md`
4. `ora-resource/ora_reference_lookups.md`
5. `ora-resource/ora_defaulting_rules.md`
6. `ora-resource/ora_bulk_intake.md`
7. `ora-resource/ora_fbdi_processing.md`
8. `ora-resource/ora_design_enforcement.md`
9. `ora-resource/ora_error_handling.md`

## Boundaries

- Use the FBDI Data Loader route only for value creation and update.
- Use only a read-only parent Value Sets GET to prove exact existence and obtain
  `MaximumLength` and basic definition metadata.
- Do not use child Values REST. Do not use Value Sets parent mutation.
- Do not query whether supplied values already exist, before or after import.
- Do not query values to classify Natural Account usage; use
  established Structure Instance context or an explicit standalone declaration.
- Do not run a post-handoff value or separate status call; determine the outcome
  only from `core.data-loader`.
- Do not use FSM import/export, task-level setup export, or a fresh baseline
  export anywhere in this task.
- Do not create hierarchy rows or include a hierarchy CSV.
- Do not delete values.
- Route every create/update through `core.data-loader`.
- Do not expose credentials, tokens, UCM security details, or authorization
  headers.

## Oracle Sources

- https://docs.oracle.com/en/cloud/saas/financials/26c/faigl/how-segment-value-and-hierarchy-import-data-is-processed.html
- https://docs.oracle.com/en/cloud/saas/financials/26c/oefbf/index.html
- https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-servername-fscmrestapi-resources-11.13.18.05-valuesets-get.html
