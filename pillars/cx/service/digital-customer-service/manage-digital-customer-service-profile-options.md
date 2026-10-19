---
task_code: "ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS"
task_name: "Manage Digital Customer Service Profile Options"
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

# Manage Digital Customer Service Profile Options

## Setup Task Metadata

- Task name: `Manage Digital Customer Service Profile Options`
- Task code: `ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS`
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

### View Digital Customer Service Profile Option List

View the Digital Customer Service profile options available in the setup task and the values configured for selected options.

1. Export Digital Customer Service profile-option setup data with shared.setup-export.task-level-export when a screen-equivalent list of task-owned profile options is required.
2. Return Profile Option Code, Profile Display Name, Application Module, Start Date, End Date, and Description for each exported profile option.
3. For selected profile options, return Profile Level, Product Name, User Name, and Profile Value from the profile-values child rows.
4. Treat profile options shown on the setup screen, such as SVC_CSS_SEND_WELCOME_EMAIL, ORA_SVC_CSS_SELF_REG_B2C_AUTO_APPROVE, SVC_CHAT_ANONYMOUS_ACCESS_ENABLED, ORACLE.ADF.VIEW.ALLOWED_ORIGINS, SVC_CHAT_INLAYS_ACCESS_ENABLED, FND_IDP_PROXY_USER_WHITELIST, CORS_ACCESS_CONTROL_ALLOW_HEADERS, SVC_CSS_REG_CONT_MAP, SVC_CSS_REG_FLD_CONTACT, SVC_CSS_SELF_REGISTRATION, and SVC_CSS_SELF_REG_AUTO_APPROVE, as candidates for this task only after they are confirmed by same-task export evidence or documentation.
5. Note that the setup screen shows SVC_CSS_SEND_WELCOME_EMAIL with a Site-level profile value row when selected.

### View Digital Customer Service Profile Option Value

View the effective value of a selected Digital Customer Service profile option for the current authenticated user session.

1. Read the selected profile option with core.fusion-api.apps-common using the Profile Values REST resource and ProfileOptionNameFinder when the option is REST exposed.
2. Return ProfileOptionName and the effective ProfileOptionValue for the current user session.
3. Stop and explain that the option must be included in the ORA_FND_AUTH_REST_ACCESS profile category before it can be returned by the authenticated Profile Values REST resource.
4. Use a fresh same-task export instead of inference when a site, product, or user-level persisted value is required and the effective REST response is unavailable.

### View Digital Customer Service Profile Option Values

View the effective values of the requested Digital Customer Service profile options for the current authenticated user session.

1. Read each requested profile option with core.fusion-api.apps-common using the Profile Values REST resource when the option is REST exposed.
2. Return ProfileOptionName and ProfileOptionValue for every resolved option; identify any option that is not REST exposed separately.
3. Do not infer a site, product, or user value from a missing REST response.
4. Use same-task export evidence when the caller needs the screen-level profile-value rows, including Profile Level, Product Name, User Name, and Profile Value.

### Update Digital Customer Service Profile Option Value

Update an approved Digital Customer Service profile option value at its supported profile level.

1. Read the current effective profile value with core.fusion-api.apps-common using the Profile Values REST resource when the option is REST exposed.
2. Validate the selected profile option, value, and target profile level against the documented semantics, the setup-task screen shape, and the task export metadata.
3. Confirm the exact Profile Option Code, Profile Level, Product Name when applicable, User Name when applicable, and Profile Value to change. For example, the setup screen shows SVC_CSS_SEND_WELCOME_EMAIL as a Site-level value with a True or False drop-down.
4. Export profile-option setup data with shared.setup-export.task-level-export.
5. Use the completed export of the same setup task as the package baseline; preserve its package structure and modify only the approved task-owned profile-value row.
6. Validate the FSM package with shared.validation.setup-data-validator.
7. Import the approved ZIP with core.data-loader.
8. Verify the effective updated value with a fresh Profile Values REST read when the option is REST exposed; otherwise verify the persisted value with a fresh task export.

