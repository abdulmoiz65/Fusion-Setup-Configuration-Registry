# Organization Structures Error Handling

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Required name or Default Set path is incomplete | Stop and request the named missing field |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Existing Default Set is zero, multiple, or nonexact; or a new set was not successfully created and re-resolved | Stop the BU import. Correct the set identity or finish the separate set-creation route, then re-run lookup. |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Existing-BU lookup is incomplete/ambiguous or returns an existing candidate with different comparable configuration | Stop creation. For an identical candidate record a no-op; for a different candidate require an explicit update decision or a new name. |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | A supplied manager or location has zero, multiple, inactive/ineffective, inaccessible, or unavailable HCM LOV results | Stop before preview/import. Correct the supplied worker/location identity, effective date, or HCM REST privilege; do not choose a partial match. A blank optional value requires no HCM lookup. |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | A financial function lacks a verified primary ledger or default legal entity | Stop and request the missing dependency; do not substitute a secondary ledger or reporting currency |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Resolved ledger or legal entity does not equal the selected BU's resolved foundation | Stop import and correct the BU, ledger, or legal entity; do not import a mismatched financial-function assignment. |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Client/provider roles, related-function pair, outsourcing policy, BU role assignments, or duplicate status is unresolved | Select SPR_FSM_ADD_RELATIONSHIP_V1 before applying maintenance-only evidence requirements. Block actual failed eligibility, missing role/pair/needed policy semantics or uncertain prior write; eligible first-submission/read limits are disclosed, not automatically blockers. |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Assignment values are absent or reference match is ambiguous | Stop and request the named value |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Execution contract is absent | Refuse payload, CSV, REST, FSM, or import generation |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Execution contract is absent | Refuse payload, CSV, REST, FSM, or import generation |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Execution contract is absent | Refuse payload, CSV, REST, FSM, or import generation |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Execution contract is absent | Refuse payload, CSV, REST, FSM, or import generation |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Dependent function-assignment data reports that required parent-BU data is absent | Acquire and validate the missing current matching parent-BU data, then prepare a corrected preview for only this stage. Do not blindly retry a write or reuse an unverified original create row. |
| FUN_MANAGE_BUSINESS_UNIT; FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Business Unit import tasks | API process completes but no process log is written locally | Create the output directory, retrieve the process log by process ID, and base the result on its row-level status. |

## Error Classifications

| Task Code | Task Name | Result Category | When Used | Next Action |
|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Input validation | Required group or length rule fails | Correct the named field |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Idempotency | Existing-BU lookup is ambiguous or differs from the desired comparable configuration | Use the existing identical BU as a no-op, obtain an explicit update decision, or select a new name |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Optional HCM reference | A supplied manager or location cannot be resolved exactly and currently | Correct the named person/location or grant only the required HCM LOV privilege; do not populate ManagerId or LocationId by inference |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Dependency readiness | Ledger, legal entity, or Business Unit cannot be verified | Resolve the dependency by name or code |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Foundation compatibility | Resolved ledger or legal entity does not match the selected BU | Correct the selected values before import |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Role, pair, duplicate, or ambiguity | Actual role/pair/identity conflict or missing operation-specific evidence outside qualified first submission | Correct the relevant dependency; qualified first submission is not global absence proof, and existing-state no-op requires comparable current values |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Reference ambiguity | Business Unit or set code has no unique match | Provide a unique reference |

## Disclosure Rules

| Task Code | Task Name | Gate | What Must Be Shown |
|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Validation failure | Blocking rule, supplied value, corrective action, and source |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Validation failure | Blocking rule, supplied value, corrective action, and source |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Validation failure | Blocking rule, supplied value, corrective action, and source |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Validation failure | Blocking rule, supplied value, corrective action, and source |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Source does not establish an execution contract | Do not invent REST, FSM, CSV, package, endpoint, or payload behavior |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Source does not establish an execution contract | Do not invent REST, FSM, CSV, package, endpoint, or payload behavior |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Source does not establish an execution contract | Do not invent REST, FSM, CSV, package, endpoint, or payload behavior |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Source does not establish an execution contract | Do not invent REST, FSM, CSV, package, endpoint, or payload behavior |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---:|---:|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.BLOCKED | terminal | 5 | terminal | none | none | stop | Required group, set-resolution, or idempotency validation fails |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.NOOP | terminal | 6 | terminal | none | BU.IDEMPOTENCY | stop | An existing BU is identical; record no-op and do not import a duplicate |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU.READY | terminal | 7 | terminal | none | BU.IDEMPOTENCY | stop | All mandatory validation passes and the request is classified New |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | BUF.BLOCKED | terminal | 4 | terminal | none | BUF.VALIDATE | stop | Required group or hard field validation fails |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | BUF.READY | terminal | 5 | terminal | none | BUF.DEPENDENCY | stop | Applicable validation, dependencies and the current task contract are verified; return readiness to the caller; this terminal does not authorize a write |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR.BLOCKED | terminal | 5 | terminal | none | none | stop | Identity, role assignment, pair compatibility, defaulting, or duplicate validation fails |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | SPR.READY | terminal | 6 | terminal | none | SPR.DEPENDENCY | stop | Applicable validation, dependencies and the current task contract are verified; return readiness to the caller; this terminal does not authorize a write |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | BUSA.BLOCKED | terminal | 4 | terminal | none | BUSA.VALIDATE | stop | Assignment values are missing or reference resolution is ambiguous |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | BUSA.READY | terminal | 3 | terminal | none | BUSA.VALIDATE | stop | Applicable validation, dependencies and the current task contract are verified; return readiness to the caller; this terminal does not authorize a write |
## Ledger-to-Legal-Entity Association Failure

