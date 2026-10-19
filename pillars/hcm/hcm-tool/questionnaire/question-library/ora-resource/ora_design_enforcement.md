# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce target contract and identity | Use the live Question HDL schema, complete versioned key, explicit business operation, and exact subscriber boundary. |
| 2 | Enforce question, answer, context, and attachment design | Confirm type compatibility, coherent choices and scoring, complete conditional links, subscriber-appropriate contexts, and registered content components. |
| 3 | Enforce lifecycle and approval safety | Classify create versus change correctly, review current state and dependencies, and bind approval to one immutable DAT preview. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| HDL DAT preparation is requested | Blocker | resolve_question_hdl_contract | The current registration, template, component, attribute, user key, operation, or content contract is missing or differs from the proposed DAT | Regenerate the DAT from the current live contract; treat supplied templates as candidate evidence only | Yes |
| Always | Blocker | resolve_question_subscriber | SubscriberName is missing, ambiguous, or incompatible with another supplied reference | Correct the exact target subscriber boundary | Yes |
| A declared suggestion-capable reference has zero exact matches | Blocker | propose_reference_value | The authorized candidate catalog is incomplete, restrictions were not applied, more than three candidates are shown, approval is absent or stale, or the approved value fails the original exact resolver and compatibility checks | Follow the parent approval-bound suggestion contract; never treat a probable value as valid input | Yes, only after explicit candidate approval and exact revalidation |
| A question is created or CategoryName is supplied | Blocker | resolve_question_category | A required category is missing, cannot contain questions, or belongs to another subscriber; no current target exception is proven | Use one exact compatible target category or document the confirmed target exception | Yes |
| QuestionType or ResponseTypeName is blank, non-exact, or supplied | Blocker | resolve_question_response_type | The final pair is unavailable or incompatible, an FSM response code is being used as an HDL name, a probable pair has not been explicitly approved, or the approved pair fails its immediate permitted-type or exact-pair live recheck | Resolve exact target candidates, approve one complete pair when correction is needed, and validate the approved pair together before preview | Yes, only after exact-pair approval when correction is needed |
| A choice-based design is supplied | Blocker | resolve_live_question_answer_code_uniqueness | No valid answers exist, an AnswerCode is duplicated in the DAT, a create or new-child AnswerCode already exists, an existing update-child code does not resolve exactly once beneath the same question/version, or length/date/selection controls conflict with the final answer population | Use question-specific AnswerCode values, retain display labels such as Yes and No in LongText, and validate every submitted code with operation-aware identity rules before preview | Yes |
| An AnswerCode fails uniqueness validation | Blocker | propose_question_specific_answer_code | The original code is blank or format-invalid, the composed proposal violates the live contract or either uniqueness check, or the user has not explicitly approved the exact old-to-new mapping | Show the invalidity reason and propose QuestionCode_QstnVersionNum_OriginalAnswerCode. Apply the change only after user approval, retain LongText, rerun validation, and create a new immutable preview | Yes, only after explicit mapping approval |
| Text, date, or no-response design is supplied | Blocker | resolve_question_response_type | Choice answers, scoring, selections, or incompatible length/date controls remain | Remove incompatible fields and retain only controls supported by the resolved response type | Yes |
| PrivacyFlag is Y or owner is required | Blocker | resolve_question_owner | No exact permitted active owner resolves | Supply one target OwnerPersonNumber | Yes |
| Conditional display is supplied | Blocker | resolve_controlling_question_answer | Display flag and controlling question, version, and answer do not travel together or the reference is missing, ambiguous, or cross-subscriber | Supply one complete same-subscriber controlling key | Yes |
| Scoring or a rating model is supplied | Blocker | resolve_question_rating_model | Score design, thresholds, answer values, model, or levels are incomplete, unsupported, or internally inconsistent | Reconcile the final answer and rating design using exact target values | Yes |
| Recruiting context is supplied | Blocker | resolve_recruiting_question_context | A restricted dimension has no matching context row, Recruiting-only values are used for another subscriber, or OrganizationName is a recruitingOrganizationsLOV hierarchy label rather than one active canonical organizationsLOV leaf | Resolve the complete organization through the two-hop canonicalization lookup and emit only the returned canonical leaf; otherwise add exact supported contexts or remove subscriber-inapplicable values | Yes |
| Create, change, new-version, inactivate, remove, or validation intent is supplied | Blocker | resolve_question_existing_identity | The target match count conflicts with the intent, submitted keys collide, a later version is not sequential, or required current-state evidence is absent | Correct the intent or key and use the supported lifecycle path; do not turn a create collision into an implicit update | Yes |
| Change intent is supplied | Blocker | resolve_question_existing_identity | The root is not exactly resolved, UpdateAllowedFlag is not true, a portable root or child key changes, changed fields are empty or not mutable, an emitted unchanged value lacks exact current readback, or omission is treated as child deletion | Preserve immutable keys and omitted children; bind one explicit changed-field set and exact current values to a target-registered MERGE update | Yes |
| A lifecycle-sensitive or destructive action is requested | Blocker | resolve_question_downstream_usage | Seeded, locked, in-use, template, questionnaire, or conditional dependencies are unresolved, or destructive approval is absent. The only exception is the documented Question status-only inactivation route with zero visible usage and explicit impact-bound approval. | Preserve, version, or inactivate where supported. Use the exception only for an exact active/latest/updateable Question with `Status` as its sole changed field, zero results from every declared visible dependency lookup, no child rows, and a current approval bound to that evidence. | Yes, only where the live contract permits |
| An approved status-only Question inactivation is rechecked | Blocker | compare_question_inactivation_review | Current evidence fails route eligibility or scan completeness, material approval scope changed, or a diagnostic-only change lacks a complete confirming scan | Retain business approval only for approval_retained. For rescan_required perform one read-only confirmation; for approval_required review the changed material fields; for blocked diagnose the failed check. Unrelated counts alone never demand renewed approval. | Yes, only within the documented status-only Question route |
| Translation data is supplied | Blocker | resolve_question_language | The translation object is not live-registered or the installed language and parent version do not resolve exactly | Exclude the translation or correct its exact parent-language key | Yes |
| Attachment data is supplied | Blocker | resolve_question_hdl_contract | The component or operation is unregistered, metadata is incomplete, a local path is emitted, or packaged content is absent | Use only the live attachment contract and package content correctly | Yes |
| FSM evidence is used | Blocker | verify_fsm_question_evidence | The package is incomplete, altered, orphaned, unsafe, or used as the selected mutation artifact | Restore the immutable evidence bundle and derive HDL only after it validates | Yes |

