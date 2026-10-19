# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| CSV or archive validation fails | Stop, correct the exact artifact, and repeat validation before approval. |
| Required country or level-mapping evidence is missing | Stop and obtain approved evidence; do not infer a mapping. |
| Detailed FSM result has an error, warning, or uncertain outcome | Treat the import as unverified and inspect the detailed process log before any corrective action. |
| Target UI or re-export differs from the expected mapping | Retain the package and log evidence; do not automatically retry. |

## Approval Rules

| Operation | Required Gate |
|---|---|
| FSM import | Explicit approval for the exact validated ZIP and exact target environment immediately before one core.data-loader import. |
| Retry | Fresh validation and fresh approval for a new or corrected ZIP; never replay an uncertain import automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GHS.READ_DONE | terminal | 16 | terminal | none | GHS.LABELS | stop | Return the configured mapping with resolved or unresolved POC labels from resolve_structure_level_labels; no package creation or Fusion mutation |
| GHS.APPROVAL_GATE | decision | 50 | execution_gate | approved->GHS.READY_IMPORT;missing->GHS.APPROVAL_ISSUES | GHS.ENFORCE | stop | A validated immutable ZIP is ready for import |
| GHS.INPUT_ISSUES | step | 60 | error_handler | disclosed->RETURN_ISSUES | none | stop | Required structure inputs are missing or invalid |
| GHS.DEPENDENCY_ISSUES | step | 70 | error_handler | disclosed->RETURN_ISSUES | none | stop | Required country, package, or approval evidence is absent |
| GHS.DESIGN_ISSUES | step | 80 | error_handler | disclosed->RETURN_ISSUES | none | stop | A structure design or package-representation rule fails |
| GHS.APPROVAL_ISSUES | step | 90 | error_handler | disclosed->RETURN_ISSUES | none | stop | Approval is absent, stale, or bound to another ZIP or environment |
| GHS.READY_IMPORT | terminal | 100 | terminal | none | GHS.APPROVAL_GATE | stop | One approved core.data-loader import may be invoked, followed by detailed-log and UI or re-export verification |
| RETURN_ISSUES | terminal | 110 | terminal | none | none | stop | A blocking issue has been disclosed |
