---
skill_id: "hcm.global-payroll.hcm-extract.manage-hcm-extract-definitions"
name: "Manage HCM Extract Definitions Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage HCM Extract Definitions under the HCM Extract functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Payroll"
functional_area: "HCM Extract"
functional_area_code: "ORA_HCM_EXTRACT"
task_code: "PER_MANAGE_EXTRACT_DEFINITION"
task_name: "Manage HCM Extract Definitions"
parent_skill_id: "hcm.global-payroll.hcm-extract"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global payroll pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/hcm-extract/manage-hcm-extract-definitions/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/hcm-extract/manage-hcm-extract-definitions/current/"
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

# Manage HCM Extract Definitions Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage HCM Extract Definitions` under `HCM Extract`.

## Setup Task Skill Contract

- task_code: `PER_MANAGE_EXTRACT_DEFINITION`
- task_name: `Manage HCM Extract Definitions`
- parent_skill_id: `hcm.global-payroll.hcm-extract`
- pillar: `HCM`
- offering: `Payroll`
- functional_area: `HCM Extract`
- functional_area_code: `ORA_HCM_EXTRACT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage HCM Extract Definitions` under `HCM Extract`.

## Setup Task Metadata

- Task name: `Manage HCM Extract Definitions`
- Task code: `PER_MANAGE_EXTRACT_DEFINITION`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

## Extract Definitions Data Loader Create Guidance

For extract definition creation from current user input, generate a Data Loader source artifact for the registered business object `Extract Definitions`.

For extract block/data group creation from current user input, generate a Data Loader source artifact for the registered business object `Extract Data Groups` with top discriminator `extractBlocks`.

For extract data group filter criteria creation from current user input, generate a Data Loader source artifact for the registered child business object `Extract Data Group Filter Criteria` with discriminator `ExtractBlockCriteria` under `extractBlocks`.

For extract record creation from current user input, generate a Data Loader source artifact for the registered business object `Extract Records` with top discriminator `extractRecords`.

For extract data element/attribute creation from current user input, generate a Data Loader source artifact for the registered business object `Extract Attributes` with top discriminator `extractDataElements`.

For extract delivery option creation from current user input, generate a Data Loader source artifact for the registered business object `Extract Delivery Options` with top discriminator `extractDeliveryOptions`.

For post-create extract actions that require a persisted extract definition, support a second-level Data Loader set after the first Data Loader upload and load completes successfully. Generate second-level Data Loader source artifacts for the registered RAW_REST business objects `Extract Generate All Formulas` with top discriminator `generateAllFormulas` and `Extract Compile All Formulas` with top discriminator `compileAllFormulas`. Do not include these DAT files in the initial extract creation ZIP because they require the persisted `ExtractDefinitionId`. After the first load succeeds, resolve `ExtractDefinitionId` from the created extract definition using `extractDefinitions` by `DefinitionName`. Then generate `generateAllFormulas.dat` and `compileAllFormulas.dat`, package both into the same second-level ZIP, preview that ZIP, and proceed through approval/upload/initiation.

Resolve live Data Loader metadata through `core.data-loader` before source generation. Use the resolved top discriminator, field names, required fields, conditional fields, accepted source format, and payload behavior.

For definition-only scratch creation, include only the root `Extract Definitions` section unless child-object input is explicitly supplied or live metadata requires child rows.

For scratch extract definition creation, generate `extractDefinitions` DAT rows with `DefinitionName`, `BaseDefinitionName`, `DateStart`, `ExtractTypeCode`, `AttributeNineteen`, `ChangesOnlyFlg`, `FreezeStatus`, `UnfreezeComments`, `XmlTagName`, and `RestAction`. Derive `BaseDefinitionName` from `DefinitionName` unless supplied. Derive `XmlTagName` from `DefinitionName` unless supplied. Generate `ExtractTypeCode` from the resolved extract type lookup code, and generate `AttributeNineteen` from the resolved consumer lookup code when consumer is required.

For custom extract parameter creation, generate an `ExtractParameter` child section within `extractDefinitions.dat`. Use `DefinitionName` as the metadata-supported parent reference. Require the parameter name and data type, resolve the data type through `resolve_extract_parameter_data_type_lov`, and apply parameter naming rules and defaults before source generation.

Include required fields, supplied optional values that are part of the task-standard field set, and applicable defaults. Package the definition and its requested parameters through the existing single-ZIP workflow.

For block/data group scratch creation, resolve live Data Loader metadata for `Extract Data Groups` before source generation. The registered top discriminator is `extractBlocks`; generate only the root `extractBlocks` DAT source section.

For `Extract Data Groups` root source generation, use the latest live `extractBlocks` contract to shape the DAT source, but do not treat every metadata-required field as user readiness input. Classify each required/key field as user input, resolved lookup value, task-local default, generated artifact value, template-only value, or feature-conditional value before blocking.

