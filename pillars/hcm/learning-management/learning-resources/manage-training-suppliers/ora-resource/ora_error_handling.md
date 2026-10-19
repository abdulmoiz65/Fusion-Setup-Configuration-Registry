# Manage Training Suppliers Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required name is missing | Block only the affected row and ask for the supplier name |
| Optional contact is invalid or ambiguous | Offer correction, selection, removal, or row exclusion; never substitute a person |
| Same-name supplier exists | Show identifiers and statuses and request explicit intent |
| Current proposal lacks exact-version approval | Stop before create and request `Approve proposal vN` |
| Create fails or has uncertain outcome | Stop without automatic retry; read back and reconcile before another attempt |
| Creation route is not selected | Stop before proposal and ask the user to choose REST upload or Data Loader |
| Browser UI is proposed for create, duplicate check, or verification | Stop; creation must use the user-selected REST upload or Data Loader route, and checks must use the documented REST GET contract |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required supplier name is missing or unreadable | Correct the affected row |
| selection_required | Contact or existing-record intent is ambiguous | Select or remove the optional value, or state create intent |
| approval_blocker | Approval is absent, stale, or for another proposal | Review and approve the exact current version |
| execution_failure | Create or child-data operation fails | Read back, report sanitized details, and request one safe next action |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Proposal | Selected execution route, exact name, description provenance, resolved contact, Set/flexfields, related-material decision, warnings, validation, and action |
| Post-create | Created, existing, blocked, and failed rows plus supplier identifier and status when available |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Name is not user-provided | Do not derive or propose a placeholder supplier name |
| Proposal changed after approval | Do not reuse the earlier approval |
| Selected creation route changed after approval | Do not reuse the earlier approval; issue a new proposal version |
| Mutation outcome is uncertain | Do not automatically retry |
| Selected REST or Data Loader route is unavailable | Do not substitute another route or fall back to browser UI; request a new route choice and proposal |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TS.APPROVAL_GATE | decision | 5 | execution_gate | approved->TS.READY;missing->TS.BLOCKED;changed->TS.BLOCKED;failure->TS.FAILED | TS.ENFORCE_DESIGN | stop | Immediately before executing the approved REST upload or Data Loader route |
| TS.READY | terminal | 6 | terminal | none | TS.APPROVAL_GATE | continue | Exact current proposal is approved and every selected row passes validation |
| TS.BLOCKED | terminal | 7 | terminal | none | none | continue | Input, dependency, lookup, design, or approval blocks creation |
| TS.FAILED | terminal | 8 | terminal | none | none | continue | Validation or readiness evaluation fails unexpectedly |
