# Performance Process Flows Reference Lookups

Apply this task guidance using current target metadata and the declared execution route.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| get_performance_process_flow_by_id | A PATCH request identifies an existing flow. | ProcessFlowId | GET /latest/talentPerformanceProcessFlows/{ProcessFlowId} | ProcessFlowId, Name, DateFrom, DateTo, Status, InUseFlag, published flags | PrimaryKey finder matches the exact ProcessFlowId. | Current process-flow state for update validation. | No match: stop as unsupported identity. Many matches: stop; PrimaryKey must identify one row. |
| find_performance_process_flows_by_advanced_search | A read-only search is requested before selecting a flow. | query, Status, InUseFlag, DateFrom, DateTo, limit, offset, sort | POST /latest/talentPerformanceProcessFlows/action/findByAdvancedSearchQuery | Requested displayFields plus summary offset, limit, count, hasMore | Query applies to Name; supported filters are Status, InUseFlag, DateFrom, and DateTo; sort uses name and direction. | Matching process-flow summary and ProcessFlowId. | No match: return no candidates. Many matches: return the paged result and require an exact selection before update. |
| resolve_process_flow_status | Status is supplied | Status | ACTIVE_INACTIVE lookup| Code | Exact active/inactive status code | Validated Status | No match: stop as invalid. |
| resolve_redwood_performance_documents_feature | CalendarInviteFlag is true. | ORA_HRA_PERFORMANCE_DOCUMENTS_AND_GOALS_REDWOOD_ENABLED | core.fusion-api.apps-common.profile-options via /fscmRestApi/resources/11.13.18.05/profileValues | ProfileOptionValue | Read the effective profile value through the core skill and require exactly one Y value. | Redwood performance-documents feature enabled when ProfileOptionValue is Y. | No match, many matches, or a value other than Y: stop and clear CalendarInviteFlag. |
| resolve_compensation_calibration_feature | AllowShareLockForCalib is true. | ORA_HRA_COMP_CALIBRATION_STATUS_ENABLED | core.fusion-api.apps-common.profile-options via /fscmRestApi/resources/11.13.18.05/profileValues | ProfileOptionValue | Read the effective profile value through the core skill and require exactly one Y value. | Compensation-calibration feature enabled when ProfileOptionValue is Y. | No match, many matches, or a value other than Y: stop and clear AllowShareLockForCalib. |
| resolve_process_task_definition_by_task_name | A CSV task-role row is created or updated. | User-supplied task name | POST /hcmRestApi/resources/latest/talentPerformanceEvaluations/service/action/getProcessTaskDefinitions with no payload and Content-Type: application/vnd.oracle.adf.action+json | result[].TaskCode, result[].TaskName | Exactly one returned TaskName must match the user-supplied task name. | Use the matched TaskCode in TaskCode. For every code except MGREVAL, put the matched TaskName in both MgrTaskName and WkrTaskName; for MGREVAL, put it only in MgrTaskName. | No match or many matches: stop; do not copy or invent task names. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup contract is used | Use it only for a read-only operation; neither lookup authorizes POST, PATCH, DELETE, SOAP CRUD, or migration import. |
| A requested lookup concerns Redwood or compensation-calibration feature state | Use core.fusion-api.apps-common.profile-options and its /fscmRestApi profileValues route; it is read-only and does not authorize a mutation. |
| A requested lookup resolves process-task definitions | Use the documented no-payload POST action once to retrieve result[].TaskCode and result[].TaskName, then exact-match each user-supplied task name; it is read-only and does not authorize task-role CRUD or a migration import. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_PROCESS_FLOWS.REFERENCE_LOOKUPS | decision | 40 | reference_lookup | resolved->PERFORMANCE_PROCESS_FLOWS.ENFORCE_DEPENDENT_FIELD_INVARIANTS;not_found->PERFORMANCE_PROCESS_FLOWS.STOP_DEPENDENCY | PERFORMANCE_PROCESS_FLOWS.DEPENDENCIES | stop | An update or supported read-only search requires a process-flow lookup. |
