# Inventory ABC Analysis Dependency Readiness

## Source Evidence

| Source | Used For |
|---|---|
| User confirmation | External BO registration is complete in the requested processing order |
| Per-run Data Loader metadata preflight | Verifies that each registered BO is visible in the selected environment; the result is runtime evidence, not reusable readiness evidence |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | abcClasses | Verify visibility in the selected environment, then prepare ABC Classes when the request includes them |
| 2 | abcClassifications | Verify visibility in the selected environment, then prepare ABC Classifications after their required class context is available |
| 3 | abcAssignmentGroups | Verify visibility in the selected environment, then prepare ABC Assignment Groups after their required class and classification context is available |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| abc_classes_bo | Data Loader business object metadata | Yes | Before core.data-loader prepares a request containing ABC Classes | Required per run | Read-only Data Loader metadata preflight for abcClasses in the selected environment |  | BO visibility can vary by environment and over time | Verify abcClasses and record the sanitized result in the task validation artifact and skill-run record | abcClasses |
| abc_classifications_bo | Data Loader business object metadata | Yes | Before core.data-loader prepares a request containing ABC Classifications | Required per run | Read-only Data Loader metadata preflight for abcClassifications in the selected environment |  | BO visibility can vary by environment and over time | Verify abcClassifications and record the sanitized result in the task validation artifact and skill-run record | abcClassifications |
| abc_assignment_groups_bo | Data Loader business object metadata | Yes | Before core.data-loader prepares a request containing ABC Assignment Groups | Required per run | Read-only Data Loader metadata preflight for abcAssignmentGroups in the selected environment |  | BO visibility can vary by environment and over time | Verify abcAssignmentGroups and record the sanitized result in the task validation artifact and skill-run record | abcAssignmentGroups |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ABC.CHECK_READINESS | decision | 30 | resolve_dependency | ready->ABC.RESOLVE_ITEM_SCOPE;blocked->ABC.HANDLE_ERROR | ABC.APPLY_DEFAULT | stop | After approved local defaulting, perform the current run's read-only Data Loader metadata preflight for all three BOs before Data Loader handoff |
