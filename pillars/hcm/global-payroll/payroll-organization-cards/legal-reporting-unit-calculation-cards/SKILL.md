---
skill_id: "hcm.global-payroll.payroll-organization-cards.legal-reporting-unit-calculation-cards"
name: "Legal Reporting Unit Calculation Cards Setup Task Guidance"
description: "Provides TRU-scoped Legal Reporting Unit Calculation Cards guidance with read-only existence/history discovery, automatic DIR card and component key resolution, object-level create-versus-update classification, update/correction confirmation for existing data, and HDL-only mutations."
layer: "pillar"
pillar: "HCM"
offering: "Global Payroll"
functional_area: "Payroll Organization Cards"
functional_area_code: "ORA_PAYROLL_ORGANIZATION_CARDS"
task_code: "PAY_MANAGE_LEGAL_REPORTING_UNIT_DEDUCTION_RECORDS"
task_name: "Legal Reporting Unit Calculation Cards"
parent_skill_id: "hcm.global-payroll.payroll-organization-cards"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "HDL"
businessObject: "CalculationCard"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global payroll pillar team"
version: "0.12.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "legal_reporting_unit_search_text"
  - "legislative_data_group_search_text"
  - "legislative_data_group_territory"
  - "ldg_owner_association_request"
  - "tax_reporting_unit_name"
  - "legislative_data_group_name_request"
  - "component_flexfield_value_request"
  - "component_calculation_value_request"
  - "requested_effective_date"
  - "date_effective_action_preference"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "legal_reporting_availability_result"
  - "legal_reporting_candidates"
  - "legislative_data_group_availability_result"
  - "legislative_data_group_candidates"
  - "tax_reporting_unit_association_candidates"
  - "legislative_data_group_name"
  - "legislative_data_group_id"
  - "legislation_code"
  - "component_flexfield_values"
  - "existence_discovery_summary"
  - "resolved_operation_plan"
  - "resolved_runtime_technical_keys"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-organization-cards/legal-reporting-unit-calculation-cards/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-organization-cards/legal-reporting-unit-calculation-cards/current/"
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

# Legal Reporting Unit Calculation Cards Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Legal Reporting Unit Calculation Cards` under `Payroll Organization Cards`.

## Setup Task Skill Contract

- task_code: `PAY_MANAGE_LEGAL_REPORTING_UNIT_DEDUCTION_RECORDS`
- task_name: `Legal Reporting Unit Calculation Cards`
- parent_skill_id: `hcm.global-payroll.payroll-organization-cards`
- pillar: `HCM`
- offering: `Payroll`
- functional_area: `Payroll Organization Cards`
- functional_area_code: `ORA_PAYROLL_ORGANIZATION_CARDS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Legal Reporting Unit Calculation Cards` under `Payroll Organization Cards`.

## REST Retrieval and HDL Mutation Contract

- Inherit the parent skill's REST retrieval and HDL mutation boundary without exception.
- Use REST only for read-only discovery and reference resolution, including `getCardDetails`, `payGenericRestQuery`, `payrollGenericLOV`, legal-reporting-unit searches, and LDG lookups. A read-only action may use `POST` when required by its retrieval contract.
- Never call `calculationEntries/mergeCard`, `calculationEntries/deleteCard`, or another REST mutation endpoint for a TRU card. Never prepare or approve a direct REST mutation payload.
- Prepare every create, update, correction, end-date, and delete as `CalculationCard` HDL. Validate the exact target-supported action, sections, user keys, effective dates, and parent-child rows before preview; block an unsupported action instead of falling back to REST.
- Treat `getCardDetails` `mode=ADD` only as read-only template discovery. Route any approved HDL archive through `core.data-loader` for validation and load handling.
- Ignore any historical mutation wording retained in HAR-derived resources; it is non-executable evidence and cannot override this contract.

## Existing-Data and Operation Decision Contract

