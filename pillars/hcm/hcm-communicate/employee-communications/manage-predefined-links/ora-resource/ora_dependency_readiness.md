# Manage Predefined Links Dependency Readiness

Sources: Confluence page 21736675148, Manage Predefined Links — ORA_IRC_EMP_CAMP_DEEP_LINKS; user-requested FSM export-and-inspect query route.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Exact task metadata | Resolve Manage Predefined Links as ORA_IRC_EMP_CAMP_DEEP_LINKS and confirm CSV export/import support is Y |
| 2 | Export context | Resolve the target Fusion environment and project workspace for the export artifact |
| 3 | Current FSM export | Run shared.setup-export.task-level-export and retain the downloaded result in the project workspace |
| 4 | Export inspection | Inspect the task CSV metadata and rows before applying the Active filter |
| 5 | Mutation baseline | Confirm exactly one current Draft row using DisplayName, ObjectType, and Action |
| 6 | Immutable mutation archive | Preserve the current metadata and all non-target rows; modify only the approved target field |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| MPL-TASK-EXPORT-SUPPORT | Catalog-supported task CSV export | Yes | A current link count is requested | Satisfied | Generated task manifest and effective setup-task catalog | | The task has CSVExportImportSupportedFlag Y | Use task code ORA_IRC_EMP_CAMP_DEEP_LINKS | TaskCode, Offering, Functional Area |
| MPL-EXPORT-CONTEXT | Target environment and project workspace | Yes | A current link count is requested | Verify | User-provided export context | | The routed export workflow needs a target and durable artifact destination | Supply the exact environment and project id | Environment, project id |
| MPL-CURRENT-EXPORT | Downloaded FSM export result | Yes | A current link count is requested | Verify | shared.setup-export.task-level-export output | | The count must be based on current exported data rather than a stale UI observation | Run the routed export and provide its ZIP or extracted task CSV evidence | Archive path, process status, CSV headers, rows |
| MPL-MUTATION-BASELINE | Exact Draft link baseline | Yes | Activate or Rename is requested | Verify | Current exported ORA_IRC_EMP_CAMP_DEEP_LINK.csv | | Prevents an ambiguous or stale update | Require exactly one row matching DisplayName, ObjectType, Action, and ORA_DRAFT | Current row and match count |
| MPL-IMMUTABLE-ARCHIVE | Reviewed FSM activation or rename archive | Yes | Activate or Rename is requested | Verify | Current export metadata and approved modified CSV | | Binds the Data Loader submission to one approved minimal change | Build the ZIP from current export metadata and CSV; retain its SHA-256 | Archive path, SHA-256, changed row |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact task metadata confirms CSV export support | Yes |
| Verify | Export context or downloaded archive must be established | Yes |
| Blocked | The task is unsupported, export context is missing, or the export failed | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPL.CHECK_REQUEST_READINESS | decision | 2 | resolve_dependency | ready->MPL.ENFORCE_EXPORT_SCOPE;blocked->MPL.HANDLE_ERROR | MPL.VALIDATE_REQUEST | stop | A current active-link count has valid query inputs |
| MPL.CHECK_MUTATION_BASELINE | decision | 3 | resolve_dependency | ready->MPL.ENFORCE_MUTATION_SCOPE;blocked->MPL.HANDLE_ERROR | MPL.VALIDATE_REQUEST | stop | An activation or rename target is resolved from a current export |

## Open TBD Items

| TBD Item | Owner | Blocker | Next Action |
|---|---|---|
| Exported business-object and status-field schema | Task export owner | Blocks fixed CSV field mapping, not export initiation or archive inspection | Inspect the first successful export and record its metadata and headers |
