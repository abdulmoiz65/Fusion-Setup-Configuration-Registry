# Repeating Time Periods Error Handling

## Source Basis

- Repeating Time Period UI Skeleton, developer-provided text file, used only for UI field validation.
- Generic FSM Baseline, developer-provided text, used only for FSM CSV flow, safety, and failure rules.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required field or conditional field is missing | Stop and identify the missing field group required for the selected Period Type and Period Length |
| A selected value is outside the UI skeleton's allowed choices | Stop and present only the supported choices documented in the skeleton |
| The remaining parent CSV contract is absent | Keep the task incomplete; do not prepare or submit an FSM ZIP until create or edit key behavior, unselected-usage representation, and unsupported parent period-definition cases are documented |
| A validation result cannot be classified by the documented UI skeleton | Stop rather than infer a field rule, lookup, default, or execution behavior |
| A create derives a PeriodCd that already exists in the fresh same-task export | Stop before preview and require a Name that derives a distinct PeriodCd |
| Current Name is missing, absent from the fresh export, or matches multiple exported rows | Stop before preview and require one exact existing Repeating Time Period Current Name |
| An edit changes a field other than Name or Description, or changes PeriodCd or GroupingKey | Stop and rebuild from the matched fresh-export rows with only Name and/or Description changed |
| A fresh same-task export cannot be obtained or validated | Stop and do not prepare an FSM package |
| The FSM payload includes a Repeating Time Period outside the requested create or update scope, or does not support every task-scoped CSV member in the fresh export | Stop and rebuild a delta-only package containing only the requested rows in every exported task-scoped CSV member |
| FSM evidence does not prove the expected import route | Stop and rebuild the package from the fresh same-task export |
| One or more exact functional matches exist and the user has not explicitly confirmed a new period | Show every matching period using populated UI-exposed values only and stop before package creation |
| The Complete Summary cannot be generated solely from verified structured UI fields, omits a populated UI value or applied default, includes a non-UI or technical value, or includes an empty child section | Stop before the provider-owned approval process and regenerate the required business-only summary |
| Immutable preview or approval evidence is missing or stale | Stop before submission |
| Import fails, partially succeeds, times out, or is uncertain | Preserve diagnostics, reconcile current state, and stop without automatic retry |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| INPUT_VALIDATION | Required, conditional, or enumerated field validation fails | Correct the affected input and validate again |
| AUTHORING_GAP | Remaining parent CSV operation details are absent | Supply the missing parent CSV contract before execution planning |
| FSM_EVIDENCE | Fresh export, archive, preview, or approval evidence is absent or invalid | Rebuild or revalidate the required artifact and stop before import |
| FUNCTIONAL_MATCH_DECISION | Exact functional matches exist but the required create decision is missing or declined | Show all matches and stop unless the user explicitly confirms creation of a new period |
| SUMMARY_DISCLOSURE | The business-only Complete Summary is missing, incomplete, unverified, or contains a prohibited non-UI or technical value | Regenerate the summary from verified structured UI fields and stop before provider-owned approval |
| PROCESS_FAILED | Import fails, partially succeeds, times out, or is uncertain | Preserve diagnostics, reconcile current state, and stop without retry |
| UNSUPPORTED | The requested behavior is not described by the UI skeleton | Provide an authoritative source for the requested behavior |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Task-specific FSM details are absent | Do not infer object CSV members beyond the export evidence, create or edit key behavior, relationships, or CSV representations of defaults and LOV selections |
| Validation fails | Do not preview, import, or execute a repeating time period configuration |
| The Complete Summary fails its business-only requirements | Do not continue to the provider-owned approval process or change provider execution ownership |
| Functional matches are found | Do not create a new period unless every match has been shown and the user explicitly confirms creation |
| Import is failed, partial, timed out, or uncertain | Do not automatically retry the import |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RTP.FSM_EXECUTION_GATE | decision | 60 | execution_gate | ready->RTP.READY;blocked->RTP.BLOCKED | RTP.GENERATE_COMPLETE_SUMMARY | stop | After the required Complete Summary, before calling core.data-loader: require the fresh export, validated FSM ZIP, current immutable preview, explicit provider-owned approval, one import, and reconciliation through the documented task read or export path |
| RTP.READY | terminal | 70 | terminal | none | RTP.FSM_EXECUTION_GATE | stop | The declared FSM gate is satisfied and the task is ready for the authorized core.data-loader route |
| RTP.CREATE_CANCELLED | terminal | 75 | terminal | none | RTP.CONFIRM_CREATE_AFTER_MATCHES | stop | The user declined creation after every exact functional match was shown |
| RTP.BLOCKED | terminal | 80 | terminal | none | none | stop | A required input, FSM evidence, or task-specific contract is invalid, missing, or incomplete |
