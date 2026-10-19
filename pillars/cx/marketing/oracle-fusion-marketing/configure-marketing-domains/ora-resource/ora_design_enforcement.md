# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate sparse source | Verify that the prepared immutable artifact binds the selected primaryDomain and required update identity to $operation=MERGE and only the requested changed fields. Exclude $statusCode and unchanged fields; reject blank identity or changed values. |
| 2 | Limit disclosure | Retain server identifiers and internal envelopes internally; allow only the user-facing field changes and Data Loader preview in the later approval request. |
| 3 | Return validation result | Return DOMAINS.VALIDATION_READY after every applicable check passes. This completes task validation only. Data Loader then builds its preview and obtains explicit approval before upload and initiation. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A prepared immutable artifact is validated before the Data Loader approval preview | Error | | The selection is not exact, a requested input is invalid, the source contains unsupported or unchanged fields, or identity, MERGE operation, or requested values do not match the selected record and request | Correct the source and repeat Data Loader preflight and task validation before building the preview. User approval is obtained afterward by core.data-loader and is not a prerequisite for this validation. | Yes, by correcting the source and repeating validation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DOMAINS.PREVIEW | step | 7 | design_enforcement | validated->DOMAINS.VALIDATION_READY;blocked->RETURN_ISSUES | DOMAINS.COLLECT_CHANGES | stop | Data Loader preflight has prepared the immutable artifact for the displayed selected domain; user approval has not yet been requested |
