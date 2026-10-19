---
skill_id: "hcm.global-payroll.payroll-organization-cards.legal-entity-calculation-cards"
name: "Legal Entity Calculation Cards Setup Task Guidance"
description: "Provides PSU-scoped Legal Entity Calculation Cards guidance with read-only existence/history discovery, target-metadata-validated DIR card and component key resolution, object-level create-versus-update classification, HDL load-failure diagnosis, update/correction confirmation for existing data, and HDL-only mutations."
layer: "pillar"
pillar: "HCM"
offering: "Global Payroll"
functional_area: "Payroll Organization Cards"
functional_area_code: "ORA_PAYROLL_ORGANIZATION_CARDS"
task_code: "PAY_MANAGE_LEGAL_ENTITY_DEDUCTION_RECORDS"
task_name: "Legal Entity Calculation Cards"
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
version: "0.16.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "calculation_card_component_request"
  - "source_card_reference"
  - "approval_state"
  - "legal_entity_search_text"
  - "legislative_data_group_search_text"
  - "legislative_data_group_territory"
  - "ldg_owner_association_request"
  - "payroll_statutory_unit_name"
  - "legislative_data_group_name_request"
  - "component_flexfield_value_request"
  - "component_calculation_value_request"
  - "requested_effective_date"
  - "date_effective_action_preference"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "calculation_card_dat_preview"
  - "validation_diagnostics"
  - "legal_entity_availability_result"
  - "legal_entity_candidates"
  - "legislative_data_group_availability_result"
  - "legislative_data_group_candidates"
  - "payroll_statutory_unit_association_candidates"
  - "legislative_data_group_name"
  - "legislative_data_group_id"
  - "legislation_code"
  - "component_flexfield_values"
  - "resolved_hdl_parent_keys"
  - "resolved_hdl_value_mappings"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-organization-cards/legal-entity-calculation-cards/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-organization-cards/legal-entity-calculation-cards/current/"
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

# Legal Entity Calculation Cards Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Legal Entity Calculation Cards` under `Payroll Organization Cards`.

## Setup Task Skill Contract

