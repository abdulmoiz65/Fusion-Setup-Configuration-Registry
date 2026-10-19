# Categories Input Validation

Sources: OLC-116681 FDD v7 section 6.0 and OLC-120246, page 21981496001
updated 2026-09-22 15:54:32, the approved Learning Management Guide Skill
Baseline snapshot, the approved Learning taxonomy CSV, and the supplied raw
target `learningCommunities` Describe reviewed 2026-09-22.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Request identity | target environment; requested operation; stable parent and child row identifiers | Stop the affected row before preview | Supply one exact environment, supported operation, and stable row identity | All requests | |
| Profile-option context | whether unified Redwood catalog listing or CAP-based administration applies; whether catalog search behavior is being designed/tuned; intended category or catalog administrator role | Stop the applicable dependency proposal when its trigger or intended role is unclear | Confirm each trigger and intended role; read current effective values before asking for a decision | Before proposal or execution | resolve_category_profile_option |
| Category create definition | user-provided learningItemTitle; optional supplied learningItemNumber or a target-confirmed generated-number contract; optional summary; visibility; featured start/end dates; optional branding and DFF values | Ask for a user-provided title and perform no write; block when another runtime-required field cannot be resolved | Supply a nonblank title and any unresolved runtime-required value; select or approve the remaining proposed values | Create | |
| Existing Category identity | learningItemId, learningItemNumber, or exact title plus a selected unique subtype-filtered match | Stop the affected operation | Supply an ID or number, or select one exact accessible Category title result | Retrieve, update, Topic relationship, membership, or branding operation | resolve_category_identity |
| Topic child identity | parent stable row ID; Topic learningItemId, learningItemNumber, or exact title; requested association operation; optional association featured dates | Block only the ambiguous or unlinked child row | Link the row to one Category and supply or select one exact accessible Topic | Add, feature, update, or remove a Topic association | resolve_category_topic |
| Membership child identity | parent stable row ID; manager/required/voluntary role; person selection for manager additions; supported person, CSV, filtered-list, analysis, user-group, hierarchy-manager, or directs selection for member work; person or criteria reference | Block only the invalid or unlinked child row | Link the row to one Category and complete the exact role-compatible runtime contract | Add, update, or remove managers or members | |
| Exact approval | immutable proposal version; normalized request fingerprint; exact environment; every applicable proposed profile-option change; selected parent/child row IDs; operation; relationship and asynchronous effects | Stop before every mutation | Approve the unchanged proposal after all blocking corrections | Profile-option, create, update, or child mutation | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Current effective values have not been read for every applicable profile option | Operation Blocked | Read the applicable exact codes through the Application Profile Option Foundation capability before asking for a decision | resolve_category_profile_option |
| ORA_WLF_CATG_TOP_REDWOOD_ENABLED is not Site Y, or related Category/Topic privilege and HCM data-role access is unresolved | Operation Blocked | Include an exact Site Y change in approval when needed, read it back, and validate the intended role's access | resolve_category_profile_option |
| Unified catalog listing or CAP-based administration applies and ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD is not Site Y | Dependency Blocked | Create or validate applicable Catalog Administration Profiles through their separate excluded scope, then approve and read back the exact Site Y change | resolve_single_catalog_listing_profile |
| Category search is being designed/tuned and ORA_WLF_SS_CATALOG_SEARCH_MODE needs a user decision | Decision Required | Ask for broader recall, balanced matching, or tighter precision; preserve the current value unless an exact change is approved, read back, and tested | resolve_category_search_mode_profile |
| Category subtype, Active value, or requested visibility is unresolved | Operation Blocked | Resolve the current field values and retain both system code and translated meaning | resolve_category_field_values |
| Existing identity resolves to zero, multiple, inaccessible, or wrong-subtype records | Row Blocked | Correct the identifier or select one exact Category | resolve_category_identity |
| Topic identity resolves to zero, multiple, inaccessible, wrong-subtype, self-reference, or an already-associated row | Child Row Blocked | Correct, select, remove, or exclude only that Topic row | resolve_category_topic |
| A Topic association write contract is not registered and verified for the target | Child Operation Blocked | Preserve the proposal and obtain the target-confirmed child route and payload contract | inspect_category_topic_capability |
| A membership selection or group operation is unsupported or its exact target contract is not verified | Child Operation Blocked | Select a supported method or obtain the target-confirmed capability | inspect_category_membership_capability |
| A membership change would leave no active Category manager | Parent Operation Blocked | Retain or add an active manager before approving the removal | read_category_membership_state |
| Category, manager set, profile option, privilege, or Topic relationship changed after approval | Approval Stale | Reread dependencies and issue a new proposal version and fingerprint | resolve_category_identity |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Title | Require nonblank user-provided text within the runtime length limit; never generate a Category title | Create or title update | |
| Learning item number | Accept a supplied valid number, or use server generation only when the current target contract proves it and shows the persisted number in readback | Create | |
| Summary | Validate current text/rich-text rules; when generation is enabled, derive the proposal only from the supplied title, label it generated, and require approval; blank remains a warning | Summary is supplied or generated | |
| Category subtype | Require exactly the target-supported Category subtype; never infer it from endpoint name or title | Every parent read or write | resolve_category_field_values |
| Visibility | Require one target-supported Open, Closed, or Secret value; retain its system code; an omitted value may use only a confirmed and disclosed Open default | Create or visibility update | resolve_category_field_values |
| Featured dates | Parse unambiguously; end requires start; start must be on or before end; omitted dates mean not featured | Parent or association dates are supplied | |
| Branding image | Validate current extension, MIME, size, upload, and processing limits before child execution; isolate processing failure from parent creation | Branding is supplied | inspect_category_asset_capability |
| DFF values | Require exact current context, segment, data type, length, and allowed value | DFF data is supplied | resolve_category_dff_metadata |
| Topic association | Require one accessible Topic, no self-reference or duplicate under the same Category, valid association dates, and a verified write contract | A Topic child row is selected | resolve_category_topic |
| Person reference | Accept full name, person number, work email, or technical person ID; require selection for multiple name matches and persist the target-required person ID | A person-based manager or member is supplied | resolve_category_person |
| Manager selection | Require person selection for every manager addition; do not apply CSV, filtered-list, analysis, user-group, hierarchy-manager, or directs selection to a manager-add row | A manager is added | resolve_category_person |
| Member criteria | Require a target-supported person, CSV, filtered-list, analysis, user-group, hierarchy-manager, or directs method; validate Once/Continuous processing and automated withdrawal when applicable | Required or voluntary member criteria/group work is requested | inspect_category_membership_capability |
| Profile-option dialog | Omit applicable options already correctly populated; show only triggered options needing a user decision or change | Before proposing dependency work | resolve_category_profile_option |
| Profile-option change | Require exact option code, current/effective value, Site level or exact target scope, proposed value, trigger, prerequisite evidence, representative search test when applicable, approval, and post-change readback | An applicable option change is proposed | resolve_category_profile_option |
| Manager safety | Require a post-operation count of at least one active manager and preserve the creator's system-populated initial relationship unless another active manager remains | Manager membership changes | read_category_membership_state |
| Parent-child ordering | Validate and approve parents before eligible children; keep blocked child rows separate from otherwise valid parents and siblings | Multi-row or child-bearing request | |
| Unsupported operation | Reject direct learning, skills and qualifications, contributions, self-service conversations, Draft, deactivate, reactivate, object delete, and generic upsert | Any excluded operation is requested | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAT.VALIDATE_INPUT | decision | 1 | validate_input | valid->CAT.CHECK_DEPENDENCIES;invalid->CAT.HANDLE_ERROR | none | stop | Applicable profile-option context and one or more Category parent and child rows are normalized |
| CAT.EVALUATE_RESULT | decision | 7 | evaluate_result | verified->CAT.RETURN_SUCCESS;issues->CAT.HANDLE_ERROR | CAT.EXECUTION_GATE | stop | Profile readback plus validation or mutation evidence is reconciled with the approved stable row previews |
