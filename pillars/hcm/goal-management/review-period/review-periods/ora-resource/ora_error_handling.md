# Review Period Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Ambiguous identity | Stop and request disambiguation |
| Describe or management resource unavailable | Stop REST preview and offer guided FSM/UI planning |
| Only captured create/fetch/update calls exist for delete | Treat DELETE as unsupported evidence and offer inactivation/guided UI |
| Timeout or ambiguous write response | Return UNKNOWN_AFTER_SUBMISSION and reconcile by safe read |
| CSV process failure | Preserve sanitized status/log evidence and do not retry uncertain import |
| Status LOV unavailable, empty, or missing required fallback `A` | Return a sanitized lookup diagnostic; block a status-bearing mutation and do not assume `A` or `I` from a captured response |
| Worker or assignment context unavailable | Return partial entry context with the status LOV result and a sanitized diagnostic; do not block Review Period management reads or mutations |
| One approval covers multiple updates but no batch contract is advertised | Retain the approval group and execute only the metadata-supported ordered requests; do not invent a batch route. If no update method is advertised, return a contract blocker. |
| Parent execution control is missing or does not identify this as the earliest incomplete task | Return `RUNBOOK_SEQUENCE_BLOCKED` without preparing or submitting the mutation. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Missing or contradictory request | Correct intake |
| Transport/environment | Entry-context resource root, caller context, or lookup service is unavailable | Return partial read result when status LOV is available; otherwise report the unavailable source |
| Catalog mismatch | Task identity does not match effective catalog | Stop and escalate to catalog owner |
| Fusion API | Supported request is rejected | Capture sanitized diagnostics and revalidate contract |
| Unknown after submission | Outcome cannot be proven | Read and reconcile; never replay automatically |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview | Environment, operation, target, dates, usage, payload mapping report, and fingerprint |
| Failure | Stage, failure class, message, safe external ID, and recommended action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing approval | No mutation or import |
| Unproven zero usage | No delete |
| Ambiguous submission | No automatic retry |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| REVIEW_PERIODS.CSV_READY | terminal | 220 | terminal | none | REVIEW_PERIODS.VALIDATE | stop | CSV export or validated import handoff is ready |
| REVIEW_PERIODS.NO_CHANGE | terminal | 230 | terminal | none | REVIEW_PERIODS.WRITE_ROUTE | stop | Fresh values already match |
| REVIEW_PERIODS.DONE_ENTRY_CONTEXT | terminal | 239 | terminal | none | REVIEW_PERIODS.ENTRY_CONTEXT | stop | Status LOV and any available caller context were read |
| REVIEW_PERIODS.DONE_READ | terminal | 240 | terminal | none | REVIEW_PERIODS.READ | stop | Read completed |
| REVIEW_PERIODS.DONE_SEARCH | terminal | 241 | terminal | none | REVIEW_PERIODS.SEARCH | stop | Bounded search completed, including an empty result |
| REVIEW_PERIODS.DONE_CREATED | terminal | 250 | terminal | none | REVIEW_PERIODS.CREATE | stop | Create verified |
| REVIEW_PERIODS.DONE_UPDATED | terminal | 260 | terminal | none | REVIEW_PERIODS.UPDATE | stop | Update verified |
| REVIEW_PERIODS.DONE_INACTIVATED | terminal | 270 | terminal | none | REVIEW_PERIODS.INACTIVATE | stop | Inactivation verified |
| REVIEW_PERIODS.DONE_DELETED | terminal | 280 | terminal | none | REVIEW_PERIODS.DELETE | stop | Delete verified |
| REVIEW_PERIODS.UNKNOWN | terminal | 290 | terminal | none | none | stop | A submitted mutation has an ambiguous outcome |
| REVIEW_PERIODS.BLOCKED | terminal | 300 | terminal | none | none | stop | A prerequisite, approval, or contract blocks the request |
