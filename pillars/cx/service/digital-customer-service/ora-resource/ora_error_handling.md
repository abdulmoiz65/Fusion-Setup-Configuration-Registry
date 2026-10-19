# Error Handling

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | Profile option value, same-task package evidence, or opt-in state is missing | Stop and request only the missing value or evidence |
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | The Profile Values REST resource does not return a requested option | Stop and explain that the option may need ORA_FND_AUTH_REST_ACCESS exposure or same-task export evidence before its effective value can be reported |
| ORA_SVC_MANAGE_CSS_ACCOUNT_SETUP_OPTS | Manage Digital Customer Service Account Setup Profile Options | Account message queue profile option value or same-task package evidence is missing | Stop and request the account setup profile option code, value, or package evidence |
| ORA_MANAGE_PROXY_USER_CONFIGURATION_DATA | Manage Proxy User Configuration Data | Secret material appears in input or artifacts | Redact it, stop persistence, and ask for live secured entry |
| ORA_SVC_MANAGE_SELF_SERVICE_RELATIONSHIP_TYPE_STANDARD_LOOKUP | Manage Self-Service Relationship Type Standard Lookup | Lookup code payload or package evidence is incomplete | Stop and request LookupCode, Meaning, and same-task package evidence |
| ORA_CREATE_DIGITAL_CUSTOMER_SERVICE_CUSTOM_ROLE_MAPPING | Manage Custom Role Mapping for Digital Customer Service | Custom self-service role or job role does not exist | Stop and complete prerequisite role setup before mapping |

## Disclosure Rules

| Task Code | Task Name | Gate | What Must Be Shown |
|---|---|---|---|
| ORA_MANAGE_PROXY_USER_CONFIGURATION_DATA | Manage Proxy User Configuration Data | Before save or import | Target environment, URL pattern, HTTP methods, role, proxy user key, active flag, and a statement that credentials are redacted |
| ORA_SVC_MANAGE_SELF_SERVICE_RELATIONSHIP_TYPE_STANDARD_LOOKUP | Manage Self-Service Relationship Type Standard Lookup | Before create or update | Lookup type ORA_SVC_CSS_REL_TYPE_CD, lookup code, meaning, enabled flag, and source package or REST evidence |
| ORA_CREATE_DIGITAL_CUSTOMER_SERVICE_CUSTOM_ROLE_MAPPING | Manage Custom Role Mapping for Digital Customer Service | Before save | Self-service role, job role, prerequisite role evidence, and target environment |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | Same-task FSM package structure is missing for import | Do not hand-build a package from field names alone |
| ORA_SVC_MANAGE_CSS_ACCOUNT_SETUP_OPTS | Manage Digital Customer Service Account Setup Profile Options | Same-task FSM package structure is missing for import | Do not hand-build a package from field names alone |
| ORA_MANAGE_PROXY_USER_CONFIGURATION_DATA | Manage Proxy User Configuration Data | Credentials or proxy user passwords are present | Do not persist, echo, diff, or include them in artifacts |
| ORA_SVC_MANAGE_SELF_SERVICE_RELATIONSHIP_TYPE_STANDARD_LOOKUP | Manage Self-Service Relationship Type Standard Lookup | A request targets a lookup type other than ORA_SVC_CSS_REL_TYPE_CD | Do not process it through this task |
| ORA_CREATE_DIGITAL_CUSTOMER_SERVICE_CUSTOM_ROLE_MAPPING | Manage Custom Role Mapping for Digital Customer Service | A ready-to-use self-service role is selected | Do not map it to an identity-provider role |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | DCS.PROFILE_OPTS.READY | terminal | 90 | terminal | none | DCS.PROFILE_OPTS.LOOKUP_PROFILE_VALUE | stop | Validation and lookup checks are complete |
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | DCS.PROFILE_OPTS.BLOCKED | terminal | 95 | terminal | none | DCS.PROFILE_OPTS.VALIDATE | stop | Input, dependency, or lookup evidence is missing |
| ORA_SVC_MANAGE_CSS_ACCOUNT_SETUP_OPTS | Manage Digital Customer Service Account Setup Profile Options | DCS.ACCOUNT_OPTS.READY | terminal | 90 | terminal | none | DCS.ACCOUNT_OPTS.LOOKUP_PROFILE_VALUE | stop | Validation and lookup checks are complete |
| ORA_SVC_MANAGE_CSS_ACCOUNT_SETUP_OPTS | Manage Digital Customer Service Account Setup Profile Options | DCS.ACCOUNT_OPTS.BLOCKED | terminal | 95 | terminal | none | DCS.ACCOUNT_OPTS.VALIDATE | stop | Input, dependency, or lookup evidence is missing |
| ORA_MANAGE_PROXY_USER_CONFIGURATION_DATA | Manage Proxy User Configuration Data | DCS.PROXY_CONFIG.READY | terminal | 90 | terminal | none | DCS.PROXY_CONFIG.VALIDATE | stop | Validation checks are complete |
| ORA_MANAGE_PROXY_USER_CONFIGURATION_DATA | Manage Proxy User Configuration Data | DCS.PROXY_CONFIG.BLOCKED | terminal | 95 | terminal | none | DCS.PROXY_CONFIG.VALIDATE | stop | Proxy configuration evidence is missing or unsafe |
| ORA_SVC_MANAGE_SELF_SERVICE_RELATIONSHIP_TYPE_STANDARD_LOOKUP | Manage Self-Service Relationship Type Standard Lookup | DCS.REL_TYPE.READY | terminal | 90 | terminal | none | DCS.REL_TYPE.LOOKUP_CODES | stop | Validation and lookup checks are complete |
| ORA_SVC_MANAGE_SELF_SERVICE_RELATIONSHIP_TYPE_STANDARD_LOOKUP | Manage Self-Service Relationship Type Standard Lookup | DCS.REL_TYPE.BLOCKED | terminal | 95 | terminal | none | DCS.REL_TYPE.VALIDATE | stop | Lookup code evidence is missing or ambiguous |
| ORA_CREATE_DIGITAL_CUSTOMER_SERVICE_CUSTOM_ROLE_MAPPING | Manage Custom Role Mapping for Digital Customer Service | DCS.ROLE_MAPPING.READY | terminal | 90 | terminal | none | DCS.ROLE_MAPPING.LOOKUP_ASSIGNED_ROLES | stop | Validation and lookup checks are complete |
| ORA_CREATE_DIGITAL_CUSTOMER_SERVICE_CUSTOM_ROLE_MAPPING | Manage Custom Role Mapping for Digital Customer Service | DCS.ROLE_MAPPING.BLOCKED | terminal | 95 | terminal | none | DCS.ROLE_MAPPING.VALIDATE | stop | Role mapping evidence is missing |