- Inherit the parent skill's object-level existence states and effective-date decision matrix.
- Analyze the request by functional owner, card, component, field/value, assignment or association when applicable, and effective date. Treat the user's create/update wording as intent until target discovery completes.
- Run owner-scoped `getCardDetails` discovery without `dirCardId`, select the exact TRU card by business name and effective history, retain its returned `dirCardId` internally, and run the exact drilldown. Resolve all other technical IDs internally; never ask a functional user for `dirCardId`, `dirCardCompId`, `dirCardCompDefId`, an override-group ID, source ID, LDG ID, or assignment/association ID.
- Use the complete returned current/future/history state to classify every requested leaf record. If no exact business key exists, create only that missing card, component, override/FLEX/value, or association row under any resolved existing parents. If the business key exists, do not duplicate it.
- Before preparing HDL for existing data, notify the user with business names, current value when relevant, effective interval, requested date, and adjacent future row. Ask the user to confirm `Update` or `Correction`. Recommend Update for a later date inside the selected interval and Correction when the requested date equals the selected row start; block unsupported or conflicting date shapes instead of guessing.
- Do not treat one empty effective-date response as proof that data never existed. Require complete existing-state discovery or return a blocking diagnostic.

## Owner Scope Contract

- Inherit the parent skill's case-insensitive owner-scope synonym map.
- Accept only the TRU family: `Legal Reporting Cards`, `Legal Reporting Unit HCM Information`, `TRU Cards`, `Tax Reporting Unit Cards`, and `Legal Reporting Unit Calculation Cards`.
- Resolve the owner as a Tax Reporting Unit and use `sourceType=TRU` for calculationEntries requests.
- If the request resolves to the PSU family, stop this route and hand off to the sibling Legal Entity Calculation Cards skill. Do not reinterpret a PSU request as TRU based on card name or legislation.

## Legal Reporting Unit Availability Contract

- Use the read-only `hcmLegalReportingUnits/action/findByAdvancedSearchQuery` POST contract in `ora-resource/ora_rest_execution.md` when the user asks whether a legal reporting unit exists or is available.
- Preserve the trimmed user input as the query. For one or more matches, return only `Legal Reporting Unit names:` and the returned `Name` values, one name per line in response order; do not number the names or show technical fields unless explicitly requested.
- Keep `EstablishmentId`, `TruStatus`, registration values, parent organizations, dates, and pagination metadata internal. A list-only request ends after the names are returned. If downstream TRU or card work was also requested and multiple rows matched, wait for the user to select one before continuing.
- Use `TruStatus` internally to distinguish a returned reporting unit from one that is active for this TRU-scoped calculation-card flow.

## TRU List by Legislation, LDG, or PSU Contract

- Treat a request for TRU or Legal Reporting Unit organization cards by legislation code, LDG ID, or PSU ID as read-only TRU discovery.
- Call `OrgTaxReportingUnitPVO` through one serialized `payGenericRestQuery` finder beginning `finder=findByWord;PayRestName=OrgTaxReportingUnitPVO` and ending `DisplayAttributes=PsuId||Name||OrganizationId||LdgId`; use commas between finder inputs rather than separate URL query parameters. Do not request `LegalEntityId` from this PVO.
- Use `AdditionalViewCriteria=findByLegislationCode` with `ParameterKeys=pLegislationCode` when a legislation code is supplied.
- Use `AdditionalViewCriteria=findByLdgId` with `ParameterKeys=pLdgId` when an LDG ID is supplied.
- Use `AdditionalViewCriteria=findByPsuId` with `ParameterKeys=pPsuId` when a PSU ID is supplied.
- When more than one filter value is known, combine criteria and keys with `||`, for example `AdditionalViewCriteria=findByLegislationCode||findByLdgId||findByPsuId`, `ParameterKeys=pLegislationCode||pLdgId||pPsuId`, and matching ordered `ParameterValues`.
- Map each returned `OrganizationId` to the TRU calculationEntries `sourceId`, map `LdgId` to `legislativeDataGroupId`, retain `PsuId` as the parent payroll statutory unit reference, and keep `sourceType=TRU`.
- For one or more rows, return only `Legal Reporting Unit names:` and the returned `Name` values, one name per line in response order; do not number names or show technical fields unless explicitly requested.

## Legislative Data Group Name Resolution Contract