For scratch block/data group creation, generate `extractBlocks` DAT rows with `DefinitionName`, `BlockName`, `BaseBlockName`, `BlockUserEntityId`, `MainBlockFlg`, `XmlTagName`, and `RestAction`. Derive `BaseBlockName` from `BlockName` unless supplied. Resolve `BlockUserEntityId` only through `extractBlockUserEntitiesLOV` before source generation. Resolve database item values only through `extractThreadingDBIsLOV` after the parent block user entity is resolved. Query `extractThreadingDBIsLOV` with the parent block `UserEntityId` and the supplied DBI label or ID first; if no exact row is returned, retry within the same `UserEntityId` scope and allow one unambiguous normalized candidate. When `MultiThreadActType=O`, generate the resolved `DatabaseItemId` into `MultiDbiId`.

For extract data group filter criteria creation, require `DefinitionName`, `BlockName`, and a filter criteria expression. Resolve the parent block from `DefinitionName` and `BlockName`; do not ask the user for `ReportBlockId`, `ReportCriteriaId`, or `ExtractDefinitionId`. Generate `ExtractBlockCriteria` rows only when the live `Extract Data Groups` Data Loader template exposes both `extractBlocks` and `ExtractBlockCriteria` `METADATA` sections. Generate `CriteriaFlg=C` for expression-based criteria, `EffectiveStartDate` from the parent extract `DateStart` unless supplied, `EffectiveEndDate=4712-12-31` unless supplied, and `RestAction=POST`. Classify the supplied criteria expression before source generation as plain UI expression, tokenized display CLOB, or executable criteria CLOB. Transform plain UI expressions into both generated CLOB fields; use tokenized display CLOB directly only for `DisplayCriteriaExpressionClob` and generate `CriteriaClob`; use executable criteria CLOB directly only for `CriteriaClob` and generate `DisplayCriteriaExpressionClob` only when every referenced column maps unambiguously to a resolved DBI. For CLOB-backed criteria, keep scalar `Criteria` and `DisplayCriteriaExpression` empty.

Plain UI criteria may be generated without calling item-level criteria actions when every referenced DBI, operator, connector, and value resolves unambiguously. Generate the executable `CriteriaClob` from the resolved DBI SQL column/expression mapping and generate `DisplayCriteriaExpressionClob` from the resolved DBI token/operator/value sequence. Do not block solely because `calculateCriteria` or `validateAdvancedCriteria` requires an existing criteria item.

Generated filter criteria CLOBs must use the Fusion Extracts advanced-criteria storage format. `CriteriaClob` must use the resolved SQL expression for each DBI, such as `per.person_number`, not the DBI token such as `PER_EXT_PER_PERSON_NUMBER`. Date literals in executable criteria must use the Extracts date helper format observed from Fusion, for example `FF_FUNC.TD('01-01-1999')`, not `TO_DATE(...)`, unless live metadata for that DBI explicitly proves another expression. `DisplayCriteriaExpressionClob` must be fully tokenized as brace-delimited DBI/operator/value/connector tokens, for example `{PER_EXT_PER_PERSON_NUMBER}{Is Like}{'111%'}{And}{PER_EXT_PER_START_DATE}{>}{'01-01-1999'}`. Free text such as `IS LIKE`, `AND`, or unbraced values must not appear outside braces in `DisplayCriteriaExpressionClob`.

Before preview, validate and rectify generated criteria CLOBs. If a generated `CriteriaClob` contains DBI tokens, `TO_DATE(...)`, copied plain UI text, or unresolved SQL expressions, regenerate it from the resolved DBI SQL-expression evidence. If generated `DisplayCriteriaExpressionClob` is not a complete brace-token sequence, regenerate it from the resolved DBI/operator/value/connector evidence. Stop before preview only when the required DBI SQL expression or token evidence is missing or ambiguous.

For scratch extract record creation, generate `extractRecords` DAT rows with `DefinitionName`, `BlockName`, `RecordName`, `BaseRecordName`, `TypeCode`, `ProcessCode`, `EffectiveStartDate`, `EffectiveEndDate`, `Sequence`, `XmlTagName`, `FlexStructureCode`, `HideFlg`, `RequiredFlg`, and `RestAction`. Derive `BaseRecordName` from `RecordName` unless supplied. Derive `XmlTagName` and `FlexStructureCode` as tag names from `RecordName`. Apply task-local defaults for record type, process code, effective dates, sequence, hide flag, and required flag before source generation.

