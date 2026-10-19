# Official Communities Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Profile and external-prerequisite integrity | Read only applicable effective profile values through the Application Profile Option Foundation route, record satisfied options without prompting, and require external CAP evidence before a unified-listing Site Y proposal |
| 2 | Access and parent-definition integrity | Require the current community-management surface, applicable scope/privilege evidence, user title, target-authoritative subtype and Active status, summary rule, visibility, dates, DFFs, and disclosed defaults |
| 3 | Manager and relationship integrity | Preserve one active manager and validate only selected catalog, membership, group, assignment, moderation, and optional-child rows |
| 4 | Approval and execution safety | Freeze every proposed profile change plus parent/child fingerprints, obtain exact approval, re-read, verify profile-change readback, execute parent-first once, and verify each attempted result |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Before proposal or execution | Blocker | read_official_community_profile_options | The effective value of an applicable exposed profile option is unreadable, ambiguous, or stale | Read the exact triggered option through the Application Profile Option Foundation route and preserve its current value until exact | Yes |
| Unified Redwood listing or CAP-based administration | Blocker | | Applicable Catalog Administration Profiles are not externally created or validated, or intended administrator access is unverified | Complete the external CAP prerequisite and supply readiness/access evidence; do not implement CAP setup or invent a provider skill here | Yes, outside this skill |
| ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD applies | Blocker | read_official_community_profile_options | CAP evidence is absent, the Site level is unavailable/not updatable, or Site is not Y and its exact change is not approved | After CAP readiness, propose the exact Site old-to-Y change and verify access; when already Y, record satisfied and omit from dialog | Yes |
| Official Community management is in scope | Blocker | read_official_community_profile_options | The exposed ORA_WLF_COMMUNITIES_REDWOOD_ENABLED value or community-management surface is unverified; when the option is absent, the supported current-release control/surface is unverified | Discover runtime behavior. Never hard-code the option, propose a value when absent, or manufacture a replacement | Yes |
| Official Community catalog search is being designed or tuned | Blocker | read_official_community_profile_options | Current ORA_WLF_SS_CATALOG_SEARCH_MODE is unreadable, a change lacks broader/balanced/tighter preference, stored-value support, or exact approval, or representative searches are unverified after change | Preserve the current value unless the user approves one target-supported change; then test representative searches | Yes |
| Applicable profile option is already correct | Allowed | read_official_community_profile_options | The option is unnecessarily shown as a user decision or included as a no-op mutation | Record it as satisfied and omit it from the user dialog and write set | Yes |
| Profile change is proposed or attempted | Blocker | read_official_community_profile_options | Exact option, level, old/new values, dependent effect, approval, or configured/effective readback is missing or changed | Rebuild the proposal, obtain exact approval, submit once through the Foundation route, and verify readback before dependent work | Yes |
| Every request | Blocker | | Manager/all-items scope or the requested operation privilege is unproven | Supply approved HCM Security Profile and HCM Data Role evidence | Yes |
| Create | Blocker | | Title is missing or not user-provided; exact Official Community subtype, Active code, summary property, or required field is unresolved | Supply the title and approved runtime value contracts | Yes |
| Existing target | Blocker | resolve_official_community_identity | ID/number is unresolved or the selected result is inaccessible, ambiguous, or not an Official Community | Supply an exact technical identifier or select one subtype-filtered candidate | Yes |
| Visibility | Blocker | resolve_official_community_visibility | Value is missing without a confirmed Open default, disabled, expired, ambiguous, or unsupported | Select one current enabled value | Yes |
| Parent or association featured dates | Blocker | | End is present without start, values are ambiguous, or start is after end | Correct the dates and review their Featured effect | Yes |
| Manager or membership change | Blocker | read_official_community_state | Final active-manager count is below one or active/pending rows are incompatible | Retain or add an active manager and split incompatible operations | Yes |
| Add members | Blocker | | More than one selection method is staged in the transaction | Clear the staged selection and use one method | Yes |
| Criteria or group operation | Blocker | | Exact FDD-defined group capability, legacy destinations, evaluation rule, withdrawal behavior, or process/readback route is unavailable | Supply the registered capability or defer only the group row | Yes |
| Catalog learning | Blocker | read_official_community_state | Learning selector authority is absent, item is inactive/inaccessible/ambiguous/unsupported, or the association already exists | Resolve one selector-supported item and keep association dates separate | Yes |
| Catalog relationship removal | Warning | read_official_community_state | Impact has not been shown or the proposal implies deletion of the learning item | State that only this relationship is removed and obtain approval | Yes |
| Assignment operation | Blocker | read_official_community_state | Learning is absent from the community catalog, members are not required, required timing/rules are absent, or the authoritative assignment contract/privilege is unavailable | Correct scope and supply the registered assignment contract | Yes |
| Skills or qualifications | Blocker | | Parent is not verified or exact active-reference and child-write contracts are unavailable | Execute only as a target-confirmed post-create child operation | Yes |
| Contribution enablement | Blocker | | User did not request it or target capability is unproven | Keep disabled or supply capability evidence and disclose learner effect | Yes |
| Rating/comment moderation | Blocker | | Applicable item access, moderation privilege, exact action schema, or requested method is absent | Permit read only or supply the exact moderation contract; never infer delete support | Yes |
| Asset, forum, related material, translation, or DFF | Blocker | | Child link/method, content constraints, DFF segment, or required value is absent in current target metadata | Correct or exclude only the affected optional child | Yes |
| Draft, deactivate, reactivate, delete-object, or generic upsert | Blocker | | Operation is outside FDD v7 Official Community scope even when generic Describe metadata exposes upsert or DELETE | Do not execute; return a scoped next step for a later approved requirement | No |
| Any approved row | Blocker | read_official_community_state | Environment, parent, manager set, capability, relationship, row selection, or fingerprint changed | Rebuild the proposal and obtain fresh approval | Yes |
| Any attempted mutation | Blocker | read_official_community_state | Parent-first dependency, single-submit rule, process reconciliation, or readback cannot be satisfied | Stop and return verified, partial, failed, or indeterminate row results | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| read_official_community_profile_options | Before proposal/execution and after an approved profile change | Applicable option presence, effective/configured values, enabled/updatable level evidence, satisfied/decision status, and readback | ora_reference_lookups.md |
| resolve_official_community_identity | Existing target, duplicate review, child operation, or reconciliation | Exact identity, subtype, state, item link, and fingerprint | ora_reference_lookups.md |
| resolve_official_community_visibility | Create or visibility update | Current enabled code, meaning, and default evidence | ora_reference_lookups.md |
| read_official_community_state | Manager safety, relationship impact, stale-state check, or readback | Manager count, selected child state, last-modified evidence, impact, and fingerprint | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OCM.ENFORCE_DESIGN | decision | 5 | design_enforcement | passed->OCM.EXECUTION_GATE;blocked->OCM.HANDLE_ERROR | OCM.APPLY_DEFAULTS | stop | Validated rows have completed applicable dependencies, lookups, defaults, capability gates, and manager-safety checks |
