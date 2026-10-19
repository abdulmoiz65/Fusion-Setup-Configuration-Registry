# Rate Definitions HDL Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| validate_rate_definition_hdl_identity | Before a RateDefinitionV2 or RateContributorV2 MERGE record is accepted | Prepared immutable RateDefinitionV2 and RateContributorV2 records | Require exactly one parent row for RateDefinitionCode, LegislativeDataGroupName, and EffectiveStartDate; require every child to use that same parent key and a unique SequenceNumber; validate supplied source-system pairs only when present | Parent MERGE key, child parent linkage, contributor sequence | Stop preparation; report the conflicting parent key or sequence and do not submit the artifact. |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_rate_definition_hdl_contract | HDL preparation, validation, or import is requested | Configured target environment and RateDefinitionV2 business-object discriminator | GET /hcmRestApi/resources/latest/dataLoaderBusinessObjects?finder=findDataLoaderBos&onlyData=true&limit=500&offset=<n>; then GET /hcmRestApi/resources/latest/dataLoaderBusinessObjects/{BusinessObjectId}; then GET /documents/files/{UcmContentId}/data | Registered business object discriminator, BusinessObjectId, UcmContentId, and downloaded target template | Require exactly one target Data Loader business object whose discriminator is RateDefinitionV2; use its returned UcmContentId to retrieve the current template and validate every selected RateDefinitionV2 and RateContributorV2 attribute against it | BusinessObjectId, template content ID, valid parent and child attribute contract, supported reference field names | No match or many matches: stop HDL preparation and report the target discriminator and match result; do not substitute another object or template. |
| resolve_legislative_data_group_by_exact_name | Before the LDG is accepted for a parent or contributor | LegislativeDataGroupName and configured target environment | GET /hcmRestApi/resources/11.13.18.05/legislativeDataGroupsLOV | LegislativeDataGroupId and LegislativeDataGroupName | Retrieve the collection through the configured target environment and retain exactly one case-sensitive LegislativeDataGroupName match | LegislativeDataGroupId and LegislativeDataGroupName | No match or many matches: stop preparation; report the supplied LDG and match count without selecting a substitute. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A RateDefinitionV2 or RateContributorV2 field is selected | Obtain the current target HDL template through the core Data Loader contract and use its exact attribute names and supported values. |
| A supplied business value is represented by an HDL code field | Preserve the supplied code only when the current target template accepts the corresponding attribute; let the approved HCM Data Loader validation resolve the target reference during import processing. |
| Parent or contributor records are prepared | Validate parent-key correlation, optional source-system pairs, and child sequence uniqueness from the immutable local HDL artifact. |
| A required target template, LDG, or local artifact correlation is unavailable | Stop preparation; do not infer an attribute, code, parent linkage, or substitute REST endpoint. |
| HCM Data Loader validation rejects a target reference | Preserve the sanitized loader diagnostic, correct the supplied code or prerequisite, regenerate the immutable artifact, and obtain new approval before retry. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RATE_DEFINITION.ASSESS_MERGE_IDENTITY | decision | 20 | reference_lookup | identity_confirmed->RATE_DEFINITION.RESOLVE_DEPENDENCIES;identity_unresolved->RATE_DEFINITION.HANDLE_LOOKUP_ERROR | RATE_DEFINITION.VALIDATE_INPUT | stop | Validate the prepared HDL parent key and contributor-parent linkage before submission. |
| RATE_DEFINITION.RESOLVE_REFERENCES | decision | 40 | reference_lookup | resolved->RATE_DEFINITION.DESIGN_GATE;blocked->RATE_DEFINITION.HANDLE_LOOKUP_ERROR | RATE_DEFINITION.RESOLVE_DEPENDENCIES | stop | Obtain and apply the current target HCM Data Loader template contract for RateDefinitionV2 and RateContributorV2. |
