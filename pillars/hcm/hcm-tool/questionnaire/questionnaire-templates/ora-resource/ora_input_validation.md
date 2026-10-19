# Input Validation

Live target Data Loader metadata owns the Questionnaire Template HDL discriminator, hierarchy, attributes, user keys, mandatory indicators, and operations. Supplied DAT and FSM files establish candidate fields and relationships only; validate them against the current target immediately before preview.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Request context | Target environment, target release, requested business operation, approved source material | Stop before artifact preparation | Supply target context, operation intent, and approved prompt, spreadsheet, DAT, setup export, or specification | Always | |
| Live HDL contract | Exact Questionnaire Template and optional translation registrations, downloadable templates, components, attributes, user keys, mandatory indicators, and registered operations | Stop before normalizing or rendering DAT rows | Resolve the current target contract and follow every page and returned detail/template link | HDL is the selected mutation route | resolve_template_hdl_contract |
| Template identity | SubscriberName, QuestionnaireCode | Stop before dependency checks | Supply the complete portable root key; do not substitute QstnrTemplateId, QuestionnaireId, SubscriberId, or display text | Always | |
| Operation intent | Create, change, new version, inactivate, remove, or validate | Stop before duplicate and current-state checks | State the intended business effect separately from the HDL instruction | Always | |
| Update contract | One authoritative full-template readback, current root mutability and in-use/seeded/locked state, immutable portable root and child keys, non-empty aggregate changed-field set, explicit existing/new child intent, every emitted current value, and full impact evidence where required | Stop before DAT rendering | Resolve the full current template and affected hierarchy rows; do not treat a lightweight LOV row as update authority | Change intent is selected | resolve_template_existing_identity |
| Template header | Name, Status, PrivacyFlag, OwnerPersonNumber, introduction, presentation, override, allowed-response, and scoring values applicable to the design | Stop before dependency checks | Supply the approved header using only attributes registered for the selected operation | A QuestionnaireTemplate row is prepared | resolve_template_owner |
| Create-time service controls | AllowFormatChg, AllowIntroChg, AllowQstnOrderChg, AllowRespOrderChg, and AllowSectionChg | Stop before dependency checks | Supply one target-valid Y/N value for each current target create-required control; do not default one from a sample or another template | Create | |
| Template hierarchy | At least one Section for create, positive SectionSeqNum, and complete Question placement keys and sequence when placements are supplied | Stop before dependency checks | Supply the approved parent-child hierarchy and preserve complete parent keys | Create or a hierarchy-bearing change is requested | |
| Referenced question | QuestionCode, QstnVersionNum, SectionSeqNum, SeqNum, and optional registered placement override | Stop before dependency checks | Supply one exact same-subscriber reusable question version and placement key | An existing Question Library question is placed | resolve_template_question_version |
| Embedded question creation | Explicit creation intent, SubscriberName, QuestionCode, QstnVersionNum, CategoryName, question and response type values, SeqNum, and required answer design | Stop before dependency checks | Supply a complete new-question definition only when the live template supports embedded creation and the user approves it | A missing question is intentionally created inside the template hierarchy | resolve_template_category |
| Template attachment | Live-registered TemplateAttachment component, complete type, title, file or URL metadata, and packaged content where required | Stop before dependency checks | Supply all values required by the current attachment component | A TemplateAttachment is supplied | resolve_template_hdl_contract |
| Translation identity | QuestionnaireCode, VersionNumber, SubscriberName, TemplateFlag, Language, and translated Name | Stop before translation preparation | Use TemplateFlag Y and a separate translation DAT only when the target registers that contract | Template translation data is supplied | resolve_template_language |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The live template HDL registration or downloadable template cannot be resolved exactly | Blocked | Refresh target metadata; do not use the supplied DAT as the current schema | resolve_template_hdl_contract |
| A required root, hierarchy, parent, operation-intent, or translation key is absent | Blocked | Correct only the missing input before resolving references | |
| Input shape and live schema are valid | Verify | Evaluate task-local subscriber, reference, duplicate, lifecycle, response-format, and scoring dependencies | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| DAT schema | Reject an unknown filename discriminator, component, attribute, duplicate attribute, or attribute not registered for the selected operation | Any HDL DAT is prepared | resolve_template_hdl_contract |
| Executable serialization | Reject a DAT that was not emitted by the parent Questionnaire serializer and bound to a `status: passed` validation receipt with exact metadata/value parity, round-trip success, and the candidate SHA-256 | Any HDL DAT is prepared | resolve_template_hdl_contract |
| Operation registration | Reject an instruction not registered for its exact root, child, attachment, or translation business object; do not hard-code UPDATE or assume DELETE | Any data-operation row is prepared | resolve_template_hdl_contract |
| Root business key | Require QuestionnaireCode and SubscriberName in the exact target attributes; apply any additional live user-key fields returned for the selected operation | A QuestionnaireTemplate row is prepared | |
| Template update preservation | Require exactly one authoritative full-template match and proven update permission; reject changes to SubscriberName, QuestionnaireCode, or any existing child user-key field; require at least one approved changed field across the root and affected children; require every changed attribute and child operation to be mutable in the current state; and require every emitted unchanged value to equal exact current readback | Change intent is selected | resolve_template_existing_identity |
| Owner presence | Require a nonblank OwnerPersonNumber before querying the Questionnaire Templates service or rendering a QuestionnaireTemplate row. `Owner`, `OwnerPersonId`, and other owner/person IDs do not satisfy this requirement and must not be emitted. | A QuestionnaireTemplate row is prepared | resolve_template_owner |
| Generated identifiers | Reject QstnrTemplateId, QuestionnaireId, SubscriberId, QstnrSectionId, QstnrQuestionId, AnswerId, attachment IDs, or another generated target ID unless the selected existing-target operation explicitly requires it | A generated-ID attribute is populated | |
| Root field shape | Reject blank Name, Status, PrivacyFlag, OwnerPersonNumber, or any create-required change-control flag; reject invalid Y or N controls, invalid presentation/order codes, unregistered response-format flags, or values outside target lengths and types | A QuestionnaireTemplate row is prepared | |
| Section shape | Require complete parent key, positive unique SectionSeqNum, nonblank Name, and target-valid NewPage, QuestionOrder, ResponseOrder, Mandatory, and AllowAdhoc values | A Section row is supplied | |
| Question placement shape | Require exact parent section key, QuestionCode, QstnVersionNum, and positive unique SeqNum; validate every optional override against the live component | A Question placement row is supplied | |
| Answer shape | Require the exact placed-question parent plus the live-registered answer key and coherent text, score, feedback, correctness, and attachment fields | An Answer row is supplied | |
| Update child identity | Require each submitted Section, Question placement, and Answer row to declare existing or new intent. Existing requires one exact complete-key match; new requires zero key matches and a registered add-through-MERGE operation. Reject section resequencing, placement movement/resequencing, reusable-question/version substitution, answer-key changes, or omission interpreted as deletion. | A hierarchy-bearing change is requested | resolve_template_existing_identity |
| Response-format shape | Accept only the response-format attributes and values declared by the current template; do not convert FSM row presence or blank AdhocAllowed into an HDL value | Allowed response formats are supplied | resolve_template_response_format |
| Attachment shape | Reject an unregistered component, mixed file and URL mode when unsupported, incomplete metadata, local absolute path, or missing packaged content | Template or answer attachment data is supplied | resolve_template_hdl_contract |
| Translation shape | Require QuestionnaireCode, VersionNumber, SubscriberName, TemplateFlag Y, Language, and nonblank translated Name; reject an orphan or unregistered instruction | Template translation data is supplied | resolve_template_hdl_contract |
| Source references | Treat live-registered SourceRef attributes as optional correlation only; reject their use as a substitute for the portable template key unless the live object registers that key | Source reference values are supplied | resolve_template_hdl_contract |
| Load content | Treat COMMENT and METADATA-only content as a schema template; require at least one registered data-operation row for an import artifact | HDL import is requested | |
| Template lifecycle and portability | Require the complete portable template key and target-valid Status, PrivacyFlag, OwnerPersonNumber, allow-change flags, and randomization codes; UpdateAllowed is preserved unless a supported operation explicitly changes it; reject Owner, owner/person IDs, generated IDs, audit values, and source references | A QuestionnaireTemplate row is supplied | resolve_template_owner |
| In-use update safety | Require current release-specific proof that every changed root field and child operation is editable for the exact in-use state. Treat direct REST usage evidence as partial; block an in-use hierarchy or lifecycle change until complete impact and mutability evidence is available. | Change intent is selected and the template is in use or usage is unresolved | resolve_template_downstream_usage |
| Template hierarchy and response design | Require positive unique SectionSeqNum, nonblank section name, valid page/order/mandatory/ad-hoc controls, and exact reusable-question placement keys; blank QstnResponseTypeName inherits and a supplied override must match template format controls | Section or Question row is supplied | resolve_template_question_version |
| Template answer, attachment, and translation boundary | Validate answer identity/order/text/scoring against the placed question; require packaged attachment content and complete metadata; keep QuestionnaireTemplateTranslation unsupported until its target parent-version contract is proven | Answer, TemplateAttachment, or translation data is supplied | resolve_template_hdl_contract |

