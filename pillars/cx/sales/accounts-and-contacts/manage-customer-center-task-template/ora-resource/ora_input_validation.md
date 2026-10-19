# Input Validation

Validate the fixed setup-task identity and complete FSM CSV package before an
export preview or import approval. A filtered offering or functional-area miss
is non-blocking when the local task identity and package metadata agree.

Official sources:

- [Add task templates to sales stages](https://docs.oracle.com/en/cloud/saas/sales/oasal/add-task-templates-to-sales-stages.html)
- [Export and import CSV file packages](https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/export-and-import-csv-file-packages.html)
- [Setup Task CSV Imports REST endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-imports.html)

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | operation=export or operation=import | Stop before preview | Select exactly one supported task CSV operation | Every run | |
| Fixed task identity | task_name=Manage Customer Center Task Template and task_code=ZCM_MANAGE_CUSTOMER_CENTER_TASK_TEMPLATE | Stop before preview | Use the identity from the enclosing skill and package metadata; do not accept an override | Every run | |
| Fusion environment | fusion_environment_context | Stop before authentication or preview | Select one exact configured source for export or target for import and display it in the immutable preview | Export or import | |
| Import package | setup_data_zip_path and archive_sha256 | Stop before preview | Supply one unchanged FSM CSV ZIP and compute SHA-256 from its exact bytes | Import | |
| Import approval | Approval bound to the exact environment, task code, ZIP path, SHA-256, and operation | Stop before the first mutating request | Present the immutable preview and obtain a standalone affirmative response | Live import is ready | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Local catalog and enclosing skill identify ZCM_MANAGE_CUSTOMER_CENTER_TASK_TEMPLATE and package metadata contains that exact task code | Satisfied | Continue with archive validation | |
| A discovery request filtered by one offering or functional area returns no row while fixed task code and package metadata agree | Non-blocking context mismatch | Continue; do not require another discovery or task-action confirmation | |
| The archive contains the complete exported CSV package and metadata member | Satisfied | Preserve exact bytes and build the immutable preview | |
| A CSV member was deleted, renamed, or replaced, or package no longer matches selected task | Blocked | Use the complete task-level package exported for this task | |
| Approval matches latest immutable preview and SHA-256 is unchanged | Authorized | Hand off once to the repository-selected FSM import workflow | |
| Any preview-bound value or archive byte changes after approval | Blocked | Revalidate and request fresh approval | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation | Accept only export or import | Every run | |
| Task code | Require exactly ZCM_MANAGE_CUSTOMER_CENTER_TASK_TEMPLATE | Every run | |
| ZIP signature | Require a valid ZIP archive | Import | |
| Metadata member | Require exactly one archive member whose basename is ASM_SETUP_CSV_METADATA.xml | Import | |
| Metadata task binding | Require metadata ObjectShortName to include ZCM_MANAGE_CUSTOMER_CENTER_TASK_TEMPLATE | Import | |
| Complete package | Preserve every CSV member; retain intentionally unused objects as header-only CSV files | Import | |
| CSV member size | Reject any individual CSV member larger than 10 MB | Import | |
| Immutable bytes | Do not extract, edit, normalize, or repack the approved ZIP between validation and submission | Import | |
| Package fingerprint | Require a lowercase 64-character SHA-256 calculated from submitted bytes | Import preview and approval | |
| Seeded data | Do not claim that unmodified seeded data can be migrated through task CSV export or import | Export or import | |
| Offering context | Do not require a single offering or functional-area label to establish task identity | Task selection and preflight | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TT.VALIDATE_REQUEST | step | 1 | validate_input | valid->TT.VALIDATE_PACKAGE;invalid->TT.ERROR | none | stop | Before building an export or import preview |
| TT.VALIDATE_PACKAGE | step | 2 | validate_input | valid->TT.APPROVAL;invalid->TT.ERROR | TT.VALIDATE_REQUEST | stop | Before import approval |