Classify an absent, repeated, nonexact, incomplete, or unavailable `legalEntitiesLOV` `LedgerFinder` association result as dependency readiness failure. Stop the Business Unit or financial-function import and correct the primary ledger or legal entity; never substitute independent LOV matches.

## Optional Manager and Location Failure

Classify an unresolved supplied manager or location as input validation or authorization/dependency readiness, as appropriate. Resolve a supplied manager through publicWorkers to one active PersonId and a supplied location through locationsLovV2 to one active/effective LocationId before import; do not treat an HCM lookup failure as permission to omit a value that was supplied.

  <!-- -->

## Evidence, Export and Resume Failures

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Native new-set contract or privilege unavailable | Report the native setIdSets gap and reconcile any existing receipt; do not invoke HCM Manage Reference Data Sets as a fallback |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Template-only create rejects omitted technical fields | Retrieve the actual FSM error and identify the required field/current contract; do not copy unrelated BU defaults or silently escalate to a populated export |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Successful import but requested value is unexposed by read API | Report processed-row success and the exact saved-state verification limit separately; do not claim a saved default set/date from template or payload alone |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Network timeout during template discovery or prerequisite read | Classify transport/environment; preserve whether a POST was reached and any process ID; do not claim an assignment failed when it was never submitted |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Oversized child omitted or scope criterion ignored | Reject full/unscoped data as a source. Use current template and select BUSA_FSM_ADD_OVERRIDE_V1, otherwise BUSA_FSM_PARENT_KEY_V1 with exact permitted values; complete BU assignment GETs supply current state. A missing exported child or eligible omitted technical fields are not mapping blockers. |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Prior stage failed or write outcome uncertain | Stop dependent stages, preserve completed BUs/assignments and reconcile recorded requests; resume rather than recreate or roll back by deletion |

Use the core OAuth/client retry policy and preserve native/import receipts. Refresh auth serially, distinguish identity/privilege/transport/Fusion/process/artifact failures, and never interpret a failed GET as an empty collection. Existing successful objects are not cleanup targets for a failed later stage; destructive work requires its own supported workflow and authorization.

## Mandatory Log Review Before Outcome Reporting

| Task Code | Task Name | Reporting Gate | Required Evidence |
|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Before reporting a submitted FSM import as succeeded or failed | Retrieve, persist and inspect the actual ProcessLog for this environment and recorded request/process; reconcile terminal status with business-object and row results, failed counts, warnings and error details |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Before reporting a submitted FSM import as succeeded or failed | Retrieve, persist and inspect the actual ProcessLog for this environment and recorded request/process; reconcile terminal status with business-object and row results, failed counts, warnings and error details |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Before reporting a submitted FSM import as succeeded or failed | Retrieve, persist and inspect the actual ProcessLog for this environment and recorded request/process; reconcile terminal status with business-object and row results, failed counts, warnings and error details |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Before reporting a submitted FSM import as succeeded or failed | Retrieve, persist and inspect the actual ProcessLog for this environment and recorded request/process; reconcile terminal status with business-object and row results, failed counts, warnings and error details |

This gate applies to both success and failure reports, including status-check prompts. A loader summary, HTTP response, terminal API status or absence of a visible error is insufficient by itself. Report the verified request/process identity, counts actually exposed by the log, warnings or errors, and a link to the reviewed log. Do not invent unreported row counts. Preserve partial successes and disclose mixed results; do not describe the entire requested configuration as successful when some objects or rows failed. If status and log disagree, report the discrepancy and keep the outcome unconfirmed until reconciled.

