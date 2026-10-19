# Activity Profile Options Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target environment and operation | Resolve the canonical project environment and normalize Inventory, Review, Set, Remove, or BulkSet. |
| 2 | Exact profile and scope identity | Resolve the exact profile code, selected Site, Product, or User key, live level capability, and current child state. |
| 3 | Activity behavior dependencies | Resolve reminder-channel state and obtain required acknowledgement for search, delegation, or company-wide notification impact. |
| 4 | Stored value and privilege | Resolve the exact stored value contract and confirm the profile-value management privilege for mutation. |
| 5 | Immutable preview and approval | Bind approval to the exact method, endpoint, target, expected state, body or delete effect, and digest. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| target_environment | Canonical target environment | Yes | Always | Satisfied when project identity, environment identity, and REST host agree | Selected project and Fusion context | | Prevents reads or writes against the wrong environment | Correct the project or environment mismatch before continuing | EnvironmentIdentity, RestBaseUrl, ProjectId |
| export_attempt | Current task export attempt | Conditional | Inventory or Review | Satisfied when automatic export outcome and evidence are recorded | shared.setup-export.task-level-export | inventory_activity_profile_options_from_reference_export | Export reconciles task membership but does not authorize mutation | Attempt export, then continue live reads even when export fails | ExportStatus, ProcessId, ExportHash, Timestamp |
| documented_identity | Exact Activity profile option identity | Conditional | Documented Inventory, Review, Set, or Remove | Satisfied when one exact documented code or display name resolves | Current Oracle Activity guidance and task baseline | resolve_documented_activity_profile_option_identity | Avoids fuzzy or cross-task profile selection | Provide an exact code when more than one option is possible | ProfileOptionCode, DisplayName, SourceClass |
| apps_common_read_route | Exact Apps Common read route | Yes | Always | Satisfied when definition, level, and child collections can be read | core.fusion-api.apps-common | resolve_exact_activity_profile_option_and_dependencies | Live state is authoritative for configured values and CRUD selection | Resolve the actual auth, privilege, transport, or response-shape failure | Definition, LevelCapabilities, ChildRows, LookupTimestamps |
| scope_identity | Exact Site, Product, or User identity | Conditional | Set, Remove, or BulkSet | Satisfied when SITE, one application short name, or one UserName and UserGuid resolves | Request and live Apps Common reads | resolve_exact_activity_profile_option_and_dependencies | Each level uses a different item key and User Create needs a GUID | Correct the scope key; never use a display name or another level's key | ProfileLevel, ItemKey, UserGuid |
| scope_capability | Enabled and updatable selected level | Conditional | Set, Remove, or BulkSet | Satisfied when the selected live level flags are both Y and Activity guidance permits the scope | Live profile option level metadata and Activity guidance | resolve_exact_activity_profile_option_and_dependencies | Prevents writes to disabled, read-only, or task-inappropriate scopes | Select an eligible scope or stop | EnabledFlag, UpdateableFlag, ScopePolicy |
| current_child_state | Exact current configured row or explicit absence | Conditional | Set, Remove, or BulkSet | Satisfied when the selected child item resolves once or the exact collection proves absence | Live Apps Common child collection | resolve_exact_activity_profile_option_and_dependencies | Deterministically selects POST, PATCH, DELETE, or no write | Resolve ambiguity or access before preview | CurrentState, CurrentValue, NormalizedOperation, Method |
| reminder_channel | Related company notification channel | Conditional | Enabling ORA_ZMM_TASK_EMAIL_REMINDER or ORA_ZMM_TASK_NOTIF_LIST_REMINDER | Satisfied when the corresponding task email or notification-list channel is not disabled | Exact live related Activity profile values | resolve_exact_activity_profile_option_and_dependencies | A reminder cannot work when its delivery channel is disabled company-wide | Keep the related channel available or do not enable the reminder | ChannelCode, ChannelConfiguredValue, ChannelReady |
| behavior_acknowledgement | Activity behavior impact acknowledgement | Conditional | Enabling all-record search or delegation, or disabling a company-wide notification channel | Satisfied when the preview states the exact search, co-owner, or company-wide impact | Current Oracle Activity guidance | | These options can broaden search, create co-ownership, or disable notifications for everyone | Review and explicitly approve the stated impact | ImpactStatement, Acknowledged |
| stored_value | Exact stored profile value | Conditional | Create, Update, Set, or BulkSet | Satisfied when live validation resolves one exact active code or identifier | Live definition validation and authoritative lookup | resolve_exact_activity_profile_option_and_dependencies | Fusion can store codes or identifiers rather than display meanings | Resolve the exact stored value before preview | ProposedStoredValue, ProposedMeaning |
| mutation_privilege | Profile value management privilege | Conditional | Before POST, PATCH, or DELETE | Satisfied when FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV is available | Executor authorization | | Apps Common protects configured-value CRUD with this privilege | Use an authorized executor or stop | AuthorizedExecutor |
| immutable_approval | Digest-bound standalone approval | Conditional | Immediately before POST, PATCH, or DELETE | Satisfied when approval matches the complete fresh canonical preview | Approval record | | Prevents stale or vague authorization | Approve the exact preview after all reads and dependencies complete | PreviewSha256, ApprovalState |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required identity, dependency, capability, privilege, or approval is complete | Yes, but only the next declared graph action |
| Verify | A live state or acknowledgement still needs resolution | Read-only lookup only |
| Blocked | A required identity, dependency, capability, privilege, or approval is missing or ambiguous | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY_PROFILE.DEPENDENCIES | step | 2 | resolve_dependency | satisfied->ACTIVITY_PROFILE.LOOKUP_PROFILE;missing->ACTIVITY_PROFILE.RETURN_ISSUES | ACTIVITY_PROFILE.VALIDATE | stop | Require canonical environment, Apps Common read readiness, exact identity, Activity-specific dependencies, scope key and capability, current-state evidence, mutation privilege, and approval readiness when execution is requested |
