# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Existing profile option | Select an existing profile option; this workflow does not create a profile option definition. |
| 2 | Scoped value state | Resolve the current value and confirm the requested level is enabled and updateable. |
| 3 | Privilege and approval | Confirm required privilege and exact-change approval before an update. |
| 1 | Same-task export baseline | Export the Action Categories task before a create, update, or disable package is prepared. |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS | Manage Action Plan Profile Options | selected_profile_option | Existing profile option and scoped value | Yes | Reviewing or configuring | Verify | Profile options API examples supplied in metadata | resolve_profile_option_scope | The workflow must retain the selected existing definition and scope state | Provide the exact option and scope | Profile definition, current configured value |
| ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS | Manage Action Plan Profile Options | profile_value_privilege | Required profile-value privilege | Yes | Configuring | TBD | TBD | TBD | The supplied source requires the privilege but does not define a verification contract | Provide evidence of the required privilege | TBD |
| ORA_SVC_MANAGE_ACTION_CATEGORIES_FOR_ACTION_PLANS | Manage Action Categories for Action Plans | action_category_export_baseline | Completed same-task export | Yes | Creating, updating, or disabling | Verify | shared.setup-export.task-level-export | | The package must retain the same-task export baseline and task-owned values | Provide the completed Action Categories export | Exported parent, rows, headers, and package metadata |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|---|
| ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS | Manage Action Plan Profile Options | Blocked | A required option, scope, privilege, or approval is unresolved | No |
