# Input Validation

Validate the fixed whole-task FSM contract, direct shared-export route,
immutable import package, and Core Data Loader-owned import handoff before any
live submission.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | operation=export, import, migrate, validate, or status | Stop before preview or polling | Select one supported operation | Every run | |
| Fixed task identity | task_name=Manage Contact Point Descriptive Flexfields and task_code=HZ_MANAGE_CONTACT_POINT_DESCRIPTIVE_FLEXFIELDS | Stop before preview | Use the enclosing catalog-backed task identity; never accept an override | Every run | |
| Fusion environment | fusion_environment_context | Stop before authentication, preview, or status lookup | Select exactly one configured source or target environment | Live export, import, or status | |
| Durable context | project_id and persisted task_context inside that project | Stop before preview | Select the implementation project and matching task context | Export, import, migrate, or status | |
| Export contract | template_only=false, export_criteria=[], fixed output_dir, wait_seconds=300, poll_interval=10, and shared export adapter | Stop before preview | Use the fixed whole-task contract from the enclosing skill | Export or migrate source phase | |
| Whole-task package | setup_data_zip_path and lowercase 64-character setup_data_zip_sha256 | Stop before preview | Supply one unchanged FSM ZIP and hash its exact bytes | Validate, import, or migrate target phase | |
| Import contract | unchanged ZIP, fixed task identity, SourceTargetDiffOkFlag unset, wait_seconds=180, poll_interval=15, and shared import adapter | Stop before preview | Use the fixed task-level FSM import contract | Import or migrate target phase | |
| Existing process | operation direction and persisted ProcessId | Stop without submitting | Supply the exact prior process record | Status | |
| Export approval | approval matching the exact environment, fixed task, whole-task scope, output path, adapter, and execution options | Stop before export submission | Display and approve the task-level export preview | Live export | |
| Import approval | approval matching Core Data Loader's exact immutable import preview and Task Hook validation envelope | Stop before import submission | Let Core Data Loader build, display, approve, and verify the import preview | Live import | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Export final data is complete, unfiltered, non-template, and selects the shared export adapter | Satisfied | Display the task-level export preview; do not request deployment evidence or a pre-existing ZIP/hash | |
| Export requests a template, criteria, filter, partial scope, different task, or task-local executor | Blocked | Restore the fixed whole-task contract | |
| ZIP has a valid signature and exactly one case-sensitive ASM_SETUP_CSV_METADATA.xml whose single task identity matches the fixed task code | Satisfied | Preserve bytes and bind the ZIP path and SHA-256 into the preview | |
| ZIP is loose CSV, edited, repacked, unsafe, encrypted, ambiguous, or has missing or mismatched metadata | Blocked | Supply the complete original exact-task FSM export ZIP | |
| Export preview environment, task, scope, adapter, output path, and options match approval | Authorized | Invoke shared.setup-export.task-level-export directly exactly once | |
| Import preview environment, task, ZIP/hash, validation envelope, and impact match approval | Authorized | Let Core Data Loader execute through its selected registered route | |
| Any operation-specific preview-bound value changes after approval | Blocked | Revalidate and obtain fresh approval | |
| Status request identifies one persisted ProcessId | Satisfied | Poll or retrieve artifacts for that process only | |
| Status request has no exact ProcessId | Blocked | Reconcile using read-only process lookup; never submit a replacement process | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation | Accept only export, import, migrate, validate, or status | Every run | |
| Export route | Require direct shared.setup-export.task-level-export routing; reject Data Loader routing, approved-loader-payload, and any pre-existing ZIP/hash requirement | Export | |
| Import execution owner | Require core.data-loader to own adapter, endpoint, payload, upload, initiation, status, and retry-policy selection | Import | |
| Task override | Reject any task name or code other than the fixed contact point DFF task | Every run | |
| Export scope | Require template_only=false and export_criteria=[] | Export | |
| Export path | Require project/{project_id}/exports/customer-data-management/trading-community-foundation/manage-contact-point-descriptive-flexfields/ | Export | |
| Export adapter | Require shared.setup-export.task-level-export | Export | |
| ZIP signature | Require a valid ZIP beginning with the PK signature | Package validation | |
| Metadata member | Require exactly one member basename ASM_SETUP_CSV_METADATA.xml with matching case and one exact task identity | Package validation | |
| Immutable bytes | Do not extract, edit, normalize, or repack the supplied archive | Import validation through submission | |
| Package fingerprint | Require SHA-256 computed from the submitted bytes | Import preview and approval | |
| Import route selection | Reject any adapter, endpoint, routing field, payload builder, or retry policy selected by this pillar skill | Import | |
| Revision override | Do not request or construct a revision-mismatch override; Core Data Loader owns the payload | Import | |
| Direct DFF operation | Reject direct CRUD, deployment, individual contexts, segments, value sets, attributes, templates, filters, and partial scope | Every run | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CPDFF.VALIDATE_CONTEXT | step | 1 | validate_input | valid->CPDFF.VALIDATE_OPERATION;invalid->CPDFF.ERROR | none | stop | Before operation review, immutable preview, or status continuation |
| CPDFF.VALIDATE_OPERATION | step | 2 | validate_input | valid->CPDFF.DEPENDENCY_READINESS;invalid->CPDFF.ERROR | CPDFF.VALIDATE_CONTEXT | stop | Before operation-specific dependency review |
