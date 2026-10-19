# Time Categories Defaulting Rules

## Source Basis

- Developer-provided Time Categories UI structure and task behavior, 2026-09-08.
- Developer-provided Time Categories FSM authoring input, 2026-09-08.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Track Usage | No | Create omits Track Usage | Yes | |
| Unit of Measure | Blank | Create omits Unit of Measure | Yes | |

## Preservation and Edit Rules

| Situation | What Happens |
|---|---|
| An edit omits an editable value | Preserve the fresh exported value; omission is not a request to clear it. |
| Name is changed during edit | Allow the change only when the resulting Name remains unique. |
| Track Usage is changed during edit | Block the change; Track Usage is immutable after creation. |
| Unit of Measure is changed during edit | Allow the change. |
| Rule Name is removed during edit | Allow the Rule Name to be cleared. |
| Category Conditions are edited | Preserve row order and balanced parenthesis grouping unless the approved change changes them. |

## Complete Summary Default Presentation

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Applied defaults | Include every default that was actually applied in the Defaults Applied section, using its business label and verified business display value | A Complete Summary is generated | No | |
| Boolean display | Use Selected or Not selected, Enabled or Disabled, or Yes or No when a verified business label is available | A populated boolean is shown in the Complete Summary | No | |
| Status display | Use a verified business-friendly status such as Draft or Submitted | A populated internal status is shown in the Complete Summary | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TC.DEFAULTS | step | 40 | apply_default | applied->TC.ENFORCE;preserved->TC.ENFORCE;not_applicable->TC.ENFORCE;blocked->TC.ERROR | TC.RESOLVE_TIME_ATTRIBUTE | stop | Dependency, package-verification, and Time Attribute resolution gates have passed |
