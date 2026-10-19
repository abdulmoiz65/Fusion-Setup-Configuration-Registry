# Input Validation

Validate the operation-specific whole-task contract and immutable Data Loader
handoff before any Fusion export or import request. These checks prepare the
operation without creating an extra approval gate or modifying individual setup
records.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | operation=export or operation=import | Stop before preview | Select exactly one supported whole-task operation | Every run | |
| Fixed task identity | task_name=Manage Hierarchy Labels and task_code=HZ_MANAGE_HIERARCHY_LABELS | Stop before preview | Use the catalog-backed identity from the enclosing task skill; never accept an override | Every run | |
| Fusion environment | fusion_environment_context | Stop before authentication or preview | Select one exact configured source for export or target for import and include it in the immutable preview | Export or import is requested | |
| Durable context | project_id and persisted task_context path inside that project | Stop before preview | Select the implementation project and its matching task context | Export or import is requested | |
| Export contract | template_only=false, export_criteria=[], output_dir inside the task project export path, wait_seconds=300, and poll_interval=10 | Stop before preview | Use the fixed whole-task export contract from the enclosing task skill | Export is requested | |
| Whole-task package | setup_data_zip_path and archiveSha256 | Stop before preview | Provide one unchanged ZIP and compute its SHA-256 from the exact bytes | Import is requested | |
| Data Loader route | executionRoute=data-loader, sourceType=FSM, and uploader=core/data-loader/scripts/upload_and_initiate.py | Stop before preview | Route the unchanged FSM ZIP through core.data-loader and its Task Hook | Import is requested | |
| Single execution approval boundary | A complete immutable export or import preview; approval is absent during preflight and required only immediately before the first POST | Stop before submission | Show one complete execution summary and obtain one exact approve response for that immutable operation | Live export or import is ready to execute | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Task context resolves exactly one Manage Hierarchy Labels entry with task code HZ_MANAGE_HIERARCHY_LABELS | Satisfied | Continue with operation-specific validation | |
| Task context is missing, outside the project, ambiguous, or resolves another task code | Blocked | Correct the persisted task context; do not create an export or import process | |
| Export final data contains the fixed unfiltered, non-template scope and shared task-level export adapter | Satisfied | Compute and display the export preview fingerprint | |
| Export final data changes the fixed scope, path boundary, adapter, timeout, or polling interval | Blocked | Restore the fixed contract and rebuild the export preview | |
| ZIP contains a file whose basename is exactly ASM_SETUP_CSV_METADATA.xml | Satisfied | Preserve the archive bytes and compute the approval fingerprint | |
| ZIP is loose CSV, edited, repacked, invalid, or lacks the exact metadata member | Blocked | Supply the complete original task-level export ZIP | |
| Import preview target, task code, ZIP path, SHA-256, sourceType=FSM, and executionRoute=data-loader are complete | Satisfied | Show the single execution summary and wait for one exact approve response | |
| Approval matches the displayed immutable preview and all bound values remain unchanged | Authorized | Record the downstream approval envelope internally and release the unchanged archive to core.data-loader without another prompt | |
| Any preview-bound value changed after approval | Blocked | Revalidate and obtain one fresh approval for the new immutable operation | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation value | Accept only export or import | Every run | |
| Data Loader route | Require executionRoute=data-loader and sourceType=FSM in the import preview and approved payload | Import preview and approval | |
| Export scope | Require template_only=false and an empty export_criteria array | Export | |
| Export path | Require output_dir to resolve inside project/{project_id}/exports/customer-data-management/trading-community-foundation/manage-hierarchy-labels/ | Export | |
| Export adapter | Reject any adapter other than shared.setup-export.task-level-export | Export | |
| ZIP signature | Require a valid ZIP beginning with the PK signature | Import | |
| Metadata member | Require exactly one archive entry whose basename is ASM_SETUP_CSV_METADATA.xml with matching case | Import | |
| FSM task binding | Require exactly one metadata ObjectShortName and require it to equal HZ_MANAGE_HIERARCHY_LABELS | Import preview and approval verification | |
| Immutable bytes | Preserve the exact supplied archive; do not extract, edit, normalize, or repack it | Import validation through submission | |
| Package fingerprint | Require a lowercase 64-character SHA-256 value calculated from the submitted bytes | Import preview and approval | |
| Task override | Reject any task name or code other than Manage Hierarchy Labels and HZ_MANAGE_HIERARCHY_LABELS | Every run | |
| Partial scope | Reject record, business-object, export-criteria, or template-only filters | Every run | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HL.VALIDATE_CONTEXT | step | 1 | validate_input | valid->HL.VALIDATE_OPERATION;invalid->HL.ERROR | none | stop | Before operation review or immutable preview creation |
| HL.VALIDATE_OPERATION | step | 2 | validate_input | valid->HL.VALIDATED;invalid->HL.ERROR | HL.VALIDATE_CONTEXT | stop | Before an export POST or Data Loader import preview |

