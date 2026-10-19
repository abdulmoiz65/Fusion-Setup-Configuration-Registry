# Input Validation

Validate the fixed task identity, whole-task FSM archive, changed profile-option rows, and immutable import approval before Core Data Loader is allowed to submit an import.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | operation=export, import, migrate, validate, view, update, or status | Stop before preview or live action | Select one supported operation | Every run | |
| Fixed task identity | task_name=Manage Account Industry Classification Profile Values and task_code=ORA_SVC_MANAGE_ACCT_IND_CLASS | Stop before preview | Use the enclosing catalog-backed task identity; never accept an override | Every run | |
| Fusion environment | fusion_environment_context | Stop before authentication, preview, or status lookup | Select exactly one configured target environment | Live export, import, update, or status | |
| Durable context | project_id and persisted task_context inside that project | Stop before preview | Select the implementation project and matching task context | Export, import, migrate, or status | |
| Whole-task package | setup_data_zip_path and lowercase 64-character setup_data_zip_sha256 | Stop before preview | Supply one exact-task FSM ZIP and hash its exact bytes | Validate, import, or migrate target phase | |
| Package content | one case-sensitive ASM_SETUP_CSV_METADATA.xml member and FND_APP_PROFILE_VALUE.csv when profile values are changed | Stop before preview | Use an FSM archive produced for this task; preserve required members and task metadata | Import or migrate target phase | |
| Profile change plan | ProfileOptionName=MOT_INDUSTRY_CLASS_CATEGORY, level, persisted current value, and proposed value for every changed FND_APP_PROFILE_VALUE row | Stop before preview | Use a fresh task export to verify the persisted row and show the change plan; read the effective value only when REST exposed | Import or migrate target phase with changed profile values | read_industry_classification_profile_value |
| Task profile-option inventory | requested and exported profile option code must equal MOT_INDUSTRY_CLASS_CATEGORY | Stop before view, preview, update, or import; for an expected option omitted by an otherwise completed export, report export_content_discrepancy and do not synthesize a row | Compare exact codes with the task contract | View, update, export validation, import, or migrate | |
| Import approval | approval matching Core Data Loader's exact immutable import preview and Task Hook validation envelope | Stop before import submission | Let Core Data Loader build, display, approve, and verify the import preview | Live import | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| ZIP has a valid signature, exactly one case-sensitive ASM_SETUP_CSV_METADATA.xml, and one exact task identity matching ORA_SVC_MANAGE_ACCT_IND_CLASS | Satisfied | Preserve bytes and bind the ZIP path and SHA-256 into the preview | |
| ZIP is loose CSV, edited without a fresh preview, repacked with changed metadata, unsafe, encrypted, ambiguous, or has missing or mismatched metadata | Blocked | Supply a safe complete FSM archive and restart validation | |
| The MOT_INDUSTRY_CLASS_CATEGORY row is changed and a fresh task export provides its persisted current value | Satisfied | Show the exact current-to-proposed change plan; include an effective value only when it is REST exposed | read_industry_classification_profile_value |
| The required profile row is absent from the export, the level is unsupported, the value is invalid, or the persisted value differs from the rebase basis | Blocked | Correct the change plan or rebase against a fresh target export; do not submit | read_industry_classification_profile_value |
| Import preview environment, task, ZIP/hash, validation envelope, and stated profile changes match approval | Authorized | Let Core Data Loader execute through its registered FSM route once | |
| Any package, current-value evidence, or preview-bound value changes after approval | Blocked | Revalidate and obtain fresh approval | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Profile task membership | Reject a requested or packaged profile option code other than MOT_INDUSTRY_CLASS_CATEGORY; report its omission from an otherwise completed export as export_content_discrepancy without reconstructing it | View, update, export validation, import, or migrate | |
| Task override | Reject any task name or code other than the fixed profile-options task | Every run | |
| Export scope | Require a complete, unfiltered, non-template export through shared.setup-export.task-level-export | Export | |
| ZIP signature | Require a valid ZIP beginning with the PK signature | Package validation | |
| Metadata member | Require exactly one member basename ASM_SETUP_CSV_METADATA.xml with matching case and one exact task identity | Package validation | |
| Profile CSV | When profile values change, require FND_APP_PROFILE_VALUE.csv and retain all nonchanged rows and FSM metadata exactly from the loader-accepted source package or a loader-required target rebase | Import preparation | |
| Changed rows | Require MOT_INDUSTRY_CLASS_CATEGORY, its level, persisted current value, and proposed value to be explicit in the approval preview | Rebased import preparation | read_industry_classification_profile_value |
| Immutable bytes | Do not extract, normalize, or repack the submitted archive after its final SHA-256 is calculated | Import validation through submission | |
| Package fingerprint | Require SHA-256 computed from the exact submitted bytes | Import preview and approval | |
| Import execution owner | Require core.data-loader to own adapter, endpoint, payload, upload, initiation, polling, and retry selection | Import | |
| Generic import ownership | Consume core.data-loader's existing validation, adapter, approval, and execution contract unchanged; do not add a task-local package-origin check, release policy, or adapter option | Import | |
| Revision mismatch | Do not resubmit the rejected archive unchanged; preserve the Fusion rejection and let core.data-loader prescribe the supported recovery before a new package, preview, and approval | Import | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AICP.VALIDATE_CONTEXT | step | 1 | validate_input | valid->AICP.READ_PROFILE_OPTION;invalid->AICP.ERROR | none | stop | Before operation review, immutable preview, or status continuation |
