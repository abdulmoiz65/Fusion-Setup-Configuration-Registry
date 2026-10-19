---
skill_id: "erp.financials.customer-payments.manage-receipt-sources"
name: "Manage Receipt Sources Setup Task Guidance"
description: "Handles business-language Oracle Receivables receipt-source setup requests. Iteratively resolves missing, ambiguous, or invalid business data through focused follow-up questions, validates business-unit and receipt-method dependencies, deterministically prepares create and update CSV packages from genuine task exports, preserves unspecified update state, delegates every import to Core Data Loader, and requires fresh-export reconciliation before completion."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Customer Payments"
functional_area_code: "ORA_FIN_CUSTOMER_PAYMENTS"
task_code: "AR_MANAGE_RECEIPT_SOURCES"
task_name: "Manage Receipt Sources"
parent_skill_id: "erp.financials.customer-payments"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
version: "0.3.5"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "offline_package_review"
  - "candidate_handoff"
  - "reconciliation_report"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
state_updates:
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-payments/manage-receipt-sources/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-payments/manage-receipt-sources/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "After Core Data Loader creates an immutable preview and the customer supplies its current candidate-specific approval, the authorized FSM adapter may create, update, or end-date receipt-source setup in the approved Fusion environment."
required_privileges: []
---

<!-- fscr-supported-operations: create, update -->
<!-- fscr-create-fields: AR_RECEIPT_SOURCE::AutoBatchNumbering, AR_RECEIPT_SOURCE::BUName, AR_RECEIPT_SOURCE::BankAccountName, AR_RECEIPT_SOURCE::Description, AR_RECEIPT_SOURCE::EndDateActive, AR_RECEIPT_SOURCE::LastBatchNum, AR_RECEIPT_SOURCE::Name, AR_RECEIPT_SOURCE::ReceiptClassName, AR_RECEIPT_SOURCE::ReceiptMethodName, AR_RECEIPT_SOURCE::StartDateActive, AR_RECEIPT_SOURCE::Type1 -->
<!-- fscr-update-fields: AR_RECEIPT_SOURCE::AutoBatchNumbering, AR_RECEIPT_SOURCE::BankAccountName, AR_RECEIPT_SOURCE::Description, AR_RECEIPT_SOURCE::EndDateActive, AR_RECEIPT_SOURCE::LastBatchNum, AR_RECEIPT_SOURCE::ReceiptClassName, AR_RECEIPT_SOURCE::ReceiptMethodName, AR_RECEIPT_SOURCE::StartDateActive, AR_RECEIPT_SOURCE::Type1 -->


# Manage Receipt Sources

## Purpose

Plan, clarify, validate, package, route, monitor, and verify the exact `Manage Receipt Sources` FSM task. A receipt source is owned by one Receivables business unit and may reference a receipt class, receipt method, and bank account. Resolve every correctable issue interactively rather than ending the workflow or inventing a value.

## Customer interaction contract

A business-language request is sufficient. Do not ask a customer for the FSM task code, CSV filename, XML node, database table, service name, or generated identifier. Examples include:

- "Create a manual receipt source for our lockbox in this business unit."
- "Create an automatic receipt source and number batches automatically."
- "Change the description of this receipt source."
- "End-date this receipt source at the end of the quarter."
- "Prepare these receipt sources from my table for offline review."

Normalize the request into create, update, end-date, or verify operations. Ask one consolidated business-language question containing only material unresolved choices. After each answer, rerun normalization and resolution; if anything is still missing, ambiguous, contradictory, or invalid, ask the next smallest useful follow-up and continue this loop until the design is complete. This includes a missing or ambiguous business unit/name, missing create type/numbering/start date, invalid or contradictory dates, automatic numbering without `Batch Number Starts After`, zero or multiple update matches, an update with no explicit change, and unresolved method/class/bank/DFF dependencies. Do not label a correctable business issue as blocked or unsupported. Do not block a valid update merely because optional fields were omitted; preserve those fields from the exact baseline. A global request to proceed never substitutes for the design preview's orchestration-owned design confirmation, and design confirmation never substitutes for Core Data Loader's later candidate-specific approval.

Use these outcomes consistently:

| Outcome | Required behavior |
|---|---|
| Resolved | Continue automatically to the next rule. |
| Needs customer choice | Ask a focused question, retain all already resolved values, and re-evaluate after the answer. |
| Needs target evidence | Attempt the documented read-only lookup or fresh export; if it cannot resolve the value, ask specifically for the missing evidence and resume when supplied. |
| Requested operation lacks this CSV implementation | Explain the exact limitation and ask whether the closest supported outcome—usually end-date, create a replacement, verify only, or use the named product workflow—meets the intent. Continue with the selected supported route. |
| Unsafe or impossible external condition | Do not mutate Fusion; explain the condition and the concrete recovery action, then resume from the same design after it is corrected. |