### Configure Digital Customer Service Registration Profile Options

Configure self-registration, approval, account, contact-mapping, sign-in, and role profile options used by Digital Customer Service registration.

1. Validate that each requested registration setting maps to a documented or same-task-exported profile option, such as SVC_CSS_SELF_REGISTRATION, SVC_CSS_SELF_REG_AUTO_APPROVE, ORA_SVC_CSS_SELF_REG_B2C_AUTO_APPROVE, SVC_CSS_ACCT_ADMIN_APPROVE, SVC_CSS_ACCT_KEY_FIELD, SVC_CSS_REG_CONT_MAP, SVC_CSS_REG_FLD_CONTACT, SVC_CSS_SIGN_IN_ATTR_NAME, SVC_CSS_IMP_SIGN_IN_ATTR_NAME, SVC_CSS_USER_ROLE_COMMON_NAME, SVC_CSS_ACCT_ADMIN_ROLE_COMMON_NAME, SVC_CSS_USER_CATEGORY, SVC_CSS_CONSUMER_USER_CATEGORY, SVC_CSS_ALLOW_CONTACT, or SVC_CSS_ALLOW_CONSUMER.
2. Resolve dependencies on account setup, identity provider, proxy user, and role setup before approving changes that alter registration behavior.
3. Follow update_digital_customer_service_profile_option_value for each approved value change.

### Configure Digital Customer Service Access Profile Options

Configure Digital Customer Service access-related profile options for chat, allowed origins, CORS headers, proxy-user whitelisting, and PUDS cache duration.

1. Validate that each requested access setting maps to a documented or same-task-exported profile option, such as SVC_CHAT_ANONYMOUS_ACCESS_ENABLED, SVC_CHAT_INLAYS_ACCESS_ENABLED, ORACLE.ADF.VIEW.ALLOWED_ORIGINS, FND_IDP_PROXY_USER_WHITELIST, CORS_ACCESS_CONTROL_ALLOW_HEADERS, or SVC_CSS_PUDS_CACHE_DURATION.
2. Confirm the exact allowed origin, header, whitelist, cache-duration, or Boolean value before packaging the change; do not persist credentials, tokens, client secrets, or private keys in the package evidence or diagnostics.
3. Follow update_digital_customer_service_profile_option_value for each approved value change.

### Create Digital Customer Service Profile Option Value

Add the first value for an existing Digital Customer Service profile option at a supported level when no value row exists.

1. Export the same setup task with shared.setup-export.task-level-export and resolve the existing profile-option definition and its enabled, updateable level.
2. Verify that no value row exists for the exact ProfileOptionName, ApplicationId, LevelName, and LevelValue combination; route an existing match to the update use case.
3. Construct a new FND_APP_PROFILE_VALUE row using fsm_contract.create_rules and value_formats, preserving required parent and level rows. A header-only value CSV is valid; do not create a profile-option definition.
4. Confirm the target level and option-specific encoded value derived from the customer's business intent.
5. Validate the FSM package with shared.validation.setup-data-validator.
6. Import the approved ZIP with core.data-loader.
7. Verify the persisted new value with a fresh same-task export; use Profile Values REST only as an additional effective-value check when exposed.

### Create Digital Customer Service Profile Option

Create a Digital Customer Service profile option definition.

Not supported. This setup task manages Digital Customer Service profile values; do not create profile option definitions through REST or FSM without a separately documented profile-option-definition workflow.

### Delete Digital Customer Service Profile Option

Delete a Digital Customer Service profile option definition.

Not supported. This setup task manages Digital Customer Service profile values; do not delete profile option definitions through REST or FSM.
## Purpose

Configure Digital Customer Service registration and self-service profile options.
## FSM Contract

### FND_APP_PROFILE_OPTION

