# Input Validation

Live target Data Loader metadata owns the HDL filename discriminator, component hierarchy, attributes, user keys, mandatory indicators, and operations. The approved runbook, field matrix, supplied DAT files, and FSM export are authoring evidence only and must not override the current target contract.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Request context | Requested business operation and approved source material | Stop before artifact preparation | Supply the operation intent and approved prompt, spreadsheet, DAT, setup export, or specification; FSCR is the default target environment | Always | |
| Live HDL contract | Exact Question business-object registration, downloadable template, components, attributes, user keys, mandatory indicators, and registered operations | Stop before normalizing or rendering DAT rows | Resolve the current target contract and follow all pages and returned detail or template links | HDL is the selected mutation route | resolve_question_hdl_contract |
| Question identity | SubscriberName, QuestionCode, QstnVersionNum | Stop before dependency checks | Supply the complete portable user key; do not substitute a source reference or surrogate ID | Always | |
| Operation intent | Create, change, new version, inactivate, remove, or validate | Stop before duplicate and target-state checks | State the intended business effect separately from the HDL instruction | Always | |
| Update contract | Exact existing root readback, UpdateAllowedFlag, immutable portable keys, non-empty changed-field set, every emitted current value, affected-child intent and readback | Stop before DAT rendering | Resolve exactly one current question/version and every affected existing child; identify changed versus preserved values explicitly | Change intent is selected | resolve_question_existing_identity |
| Question definition | QuestionText; exact or raw QuestionType and ResponseTypeName values, or enough explicit response-design evidence to rank target pairs; CategoryName when required; Status; PrivacyFlag; OwnerPersonNumber when required | Stop before dependency readiness and DAT rendering. Candidate lookup may proceed only when raw values or explicit design evidence can support a suggestion. | Supply the intended business definition. When either type value is blank or non-exact but the request contains enough response-design evidence, obtain current target candidates, present the probable exact pairs, and wait for explicit approval of one pair. | A Question row is prepared | propose_question_response_type_pair |
| Choice answer definition | AnswerCode, SequenceNumber, LongText, optional ShortText, scoring and feedback fields | Stop before dependency checks | Supply one complete Answer row per intended choice using a stable answer code and deterministic sequence | A choice-based question is prepared | |
| Conditional or scoring definition | ConditionDisplay and complete controlling key; ScoredFlag and complete score or rating-model design | Stop before dependency checks | Supply all related fields as one coherent design; do not infer them from wording or order | Conditional display or scoring is requested | |
| Recruiting context identity | Parent question key and exactly one supported LocationName, OrganizationName, JobFunction, or JobFamilyName value. For OrganizationName, provide canonical organizationsLOV evidence rather than a Recruiting hierarchy display label. | Stop before dependency checks | Supply one supported context dimension per QuestionContext row; resolve organization through the two-hop Recruiting organization contract | A Recruiting context is supplied | resolve_live_recruiting_question_context |
| Attachment content | Live-registered attachment component, complete title and file metadata, and packaged content | Stop before dependency checks | Supply every field required by the live component and package content under the required content folder | A question or answer attachment is supplied | resolve_question_hdl_contract |
| Translation identity | QuestionCode, QstnVersionNum, SubscriberName, Language, translated QuestionText | Stop before translation preparation | Supply the complete parent and installed-language key; use a separate translation DAT only when the target registers it | Translation data is supplied | resolve_question_language |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The live Question HDL registration or template cannot be resolved exactly | Blocked | Refresh target metadata; do not use a sample DAT as the current schema | resolve_question_hdl_contract |
| A required portable identity, parent key, operation intent, or content group is absent | Blocked | Correct only the missing input before reference resolution | |
| Input shape and live schema are valid | Verify | Evaluate the task-local dependency rules and operation-aware target identity checks | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| DAT schema | Reject an unknown filename discriminator, component, attribute, duplicate attribute, or attribute not registered for the selected operation | Any HDL DAT is prepared | resolve_question_hdl_contract |
| Executable serialization | Reject a DAT that was not emitted by the parent Questionnaire serializer and bound to a `status: passed` validation receipt with exact metadata/value parity, round-trip success, and the candidate SHA-256 | Any HDL DAT is prepared | resolve_question_hdl_contract |
| Operation registration | Reject an instruction not registered for its exact root, child, or translation business object; do not invent UPDATE or assume DELETE | Any data-operation row is prepared | resolve_question_hdl_contract |
| Question business key | Require QuestionCode, QstnVersionNum, and SubscriberName in the exact case-sensitive attributes registered by the target | A Question row is prepared | |
| Generated identifiers | Reject QuestionId, AnswerId, QuestionContextId, RatingModelId, attachment IDs, or another generated target identifier unless the selected existing-target operation explicitly requires it | A generated-ID attribute is populated | |
| Root content shape | Reject blank QuestionText, invalid Y or N flags, or values exceeding live lengths and formats. A blank or non-exact QuestionType or ResponseTypeName may enter the approval-bound suggestion flow, but remains invalid for DAT rendering until one exact target pair is approved and revalidated. | A Question row is prepared | resolve_question_response_type |
| Question and response type correction | Preserve the raw values, propose at most three exact permitted compatible target pairs, and require explicit approval of one complete pair. Reject silent normalization, partial-field approval, an unbound approval, a type absent from the target allow-list, or an approved pair that no longer passes the exact live lookups. | QuestionType or ResponseTypeName is blank or the pair has zero exact matches | propose_question_response_type_pair |
| Category and owner shape | Require CategoryName for normal question creation unless a confirmed target subscriber exception applies; require OwnerPersonNumber when PrivacyFlag is Y or target policy requires it | A question is created or made private | |
| Range and date shape | Reject negative or reversed length, selection, threshold, date, or random-sample bounds and values that exceed the available answer population | Related bounds are supplied | |
| Answer shape | Reject an Answer without the complete parent key, AnswerCode required by the live HDL key, positive unique SequenceNumber, or nonblank LongText | An Answer row is supplied | |
| Submitted AnswerCode uniqueness | Reject a DAT when an AnswerCode occurs more than once anywhere in its Answer rows, including under different QuestionCode, QstnVersionNum, or SubscriberName values; the uniqueness boundary is the complete DAT | A Question.dat contains Answer rows | validate_submitted_answer_code_uniqueness |
| Target AnswerCode availability | For create or a new Answer in an update, require zero target matches. For an affected existing Answer in an update, require exactly one match beneath the same resolved question/version and preserve its immutable AnswerCode. A match under another parent, an undeclared existing-child match, or multiple matches blocks preview. | A Question.dat import contains Answer rows | resolve_live_question_answer_code_uniqueness |
| AnswerCode correction proposal | Require the affected QuestionCode, QstnVersionNum, nonblank original AnswerCode, and invalidity reason before proposing a replacement; do not propose a value for a blank or format-invalid source code | An AnswerCode uniqueness failure is being corrected | propose_question_specific_answer_code |
| Conditional key shape | Require ConditionQuestionCode, ConditionQstnVersionNum, and ConditionAnswerCode together when ConditionDisplay is Y; reject a partial controlling key | Conditional display is supplied | |
| Recruiting context shape | Reject a QuestionContext with no dimension, more than one dimension, or an incomplete parent question key. When OrganizationName is populated, require one passed canonical organizationsLOV evidence record bound to that exact QuestionContext key; reject a recruitingOrganizationsLOV hierarchy display name and any persisted OrganizationId. | A QuestionContext row is supplied | resolve_live_recruiting_question_context |
| Attachment shape | Reject a local absolute path, missing packaged content, incomplete add or replacement metadata, or an attachment component absent from the live schema | Attachment data is supplied | resolve_question_hdl_contract |
| Translation shape | Reject an unregistered translation object, unknown attribute, incomplete parent-language key, blank translated QuestionText, or unsupported instruction | Question translation data is supplied | resolve_question_hdl_contract |
| Source references | Treat live-registered SourceRef attributes as optional correlation values only; reject their use as a substitute for the portable question key unless the live object explicitly registers that key | Source reference values are supplied | resolve_question_hdl_contract |
| Load content | Treat COMMENT and METADATA-only content as a schema template; require at least one registered data-operation row for an import artifact | HDL import is requested | |
| Question lifecycle and portability | Require QuestionCode, QstnVersionNum, SubscriberName, QuestionText, target-valid Status, PrivacyFlag, and an exact response-compatible QuestionType/ResponseTypeName pair, supplied directly or explicitly approved from current target candidates; reject copied QuestionId, owner IDs, rating IDs, audit fields, source references, and JSON booleans | A Question row is supplied | resolve_question_subscriber |
| Question lifecycle controls | First version is 1; later versions are sequential; UpdateAllowed is target-valid and preserved unless the supported operation explicitly changes it; reject AdhocFlag create, change, or removal | A Question lifecycle field is supplied | resolve_question_existing_identity |
| Question update preservation | Require exactly one existing root and UpdateAllowedFlag=true; reject changes to SubscriberName, QuestionCode, QstnVersionNum, or any affected child user key; require a non-empty explicit changed-field set; require each changed field to be mutable under the live MERGE contract; and require every emitted unchanged value to equal exact current readback. Omitted children are preserved and never mean delete. | Change intent is selected | resolve_question_existing_identity |
| Status-only inactivation | Permit `partial_no_visible_usage` only for explicit `inactivate` intent when one active/latest/updateable Question is resolved, target-valid inactive Status is the sole changed field, all other emitted root values are exact current readback, no child rows are emitted, every declared visible downstream lookup completed with zero matches, no returned state is seeded/locked/in-use, and an impact-bound approval is current. Rerun each check after approval. | A Question is inactivated | resolve_question_downstream_usage |
| Question conditional, choice, and score bounds | Require the complete controlling question/version/answer key when ConditionDisplay is Y; validate text lengths, date bounds, selection bounds, response random sample size, scoring thresholds, rating model, and comments only for compatible question/response types | Related field is supplied | resolve_question_response_type |
| Recruiting context and answer design | Restrict Recruiting-only flags, candidate/classification values, contexts, and additional questionnaire links to compatible Recruiting evidence. For an organization context, retain the Recruiting discovery value only for selection and emit the active canonical organizationsLOV.Name; require unique positive answer sequence, exact AnswerCode, required LongText, and coherent score/correctness/attachment data | QuestionContext or Answer row is supplied | resolve_recruiting_question_context |

