# Defaulting Rules

## Standard Defaults

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| ORA_CSO_LOCALES_MGMT | Manage Knowledge Locales | Default Knowledge locale | English, United States locale set automatically | No default locale has been changed by the organization | Yes |  |
| ORA_CSO_LOCALES_MGMT | Manage Knowledge Locales | User knowledge locale | User language and territory preference | The user has not set a preferred locale and no default preferred Knowledge locale is set | Yes |  |
| ORA_MANAGE_KNOWLEDGE_FOR_SERVICE_REQUESTS_PROFILE_OPTIONS | Manage Knowledge for Service Requests with Redwood User Interface Profile Options | LevelName | SITE | No supported profile level is supplied for a task-owned profile-value row | No | resolve_fsm_service_requests_profile_option_export |
| ORA_MANAGE_KNOWLEDGE_FOR_SERVICE_REQUESTS_PROFILE_OPTIONS | Manage Knowledge for Service Requests with Redwood User Interface Profile Options | LevelValue | SITE | LevelName defaults to SITE and no level value is supplied | No | resolve_fsm_service_requests_profile_option_export |
