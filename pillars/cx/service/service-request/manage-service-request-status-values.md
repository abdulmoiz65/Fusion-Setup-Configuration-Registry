---
task_code: "ORA_SVC_SERVICE_REQUEST_STATUS"
task_name: "Manage Service Request Status Values"
parent_skill_id: "cx.service.service-request"
pillar: "CX"
offering: "Service"
functional_area: "Service Request"
functional_area_code: "ORA_SVC_SERVICE_REQUEST"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Service Request Status Values

## Setup Task Metadata

- Task name: `Manage Service Request Status Values`
- Task code: `ORA_SVC_SERVICE_REQUEST_STATUS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## FSM Contract

### FND_APP_STANDARD_LOOKUP

- `LookupType`: Set to ORA_SVC_SR_STATUS_CD.
- `Meaning`: Retain the exported value or use SR Status.
- `Description`: Retain the exported value or use "".
- `CreatedBy`: Retain the exported value or use the current user.
- `CreationDate`: Retain the exported value or use the current date and time.
- `LastUpdatedBy`: Retain the exported value or use the current user.
- `LastUpdateDate`: Retain the exported value or use the current date and time.
- `LastUpdateLogin`: Retain the exported value or use -1.
- `ModuleId`: Retain the exported value or use 08C1ABF048177E22E050F00A1720179C.
- `CustomizationLevel`: Retain the exported value or use U.
- `RestAccessSecured`: Retain the exported value or use AUTH.
- `BossAppPackageName`: Retain the exported value or leave blank.
- `BossAppPackageVersion`: Retain the exported value or leave blank.
- `BossModuleName`: Retain the exported value or leave blank.
- `BossIdentifier`: Retain the exported value or leave blank.

### ORA_FND_APP_STANDARD_LOOKUP_CODE

- `FND_APP_STANDARD_LOOKUP.LookupType`: Set to ORA_SVC_SR_STATUS_CD.
- `LookupCode`: Set the unique customer-owned status code. When no code is provided, generate one from Meaning and Description; do not use the reserved ORA prefix.
- `DisplaySequence`: Set to the status display sequence. DisplaySequence is required for a new status; ask the customer when it is not provided.
- `EnabledFlag`: Set to Y to enable or N to deactivate the status. When no value is provided, default to Y.
- `StartDateActive`: Set to the optional start date. Leave blank when no value is provided.
- `EndDateActive`: Set to the optional end date. Leave blank when no value is provided.
- `Meaning`: Set to the status meaning. Meaning is required for a new status; ask the customer when it is not provided.
- `Description`: Set to the optional status description.
- `CreatedBy`: Retain the exported value or use the current user.
- `CreationDate`: Retain the exported value or use the current date and time.
- `LastUpdatedBy`: Retain the exported value or use the current user.
- `LastUpdateDate`: Retain the exported value or use the current date and time.
- `LastUpdateLogin`: Retain the exported value for existing rows; omit for new rows unless same-task package evidence requires it.
- `Tag`: Set to the optional status tag. Leave blank when no value is provided.

### ORA_SVC_LOOKUP_CODE_RELS

- `ChildLookupCode`: Set to the approved Service Request status lookup code.
- `ParentLookupCode`: Fetch the approved parent lookup code with core.fusion-api.apps-common using ParentLookupType and the Service Request Statuses LOV REST resource. Leave blank only when same-task export evidence permits a status without a parent relationship.
- `RelationCode`: Set to ORA_SVC_STATUS_TYPE_STATUS.
- `ChildLookupType`: Set to ORA_SVC_SR_STATUS_CD.
- `LookupTypeRelationRelationCode`: Set to ORA_SVC_STATUS_TYPE_STATUS.
- `ChildLookupCodeMeaning`: Set to the selected status lookup's Meaning; preserve the exported value for an existing relationship unless the status Meaning is changed in the same approved package.
- `EnabledFlag`: Set to Y to enable or N to deactivate the status relationship. Retain the exported value for an existing relationship unless an approved enabled-state change is supported by same-task package evidence.
- `DisplaySequence`: Set to the status display sequence. Leave blank only when no display sequence is supplied and same-task package evidence permits it.
- `ParentLookupType`: Set to ORA_SVC_SR_STATUS_TYPE_CD.
## Purpose

Manage the status values and parent-status relationships used by Service Requests.
## Use Cases

### View Service Request Status Values

View all configured Service Request status values, their parent relationships, and active states.

1. Read Service Request Statuses with core.fusion-api.apps-common using the Service Request Statuses LOV REST resource.
2. Return LookupCode, ParentLookupCode, Meaning, EnabledFlag, StartDateActive, EndDateActive, and DisplaySequence.

### View Service Request Status Value

View a selected Service Request status value before changing it.

1. Read the requested Service Request status with core.fusion-api.apps-common using the Service Request Statuses LOV REST resource.
2. Require exactly one match for the requested LookupCode and ParentLookupCode when supplied; stop when no matching status or multiple matches are returned.

### Create Service Request Status Value

Create a Service Request status value with its required code, meaning, active state, display sequence, and optional parent status.

1. Read the requested Service Request status with core.fusion-api.apps-common using the Service Request Statuses LOV REST resource.
2. Stop if the requested LookupCode and ParentLookupCode combination already exists.
3. Confirm the LookupCode, Meaning, EnabledFlag, DisplaySequence, optional ParentLookupCode, and optional active dates.
4. Export Service Request status setup data with shared.setup-export.task-level-export.
5. Use the completed export of the same setup task as the package baseline; preserve its package structure and add only the approved status row and required parent relationship.
6. Validate the FSM package with shared.validation.setup-data-validator.
7. Import the approved ZIP with core.data-loader.
8. Verify the new status with a fresh Service Request Statuses LOV REST read.

### Update Service Request Status Value

Update an existing Service Request status value's meaning, parent status, active dates, display sequence, or enabled state.

1. Read the requested Service Request status with core.fusion-api.apps-common using the Service Request Statuses LOV REST resource.
2. Require exactly one match for the requested LookupCode and ParentLookupCode when supplied and validate the approved changes.
3. Export Service Request status setup data with shared.setup-export.task-level-export.
4. Use the completed export of the same setup task as the package baseline; retain the existing status identity and required parent relationship and modify only the approved status fields.
5. Validate the FSM package with shared.validation.setup-data-validator.
6. Import the approved ZIP with core.data-loader.
7. Verify the updated status with a fresh Service Request Statuses LOV REST read.

### Activate Service Request Status Value

Activate an existing Service Request status value.

1. Read the requested Service Request status with core.fusion-api.apps-common using the Service Request Statuses LOV REST resource.
2. Export Service Request status setup data with shared.setup-export.task-level-export.
3. Set the selected status to enabled in the FSM package.
4. Validate the FSM package with shared.validation.setup-data-validator.
5. Import the approved ZIP with core.data-loader.
6. Verify the status is active with a fresh Service Request Statuses LOV REST read.

### Deactivate Service Request Status Value

Deactivate an existing Service Request status value.

1. Read the requested Service Request status with core.fusion-api.apps-common using the Service Request Statuses LOV REST resource.
2. Export Service Request status setup data with shared.setup-export.task-level-export.
3. Show "The Service Request status value will be deactivated. Do you want to continue?" and wait for confirmation.
4. Set the selected status to disabled in the FSM package.
5. Validate the FSM package with shared.validation.setup-data-validator.
6. Import the approved ZIP with core.data-loader.
7. Verify the status is inactive with a fresh Service Request Statuses LOV REST read.

### Delete Service Request Status Value

Delete a Service Request status value.

Not supported. Service Request status-value deletion is not supported through this FSM workflow; deactivate the status instead.
## Guard Rails

1. Require an authenticated Fusion user context before any Fusion operation; use `core.auth.fusion-oauth-authentication`.
2. Do not use `core.fusion-api.rest-api-client` to create, update, or delete records.
3. Do not use `shared.setup-import.task-level-import` to create, update, or delete records.
## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import reviewed task setup data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Service`
- Functional area / Setup Object: `Service Request`
- Setup task name: `Manage Service Request Status Values`
- Setup task code: `ORA_SVC_SERVICE_REQUEST_STATUS`


