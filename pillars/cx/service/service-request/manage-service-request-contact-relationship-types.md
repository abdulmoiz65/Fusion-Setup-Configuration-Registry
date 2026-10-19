---
task_code: "ORA_SVC_MANAGE_SERVICE_REQUEST_CONTACT_RELATIONSHIP_TYPES"
task_name: "Manage Service Request Contact Relationship Types"
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

# Manage Service Request Contact Relationship Types

## Setup Task Metadata

- Task name: `Manage Service Request Contact Relationship Types`
- Task code: `ORA_SVC_MANAGE_SERVICE_REQUEST_CONTACT_RELATIONSHIP_TYPES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## FSM Contract

### FND_APP_STANDARD_LOOKUP

- `LookupType`: Set to ORA_SVC_CONTACT_REL_TYPE_CD.
- `Meaning`: Retain the exported value or use SR Contact Relation Type.
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

- `FND_APP_STANDARD_LOOKUP.LookupType`: Set to ORA_SVC_CONTACT_REL_TYPE_CD.
- `LookupCode`: Set the unique customer-owned contact-relationship-type code. When no code is provided, generate one from Meaning and Description; do not use the reserved ORA prefix.
- `DisplaySequence`: Set to the contact-relationship-type display sequence. DisplaySequence is required for a new contact relationship type; ask the customer when it is not provided.
- `EnabledFlag`: Set to Y to enable or N to deactivate the contact relationship type. When no value is provided, default to Y.
- `StartDateActive`: Set to the optional start date. Leave blank when no value is provided.
- `EndDateActive`: Set to the optional end date. Leave blank when no value is provided.
- `Meaning`: Set to the contact-relationship-type meaning. Meaning is required for a new contact relationship type; ask the customer when it is not provided.
- `Description`: Set to the optional contact-relationship-type description.
- `CreatedBy`: Retain the exported value or use the current user.
- `CreationDate`: Retain the exported value or use the current date and time.
- `LastUpdatedBy`: Retain the exported value or use the current user.
- `LastUpdateDate`: Retain the exported value or use the current date and time.
- `LastUpdateLogin`: Retain the exported value for existing rows; omit for new rows unless same-task package evidence requires it.
- `Tag`: Set to the optional contact-relationship-type tag. Leave blank when no value is provided.
## Purpose

Manage the contact-relationship-type lookup values used by Service Requests.
## Use Cases

### View Service Request Contact Relationship Types

View all configured Service Request contact relationship types and their active states.

1. Read the ORA_SVC_CONTACT_REL_TYPE_CD lookup codes with core.fusion-api.apps-common using the Standard Lookup Codes REST resource.
2. Return LookupCode, Meaning, Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, and Tag.

### View Service Request Contact Relationship Type

View a selected Service Request contact relationship type before changing it.

1. Read the requested ORA_SVC_CONTACT_REL_TYPE_CD lookup code with core.fusion-api.apps-common using LookupCodeFinder.
2. Require exactly one matching lookup code; stop when no matching code or multiple matches are returned.

### Create Service Request Contact Relationship Type

Create a Service Request contact relationship type with a unique code, meaning, enabled state, and display sequence.

1. Read the requested ORA_SVC_CONTACT_REL_TYPE_CD lookup code with core.fusion-api.apps-common using LookupCodeFinder.
2. Stop if the code already exists.
3. Confirm the unique LookupCode, Meaning, EnabledFlag, DisplaySequence, and any optional description, dates, or tag.
4. Export contact-relationship-type setup data with shared.setup-export.task-level-export.
5. Use the completed export of the same setup task as the package baseline; preserve its package structure and add only the approved contact-relationship-type row.
6. Validate the FSM package with shared.validation.setup-data-validator.
7. Import the approved ZIP with core.data-loader.
8. Verify the new contact relationship type with a fresh Standard Lookup Codes REST read.

### Update Service Request Contact Relationship Type

Update an existing Service Request contact relationship type's meaning, description, active dates, display sequence, tag, or enabled state.

1. Read the requested ORA_SVC_CONTACT_REL_TYPE_CD lookup code with core.fusion-api.apps-common using LookupCodeFinder.
2. Require exactly one matching lookup code and validate the approved changes.
3. Export contact-relationship-type setup data with shared.setup-export.task-level-export.
4. Use the completed export of the same setup task as the package baseline; retain the existing lookup identity and modify only the approved contact-relationship-type fields.
5. Validate the FSM package with shared.validation.setup-data-validator.
6. Import the approved ZIP with core.data-loader.
7. Verify the updated contact relationship type with a fresh Standard Lookup Codes REST read.

### Activate Service Request Contact Relationship Type

Activate an existing Service Request contact relationship type.

1. Read the requested ORA_SVC_CONTACT_REL_TYPE_CD lookup code with core.fusion-api.apps-common using LookupCodeFinder.
2. Export contact-relationship-type setup data with shared.setup-export.task-level-export.
3. Set the selected contact relationship type to enabled in the FSM package.
4. Validate the FSM package with shared.validation.setup-data-validator.
5. Import the approved ZIP with core.data-loader.
6. Verify the contact relationship type is active with a fresh Standard Lookup Codes REST read.

### Deactivate Service Request Contact Relationship Type

Deactivate an existing Service Request contact relationship type.

1. Read the requested ORA_SVC_CONTACT_REL_TYPE_CD lookup code with core.fusion-api.apps-common using LookupCodeFinder.
2. Export contact-relationship-type setup data with shared.setup-export.task-level-export.
3. Show "The Service Request contact relationship type will be deactivated. Do you want to continue?" and wait for confirmation.
4. Set the selected contact relationship type to disabled in the FSM package.
5. Validate the FSM package with shared.validation.setup-data-validator.
6. Import the approved ZIP with core.data-loader.
7. Verify the contact relationship type is inactive with a fresh Standard Lookup Codes REST read.

### Delete Service Request Contact Relationship Type

Delete a Service Request contact relationship type.

Not supported. Contact-relationship-type deletion is not supported through this FSM workflow; deactivate the contact relationship type instead.
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
- Setup task name: `Manage Service Request Contact Relationship Types`
- Setup task code: `ORA_SVC_MANAGE_SERVICE_REQUEST_CONTACT_RELATIONSHIP_TYPES`


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

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Service Request Contact Relationship Types` under `Service Request`.
