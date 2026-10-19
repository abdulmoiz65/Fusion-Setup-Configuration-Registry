# Content Type Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Department | Select the content type department before configuring attribute visibility. |
| 2 | Department user groups | Resolve the user groups available for the selected department before restricting field visibility. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| content_type_department | Department | Yes | Create or update a content type | Required | User-provided content type definition | | The department determines the relevant products, categories, and users. | Select a department. | Department |
| attribute_visibility_groups | Department user groups | Conditional | Restricting a schema attribute's visibility | Lookup | Fusion lookup contract TBD | resolve_department_user_groups | Only user groups mapped to the selected department are available for visibility. | Select the department, then resolve the available user groups before setting visibility. | Available user groups |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Required | A department has not been provided | No |
| Lookup | Attribute visibility is restricted | No; lookup contract is TBD |
