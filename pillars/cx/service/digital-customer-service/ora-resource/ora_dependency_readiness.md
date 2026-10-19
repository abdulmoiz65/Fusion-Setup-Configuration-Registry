# Dependency Readiness

## Required Dependency Order

| Task Code | Task Name | Sequence | Dependency | What Must Happen |
|---|---|---|---|---|
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | 10 | Digital Customer Service opt-in | Digital Customer Service must be enabled before the profile option task and work areas are expected to be available |
| ORA_SVC_MANAGE_CSS_ACCOUNT_SETUP_OPTS | Manage Digital Customer Service Account Setup Profile Options | 10 | Digital Customer Service opt-in | Digital Customer Service must be enabled before account setup profile options are configured |
| ORA_MANAGE_PROXY_USER_CONFIGURATION_DATA | Manage Proxy User Configuration Data | 10 | Self-Service Optimization prerequisites | Profile options, proxy users, and IDCS role or group setup must be ready before proxy user configuration rows are finalized |
| ORA_SVC_MANAGE_SELF_SERVICE_RELATIONSHIP_TYPE_STANDARD_LOOKUP | Manage Self-Service Relationship Type Standard Lookup | 10 | Custom role design | Confirm the custom self-service role names before creating lookup codes |
| ORA_CREATE_DIGITAL_CUSTOMER_SERVICE_CUSTOM_ROLE_MAPPING | Manage Custom Role Mapping for Digital Customer Service | 10 | Custom self-service role and identity-provider role | Create or identify both roles before mapping them |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | dcs_opt_in | Digital Customer Service opt-in | Yes | Profile option configuration is requested | Verify | Setup and Maintenance offering opt-in | | Profile option work areas depend on Digital Customer Service being enabled | Confirm Digital Customer Service is enabled in the Service offering | DigitalCustomerServiceEnabled: Yes |
| ORA_MANAGE_PROXY_USER_CONFIGURATION_DATA | Manage Proxy User Configuration Data | proxy_user_credentials | Proxy user credentials | Conditional | Proxy user key rows are created or edited | Verify | Live task UI only | | Passwords are required for proxy user keys but must not be persisted | Enter credentials only in the live UI/session and redact them from artifacts | ProxyUserCredentialEntered: Yes |
| ORA_CREATE_DIGITAL_CUSTOMER_SERVICE_CUSTOM_ROLE_MAPPING | Manage Custom Role Mapping for Digital Customer Service | custom_role_pair | Custom self-service role and identity-provider job role | Yes | Custom role mapping is requested | Verify | Security Console, IDCS, and standard lookup setup | | The mapping requires both role sides to exist | Provide or create the custom self-service role and the corresponding identity-provider job role first | CustomSelfServiceRole, JobRole |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | Satisfied | Required opt-in and profile option source data are available | No |
| ORA_MANAGE_PROXY_USER_CONFIGURATION_DATA | Manage Proxy User Configuration Data | Blocked | Credential, proxy user key, role, or same-task package evidence is missing | No |
| ORA_CREATE_DIGITAL_CUSTOMER_SERVICE_CUSTOM_ROLE_MAPPING | Manage Custom Role Mapping for Digital Customer Service | Blocked | Custom role or identity-provider job role is missing | No |
