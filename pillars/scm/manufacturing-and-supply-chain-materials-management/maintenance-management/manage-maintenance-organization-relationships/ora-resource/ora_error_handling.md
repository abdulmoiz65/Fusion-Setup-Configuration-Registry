# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required relationship identity or type is missing | Stop and request the missing input. |
| Contextual organization is not maintenance-enabled | Stop; select a maintenance-enabled contextual organization. |
| Relationship type conflicts with organization eligibility | Stop; select a permitted reciprocal, supports, or supports as primary relationship. |
| Primary relationship conflicts with Oracle's single-primary rule | Stop; retain only one primary maintenance organization for the non-maintenance organization. |
| Work-order prerequisite is missing | Stop before relying on the relationship for work-order creation; correct access, item enablement, or common work-definition setup. |
| Data Loader validation, preview, approval, submission, or status reports a failure | Preserve the safe Data Loader diagnostic and follow its recovery guidance; do not submit another attempt automatically. |
| A direct Fusion REST write is requested | Stop; route the request to core.data-loader through the active Run Book. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Maintenance organization relationship create or remove | Do not construct a REST payload, select a REST endpoint, or call a direct Fusion REST write. |
| Data Loader scope or approval is absent | Do not submit a load. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MMOR.DATALOADER_GATE | decision | 40 | execution_gate | handoff_ready->MMOR.DATALOADER_HANDOFF;blocked->MMOR.HANDOFF_BLOCKED | MMOR.ENFORCE_RELATIONSHIP_DESIGN | stop | Before core.data-loader preview or submission |
| MMOR.MISSING_INPUT | terminal | 90 | terminal | none | none | stop | Required input is missing or invalid |
| MMOR.DEPENDENCY_BLOCKED | terminal | 91 | terminal | none | none | stop | A mandatory dependency is not ready |
| MMOR.DESIGN_BLOCKED | terminal | 92 | terminal | none | none | stop | A relationship design rule is violated |
| MMOR.HANDOFF_BLOCKED | terminal | 93 | terminal | none | none | stop | Data Loader preview or approval gate is not ready |
| MMOR.DATALOADER_HANDOFF | terminal | 100 | terminal | none | MMOR.DATALOADER_GATE | stop | Validated request is handed to core.data-loader |