For every identity or reference:

| Evidence result | Behavior |
|---|---|
| One exact candidate | Disclose the resolved value and evidence, then continue. |
| No candidate | Ask one clear business question; show valid choices when authoritative evidence provides them, then retry after the answer. |
| Multiple candidates | Show distinguishing business fields and ask the customer to choose. |
| Missing or stale evidence | Obtain a fresh exact-task export or supported read-only reference result. |
| Request conflicts with evidence | Explain the conflict and ask which outcome is intended; never turn create into update silently. |

## Task and package contract

- Offering: Financials
- Functional area: Customer Payments
- Task: Manage Receipt Sources
- Task code: AR_MANAGE_RECEIPT_SOURCES
- FSM business object: AR_RECEIPT_SOURCE
- CSV member: AR_RECEIPT_SOURCE.csv
- Metadata member: ASM_SETUP_CSV_METADATA.xml
- XML node: /ReceiptBatchSourceVO/ReceiptBatchSourceVORow
- Portable identity: exact BUName plus Name
- Data Loader mode: FSM; businessObject stays empty

Build only from a successful exact task-level template export. The template owns the CSV member schema, header order, and ZIP member envelope. A fresh exact-task current-data export owns duplicate/update state, Business Unit scope, `ASM_SETUP_CSV_METADATA.xml` content and metadata-member envelope, preservation checks, and reconciliation. The current export must be scoped to exactly the requested Business Unit: its metadata must contain exactly one `FUN_BUSINESS_UNIT` / `ORGANIZATION_ID` scope row. Resolve that scope locally when its displayed value equals every operation's `BUName`, or when its value is a numeric organization identifier and every populated `AR_RECEIPT_SOURCE` row independently has the same exact requested `BUName`. Use the documented Receivables Business Units LOV only as a fallback when the exact-task package does not prove the name-to-scope relationship. A missing, multiple, or mismatched scope, or conflicting populated BU rows, triggers a focused request for a fresh correctly scoped export or authoritative BU evidence. Split cross-Business-Unit requests into separately scoped packages. Reject broader, unscoped, mixed-scope, mixed-task, failed, unsafe, mixed-release, mixed-environment, schema-mismatched, or hand-built source packages.

Acquire task exports through `shared.setup-export.fsm-csv-export` and apply its preflight, approval, timeout, retry, diagnostic, redaction, and known-ProcessId recovery contract. Do not bypass that shared safety boundary with a task-local exporter or an ungoverned retry.

CodeSearch confirms that the Receipt Sources migrator resolves an imported row by `Name + OrgId`, calls `updatePrimaryKeysInXML`, and supplies generated primary-key/object-version attributes before `readXML`. Valid existing-record updates are therefore supported when the exact BU and name resolve to one baseline row. A generic pre-submit relevance alert is a package/context failure, not evidence that the requested update is unsupported.

The package has 34 ordered columns. Treat CreatedBy, CreationDate, LastUpdateDate, LastUpdateLogin, and LastUpdatedBy as service-owned and emit them blank in every candidate row. BankAcctCreationSrcCode and BankOnboardingRequestId are system-owned; keep them blank on create and preserve their exact exported values on update/end-date. Never accept customer-supplied values for either pair.

## Source-Backed Task Behavior

- Identify a receipt source by the exact composite key `BUName + Name`; create requires zero exact matches, while update, end-date, and verification require exactly one current match.
- Require a successful exact-task template export and a fresh current-data export scoped to exactly one matching Business Unit. Accept either an exact textual scope value or a numeric organization identifier corroborated by unanimous populated `BUName` rows; reject broader, mixed-task, mixed-scope, conflicting-row, failed, schema-mismatched, or hand-built source packages.
- Require explicit `BUName`, `Name`, `Description`, `Type1`, `AutoBatchNumbering`, and `StartDateActive` values for create; accept only `MANUAL` or `AUTOMATIC` for source type and batch numbering.
- Require `LastBatchNum` for automatic numbering and keep it blank for manual numbering; the next automatically generated batch number is the supplied value plus one.
- Resolve any requested receipt class, receipt method, and bank account exactly and prove applicable Business Unit, method, bank, and effective-date compatibility before packaging; ask a focused follow-up instead of guessing when evidence is incomplete.
- Preserve every unspecified baseline value on update and end-date, distinguish an omitted field from an explicit supported clear, and suppress no-op updates.
- Treat audit columns as service-owned and onboarding columns as system-owned: emit audit values blank in candidates, keep onboarding values blank on create, and preserve exported onboarding values on update or end-date.
- Populate DFF storage only when target-environment context, segment mapping, and value-set evidence are available; otherwise keep unrequested DFF columns blank and ask for missing deployment evidence when DFF values were requested.
- Validate mixed and bulk requests atomically within one exact Business Unit scope; retain valid business input while asking one consolidated follow-up, and never produce a partial package.
- Support create, exact update, verification/no-op, and end-date-as-update. Do not silently translate hard delete, rename, or Business Unit move requests into a different operation.

