# Input Validation

Live target Data Loader metadata owns the Questionnaire HDL discriminator, hierarchy, attributes, user keys, mandatory indicators, and operations. A template is required only when the selected live HDL/subscriber contract requires it; a supplied template must always resolve exactly in the same subscriber.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Request context | Target environment, target release, requested business operation, approved source material | Stop before artifact preparation | Supply target context, operation intent, and approved prompt, spreadsheet, DAT, setup export, or specification | Always | |
| Live HDL contract | Exact Questionnaire and optional translation registrations, downloadable templates, components, attributes, user keys, mandatory indicators, and registered operations | Stop before normalizing or rendering DAT rows | Resolve the current target contract and follow every page and returned detail/template link | HDL is the selected mutation route | resolve_questionnaire_hdl_contract |
| Questionnaire identity | SubscriberName, QuestionnaireCode, QstnrVersionNum | Stop before dependency checks | Supply the complete portable versioned key; do not substitute a source reference or surrogate ID | Always | |
| Operation intent | Create, change, new version, inactivate, remove, or validate | Stop before duplicate and current-state checks | State the intended business effect separately from the HDL instruction | Always | |
| Update contract | One authoritative full-questionnaire and hierarchy readback, current latest/update/in-use/seeded/locked/response state, template-linkage intent, immutable portable root and child keys, non-empty aggregate changed-field set, explicit existing/new child intent, every emitted current value, and complete impact evidence where required | Stop before DAT rendering | Resolve the full current questionnaire and affected hierarchy rows; do not treat a lightweight identity or partial lifecycle response as update authority | Change intent is selected | resolve_questionnaire_existing_identity |
| Questionnaire header | QuestionnaireName and every live-required status, InUse, privacy, owner, category, presentation, layout, instruction, scoring, and template field | Stop before dependency checks | Supply approved values using only attributes registered for the selected operation | A Questionnaire row is prepared | |
| Template reference | TemplateQstnrCode and any additional live-registered template key | Stop before dependency checks | Supply one exact active compatible same-subscriber template | A template is supplied or the live HDL/subscriber contract requires it | resolve_questionnaire_template |
| Questionnaire hierarchy | Complete parent key, Sections and SectionSeqNum, placed QuestionCode and QstnVersionNum, and QstnSequenceNumber | Stop before dependency checks | Supply the complete approved hierarchy when authored or when the selected operation requires full hierarchy | Sections or placements are included or route-required | |
| Direct Question definition | Mode `direct`; QuestionCode, QstnVersionNum, QuestionText, QuestionType `TEXT`, `1CHOICE`, `MULTCHOICE`, or `NONE`, ResponseTypeName, Status, PrivacyFlag, CategoryName, QstnSequenceNumber, Mandatory, AdhocQstn, SectionSeqNum, QuestionnaireCode, QstnrVersionNum, and SubscriberName | Stop before DAT rendering | Resolve the live direct-question and conditional Answer components, operations, parent keys, attributes, exact metadata order, category, response type, template capability, and executable procedure | A direct Question is requested instead of a reusable-question reference | resolve_questionnaire_direct_question_contract |
| Placement response override | QstnrQstnResponseTypeName | Reject an incomplete supplied override | Leave blank to inherit; when supplied, resolve the exact compatible target placement LOV value | An explicit placement override is intended | resolve_questionnaire_response_type |
| Questionnaire attachment | Live-registered attachment component, complete type, title, file or URL metadata, and packaged content where required | Stop before dependency checks | Supply all values required by the current component and operation | A QuestionnaireAttachment is supplied | resolve_questionnaire_hdl_contract |
| Translation identity | QuestionnaireCode, VersionNumber, SubscriberName, TemplateFlag, Language, and translated Name | Stop before translation preparation | Use TemplateFlag N and a separate translation DAT only when the target registers that contract | Questionnaire translation data is supplied | resolve_questionnaire_language |
| Consumer boundary | Intended consuming object or no-linkage confirmation | Stop only the downstream handoff, not questionnaire artifact preparation | Record the separately owned consumer task after questionnaire verification | A consumer linkage is requested | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The live Questionnaire HDL registration or downloadable template cannot be resolved exactly | Blocked | Refresh target metadata; do not use the supplied DAT as the current schema | resolve_questionnaire_hdl_contract |
| A route-required or supplied template cannot be resolved exactly | Blocked | Correct the template key or target contract before hierarchy preparation | resolve_questionnaire_template |
| A template is not supplied and the current live HDL/subscriber contract does not require it | Valid | Continue without inventing a template reference | |
| A required versioned root, hierarchy, parent, operation-intent, or translation key is absent | Blocked | Correct only the missing input before reference resolution | |
| Input shape and live schema are valid | Verify | Evaluate task-local subscriber, reference, duplicate, lifecycle, scoring, and hierarchy dependencies | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| DAT schema | Reject an unknown filename discriminator, component, attribute, duplicate attribute, or attribute not registered for the selected operation | Any HDL DAT is prepared | resolve_questionnaire_hdl_contract |
| Executable serialization | Reject a DAT that was not emitted by the parent Questionnaire serializer and bound to a `status: passed` validation receipt with exact metadata/value parity, round-trip success, and the candidate SHA-256 | Any HDL DAT is prepared | resolve_questionnaire_hdl_contract |
| Operation registration | Reject an instruction not registered for its exact root, child, attachment, Answer, or translation business object; do not hard-code UPDATE, assume DELETE, or infer omission as deletion | Any data-operation row is prepared | resolve_questionnaire_hdl_contract |
| Root business key | Require SubscriberName, QuestionnaireCode, and QstnrVersionNum plus any additional key returned by live metadata | A Questionnaire row is prepared | |
| Questionnaire update preservation | Require exactly one authoritative full-questionnaire match, latest/update permission where required, and proven per-field/per-component mutability; reject changes to SubscriberName, QuestionnaireCode, QstnrVersionNum, or any existing child user-key field; require at least one approved changed field across root and affected children; and require every emitted unchanged value to equal exact current readback | Change intent is selected | resolve_questionnaire_existing_identity |
| Generated identifiers | Reject QuestionnaireId, SubscriberId, QstnrTemplateId, QstnrSectionId, QstnrQuestionId, AnswerId, attachment IDs, response-type IDs, or another generated target ID unless the selected existing-target operation explicitly requires it | A generated-ID attribute is populated | |
| Root field shape | Reject blank QuestionnaireName, invalid Y or N flags, unregistered status/presentation/layout/scoring values, or values outside target length and type | A Questionnaire row is prepared | |
| Template shape | Require TemplateQstnrCode only when supplied or current live metadata marks it mandatory; reject copied template IDs or an incomplete live-registered template key | Template applicability is evaluated | resolve_questionnaire_template |
| Section shape | Require complete root key, positive unique SectionSeqNum, nonblank Name, and target-valid NewPage, QuestionOrder, ResponseOrder, Mandatory, AllowAdhoc, and random-sample values | A Section row is supplied | |
| Question placement shape | Require exact parent section, QuestionCode, QstnVersionNum, and positive unique QstnSequenceNumber; QstnrQstnResponseTypeName is optional and blank means inherit | A Question placement row is supplied | resolve_questionnaire_question_version |
| Update child identity | Require every submitted Section, reusable/direct Question, and Answer row to declare existing or new intent. Existing requires one exact complete-key match; new requires zero key matches and a registered add-through-MERGE operation. Reject section resequencing, placement movement/resequencing, reusable-question/version replacement, direct-question identity change, answer-key change, or omission interpreted as deletion. | A hierarchy-bearing change is requested | resolve_questionnaire_existing_identity |
| Direct Question rendering | Reject Questionnaire.dat generation unless `mode: direct` has the complete required field set, one of the four supported types, current target Question and conditional Answer component MERGE evidence, an exact compatible category and response type, and the approved executable direct-question procedure. Accept `mode: direct-text` only when QuestionType is TEXT. | A direct Question is requested | resolve_questionnaire_direct_question_contract |
| Direct choice answer shape | Require one or more complete Answer rows for a direct `1CHOICE` or `MULTCHOICE` Question; each has the exact parent hierarchy, target-valid unique AnswerCode, positive unique AnsSequenceNumber, LongText, and only approved target-registered optional values. Reject answers for direct `TEXT` or `NONE`. | A direct Question or Answer row is supplied | resolve_questionnaire_direct_question_contract |
| Attachment shape | Reject an unregistered component or operation, mixed file/URL mode when unsupported, incomplete metadata, local absolute path, or missing packaged content | Attachment data is supplied | resolve_questionnaire_hdl_contract |
| Translation shape | Require QuestionnaireCode, VersionNumber, SubscriberName, TemplateFlag N, Language, and nonblank translated Name; reject an orphan or unregistered instruction | Questionnaire translation data is supplied | resolve_questionnaire_hdl_contract |
| Source references | Treat live-registered SourceRef attributes as optional correlation only; reject their use as a substitute for the portable questionnaire key unless the live object registers that key | Source reference values are supplied | resolve_questionnaire_hdl_contract |
| Load content | Treat COMMENT and METADATA-only content as a schema template; require at least one registered data-operation row for an import artifact | HDL import is requested | |
| Questionnaire root lifecycle and portability | Require target-valid Status, mandatory create-time InUse, QuestionnaireName, versioned portable key, privacy/owner combination, and CategoryName/TemplateQstnrCode when route-required; UpdateAllowed is preserved unless a supported operation explicitly changes it; reject generated IDs, audit values, source references, and JSON booleans | A Questionnaire row is supplied | resolve_questionnaire_existing_identity |
| Template-linkage update | Preserve TemplateQstnrCode and its resolved template identity unless current target evidence explicitly proves the requested linkage change mutable and impact-safe. Reject a copied template ID or silent relinking. | Change intent is selected | resolve_questionnaire_template |
| In-use and response-bearing update safety | Require current release-specific proof that every changed root field and child operation is editable in the exact latest/in-use/response state. Treat lifecycle REST evidence as partial; block hierarchy, scoring, template-linkage, status, or lifecycle mutation until complete impact and mutability evidence is available. | Change intent is selected and the questionnaire is in use, has responses, or either state is unresolved | resolve_questionnaire_usage_state |
| Questionnaire presentation and scoring | Validate VersionDescription for later versions, IntroText, SectionOrder, SectionPresentation, PageLayout, QstnsPerPage, CalcRuleCode, MaxPossibleScore, and LayoutOption only when compatible with current target metadata, subscriber, and final hierarchy | A related root field is supplied | resolve_questionnaire_scoring |
| Questionnaire section and placement | Require positive unique SectionSeqNum, nonblank Name, valid page/order/mandatory/ad-hoc/random-sample controls, exact reusable-question identity, positive unique QstnSequenceNumber, and compatible placement flags; blank QstnrQstnResponseTypeName inherits | Section or Question row is supplied | resolve_questionnaire_question_version |
| Questionnaire answer, attachment, and translation | Require the full placed-question parent, target AnswerCode and AnsSequenceNumber contract, coherent text/scoring/correctness/additional-questionnaire values, complete packaged attachment content, and TemplateFlag N translation identity | Answer, QuestionnaireAttachment, or translation data is supplied | resolve_questionnaire_hdl_contract |