Subscriber-specific rules such as Talent Review restrictions or exact in-use editable attributes are blocking only when current source, target metadata, or target runtime evidence for the selected release proves them. Do not carry old implementation findings forward as universal rules.

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_question_hdl_contract | Before any HDL schema or operation decision | Current discriminator, components, attributes, keys, operations, mandatory indicators, and template | ora_reference_lookups.md |
| resolve_question_subscriber | For every question request | Exact target subscriber evidence | ora_reference_lookups.md |
| propose_reference_value | When a declared suggestion-capable reference has zero exact matches | Raw value, restricted target candidates, catalog timestamp, fingerprints, explicit approval, and exact post-approval recheck | ora_reference_lookups.md and parent reference-value suggestion contract |
| resolve_question_category | When category is supplied or route-required | Exact compatible category and exception evidence when applicable | ora_reference_lookups.md |
| resolve_question_response_type | When question or response type is supplied | Exact compatible QuestionType and ResponseTypeName | ora_reference_lookups.md |
| propose_question_response_type_pair | When either type value is blank or the exact pair lookup returns zero matches | Raw values, explicit response-design evidence, complete current target candidate catalog, ranked exact pairs, and pair-bound approval | ora_reference_lookups.md |
| resolve_live_question_answer_code_uniqueness | Before Question.dat preview or upload | Local duplicate report and target absence evidence for every submitted AnswerCode | ora_reference_lookups.md |
| propose_question_specific_answer_code | An AnswerCode uniqueness failure is corrected | Exact old-to-proposed mapping, invalidity reason, live-contract check, and local and target uniqueness evidence | ora_reference_lookups.md |
| resolve_question_owner | When privacy or subscriber policy requires owner | Exact OwnerPersonNumber evidence | ora_reference_lookups.md |
| resolve_question_rating_model | When scoring or rating model is supplied | Exact model, levels, and compatibility evidence | ora_reference_lookups.md |
| resolve_controlling_question_answer | When conditional display is supplied | Same-subscriber controlling question version and answer | ora_reference_lookups.md |
| resolve_recruiting_question_context | When Recruiting contexts are supplied | Complete supported work-structure key | ora_reference_lookups.md |
| resolve_question_existing_identity | For operation and duplicate classification | Target and in-batch match counts, latest version, and state | ora_reference_lookups.md |
| resolve_question_downstream_usage | For lifecycle-sensitive or destructive changes | Exact dependency, use, lock, seeded, and impact evidence | ora_reference_lookups.md |
| compare_question_inactivation_review | Only when revalidating an approved status-only Question inactivation | Approved material scope, fresh question-specific evidence, complete scan coverage and any required confirmation | ora_reference_lookups.md |
| resolve_question_language | When translation data is supplied | Installed language and exact parent version | ora_reference_lookups.md |
| verify_fsm_question_evidence | When FSM evidence is used | Immutable package, metadata, schema, hierarchy, and orphan report | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QLIB.ENFORCE-DESIGN | decision | 40 | design_enforcement | compliant->QLIB.READY;blocked->QLIB.HANDLE-ISSUE | QLIB.APPLY-DEFAULTS | stop | Always |
