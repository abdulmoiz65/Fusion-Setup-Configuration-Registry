---
task_code: "ORA_SVC_MANAGE_ACTION_CATEGORIES_FOR_ACTION_PLANS"
task_name: "Manage Action Categories for Action Plans"
parent_skill_id: "cx.service.action-plans"
pillar: "CX"
offering: "Service"
functional_area: "Action Plans"
functional_area_code: "ORA_SVC_ACTION_PLANS"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Action Categories for Action Plans

## Setup Task Metadata

- Task name: `Manage Action Categories for Action Plans`
- Task code: `ORA_SVC_MANAGE_ACTION_CATEGORIES_FOR_ACTION_PLANS`
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

### Review Action Plan Action Categories

Review the Action Plans action-category lookup and its existing lookup codes before making a change.

1. Export Action Plans action categories with shared.setup-export.task-level-export.
2. Review the ORA_SVC_AP_ACTION_CATEGORY_CD lookup codes and their code, display sequence, enabled state, start and end dates, meaning, description, tag, and descriptive flexfield values.

### Create Action Plan Action Category

Create an Action Plans action-category lookup code.

1. Export Action Plans action categories with shared.setup-export.task-level-export.
2. Use the completed export of the same setup task as the package baseline and add only the approved lookup-code row and required task-owned values.
3. Validate the new code does not duplicate an existing lookup code and that its requested dates and enabled state are compatible with the approved category design.
4. Validate the FSM package with shared.validation.setup-data-validator.
5. Import the approved ZIP with core.data-loader.
6. Verify the created lookup code with a fresh export.

### Update Action Plan Action Category

Update an existing Action Plans action-category lookup code without changing its identity.

1. Export Action Plans action categories with shared.setup-export.task-level-export.
2. Retain the selected lookup code and update only approved display sequence, enabled state, dates, meaning, description, tag, or descriptive flexfield values.
3. Validate the FSM package with shared.validation.setup-data-validator.
4. Import the approved ZIP with core.data-loader.
5. Verify the updated lookup code with a fresh export.

### Disable Action Plan Action Category

Disable an existing Action Plans action-category lookup code while retaining it for historical reference.

1. Export Action Plans action categories with shared.setup-export.task-level-export.
2. Retain the selected lookup-code identity and change only its enabled state and any approved effective end date.
3. Validate the FSM package with shared.validation.setup-data-validator.
4. Import the approved ZIP with core.data-loader.
5. Verify the disabled lookup code with a fresh export.
## Purpose

Manage categories for an action to be used in service action plans.
## FSM Contract

### FND_APP_STANDARD_LOOKUP

- `LookupType`: Set to ORA_SVC_AP_ACTION_CATEGORY_CD.
- `Meaning`: Retain the exported lookup meaning.
- `Description`: Retain the exported lookup description.
- `CreatedBy`: Retain the exported audit value.
- `CreationDate`: Retain the exported audit value.
- `LastUpdatedBy`: Retain the exported audit value.
- `LastUpdateDate`: Retain the exported audit value.
- `LastUpdateLogin`: Retain the exported audit value when required by the package contract.
- `ModuleId`: Retain the exported module identity.
- `CustomizationLevel`: Retain the exported customization level.
- `RestAccessSecured`: Retain the exported REST access setting.
- `BossAppPackageName`: Retain the exported value.
- `BossAppPackageVersion`: Retain the exported value.
- `BossModuleName`: Retain the exported value.
- `BossIdentifier`: Retain the exported value.

### ORA_FND_APP_STANDARD_LOOKUP_CODE

- `FND_APP_STANDARD_LOOKUP.LookupType`: Set to ORA_SVC_AP_ACTION_CATEGORY_CD as the parent linkage.
- `LookupCode`: Populate a unique approved customer-owned code; do not use the reserved ORA prefix.
- `Meaning`: Populate the approved category meaning.
- `Description`: Populate only the approved category description.
- `EnabledFlag`: Set to the approved enabled state.
- `StartDateActive`: Populate only the approved effective start date.
- `EndDateActive`: Populate only the approved effective end date.
- `DisplaySequence`: Populate only the approved display sequence.
- `CreatedBy`: Retain the exported audit value when required by the package contract.
- `CreationDate`: Retain the exported audit value when required by the package contract.
- `LastUpdatedBy`: Retain the exported audit value when required by the package contract.
- `LastUpdateDate`: Retain the exported audit value when required by the package contract.
- `LastUpdateLogin`: Retain the exported audit value when required by the package contract.
- `Tag`: Populate only the approved tag or descriptive flexfield value.
## Guard Rails

1. Require an authenticated Fusion user context before any Fusion operation; use `core.auth.fusion-oauth-authentication`.
2. Do not use `core.fusion-api.rest-api-client` to create or update records. The only deletion exception is no-ship test rollback of independently created, group-owned action-category codes through `standardLookups/ORA_SVC_AP_ACTION_CATEGORY_CD/child/lookupCodes/{LookupCode}` after separate explicit approval and a fresh read-back. This exception must never target a pre-existing code, substitute for FSM restoration, or be used for normal setup work.
3. Do not use `shared.setup-import.task-level-import` to create, update, or delete records.
## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Service`
- Functional area / Setup Object: `Action Plans`
- Setup task name: `Manage Action Categories for Action Plans`
- Setup task code: `ORA_SVC_MANAGE_ACTION_CATEGORIES_FOR_ACTION_PLANS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Action Categories for Action Plans` under `Action Plans`.
