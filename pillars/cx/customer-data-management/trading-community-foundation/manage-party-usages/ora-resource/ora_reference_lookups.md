# Reference Lookups

Resolve the live setup task during export preparation without depending on
hierarchy fields that the `setupTasks` resource may omit.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_party_usages_task_by_name_then_exact_code | Export preparation before immutable preview creation | TaskName=Manage Party Usages; TaskCode=HZ_MANAGE_PARTY_USAGES | /fscmRestApi/resources/11.13.18.05/setupTasks with onlyData=true, totalResults=true, q=TaskName LIKE '%Manage Party Usages%', and limit=100 | TaskCode, TaskName, AvailableFlag, ExportImportSupportedFlag, CSVExportImportSupportedFlag, OfferingName, OfferingCode, FunctionalAreaName, FunctionalAreaCode | Ignore non-exact rows; require exactly one row with the fixed task name and code, AvailableFlag=Y, and CSVExportImportSupportedFlag=Y; accept absent or blank hierarchy fields; reject contradictory nonblank hierarchy fields | Live task identity and support flags; optional nonblank hierarchy evidence | Stop before approval or POST with catalog_or_metadata_mismatch |

Run the shared lookup without offering or functional-area arguments so absent
live hierarchy fields cannot remove the valid task row:

~~~bash
python3 shared/setup-export/task-level-export/scripts/find_setup_task_code.py \
  --task-name "Manage Party Usages" \
  --token-cache auto \
  --json \
  --output project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-party-usages/current/setup-task-search.json \
  --print
~~~

Use the effective catalog and enclosing task manifest as hierarchy authority
when Fusion omits offering or functional-area fields. Never select the first
row merely because Fusion returned it first. Retry this read-only lookup once
after a cache-managed token refresh on 401 or 403; a second authentication
failure blocks execution.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PU.LOOKUP_SETUP_TASK | step | 1 | reference_lookup | resolved->PU.VALIDATE_CONTEXT;blocked->PU.ERROR;failure->PU.ERROR | none | stop | Export preparation before immutable preview creation |
