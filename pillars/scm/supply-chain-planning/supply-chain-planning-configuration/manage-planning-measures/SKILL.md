---
skill_id: "scm.supply-chain-planning.supply-chain-planning-configuration.manage-planning-measures"
name: "Manage Planning Measures Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Planning Measures under the Supply Chain Planning Configuration functional area."
layer: "pillar"
pillar: "SCM"
offering: "Supply Chain Planning"
functional_area: "Supply Chain Planning Configuration"
functional_area_code: "ORA_MSC_VC_PLANNING_CONFIGURAT"
task_code: "CUSTOM_MSC_MANAGE_PLANNING_MEASURES"
task_name: "Manage Planning Measures"
parent_skill_id: "scm.supply-chain-planning.supply-chain-planning-configuration"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObjects:
  - "planningMeasures"
  - "planningMeasureSourceLists"
  - "planningMeasureValidateExpressions"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM supply chain planning pillar team"
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
  - "core.data-loader.task-hook"
  - "core.fusion-api.rest-api-client"
uses_core:
  - "core.data-loader.task-hook"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/supply-chain-planning/supply-chain-planning-configuration/manage-planning-measures/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/supply-chain-planning/supply-chain-planning-configuration/manage-planning-measures/current/"
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

# Manage Planning Measures Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Planning Measures` under `Supply Chain Planning Configuration`.

## Setup Task Skill Contract

