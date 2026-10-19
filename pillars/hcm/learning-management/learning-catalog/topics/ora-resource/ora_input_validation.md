# Topics Input Validation

Sources: OLC-116681 FDD v7 section 7.0 and OLC-120247, page 21981496001
updated 2026-09-22 15:54:32, the approved Learning taxonomy and baseline
supplied by the developer, and the supplied raw target learningCommunities
Describe.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Request identity | Target environment, requested operation, and stable parent or child row identifier | Stop the affected row before proposal | Supply one exact environment, supported operation, and row identity | All requests | |
| Profile-option context | Whether unified Redwood catalog listing or CAP-based administration applies; whether Topic catalog-search behavior is being designed or tuned; intended Topic or catalog administrator role | Stop the applicable dependency proposal when its trigger or intended role is unclear | Confirm each trigger and intended role; read current effective values before asking for a decision | Before proposal or execution | resolve_topic_profile_option |
| New Topic identity | Nonblank user-provided title; optional number; requested summary behavior | Ask for the title and perform no write | The user must provide the Topic title; generated text may apply only to summary | Create | |
| Existing Topic identity | learningItemId, learningItemNumber, or title plus explicit selection when ambiguous | Stop before proposal for that action | Resolve one accessible object of the Topic subtype | Retrieve, update, or child operation | resolve_topic_identity |
| Parent definition | Topic subtype, Active-on-create intent, visibility, optional featured dates, summary, contribution setting, and required DFFs | Return the exact unresolved fields | Resolve target-supported values and tenant-required fields | Create or parent update | resolve_topic_runtime_values |
| Category relationship row | Parent row ID, requested action, Category ID, number, or title, and optional association featured dates | Block only that child row | Resolve one accessible Category and an exact registered relationship capability | Category association is requested | resolve_topic_category |
| Catalog learning row | Parent row ID, requested action, learning ID, number, or title, intended allowed subtype, and optional association featured dates | Block only that child row | Resolve one accessible self-paced item, standalone event, course, or learning path | Learning association is requested | resolve_topic_catalog_learning |
| Membership or contribution row | Parent row ID, requested membership action, one supported selection method, member type or status, person or criteria identity, and contribution intent | Block only the affected child row | Resolve current membership capability, persons, manager set, and supported values | Membership, group, pending request, type change, reconciliation, or contribution is requested | resolve_topic_capability |
| Skill or qualification row | Parent row ID, reference type, exact ID, number, or title, and requested association action | Block only that child row | Resolve one active accessible post-create reference and write capability | Skill or qualification maintenance is requested | resolve_topic_skill_qualification |
| Media, related material, or DFF row | Parent row ID, child type, file or URL metadata, visibility, and exact DFF context or segment when applicable | Block only the affected child unless a required DFF blocks the parent | Resolve target limits, child capability, and current DFF metadata | Optional child data is supplied | resolve_topic_dff |
| Approval evidence | Immutable versioned proposal, exact included rows, every applicable proposed profile-option change, current-state fingerprint, and fresh explicit approval | Stop before mutation | Refresh applicable evidence and obtain approval for the exact proposal | Profile-option, parent, or child mutation | read_topic_relationships |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Current effective values have not been read for every applicable profile option | Operation Blocked | Read the applicable exact codes through the Application Profile Option Foundation capability before asking for a decision | resolve_topic_profile_option |
| ORA_WLF_CATG_TOP_REDWOOD_ENABLED is not Site Y | Operation Blocked | Include an exact Site Y change in approval when needed and read it back before Topic execution | resolve_topic_profile_option |
| Related Category/Topic privilege, manager/all-items scope, or HCM data-role access is unresolved | Operation Blocked | Validate the intended role after the Category/Topic Site value is Y | resolve_topic_access |
| Unified catalog listing or CAP-based administration applies and ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD is not Site Y | Dependency Blocked | Create or validate applicable Catalog Administration Profiles through their separate excluded scope, then approve and read back the exact Site Y change | resolve_topic_profile_option |
| Unified catalog listing or CAP-based administration applies and applicable CAP readiness or intended administrator access is unverified | Dependency Blocked | Create or validate the applicable Catalog Administration Profiles through their separate excluded scope and provide current readiness evidence; do not perform CAP setup here | |
| Topic search is being designed or tuned and ORA_WLF_SS_CATALOG_SEARCH_MODE needs a user decision | Decision Required | Ask for broader recall, balanced matching, or tighter precision; preserve the current value unless an exact change is approved, read back, and tested | resolve_topic_profile_option |
| Topic subtype, Active status, visibility, membership, contribution, or moderation value is unresolved | Lookup required | Resolve one current enabled code for the owning attribute | resolve_topic_runtime_values |
| A requested child write has no exact registered capability | Operation blocked | Preserve other valid operations and report the missing route precisely | resolve_topic_capability |
| A Category, learning, person, skill, qualification, rating, asset, or related-material reference is missing, inactive, inaccessible, ambiguous, or wrong subtype | Invalid child row | Correct, select, or explicitly exclude that child before a revised proposal | resolve_topic_category |
| A relationship already exists | No-op or blocked | Mark an identical add as No-op; require a supported update for changed association dates | read_topic_relationships |
| A membership action would leave zero active managers | Blocked | Preserve at least one current or approved replacement manager | read_topic_relationships |
| Topic, manager set, or affected relationship changed after approval | Stale | Skip the affected action, invalidate approval, refresh, and re-propose | read_topic_relationships |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Title is user-provided and valid | Reject blank, generated, or over-limit identity; never infer a Topic title | Create | |
| Existing target is one Topic | Reject zero, multiple unresolved, inaccessible, Category, or Official Community results | Non-create operation | resolve_topic_identity |
| Summary and rich text are valid | Enforce current length, markup, and safety rules; generate only from the user-supplied title when enabled and permitted, then keep the result labeled and editable | Summary is supplied or generated | |
| Visibility and subtype are target-supported | Reject unresolved, disabled, expired, ambiguous, or cross-attribute values | Create or applicable update | resolve_topic_runtime_values |
| Featured dates are coherent | Reject an end without a start or start later than end; keep parent and association dates independent | Parent or association dates are supplied | |
| Category relationship is valid | Require one accessible Category and reject wrong subtype, duplicate, unsupported write route, self-reference, or cycle | Category child row is included | resolve_topic_category |
| Catalog learning subtype is allowed | Permit only self-paced learning, standalone event, course, or learning path; reject Category, Topic, self, duplicate, inactive, or inaccessible items | Catalog child row is included | resolve_topic_catalog_learning |
| Person identity is writable | Require one active person and persist the service-required person ID rather than a display label | Membership person row is included | resolve_topic_person |
| Manager safety is preserved | Reject any individual or bulk result with fewer than one active manager | Manager or membership state changes | read_topic_relationships |
| Criteria and group behavior is supported | Require a confirmed selection method, Once or Continuous rule, withdrawal behavior, and current group capability | Criteria, group, or reconciliation is requested | resolve_topic_capability |
| Contribution and moderation access is explicit | Reject missing capability or privilege and distinguish contribution from manager access | Contribution or rating action is requested | resolve_topic_access |
| Skill and qualification is post-create | Reject creation-time serialization, inactive references, and missing capability | Skill or qualification row is included | resolve_topic_skill_qualification |
| Asset and related material is valid | Enforce target extension, MIME, size, URL, upload, processing, and visibility constraints | Media or related material is supplied | resolve_topic_capability |
| DFF segment is current | Reject absent, disabled, wrong-context, invalid, or unresolved required segments | DFF data is supplied or required | resolve_topic_dff |
| Profile-option dialog | Omit applicable options already correctly populated; show only triggered options needing a user decision or change | Before proposing dependency work | resolve_topic_profile_option |
| Profile-option change | Require exact option code, current and effective value, Site scope, proposed value, trigger, CAP prerequisite evidence when applicable, representative search test when applicable, approval, and post-change readback | An applicable option change is proposed | resolve_topic_profile_option |
| Batch graph is acyclic | Reject parent-child cycles, self-reference, duplicate edges, and children of failed parent rows | Multi-row or grouped request | |
| Operation is in scope | Permit create, retrieve, update, and confirmed child operations; reject Draft, deactivate, reactivate, and object delete | All requests | resolve_topic_capability |
| Approved selection is unchanged | Invalidate approval when a row, child, default, reference, environment, or fingerprint changes | After proposal | read_topic_relationships |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TOP.VALIDATE_INPUT | decision | 1 | validate_input | valid->TOP.CHECK_DEPENDENCIES;invalid->TOP.HANDLE_ERROR | none | stop | One or more Topic parent or child rows are normalized |
| TOP.EVALUATE_RESULT | decision | 7 | evaluate_result | verified->TOP.RETURN_SUCCESS;issues->TOP.HANDLE_ERROR | TOP.EXECUTION_GATE | stop | Validation or mutation evidence is reconciled with the approved Topic proposal and row selection |
