# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| The user provides only enable or disable wording | Apply the documented update-only defaults to the Data Loader workbook before validation. |
| The user requests a new control row or deletion of a control row | Stop; Manage Data Security Controls for Manufacturing updates DataSecurityEnabledFlag on the existing WORK_DEFINITION row only. |
| The workbook headers, row count, object code, or Y/N value is invalid | Stop before validation; identify the affected workbook rule. |
| The Data Loader workbook or immutable validated ZIP is unavailable or invalid | Stop before submission; correct the workbook against the live schema and validate it again through core.data-loader. |
| Data Loader validation, upload, or initiation returns a failure | Stop before retry; report the returned diagnostic and preserve the reviewed artifact unchanged. Revalidate and obtain a new approval preview after correction. |
| A Data Loader result is uncertain, timed out, or cannot be reconciled | Stop and reconcile the result through safe reads. Do not re-submit the artifact. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | Workbook shape, required values, supported object code, or update-only action is invalid | Correct the workbook and rerun task validation. |
| dependency | The validated artifact or existing-object readiness is unavailable | Correct the artifact or environment prerequisite before retry. |
| auth/authz | Required role or privilege fails | Correct access before retry. |
| transport/environment | A Data Loader metadata, validation, upload, or initiation request cannot be completed | Verify the environment; retry only safe reads when appropriate. |
| Fusion API | Data Loader metadata, validation, upload, or initiation returns a functional error | Review the diagnostic and correct the input, registered business-object configuration, or environment configuration; do not automatically retry a write. |
| approval blocker | The validated artifact has not received the required central Data Loader approval | Obtain approval for the exact reviewed artifact before submission. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Failure | Failure class, stage, sanitized message, affected workbook rule or Data Loader validation status, and recommended action. |
| Data Loader approval preview | Immutable artifact name and SHA-256, requested Y or N state, update-only scope, and the approval required before submission. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A validated Data Loader artifact is absent | Do not invent a workbook layout, schema, or ZIP structure in the task resource. |
| Supplied object code is not WORK_DEFINITION | Do not substitute another object code or proceed to approval. |
| The request would create or delete a row | Do not create, delete, or substitute a data-security-control row. |
| The artifact differs from the exact approved immutable ZIP | Do not upload or initiate the load; restart validation and approval. |
| Data Loader has an uncertain result | Do not automatically retry or re-submit the artifact. |
| A direct REST item update is proposed | Do not issue a direct REST write; use the centralized core.data-loader workflow. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SEC.DONE | terminal | 5 | terminal | none | SEC.DESIGN | continue | Validated Data Loader REST artifact and all applicable validation, dependency, and design checks pass |
| SEC.FAILED | terminal | 6 | terminal | none | none | continue | A blocking validation, dependency, or design failure occurs |
