# Reference Lookups

Resolve the live setup task during export or import preparation without depending on
hierarchy fields that the `setupTasks` resource may omit.

## Resolver: `find_setup_task_by_name_then_exact_code`

1. Authenticate through `core.auth.fusion-oauth-authentication` and use the
   configured environment.
2. Run the shared task-name lookup with `TaskName LIKE` semantics and no
   offering or functional-area filters:

   ```bash
   python3 shared/setup-export/task-level-export/scripts/find_setup_task_code.py \
     --task-name "Manage Address Formats" \
     --token-cache auto \
     --json \
     --print
   ```

3. Ignore non-exact rows. Require exactly one row whose `TaskName` is
   `Manage Address Formats` and whose `TaskCode` is
   `HZ_MANAGE_ADDRESS_FORMATS`.
4. Require `AvailableFlag=Y` and `CSVExportImportSupportedFlag=Y` on that exact
   row.
5. Treat absent or blank `OfferingName`, `OfferingCode`, `FunctionalAreaName`,
   and `FunctionalAreaCode` as unavailable live metadata, not a mismatch. Use
   the effective catalog and persisted task context as hierarchy authority.
6. If a returned nonblank hierarchy value contradicts catalog-backed context,
   or if zero or multiple exact fixed-code-and-name rows exist, stop before
   approval or POST with `catalog_or_metadata_mismatch`.
7. Persist the redacted lookup result and bind its path and exact-match outcome
   into the operation approval preview. Never persist authentication material.

Do not select the first row merely because Fusion returned it first. Retry this
read-only lookup once after a cache-managed token refresh on 401 or 403; a
second authentication failure blocks execution.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_setup_task_by_name_then_exact_code | Export or import preparation before immutable preview creation | TaskName=Manage Address Formats; TaskCode=HZ_MANAGE_ADDRESS_FORMATS | /fscmRestApi/resources/11.13.18.05/setupTasks with TaskName LIKE search | TaskCode, TaskName, AvailableFlag, CSVExportImportSupportedFlag, OfferingName, OfferingCode, FunctionalAreaName, FunctionalAreaCode | Retain exactly one row with the exact task name and code; require AvailableFlag=Y and CSVExportImportSupportedFlag=Y; ignore blank optional hierarchy fields and reject contradictory nonblank hierarchy values | Confirmed task name, task code, availability, CSV support, and live lookup artifact reference | Stop with catalog_or_metadata_mismatch before approval or POST |

## Task Node

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AF.LOOKUP_SETUP_TASK | step | 1 | reference_lookup | resolved->AF.VALIDATE_CONTEXT;blocked->AF.ERROR;failure->AF.ERROR | none | stop | Export or import preparation before immutable preview creation |
