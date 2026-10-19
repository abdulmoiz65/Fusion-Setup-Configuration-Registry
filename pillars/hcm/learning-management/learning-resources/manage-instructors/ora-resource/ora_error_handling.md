# Manage Instructors Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Person is missing, invalid, inaccessible, or ambiguous | Block the row and request a supported precise identifier or selection |
| Existing instructor is found | Show its identifier/status and exclude the row from creation |
| Supplier or other excluded child data is supplied | Stop; request explicit removal or deferral |
| Assignment is not ACTIVE | Block pending verified contract; no warning-acceptance override |
| Exact immutable-load approval is absent or stale | Stop before upload; obtain the shared Task Hook approval for the current proposal and final artifact only |
| Create fails or outcome is uncertain | Stop without automatic retry; read back and reconcile before another attempt |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Person identifier is absent or unreadable | Correct the affected row |
| duplicate | The person already has an instructor resource | Use the existing instructor or change the person |
| selection_required | Person or supplier is ambiguous | Select one documented option |
| approval_blocker | Shared final-artifact approval is absent/stale | Review and approve the current immutable load |
| execution_failure | Create or child-data operation fails | Read back, report sanitized details, and request one safe next action |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Proposal | Verified person, number, department/location when available, assignment status, supplier, Set/flexfields, warnings, validation, and action |
| Post-create | Created, existing, blocked, and failed rows plus instructor identifier, status, availability, and child-data results |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Person was not supplied | Do not derive or recommend one |
| Existing instructor is found | Do not create a duplicate |
| Proposal changed after approval | Do not reuse the earlier approval |
| Mutation outcome is uncertain | Do not automatically retry |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IN.APPROVAL_GATE | decision | 5 | execution_gate | approved->IN.READY;missing->IN.BLOCKED;changed->IN.BLOCKED;failure->IN.FAILED | IN.ENFORCE_DESIGN | stop | Confirm exact proposal and final artifact binding before shared preview; this node does not record or replace the later shared upload approval |
| IN.READY | terminal | 6 | terminal | none | IN.APPROVAL_GATE | continue | Every selected row and final artifact pass; eligible for shared preview, not upload authorization |
| IN.BLOCKED | terminal | 7 | terminal | none | none | continue | Input, dependency, lookup, design, or approval blocks creation |
| IN.FAILED | terminal | 8 | terminal | none | none | continue | Validation or readiness evaluation fails unexpectedly |
