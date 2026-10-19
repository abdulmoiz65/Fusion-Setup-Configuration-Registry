# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Establish the business outcome | Identify the affected Recruiting experience, intended users, timing, and requested profile-value outcome. |
| 2 | Prove Recruiting ownership | Match the exact ProfileOptionName through one current approved ownership-crosswalk row whose ModuleId is in the complete maintained allowlist. |
| 3 | Read the exact definition | Delegate an exact ProfileOptionName definition read to Common Profile Options and retain only metadata actually returned. |
| 4 | Confirm level capability | Require both Enabled and Updatable metadata for the selected Site, Product, or User level. |
| 5 | Resolve exact scope and current state | Use `SITE`, one approved Product technical key, or one provider-resolved User identity/GUID; prove current-item presence or create absence. |
| 6 | Enforce minimal change | Preserve profile identity, ownership mapping, level, scope, protection metadata, and all unrequested values. |
| 7 | Bind approval | Present one immutable business-first preview and obtain exact approval immediately before one delegated configured-value mutation. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every profile-specific request | Blocker | resolve_profile_option_ownership_crosswalk | The approved versioned crosswalk is missing, stale, ambiguous, lacks any required contract field, or does not contain one exact ProfileOptionName row | Supply or refresh the separately approved crosswalk; do not infer ownership from the module baseline or runtime values | Yes |
| Every profile-specific request | Blocker | resolve_profile_option_ownership_crosswalk | The crosswalk ModuleId does not exactly match one current Recruiting allowlist row | Correct the approved mapping or refresh the complete baseline from the approved Confluence section | No |
| Effective-value review | Blocker | read_effective_profile_values | Values are not from the authenticated current session, or ownership filtering occurs without the approved crosswalk | Re-read through Common Profile Options, then filter by exact approved ProfileOptionName rows | Yes |
| Definition, configured-value, or mutation request | Blocker | read_profile_option_definition | ProfileOptionName is partial, inferred, approximate, absent, or does not exactly match the approved crosswalk identity | Obtain one exact approved ProfileOptionName and pass it unchanged to Common Profile Options | Yes |
| Profile definition mutation | Blocker | | The request creates, updates, deletes, or changes the parent profile-option definition or any of its identity or level-capability metadata | Explain that this skill manages supported configured child values only | No |
| Site configured-value mutation | Blocker | read_profile_option_definition | SiteLevelEnabled or SiteLevelUpdatable is not `Y`, or the scope is not the exact `SITE` item | Select a currently enabled and updatable supported level | Yes |
| Product configured-value mutation | Blocker | resolve_product_application_scope | ProductLevelEnabled or ProductLevelUpdatable is not `Y`, or one exact approved application short name/scope key is not resolved | Supply current approved Product scope evidence and use its exact technical key | Yes |
| User configured-value mutation | Blocker | resolve_profile_user_identity | UserLevelEnabled or UserLevelUpdatable is not `Y`, exact provider-resolved UserName is missing, or create lacks the provider-resolved user GUID | Resolve one exact current user through Common Profile Options | Yes |
| Create configured value | Blocker | resolve_configured_profile_value | Exact absence is not established or the scoped item already exists | Resolve the collision or complete a fresh current-state read | Yes |
| Update or delete configured value | Blocker | resolve_configured_profile_value | One fresh exact scoped item and its returned identity are not established | Resolve and freshly read the exact Site, Product, or User item | Yes |
| Any configured-value mutation | Blocker | resolve_configured_profile_value | Profile identity, ownership, level, scope, protection metadata, or unrequested values would change | Restore preserved values and retain only the approved supported delta | Yes |
| Sensitive configured value | Blocker | resolve_configured_profile_value | Raw sensitive current or proposed content would be displayed, logged, or persisted | Use a redacted comparison and keep the mutation payload only in the delegated protected execution context | Yes |
| Mutation preview | Blocker | | Target environment, approved profile ownership, exact level/scope, current redacted state, requested delta, business impact, unchanged configuration, verification read, or approval fingerprint is absent | Rebuild the immutable minimal-change preview | Yes |
| Explicit CSV export or import | Blocker | | Export is not routed to task-level export, or import is not an explicitly requested, validated, and approved FSM package | Use the catalog route only for the explicit bulk request | Yes |
| Unsupported route | Blocker | | Direct REST, curl, OAuth handling, browser automation, UI, FSM, export/import, or another route would bypass Common Profile Options or an unsupported request | Explain the supported boundary and stop | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_profile_option_ownership_crosswalk | Every profile-specific request | Exact ProfileOptionName, ModuleId, display module name, evidence source/version, and baseline version | ora_reference_lookups.md |
| read_effective_profile_values | Effective values are requested | Current-session identities and effective values filtered only after approved ownership matching | ora_reference_lookups.md |
| read_profile_option_definition | Definition, configured-value, or mutation request | Exact identity plus current Site, Product, and User Enabled/Updatable flags and returned child metadata | ora_reference_lookups.md |
| resolve_configured_profile_value | Configured-value read or mutation | Exact scoped item, current redacted state, returned identity, protection metadata, or exact create absence | ora_reference_lookups.md |
| resolve_product_application_scope | Product level is selected | One exact approved application short name or scope key and evidence version | ora_reference_lookups.md |
| resolve_profile_user_identity | User level is selected | Exact provider-resolved UserName and GUID where create requires LevelValue | ora_reference_lookups.md |
| verify_profile_value_change | A delegated mutation returns | Exact fresh configured state or verified exact-item absence | ora_reference_lookups.md |

## Immutable Preview Contract

| Preview Element | Required Content |
|---|---|
| Business outcome | Desired Recruiting experience, intended users, timing, and expected result. |
| Target | Exact environment, ProfileOptionName, approved ModuleId/display name and evidence versions, selected level, and exact `SITE`, Product key, or provider-resolved User identity. |
| Current state | Fresh exact definition and configured child fields actually returned, with sensitive values redacted. |
| Requested delta | Only the exact supported configured-value create, update, or delete. |
| Impact and unchanged configuration | Business impact plus explicit preservation of the parent definition, ownership, level, scope, protection metadata, and unrequested values. |
| Verification | Fresh exact configured-value read after create/update or verified scoped-item absence after delete. |
| Approval fingerprint | Immutable environment, profile identity, ownership receipt, level/scope, minimal payload or delete target, current-state receipt, and verification plan. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RPO.ENFORCE | decision | 7 | design_enforcement | create->RPO.PREVIEW;update->RPO.PREVIEW;delete->RPO.PREVIEW;blocked->RPO.DESIGN_ISSUES | RPO.RESOLVE_SCOPE | stop | A configured-value mutation has exact approved ownership, current definition, level capability, scope, and state evidence |
