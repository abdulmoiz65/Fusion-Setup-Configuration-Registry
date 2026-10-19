# Consolidation Groups Reference Lookups

Use public LOV resources for Legislative Data Group resolution. Use the internal payrollGeneric query or LOV only for the supplied current App UI read and display behavior. Loader status resources are read-only monitoring operations; they do not authorize upload, submission, retry, or another mutation.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| verify_legislative_data_group_by_id | An LDG ID must establish accessible scope or supply an HDL LDG name | LegislativeDataGroupId | GET /hcmRestApi/resources/11.13.18.05/legislativeDataGroupsLOV with an exact ID q filter, fields selection, onlyData true, and documented paging | LegislativeDataGroupId, Name, LegislationCode, count, hasMore, limit, offset | Follow paging and require exactly one exact ID match | LegislativeDataGroupName: Name; LegislativeDataGroupId: LegislativeDataGroupId; LegislationCode: LegislationCode | Stop with not-found, ambiguity, or authorization; do not reinterpret denial as absence |
| find_legislative_data_group_by_exact_name | An LDG name must resolve to accessible scope or supply an HDL LDG name | Exact Name; optional LegislationCode | GET /hcmRestApi/resources/11.13.18.05/legislativeDataGroupsLOV with an exact Name q filter, optional LegislationCode, fields selection, onlyData true, and documented paging | LegislativeDataGroupId, Name, LegislationCode, count, hasMore, limit, offset | Compare returned Name exactly and require one accessible match; use supplied LegislationCode only to disambiguate | LegislativeDataGroupName: Name; LegislativeDataGroupId: LegislativeDataGroupId; LegislationCode: LegislationCode | Stop with not-found, ambiguity, or authorization |
| search_consolidation_groups_by_ldg | Current App UI list or keyword search | Resolved LegislativeDataGroupId; optional SearchTerm | GET /hcmRestApi/redwood/11.13.18.05/payrollGeneric/payrollGenericQuery using the supplied LDG-scoped findByWord contract; append SearchTerms and FilterAttributes only for a keyword; limit 500; onlyData true | Code, Meaning, LegislativeDataGroupId, ConsolidationSetId, ConsolidationSetName, ConsolidationSetCode, Comments, CreationDate, CreatedBy, LastUpdateDate, LastUpdatedBy, count, hasMore, limit, offset | Preserve LDG scope, follow verified paging, and never assume limit 500 is exhaustive | Rows: returned group rows; PagingState: count, hasMore, limit, offset | Stop on incomplete paging, invalid finder, authorization, or transport failure; do not claim a complete list |
| check_consolidation_group_duplicate_by_ldg | A new Consolidation Group or Consolidation Set create is prepared or submitted | Resolved LegislativeDataGroupId, proposed ConsolidationSetCode, and proposed ConsolidationSetName | GET the literal runtime URL defined in Consolidation Group duplicate request serialization below. The complete comma-delimited text is one finder value; only limit and onlyData are separate query parameters. | LegislativeDataGroupId, ConsolidationSetId, ConsolidationSetName, ConsolidationSetCode, Comments, CreationDate, CreatedBy, LastUpdateDate, LastUpdatedBy, count, hasMore, limit, offset | Follow every page until hasMore=false; retain only rows in the exact LDG; compare proposed code to ConsolidationSetCode and proposed name to ConsolidationSetName exactly. Do not fuzzy-match, normalize, or select a near match. | DuplicatePreflight: passed when no exact code or name exists; DuplicateError: existing ConsolidationSetId, ConsolidationSetName, ConsolidationSetCode, LegislativeDataGroupId, and audit fields when either exact value exists | Stop before create on duplicate, incomplete paging, ambiguity, authorization, or transport failure. A passed preflight permits only preview preparation, never creation. |
| find_consolidation_group_by_id_in_ldg | Read One or Update precheck | Resolved LegislativeDataGroupId and exact ConsolidationSetId | Run search_consolidation_groups_by_ldg without a keyword that could exclude the target, follow paging, and compare ConsolidationSetId exactly | Complete group row from the LDG-scoped collection | Require exactly one exact ConsolidationSetId match | ConsolidationSetId: ConsolidationSetId; ConsolidationSetName: ConsolidationSetName; ConsolidationSetCode: ConsolidationSetCode; Comments: Comments; LegislativeDataGroupId: LegislativeDataGroupId; AuditValues: returned audit values | Return client-side not-found or ambiguity; do not invent an item endpoint |
| list_consolidation_group_payroll_references_by_ldg | Payroll Definition selector choices are requested | Resolved LegislativeDataGroupId; optional search text | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV using the supplied LDG-scoped findByWord contract, fields Code and Meaning, orderBy Meaning, limit 500, and onlyData true | Code, Meaning | Preserve each pair and require explicit selection | ConsolidationSetId: generic Code; DisplayName: Meaning | Stop if no eligible choice is returned or selection is ambiguous; never relabel generic Code as ConsolidationSetCode |
| get_hdl_data_set_status | Loader progress or completion is requested | RequestId | GET /hcmRestApi/resources/11.13.18.05/dataLoadDataSets/{RequestId}?onlyData=true | Request identity and returned transfer, import, and load status values | Require the exact requested data set and retain status until terminal | DataSetStatus: returned data-set status values; RequestId: RequestId | Stop on not-found, authorization, transport failure, or an unrecognized status; do not infer completion |
| list_hdl_business_object_statuses | Loader progress or completion is requested | RequestId | GET /hcmRestApi/resources/11.13.18.05/dataLoadDataSets/{RequestId}/child/businessObjects?onlyData=true | Business-object identity and returned import, load, and count values | Select PayrollConsolidationGroup and require one relevant terminal result | BusinessObjectStatus: PayrollConsolidationGroup result; Counts: returned object counts | Stop if PayrollConsolidationGroup is absent, duplicated, nonterminal, or failed |
| list_hdl_data_set_messages | Loader progress is requested or a loader phase fails | RequestId | GET /hcmRestApi/resources/11.13.18.05/dataLoadDataSets/{RequestId}/child/messages?onlyData=true | Returned message text and business-object or record context when available | Retain all relevant confirmed messages for PayrollConsolidationGroup | Messages: sanitized confirmed loader messages | An empty result is not proof of success; use data-set and business-object status, and stop on ambiguity or access failure |

