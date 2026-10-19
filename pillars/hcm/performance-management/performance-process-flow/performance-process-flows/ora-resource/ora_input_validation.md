# Performance Process Flows Input Validation

Apply this task guidance using current target metadata and the declared execution route.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Create identity | Name and DateFrom | Stop before POST | Supply Name of 240 characters or fewer and DateFrom. | Create | |
| Effective period | DateFrom and optional DateTo | Stop before POST or PATCH | Supply a date range where DateFrom is not after DateTo. | Create or update | |
| Writable root payload | Name, Description, DateFrom, DateTo, Status, and published boolean flags | Stop before POST or PATCH | Remove hidden, derived, key, and child-collection values. | Create or update | |
| Update identity | ProcessFlowId | Stop before PATCH | Supply the existing ProcessFlowId and read the current resource first. | Update | get_performance_process_flow_by_id |
| Redwood calendar invitations | CalendarInviteFlag plus its required parent and Redwood feature state | Stop before POST or PATCH | Provide the required parent flag and resolve the Redwood feature applicability. | CalendarInviteFlag is true | resolve_redwood_performance_documents_feature |
| Compensation calibration sharing | AllowShareLockForCalib plus its required parent and compensation-calibration feature state | Stop before POST or PATCH | Provide the required parent flag and resolve the compensation-calibration feature applicability. | AllowShareLockForCalib is true | resolve_compensation_calibration_feature |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An update targets an existing flow | Verify | Read its current state, including InUseFlag, before deciding whether the requested change is permitted. | get_performance_process_flow_by_id |
| A flow is created or updated in template context | Verify | Require the flow period to cover the template period; for inline creation, DateFrom cannot be later than the template DateFrom. | |
| Status is supplied | Verify | Accept only an ACTIVE_INACTIVE code. | |
| A task definition is required | Blocked | Do not send taskNames through the REST root; the child collection is read-only in this REST contract. | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name | Require a nonempty value of at most 240 characters. | Create or Name update | |
| Description | Accept an optional value of at most 4000 characters. | Description is supplied | |
| Date range | Require DateFrom less than or equal to DateTo when DateTo is supplied. | Create or update | |
| Status | Accept an ACTIVE_INACTIVE code, not StatusMeaning. | Status is supplied | |
| Boolean flags | Accept only REST boolean semantics for published Y/N-backed flags. | A published flag is supplied | |
| Document acknowledgement versus review meetings | Treat WkrAckDocFlag as the acknowledgement of a shared document only. Do not set ConductMeetingsFlag or WkrAckReviewMtgFlag to Y unless the user explicitly requests the corresponding review-meeting behavior. | WkrAckDocFlag is Y or a review-meeting flag is supplied | |
| FSM CSV escaping | When creating or regenerating a CSV member, write headers and ordinary values without double quotes. Add double quotes only for an individual value containing a comma, double quote, carriage return, or line feed; double embedded quotes. Reject blanket-quoted CSV members. | FSM CSV import is prepared or revalidated | |
| Server-managed fields | Reject BusinessGroupId, ObjectVersionNumber, StatusMeaning, InUseFlag, and generated ProcessFlowId as ordinary client values. | Create or update | |
| Unsupported fields | Reject PreliminaryRatingsFlag, ParticipantEvalFlag, manager or worker assignment-completion flags, FirstApprovalId, and SecondApprovalId when their documented fixed values are violated. | Create or update | |
| Final feedback parent flag | Require FinalFeedbackFlag to be N. Worker and manager final-feedback behavior is represented by WkrFinalFeedbckFlag and MgrFinalFeedbackFlag; FinalFeedbackFlag must not be set to Y. | Create or update | |
| Conditional process-flow flags | Apply the documented conditional defaults, then reject an explicit Y value that violates its parent condition: manager evaluation, criteria confirmation/preparation, participant assignment/selection/tracking, sharing, meetings, or first approval. When `ConfirmCriteriaFlag=Y`, require at least one manager or worker set flag and one manager or worker complete flag to be Y. When `AssignParticipantsFlag=Y`, require manager or worker tracking to be Y. | Create or update | |
| REST child collection | Reject taskNames in POST or PATCH. | Create or update | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_PROCESS_FLOWS.VALIDATE | decision | 10 | validate_input | valid->PERFORMANCE_PROCESS_FLOWS.APPLY_DEFAULTS;invalid->PERFORMANCE_PROCESS_FLOWS.STOP_INVALID | none | stop | A REST create or update request is prepared. |
