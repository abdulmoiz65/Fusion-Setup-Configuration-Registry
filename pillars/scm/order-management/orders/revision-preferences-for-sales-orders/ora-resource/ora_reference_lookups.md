# Revision Preferences for Sales Orders Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| discover_revision_preference_attributes | Before validating, previewing, or updating a Revision Preferences change | limit=1000, offset=0, onlyData=true, totalResults=true | /fscmRestApi/resources/11.13.18.05/omSalesOrderAttributePreferences | AttributeName, AttributeCode, CategoryCode, RevisionRequiredFlag, totalResults, count, hasMore | Require count to equal totalResults and hasMore to be false. Match each submitted attribute by exact AttributeName only. | Resolved exact attribute name, same-record CategoryCode, and current revision requirement for the Data Loader workflow. | Stop on incomplete paging, no exact name match, blank AttributeCode or CategoryCode, or more than one exact name match. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The response is complete | Retain only sanitized discovery facts in project artifacts; do not persist credentials, URLs, tokens, or headers. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| REVISION_PREFERENCES.DISCOVER_ATTRIBUTES | step | 20 | reference_lookup | resolved->REVISION_PREFERENCES.ENFORCE_GROUPS;unresolved->RETURN_ISSUES;failure->RETURN_ISSUES | REVISION_PREFERENCES.VALIDATE_INPUT | stop | A Revision Preferences request has passed input validation. |
