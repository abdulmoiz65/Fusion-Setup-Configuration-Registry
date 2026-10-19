---
task_code: "ORA_SVC_MANAGE_SR_KNOWLEDGE_PROFILE_OPTIONS"
task_name: "Manage Service Request Knowledge Profile Options"
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

# Manage Service Request Knowledge Profile Options

## Setup Task Metadata

- Task name: `Manage Service Request Knowledge Profile Options`
- Task code: `ORA_SVC_MANAGE_SR_KNOWLEDGE_PROFILE_OPTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## FSM Contract

### FND_APP_PROFILE_OPTION

- `ProfileOptionName`: Set to SVC_ENABLE_KNOWLEDGE_IN_SR. Do not create a profile option definition through this workflow.
- `ApplicationId`: Retain the exported application ID for SVC_ENABLE_KNOWLEDGE_IN_SR.
- `ModuleId`: Retain the exported module ID.
- `Description`: Retain the exported description.
- `SqlValidation`: Retain the exported SQL validation.
- `StartDateActive`: Retain the exported start date.
- `EndDateActive`: Retain the exported end date.
- `UserProfileOptionName`: Retain the exported user-facing name.
- `CreationDate`: Retain the exported value.
- `CreatedBy`: Retain the exported value.
- `LastUpdateDate`: Retain the exported value unless the same approved package updates the profile option definition.
- `LastUpdatedBy`: Retain the exported value unless the same approved package updates the profile option definition.
- `LastUpdateLogin`: Retain the exported value.

### ORA_FND_APP_PROFILE_OPTION_LEVEL

- `FND_APP_PROFILE_OPTION.ProfileOptionName`: Set to SVC_ENABLE_KNOWLEDGE_IN_SR.
- `FND_APP_PROFILE_OPTION.ApplicationId`: Retain the exported application ID.
- `LevelName`: Retain the exported supported profile level. When no supported level is supplied, default to SITE; the same-task export shows SITE as the supported updateable profile level.
- `UpdateableFlag`: Retain the exported value. Do not enable PRODUCT or USER because the export marks those levels as not updateable and not enabled.
- `EnabledFlag`: Retain the exported value. Do not enable PRODUCT or USER because the export marks those levels as not updateable and not enabled.
- `CreationDate`: Retain the exported value.
- `CreatedBy`: Retain the exported value.
- `LastUpdateDate`: Retain the exported value.
- `LastUpdatedBy`: Retain the exported value.
- `LastUpdateLogin`: Retain the exported value.

### FND_APP_PROFILE_VALUE

- `FND_APP_PROFILE_OPTION.ProfileOptionName`: Set to SVC_ENABLE_KNOWLEDGE_IN_SR.
- `FND_APP_PROFILE_OPTION.ApplicationId`: Retain the exported application ID.
- `LevelName`: Retain the exported supported profile level. When no supported level is supplied, default to SITE.
- `LevelValue`: Retain the exported level value. When LevelName defaults to SITE and no level value is supplied, default to SITE.
- `ProfileOptionValue`: Derive the value from the customer's stated intent: Y to enable Knowledge in Service Requests or N to disable it. Present the derived value for approval before import. Set Y only after Knowledge Management scope and the required administrator role are confirmed; stop when the intent is insufficient.
- `CreationDate`: Retain the exported value.
- `CreatedBy`: Retain the exported value.
- `LastUpdateDate`: Set to the current date and time for an approved value update.
- `LastUpdatedBy`: Set to the current user for an approved value update.
- `LastUpdateLogin`: Retain the exported value unless same-task package evidence requires an update.
## Purpose

Manage the Service Request Knowledge profile-option values that control Knowledge availability in Service Requests.
## Use Cases

### View Service Request Knowledge Profile Option Value

View the effective value of a selected Service Request Knowledge profile option for the current authenticated user session.

1. Read the selected profile option with core.fusion-api.apps-common using the Profile Values REST resource and ProfileOptionNameFinder.
2. Return ProfileOptionName and the effective ProfileOptionValue for the current user session.

### View Service Request Knowledge Profile Option Values

View the effective values of the requested Service Request Knowledge profile options for the current authenticated user session.

1. Read each requested profile option with core.fusion-api.apps-common using the Profile Values REST resource.
2. Return ProfileOptionName and ProfileOptionValue for every resolved option; identify any option that is not REST exposed separately.
3. Do not infer a site or user value from a missing REST response.

### Update Service Request Knowledge Profile Option Value

Update an approved Service Request Knowledge profile option value at its supported profile level.

1. Confirm Knowledge Management is in scope and validate the selected profile option, value, and target profile level against documented semantics.
2. Read the current effective profile value with core.fusion-api.apps-common using the Profile Values REST resource when the option is REST exposed.
3. Export profile-option setup data with shared.setup-export.task-level-export.
4. Use the completed export of the same setup task as the package baseline; preserve its package structure and modify only the approved task-owned profile-value row.
5. Validate the FSM package with shared.validation.setup-data-validator.
6. Import the approved ZIP with core.data-loader.
7. Verify the effective updated value with a fresh Profile Values REST read when the option is REST exposed; otherwise verify the persisted value with a fresh task export.

### Create Service Request Knowledge Profile Option

Create a Service Request Knowledge profile option definition.

Not supported. This setup task manages Service Request Knowledge profile values; do not create profile option definitions through REST or FSM without a separately documented profile-option-definition workflow.

### Delete Service Request Knowledge Profile Option

Delete a Service Request Knowledge profile option definition.

Not supported. This setup task manages Service Request Knowledge profile values; do not delete profile option definitions through REST or FSM.
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
- Setup task name: `Manage Service Request Knowledge Profile Options`
- Setup task code: `ORA_SVC_MANAGE_SR_KNOWLEDGE_PROFILE_OPTIONS`


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

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Service Request Knowledge Profile Options` under `Service Request`.
