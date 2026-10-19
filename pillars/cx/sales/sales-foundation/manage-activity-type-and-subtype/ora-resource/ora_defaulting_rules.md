# Defaulting Rules

Apply the lookup-type tag default only when creating a new activity type for all three supplied activity functions. The documented tag makes the type available for Appointment, Task, and Call Report activity use.

Source: [About Activity Type and Subtype](https://docs.oracle.com/en/cloud/saas/sales/oasal/about-activity-type-and-subtype.html).

## Defaults

| Business Value | Default | Applies When | Can User Override? | Why This Default Is Safe |
|---|---|---|---|---|
| lookup_type_tag | APPOINTMENT:TASK:CALLREPORT | change_mode is create, all three supplied activity functions are selected, and no tag was supplied | No | Oracle requires this tag for a new lookup type that is used by all three supplied activity functions. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY.DEFAULT_TAG | step | 2 | apply_default | defaulted->ACTIVITY.DEPENDENCY;not_applicable->ACTIVITY.DEPENDENCY;invalid->ACTIVITY.BLOCKED | ACTIVITY.VALIDATE | stop | Before resolving existing relationships or preparing a new activity type. |
