# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Business outcome | Desired Recruiting outcome, affected process or user experience, intended audience, timing, and requested behavior | Return a business-language issue | Ask only for the missing business decision | Every request | |
| Requested operation | Review effective values, read a definition, review configured values, or create/update/delete one configured value | Return a business-language issue | Resolve the technical operation internally and clarify only a genuine ambiguity | Every request | |
| Approved ownership crosswalk | Versioned ProfileOptionName, approved Recruiting ModuleId, display module name, evidence source, and evidence version | Block all profile-specific results and mutations | Obtain or refresh the approved crosswalk; the ModuleId baseline alone is insufficient | Every request | resolve_profile_option_ownership_crosswalk |
| Exact profile identity | One exact ProfileOptionName appearing exactly once in the approved crosswalk | Block definition/configured read or mutation | Resolve from approved evidence; do not infer from prefixes, descriptions, effective values, or user-provided values | Definition, configured value, or mutation | resolve_profile_option_ownership_crosswalk |
| Configuration level | Site, Product, or User | Block configured-value operation | Ask which business scope is intended only when it cannot be resolved from the request | Configured read or mutation | read_profile_option_definition |
| Target scope | Site; exact supported product/application key from approved evidence; or exact user identity resolvable by Common Profile Options | Block configured-value operation | Obtain the required business scope and approved technical evidence | Product or User configured value | resolve_configured_profile_value |
| Target environment and delta | Exact Fusion environment and requested configured value change | Block mutation preview | Ask for the missing target or business decision | Create, update, or delete | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Module baseline is current and complete but crosswalk is absent | Blocked | Request the approved versioned crosswalk; do not authorize from ModuleId alone | resolve_profile_option_ownership_crosswalk |
| ProfileOptionName has one crosswalk row mapped to a current approved ModuleId | In scope | Continue to current definition and configured-value reads | resolve_profile_option_ownership_crosswalk |
| ProfileOptionName is missing, duplicated, or maps outside the ModuleId baseline | Blocked | Correct or refresh approved ownership evidence | resolve_profile_option_ownership_crosswalk |
| Requested level is not both enabled and updatable | Blocked | Explain that the configured value cannot be changed at that level | read_profile_option_definition |
| Product scope key or user identity is unresolved | Blocked | Obtain exact approved product scope evidence or use the Common Profile Options user resolver | resolve_configured_profile_value |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Effective values | Read effective values for the current authenticated session, then retain only identities that match the approved ownership crosswalk | Effective review | read_effective_profile_values |
| Definition identity | Read one approved definition using its exact ProfileOptionName | Definition or configured-value operation | read_profile_option_definition |
| Level eligibility | Require both Enabled and Updatable to equal `Y` for the selected Site, Product, or User level before mutation | Configured-value mutation | read_profile_option_definition |
| Site scope | Use only the supported `SITE` item identity and permit at most one current value | Site configured value | resolve_configured_profile_value |
| Product scope | Require the exact supported application short name or scope key from approved evidence; never derive it from a display label | Product configured value | resolve_product_application_scope |
| User scope | Require the Common Profile Options workflow to resolve the exact user GUID; never use a display name as the GUID | User configured value | resolve_profile_user_identity |
| Definition boundary | Reject create, update, or delete of a profile-option definition | Any definition mutation | |
| Preservation | Preserve ProfileOptionName, approved Recruiting ownership mapping, level, scope key, identity, and every unrequested field | Configured-value mutation | resolve_configured_profile_value |
| Sensitive value handling | Redact sensitive configured values in previews, output, diagnostics, and persisted artifacts; never persist credentials, tokens, or headers | Every read or mutation | |
| Explicit bulk boundary | Use task CSV export or FSM CSV import only when explicitly requested; never as the default read or configured-value CRUD route | Export or import | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RPO.VALIDATE | decision | 1 | validate_input | effective->RPO.CHECK_EVIDENCE;definition->RPO.CHECK_EVIDENCE;configured->RPO.CHECK_EVIDENCE;create->RPO.CHECK_EVIDENCE;update->RPO.CHECK_EVIDENCE;delete->RPO.CHECK_EVIDENCE;post_change->RPO.VERIFY_VALUE;issues->RPO.INPUT_ISSUES | none | stop | Every Recruiting and Candidate Experience Profile Option Values request |