## FSM Data Loader Package Requirements

1. Read the task's fsm_contract first when it is present. Treat its objects and field guidance as the task-specific starting point for classifying each requested change as an existing-root update, new root, existing-child update, new child of an existing parent, new relationship, or mixed package change.
2. Read `ASM_SETUP_CSV_METADATA.xml` in the task export package for business objects, XML paths, node sequence, attributes, scope, and relationships; reconcile it with the task's fsm_contract when one is present.
3. Use the fsm_contract object and field guidance together with metadata-defined node sequence and relationships to determine package order and required object coverage.
4. Verify the selected baseline or template package includes the members, file names, structure, headers, encoding, scope, relationship rows, and fsm_contract objects and fields required for the requested change.
5. Treat a completed export of this same setup task as authoritative evidence for package structure, headers, node order, key and linkage shape, and generated-identity handling. Use it to corroborate the fsm_contract and record provenance for copied template values.
6. For existing-row updates, retain exported identities and all unchanged values, parent rows, child rows, and relationships required by the fsm_contract and package evidence; do not carry unrelated baseline rows into the change package unless they are required for import integrity. Change only approved fields.
7. For a new child or relationship, retain the existing parent identity and use only linkage, keys, and required values specified by the fsm_contract or confirmed by same-task package evidence.
8. For greenfield rows, construct the create contract from the fsm_contract, task-specific documented requirements, `ASM_SETUP_CSV_METADATA.xml`, a completed export of this same task, and supported preview or dry-run results where available.
9. An export whose data CSV members contain only headers is valid structural evidence for a greenfield contract, not an automatic blocker. Use the fsm_contract, exported package structure, and explicit supported inputs to construct the rows; stop only when required fields, keys, relationships, or values remain unresolved or validation rejects the package.
10. Populate every root, child, scoped, localized, and relationship object required by the fsm_contract or confirmed package contract. Populate approved business keys, required values, and reference values; omit generated identities unless explicitly required.
11. Classify every populated fsm_contract field as request-provided, documented requirement, export-derived structural value, export-derived template value, generated or omittable, or unresolved.
12. A fsm_contract field may be omitted only when it is documented as generated or optional, is absent or consistently blank in semantically comparable exports of this same task, or is accepted as omitted by supported preview or dry-run validation. Do not infer a value solely from a field name or description.
13. Do not copy identities, reference keys, parent keys, scope values, localized values, lookup codes, or behavior-changing settings unless the fsm_contract, request, documented guidance, or approved compatible template default explicitly supports the value.
14. Verify every non-generated parent, lookup, code, scope, locale, and related-object reference required by the fsm_contract against approved same-task package evidence or the workflow's documented resolver; include required parents or relationship rows only when the package contract requires them.
15. Build the complete package required by the fsm_contract and package evidence; never use a child-only package or infer fields, defaults, identities, or relationships from another task or object type.
16. Validate package members, fsm_contract objects and fields, metadata, keys, scopes, references, relationships, node order, field-value provenance, and approved changes before import; confirm that no baseline identity, template-only setting, or unrelated row is introduced or modified unintentionally. Use preview or dry-run validation when available.
17. Stop when a required fsm_contract field or object, identity rule, parent-child linkage, scope, dependency, or behavior-changing setting remains unresolved and lacks an explicit approved value or sufficient same-task evidence. Do not block for fields evidenced as generated or validated-omittable.
## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Service Request Status Values` under `Service Request`.
