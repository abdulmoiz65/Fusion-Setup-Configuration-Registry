# Configure Item Shortage Parameters Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| An Item Shortage Parameter context is unrecognized or conflicts with an explicit RuleType | Stop before Data Loader handoff and request one approved context value or its matching RuleType |
| Module is explicitly supplied with a value other than SHORTAGE | Stop before Data Loader handoff and correct Module to SHORTAGE or omit it for approved defaulting |
| A supplied Default Period meaning or code does not resolve to exactly one context-specific standard-lookup row | Stop before Data Loader handoff and show the supplied value, resolver name, lookup type, match count, and correction needed |
| Default Period meaning and code resolve to different rows | Stop before Data Loader handoff and request one authoritative matching value |
| A DefaultCatalogName does not resolve to exactly one catalog row | Stop before Data Loader handoff and show the resolver name, supplied catalog name, returned match count, and correction needed |
| A DefaultCategoryName does not resolve to exactly one scoped row | Stop before Data Loader handoff and show the resolver name, supplied category name, returned match count, and correction needed |
| The Item Category resolver omits or cannot apply `REST-Framework-Version: 9` | Stop before Data Loader handoff. Report the resolver name, required framework version, sanitized route result, and correction needed; rerun the read-only resolver through the configured core REST client with the required header. |
| ruleConfigurationHeaders metadata is unavailable or not visible in the selected environment | Stop and report a Data Loader availability issue; do not fall back to direct REST write guidance |
| The selected environment or BO discriminator is absent from the current preflight record | Stop before handoff and require a fresh per-run metadata preflight |
| Data Loader or Fusion rejects prepared data | Preserve the Data Loader status, row identity, failure class, and sanitized message; Data Loader and Fusion own backend validation |


## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Context defaulting | Item Shortage Parameter context is unrecognized or conflicts with RuleType, or Module conflicts with SHORTAGE | Supply a recognized context and matching RuleType, and use SHORTAGE for Module |
| Lookup readiness | A Default Period value is not found, ambiguous, inaccessible, or conflicts with its supplied code or meaning | Provide an exact Meaning or matching LookupCode from the RuleType-specific standard lookup |
| Lookup readiness | A DefaultCatalogName is not found, ambiguous, or inaccessible | Provide one exact catalog name from the standard Item Catalog lookup |
| Lookup readiness | A DefaultCategoryName is not found, ambiguous, inaccessible, or outside the resolved catalog scope | Provide one exact category name from the Item Category lookup for the resolved catalog |
| Lookup readiness | The Item Category resolver omits or cannot apply `REST-Framework-Version: 9` | Require framework version 9 for the same scoped Item Category resolver, then retry the read-only lookup |
| Input readiness | A UI display value lacks its registered physical code or ID | Supply the physical value or approve a complete lookup contract |
| Data Loader availability | Current ruleConfigurationHeaders metadata cannot be read or is not visible | Verify registration and target-environment access, then run a fresh metadata preflight |
| Data Loader validation | Data Loader or Fusion rejects prepared data | Correct the source using the returned sanitized diagnostic |
| FSM export result | The task export manifest or ProcessLog reports errors | Preserve the available ZIP and ProcessLog, report the returned status, and do not infer that an Item Shortage Rule Header correction is required from the export result alone. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Metadata preflight failure | Selected environment, ruleConfigurationHeaders discriminator, failure class, sanitized message, and recommended next action |
| Default Period lookup failure | Supplied DefaultPeriod and DefaultPeriodCode when present, resolver name, lookup type, match count, and correction needed |
| Catalog/category lookup failure | Resolver name, supplied DefaultCatalogName or DefaultCategoryName, resolved catalog context where available, match count, sanitized route availability, and correction needed |
| Item Category framework-version failure | Resolver name, required framework version 9, sanitized route result, and correction needed |
| Data Loader handoff | Task code, task name, business object, and current metadata-preflight result |
| Data Loader failure | Data Loader request or process identifier when available, failed row identity, sanitized message, stage, and recommended next action |
| FSM export result | Task code, export process identifier, requested scope criterion, manifest process status, sanitized ProcessLog result, and ZIP path |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A LOV resolver is not fully approved | Do not infer a Fusion REST URL from a VBC service alias, fuzzy-match a display value, or select the first candidate |
| BO/Data Loader route is unavailable | Do not use task-local REST POST, PATCH, or DELETE guidance as a fallback |
| Data Loader outcome is uncertain | Do not resubmit until status and read-only verification clarify the outcome |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ISP.DATA_LOADER_HANDOFF | decision | 90 | execution_gate | ready->ISP.DONE;blocked->ISP.HANDLE_ERROR;failure->ISP.HANDLE_ERROR | ISP.CHECK_METADATA | stop | Before handing physical shortage-parameter data to core.data-loader |
| ISP.HANDLE_ERROR | step | 100 | error_handler | handled->ISP.RETURN_ISSUES | none | stop | Any local defaulting, lookup, readiness, Data Loader, or FSM setup-export issue |
| ISP.RETURN_ISSUES | terminal | 110 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| ISP.DONE | terminal | 120 | terminal | none | ISP.DATA_LOADER_HANDOFF | stop | Local task rules passed and Data Loader owns final validation and execution |
