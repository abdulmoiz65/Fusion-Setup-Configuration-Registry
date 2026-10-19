# Common design enforcement

Source: current Learning guidance, PM FDD and existing provider boundaries in
../references/taxonomy-and-sources.md. Rules evaluate authoritative provider
results, not an assumed local tenant baseline. No policy correction silently
replaces supplied data or creates a related setup object.

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|---|
| FND_MANAGE_PROFILE_OPTIONS | Manage Profile Options | 1 | Review this task's design against the verified scope | Pass the task-specific rule below; this is not cross-task sequencing |
| FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES | Manage Administrator Profile Values | 1 | Review this task's design against the verified scope | Pass the task-specific rule below; this is not cross-task sequencing |
| FND_MANAGE_COMMON_LOOKUPS | Manage Common Lookups | 1 | Review this task's design against the verified scope | Pass the task-specific rule below; this is not cross-task sequencing |
| FND_MANAGE_VALUE_SETS | Manage Value Sets | 1 | Review this task's design against the verified scope | Pass the task-specific rule below; this is not cross-task sequencing |
| FND_MANAGE_DESCRIPTIVE_FLEXFIELDS | Manage Descriptive Flexfields | 1 | Review this task's design against the verified scope | Pass the task-specific rule below; this is not cross-task sequencing |
| ORA_FND_GLOBAL_SEARCH_CONFIGURATIONS | Manage Applications Core Global Search Configurations | 1 | Review this task's design against the verified scope | Pass the task-specific rule below; this is not cross-task sequencing |
| ORA_FND_SUGGESTION_GROUPS | Manage Applications Core Global Search Suggestion Groups | 1 | Review this task's design against the verified scope | Pass the task-specific rule below; this is not cross-task sequencing |
| ORA_FND_MANAGE_INDEX_CONFIGURATION | Manage Search Indexes | 1 | Review this task's design against the verified scope | Pass the task-specific rule below; this is not cross-task sequencing |
| FND_MANAGE_AUDIT_POLICIES | Manage Audit Policies | 1 | Review this task's design against the verified scope | Pass the task-specific rule below; this is not cross-task sequencing |
| ORA_GMS_MANAGE_AUDIT_TYPES | Manage Audit Types | 1 | Review this task's design against the verified scope | Pass the task-specific rule below; this is not cross-task sequencing |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| FND_MANAGE_PROFILE_OPTIONS | Manage Profile Options | Selected task before preview | Error | resolve_learning_profile_definition | Unresolved identity, unsupported operation, unvalidated baseline or violation of this policy | Do not recreate a delivered definition to update a configured value; the provider parent is read-only. | No automatic fix; revise proposal and obtain fresh approval for any later mutation |
| FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES | Manage Administrator Profile Values | Selected task before preview | Error | resolve_learning_profile_configured_values | Unresolved identity, unsupported operation, unvalidated baseline or violation of this policy | Validate enabled/updatable level, exact allowed values and consumer impact; recommendations are not defaults; keep the seven Redwood flags separate from Grow and the release-dependent Communities row. | No automatic fix; revise proposal and obtain fresh approval for any later mutation |
| FND_MANAGE_COMMON_LOOKUPS | Manage Common Lookups | Selected task before preview | Error | resolve_learning_common_lookup_codes | Unresolved identity, unsupported operation, unvalidated baseline or violation of this policy | Preserve seed restrictions, stable in-use codes and distinct business actions; required review does not require new codes. | No automatic fix; revise proposal and obtain fresh approval for any later mutation |
| FND_MANAGE_VALUE_SETS | Manage Value Sets | Selected task before preview | Error | resolve_learning_value_set_definition | Unresolved identity, unsupported operation, unvalidated baseline or violation of this policy | Reuse a compatible governed definition; no root value-set create/update through the child-value provider; inspect all consumers before changing shared values. | No automatic fix; revise proposal and obtain fresh approval for any later mutation |
| FND_MANAGE_DESCRIPTIVE_FLEXFIELDS | Manage Descriptive Flexfields | Positive baseline review or mutation preflight | Error | resolve_learning_dff_readiness | Unresolved identity, unsupported operation or unvalidated evidence for the requested check/change | For review report only verified dimensions and remaining gaps; for segment changes require compatible value sets and approved design. Separate import and deployment; no root-DFF creation or search-ready claim. | No automatic fix; revise proposal and obtain fresh approval for any later mutation |
| ORA_FND_GLOBAL_SEARCH_CONFIGURATIONS | Manage Applications Core Global Search Configurations | Selected task before preview | Error | resolve_learning_global_search_configuration | Unresolved identity, unsupported operation, unvalidated baseline or violation of this policy | CSV is not supported; blank businessObject does not authorize REST or Data Loader; distinguish global search from HCM Tool Search Views. | No automatic fix; revise proposal and obtain fresh approval for any later mutation |
| ORA_FND_SUGGESTION_GROUPS | Manage Applications Core Global Search Suggestion Groups | Selected task before preview | Error | resolve_learning_search_suggestion_group | Unresolved identity, unsupported operation, unvalidated baseline or violation of this policy | Do not equate a suggestion group with a Learning search view or an assignment audience; no empty-object loader request. | No automatic fix; revise proposal and obtain fresh approval for any later mutation |
| ORA_FND_MANAGE_INDEX_CONFIGURATION | Manage Search Indexes | Selected task before preview | Error | resolve_learning_search_index | Unresolved identity, unsupported operation, unvalidated baseline or violation of this policy | Index enablement, initial ingestion and HCM Tool Search Views are separate steps; no recurring initial ingest or invented ESS identifiers. | No automatic fix; revise proposal and obtain fresh approval for any later mutation |
| FND_MANAGE_AUDIT_POLICIES | Manage Audit Policies | Selected task before preview | Error | resolve_learning_audit_baseline | Unresolved identity, unsupported operation, unvalidated baseline or violation of this policy | Overall Fusion audit switch is manual-only; audit inventory is not enabled-field state; no profile REST workaround; verify current Learning audit coverage. | No automatic fix; revise proposal and obtain fresh approval for any later mutation |
| ORA_GMS_MANAGE_AUDIT_TYPES | Manage Audit Types | Selected task before preview | Error | resolve_learning_audit_type_identity | Unresolved identity, unsupported operation, unvalidated baseline or violation of this policy | Preserve the taxonomy entry but stop execution on the Grants/Learning mismatch; do not substitute Manage Audit Policies or create award audit types. | No automatic fix; revise proposal and obtain fresh approval for any later mutation |

