# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required input, operation intent, or complete portable identity is missing | Stop and identify only the missing or ambiguous business value. |
| Live Data Loader metadata is unavailable, incomplete, stale, or ambiguous | Stop DAT preparation; refresh the collection and returned detail/template evidence without falling back to a sample schema. |
| An operation, component, attribute, user key, or mandatory field differs from the current target contract | Stop before preview and report the first exact contract difference; do not rewrite the target schema or invent an instruction. |
| A create root already exists, an update target is absent, or an in-batch key is duplicated | Stop and report the operation intent, complete business key, and match count; never convert create to update implicitly. |
| An update target exists but is not safely mutable | Stop before DAT rendering and report whether UpdateAllowedFlag, immutable-key integrity, changed-field selection, full emitted-value readback, or affected-child identity failed. Do not fall back to create, version, delete, or sparse guessed values. |
| QuestionType or ResponseTypeName is blank or the pair has no exact target match | Stop before DAT rendering. Preserve the raw values, retrieve the current target candidate catalogs, and show at most three exact compatible pairs with ranking reasons. Mark a uniquely supported pair as probable, but do not use it until the user explicitly approves that complete pair. |
| A suggested QuestionType and ResponseTypeName pair is approved | Bind the approval to the exact pair, target, question business key, source-request fingerprint, candidate-set fingerprint, and catalog timestamp; rerun the live permitted-type and exact-pair lookups and create a new immutable preview. If the request, target, candidate set, permitted type, or pair changed, invalidate the approval and ask again. |
| Another suggestion-capable reference has zero exact matches | Preserve the raw value, retrieve only its declared restricted target catalog, show at most three exact candidates, and stop DAT rendering for explicit approval. If candidate retrieval is incomplete or no eligible candidate exists, classify the reference as MISSING or FAILED. |
| A reference-value suggestion is approved | Bind approval under the parent suggestion contract, rerun the original exact resolver and compatibility checks, and create a new immutable preview. Invalidate approval when the target, request, parent key, catalog, candidate set, or selected value changes. |
| An AnswerCode is duplicated in the DAT, collides with another target parent, or has an operation-inconsistent target match | Stop before preview and show the invalidity reason, portable parent key, operation and child intent, original code, and any proposed QuestionCode_QstnVersionNum_OriginalAnswerCode mapping. For an existing update child, accept only one exact same-parent match. Do not change the DAT unless the user explicitly approves an exact replacement mapping; preserve the intended LongText. |
| A reference is missing, ambiguous, stale, or cross-subscriber | Stop the affected hierarchy and identify the reference business key without disclosing internal IDs. |
| A Recruiting organization resolves only as a hierarchy display label or lacks a canonical active organizationsLOV row | Stop before DAT rendering. Keep the discovery OrganizationId transient, do not split the display label, and obtain one exact active canonical organizationsLOV.Name bound to the QuestionContext key. |
| A status-only Question inactivation has zero visible usage but the evidence is partial | Do not treat the outcome as complete dependency proof. Present `partial_no_visible_usage` with the exact key, endpoint completion and zero counts, residual-impact warning, status-only change set, and required impact-bound approval. Rerun the exact checks after approval; block on any nonzero result, lookup failure, state conflict, child change, or stale approval. |
| Unrelated template/placement totals or template-set diagnostics change during status-only inactivation revalidation | Use compare_question_inactivation_review and perform one complete confirmation scan. Retain approval when material scope is unchanged and both scans prove zero visible matching usages. Record the count drift as a warning; do not enter another approval loop. If collection coverage or identity cannot be reconciled, stop for diagnosis. |
| A DAT child or translation is orphaned | Stop the affected versioned question hierarchy and report the parent key, child component, and translation language where applicable. |
| Attachment packaging is incomplete or contains a local path | Stop before ZIP preview and identify the missing metadata or content member; never upload local-path text as file content. |
| FSM baseline evidence is incomplete or inconsistent | Stop derivation, restore the immutable export, and keep FSM out of the mutation route. |
| The approved DAT or ZIP changes after preview | Invalidate approval, generate a new immutable preview and fingerprint, and request approval again. |
| HDL import or load fails, partially succeeds, or has an uncertain outcome | Stop dependent work, preserve sanitized attempt evidence, and reconcile exact user keys with read-only target verification before considering another attempt. |
| Load status succeeds but readback differs from the approved hierarchy | Classify verification as FAILED or PARTIAL, list the exact mismatched keys and fields, and do not declare completion. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | A required input, reference, current target state, metadata contract, or approval is absent | Supply or refresh the missing evidence and rerun from validation. |
| UNSUPPORTED | The requested component, attribute, operation, subscriber behavior, or lookup mutation lacks a current registered contract | Exclude it and obtain implementation-owner confirmation. |
| FAILED | Schema validation, dependency resolution, import, load, or verification fails | Stop, preserve sanitized evidence, correct the source, and produce a new preview. |
| PARTIAL | Some approved rows loaded but the full approved hierarchy did not | Stop dependent tasks, reconcile successful keys, and prepare a separately approved corrective attempt. |
| HDL contract violation | DAT identity, operation, component, attribute, key, hierarchy, packaging, or target cardinality is invalid | Correct the normalized hierarchy against live metadata and regenerate the artifact. |
| FSM evidence contract violation | The immutable metadata, file, header, hierarchy, or parent-key contract is invalid | Restore the source export before deriving HDL or reconciling results. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview | Task code and name, target and verified release when available, operation intent, live metadata timestamp, exact DAT and ZIP identity, fingerprint, hierarchy counts, user keys, supplied and preserved values, dependencies, exclusions, warnings, and HDL route. For status-only inactivation, show unavailable release/principal provenance explicitly and retain the partial data-visibility warning; do not block solely on those unavailable provenance values. |
| Type-pair suggestion | Original QuestionType and ResponseTypeName, at most three exact target-compatible pairs, ranking reasons, the uniquely probable pair when supported, target, catalog timestamp, source-request fingerprint, candidate-set fingerprint, and the exact approval required. |
| Reference suggestion | Original value, value family, at most three exact restricted target candidates, ranking reasons, any uniquely probable candidate, target and parent key, catalog timestamp, fingerprints, and the exact approval required. |
| Status-only inactivation approval | Exact portable question key, current active/latest/updateable evidence, target inactive status, exact changed-field set `["Status"]`, preserved root values, no-child assertion, stable lookup-scope fingerprints and zero matching usages, residual-impact warning, template and operation-contract hashes, and the exact approval required. Show scanned totals separately as diagnostics. |
| Failure | Affected business key, attempt stage, sanitized loader message, verified side effects, unresolved outcome, and one safe next action. |
| Verification | Exact readback keys, expected and observed hierarchy counts, mismatched fields or behavior, and whether the outcome is ALL_GOOD, PARTIAL, or FAILED. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing or ambiguous identity or reference | Do not select the first result, copy a source ID, or generate a substitute business value. |
| Blank or non-exact QuestionType or ResponseTypeName | Do not silently normalize, substitute, or write a probable value. Suggestions may contain only exact current target pairs and require explicit approval before use. |
| A suggestion-capable value is non-exact | Do not select the first, nearest, or probable value automatically. Do not suggest from an incomplete, cross-subscriber, inactive, unauthorized, or capability-incompatible candidate set. |
| Missing or inconsistent live HDL metadata | Do not generate from a stale sample, invent a component, operation, mandatory field, or endpoint, or claim readiness. |
| Unregistered lookup or write behavior | Do not invent a REST request, direct Fusion write, or alternate execution method. |
| Failed, partial, or uncertain import | Do not automatically replay, reuse stale approval, continue dependent template/questionnaire work, or delete compensation data automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QLIB.HANDLE-ISSUE | step | 50 | error_handler | handled->QLIB.RETURN-ISSUES | none | stop | Any validation, lookup, dependency, defaulting, or design check fails or requires explicit user approval before continuation |
| QLIB.READY | terminal | 60 | terminal | none | QLIB.ENFORCE-DESIGN | stop | The Question Library request is ready for immutable HDL preview, not authorized import |
| QLIB.RETURN-ISSUES | terminal | 70 | terminal | none | QLIB.HANDLE-ISSUE | stop | An issue has been classified and disclosed |
