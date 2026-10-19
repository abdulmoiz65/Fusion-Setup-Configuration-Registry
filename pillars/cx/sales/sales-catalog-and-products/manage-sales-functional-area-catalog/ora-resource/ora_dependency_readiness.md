# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Sales functional-area scope | Confirm the request targets Sales Functional Area Assignments. |
| 2 | Catalog identity | For an inquiry, resolve the assigned catalog from a fresh validated EGP_MANAGE_DEFAULT_CATALOGS export; for an assignment change, provide the target Catalog Code. |
| 3 | Delegated SCM workflow | Use Manage Functional Area Catalogs for any FSM package, import, and post-import validation. |
| 4 | Assignment-only package | Build and validate the contained Sales assignment-only package before handing it to SCM. |
| 5 | Index invocation prompt | After the delegated import is accepted, persist a prompt that Manage Sales Index can be invoked; do not wait for import verification. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| SALES_CATALOG_ASSIGNMENT.SALES_SCOPE | Sales Functional Area Assignments | Yes | Every inquiry or assignment request | Satisfied only for Sales | Requested functional-area identity | | This task is limited to Sales | Reject every non-Sales functional-area request; do not delegate it to another functional-area workflow. | Functional Area Name, Functional Area ID |
| SALES_CATALOG_ASSIGNMENT.CATALOG_INQUIRY_EXPORT | Current Sales assignment export | Yes | A catalog inquiry is requested | Lookup | Fresh validated EGP_MANAGE_DEFAULT_CATALOGS export from the target environment | resolve_sales_catalog_assignment_from_scm_export | A current response requires authoritative same-environment assignment data | Complete a fresh delegated SCM task export; return Catalog Code and Catalog Name from exactly one Sales assignment | Catalog Code, Catalog Name, export receipt |
| SALES_CATALOG_ASSIGNMENT.ASSIGNMENT_CATALOG_CODE | Target Catalog Code | Yes | A catalog assignment change is requested | Satisfied | User-provided Catalog Code | | The delegated assignment package requires one target catalog identity | Provide the exact target Catalog Code | Catalog Code |
| SALES_CATALOG_ASSIGNMENT.ASSIGNMENT_PACKAGE | Contained Sales assignment-only package | Yes | A catalog assignment change is requested | Satisfied | Fresh validated same-task baseline, project workspace, target Catalog Code, and build_sales_assignment_package.py | | The SCM task must receive a package that changes only the Sales assignment and does not overwrite source evidence. | Build one staged package with the required metadata, one Sales assignment row and header-only unrelated members; reject unsafe path, package or overwrite conditions. | Immutable package reference and validation receipt |
| SALES_CATALOG_ASSIGNMENT.SCM_DELEGATION | SCM Manage Functional Area Catalogs | Yes | An assignment change is requested | Satisfied | Delegated task guidance | | The Sales task delegates FSM operations to SCM | Use the delegated task workflow; do not import from this task directly | Delegated Task Code EGP_MANAGE_DEFAULT_CATALOGS |
| SALES_CATALOG_ASSIGNMENT.INDEX_INVOCATION_PROMPT | Manage Sales Index prompt after import acceptance | Yes | A Sales catalog-assignment import has been accepted | Satisfied | Accepted import reference, target environment, and requested catalog identity | prepare_index_invocation_prompt | The user should be notified immediately that independent Item or Catalog indexing can be requested. | Persist the prompt and present the exact invocation message; do not invoke the child or wait for verification. | Prompt reference, accepted import reference, target environment |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| BLOCKED | Sales scope, a fresh inquiry export, target Catalog Code, or SCM delegation is missing or conflicts with the request; any non-Sales scope is rejected | No |
| READY | All applicable dependencies are present and consistent | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_CATALOG_ASSIGNMENT.CHECK-DEPENDENCIES | decision | 3 | resolve_dependency | ready->SALES_CATALOG_ASSIGNMENT.ENFORCE-SALES-SCOPE;missing->RETURN_ISSUES | SALES_CATALOG_ASSIGNMENT.VALIDATE-REQUEST | stop | A Sales default catalog assignment is requested |
| SALES_CATALOG_ASSIGNMENT.PROMPT-MANAGE-SALES-INDEX | step | 25 | resolve_dependency | prompted->SALES_CATALOG_ASSIGNMENT.DONE-ASSIGNMENT;blocked->RETURN_ISSUES | SALES_CATALOG_ASSIGNMENT.ENFORCE-SALES-RULES | stop | The Sales assignment import has been accepted. |
