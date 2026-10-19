# Lot and Serial Attribute Mappings Error Handling

## Source Evidence

| Source | Used For |
|---|---|
| User confirmation and configured target environment, View Business Objects | Inventory Descriptive Flexfield Context Mappings is registered and visible to Data Loader. |
| Authoring scope decision | No direct REST write guidance is permitted; core.data-loader owns execution and backend validation. |

## Error Situations

| Situation | What Should Happen |
|---|---|
| Data Loader metadata for Inventory Descriptive Flexfield Context Mappings is unavailable in a future environment | Stop and report the registered BO and failed metadata check. Do not fall back to direct REST write guidance. |
| Data Loader rejects a prepared row | Preserve the Data Loader status, row identity, failure class, and sanitized message. Data Loader and Fusion own backend validation. |
| A task-specific LOV, default, or normalization is requested without verified Redwood evidence | Stop and obtain the UI source evidence and required approval before adding a local rule. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Data Loader availability | Business-object metadata is unavailable. | Verify registration and target-environment access before retrying. |
| Data Loader validation | Data Loader or Fusion rejects prepared data. | Correct the source data using the reported diagnostic. |
| Authoring evidence | A UI-derived rule lacks verified source evidence. | Obtain the Redwood page source or verified UI evidence and approve the proposed rule. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Data Loader handoff | Task code, task name, business object Inventory Descriptive Flexfield Context Mappings, and metadata-visibility status. |
| Data Loader failure | Data Loader request or process identifier when available, failed row identity, sanitized message, stage, and recommended next action. |
| UI-derived rule blocker | Missing source evidence, affected proposed rule type, and the required evidence or approval. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Data Loader metadata is unavailable | Do not create direct REST POST, PATCH, or DELETE guidance as a fallback. |
| A retry follows an uncertain Data Loader failure | Do not resubmit until Data Loader status and read-only verification clarify the outcome. |
| Redwood behavior is unverified | Do not infer LOV resolution, defaulting, checkbox conversion, or other client-side normalization. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LSAM.DATA_LOADER_HANDOFF | decision | 30 | execution_gate | ready->LSAM.DONE;blocked->LSAM.HANDLE_ERROR;failure->LSAM.HANDLE_ERROR | LSAM.CHECK_DEPENDENCIES | stop | Before handing prepared data to core.data-loader for Inventory Descriptive Flexfield Context Mappings. |
| LSAM.HANDLE_ERROR | step | 40 | error_handler | handled->LSAM.RETURN_ISSUES | none | stop | Any normalization, readiness, Data Loader, or authoring-evidence issue. |
| LSAM.RETURN_ISSUES | terminal | 50 | terminal | none | none | stop | A blocking issue was classified and disclosed. |
| LSAM.DONE | terminal | 60 | terminal | none | LSAM.DATA_LOADER_HANDOFF | stop | BO readiness passed and core.data-loader owns subsequent validation and execution. |
