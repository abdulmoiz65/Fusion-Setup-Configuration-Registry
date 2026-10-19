# Manage Resource Roles Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Resource roles | Create needed roles before assigning field resources to organizations or work |
| 2 | Resource role types | Validate each supplied Role Type or RoleTypeCode against the `JTF_RS_ROLE_TYPE` standard lookup through Manage Resource Role Lookups |
| 3 | Resource types | Associate roles with required field resource types before adding users |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| MRR-ROLE-TYPES | Resource types and associated roles | Yes | Before adding users | Verify | User-provided setup evidence | Manual UI verification | Roles must be associated with resource types | Confirm required roles and types are created and associated | Associated Resource Role |
| MRR-ROLE-TYPE-LOOKUP | Resource role type lookup code | Yes | Before creating, importing, or updating a resource role | Verify | Role Type or RoleTypeCode | `cx.customer-data-management.resources.manage-resource-role-lookups` using `JTF_RS_ROLE_TYPE` | The role type must be a valid lookup code before the role can be used | Require an exact `LookupCode` match. If absent, direct the user to Manage Resource Role Lookups to set up or activate the type, then revalidate | Role Type or RoleTypeCode |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Verify | Before user onboarding or work assignment | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRR.DEPENDENCIES | decision | 4 | resolve_dependency | ready->MRR.ADVISORY;blocked->MRR.BLOCKED | MRR.ROLE_TYPE_LOOKUP | stop | Role inputs and role-type lookup validation pass |
