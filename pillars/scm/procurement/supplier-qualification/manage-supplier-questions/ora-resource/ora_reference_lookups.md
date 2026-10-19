# Supplier Qualification Questions Reference Lookups

Use these read-only lookups only during preparation or validation. They do not authorize a create, update, revision, or delete.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_question_by_id | A QuestionId is supplied for update, revision, delete, activation, inactivation, or status PATCH preparation | QuestionId | /fscmRestApi/resources/11.13.18.05/supplierQualificationQuestions/{QuestionId} | QuestionId, Question, Revision, LatestRevisionFlag, QuestionStatusCode | Return the single resource identified by QuestionId | QuestionId, Question, Revision, LatestRevisionFlag, QuestionStatusCode | Stop if the question is not found; do not substitute a similarly named question |
| validate_question_level_lookup | QuestionLevel or QuestionLevelCode is supplied | QuestionLevel, QuestionLevelCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='POQ_QUESTION_LEVEL' | LookupCode, Meaning | Match a supplied code exactly to LookupCode or a supplied meaning exactly to Meaning; when both are supplied, they must identify the same lookup code | QuestionLevel, QuestionLevelCode | Stop when no exact match exists or the supplied meaning and code resolve differently |
| validate_responder_type_lookup | ResponderType or ResponderTypeCode is supplied | ResponderType, ResponderTypeCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='POQ_RESPONDER_TYPE' | LookupCode, Meaning | Match a supplied code exactly to LookupCode or a supplied meaning exactly to Meaning; when both are supplied, they must identify the same lookup code | ResponderType, ResponderTypeCode | Stop when no exact match exists or the supplied meaning and code resolve differently |
| validate_question_status_lookup | QuestionStatus or QuestionStatusCode is supplied | QuestionStatus, QuestionStatusCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='POQ_QUESTION_STATUS' | LookupCode, Meaning | Match a supplied code exactly to LookupCode or a supplied meaning exactly to Meaning; when both are supplied, they must identify the same lookup code | QuestionStatus, QuestionStatusCode | Stop when no exact match exists or the supplied meaning and code resolve differently |
| validate_question_type_lookup | QuestionType or QuestionTypeCode is supplied | QuestionType, QuestionTypeCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='POQ_QUESTION_TYPE' | LookupCode, Meaning | Match a supplied code exactly to LookupCode or a supplied meaning exactly to Meaning; when both are supplied, they must identify the same lookup code | QuestionType, QuestionTypeCode | Stop when no exact match exists or the supplied meaning and code resolve differently |
| validate_response_type_lookup | ResponseType or ResponseTypeCode is supplied | ResponseType, ResponseTypeCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='POQ_RESPONSE_TYPE' | LookupCode, Meaning | Match a supplied code exactly to LookupCode or a supplied meaning exactly to Meaning; when both are supplied, they must identify the same lookup code | ResponseType, ResponseTypeCode | Stop when no exact match exists or the supplied meaning and code resolve differently |
| validate_scoring_method_lookup | ScoringMethod or ScoringMethodCode is supplied | ScoringMethod, ScoringMethodCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='ORA_POQ_QUES_SCORING_METHOD' | LookupCode, Meaning | Match a supplied code exactly to LookupCode or a supplied meaning exactly to Meaning; when both are supplied, they must identify the same lookup code | ScoringMethod, ScoringMethodCode | Stop when no exact match exists or the supplied meaning and code resolve differently |
| validate_subject_lookup | Subject or SubjectCode is supplied | Subject, SubjectCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='POQ_SUBJECT' | LookupCode, Meaning | Match a supplied code exactly to LookupCode or a supplied meaning exactly to Meaning; when both are supplied, they must identify the same lookup code | Subject, SubjectCode | Stop when no exact match exists or the supplied meaning and code resolve differently |
| validate_standards_organization_lookup | StandardsOrganization or StandardsOrganizationCode is supplied | StandardsOrganization, StandardsOrganizationCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='POQ_STDS_ORG' | LookupCode, Meaning | Match a supplied code exactly to LookupCode or a supplied meaning exactly to Meaning; when both are supplied, they must identify the same lookup code | StandardsOrganization, StandardsOrganizationCode | Stop when no exact match exists or the supplied meaning and code resolve differently |
| validate_attachment_allowed_lookup | AttachmentAllowed or AttachmentAllowedCode is supplied | AttachmentAllowed, AttachmentAllowedCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='POQ_QUESTION_RESPONSE_ATTACH' | LookupCode, Meaning | Match a supplied code exactly to LookupCode or a supplied meaning exactly to Meaning; when both are supplied, they must identify the same lookup code | AttachmentAllowed, AttachmentAllowedCode | Stop when no exact match exists or the supplied meaning and code resolve differently |
| validate_scoring_approach_lookup | ScoringApproach or ScoringApproachCode is supplied | ScoringApproach, ScoringApproachCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='ORA_POQ_QUES_SCORING_APPROACH' | LookupCode, Meaning | Match a supplied code exactly to LookupCode or a supplied meaning exactly to Meaning; when both are supplied, they must identify the same lookup code | ScoringApproach, ScoringApproachCode | Stop when no exact match exists or the supplied meaning and code resolve differently |
| validate_creation_source_lookup | CreationSource or CreationSourceCode is supplied | CreationSource, CreationSourceCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='ORA_POQ_QSTN_CREATION_SOURCE' | LookupCode, Meaning | Match a supplied code exactly to LookupCode or a supplied meaning exactly to Meaning; when both are supplied, they must identify the same lookup code | CreationSource, CreationSourceCode | Stop when no exact match exists or the supplied meaning and code resolve differently |

