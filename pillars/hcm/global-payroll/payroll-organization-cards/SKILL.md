---
skill_id: "hcm.global-payroll.payroll-organization-cards"
name: "Payroll Organization Cards Implementation Guidance"
description: "Provides HCM Global Payroll implementation guidance for Payroll Organization Cards, including read-only REST discovery, automatic technical-key resolution, object-level create-versus-date-effective-update classification, update-versus-correction confirmation for existing data, and HDL-only calculation-card mutations."
layer: "pillar"
pillar: "HCM"
offering: "Global Payroll"
functional_area: "Payroll Organization Cards"
functional_area_code: "ORA_PAYROLL_ORGANIZATION_CARDS"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global payroll pillar team"
version: "0.16.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "payroll_organization_cards_scope"
  - "payroll_organization_cards_requirements"
  - "legal_entity_search_text"
  - "legal_reporting_unit_search_text"
  - "legislative_data_group_search_text"
  - "legislative_data_group_territory"
  - "ldg_owner_association_request"
  - "organization_card_owner_name"
  - "legislative_data_group_name_request"
  - "component_flexfield_value_request"
  - "component_calculation_value_request"
  - "requested_effective_date"
  - "date_effective_action_preference"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "owner_scope_resolution"
  - "source_type"
  - "nested_task_route"
  - "legal_entity_availability_result"
  - "legal_entity_candidates"
  - "legal_reporting_availability_result"
  - "legal_reporting_candidates"
  - "legislative_data_group_availability_result"
  - "legislative_data_group_candidates"
  - "legislative_data_group_owner_associations"
  - "legislative_data_group_name"
  - "legislative_data_group_id"
  - "legislation_code"
  - "component_flexfield_values"
  - "calculation_card_dat_preview"
  - "existence_discovery_summary"
  - "resolved_operation_plan"
  - "resolved_runtime_technical_keys"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
uses_core:
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-organization-cards/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-organization-cards/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-organization-cards/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "PAY_MANAGE_LEGAL_ENTITY_DEDUCTION_RECORDS"
  - "PAY_MANAGE_LEGAL_REPORTING_UNIT_DEDUCTION_RECORDS"
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

# Payroll Organization Cards Implementation Guidance

## Purpose

Provides HCM Payroll implementation guidance for the Payroll Organization Cards functional area.

## When to Use

