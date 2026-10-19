---
task_code: "ORA_MANAGE_PROXY_USER_CONFIGURATION_DATA"
task_name: "Manage Proxy User Configuration Data"
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

# Manage Proxy User Configuration Data

## Setup Task Metadata

- Task name: `Manage Proxy User Configuration Data`
- Task code: `ORA_MANAGE_PROXY_USER_CONFIGURATION_DATA`
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

### View Proxy User Configuration Data

View Digital Customer Service proxy user configuration rows and their URL patterns, HTTP methods, IdP roles, proxy-user keys, priority, and active state.

1. Export proxy user configuration data with shared.setup-export.task-level-export when a screen-equivalent list of task-owned rows is required.
2. Return URL Pattern, HTTP Methods, IdP User Roles, Proxy User Key, Priority, Active, Predefined, and Allow Identity Propagation when those fields are present in the export.
3. Do not return or persist proxy user passwords, client secrets, tokens, or private keys from any source.
4. Note that proxy user configuration data is cached and changes might not be reflected until the SVC_CSS_PUDS_CACHE_DURATION profile option cache duration expires.

### View Proxy User Configuration Row

View one proxy user configuration row before changing it.

1. Export proxy user configuration data with shared.setup-export.task-level-export and filter by the requested URL Pattern, HTTP Method, IdP User Role, Proxy User Key, or Active value.
2. Require exactly one matching exported row before preparing a row-level change; stop when no matching row or multiple matching rows are returned.
3. Return the selected row's URL Pattern, HTTP Methods, IdP User Roles, Proxy User Key, Priority, Active, Predefined, and Allow Identity Propagation fields when available.
4. Do not disclose or persist password values; report only whether credential update is required when that can be determined without exposing the secret.

### Create Proxy User Configuration Data

Create a proxy user configuration row for an approved URL pattern, HTTP method set, IdP user role, proxy-user key, priority, and active state.

1. Validate the requested URL pattern, HTTP methods, IdP user role, proxy user key, priority, active flag, and allow identity propagation value against the setup-task screen shape and documented allowlist rules.
2. Confirm that only allowlisted resources, or documented Application Composer custom objects, are being exposed to anonymous users; stop when the URL pattern would expose an unsupported resource.
3. Require proxy user keys to follow the documented PUK#_ naming convention when a new key is requested.
4. Confirm the exact URL Pattern, HTTP Methods, IdP User Roles, Proxy User Key, Priority, Active value, and Allow Identity Propagation value before packaging the change.
5. Export proxy user configuration data with shared.setup-export.task-level-export.
6. Use the completed export of the same setup task as the package baseline; preserve its package structure and add only the approved proxy user configuration row.
7. Validate the FSM package with shared.validation.setup-data-validator.
8. Import the approved ZIP with core.data-loader.
9. Verify the created row with a fresh task export and, when immediate runtime behavior is required, clear the PUDS cache through the SVC_CSS_PUDS_CACHE_DURATION profile option workflow.

### Update Proxy User Configuration Data

Update an existing proxy user configuration row's HTTP methods, IdP roles, proxy-user key, priority, active state, or identity-propagation setting.

1. Export proxy user configuration data with shared.setup-export.task-level-export and require exactly one matching row for the requested URL pattern and discriminator fields.
2. Stop before changing predefined rows unless the requested update is limited to documented editable fields such as priority, proxy-user credentials, active state, or identity propagation.
3. Validate the approved field changes against the setup-task screen shape and documented allowlist rules.
4. Use the completed export of the same setup task as the package baseline; retain the selected row's exported identity and modify only approved non-secret fields.
5. Validate the FSM package with shared.validation.setup-data-validator.
6. Import the approved ZIP with core.data-loader.
7. Verify the updated row with a fresh task export and, when immediate runtime behavior is required, clear the PUDS cache through the SVC_CSS_PUDS_CACHE_DURATION profile option workflow.

### Set Proxy User Credentials

Set or rotate credentials for the documented Digital Customer Service proxy user keys.

1. Limit credential setup to an approved proxy user key such as PUK#_ANONYMOUS_USER, PUK#_SELF_SERVICE_USER, or PUK#_SELF_SERVICE_ACCOUNT_ADMIN unless documentation or same-task export evidence confirms another key.
2. Because the same proxy user key can be used by multiple URL patterns, require exactly one representative row for the selected proxy user key before opening a credential change.
3. Allow Proxy User Name to be confirmed as non-secret setup data, but treat Password and Retype Password as transient runtime-only values.
4. Do not write proxy user passwords, password placeholders, client secrets, tokens, or private keys to metadata, FSM packages, logs, diagnostics, exports, or project artifacts.
5. After the credential is set through an approved runtime workflow, verify only the non-secret row configuration and remind the caller that cached proxy user configuration data might not reflect the change until the SVC_CSS_PUDS_CACHE_DURATION cache expires.

### Activate Proxy User Configuration Data

Activate an existing proxy user configuration row.

1. Export proxy user configuration data with shared.setup-export.task-level-export and require exactly one matching row.
2. Set the selected row's Active value to enabled in the FSM package.
3. Validate the FSM package with shared.validation.setup-data-validator.
4. Import the approved ZIP with core.data-loader.
5. Verify the row is active with a fresh task export and clear the PUDS cache through the SVC_CSS_PUDS_CACHE_DURATION profile option workflow when immediate behavior is required.

