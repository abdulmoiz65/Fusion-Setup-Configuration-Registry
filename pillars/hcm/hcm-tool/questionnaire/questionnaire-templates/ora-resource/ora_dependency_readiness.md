# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Live Questionnaire Template HDL contract | Resolve the current root, translation, child, attribute, key, operation, and content contract before rendering any DAT row. |
| 2 | Subscriber and authoritative existing template identity | Resolve one exact subscriber; for change, resolve one full template and hierarchy rather than relying on its lightweight LOV row. |
| 3 | Sections and reusable or embedded questions | Confirm a complete ordered hierarchy, explicit existing/new child intent, immutable existing-child keys, and each referenced question in the same subscriber; embedded creation requires separate explicit intent. |
| 4 | Owner, response formats, scoring, attachments, and language | Resolve only the controls and references applicable to the approved design and current live schema. |
| 5 | Mutability and downstream questionnaire usage | For every update, prove exact root and per-component mutability. For in-use, hierarchy, or lifecycle changes, require complete current impact evidence beyond the partial direct-usage REST view. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| hdl_contract | Live Questionnaire Template HDL contract | Yes | HDL is the selected mutation route | Verify | Current target Data Loader metadata collection and its returned detail/template links | resolve_template_hdl_contract | Transport schema and operations are target- and release-specific | Refresh the live contract immediately before preview | DAT discriminator, hierarchy, attributes, keys, mandatory indicators, operations, and template evidence |
| subscriber | Questionnaire subscriber | Yes | Always | Verify | Current approved target subscriber export or exact readback supplied in task context | resolve_template_subscriber | Every template belongs to one subscriber boundary | Provide one exact target SubscriberName | Sanitized subscriber evidence |
| reference_suggestion | Approval-bound reference correction | Conditional | A declared suggestion-capable reference returns zero exact matches | Approval required | Complete authorized target candidate catalog after subscriber, parent, capability, active/effective, and permission restrictions | propose_reference_value | A probable value cannot enter the template DAT until explicitly approved and exactly revalidated | Review at most three exact target candidates and approve one complete value or compatible value set | Raw value, ranked candidates, fingerprints, approval state, and exact post-approval recheck |
| identity_state | Existing template identity, hierarchy, version, mutability, and duplicate state | Yes | Any create, change, new-version, inactivate, remove, or validate request is prepared | Verify | Current approved full target template and hierarchy readback plus submitted keys, child intent, and changed-field set | resolve_template_existing_identity | Correct operation classification and safe preservation require authoritative full-resource identity, exact child cardinality, immutable keys, and current emitted values | State the operation intent and complete template key; for change, identify root/child changes and each child as existing or new | Operation classification, full identity, current state, version, mutability, changed-versus-preserved values, child match report, and duplicate evidence |
| questions | Same-subscriber reusable question versions | Conditional | Existing Question Library questions are placed | Verify | Current approved target Question Library readback | resolve_template_question_version | A placement must resolve one active compatible question version in the same subscriber | Provide exact QuestionCode and QstnVersionNum values | Sanitized question-version evidence |
| embedded_category | Embedded-question category and capability | Conditional | A missing question is intentionally created in the template hierarchy | Verify | Current approved target category/readback and live HDL hierarchy | resolve_template_category | Embedded creation is not implied by a missing reusable question | Provide explicit creation intent and one exact compatible category | Sanitized category and embedded-creation capability evidence |
| owner | Template owner | Yes | Always | Verify | Current approved target person/owner readback | resolve_template_owner | The Questionnaire Templates service is not queried with an ownerless header in this workflow | Provide one target OwnerPersonNumber | Sanitized owner evidence |
| response_formats | Allowed response formats and placement overrides | Conditional | Format controls or a placement override is supplied | Verify | Current approved target format and placement LOV/readback | resolve_template_response_format | Values and compatibility vary by target and question type | Supply the intended exact target values | Canonical response-format and placement response-type evidence |
| scoring | Calculation rule, rating model, and levels | Conditional | Scoring or rating values are supplied | Verify | Current approved target scoring and rating readback | resolve_template_scoring | Scoring must be coherent with the final hierarchy | Supply exact target scoring values and final answer design | Sanitized calculation, model, level, and hierarchy evidence |
| language | Installed language and template translation parent | Conditional | Translation data is supplied | Verify | Current approved target language and template readback | resolve_template_language | Translation requires a complete TemplateFlag-aware parent key | Provide QuestionnaireCode, VersionNumber, SubscriberName, TemplateFlag Y, and Language | Sanitized language and parent evidence |
| downstream_usage | Derived questionnaires and exact mutability state | Conditional | Any change is requested; complete impact is mandatory for in-use hierarchy/lifecycle change, inactivation, or removal | Verify | Current approved target questionnaire, full template-state, and release-specific mutability evidence | resolve_template_downstream_usage | Existing use can constrain individual fields, hierarchy operations, and lifecycle changes; the declared live REST usage resolver is partial | Supply current usage, seeded, locked, in-use, hierarchy, and per-field/per-component mutability evidence | Sanitized usage, impact, and exact editable-operation evidence |
| fsm_evidence | Setup migration baseline integrity | Conditional | An FSM export is used as authoring or reconciliation evidence | Verify | The same immutable approved FSM bundle | verify_fsm_template_evidence | Template migration evidence is a two-part graph and must remain intact | Keep metadata and both graphs together; never submit the bundle as this task's current mutation artifact | Checksum, graph/schema match, orphan report, and baseline counts |

## HDL Hierarchy Order

For QuestionnaireTemplate.dat, prepare the live-registered root before Section, Section before Question, Question before Answer, and TemplateAttachment only after its template parent. Process QuestionnaireTemplateTranslation.dat only after the TemplateFlag-aware parent key resolves. File order never repairs a missing parent.

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every applicable dependency has one exact compatible match and the live HDL contract is current | Yes, artifact preparation only |
| Blocked | Metadata, identity, parent, reference, current state, or operation is missing, ambiguous, stale, or incompatible | No |
| Approval required | A declared reference candidate has been proposed but no exact value has been explicitly approved and revalidated | Read-only candidate and exact-reference lookups only; no DAT preparation or upload |
| Lifecycle review | Derived questionnaires or in-use/seeded hierarchy may be affected, or exact editable fields/operations are unproven | No mutation until complete impact and mutability review and renewed approval |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QTPL.CHECK-DEPENDENCIES | decision | 20 | resolve_dependency | ready->QTPL.APPLY-DEFAULTS;approval_required->QTPL.HANDLE-ISSUE;blocked->QTPL.HANDLE-ISSUE | QTPL.VALIDATE-INPUT | stop | Resolve required dependencies and stop for explicit approval when an eligible reference has only suggested exact catalog candidates |
