# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Business outcome | Desired candidate, recruiter, requisition, application-flow, or sourcing outcome; affected Recruiting experience; intended users; timing; requested policy or list-of-values change | Return a business-language issue | Ask only for the missing business decision | Every request | |
| Requested operation | List Recruiting value sets, inspect an exact root, inspect validation metadata, list or inspect child values, or create, update, or delete a child value | Return a business-language issue | Clarify the intended outcome without asking the user to choose a technical route | Every request | |
| Exact value-set identity | One user-provided exact ValueSetCode | Block the particular-value-set request | Ask for the exact ValueSetCode; do not accept a partial code, description, display name, or inferred code | Exact root, validation metadata, child read, or child mutation | read_value_set_by_exact_code |
| Child-value identity | Proposed value for create, or one exact child selected through its returned child identifier for update or delete | Block the mutation preview | Resolve current children through Common Value Sets; never derive the child identifier from a display value | Child mutation | resolve_value_set_child |
| Target environment | Exact Fusion environment | Block the mutation preview or FSM import | Ask for the target environment | Child mutation or import | |
| Requested child delta | Only fields supported by current parent validation behavior, child metadata, and protection indicators | Block the mutation preview | Explain the supported current fields and request a minimal business change | Child create or update | resolve_value_set_child |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Current root response has a concrete ModuleId in the maintained allowlist | In scope | Continue with the requested read or supported child-value operation | match_recruiting_module_id |
| Current root response omits ModuleId | Blocked | Report that module-scoped ownership cannot be evaluated | match_recruiting_module_id |
| Current ModuleId is absent from the maintained allowlist | Blocked | Explain that the value set is outside this Recruiting task | match_recruiting_module_id |
| Parent validation behavior or child metadata does not establish managed child-row support | Blocked | Explain the current capability boundary; do not use another route | read_value_set_by_exact_code |
| Common Value Sets returns `hasMore=true` without a safe continuation procedure | Conditional fallback | Use only the documented root-collection pagination fallback and require usable response offset and limit | discover_recruiting_value_sets |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Exact code routing | Pass the exact user-provided ValueSetCode unchanged as `valueSets_Id` to Common Value Sets | Particular value set or children | read_value_set_by_exact_code |
| Root definition boundary | Reject creation, update, or deletion of a root value set and reject root identity, ownership, description, validation, data type, subtype, length, range, formatting, or security changes | Any root mutation request | |
| Response-grounded fields | Return only fields present in the current response; do not claim ModuleId filters, module display names, validation behavior, root fields, or child capabilities from inference | Every read | |
| Ownership | Require the current API ModuleId to match exactly one concrete ModuleId in the complete allowlist | Every root or child operation | match_recruiting_module_id |
| Child create | Confirm the proposed child is absent using the supported current read | Create child value | resolve_value_set_child |
| Child update or delete | Freshly read the exact child through its returned child identifier | Update or delete child value | resolve_value_set_child |
| Preservation | Preserve parent identity, child identity, validation definition, protected fields, and all unrequested fields | Child update or delete | resolve_value_set_child |
| De-duplication | De-duplicate root and child results only by identifiers actually returned by the API | List or read | |
| Explicit bulk boundary | Route explicit task CSV export to `shared.setup-export.task-level-export` and an explicit validated approved FSM CSV package to `core.data-loader`; use neither as default CRUD | Export or import | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RVS.VALIDATE | decision | 1 | validate_input | list_roots->RVS.DISCOVER_ROOTS;exact_root->RVS.READ_PARENT;validation->RVS.READ_PARENT;children->RVS.READ_PARENT;create_child->RVS.READ_PARENT;update_child->RVS.READ_PARENT;delete_child->RVS.READ_PARENT;post_change->RVS.VERIFY_CHILD;issues->RVS.INPUT_ISSUES | none | stop | Every Recruiting and Candidate Experience Value Sets request |
