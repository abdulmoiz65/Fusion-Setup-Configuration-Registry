# Configure Benefits Feature Preferences Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| The requested operation is missing, unsupported, or mapped to the wrong HDL object | Classify as input_validation and stop before preflight. |
| The current Data Loader sample does not support the Update preferences object or requested update operation | Classify as catalog_or_metadata_mismatch and stop; do not infer a schema or substitute an object. |
| The fixed Create preferences DAT or an Update preferences DAT artifact is empty, malformed, changed, or has not passed preflight | Classify as input_validation and stop before upload or initiation. |
| An update DAT filename does not exactly match benefitFeaturePreferences or uses an action other than PATCH | Classify as input_validation and stop before preflight; rebuild the source from the current sample. |
| An update has neither a complete current-sample user key nor an explicitly required PreferenceId | Classify as input_validation and stop; request only the missing identity value. |
| A conditional Update preferences LOV returns 403 | Record unverified_forbidden only for that row and field; do not throw a field-validation error or mark it invalid. Continue independent checks; require authoritative verification before live load. |
| A conditional Update preferences LOV returns zero or multiple distinct exact matches | Record invalid or ambiguous for the affected field; do not choose a candidate or rewrite the supplied value. |
| A data-changing upload or initiation has an uncertain result | Classify as approval_blocker, preserve redacted diagnostics, reconcile through the selected read-only status route, and do not retry automatically. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | The operation, object route, or required load artifact is missing or invalid | Correct the exact missing or invalid value and rerun preflight. |
| catalog_or_metadata_mismatch | The current sample does not support the selected update object or operation | Resolve the current metadata gap; do not infer a replacement route or schema. |
| unverified_forbidden | A conditional lookup returned 403 | Keep field validation nonfailing; verify the value authoritatively before live load. |
| approval_blocker | Approval is missing, stale, or the outcome is uncertain | Do not upload, initiate, or retry without current approval for the exact artifact. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preflight failure | Failure class, failed stage, selected operation, selected HDL object, and corrective action. |
| Reference validation | Each supplied lookup field's row reference, status, and safe correction; distinguish invalid, ambiguous, and unverified_forbidden. |
| Any diagnostic | Sanitized artifact references and external identifiers only; never credentials, tokens, private keys, or full payload values. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Create preferences is requested with benefitFeaturePreferences or Update preferences is requested with initializeBenefitFeaturePreferences | Do not substitute, remap, or submit the object. |
| A Create preferences request includes user-supplied preference values or changes the fixed DAT | Do not transform or submit the values or modified DAT; use the fixed parameterless initialization DAT through core.data-loader. |
| An update DAT uses a suffixed filename, RestAction other than PATCH, or an invented PreferenceStatus code | Do not preflight or submit it; regenerate from the current sample using the exact discriminator filename and supported meaning fields. |
| PreferenceId is blank but the current-sample user key is incomplete | Do not ask for PreferenceId by default; request the missing user-key value unless the current sample explicitly requires PreferenceId. |
| The current sample does not support the selected update schema or operation | Do not invent DAT fields, action syntax, or a delete route. |
| A mutation fails or has an uncertain outcome | Do not automatically retry the upload or initiation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_PREF.GATE_EXECUTION | decision | 20 | execution_gate | approved->BEN_PREF.READY_FOR_EXECUTION;blocked->BEN_PREF.HANDLE_ISSUE | BEN_PREF.LOOKUP_LEGISLATION | stop | Confirm approval is bound to the target, operation, mapped HDL object, and its preflighted immutable load artifact; unverified_forbidden must be authoritatively resolved before live load |
| BEN_PREF.HANDLE_ISSUE | step | 90 | error_handler | handled->BEN_PREF.RETURN_ISSUES | none | stop | A validation, metadata, preflight, approval, or load failure blocks progress |
| BEN_PREF.READY_FOR_EXECUTION | terminal | 100 | terminal | none | BEN_PREF.GATE_EXECUTION | stop | Every documented gate passed; ready for the selected core.data-loader workflow |
| BEN_PREF.RETURN_ISSUES | terminal | 110 | terminal | none | none | stop | A blocking issue was safely disclosed |
