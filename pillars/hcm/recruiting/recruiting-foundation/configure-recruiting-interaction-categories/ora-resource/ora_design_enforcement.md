# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Establish business intent | Capture the desired Recruiting outcome, affected recruiter or candidate experience, intended users, timing, and requested change. |
| 2 | Resolve fixed identity | Restrict work to `ORA_IRC_INTERACTION_TYPE` in the `Common` category and resolve one exact code when the operation targets an existing entry. |
| 3 | Validate supported change | Prove create uniqueness or limit an update to Meaning, Description, StartDate, and EndDate while preserving all protected and unrequested values. |
| 4 | Build complete comparison | Show the required full-field create or edit comparison without expanding the mutation payload. |
| 5 | Bind immutable preview | Record environment, current state, requested delta, impact, verification read, and approval fingerprint. |
| 6 | Gate delegated mutation | Obtain one exact create/update approval or both required deletion confirmations immediately before the delegated Common Lookups action. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Blocker | | LookupType or LookupCategory differs from the fixed task-owned scope, or another lookup type would be accessed or discovered | Keep the request entirely within `ORA_IRC_INTERACTION_TYPE` and `Common` | No |
| Create | Blocker | check_interaction_category_code_unique | LookupCode or Meaning is missing, the exact code exists, or uniqueness is uncertain | Supply the missing business identity or choose a unique code | Yes |
| Update or delete | Blocker | resolve_interaction_category_by_exact_code | A fresh exact read does not resolve one current LookupType and LookupCode | Refresh exact current state and clarify only a genuine ambiguity | Yes |
| Update | Blocker | resolve_interaction_category_by_exact_code | The delta changes anything except Meaning, Description, StartDate, or EndDate | Limit the request to task-page-supported editable fields | Yes |
| Update | Blocker | resolve_interaction_category_by_exact_code | LookupType, LookupCategory, LookupCode, ModuleId or seed ownership, EnabledFlag, Tag, DisplaySequence, or any unrequested field is not preserved | Restore every protected and unrequested current value | Yes |
| Create or update comparison | Blocker | | Any required field or exact column is omitted, statuses are wrong, or unchanged display fields are added to the mutation payload | Rebuild the complete display and retain a minimal approved payload | Yes |
| Mutation preview | Blocker | | Target environment, current state, requested delta, impact, verification read, or approval fingerprint is absent or mutable | Regenerate the immutable minimal-change preview | Yes |
| Delete | Blocker | resolve_interaction_category_by_exact_code | The exact current entry, deletion impact table, immutable-preview approval, or second fresh confirmation naming LookupCode and Meaning is absent | Complete both deletion gates against fresh exact evidence | Yes |
| Any mutation | Blocker | | Activation, deactivation, code, tag, display sequence, seed ownership, or another undocumented change is requested | Explain the supported business boundary and stop until approved evidence expands it | No |
| Explicit CSV export or import | Blocker | | Export is not routed to task-level export, or import is not an explicitly requested validated and approved FSM CSV package routed through Core Data Loader | Use the catalog-supported route only for the explicit bulk request | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| check_interaction_category_code_unique | Create | Exact code-uniqueness result inside the fixed lookup type | ora_reference_lookups.md |
| resolve_interaction_category_by_exact_code | Update or delete | Exact current identity, editable values, protected values, and seed ownership when returned | ora_reference_lookups.md |

## Create and Edit Comparison Contract

Every create and edit preview and result uses exactly these columns:

| Field | Current Value | Proposed Value | Change Status |
|---|---|---|---|
| LookupType | Required | Required | Required |
| LookupCategory | Required | Required | Required |
| LookupCode | Required | Required | Required |
| Meaning | Required | Required | Required |
| Description | Required | Required | Required |
| EnabledFlag | Required | Required | Required |
| StartDate | Required | Required | Required |
| EndDate | Required | Required | Required |
| Tag | Required | Required | Required |
| DisplaySequence | Required | Required | Required |
| ModuleId / Seed Ownership | Required | Required | Required |

For edits, populate every Current Value from the fresh exact read. Put requested post-change values in Proposed Value, preserve current values for every unchanged field, mark changed rows `🟡 Updated`, mark LookupType and LookupCategory `Fixed`, and mark other unchanged Fusion-returned values `Preserved`. Present changed rows first in their standard relative order, then fixed and preserved rows in the standard relative order shown above.

For creates, use `Not present` as Current Value for every nonexistent field. Show each supplied or fixed intended value in Proposed Value. Mark LookupType and LookupCategory `Fixed`, user-supplied values `Provided`, the active creation state `Fixed`, and absent optional values `Not sent`. Never use `Create` or `🟢 Create` as a status.

The comparison is an audit display, not a payload template. The delegated mutation receives only the approved fields required for create or update and never receives unchanged fields merely because they appear in this table.

## Deletion Display Contract

| LookupCode | Meaning | Description | Current State | Impact | Deletion Status |
|---|---|---|---|---|---|
| Exact fresh value | Exact fresh value | Exact fresh value | Existing entry and availability | Recruiter or candidate experience affected by removal | Awaiting preview approval or awaiting final confirmation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RIC.ENFORCE | decision | 5 | design_enforcement | create->RIC.PREVIEW_CHANGE;update->RIC.PREVIEW_CHANGE;delete->RIC.PREVIEW_DELETE;blocked->RIC.DESIGN_ISSUES | none | stop | A create, update, or delete has current identity evidence |
