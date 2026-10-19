# Schedule and Shift Options Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Initial scheduleCommonSetups response is unsuccessful or lacks items | Stop and report the read failure; do not infer a current setup-option row. |
| Item update returns errorDetails | Show the returned detail strings after removing trailing parenthesized text where present. |
| Item update returns another error body | Show the returned error body through the approved executor diagnostics. |
| Common Lookup provider returns a gap, no match, or ambiguity | Stop before preview or write handoff and show the provider evidence. |
| Complete Summary cannot be generated only from verified structured values | Stop before the provider-owned approval process; do not add a warning, diagnostic, technical note, placeholder, or unverified substitute to the summary. |
| A save outcome is uncertain | Do not retry automatically; verify through the selected read-only status or lookup workflow. |
| A Data Loader status request succeeds | Show the standard successful status result followed by the verified, approved Complete Summary for the exact submitted change. Do not regenerate, infer, or add values that were not part of the approved change. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required value, range, timing pair, or selection is invalid | Correct the stated field and restart validation. |
| Lookup provider | A required provider request returns a gap, is unavailable, or is ambiguous | Resolve the provider gap or select one exact provider result. |
| Fusion API | A documented read or update response fails | Show redacted diagnostics and follow the executor's next action. |
| Approval blocker | Preview or current approval is absent | Prepare the required preview and obtain approval before mutation. |
| Complete Summary | A required business value or actually applied default is not verified, or the formatted summary is not business-only | Correct the verified structured values and regenerate the summary before provider-owned approval. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before a mutation | Exact setup-option identity, normalized ParameterValue, expected update effect, target environment, and current approval requirement. |
| After a failed operation | Failure class, sanitized provider diagnostics, whether any effect is uncertain, and one safe next action. |
| After a successful Data Loader status result | Show the standard successful status result and the business-only Complete Summary retained from the exact approved change. Omit the summary when the load is in progress, failed, unknown, or has errors. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A direct REST write is requested from this resource guidance | Do not submit the write; hand off to the authorized execution workflow. |
| A write outcome is uncertain | Do not replay the update automatically. |
| Common Lookup resolution is required | Do not call a physical endpoint from this consumer; delegate to hcm.workforce-scheduling-management.workforce-scheduling-common.manage-common-lookups with its documented lookupType. |
| Complete Summary is absent or incomplete | Do not begin the provider-owned approval process. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SSO.EXECUTION_GATE | step | 9 | execution_gate | handed_off->SSO.DONE;blocked->SSO.ERROR | SSO.COMPLETE_SUMMARY | stop | Hand off the completed summary to the unchanged provider-owned approval process; do not collect, decide, or execute approval in this task |
| SSO.ERROR | terminal | 10 | terminal | none | none | stop | Any failed, blocked, unresolved, invalid, or summary-sanitization outcome |
| SSO.DONE | terminal | 11 | terminal | none | SSO.EXECUTION_GATE | stop | Complete Summary generated and handed to the unchanged provider-owned approval process |
