# Time Consumer Sets Defaulting Rules

## Source Basis

- Time Consumer Sets authoring pack: 01-functional-specification.md, 02-ui-rest-field-mapping.md, and 06-rest-describe-evidence.md.
- Developer-provided Time Consumer ID mapping: Payroll = 300100028310506; Project Costing = 300100028310502.
- Developer-provided business-only Complete Summary requirements, 2026-09-09.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ApprovalWorkflowForWorkersFlag | false | A new UI-backed create request is initialized and no value is supplied | No; preserve an explicitly supplied supported Boolean |  |
| EntryLevelApprovalFlag | false | A selected consumer configuration is initialized and no value is supplied | No; preserve an explicitly supplied Boolean |  |
| AbsenceApprovalRoutingCode | ORA_TL_APPRVL_RULES | Server-side Describe default only; the UI still requires an explicit routing selection | Do not override a user selection |  |
| Description | No default | Description is omitted | No |  |
| TimeConsumerId | 300100028310502 | A Project Costing configuration is initialized | No; apply the supplied Project Costing Time Consumer ID |  |
| TimeConsumerId | 300100028310506 | A Payroll configuration is initialized | No; apply the supplied Payroll Time Consumer ID |  |

## Defaulting Boundaries

| Situation | What Happens |
|---|---|
| Project Costing is selected | Initialize only the Project Costing configuration with TimeConsumerCode PJC and TimeConsumerId 300100028310502; do not create an unselected configuration. |
| Payroll is selected | Initialize only the Payroll configuration with TimeConsumerCode PYR and TimeConsumerId 300100028310506; do not create an unselected configuration. |
| A Time Category is absent | Do not default it. The visible selected-consumer section requires a resolved Time Category. |
| A UI request omits ApprovalWorkflowForWorkersFlag | Apply false before request shaping because the parent attribute is input required by live Describe. Retain it internally and never display it as Worker approval in a Complete Summary. |
| A routing value is supplied | Preserve the selected documented routing code; do not replace it with the server default. |

## Complete Summary Default Presentation

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Applied defaults | Include every user-facing default that was actually applied in the Defaults Applied section, using its business label and verified business display value | A Complete Summary is generated | No | |
| ApprovalWorkflowForWorkersFlag | Retain false for loader execution but omit it from the Complete Summary and Defaults Applied | A Complete Summary is generated | No | |
| Boolean display | Use Selected or Not selected, Enabled or Disabled, or Yes or No when a verified business label is available | A populated boolean is shown in the Complete Summary | No | |
| Status display | Use a verified business-friendly status such as Draft or Submitted | A populated internal status is shown in the Complete Summary | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCS.APPLY_DEFAULTS | step | 40 | apply_default | applied->TCS.ENFORCE_DESIGN;not_applicable->TCS.ENFORCE_DESIGN;blocked->TCS.HANDLE_ERROR | TCS.RESOLVE_TIME_CATEGORIES | stop | A request has passed input and dependency validation |
