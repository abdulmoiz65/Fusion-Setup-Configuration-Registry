# Input Validation

Validate the fixed setup-task identity and the complete FSM CSV package before
an export preview or import approval. Oracle documents task CSV import by task
code and validates that an uploaded package corresponds to the selected task;
do not make an offering-and-functional-area search an additional eligibility
gate.

Official sources:

- [Manage Classification Groups procedure](https://docs.oracle.com/en/cloud/saas/sales/fadsi/add-to-the-list-of-available-industry-classification-categories.html)
- [Export and import CSV file packages](https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/export-and-import-csv-file-packages.html)
- [Setup Task CSV Imports REST endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-imports.html)

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | operation=export or operation=import | Stop before preview | Select exactly one supported task CSV operation | Every run | |
| Fixed task identity | task_name=Manage Classification Groups and task_code=HZ_MANAGE_CLASSIFICATION_GROUPS | Stop before preview | Use the task identity from the enclosing skill and the package metadata; do not accept an override | Every run | |
| Fusion environment | fusion_environment_context | Stop before authentication or preview | Select one exact configured source for export or target for import and display it in the immutable preview | Export or import is requested | |
| Import package | setup_data_zip_path and archive_sha256 | Stop before preview | Supply one unchanged FSM CSV ZIP and compute SHA-256 from its exact bytes | Import is requested | |
| Import approval | Approval bound to the exact environment, task code, ZIP path, SHA-256, and operation | Stop before the first mutating request | Present the immutable preview and obtain a standalone affirmative response | Live import is ready for submission | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Local catalog and enclosing skill identify HZ_MANAGE_CLASSIFICATION_GROUPS and the package metadata contains that exact task code | Satisfied | Continue with archive validation | |
| A discovery request filtered by one offering or functional area returns no row, while the fixed task code and package metadata agree | Non-blocking context mismatch | Continue with archive validation; do not require another task-discovery or task-action confirmation | |
| The archive contains the complete exported CSV package and its metadata member | Satisfied | Preserve the exact bytes and build the immutable preview | |
| A CSV member was deleted, renamed, or replaced, or the package no longer matches the selected task | Blocked | Use the complete task-level package exported for Manage Classification Groups | |
| Approval matches the latest immutable preview and the archive SHA-256 is unchanged | Authorized | Release the package to the repository-selected FSM import workflow for one submission | |
| Any preview-bound value or archive byte changes after approval | Blocked | Revalidate and request fresh approval | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation | Accept only export or import | Every run | |
| Task code | Require exactly HZ_MANAGE_CLASSIFICATION_GROUPS | Every run | |
| ZIP signature | Require a valid ZIP archive | Import | |
| Metadata member | Require exactly one archive member whose basename is ASM_SETUP_CSV_METADATA.xml | Import | |
| Metadata task binding | Require the metadata ObjectShortName to include HZ_MANAGE_CLASSIFICATION_GROUPS | Import | |
| Complete package | Preserve every CSV member from the exported package; an intentionally unused business object remains as a header-only CSV rather than being deleted | Import | |
| CSV member size | Reject any individual CSV member larger than 10 MB | Import | |
| Immutable bytes | Do not extract, edit, normalize, or repack the approved ZIP between validation and submission | Import | |
| Package fingerprint | Require a lowercase 64-character SHA-256 calculated from the submitted bytes | Import preview and approval | |
| Seeded data | Do not claim that unmodified seeded data can be migrated through task CSV export or import | Export or import | |
| Offering context | Do not require a single offering or functional-area label to establish task identity; Oracle documents this task in more than one Sales context | Task selection and preflight | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CG.VALIDATE_REQUEST | step | 1 | validate_input | valid->CG.VALIDATE_PACKAGE;invalid->CG.ERROR | none | stop | Before building an export or import preview |
| CG.VALIDATE_PACKAGE | step | 2 | validate_input | valid->CG.APPROVAL;invalid->CG.ERROR | CG.VALIDATE_REQUEST | stop | Before import approval |
