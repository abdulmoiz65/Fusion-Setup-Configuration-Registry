# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Activity Type Group | Verify the selected group before previewing an activity type that references it |
| 2 | Current activity type state | Run collision checks before preview so a replacement preserves existing optional fields |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| activity_type_group | Selected Activity Type Group | Yes | Every proposed activity type | Verify | GET /rest/ofscMetadata/v1/activityTypeGroups/{label} | verify_activity_type_group | groupLabel must equal an existing selected group before an activity type write | Supply the selected group label and stop if its current state cannot be verified | Group Label and current group fields |
| activity_type_collision | Existing Activity Type | Yes | Every proposed activity type | Verify | GET /rest/ofscMetadata/v1/activityTypes/{label} | find_activity_type_by_label | Collision checks distinguish a new record from a replacement and preserve optional fields on replacement | Supply the stable activity type label and stop if current state cannot be verified | Existing optional fields and Activity Type Label |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The required group and activity type state are verified | No |
| Blocked | A group is absent, a lookup is unresolved, or a collision cannot be classified | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AT.DEPENDENCIES | step | 3 | resolve_dependency | ready->AT.DESIGN;blocked->AT.RETURN_ISSUES | AT.LOOKUP_CURRENT_STATE | stop | After current-state checks and before the design gate |
