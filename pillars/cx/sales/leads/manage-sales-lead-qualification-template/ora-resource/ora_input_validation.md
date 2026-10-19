# Input and Package Validation

Source basis: Oracle Fusion Cloud Sales, *Create a Lead Qualification Template*.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Operation: Create, Copy, Review, or Deploy | Block validation | Provide one supported operation; Deploy is readiness review only | Always | |
| Target environment | EnvironmentUrl, EnvironmentIdentity, FusionRelease, and ProjectId | Block before export | Select and verify the Fusion environment and durable project workspace | Always | |
| Template identity | TemplateName; SourceTemplateName is also accepted for Copy | Block validation | Provide the new template name, or both source and new names for Copy | Always | |
| Template classification | TemplateType with value Lead | Block validation | Set TemplateType to Lead for this setup task | Create or Copy | |
| Reference-data scope | TemplateSet and intended business-unit coverage | Block validation | Select the reference-data set that represents the intended business units | Create or Copy | |
| Rating model | RatingName and optional RatingDescription for every rating used by a response | Block validation | Provide the rating categories used by the qualification questionnaire | Create or Copy | |
| Questionnaire | QuestionGroupName, QuestionText, QuestionWeight, ResponseText, ResponseScore, and ResponseRating | Block validation | Provide at least one group, question, and scored response set | Create or Copy | |
| Deployment review | Final question-weight total and reviewed score ranges | Block read-only deployment readiness | Review the complete questionnaire and score-range model; this does not authorize deployment | Deploy | |
| Fresh reference export | ExportProcessId, ReferenceZipPath, ReferenceZipSha256, ProcessEnv, ProcessRelease, ExportedAt, and inventory | Block package generation or review | Run the current-data task export; use a user ZIP only through the documented offline fallback | Create, Copy, Review, or Deploy-readiness | |
| Duplicate reconciliation | ExportExactMatchCount, LiveExactMatchCount, and evidence timestamps | Block package generation | Reconcile the proposed exact name against the export and the live endpoint | Create or Copy | reconcile_lead_template_name_evidence |
| Generated import package | PackagePath, PackageSha256, package row counts, and validation result | Block preview or import | Build a single-template FSM package from the validated reference contract | Create or Copy | |
| Data Loader task context | TaskContextPath, TaskName, positive TaskSequence, PackagePath, PackageSha256, and finalData.archiveSha256 | Block Data Loader handoff | Supply the selected task context and bind finalData.archiveSha256 to the validated package SHA-256 | Create or Copy import handoff | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Create and both export and live lookup return no exact Lead template name | Satisfied | Continue to design enforcement | reconcile_lead_template_name_evidence |
| Create and either source returns an exact Lead template name | Blocked | Choose a new name or use Copy or Review | reconcile_lead_template_name_evidence |
| Create and export/live match counts disagree | Blocked | Treat the evidence as stale and run a fresh export before continuing | reconcile_lead_template_name_evidence |
| Copy, Review, or Deploy and exactly one Lead template is found | Satisfied | Continue with the resolved AssessTemplateId | find_assessment_template_by_exact_name |
| Copy, Review, or Deploy and no exact Lead template is found | Blocked | Correct the template name | find_assessment_template_by_exact_name |
| Any operation and more than one exact Lead template is returned | Blocked | Narrow the business-unit context before continuing | find_assessment_template_by_exact_name |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation is not Create, Copy, Review, or Deploy | Reject the request as unsupported | Always | |
| TemplateName is blank | Block before lookup | Always | |
| TemplateType is not Lead | Reject because this task owns Lead qualification templates | Create or Copy | |
| TemplateSet is blank | Block before package preparation | Create or Copy | |
| A question has no group, text, weight, or response set | Block before package preparation | Create or Copy | |
| A scored response has no numeric score or defined rating | Block before package preparation | Create or Copy | |
| Deploy execution is requested | Return unsupported and stop; no validated FSM deployment contract exists | Deploy mutation | |
| Sum of all question weights is not exactly 100 | Block deployment readiness and return the calculated total | Create, Copy, or Deploy | |
| Score-range override is requested without a complete nonoverlapping rating range model | Block deployment readiness | Create, Copy, or Deploy | |
| Reference archive is not ZIP-valid or any CRC fails | Block all reference-derived processing | Create, Copy, or Review | |
| Reference archive does not contain exactly the seven task CSVs plus ASM_SETUP_CSV_METADATA.xml | Block and identify missing or unexpected members | Create, Copy, or Review | |
| Metadata ObjectShortName, ObjectType, ProcessType, ProcessStatus, ProcessEnv, ProcessRelease, or LEAD scope does not match the request | Block and require a current export from the target environment | Create, Copy, or Review | |
| A required CSV header or its order differs from the fresh metadata contract | Block package generation; do not guess or normalize headers | Create or Copy | |
| Package contains zero or more than one row in either template CSV | Block import readiness | Create or Copy | |
| Package template has AssessedObjTypeCode other than LEAD or StatusCode other than IN_PROGRESS | Block import readiness | Create or Copy | |
| AssessTemplateNumber, group, attribute, value, rating, or score-range identifiers are reused from the reference inventory | Block import readiness and regenerate every proposed identifier | Create or Copy | |
| Any child foreign key does not resolve within the one proposed template dependency closure | Block import readiness | Create or Copy | |
| Package contains a reference template row, unrelated record, or source audit value | Block import readiness; prune the package to the proposed dependency closure | Create or Copy | |
| Question, response, rating, group, or score-range sequence numbers are missing or duplicated within their parent | Block import readiness | Create or Copy | |
| NormalizedScore is outside 0 through 100, or raw and normalized score semantics are conflated | Block import readiness | Create, Copy, or Deploy | |
| Score ranges overlap, leave gaps, are reversed, or do not cover 0 through 100 when overridden | Block deployment or import readiness | Create, Copy, or Deploy | |
| Recalculated weighted sample score does not equal sum of QuestionWeight multiplied by NormalizedScore divided by 100 | Block import readiness and show the calculated result | Create or Copy | |
| PackageSha256 and finalData.archiveSha256 differ, or the archive changes after task validation | Block Data Loader handoff; rebuild task validation and its Data Loader preview | Create or Copy import handoff | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LQT.VALIDATE | step | 1 | validate_input | valid->LQT.DEPENDENCIES;invalid->LQT.RETURN_ISSUES | none | stop | Apply only operation-specific validation: all operations need identity/environment evidence; Create/Copy additionally need design, package, task-context, and archive evidence; Review/Deploy-readiness must not inherit import-package requirements; actual Deploy mutation is invalid |