## Business design contract

For create, require exact BU, source name, source type, batch-numbering method, and start date. Ask for a description decision instead of silently copying another source. Accept only source type MANUAL or AUTOMATIC and numbering method MANUAL or AUTOMATIC.

For automatic numbering, require an explicit `Batch Number Starts After` whole number; explain that the next generated batch number is that value plus one. For manual numbering, LastBatchNum must be blank.

An explicit lockbox source requires MANUAL source type, AUTOMATIC batch numbering, one exact receipt method and its owning receipt class, and one exact bank account associated with the selected business unit. Bank-account existence is not proof of receipt-method and effective-date compatibility. Attempt the documented read-only resolutions first. If complete compatibility still cannot be proven, ask for the exact missing assignment/effective-date evidence and resume when it is supplied; never guess or silently omit the bank account.

Populate AttributeCategory and Attribute1 through Attribute15 only when the customer requested DFF values and exact target-environment context, segment-to-column mapping, and value-set validation are available. Otherwise keep all DFF columns blank; when DFF values were requested, ask for the missing mapping and generate no candidate.

## Operation and preservation contract

| Request | Handling |
|---|---|
| Create | Require zero exact BUName plus Name matches in the fresh current export. A collision triggers a question; it never becomes update automatically. |
| Update | Require exactly one exact target and at least one explicit effective change. Preserve every unspecified baseline value and ask for clarification only when the target or requested change is missing/ambiguous/invalid. |
| End-date | Require exactly one target and an explicit valid end date on or after its start date. Ask for a corrected date when missing or invalid. Encode a narrow baseline-preserving update. |
| Verify or no-op | Compare requested values with exactly one current row and report differences without creating a candidate. |
| Mixed or bulk | Validate every create/update/end-date row and dependency as one atomic design within one exact Business Unit scope. Ask one consolidated follow-up for all missing or invalid values, retain valid rows, and re-evaluate the whole design after the answer. Do not drop a row or create a partial package. |
| Hard delete, rename, or move to another BU | Ask whether end-dating, creating a replacement, or the separately supported product workflow satisfies the intent. Continue with the selected supported alternative; never silently translate the request. |

For create, omitted optional fields stay blank unless an evidence-backed default is explicitly disclosed. For update/end-date, omitted means preserve the exact baseline value; blank means clear only when the user explicitly requests it and the field supports clearing. Never copy defaults, audit values, DFF values, business units, methods, classes, or bank accounts from the first or most common export row.

## Preview and routed workflow

Before generating a candidate ZIP, show one complete normalized preview: task and target evidence, every operation and BUName plus Name key, source type, numbering method and start value, dates, description, receipt class/method/bank references, DFF intent, preserved values, blockers, warnings, row counts, source hashes, compiled rule-plan SHA-256, and design SHA-256. The compiled rule-plan hash is part of the normalized blueprint and therefore the design hash. Require orchestration-owned design confirmation bound to that exact design, rule plan, and those source hashes. Until that reply is received, stop after writing only the normalized blueprint, preview, requirements, and design record. Do not invoke `build`, `validate`, `determinism`, or `rollback`, and do not create, copy, rename, stage, or hand off any ZIP.

1. Enter through the implementation router, then the Customer Payments skill, and select this exact task by catalog metadata.
2. Apply the six resources and compiled task plan in the read order below.
3. Obtain or validate the genuine exact-task template and fresh current export.
4. Normalize the unchanged request, resolve supported references, and iterate focused follow-up questions until every material ambiguity or invalid value is resolved.
5. Show the complete preview and require orchestration-owned design confirmation. Treat any ZIP created before this gate as an invalid failed-attempt artifact: preserve it as evidence, quarantine its SHA, never import it, and start a fresh uniquely named attempt after a new preview and confirmation.
6. Build from the genuine template, independently validate, rebuild to prove identical SHA-256, and label the result locally validated only.
7. For live work, hand the immutable ZIP to `core.data-loader`. It owns submission preview, current candidate-specific approval, upload, one-time submission, monitoring, logs, and diagnostics. Never use a direct REST write, SQL, table update, or task-local importer.
8. After successful terminal processing, obtain a fresh exact-task export and reconcile every requirement and preservation assertion. Submission or process completion alone is not success.

## Portable task adapter

