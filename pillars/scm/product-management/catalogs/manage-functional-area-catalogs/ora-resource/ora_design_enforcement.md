# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm applicability | Confirm the catalog is needed for the intended SCM product usage before proceeding. |
| 2 | Validate catalog configuration | Ensure the catalog conforms to the selected functional area's rules before treating the assignment as ready. |
| 3 | Assess assignment impact | Assess automatic-assignment and shared-offering impact before proceeding. |

## Design Rules

| Applies When | Severity | Required Lookup | What Blocks Preview | Fix Allowed? | User Guidance |
|---|---|---|---|---|---|
| A catalog is created or assigned to a resolved functional area | Error | | The user has not supplied `MultItemCatAssignFlag`; `DefaultCategoryRequired` is also missing only when no default Category Code or Category Name is supplied | No | Prompt once for an applicable public Oracle Functional Area Catalog Rules document reference. Continue when the user declines or does not provide it, recording `not_provided`. Infer `DefaultCategoryRequired=Yes` from a supplied default-category identity. Preserve explicit `HierarchyEnabled`; otherwise use the REST Describe default `Y`. |
| `DefaultCategoryRequired` is user-provided or inferred as Yes | Error | | A default category does not exist or EGP_CATALOG.csv.CategoryCode is blank | No | Ask the user to provide the default Category Code or Category Name only when neither was supplied. After the user supplies it, resolve the identity, retain the matching category row, and map the resolved Category Code as the catalog default category. |

## Design Evidence Requirements

For a catalog created or assigned to a resolved functional area, retain the user-provided Functional Area Name, `HierarchyEnabled`, `MultItemCatAssignFlag`, public-document reference status (`provided` with its value, or `not_provided`), and `DefaultCategoryRequired` with its source (`user-provided` or `inferred from default category`) as validation evidence. This is user input and deterministic input derivation, not a task-local lookup.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CATALOGS.ENFORCE-FUNCTIONAL-AREA-RULES | step | 18 | design_enforcement | compliant->CATALOGS.VERIFY-REFERENCED-BASELINE-CATALOG;default_category_missing->RETURN_ISSUES | CATALOGS.RESOLVE-FUNCTIONAL-AREA-ID | stop | A catalog is created or assigned to a functional area |