### Deactivate Proxy User Configuration Data

Deactivate an existing proxy user configuration row.

1. Export proxy user configuration data with shared.setup-export.task-level-export and require exactly one matching row.
2. Show "The proxy user configuration row will be deactivated. Do you want to continue?" and wait for confirmation.
3. Set the selected row's Active value to disabled in the FSM package.
4. Validate the FSM package with shared.validation.setup-data-validator.
5. Import the approved ZIP with core.data-loader.
6. Verify the row is inactive with a fresh task export and clear the PUDS cache through the SVC_CSS_PUDS_CACHE_DURATION profile option workflow when immediate behavior is required.

### Delete Proxy User Configuration Data

Delete a proxy user configuration row.

Not supported. Delete is outside the supported Manage Proxy User Configuration Data workflow; deactivate the row instead unless Oracle documentation provides a task-specific delete path.
## Purpose

Manage URL patterns and proxy-user keys used by Digital Customer Service proxy user data service access.
## FSM Contract

### ORA_PROXY_USER_CONFIGURATION

- `ConfigShortName`: Non-empty unique string business key for a new customer configuration, for example CUST_DCS_CATEGORY_GET. Use an approved customer-owned name and check for duplicates; do not use the SEED_ prefix or reuse an exported row identity. Retain the exact key on update.
- `ConfigType`: Use the literal ORA_CONFIG_PROXY_USER_DS for this task, as established by the same-task export. Do not use a client-credentials configuration type.
- `CreatedBy`: For a new row, supply the current authenticated user name when required by the package contract; retain the original creator on update. Do not copy a seeded creator.
- `HttpMethods`: Comma-separated uppercase HTTP method tokens with no spaces, for example GET,OPTIONS or OPTIONS,POST, enclosed as one quoted CSV cell. Exported examples include DELETE, GET, OPTIONS, and POST; these examples are not an exhaustive allowlist. Supply only methods supported for the approved endpoint; verify additional methods before use.
- `IdpUserRoles`: Exact existing IdP role code as a string, for example ORA_SVC_CUSTOMER_SELF_SERVICE_USER_ABSTRACT. The inspected export contains single-role values; use one resolved role per new row unless a task-specific multi-role serialization is separately established. Do not assume the HttpMethods delimiter applies to this field.
- `LastUpdateLogin`: Retain the exported value for an existing row. Omit for a new row only when same-task evidence or supported validation confirms it is generated or optional.
- `LastUpdatedBy`: For an approved create or update, supply the current authenticated user name when required by the package contract. Retain the existing value for unchanged rows.
- `Priority`: Integer priority in base-10 form, for example 1 or 10; 1 has the highest priority. Require an approved priority for a new row, considering overlapping URL patterns. Retain the existing priority unless an update is requested.
- `ProxyUserKey`: Set to the approved proxy user key. A newly requested key must begin with PUK#_ and must have its credentials configured through the approved runtime credential workflow; do not include passwords or password placeholders in the FSM package.
- `UrlPattern`: String URL path pattern, for example /crmRestApi/resources/.*/categories. Preserve the pattern syntax; do not URL-encode its metacharacters or substitute a full host URL. Expose only documented allowlisted resources or supported Application Composer custom objects to anonymous users.
- `ModuleId`: Exact module identifier string. The same-task export uses 2396C82BEC13F1E1E050F00A172047A9; use it as a template-derived candidate only after confirming the same module exists and applies in the target environment. An empty configuration export does not prevent resolving the module separately.
- `ActiveFlagNum`: Allowed values are 1 (active) and 0 (inactive), confirmed in the same-task export. Set 1 with ActiveFlag true or 0 with ActiveFlag false. Require the approved active state for a new row.
- `ActiveFlag`: Allowed values are lowercase true and false. Set true with ActiveFlagNum 1 or false with ActiveFlagNum 0. Deactivation of an existing row follows the use-case confirmation; do not silently activate a new row.
- `SupportIdentityPropagationNum`: Use 1 with SupportIdentityPropagation true or 0 with false. The export directly demonstrates 1/true; 0/false follows the object's paired numeric/Boolean encoding and must pass package validation. Require an explicit approved choice for a new row.
- `SupportIdentityPropagation`: Allowed values are lowercase true and false per the FSM Boolean type. Set the matching numeric companion. Do not enable identity propagation by default; require an approved choice even when the export is empty.
- `OutOfTheBoxFlagNum`: Allowed values are 1 (predefined) and 0 (customer-owned), confirmed in the same-task export. Set 0 for a new customer row and pair it with OutOfTheBoxFlag false. Retain both flags on update; never convert seeded ownership.
- `OutOfTheBoxFlag`: Allowed values are lowercase true (predefined) and false (customer-owned). Set false for a new customer row and pair it with OutOfTheBoxFlagNum 0. Retain both flags on update and obey predefined-row edit restrictions.
- `ProxyUserName`: Set to the approved existing proxy user name associated with ProxyUserKey, or retain the exported value when unchanged. This non-secret field does not set or rotate a password; credential values remain outside the FSM contract.
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
- Setup task name: `Manage Proxy User Configuration Data`
- Setup task code: `ORA_MANAGE_PROXY_USER_CONFIGURATION_DATA`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Proxy User Configuration Data` under `Digital Customer Service`.