If the matching log is unavailable, incomplete or cannot be retrieved, report the API status as provisional and state that the import outcome is unconfirmed pending log review. Preserve the request/process IDs and retrieval error; do not declare success/failure, advance dependent stages or resubmit solely because log evidence is missing. Log-confirmed processing success still requires the applicable saved-state checks before claiming persisted business values.

For a request rejected before submission, report the actual validation, authentication, transport or API error and explicitly state that no import was submitted; no FSM process log exists to review. For native reference-set REST creation, inspect the core client's diagnostic/audit record, response receipt and exact re-lookup evidence instead of inventing an FSM ProcessLog. A no-op must cite the current-state comparison and must not be presented as a successful import.

## Full Export Policy Failure

For any of the four BU tasks, classify a proposed full populated export or an ignored scope as a policy/catalog mismatch with reason `full_data_export_prohibited`. Stop that acquisition and do not consume or locally filter the returned populated package. Continue only with the current template, declared GETs, verified current-workflow evidence or a named, declared, authorized and genuinely scoped route. Preserve prior successful objects. Select the independently tested task profile first. Identify only values that remain required by that selected operation; its accepted omissions are not fabricated saved values or preservation waivers. Outside profile eligibility, report the actual source gap without full-export fallback.

## Function Readiness and Verification Limits

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Generated parent keys/dates or ConfigurationStatus unavailable | Evaluate BUF_FSM_ADD_FUNCTION_V1 eligibility first. If it passes, proceed through normal preparation/validation/approval with its documented omissions; report unexposed saved values separately. Do not require a waiver or full export solely for these fields. |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Additive profile rejected by actual processing | Review the matching ProcessLog and available detailed diagnostics; identify the server-confirmed contract mismatch, reconcile saved state and prepare any correction through core approval; no silent export fallback or automatic resubmission |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Processing succeeds and exact BU appears in the module finder | Report log-confirmed processing and visible module membership with their sources; do not claim ConfigurationStatus or complete optional/default/date preservation was independently read |

Unknown saved fields are not universally a preparation failure. Classify an actual missing mandatory input/contract/identity as a blocker, and an unexposed post-change attribute as a verification limit unless the requested operation explicitly requires it. Preserve strict evidence requirements for existing-state no-op/maintenance and provider eligibility outside this additive profile.


## Set Override and First Relationship Evidence Limits

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Generated parent/assignment keys or effective dates are unexposed | Evaluate BUSA_FSM_ADD_OVERRIDE_V1 first; if eligible, use tested name linkage and omissions through normal validation/approval without a waiver; outside it obtain exact required current values |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Technical party keys/dates or saved four-key read unavailable | Evaluate SPR_FSM_ADD_RELATIONSHIP_V1 first; eligible first submission uses tested omissions and workflow provenance, discloses saved-row limits, and needs no missing-read waiver; unsupported maintenance stays blocked |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | ServiceProviderFinder errors that Business Unit ID is required | Classify target contract/context failure; retain diagnostics; no empty-state claim, guessed finder parameter, unchanged repeated call or full export; only an otherwise eligible first-link profile can proceed with the read limit |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Import log confirms relationship row but independent read remains unavailable | Report log-confirmed processing, exact request/fingerprint and independently verified party/module state; explicitly mark saved relationship row unverified; do not resubmit to resolve that verification gap |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Requested override and other visible assignments compare correctly after reviewed processing | Report exact saved override and visible explicit-assignment preservation; distinguish unexposed default-set/date certification limits |

Missing post-change certification and missing pre-import inputs are different conditions. A tested omission contract can resolve preparation without supplying the saved value. On a genuine backend rejection, inspect the detailed log, reconcile state and prepare a corrected approved artifact only for the failed stage. Do not turn transport/artifact persistence errors or unsubmitted validation blockers into an import failure.


## All Result Reporting and UI Refusal

The mandatory log-review gate applies before quoting any submitted import result, including status-check replies and failure analysis. Persist and read the actual matching log; do not substitute a loader summary, initiation receipt or UI observation. Missing or contradictory logs leave the outcome unconfirmed, with request/process identity and the retrieval gap disclosed.

For lookup, duplicate-check, review and no-op results, inspect the actual declared endpoint responses and available core diagnostics first, complete paging, and state visibility/unexposed-field limits. For native REST creation inspect its matching core diagnostic/audit record, response receipt and exact re-lookup. For pre-submission rejection inspect the actual rule/client diagnostic and say no import was submitted. These routes do not have FSM import logs; never invent one or require a dummy import to obtain it.

Refuse UI navigation or inspection by this skill or any delegate, including manual screenshots supplied as a verification workaround. Missing required evidence remains a reported endpoint/contract gap. Authentication is only the user-completed core.auth handoff; it grants no task UI access. Existing qualified preparation profiles and their bounded verification limits remain unchanged.
