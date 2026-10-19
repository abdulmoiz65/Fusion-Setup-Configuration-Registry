# Revision Preferences for Sales Orders Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Discovery response is incomplete, unavailable, or ambiguous | Stop before preview preparation and report the failed read-only discovery stage. |
| Data Loader update fails or has an indeterminate outcome | Do not retry automatically. Preserve sanitized diagnostics and reconcile through read-only verification. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Change approval | Requested attribute names, normalized preference, group expansion, target environment, and the current approved pre-upload approval preview. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| REVISION_PREFERENCES.APPROVAL_GATE | step | 40 | execution_gate | preview-ready->RETURN_SUCCESS;preview-missing-or-changed->RETURN_ISSUES | REVISION_PREFERENCES.ENFORCE_GROUPS | stop | The pre-upload approval preview has passed input, discovery, group-enforcement, and approval validation. |
| RETURN_SUCCESS | terminal | 50 | terminal | none | REVISION_PREFERENCES.APPROVAL_GATE | continue | The validated change is ready for separate explicit Data Loader submission approval. |
| RETURN_ISSUES | terminal | 60 | terminal | none | none | continue | A validation, lookup, group-enforcement, preview, or approval gate failed. |
