# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Classify Sales request | Treat a current-catalog question as a Sales Functional Area Assignments inquiry and keep it separate from an assignment change. |
| 2 | Enforce Sales-only scope | Confirm that the request targets Sales; reject every non-Sales request before lookup, package preparation, import, or delegation. |
| 3 | Resolve inquiry identity | For an inquiry, use the documented fresh SCM export lookup and return Catalog Code and Catalog Name together. |
| 4 | Apply Sales rule profile | For an assignment change, apply the supplied Sales values to assignment inputs. Apply catalog and category values only when the package already includes the corresponding catalog or category row for an independently requested change; do not add those rows solely to restate Sales policy. |
| 5 | Preserve assignment-only scope | Prepare exactly one Sales assignment row and header-only unrelated members from a validated baseline; never overwrite source evidence or a package without confirmation. |
| 6 | Reject unsupported scope or mapped-rule violations | Stop this task when the request is not for Sales, an inquiry cannot resolve one complete catalog identity, or an assignment violates a Sales rule represented in the validated package. |

## Design Rules

| Applies When | Severity | Required Lookup | What Blocks Preview | Fix Allowed? | User Guidance |
|---|---|---|---|---|---|
| A default catalog assignment is requested through manage-sales-functional-area-catalog | Error |  | The requested functional area is missing, ambiguous, or is not exactly Sales | No | Reject the request. This task accepts only Sales functional area assignments and must not route a non-Sales request to another workflow. |
| A user asks which catalog is associated with the Sales functional area | Error | resolve_sales_catalog_assignment_from_scm_export | A fresh validated EGP_MANAGE_DEFAULT_CATALOGS export does not resolve exactly one Sales assignment and one matching catalog identity | Yes | Export the delegated SCM task from the target environment and return its resolved Catalog Code and Catalog Name together. |
| A catalog is assigned to Sales | Error |  | The assignment input attempts to override MultItemCatAssignFlag N or DefaultCategoryRequired No; or a separately included catalog/category row conflicts with the applicable supplied Sales rule value | No | Use the Sales profile. An assignment-only EGP_DEFAULT_CATALOG_FUNCTIONAL_AREA.csv row does not carry catalog or category policy fields, so do not add EGP_CATALOG.csv or EGP_CATEGORY.csv rows solely to enforce them. |
| A Sales assignment-only package is prepared | Error |  | The baseline/output paths leave the initialized project workspace, contain symlinks, alias each other, an output exists without explicit replacement confirmation, or the staged member set is not the required metadata, one Sales assignment row and header-only unrelated members | No | Correct the artifact inputs and prepare a new staged package; hand only its immutable validated reference to the delegated SCM task. |
| Catalog details are requested for a Sales functional-area assignment | Error | resolve_sales_catalog_assignment_from_scm_export | The response omits Catalog Code or Catalog Name after the catalog identity has been resolved | No | Always return Catalog Code and Catalog Name together. |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_sales_catalog_assignment_from_scm_export | A user requests current Sales functional-area catalog details | Catalog Code, Catalog Name, target environment, and fresh export receipt | ora_reference_lookups.md |

## Sales Functional Area Policy Reference

The policy values below remain the Sales design reference. The current delegated EGP_MANAGE_DEFAULT_CATALOGS export proves only `HierarchyEnabled` and `MultItemCatAssignFlag`; therefore this task does not claim that the other policy values were runtime-validated. Validate those values only through a separately documented authoritative source and routed workflow.

| Rule | Required Sales Value | Validation Status in This Task |
|---|---|---|
| Functional Area ID | 38 | Enforced through the Sales scope lookup |
| Assign items to leaf-level categories only | False | Map to CatalogContentCode ALL_ITEMS only when a catalog row is independently included; do not add a catalog row for an assignment-only change |
| Enable duplicate category names | True | Policy reference only; not represented in the delegated export mapping |
| Allow multiple item category assignments | False | Default assignment input MultItemCatAssignFlag to N; map to EGP_CATALOG.csv.MultItemCatAssignFlag only when a catalog row is independently included |
| Enable deletion of item category assignments | True | Policy reference only; not represented in the delegated export mapping |
| Enable hierarchy for catalog | True | Map to EGP_CATALOG.csv.HierarchyEnabled = Y only when a catalog row is independently included |
| Enable date-level control for item category assignments | True | Policy reference only; not represented in the delegated export mapping |
| Default category required | False | Default assignment input DefaultCategoryRequired to No; do not create a category or catalog row solely to carry this rule |
| Controlled at | Master | Map to EGP_CATALOG.csv.ControlLevel = 1 only when a catalog row is independently included |
| Catalog assignment change | Change allowed unconditionally | Policy reference only; not represented in the delegated export mapping |
| Catalog data security enabled | False | Policy reference only; not represented in the delegated export mapping |
| Automatic assignment of items | False | Policy reference only; not represented in the delegated export mapping |
| Restrict category to item assignment only | False | Map to EGP_CATEGORY.csv.CategoryContentCode = MIXED only when a category row is independently included |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_CATALOG_ASSIGNMENT.ENFORCE-SALES-SCOPE | decision | 10 | design_enforcement | sales_scope_valid->SALES_CATALOG_ASSIGNMENT.ENFORCE-SALES-RULES;unsupported_scope->RETURN_ISSUES | SALES_CATALOG_ASSIGNMENT.CHECK-DEPENDENCIES | stop | A Sales default catalog assignment is requested; non-Sales scope must already have been rejected by SALES_CATALOG_ASSIGNMENT.VALIDATE-REQUEST |
| SALES_CATALOG_ASSIGNMENT.ENFORCE-SALES-RULES | decision | 20 | design_enforcement | compliant->SALES_CATALOG_ASSIGNMENT.PROMPT-MANAGE-SALES-INDEX;noncompliant->RETURN_ISSUES | SALES_CATALOG_ASSIGNMENT.ENFORCE-SALES-SCOPE | stop | A catalog is assigned to Sales and its assignment inputs or any independently included catalog/category rows are checked against the supplied Sales rule profile. |