- Treat a request for the LDG name of a supplied TRU as read-only. Resolve the TRU name to exactly one legal-reporting-unit row, require the selected active TRU, retain its `EstablishmentId`, and do not auto-select among fuzzy matches.
- Call `OrgTaxReportingUnitPVO` with `finder=findByWord;PayRestName=OrgTaxReportingUnitPVO,AdditionalViewCriteria=findByEstablishmentId,ParameterKeys=pEstablishmentId,ParameterValues=<EstablishmentId>,DisplayAttributes=OrganizationId||LdgId`. Require one row, map `OrganizationId` to the TRU calculationEntries `sourceId`, and map `LdgId` to `legislativeDataGroupId`.
- Call `GET /hcmRestApi/resources/11.13.18.05/legislativeDataGroupsLOV` with `q=LegislativeDataGroupId=<LdgId>`, `fields=LegislativeDataGroupId,Name,LegislationCode`, `onlyData=true`, and complete paging. Require one exact ID match and map `Name` to `legislative_data_group_name` and HDL `LegislativeDataGroupName`.
- Return only `Legislative Data Group name:` and the exact LDG `Name` unless technical details are requested. Never derive or hardcode the name from the TRU name, parent legal entity, or legislation.
- Use the live lookup contracts in `ora-resource/ora_reference_lookups.md` through `core.fusion-api.rest-api-client` and `core/auth/fusionEnv.properties`. Stop on absence, ambiguity, inactive TRU state, incomplete paging, authorization denial, an ID mismatch, or a missing `OrganizationId`/`LdgId`. Do not generate or load HDL for this lookup.

## Legislative Data Group Availability Contract

- Treat a request containing a full or partial LDG name, or requesting all LDGs in a territory, as read-only LDG discovery; it does not require a TRU to be selected.
- For name search, preserve meaningful trimmed text as `query` and send `filters=[]`. For “all US LDGs”, send `query=""` with `TerritoryShortName=United States` using the exact filter shape in `ora-resource/ora_rest_execution.md`. Allow an empty query only with a nonblank restrictive filter.
- Preserve the fields, filters, pagination, environment, and runtime-route contract across all pages. Verify every territory-filtered row has the requested `TerritoryShortName`.
- For zero matches, report not found and invite refinement. For one or more matches, return only `Legislative Data Group names:` and every returned `Name`, one per line in response order. A list-only request ends after the complete list; multiple matches require user selection only before downstream card work.
- Keep IDs, currency, territory, costing structure, and pagination internal unless technical details are requested. This search must not create a DAT or ZIP, upload a file, or initiate a load.

## Combined LDG Owner Discovery Contribution Contract

- When the parent skill requests the combined LDG, PSU, and TRU mapping for a territory, contribute the complete legislation-scoped TRU dataset; do not render a standalone `Legal Reporting Unit names:` response and do not ask the user to select a TRU.
- For United States, call `OrgTaxReportingUnitPVO` once with `AdditionalViewCriteria=findByLegislationCode`, `ParameterKeys=pLegislationCode`, `ParameterValues=US`, and `DisplayAttributes=PsuId||Name||OrganizationId||LdgId`. Follow all returned paging or next links before returning control to the parent. Do not substitute `LegalEntityId`; that unsupported display attribute can produce a zero-row response.
- Require nonblank `Name`, `OrganizationId`, and `LdgId`. Deduplicate by `OrganizationId`, preserve first-seen order, and return `tax_reporting_unit_association_candidates` with `PsuId`, `Name`, `OrganizationId`, and `LdgId` to the parent.
- Let the parent join `LdgId` to the LDG response's exact `LegislativeDataGroupId`. Retain `PsuId` only as the parent PSU reference; do not use it instead of `LdgId` for the LDG join. Do not associate a TRU by name, response position, or naming convention, and do not discard an owner whose `LdgId` is outside the parent's retrieved LDG set.
- Treat this contribution as read-only. It must not generate HDL, create a DAT or ZIP, upload a file, or initiate a load.

## Component Flexfield Value List Contract

