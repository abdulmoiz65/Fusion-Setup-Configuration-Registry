# Custom Time Attributes Error Handling

## Source Basis

- User-provided Generic FSM Baseline for Custom Time Attributes, 5 October 2026.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required parent or dependent field is missing or has an unsupported selection | Identify the field and accepted choices; stop before preview. |
| Name normalization, Value Location mapping, or source/category lookup is unresolved | Report the specific missing contract; do not generate a guessed value or assume local authority. |
| A requested data source is absent from the fresh export | Present the mismatch and obtain explicit user confirmation that the source is available in Fusion before continuing. Record the lookup as overridden and reconcile the requested source link after import. If the link is unchanged, report the update as not applied and do not retry automatically. |
| Dependent attributes conflict with Classification | Request correction; do not silently discard children or add excluded fields. |
| An edit changes a protected parent field | Identify the protected field, preserve its exported value, and stop before preview until the requested change excludes Display Name, Name, Data Type, Classification, Attribute Category, and Value Location. |
| An edit changes a protected dependent field | Identify the protected field, preserve its exported value, and stop before preview until the requested change excludes Display Name, Name, Data Type, and Value Location. |
| Fresh same-task export cannot be obtained or validated | Stop; preserve diagnostics and identify the failed export or validation stage. |
| FSM evidence does not prove the expected import route | Stop and rebuild; do not substitute a direct REST mutation or HDL archive. |
| Approval is missing or stale | Stop before submission; require explicit approval for the current immutable preview. |
| Import fails, partially succeeds, times out, or is uncertain | Preserve diagnostics, reconcile current state through the documented task read/export path, and stop. Never automatically retry. |
| Task-specific contract is missing | Identify the precise missing business contract before export, or missing package/reconciliation evidence at its post-export stage. Do not invent fields, defaults, LOV behavior, keys, or selectors. |
| Reconciliation cannot complete | Preserve the uncertain result and diagnostics; stop without resubmission. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Preparing the package | Do not change unrelated exported values. |
| Selecting execution route | Do not convert the FSM package to an HCM Data Loader archive or make direct Fusion REST mutations. |
| Reusing execution evidence | Do not reuse stale preview or approval evidence. |
| Failed, partial, timed-out, or uncertain import | Do not automatically retry or claim success. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CTA.HANDLE_ISSUE | step | 80 | error_handler | handled->CTA.RETURN_ISSUES | none | stop | A validation, design, export, approval, import, or reconciliation failure is reported |
| CTA.RETURN_ISSUES | terminal | 91 | terminal | none | CTA.HANDLE_ISSUE | stop | Return the specific blocker and safe next action |
| CTA.RETURN_HANDOFF | terminal | 90 | terminal | none | CTA.ENFORCE_FSM | stop | The Complete Summary is displayed and the validated package is ready for the provider-owned approval preview and import |