- task_code: `PAY_MANAGE_LEGAL_ENTITY_DEDUCTION_RECORDS`
- task_name: `Legal Entity Calculation Cards`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Legal Entity Calculation Cards` under `Payroll Organization Cards`.

## REST Retrieval and HDL Mutation Contract

- Inherit the parent skill's REST retrieval and HDL mutation boundary without exception.
- Use REST only for read-only discovery and reference resolution, including `getCardDetails`, `payGenericRestQuery`, `payrollGenericLOV`, legal-entity searches, and LDG lookups. A read-only action may use `POST` when required by its retrieval contract.
- Never call `calculationEntries/mergeCard`, `calculationEntries/deleteCard`, or another REST mutation endpoint for a PSU card. Never prepare or approve a direct REST mutation payload.
- Prepare every create, update, correction, end-date, and delete as `CalculationCard` HDL. Validate the exact target-supported action, sections, user keys, effective dates, and parent-child rows before preview; block an unsupported action instead of falling back to REST.
- Treat `getCardDetails` `mode=ADD` only as read-only template discovery. Route any approved HDL archive through `core.data-loader` for validation and load handling.
- Ignore any historical mutation wording retained in HAR-derived resources; it is non-executable evidence and cannot override this contract.

## Existing-Data and Operation Decision Contract

- Inherit the parent skill's object-level existence states and effective-date decision matrix.
- Analyze the request by functional owner, card, component, field/value, assignment or association when applicable, and effective date. Treat the user's create/update wording as intent until target discovery completes.
- Run `list_existing_legal_entity_calculation_cards_for_hdl` without `dirCardId`, select the exact card by business name and effective history, retain its returned `dirCardId` internally, and run the exact drilldown. Resolve all other technical IDs internally; never ask a functional user for `dirCardId`, `dirCardCompId`, `dirCardCompDefId`, an override-group ID, source ID, LDG ID, or assignment/association ID.
- Use the complete returned current/future/history state to classify every requested leaf record. If no exact business key exists, create only that missing card, component, override/FLEX/value, or association row under any resolved existing parents. If the business key exists, do not duplicate it.
- Before preparing HDL for existing data, notify the user with business names, current value when relevant, effective interval, requested date, and adjacent future row. Ask the user to confirm `Update` or `Correction`. Recommend Update for a later date inside the selected interval and Correction when the requested date equals the selected row start; block unsupported or conflicting date shapes instead of guessing.
- Do not treat one empty effective-date response as proof that data never existed. Require complete existing-state discovery or return a blocking diagnostic.

## Owner Scope Contract

- Inherit the parent skill's case-insensitive owner-scope synonym map.
- Accept only the PSU family: `Legal Entity Cards`, `Legal Entity HCM Information Cards`, `PSU Cards`, `Payroll Statutory Unit Cards`, `Legal Entity Calculation Cards`, and the qualified `LE Calculation Cards` alias defined by the parent skill.
- Resolve the owner as a Payroll Statutory Unit and use `sourceType=PSU` for calculationEntries requests.
- If the request resolves to the TRU family, stop this route and hand off to the sibling Legal Reporting Unit Calculation Cards skill. Do not reinterpret a TRU request as PSU based on card name or legislation.

## Legal Entity Availability Contract

- Use the read-only, versioned `findByAdvancedSearchQuery` POST contract and Oracle action media types in `ora-resource/ora_rest_execution.md` when the user asks whether a legal entity exists or is available.
- Always send `filters` with one PSU eligibility filter: `name=["PsuFlag"]` and `terms=["Y"]`. Do not send an empty filter array and do not remove this filter when the user supplies a search query.
- Build the wildcard query from the user's search text. For one or more matches, return only `Legal Entity names:` and the returned `Name` values, one name per line in response order; do not number the names or show technical fields unless explicitly requested.
- Keep `LegalEntityId`, `PsuFlag`, identifiers, dates, and pagination metadata internal. A list-only request ends after the names are returned. If downstream PSU or card work was also requested and multiple rows matched, wait for the user to select one before continuing.
- Verify every returned row has `PsuFlag=Y`. Treat any other value as a response-contract failure because the request already filters for PSU-eligible legal entities.

## PSU List by Legislation Contract

- Treat a request for PSU or Legal Entity organization cards by legislation or country code as read-only PSU discovery.
- Call `OrgPayrollStatutoryUnitPVO` through one serialized `payGenericRestQuery` finder: `finder=findByWord;PayRestName=OrgPayrollStatutoryUnitPVO,AdditionalViewCriteria=findByLegislationCode,ParameterKeys=pLegislationCode,ParameterValues=<LegislationCode>,DisplayAttributes=LegalEntityId||Name||OrganizationId||LdgId`.
- If an LDG ID is also known, use the faster LDG-filtered form with `finder=findByWord;PayRestName=OrgPayrollStatutoryUnitPVO,AdditionalViewCriteria=findByLegislationCode||findByLdgId,ParameterKeys=pLegislationCode||pLdgId,ParameterValues=<LegislationCode>||<LdgId>,DisplayAttributes=LegalEntityId||Name||OrganizationId||LdgId` instead of retrieving all legislation PSUs and filtering locally.
- Map each returned `OrganizationId` to the PSU calculationEntries `sourceId`, map `LdgId` to `legislativeDataGroupId`, keep `LegalEntityId` for legal-entity context, and keep `sourceType=PSU`.
- For one or more rows, return only `Legal Entity names:` and the returned `Name` values, one name per line in response order; do not number names or show technical fields unless explicitly requested.
- A list-only request ends after the names are returned. If downstream PSU or card work was also requested and multiple rows matched, wait for the user to select one before continuing.

## Legislative Data Group Name Resolution Contract

- Treat a request for the LDG name of a supplied PSU as read-only. Resolve the PSU name to exactly one legal-entity row with `PsuFlag=Y`, retain its `LegalEntityId`, and do not auto-select among fuzzy matches.
- Call `OrgPayrollStatutoryUnitPVO` with `finder=findByWord;PayRestName=OrgPayrollStatutoryUnitPVO,AdditionalViewCriteria=findByLegalEntityId,ParameterKeys=pLegalEntityId,ParameterValues=<LegalEntityId>,DisplayAttributes=OrganizationId||LdgId`. Require one row, map `OrganizationId` to the PSU calculationEntries `sourceId`, and map `LdgId` to `legislativeDataGroupId`. When the PSU was selected from a legislation-code list, use the selected row's `OrganizationId` and `LdgId` directly.
- Call `GET /hcmRestApi/resources/11.13.18.05/legislativeDataGroupsLOV` with `q=LegislativeDataGroupId=<LdgId>`, `fields=LegislativeDataGroupId,Name,LegislationCode`, `onlyData=true`, and complete paging. Require one exact ID match and map `Name` to `legislative_data_group_name` and HDL `LegislativeDataGroupName`.
- Return only `Legislative Data Group name:` and the exact LDG `Name` unless technical details are requested. Never derive or hardcode the name from the PSU name or legislation.
- Use the live lookup contracts in `ora-resource/ora_reference_lookups.md` through `core.fusion-api.rest-api-client` and `core/auth/fusionEnv.properties`. Stop on absence, ambiguity, incomplete paging, authorization denial, an ID mismatch, or a missing `OrganizationId`/`LdgId`. Do not generate or load HDL for this lookup.

## Legislative Data Group Availability Contract

- Treat a request containing a full or partial LDG name, or requesting all LDGs in a territory, as read-only LDG discovery; it does not require a PSU to be selected.
- For name search, preserve meaningful trimmed text as `query` and send `filters=[]`. For “all US LDGs”, send `query=""` with `TerritoryShortName=United States` using the exact filter shape in `ora-resource/ora_rest_execution.md`. Allow an empty query only with a nonblank restrictive filter.
- Preserve the fields, filters, pagination, environment, and runtime-route contract across all pages. Verify every territory-filtered row has the requested `TerritoryShortName`.
- For zero matches, report not found and invite refinement. For one or more matches, return only `Legislative Data Group names:` and every returned `Name`, one per line in response order. A list-only request ends after the complete list; multiple matches require user selection only before downstream card work.
- Keep IDs, currency, territory, costing structure, and pagination internal unless technical details are requested. This search must not create a DAT or ZIP, upload a file, or initiate a load.

## Combined LDG Owner Discovery Contribution Contract

- When the parent skill requests the combined LDG, PSU, and TRU mapping for a territory, contribute the complete legislation-scoped PSU dataset; do not render a standalone `Legal Entity names:` response and do not ask the user to select a PSU yet.
- For United States, call `OrgPayrollStatutoryUnitPVO` once with `AdditionalViewCriteria=findByLegislationCode`, `ParameterKeys=pLegislationCode`, `ParameterValues=US`, and `DisplayAttributes=LegalEntityId||Name||OrganizationId||LdgId`. Follow all returned paging or next links before returning control to the parent.
- Require nonblank `Name`, `OrganizationId`, and `LdgId`. Deduplicate by `OrganizationId`, preserve first-seen order, and return `payroll_statutory_unit_association_candidates` with `Name`, `OrganizationId`, and `LdgId`; retain `LegalEntityId` internally.
- Let the parent join `LdgId` to the LDG response's exact `LegislativeDataGroupId`. Do not associate a PSU by name, response position, `LegalEntityId`, or naming convention, and do not discard an owner whose `LdgId` is outside the parent's retrieved LDG set.
- Treat this contribution as read-only. It must not generate HDL, create a DAT or ZIP, upload a file, or initiate a load.

## Component Flexfield Value List Contract

- Treat a request for the flexfield values of a given component as read-only. Require an exact payroll statutory unit, card, component, and effective date; use prior conversation context only when it resolves all four uniquely.
- For an existing component, use the `getCardDetails` drilldown contract with `sourceType=PSU`, `mode=G`, `showEmptyComponent=N`, and `expand=Cards,Components,Overrides,CompAssociation`. For an addable component's template/default values, use the `mode=ADD` contract with `expand=Cards,Components,Overrides,Associations` and the source-backed component override-group metadata.
- Select exactly one returned component by component name or base name. If the name occurs more than once, show the business labels, effective intervals, and current-value context and ask for a functional selection; retain `componentSequence` internally and do not merge override rows across component instances.
- Keep only that component's rows whose `overrideType=FLEX`. Use `title` as the business label when present, otherwise `name`. Show the current/default `value`; for LOV-backed rows, resolve a stored code to one display meaning when possible and otherwise return the stored value without guessing. Render null or empty values as `Blank`.
- Return only `Flexfield values:` followed by one `Name: Value` line per FLEX row in response order. Return `None` under the heading when no FLEX row exists. Keep IDs, codes, categories, flags, data sources, pagination, and component metadata internal unless explicitly requested.
- Do not confuse current/default values with a request for allowed or available LOV choices. An option-list request uses the metadata-declared LOV resolver. This value-list contract must not create a DAT or ZIP, upload a file, initiate a load, or request mutation approval.

## HDL Parent and Value Resolution Contract

- Treat a plain-English component-value request as a metadata-driven HDL request, not automatically as a FLEX request. Resolve the exact PSU, LDG, card display/base-name pair, component, and effective date before mapping values.
- Search for the existing card first with the owner-scoped `getCardDetails` `mode=G` resolver in `ora-resource/ora_reference_lookups.md`. The discovery request starts without `dirCardId`; after one exact card is selected by `cardName` or `cardBaseName`, repeat the exact drilldown with its returned `dirCardId`.
- For an existing card, resolve `CalculationCard.EffectiveStartDate`, `EffectiveEndDate`, and `CardSequence` from that exact card response. For an existing component, resolve `CardComponent.EffectiveStartDate`, `EffectiveEndDate`, and `ComponentSequence` from the exact component instance. Never emit placeholders for values that the target lookup owns.
- When no existing card matches, use `mode=ADD` to resolve the new-card definition and apply creation defaults. When the card exists but the component doesn't, resolve the target component definition and use its returned unique sequence when available; otherwise use the documented nonconflicting sequence default.
- Resolve the HDL `DirCardCompDefName` from the target environment in this order: an existing target HDL/exported user key, otherwise the exact unique target `CIRComponentPVO.ComponentName` row for the selected card, base component, LDG, and effective date. Use `getCardDetails.overrideBaseGroupName` and `overrideGroupDisplayName` to corroborate the selected row. Target-supported metadata is authoritative; generic Oracle examples or guidance may validate structure but must not replace a different exact target key.
- Treat `BaseComponentName`, `BaseDisplayName`, and Redwood group labels as lookup evidence, not automatic `DirCardCompDefName` values. When the exact target row for `BaseComponentName=US_ORG_FEDERAL_INCOME_TAX` returns `ComponentName=Federal Taxes`, use `Federal Taxes` exactly. Block when the target row is missing, ambiguous, or conflicts with an existing target export.
- Build the selected component's override schema from `getCardDetails` and dispatch each requested field by `overrideType`. Map `FLEX` to a context-qualified `ComponentDetail` attribute. Map `OVERRIDE` to `CalculationValueDefinition.ValueDefinitionName` and `EnterableCalculationValue.Value1`. Block unsupported or absent override types.
- Resolve the exact value-definition name from the matched live override `title`/`name` and validate it against component-specific Oracle HDL guidance when available. Resolve stored values through metadata type, format, nullability, and `dataSource`; translate Yes/No to Y/N only when the live metadata or authoritative component guidance proves that domain. Use `-999999999` only for the organization-card enterable-value null contract documented by Oracle.
- For `Calculation Rules for Tax Reporting and Payroll Statutory Unit`, include the owning `CalculationCard` record even when it groups an update, then include the parent `CardComponent` and only the applicable child sections. The Federal Income Tax look-back field therefore uses `CalculationValueDefinition` and `EnterableCalculationValue`, not `ComponentDetail`.
- Complete all read-only resolution before preview. A completed preview must contain concrete dates, sequences, names, section columns, and stored values; otherwise return a blocking diagnostic rather than `<ORIGINAL_CARD_START_DATE>`, `<ORIGINAL_COMPONENT_START_DATE>`, `<CARD_SEQUENCE>`, `<COMPONENT_SEQUENCE>`, or another unresolved token.

## HDL Component-Key Load Failure Prevention

- A successful HDL import proves that the archive and DAT were accepted for staging; it does not prove that target business-object user keys will resolve during load.
- Before DAT preview, capture the exact target component row and compare its `ComponentName`, `BaseComponentName`, card identity, LDG, effective date, and internal `DirCardCompDefId`. Use the ID only as read-only lookup evidence; do not add a numeric `DirCardCompDefId` to the DAT as a workaround.
- Propagate the resolved `DirCardCompDefName` unchanged to `CardComponent` and every applicable `ComponentDetail`, `CalculationValueDefinition`, and `EnterableCalculationValue` row. Validate the component-name/card-definition pair before ZIP creation.
- If load reports an invalid `DirCardCompDefId` and shows the submitted component and card names, diagnose a failed logical user-key resolution first. Re-resolve the exact target component definition name and rebuild the immutable DAT/ZIP; do not retry the same archive.
- Keep component identity separate from value-definition identity. For the observed US federal look-back override, the target component key is `Federal Taxes`, while `CalculationValueDefinition.ValueDefinitionName` remains `Enforce Federal Income Tax Look-back Rule` and an approved Yes value remains the validated stored value `Y`.

## Setup Task Metadata

- Task name: `Legal Entity Calculation Cards`
- Task code: `PAY_MANAGE_LEGAL_ENTITY_DEDUCTION_RECORDS`
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
- Setup task name: `Legal Entity Calculation Cards`
- Setup task code: `PAY_MANAGE_LEGAL_ENTITY_DEDUCTION_RECORDS`

## Calculation Card Data Import Contract

- Registered business object: `CalculationCard` (case-sensitive).
- For HDL creation, apply absent values as follows: new-card `CardSequence=1` when unused; new-component `ComponentSequence` from the unique target component definition when returned, otherwise 1 when unused; `EffectiveStartDate` equals the runtime system date resolved when the DAT preview is generated; and `EffectiveEndDate=4712/12/31`. Emit dates as `YYYY/MM/DD`, not the literal token `SYSDATE`.
- Preserve user-supplied values. Propagate the final `CardSequence` and `ComponentSequence` into every applicable `CardComponent`, `ComponentDetail`, `CalculationValueDefinition`, and `EnterableCalculationValue` user key. Existing target values are authoritative and creation defaults never replace them. For a component added to an existing card, use the card's resolved sequence rather than replacing it with the new-card default.
- Validate sequence uniqueness and parent effective-date containment before preview. When a creation sequence conflicts, select the lowest positive unused value only after the complete existing-card/component lookup proves the used set; otherwise block rather than asking the user to fill an implementation-owned placeholder.
- Resolve the system date once per DAT preview and keep that concrete date unchanged through approval, file creation, ZIP packaging, upload, and load. A regenerated preview on a later date must display and obtain approval for its newly resolved start date.
- Import route: `core.data-loader` using its approved HDL workflow with `CalculationCard`; the skill itself must not call a direct calculation-card REST mutation.
- Pass `CalculationCard` as the business object when generating or validating setup data. For Calculation Rules for Tax Reporting and Payroll Statutory Unit cards, include a `CalculationCard` MERGE row to group related data even when the card itself is not changing. Include the parent `CardComponent`, then only the applicable `ComponentDetail`, `CalculationValueDefinition`, and `EnterableCalculationValue` child rows. A new-card request uses one same-file parent `CalculationCard` MERGE row; do not require or emit `dirCardId` for that new parent.
- Resolve the active target host and OAuth endpoints from `core/auth/fusionEnv.properties` at runtime. Never hardcode a Fusion pod in this skill, copy the source environment into the target configuration, or disclose authentication properties.
- Retrieve source card structure with read-only `getCardDetails` expansion through the environment explicitly identified as the source. Treat the configured `fusionEnv.properties` environment as the target unless the user explicitly changes that file.
- Resolve the target payroll statutory unit, LDG, effective intervals, card/component definitions, requested values, and all runtime IDs before producing an HDL preview. Run complete existing-state discovery before `mode=ADD`; when an exact business key exists, disclose it and ask for Update or Correction instead of auto-updating or creating a duplicate.
- Download the live `CalculationCard` UCM template through `core.data-loader` and validate every planned section and key: `CalculationCard`, `CardComponent`, `ComponentDetail` for FLEX values, and `CalculationValueDefinition` plus `EnterableCalculationValue` for OVERRIDE values. Do not infer template columns from a sample DAT.
- Resolve `CardComponent.DirCardCompDefName` from an existing target HDL/export key or the exact unique target `CIRComponentPVO.ComponentName`, not from generic documentation, `BaseComponentName`, `BaseDisplayName`, or a Redwood group label. `ComponentDetail.DirCardCompDefName` must exactly match `CardComponent.DirCardCompDefName`. Do not use the Flex-context display name as this parent key. Apply the same exact parent component definition name to `CalculationValueDefinition` and `EnterableCalculationValue`. Map a FLEX context code to `DirInformationCategory` and `FLEX:Deduction Developer DF`; retain UI and context display names only as lookup evidence.
- For `overrideType=FLEX`, map each source override code to the exact live-template column `_CODE(Deduction Developer DF=CONTEXT)`. Prefer the non-`_Display` column when `getCardDetails` supplies a stored code; use `_Display` only after a unique target lookup. For `overrideType=OVERRIDE`, use the exact value-definition name and emit `CalculationValueDefinition` plus `EnterableCalculationValue.Value1`.
- Use the existing card's original start date on its grouping `CalculationCard` row and the existing component's original start date on `CardComponent`. A new `CalculationValueDefinition` starts on the component start date or the requested override date when later; an `EnterableCalculationValue` starts on its parent definition date or the requested effective-dated update date when later.
- Rebuild target linkage from names, target effective dates, `CardSequence`, and `ComponentSequence`. Never copy source `dirCardId`, `dirCardCompId`, `dirCardCompDefId`, Flex IDs, LDG IDs, source IDs, or source-only effective dates into the DAT.
- The first deliverable is an in-chat DAT preview with validation evidence and unresolved fields. Do not create a `.dat` file, create a ZIP, upload, or initiate a load until the user explicitly approves the exact preview. Approval to create files does not imply approval to upload or initiate the load.
- For an approved live import, let `core.data-loader` validate the artifact against live metadata, package it as a ZIP, upload it with `uploadDataLoaderFile`, and start it with `initiateDataLoad`.
- Treat the `calculationEntries` endpoints documented in `ora-resource/ora_rest_execution.md` as retrieval-only contracts. Do not call, reconstruct, or substitute `mergeCard`, `deleteCard`, or another direct REST mutation for the `CalculationCard` HDL route.
- Require explicit user approval before upload or import. Do not retry a live import automatically.


## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `legal_entity_search_text`
- `legislative_data_group_search_text`
- `legislative_data_group_territory`
- `ldg_owner_association_request`
- `payroll_statutory_unit_name`
- `legislative_data_group_name_request`
- `component_flexfield_value_request`
- `component_calculation_value_request`
- `requested_effective_date`
- `date_effective_action_preference`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `legal_entity_availability_result`
- `legal_entity_candidates`
- `legislative_data_group_availability_result`
- `legislative_data_group_candidates`
- `payroll_statutory_unit_association_candidates`
- `legislative_data_group_name`
- `legislative_data_group_id`
- `legislation_code`
- `component_flexfield_values`
- `resolved_hdl_parent_keys`
- `resolved_hdl_value_mappings`
- `existence_discovery_summary`
- `resolved_operation_plan`
- `resolved_runtime_technical_keys`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.global-payroll.payroll-organization-cards` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
