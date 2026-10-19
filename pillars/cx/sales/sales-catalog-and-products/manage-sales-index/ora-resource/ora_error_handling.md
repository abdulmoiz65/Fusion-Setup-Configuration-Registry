# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| The selected Item or Catalog profile is incomplete or combined | Stop before any delegation and show the invalid selection or identity. |
| The current metadata comparison source or Product Management invocation contract is undocumented | Stop at the readiness gate; do not infer an index state or invocation mechanism. |
| A delegated Product Management request fails or remains pending | Preserve the sanitized handoff record and return the delegated status. Do not retry, run Data Loader, or run ESS from this task. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required profile, invocation contract, or metadata evidence is absent. | Obtain the missing documented input or contract. |
| FAILED | A delegated request reports a terminal failure. | Use the delegated Product Management diagnostic path. |
| PROCESS_TIMEOUT | A delegated request remains non-terminal beyond its polling window. | Preserve its reference and use the delegated status-check path. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Index state has not been authoritatively compared | Do not claim that the attributes already exist or trigger a rebuild-only path. |
| Product Management delegation is unavailable | Do not substitute a direct Data Loader or ESS call. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_INDEX.DONE-REBUILD-HANDOFF | terminal | 60 | terminal | none | SALES_INDEX.APPLY-REBUILD-DEFAULT | stop | A rebuild-only request has been prepared for delegation to Manage Product Management Indexes. |
| SALES_INDEX.DONE-DELTA-HANDOFF | terminal | 70 | terminal | none | SALES_INDEX.ENFORCE-DELEGATED-INDEXING | stop | A selected profile delta request has been prepared for delegation to Manage Product Management Indexes. |
| RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | Validation, readiness, metadata comparison, or delegation handling is blocked. |
