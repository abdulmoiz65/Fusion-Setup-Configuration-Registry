# Categories Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Profile-option applicability | Determine unified-listing/CAP and search-design triggers; read every applicable current effective value before proposal or execution |
| 2 | Profile prerequisites and decisions | Record correct options as satisfied, require applicable CAP readiness, omit satisfied options from dialog, and bind every proposed change to exact approval and readback |
| 3 | Feature, access, and identity | Require the Category/Topic option at Site Y, related privileges and HCM data-role access, Category subtype, exact existing identity when applicable, and runtime-required create values |
| 4 | Parent definition | Validate user-provided title, title-only summary generation, Active creation, visibility, featured dates, branding, and DFF values |
| 5 | Relationship and membership integrity | Resolve Topics, people, role-compatible methods, current membership, parent-specific duplicates, asynchronous behavior, and one-manager minimum |
| 6 | Capability and approval safety | Verify each requested write contract, preserve stable parent/child rows, refresh profile and Category state, and bind approval to the immutable proposal fingerprint |
| 7 | Verification | Execute parent before eligible children, isolate failures, and read back every profile, parent, and child operation |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Before every proposal or execution | Blocker | resolve_category_profile_option | Applicable current effective profile-option values have not been read through the Application Profile Option Foundation capability | Read each triggered exact code before asking for a decision | Yes |
| Any applicable option is already correct | Blocker | resolve_category_profile_option | The satisfied option is unnecessarily shown as a decision or proposed change | Record it as satisfied and omit it from the user dialog | Yes |
| Every executable request | Blocker | resolve_category_profile_option | ORA_WLF_CATG_TOP_REDWOOD_ENABLED is not Site Y and its exact Site-level change is not approved and read back | Put the exact change in the immutable approval payload, route it through the governed provider, and verify readback | Yes |
| Unified listing or CAP-based administration applies | Blocker | verify_category_catalog_profile_prerequisite | Applicable Catalog Administration Profiles are not already created or validated | Complete or validate CAPs through their separate excluded scope; do not implement them here | Yes |
| Unified listing or CAP-based administration applies | Blocker | resolve_single_catalog_listing_profile | ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD is not Site Y and its exact change/readback or intended administrator access test is missing | After CAP readiness, approve and read back Site Y and verify intended category/catalog administrator access | Yes |
| Category search is designed or tuned | Blocker | resolve_category_search_mode_profile | Broader recall, balanced matching, or tighter precision is undecided; an exact value change lacks approval/readback; or representative searches are not tested | Preserve current unless an exact change is approved, then read back and test representative searches | Yes |
| Every executable request | Blocker | resolve_category_access | Learning administrator view/manage privilege, related Category/Topic privileges, intended-role HCM data-role access, Category manager/all-items access, or operation access is missing or unverified | Obtain the exact privilege, data-role, and row access after profile readiness | Yes |
| Create | Blocker | resolve_category_field_values | Title is not user-provided, Category subtype or Active value is unresolved, or a runtime-required number/field lacks a confirmed value | Supply the title and missing runtime value; select only exact enabled Category/Active codes | Yes |
| Create with omitted visibility | Blocker | resolve_category_field_values | The current Open value and default behavior are not confirmed and disclosed | Resolve Open or have the user choose another target-supported visibility | Yes |
| Summary generation | Blocker | | Generation is disabled, uses anything beyond the supplied title, is not labeled, or is absent from the exact approved proposal | Use user-authored text, proceed blank, or disclose and approve text generated only from the supplied title | Yes |
| Parent or association featured dates | Blocker | | End is supplied without start, a date is ambiguous, or start is after end | Correct the dates or omit both | Yes |
| Similar Category title | Warning | resolve_category_identity | The request has not reviewed likely duplicates or create-versus-update intent | Show persisted number/ID candidates and retain the user's explicit intent | Yes |
| Existing Category | Blocker | resolve_category_identity | ID/number does not resolve exactly, title is ambiguous, subtype is not Category, or current state is incomplete | Correct or select one exact accessible Category and refresh state | Yes |
| Add, feature, or remove Topic | Blocker | resolve_category_topic | Topic is missing, inaccessible, ambiguous, wrong subtype, self-referential, duplicated under the same Category, or changed after approval | Correct/select the Topic and refresh the parent-specific relationship | Yes |
| Add, feature, or remove Topic | Blocker | inspect_category_topic_capability | Exact registered Category-to-Topic route, request representation, method, or association key is unverified | Obtain the target-confirmed contract or defer only the Topic child row | Yes |
| Remove Topic association | Blocker | resolve_category_topic | The proposal does not identify the one parent relationship being removed or acknowledge that the Topic and its other Category relationships remain | Show and approve the exact association effect | Yes |
| Manager addition | Blocker | resolve_category_person | The request uses anything other than one exact person selection | Select one target-visible person; reserve CSV, filtered-list, analysis, user-group, hierarchy-manager, and directs methods for member work | Yes |
| Required or voluntary member operation | Blocker | inspect_category_membership_capability | The requested person, CSV, filtered-list, analysis, user-group, hierarchy-manager, directs, criteria, group, or withdrawal contract is unavailable | Choose a confirmed method or defer only affected child rows | Yes |
| Person-based membership | Blocker | resolve_category_person | A person does not resolve to one active target-visible identity | Supply a technical ID/number, exact work email, or select one name match | Yes |
| Manager removal | Blocker | read_category_membership_state | Current or projected state has fewer than one active Category manager | Retain or add an active manager before removal | Yes |
| Criteria/group membership | Blocker | read_category_membership_state | Pending versus active state, Once/Continuous behavior, automated withdrawal, or asynchronous row results cannot be represented and verified | Refresh membership state and use only the confirmed processing contract | Yes |
| Branding image | Blocker | inspect_category_asset_capability | The file violates current extension, MIME, size, upload, or processing rules | Correct or exclude only the asset operation; preserve valid parent work | Yes |
| DFF values | Blocker | resolve_category_dff_metadata | Context or segment is absent, incompatible, read-only, or invalid in the current target | Use only exact current Category-applicable metadata | Yes |
| Direct learning, skills, qualifications, contributions, or self-service conversation | Blocker | | The request applies a Topic-only operation directly to a Category | Route the operation to a Topic or remove it from the Category proposal | No |
| Draft, deactivate, reactivate, delete-object, or generic upsert | Blocker | | The request exposes an operation excluded by OLC-120246 even if generic metadata advertises it | Use supported Active create/retrieve/update scope; do not invoke the excluded method | No |
| Any approved profile, parent, or child row | Blocker | resolve_category_identity | Environment, applicable option, Category, manager set, Topic relationship, field value, privilege, data role, or capability fingerprint changed after approval | Rebuild the affected proposal and obtain new approval | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_category_profile_option | Every executable request | Exact option value, level, effective evidence, and timestamp | ora_reference_lookups.md |
| resolve_single_catalog_listing_profile | Unified listing or CAP-based administration applies | Trigger, Site-level value, CAP readiness, exact proposed change, approval/readback, and administrator access-test evidence | ora_reference_lookups.md |
| verify_category_catalog_profile_prerequisite | Unified listing or CAP-based administration applies | Applicable CAP identity, validation state, intended administrator, and current evidence | ora_reference_lookups.md |
| resolve_category_search_mode_profile | Category search is designed or tuned | Trigger, current value, approved search intent/exact value, readback, and representative-search results | ora_reference_lookups.md |
| resolve_category_access | Every request and immediately before mutation | Privilege, access scope, permitted action evidence, and timestamp | ora_reference_lookups.md |
| resolve_category_field_values | Subtype, status, or visibility is used | Enabled code/meaning, field mapping, and effective evidence | ora_reference_lookups.md |
| resolve_category_identity | Duplicate review, existing operation, preview, stale-state check, or readback | Exact identity, subtype, state, returned links, last-modified evidence, current children, and fingerprint | ora_reference_lookups.md |
| resolve_category_topic | Topic relationship is requested | Exact Topic identity/subtype, accessibility, parent-specific association state, item link, and fingerprint | ora_reference_lookups.md |
| inspect_category_topic_capability | Topic add/date update/removal is requested | Registered child route, method, request fields, association key, and action support | ora_reference_lookups.md |
| resolve_category_person | Person-based manager/member is supplied | Exact active person identity and match evidence | ora_reference_lookups.md |
| inspect_category_membership_capability | Membership or group work is requested | Supported method, route, request fields, role/status, processing behavior, privilege, and async contract | ora_reference_lookups.md |
| read_category_membership_state | Membership work or stale-state check is requested | Active manager count, member and criteria states, row/process results, and fingerprint | ora_reference_lookups.md |
| inspect_category_asset_capability | Branding is supplied | Exact file limits, request fields, processing contract, and readback link | ora_reference_lookups.md |
| resolve_category_dff_metadata | DFF values are supplied | Current context, segment identity, schema, allowed values, and writable mapping | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAT.ENFORCE_DESIGN | decision | 5 | design_enforcement | passed->CAT.EXECUTION_GATE;blocked->CAT.HANDLE_ERROR | CAT.APPLY_DEFAULTS | stop | Validated profile decisions and Category parent/child rows have completed applicable dependencies, lookups, defaults, and prerequisite readbacks |
