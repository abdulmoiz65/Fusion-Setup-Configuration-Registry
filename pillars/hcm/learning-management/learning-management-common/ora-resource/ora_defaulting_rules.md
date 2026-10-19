# Common default policy

Source: FDD GB-07 and existing profile/lookup guidance. Business recommendations
are not automatic defaults. This resource has no implicit Oracle payload defaults;
provider-specific transport/deployment defaults stay with their owning provider.

## Standard Defaults

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| FND_MANAGE_PROFILE_OPTIONS | Manage Profile Options | Not Applicable: no automatic configuration value | None; preserve current state and record Deferred for an undecided optional requirement | No explicit validated business decision | No |  |
| FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES | Manage Administrator Profile Values | Not Applicable: no automatic configuration value | None; preserve current state and record Deferred for an undecided optional requirement | No explicit validated business decision | No |  |
| FND_MANAGE_COMMON_LOOKUPS | Manage Common Lookups | Not Applicable: no automatic configuration value | None; preserve current state and record Deferred for an undecided optional requirement | No explicit validated business decision | No |  |
| FND_MANAGE_VALUE_SETS | Manage Value Sets | Not Applicable: no automatic configuration value | None; preserve current state and record Deferred for an undecided optional requirement | No explicit validated business decision | No |  |
| FND_MANAGE_DESCRIPTIVE_FLEXFIELDS | Manage Descriptive Flexfields | Not Applicable: no automatic configuration value | None; preserve current state and record Deferred for an undecided optional requirement | No explicit validated business decision | No |  |
| ORA_FND_GLOBAL_SEARCH_CONFIGURATIONS | Manage Applications Core Global Search Configurations | Not Applicable: no automatic configuration value | None; preserve current state and record Deferred for an undecided optional requirement | No explicit validated business decision | No |  |
| ORA_FND_SUGGESTION_GROUPS | Manage Applications Core Global Search Suggestion Groups | Not Applicable: no automatic configuration value | None; preserve current state and record Deferred for an undecided optional requirement | No explicit validated business decision | No |  |
| ORA_FND_MANAGE_INDEX_CONFIGURATION | Manage Search Indexes | Not Applicable: no automatic configuration value | None; preserve current state and record Deferred for an undecided optional requirement | No explicit validated business decision | No |  |
| FND_MANAGE_AUDIT_POLICIES | Manage Audit Policies | Not Applicable: no automatic configuration value | None; preserve current state and record Deferred for an undecided optional requirement | No explicit validated business decision | No |  |
| ORA_GMS_MANAGE_AUDIT_TYPES | Manage Audit Types | Not Applicable: no automatic configuration value | None; preserve current state and record Deferred for an undecided optional requirement | No explicit validated business decision | No |  |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| FND_MANAGE_PROFILE_OPTIONS | Manage Profile Options | COMMON.PROFILE_DEFINITION.DEFAULTS | step | 4 | apply_default | pass->COMMON.PROFILE_DEFINITION.DESIGN;fail->RETURN_ISSUES | COMMON.PROFILE_DEFINITION.DEPENDENCY | stop | Selected task; validate only, never authorize a write |
| FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES | Manage Administrator Profile Values | COMMON.PROFILE_VALUES.DEFAULTS | step | 4 | apply_default | pass->COMMON.PROFILE_VALUES.DESIGN;fail->RETURN_ISSUES | COMMON.PROFILE_VALUES.DEPENDENCY | stop | Selected task; validate only, never authorize a write |
| FND_MANAGE_COMMON_LOOKUPS | Manage Common Lookups | COMMON.LOOKUPS.DEFAULTS | step | 4 | apply_default | pass->COMMON.LOOKUPS.DESIGN;fail->RETURN_ISSUES | COMMON.LOOKUPS.DEPENDENCY | stop | Selected task; validate only, never authorize a write |
| FND_MANAGE_VALUE_SETS | Manage Value Sets | COMMON.VALUE_SETS.DEFAULTS | step | 4 | apply_default | pass->COMMON.VALUE_SETS.DESIGN;fail->RETURN_ISSUES | COMMON.VALUE_SETS.DEPENDENCY | stop | Selected task; validate only, never authorize a write |
| FND_MANAGE_DESCRIPTIVE_FLEXFIELDS | Manage Descriptive Flexfields | COMMON.DFF.DEFAULTS | step | 4 | apply_default | pass->COMMON.DFF.DESIGN;fail->RETURN_ISSUES | COMMON.DFF.DEPENDENCY | stop | Selected task; validate only, never authorize a write |
| ORA_FND_GLOBAL_SEARCH_CONFIGURATIONS | Manage Applications Core Global Search Configurations | COMMON.SEARCH_CONFIG.DEFAULTS | step | 4 | apply_default | pass->COMMON.SEARCH_CONFIG.DESIGN;fail->RETURN_ISSUES | COMMON.SEARCH_CONFIG.DEPENDENCY | stop | Selected task; validate only, never authorize a write |
| ORA_FND_SUGGESTION_GROUPS | Manage Applications Core Global Search Suggestion Groups | COMMON.SEARCH_SUGGESTIONS.DEFAULTS | step | 4 | apply_default | pass->COMMON.SEARCH_SUGGESTIONS.DESIGN;fail->RETURN_ISSUES | COMMON.SEARCH_SUGGESTIONS.DEPENDENCY | stop | Selected task; validate only, never authorize a write |
| ORA_FND_MANAGE_INDEX_CONFIGURATION | Manage Search Indexes | COMMON.SEARCH_INDEX.DEFAULTS | step | 4 | apply_default | pass->COMMON.SEARCH_INDEX.DESIGN;fail->RETURN_ISSUES | COMMON.SEARCH_INDEX.DEPENDENCY | stop | Selected task; validate only, never authorize a write |
| FND_MANAGE_AUDIT_POLICIES | Manage Audit Policies | COMMON.AUDIT_POLICY.DEFAULTS | step | 4 | apply_default | pass->COMMON.AUDIT_POLICY.DESIGN;fail->RETURN_ISSUES | COMMON.AUDIT_POLICY.DEPENDENCY | stop | Selected task; validate only, never authorize a write |
| ORA_GMS_MANAGE_AUDIT_TYPES | Manage Audit Types | COMMON.AUDIT_TYPES.DEFAULTS | step | 4 | apply_default | pass->COMMON.AUDIT_TYPES.DESIGN;fail->RETURN_ISSUES | COMMON.AUDIT_TYPES.DEPENDENCY | stop | Selected task; validate only, never authorize a write |
