# Supplier Qualification Questions Design Enforcement

Apply these REST-resource constraints before preview. This resource establishes gates only and does not execute the REST operation.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate core and conditional fields | Apply the question, response, supplier-attribute, and scoring contracts |
| 2 | Validate supplied lookup attributes | Confirm every supplied meaning or code value matches the fixed common lookup type and that supplied pairs agree |
| 3 | Enforce lifecycle eligibility | Confirm the requested status PATCH is allowed for the current status and revision |
| 4 | Enforce question-type behavior | Select Input Box, standard acceptable-response, Products and Services, or Business Classification behavior |
| 5 | Enforce applicable field-pair and question-type gates | Confirm each required code-or-display field group and conditional question behavior is satisfied |
| 6 | Identify existing question | For edit, revision, activation, inactivation, or delete, verify the supplied QuestionId |
| 7 | Hand off for preview | Complete task validation and return ready_for_preview to the selected execution workflow. For core.data-loader, let its retained session build the final preview and obtain contextual approval before upload or initiation; do not require that later approval to finish these task checks or add a second approval. A lifecycle operation without a supported selected executor remains blocked |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Question Name, Question Level, or Responder Type changes | Error | find_question_by_id | The question is not Draft revision 0 | Keep core identity fields unchanged or create a permitted revision path | Yes |
| Status PATCH | Error | find_question_by_id | The target status is not Active or Inactive | Patch only to Active or Inactive; validate the supplied status through the input-validation lookup | Yes |
| Activate by status PATCH | Error | find_question_by_id | Question status is neither Draft nor Inactive | Patch the status to Active only for Draft or Inactive questions | No |
| Inactivate an Active question by status PATCH | Error | find_question_by_id | Question status is Active; Fusion rejects this PATCH because it only permits the operation for Draft questions | Do not PATCH an Active question to Inactive; use a separately documented lifecycle path and obtain a new preview and approval | No |
| Delete Draft | Error | find_question_by_id | Question is not Draft in edit mode | Do not delete a non-draft question through the draft-delete action | No |
| QuestionType is Input Box | Error | | ResponseType or applicable preferred-response value is missing | Provide the conditional response fields | Yes |
| QuestionType is not Input Box | Error | | Acceptable-response setup is missing or invalid | Maintain acceptable responses unless supplier-attribute behavior owns them | Yes |
| Supplier attribute mapping | Error | | SupplierAttributeFlag is true and neither SupplierAttributeCode nor SupplierAttribute is provided | Provide a supplier attribute code or display value | Yes |
| Scoring Method is Manual | Error | | MaximumScore is missing or less than 1 | Provide a maximum score of at least 1 | Yes |
| Automatic scoring | Error | | ScoreForNoResponse or response scores violate their conditional rules | Correct the applicable score values | Yes |
| Critical response or score exists | Error | | Critical Question is changed | Keep the question-level critical setting unchanged | No |
| Update, revision, delete, activation, inactivation, or status PATCH | Error | find_question_by_id | The supplied QuestionId cannot be resolved to one question | Correct the QuestionId before requesting approval | Yes |
| Branching is configured | Error | | Branching exceeds five levels | Redesign the question flow to five or fewer levels | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| validate_question_level_lookup | When QuestionLevel or QuestionLevelCode is supplied | QuestionLevel, QuestionLevelCode | ora_reference_lookups.md |
| validate_responder_type_lookup | When ResponderType or ResponderTypeCode is supplied | ResponderType, ResponderTypeCode | ora_reference_lookups.md |
| validate_question_status_lookup | When QuestionStatus or QuestionStatusCode is supplied | QuestionStatus, QuestionStatusCode | ora_reference_lookups.md |
| validate_question_type_lookup | When QuestionType or QuestionTypeCode is supplied | QuestionType, QuestionTypeCode | ora_reference_lookups.md |
| validate_response_type_lookup | When ResponseType or ResponseTypeCode is supplied | ResponseType, ResponseTypeCode | ora_reference_lookups.md |
| validate_scoring_method_lookup | When ScoringMethod or ScoringMethodCode is supplied | ScoringMethod, ScoringMethodCode | ora_reference_lookups.md |
| validate_subject_lookup | When Subject or SubjectCode is supplied | Subject, SubjectCode | ora_reference_lookups.md |
| validate_standards_organization_lookup | When StandardsOrganization or StandardsOrganizationCode is supplied | StandardsOrganization, StandardsOrganizationCode | ora_reference_lookups.md |
| validate_attachment_allowed_lookup | When AttachmentAllowed or AttachmentAllowedCode is supplied | AttachmentAllowed, AttachmentAllowedCode | ora_reference_lookups.md |
| validate_scoring_approach_lookup | When ScoringApproach or ScoringApproachCode is supplied | ScoringApproach, ScoringApproachCode | ora_reference_lookups.md |
| validate_creation_source_lookup | When CreationSource or CreationSourceCode is supplied | CreationSource, CreationSourceCode | ora_reference_lookups.md |
| find_question_by_id | Before update, revision, activation, inactivation, or delete preparation | QuestionId, Revision, LatestRevisionFlag, QuestionStatusCode | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SUPQ.DESIGN | decision | 3 | design_enforcement | create_compliant->SUPQ.GATE;existing_compliant->SUPQ.QUESTION_LOOKUP;noncompliant->SUPQ.BLOCKED | SUPQ.LOOKUP_VALUES | stop | Always |
