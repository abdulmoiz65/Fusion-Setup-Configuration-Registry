# Reference Lookups

## Official Oracle Documentation

| Source | Oracle URL | What It Confirms | Evidence Boundary |
|---|---|---|---|
| Find the Code for a Setup Task | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/Find_SetupTask_Code.html | The setupTasks resource supports task-name lookup and returns TaskCode, TaskName, AvailableFlag, ExportImportSupportedFlag, and CSVExportImportSupportedFlag | The documented response does not establish offering or functional-area hierarchy; use the effective catalog and persisted task context for that hierarchy |

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| ANT.LOOKUP_SETUP_TASK | find_setup_task_by_name_then_exact_code | Before export or import preview preparation | Exact TaskName Manage Additional Name Types, fixed TaskCode HZ_MANAGE_ADDITIONAL_NAME_TYPES, expected AvailableFlag Y, expected CSVExportImportSupportedFlag Y, catalog-backed Customer Data Management and Trading Community Foundation hierarchy | Use shared.setup-export.task-level-export find_setup_task_code.py with task-name Manage Additional Name Types, no hierarchy filters, and limit 100; the adapter calls /fscmRestApi/resources/11.13.18.05/setupTasks with a TaskName LIKE query | TaskCode, TaskName, AvailableFlag, ExportImportSupportedFlag, CSVExportImportSupportedFlag, OfferingName, OfferingCode, FunctionalAreaName, FunctionalAreaCode when returned | From all returned rows, require exactly one row with exact TaskCode and TaskName, AvailableFlag Y, and CSVExportImportSupportedFlag Y; ignore non-exact rows; validate hierarchy from the effective catalog and persisted task context when hierarchy fields are absent; fail on any nonblank returned hierarchy value on the exact row that contradicts that context | Live task identity, availability, CSV support, returned hierarchy evidence, and validation provenance | Zero or multiple exact fixed-code-and-name rows, unavailable task, unsupported CSV flag, or contradictory nonblank hierarchy evidence blocks approval and POST |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Live offering or functional-area fields are absent or blank | Record that hierarchy was not returned live and validate it from the effective catalog and persisted task context; do not classify absence alone as a mismatch |
| Live hierarchy field is nonblank and agrees with catalog-backed context | Record the corroborating value and continue |
| Live hierarchy field is nonblank and contradicts catalog-backed context | Stop with catalog_or_metadata_mismatch before approval or POST |
| Authentication returns 401 or 403 | Refresh the cache-managed token once and repeat only the GET; a second authentication response blocks |
| Lookup is ambiguous or unsupported | Stop before the immutable preview; do not select the first row or accept a name-only match without the exact fixed TaskCode |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ANT.LOOKUP_SETUP_TASK | step | 1 | reference_lookup | resolved->ANT.VALIDATE_CONTEXT;blocked->ANT.ERROR;failure->ANT.ERROR | none | stop | Confirm the fixed live setup task and CSV support before validating an export or import operation |
