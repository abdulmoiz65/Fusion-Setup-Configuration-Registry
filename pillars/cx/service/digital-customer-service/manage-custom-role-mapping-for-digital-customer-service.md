---
task_code: "ORA_CREATE_DIGITAL_CUSTOMER_SERVICE_CUSTOM_ROLE_MAPPING"
task_name: "Manage Custom Role Mapping for Digital Customer Service"
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

# Manage Custom Role Mapping for Digital Customer Service

## Setup Task Metadata

- Task name: `Manage Custom Role Mapping for Digital Customer Service`
- Task code: `ORA_CREATE_DIGITAL_CUSTOMER_SERVICE_CUSTOM_ROLE_MAPPING`
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

### View Custom Role Mappings For Digital Customer Service

View existing Digital Customer Service mappings between custom self-service roles and custom identity provider job roles.

1. Export Manage Custom Role Mapping for Digital Customer Service setup data with shared.setup-export.task-level-export when a screen-equivalent list of existing mappings is required.
2. Return the mapped Self-Service Role and Job Role values for each exported mapping when those fields are present in the export.
3. Treat ready-to-use Digital Customer Service self-service roles, such as User, Account Administrator, and Account Manager, as ineligible for custom identity provider role mapping.
4. Use Manage Self-Service Relationship Type Standard Lookup, Security Console role setup, and Identity Cloud Service group setup evidence when the caller needs to confirm role prerequisites before a mapping change.

### View Custom Role Mapping For Digital Customer Service

View one existing custom self-service role to identity provider job-role mapping before changing related setup.

1. Export Manage Custom Role Mapping for Digital Customer Service setup data with shared.setup-export.task-level-export and filter by the requested Self-Service Role or Job Role value.
2. Require exactly one matching exported mapping before preparing a mapping-dependent change; stop when no matching row or multiple matching rows are returned.
3. Return the selected mapping's Self-Service Role and Job Role values when present in the export.
4. Do not infer a mapping from user-role assignments created through the selfServiceRoles REST API; use this setup task's mapping export as the source of truth for role mappings.

### Create Custom Role Mapping For Digital Customer Service

Create a mapping between one custom Digital Customer Service self-service role and one custom identity provider job role.

1. Validate that the requested self-service role is a custom role created as a code in the ORA_SVC_CSS_REL_TYPE_CD lookup type through Manage Self-Service Relationship Type Standard Lookup.
2. Validate that the requested job role is a custom identity provider role and that the matching Identity Cloud Service group exists with the Fusion Service role code as its external ID.
3. Reject mappings for ready-to-use self-service roles because ready-to-use self-service roles can't be mapped to identity provider roles.
4. Reject the request when the selected custom self-service role is already mapped to an identity provider role, because a custom self-service role can be mapped to only one custom identity provider role.
5. Confirm the exact Self-Service Role and Job Role values before packaging the change.
6. Export Manage Custom Role Mapping for Digital Customer Service setup data with shared.setup-export.task-level-export.
7. Use the completed export of the same setup task as the package baseline; preserve its package structure and add only the approved custom role mapping row.
8. Validate the FSM package with shared.validation.setup-data-validator.
9. Import the approved ZIP with core.data-loader.
10. Verify the created mapping with a fresh task export before using the selfServiceRoles REST API to grant the custom self-service role to a user.

### Update Custom Role Mapping For Digital Customer Service

Change an existing custom self-service role to identity provider job-role mapping.

Not supported. Oracle's documented Manage Custom Role Mapping for Digital Customer Service workflow supports viewing existing mappings and creating new mappings; do not update an existing mapping unless current task export evidence and task-specific documentation provide an approved update path.

### Delete Custom Role Mapping For Digital Customer Service

Delete a custom self-service role to identity provider job-role mapping.

Not supported. Oracle's documented Manage Custom Role Mapping for Digital Customer Service workflow supports viewing existing mappings and creating new mappings; do not delete a mapping unless current task export evidence and task-specific documentation provide an approved delete path.
## Purpose

Create mappings between custom self-service roles and identity provider job roles.
## FSM Contract

### ORA_CUSTOM_SELF_SERVICE_ROLE_MAPPINGS

- `IdpRoleCode`: Set to the approved existing custom identity provider job role code, not its display name. Verify that the matching Identity Cloud Service group exists with this Fusion Service role code as its external ID.
- `CssRoleCd`: Set to the approved existing custom self-service relationship code in ORA_SVC_CSS_REL_TYPE_CD, not its display meaning. Reject ready-to-use roles and any custom role already mapped to an identity provider role. Create only a new approved mapping; do not update or delete an existing mapping through this workflow.
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
- Setup task name: `Manage Custom Role Mapping for Digital Customer Service`
- Setup task code: `ORA_CREATE_DIGITAL_CUSTOMER_SERVICE_CUSTOM_ROLE_MAPPING`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Custom Role Mapping for Digital Customer Service` under `Digital Customer Service`.