- `ProfileOptionName`: Set to the approved existing Digital Customer Service profile option name. Do not create a profile option definition through this workflow.
- `ApplicationId`: Retain the exported application ID for the selected existing profile option.
- `ModuleId`: Retain the exported module ID for the selected existing profile option.
- `Description`: Retain the exported description for the selected existing profile option.
- `SqlValidation`: Retain the exported SQL validation for the selected existing profile option.
- `StartDateActive`: Retain the exported start date for the selected existing profile option.
- `EndDateActive`: Retain the exported end date for the selected existing profile option.
- `UserProfileOptionName`: Retain the exported user-facing name for the selected existing profile option.
- `CreationDate`: Retain the exported value.
- `CreatedBy`: Retain the exported value.
- `LastUpdateDate`: Retain the exported value; profile option definition changes are outside this workflow.
- `LastUpdatedBy`: Retain the exported value; profile option definition changes are outside this workflow.
- `LastUpdateLogin`: Retain the exported value.

### ORA_FND_APP_PROFILE_OPTION_LEVEL

- `FND_APP_PROFILE_OPTION.ProfileOptionName`: Set to the approved existing Digital Customer Service profile option name.
- `FND_APP_PROFILE_OPTION.ApplicationId`: Retain the exported application ID for the selected existing profile option.
- `LevelName`: Allowed level codes in the export are SITE, PRODUCT, and USER. Use only a level enabled and updateable for the selected existing option. Default to SITE when supported, including when its value row is absent.
- `UpdateableFlag`: Allowed values are Y and N (uppercase strings), meaning updateable and not updateable. Retain the definition's value; only levels with UpdateableFlag Y and EnabledFlag Y can receive a new value. Do not enable unsupported levels.
- `EnabledFlag`: Allowed values are Y and N (uppercase strings), meaning enabled and disabled. Retain the definition's value; do not change level availability while creating a profile value.
- `CreationDate`: Retain the exported value.
- `CreatedBy`: Retain the exported value.
- `LastUpdateDate`: Retain the exported value.
- `LastUpdatedBy`: Retain the exported value.
- `LastUpdateLogin`: Retain the exported value.

### FND_APP_PROFILE_VALUE

- `FND_APP_PROFILE_OPTION.ProfileOptionName`: Set to the approved existing Digital Customer Service profile option name.
- `FND_APP_PROFILE_OPTION.ApplicationId`: Retain the exported application ID for the selected existing profile option.
- `LevelName`: Allowed level codes in the export are SITE, PRODUCT, and USER. Use only a level enabled and updateable for the selected existing option. Default to SITE when supported, including when its value row is absent.
- `LevelValue`: For SITE, use the literal SITE. For PRODUCT or USER, use the resolved internal level key in the task-supported string format. Retain an existing key on update; never invent a key or use a display name.
- `ProfileOptionValue`: String encoded according to the selected option, not a universal Boolean. SVC_CHAT_ANONYMOUS_ACCESS_ENABLED and SVC_CHAT_INLAYS_ACCESS_ENABLED use Y or N (YES_NO validation); SVC_CSS_SELF_REG_AUTO_APPROVE and SVC_CSS_USE_FA_AS_IDP use lowercase true or false (FND_TRUE_FALSE_TYPE validation). These encodings are established by the same-task exported SqlValidation and values. For all other options, resolve the option-specific validation and documented syntax before create or update; do not convert every Boolean-looking value to Y/N. Derive the approved value from business intent and present it before import.
- `CreationDate`: For a new value row, use the current timestamp in YYYY/MM/DD HH:mm:ss.fraction format when an audit value is required; retain the original value on update.
- `CreatedBy`: For a new value row, use the current authenticated user name when an audit value is required; retain the original creator on update.
- `LastUpdateDate`: For an approved create or update, use the current timestamp in YYYY/MM/DD HH:mm:ss.fraction format when an audit value is required.
- `LastUpdatedBy`: Set to the current user for an approved value update.
- `LastUpdateLogin`: Retain the exported login identifier on update. For a new row, omit only when documented or validated as generated/optional; do not copy another row's session identifier or use a fabricated default.
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
- Setup task name: `Manage Digital Customer Service Profile Options`
- Setup task code: `ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Digital Customer Service Profile Options` under `Digital Customer Service`.
