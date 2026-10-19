# Reference Lookups

The validated reference export and Questionnaires REST response confirm the required CSV mapping: QuestionnaireCode, QuestionnaireName, and QuestionnaireId retain their names; REST VersionNumber maps to CSV QstnrVersionNum.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_questionnaire_lov | An attestation row supplies or selects a Questionnaire | Supplied Questionnaire business value; SubscriberId=11; QuestionnaireTemplateId>0 | GET {FA_HOST}/hcmRestApi/resources/11.13.18.05/questionnaires?q=SubscriberId=11;QuestionnaireTemplateId>0 | QuestionnaireId, QuestionnaireName, QuestionnaireCode, and VersionNumber | Trim only leading and trailing Unicode whitespace from the supplied value and each returned QuestionnaireName, then require exactly one normalized exact match. Do not alter case, internal whitespace, punctuation, or other characters. | QuestionnaireCode, QuestionnaireName, QuestionnaireId, and QstnrVersionNum from VersionNumber exactly as returned | Treat zero, many, or unavailable normalized exact matches as blocked; do not invent an identifier or select a partial match |
| resolve_time_category_lov | An attestation row supplies or selects a Time Category | Supplied Time Category business value | GET {FA_HOST}/hcmRestApi/resources/11.13.18.05/timeCategoriesLOV | TcatId and TcatName | Retrieve the collection and require exactly one returned item whose TcatName exactly equals the supplied Time Category business value | TimeCategoryId from TcatId and verified Time Category name from TcatName | Treat zero, many, or unavailable results as blocked; do not invent a category ID or select a partial match |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Questionnaire lookup | Trim only leading and trailing Unicode whitespace, then require one normalized exact returned Questionnaire display-name match. Block zero, multiple, unavailable, partial, case-altered, or internally whitespace-altered matches. |
| Time Category lookup | Use the documented timeCategoriesLOV collection and retain the single exact TcatName match with its returned TcatId; do not use a sample ID, static value, or partial match. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TAS_VALIDATE_LOVS | step | 30 | reference_lookup | resolved_or_not_needed->TAS_ENFORCE_FIELDS;incomplete_or_unresolved->RETURN_ISSUES | TAS_DEFAULT_EVENTS | stop | Questionnaire or Time Category is supplied in an attestation row |
