# Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_connector_source_type | Every request before dependency evaluation | Connector type supplied by the request | Match exact registry key OCI or USER-DEFINED in pillars/erp/risk-and-security/add-other-data-sources/connector-source-types.json | OCI maps to sourceTypeName OCI and sourceTypeCode 2; USER-DEFINED maps to sourceTypeName User-Defined and sourceTypeCode 10 | Stop and request one supported connector type; do not accept caller-supplied source type names or codes |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| verify_oci_seeded_source | Resolved source type is OCI and BOSS OAuth readiness is confirmed | Resolved sourceTypeName OCI | POST /api/boss/data/objects/ora/riskMgmtRisk/dataIntegration/v1/connectorDefinitions/$query | Collection response and returned connector-definition fields | Apply exactly sourceTypeName='OCI'; preserve returned collection without broadening the filter | Seeded connector collection; connector ID; OCI seeded-source readiness | Multiple records or hasMore true indicate seeded readiness; one active completed record indicates seeded readiness; one unready record or an empty collection blocks downstream work |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The resolved source type is OCI | Continue to the conditional OCI seeded-source readiness dependency. |
| The resolved source type is USER-DEFINED | Skip the OCI seeded-source readiness dependency. |
| The OCI query returns multiple records, hasMore true, or one active completed record | Treat OCI seeded-source readiness as verified. |
| The OCI query returns one unready record or an empty collection | Stop downstream work and report OCI seeded-source readiness is not satisfied. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CDS.RESOLVE_SOURCE_TYPE | step | 20 | evaluate_result | resolved->CDS.CHECK_DEPENDENCIES;invalid->CDS.HANDLE_ISSUE | CDS.VALIDATE_RESPONSE_SCHEMA | stop | After connector type and OpenAPI response schema validation and before dependency evaluation |
| CDS.VERIFY_OCI_SEEDED | step | 40 | reference_lookup | seeded->CDS.ENFORCE_DESIGN;empty->CDS.HANDLE_ISSUE;incomplete->CDS.HANDLE_ISSUE;unauthorized->CDS.HANDLE_ISSUE;failed->CDS.HANDLE_ISSUE | CDS.CHECK_DEPENDENCIES | stop | Resolved source type is OCI |
