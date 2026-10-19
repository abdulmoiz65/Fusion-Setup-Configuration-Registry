<!-- fscr-supported-operations: create, update -->
<!-- fscr-create-fields: AR_RECEIPT_SOURCE::AutoBatchNumbering, AR_RECEIPT_SOURCE::BUName, AR_RECEIPT_SOURCE::BankAccountName, AR_RECEIPT_SOURCE::Description, AR_RECEIPT_SOURCE::EndDateActive, AR_RECEIPT_SOURCE::LastBatchNum, AR_RECEIPT_SOURCE::Name, AR_RECEIPT_SOURCE::ReceiptClassName, AR_RECEIPT_SOURCE::ReceiptMethodName, AR_RECEIPT_SOURCE::StartDateActive, AR_RECEIPT_SOURCE::Type1 -->
<!-- fscr-update-fields: AR_RECEIPT_SOURCE::AutoBatchNumbering, AR_RECEIPT_SOURCE::BankAccountName, AR_RECEIPT_SOURCE::Description, AR_RECEIPT_SOURCE::EndDateActive, AR_RECEIPT_SOURCE::LastBatchNum, AR_RECEIPT_SOURCE::ReceiptClassName, AR_RECEIPT_SOURCE::ReceiptMethodName, AR_RECEIPT_SOURCE::StartDateActive, AR_RECEIPT_SOURCE::Type1 -->


# Manage Receipt Sources Input Validation

## Scope

Validate single, mixed, and bulk requests for `AR_MANAGE_RECEIPT_SOURCES`. These rules do not authorize a Fusion import, direct REST write, SQL statement, UI data-entry automation, or update to `AR_BATCH_SOURCES_ALL`.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Exact task evidence | Successful template-only export and fresh current-data export for the same task, environment, and release | Obtain or request corrected evidence | Obtain exact task-level exports for AR_MANAGE_RECEIPT_SOURCES, then resume validation | Create build, duplicate check, verification, or reconciliation | inspect_receipt_source_package |
| Requested operation | create, update, end-date, or verify for each requested source | Ask one consolidated question | Use the customer's explicit lifecycle intent; normalize end-date as an update of EndDateActive | Every request |  |
| Portable identity | BUName and Name | Ask for the exact business unit and source name | Resolve BUName against the target and Name against the exact current export | Every operation | resolve_receivables_business_unit |
| Create design | Type1, AutoBatchNumbering, StartDateActive, and description decision | Ask only for missing business choices | Accept only exact source-backed enums and a valid date | Create |  |
| Automatic numbering | LastBatchNum | Ask for Batch Number Starts After | Require a whole number and explain that the next batch number is this value plus one | AutoBatchNumbering is AUTOMATIC |  |
| Lockbox design | Type1 MANUAL, AutoBatchNumbering AUTOMATIC, ReceiptMethodName, ReceiptClassName, and BankAccountName | Ask for the unresolved value or evidence | Resolve exact method/class and bank evidence; separately prove compatibility, then resume | Explicit lockbox use | resolve_receipt_method_class |
| Update target and patch | Exactly one current BUName plus Name match and at least one explicit changed field | Ask for the exact target or intended change | Preserve all omitted baseline values; never reinterpret an update as create | Update or end-date, including mixed/bulk | find_receipt_source_exact |
| DFF values | AttributeCategory plus exact segment-to-AttributeN mapping and value-set evidence | Ask for the missing mapping/evidence | Obtain target Batch Source DFF metadata, then resume | Any DFF value is requested |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Task identity | Require ObjectShortName AR_MANAGE_RECEIPT_SOURCES, ObjectType TASK, ProcessType EXPORT, completed status, AR_RECEIPT_SOURCE.csv, and ASM_SETUP_CSV_METADATA.xml | Any source ZIP | inspect_receipt_source_package |
| Archive safety and schema | Reject unreadable, encrypted, traversal, duplicate-member, mixed-task, mixed-release, mixed-environment, header, type, or node-path mismatches | Any ZIP | inspect_receipt_source_package |
| Metadata provenance | Candidate metadata must match the validated fresh current-data baseline byte-for-byte; the template owns member and CSV schema/header shape | Build and validate | inspect_receipt_source_package |
| Name | Nonblank, at most 50 characters, exact create collision check within BUName | Every operation | find_receipt_source_exact |
| Description | At most 240 characters | Create or explicit update |  |
| Source type | Accept only MANUAL or AUTOMATIC | Create or explicit update |  |
| Batch numbering | Accept only MANUAL or AUTOMATIC | Create or explicit update |  |
| Last batch number | Whole number from 0 through 999999999999999999 when numbering is AUTOMATIC; blank when MANUAL | Numbering design |  |
| Dates | Require valid dates; EndDateActive cannot precede the effective StartDateActive | Create, date update, or end-date |  |
| Method/class | Require exactly one method and its owning class when either value is supplied | Method/class reference | resolve_receipt_method_class |
| Bank account | Require one exact BU-associated account and separate receipt-method/effective-date compatibility proof | BankAccountName is supplied | resolve_bank_account_business_unit |
| DFF | Populate only with exact deployed context, segment-column mapping, and value-set validation | Any DFF value is requested |  |
| Audit fields | CreatedBy, CreationDate, LastUpdateDate, LastUpdateLogin, and LastUpdatedBy must be blank in candidate rows | Candidate generation |  |
| Onboarding fields | Reject customer-supplied BankAcctCreationSrcCode or BankOnboardingRequestId; emit both blank on create and preserve their baseline values on update/end-date | Every candidate |  |
| Unknown field | Ask what business attribute the customer means and show the closest evidenced fields when useful; retry after clarification instead of guessing a CSV column | Every request |  |
| Duplicate operations | Reject incompatible operations against the same exact BUName plus Name in one request | Mixed or bulk | find_receipt_source_exact |

## Many-record rules

| Rule | Requirement |
|---|---|
| One logical row | One row identifies one operation and one complete BUName plus Name receipt-source design. |
| Row errors | Report every row-level issue in one consolidated follow-up; retain valid rows, retry the whole design after answers, and never silently drop a row or build a partial package. |
| Atomic preview | Show all operations, resolved dependencies, preserved values, warnings, row counts, and design hash together. |
| Confirmation invalidation | Any changed row, source artifact, resolution, release, environment, rule plan, or blueprint requires a new preview and orchestration-owned design confirmation. |
| Pre-confirmation artifacts | Before orchestration-owned design confirmation, write only the normalized blueprint, preview, requirements, and design record. Do not run package-producing adapter commands or create any ZIP. |
| Invalid early package | If a ZIP is produced before confirmation, quarantine its SHA permanently for that run, preserve the artifact as evidence, and begin a fresh attempt; never import it. |
| Runtime boundary | Offline validation may proceed; import remains owned by the Run Book and Core Data Loader. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RS.VALIDATE | decision | 10 | validate_input | valid->RS.DEPENDENCIES;needs_input->RS.NEEDS_INPUT;unsafe->RS.SAFETY_HOLD | none | stop | Every Manage Receipt Sources request before dependency or package evaluation. |
