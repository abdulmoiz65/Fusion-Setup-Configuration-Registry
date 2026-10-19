---
task_code: "ORA_SVC_MANAGE_SELF_SERVICE_RELATIONSHIP_TYPE_STANDARD_LOOKUP"
task_name: "Manage Self-Service Relationship Type Standard Lookup"
parent_skill_id: "cx.service.digital-customer-service"
pillar: "CX"
offering: "Service"
functional_area: "Digital Customer Service"
functional_area_code: "ORA_SVC_DIGITAL_CUSTOMER_SERVICE"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Self-Service Relationship Type Standard Lookup

## Setup Task Metadata

- Task name: `Manage Self-Service Relationship Type Standard Lookup`
- Task code: `ORA_SVC_MANAGE_SELF_SERVICE_RELATIONSHIP_TYPE_STANDARD_LOOKUP`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``






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
## Use Cases

### View Self Service Relationship Type Standard Lookup

View the Self-Service Relationship Type standard lookup header and its lookup-code rows.

1. Retrieve the ORA_SVC_CSS_REL_TYPE_CD lookup type with core.fusion-api.apps-common using the Standard Lookups REST resource when a REST view is sufficient.
2. Export Manage Self-Service Relationship Type Standard Lookup setup data with shared.setup-export.task-level-export when a screen-equivalent list or FSM package baseline is required.
3. Return the lookup header fields Lookup Type, Meaning, Description, Module, Lookup Configuration Level, and REST Access Secured.
4. Treat the screenshot values ORA_SVC_CSS_REL_TYPE_CD, Self registrations relationship type code, Service, Extension, and Authenticated as same-task screen evidence until replaced by a fresh export or REST response.

### View Self Service Relationship Type Lookup Codes

View the lookup codes that define available self-service relationship types.

1. Read lookup codes under ORA_SVC_CSS_REL_TYPE_CD with core.fusion-api.apps-common using the Standard Lookup Codes REST child resource when REST access is available.
2. Export the setup task when Display Sequence, Start Date, End Date, Description, Tag, or a package baseline is required.
3. Return Lookup Code, Display Sequence, Enabled, Start Date, End Date, Meaning, Description, and Tag for each row.
4. Treat ORA_CSS_ACC_ADMIN with meaning Account Administrator, ORA_CSS_ACC_MGR with meaning Account Manager, and ORA_CSS_USER with meaning User as the seeded enabled rows shown in the task screen, each with start date 12/25/15, until verified by current environment evidence.

### View Self Service Relationship Type Lookup Code

View one self-service relationship type lookup code before changing it.

1. Resolve the requested row by exact Lookup Code or exact Meaning within ORA_SVC_CSS_REL_TYPE_CD.
2. Require exactly one matching row before preparing a row-level change; stop when no matching row or multiple matching rows are returned.
3. Return the selected row's Lookup Code, Display Sequence, Enabled, Start Date, End Date, Meaning, Description, and Tag.
4. Preserve the lookup type header context, including Lookup Configuration Level Extension and REST Access Secured Authenticated when confirmed by the active environment.

### Create Self Service Relationship Type Lookup Code

Create a self-service relationship type lookup code for a custom Digital Customer Service relationship type.

1. Validate the requested Lookup Code, Meaning, Enabled value, effective dates, optional Display Sequence, Description, and Tag against the setup-task screen shape and standard lookup-code rules.
2. Require a non-ORA custom lookup code for new customer-owned rows; do not create new seeded-style ORA_* codes.
3. Check ORA_SVC_CSS_REL_TYPE_CD for an existing row with the same Lookup Code or conflicting Meaning before packaging the change.
4. Export Manage Self-Service Relationship Type Standard Lookup setup data with shared.setup-export.task-level-export.
5. Use the completed export of the same setup task as the package baseline; preserve its package structure and add only the approved lookup-code row.
6. Validate the FSM package with shared.validation.setup-data-validator.
7. Import the approved ZIP with core.data-loader.
8. Verify the created lookup code with a fresh REST read or task export.

### Update Self Service Relationship Type Lookup Code

Update an existing self-service relationship type lookup code's meaning, description, display sequence, tag, enablement, or effective dates.

1. Resolve the existing row by exact Lookup Code in ORA_SVC_CSS_REL_TYPE_CD and require exactly one match.
2. Validate each requested field change against the lookup configuration level, predefined-data restrictions, setup-task screen shape, and current export metadata.
3. Stop before changing a seeded ORA_* row unless the current task evidence shows the field is editable and the requested change is limited to allowed extension-level attributes such as meaning, description, display sequence, tag, enablement, or effective dates.
4. Export Manage Self-Service Relationship Type Standard Lookup setup data with shared.setup-export.task-level-export.
5. Use the completed export of the same setup task as the package baseline; retain the selected row's exported identity and modify only approved fields.
6. Validate the FSM package with shared.validation.setup-data-validator.
7. Import the approved ZIP with core.data-loader.
8. Verify the updated lookup code with a fresh REST read or task export.

### Activate Self Service Relationship Type Lookup Code

Activate an existing self-service relationship type lookup code.

