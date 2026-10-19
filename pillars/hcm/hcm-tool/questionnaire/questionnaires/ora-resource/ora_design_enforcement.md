# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce target contract and identity | Use the current live schema, complete versioned key, explicit operation intent, and one subscriber boundary. |
| 2 | Enforce conditional template and hierarchy design | Require a template only when supplied or live-required, then validate the complete section, placement, answer, scoring, attachment, and translation hierarchy. |
| 3 | Enforce lifecycle, consumer, and approval safety | Review current use and destructive impact, keep consumer linkage separate, and bind approval to one immutable DAT preview. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| HDL DAT preparation is requested | Blocker | resolve_questionnaire_hdl_contract | The current root, translation, component, attribute, key, operation, or content contract is missing or differs from the proposed DAT | Regenerate from current target metadata; never treat supplied DAT as registration proof | Yes |
| Always | Blocker | resolve_questionnaire_subscriber | SubscriberName is missing, ambiguous, or incompatible with another supplied reference | Correct the exact target subscriber boundary | Yes |
| A declared suggestion-capable reference has zero exact matches | Blocker | propose_reference_value | The authorized candidate catalog is incomplete, restrictions were not applied, more than three candidates are shown, approval is absent or stale, or the approved value fails the original exact resolver and compatibility checks | Follow the parent approval-bound suggestion contract; never treat a probable value as valid input | Yes, only after explicit candidate approval and exact revalidation |
| Create, change, new-version, inactivate, remove, or validation intent is supplied | Blocker | resolve_questionnaire_existing_identity | Target match count conflicts with intent, submitted keys collide, later version is not sequential, or required current-state evidence is absent | Correct intent or key; never turn a create collision into an implicit update | Yes |
| Change intent is supplied | Blocker | resolve_questionnaire_existing_identity | The full versioned questionnaire or affected hierarchy is unresolved; latest/update permission or current state is unproven; root or child keys change; the aggregate changed-field set is empty; a changed field or child operation is not proven mutable; an emitted unchanged value lacks current readback; a new child collides; template linkage changes without proof; or omission is treated as deletion, movement, resequencing, or replacement | Use one authoritative full-questionnaire readback, preserve immutable keys, omitted children, and default template linkage, classify affected children as existing or new, and bind exact changes to a target-registered MERGE | Yes |
| The questionnaire is in use, has responses, or either state is unresolved | Blocker | resolve_questionnaire_usage_state | Current release-specific editable fields/operations or complete impact evidence for requested hierarchy, scoring, template-linkage, status, or lifecycle change is unavailable; only partial lifecycle REST evidence exists | Restrict the change to proven editable fields or stop until complete mutability, response, and downstream-impact evidence is available | Yes, only where the exact current state permits |
| CategoryName is supplied or live-required | Blocker | resolve_questionnaire_category | Category is missing, incompatible, cross-subscriber, or an exception is assumed without current target proof | Use one exact compatible category or omit it only when the target contract permits | Yes |
| TemplateQstnrCode is supplied or live-required | Blocker | resolve_questionnaire_template | Template is missing, inactive, incompatible, incomplete, ambiguous, or cross-subscriber | Use one exact active compatible same-subscriber template | Yes |
| No template is supplied and the current contract does not require one | Warning |  | A template is being synthesized solely because an older HDL sample required it | Preserve explicit template-less intent and omit the reference | Yes |
| A new or changed hierarchy is prepared | Blocker |  | Required Section is absent, sequence is duplicated, a parent key is incomplete, or randomization/presentation counts conflict | Supply the complete deterministic hierarchy required by the selected operation | Yes |
| A reusable question is placed | Blocker | resolve_questionnaire_question_version | Question version is missing, inactive, incompatible, or cross-subscriber | Use one exact active same-subscriber question version | Yes |
| A direct Question is requested | Blocker | resolve_questionnaire_direct_question_contract | The request is not `mode: direct` with QuestionType `TEXT`, `1CHOICE`, `MULTCHOICE`, or `NONE`, or the target Question/conditional Answer component, MERGE operation, hierarchy, parent keys, attributes, category, response type, template capability, type/answer rules, or executable-procedure evidence is missing, ambiguous, or unregistered | Resolve the current target contract and complete the executable direct-question procedure before generating Questionnaire.dat | Yes |
| A placement response override is supplied | Blocker | resolve_questionnaire_response_type | Override is unavailable or incompatible; blank inherited response is being treated as missing | Use the exact target override or leave blank to inherit | Yes |
| PrivacyFlag is Y or owner is required | Blocker | resolve_questionnaire_owner | No exact permitted active owner resolves | Supply one target OwnerPersonNumber | Yes |
| Scoring, rating, thresholds, or maximum score is supplied | Blocker | resolve_questionnaire_scoring | Final placed questions, answers, calculation rule, rating values, thresholds, or maximum score are incomplete or inconsistent | Reconcile scoring from the final hierarchy using target-supported values | Yes |
| Answer overrides are supplied | Blocker | resolve_questionnaire_hdl_contract | An unregistered operation is used, the parent placement is missing, or final scoring cannot be recalculated | Use only registered operations and include the complete approved answer override set required by the live contract | Yes |
| LayoutOption is supplied | Blocker | resolve_questionnaire_subscriber | Current target subscriber and transport evidence does not support LayoutOption | Remove it or provide current target support evidence; never use a copied numeric subscriber ID | Yes |
| Translation data is supplied | Blocker | resolve_questionnaire_language | Translation object is unregistered or QuestionnaireCode, VersionNumber, SubscriberName, TemplateFlag N, and Language do not resolve one parent | Correct the complete parent-language key or exclude the translation | Yes |
| Attachment data is supplied | Blocker | resolve_questionnaire_hdl_contract | Component or operation is unregistered, replacement behavior is unproven, metadata is incomplete, or packaged content is missing | Use only the current attachment contract and disclose any proven destructive replacement effect | Yes |
| A lifecycle-sensitive or destructive action is requested | Blocker | resolve_questionnaire_usage_state | Responses, in-use state, seeded provenance, template usage, hierarchy impact, or destructive approval is unresolved | Preserve, version, or inactivate where supported; otherwise obtain new impact-bound approval | Yes, only where the live contract permits |
| A consuming object is identified | Warning |  | Consumer linkage is included in the Questionnaire HDL package | Verify the questionnaire first, then hand off to the separately owned consumer task | Yes |
| FSM evidence is used | Blocker | verify_fsm_questionnaire_evidence | The ordinary-questionnaire graph is incomplete, altered, orphaned, has an undisclosed fidelity gap, or is used as the mutation artifact | Restore the immutable baseline, disclose omitted children, and derive HDL only after validation | Yes |