## HDL DAT Contract

| File | Root Component | Supported Child Scope | Identity and Pairing Contract |
|---|---|---|---|
| Questionnaire.dat | Exact root returned by live metadata, expected from current evidence to be Questionnaire | QuestionnaireAttachment, Section, Question, and Answer only when registered by the target | Pair the root by SubscriberName, QuestionnaireCode, and QstnrVersionNum; sections by SectionSeqNum; placements by section, question/version, and QstnSequenceNumber; answers by the registered answer key and complete parent hierarchy |
| QuestionnaireTranslation.dat | Exact translation root returned by live metadata | None unless the current target template declares otherwise | Match one loaded ordinary questionnaire with QuestionnaireCode, VersionNumber, SubscriberName, TemplateFlag N, and Language |

Use exact live METADATA lines and attribute order. Escaping, null handling, date and number formatting, file packaging, and operation-specific mandatory fields come from the current target template and common Data Loader contract.

## Approval-Bound Suggestion Validation

| Check | Rule |
|---|---|
| Entry condition | Suggestion handling is allowed only after the declared exact resolver returns zero matches for a suggestion-capable value. Multiple exact matches remain ambiguous. |
| Candidate evidence | Require a complete documented and authorized target catalog, subscriber/parent/capability restrictions, at most three exact candidates, a catalog timestamp, source-request fingerprint, and candidate-set fingerprint. |
| Pending state | Preserve the raw input and stop DAT rendering until the user explicitly approves one complete exact value or compatible value set. |
| Approved state | Bind approval to the target, task, portable parent key, original value, exact candidate, catalog and fingerprints; rerun the original exact resolver immediately before preview. |
| Exact-only values | Reject suggestion use for Data Loader registration, OwnerPersonNumber, a submitted update target key, version/child sequence keys, generated IDs, lifecycle/in-use/response/usage evidence, and returned links. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QNR.VALIDATE-INPUT | step | 10 | validate_input | valid->QNR.CHECK-DEPENDENCIES;invalid->QNR.HANDLE-ISSUE | none | stop | Always |
