# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Run Book scope | The active Run Book must include the published assetSystemOptions Data Loader REST business object before Data Loader preview or submission. |
| 2 | Generated or supplied source | Before the Task Hook and preview, core.data-loader must have created a live-schema update XLSX sample or validated the supplied source artifact. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| AAMP_RUNBOOK_SCOPE | Active Run Book scope | Yes | Asset Maintenance Parameters create or update | Verify | Active Run Book and Data Loader state | | Data Loader rejects a business object outside the Run Book scope | Select or create a Run Book task that includes assetSystemOptions | Active Run Book task and business object scope |
| AAMP_SOURCE_ARTIFACT | Data Loader source artifact | Yes | Asset Maintenance Parameters create or update | Verify | core.data-loader result | | The Task Hook runs only after the exact immutable upload artifact is prepared | Generate the live XLSX sample from assetSystemOptions or provide a supported artifact, then validate it through core.data-loader | Generated or validated artifact fingerprint |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AAMP.CHECK_RUNBOOK_SCOPE | decision | 20 | resolve_dependency | scope_ready->AAMP.ENFORCE_DATALOADER_ROUTE;blocked->AAMP.SCOPE_BLOCKED | AAMP.VALIDATE_INPUT | stop | Asset Maintenance Parameters create or update |
