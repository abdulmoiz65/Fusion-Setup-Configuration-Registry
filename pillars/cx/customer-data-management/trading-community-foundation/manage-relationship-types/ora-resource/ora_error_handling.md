# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Documented input is incomplete | Stop and identify the missing relationship type, role and phrase pair value, or relationship group. |
| Search lookup contract is incomplete | Stop before attempting a live lookup or change. The authorized guide provides a UI workflow but does not provide an API path, response mapping, or no-match and many-match handling. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Missing input | A required documented input is absent | Provide the missing value and rerun validation. |
| Lookup contract gap | A live lookup or automated execution is requested | Provide Oracle documentation or implementation details for the lookup contract. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Lookup contract gap | Do not infer a Fusion REST endpoint, no-match behavior, result mapping, or automated change operation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRT.HANDLE-MISSING-INPUT | step | 30 | error_handler | handled->MRT.RETURN_ISSUES | MRT.VALIDATE-DOCUMENTED-INPUT | stop | Documented input is incomplete |
| MRT.HANDLE-LOOKUP-CONTRACT-GAP | step | 40 | error_handler | handled->MRT.RETURN_ISSUES | MRT.FIND-RELATIONSHIP-TYPE | stop | The lookup contract is not documented |
| MRT.DONE-DOCUMENTED-FLOW | terminal | 50 | terminal | none | MRT.FIND-RELATIONSHIP-TYPE | stop | The documented UI workflow has selected the relationship type for editing |
| MRT.RETURN_ISSUES | terminal | 60 | terminal | none | none | stop | A documented input or lookup-contract issue is handled |
