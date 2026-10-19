# Error Handling

## Source

- Oracle Fusion Cloud SCM, [Manage Cost Elements and Analysis Groups](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/manage-cost-elements-and-analysis-groups.html)
- Developer-provided REST payload example and required `costAccountingCostAnalysisGroups` Data Loader business object

## Error Situations

| Situation | What Should Happen |
|---|---|
| AnalysisGroupCode is missing | Stop and request the analysis group code. |
| A supplied child analysis-code record has no AnalysisCode | Stop and request the missing analysis code. |
| A supplied DefaultAnalysisCodeFlag cannot be normalized from `Yes`/`No`, `True`/`False`, or `Y`/`N` | Stop before preview. Correct the selection, normalize it to the string literal `Y` or `N`, and revalidate. |
| A create-together source lacks a matching AnalysisGroupCode in its parent and child rows, or the live template rejects code-based linkage | Stop before import. Correct the code linkage when supported; otherwise use the master-first fallback, resolve the master by exact AnalysisGroupCode, and prepare a separate parent-plus-children source. |
| A child source for an existing master has no resolved AnalysisGroupId, or the source lacks the matching parent row | Stop before Data Loader artifact preparation. Resolve the master by exact AnalysisGroupCode; then populate the same parent ID in one parent row and every child row. |
| `RestAction: CREATE` is supplied for `costAccountingCostAnalysisCodes` | Stop and remove CREATE. Fusion does not support CREATE for this Data Loader child section; retain blank child RestAction and submit the parent-plus-children archive. |
| A parent lookup returns no matching group, multiple groups, or no analysisGroupId | Stop before child creation and ask the functional user to verify the AnalysisGroupCode. |
| An analysis code is duplicated within the same analysis group | Stop and make the child analysis codes unique within the group. |
| The resulting child-code set for an AnalysisGroupCode has no default analysis code or more than one default analysis code | Stop and correct the combined existing and proposed child records so exactly one record has DefaultAnalysisCodeFlag set to Y. |
| A child-only addition cannot retrieve every existing child for the AnalysisGroupCode | Stop before Data Loader artifact preparation; resolve the read-only child lookup and retry validation. |
| An update or delete source lacks a resolved existing record or a key field required by the live Data Loader template | Stop before preview; retrieve the live update/delete sample and resolve the exact target record. |
| The live Data Loader template or validation rejects the requested update/delete action for the master or detail section | Stop and record an unsupported-operation diagnostic; do not substitute direct REST. |
| A request changes AnalysisGroupCode, AnalysisCode, or AnalysisGroupId as though it were an update | Stop and redesign it as a reviewed delete-and-create change. |
| A detail deletion would leave no default analysis code or more than one default analysis code | Stop and correct the complete resulting child-code set before preparing the source. |
| A master deletion has remaining child rows, dependent references, or incomplete dependency lookup results | Stop before preview; do not assume cascade deletion. |
| A delete is requested without an immutable approval preview and later explicit approval | Stop before the first POST. |
| Data Loader source or `costAccountingCostAnalysisGroups` business-object validation fails | Stop before preview, correct the source data, and revalidate through `core.data-loader`. |
| Upload or initiation is requested without an immutable approval preview and later standalone approval | Stop before the first POST. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required group or child analysis-code value is missing or malformed | Correct the source data and revalidate. |
| Reference lookup | Parent lookup cannot resolve exactly one nonblank analysisGroupId, or a child row is unlinked | Correct the group code or parent lookup result and revalidate before preparing children. |
| Design enforcement | A child analysis code is duplicated in its group, or the combined child-code set has zero or more than one default | Correct the analysis-code design and revalidate. |
| Reference lookup | A child-only addition cannot resolve the existing children for the AnalysisGroupCode | Retrieve the complete child set for the resolved parent before revalidating. |
| Data Loader validation | The source or registered business object does not pass Data Loader validation | Correct the source and generate a new immutable approval preview. |
| Destructive-operation blocker | A delete has unresolved children/dependencies, incomplete validation, or no current explicit approval | Resolve the blocker and produce a fresh immutable preview. |
| Approval blocker | Upload or initiation is requested without current approval for the exact immutable source | Stop before upload and obtain the required approval. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input or design failure | The affected analysis group or analysis code and the corrective action. |
| Data Loader validation failure | The affected source-data validation result and corrective action. |
| Data Loader approval gate | The immutable preview and the required standalone approval action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing, invalid, or noncompliant design input | Do not infer an analysis group code, analysis code, or default-code selection. |
| Data Loader validation or approval gate is incomplete | Do not upload, initiate, retry, or construct a direct REST request. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAG.HANDLE_ISSUE | step | 4 | error_handler | disclosed->RETURN_ISSUES | none | stop | A prior node reports invalid or blocked input, lookup, or design. |
| CAG.DONE_REVIEW | terminal | 5 | terminal | none | CAG.ENFORCE_DESIGN | stop | Input, parent resolution, and analysis-code design review are complete. |
| RETURN_ISSUES | terminal | 6 | terminal | none | none | stop | Error disclosure is complete. |
