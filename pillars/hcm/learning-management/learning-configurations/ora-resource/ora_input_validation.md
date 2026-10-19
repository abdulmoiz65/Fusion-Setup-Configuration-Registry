# Learning configuration input validation

Sources: FDD GB-02–07 and Oracle D1–D7; see ../references/sources-and-dependencies.md.
This file owns input shape, not business policy. Labels are business settings,
not invented REST attributes. Do not serialize them. Provider input-schema and
evidence-authority bindings remain TBD; no local authority is inferred.

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Selected configuration intent | Environment reference; objective; topic/workload; target scope; desired value or review intent | Ask only the missing business information; retain independent planning | TBD: bind authoritative provider schema; do not require release/build | Selected task | read_learning_defaults |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Selected configuration intent | Environment reference; objective; topic/workload; target scope; desired value or review intent | Ask only the missing business information; retain independent planning | TBD: bind authoritative provider schema; do not require release/build | Selected task | read_learning_processing_defaults |

## Field Validation

| Task Code | Task Name | Check | What Happens | Applies When | Resolver |
|---|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Duplicates and conflicts | Same task/topic/scope/setting with conflicting desired values requires clarification; identical repeats may collapse with provenance; do not count twice | Multiple inputs | read_learning_defaults |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Duplicates and conflicts | Same task/topic/scope/setting with conflicting desired values requires clarification; identical repeats may collapse with provenance; do not count twice | Multiple inputs | read_learning_processing_defaults |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Topic and values | Validate type, scope and documented choices; exact enum/field binding TBD for the selected provider | Defaults request | read_learning_defaults |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Evaluation reference | Require offering type, evaluation decision, selected questionnaire when enabled, and required-for-completion choice | Evaluation enabled | find_learning_evaluation_questionnaire |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Certificate reference | Require certificate choice and template reference when Certificate is selected | Certificate requested | find_learning_certificate_template |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Attendance input | Require explicit percentage and override choice; wire range, precision and field binding TBD; do not invent a threshold | Virtual attendance selected | verify_learning_attendance_dependencies |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Bulk scheduled jobs | Integer 1..200 | Each of Assignments, Recommendations, Access | read_learning_processing_defaults |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Ad hoc UI jobs (reconciliation) | Integer 1..20 | Each of Assignments, Recommendations, Access | read_learning_processing_defaults |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Threads per bulk job (expansion) | Integer 1..200 | Each of Assignments, Recommendations, Access | read_learning_processing_defaults |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Threads per UI job (expansion) | Integer 1..20 | Each of Assignments, Recommendations, Access | read_learning_processing_defaults |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Catalog bulk concurrency | Video 1..5; other content 1..50; integers | Catalog Items | read_learning_processing_defaults |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Catalog UI concurrency | Video maximum 5; other maximum 50; lower bound TBD | Catalog Items | read_learning_processing_defaults |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Run-as selection | Require the selected account reference when override is requested; do not infer identity from display name | Execution identity change | verify_learning_execution_user |

## Dependency-Aware Validation

| Task Code | Task Name | Applies When | Result | Next Action | Resolver |
|---|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Required provider evidence unavailable | Not validated | Ask for missing business facts; route technical gaps to owner; block affected execution only | read_learning_defaults |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Required provider evidence unavailable | Not validated | Ask for missing business facts; route technical gaps to owner; block affected execution only | read_learning_processing_defaults |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | LC.DEFAULTS.INPUT | step | 1 | validate_input | pass->LC.DEFAULTS.LOOKUP;fail->RETURN_ISSUES | none | stop | Selected task; unresolved authority or contract prevents executable readiness |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | LC.BACKGROUND.INPUT | step | 1 | validate_input | pass->LC.BACKGROUND.LOOKUP;fail->RETURN_ISSUES | none | stop | Selected task; unresolved authority or contract prevents executable readiness |
