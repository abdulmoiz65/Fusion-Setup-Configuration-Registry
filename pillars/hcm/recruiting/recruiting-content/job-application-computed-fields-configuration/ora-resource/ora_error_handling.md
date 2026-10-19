# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Input, EFF, formula, or mapping validation fails | Explain the invalid mapping and corrective business step; do not build an import artifact. |
| Existing mappings are present | Stop, instruct manual deletion in the Job Application Computed Fields Configuration FSM task, wait for confirmation, then re-export. |
| Task Hook validation fails | Return the user-friendly validation findings without an approval request. |
| Import outcome is uncertain | Stop and preserve sanitized diagnostics; do not retry or submit a replacement. |
| Import reports success but verification export differs | Record a sanitized verification discrepancy and stop without retry. |
| Import status is still running | Poll Core Data Loader only when the user requested status or completion monitoring; do not claim completion. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Mapping summary | One row per mapping with Context, Segment, Formula, and Base formula name; omit FormulaCode, FormulaFormulaTypeId, and FormulaBaseFormulaTypeName unless technical traceability is requested. |
| Final immutable preview | Target environment, current-state export, EFF eligibility, formula eligibility, one-to-one validation, impact, unchanged values, ZIP filename, SHA-256, verification plan, Task Hook results, envelope readiness, and approval fingerprint. |
| Approval | Request one concise approval tied to the exact immutable ZIP filename and checksum immediately before submission. |
| Post-import completion | Preserve Core Data Loader status output unchanged, then use the required completion display only after a fresh export exactly matches all approved rows. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Existing mapping rows | Do not create or submit another archive; the import is create-only for a clean target. |
| Fast Formula identity | Do not export Fast Formulas, use Formula Text, call direct REST, or use display type as FormulaBaseFormulaTypeName. |
| Approval is stale or absent | Do not upload or initiate; any archive change requires fresh Task Hook validation and approval. |
| Import or verification is uncertain | Do not retry automatically. |
| User approved the exact ZIP | Verify the approved task-validation envelope without changing the ZIP, submit the exact envelope and ZIP once through Core Data Loader, and continue to verification without another routine question. |

## Required Post-Completion Display

Use only after Fusion reports success and a fresh task export exactly matches the complete approved mapping set:

## Job Application Computed Fields Configuration — Completed

The requested mappings were imported and verified.

| Context | Segment code | Fast Formula |
|---|---|---|
| `<FlexContextCode>` | `<FlexSegmentCode>` | `<FormulaBaseFormulaName>` |

| Verification | Result |
|---|---|
| Import status | Succeeded |
| Imported mappings | `<verified count>` of `<requested count>` verified |
| Post-import export | Exact match with the approved mapping set |
| Formula identity | Validated base formula name, Formula ID, Formula Type ID, and `IRC_JA_COMPUTED_FIELD` |

Include a link to the fresh verification export.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JACF.TASK_HOOK_PREVIEW | decision | 8 | execution_gate | ready->JACF.READY_FOR_APPROVAL;issues->JACF.TASK_HOOK_ISSUES | JACF.BUILD_ARTIFACT | stop | Exact immutable ZIP is ready for Task Hook validation |
| JACF.INPUT_ISSUES | step | 9 | error_handler | disclosed->RETURN_ISSUES | none | stop | Business intake is incomplete or ambiguous |
| JACF.DEPENDENCY_ISSUES | step | 10 | error_handler | disclosed->RETURN_ISSUES | none | stop | EFF, formula, or export dependency fails |
| JACF.MAPPING_ISSUES | step | 11 | error_handler | disclosed->RETURN_ISSUES | none | stop | Mapping validation fails |
| JACF.MANUAL_CLEANUP | step | 12 | error_handler | disclosed->RETURN_ISSUES | none | stop | Current baseline contains mapping rows |
| JACF.ARTIFACT_ISSUES | step | 13 | error_handler | disclosed->RETURN_ISSUES | none | stop | Immutable archive validation fails |
| JACF.TASK_HOOK_ISSUES | step | 14 | error_handler | disclosed->RETURN_ISSUES | none | stop | Core Data Loader Task Hook validation fails |
| JACF.DONE_REVIEW | terminal | 15 | terminal | none | JACF.FORMAT_REVIEW | stop | Requested review is complete |
| JACF.READY_FOR_APPROVAL | terminal | 16 | terminal | none | JACF.TASK_HOOK_PREVIEW | stop | Exact Task Hook-validated archive is ready for one approval-bound Core Data Loader submission |
| RETURN_ISSUES | terminal | 17 | terminal | none | none | stop | Blocking issue is disclosed |