## Design Lookup Requirements

| Task Code | Task Name | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|---|
| FND_MANAGE_PROFILE_OPTIONS | Manage Profile Options | resolve_learning_profile_definition | Before design is accepted | verified profile identity and level flags | ora_reference_lookups.md |
| FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES | Manage Administrator Profile Values | resolve_learning_profile_configured_values | Before design is accepted | configured value and child existence; distinguish missing child from denied/incomplete read | ora_reference_lookups.md |
| FND_MANAGE_COMMON_LOOKUPS | Manage Common Lookups | resolve_learning_common_lookup_codes | Before design is accepted | existing code identity and configured values; missing versus unvalidated status | ora_reference_lookups.md |
| FND_MANAGE_VALUE_SETS | Manage Value Sets | resolve_learning_value_set_definition | Before design is accepted | verified definition identity and validation compatibility | ora_reference_lookups.md |
| FND_MANAGE_DESCRIPTIVE_FLEXFIELDS | Manage Descriptive Flexfields | resolve_learning_dff_readiness | Before accepting baseline review or proposed configuration | export_identity; source_mapping; exact dff_rows; configuration evidence and gaps; deployment evidence only when requested | ora_reference_lookups.md |
| ORA_FND_GLOBAL_SEARCH_CONFIGURATIONS | Manage Applications Core Global Search Configurations | resolve_learning_global_search_configuration | Before design is accepted | TBD: current configuration and capability evidence | ora_reference_lookups.md |
| ORA_FND_SUGGESTION_GROUPS | Manage Applications Core Global Search Suggestion Groups | resolve_learning_search_suggestion_group | Before design is accepted | TBD: current group definition and applicability | ora_reference_lookups.md |
| ORA_FND_MANAGE_INDEX_CONFIGURATION | Manage Search Indexes | resolve_learning_search_index | Before design is accepted | TBD: current index configuration and ingestion evidence | ora_reference_lookups.md |
| FND_MANAGE_AUDIT_POLICIES | Manage Audit Policies | resolve_learning_audit_baseline | Before design is accepted | TBD: combined provider/UI baseline for the requested audit scope | ora_reference_lookups.md |
| ORA_GMS_MANAGE_AUDIT_TYPES | Manage Audit Types | resolve_learning_audit_type_identity | Before design is accepted | TBD: corrected or confirmed mapping before any operation | ora_reference_lookups.md |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| FND_MANAGE_PROFILE_OPTIONS | Manage Profile Options | COMMON.PROFILE_DEFINITION.DESIGN | step | 5 | design_enforcement | pass->COMMON.PROFILE_DEFINITION.GATE;fail->RETURN_ISSUES | COMMON.PROFILE_DEFINITION.DEFAULTS | stop | Selected task; validate only, never authorize a write |
| FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES | Manage Administrator Profile Values | COMMON.PROFILE_VALUES.DESIGN | step | 5 | design_enforcement | pass->COMMON.PROFILE_VALUES.GATE;fail->RETURN_ISSUES | COMMON.PROFILE_VALUES.DEFAULTS | stop | Selected task; validate only, never authorize a write |
| FND_MANAGE_COMMON_LOOKUPS | Manage Common Lookups | COMMON.LOOKUPS.DESIGN | step | 5 | design_enforcement | pass->COMMON.LOOKUPS.GATE;fail->RETURN_ISSUES | COMMON.LOOKUPS.DEFAULTS | stop | Selected task; validate only, never authorize a write |
| FND_MANAGE_VALUE_SETS | Manage Value Sets | COMMON.VALUE_SETS.DESIGN | step | 5 | design_enforcement | pass->COMMON.VALUE_SETS.GATE;fail->RETURN_ISSUES | COMMON.VALUE_SETS.DEFAULTS | stop | Selected task; validate only, never authorize a write |
| FND_MANAGE_DESCRIPTIVE_FLEXFIELDS | Manage Descriptive Flexfields | COMMON.DFF.DESIGN | step | 5 | design_enforcement | pass->COMMON.DFF.GATE;fail->RETURN_ISSUES | COMMON.DFF.DEFAULTS | stop | Selected task; validate only, never authorize a write |
| ORA_FND_GLOBAL_SEARCH_CONFIGURATIONS | Manage Applications Core Global Search Configurations | COMMON.SEARCH_CONFIG.DESIGN | step | 5 | design_enforcement | pass->COMMON.SEARCH_CONFIG.GATE;fail->RETURN_ISSUES | COMMON.SEARCH_CONFIG.DEFAULTS | stop | Selected task; validate only, never authorize a write |
| ORA_FND_SUGGESTION_GROUPS | Manage Applications Core Global Search Suggestion Groups | COMMON.SEARCH_SUGGESTIONS.DESIGN | step | 5 | design_enforcement | pass->COMMON.SEARCH_SUGGESTIONS.GATE;fail->RETURN_ISSUES | COMMON.SEARCH_SUGGESTIONS.DEFAULTS | stop | Selected task; validate only, never authorize a write |
| ORA_FND_MANAGE_INDEX_CONFIGURATION | Manage Search Indexes | COMMON.SEARCH_INDEX.DESIGN | step | 5 | design_enforcement | pass->COMMON.SEARCH_INDEX.GATE;fail->RETURN_ISSUES | COMMON.SEARCH_INDEX.DEFAULTS | stop | Selected task; validate only, never authorize a write |
| FND_MANAGE_AUDIT_POLICIES | Manage Audit Policies | COMMON.AUDIT_POLICY.DESIGN | step | 5 | design_enforcement | pass->COMMON.AUDIT_POLICY.GATE;fail->RETURN_ISSUES | COMMON.AUDIT_POLICY.DEFAULTS | stop | Selected task; validate only, never authorize a write |
| ORA_GMS_MANAGE_AUDIT_TYPES | Manage Audit Types | COMMON.AUDIT_TYPES.DESIGN | step | 5 | design_enforcement | pass->COMMON.AUDIT_TYPES.GATE;fail->RETURN_ISSUES | COMMON.AUDIT_TYPES.DEFAULTS | stop | Selected task; validate only, never authorize a write |
