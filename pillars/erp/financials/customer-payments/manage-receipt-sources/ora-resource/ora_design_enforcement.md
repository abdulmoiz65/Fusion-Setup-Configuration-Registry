<!-- fscr-supported-operations: create, update -->
<!-- fscr-create-fields: AR_RECEIPT_SOURCE::AutoBatchNumbering, AR_RECEIPT_SOURCE::BUName, AR_RECEIPT_SOURCE::BankAccountName, AR_RECEIPT_SOURCE::Description, AR_RECEIPT_SOURCE::EndDateActive, AR_RECEIPT_SOURCE::LastBatchNum, AR_RECEIPT_SOURCE::Name, AR_RECEIPT_SOURCE::ReceiptClassName, AR_RECEIPT_SOURCE::ReceiptMethodName, AR_RECEIPT_SOURCE::StartDateActive, AR_RECEIPT_SOURCE::Type1 -->
<!-- fscr-update-fields: AR_RECEIPT_SOURCE::AutoBatchNumbering, AR_RECEIPT_SOURCE::BankAccountName, AR_RECEIPT_SOURCE::Description, AR_RECEIPT_SOURCE::EndDateActive, AR_RECEIPT_SOURCE::LastBatchNum, AR_RECEIPT_SOURCE::ReceiptClassName, AR_RECEIPT_SOURCE::ReceiptMethodName, AR_RECEIPT_SOURCE::StartDateActive, AR_RECEIPT_SOURCE::Type1 -->


# Manage Receipt Sources Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Identity and operation | Require explicit create, update, end-date, or read-only verify and enforce the operation-specific zero/one-match boundary. |
| 2 | Type and numbering | Validate type, numbering method, and conditional LastBatchNum. |
| 3 | Lockbox and references | Enforce Manual type, Automatic numbering, method/class, and compatible bank evidence for lockbox use. |
| 4 | Effective dates and DFF | Validate date order; ask for corrected dates or exact target DFF mappings and resume after the response. |
| 5 | Confirmation boundary | Show the complete design and source hashes, then stop until the governing implementation orchestration records orchestration-owned design confirmation. |
| 6 | Package safety | Only after confirmation, blank service-owned audit fields, preserve update-only baseline values, and validate deterministic exact-task output. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Create | Error | find_receipt_source_exact | One or more exact BUName plus Name matches exist | Ask whether the customer intended an update, or request a unique create identity; do not change the operation automatically. | Yes, after explicit clarification |
| Update or end-date | Error | find_receipt_source_exact | Zero or multiple exact BUName plus Name matches exist | Ask for the exact business unit and source name, then refresh current evidence if necessary. | Yes |
| Update or end-date | Error | find_receipt_source_exact | No explicit changed business field remains after normalization | Ask what should change; do not generate a no-op ZIP. | Yes |
| Verify | Error | find_receipt_source_exact | Zero or multiple exact matches | Ask for the exact BU and source name or refresh evidence. | Yes |
| AutoBatchNumbering is MANUAL | Error |  | LastBatchNum is populated | Clear LastBatchNum or choose automatic numbering explicitly. | Yes |
| AutoBatchNumbering is AUTOMATIC | Error |  | LastBatchNum is absent or outside 0 through 999999999999999999 | Provide Batch Number Starts After. | Yes |
| Explicit lockbox use | Error | resolve_receipt_method_class | Type1 is not MANUAL, numbering is not AUTOMATIC, or method/class is unresolved | Correct the design and resolve one exact method/class. | Yes |
| BankAccountName is supplied | Error |  | Exact method plus BU plus bank plus effective-date compatibility is unproven and no supported combined resolver is registered | Supply approved target assignment evidence; bank existence alone is insufficient. | No automatic fix |
| DFF value is requested | Error |  | Context, segment mapping, or value-set validation is missing or ambiguous and no portable target-DFF resolver is registered | Supply exact target DFF deployment metadata. | No automatic fix |
| Hard delete, rename, or BU move | Error |  | Operation is requested through the generic FSM CSV route | Preserve current state and use only a separately supported product workflow. | No |
| Mixed or bulk | Error |  | Any row is unresolved, invalid, ambiguous, unsupported, or would be dropped | Ask one consolidated follow-up listing all affected rows; proceed atomically once every row is valid. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_receipt_source_exact | Every create/update/end-date/verify and mixed/bulk request | Exact BUName, Name, and fresh baseline row or zero-match proof | ora_reference_lookups.md |
| resolve_receipt_method_class | Method/class reference or lockbox design | Exact ReceiptMethodName and ReceiptClassName | ora_reference_lookups.md |

## Candidate package invariants

| Invariant | Enforcement |
|---|---|
| Task scope | Exact AR_MANAGE_RECEIPT_SOURCES metadata and AR_RECEIPT_SOURCE.csv only. |
| Source fidelity | Preserve member and CSV schema/header shape from the genuine template, and preserve ASM_SETUP_CSV_METADATA.xml byte-for-byte from the validated fresh current-data baseline. |
| Audit safety | Service-owned audit fields are blank on every candidate; onboarding fields are blank on create and preserved from the baseline on update/end-date. |
| Determinism | Identical blueprint and source artifacts produce byte-identical ZIP content and SHA-256. |
| Independent validation | Reopen and validate against template, current export, blueprint, and rule plan before handoff. |
| Complete preview | Show every operation/value, preservation decision, blocker, warning, row count, source hash, and design hash before orchestration-owned design confirmation. |
| Pre-confirmation boundary | Before the current design is confirmed, only blueprint, preview, requirements, and design-record artifacts may exist. Package-producing commands and ZIP creation are forbidden. |
| Gate ownership | The governing implementation orchestration owns design confirmation; successful adapter validation cannot prove or replace it. |
| Rule-plan binding | Store the compiled rule-plan SHA-256 in the blueprint and include it in the design hash; re-hash it before build, validation, determinism, rollback, and reconciliation. |
| Quarantine | If any ZIP exists before confirmation, preserve it as failed-attempt evidence, reject its SHA permanently, and never import it. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RS.ENFORCE | decision | 50 | design_enforcement | passed->RS.EXECUTION_GATE;needs_input->RS.NEEDS_INPUT;unsafe->RS.SAFETY_HOLD | RS.DEFAULTS | stop | Normalized values, applicable lookup outcomes, and defaults are ready for design validation. |
