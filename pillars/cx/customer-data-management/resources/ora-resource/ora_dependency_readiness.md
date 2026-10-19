# Manage Resource Roles Dependency Readiness

## Required Dependency Order

| Task Code | Task Name | Sequence | Dependency | What Must Happen |
|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | 1 | Resource roles | Create needed roles before assigning field resources to organizations or work |
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | 2 | Resource types | Associate roles with required field resource types before adding users |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | MRR-ROLE-TYPES | Resource types and associated roles | Yes | Before adding users | Verify | User-provided setup evidence | Manual UI verification | Roles must be associated with resource types | Confirm all required roles and types are created and associated | Associated Resource Role |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Verify | Before user onboarding or work assignment | No |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | MRR.DEPENDENCIES | decision | 3 | resolve_dependency | ready->MRR.ADVISORY;blocked->MRR.BLOCKED | MRR.VALIDATE | stop | Role inputs pass validation |
