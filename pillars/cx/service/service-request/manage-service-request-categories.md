---
task_code: "ORA_SVC_SERVICE_REQUEST_CATEGORIES"
task_name: "Manage Service Request Categories"
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

# Manage Service Request Categories

## Setup Task Metadata

- Task name: `Manage Service Request Categories`
- Task code: `ORA_SVC_SERVICE_REQUEST_CATEGORIES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## FSM Contract

### ORA_SVC_CATEGORY

- `StripeCd`: Set to the applicable Service Request category stripe, such as ORA_SVC_CRM, ORA_SVC_HCM, ORA_SVC_HRHD, or ORA_SVC_ISR. Retain the exported value for an existing category.
- `CategoryShortName`: Set to the unique category short name within the selected stripe and business unit. Retain the exported value for an existing category.
- `BusinessUnitName`: Set to the selected business unit name. Retain the exported value for an existing category.
- `CategoryName`: Set to the category display name. CategoryName is required for a new category; ask the customer when it is not provided.
- `CategoryCode`: Set to the unique category code. Retain the exported value for an existing category; for a new generated category, derive the code from the approved short name, stripe, and business unit only when the baseline package establishes that convention. Generate codes in uppercase, using only letters, digits, and underscores; normalize spaces, hyphens, and other separators to underscores and collapse repeated underscores.
- `ParentCategoryCode`: Set to the optional parent category code for a child category. Leave blank for a top-level category.
- `EnabledFlag`: Set to Y to enable or N to deactivate the category. When no value is provided, default to Y.
- `DeletedFlag`: Retain the exported value or set to N. Do not set to Y through this workflow.
- `CSSFlag`: Retain the exported value for the applicable category stripe and business unit.
- `BUOrgId`: Set to the selected business-unit organization ID. Retain the exported value for an existing category.
- `Depth`: Retain the exported hierarchy depth for existing categories. Leave blank for a new category unless same-task baseline evidence requires a value.
- `Hierarchy`: Retain the exported hierarchy path for existing categories. Leave blank for a new category unless same-task baseline evidence requires a value.
- `ChildCountParentCategoryId`: Retain the exported value for existing categories. Leave blank for a new category unless same-task baseline evidence requires a value.
- `CategoryIdHierarchy`: Retain the exported category-ID hierarchy for existing categories. Leave blank for a new category unless same-task baseline evidence requires a value.
- `RootCategoryCode`: Set to the root category code for a child category; set to the category code for a top-level category. Retain the exported value for an existing category.
- `CategoryDescription`: Set to the optional category description.

### ORA_SEVICE_CATEGORY_ASSOCIATION

- `StripeCd`: Set to the child category's stripe. Retain the exported value for an existing relationship.
- `CategoryShortName`: Set to the child category's short name.
- `BUOrgId`: Set to the child category's business-unit organization ID.
- `CategoryShortNameParent`: Set to the parent category's short name for a child category. Leave blank for a top-level category.
- `BUOrgIdParent`: Set to the parent category's business-unit organization ID for a child category. Leave blank for a top-level category.
- `StripeCdParent`: Set to the parent category's stripe for a child category. Leave blank for a top-level category.
## Purpose

Maintain the Service Request category hierarchy used for classification and support routing.
## Use Cases

### Review Service Request Categories

View the current category hierarchy before creating or changing a category.

1. Read Service Request Categories with core.fusion-api.rest-api-client.
2. Export categories with shared.setup-export.task-level-export when an FSM baseline is required.

### Review Active And Inactive Categories

Determine which configured categories are available or unavailable for Service Request use.

1. Read Service Request Categories with core.fusion-api.rest-api-client.
2. Export categories with shared.setup-export.task-level-export when an FSM baseline is required.

### Create Top Level Service Request Category

Create a root category for Service Request classification and routing.

1. Export categories with shared.setup-export.task-level-export.
2. Add the top-level category; do not add an association row.
3. Validate the FSM package with shared.validation.setup-data-validator.
4. Import the approved ZIP with core.data-loader.
5. Verify the category with shared.setup-export.task-level-export.

### Create Child Service Request Category

Create a child Service Request category.

1. Export categories with shared.setup-export.task-level-export.
2. Add the child and required relationship rows using the exported parent identity.
3. Validate the FSM package with shared.validation.setup-data-validator.
4. Import the approved ZIP with core.data-loader.
5. Verify the child category with shared.setup-export.task-level-export.

### Update Service Request Category

Update a Service Request category.

1. Export categories with shared.setup-export.task-level-export.
2. Update approved values and retain required child relationships.
3. Validate the FSM package with shared.validation.setup-data-validator.
4. Import the approved ZIP with core.data-loader.
5. Verify the update with shared.setup-export.task-level-export.

### Activate Service Request Category

Activate a Service Request category.

1. Export categories with shared.setup-export.task-level-export.
2. Set the category to active.
3. Validate the FSM package with shared.validation.setup-data-validator.
4. Import the approved ZIP with core.data-loader.
5. Verify the category is active with shared.setup-export.task-level-export.

### Deactivate Service Request Category

Deactivate a Service Request category.

1. Export categories with shared.setup-export.task-level-export.
2. Show "The category will be deactivated. Do you want to continue?" and wait for confirmation.
3. Set the category to inactive.
4. Validate the FSM package with shared.validation.setup-data-validator.
5. Import the approved ZIP with core.data-loader.
6. Verify the category is inactive with shared.setup-export.task-level-export.

### Delete Service Request Category

Delete a Service Request category.

Not supported. Category deletion is not supported through this flow. Delete the category from the UI.
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
- Setup task name: `Manage Service Request Categories`
- Setup task code: `ORA_SVC_SERVICE_REQUEST_CATEGORIES`

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
