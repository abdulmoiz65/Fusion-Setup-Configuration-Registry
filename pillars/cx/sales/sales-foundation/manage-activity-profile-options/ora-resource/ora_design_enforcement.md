# Activity Profile Options Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Establish live identity and scope | Resolve one exact profile definition, selected scope key, live capability, and current child state. |
| 2 | Resolve Activity impact | Check all-record search, delegation co-ownership, reminder channels, and company-wide notification effects when applicable. |
| 3 | Select deterministic CRUD | Choose POST, PATCH, DELETE, or no write from exact current state and build the minimal child request. |
| 4 | Bind approval and verification | Bind the immutable preview digest and require an immediate stale-state read plus exact post-write verification. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any Inventory or Review | Error | resolve_exact_activity_profile_option_and_dependencies | Configured values come from documentation, export, Site fallback, or profileValues rather than complete exact child reads or explicit absence | Complete candidate reconciliation and paginated Site, Product, and User reads | Yes |
| Any Create, Update, or Delete | Error | resolve_exact_activity_profile_option_and_dependencies | Definition is missing, scope is disabled or read-only, scope key is unresolved, or current state differs from the preview | Refresh the exact live preflight and rebuild the preview | Yes |
| ZMM_ACTIVITY_ENABLE_ALL_RECORDS is enabled | Error | | Search and security impact or saved-search performance guidance has not been acknowledged | Confirm the intended Site or User scope and use smaller saved-search record sets when practical | Yes |
| ZMM_ACTIVITY_APPT_DELEGATION or ZMM_ACTIVITY_TASK_DELEGATION is enabled | Error | | Scope is not Site or the original-owner and delegated-owner edit behavior is not acknowledged | Enable only the exact delegation capability needed and disclose co-ownership behavior | Yes |
| ORA_ZMM_TASK_EMAIL_REMINDER or ORA_ZMM_TASK_NOTIF_LIST_REMINDER is enabled | Error | resolve_exact_activity_profile_option_and_dependencies | Scope is not Site or the related delivery channel is disabled or unresolved | Keep the required company-level notification channel available before enabling the reminder | Yes |
| A ZMM_ACTIVITY_DISABLE option is set to Yes | Error | | Scope is not Site or the company-wide appointment or task impact is not explicitly acknowledged | Limit the change to the exact requested channel and preview the company-wide effect | Yes |
| Set target is absent | Error | resolve_exact_activity_profile_option_and_dependencies | Operation is not Create with collection POST or expected state is not configured | Reclassify from the exact collection and use a minimal Create body | Yes |
| Set target exists | Error | resolve_exact_activity_profile_option_and_dependencies | Operation is not Update with item PATCH or expected value is stale | Reclassify from the exact item and use ProfileOptionValue only | Yes |
| Remove target exists | Error | resolve_exact_activity_profile_option_and_dependencies | Operation is not bodyless item DELETE or fallback behavior is undisclosed | Rebuild a Delete preview with lower-precedence or delivered behavior | Yes |
| BulkSet | Error | resolve_exact_activity_profile_option_and_dependencies | Targets are duplicated, writes are parallel, execution continues after failure, or rollback is promised | Use one ordered unique list and stop on first stale state, write failure, or verification mismatch | Yes |
| Any mutation request | Error | | FSM ZIP, Data Loader, setup import, browser write, direct curl, Upsert-Mode, or task-local HTTP code is selected | Route only through core.fusion-api.apps-common with deterministic CRUD | No |
| Any request body | Error | | Create includes unrelated or audit fields, Update includes anything except ProfileOptionValue, Delete has a body, or parent/level metadata is targeted | Rebuild the minimal level-specific child request | Yes |
| Mutation approval | Error | | Approval does not match the complete canonical digest, target, method, expected state, body or delete effect, and environment | Produce a fresh immutable preview and obtain standalone approval | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_exact_activity_profile_option_and_dependencies | Inventory, Review, or any mutation preflight | Exact definition, level capabilities, complete child state, scope key, related Activity dependency state, stored value, and timestamps | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY_PROFILE.DESIGN | decision | 5 | design_enforcement | pass->ACTIVITY_PROFILE.EXECUTION_GATE;fail->ACTIVITY_PROFILE.RETURN_ISSUES | ACTIVITY_PROFILE.ROUTE | stop | After complete Inventory or Review reconciliation or after an exact mutation target, method, endpoint, body or delete effect, Activity dependencies, current-state lock, verification plan, and approval boundary are established |
