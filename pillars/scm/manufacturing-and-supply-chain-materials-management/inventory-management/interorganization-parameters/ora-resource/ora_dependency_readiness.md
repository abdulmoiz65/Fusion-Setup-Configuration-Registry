# Interorganization Parameters Dependency Readiness

## Source Evidence

| Source | Used For |
|---|---|
| User confirmation | External BO registration is complete for interOrganizationParameters |
| Per-run Data Loader metadata preflight | Verifies that interOrganizationParameters is visible in the selected environment; the result is runtime evidence, not reusable readiness evidence |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Data Loader business object metadata | Complete a read-only per-run metadata preflight for interOrganizationParameters in the selected environment before Data Loader preparation |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| interorganization_parameters_bo | Data Loader business object metadata | Yes | Before core.data-loader prepares a request containing Interorganization Parameters | Required per run | Read-only Data Loader metadata preflight for interOrganizationParameters in the selected environment |  | BO visibility can vary by environment and over time | Verify interOrganizationParameters and record the sanitized result in the task validation artifact and skill-run record | interOrganizationParameters |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IOP.CHECK_READINESS | decision | 20 | resolve_dependency | ready->IOP.RESOLVE_TRANSFER_TYPE;blocked->IOP.HANDLE_ERROR | IOP.VALIDATE_INPUT | stop | After input validation, perform the current run's read-only Data Loader metadata preflight for interOrganizationParameters before lookup resolution or Data Loader handoff |
