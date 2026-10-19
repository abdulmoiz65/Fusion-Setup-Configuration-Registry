# Input Validation

## Evidence and Scope

| Evidence | Established Task Boundary |
|---|---|
| Configure Recruiting Interaction Categories task page | Use the Common Applications Manage Lookups capability for `ORA_IRC_INTERACTION_TYPE` in the `Common` category; normal review uses `includeInactive: false`; supported editable fields are Meaning, Description, Start Date, and End Date. |
| Approved Common Lookups contract | Delegated parent/code reads and approved lookup-code create, update, and delete operations are available; this task remains responsible for its narrower Recruiting scope and approval gates. |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Business outcome | Desired Recruiting outcome, affected recruiter or candidate experience, intended users, timing, and requested business change | Return a business-language issue | Ask only for the missing business decision | Every request | |
| Requested operation | Review, create, update, delete, task-level CSV export, or validated FSM CSV import | Return a business-language issue | Clarify only when the requested outcome does not identify one supported operation | Every request | |
| Target environment | Exact Fusion environment | Block mutation preview | Ask for the environment before any create, update, delete, or import preview | Mutation or import | |
| New interaction category | Unique LookupCode and Meaning; optional Description, StartDate, and EndDate | Block creation | Obtain the missing business identity; explain LookupCode only when the user must choose between valid identities | Create | check_interaction_category_code_unique |
| Existing interaction category | Business name or exact LookupCode that resolves to one current entry | Block update or deletion | Resolve internally from current configuration; ask for a technical identifier only when multiple valid matches remain | Update or delete | resolve_interaction_category_by_exact_code |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Fixed lookup scope | Require LookupType `ORA_IRC_INTERACTION_TYPE` and LookupCategory `Common`; reject every other lookup type or category without discovery | Every request | |
| Active review | Use `includeInactive: false` and return LookupCode, Meaning, Description, EnabledFlag, StartDate, EndDate, Tag, and DisplaySequence | Review | list_active_interaction_categories |
| Creation identity | Interpret “create interaction type” as a new lookup entry, never a new lookup type; require exact LookupCode uniqueness and Meaning | Create | check_interaction_category_code_unique |
| Creation fields | Permit LookupCode, Meaning, Description, StartDate, and EndDate; create the entry as active | Create | |
| Editable fields | Permit changes only to Meaning, Description, StartDate, and EndDate | Update | resolve_interaction_category_by_exact_code |
| Protected fields | Reject changes to LookupType, LookupCategory, LookupCode, ModuleId or seed ownership, EnabledFlag, Tag, DisplaySequence, and every unrequested field | Update | resolve_interaction_category_by_exact_code |
| Exact current identity | Require a fresh read of the exact LookupType and LookupCode before update or delete | Update or delete | resolve_interaction_category_by_exact_code |
| Ambiguous match | Stop and ask one concise business-language clarification; do not guess a code or entry | Any non-unique business-name match | resolve_interaction_category_by_exact_code |
| Evidence boundary | Block behavior outside the documented task-page fields and approved Common Lookups contract unless later approved task-page or seed-data evidence expands the boundary | Every request | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RIC.VALIDATE | decision | 1 | validate_input | review->RIC.LIST_ACTIVE;create->RIC.CHECK_UNIQUE;update->RIC.RESOLVE_EXACT;delete->RIC.RESOLVE_EXACT;post_change->RIC.VERIFY_CHANGE;post_delete->RIC.VERIFY_DELETE;issues->RIC.INPUT_ISSUES | none | stop | Every Configure Recruiting Interaction Categories request |
