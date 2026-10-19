# Performance Document Types Design Enforcement

Source: Oracle Fusion Cloud Talent Management, Overview of Performance Document Types.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Define validity | Configure a document type name, optional description, From Date, To Date, and status. |
| 2 | Cover template dates | Ensure the document type date range contains the date range of every performance template that will use it. |
| 3 | Enable availability | Set status to Active before using the document type in performance templates or performance goal plans. |
| 4 | Configure template use | Select the document type on the General tab of every performance template. |
| 5 | Configure interim evaluations | Select at least one document type and applicable review periods on the Document Periods tab when interim evaluations are used. |
| 6 | Configure goal-plan use | Associate the document type with each applicable goal plan and review period. |
| 7 | Preserve in-use availability | Do not set a document type to Inactive after it is used by a performance template or goal plan. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A document type is used in a performance template | Blocker | | The document type From Date is after the template From Date, or its To Date is before the template To Date. | Align the document type dates so they contain the template date range. | Yes |
| A document type must be available in a performance template or performance goal plan | Blocker | | Status is not Active. | Set the status to Active. | Yes |
| A performance template is created or updated | Blocker | | No performance document type is selected on the template General tab. | Select the applicable document type. | Yes |
| A performance template uses interim evaluations | Blocker | | No document type is associated with the document period. | Associate at least one document type and applicable review periods on the Document Periods tab. | Yes |
| A goal plan must be available in performance documents | Blocker | | The goal plan has no associated document type. | Associate the applicable document type and review period with the goal plan. | Yes |
| A document type already used by a template or goal plan is changed | Blocker | | A request sets its status to Inactive. | Retain Active status. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_DOCUMENT_TYPES.ENFORCE | decision | 50 | design_enforcement | passed->PERFORMANCE_DOCUMENT_TYPES.EXECUTION_CONTRACT;blocked->PERFORMANCE_DOCUMENT_TYPES.STOP_DESIGN | PERFORMANCE_DOCUMENT_TYPES.DEFAULTS | stop | A Performance Document Type requires documented design checks. |
