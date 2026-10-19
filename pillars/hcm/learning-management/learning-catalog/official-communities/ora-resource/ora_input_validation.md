# Official Communities Input Validation

Sources: OLC-116681 FDD v7 section 5.0 and OLC-120245, from the page updated
2026-09-22 15:54:32, the approved Learning baseline and taxonomy, and the
user-supplied `learningCommunities` Describe.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Request identity | target environment; requested operation; stable parent row ID; stable child row IDs | Stop the affected row before preview | Supply one exact environment, supported operation, and row identity | All requests | |
| Official Community definition | user-provided title; summary or approved generation when tenant-required; Official Community subtype; Active create intent; visibility; optional featured dates and contribution intent | Return the exact missing fields; never derive the title | Supply the title and resolve every runtime-required value before execution | Create or parent update | |
| Existing Official Community identity | learningItemId, learningItemNumber, or subtype-filtered title plus explicit selection when ambiguous | Stop before a non-create proposal | Resolve one exact accessible Official Community and follow its returned item link | Retrieve, update, child mutation, duplicate review, or reconciliation | resolve_official_community_identity |
| Catalog relationship row | parent row ID; learning identifier; requested add, date change, or removal; optional association featured dates | Block only the affected relationship row | Supply one relationship intent and a uniquely resolvable supported learning item | Catalog learning is managed | |
| Membership selection | exactly one selection method; required or voluntary membership type; compatible active or pending state; stable member/group row IDs | Block the affected transaction | Choose one FDD-supported method and clear staged selections before switching | Membership, pending request, type change, removal, or group operation | |
| Assignment plan | learning already associated to the community; required-member target; supported start, due date, note, evaluation rule; cancellation reason and outcome when applicable | Block the assignment row | Complete the operation-specific assignment inputs | Assign, edit, or cancel community learning | |
| Optional child plan | exact asset, conversation, related-material, translation, DFF, skill, qualification, or rating intent tied to one parent | Exclude or block only the affected optional child | Correct the row or explicitly exclude it from the next proposal | An optional child operation is requested | |
| Related profile-option intent | applicable FDD trigger; current effective value; CAP readiness evidence when unified listing applies; optional search preference; exact proposed option name, level, old value, and new value | Stop only the dependent operation or preserve the current value | Read through the Application Profile Option Foundation route and supply the missing decision or external CAP evidence | Before proposal or execution; a profile change is proposed only when applicable and needed | read_official_community_profile_options |
| Approval evidence | immutable proposal version; exact environment; selected parent and child rows; every proposed profile change; current-state fingerprint; fresh exact approval | Stop before every mutation | Refresh evidence and approve the exact current proposal, including profile option name, level, old value, and new value | Any live mutation | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An applicable profile-option effective value cannot be read through the Application Profile Option Foundation route | Blocked | Read only the triggered option and preserve the current value until its contract is exact | read_official_community_profile_options |
| Unified Redwood catalog listing or CAP-based administration applies but applicable Catalog Administration Profile readiness is unproven | Blocked | Complete or validate the external CAP prerequisite; do not implement CAP setup in this skill | |
| ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD is applicable and not already Site Y | Change decision required | After CAP readiness, propose Site Y and intended-administrator access verification; omit the option from the dialog when already satisfied | read_official_community_profile_options |
| ORA_WLF_COMMUNITIES_REDWOOD_ENABLED is exposed by the current tenant and release | Runtime verification required | Verify the effective value and community-management surface; do not hard-code a value | read_official_community_profile_options |
| ORA_WLF_COMMUNITIES_REDWOOD_ENABLED is absent | Runtime control discovery required | Do not propose a value or manufacture a replacement; require evidence for the current supported control and management surface | read_official_community_profile_options |
| Catalog search behavior is being designed or tuned | Decision required only when a change is needed | Ask for broader recall, balanced matching, or tighter precision; preserve the current ORA_WLF_SS_CATALOG_SEARCH_MODE value without exact approval | read_official_community_profile_options |
| An applicable option is already correctly populated | Satisfied | Record the dependency and omit it from the user dialog | read_official_community_profile_options |
| ID or number does not resolve exactly, or subtype-filtered title yields zero or multiple accessible results | Invalid | Supply an exact ID/number or select one returned Official Community | resolve_official_community_identity |
| Visibility is omitted or supplied as a translated meaning | Lookup required | Resolve one enabled runtime value and disclose any Open default | resolve_official_community_visibility |
| Exact Official Community subtype, Active status code, summary rule, or another service-required value lacks an authoritative target contract | Blocked | Supply or enable an approved runtime resolver contract; do not infer a code or property | |
| A person, learning, filtered-list, criteria, user-group, hierarchy, skill, qualification, or moderation reference lacks a documented resolver | Blocked for that child row | Preserve unrelated valid rows and report the exact missing authority | |
| Current manager count or selected child state cannot be read completely | Stale or incomplete | Refresh the parent and applicable returned child links before preview | read_official_community_state |
| A requested child write is absent from the registered target capability | Blocked for that child row | Name the missing operation contract; do not substitute another child resource | |
| Parent, manager set, capability, or selected child relationship changed after approval | Stale | Skip the affected action, rebuild the proposal, and obtain new approval | read_official_community_state |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Title is user-provided, nonblank, and within the runtime limit | Reject blank, generated, or over-limit title input | Create | |
| Parent type and subtype identify an Official Community | Require the Describe-confirmed ORA_COMMUNITY type and a target-authoritative Official Community subtype; reject Topic, Category, or self-service results | Create, retrieve, update, or child mutation | resolve_official_community_identity |
| Summary follows the tenant rule | Require user text or approved generated text when the tenant marks summary required; validate target length, rich-text, and unsafe-markup rules | Create or summary update | |
| Featured dates are coherent | Reject ambiguous dates, start after end, or end without start; show current or future Featured effect | Parent or association featured dates are supplied | |
| Lookup-backed values are target-supported | Require current codes for status, visibility, contribution, conversation, membership, processing, assignment, and other lookup-backed fields | A lookup-backed value is used | resolve_official_community_visibility |
| Person and membership rows are structurally valid | Accept full name, person number, or work email; CSV rows use one supported identifier and isolate blank, malformed, duplicate, unresolved, or inaccessible rows | Membership or manager rows are supplied | |
| One add-members method is selected | Reject mixed selection methods within one staged transaction | Add members | |
| Final active-manager count remains at least one | Reject individual or bulk actions that would leave zero active managers | Manager or membership change | read_official_community_state |
| Learning relationship is valid | Reject inactive, inaccessible, ambiguous, unsupported, or already-associated learning and preserve its actual subtype and state | Catalog relationship add or update | |
| Assignment input is scoped | Reject learning outside the community catalog, non-required-member targets, missing timing/rules, or incomplete cancellation reason/outcome | Assignment operation | read_official_community_state |
| Post-create-only children wait for parent readback | Skills and qualifications and any other child requiring identity cannot run before verified parent creation | Create with child operations | |
| Operation is in story scope | Permit parent read, create Active, update, and only target-confirmed children; reject generic upsert, Draft, deactivate, reactivate, and delete-object | Any requested operation | |
| Profile-option trigger and value are exact | Evaluate only triggered options; reject a proposed change without current effective/configured values, target-supported level/value, or required CAP evidence | Before proposal or profile mutation | read_official_community_profile_options |
| Profile-option dialog is minimal | Record already-correct triggered options as satisfied and do not ask the user to reconfirm them | Before proposal | read_official_community_profile_options |
| Profile-option change is approval-bound and verified | Require its exact option, level, old value, new value, and dependent effect in approval; read back configured and effective values before community work | Profile mutation | read_official_community_profile_options |
| Approved selection is unchanged | Invalidate approval when a row is corrected, excluded, added, removed, reordered, or has changed evidence | After preview | read_official_community_state |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OCM.VALIDATE_INPUT | decision | 1 | validate_input | valid->OCM.CHECK_DEPENDENCIES;invalid->OCM.HANDLE_ERROR | none | stop | One or more Official Community parent or child rows are normalized |
| OCM.EVALUATE_RESULT | decision | 7 | evaluate_result | verified->OCM.RETURN_SUCCESS;issues->OCM.HANDLE_ERROR | OCM.EXECUTION_GATE | stop | Validation or mutation evidence is reconciled with the approved profile-change, parent, and child previews |
