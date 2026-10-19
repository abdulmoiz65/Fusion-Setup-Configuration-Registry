# Error Handling

| Situation | Required action |
|---|---|
| Source is unreadable, ambiguous, or missing required values | Stop before CSV generation and request the smallest clarification. |
| Current public template cannot be fetched or differs from the local contract | Stop as template drift; do not use a stale layout. |
| CSV or ZIP validation fails | Discard the incomplete transient artifact and regenerate after correcting the local issue. |
| ZIP changes after validation | Restart template-driven validation and produce new handoff evidence. |
| Handoff metadata is incomplete | Stop before handing the ZIP to `core.data-loader`. |

Classify these failures as input validation, catalog mismatch, or artifact
persistence. This skill does not perform authorization, upload, import,
monitoring, ESS, or Fusion API operations; `core.data-loader` handles any
later execution failure in its own workflow.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ITEM_IMPORT.HANDOFF_GATE | decision | 3 | execution_gate | ready->ITEM_IMPORT.READY_FOR_CORE_DATA_LOADER;blocked->ITEM_IMPORT.FAILED | ITEM_IMPORT.CONFIRM_LOADER_ROUTE | stop | Immediately before handing the unchanged validated ZIP to `core.data-loader`. |
| ITEM_IMPORT.READY_FOR_CORE_DATA_LOADER | terminal | 4 | terminal | none | ITEM_IMPORT.HANDOFF_GATE | continue | Local validation and immutable handoff evidence are complete. |
| ITEM_IMPORT.FAILED | terminal | 5 | terminal | none | none | continue | Any local validation, template, or artifact-persistence failure occurs. |