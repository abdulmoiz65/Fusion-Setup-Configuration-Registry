# Dependency Readiness

## Required Dependency Order

| Task Code | Task Name | Sequence | Dependency | What Must Happen |
|---|---|---|---|---|
| ORA_CSO_LOCALES_MGMT | Manage Knowledge Locales | 1 | Locale state | Resolve the selected locale's active, default, and default-preferred state through the completed Manage Knowledge Locales FSM export |
| ORA_CSO_LOCALES_MGMT | Manage Knowledge Locales | 2 | Default locale eligibility | Confirm that a selected default Knowledge locale is active |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ORA_CSO_LOCALES_MGMT | Manage Knowledge Locales | locale_current_state | Current locale state | Yes | Any locale review or configuration request | Lookup | Completed Manage Knowledge Locales FSM export | resolve_fsm_locale_state | The FSM active-locale object is authoritative for activity and the tenant object identifies the defaults | Provide the locale code or record ID when the request is for one locale | LocaleRecordId: recordId; Active: active; DefaultLocale: defaultLocale; DefaultPreferredLocale: defaultPreferredLocale |
| ORA_CSO_LOCALES_MGMT | Manage Knowledge Locales | default_locale_active | Active default locale | Yes | Set the default Knowledge locale | Verify | Completed Manage Knowledge Locales FSM export | resolve_fsm_locale_state | Only a locale present in the FSM active-locale object can be selected in the Default Locale list | Enable the locale first or select another active locale | LocaleCode: recordId; Active: active |
| ORA_CSO_LOCALES_MGMT | Manage Knowledge Locales | fsm_write_contract | FSM package contract | Yes | Any enable, disable, default-locale, or default-preferred-locale change | Lookup | Completed Manage Knowledge Locales FSM export | resolve_fsm_package_contract | A write must use the current exported package structure rather than an inferred contract | Complete a fresh task export and use its package members, headers, metadata, and keys before a mutation preview | Package members, CSV headers, metadata, and parent-child keys |
| ORA_CSO_ARTICLE_STATUS_MGMT | Manage Knowledge Article Statuses | article_status_feature_enablement | Article Statuses feature enabled | Yes | Authors need predefined or user-defined article statuses | Verify | Completed Manage Knowledge Article Statuses FSM export | resolve_article_statuses_fsm_export | Predefined statuses are available to authors only after the feature is enabled | Enable Article Statuses before configuring or assigning statuses | FeatureState: KM_ARTICLE_STATUS_ENABLED; ArticleStatus: referenceKey, name, active |
| ORA_MANAGE_KNOWLEDGE_FOR_SERVICE_REQUESTS_PROFILE_OPTIONS | Manage Knowledge for Service Requests with Redwood User Interface Profile Options | fsm_profile_option_contract | FSM profile-option contract | Yes | Before an FSM profile-option update | Lookup | Completed task export and selected ProfileOptionName | resolve_fsm_service_requests_profile_option_export | The update must retain the exported definition, supported level, and audit fields while changing only the approved value and current update audit fields | Complete a fresh task export and select one existing profile option | ProfileOptionName; ApplicationId; supported LevelName and LevelValue; ProfileOptionValue; retained definition and audit fields |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|---|
| ORA_CSO_LOCALES_MGMT | Manage Knowledge Locales | Lookup | Locale identity or active state must be resolved from the completed Manage Knowledge Locales FSM export | Yes |
| ORA_CSO_LOCALES_MGMT | Manage Knowledge Locales | Verify | The request requires a documented prerequisite to be confirmed | No |
| ORA_CSO_LOCALES_MGMT | Manage Knowledge Locales | Lookup | The current FSM package contract must be resolved from a completed task export | Yes |
| ORA_CSO_ARTICLE_STATUS_MGMT | Manage Knowledge Article Statuses | Verify | Article statuses must be enabled before authors can use them | No |
| ORA_MANAGE_KNOWLEDGE_FOR_SERVICE_REQUESTS_PROFILE_OPTIONS | Manage Knowledge for Service Requests with Redwood User Interface Profile Options | Lookup | The existing profile-option definition, level, and value row must be resolved from a completed task export | Yes |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_CSO_ARTICLE_STATUS_MGMT | Manage Knowledge Article Statuses | ARTICLESTATUS.DEPENDENCIES | step | 3 | resolve_dependency | ok->ARTICLESTATUS.DESIGN;blocked->ARTICLESTATUS.FAILED;failure->ARTICLESTATUS.FAILED | ARTICLESTATUS.LOOKUP | stop | Before an Article Statuses request is ready for preview |
| ORA_CSO_LOCALES_MGMT | Manage Knowledge Locales | KNOWLEDGELOCALES.DEPENDENCIES | step | 3 | resolve_dependency | ok->KNOWLEDGELOCALES.DESIGN;blocked->KNOWLEDGELOCALES.FAILED;failure->KNOWLEDGELOCALES.FAILED | KNOWLEDGELOCALES.LOOKUP | stop | Before a locale configuration request is ready for preview |
| ORA_MANAGE_KNOWLEDGE_FOR_SERVICE_REQUESTS_PROFILE_OPTIONS | Manage Knowledge for Service Requests with Redwood User Interface Profile Options | SERVICEREQUESTSPROFILE.DEPENDENCIES | step | 3 | resolve_dependency | ok->SERVICEREQUESTSPROFILE.DESIGN;blocked->SERVICEREQUESTSPROFILE.FAILED;failure->SERVICEREQUESTSPROFILE.FAILED | SERVICEREQUESTSPROFILE.LOOKUP | stop | Before a Knowledge for Service Requests FSM profile-option update is ready for preview |
