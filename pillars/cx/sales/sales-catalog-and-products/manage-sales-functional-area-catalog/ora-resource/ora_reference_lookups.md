# Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_sales_catalog_assignment_from_scm_export | A user asks which catalog is associated with the Sales functional area | Fresh successful EGP_MANAGE_DEFAULT_CATALOGS export from the target environment, its persisted export receipt, validated same-task package, resolved Sales Functional Area ID 38, functional-area assignment rows, and catalog rows | Require the export receipt and package validation from scm.product-management.catalogs.manage-functional-area-catalogs. In the validated package, require exactly one functional-area assignment row whose functional-area identity is 38 and Sales. Resolve its Catalog Code, then require exactly one catalog row with that exact Catalog Code and map the catalog row's CategorySetName as Catalog Name. Do not use a stale, cross-environment, partial, or candidate import package as current-state evidence. | Catalog Code from the assignment row; Catalog Name from the matching catalog row's CategorySetName; target environment and export receipt | Stop without returning catalog details if the export is absent, stale, unsuccessful, wrong-task, from another environment, structurally invalid, has zero or multiple Sales assignment rows, or has zero or multiple matching catalog rows. |
| prepare_index_invocation_prompt | A Sales catalog-assignment import has been accepted | Accepted import reference, target environment, and optional requested catalog identity | Require a nonblank accepted import reference and environment; write one notification artifact through the local preparation script. | Prompt reference and exact invocation message | Stop when acceptance evidence or target environment is missing. Do not require post-import verification. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Current Sales catalog details are requested | Run a fresh read-only export for EGP_MANAGE_DEFAULT_CATALOGS through shared.setup-export.task-level-export, validate it through the delegated SCM task, resolve the exact Sales assignment, and return Catalog Code and Catalog Name together. |
| A current assignment cannot be resolved exactly | Stop and report the missing, stale, invalid, absent, or ambiguous export evidence. Do not infer a catalog from a prior conversation, candidate import package, or another environment. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_CATALOG_ASSIGNMENT.RESOLVE-CURRENT-SALES-CATALOG | step | 5 | reference_lookup | resolved->SALES_CATALOG_ASSIGNMENT.DONE-INQUIRY;not_found->RETURN_ISSUES;ambiguous->RETURN_ISSUES;failure->RETURN_ISSUES | SALES_CATALOG_ASSIGNMENT.VALIDATE-REQUEST | stop | A question asks which catalog is associated with the Sales functional area |