## Current Create-Time Service Requirement Matrix

Reconfirm this matrix against current target metadata immediately before preview. It records only portable values that the skill can safely supply; generated IDs marked mandatory by metadata are resolved from their registered user keys and remain prohibited in a new DAT.

| Component | Required portable values | Validation outcome when missing |
|---|---|---|
| QuestionnaireTemplate | QuestionnaireCode, SubscriberName, Name, Status, PrivacyFlag, OwnerPersonNumber, AllowFormatChg, AllowIntroChg, AllowQstnOrderChg, AllowRespOrderChg, AllowSectionChg | Block and request the first missing value; for owner, do not call the template service first |
| Section | QuestionnaireCode, SubscriberName, positive SectionSeqNum, Name | Block the hierarchy |
| Existing Question placement | QuestionnaireCode, SubscriberName, SectionSeqNum, QuestionCode, QstnVersionNum, positive SeqNum, AdhocQstn | Block the placement |

## HDL DAT Contract

| File | Root Component | Supported Child Scope | Identity and Pairing Contract |
|---|---|---|---|
| QuestionnaireTemplate.dat | Exact root returned by live metadata, expected from current evidence to be QuestionnaireTemplate | Section, Question, Answer, and TemplateAttachment only when registered by the target | Pair the root by SubscriberName and QuestionnaireCode; sections by SectionSeqNum; placements by section, question/version, and SeqNum; answers by the registered answer key and complete parent hierarchy |
| QuestionnaireTemplateTranslation.dat | Exact translation root returned by live metadata | None unless the current target template declares otherwise | Match one loaded template backing hierarchy with QuestionnaireCode, VersionNumber, SubscriberName, TemplateFlag Y, and Language |

Use exact live METADATA lines and attribute order. Escaping, null handling, date and number formatting, file packaging, and operation-specific mandatory fields come from the current target template and common Data Loader contract.

## Approval-Bound Suggestion Validation

| Check | Rule |
|---|---|
| Entry condition | Suggestion handling is allowed only after the declared exact resolver returns zero matches for a suggestion-capable value. Multiple exact matches remain ambiguous. |
| Candidate evidence | Require a complete documented and authorized target catalog, subscriber/parent/capability restrictions, at most three exact candidates, a catalog timestamp, source-request fingerprint, and candidate-set fingerprint. |
| Pending state | Preserve the raw input and stop DAT rendering until the user explicitly approves one complete exact value or compatible value set. |
| Approved state | Bind approval to the target, task, portable parent key, original value, exact candidate, catalog and fingerprints; rerun the original exact resolver immediately before preview. |
| Exact-only values | Reject suggestion use for Data Loader registration, OwnerPersonNumber, a submitted update target key, child identity/sequence keys, generated IDs, usage/mutability evidence, and returned links. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QTPL.VALIDATE-INPUT | step | 10 | validate_input | valid->QTPL.CHECK-DEPENDENCIES;invalid->QTPL.HANDLE-ISSUE | none | stop | Always |
