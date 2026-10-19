# Learning configuration dependency readiness

Sources: FDD GB-09, taxonomy foundation map and D1–D7. Resolver mechanics live
only in ora_reference_lookups.md. Evaluate applicable prerequisites, not every
foundation for every request. No cross-task graph edges or implicit creation.

## Required Dependency Order

| Task Code | Task Name | Sequence | Dependency | What Must Happen |
|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | 1 | Selected task prerequisites | Resolve applicable same-task evidence before defaulting/design review; return conditional handoffs to orchestration |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | 1 | Selected task prerequisites | Resolve applicable same-task evidence before defaulting/design review; return conditional handoffs to orchestration |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | read_learning_defaults | Current configuration | Yes | Selected defaults review | Verify | TBD: authoritative provider evidence binding | read_learning_defaults | Establish the selected prerequisite without assumed readiness | Provide unresolved business identity/decision; implementation owner resolves the provider contract | TBD: normalized prerequisite evidence |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | find_learning_evaluation_questionnaire | Evaluation questionnaire | Conditional | Evaluation selected | Verify | TBD: authoritative provider evidence binding | find_learning_evaluation_questionnaire | Establish the selected prerequisite without assumed readiness | Provide unresolved business identity/decision; implementation owner resolves the provider contract | TBD: normalized prerequisite evidence |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | find_learning_certificate_template | Certificate template | Conditional | Certificate selected | Verify | TBD: authoritative provider evidence binding | find_learning_certificate_template | Establish the selected prerequisite without assumed readiness | Provide unresolved business identity/decision; implementation owner resolves the provider contract | TBD: normalized prerequisite evidence |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | verify_learning_attendance_dependencies | Virtual attendance readiness | Conditional | Virtual attendance selected | Verify | TBD: authoritative provider evidence binding | verify_learning_attendance_dependencies | Establish the selected prerequisite without assumed readiness | Provide unresolved business identity/decision; implementation owner resolves the provider contract | TBD: normalized prerequisite evidence |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | verify_learning_notification_dependencies | Notification configuration readiness | Conditional | Conversation, template or alert selected | Verify | TBD: authoritative provider evidence binding | verify_learning_notification_dependencies | Establish the selected prerequisite without assumed readiness | Provide unresolved business identity/decision; implementation owner resolves the provider contract | TBD: normalized prerequisite evidence |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | read_learning_processing_defaults | Current configuration | Yes | Processing review | Verify | TBD: authoritative provider evidence binding | read_learning_processing_defaults | Establish the selected prerequisite without assumed readiness | Provide unresolved business identity/decision; implementation owner resolves the provider contract | TBD: normalized prerequisite evidence |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | find_learning_processing_schedule | Processing schedule | Conditional | Immediate processing disabled or scheduling requested | Verify | TBD: authoritative provider evidence binding | find_learning_processing_schedule | Establish the selected prerequisite without assumed readiness | Provide unresolved business identity/decision; implementation owner resolves the provider contract | TBD: normalized prerequisite evidence |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | verify_learning_execution_user | Execution user | Conditional | Run-as override requested | Verify | TBD: authoritative provider evidence binding | verify_learning_execution_user | Establish the selected prerequisite without assumed readiness | Provide unresolved business identity/decision; implementation owner resolves the provider contract | TBD: normalized prerequisite evidence |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Verify | Applicable prerequisite needs authoritative evidence | Only a completed declared read contract; no creation |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Blocked | Required contract/evidence unresolved | No affected execution; independent planning continues |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Not Applicable | Business condition not selected | No; retain rationale in inventory |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Verify | Applicable prerequisite needs authoritative evidence | Only a completed declared read contract; no creation |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Blocked | Required contract/evidence unresolved | No affected execution; independent planning continues |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Not Applicable | Business condition not selected | No; retain rationale in inventory |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | LC.DEFAULTS.DEPENDENCY | step | 3 | resolve_dependency | pass->LC.DEFAULTS.DEFAULT;fail->RETURN_ISSUES | LC.DEFAULTS.LOOKUP | stop | Selected task; unresolved authority or contract prevents executable readiness |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | LC.BACKGROUND.DEPENDENCY | step | 3 | resolve_dependency | pass->LC.BACKGROUND.DEFAULT;fail->RETURN_ISSUES | LC.BACKGROUND.LOOKUP | stop | Selected task; unresolved authority or contract prevents executable readiness |
