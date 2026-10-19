# Defaulting Rules

## Standard Defaults

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | SVC_CSS_SELF_REGISTRATION | New Or Existing | The implementation owner accepts the documented registration default | No | |
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | SVC_CSS_SELF_REG_AUTO_APPROVE | False | The implementation owner accepts the documented registration default | No | |
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | SVC_CSS_ACCT_ADMIN_APPROVE | True | The implementation owner accepts the documented registration default | No | |
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | SVC_CSS_SIGN_IN_ATTR_NAME | EmailAddress | The implementation owner accepts the documented sign-in attribute default | No | |
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | SVC_CSS_USE_FA_AS_IDP | False | Self-Service Optimization mode is used | No | |
| ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS | Manage Digital Customer Service Profile Options | SVC_CSS_PUDS_CACHE_DURATION | 15 minutes | Self-Service Optimization cache duration is not explicitly changed | Yes | |
| ORA_SVC_MANAGE_SELF_SERVICE_RELATIONSHIP_TYPE_STANDARD_LOOKUP | Manage Self-Service Relationship Type Standard Lookup | EnabledFlag | Y | Creating a new self-service relationship type lookup code | Yes | |
