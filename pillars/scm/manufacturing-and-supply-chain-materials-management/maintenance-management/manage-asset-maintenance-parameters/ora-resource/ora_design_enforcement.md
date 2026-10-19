# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce Data Loader ownership | Route the request through core.data-loader; the pillar skill must not select a REST endpoint, construct a REST payload, or submit a Fusion write. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Asset Maintenance Parameters create or update | Error | | The request bypasses the active Run Book or core.data-loader, or the business object is not assetSystemOptions | Correct the Run Book task and route before preview | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|
| AAMP.ENFORCE_DATALOADER_ROUTE | decision | 30 | design_enforcement | compliant->AAMP.DATALOADER_GATE;blocked->AAMP.DIRECT_REST_BLOCKED | AAMP.CHECK_RUNBOOK_SCOPE | stop | Asset Maintenance Parameters create or update |