## HDL DAT Contract

| File | Root Component | Supported Child Scope | Identity and Pairing Contract |
|---|---|---|---|
| Question.dat | Exact root returned by live metadata, expected from current evidence to be Question | Answer, QuestionContext, and attachment components only when the current target registers them | Pair every child with SubscriberName, QuestionCode, and QstnVersionNum plus its registered child key; parents precede children |
| QuestionTranslation.dat | Exact translation root returned by live metadata | None unless the current target template declares otherwise | Match one loaded question using SubscriberName, QuestionCode, QstnVersionNum, and Language; never invent a separate answer-translation DAT |

Use the exact current target METADATA lines and attribute order when rendering. The supplied DAT establishes candidate names only. Escaping, null handling, date formatting, content packaging, and operation-specific mandatory attributes must follow the current template and common Data Loader contract.

## Approval-Bound Suggestion Validation

| Check | Rule |
|---|---|
| Entry condition | Suggestion handling is allowed only after the declared exact resolver returns zero matches for a suggestion-capable value. Multiple exact matches remain ambiguous. |
| Candidate evidence | Require a complete documented and authorized target catalog, all subscriber/parent/capability restrictions, at most three exact returned candidates, a catalog timestamp, source-request fingerprint, and candidate-set fingerprint. |
| Pending state | Preserve the raw input and stop DAT rendering until the user explicitly approves one complete exact value or compatible value set. |
| Approved state | Require approval bound to the target, task, portable parent key, original value, exact candidate, catalog and fingerprints; rerun the original exact resolver immediately before preview. |
| Exact-only values | Reject suggestion use for Data Loader registration, portable create/update identity, QstnVersionNum, OwnerPersonNumber, AnswerCode uniqueness, generated IDs, lifecycle/usage evidence, and returned links. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QLIB.VALIDATE-INPUT | step | 10 | validate_input | valid->QLIB.RESOLVE-REFERENCES;invalid->QLIB.HANDLE-ISSUE | none | stop | Always |
