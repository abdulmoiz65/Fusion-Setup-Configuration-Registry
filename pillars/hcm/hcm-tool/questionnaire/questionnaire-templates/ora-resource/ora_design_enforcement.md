# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce target contract and identity | Use the current live schema, exact template key, explicit operation intent, and one subscriber boundary. |
| 2 | Enforce hierarchy and controls | Require a complete ordered section/placement hierarchy and validate response, scoring, attachment, and translation behavior against the live contract. |
| 3 | Enforce lifecycle and approval safety | Classify create versus change correctly, review derived-questionnaire impact, and bind approval to one immutable DAT preview. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| HDL DAT preparation is requested | Blocker | resolve_template_hdl_contract | The current root, translation, component, attribute, key, operation, or content contract is missing or differs from the proposed DAT | Regenerate from current target metadata; never treat the supplied schema template as current registration proof | Yes |
| Always | Blocker | resolve_template_subscriber | SubscriberName is missing, ambiguous, or incompatible with another supplied reference | Correct the exact target subscriber boundary | Yes |
| A declared suggestion-capable reference has zero exact matches | Blocker | propose_reference_value | The authorized candidate catalog is incomplete, restrictions were not applied, more than three candidates are shown, approval is absent or stale, or the approved value fails the original exact resolver and compatibility checks | Follow the parent approval-bound suggestion contract; never treat a probable value as valid input | Yes, only after explicit candidate approval and exact revalidation |
| Create, change, new-version, inactivate, remove, or validation intent is supplied | Blocker | resolve_template_existing_identity | The target match count conflicts with the intent, submitted keys collide, or current version/state evidence is absent | Correct the intent or key; never turn a create collision into an implicit update | Yes |
| Change intent is supplied | Blocker | resolve_template_existing_identity | Only an LOV identity is available; the full template or affected hierarchy is unresolved; root or child keys change; the aggregate changed-field set is empty; a changed field or child operation is not proven mutable; an emitted unchanged value lacks current readback; a new child collides; or omission is treated as deletion, movement, resequencing, or replacement | Use one authoritative full-template readback, preserve immutable keys and omitted children, classify affected children as existing or new, and bind exact changes to a target-registered MERGE | Yes |
| The template is in use or usage is unresolved | Blocker | resolve_template_downstream_usage | Current release-specific editable fields/operations or complete impact evidence for a requested hierarchy/lifecycle change is unavailable; only partial direct-usage REST evidence exists | Restrict the change to proven editable fields or stop until complete mutability and downstream-impact evidence is available | Yes, only where the exact current state permits |
| A new template hierarchy is prepared | Blocker |  | No section exists, section or placement order is duplicated, a parent key is incomplete, or required names are blank | Supply one complete deterministic hierarchy using the live component contract | Yes |
| An existing Question Library question is placed | Blocker | resolve_template_question_version | The question version is missing, inactive, incompatible, or cross-subscriber | Use one exact active same-subscriber reusable question version | Yes |
| An embedded question is intentionally created | Blocker | resolve_template_category | Creation intent is absent, live embedded-creation support is unproven, category is incompatible, or the new question definition is incomplete | Create through this hierarchy only when explicitly approved and fully supported; otherwise create through Question Library first | Yes |
| Always | Blocker | resolve_template_owner | OwnerPersonNumber is absent, ambiguous, inactive, or not permitted for the subscriber | Supply one target OwnerPersonNumber before a template-service lookup or DAT rendering | Yes |
| Allowed response formats or a placement override is supplied | Blocker | resolve_template_response_format | A value is not registered, an override is incompatible, or FSM codes/row presence are converted into guessed HDL values | Use only exact target format and placement values compatible with the referenced questions | Yes |
| Scoring or a rating model is supplied | Blocker | resolve_template_scoring | Calculation rule, model, level, answer score, threshold, or maximum-score design is missing or inconsistent | Reconcile scoring against the final placed-question and answer hierarchy | Yes |
| Section presentation or randomization is supplied | Blocker |  | Section/question/response order, sample sizes, mandatory counts, or page controls are internally inconsistent | Recalculate from the final hierarchy and use only current target codes | Yes |
| Translation data is supplied | Blocker | resolve_template_language | The translation object is unregistered or QuestionnaireCode, VersionNumber, SubscriberName, TemplateFlag Y, and Language do not resolve one parent | Correct the complete parent-language key or exclude the translation | Yes |
| Attachment data is supplied | Blocker | resolve_template_hdl_contract | Component/operation is unregistered, metadata is incomplete, file/URL mode is invalid, or packaged content is missing | Use only the current attachment contract and package content correctly | Yes |
| A lifecycle-sensitive or destructive action is requested | Blocker | resolve_template_downstream_usage | Derived questionnaires, seeded/in-use hierarchy, or destructive impact is unresolved, or approval is absent | Preserve or inactivate where supported; otherwise obtain a new impact-bound approval | Yes, only where the live contract permits |
| FSM evidence is used | Blocker | verify_fsm_template_evidence | Either backing or configuration graph is missing, the package is altered/orphaned, or it is being used as this task's mutation artifact | Restore the immutable two-part baseline and derive HDL only after validation | Yes |

Rules such as one ad hoc section, DateResponse update limitations, Talent Review restrictions, and exact in-use editable attributes are blocking only when current source, target metadata, or runtime evidence for the selected release proves them. Do not preserve dated findings as universal policy.

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_template_hdl_contract | Before any HDL schema, operation, attachment, or translation decision | Current discriminator, components, attributes, keys, operations, mandatory indicators, and templates | ora_reference_lookups.md |
| resolve_template_subscriber | For every template request | Exact target subscriber evidence | ora_reference_lookups.md |
| propose_reference_value | When a declared suggestion-capable reference has zero exact matches | Raw value, restricted target candidates, catalog timestamp, fingerprints, explicit approval, and exact post-approval recheck | ora_reference_lookups.md and parent reference-value suggestion contract |
| resolve_template_existing_identity | For operation and duplicate classification | Target and in-batch match counts, version, state, and supported lifecycle | ora_reference_lookups.md |
| resolve_template_question_version | When an existing reusable question is placed | Active compatible same-subscriber question key | ora_reference_lookups.md |
| resolve_template_category | When embedded creation is requested | Exact category and current embedded-creation capability | ora_reference_lookups.md |
| resolve_template_owner | For every template header | Exact OwnerPersonNumber evidence | ora_reference_lookups.md |
| resolve_template_response_format | When format controls or placement override is supplied | Exact target format and placement response values | ora_reference_lookups.md |
| resolve_template_scoring | When scoring or rating behavior is supplied | Calculation rule, model, levels, final hierarchy, and score evidence | ora_reference_lookups.md |
| resolve_template_language | When translation data is supplied | Installed language and exact TemplateFlag-aware parent key | ora_reference_lookups.md |
| resolve_template_downstream_usage | For lifecycle-sensitive or destructive changes | Derived questionnaire, seeded, in-use, and hierarchy impact evidence | ora_reference_lookups.md |
| verify_fsm_template_evidence | When FSM evidence is used | Immutable two-part graph, metadata, schema, hierarchy, and orphan report | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QTPL.ENFORCE-DESIGN | decision | 40 | design_enforcement | compliant->QTPL.READY;blocked->QTPL.HANDLE-ISSUE | QTPL.APPLY-DEFAULTS | stop | Always |
