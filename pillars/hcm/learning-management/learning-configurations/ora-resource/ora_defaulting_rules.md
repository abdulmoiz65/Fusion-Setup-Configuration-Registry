# Learning configuration defaulting

Sources: FDD GB-07/08 and Oracle D7. Delivered defaults are documentation,
never a pod baseline. Recommendations are separate design rules. Do not
apply a value automatically or override a valid user choice. The future
provider must bind each named business setting to its actual field.

## Standard Defaults

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Unspecified optional decision | Retain verified current value; mark Deferred; no fabricated value if unknown | Optional decision unresolved | No | read_learning_defaults |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Evaluation, enrollment, certificates, attendance, conversations, templates, alerts | No universal default; TBD: provider field/value and current-state binding | Selected business setting not confirmed | No | read_learning_defaults |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Four concurrency settings for Assignments, Recommendations and Access | Delivered: 1 each | D7 reference only; actual field mapping TBD | No | read_learning_processing_defaults |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Immediate processing after save | Delivered: selected | D7 reference only; actual field mapping TBD | No | read_learning_processing_defaults |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Execution identity | Delivered: creator | D7 reference only; actual field mapping TBD | No | read_learning_processing_defaults |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Other unspecified setting | Retain verified current value; otherwise unknown and Deferred | No explicit change decision | No | read_learning_processing_defaults |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | LC.DEFAULTS.DEFAULT | step | 4 | apply_default | pass->LC.DEFAULTS.DESIGN;fail->RETURN_ISSUES | LC.DEFAULTS.DEPENDENCY | stop | Selected task; unresolved authority or contract prevents executable readiness |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | LC.BACKGROUND.DEFAULT | step | 4 | apply_default | pass->LC.BACKGROUND.DESIGN;fail->RETURN_ISSUES | LC.BACKGROUND.DEPENDENCY | stop | Selected task; unresolved authority or contract prevents executable readiness |
