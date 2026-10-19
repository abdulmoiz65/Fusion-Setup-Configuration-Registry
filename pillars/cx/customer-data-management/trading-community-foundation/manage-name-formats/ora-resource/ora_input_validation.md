# Input Validation

Validate the operation-specific whole-task contract and immutable Data Loader
handoff before any Fusion export or import request. These rules do not inspect
or modify individual name formats.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | operation=export or operation=import | Stop before preview | Select exactly one supported whole-task operation | Every run | |
| Fixed task identity | task_name=Manage Name Formats and task_code=HZ_MANAGE_NAME_FORMATS | Stop before preview | Use the catalog-backed identity from the enclosing task skill; never accept an override | Every run | |
| Fusion environment | fusion_environment_context | Stop before authentication or preview | Select one exact configured source for export or target for import and include it in the immutable preview | Export or import is requested | |
| Durable context | project_id and persisted task_context path inside that project | Stop before preview | Select the implementation project and its matching task context | Export or import is requested | |
| Export contract | template_only=false, export_criteria=[], output_dir inside the task project export path, wait_seconds=300, and poll_interval=10 | Stop before preview | Use the fixed whole-task export contract from the enclosing task skill | Export is requested | |
| Whole-task package | setup_data_zip_path and archiveSha256 | Stop before preview | Provide one unchanged ZIP and compute its SHA-256 from the exact bytes | Import is requested | |
| Data Loader route | executionRoute=data-loader, sourceType=FSM, and uploader=core/data-loader/scripts/upload_and_initiate.py | Stop before preview | Route the unchanged FSM ZIP through core.data-loader and its Task Hook | Import is requested | |
| Live approval | approval matching the exact export preview or the separate Data Loader immutable-artifact preview | Stop before submission | Display the exact operation, environment, task identity, scope or archive hash, and obtain the required current approval | Live export or import is requested | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Task context resolves exactly one Manage Name Formats entry with task code HZ_MANAGE_NAME_FORMATS | Satisfied | Continue with operation-specific validation | |
| Task context is missing, outside the project, ambiguous, or resolves another task code | Blocked | Correct the persisted task context; do not create an export or import process | |
| Export final data contains the fixed unfiltered, non-template scope and shared task-level export adapter | Satisfied | Compute and display the export preview fingerprint | |
| Export final data changes the fixed scope, path boundary, adapter, timeout, or polling interval | Blocked | Restore the fixed contract and rebuild the export preview | |
| ZIP contains a file whose basename is exactly ASM_SETUP_CSV_METADATA.xml | Satisfied | Preserve the archive bytes and compute the approval fingerprint | |
| ZIP is loose CSV, edited, repacked, invalid, or lacks the exact metadata member | Blocked | Supply the complete original task-level export ZIP | |
| Import preview target, task code, ZIP path, SHA-256, sourceType=FSM, and executionRoute=data-loader match the approval | Authorized | Release the approved envelope and unchanged archive to core.data-loader | |
| Any preview-bound value changed after approval | Blocked | Revalidate and obtain fresh explicit approval | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation value | Accept only export or import | Every run | |
| Data Loader route | Require executionRoute=data-loader and sourceType=FSM in the import preview and approved payload | Import preview and approval | |
| Export scope | Require template_only=false and an empty export_criteria array | Export | |
| Export path | Require output_dir to resolve inside project/{project_id}/exports/customer-data-management/trading-community-foundation/manage-name-formats/ | Export | |
| Export adapter | Reject any adapter other than shared.setup-export.task-level-export | Export | |
| ZIP signature | Require a valid ZIP beginning with the PK signature | Import | |
| Metadata member | Require exactly one archive entry whose basename is ASM_SETUP_CSV_METADATA.xml with matching case | Import | |
| FSM task binding | Require exactly one metadata ObjectShortName and require it to equal HZ_MANAGE_NAME_FORMATS | Import preview and approval verification | |
| Immutable bytes | Preserve the exact supplied archive; do not extract, edit, normalize, or repack it | Import validation through submission | |
| Package fingerprint | Require a lowercase 64-character SHA-256 value calculated from the submitted bytes | Import preview and approval | |
| Task override | Reject any task name or code other than Manage Name Formats and HZ_MANAGE_NAME_FORMATS | Every run | |
| Partial scope | Reject name-format, business-object, export-criteria, or template-only filters | Every run | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NF.VALIDATE_CONTEXT | step | 1 | validate_input | valid->NF.VALIDATE_OPERATION;invalid->NF.ERROR | none | stop | Before operation review or immutable preview creation |
| NF.VALIDATE_OPERATION | step | 2 | validate_input | valid->NF.VALIDATED;invalid->NF.ERROR | NF.VALIDATE_CONTEXT | stop | Before an export POST or Data Loader import preview |