## Lookup Execution Rules

All 11 value resolvers above use the case-sensitive standardLookupsLOV collection.
The question-by-ID resolver remains a supplierQualificationQuestions item GET.
Pass the query separately to the shared client; the table's ?q= notation defines
that query and is not a child-resource path.

```bash
python core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  /fscmRestApi/resources/11.13.18.05/standardLookupsLOV \
  --query "q=LookupType='POQ_QUESTION_LEVEL'" \
  --query fields=LookupCode,Meaning \
  --query onlyData=true --query limit=500 --query offset=0 \
  --header REST-Framework-Version=9 --no-open-browser
```

Replace only POQ_QUESTION_LEVEL with the exact type from the selected resolver.
Use the configured Fusion environment and shared OAuth service. These lookups
are read-only validation operations; they do not authorize question creation.


| Situation | What Happens |
|---|---|
| Every value lookup GET | Send REST-Framework-Version: 9, fields=LookupCode,Meaning, onlyData=true, and limit=500; start at offset=0 and preserve the exact LookupType filter when advancing pages |
| A declared standardLookupsLOV request fails | Stop and report the HTTP status and selected resolver; do not retry through a maintenance lookup resource or change the lookup type |
| Collection reads need pagination | Use offset and limit; do not expect more than 500 records in one response |
| A lookup needs a narrow response | Use fields to request only the attributes needed for validation |
| A lookup is used to identify a question | Treat QuestionId as the unique identifier; do not infer identity from a non-unique question text |
| A bulk create request is validated | Compare normalized Question values within the supplied batch only; no live duplicate lookup is performed |
| A meaning or code attribute is supplied | Use the standardLookupsLOV GET collection through core.fusion-api.rest-api-client with the exact LookupType filter declared for that attribute pair; do not select commonLookups, standardLookups maintenance resources, or a similar meaning or code |
| A lookup-code response is paginated | Follow offset and limit until the requested exact meaning or code is found or the collection is exhausted |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SUPQ.LOOKUP_VALUES | step | 2 | reference_lookup | valid->SUPQ.DESIGN;invalid->SUPQ.BLOCKED | SUPQ.VALIDATE | stop | Any listed meaning or code attribute is supplied; otherwise valid without a lookup |
| SUPQ.QUESTION_LOOKUP | step | 4 | reference_lookup | found->SUPQ.GATE;not_found->SUPQ.BLOCKED | SUPQ.DESIGN | stop | Update, revision, delete, activation, inactivation, or status PATCH preparation |

## Source

Oracle Fusion Cloud Procurement 26D, [Get all standard lookups](https://docs.oracle.com/en/cloud/saas/procurement/26d/fapra/op-standardLookupsLOV-get.html), documents the standardLookupsLOV collection, LookupType query filter, LookupCode and Meaning fields, and pagination.
