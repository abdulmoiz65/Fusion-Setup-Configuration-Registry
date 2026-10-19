# Topics Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Profile, access, and parent readiness | Validate target, all applicable profile-option values and prerequisites, intended-role privilege and HCM data-role access, user-provided title, Topic subtype, Active status, visibility, DFFs, and current parent state |
| 2 | Relationship integrity | Resolve Category and catalog learning references, exact capabilities, dates, duplicates, self-reference, and graph cycles |
| 3 | Membership and optional-child integrity | Preserve one manager and validate membership, contributions, skills, moderation, media, related materials, and independent child outcomes |
| 4 | Proposal and execution safety | Show defaults and impacts, preserve stable row selection, recheck fingerprints, require exact approval, and verify each attempted result |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any mutation | Blocker | resolve_topic_profile_option | ORA_WLF_CATG_TOP_REDWOOD_ENABLED is not confirmed as effective Site Y, or a required change lacks exact approval or readback | Preserve an already-correct value or approve and read back the exact Site Y change through the foundation capability | Yes |
| Unified catalog listing or CAP-based administration | Blocker | resolve_topic_profile_option | ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD is not effective Site Y, applicable CAP readiness is absent, or the exact change lacks approval or readback | Create or validate CAPs through their separate excluded scope, then approve and verify only the profile change | Yes |
| Topic catalog-search design or tuning | Blocker | resolve_topic_profile_option | Current search mode is unread, the recall/precision preference is unresolved, or a proposed change lacks exact approval, readback, or representative testing | Preserve the current value or approve one explicit broader, balanced, or tighter setting and test representative searches | Yes |
| Any managed operation | Blocker | resolve_topic_access | Applicable manage privilege, HCM data-role access, or manager-scoped or all-items access is absent | Use an authorized caller with the required role and data scope | Yes |
| Create | Blocker | resolve_topic_runtime_values | Title is absent or generated, Topic subtype is unresolved, or Active status is not target-confirmed | Supply the title and resolve exact current values | Yes |
| Create without Category | Allowed | | No Category relationship is supplied | Create the Topic as standalone and disclose that Categories can be associated later | Not needed |
| Category relationship | Blocker | resolve_topic_category | Reference is missing, ambiguous, inaccessible, wrong subtype, duplicate, self-referential, cyclic, stale, or lacks an exact registered write capability | Correct or exclude the child row; never serialize it as catalog learning | Yes |
| Catalog learning relationship | Blocker | resolve_topic_catalog_learning | Item is missing, ambiguous, inaccessible, inactive, unsupported, Category, Topic, self, duplicate, stale, or lacks an exact association capability | Select one allowed accessible learning item or exclude the child row | Yes |
| Association featured dates | Blocker | read_topic_relationships | End has no start, start is after end, or parent dates are substituted for relationship dates | Correct and preserve the dates on the exact association | Yes |
| Membership or group change | Blocker | read_topic_relationships | Method or capability is unsupported, rows mix incompatible states, graph is stale, or final active manager count is zero | Select one supported method, refresh membership, and preserve a manager | Yes |
| Member contributions | Blocker | resolve_topic_capability | Target capability or privilege is absent, or learner-facing effect is not disclosed | Keep disabled or obtain exact capability, privilege, and approval | Yes |
| Skill or qualification | Blocker | resolve_topic_skill_qualification | Topic does not yet exist or reference or post-create capability is invalid | Create and verify the Topic first, then use one exact active reference | Yes |
| Rating or comment moderation | Blocker | resolve_topic_access | Moderation privilege, Topic access, exact action, or registered capability is absent | Preserve read-only access and defer the mutation | Yes |
| Media, related material, conversation, or DFF | Blocker | resolve_topic_capability | Child contract, limits, processing, visibility, required segment, or readback route is unresolved | Correct or exclude the optional child; resolve a tenant-required DFF before parent execution | Yes |
| Draft, deactivate, reactivate, or Topic delete | Blocker | | Operation is outside OLC-120247 current 26C scope | Return a scoped unsupported result without invoking root DELETE or a status change | No |
| Multi-row request | Blocker | | Graph contains a cycle, self-edge, duplicate edge, or child of a failed parent | Correct the graph and issue a revised versioned proposal | Yes |
| Any approved row | Blocker | read_topic_relationships | Environment, included rows, Topic, manager set, reference, relationship, capability, or fingerprint changed | Skip the stale action, rebuild the proposal, and obtain new approval | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_topic_profile_option | Any mutation or applicable conditional profile trigger | Exact applicable code, trigger, current/effective Site value, prerequisite state, approval, readback, and test evidence when relevant | ora_reference_lookups.md |
| resolve_topic_access | Managed, contribution, or moderation operation | Manage result, HCM data-role result, manager or all-items scope, and operation privilege | ora_reference_lookups.md |
| resolve_topic_runtime_values | Create or lookup-backed update | Topic subtype, Active status, visibility, and requested current codes | ora_reference_lookups.md |
| resolve_topic_identity | Duplicate review, non-create action, stale-state comparison, or readback | Exact identity, subtype, item link, current state, and fingerprint | ora_reference_lookups.md |
| resolve_topic_capability | Any child write beyond confirmed root create or update | Exact registered route, method, keys, writable fields, and readback | ora_reference_lookups.md |
| resolve_topic_category | Category relationship | Category identity, subtype, state, link, and relationship evidence | ora_reference_lookups.md |
| resolve_topic_catalog_learning | Catalog association | Allowed learning identity, subtype, state, link, and relationship evidence | ora_reference_lookups.md |
| resolve_topic_person | Person membership row | Exact person ID, active state, display evidence, and match count | ora_reference_lookups.md |
| resolve_topic_skill_qualification | Skill or qualification child | Exact active reference, type, route, and readback evidence | ora_reference_lookups.md |
| resolve_topic_dff | Supplied or required DFF | Context, segment, type, required flag, and validated value | ora_reference_lookups.md |
| read_topic_relationships | Existing parent or child operation | Manager count, relationship keys, impact, current state, and fingerprint | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TOP.ENFORCE_DESIGN | decision | 5 | design_enforcement | passed->TOP.EXECUTION_GATE;blocked->TOP.HANDLE_ERROR | TOP.APPLY_DEFAULTS | stop | Validated Topic rows have completed applicable dependencies, lookups, and defaults |
