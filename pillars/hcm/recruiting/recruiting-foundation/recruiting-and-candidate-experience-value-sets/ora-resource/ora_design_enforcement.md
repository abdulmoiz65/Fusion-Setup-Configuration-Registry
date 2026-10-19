# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Establish the business outcome | Identify the affected Recruiting experience, intended users, timing, and requested policy or list-of-values change. |
| 2 | Resolve the exact parent | Use the exact user-provided ValueSetCode as the Common Value Sets `valueSets_Id` and read the current root. |
| 3 | Prove Recruiting ownership | Match the root response's current ModuleId to exactly one entry in the complete maintained allowlist. |
| 4 | Confirm child capability | Require current validation behavior, protection indicators, and child metadata to establish managed child rows and supported fields. |
| 5 | Resolve current child state | Prove create absence or freshly read the exact update/delete child through its returned identifier. |
| 6 | Enforce minimal change | Preserve parent identity, child identity, validation definition, protection state, and all unrequested values. |
| 7 | Bind approval | Present one immutable business-first preview and obtain exact approval immediately before one delegated child mutation. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Particular root or child request | Blocker | read_value_set_by_exact_code | ValueSetCode is partial, inferred, derived from a description, or not supplied by the user | Obtain one exact ValueSetCode and pass it unchanged to Common Value Sets | Yes |
| Every root or child operation | Blocker | match_recruiting_module_id | Current root ModuleId is absent, ambiguous, or not in the complete allowlist | Report the ownership result; refresh the complete baseline only from the approved Confluence section when stale | No |
| Root mutation | Blocker | | The request creates, updates, or deletes a root value set or changes its identity, ownership, description, validation definition, data type, subtype, length, range, formatting, or security settings | Explain that only supported child value rows can be managed | No |
| Child mutation | Blocker | read_value_set_by_exact_code | Current parent validation behavior does not explicitly establish managed child-row support | Stop without inferring capability from the presence of a child resource | No |
| Child mutation | Blocker | resolve_value_set_child | Current metadata does not establish the requested field as supported, or a returned protection indicator blocks it | Limit the delta to fields explicitly supported by current metadata | Yes |
| Create child value | Blocker | resolve_value_set_child | The proposed child is already present or absence is not proven by a complete supported read | Resolve the collision or complete the current read | Yes |
| Update or delete child value | Blocker | resolve_value_set_child | The exact child was not freshly read using its returned child identifier | Resolve and freshly read one exact current child | Yes |
| Update or delete child value | Blocker | resolve_value_set_child | Parent identity, child identity, validation definition, ownership, protected fields, or unrequested values would change | Restore every protected and unrequested value and retain only the supported delta | Yes |
| Comparable Recruiting configuration | Blocker | match_recruiting_module_id | A comparable value set is used as authority instead of a current exact parent/child read | Use the comparison only to inform the business proposal; validate the target independently | Yes |
| Root discovery | Blocker | discover_recruiting_value_sets | Not every page was processed before ownership filtering, or continuation parameters were guessed | Complete provider pagination or use only the restricted offset/limit fallback | Yes |
| Mutation preview | Blocker | | Target environment, exact parent and child identity, current child state, requested delta, business impact, verification read, unchanged configuration, or approval fingerprint is absent | Rebuild the immutable minimal-change preview | Yes |
| Explicit CSV export or import | Blocker | | Export is not routed to task-level export, or import is not an explicitly requested validated and approved FSM CSV package | Use the catalog route only for the explicit bulk request | Yes |
| Unsupported route | Blocker | | Direct REST, UI automation, FSM, export, import, or another route would bypass an unsupported request | Explain the limitation and stop | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| read_value_set_by_exact_code | Every exact root or child operation | Exact current parent identity, validation behavior, protection state, and ModuleId | ora_reference_lookups.md |
| match_recruiting_module_id | Every root or child operation | In-scope decision, concrete ModuleId, module key, display name, and baseline version | ora_reference_lookups.md |
| resolve_value_set_child | Child listing or mutation | Returned child identity, complete current state, supported fields, protection state, and absence or exact-match result | ora_reference_lookups.md |
| discover_recruiting_value_sets | Complete root listing | Every root page and continuation evidence | ora_reference_lookups.md |

## Immutable Preview Contract

| Preview Element | Required Content |
|---|---|
| Business outcome | Desired Recruiting experience, intended users, timing, and expected result. |
| Target | Exact environment, ValueSetCode, returned parent identifier, current ModuleId, baseline-derived module name, and returned child identifier when applicable. |
| Current state | Fresh parent and child response fields actually returned, with sensitive values redacted when necessary. |
| Requested delta | Only the exact supported child fields to create, update, or delete. |
| Impact and unchanged configuration | Business impact plus explicit preservation of parent definition, identity, ownership, protected fields, and unrequested child values. |
| Verification | Exact fresh child read after create/update or verified absence after delete. |
| Approval fingerprint | Immutable environment, identities, minimal payload or delete target, current-state receipt, and verification plan. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RVS.ENFORCE | decision | 7 | design_enforcement | create->RVS.PREVIEW;update->RVS.PREVIEW;delete->RVS.PREVIEW;blocked->RVS.DESIGN_ISSUES | RVS.RESOLVE_CHILD | stop | A supported child-value mutation has exact current parent and child evidence |