The generated standard-library adapter discovers repository and project paths at runtime and exposes `manifest`, `normalize`, `build`, `validate`, `determinism`, `rollback`, and `reconcile`. It never stores a laptop path, browser profile, environment, credential, token, or customer export. `rollback` prepares only an evidence-backed narrow reversal of a validated update and never authorizes live submission.

Use a unique attempt directory for every conversation and candidate. The adapter accepts long workspace roots portably, including Windows extended-length filesystem paths, but persisted artifacts must retain ordinary repository-relative paths. Do not reuse, delete, or rewrite another active attempt directory; concurrent prompt tests may share immutable source exports only.

The adapter is a low-level semantic tool and does not own customer confirmation. A caller may invoke its package commands only after the governing implementation orchestration has recorded the current orchestration-owned design confirmation against the exact design and source hashes. Successful adapter output is not evidence that this gate occurred.

Every package-producing or reconciliation command must re-hash the compiled `ora_rule_registry.json` and require it to equal the `rulePlanSha256` stored in the normalized blueprint. A registry change requires normalization, preview, and confirmation again even when all customer-entered business values are unchanged.

## Current documentation and implementation evidence

Use the newest documentation matching the target release. This authoring baseline uses Oracle Financials 26C guidance where an exact page exists, with recorded 26B or 26A fallbacks only where the newer exact topic was unavailable:

- [Where are receipt sources used?](https://docs.oracle.com/en/cloud/saas/financials/26c/fairp/where-are-receipt-sources-used.html)
- [How does automatic batch numbering work?](https://docs.oracle.com/en/cloud/saas/financials/26b/fairp/how-does-automatic-batch-numbering-work.html)
- [Why can't I find a receipt source in the lockbox?](https://docs.oracle.com/en/cloud/saas/financials/26a/fairp/why-can-t-i-find-a-receipt-source-in-the-lockbox.html)
- [Receivables Business Units LOV](https://docs.oracle.com/en/cloud/saas/financials/26c/farfa/api-list-values-receivables-business-units-list-values.html)
- [Receipt Methods REST resource](https://docs.oracle.com/en/cloud/saas/financials/26c/farfa/api-receipt-methods.html)
- [Cash Bank Accounts LOV](https://docs.oracle.com/en/cloud/saas/financials/26a/farfa/op-cashbankaccountslov-get.html)
- [AR_BATCH_SOURCES_ALL data model](https://docs.oracle.com/en/cloud/saas/financials/26b/oedmf/arbatchsourcesall-5270.html)

Reviewed implementation evidence establishes the ownership chain `AR_MANAGE_RECEIPT_SOURCES` to `ReceiptSourceMainFlow` to receipt-source pages, `ReceiptBatchSourceUIAM`, `ReceiptSourceManageUIVO`, `ReceiptBatchSourceEO`, the setup migration service, and `AR_BATCH_SOURCES_ALL`. This is authoring provenance, not permission to update the table or use a private implementation as a public runtime service.

## Resource read order

1. [Input validation](ora-resource/ora_input_validation.md)
2. [Dependency readiness](ora-resource/ora_dependency_readiness.md)
3. [Reference lookups](ora-resource/ora_reference_lookups.md)
4. [Defaulting rules](ora-resource/ora_defaulting_rules.md)
5. [Design enforcement](ora-resource/ora_design_enforcement.md)
6. [Error handling](ora-resource/ora_error_handling.md)
7. Generated [rule registry](ora-resource/ora_rule_registry.json)
8. Generated [E2E adapter](e2e-adapter.json) and [test catalog](e2e-test-catalog.json)

## Refusal rules

- Do not invent a BU, type, numbering policy, starting batch number, class, method, bank account, date, DFF mapping, or lifecycle action.
- Do not choose COMMON, the first export row, a fuzzy match, or the most frequent value.
- Do not build while bank/method/effective-date compatibility or requested DFF mapping is unresolved; ask for the missing evidence and resume when supplied.
- Do not transform a create collision into update or choose among zero/multiple matches.
- Do not generate a ZIP while a create/update/end-date value is missing, ambiguous, contradictory, unresolved, or invalid; keep asking focused business-language follow-ups and re-evaluating until it is resolved.
- Do not invoke any package-producing adapter command or create a ZIP before the current design is confirmed. Quarantine and permanently reject any candidate SHA produced before confirmation.
- Do not populate service-owned audit fields or accept customer-supplied onboarding fields.
- Do not build a partial mixed/bulk package or silently drop an invalid row.
- Do not hard-delete, rename, or move a receipt source through this generic CSV workflow; ask the customer to choose an evidenced supported alternative or the named separate product workflow.
- Do not treat design confirmation as import approval or reuse either gate after a bound input changes.
- Do not claim success without fresh-export reconciliation.