Talent Review restrictions, exact in-use editable attributes, Answer delete limitations, attachment delete-and-recreate behavior, and subscriber-specific LayoutOption rules are blocking only when current source, target metadata, or runtime evidence for the selected release proves them.

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_questionnaire_hdl_contract | Before any HDL schema, operation, attachment, answer, or translation decision | Current discriminator, components, attributes, keys, operations, mandatory indicators, and templates | ora_reference_lookups.md |
| resolve_questionnaire_subscriber | For every questionnaire and LayoutOption applicability decision | Exact target subscriber evidence | ora_reference_lookups.md |
| propose_reference_value | When a declared suggestion-capable reference has zero exact matches | Raw value, restricted target candidates, catalog timestamp, fingerprints, explicit approval, and exact post-approval recheck | ora_reference_lookups.md and parent reference-value suggestion contract |
| resolve_questionnaire_existing_identity | For operation and duplicate classification | Target/in-batch match counts, latest version, state, and lifecycle evidence | ora_reference_lookups.md |
| resolve_questionnaire_category | When category is supplied or live-required | Exact compatible category and exception evidence where applicable | ora_reference_lookups.md |
| resolve_questionnaire_template | When template is supplied or live-required | Exact active compatible same-subscriber template key | ora_reference_lookups.md |
| resolve_questionnaire_question_version | When a reusable question is placed | Active compatible same-subscriber question key | ora_reference_lookups.md |
| resolve_questionnaire_direct_question_contract | When a direct Question is requested | Target Question and conditional Answer component and operation evidence plus approved executable procedure | ora_reference_lookups.md |
| resolve_questionnaire_response_type | When placement override is supplied | Exact compatible QstnrQstnResponseTypeName | ora_reference_lookups.md |
| resolve_questionnaire_owner | When privacy or subscriber policy requires owner | Exact OwnerPersonNumber evidence | ora_reference_lookups.md |
| resolve_questionnaire_scoring | When scoring or rating behavior is supplied | Final hierarchy, calculation, rating, threshold, and score evidence | ora_reference_lookups.md |
| resolve_questionnaire_language | When translation data is supplied | Installed language and exact TemplateFlag N parent key | ora_reference_lookups.md |
| resolve_questionnaire_usage_state | For lifecycle-sensitive or destructive changes | Response, in-use, seeded, template-usage, and hierarchy-impact evidence | ora_reference_lookups.md |
| verify_fsm_questionnaire_evidence | When FSM evidence is used | Immutable ordinary-questionnaire graph, metadata, schema, hierarchy, omissions, and orphan report | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QNR.ENFORCE-DESIGN | decision | 40 | design_enforcement | compliant->QNR.READY;blocked->QNR.HANDLE-ISSUE | QNR.APPLY-DEFAULTS | stop | Always |
