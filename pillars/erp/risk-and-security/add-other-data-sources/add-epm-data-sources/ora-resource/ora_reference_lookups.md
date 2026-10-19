# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| query_seeded_epm_connector_definition | First workflow stage after connector selection and BOSS OAuth readiness | Resolved seeded_source_type_name | POST /api/boss/data/objects/ora/riskMgmtRisk/dataIntegration/v1/connectorDefinitions/$query | Collection response and returned connector-definition fields | Apply exactly sourceTypeName='<seeded_source_type_name>'; preserve returned collection without broadening the filter | Seeded connector collection; connector ID; seeded-connector readiness | Multiple records or hasMore true hand off to OpenAPI; one ready record hands off to OpenAPI; one unready record requires UI credential setup; an empty collection stops the workflow |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The query returns multiple records, or hasMore is true | Treat initial connector setup as complete and hand off directly to generic OpenAPI preparation using the manifest selected from connector type. |
| The query returns exactly one active completed record | Hand off directly to generic OpenAPI preparation. |
| The query returns exactly one record that is not active and completed | Retain its id as connector_id, open the Fusion connector setup page, and wait for user confirmation. Do not PATCH. |
| The query returns an empty collection | Report that no connector ID is available and stop. Do not generate OpenAPI or attempt UI credential setup. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPMDS.QUERY_SEEDED_CONNECTOR | step | 30 | reference_lookup | seeded->EPMDS.ENFORCE_DESIGN;empty->EPMDS.ENFORCE_DESIGN;incomplete->EPMDS.ENFORCE_DESIGN;unauthorized->EPMDS.HANDLE_ISSUE;failed->EPMDS.HANDLE_ISSUE | EPMDS.CHECK_DEPENDENCIES | stop | After connector selection and BOSS OAuth readiness |
| EPMDS.SEEDED_READY | step | 90 | evaluate_result | ready->EPMDS.VALIDATE_RESPONSE_SCHEMA | EPMDS.ENFORCE_DESIGN | stop | Multiple records, hasMore true, or one active completed record was returned; proceed to OpenAPI preparation |
