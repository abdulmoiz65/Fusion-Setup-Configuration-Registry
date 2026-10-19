# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| CSV field count or archive validation fails | Stop, correct the exact artifact, and repeat validation before approval. |
| Identifier file is header-only or incomplete | Stop and add one matching identifier row per imported node. |
| Geography identity or parentage is uncertain | Stop and obtain authoritative evidence; do not guess or resubmit variants. |
| Detailed FSM result has an error, warning, or uncertain outcome | Treat the import as unverified and inspect the detailed process log before any corrective action. |
| Target UI or re-export does not match the approved hierarchy | Retain package and log evidence; do not automatically retry. |

## Approval Rules

| Operation | Required Gate |
|---|---|
| FSM import | Explicit approval for the exact validated ZIP and exact target environment immediately before one core.data-loader import. |
| Retry | Fresh validation and fresh approval for a new or corrected ZIP; never replay an uncertain import automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GHH.APPROVAL_GATE | decision | 50 | execution_gate | approved->GHH.READY_IMPORT;missing->GHH.APPROVAL_ISSUES | GHH.ENFORCE | stop | A validated immutable ZIP is ready for import |
| GHH.INPUT_ISSUES | step | 60 | error_handler | disclosed->RETURN_ISSUES | none | stop | Required hierarchy inputs are missing or invalid |
| GHH.DEPENDENCY_ISSUES | step | 70 | error_handler | disclosed->RETURN_ISSUES | none | stop | Required geography, structure, package, or approval evidence is absent |
| GHH.DESIGN_ISSUES | step | 80 | error_handler | disclosed->RETURN_ISSUES | none | stop | A hierarchy design or package-representation rule fails |
| GHH.APPROVAL_ISSUES | step | 90 | error_handler | disclosed->RETURN_ISSUES | none | stop | Approval is absent, stale, or bound to another ZIP or environment |
| GHH.READY_IMPORT | terminal | 100 | terminal | none | GHH.APPROVAL_GATE | stop | One approved core.data-loader import may be invoked, followed by detailed-log and UI or re-export verification |
| RETURN_ISSUES | terminal | 110 | terminal | none | none | stop | A blocking issue has been disclosed |
