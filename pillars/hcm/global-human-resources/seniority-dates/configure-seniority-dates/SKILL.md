---
skill_id: "hcm.global-human-resources.seniority-dates.configure-seniority-dates"
name: "Configure Seniority Dates Setup Task Guidance"
description: "Provides task-specific setup guidance for Configure Seniority Dates under the Seniority Dates functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Seniority Dates"
functional_area_code: "ORA_SENIORITY_DATES"
task_code: "ORA_CONFIGURE_SENIORITY_DATES"
task_name: "Configure Seniority Dates"
parent_skill_id: "hcm.global-human-resources.seniority-dates"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "employmentSeniorityDateConfigurations"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
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
  - "hcm.global-human-resources.global-human-resources-common.manage-common-lookups"
  - "hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values"
oracle_supplied_guidance_files:
  - purpose: "Operation-specific input validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Dependency and reference readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Exact seniority-rule and related-reference resolution"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Defaulting and omitted-value preservation"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Data Loader route, preview, approval, and reconciliation enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Read and Data Loader failure handling"
    location: "ora-resource/ora_error_handling.md"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/seniority-dates/configure-seniority-dates/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/seniority-dates/configure-seniority-dates/current/"
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

# Configure Seniority Dates Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Configure Seniority Dates` under `Seniority Dates`.

## Task Overview

Use this task to plan and govern `Configure Seniority Dates` configuration in Global Human Resources.

- **Task identity:** `ORA_CONFIGURE_SENIORITY_DATES` — Configure Seniority Dates.
- **Scope:** HCM → Global Human Resources → Seniority Dates.
- **Catalog routing:** CSV export/import support is `Y`; the declared Data Loader mode is `REST` with `employmentSeniorityDateConfigurations`.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `ORA_CONFIGURE_SENIORITY_DATES`
- task_name: `Configure Seniority Dates`
- parent_skill_id: `hcm.global-human-resources.seniority-dates`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Seniority Dates`
- functional_area_code: `ORA_SENIORITY_DATES`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `employmentSeniorityDateConfigurations`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Configure Seniority Dates` under `Seniority Dates`.

## Setup Task Metadata

