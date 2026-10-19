# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Recruiting ModuleId baseline | Use the complete versioned set of concrete LBA ModuleId rows from the approved Supported Modules table. |
| 2 | Profile-option ownership crosswalk | Require one approved current mapping from exact ProfileOptionName to an approved ModuleId, display module name, evidence source, and version. |
| 3 | Current definition | Read the exact permitted profile definition and its level-enabled and level-updatable flags. |
| 4 | Target scope and current configured value | Resolve Site, exact approved Product key, or exact User identity and freshly read the current configured value. |
| 5 | Immutable approval and verification | Bind one exact approval to the preview, then re-read the exact configured value after the delegated mutation. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| RPO_MODULE_BASELINE | Recruiting ModuleId baseline | Yes | Every request | Satisfied | Complete task-local allowlist from the complete table provided 2026-10-06 |  | Establishes which module mappings are Recruiting-owned but does not authorize a ProfileOptionName by itself | Refresh the whole baseline only from the approved Supported Modules table | Approved ModuleId set and baseline version |
| RPO_OWNERSHIP_CROSSWALK | Approved profile-option ownership crosswalk | Yes | Every request | Lookup | Approved versioned project or repository evidence with ProfileOptionName, approved Recruiting ModuleId, display module name, evidence source, and evidence version | resolve_profile_option_ownership_crosswalk | Common Profile Options cannot list or filter definitions by ModuleId | Supply or refresh one approved crosswalk; missing or stale evidence blocks | Exact ProfileOptionName, ModuleId, display module name, source, and version |
| RPO_DEFINITION | Current profile definition | Yes | Definition, configured-value, or mutation request | Verify | Delegated Common Profile Options exact definition read | read_profile_option_definition | Establishes exact identity and enabled/updatable levels | Use the exact approved ProfileOptionName | Business label, exact name, level flags, and configured-value links |
| RPO_PRODUCT_SCOPE | Product/application scope key | Conditional | Product configured-value operation | Lookup | Approved product/application scope evidence | resolve_product_application_scope | Product values require an exact supported application short name or LevelValue | Supply approved exact scope evidence; do not provide only a display label | Exact application scope key and evidence version |
| RPO_USER_IDENTITY | User identity | Conditional | User configured-value operation | Lookup | Delegated Common Profile Options profile-user resolution | resolve_profile_user_identity | User create requires the exact GUID while item reads use the exact user identity | Supply the intended user identity for provider resolution | Exact user item identity and GUID for create when returned |
| RPO_CURRENT_VALUE | Current configured value | Yes | Configured-value read or mutation | Verify | Delegated level-specific child read | resolve_configured_profile_value | Establishes current redacted state, identity, scope, and mutation basis | Resolve one exact Site, Product, or User child | Current value receipt, level, scope key, and returned identity |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Baseline and crosswalk are current and the exact ProfileOptionName maps once to an approved ModuleId | Yes; continue to provider reads |
| Scope evidence required | Product key or user identity is missing | No mutation; obtain exact scope evidence |
| Blocked | Baseline is stale, crosswalk is missing/stale/ambiguous, or the profile is unmapped | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RPO.CHECK_EVIDENCE | decision | 2 | resolve_dependency | effective->RPO.READ_EFFECTIVE;exact->RPO.MATCH_OWNERSHIP;blocked->RPO.EVIDENCE_ISSUES | RPO.VALIDATE | stop | Ownership and scope dependencies must be evaluated before profile reads or mutations |