- Treat a request for the flexfield values of a given component as read-only. Require an exact tax reporting unit, card, component, and effective date; use prior conversation context only when it resolves all four uniquely.
- For an existing component, use the `getCardDetails` drilldown contract with `sourceType=TRU`, `mode=G`, `showEmptyComponent=N`, and `expand=Cards,Components,Overrides,CompAssociation`. For an addable component's template/default values, use the `mode=ADD` contract with `expand=Cards,Components,Overrides,Associations` and the source-backed component override-group metadata.
- Select exactly one returned component by component name or base name. If the name occurs more than once, show the business labels, effective intervals, and current-value context and ask for a functional selection; retain `componentSequence` internally and do not merge override rows across component instances.
- Keep only that component's rows whose `overrideType=FLEX`. Use `title` as the business label when present, otherwise `name`. Show the current/default `value`; for LOV-backed rows, resolve a stored code to one display meaning when possible and otherwise return the stored value without guessing. Render null or empty values as `Blank`.
- Return only `Flexfield values:` followed by one `Name: Value` line per FLEX row in response order. Return `None` under the heading when no FLEX row exists. Keep IDs, codes, categories, flags, data sources, pagination, and component metadata internal unless explicitly requested.
- Do not confuse current/default values with a request for allowed or available LOV choices. An option-list request uses the metadata-declared LOV resolver. This value-list contract must not create a DAT or ZIP, upload a file, initiate a load, or request mutation approval.

## Setup Task Metadata

- Task name: `Legal Reporting Unit Calculation Cards`
- Task code: `PAY_MANAGE_LEGAL_REPORTING_UNIT_DEDUCTION_RECORDS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

These catalog flags do not authorize a CSV/FSM or direct REST mutation of a calculation card. A read-only setup export may use its approved export contract, but step 4 below must use the `CalculationCard` HDL contract in this skill.

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Global Payroll`
- Functional area / Setup Object: `Payroll Organization Cards`
- Setup task name: `Legal Reporting Unit Calculation Cards`
- Setup task code: `PAY_MANAGE_LEGAL_REPORTING_UNIT_DEDUCTION_RECORDS`

## Calculation Card Data Import Contract

- Registered business object: `CalculationCard` (case-sensitive).
- For HDL creation, apply absent values as follows: new-card `CardSequence=1`; new-component `ComponentSequence=1`; `EffectiveStartDate` equals the runtime system date resolved when the DAT preview is generated; and `EffectiveEndDate=4712/12/31`. Emit dates as `YYYY/MM/DD`, not the literal token `SYSDATE`.
- Preserve user-supplied values. Propagate the final parent `CardSequence` into `CardComponent` and `ComponentDetail`, and propagate the final `ComponentSequence` into `ComponentDetail`. For a component added to an existing card, use the card's resolved sequence rather than replacing it with the new-card default.
- Validate sequence uniqueness and parent effective-date containment before preview. When a creation sequence conflicts, resolve the lowest positive unused sequence only after complete target discovery proves the used set; otherwise block with an internal resolver diagnostic rather than asking the functional user for a technical key.
- Resolve the system date once per DAT preview and keep that concrete date unchanged through approval, file creation, ZIP packaging, upload, and load. A regenerated preview on a later date must display and obtain approval for its newly resolved start date.
- Import route: `core.data-loader` using its approved HDL workflow with `CalculationCard`; the skill itself must not call a direct calculation-card REST mutation.
- Pass `CalculationCard` as the business object when generating or validating setup data, and preserve it as the top-level DAT discriminator.
- For an approved live import, let `core.data-loader` validate the artifact against live metadata, package it as a ZIP, upload it with `uploadDataLoaderFile`, and start it with `initiateDataLoad`.
- Treat the `calculationEntries` endpoints documented in `ora-resource/ora_rest_execution.md` as retrieval-only contracts. Do not call, reconstruct, or substitute `mergeCard`, `deleteCard`, or another direct REST mutation for the `CalculationCard` HDL route.
- Require explicit user approval before upload or import. Do not retry a live import automatically.


## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `legal_reporting_unit_search_text`
- `legislative_data_group_search_text`
- `legislative_data_group_territory`
- `ldg_owner_association_request`
- `tax_reporting_unit_name`
- `legislative_data_group_name_request`
- `component_flexfield_value_request`
- `component_calculation_value_request`
- `requested_effective_date`
- `date_effective_action_preference`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `legal_reporting_availability_result`
- `legal_reporting_candidates`
- `legislative_data_group_availability_result`
- `legislative_data_group_candidates`
- `tax_reporting_unit_association_candidates`
- `legislative_data_group_name`
- `legislative_data_group_id`
- `legislation_code`
- `component_flexfield_values`
- `existence_discovery_summary`
- `resolved_operation_plan`
- `resolved_runtime_technical_keys`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.global-payroll.payroll-organization-cards` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
