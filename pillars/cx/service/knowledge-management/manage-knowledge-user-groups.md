---
task_code: "ORA_CSO_USER_GROUPS_MGMT"
task_name: "Manage Knowledge User Groups"
parent_skill_id: "cx.service.knowledge-management"
pillar: "CX"
offering: "Service"
functional_area: "Knowledge Management"
functional_area_code: "ORA_CSO_KNOWLEDGE_MANAGEMENT"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Knowledge User Groups

## Setup Task Metadata

- Task name: `Manage Knowledge User Groups`
- Task code: `ORA_CSO_USER_GROUPS_MGMT`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``


## FSM Contract

### ORA_CSO_USER_GROUP_OBJECT

- `referenceKey`: Use the exact exported user-group reference key as the root identity and as the parent linkage for localized-attribute rows. For an approved new user group, use the approved unique reference key; retain the existing exported key for every unchanged user group.
- `businessUnitIds`: Retain the exported value for an existing user group. For an approved new or updated custom user group, populate only the approved valid Service Business Unit identifier when Knowledge Management Business Unit Support is enabled; otherwise retain the export's empty representation.
- `stripeCd`: Retain the exported value for an existing user group. For an approved new or updated user group, resolve the proper exported stripe code for the selected ISR, Help Desk, or Service context. Use only ORA_SVC_CRM, ORA_SVC_HRHD, or ORA_SVC_ISR; do not use a display label as a stripe code or infer a substitute value.
- `objectId`: Retain the exported value for an existing user group. Leave it blank for an approved new user group so Fusion generates the value; do not add the REST-only recordId field to this FSM CSV object.

### ORA_KNOWLEDGE_USER_GROUP_LOCALIZED_ATTRIBUTE_OBJECT

- `ORA_CSO_USER_GROUP_OBJECT.referenceKey`: Link every localized-attribute row to its user-group root with that root's exact exported or approved reference key. Do not add an orphan localized-attribute row.
- `localeId`: Use the exact locale representation from the same-task export for each approved localized row; do not infer a locale ID from a display name.
- `name`: Retain the exported localized name unless it is an approved user-group name change. Provide the approved localized name for every required locale.
- `description`: Retain the exported localized description unless it is an approved user-group description change. Provide the approved localized description for every required locale.
## Guard Rails

1. Require an authenticated Fusion user context before any Fusion operation; use `core.auth.fusion-oauth-authentication`.
2. Do not use `core.fusion-api.rest-api-client` to create, update, or delete records.
3. Do not use `shared.setup-import.task-level-import` to create, update, or delete records.
## Purpose

Manage Knowledge user groups, including their department, name, reference key, description, and translations.
## Use Cases

### View Knowledge User Groups

Review Knowledge user groups.

1. Export Knowledge user groups with shared.setup-export.task-level-export.

### Create Knowledge User Group

Create a Knowledge user group.

1. Export Knowledge user groups with shared.setup-export.task-level-export.
2. Generate a unique referenceKey using only uppercase letters, numbers, and underscores.
3. Leave objectId blank for a new user group so Fusion generates it. Don't add the REST-only recordId field to the FSM CSV.
4. When Knowledge Management Business Unit Support is enabled, populate businessUnitIds with the valid Service Business Unit identifier; otherwise leave it empty.
5. Add the user group with its required Department and include its localized Name and Description for every active locale.
6. Validate the FSM package with shared.validation.setup-data-validator.
7. Import the approved ZIP with core.data-loader.
8. Verify the user group with a fresh export.

### Edit Knowledge User Group

Update an existing Knowledge user group.

1. Export Knowledge user groups with shared.setup-export.task-level-export.
2. Preserve the selected custom user group's businessUnitIds; when Knowledge Management Business Unit Support is enabled, a user group must remain associated with a valid Service Business Unit.
3. Update the selected custom user group's Name, Reference Key, Description, and localized values for every active locale as required.
4. Validate the FSM package with shared.validation.setup-data-validator.
5. Import the approved ZIP with core.data-loader.
6. Verify the user group with a fresh export.

### Delete Knowledge User Group

Remove a Knowledge user group.

Not supported. Knowledge user group deletion is not supported through either the FSM package flow or the REST use-case flow. Do not use a direct REST DELETE as a substitute for the unsupported operation.
## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Service`
- Functional area / Setup Object: `Knowledge Management`
- Setup task name: `Manage Knowledge User Groups`
- Setup task code: `ORA_CSO_USER_GROUPS_MGMT`




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

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Knowledge User Groups` under `Knowledge Management`.
