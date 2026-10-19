# Input Validation

Validate the fixed setup-task identity and complete FSM CSV package before an
export preview or import approval. A filtered offering or functional-area miss
is non-blocking when the local task identity and package metadata agree.

Official sources:

- [How to create assessment templates](https://docs.oracle.com/en/cloud/saas/sales/oasal/how-to-create-assessment-templates.html)
- [Export and import CSV file packages](https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/export-and-import-csv-file-packages.html)
- [Setup Task CSV Imports REST endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-imports.html)

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | operation=export or operation=import | Stop before preview | Select exactly one supported task CSV operation | Every run | |
| Fixed task identity | task_name=Manage Customer Center Assessment Template and task_code=ZCM_MANAGE_CUSTOMER_CENTER_ASSESSMENT_TEMPLATE | Stop before preview | Use identity from enclosing skill and package metadata; do not accept override | Every run | |
| Fusion environment | fusion_environment_context | Stop before authentication or preview | Select one exact configured source for export or target for import and display it in immutable preview | Export or import | |
| Import package | setup_data_zip_path and archive_sha256 | Stop before preview | Supply one unchanged FSM CSV ZIP and compute SHA-256 from exact bytes | Import | |
| Import approval | Approval bound to exact environment, task code, ZIP path, SHA-256, and operation | Stop before first mutating request | Present immutable preview and obtain standalone affirmative response | Live import is ready | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Local catalog and enclosing skill identify ZCM_MANAGE_CUSTOMER_CENTER_ASSESSMENT_TEMPLATE and package metadata contains exact task code | Satisfied | Continue with archive validation | |
| Discovery filtered by one offering or functional area returns no row while fixed task code and package metadata agree | Non-blocking context mismatch | Continue; do not require another discovery or task-action confirmation | |
| Archive contains complete exported CSV package and metadata member | Satisfied | Preserve exact bytes and build immutable preview | |
| CSV member was deleted, renamed, or replaced, or package no longer matches selected task | Blocked | Use complete task-level package exported for this task | |
| Approval matches latest immutable preview and SHA-256 is unchanged | Authorized | Hand off once to repository-selected FSM import workflow | |
| Any preview-bound value or archive byte changes after approval | Blocked | Revalidate and request fresh approval | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation | Accept only export or import | Every run | |
| Task code | Require exactly ZCM_MANAGE_CUSTOMER_CENTER_ASSESSMENT_TEMPLATE | Every run | |
| ZIP signature | Require valid ZIP archive | Import | |
| Metadata member | Require exactly one archive member whose basename is ASM_SETUP_CSV_METADATA.xml | Import | |
| Metadata task binding | Require metadata ObjectShortName to include ZCM_MANAGE_CUSTOMER_CENTER_ASSESSMENT_TEMPLATE | Import | |
| Complete package | Preserve every CSV member; retain intentionally unused objects as header-only CSV files | Import | |
| CSV member size | Reject any individual CSV member larger than 10 MB | Import | |
| Immutable bytes | Do not extract, edit, normalize, or repack approved ZIP between validation and submission | Import | |
| Package fingerprint | Require lowercase 64-character SHA-256 calculated from submitted bytes | Import preview and approval | |
| Seeded data | Do not claim unmodified seeded data can be migrated through task CSV export or import | Export or import | |
| Offering context | Do not require a single offering or functional-area label to establish task identity | Task selection and preflight | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AT.VALIDATE_REQUEST | step | 1 | validate_input | valid->AT.VALIDATE_PACKAGE;invalid->AT.ERROR | none | stop | Before building an export or import preview |
| AT.VALIDATE_PACKAGE | step | 2 | validate_input | valid->AT.APPROVAL;invalid->AT.ERROR | AT.VALIDATE_REQUEST | stop | Before import approval |