Use this functional-area skill after Payroll scope is confirmed and the project needs payroll organization cards setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Global Payroll` (`ORA_GLOBAL_PAYROLL`)
- Functional area / Setup Object: `Payroll Organization Cards` (`ORA_PAYROLL_ORGANIZATION_CARDS`)

## Setup Tasks

1. [Legal Entity Calculation Cards](legal-entity-calculation-cards/SKILL.md) (`PAY_MANAGE_LEGAL_ENTITY_DEDUCTION_RECORDS`)
2. [Legal Reporting Unit Calculation Cards](legal-reporting-unit-calculation-cards/SKILL.md) (`PAY_MANAGE_LEGAL_REPORTING_UNIT_DEDUCTION_RECORDS`)

## REST Retrieval and HDL Mutation Boundary

Apply this boundary before selecting any calculation-card operation:

1. Use REST APIs only to fetch or retrieve owner, LDG, card, component, override, LOV, template, status, or other reference data. A REST action implemented as `POST` is permitted only when its documented behavior is read-only retrieval and it creates no Fusion business data.
2. Never call `calculationEntries/mergeCard`, `calculationEntries/deleteCard`, or any other direct REST create, update, correct, end-date, or delete operation. Never construct, preview, approve, retry, or execute their mutation payloads.
3. Use the `CalculationCard` HDL business object for every create, update, correction, end-date, and delete request. Select only target-template-supported HDL sections and actions; if current target metadata does not prove the requested delete or date-effective action, block instead of falling back to REST.
4. Treat `getCardDetails` `mode=ADD` as read-only definition and default-value retrieval. It does not authorize or perform card creation.
5. Route approved HDL validation, DAT/ZIP preparation, upload, and load initiation exclusively through `core.data-loader`. Loader transport APIs may carry the approved HDL archive, but they must not be replaced by a direct Calculation Cards REST mutation.
6. This boundary overrides every historical HAR-derived `mergeCard`, `deleteCard`, mutation-payload, or live-REST-write instruction in the nested skills and their `ora-resource` files. Treat such evidence as non-executable and follow the HDL route.

## Automatic Existence and Operation Resolution

Determine the operation from target state rather than trusting verbs such as “add,” “set,” “change,” or “update” in isolation.

1. Parse the functional request into the owner, LDG, card, component, requested override/FLEX/value, assignment or association when applicable, other related transactional row, and requested effective date. Ask only for missing business information.
2. Resolve runtime technical identifiers automatically through read-only retrieval. Start with the functional owner and card name, run owner-scoped existing-card discovery without `dirCardId`, retain the uniquely returned `dirCardId`, and use it internally for exact card/component/history drilldown. Resolve `dirCardCompId`, `dirCardCompDefId`, definition IDs, override-group IDs, source IDs, LDG IDs, sequences, and assignment/association identifiers the same way. Never require a functional user to provide a technical identifier; when matches are ambiguous, show business names, effective intervals, current values, or assignment labels and ask the user to select by those business details.
3. Build an object-level existence graph for the requested path: card, component, override or FLEX row, calculation-value definition/value, assignment or association, and any source-backed related transactional row. Search current, future, and historical effective-dated rows by their complete business key. A failed, partial, single-date, or unauthorized lookup does not prove absence.
4. Classify each requested object independently:
   - `CREATE`: no matching business-key row exists in a complete target lookup. Create only the missing object and reuse resolved existing ancestors.
   - `EXISTING_AT_DATE`: one matching row contains the requested effective date.
   - `EXISTS_OUTSIDE_DATE`: matching history or a future row exists, but no row contains the requested date.
   - `AMBIGUOUS`: multiple rows remain after business-key matching; stop for a business discriminator.
5. When every requested leaf object is `CREATE`, state that no existing matching leaf data was found and proceed with an HDL create preview. Report and reuse any existing ancestor card or component, but do not ask for Update or Correction for an ancestor that the request does not change.
6. When any requested target business key is `EXISTING_AT_DATE` or `EXISTS_OUTSIDE_DATE`, notify the user before generating a DAT. Show business names, current value when relevant, the selected effective interval, the requested date, and any adjacent future interval; keep technical IDs internal. Ask the user to confirm one supported date-effective choice:
   - `Update`: preserve prior history and start a new effective-dated slice on the requested date. Recommend this when the requested date is later than the selected row's start and falls within its interval.
   - `Correction`: change the selected existing slice without creating a new effective-dated slice. Recommend this when the requested date equals the selected row's start, or when the user intends to fix the whole selected slice.
7. If the requested date is before the first row, in a history gap, after an end date, or conflicts with a future row, show the relevant intervals and offer only actions proven by the live `CalculationCard` HDL contract. Never convert an existing business key into a duplicate create merely because no row is active on one date.
8. Treat an operation word in the original request as a provisional preference. Existing-data disclosure and confirmation remain mandatory; after confirmation, freeze the resolved per-object action and effective date in the exact DAT preview.

## Owner Scope Routing

Resolve the organization-card owner before resolving IDs, retrieving cards, generating HDL, or selecting a nested task. Normalize the supplied scope phrase case-insensitively by trimming it and collapsing repeated whitespace, then apply this exact synonym map:

| Owner scope | Recognized user terminology | REST `sourceType` | Nested task route |
|---|---|---|---|
| Payroll Statutory Unit | `Legal Entity Cards`; `Legal Entity HCM Information Cards`; `PSU Cards`; `Payroll Statutory Unit Cards`; `Legal Entity Calculation Cards`; `LE Calculation Cards` when `LE` is explicitly defined or clearly qualified as Legal Entity | `PSU` | `legal-entity-calculation-cards` (`PAY_MANAGE_LEGAL_ENTITY_DEDUCTION_RECORDS`) |
| Tax Reporting Unit | `Legal Reporting Cards`; `Legal Reporting Unit HCM Information`; `TRU Cards`; `Tax Reporting Unit Cards`; `Legal Reporting Unit Calculation Cards` | `TRU` | `legal-reporting-unit-calculation-cards` (`PAY_MANAGE_LEGAL_REPORTING_UNIT_DEDUCTION_RECORDS`) |

Apply these routing rules:

1. Treat a match from only the PSU row as `sourceType=PSU` and route to the Legal Entity Calculation Cards nested skill.
2. Treat a match from only the TRU row as `sourceType=TRU` and route to the Legal Reporting Unit Calculation Cards nested skill.
3. Treat these phrases as task and owner-scope synonyms, not as calculation-card definition names. A card name such as `Employer Gratuity Details` does not by itself establish PSU or TRU scope.
4. Verify the resolved owner and returned `sourceType` before preview or execution. Never change PSU to TRU, or TRU to PSU, merely because a lookup returns a card with a similar name.
5. If both scope families are present, or neither family can be determined from the request, task context, or an explicit owner type, stop and ask the user to identify PSU or TRU. Do not guess from the legislation, LDG, legal-entity name, reporting-unit name, or card definition.
6. Treat `LE calculation card`, `LE calculation card data`, and an explicit statement that `LE means Legal Entity` as PSU-family intent. Do not expand a bare or unrelated `LE` abbreviation without that calculation-card context or explicit definition.

## Legal Entity Availability

When a user asks whether a legal entity is available, classify the request as a read-only PSU discovery operation and use the Legal Entity Calculation Cards nested skill's `findByAdvancedSearchQuery` contract.

1. Require nonblank legal-entity name or identifier search text.
2. Convert whitespace-separated search terms into a contains query by joining them with `%` and adding leading and trailing `%`; for example, `SA Regression` becomes `%SA%Regression%`.
3. Send a `POST` to the versioned standard resource path with the Oracle action request and response media types documented in `legal-entity-calculation-cards/ora-resource/ora_rest_execution.md`. Always include a `filters` entry whose `name` is `["PsuFlag"]` and whose `terms` is `["Y"]`, so the search returns only PSU-eligible legal entities. Route it through `core.fusion-api.rest-api-client` using the active environment from `core/auth/fusionEnv.properties`.
4. Return a clear “not found” response for zero matches. For one or more matches, return only the heading `Legal Entity names:` followed by each returned `Name` on its own line in response order. Do not number the names or display IDs, identifiers, flags, parent organizations, dates, counts, offsets, or pagination details unless the user explicitly requests them.
5. Retain `LegalEntityId`, `PsuFlag`, and other response fields internally for validation and downstream routing. Verify defensively that every returned item still has `PsuFlag=Y`; a different value is a response-contract failure because the request already filters for PSU rows. If the request also asks for card work and multiple entities match, stop after the names-only list and wait for the user to select one; a list-only request is complete after returning the names.
6. Treat this operation as read-only: it requires no mutation approval and must not create a DAT, ZIP, upload, or load.

## PSU List by Legislation

When a user asks for PSU or Legal Entity organization cards by legislation or country code, classify the request as a read-only PSU discovery operation and use the Legal Entity Calculation Cards nested skill's `OrgPayrollStatutoryUnitPVO` legislation-code contract.

1. Require a nonblank legislation or country code and normalize it to the Fusion legislation code expected by the caller, such as `US`.
2. Send all `payGenericRestQuery` finder inputs as one `finder` query parameter: begin with `finder=findByWord;`, then separate `PayRestName`, `AdditionalViewCriteria`, `ParameterKeys`, `ParameterValues`, and `DisplayAttributes` with commas. Do not send those inputs as separate URL query parameters. For a URL, percent-encode each `||` value separator as `%7C%7C`.
3. If an LDG ID is also known, use `finder=findByWord;PayRestName=OrgPayrollStatutoryUnitPVO,AdditionalViewCriteria=findByLegislationCode||findByLdgId,ParameterKeys=pLegislationCode||pLdgId,ParameterValues=<LegislationCode>||<LdgId>,DisplayAttributes=LegalEntityId||Name||OrganizationId||LdgId`. Use this LDG-filtered resolver instead of retrieving all legislation PSUs and filtering locally.
4. If no LDG ID is known, use `finder=findByWord;PayRestName=OrgPayrollStatutoryUnitPVO,AdditionalViewCriteria=findByLegislationCode,ParameterKeys=pLegislationCode,ParameterValues=<LegislationCode>,DisplayAttributes=LegalEntityId||Name||OrganizationId||LdgId`.
5. Treat each returned row as a PSU candidate. Retain `LegalEntityId`, `OrganizationId`, and `LdgId` internally; map `OrganizationId` to calculationEntries `sourceId`, `LdgId` to `legislativeDataGroupId`, and keep `sourceType=PSU` for downstream card work.
6. For a list-only request, return only `Legal Entity names:` followed by each returned `Name` on its own line in response order. Do not number the names or display IDs unless the user explicitly requests technical details.
7. If downstream card work is also requested and multiple PSUs are returned, stop after the names-only list and wait for the user to select one.
8. Treat this operation as read-only: it requires no mutation approval and must not create a DAT, ZIP, upload, or load.

## Legal Reporting Unit Availability

When a user asks whether a legal reporting unit or legal reporting is available, classify the request as a read-only TRU discovery operation and use the Legal Reporting Unit Calculation Cards nested skill's `findByAdvancedSearchQuery` contract.

1. Require nonblank legal-reporting-unit name or registration-number search text.
2. Preserve the trimmed search text as the `query` value, including underscores and any explicit user-supplied `%` wildcards. For example, `ZHRX_France_Reg_OrgQA` remains `ZHRX_France_Reg_OrgQA`.
3. Send a `POST` with the JSON request body documented in `legal-reporting-unit-calculation-cards/ora-resource/ora_rest_execution.md` through `core.fusion-api.rest-api-client`, using the active environment from `core/auth/fusionEnv.properties`.
4. Return a clear “not found” response for zero matches. For one or more matches, return only the heading `Legal Reporting Unit names:` followed by each returned `Name` on its own line in response order. Do not number the names or display IDs, registration values, flags, parent organizations, dates, counts, offsets, or pagination details unless the user explicitly requests them.
5. Retain `EstablishmentId`, `TruStatus`, and other response fields internally for validation and downstream routing. Treat `TruStatus=A` as the active TRU marker. If the request also asks for card work and multiple reporting units match, stop after the names-only list and wait for the user to select one; a list-only request is complete after returning the names.
6. Treat this POST as a read-only search: it requires no mutation approval and must not create a DAT, ZIP, upload, or load.

## Legislative Data Group Name Resolution

When a user supplies an exact PSU or TRU name and asks for its Legislative Data Group, classify the request as a read-only owner-to-LDG lookup and route it to the matching nested skill.

1. Resolve exactly one owner before looking up the LDG. For PSU scope, use the legal-entity availability contract, require `PsuFlag=Y`, and retain the selected `LegalEntityId`. For TRU scope, use the legal-reporting-unit availability contract, require the selected active TRU, and retain its `EstablishmentId`. Do not select the first fuzzy match.
2. For PSU scope by selected legal entity, call `OrgPayrollStatutoryUnitPVO` with `finder=findByWord;PayRestName=OrgPayrollStatutoryUnitPVO,AdditionalViewCriteria=findByLegalEntityId,ParameterKeys=pLegalEntityId,ParameterValues=<LegalEntityId>,DisplayAttributes=OrganizationId||LdgId` and map its one returned `OrganizationId` to `sourceId` and `LdgId` to `legislativeDataGroupId`. For PSU scope by legislation or country code, use the same single-finder serialization described above. Select exactly one returned PSU before downstream card work. For TRU scope, call `OrgTaxReportingUnitPVO` with the same single-finder serialization and `AdditionalViewCriteria=findByEstablishmentId`, then apply the mappings with `sourceType=TRU`.
3. Pass the returned `LdgId` unchanged to `GET /hcmRestApi/resources/11.13.18.05/legislativeDataGroupsLOV` using the exact query `q=LegislativeDataGroupId=<LdgId>`, request `LegislativeDataGroupId,Name,LegislationCode`, set `onlyData=true`, and follow paging through `hasMore=false`.
4. Require exactly one accessible row whose `LegislativeDataGroupId` equals the supplied `LdgId`. Map `Name` to `legislative_data_group_name` and HDL `LegislativeDataGroupName`; retain `LegislationCode` and the ID for downstream lookups. Never derive the LDG name from the owner name, legislation, or naming conventions.
5. Return `Legislative Data Group name:` followed by the exact `Name`. Keep IDs and legislation internal unless the user explicitly requests technical details. Treat zero rows, multiple rows, an ID mismatch, incomplete paging, or authorization denial as a blocking lookup failure.
6. Route every call through `core.fusion-api.rest-api-client` using `core/auth/fusionEnv.properties`. This workflow is read-only and must not create a DAT or ZIP, upload a file, or initiate a load.

## Legislative Data Group Availability by Name or Territory

When a user supplies a full or partial Legislative Data Group name, or asks for every LDG in a territory, classify the request as a read-only LDG discovery operation. This search is independent of PSU/TRU owner resolution and is different from resolving one LDG by ID after an owner has been selected.

1. For full or partial name search, require meaningful nonblank text, preserve the trimmed text exactly as `query`, use `filters=[]`, and reject blank or all-`%` input. Do not add wildcard characters.
2. For the request “all US LDGs”, normalize `US` or `United States` case-insensitively to the Fusion territory display value `United States`. Send `query=""` and exactly one filter object with `name=["TerritoryShortName"]` and `terms=["United States"]`. Do not reinterpret `US` as an LDG-name fragment in this territory-scoped wording.
3. Permit an empty `query` only when at least one source-backed restrictive filter contains a nonblank term. Reject an empty query with `filters=[]`, a blank filter term, or an unsupported territory mapping. For territories other than the documented United States mapping, require the exact Fusion `TerritoryShortName` or a source-backed resolver before execution.
4. Send a `POST` to the runtime-routed `legislativeDataGroups/action/findByAdvancedSearchQuery` action using the JSON body documented in both nested skills' `ora-resource/ora_rest_execution.md`. In both modes use `limit="500"`, `offset=0`, `searchFields=["Name"]`, and request `Name`, `CurrencyName`, `TerritoryShortName`, `CostAllocationStructureName`, and `LegislativeDataGroupId`.
5. Resolve the Fusion host and environment-specific `rv:` route identifier at runtime through `core.fusion-api.rest-api-client` and `core/auth/fusionEnv.properties`. Never persist or reuse the example hostname or captured route identifier from another environment.
6. Follow `result.summary[0].hasMore` until false, advancing `offset` while preserving the same query, fields, and filters. Deduplicate by `LegislativeDataGroupId` and preserve first-seen response order. For territory mode, verify every returned `TerritoryShortName` equals the requested normalized territory; treat any mismatch as a response-contract failure.
7. For zero matches, clearly state that no Legislative Data Group matched the supplied name or territory and invite refinement. For one or more matches, return only `Legislative Data Group names:` followed by every returned `Name`, one name per line in response order. Do not number the names or display IDs, currency, territory, costing structure, counts, offsets, or pagination unless the user explicitly requests details.
8. Retain `LegislativeDataGroupId`, territory, currency, and costing structure internally for validation and downstream work. If downstream card work was also requested and multiple LDGs match, stop after the complete names-only list and wait for the user to select one. A list-only request is complete after returning the names.
9. Treat this POST as a read-only search: it requires no mutation approval and must not create a DAT or ZIP, upload a file, or initiate a load.

## Combined LDG, PSU, and TRU Discovery

When a user asks for all LDGs in a territory together with their associated PSUs and TRUs, classify the request as one read-only combined discovery workflow. A prompt such as “I need to add LE calculation card data for one of the US LDGs; list all US LDGs and the PSUs and TRUs associated” triggers this workflow. The mention of future card creation does not authorize HDL generation or any mutation.

1. Normalize the territory and legislation independently. For `US` or `United States`, use `TerritoryShortName=United States` for the LDG search and `pLegislationCode=US` for both owner searches. Require source-backed mappings for other country or territory phrases.
2. Retrieve three complete paged datasets through `core.fusion-api.rest-api-client` and the active `core/auth/fusionEnv.properties` environment:
   - LDGs: use the territory-mode `legislativeDataGroups/action/findByAdvancedSearchQuery` POST contract, retaining `Name`, `TerritoryShortName`, and `LegislativeDataGroupId`.
   - PSUs: use one legislation-scoped `OrgPayrollStatutoryUnitPVO` finder with `AdditionalViewCriteria=findByLegislationCode`, `ParameterKeys=pLegislationCode`, `ParameterValues=US`, and `DisplayAttributes=LegalEntityId||Name||OrganizationId||LdgId`.
   - TRUs: use one legislation-scoped `OrgTaxReportingUnitPVO` finder with `AdditionalViewCriteria=findByLegislationCode`, `ParameterKeys=pLegislationCode`, `ParameterValues=US`, and `DisplayAttributes=PsuId||Name||OrganizationId||LdgId`. Retain `PsuId` as the parent PSU reference.
3. Do not issue one PSU call and one TRU call per LDG. Fetch each legislation-scoped owner dataset once, follow every response's paging or next-link contract to completion, and then group the results locally.
4. Deduplicate LDGs by `LegislativeDataGroupId`; deduplicate PSU rows and TRU rows separately by `OrganizationId`. Preserve first-seen LDG order and first-seen owner order.
5. Join only by exact ID equality after normalizing numeric IDs to a common string representation: `LDG.LegislativeDataGroupId = PSU.LdgId` and `LDG.LegislativeDataGroupId = TRU.LdgId`. Never associate an owner by name similarity, naming convention, response position, PSU `LegalEntityId`, TRU `PsuId`, or `OrganizationId`.
6. Require nonblank `Name` and identity fields on every row used in the result. Verify every LDG has the requested territory, every PSU/TRU `LdgId` belongs to the retrieved territory LDG set, and every nonblank TRU `PsuId` matches a retrieved PSU `OrganizationId` in the same LDG. Treat a missing required field, territory mismatch, incomplete page set, orphan owner `LdgId`, or mismatched TRU parent PSU as a blocking Fusion API/source-contract failure; do not silently omit the row or present a partial mapping as complete.
7. Return the complete grouped result in LDG response order using this user-facing format. Show names only unless technical details are requested:

   ```text
   Legislative Data Groups with associated PSUs and TRUs:

   <LDG Name>
   PSUs:
   <PSU Name, one per line, or None>
   TRUs:
   <TRU Name, one per line, or None>
   ```

8. Treat multiple LDGs as the expected result, not an ambiguity. Finish the complete mapping before asking for a choice. If the prompt also requests Legal Entity card creation, ask the user to select one LDG and one associated PSU only after the mapping is shown; do not ask for a TRU for PSU-scoped Legal Entity card work.
9. This workflow must not generate a DAT or ZIP, upload a file, initiate a load, or request mutation approval.

## Component Flexfield Value List

When a user asks for the flexfield values for a given component, classify the request as a read-only current-value lookup and route it by the already resolved owner scope.

1. Require one exact owner, calculation card, component, and effective date. Reuse the current conversation selection only when each value is unambiguous; otherwise ask for the missing selection.
2. Route `sourceType=PSU` to the Legal Entity Calculation Cards nested skill and `sourceType=TRU` to the Legal Reporting Unit Calculation Cards nested skill.
3. For a component that already exists on the card, retrieve the selected card with `getCardDetails` using `mode=G`, `showEmptyComponent=N`, and `expand=Cards,Components,Overrides,CompAssociation`. For an addable component whose template/default values are requested, use the nested skill's `mode=ADD` template contract instead.
4. Select exactly one component by its returned name or base name. When repeated component names exist, show their business labels, effective intervals, and current-value context and ask the user to select one; retain `componentSequence` internally and do not combine rows from different components.
5. From the selected component only, keep override rows whose `overrideType=FLEX`. Use the business label and current/default value. For an LOV-backed value, resolve a stored code to one display meaning when possible; if it cannot be resolved uniquely, return the stored value without guessing. Render null or empty values as `Blank`.
6. Return only the heading `Flexfield values:` followed by one `Name: Value` line per FLEX row in response order. If there are no FLEX rows, return `Flexfield values:` followed by `None`. Do not display IDs, codes, categories, flags, data sources, pagination, or component metadata unless the user explicitly requests technical details.
7. Treat “flexfield values” as the component's current/default values. If the user asks which values are allowed or available for one field, run the nested skill's LOV option-list contract instead; do not silently substitute an allowed-values list for current values.
8. This lookup requires no mutation approval and must not generate a DAT or ZIP, upload a file, or initiate a load.

## HDL Card and Component Creation Defaults

Apply these defaults only when generating an HDL preview for a new calculation card or card component and the user has not supplied the corresponding value:

| HDL field | Default | Application rule |
|---|---|---|
| `CardSequence` | `1` | Default a new `CalculationCard` to 1 when unused. Propagate the resolved value to every `CardComponent`, `ComponentDetail`, `CalculationValueDefinition`, and `EnterableCalculationValue`; an existing card's returned sequence is authoritative |
| `ComponentSequence` | `1` | Default a new component to 1 when unused, or use the target component definition's unique sequence when returned. Propagate the resolved value to every child record; an existing component's returned sequence is authoritative |
| `EffectiveStartDate` | Runtime system date (`sysdate`) | Resolve the date once when the exact DAT preview is generated and emit it as `YYYY/MM/DD`; never emit the literal text `SYSDATE` |
| `EffectiveEndDate` | `4712/12/31` | Apply to a new card when absent; for a new child, use the earlier of this date and the resolved parent end date |

Preserve every explicit user value. For an existing card or component, do not apply creation defaults: retrieve the original `EffectiveStartDate`, current `EffectiveEndDate`, `CardSequence`, and `ComponentSequence` from the exact target instance. For a new row, use sequence 1 when it is free; if it conflicts, select the lowest positive unused sequence only after a complete target lookup proves the used set. Otherwise block rather than exposing a placeholder. Freeze the resolved system date in the approved preview; if the preview is regenerated on a later date, show the new resolved date and require approval of that new preview.

## HDL Parent-Key and Calculation-Value Resolution

Route PSU and TRU requests to the matching nested skill and require it to return a complete preview without unresolved HDL key placeholders.

1. Resolve the exact owner, LDG, card definition, card display/base-name pair, and requested effective date.
2. Search existing cards before using add mode. If one exact card exists, carry its original start date, current end date, and `CardSequence`; otherwise resolve a new-card definition and creation defaults.
3. Search the selected card's complete component history. If the intended component exists, carry its original start date, current end date, and `ComponentSequence` internally, disclose the matching interval and current value, and ask the user to confirm Update or Correction. If it does not exist across complete history, classify only that component as CREATE, resolve its definition and a nonconflicting creation sequence, and reuse the existing card.
4. Resolve `DirCardCompDefName` from the HDL component definition or component-specific Oracle HDL guidance. Do not use a component-group or UI display label merely because it selected the component in Redwood.
5. Dispatch every selected `getCardDetails` override independently. Use `ComponentDetail` only for `overrideType=FLEX`. Use a `CalculationValueDefinition` plus `EnterableCalculationValue` pair for `overrideType=OVERRIDE`. Block an unknown type instead of forcing it into a DFF column.
6. Resolve stored values from live metadata: apply type, format, nullability, and metadata-declared LOV rules; translate business display text to one stored code only when the target metadata or authoritative component guidance proves the mapping. Preserve the organization-card null sentinel required by current Oracle HDL guidance.
7. Include every parent row required by the component-specific Oracle HDL contract. For Calculation Rules for Tax Reporting and Payroll Statutory Unit cards, include the owning `CalculationCard` and `CardComponent` rows even when only a child override is being updated.
8. Keep the result in chat until the exact `METADATA` and `MERGE` lines are approved. Do not emit `<ORIGINAL_*_DATE>`, `<CARD_SEQUENCE>`, `<COMPONENT_SEQUENCE>`, or similar placeholders as a completed preview.

## Inputs

- `implementation_objective`
- `project_context`
- `payroll_organization_cards_scope`
- `payroll_organization_cards_requirements`
- `legal_entity_search_text`
- `legal_reporting_unit_search_text`
- `legislative_data_group_search_text`
- `legislative_data_group_territory`
- `ldg_owner_association_request`
- `organization_card_owner_name`
- `legislative_data_group_name_request`
- `component_flexfield_value_request`
- `component_calculation_value_request`
- `requested_effective_date`
- `date_effective_action_preference`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `owner_scope_resolution`
- `source_type`
- `nested_task_route`
- `legal_entity_availability_result`
- `legal_entity_candidates`
- `legal_reporting_availability_result`
- `legal_reporting_candidates`
- `legislative_data_group_availability_result`
- `legislative_data_group_candidates`
- `legislative_data_group_owner_associations`
- `legislative_data_group_name`
- `legislative_data_group_id`
- `legislation_code`
- `component_flexfield_values`
- `calculation_card_dat_preview`
- `existence_discovery_summary`
- `resolved_operation_plan`
- `resolved_runtime_technical_keys`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Resolve the PSU/TRU owner scope with the canonical routing map before invoking a generated nested setup-task skill. Use the nested skills for task-level planning, sequencing, setup-data routing, and validation. The Legal Entity nested skill owns the payroll-specific mapping from calculation-card component, FLEX, and enterable-value metadata to `CalculationCard` HDL sections; `core.data-loader` remains responsible for live-template validation, DAT generation, ZIP packaging, upload, and load initiation after the required approvals. Track token usage for any generated project artifact or skill-run record using the manifest policy.
