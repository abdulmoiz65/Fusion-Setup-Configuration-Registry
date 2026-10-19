# Shipping Parameters Error Handling

Source: Shipping Parameters Redwood page and approved V3 lookup contract.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A standard lookup meaning has no exact match | Stop before Data Loader handoff and request the exact supported meaning or backend code. |
| A standard lookup meaning resolves to multiple rows | Stop before Data Loader handoff and request an unambiguous backend code. |
| A supplied meaning and code resolve to different rows | Stop before Data Loader handoff and request one reconciled value. |
| A BO-owned foreign key cannot be resolved | Preserve the Data Loader diagnostic; do not substitute a task-level resolver. |
| A BO-owned foreign key is omitted before Fusion has returned a diagnostic | Do not request a raw ID, infer a create or update operation, or decide whether a null clears an existing value. Leave the field absent and let the Business Object or Data Loader apply its documented operation-specific validation. |
| A read-only lookup request fails | Preserve the redacted diagnostic and stop. Do not retry a load automatically. |
| Fusion Data Loader rejects the request | Preserve the redacted diagnostic through the Data Loader workflow and do not retry a live operation automatically. |

## Error Classifications

| Failure Class | Trigger | Recoverability | Required Action |
|---|---|---|---|
| Input validation | A supplied friendly value is absent, ambiguous, or conflicts with its code. | Recoverable after corrected input. | Stop before preview and return the affected field and supported-value guidance. |
| Authorization or privilege | The selected environment denies metadata or standard-lookup read access. | Recoverable after privileges are corrected. | Stop and record only a redacted diagnostic. |
| Fusion API error | The approved read-only lookup route returns an unexpected response or error. | Recoverable only through a new approved read attempt. | Stop; do not substitute a value or select the first returned row. |
| Data Loader validation or process failure | `core.data-loader` returns a validation or load diagnostic. | Governed by `core.data-loader`. | Preserve the redacted diagnostic and follow the delegated workflow; never retry a live operation automatically. |

## Evidence, Redaction, and Approval Boundaries

- Invoke read-only lookup requests through `core.fusion-api.rest-api-client`.
- Persist only the lookup name, requested field, outcome, normalized selected
  code when resolved, and a redacted diagnostic reference when blocked.
- Never persist or display access tokens, authorization headers, OAuth
  properties, raw Fusion response bodies, or customer-sensitive values.
- A lookup failure, ambiguous result, or missing required project/environment
  context is a stop condition before preview and Data Loader handoff.
- Only `core.data-loader` may validate, upload, initiate, monitor, or retry an
  import. A live import requires the approval gate declared by that skill.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SP.DONE | terminal | 120 | terminal | none | SP.RESOLVE_TRADE_COMPLIANCE_METHOD | stop | Input and approved standard lookup validation passed; Data Loader owns the subsequent handoff |
| RETURN_ISSUES | terminal | 130 | terminal | none | none | stop | Input or lookup validation failed |