1. Resolve the existing row by exact Lookup Code in ORA_SVC_CSS_REL_TYPE_CD and require exactly one match.
2. Validate that the lookup configuration level and current row state permit enablement changes.
3. Export Manage Self-Service Relationship Type Standard Lookup setup data with shared.setup-export.task-level-export.
4. Set the selected row's Enabled value to enabled in the FSM package, preserving all other exported values unless explicitly approved.
5. Validate the FSM package with shared.validation.setup-data-validator.
6. Import the approved ZIP with core.data-loader.
7. Verify the row is enabled with a fresh REST read or task export.

### Deactivate Self Service Relationship Type Lookup Code

Deactivate an existing self-service relationship type lookup code.

1. Resolve the existing row by exact Lookup Code in ORA_SVC_CSS_REL_TYPE_CD and require exactly one match.
2. Confirm that the relationship type is not required by active Digital Customer Service registration, role-mapping, or account-administration behavior before disabling it.
3. Validate that the lookup configuration level and current row state permit enablement changes.
4. Show "The self-service relationship type lookup code will be deactivated. Do you want to continue?" and wait for confirmation.
5. Export Manage Self-Service Relationship Type Standard Lookup setup data with shared.setup-export.task-level-export.
6. Set the selected row's Enabled value to disabled in the FSM package, preserving all other exported values unless explicitly approved.
7. Validate the FSM package with shared.validation.setup-data-validator.
8. Import the approved ZIP with core.data-loader.
9. Verify the row is disabled with a fresh REST read or task export.

### Delete Self Service Relationship Type Lookup Code

Delete a self-service relationship type lookup code.

Not supported. Delete is outside the supported Manage Self-Service Relationship Type Standard Lookup workflow; deactivate the lookup code instead unless Oracle documentation and current task export evidence provide a task-specific delete path.
## Purpose

Review and define lookup values for self-service relationship types.
## FSM Contract

### FND_APP_STANDARD_LOOKUP

- `LookupType`: Set to ORA_SVC_CSS_REL_TYPE_CD.
- `Meaning`: Retain the exported self-service relationship lookup meaning.
- `Description`: Retain the exported value or use "".
- `CreatedBy`: Retain the exported value or use the current user.
- `CreationDate`: Retain the exported value or use the current date and time.
- `LastUpdatedBy`: Retain the exported value or use the current user.
- `LastUpdateDate`: Retain the exported value or use the current date and time.
- `LastUpdateLogin`: Retain the exported value or use -1.
- `ModuleId`: Retain the exported module ID.
- `CustomizationLevel`: Retain the exported customization level; do not change the lookup configuration level.
- `RestAccessSecured`: Retain the exported value or use AUTH.
- `BossAppPackageName`: Retain the exported value or leave blank.
- `BossAppPackageVersion`: Retain the exported value or leave blank.
- `BossModuleName`: Retain the exported value or leave blank.
- `BossIdentifier`: Retain the exported value or leave blank.

### ORA_FND_APP_STANDARD_LOOKUP_CODE

- `FND_APP_STANDARD_LOOKUP.LookupType`: Set to ORA_SVC_CSS_REL_TYPE_CD.
- `LookupCode`: Non-empty unique customer code string within ORA_SVC_CSS_REL_TYPE_CD, for example CUST_PARTNER_ADMIN. Require an approved code; do not use the reserved ORA prefix or replace an existing code.
- `DisplaySequence`: Optional base-10 integer with no decimal point or grouping separator, for example 10. Leave blank for a new code when not supplied; preserve on update unless explicitly changed.
- `EnabledFlag`: Allowed values are uppercase Y (enabled) and N (disabled), both confirmed by same-task export. Default to Y for a new code unless the approved initial state is disabled; preserve the value on an unrelated update.
- `StartDateActive`: Optional date in YYYY/MM/DD format, for example 2026/09/21. Leave blank for a new code when not supplied; preserve on update unless explicitly changed.
- `EndDateActive`: Optional date in YYYY/MM/DD format, not earlier than StartDateActive when both are provided. Leave blank for a new code when not supplied; preserve on update unless explicitly changed.
- `Meaning`: Set to the self-service relationship type meaning. Meaning is required for a new self-service relationship type; ask the customer when it is not provided.
- `Description`: Set to the optional self-service relationship type description.
- `CreatedBy`: Retain the exported value or use the current user.
- `CreationDate`: Retain the exported value or use the current date and time.
- `LastUpdatedBy`: Retain the exported value or use the current user.
- `LastUpdateDate`: Retain the exported value or use the current date and time.
- `LastUpdateLogin`: Retain the exported value for existing rows; omit for new rows unless same-task package evidence requires it.
- `Tag`: Set to the optional self-service relationship type tag. Leave blank when no value is provided.
## Guard Rails

1. Require an authenticated Fusion user context before any Fusion operation; use `core.auth.fusion-oauth-authentication`.
2. Do not use `core.fusion-api.rest-api-client` to create, update, or delete records.
3. Do not use `shared.setup-import.task-level-import` to create, update, or delete records.
## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Service`
- Functional area / Setup Object: `Digital Customer Service`
- Setup task name: `Manage Self-Service Relationship Type Standard Lookup`
- Setup task code: `ORA_SVC_MANAGE_SELF_SERVICE_RELATIONSHIP_TYPE_STANDARD_LOOKUP`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Self-Service Relationship Type Standard Lookup` under `Digital Customer Service`.
