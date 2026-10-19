# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required input, operation intent, versioned key, hierarchy, or translation key is missing | Stop and identify only the missing or ambiguous business value. |
| Live Data Loader metadata is unavailable, incomplete, stale, or ambiguous | Stop DAT preparation and refresh the paginated collection and returned detail/template evidence. |
| An operation, component, attribute, key, or mandatory indicator differs from the target contract | Stop before preview and report the first exact difference; never hard-code UPDATE, assume DELETE, or rewrite target schema. |
| A create root already exists, an update target is absent, or submitted hierarchy keys collide | Stop and report operation intent, complete key, and match count; never convert intent implicitly. |
| An update target exists but full hierarchy, mutability, or current values are incomplete | Stop before DAT rendering and report whether latest/update permission, in-use/seeded/locked/response state, template linkage, per-field/per-component editability, changed-field selection, current emitted values, or affected-child identity failed. Do not fall back to sparse guessed values. |
| An update changes a root or child user key, relinks a template without proof, or omits a child with destructive intent | Reject the update. Preserve omitted children and default template linkage; handle rename, move, resequence, replacement, removal, or relinking only through a separately proven lifecycle contract. |
| Lifecycle REST evidence is the only proof for an in-use or response-bearing mutation | Stop and classify the impact evidence as PARTIAL; do not authorize hierarchy, scoring, linkage, status, or lifecycle change until complete current proof exists. |
| A template is absent | Block only when it was supplied or the current live HDL/subscriber contract requires it; otherwise continue without inventing one. |
| A referenced template, question, owner, category, response override, scoring value, language, or parent is missing, ambiguous, or cross-subscriber | Stop the affected questionnaire hierarchy and report its portable business key. |
| A suggestion-capable reference has zero exact matches | Preserve the raw value, retrieve only its declared restricted target catalog, show at most three exact candidates, and stop DAT rendering for explicit approval. Incomplete candidate retrieval or no eligible candidate remains MISSING or FAILED. |
| A reference-value suggestion is approved | Bind approval under the parent suggestion contract, rerun the original exact resolver and compatibility checks, and create a new immutable preview. Invalidate approval when the target, request, parent key, catalog, candidate set, or selected value changes. |
| A direct Question is requested without a proven target Question/conditional Answer contract, category, response type, template capability, type/answer compatibility, or completed executable procedure | Classify as UNSUPPORTED, preserve sanitized target-contract evidence, and stop before Questionnaire.dat generation; do not downgrade the request to a reusable-question reference. |
| A direct `1CHOICE` or `MULTCHOICE` Question has no Answer rows, duplicate AnswerCode or sequence, an incomplete parent hierarchy, or an unregistered answer attribute; or a direct `TEXT` or `NONE` Question has an Answer row | Classify as input validation, identify the first invalid Answer key or QuestionType/Answer mismatch, and stop before Questionnaire.dat generation. |
| A DAT child, attachment, Answer, or translation is orphaned | Stop the affected hierarchy and report the questionnaire key, section sequence, component, and language where applicable. |
| Attachment update or replacement behavior is unverified | Stop before approval; do not claim delete-and-recreate semantics without current source or runtime evidence. |
| Attachment packaging is incomplete or contains a local path | Stop before ZIP preview and identify the missing metadata or content member. |
| The approved DAT or ZIP changes after preview | Invalidate approval, create a new immutable fingerprinted preview, and request approval again. |
| HDL import/load fails, partially succeeds, or is uncertain | Stop downstream consumer work, preserve sanitized attempt evidence, and reconcile exact target keys before any retry. |
| Load succeeds but readback differs in root, template linkage, hierarchy, scoring, attachments, translations, or behavior | Classify verification as FAILED or PARTIAL and report exact mismatches; do not declare completion. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required input, route-required reference, current state, live metadata, hierarchy, or approval is absent | Supply or refresh the missing evidence and rerun validation. |
| UNSUPPORTED | A requested component, attribute, operation, subscriber behavior, attachment replacement, Answer operation, or consumer linkage lacks a current registered contract | Exclude it and obtain implementation-owner confirmation. |
| FAILED | Schema validation, dependency resolution, import, load, or verification fails | Stop, preserve sanitized evidence, correct the source, and generate a new preview. |
| PARTIAL | Some approved rows loaded but the full questionnaire hierarchy did not | Stop downstream work, reconcile successful keys, and prepare a separately approved corrective attempt. |
| HDL contract violation | DAT identity, operation, component, attribute, key, hierarchy, translation, packaging, or cardinality is invalid | Correct against current live metadata and regenerate the artifact. |
| FSM evidence contract violation | The immutable ordinary-questionnaire graph, metadata, file, header, omission record, or parent-key contract is invalid | Restore the source export before deriving HDL or reconciling results. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview | Task code and name, target/release, operation intent, live metadata timestamp, DAT and ZIP identity, fingerprint, hierarchy counts, versioned root/child keys, supplied/inherited/preserved values, conditional template decision, dependencies, exclusions, warnings, and HDL route. |
| Reference suggestion | Original value, value family, at most three exact restricted target candidates, ranking reasons, any uniquely probable candidate, target and parent key, catalog timestamp, fingerprints, and exact approval required. |
| Failure | Affected questionnaire key, attempt stage, sanitized loader message, verified side effects, unresolved outcome, and one safe next action. |
| Verification | Exact root and child readback keys, expected and observed counts, template/linkage decision, behavior differences, and ALL_GOOD, PARTIAL, or FAILED outcome. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing or ambiguous identity or reference | Do not select the first result, copy a source ID, or generate a substitute code. |
| A suggestion-capable value is non-exact | Do not select the first, nearest, or probable value automatically. Do not suggest from an incomplete, cross-subscriber, inactive, unauthorized, or capability-incompatible candidate set. |
| Missing or inconsistent live HDL metadata | Do not generate from a stale sample, invent a component, operation, required field, or endpoint, or claim readiness. |
| Template absent but not live-required | Do not fabricate a template solely to satisfy a historical sample rule. |
| Unregistered lookup, Answer, attachment, or write behavior | Do not invent a REST request, operation, direct Fusion write, or alternate execution route. |
| Failed, partial, or uncertain import | Do not automatically replay, reuse stale approval, continue consumer linkage, or delete compensation data automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QNR.HANDLE-ISSUE | step | 50 | error_handler | handled->QNR.RETURN-ISSUES | none | stop | Any validation, lookup, dependency, defaulting, or design check fails or requires explicit reference-value approval before continuation |
| QNR.READY | terminal | 60 | terminal | none | QNR.ENFORCE-DESIGN | stop | The Questionnaires request is ready for immutable HDL preview, not authorized import |
| QNR.RETURN-ISSUES | terminal | 70 | terminal | none | QNR.HANDLE-ISSUE | stop | An issue has been classified and disclosed |
