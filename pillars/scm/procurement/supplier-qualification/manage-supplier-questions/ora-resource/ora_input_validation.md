# Supplier Qualification Questions Input Validation

Validate the REST import request before it is prepared for review. This file defines a contract only; it does not construct a payload or invoke Fusion.

The invoking host applies the boolean normalization contract while preparing source data, before starting a Data Loader session. These authored rules do not add an automatic converter to the generic Data Loader. After capture, SUPQ.VALIDATE checks the retained values and requires cancellation and corrected-source validation when normalization is still needed.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Core question | Question; exactly one of QuestionText or QuestionPlainText; QuestionLevelCode or QuestionLevel; ResponderTypeCode or ResponderType; QuestionTypeCode or QuestionType; QuestionStatusCode or QuestionStatus; ScoringMethodCode or ScoringMethod; and AttachmentAllowedCode or AttachmentAllowed | Apply the QuestionStatusCode and AttachmentAllowedCode defaults, then block only if a field group remains unresolved | Provide a value for every required field group and one text representation | Create or edit | |
| Input Box response | ResponseType | Block preparation | Provide a valid response type | QuestionType is Input Box | |
| Preferred response | Matching preferred response value | Block preparation | Provide the value matching the selected response type | Display Preferred Response is selected for an active Input Box question | |
| Supplier attribute mapping | SupplierAttributeCode or SupplierAttribute | Block preparation | Provide one supplier attribute identifier or display value | SupplierAttributeFlag is true | |
| Manual scoring | MaximumScore | Block preparation | Provide an integer of at least 1 | Scoring Method is Manual | |
| Automatic optional response scoring | ScoreForNoResponse | Block preparation | Provide a value of at least 0 | Scoring Method is Automatic and Response Required is false | |
| Acceptable responses | DisplaySequence and response details | Block preparation | Provide a display sequence of at least 1 and applicable response fields | Question is not Input Box and not supplier-attribute mapped | |
| Lifecycle status patch | QuestionId; exactly one of QuestionStatusCode or QuestionStatus | Block preparation | Provide the existing question identifier and the target status | A status PATCH is requested | find_question_by_id |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Boolean flag normalization | Before source capture, normalize every supplied boolean flag attribute whose technical name ends in Flag, in the question and all child sections: trim surrounding whitespace and convert any case variant of TRUE or FALSE to lowercase true or false; serialize native boolean values with the same lowercase spelling. This includes SupplierAttributeFlag and ResponseRequiredFlag, and is not limited to those two fields. Preserve blank or absent values for existing default rules; do not lowercase question text, lookup codes, or other non-flag values | Source preparation for create or edit, including CSV, XLSX, and other supported input formats | |
| Boolean flag validation | Require every nonblank boolean flag value to be exactly true or false after normalization; reject other values without guessing mappings for Y, N, 1, or 0. If a captured Data Loader session still contains uppercase or mixed-case boolean flag values, stop, cancel that session, correct the source, and start fresh validation and approval; rule results cannot modify captured records or reuse a previous approval | All supplied boolean flag attributes in the question and child sections, before preview | |
| Question length | Reject a Question value longer than 80 characters | Always | |
| Bulk question identity | Reject duplicate normalized Question values within the supplied input batch | Create request contains more than one row | |
| Question level value | Reject when both QuestionLevelCode and QuestionLevel are blank | Create or edit | |
| Responder type value | Reject when both ResponderTypeCode and ResponderType are blank | Create or edit | |
| Question type value | Reject when both QuestionTypeCode and QuestionType are blank | Create or edit | |
| Question status value | Default QuestionStatusCode to DRAFT when both QuestionStatusCode and QuestionStatus are blank; otherwise accept either field | Create or edit | |
| Lifecycle status patch value | Reject a status PATCH unless the target status resolves to Active or Inactive | A status PATCH is requested | validate_question_status_lookup |
| Scoring method value | Reject when both ScoringMethodCode and ScoringMethod are blank | Create or edit | |
| Attachment allowed value | Default AttachmentAllowedCode to NOT_ALLOWED when both AttachmentAllowedCode and AttachmentAllowed are blank; otherwise accept either field | Create or edit | |
| Question level lookup value | Reject an unresolvable QuestionLevel or QuestionLevelCode value | QuestionLevel or QuestionLevelCode is supplied | validate_question_level_lookup |
| Responder type lookup value | Reject an unresolvable ResponderType or ResponderTypeCode value | ResponderType or ResponderTypeCode is supplied | validate_responder_type_lookup |
| Question status lookup value | Reject an unresolvable QuestionStatus or QuestionStatusCode value | QuestionStatus or QuestionStatusCode is supplied | validate_question_status_lookup |
| Question type lookup value | Reject an unresolvable QuestionType or QuestionTypeCode value | QuestionType or QuestionTypeCode is supplied | validate_question_type_lookup |
| Response type lookup value | Reject an unresolvable ResponseType or ResponseTypeCode value | ResponseType or ResponseTypeCode is supplied | validate_response_type_lookup |
| Scoring method lookup value | Reject an unresolvable ScoringMethod or ScoringMethodCode value | ScoringMethod or ScoringMethodCode is supplied | validate_scoring_method_lookup |
| Subject lookup value | Reject an unresolvable Subject or SubjectCode value | Subject or SubjectCode is supplied | validate_subject_lookup |
| Standards organization lookup value | Reject an unresolvable StandardsOrganization or StandardsOrganizationCode value | StandardsOrganization or StandardsOrganizationCode is supplied | validate_standards_organization_lookup |
| Attachment allowed lookup value | Reject an unresolvable AttachmentAllowed or AttachmentAllowedCode value | AttachmentAllowed or AttachmentAllowedCode is supplied | validate_attachment_allowed_lookup |
| Scoring approach lookup value | Reject an unresolvable ScoringApproach or ScoringApproachCode value | ScoringApproach or ScoringApproachCode is supplied | validate_scoring_approach_lookup |
| Creation source lookup value | Reject an unresolvable CreationSource or CreationSourceCode value | CreationSource or CreationSourceCode is supplied | validate_creation_source_lookup |
| Supplier attribute value | Reject when both SupplierAttributeCode and SupplierAttribute are blank | SupplierAttributeFlag is true | |
| Text representation | Reject payloads containing both QuestionText and QuestionPlainText | Create | |
| Create lifecycle fields | Reject Revision and framework-managed identifiers on normal create; the framework derives the initial revision and identity | Create | |
| Question hint length | Reject QuestionHint longer than 1,000 characters | QuestionHint is provided | |
| Input Box response type | Reject a missing ResponseType | QuestionType is Input Box | |
| Preferred response | Reject a missing type-matching preferred response | Display Preferred Response is selected for an active Input Box question | |
| Maximum score | Reject MaximumScore below 1 or missing for Manual scoring | Scoring Method is Manual | |
| Score for no response | Reject ScoreForNoResponse below 0 or missing | Automatic scoring and Response Required is false | |
| Response score | Reject score rows below 0 | Response Scores are applicable | |
| Display sequence | Reject DisplaySequence below 1 | Display sequence is required | |
| Acceptable response volume | Reject more than 500 acceptable responses for one question | acceptableResponses is provided | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An update, revision, delete, activation, inactivation, or status PATCH is requested | QuestionId is required to identify the existing question | Resolve the QuestionId through the documented read-only question lookup before preparing the operation | find_question_by_id |
| A create request uses Upsert-Mode=true | Existing-resource matching behavior is server-managed | Include the header only after its duplicate-handling behavior is reviewed and approved | |
| Question Name, Question Level, or Responder Type changes | The question must be Draft at revision 0 | Stop when the lifecycle state is not eligible | find_question_by_id |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SUPQ.VALIDATE | step | 1 | validate_input | valid->SUPQ.LOOKUP_VALUES;invalid->SUPQ.BLOCKED | none | stop | Always |
