# Error Handling

## Error Handling Rules

| Situation | What Happens | Next Action |
|---|---|---|
| The requested assignment does not target Sales | Reject the request without lookup, preview, import, or delegation. | Use this Sales-only task only with Sales or functional-area ID 38. |
| A Sales catalog inquiry has no fresh successful EGP_MANAGE_DEFAULT_CATALOGS export from the target environment | Stop without returning cached or inferred catalog details. | Run a fresh delegated SCM task export, persist its receipt, and validate the same-task package. |
| The fresh export has zero or multiple Sales assignment rows or matching catalog rows | Stop and disclose the ambiguous or absent match without selecting a catalog. | Correct the export scope or tenant setup, then rerun the inquiry lookup. |
| A supplied assignment value or independently included catalog/category row conflicts with the Sales rule profile | Stop this custom task without preview or import. | Correct the value to the supplied Sales profile. Do not add catalog or category CSV rows solely to carry a functional-area assignment policy. |
| The catalog-assignment import is not accepted or does not return an import reference | Stop before creating the index invocation prompt. | Obtain an accepted import result with a non-secret request reference. |
| The assignment-only package baseline, workspace or output path is unsafe, malformed or conflicts with an existing artifact | Stop before SCM handoff and preserve the baseline and existing output. | Correct the project-contained inputs; require explicit replacement confirmation only for a deliberate output replacement. |
| Post-import association verification later fails, is nonterminal, cross-environment, or is not exactly Sales ID 38 | Report the verification result, but do not retract the already-issued prompt. | Correct or investigate the association separately; do not imply that an index job ran. |
| The Manage Sales Index prompt cannot be persisted after import acceptance, has an unsafe path, or would replace another prompt without confirmation | Classify as artifact_persistence failure and stop. | Preserve the accepted import evidence and sanitized persistence error. Do not retry the import, start Product Management directly, or imply that either index job ran. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_CATALOG_ASSIGNMENT.DONE-INQUIRY | terminal | 6 | terminal | none | SALES_CATALOG_ASSIGNMENT.RESOLVE-CURRENT-SALES-CATALOG | stop | A fresh validated SCM export resolves exactly one Sales assignment and matching Catalog Code and Catalog Name. |
| SALES_CATALOG_ASSIGNMENT.DONE-ASSIGNMENT | terminal | 30 | terminal | none | SALES_CATALOG_ASSIGNMENT.PROMPT-MANAGE-SALES-INDEX | stop | The requested assignment targets Sales, the import was accepted, and the Manage Sales Index prompt was issued. |
| RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | The request is outside Sales scope, or Sales catalog-rule validation is blocked. |
