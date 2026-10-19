# Activity Profile Options Input Validation

Source basis: exact target-environment Apps Common profile-option reads,
current Oracle Activity profile-option guidance, and the task export used only
for Inventory and Review reconciliation.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Inventory, Review, Create, Update, Set, Remove, Delete, or BulkSet, or an unambiguous objective mapping to one | Block validation | Normalize list/current to Inventory or Review, Create/Update to Set with live method selection, and Remove/Delete to Remove | Always | |
| Target environment | EnvironmentUrl, canonical EnvironmentIdentity, and ProjectId from selected implementation context | Block before external calls | Resolve and verify the already selected Fusion environment and project | Always | |
| Export attempt evidence | Export status and, when successful, ProcessId, ZIP hash, environment, release, timestamp, members, and counts | Disclose and continue live reads | Run automatic task export | Inventory or Review | inventory_activity_profile_options_from_reference_export |
| Exact option identity | ProfileOptionCode, one exact documented display name, or one exact immediate-context code | Block lookup | Resolve exact case-sensitive identity | Review, Set, Remove, or BulkSet | resolve_documented_activity_profile_option_identity |
| Target scope | ProfileLevel of Site, Product, or User; ProductApplicationShortName for Product; UserName for User | Block mutation preview | Supply the exact scope key | Set, Remove, or BulkSet | resolve_exact_activity_profile_option_and_dependencies |
| Expected state | ExpectedCurrentValue or explicit not configured | Block mutation preview | Read the exact child item or collection | Set, Remove, or BulkSet | resolve_exact_activity_profile_option_and_dependencies |
| Proposed value | ProposedValue | Block Create or Update preview | Supply and resolve the intended stored value | Set or BulkSet | resolve_exact_activity_profile_option_and_dependencies |
| Bulk rows | Unique ordered rows with code, level, scope key, expected state, and proposed value | Block BulkSet | Correct missing or duplicate rows | BulkSet | resolve_exact_activity_profile_option_and_dependencies |
| Immutable preview | Canonical environment, operation, method, relative endpoint, exact target, expected state, body or delete effect, dependencies, verification plan, and PreviewSha256 | Block approval | Build the complete Apps Common preview after fresh live preflight | Before mutation approval | |
| Execution approval | Standalone approval bound to PreviewSha256 and all canonical preview fields | Block write | Present the immutable preview and wait for exact approval | Immediately before POST, PATCH, or DELETE | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Unsupported operation | Reject before export or lookup | Always | |
| Current or configured request is classified as documentation-only | Normalize to Inventory or Review | Inventory or Review intent | |
| One exact code exists in immediate request context | Inherit it for a short Review follow-up | Review | resolve_documented_activity_profile_option_identity |
| Zero or multiple immediate-context codes exist | Request one exact code | Review | resolve_documented_activity_profile_option_identity |
| Environment identity is blank, URL-shaped, or disagrees with project or REST host | Stop before external calls | Always | |
| ProfileOptionCode requires fuzzy matching | Reject; accept exact code or one exact documented display-name match | Review, Set, Remove, or BulkSet | resolve_documented_activity_profile_option_identity |
| Code is absent from fresh FSM export | Continue exact live lookup; omission does not block Apps Common CRUD | Always | resolve_exact_activity_profile_option_and_dependencies |
| Scope is outside Site, Product, or User | Reject | Set, Remove, or BulkSet | |
| Product application short name is missing | Block before Product lookup | Product mutation | resolve_exact_activity_profile_option_and_dependencies |
| UserName is missing | Block before User lookup | User mutation | resolve_exact_activity_profile_option_and_dependencies |
| Selected level is not enabled and updatable | Block before preview | Set, Remove, or BulkSet | resolve_exact_activity_profile_option_and_dependencies |
| Delegation, company-wide disable, or task-reminder option is not Site scoped | Block unless current Oracle guidance explicitly supports the requested scope | Applicable mutation | resolve_exact_activity_profile_option_and_dependencies |
| ZMM_ACTIVITY_ENABLE_ALL_RECORDS uses a scope other than Site or User | Block | Applicable mutation | resolve_exact_activity_profile_option_and_dependencies |
| Expected state differs from latest child state | Invalidate preview and approval | Set, Remove, or BulkSet | resolve_exact_activity_profile_option_and_dependencies |
| Set target is absent | Normalize to Create and POST; ExpectedCurrentValue must be not configured | Set | resolve_exact_activity_profile_option_and_dependencies |
| Set target exists | Normalize to Update and PATCH; lock its exact value | Set | resolve_exact_activity_profile_option_and_dependencies |
| Remove target is absent | Return already not configured; do not issue DELETE | Remove | resolve_exact_activity_profile_option_and_dependencies |
| Remove target exists | Normalize to Delete and require fallback-impact preview | Remove | resolve_exact_activity_profile_option_and_dependencies |
| Proposed value is missing for Create or Update | Block preview | Set or BulkSet | |
| Reminder channel is disabled | Block reminder enablement and show the exact related profile state | Reminder mutation | resolve_exact_activity_profile_option_and_dependencies |
| All-record, delegation, or company-wide notification impact is unacknowledged | Block preview | Applicable mutation | |
| Lookup-backed meaning or code does not resolve exactly and actively | Block; never guess | Lookup-backed mutation | resolve_exact_activity_profile_option_and_dependencies |
| Bulk rows repeat code, level, and level-value | Reject and identify duplicates | BulkSet | |
| Create body includes audit or unrelated fields | Reject and rebuild the minimal body | Create | |
| Update body contains anything except ProfileOptionValue | Reject and rebuild the minimal body | Update | |
| Delete includes a body | Reject and rebuild as bodyless DELETE | Remove | |
| Preview approval omits or mismatches complete digest, target, method, body, or effect | Block write and require a new approval | Mutation execution | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY_PROFILE.VALIDATE | step | 1 | validate_input | valid->ACTIVITY_PROFILE.DEPENDENCIES;invalid->ACTIVITY_PROFILE.RETURN_ISSUES | none | stop | Normalize intent, validate canonical environment, conditional export-attempt evidence, exact identity, supported scope, expected and proposed values, bulk uniqueness, and immutable preview and approval inputs when execution is requested |
