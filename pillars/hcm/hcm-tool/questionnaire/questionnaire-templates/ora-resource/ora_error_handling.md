# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required input, operation intent, root key, hierarchy, or translation key is missing | Stop and identify only the missing or ambiguous business value. |
| OwnerPersonNumber is missing | Stop before any Questionnaire Templates service lookup or DAT rendering and request OwnerPersonNumber. |
| Live Data Loader metadata is unavailable, incomplete, stale, or ambiguous | Stop DAT preparation and refresh the paginated collection and returned detail/template evidence. |
| An operation, component, attribute, key, or mandatory indicator differs from the target contract | Stop before preview and report the first exact difference; never hard-code UPDATE, assume DELETE, or rewrite the target schema. |
| A create root already exists, an update target is absent, or submitted hierarchy keys collide | Stop and report operation intent, complete key, and match count; never convert intent implicitly. |
| A template resolves in the LOV but not as one authoritative full-resource template | Stop before DAT rendering. Report the identity-contract mismatch and do not treat LOV IDs or a backing QuestionnaireId as a full-template update key. |
| An update target exists but mutability or current values are incomplete | Stop before DAT rendering and report whether root permission, in-use/seeded/locked state, per-field/per-component editability, changed-field selection, current emitted values, or affected-child identity failed. Do not fall back to sparse guessed values. |
| An update changes a root or child user key, or omits a child with destructive intent | Reject the update. Preserve omitted children; handle rename, move, resequence, replacement, or removal only through a separately supported lifecycle contract. |
| A referenced question, owner, category, format, scoring value, language, or parent is missing, ambiguous, or cross-subscriber | Stop the affected template hierarchy and report its portable business key. |
| A suggestion-capable reference has zero exact matches | Preserve the raw value, retrieve only its declared restricted target catalog, show at most three exact candidates, and stop DAT rendering for explicit approval. Incomplete candidate retrieval or no eligible candidate remains MISSING or FAILED. |
| A reference-value suggestion is approved | Bind approval under the parent suggestion contract, rerun the original exact resolver and compatibility checks, and create a new immutable preview. Invalidate approval when the target, request, parent key, catalog, candidate set, or selected value changes. |
| A missing reusable question is encountered | Stop unless explicit embedded-creation intent, complete new-question data, current target support, and renewed preview approval are present. |
| A DAT child, attachment, or translation is orphaned | Stop the affected hierarchy and report the template key, section sequence, component, and language where applicable. |
| Attachment packaging is incomplete or contains a local path | Stop before ZIP preview and identify the missing metadata or content member. |
| A release-specific behavior such as DateResponse update parity is unverified | Mark the behavior UNSUPPORTED for automatic handling and require current implementation-owner or runtime evidence. |
| The approved DAT or ZIP changes after preview | Invalidate approval, create a new immutable fingerprinted preview, and request approval again. |
| HDL import/load fails, partially succeeds, or is uncertain | Stop dependent questionnaires, preserve sanitized attempt evidence, and reconcile exact target keys before any retry. |
| Load succeeds but readback differs in header, controls, hierarchy, attachments, or translations | Classify verification as FAILED or PARTIAL and report exact mismatches; do not declare completion. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required input, reference, current state, live metadata, hierarchy, or approval is absent | Supply or refresh the missing evidence and rerun validation. |
| UNSUPPORTED | A requested component, attribute, operation, embedded-creation path, subscriber behavior, or implementation-gap workaround lacks current proof | Exclude it and obtain implementation-owner confirmation. |
| FAILED | Schema validation, dependency resolution, import, load, or verification fails | Stop, preserve sanitized evidence, correct the source, and generate a new preview. |
| PARTIAL | Some approved rows loaded but the full template hierarchy did not | Stop dependent work, reconcile successful keys, and prepare a separately approved corrective attempt. |
| HDL contract violation | DAT identity, operation, component, attribute, key, hierarchy, translation, packaging, or cardinality is invalid | Correct against current live metadata and regenerate the artifact. |
| FSM evidence contract violation | The immutable two-part graph, metadata, file, header, or parent-key contract is invalid | Restore the source export before deriving HDL or reconciling results. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview | Task code and name, target/release, operation intent, live metadata timestamp, DAT and ZIP identity, fingerprint, hierarchy counts, root and child keys, supplied and preserved values, dependencies, exclusions, warnings, and HDL route. |
| Reference suggestion | Original value, value family, at most three exact restricted target candidates, ranking reasons, any uniquely probable candidate, target and parent key, catalog timestamp, fingerprints, and exact approval required. |
| Failure | Affected template key, attempt stage, sanitized loader message, verified side effects, unresolved outcome, and one safe next action. |
| Verification | Exact root and child readback keys, expected and observed counts, control or behavior differences, and ALL_GOOD, PARTIAL, or FAILED outcome. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing or ambiguous identity or reference | Do not select the first result, copy a source ID, or generate a substitute code. |
| A suggestion-capable value is non-exact | Do not select the first, nearest, or probable value automatically. Do not suggest from an incomplete, cross-subscriber, inactive, unauthorized, or capability-incompatible candidate set. |
| Missing or inconsistent live HDL metadata | Do not generate from a stale sample, invent a component, operation, required field, or endpoint, or claim readiness. |
| Missing reusable question | Do not silently create it inside the template hierarchy. |
| Unregistered lookup or write behavior | Do not invent a REST request, direct Fusion write, or alternate execution route. |
| Failed, partial, or uncertain import | Do not automatically replay, reuse stale approval, continue dependent questionnaires, or delete compensation data automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QTPL.HANDLE-ISSUE | step | 50 | error_handler | handled->QTPL.RETURN-ISSUES | none | stop | Any validation, lookup, dependency, defaulting, or design check fails or requires explicit reference-value approval before continuation |
| QTPL.READY | terminal | 60 | terminal | none | QTPL.ENFORCE-DESIGN | stop | The Questionnaire Templates request is ready for immutable HDL preview, not authorized import |
| QTPL.RETURN-ISSUES | terminal | 70 | terminal | none | QTPL.HANDLE-ISSUE | stop | An issue has been classified and disclosed |
