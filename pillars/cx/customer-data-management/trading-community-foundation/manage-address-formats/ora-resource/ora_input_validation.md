# Input Validation

Validate the operation-specific whole-task contract before export or import.
These checks prepare one immutable execution summary without adding extra
approval gates or inspecting individual address styles.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | operation=export or operation=import | Stop before preview | Infer export from whole-task export wording; otherwise select exactly one supported operation | Every run | |
| Fixed task identity | task_name=Manage Address Formats and task_code=HZ_MANAGE_ADDRESS_FORMATS | Stop before preview | Use the catalog-backed identity; search live by the fixed name and select exactly one row with the exact fixed code and name | Every run | find_setup_task_by_name_then_exact_code |
| Fusion environment | fusion_environment_context | Stop before authentication or preview | Use the single configured source for export or target for import | Export or import | |
| Authentication preparation | Valid cache or one active OAuth callback flow using the configured local gitignored token cache | Stop before preview only after refresh/login fails or times out | Start or resume authentication directly; if browser interaction is needed, inform the user without requesting `ready`, `continue`, approval, or any reply, then continue automatically from the same waiting process | Export or import | |
| Durable context | project_id and persisted task context inside that project | Stop before preview | Resolve or create the project and refresh local task artifacts | Export or import | |
| Export contract | template_only=false, export_criteria=[], task output path, shared task-level exporter, wait_seconds=300, poll_interval=10 | Stop before preview | Apply the fixed whole-task export defaults | Export | |
| Whole-task package | setup_data_zip_path and archiveSha256 | Stop before preview | Provide one unchanged ZIP and compute SHA-256 from the exact bytes | Import only | |
| Data Loader route | executionRoute=data-loader, packageType=FSM, executionAdapter=cx.customer-data-management.trading-community-foundation.manage-address-formats.native-fsm-import | Stop before preview | Route the unchanged FSM ZIP through core.data-loader validation and Task Hook, then release the approved payload to this task's native FSM adapter | Import only | |
| Revision policy | `revisionMismatchPolicy=auto_override_on_exact_mismatch` and `sourceTargetDiffOkFlagSequence=[N,Y_on_exact_revision_mismatch]` | Stop before preview if absent, ambiguous, or changed after approval | Bind the initial `N` submission and the single conditional `Y` fallback to the same immutable target, task, ZIP hash, adapter, and options | Import only | |
| Live adapter contract | Target `dataLoaderDataSets/describe` action parameters and the selected setup-task CSV import adapter | Stop before preview | Reject the generic UCM upload/initiation route when `initiateDataLoad` does not advertise every proposed property, including `sourceType`; select the native `setupTaskCSVImports` adapter | Import only | |
| Single execution approval | Complete immutable export or import preview; approval absent during preparation and required immediately before the first POST | Stop before submission | Show one complete summary and obtain one standalone approve response | Live operation ready to execute | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Task context resolves exactly one Manage Address Formats entry with task code HZ_MANAGE_ADDRESS_FORMATS | Satisfied | Continue with operation validation | |
| Task context is missing, outside the project, ambiguous, or resolves another task code | Blocked | Correct or refresh the local task context; do not submit | |
| Name search contains exactly one fixed-code-and-name row that is available and CSV export/import supported | Satisfied | Use catalog and task context as hierarchy authority | find_setup_task_by_name_then_exact_code |
| Name search contains zero or multiple exact rows, or the exact row is unavailable, unsupported, or has contradictory nonblank hierarchy metadata | Blocked | Stop before approval or POST with catalog_or_metadata_mismatch | find_setup_task_by_name_then_exact_code |
| Export final data contains the fixed scope and shared exporter | Satisfied | Compute and persist the export request fingerprint | |
| Export final data changes the fixed scope, path, adapter, timeout, or polling interval | Blocked | Restore the fixed contract and rebuild the export preview | |
| Export preview requires archiveSha256 or a Data Loader archive-verification command | Blocked | Remove the import-only requirement and use the export request fingerprint | |
| ZIP contains exactly one member whose basename is ASM_SETUP_CSV_METADATA.xml and whose ObjectShortName is HZ_MANAGE_ADDRESS_FORMATS | Satisfied | Preserve bytes and compute the import fingerprint | |
| ZIP is loose CSV, edited, repacked, invalid, or has wrong/missing task metadata | Blocked | Supply the complete original task-level export ZIP | |
| Import preview binds target, task, ZIP path, SHA-256, packageType=FSM, executionRoute=data-loader, and executionAdapter=cx.customer-data-management.trading-community-foundation.manage-address-formats.native-fsm-import | Satisfied | Show the single execution summary and wait for approve | |
| Import preview binds the exact-mismatch automatic fallback and immutable values | Satisfied | Submit through the task-local adapter after approval | |
| Fusion returns the explicit HTTP 400 source-target revision-mismatch rejection without a ProcessId | Authorized continuation | Resubmit the same immutable operation once with `SourceTargetDiffOkFlag=Y` without another approval | |
| Fusion returns any other error, uncertain response, or ProcessId | Stop | Do not invoke the fallback or submit another POST | |
| Generic `initiateDataLoad` action omits `sourceType` or another proposed property from live describe metadata | Blocked for generic adapter | Select the native `setupTaskCSVImports` adapter before preview; do not upload to UCM | |
| Approval matches the displayed preview and bound values remain unchanged | Authorized | Record downstream approval internally and release one operation without another prompt | |
| Any preview-bound value changed after approval | Blocked | Revalidate and obtain one fresh approval | |
| Authentication needs browser interaction | Preparation | Open the configured sign-in flow, keep the callback listener active, and continue automatically; never create an approval or `ready` gate | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation | Accept only export or import | Every run | |
| Export scope | Require template_only=false and export_criteria=[] | Export | |
| Export path | Require output_dir inside project/{project_id}/exports/customer-data-management/trading-community-foundation/manage-address-formats/ | Export | |
| Export adapter | Require shared.setup-export.task-level-export; reject core.data-loader and Task Hook as export preview/execution routes | Export | |
| Export fingerprint | Bind project, source, task, scope, output, adapter, options, and lookup evidence; never require a ZIP hash | Export preview and approval | |
| ZIP signature | Require a valid ZIP beginning with the PK signature | Import | |
| Metadata member | Require exactly one archive entry whose basename is ASM_SETUP_CSV_METADATA.xml with matching case | Import | |
| FSM task binding | Require exactly one metadata ObjectShortName equal to HZ_MANAGE_ADDRESS_FORMATS | Import | |
| Immutable bytes | Preserve the exact archive without extraction, normalization, editing, or repacking | Import validation through submission | |
| Package fingerprint | Require a lowercase 64-character SHA-256 from the submitted bytes | Import preview and approval | |
| Data Loader route | Require executionRoute=data-loader, packageType=FSM, and executionAdapter=cx.customer-data-management.trading-community-foundation.manage-address-formats.native-fsm-import | Import preview and approval | |
| Adapter payload | Require the task-local adapter's fixed task-level `setupTaskCSVImports` contract with the approved `N` then exact-mismatch-only `Y` sequence; prohibit `uploadDataLoaderFile`, `initiateDataLoad`, `runID`, and `sourceType` for this package | Import preparation through submission | |
| Task override | Reject any task name or code other than Manage Address Formats and HZ_MANAGE_ADDRESS_FORMATS | Every run | |
| Partial scope | Reject country, address-style, record, business-object, attribute, export-criteria, and template filters | Every run | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AF.VALIDATE_CONTEXT | step | 2 | validate_input | valid->AF.VALIDATE_OPERATION;invalid->AF.ERROR | AF.LOOKUP_SETUP_TASK | stop | Before operation review or immutable preview creation |
| AF.VALIDATE_OPERATION | step | 3 | validate_input | valid->AF.VALIDATED;invalid->AF.ERROR | AF.VALIDATE_CONTEXT | stop | Before an export POST or Data Loader import preview |