For scratch extract data element creation, generate `extractDataElements` DAT rows with `DefinitionName`, `BlockName`, `RecordName`, `DataElementName`, `XmlTagName`, `ShortCode`, `InformationColumn`, `InformationLabel`, `HideFlg`, `RequiredFlg`, `DbiGroupId`, `DataType`, `TypeCode`, `ContextFlg`, `UIHideFlg`, `AttributeTwentyFive`, `StartDate`, and `RestAction`. Resolve DBI-backed data element identity through `userEntityDatabaseItems` filtered by the parent block user entity: `q=UserEntityId=<parent block user entity id>`. Generate `DbiGroupId` from the resolved row. Require `DataType` from the user for DBI-backed data elements and validate it as `N`, `D`, or `T`. For DBI-backed data elements, generate `TypeCode=F`. Default `DataElementName` from the resolved DBI/group name unless the user explicitly supplied `DataElementName`. Final `extractDataElements` DAT output must be constrained to the task-standard field set and must omit empty, template-only, optional, unresolved, or non-standard fields.

For scratch extract delivery option creation, generate `extractDeliveryOptions` DAT rows with `DefinitionName`, `DeliveryOptionName`, `BaseDeliveryOptionName`, `DeliveryTypeNew`, `OutputType`, `OutputName`, `DateFrom`, and `RestAction`. Treat `ExtractDefinitionId` as the metadata-supported foreign key resolved from `DefinitionName`, not as a user-supplied value. Derive `BaseDeliveryOptionName` from `DeliveryOptionName` unless supplied. Default `OutputType=XML` when not supplied. Default `OutputName` from `DeliveryOptionName` when not supplied. Default `DateFrom` from the parent extract definition `DateStart`. Default `RestAction=POST`.

For `generateAllFormulas` and `compileAllFormulas`, generate DAT rows with `ExtractDefinitionId` and `RestAction`. Resolve `ExtractDefinitionId` only after the first Data Loader load has completed successfully. Generate `RestAction=POST`.

For scratch delivery option creation, require the user to explicitly supply delivery type. Only `NONE` is supported. Stop before source generation when delivery type is missing or anything other than `NONE`. For output type, support only `DATA` and `XML`; stop before source generation when another output type is supplied. For delivery type `NONE`, generate `ExtractDeliveryOptionDetail` child rows with parent context, `OptionType`, and `RestAction` for each default option type: `BURSTING`, `FILE_NAME_DE`, `KEY`, `LOCALE`, `OBJECT_ID`, `OBJECT_TYPE`, `SYSTEM_DOCUMENT_TYPE`, `TIMEZONE`, and `ZIP`. Generate `OptionValue` only when the user provides a supported option-specific value; otherwise leave it blank/null.

For live creation requests that generate more than one DAT source for the same extract-definition operation, prepare one upload ZIP containing every validated DAT file for that request. Validate each DAT source independently, then bind preview and approval to the single combined ZIP fingerprint.

For scratch root-only source generation, do not include optional metadata-exposed attributes merely because they appear in the template or schema. Generate only required fields, user-supplied fields, task-local defaults, and resolved conditional fields. Treat optional LOV-backed attributes as blocked unless their LOV contract and generated value are explicitly resolved.

For `Extract Definitions` scratch creation, generate `DateStart` as `YYYY-MM-DD`.

Resolve Extract Type through the `PER_EXT_TYPES` lookup and generate the resolved `LookupCode`. Match by exact `LookupCode` or `Meaning` first; when no exact match exists, allow a single unambiguous returned candidate whose meaning or code contains, starts with, or token-matches the user value.

Resolve Consumer through `resolve_extract_consumer_lov` when required, using the same exact-first, single-candidate fallback rule. Generate the resolved Consumer `LookupCode` into `AttributeNineteen` for the `Extract Definitions` source artifact. Carry resolver evidence through preview: selected extract type, consumer lookup type, supplied consumer value, resolved `LookupCode`, resolved `Meaning`, and match mode.

Apply task-local defaults from `ora-resource/ora_defaulting_rules.md` before dependency readiness and source generation. Generated DAT rows must include applicable defaults when the field is part of the task standard and metadata exposes the attribute.

Use only the resolvers declared in the Manage HCM Extract Definitions task contract. Resolver output must come from task-declared metadata endpoints, task-declared LOV endpoints, task-local defaults, or current user input. Validation confirms conformance to the task-defined source contract; validation failures stop the flow before preview and are not used to discover alternate endpoints, infer values from existing rows, or reshape business semantics.

Use this task metadata when invoking those skills:

- Offering: `Global Payroll`
- Functional area / Setup Object: `HCM Extract`
- Setup task name: `Manage HCM Extract Definitions`
- Setup task code: `PER_MANAGE_EXTRACT_DEFINITION`


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

Use the parent functional-area skill `hcm.global-payroll.hcm-extract` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
