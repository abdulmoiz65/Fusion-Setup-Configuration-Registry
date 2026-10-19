# Reference Lookups

Delegate all lookup reads and writes to `core.fusion-api.apps-common.lookups`. This task never constructs REST URLs, calls curl, manages OAuth, uses browser automation, or duplicates Common Lookups transport. It never accesses or discovers a lookup type other than `ORA_IRC_INTERACTION_TYPE`.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| list_active_interaction_categories | Active categories are reviewed or deletion absence is checked | LookupType `ORA_IRC_INTERACTION_TYPE`; LookupCategory `Common`; includeInactive `false` | Delegated Apps Common Lookups Common view | LookupCode, Meaning, Description, EnabledFlag, StartDate, EndDate, Tag, DisplaySequence | Return only entries from the fixed type and category that the delegated active view returns | Current active interaction-category list and review fields | Return an empty active list as a valid result; block any response containing another type or category |
| check_interaction_category_code_unique | A new interaction category is requested | LookupType `ORA_IRC_INTERACTION_TYPE`; LookupCategory `Common`; exact proposed LookupCode | Delegated exact Apps Common Lookups parent/code read | LookupType, LookupCategory, LookupCode, Meaning, Description, EnabledFlag, StartDate, EndDate, Tag, DisplaySequence, ModuleId or seed ownership when returned | A create is eligible only when the exact LookupCode does not already exist in the fixed lookup type, including an entry not shown in normal active review | Exact uniqueness result and any collision state | No match means unique; one match blocks creation; multiple matches or uncertain absence block creation |
| resolve_interaction_category_by_exact_code | An update or deletion is requested | LookupType `ORA_IRC_INTERACTION_TYPE`; LookupCategory `Common`; exact code selected from the business request and current configuration | Delegated fresh exact Apps Common Lookups parent/code read | LookupType, LookupCategory, LookupCode, Meaning, Description, EnabledFlag, StartDate, EndDate, Tag, DisplaySequence, ModuleId or seed ownership when returned | Require exactly one current entry whose LookupType and LookupCode match exactly | Immutable current state, supported delta basis, and exact deletion identity | Block no match, multiple matches, stale evidence, another lookup type, or ambiguous business-name resolution |
| verify_interaction_category_change | One approved delegated create or update has returned | LookupType `ORA_IRC_INTERACTION_TYPE`; LookupCategory `Common`; exact approved LookupCode; approval fingerprint | Delegated fresh exact Apps Common Lookups parent/code read | LookupType, LookupCategory, LookupCode, Meaning, Description, EnabledFlag, StartDate, EndDate, Tag, DisplaySequence, ModuleId or seed ownership when returned | Require exactly one result matching the approved post-change values while every protected and unrequested field remains unchanged | Verified comparison result and sanitized run evidence | Treat no match, mismatch, ambiguity, or uncertain response as a post-change verification failure; do not retry the mutation |
| verify_interaction_category_deleted | One approved delegated deletion has returned | LookupType `ORA_IRC_INTERACTION_TYPE`; LookupCategory `Common`; includeInactive `false`; exact deleted LookupCode and Meaning | Delegated Apps Common Lookups active review | LookupCode, Meaning, Description, EnabledFlag, StartDate, EndDate, Tag, DisplaySequence | The exact deleted entry must no longer be returned by the active review | Verified absence and sanitized run evidence | If the entry remains or the response is uncertain, report a deletion-verification failure; do not retry the deletion |

## Delegated Mutation Contract

| Operation | Delegated Capability | Task-Owned Restriction |
|---|---|---|
| Create | Common Lookups lookup-code create | Create one active entry only in `ORA_IRC_INTERACTION_TYPE` after uniqueness validation and exact approval; do not create a lookup type. |
| Update | Common Lookups lookup-code update | Send only approved changes to Meaning, Description, StartDate, and EndDate after a fresh exact read. |
| Delete | Common Lookups lookup-code delete | Delete one exact existing entry only after immutable-preview approval and a second fresh confirmation naming LookupCode and Meaning. |
| Export | `shared.setup-export.task-level-export` | Use only when task-level CSV export is explicitly requested. |
| Import | `core.data-loader` FSM CSV Import | Use only for an explicitly requested, validated, and approved FSM CSV package; never as the default CRUD route. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RIC.LIST_ACTIVE | decision | 2 | reference_lookup | reviewed->RIC.DONE_REVIEW;issues->RIC.LOOKUP_ISSUES | RIC.VALIDATE | stop | Active interaction-category review is requested |
| RIC.CHECK_UNIQUE | decision | 3 | reference_lookup | unique->RIC.ENFORCE;exists->RIC.LOOKUP_ISSUES;issues->RIC.LOOKUP_ISSUES | RIC.VALIDATE | stop | Creation is requested |
| RIC.RESOLVE_EXACT | decision | 4 | reference_lookup | update->RIC.ENFORCE;delete->RIC.ENFORCE;issues->RIC.LOOKUP_ISSUES | RIC.VALIDATE | stop | Update or deletion is requested |
| RIC.VERIFY_CHANGE | decision | 9 | reference_lookup | verified->RIC.DONE_CHANGE;mismatch->RIC.POST_CHANGE_ISSUES | RIC.VALIDATE | stop | A delegated create or update requires post-change verification |
| RIC.VERIFY_DELETE | decision | 10 | reference_lookup | absent->RIC.DONE_DELETE;present->RIC.POST_CHANGE_ISSUES;uncertain->RIC.POST_CHANGE_ISSUES | RIC.VALIDATE | stop | A delegated deletion requires active-review absence verification |
