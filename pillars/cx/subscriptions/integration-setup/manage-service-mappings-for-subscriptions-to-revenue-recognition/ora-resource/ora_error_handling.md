# Subscription to RMCS Service Mapping Error Handling

## Scope

Owns assisted-checkpoint failure disclosure and the operation gate. Detailed candidate outcomes remain in [mapping failure guidance](../resources/ora_service_mapping_guidance.md#failure-and-review-only-assumption-outcomes); acquisition, authentication and retries remain in [reference lookups](ora_reference_lookups.md#live-lookups). Terminals return checkpoint records to the caller; primary/companion orchestration stays outside this task graph.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Current identity, highest version or pair freshness fails | Return canonical preflight failure and corrected input needed; no other version or remembered-export substitution |
| Search returns no match, ambiguity or missing exposure | Preserve the distinct [mapping outcome](../resources/ora_service_mapping_guidance.md#failure-and-review-only-assumption-outcomes) and corrective question |
| Newly recommended source remains unaccepted | Return needs_decision with named evidence, including a sole candidate |
| Optional describe cannot run | Report failed scope/status and class under the canonical lookup and primary-led review-only choice |
| Handoff legitimately reports pending, blocked or declined work | Return that outcome if its checkpoint record is complete; never relabel it analyzed or published |
| Claimed field has incompatible type, length, access or unsupported correspondence | Report violated predicate and evidence; no truncation, coercion, rename or silent alternative |
| Checkpoint input/result record is incomplete or inconsistent | Return missing field, failed check or stale reference and safe correction |
| Permitted durable record cannot be stored safely | Disclose persistence failure and safe intended destination; do not claim it was saved |
| Requested operation is outside the companion | Return unsupported at the gate; no mutation, publication, deployment or Fusion test |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Missing/malformed current input, wrong input integration identity, ambiguous action, incompatible metadata or inconsistent phase/result contract | Request exact corrected input, evidence or result field |
| catalog_mismatch | Requested task or hierarchy differs from the selected catalogue task | Correct routing without changing catalogue metadata or borrowing AR behavior |
| auth_authz | Selected describe identity or privilege is unavailable | Use canonical client policy or return authorization prerequisite |
| transport_environment | Permitted metadata read cannot reach selected environment | Return classified scope/status and primary-led remediation choice |
| fusion_api | Selected describe returns an API failure | Retain sanitized status/scope; no alternate route |
| artifact_persistence | Permitted checkpoint/handoff record cannot be retained | Report safe destination and recovery need |
| approval_blocker | Action or overwrite lacks approval required by its owning workflow | Do not infer approval from checkpoint or source choice |
| unsupported_operation | Action requires an undeclared write/publication/integration contract | Return unsupported and missing separate route |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| CHECK_EXECUTION_CONTRACT | Phase and requested operation; confirm assisted checkpoint with any already selected optional describe branch, not mutation/import/publication/test |
| Checkpoint completion | Exact task, phase, terminal/path, observed outcome, validated local facts, evidence, remaining decisions/prerequisites, actual side effects and safe continuation |
| Source or publication readiness | Separate acceptance, current-file exposure/access and evidenced publication; no analyzed-equals-published inference |
| Failure | Failed stage/class, sanitized evidence/status, known partial effects and one exact next action |
| Resume | Current request/evidence and changed decisions; reopen affected findings without re-asking unchanged choices or repeating unresolved routes |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Checkpoint or handoff passes | Do not edit mapping XML, publish, import, execute an algorithm or launch Fusion tests |
| Unsupported live contract requested | Do not substitute browser, SQL, business-data GET, another REST client or Data Loader |
| Generated flags show export/import N and blank businessObject | Do not infer CSV/FSM/loader support from dataloader_import_mode REST |
| Review-only assumptions accepted | Do not bypass [source/evidence gates](../resources/ora_service_mapping_guidance.md#source-resolution-record), context confirmation or primary Groovy/XML approval |
| Metadata read fails or completion is uncertain | No second route or unlimited retry; canonical lookup owns acquisition policy |
| Evidence contains sensitive values | Do not retain credentials, tokens, protected metadata or customer payloads in reusable files or diagnostics |
| Future mutation or downstream verification is undocumented | Do not complete the [unsupported contract](ora_reference_lookups.md#unsupported-live-contracts) or use it as a hidden prerequisite for unrelated local analysis |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMCSSM.CHECK_EXECUTION_CONTRACT | decision | 50 | execution_gate | passed->RMCSSM.EVALUATE_CHECKPOINT;blocked->RMCSSM.REPORT_ISSUES;unsupported->RMCSSM.RETURN_UNSUPPORTED | RMCSSM.ENFORCE_DESIGN | stop | Check assisted phase and operation boundary only; perform no mutation and grant no deployment approval. |
| RMCSSM.RETURN_RULE_RESULTS | terminal | 80 | terminal | none | RMCSSM.EVALUATE_CHECKPOINT | stop | Return completed checkpoint checks and actual structured outcome; no source acceptance or publication is implied. |
| RMCSSM.REPORT_ISSUES | step | 90 | error_handler | reported->RETURN_ISSUES | none | stop | Classify and disclose checkpoint issues with evidence and a safe next action; no retry or automatic source substitution. |
| RETURN_ISSUES | terminal | 100 | terminal | none | none | stop | Return failed or missing checkpoint status and exact correction. |
| RMCSSM.RETURN_UNSUPPORTED | terminal | 110 | terminal | none | none | stop | Return unsupported operation and required separate contract without invoking another task or live action. |
