# RMCS Algorithm Error Handling

## Scope

Owns checkpoint outcomes, disclosure and execution refusal. The [XML guide](../resources/ora_algorithm_xml_guidance.md#failure-reporting) defines artifact-specific failure detail; [unsupported live contracts](ora_reference_lookups.md#unsupported-live-contracts) remain blocked.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Local checkpoint is supported and phase-applicable gates pass | Continue to local changeset default evaluation and checkpoint result validation; the caller alone owns subsequent runbook operations |
| Requested operation is outside assisted authoring | Return unsupported_operation with missing contract and routed next action; do not perform Fusion mutation, process execution or verification |
| Required evidence is absent or ambiguous | Return the exact affected source, target, action or approval question and saved stage; no older-input or AR fallback |
| Supplied-file authority is mistaken for publication evidence | Correct the claim to current-file evidence; leave deployed/published state unverified |
| Source discovery outcome needs a decision or prerequisite | Preserve the companion outcome and its evidence; the primary resumes the saved stage under its canonical handoff procedure |
| Approval or extracted-expression comparison fails | Apply the XML guide's stop and correction/reapproval procedure; never silently change approved content |
| Artifact persistence is unsafe or unavailable | Report path/stage and safe corrective action; do not create XML without exact permitted proposal and approval persistence |
| An unrelated live operation or failed external process is reported | Record its last known facts as external context only; no retry or status query is selected by this task |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Wrong/current input, ambiguous action, unresolved source shape, unsupported structure or expression comparison mismatch | Identify the failing field/action and required correction under the canonical guide |
| Catalog mismatch | Task or hierarchy differs from the selected nested skill | Correct routing without changing catalogue metadata |
| Auth/authz | Companion reports describe access failure | Preserve its distinct failure and core-owned recovery result; primary performs no authentication call |
| Transport/environment | Local tooling unavailable or companion reports environment/transport failure | Report environment and stage; do not recast as no attribute match |
| Fusion API | Companion reports a declared read failure | Return sanitized status and supported core next action; no invented retry |
| Process timeout | A separately run process is reported as timed out | Preserve supplied environment, job/request ID, last status and elapsed wait; this route cannot poll it |
| Process failed | A separately run integration process is reported failed | Preserve supplied partial outcomes/errors; request its supported workflow for logs/recovery |
| Artifact persistence | Exact proposal, approval or local output cannot be retained safely | Stop artifact creation/handoff and request permitted handling |
| Approval blocker | Approval is absent, stale, ambiguous or outside the exact change scope | Obtain explicit approval of the current complete proposal |
| Unsupported operation | Requested operation has no supported route in this task | Return the owning missing live or runtime contract and next action |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Every result | Request and phase, status, evaluated/not-applicable checks, evidence and decision references, unresolved questions and next stage; never imply unevaluated checks passed |
| Final proposal | Complete Groovy, exact scope and the canonical final traceability/configuration handoff |
| Local artifact | Actual output reference, exact approval linkage, comparison result and remaining unverified runtime/import/publication behavior |
| Blocker | Stage, failure class, reason, affected operation and actionable correction with redacted evidence |
| Registry readiness | Structural assisted-checkpoint readiness only; runtime inputs, approvals and unsupported live contracts remain independent gates |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Local inputs or user decisions are authoritative | Do not equate local authority with current deployed or published state |
| A phase is earlier than approval or artifact preparation | Do not invent a proposal, approval, destination or successful output |
| Readiness is incomplete or a required fact is unresolved | Do not use a readiness override, erase a blocker or substitute another execution route |
| A live action is requested | Do not infer an importer from XML shape, dataloader_import_mode, table names, available credentials or tools |
| A result is uncertain | Do not replay imports/writes/process submissions or claim integration success |
| Companion findings are returned | Do not duplicate the primary workflow or repeat the same question without new evidence or a decision |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMCSALG.CHECK_EXECUTION_CONTRACT | decision | 50 | execution_gate | ready->RMCSALG.APPLY_DEFAULT;blocked->RMCSALG.REPORT_ISSUES;unsupported->RMCSALG.RETURN_UNSUPPORTED | RMCSALG.ENFORCE_DESIGN | stop | Gate the declared assisted phase and exact permitted operation; no file or Fusion mutation occurs here. |
| RMCSALG.RETURN_RULE_RESULTS | terminal | 80 | terminal | none | RMCSALG.EVALUATE_CHECKPOINT | stop | Return this phase's checkpoint findings to the primary caller, not a claim of deployed or tested Fusion changes. |
| RMCSALG.REPORT_ISSUES | step | 90 | error_handler | reported->RETURN_ISSUES | none | stop | Classify the reached failure and preserve evidence, missing decisions and owning next action. |
| RETURN_ISSUES | terminal | 100 | terminal | none | none | stop | Return blocking findings to the saved caller stage without an automatic retry. |
| RMCSALG.RETURN_UNSUPPORTED | terminal | 110 | terminal | none | none | stop | Refuse the unsupported operation and return its missing contract without performing it. |
