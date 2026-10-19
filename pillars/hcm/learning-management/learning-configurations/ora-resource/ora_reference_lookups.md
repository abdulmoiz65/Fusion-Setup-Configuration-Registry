# Learning configuration reference lookups

Sources: FDD GB-06/09 and D1–D7 in ../references/sources-and-dependencies.md.
These are required read-only contracts, not callable APIs. Unknown source
bindings remain TBD; user inputs do not establish local data authority.
Run only applicable resolvers after the selected workflow's external-read
preflight. A lookup never changes settings, submits a job or grants access.

## Live Lookups

| Task Code | Task Name | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | read_learning_defaults | Selected defaults review | Environment; requested topic and scope | TBD: supported defaults reader | TBD: current settings and authoritative allowed fields/values | TBD: exact setting and scope keys | TBD: verified baseline with timestamp and absence semantics | No match: distinguish absent from unreadable; ask for missing identity. Multiple: request disambiguation. Denied/incomplete: Not validated; no write. |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | find_learning_evaluation_questionnaire | Evaluation selected | Offering type; questionnaire reference | TBD: bind questionnaire provider reader | TBD: identity and Learner Evaluation type evidence | TBD: unique questionnaire identity | TBD: eligible evaluation reference | No match: distinguish absent from unreadable; ask for missing identity. Multiple: request disambiguation. Denied/incomplete: Not validated; no write. |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | find_learning_certificate_template | Certificate selected | Course or specialization; template reference | TBD: supported template reader | TBD: template identity and availability | TBD: exact eligible template match | TBD: selected template and preview evidence | No match: distinguish absent from unreadable; ask for missing identity. Multiple: request disambiguation. Denied/incomplete: Not validated; no write. |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | verify_learning_attendance_dependencies | Virtual attendance selected | Provider and attendance-processing requirement | TBD: declared provider and schedule readers | TBD: integration/report and sync readiness fields | TBD: exact provider and existing schedule | TBD: verified provider and sync readiness | No match: distinguish absent from unreadable; ask for missing identity. Multiple: request disambiguation. Denied/incomplete: Not validated; no write. |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | verify_learning_notification_dependencies | Conversation, template or alert selected | Topic; audience; language; trigger and channel | TBD: approved topic-specific reader | TBD: configuration, profile enablement and delivery evidence | TBD: exact topic identity and consumer scope | TBD: current configuration and conditional foundation readiness | No match: distinguish absent from unreadable; ask for missing identity. Multiple: request disambiguation. Denied/incomplete: Not validated; no write. |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | read_learning_processing_defaults | Processing review | Environment; workload; setting scope | TBD: supported background-settings reader | TBD: current values and metadata | TBD: exact workload and setting keys | TBD: verified processing baseline | No match: distinguish absent from unreadable; ask for missing identity. Multiple: request disambiguation. Denied/incomplete: Not validated; no write. |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | find_learning_processing_schedule | Immediate processing disabled or scheduling requested | Workload; process intent; timezone | TBD: selected process/schedule reader | TBD: supported definition, parameters and existing schedule fields | TBD: exact job/parameters/schedule identity | TBD: existing schedule, dependency status and duplicate detection | No match: distinguish absent from unreadable; ask for missing identity. Multiple: request disambiguation. Denied/incomplete: Not validated; no write. |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | verify_learning_execution_user | Run-as override requested | Selected account reference; intended process scope | TBD: governed identity and privilege verification | TBD: eligible identity and operation privileges | TBD: exact eligible account; no fuzzy match | TBD: resolved execution identity and privilege evidence | No match: distinguish absent from unreadable; ask for missing identity. Multiple: request disambiguation. Denied/incomplete: Not validated; no write. |

## Lookup Execution Rules

| Task Code | Task Name | Situation | What Happens |
|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Contract incomplete | Stop the affected lookup; report exact missing contract and owner. Continue independent intake; no REST/browser/loader substitute. |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Contract incomplete | Stop the affected lookup; report exact missing contract and owner. Continue independent intake; no REST/browser/loader substitute. |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | LC.DEFAULTS.LOOKUP | step | 2 | reference_lookup | pass->LC.DEFAULTS.DEPENDENCY;fail->RETURN_ISSUES | LC.DEFAULTS.INPUT | stop | Selected task; evaluate only applicable resolver rows; no mutation |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | LC.BACKGROUND.LOOKUP | step | 2 | reference_lookup | pass->LC.BACKGROUND.DEPENDENCY;fail->RETURN_ISSUES | LC.BACKGROUND.INPUT | stop | Selected task; evaluate only applicable resolver rows; no mutation |
