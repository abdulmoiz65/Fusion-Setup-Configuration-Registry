# Design Enforcement

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|---|
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | 10 | Confirm secure account key field | Do not rely on the account name as the account key when self-registration is enabled |
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | 20 | Confirm access profile option safety | Allowed origins, CORS headers, proxy-user whitelist, chat anonymous access, and chat inlay access must be intentionally approved before packaging changes |
| ORA_MANAGE_PROXY_USER_CONFIGURATION_DATA | Manage Proxy User Configuration Data | 10 | Confirm allowed proxy exposure | Only allowlisted resources or approved custom Application Composer objects may be exposed to anonymous users |
| ORA_CREATE_DIGITAL_CUSTOMER_SERVICE_CUSTOM_ROLE_MAPPING | Manage Custom Role Mapping for Digital Customer Service | 10 | Confirm custom role mapping rule | Map only custom self-service roles to custom identity-provider roles |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | SVC_CSS_ACCT_KEY_FIELD is configured for self-registration | Error | | The account key relies on an insecure or unapproved default | Use a case-sensitive field that is approved as the account key for the Account object | Yes |
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | ORACLE.ADF.VIEW.ALLOWED_ORIGINS or ORA_CORS_ORIGINS is configured for DCS access | Error | | Allowed origins are missing, use an unapproved wildcard, or contain an origin that is not explicitly approved | Use only approved fully qualified origins, self, or none values that match the CORS guidance and same-task evidence | Yes |
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | CORS_ACCESS_CONTROL_ALLOW_HEADERS is configured for Self-Service Optimization | Error | | Required Self-Service Optimization headers are missing from the approved comma-separated header list | Include approved required headers such as Puds-Access-Token, kmauthtoken, content-language, X-Oracle-ABCS-SessionId, and X-Oracle-ABCS-UserId when Self-Service Optimization requires them | Yes |
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | SVC_CHAT_ANONYMOUS_ACCESS_ENABLED or SVC_CHAT_INLAYS_ACCESS_ENABLED is changed | Error | | Anonymous chat or chat inlay access is changed without an approved DCS, Embedded Service, Service Center, or Help Desk access decision | Confirm the intended channel use before setting the profile option value | Yes |
| ORA_MANAGE_PROXY_USER_CONFIGURATION_DATA | Manage Proxy User Configuration Data | A URL pattern is exposed through Proxy User Data Service | Error | | The resource is not allowlisted and is not an approved custom object | Restrict anonymous access to documented allowlist resources or approved custom objects | Yes |
| ORA_MANAGE_PROXY_USER_CONFIGURATION_DATA | Manage Proxy User Configuration Data | Proxy user credentials are present in any file or diagnostic | Error | | Passwords or tokens would be persisted | Redact the secret and collect it only in the live secured execution context | Yes |
| ORA_CREATE_DIGITAL_CUSTOMER_SERVICE_CUSTOM_ROLE_MAPPING | Manage Custom Role Mapping for Digital Customer Service | A self-service role is mapped to an identity-provider role | Error | | A ready-to-use self-service role is selected for mapping | Create or select a custom self-service role before mapping | Yes |

## Design Lookup Requirements

| Task Code | Task Name | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|---|
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | find_profile_value_by_option_code | Current profile value evidence is needed before planning a profile option change | ProfileOptionValue, ProfileOptionId, ApplicationId | ora_reference_lookups.md |
| ORA_SVC_MANAGE_CSS_ACCOUNT_SETUP_OPTS | Manage Digital Customer Service Account Setup Profile Options | find_account_profile_value_by_option_code | Current profile value evidence is needed before planning account setup option changes | ProfileOptionValue, ProfileOptionId, ApplicationId | ora_reference_lookups.md |
| ORA_SVC_MANAGE_SELF_SERVICE_RELATIONSHIP_TYPE_STANDARD_LOOKUP | Manage Self-Service Relationship Type Standard Lookup | find_self_service_relationship_lookup_codes | Duplicate or update evidence is needed for a lookup code | LookupCode, Meaning, EnabledFlag | ora_reference_lookups.md |
