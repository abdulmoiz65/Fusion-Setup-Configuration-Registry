# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Source is unreadable, ambiguous, or missing required values | Stop before CSV generation and request the smallest clarification. |
| Current public page, workbook, or linked control file cannot be fetched | Stop as transport_or_environment, not template drift. Use a finite download timeout of at most 60 seconds per request and no automatic retry. Report the public source and sanitized failure; check public URL availability and network access before starting a new cycle. Never use a stale layout, an older release, or a retired exporter. |
| Retrieved workbook or control-file content differs from the run-bound contract | Stop as catalog_or_metadata_mismatch (template drift). Resolve the changed schema and start a fresh current-template cycle; never fall back to an older contract. |
| CSV or ZIP validation fails | For source-data input, discard the incomplete transient artifact and regenerate after correcting the local issue. For a supplied ZIP, stop and request a corrected archive or source. |
| ZIP changes after validation | Restart template-driven validation and produce new handoff evidence. |
| Source, run-bound template/control files, and ZIP digest are unchanged after successful preflight | Reuse the exact archive and persisted preflight envelope; do not rebuild or rerun local, preflight, or Task Hook validation. |
| Handoff metadata is incomplete | Stop before handing the ZIP to core.data-loader. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Missing or ambiguous source facts, invalid CSV/ZIP values or shape, broken header-child links, or incomplete handoff evidence | Correct the source or request a corrected supplied archive before a new validation cycle. |
| catalog_or_metadata_mismatch | Retrieved template/control contract drift or inconsistent task metadata | Resolve the schema or task identity before a fresh current-template cycle. |
| transport_or_environment | Public-source DNS, connection, timeout, or HTTP availability failure | Stop without automatic retry; verify the public source and connectivity before a new cycle. |
| artifact_persistence | Cannot read/write the controlled artifact location or persist required evidence | Resolve the path, permissions, or persistence issue; do not hand off an unrecorded archive. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Failed local cycle | Use schemas/validation-result.schema.json: status failed, an error finding with a sanitized message (including stage and failure_class), recommended_action, and a safe artifact reference when available. Use schemas/skill-run.schema.json: status failed, artifact_refs, and notes containing the stage, failure_class, public-source or local environment identity, and next action. Do not add undeclared JSON fields or a third target-local diagnostic file. |
| Public download failure | Include the public host/path, HTTP status if available, timeout or connection category, and the next connectivity/source check. Omit query credentials, headers, response bodies, tokens, and customer data. |

This skill does not perform authorization, upload, import,
monitoring, ESS, or Fusion API operations; `core.data-loader` handles any
later execution failure in its own workflow.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CHANGE_ORDER_FBDI.HANDOFF | decision | 3 | execution_gate | ready->CHANGE_ORDER_FBDI.COMPLETE;blocked->CHANGE_ORDER_FBDI.FAILED | CHANGE_ORDER_FBDI.READY | stop | Immediately before handing the unchanged validated ZIP to `core.data-loader`. |
| CHANGE_ORDER_FBDI.COMPLETE | terminal | 4 | terminal | none | CHANGE_ORDER_FBDI.HANDOFF | continue | Local validation and immutable handoff evidence are complete. |
| CHANGE_ORDER_FBDI.FAILED | terminal | 5 | terminal | none | none | continue | Any local validation, template, public-source transport, or artifact-persistence failure occurs. |
