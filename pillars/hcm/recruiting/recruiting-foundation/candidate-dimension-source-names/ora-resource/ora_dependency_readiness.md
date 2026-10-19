# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Selected task and environment | Confirm exact task, profile and applicable project execution gates without displaying secrets |
| 2 | Shared task exporter and OAuth | Verify shared.setup-export.task-level-export, shared.setup-export.fsm-csv-export and core.auth.fusion-oauth-authentication exist |
| 3 | Fresh source evidence | Obtain normal task data export through the declared shared route; a prior export is not required to start retrieval |
| 4 | Shared validation and Data Loader | For mutations verify shared validators, core.data-loader and core.data-loader.task-hook are available |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| source_export | Completed normal task export | Yes | Retrieve, rename, Add Row or validate_import | Lookup | Exact shared-export result for the selected environment | resolve_source_export | Establish authoritative identities and CSV relationships | Start a fresh export for normal work; use the preserved baseline inside Task Hook | Task metadata, base and translation rows |
| shared_services | Shared export, validation and core Data Loader | Yes | The requested operation uses the service | Verify | Repository skill manifests | | Keep technical execution in shared/core | Stop on a missing dependency; no direct API fallback | Selected service route |
| translation_ui | Verified Translation Editor action | Conditional | Translation guidance | Verify | Explicitly supplied or requested task UI evidence | | No verified translation import contract | Verify action and language without a UI write | Guidance readiness |

Follow the shared exporter's catalog discovery and require exactly
ORA_MANAGE_CANDIDATE_DIMENSION_SOURCE_NAMES with CSVExportImportSupportedFlag = Y.
Keep the same selected properties profile and token cache across export/import.
Use core OAuth recovery for expired authentication; no application browser session
is required for this route. Preflight new artifact paths and never overwrite evidence.
Missing project execution gates block mutation, not a reason to change project controls.

Internal validate_import requires existing artifacts only. It must not start an export,
perform OAuth, call Data Loader recursively or require a browser session.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CDSN.CHECK_DEPENDENCIES | step | 20 | resolve_dependency | ready->CDSN.RESOLVE_EXPORT;blocked->CDSN.HANDLE_ISSUES | CDSN.VALIDATE_REQUEST | stop | Check the dependencies applicable to the operation |

## Selected OAuth cache

Pass both `--properties <selected-profile>` and `--token-cache <selected-cache>`
to every shared export and core Data Loader validation, upload and status command.
When the user selects `core/auth/fusionEnv.local.properties` and
`.fusionaim_token.json`, retain those exact arguments throughout the workflow.
Do not rely on the loader's default cache location: a URL-valued environment can
produce an invalid default filesystem path on Windows. If authentication fails
before upload, renew login through core.auth.fusion-oauth-authentication using the
same explicit paths, then resume only after verifying that no upload was submitted.