- task_code: `CUSTOM_MSC_MANAGE_PLANNING_MEASURES`
- task_name: `Manage Planning Measures`
- parent_skill_id: `scm.supply-chain-planning.supply-chain-planning-configuration`
- pillar: `SCM`
- offering: `Supply Chain Planning`
- functional_area: `Supply Chain Planning Configuration`
- functional_area_code: `ORA_MSC_VC_PLANNING_CONFIGURAT`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `REST`
- businessObjects: `planningMeasures`, `planningMeasureSourceLists`, `planningMeasureValidateExpressions`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Planning Measures` under `Supply Chain Planning Configuration`.

For a new Planning Measure, use supplied ordered measure levels when present. Otherwise use a supplied positive integer `GranularityId`; if neither measure levels nor `GranularityId` is supplied, default `GranularityId` to `135`. Resolve the selected ID through the declared `granularityLevels` lookup and take its ordered levels and `MeasureContextId` from the exact returned item. A missing, invalid, or failed lookup still blocks creation. Do not replace invalid explicitly supplied levels or an invalid explicitly supplied ID with the default. Clear `GranularityId` from an ordinary create source after resolution. For a create handoff originating from duplication, preserve the authoritative source `GranularityId` when the selected live create schema and adapter support that field and exact value; apply the duplicate granularity contract below instead of the ordinary clearing rule.

## Planning Measure Field Capabilities

Use `ora-resource/ora_reference_lookups.md` for exact measure, UOM, and currency resolution and the configured Expression Builder validation contract. Apply `ora-resource/ora_input_validation.md` and `ora-resource/ora_design_enforcement.md` before preparing a source. A lookup or a documented REST operation is not an execution route.

- **Expression:** Accept optional `expression`. When `Expression` is requested for create, edit, or duplicate, validate its exact text through `planningMeasureValidateExpressions`. Inspect the returned validation details for `Expression is valid`. Retain the response; surface any other returned detail message verbatim and stop before submission. For a non-editable, non-stored measure require a valid Expression or select Collected and Refreshed / stored result. Include the exact validated `Expression` on create or when added or changed on update. `SeededExpression` is read-only.
- **Edit Lock Expression:** Accept optional `editLockExpression` only when Editable and Advanced Settings are enabled. Validate its exact text with the same server-side validator, passing it in the request body's `Expression` field. Require a returned validation detail containing `Expression is valid`; include the exact validated text as `EditLockExpr` on create or when added or changed on update. `SeededEditLockExpr` is read-only.
- **UOM, currency, and price lists:** Apply the field contract below to the measure Name, base codes, and display associations. For an existing measure, add an association only if the active workflow selects and verifies its parent measure batch child-create contract. Do not substitute a standalone child REST request or an unsupported batch operation.

### Name, UOM, currency, and price-list payload fields

Read and construct this portion of the measure payload with only the following attributes; other measure fields follow their own validation rules:

The create branches use `CPA.VALIDATE_CREATE_MEASURE` and
`CPA.VALIDATE_CREATE_MEASURE_FROM_GRANULARITY` in
`ora-resource/ora_input_validation.md` to validate and construct these fields.
The update branch uses `CPA.VALIDATE_MEASURE_UPDATE_FIELDS` in the same file.

`Name` is required, nonblank, and unique among existing measures. Complete the current measure lookup before deciding uniqueness; any exact match blocks a new create. For an update, the measure's own unchanged Name is allowed, but a changed Name must not collide with another MeasureId.

Set `BaseUOMCode` only for a Number `DataTypeId` on a non-seeded, non-read-only measure when the selected granularity does not contain both `PRD` and `ORG`, and the exact code resolves through the UOM LOV. Set `BaseCurrencyCode` only for a Currency `DataTypeId` under the same seeded, read-only, and `PRD` plus `ORG` restrictions, with an exact Currency LOV match. Omit or set an inapplicable, unsupplied base code to null; reject an explicitly supplied code that violates these conditions. Resolve `DataTypeId` through the live data-type lookup rather than guessing numeric IDs.

For `MeasureUOM.items`, resolve every `UomCode` from the UOM LOV, deduplicate codes, and never substitute a display name. For `MeasureCurrency.items`, do the same with `CurrencyCode` and the Currency LOV. Do not include either association for Percent, Date, or Text measure data types. Reject unresolved codes or duplicates that remain after normalization.

For `MeasurePriceList.items`, resolve each supplied Price List name to exactly one live Price List ID, write that numeric ID as `PricelistId`, and deduplicate IDs. A missing or ambiguous name blocks the payload. Never send `PriceListName`, and never use a Source List `ListId` as `PricelistId`.

### Mandatory expression gate

Before preparing or submitting a measure create or edit payload, invoke the configured server-side validator for `planningMeasureValidateExpressions` separately for each requested `Expression` and `EditLockExpr`.

`CPA.VALIDATE_CREATE_EXPRESSIONS` and `CPA.VALIDATE_UPDATE_EXPRESSIONS` in
`ora-resource/ora_reference_lookups.md` own the validator request and response
contract as executable task nodes.

For a create request containing `Expression`, enter `CPA.VALIDATE_CREATE_EXPRESSIONS` and call the validator POST in the selected Fusion environment. Continue to measure creation only after that request validates the exact supplied text.

Use the workflow-selected `core.fusion-api.rest-api-client` to `POST /fscmRestApi/resources/11.13.18.05/planningMeasureValidateExpressions` against the selected Fusion environment's configured `restBaseUrl`. This task-specific endpoint is supplied by the pillar developer; use the same relative path with each selected environment without an `rv:` revision. Do not infer validator availability from Data Loader registration. If the configured REST client cannot invoke this POST, stop with `Expression validation is unavailable through the configured Planning Measure validator. The expression was not submitted.`

After the binding passes, invoke one validator POST per requested `Expression` or `EditLockExpr`. The JSON body contains `MeasureId` (null or empty for create or duplicate; the resolved existing ID for edit), target `Name`, and the exact text in `Expression`; put Edit Lock text in that field for its own call. Data Loader source validation and an archived measure payload do not establish expression validity. Do not omit a requested expression or replace Fusion validation with local syntax checks.

Inspect Fusion's validation message in the response body even when the validator POST returns an HTTP error status. Read each `o:errorDetails[].detail` string, or the plain server message if no JSON detail is returned; unwrap an HTTP error prefix before comparing the server message. Only the exact message `Expression is valid` with no conflicting message passes this gate, regardless of HTTP status. Display every other returned server message verbatim and stop before measure create or update; a transport failure without a readable server message or an empty or unreadable response blocks submission. Preserve each validated text and result with the target name and MeasureId in the pre-submit evidence. Carry the exact validated `Expression` or `EditLockExpr` into the final payload; stop until the selected create or update adapter accepts that field. Before create, present the target environment, measure name, validated expressions, each validation result, and final immutable create payload for the selected workflow's approval immediately before execution. Changed expression text, name, MeasureId, environment, or payload requires fresh validation and approval.

Before any live action, resolve project and Run Book state, exact environment, identity, privileges, full source data, supported operation and client, payload/schema, artifact, and approval requirements. Present the final immutable payload or import artifact. The routed `core.data-loader` or `core.runbook` approval is authoritative for its own execution; another routed mutation needs explicit approval immediately before execution. Verify changes by reading the exact measure and associations after successful completion. Persist a classified diagnostic and stop if a workflow, validator, LOV, adapter, or approval contract is missing.

## Planning Measure Duplicate and Delete Requests

Use `ora-resource/ora_reference_lookups.md` to resolve a supplied measure name or MeasureId to exactly one current measure. Complete pagination before deciding whether a name is unique. A name that identifies one measure is sufficient; do not demand its internal ID from the user. A missing target, ambiguous name, incomplete lookup, or unverified environment identity stops the action with a specific explanation.

- **Delete:** Require a clear deletion request and a measure name or MeasureId. Require the user to confirm that the signed-in Fusion account has Delete Measure Definition privilege in the target environment; a separate privilege export is not required. Check whether the measure is predefined and read its manual associations and other displayed dependencies. Predefined measures and measures with blocking manual associations cannot be deleted. Present environment, exact MeasureId, name, and impacts for explicit confirmation immediately before the declared deletion step. Never retry deletion automatically. Expect `204 No Content`, then verify the measure is absent from a complete list. Classify a failure as predefined-measure, manual-association, authorization, or other API error.
- **Duplicate:** Require a source measure name or MeasureId and verify Maintain Measure Definition privilege. Create a new measure; never update the source or call an assumed dedicated duplicate operation. Copy valid applicable plan types, groups, catalogs, dimensionality, aggregation, value type, Expression, EditLockExpr, UOMs, currencies, price lists, conditional formats, and source-list values. Use a supplied new name or generate a unique `Copy of <source name>` name with a suffix. Reject a collision. Clear source MeasureId, seeded catalog associations, SeededExpression, and SeededEditLockExpr; set the duplicate to non-seeded. Force validated copied Expression and EditLockExpr into the new create request even when their text is unchanged. Never reuse source ListId values; create fresh source-list child rows only after the parent returns its new MeasureId through the selected child adapter. Validate the complete copied definition and readback; ask for missing or invalid required copied settings only. Preserve the authoritative source GranularityId through the fresh create handoff, dependency synchronization, defaulting, and final immutable source when the selected live create schema and adapter accept it. Resolve it to validate the copied levels and context, not to erase it. Retain the adapter-support evidence and duplicate origin internally. If the adapter cannot preserve it, use a level-based alternative only after verifying equivalent dimensionality; otherwise stop before approval. Never replace a duplicate's granularity with the ordinary create default. Verify the saved duplicate's granularity and dimensionality against the approved source definition.

Route preparation and execution through the active project workflow and its declared client or adapter. The reference lookup is not authority to call a live endpoint. If a required workflow step or adapter is missing, record the gap in the project workspace and stop before mutation. For an external mutation routed outside `core.data-loader` or `core.runbook`, present the exact environment, operation, and payload or immutable artifact and obtain explicit approval immediately before execution. Report success only after readback confirms the target was deleted or the duplicate exists with the approved name and validated definition. Otherwise report the failure class and specific cause, including missing privilege, predefined measure, manual association, or name collision.

### Planning Measure delete adapter

For `delete_planning_measure`, select `core.fusion-api.rest-api-client` and its standard Fusion REST route (`references/fusion-rest-api.md`, `scripts/fusion_rest_client.py`). The declared operation is `DELETE /fscmRestApi/resources/11.13.18.05/planningMeasures/{MeasureId}` with no request body. Substitute only the exact positive MeasureId returned by the fully paginated target lookup; the measure name is never a URL key. Require the client's configured `restBaseUrl` to match the active project's Run Book server origin and the environment shown for approval. Pass `--no-auth-retry` to prevent replay after a 401/403. Expect HTTP 204, then verify that the exact MeasureId is absent from a fresh complete measure lookup. [Oracle's delete contract](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25c/fasrp/op-planningmeasures-measureid-delete.html) establishes the resource shape; the existing privilege, association, immutable-preview, and immediate-approval gates still control execution.

For delete preflight, use the same selected client for `GET /fscmRestApi/resources/11.13.18.05/planningMeasures/{MeasureId}/child/measureAssociations`; collect every page and record each association's `Type`, `Name`, `ReferenceEntityId`, and `DeletionType`. Any `Manual` association blocks deletion; disclose `Automatic` associations as impacts. Record the user's explicit confirmation that the signed-in Fusion account has `MSC_DELETE_MEASURE_DEFINITION_PRIV` in the exact target environment; do not require a separate Security Console view or audit report. If that confirmation or the complete association result is missing, stop before approval. After these checks pass, persist an immutable preview containing environment origin, signed-in account context, exact MeasureId and name, association impacts, `DELETE` path, empty body, and confirmation/evidence references; hash the preview and request explicit approval of that hash immediately before the single attempt. Any changed target, evidence, environment, or operation invalidates the approval and requires a new preview. Treat a Fusion 401/403 as an authorization failure, without retrying DELETE. [Oracle association contract](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25c/fasrp/op-planningmeasures-measureid-child-measureassociations-get.html).

### Payload and operation contract

After live schema and selected-adapter validation, the complete create source may also include separately validated expression fields. Omit optional keys that were not supplied; omit unchanged expressions from an update. Supplied codes must resolve through the target environment's LOVs.

`CPA.VALIDATE_CREATE_MEASURE`,
`CPA.VALIDATE_CREATE_MEASURE_FROM_GRANULARITY`, and
`CPA.VALIDATE_DUPLICATE_MEASURE` in `ora-resource/ora_input_validation.md`
own the create and duplicate payload fields. The expression lookup nodes own
the server validation contract before either create branch prepares a source.

For an existing-measure association, `CPA.VALIDATE_MEASURE_UPDATE_FIELDS` owns the candidate parent batch child-create shapes. The workflow must verify batch support and select an adapter before using either shape; do not infer a generic batch endpoint.

The requested duplicate contract is a new `planningMeasures` create through the selected adapter. The new parent uses its unique `Name` and copied validated fields, including `Expression`, `EditLockExpr`, `MeasureUOM`, `MeasureCurrency`, and `MeasurePriceList`; it excludes source MeasureId, source `IsSeeded`, SeededExpression, SeededEditLockExpr, seeded catalog associations, and all source ListIds. Do not set `IsSeeded` to 2 by assumption. Omit it unless the live create schema requires an explicit value and the non-seeded code is verified for that environment. Re-resolve copied Price List names to numeric `PricelistId` values before the new create. For deletion, use the declared standard Fusion REST adapter above.

## Setup Task Metadata

- Task name: `Manage Planning Measures`
- Task code: `CUSTOM_MSC_MANAGE_PLANNING_MEASURES`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Objects: `planningMeasures`, `planningMeasureSourceLists`, `planningMeasureValidateExpressions`

`planningMeasureValidateExpressions` identifies the expression-validation service object and remains in the task's REST business-object list. Invoke its verified server-side operation before preparing a measure source with an expression. Its presence in the manifest does not establish a Data Loader registration or import contract; verify that contract from live Data Loader metadata before using it for sample generation or import.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task's business objects.

1. In the workflow-selected Fusion environment, resolve each of `planningMeasures`, `planningMeasureSourceLists`, and `planningMeasureValidateExpressions` against live Data Loader metadata. Confirm each exact top discriminator, registered sections, supported sample operation, and import capability. Save a sanitized metadata result with the environment and observation time in the project workspace. If any object cannot be resolved or lacks the required contract, classify a catalog mismatch, stop the three-object sample route, and report the missing contract. Do not infer Data Loader support from the REST validation service or substitute a different object.
2. Generate the default editable XLSX samples through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "planningMeasures" \
     "planningMeasureSourceLists" \
     "planningMeasureValidateExpressions" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep each business object's generated workbook set together:
   - editable sample workbook
   - attribute-details workbook
   - key-fields workbook
4. Confirm that the result contains all three requested discriminators and review their generated headers and key fields before preparing source data. The batch publishes no workbook if any requested object fails to resolve. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbooks as the starting point for the later Data Loader preparation and approval workflow.

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

Use the parent functional-area skill `scm.supply-chain-planning.supply-chain-planning-configuration` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
