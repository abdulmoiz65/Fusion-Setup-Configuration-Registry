# Learning configuration design enforcement

Sources: FDD C7/GB-08–13 and Oracle D1–D7. Business policy belongs here;
input shape belongs in validation. Required lookup bindings remain incomplete,
so no rule may be labeled verified from user statements alone.

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | 1 | Selected-topic policy | Review applicable source-backed policy using authoritative evidence; stop the dependent preview when unresolved |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | 1 | Selected-topic policy | Review applicable source-backed policy using authoritative evidence; stop the dependent preview when unresolved |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Evaluation required for completion | Required review | find_learning_evaluation_questionnaire | Selected default must gate offering completion; administrator cannot override when using this default | Preview questionnaire and explain completion impact before approval | No automatic fix |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Catalog access/enrollment defaults changed | Required review | read_learning_defaults | D2 changes apply only to newly created items/access/groups, not existing records | Do not promise retrospective updates; distinguish discoverability from enrollment | Separate owning task for existing records |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | No Certificate selected | Required review | find_learning_certificate_template | Disables learner/manager completion-certificate printing | Show the consequence before approval; template readiness needed only when Certificate selected | Only approved change |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Virtual attendance completion rule | Required review | verify_learning_attendance_dependencies | Presence starts at later scheduled start/join and ends at earlier host session end/leave; attendance requires presence/meeting duration >= chosen percentage | Require usable positive duration and authoritative report; no guessed threshold | Only approved setting; no provider/job mutation |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Conversation, template or alert change | Required review | verify_learning_notification_dependencies | TBD: detailed field-level policy and implementation evidence; FDD C7 establishes scope only | Keep topic visible and ask business questions; obtain owner contract before execution | No inferred API or default |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Workload concurrency recommendation | Required review | read_learning_processing_defaults | Review capacity before changes; reconciliation UI jobs multiply bulk scheduled jobs | D7: bulk jobs >=5; reconciliation UI jobs keep 1; expansion bulk threads >=2; expansion UI threads 2 | Recommendation only; approve explicit delta |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Immediate after-save processing disabled | Required review | find_learning_processing_schedule | Requires recurring Expansion processing | Resolve supported job/schedule and approval before disabling dependent behavior | No automatic schedule creation |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Immediate bulk-upload processing disabled | Required review | find_learning_processing_schedule | Requires Process Learning Catalog Items after bulk/API self-paced upload/update | Record processing handoff and owner | No automatic job submission |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Run-as override requested | Required review | verify_learning_execution_user | Eligible execution identity and privileges must be verified; a stable account can reduce creator-departure risk | Separate identity approval; no implicit account creation or grants | Only approved configuration |

## Design Lookup Requirements

| Task Code | Task Name | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | read_learning_defaults | Selected defaults review | TBD: policy evidence mapped from authoritative provider | ora_reference_lookups.md |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | find_learning_evaluation_questionnaire | Evaluation selected | TBD: policy evidence mapped from authoritative provider | ora_reference_lookups.md |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | find_learning_certificate_template | Certificate selected | TBD: policy evidence mapped from authoritative provider | ora_reference_lookups.md |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | verify_learning_attendance_dependencies | Virtual attendance selected | TBD: policy evidence mapped from authoritative provider | ora_reference_lookups.md |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | verify_learning_notification_dependencies | Conversation, template or alert selected | TBD: policy evidence mapped from authoritative provider | ora_reference_lookups.md |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | read_learning_processing_defaults | Processing review | TBD: policy evidence mapped from authoritative provider | ora_reference_lookups.md |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | find_learning_processing_schedule | Immediate processing disabled or scheduling requested | TBD: policy evidence mapped from authoritative provider | ora_reference_lookups.md |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | verify_learning_execution_user | Run-as override requested | TBD: policy evidence mapped from authoritative provider | ora_reference_lookups.md |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | LC.DEFAULTS.DESIGN | step | 5 | design_enforcement | pass->LC.DEFAULTS.GATE;fail->RETURN_ISSUES | LC.DEFAULTS.DEFAULT | stop | Selected task; unresolved authority or contract prevents executable readiness |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | LC.BACKGROUND.DESIGN | step | 5 | design_enforcement | pass->LC.BACKGROUND.GATE;fail->RETURN_ISSUES | LC.BACKGROUND.DEFAULT | stop | Selected task; unresolved authority or contract prevents executable readiness |