## Lookup Execution Rules

## Consolidation Group Duplicate Request Serialization

For `check_consolidation_group_duplicate_by_ldg`, construct the request exactly as this pattern. Replace only `<pod-host>` and `<LegislativeDataGroupId>`; do not hard-code either value.

```text
https://<pod-host>/hcmRestApi/redwood/11.13.18.05/payrollGeneric/payrollGenericQuery?finder=findByWord;PayRestName=ConsolidationGroupUI_PayrollConsolidationSetVO,DisplayAttributes=LegislativeDataGroupId||ConsolidationSetId||ConsolidationSetName||ConsolidationSetCode||Comments||CreationDate||CreatedBy||LastUpdateDate||LastUpdatedBy,AdditionalViewCriteria=findByLDGId,ParameterKeys=pLegislativeDataGroupId,ParameterValues=<LegislativeDataGroupId>&limit=500&onlyData=true
```

Do not replace commas after PayRestName, DisplayAttributes, AdditionalViewCriteria, ParameterKeys, or ParameterValues with `&`. The complete comma-delimited text after `finder=` is one finder value. Only `limit=500` and `onlyData=true` are separate query parameters joined with `&`.

| Situation | What Happens |
|---|---|
| Duplicate preflight is requested for Create | Resolve the supplied LDG to its LegislativeDataGroupId first, then run check_consolidation_group_duplicate_by_ldg before preparing a create preview. |
| Duplicate preflight returns a code or name match | Return a duplicate error with the existing ConsolidationSetId, Name, Code, LDG, and audit fields; do not prepare or submit a create request. |
| Duplicate preflight is complete with no exact code or name match | Mark duplicate preflight passed and allow create preview preparation only; require the normal immutable preview and explicit approval before mutation. |
| Response already contains an LDG Name or selector Meaning | Reuse it and avoid another lookup. |
| A keyword is added to the group finder | Build the decoded finder with SearchTerms and FilterAttributes, then URL-encode the complete finder once; do not pre-encode or double-encode the plus separator. |
| One group is requested | Use the LDG-scoped collection and exact client-side ConsolidationSetId comparison; no dedicated item endpoint is confirmed. |
| A generic Payroll Definition selector row is used | Keep Code and Meaning together; generic Code represents the selected ID, not business ConsolidationSetCode. |
| A public LDG lookup resolves one record | Use its exact returned Name under HDL LegislativeDataGroupName and retain its Fusion ID for search/read scope; never place the ID under the name header. |
| A reference display cannot be resolved | Preserve the original ID or code and label its display value unresolved. |
| Related Payroll Definitions are requested | Do not treat payrollDefinitionsLOV as a complete reverse relationship lookup. |
| Loader status is nonterminal | Return the current confirmed status and a safe next-check path; do not report success or resubmit. |
| Loader status is terminal | Report success only when the data set and PayrollConsolidationGroup import and load results are successful with zero relevant errors; otherwise return sanitized confirmed messages. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CG.RESOLVE_REFERENCES | decision | 3 | reference_lookup | resolved->CG.APPLY_DEFAULTS;not_required->CG.APPLY_DEFAULTS;blocked->CG.HANDLE_ERROR | CG.RESOLVE_DEPENDENCIES | stop | A request contains LDG or group references, selector choices, or loader status identifiers |

## Sources

- Developer-provided ConsolidationGroups.md, updated and reviewed 2026-08-13.
- Oracle HCM REST API, Legislative Data Groups List of Values: https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-list-values-legislative-data-groups-list-values.html
- Oracle HCM REST API, HCM Data Loader Data Sets: https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-hcm-data-loader-data-sets.html
- Oracle HCM REST API, Generic Payroll Rows: https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-payrollgenericlov-get.html