- Task name: `Configure Seniority Dates`
- Task code: `ORA_CONFIGURE_SENIORITY_DATES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `employmentSeniorityDateConfigurations`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `employmentSeniorityDateConfigurations` as the BusinessObject.

## CRUD and Reference Routing

- Read only through `employmentSeniorityDateConfigurations`. Resolve a supplied display name through `ORA_PER_SENIORITY_ITEMS`, then query the resolved `SeniorityDateCode`. When the caller explicitly requests a code contains search, use `q=SeniorityDateCode like '%term%'`, replacing `term` with the escaped caller-supplied value; never query a generic `Name` field.
- Select one list scope before reading: `active`, `inactive`, or `all`. An unqualified list request defaults to `active` (`Active=Y`); show inactive rules only when the caller explicitly requests inactive rules or all rules. If Fusion cannot apply an `Active` query predicate, retrieving bounded collection pages is transport only: apply the selected scope locally and discard nonmatching rows before lookup resolution, artifact generation, or response composition. Do not describe that transport read as an inactive-rules fetch. An explicitly all-configured-rules request retrieves every bounded page and parses every returned Seniority Date configuration row. Combine any additional caller-supplied filters with AND logic.
- Do not implicitly filter by DisplayInUI, RecordPresent, worker type, country, legal employer, union, collective agreement, blank values, or `N` values. The default Active-only list scope is the sole exception. DisplayInUI controls Fusion UI visibility only; it does not grant access to worker data, which remains controlled by Fusion data-security roles.
- For a read, complete rule resolution and the configuration read in the same turn; do not pause after resolving the lookup code.
- Route lookup resolution to [Global Human Resources Common > Manage Common Lookups](../../global-human-resources-common/manage-common-lookups/SKILL.md).
- Route profile option value resolution to [Global Human Resources Common > Manage Administrator Profile Values](../../global-human-resources-common/manage-administrator-profile-values/SKILL.md).
- For create, first identify the supplied business inputs. If any required create input is missing, stop deep validation and ask once for exactly the missing values. Only after intake is complete, run every applicable declared read and task rule in graph order. Execute all applicable declared resolvers in the same turn; pending tuple or reference resolution is not a response boundary. When the graph returns `SEN.LOADER_READY`, invoke `core.data-loader` with the task metadata, project context, `employmentSeniorityDateConfigurations`, operation, and resolved business values. Keep control until Core returns the immutable ZIP preview. Then wait for standalone `approve`; ask only for unresolved business input.
- Do not issue mutating Fusion REST calls.

## Mutation Safety Lifecycle

- Classify every mutation as `CREATE`, `UPDATE`, or `DELETE`; determine the configured Fusion environment and validate required read, Data Loader, and execution privileges before a preview is prepared. Do not ask the user to confirm the configured environment.
- Retrieve fresh current-state data and current lookup or LOV values in the same run before every mutation. Do not reuse a prior export, cached target, saved technical identifier, or preview.
- Apply all supplied predicates together. Require exactly one current match for an existing target or reference, zero current configuration rows for a create, and stop on missing, inactive, incompatible, or ambiguous evidence.
- Create intake is complete only when the caller supplies a current seniority rule code, attribute, and level. When omitted, default Active to `Y`, Cumulative to `N`, Display in Guided Flows to `N`, Allow Edit to `Y`, and scope to `No restriction`. An explicitly supplied supported value overrides its default. Do not proceed with partial create intake.
- After complete intake, resolve every supplied scope member through its declared resolver and require one exact current match for each member.
- After complete intake and independent exact resolution, validate a supplied cross-field combination only when current authoritative metadata explicitly binds the exact values. `ORA_PER_SENIORITY_ITEMS` lookup meaning is a display label, not a compatibility contract.
- Do not derive compatibility from a code suffix, naming pattern, free text, partial lookup meaning, related rule, or display label. When authoritative compatibility evidence is absent or ambiguous, report that compatibility could not be established and continue with the remaining declared validations; reject only when the authoritative source clearly proves a conflict.
- `No restriction` is the default scope choice when no scope selector is supplied; it leaves worker type, country, legal employer, union, and collective agreement blank. Resolve every supplied scope value independently and validate the combined scope only from current compatibility evidence.
- For an update, require one exact selector and one or more explicit supported changes, copy the complete fresh current row, and preserve every omitted field exactly, including blanks and multi-select scope members. Scope members are read-only and must never be added, removed, or changed.
- Users may explicitly set Active and Display in UI when supported. Object, Source Field, Triggering Field Type, Seniority Basis, Hours per Day, Hours per Month, Hours per Year, and Seniority Fast Formula are system-owned and must be derived from the current create template or preserved on update; reject user-supplied changes. Worker Type, Country, Legal Employer, Union, and Collective Agreement are unsupported in this Data Loader route because its DAT payload cannot serialize their required array values: show them in details, but do not offer or accept their creation or update; apply No restriction by default for new rules.
- Before generating a create workbook, apply `Scope: No restriction` when no scope selector is supplied, omit scope fields from the source, reject caller-supplied action and system-owned fields, derive the approved triggering-field tuple, and apply Active, Cumulative, Display in UI, Allow Edit, basis, and `POST` defaults. Fail closed when no approved tuple is available.
- For every update or deletion, invoke the current versioned Fusion `employmentConfigurations/action/performEmploymentOperations` action route immediately after resolving one fresh target. Resolve the Current supported versioned Fusion action route for the current authenticated run by GETting `/hcmRestApi/resources/latest/employmentConfigurations/describe`, locating the one collection link whose `rel` is `action` and whose `name` is `performEmploymentOperations`, and accepting it only when its host matches the configured Fusion host and its path is a versioned `/hcmRestApi/resources/{version}/employmentConfigurations/action/performEmploymentOperations` path. Use the returned href only for this run; never hardcode a tenant-specific `rv:` segment, construct, persist, or reuse a browser URL. Send `Content-Type: application/vnd.oracle.adf.action+json` and `inputParameterMap` containing `operation=configureSeniorityDatesOperation`, `evaluationMode=evaluateRuleUsage`, and `seniorityDateSetupId` set to the fresh resolved `SeniorityDateSetupId` as a string. `ruleUsed=true` means existing seniority records use the rule; `ruleUsed=false` means no existing seniority records use it. `RecordPresent=Y/N` is only the internal mapped control value; never lead a user-facing preview or result with that label. Do not infer it from a null or absent configuration-row field.
- If the evaluated `RecordPresent = Y`, permit updates only to Active, Allow Edit, and Display in UI. Block every other requested update and recommend creating a new rule or disabling the existing rule.
- For deletion, require one exact fresh target and confirmation that no existing seniority records use it (`RecordPresent=N`). If eligible, immediately prepare and present the exact delete preview. If existing seniority records use the rule (`RecordPresent=Y`), do not create a delete source or preview: return the blocked-delete error explaining that deletion is unsafe because existing seniority records use the rule. Use the registered Core Data Loader route with `RestAction=DELETE` and the resolved primary key `SeniorityDateSetupId` from the fresh target state. Do not issue a mutating Fusion REST call or invent an endpoint, payload, identifier, or alternate transport.
- Prepare the smallest supported mutation: one create row, one exact update row containing only the requested delta, or one exact delete target. Validate row shape, task identity, grouping key, references, duplicate cardinality, and immutable package integrity.
- Before execution, produce a preview with the environment alias, operation and task, exact business target, proposed values or before/after delta, scope, dependency result, and canonical current business-state fingerprint. For delete, show `Existing seniority records using this rule: Yes/No` and `Deletion eligibility: Eligible/Blocked`, rather than `RecordPresent`. For update, show the same usage result and explicitly identify the requested fields as permitted or blocked. The fingerprint excludes technical IDs, links, audit fields, and runtime context.
- A create, update, or delete request is never execution approval. Accept only a clear, standalone approval of one current preview. Reject absent, negative, conditional, ambiguous, stale, or different-preview approval.
- Immediately before execution, re-read the target and references and revalidate cardinality and the business-state fingerprint. Any change invalidates approval and requires a new preview. Submit an approved mutation once only; never replay a failed, timed-out, or uncertain mutation.
- Reconcile every mutation through a fresh current-state read. Report create or update success only when the approved state is proven, unrelated update fields are unchanged, and the execution result has no unresolved failures or warnings. Report delete success only when the former target cannot be read, the exact collection search returns zero matches, and fresh setup data contains zero matching rows.

## Seniority Date Authoring Rules

- Require explicit `read`, `create`, `edit`, or `delete` intent. For create, collect a valid seniority rule, level, attribute, applicable flags, worker types, and scope. For edit or delete, resolve exactly one current rule and require an explicit delta or delete intent.
- Resolve `SeniorityDateCode` through `ORA_PER_SENIORITY_ITEMS`, Attribute through `ORA_PER_TRIG_FIELDS`, and Level through `ORA_PER_SENIORITY_LEVELS`, each to one exact current enabled match. For Attribute, select only an enabled lookup value; never select an inactive Attribute. Treat lookup meanings as display labels. Do not parse them, or a code, to infer Attribute/Level compatibility. After the complete intake and independent resolution, enforce a cross-field constraint only when a separate current authoritative metadata contract explicitly binds the exact combination.
- When a caller supplies a misspelled, incomplete, or otherwise non-exact lookup value, do not select a close match. Present only active close candidates as suggestions and ask the caller to confirm one exact code or meaning; then resolve that confirmed value again through its declared lookup contract. Never present an inactive value as a candidate.
- For create, require zero current rows for the resolved code. For edit or delete, require exactly one current row. Preserve every omitted edit field, including worker-type members, and apply only requested additions or removals.
- Apply registered-object-supported create defaults for Active, display flag, calculation basis, standard time conversion, and blank formula or override fields. Do not default identity, dates, scope, worker types, or approval.
- Resolve worker type, country, legal employer, union, and collective agreement values independently; require one compatible current match and retain any technical IDs only transiently.
- For an exact Legal Employer selector, use the documented `legalEmployersLov` equality filter `q=Name='<escaped exact name>'` before an unfiltered page scan. Use bounded pagination only if that filter is unavailable or inconclusive, and still require exactly one exact current match.
- Determine each technical field from the current operation-specific create template. Require `Object`, `SourceField`, and `TriggeringFieldType` only when that template marks the field required. Apply the approved level and triggering-field defaults in `ora_defaulting_rules.md` only when current template and schema evidence accepts them. Populate `SeniorityVersion=V3` only when the current template exposes the field and current metadata explicitly allows `V3`; otherwise omit it. Validate every populated value against the current Data Loader schema; never copy a value from another rule or infer a value outside the approved default map.
- Before Data Loader submission, show the exact target, requested delta, preserved values, resolved references, XLSX source fingerprint, immutable preview, and post-load reconciliation plan. Any changed target, source, metadata subset, or preview requires renewed approval.
- For UI-backed `Select...` scope fields, accept user-supplied multiple values as comma-separated text, resolve each member independently, and submit the result as a JSON array. Submit a one-value selector as a one-item array; never send a scalar `Select...` value. When using a Data Loader workbook, preserve that array as compact JSON text (for example, `["Employee"]`), never a Python-style list such as `['Employee']`.
- Do not use a direct REST write, FSM import, CSV omission, or an automatic retry as a substitute for Core Data Loader.

## Seniority Date Read Presentation

- Resolve each displayed lookup-backed code against current Fusion lookup data: SeniorityDateCode through `ORA_PER_SENIORITY_ITEMS`; TriggeringField through `ORA_PER_TRIG_FIELDS`; SourceField through `ORA_PER_SRC_FIELDS`; LevelCode through `ORA_PER_SENIORITY_LEVELS`; Seniority Basis through `ORA_PER_SENIORITY_SETUP_BASIS`; and Active, Display in Guided Flows, Cumulative, and Allow Edit through `YES_NO`. Render the exact resolved Meaning, not the lookup code.
- For an all-configured-rules read, retrieve every bounded page of each required lookup type from its dedicated `commonLookups/{LookupType}/child/lookupCodes` collection before resolving the returned rows. Do not treat a parent request using `expand=lookupCodes` as exhaustive: it can return only a default-sized subset.
- Each displayed code requires exactly one current exact lookup match. Do not infer, generate, or partially match a display value. Report a missing or ambiguous lookup value for the affected rule rather than guessing.
- For every list or search result, return every matching rule and its total count. For an exact-details request, require exactly one configuration row; explicitly report zero or multiple matches.
- Present each matching rule using exactly these columns, in this order: `Seniority Rule Name (Code)`, `Status`, `Attribute`, `Level`, `Cumulative`, `Allow Edit`. Always include the underlying SeniorityDateCode beside the resolved rule name. Render `Active=Y` as `Active` and `Active=N` as `Inactive` in the Status column.
- Render `Y` as `Yes` and `N` as `No`. In a rule-detail response, omit an optional field or scope dimension when its current value is null, empty, or blank; never render it as `Blank`, `null`, or an empty-value label. This presentation rule does not filter a matching rule from an all-rules result or remove a required standard list column.
- When the caller explicitly asks for visibility details, add `Active` and `Display in Guided Flows` separately from the standard columns. Only apply a DisplayInUI filter when the caller explicitly requests UI-visible or UI-hidden rules.
- Keep row coordinates, reference IDs, links, host URLs, payloads, credentials, and tokens out of the response.
- For an all-details response, include the Seniority Date Code and every nonblank user-facing rule field. Do not show or discuss `SeniorityDateSetupId`, `Object`, `SourceField`, `TriggeringField`, or `TriggeringFieldType` unless the user explicitly names that individual field in their request.
- Finish every read response with the total number of matching rules, the safe Fusion environment alias, and the fresh export process identifier when one is available.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Seniority Dates`
- Setup task name: `Configure Seniority Dates`
- Setup task code: `ORA_CONFIGURE_SENIORITY_DATES`




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

Use the parent functional-area skill `hcm.global-human-resources.seniority-dates` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Resource References

- [Input validation](ora-resource/ora_input_validation.md)
- [Dependency readiness](ora-resource/ora_dependency_readiness.md)
- [Reference lookups](ora-resource/ora_reference_lookups.md)
- [Defaulting rules](ora-resource/ora_defaulting_rules.md)
- [Design enforcement](ora-resource/ora_design_enforcement.md)
- [Error handling](ora-resource/ora_error_handling.md)
