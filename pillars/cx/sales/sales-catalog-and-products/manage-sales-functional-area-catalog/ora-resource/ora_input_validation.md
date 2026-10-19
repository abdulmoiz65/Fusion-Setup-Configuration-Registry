# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Sales assignment inquiry | A request to identify the catalog associated with the Sales functional area and a fresh validated EGP_MANAGE_DEFAULT_CATALOGS export from the target environment | Stop before returning an assignment result | Export EGP_MANAGE_DEFAULT_CATALOGS through shared.setup-export.task-level-export and validate the same-task package | A catalog inquiry is requested | resolve_sales_catalog_assignment_from_scm_export |
| Sales catalog assignment change | Functional Area Name Sales or Functional Area ID 38, target Catalog Code, and the Sales rule profile supplied in the Functional Area Rule screenshot: MultItemCatAssignFlag N and DefaultCategoryRequired No | Stop before package preview or import | Provide the Sales functional-area identity and target Catalog Code. Apply the screenshot-backed Sales defaults; do not request a user override for these two Sales rules. | A default catalog assignment is requested | |
| Assignment-only package workspace | Initialized non-symlink project/{project_id} workspace; fresh validated same-task baseline inside it; a new contained output path; explicit replacement confirmation only when output exists | Stop before package preparation or SCM handoff | Correct the project path, baseline, output path or overwrite confirmation. | A default catalog assignment is requested | |
| Catalog detail response | Resolved Catalog Code and resolved Catalog Name | Stop before returning catalog details | Resolve the Sales assignment and catalog rows from the validated SCM export | Catalog details are requested | resolve_sales_catalog_assignment_from_scm_export |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The request names a functional area other than Sales, or provides a conflicting ID and name | BLOCKED | Reject the request before any lookup, package preview, import, or delegation. | |
| A Sales catalog assignment change has no Catalog Code | BLOCKED | Request the target Catalog Code before preparing the delegated SCM package | |
| A Sales catalog assignment change omits MultItemCatAssignFlag or DefaultCategoryRequired | DEFAULTED | Apply the authoritative Sales rule profile: MultItemCatAssignFlag N and DefaultCategoryRequired No. Do not add an EGP_CATALOG.csv row solely to carry these assignment policy values. | |
| A Sales catalog inquiry has no fresh validated SCM export or has not resolved exactly one catalog identity | BLOCKED | Export EGP_MANAGE_DEFAULT_CATALOGS, validate the same-task package, and resolve one Sales assignment before responding | resolve_sales_catalog_assignment_from_scm_export |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Functional area scope | Accept only Sales or ID 38. Reject every conflicting or non-Sales functional-area value, including a request to assign Unified Catalog to Service Functional Area. | Every inquiry or assignment request | |
| Catalog Code | Require a nonblank target Catalog Code | A default catalog assignment is requested | |
| Sales rule profile | Default MultItemCatAssignFlag to N and DefaultCategoryRequired to No from the supplied Sales Functional Area Rule screenshot. Treat an attempted conflicting value as unsupported for this Sales-specific task. | A default catalog assignment is requested | |
| Catalog identity response | Require both Catalog Code and Catalog Name from one resolved assignment and catalog identity pair | Catalog details are requested | resolve_sales_catalog_assignment_from_scm_export |
| Local artifact safety | Require the baseline and output to be distinct regular files under the project workspace; reject symlinked parents, malformed packages and an existing output without explicit replacement confirmation. | A default catalog assignment is requested | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_CATALOG_ASSIGNMENT.VALIDATE-REQUEST | decision | 1 | validate_input | inquiry_complete->SALES_CATALOG_ASSIGNMENT.RESOLVE-CURRENT-SALES-CATALOG;assignment_complete->SALES_CATALOG_ASSIGNMENT.CHECK-DEPENDENCIES;outside_sales_scope->RETURN_ISSUES;incomplete->RETURN_ISSUES | none | stop | Any catalog assignment or catalog inquiry request that names or implies a functional area is requested |
