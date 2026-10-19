# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Procurement and external purchase prices | The offering and functional area must be enabled for the target environment |
| 2 | Requisitioning BU | A specific-BU record must reference an active requisitioning BU |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| EPPPAD-BU | Active requisitioning BU | Conditional | Specific-BU setup | Core validation | User-supplied BU identity | | Oracle permits specific defaults only for an active requisitioning BU; `core.data-loader` and Fusion validate the supplied identity | Provide one exact requisitioning BU identity; correct the returned Data Loader diagnostic if validation fails | Requisitioning BU identity |
| EPPPAD-CONTRACT | Data Loader import workflow | Yes | Data Loader import | Core workflow | `core.data-loader` | | The core workflow validates the registered business object, creates an immutable archive, runs Task Hook when task-routed, and requires exact-artifact approval before upload | Use `core.data-loader`; do not construct a direct REST write payload | Validated archive and approval-bound preflight |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPPAD.CHECK_DEPENDENCIES | decision | 2 | resolve_dependency | ready->EPPPAD.APPLY_DEFAULTS;missing->EPPPAD.HANDLE_ISSUES | EPPPAD.VALIDATE_INPUT | stop | Every request |
