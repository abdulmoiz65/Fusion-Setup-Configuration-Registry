# Performance Process Flows Design Enforcement

Apply this task guidance using current target metadata and the declared execution route.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce immutable and derived values | Do not write read-only, hidden, generated, or unsupported values. |
| 2 | Enforce effective dates and duplicate identity | Require a valid date range and reject a same-name, same-business-group flow with overlapping dates. |
| 3 | Enforce evaluation and approval dependencies | Validate criteria, concurrent evaluation, manager evaluation, first/second approval, and auto-submit combinations. |
| 4 | Enforce sharing, meeting, feedback, and participant dependencies | Validate each enabled child flag against its documented parent and feature condition. |
| 5 | Enforce dependent-field invariants | Re-evaluate every applicable conditional flag relationship after normalization. A bypass request or residual contradiction blocks the run. |
| 6 | Enforce child route | Do not write taskNames with REST; route task-role changes to its documented SOAP or migration service. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every REST request | Blocker | | It includes taskNames, an EFF/DFF collection, BusinessGroupId, ObjectVersionNumber, StatusMeaning, InUseFlag, or a DELETE operation. | Use only documented writable root fields; use a separate documented route for task roles. | Yes |
| Criteria flags are supplied | Blocker | | `ConfirmCriteriaFlag=N` while any manager or worker criteria-set/complete flag is Y; `MgrCmpltEvalCrtriaFlag=Y` while `MgrSetEvalCrtriaFlag=N`; `WkrCmpltEvalCrtriaFlag=Y` while `WkrSetEvalCrtriaFlag=N`; or `ConfirmCriteriaFlag=Y` without at least one of the manager or worker set flags and at least one of the manager or worker complete flags set to Y. | Correct the criteria flag combination. | Yes |
| EvalTasksConcurrentFlag is true | Blocker | | `WkrSelfEvalFlag` and `MgrEvalOfWrkrFlag` are not both Y, or a nonexempt task falls between worker and manager evaluation. | Enable both evaluations and correct task order. | Yes |
| Approval flags are supplied | Blocker | | `SecondApprovalFlag=Y` while `FirstApprovalFlag=N`, or `AutoSubmitApprovalFlag=Y` while `FirstApprovalFlag=N` or `MgrEvalOfWrkrFlag=N`. | Correct the parent approval and manager-evaluation choices. | Yes |
| Sharing or review-meeting flags are supplied | Blocker | | `SharePerformanceDocFlag=Y` while `MgrEvalOfWrkrFlag=N`; `WkrAckDocFlag=Y` while sharing is N; `WkrAckReviewMtgFlag=Y` while meetings are N; `AllowShareLockForCalib=Y` while sharing is N; or `DisableResubmitMgrEval=Y` or `IncludeTalentReviewCalibFlag=Y` while manager evaluation is N. | Enable the parent or clear the child. | Yes |
| HidePdFrWkrBfrShareFlag is Y | Blocker | | The employee-evaluation task SequenceNumber is not greater than the manager-share-performance-document task SequenceNumber. | Place the manager-share-performance-document task before the employee-evaluation task, then rebuild and validate the task-role CSV rows. | Yes |
| Final feedback flags are supplied | Blocker | | FinalFeedbackFlag is not N. | Set FinalFeedbackFlag to N; represent requested worker and manager final feedback with WkrFinalFeedbckFlag and MgrFinalFeedbackFlag. | Yes |
| Participant feedback flags are supplied | Blocker | | `AssignParticipantsFlag=N` while any manager or worker participant selection, tracking, request, or participant-reopen flag is Y; `MgrAddQuestionFlag=Y` while `MgrSelectPcpnsFlag=N`; `WrkAddQuestionFlag=Y` while `WrkSelectPcpnsFlag=N`; `MgrReopenPcpnFdbckFlag=Y` while `MgrTrackPcpnsFlag=N`; `WrkReopenPcpnFdbckFlag=Y` while `WrkTrackPcpnsFlag=N`; or `AssignParticipantsFlag=Y` without at least one of `MgrTrackPcpnsFlag` or `WrkTrackPcpnsFlag` set to Y. | Correct the participant-feedback combination. | Yes |
| Any documented conditional flag relationship applies | Blocker | | The normalized payload retains a contradictory dependent value, or a request asks to bypass the relationship. | Apply the documented reset and re-evaluate all applicable relationships. If any contradiction remains, stop before preview, approval, import, or mutation; no request or approval can waive it. | Yes, only by making the payload compliant |
| An in-use flow is updated | Blocker | get_performance_process_flow_by_id | The update changes DateFrom or a guarded configuration value. | Preserve the guarded state unless a separately approved service contract permits the change. | No |
| CalendarInviteFlag is true | Blocker | resolve_redwood_performance_documents_feature | ORA_HRA_PERFORMANCE_DOCUMENTS_AND_GOALS_REDWOOD_ENABLED does not resolve to Y. | Clear CalendarInviteFlag or enable the Redwood performance-documents feature. | Yes |
| AllowShareLockForCalib is true | Blocker | resolve_compensation_calibration_feature | ORA_HRA_COMP_CALIBRATION_STATUS_ENABLED does not resolve to Y. | Clear AllowShareLockForCalib or enable the compensation-calibration feature. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| get_performance_process_flow_by_id | An existing flow is updated. | InUseFlag, current dates, Status, and current flags. | ora_reference_lookups.md |
| resolve_redwood_performance_documents_feature | CalendarInviteFlag is true. | ProfileOptionValue = Y for ORA_HRA_PERFORMANCE_DOCUMENTS_AND_GOALS_REDWOOD_ENABLED. | ora_reference_lookups.md |
| resolve_compensation_calibration_feature | AllowShareLockForCalib is true. | ProfileOptionValue = Y for ORA_HRA_COMP_CALIBRATION_STATUS_ENABLED. | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_PROCESS_FLOWS.ENFORCE_DEPENDENT_FIELD_INVARIANTS | decision | 50 | design_enforcement | passed->PERFORMANCE_PROCESS_FLOWS.ENFORCE;blocked->PERFORMANCE_PROCESS_FLOWS.STOP_DESIGN | PERFORMANCE_PROCESS_FLOWS.REFERENCE_LOOKUPS | stop | Every applicable conditional flag relationship is normalized and compliant. |
| PERFORMANCE_PROCESS_FLOWS.ENFORCE | decision | 60 | design_enforcement | passed->PERFORMANCE_PROCESS_FLOWS.DONE;blocked->PERFORMANCE_PROCESS_FLOWS.STOP_DESIGN | PERFORMANCE_PROCESS_FLOWS.ENFORCE_DEPENDENT_FIELD_INVARIANTS | stop | The REST request must satisfy the documented design constraints. |
