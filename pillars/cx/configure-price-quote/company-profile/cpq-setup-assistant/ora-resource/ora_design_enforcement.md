# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preflight validation | Confirm target and information needed for the selected path. |
| 2 | Verify CPQ deployment | Make the unauthenticated deployment-version request; a `404` blocks setup. |
| 3 | Check pre-initialization status | Read status once; continue only when it is `SETUP_NOT_DONE`. |
| 4 | Initialize CPQ | After `SETUP_NOT_DONE`, prepare and validate the initialization artifact, build and present its guard preview, obtain one explicit approval, then initialize CPQ once. |
| 5 | Discover state | Rediscover after initialization. |
| 6 | Collect setup inputs | Collect only the values required by the discovered company state. |
| 7 | Validate setup proposal | Validate state-applicable fields, discovered identifiers, and current LOV selections. |
| 8 | Prepare and validate | Prepare the immutable stage artifact and complete Task Hook readiness with approval pending. |
| 9 | Preview, then approve | Build the Task Hook preview and guard manifest, present the exact stage summary, then bind one explicit approval. |
| 10 | Execute and verify once | Execute the documented Data Loader sequence once, immediately retrieve status once, then end. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every CPQ Setup Assistant mutation | Blocker | resolve_cpq_setup_assistant_record | Required company profile, user, assistant identity, or approval is missing | Complete validation and approval before execution | Yes |
| CPQ deployment-version lookup returns `404` | Blocker | resolve_cpq_deployment | CPQ is not deployed in the target environment | Show: “CPQ is not dpeloyed in this instance and hence cannot proceed with Setups now.” Stop before initialization or any Setup Assistant call. | No |
| Any payload includes Company Profile `IsDataExisting`, or includes assistant `Status` outside the final approved submission payload `{ "Status": "SUBMITTED" }` | Blocker | resolve_cpq_setup_assistant_record | A read-only discovery field, or an ungoverned status transition, would be updated | Remove the prohibited field or use only the exact final submission payload after all approval gates pass | Yes |
| A Company Profile create, a manually supplied new CPQ-user identifier, or an unregistered parent-child linkage is proposed | Blocker | resolve_cpq_setup_assistant_record | The proposed Data Loader source does not match the registered `setupAssistants` child contract | Use the discovered Company Profile identity for the registered patch route; create a CPQ user with only the registered required business values; stop when current metadata cannot bind a route | Yes |
| Company Profile reports `IsDataExisting` as `DOESNT_EXIST` after CPQ initialization and configurable fields are populated | Blocker | resolve_cpq_setup_assistant_record | Existing values have not been disclosed and confirmed | Show the current values, redacting tax registration number, and require a retain-or-update decision before collecting missing data or PATCHing | Yes |
| Company Profile reports `IsDataExisting` as `DOESNT_EXIST` after CPQ initialization and no configurable fields are populated | Branch | resolve_cpq_setup_assistant_record | CPQ setup is not done | Collect enterprise name, currency, country, Legal Address Address Line 1 only, and CPQ company identifier; do not collect a complete address, city, state/province, postal or PIN code, additional address lines, Legal Entity, or Business Unit | Yes |
| A child-record identifier is manually supplied | Blocker | resolve_cpq_setup_assistant_record | The value was not returned by the current discovery response | Use the discovered child-record identifier | Yes |
| Existing company data is returned | Blocker | resolve_cpq_setup_assistant_record | The change summary omits the existing-data state or approval does not cover the company-profile update | Show the redacted existing-data state and obtain approval before PATCH | Yes |
| Company Profile reports `IsDataExisting` as `PARTIAL` | Blocker | resolve_cpq_setup_assistant_record | The setup is partial | Show: “Partial setups are completed and hence unable to proceed.” Stop before collecting changes or PATCH. | No |
| Company Profile reports `IsDataExisting` as `ESSJOBALREADYSCHEDULED` | Blocker | resolve_cpq_setup_assistant_record | A Retrieve Latest LDAP Changes or Send Pending LDAP Requests job is active | Show: “A Retrieve Latest LDAP Changes or Send Pending LDAP Requests job is active. You must cancel the existing jobs before continuing with Setup Assistant.” | No |
| A requested CPQ user already exists | Blocker | resolve_cpq_setup_assistant_record | A request would create a duplicate administrator | Reconcile the existing user state; do not create a duplicate; continue only with other validated, approved administrators | Yes |
| Role mappings or starter-data child records are discovered | Blocker | resolve_cpq_setup_assistant_record | The request attempts to mutate a child type without a verified write contract | Report the state as read-only evidence | No |
| A submission result is uncertain | Blocker | resolve_cpq_setup_progress | Completion is not verified | Reconcile through the progress lookup; do not repeat the request | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_cpq_deployment | Before a configuration workflow enters initialization | CPQ deployment result from the unauthenticated deployment-version request | ora_reference_lookups.md |
| resolve_cpq_setup_assistant_record | Before child-resource mutation | Assistant identity and child-record references | ora_reference_lookups.md |
| resolve_cpq_setup_progress | After submission or an uncertain outcome | Verified progress and completion state | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CPQ.INITIALIZATION_BINDING_READINESS | step | 9 | design_enforcement | ready->CPQ.INITIALIZATION_EXECUTION_GATE;blocked->CPQ.RETURN_ISSUES | CPQ.INITIALIZATION_READINESS | stop | Confirm the durable CPQ guard is available and the exact immutable artifact, current registration and target can be bound by its preview. Approval may remain pending; do not require a current-stage manifest, approval record, reviewed binding, actor, expiry or nonce before preview creation. The guard enforces explicit approval, attribution, binding, expiry and atomic nonce consumption at approve/execute. This node cannot approve or execute a mutation. |
| CPQ.CONFIGURATION_BINDING_READINESS | step | 10 | design_enforcement | ready->CPQ.CONFIGURATION_EXECUTION_GATE;blocked->CPQ.RETURN_ISSUES | CPQ.CONFIGURATION_READINESS | stop | Confirm the durable guard and write-boundary adapter are available and ordered operations, administrator set, Run Book, metadata and state can be bound by the preview. Require applicable prior-stage completion and reconciliation, including the documented verified existing-state route when no child write occurred. Current-stage approval remains pending until the preview is built and presented; enforce it only at approve/execute. Retain uncertain-submission locks. This node cannot approve or execute a mutation. |


Pillar recovery must distinguish a durably recorded pre-write check from a crossed write boundary. Release only a proven zero-write attempt under the execution lock, retain its consumed nonce, and require fresh approval. For existing ready configuration with no attempted child write, generate a bound, expiring current-state receipt before separate final approval; never use this route to bypass child reconciliation. Partial-result inspection is read-only, retains pending markers, and does not authorize retry. Registered transport fields are routing metadata, not business changes. See `references/cpq-approval-guard.md` for the command contracts and remaining Core approval dependency.
