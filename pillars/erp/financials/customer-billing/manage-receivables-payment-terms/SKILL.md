---
skill_id: "erp.financials.customer-billing.manage-receivables-payment-terms"
name: "Manage Receivables Payment Terms Setup Task Guidance"
description: "Handles natural-language Oracle Receivables payment-term requests, including one-term, mixed create/update/end-date, and batches of up to 100 distinct terms, plus export, validation, import, migration, monitoring, and verification. Resolves the catalog-backed FSM task, validates the four-entity PaymentTerm package, delegates every import to Core Data Loader, and verifies every persisted term without requiring customers to know task codes, CSV files, APIs, loaders, or database tables."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Customer Billing"
functional_area_code: "ORA_FIN_CUST_BILL"
task_code: "AR_MANAGE_RECEIVABLES_PAYMENT_TERMS"
task_name: "Manage Receivables Payment Terms"
parent_skill_id: "erp.financials.customer-billing"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
version: "0.10.0"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-billing/manage-receivables-payment-terms/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-billing/manage-receivables-payment-terms/current/"
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
  - "After Core Data Loader creates an immutable preview and the customer replies with the required standalone approval, the authorized FSM adapter may create, update, or end-date Receivables payment-term setup in the approved Fusion environment."
required_privileges:
  - "AR_SET_UP_RECEIVABLES_PAYMENT_TERM_PRIV or an equivalent seeded role for payment-term setup."
  - "AR_MANAGE_RECEIVABLES_PAYMENT_TERM_DATA or the equivalent reference-data-set data-security grant when enforced by the target environment."
  - "ORA_ASM_FUNCTIONAL_SETUPS_USER_ABSTRACT plus task-specific access for FSM CSV export and import."
  - "A reference-data-set data role that permits the intended payment-term set."
---

<!-- fscr-supported-operations: create, update -->
<!-- fscr-create-fields: AR_PAYMENT_TERM::BaseAmount, AR_PAYMENT_TERM::CalcDiscountOnLinesFlag, AR_PAYMENT_TERM::CreditCheckFlag, AR_PAYMENT_TERM::CycleName, AR_PAYMENT_TERM::Description, AR_PAYMENT_TERM::DiscountBasisDateType, AR_PAYMENT_TERM::DueCutoffDay, AR_PAYMENT_TERM::EndDateActive, AR_PAYMENT_TERM::FirstInstallmentCode, AR_PAYMENT_TERM::InUse, AR_PAYMENT_TERM::Name, AR_PAYMENT_TERM::PartialDiscountFlag, AR_PAYMENT_TERM::PrepaymentFlag, AR_PAYMENT_TERM::PrintingLeadDays, AR_PAYMENT_TERM::SetCode, AR_PAYMENT_TERM::StartDateActive, AR_PAYMENT_TERM_DISCOUNT::AR_PAYMENT_TERM.Name, AR_PAYMENT_TERM_DISCOUNT::AR_PAYMENT_TERM.SetCode, AR_PAYMENT_TERM_DISCOUNT::AR_PAYMENT_TERM_LINE.SequenceNum, AR_PAYMENT_TERM_DISCOUNT::DiscountDate, AR_PAYMENT_TERM_DISCOUNT::DiscountDayOfMonth, AR_PAYMENT_TERM_DISCOUNT::DiscountDays, AR_PAYMENT_TERM_DISCOUNT::DiscountMonthsForward, AR_PAYMENT_TERM_DISCOUNT::DiscountPercent, AR_PAYMENT_TERM_DISCOUNT::SequenceNum, AR_PAYMENT_TERM_DISCOUNT::SetCode, AR_PAYMENT_TERM_LINE::AR_PAYMENT_TERM.Name, AR_PAYMENT_TERM_LINE::AR_PAYMENT_TERM.SetCode, AR_PAYMENT_TERM_LINE::DueDate, AR_PAYMENT_TERM_LINE::DueDayOfMonth, AR_PAYMENT_TERM_LINE::DueDays, AR_PAYMENT_TERM_LINE::DueMonthsForward, AR_PAYMENT_TERM_LINE::RelativeAmount, AR_PAYMENT_TERM_LINE::SequenceNum, AR_PAYMENT_TERM_LINE::SetCode, AR_PAYMENT_TERM_TRANSLATION::AR_PAYMENT_TERM.Name, AR_PAYMENT_TERM_TRANSLATION::AR_PAYMENT_TERM.SetCode, AR_PAYMENT_TERM_TRANSLATION::Description, AR_PAYMENT_TERM_TRANSLATION::Language, AR_PAYMENT_TERM_TRANSLATION::Name, AR_PAYMENT_TERM_TRANSLATION::SourceLang -->
<!-- fscr-update-fields: AR_PAYMENT_TERM::BaseAmount, AR_PAYMENT_TERM::CalcDiscountOnLinesFlag, AR_PAYMENT_TERM::CreditCheckFlag, AR_PAYMENT_TERM::CycleName, AR_PAYMENT_TERM::Description, AR_PAYMENT_TERM::DiscountBasisDateType, AR_PAYMENT_TERM::DueCutoffDay, AR_PAYMENT_TERM::EndDateActive, AR_PAYMENT_TERM::FirstInstallmentCode, AR_PAYMENT_TERM::InUse, AR_PAYMENT_TERM::PartialDiscountFlag, AR_PAYMENT_TERM::PrepaymentFlag, AR_PAYMENT_TERM::PrintingLeadDays, AR_PAYMENT_TERM::StartDateActive, AR_PAYMENT_TERM_DISCOUNT::DiscountDate, AR_PAYMENT_TERM_DISCOUNT::DiscountDayOfMonth, AR_PAYMENT_TERM_DISCOUNT::DiscountDays, AR_PAYMENT_TERM_DISCOUNT::DiscountMonthsForward, AR_PAYMENT_TERM_LINE::DueDate, AR_PAYMENT_TERM_LINE::DueDayOfMonth, AR_PAYMENT_TERM_LINE::DueDays, AR_PAYMENT_TERM_LINE::DueMonthsForward, AR_PAYMENT_TERM_LINE::RelativeAmount, AR_PAYMENT_TERM_TRANSLATION::Description, AR_PAYMENT_TERM_TRANSLATION::Name, AR_PAYMENT_TERM_TRANSLATION::SourceLang -->

# Manage Receivables Payment Terms

## Purpose

Plan, validate, prepare or review an offline package, export, import, monitor,
and verify the catalog-backed `Manage Receivables Payment Terms` setup task
under Customer Billing. Resolve customer ambiguity from current evidence and
fail closed instead of inventing setup values.

## Customer Interaction Contract

A business-language request is sufficient. Do not ask the customer to name the
FSM task, CSV files, APIs, Data Loader, internal services, or database tables.
Infer those mechanics from this skill and the routed FDOS workflow.

Examples of sufficient prompts include:

- "Create a Net 30 payment term."
- "Create a term with 50 percent due in 30 days and 50 percent due in 60 days."
- "Update the discount on Net 10 to match this approved design."
- "End-date our legacy immediate payment term."
- "Import the attached approved payment terms into our test environment."
- "Check the Payment Terms load and verify it."
- "Create these 100 payment terms from the attached approved list."
- "Create the new Net 60 term and update the description of our existing Net 45 term."

Ask only for unresolved business or authorization facts that materially change
the result: payment-term identity, reference data set, effective dates,
installments, print lead days for a split term, tax/freight installment option,
discount basis, discounts, balance-forward behavior, translations, flexfields,
target environment, or the required standalone approval.

For an update, treat the exact existing `Name` plus resolved reference data set
as the immutable selector. Ask for the exact name when current evidence contains
zero or multiple candidates. Do not interpret a request to rename a term or move
it to another set as an in-place update; explain that this package workflow does
not support that identity change and ask whether the customer wants a separate
create/end-date design.

## Ambiguity and Clarification Contract

Never require a customer to know `SetCode`, CSV column names, FSM task codes, or
loader terminology. Accept business-language identities such as a reference
data set name, the business unit that must use the term, or a stated sharing
intent, and resolve them only through current target evidence.

The normalized JSON blueprint used by the bundled helper is an internal
execution artifact. Never ask the customer to create, edit, or understand that
JSON. Translate every structured blocker returned by the helper into one clear
business question under the contract below.

For every required identity or lookup-backed value, apply this exact contract:

| Evidence result | Required behavior |
|---|---|
| One exact candidate | Use it, disclose the resolved business value and source, and continue. |
| No candidate | Stop before package preparation and ask one business-first question. Show the supplied value, explain why it is required, and provide current valid choices when available. |
| Multiple candidates | Stop before package preparation and ask the customer to choose. Show distinct display names and codes; never select the first, `COMMON`, `ENTERPRISE`, or a fuzzy match. |
| Missing or stale evidence | In live mode, route a fresh read-only export through the owning workflow. In offline mode, request the current artifact and make no external call. |
| Conflicting request and evidence | State the conflict and ask which business outcome is intended. Do not silently reinterpret create as update, change a set, or replace a date or schedule. |

Ask one consolidated clarification at a time containing only the unresolved
business decisions. Offer a bounded list of current choices and say when more
choices are available. Re-run all affected rules after the reply; do not reuse
an earlier resolution after the target, artifact, request, or release changes.

When one prompt contains several requested changes, normalize it as one
all-or-nothing locally validated batch of distinct Payment Term operations.
Support mixed create, update, and
end-date operations and up to 100 distinct `Name` plus resolved-set targets in
one task-scoped package. Do not invent missing names or expand an unspecified
"100 terms" request: accept an attached list or a customer-stated deterministic
name/value pattern, otherwise ask for the missing business design. Resolve and
validate every operation before preview; one unresolved or invalid operation
blocks the entire batch and no partial ZIP is created. If the prompt addresses
the same parent more than once, consolidate compatible changes into one
operation and show the result; if they conflict, ask which outcome is intended.

For a create request, require one evidence-backed base language and a base
translation row before preview. When target evidence contains zero or multiple
possible languages and the customer did not specify one, ask which business
language to use and create no ZIP. Never treat an absent translation request as
permission to omit the base-language row.

For a payment term with more than one schedule line, require a positive
whole-number Print Lead Days value and ask whether tax and freight should be
allocated across all installments or included in the first installment. Do not
infer either business choice from the term name, allocation percentages, or a
different environment. `FirstInstallmentCode` is mandatory on every header. For
a create with exactly one installment, use and disclose `INCLUDE`: the only
installment is also the first, so this does not change allocation behavior. For
multiple installments, always require the customer's explicit tax/freight
choice. `CalcDiscountOnLinesFlag` is also mandatory on every payment-term
header. When no discount rows are requested, use and disclose the product-backed
Invoice Amount value `I`; when discount rows are requested, require the
customer-selected discount basis. Use the product default Application Date only
for the discount basis date when the customer has not requested another
supported date basis.

## Final Design Confirmation Contract

Before generating an offline candidate ZIP, run the bundled `preview` command
and show one concise business summary containing the action, payment-term name,
reference data set, effective dates, base amount, every installment, discounts,
base/source language, print lead days, installment tax/freight option, discount
basis/date, partial-discount behavior, credit-check/prepayment flags, applied
defaults, and any balance-forward or flexfield behavior. State that BaseAmount
is the installment-ratio denominator, not a currency amount. Then ask the
governing orchestration to capture design confirmation.

For updates, the preview must show a before/after change list, every added row,
and the number of unchanged fields preserved from the current export. Include
the base-language and additional-language descriptions in that preview. An
update preview that shows only the requested header values is incomplete.

For a batch, show the operation count and action counts, then identify every
term by action, exact name, set, dates, and schedule. Show the full detailed
summary for every operation with nondefault flags, discounts, translations,
flexfields, or updates. Bind one orchestration-owned design confirmation to the complete batch
design; never confirm or build a successful subset while another operation is
blocked.

Treat this as confirmation of the normalized local design only. It is not the
Core Data Loader candidate-specific approval required for a later Fusion import and does not authorize
authentication, upload, initiation, or any environment change. Do not infer
the orchestration-owned design confirmation from the original request, a reference-data-set answer, silence, or a
longer message. Bind the confirmation to the preview's design SHA-256 and both
source-package hashes. Any change to the request, resolved value, source ZIP,
blueprint, or target invalidates it and requires a new preview and confirmation.
Keep the archive-generation `confirmation` envelope in the normalized blueprint
when calling `build`; it is workflow metadata excluded from the business-design
hash, not a customer field. It must contain only `confirmed: true` and the exact
preview `design_sha256`. Never remove it before build, translate its snake-case
key to another spelling, or add approval, timestamp, user, or environment data
to that envelope. Store import approval and other execution metadata only in the
separate orchestration run record.

## Setup Task Contract

- Task code: `AR_MANAGE_RECEIVABLES_PAYMENT_TERMS`
- Catalog availability: `Y`
- Export/import support: `Y`
- CSV export/import support: `Y`
- Data Loader import mode: `FSM`
- Catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Supported Scope

| Customer request | Handling |
|---|---|
| Create | Build a new parent payment term and its applicable lines, translations, and discounts after exact-set duplicate checks. |
| Update | Preserve unchanged export-backed values and package only a supported, reviewed change. |
| End-date | Update the supported end-date field after current-state and date validation. |
| Mixed or batch request | Build one all-or-nothing task package for up to 100 distinct parent identities after every operation passes the same create/update/end-date rules. |
| Hard delete | Refuse; use an evidence-backed update or end-date when appropriate. |
| Export | Route through `shared.setup-export.task-level-export`. |
| Validate | Run shared setup/reference validation, then the compiled task-resource plan. |
| Import | Route only through `core.data-loader`; this task skill never chooses or calls an import endpoint or adapter. |
| Monitor | Route request-ID or data-set status and diagnostics through `core.data-loader`. |
| Verify | Run a fresh read-only task export and compare the persisted header, lines, translations, and discounts with the approved preview. |
| Offline prepare | Preview the normalized design, obtain the orchestration-owned design confirmation, then build a candidate ZIP only from an exact successful task-level template and current baseline using the bundled local helper; make no network call and do not treat design confirmation as import approval. |
| Offline review | Inspect an attached ZIP locally, report task scope, metadata, rows, relationships, rule results, and SHA-256, and stop without authentication, upload, or approval. |

## Business Object Package

Treat the PaymentTerm package as one parent-child unit in the order established
by the current target template and `ASM_SETUP_CSV_METADATA.xml`.

| Role | CSV entity | Required business linkage |
|---|---|---|
| Header | `AR_PAYMENT_TERM` | `Name` plus `SetCode` |
| Installment schedule | `AR_PAYMENT_TERM_LINE` | Parent `Name` and `SetCode`, plus unique line `SequenceNum` |
| Translation | `AR_PAYMENT_TERM_TRANSLATION` | Parent identity plus supported `Language` and `SourceLang` |
| Discount schedule | `AR_PAYMENT_TERM_DISCOUNT` | Parent identity plus an existing payment-line sequence; child `SequenceNum` must equal the referenced line sequence, and DiscountPercent must be unique on that line |

## Source-Backed Task Behavior

- A payment term is one parent package containing a header, at least one
  installment line, the required base-language translation, and any applicable
  discount rows. The parent identity is the exact `Name` plus `SetCode`.
  Sources: SRC-FSM-PACKAGE, SRC-INTERNAL-DEV-001.
- `BaseAmount` is the installment-ratio denominator, not a currency amount. The
  relative amounts of all installment lines must add exactly to that base
  amount; one unresolved or invalid line blocks the complete parent operation.
  Sources: SRC-FSM-PACKAGE, SRC-INTERNAL-DEV-001.
- Each installment line has a stable positive `SequenceNum` and must use one
  complete supported due-date method. A split term requires an explicit
  positive whole-number Print Lead Days value and an explicit tax-and-freight
  allocation choice before preview.
  Sources: SRC-FSM-PACKAGE, SRC-INTERNAL-DEV-001.
- A discount belongs to an existing installment line. Its `SequenceNum` must
  equal that line sequence, its percentage must be unique on the line, and no
  line may contain more than three discount rows.
  Sources: SRC-FSM-PACKAGE, SRC-INTERNAL-DEV-001.
- A create must include exactly one evidence-backed base-language translation
  where `Language` equals `SourceLang`. Updating the base description changes
  both the header and that base translation while preserving every unrequested
  non-base translation.
  Sources: SRC-FSM-PACKAGE, SRC-INTERNAL-DEV-001.
- Create, update, and end-date operations may be combined in one all-or-nothing
  task package for distinct parent identities. A duplicate target, conflicting
  operation, unresolved prerequisite, or invalid row blocks the entire package;
  no partial candidate is generated.
  Sources: SRC-FSM-PACKAGE, SRC-INTERNAL-DEV-001.
- An update is a patch against exactly one current exported parent. Preserve
  every unspecified supported header value and child row. `Name` and `SetCode`
  are immutable, and omission is not a supported request to delete a line,
  translation, discount, or parent.
  Sources: SRC-FSM-PACKAGE, SRC-INTERNAL-DEV-001.
- `LastUpdateDate`, `LastUpdatedBy`, `CreationDate`, `CreatedBy`, and
  `LastUpdateLogin` are service-owned. Keep them only as read-only baseline
  evidence and emit them blank in every generated import row.
  Sources: SRC-FSM-PACKAGE, SRC-INTERNAL-DEV-001.
- Build only from a successful exact-task template and current export whose
  environment, Fusion release, entity paths, CSV headers, and metadata agree.
  A broader offering or functional-area archive is review evidence, not a
  Payment Terms import template.
  Source: SRC-FSM-PACKAGE.

## Update Mutation Contract

An update blueprint is a patch against exactly one current exported parent, not
a replacement document. Preserve every unspecified supported header field and
every unspecified line, translation, and discount row. Patch children only by
their stable import identity: payment line `SequenceNum`, translation
`Language`, and discount parent-line sequence plus `DiscountPercent`.

`Name` and `SetCode` identify the parent for this workflow and are not mutable
update fields. Omitting a child row never means delete: Fusion CSV import does
not provide a safe generic delete-by-omission contract. Refuse requests to
remove an installment, translation, or discount, contract a schedule by
omission, rename a term, or move it between sets. Offer a separately reviewed
create/end-date or supported product workflow instead.

`Description` is translatable. When the customer changes the base description,
write the same value to the header and the one current base-language translation
row where `Language` equals `SourceLang`; preserve every non-base translation
unless it was explicitly supplied. If the base row is missing or ambiguous,
stop before preview and request fresh evidence or a business-language choice.
Reject conflicting header and base-translation descriptions. A structurally
valid ZIP is not sufficient unless its complete rows exactly match the
normalized request plus the preserved baseline state.

Never invent columns, audit values, lookup codes, package order, or metadata.
Treat `LastUpdateDate`, `LastUpdatedBy`, `CreationDate`, `CreatedBy`, and
`LastUpdateLogin` as service-owned evidence on every create, update, and
end-date import candidate. Preserve them in the read-only baseline for
diagnosis, but emit them blank in every candidate row.
Derive them from the current target template/data export. Never write directly
to `RA_TERMS_B`, `RA_TERMS_TL`, `RA_TERMS_LINES`, or
`RA_TERMS_LINES_DISCOUNTS`.

Treat current metadata as an executable contract: compare every CSV header to
its declared `XmlAttributeList`/`XmlAttributeTypeList`, and require template and
baseline environment, release, entity contract, and CSV headers to match. Do
not build from mixed-pod or mixed-release exports.

A task-level build template must contain exactly one
`ASM_SETUP_CSV_METADATA.xml`, declare only the Payment Terms entities, and have
a successful completed process status. Accept either of Fusion's exact
task-export identity shapes: one explicit migration task definition with only
`AR_MANAGE_RECEIVABLES_PAYMENT_TERMS` selected, or no task-definition rows and
the top-level `ObjectShortName` equal to that task code with `ObjectType` equal
to `TASK`. A broader functional-area or offering package may be reviewed as a
multi-task package, but this task skill must not rewrite its metadata, extract
it into a new import package, or present it as a task-level Payment Terms
archive.

## Routed Workflow

1. Start through `router/implementation-router/SKILL.md` and select the active project and target environment.
2. Normalize the business request. Resolve each required identity by the ambiguity contract and ask only one consolidated business clarification when evidence cannot prove one result.
3. Determine the requested mode. For offline preparation or review, use only supplied local artifacts. Otherwise export the current task template and, when existing-state comparison is needed, current task data through `shared.setup-export.task-level-export`.
4. Run `shared.validation.setup-data-validator` and `shared.validation.reference-data-validator`.
5. Compile and plan the task-local rules, then evaluate the six resources in the order listed below. Execute every known product constraint in the local validator; a message listed only in documentation is not considered covered.
6. For offline preparation, first run `validate --source-evidence` on both the exact task-level template and current baseline export. This checks their archive, metadata, task scope, status, CSV presence, and source row counts without applying new-candidate rules to pre-existing target rows. Resolve the create base language and all other ambiguity, then run `preview` with the normalized blueprint. Show its complete business summary, including update deltas and translated descriptions, and ask for the orchestration-owned design confirmation; create no ZIP yet. After that exact reply, record the returned design SHA-256 in the internal blueprint confirmation and use `build`. The helper must reject missing or stale confirmation, independently validate the candidate against the current baseline and normalized blueprint, and repeat generation to prove an identical SHA-256. For review of a proposed import package, run `validate`; when a baseline and blueprint are available, both are mandatory so semantic intent is checked rather than ZIP structure alone. These commands are local and never authorize a Fusion write.
7. Treat the build result's `uploadHandoff` as a mandatory human/tool handoff. Confirm the filename and SHA-256, target environment and release, and exact task name/code. Never reuse a ZIP from a failed run or choose a similarly named file. If a person performs the upload, they must open the exact `Manage Receivables Payment Terms` task and use its `Import from CSV File` action; an offering-level or functional-area-level import page will reject this task-scoped archive.
8. For an intended import, hand the exact task context and validated candidate to `core.data-loader`. Core Data Loader owns final immutable archive preparation, Task Hook validation, preview, archive SHA-256 binding, execution routing, upload, and initiation.
9. Stop after the immutable preview and hand the immutable candidate to Core Data Loader for its candidate-specific approval. Do not infer approval from the original request or a longer message.
10. On that separate approval, let Core Data Loader revalidate and submit the unchanged archive once. Do not select a task-local fallback or reconstruct the validation envelope.
11. Treat successful initiation as accepted, not as verified setup. For a later generic status request, let Core Data Loader retrieve status, counts, errors, and available logs without resubmitting.
12. After successful terminal processing, perform a fresh read-only task export and run the bundled `reconcile` comparison against the exact submitted candidate. Mark the setup verified only when every expected header, line, base/additional translation, and discount value matches. System-generated extra translation languages may be reported separately; unexpected extra schedule or discount rows remain mismatches.

## Portable Offline Package Workflow

The bundled helper uses only the Python standard library and repository-relative
paths. It reads ZIP/CSV/XML artifacts locally and never reads environment
properties, credentials, tokens, browser state, or laptop-specific paths.

Use the legacy normalized JSON shape with `action`, `header`, `lines`,
`translations`, and `discounts` for one operation. For more than one operation,
use `operations`, where each item contains `operation_id`, `action`, `header`,
`lines`, `translations`, and `discounts`. Never mix the two shapes. Both shapes
may include optional current `evidence` for reference data
sets, billing cycles, the partial-payment system option, languages, or
flexfield contexts, and an internal archive-generation `confirmation` added
only after standalone customer confirmation. Reference-data-set evidence may prove a valid empty set
that has no Payment Terms rows in the current task export.
  Preserve only template-supported fields. For descriptive flexfields, require
  both the exact current target context and the exact template attribute columns
  proven for that context; context existence alone does not authorize any
  `Attribute1` through `Attribute15` value. Derive evidence only from the routed
current exports; never ask a customer to fabricate technical evidence. For
update or end-date, supply the current baseline so unchanged export-backed
values are retained.

The helper accepts at most 100 operations, requires a unique `operation_id` and
resolved `Name` plus `SetCode` target for each, combines the four entity CSVs only after all
operations pass, and binds confirmation and deterministic generation to the
entire combined row set. A batch failure reports the operation index and ID.
This is an all-or-nothing local validation and generation guarantee, not a
claim that Fusion import processing is one database transaction. Never hand-edit
a partial batch after validation, and always reconcile every operation after
live processing, including after a failed process that might have persisted a
subset.

For create, apply only these product-backed non-business defaults when their
template columns exist: BaseAmount `100` as the ratio denominator,
CreditCheckFlag `N`, InUse `N`, PartialDiscountFlag `N`, PrepaymentFlag `N`,
and DiscountBasisDateType `APPLICATION_DATE`. For a create with one payment
line, also set FirstInstallmentCode to `INCLUDE`; for a create with no discount
rows, set CalcDiscountOnLinesFlag to Invoice Amount code `I`. Both entity
attributes are non-null even when their business behavior is not visible in a
simple Net term. Show every applied default in the preview. Never default
PrintingLeadDays or a split-term FirstInstallmentCode, CalcDiscountOnLinesFlag
when discounts exist, reference data set, language, billing cycle, or flexfield
context.

For update, never apply create defaults. Use the current exact export as the
source of truth, merge only fields and child rows explicitly requested, and
retain all other values. A requested base-description change is mirrored into
the current base-language translation row. The helper reports changed, added,
removed, and preserved state; any removed row is a blocker for this workflow.
Service-owned audit columns are the only baseline fields deliberately cleared
from update and end-date candidates; they are not writable business state.
Before writing any candidate row, canonicalize every metadata `date` value to
ISO `YYYY-MM-DD` and every `dateTime` value to ISO date-time. Fusion current
exports can contain slash-separated dates such as `2026/10/01`; those values
are valid source evidence, but the Payment Terms CSV loader rejects them when
copied unchanged into an update or atomic-batch import candidate.

```text
python pillars/erp/financials/customer-billing/manage-receivables-payment-terms/scripts/payment_terms_fsm_package.py preview --template <task-template.zip> --baseline <task-data-export.zip> --blueprint <request.json>
python pillars/erp/financials/customer-billing/manage-receivables-payment-terms/scripts/payment_terms_fsm_package.py build --template <task-template.zip> --baseline <task-data-export.zip> --blueprint <request.json> --output <candidate.zip>
python pillars/erp/financials/customer-billing/manage-receivables-payment-terms/scripts/payment_terms_fsm_package.py validate --package <candidate.zip> --baseline <task-data-export.zip> --blueprint <request.json>
python pillars/erp/financials/customer-billing/manage-receivables-payment-terms/scripts/payment_terms_fsm_package.py validate --source-evidence --package <task-template-or-current-data-export.zip>
python pillars/erp/financials/customer-billing/manage-receivables-payment-terms/scripts/payment_terms_fsm_package.py reconcile --candidate <submitted-candidate.zip> --export <fresh-successful-task-data-export.zip>
```

If required information is absent or ambiguous, return `blocked` with a single
business clarification and create no ZIP. If the design is complete but not
confirmed, return `confirmation_required`, show the business summary, and
create no ZIP. An offline success means only that
the candidate passed local package and task rules; it does not prove target
authorization, Fusion acceptance, process completion, or persisted state.

## Completion and Evidence Contract

Keep submission, process completion, and persisted-state verification as
separate facts. Do not mark the implementation task complete unless all of the
following are true:

1. Submitted bytes match the approved archive SHA-256.
2. The external process reaches a successful terminal state.
3. Failed rows are zero and warnings are either zero or explicitly accepted.
4. Available process status, counts, logs, and diagnostics are retained by the owning workflow.
5. A fresh read-only export finds the expected payment-term identity in the approved reference data set.
6. Bundled `reconcile` reports `verified`: persisted header, lines, translations, and discounts match the exact approved candidate, with any system-generated extra translation languages disclosed.

If any condition is false or unknown, report the last confirmed state, preserve
safe evidence, and give one next action. Never retry an import automatically.

## Current Oracle Documentation

Use documentation for the target release. The following 26C sources were
verified accessible on 2026-08-12 and are the current authoring baseline; check
for and use a newer published release at runtime:

- [Guidelines for Defining Payment Terms](https://docs.oracle.com/en/cloud/saas/financials/26c/fairp/guidelines-for-defining-payment-terms.html)
- [Payment Terms and Reference Data Sharing](https://docs.oracle.com/en/cloud/saas/financials/26c/faipp/payment-terms-and-reference-data-sharing.html)
- [Receivables Payment Terms service data object](https://docs.oracle.com/en/cloud/saas/financials/26c/oeswf/receivablespaymentterms-d16553e75248.html)
- [Receivables Payment Terms Translation service data object](https://docs.oracle.com/en/cloud/saas/financials/26c/oeswf/receivablespaymenttermstranslation-d16553e74819.html)
- [Receivables Payment Schedule Discount service data object](https://docs.oracle.com/en/cloud/saas/financials/26c/oeswf/receivablespaymentschedulediscount-d16553e75707.html)
- [Export and Import of CSV File Packages](https://docs.oracle.com/en/cloud/saas/applications-common/26c/oafsm/export-and-import-of-csv-file-packages.html)
- [Setup Task CSV Exports REST endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-exports.html)

Core Data Loader remains the mandatory import orchestrator even when Oracle
documents the underlying setup-task CSV import service.

## Registered Implementation Evidence

The CodeSearch baseline refreshed on 2026-08-12 establishes this ownership
chain:

`AR_MANAGE_RECEIVABLES_PAYMENT_TERMS` -> `PaymentTermMainFlow` -> manage/create
pages -> `PaymentTermUIAM` -> payment-term view/entity objects ->
`RA_TERMS_*` persistence.

The FSM business-object mapping covers `AR_PAYMENT_TERM`,
`AR_PAYMENT_TERM_LINE`, and `AR_PAYMENT_TERM_DISCOUNT`; the task export also
contains the translation child. Refresh the current accessible CodeSearch
series when behavior or exception coverage must be reconfirmed. Use the
registered FPHDEV series only as labeled fallback provenance, never as a fixed
runtime dependency.

## Resource Read Order

1. [Input validation](ora-resource/ora_input_validation.md)
2. [Dependency readiness](ora-resource/ora_dependency_readiness.md)
3. [Reference lookups](ora-resource/ora_reference_lookups.md)
4. [Defaulting rules](ora-resource/ora_defaulting_rules.md)
5. [Design enforcement](ora-resource/ora_design_enforcement.md)
6. [Error handling](ora-resource/ora_error_handling.md)
7. Generated [rule registry](ora-resource/ora_rule_registry.json)

The task resource set follows the current v3 contract. Input collection,
spreadsheet/CSV processing, preview generation, approval, payload construction,
Fusion writes, monitoring, and loader diagnostics remain owned by routed
runbooks and Core Data Loader, not by task-local resource files.

## Refusal Rules

- Do not invent a reference data set, billing cycle, language, flexfield context, template column, service route, or accepted value.
- Do not default a missing reference data set to `COMMON`, `ENTERPRISE`, the first exported set, or the set used by a different environment.
- Do not turn a zero-match or many-match lookup into a candidate ZIP; ask one business-first clarification and retain the blocked rule result.
- Do not split a mixed or batch request into an unconfirmed partial package. Validate every operation, cap one package at 100 distinct targets, and require one design confirmation over the complete batch.
- Do not generate arbitrary names or values for a requested count of terms. Require an attached list or an explicit deterministic business pattern that previews every resulting term.
- Do not place two operations for the same Name and resolved reference data set in one batch; consolidate compatible changes or ask about conflicts.
- Do not create a new payment-term ZIP without one evidence-backed base/source language row.
- Do not generate an offline candidate before an orchestration-owned design confirmation bound to the unchanged preview design SHA-256 and source-package hashes.
- Do not strip, rename, or extend the internal `confirmation` envelope between preview and build; only `confirmed` and `design_sha256` are allowed, while import approval and execution metadata belong in the separate run record.
- Do not preview or build a split term until positive whole-number Print Lead Days and the tax/freight installment option are explicitly resolved.
- Do not hand off a candidate whose required header fields, current entity string precisions, child links, or discount line/percentage uniqueness have not passed the bundled executable validator.
- Do not hand off a candidate with a nonblank service-owned audit value in any Payment Terms CSV row, including update and end-date packages.
- Do not hand off a candidate containing an export-format slash-separated date. Preserve the semantic date but emit its ISO import-safe representation.
- Do not treat an update blueprint as a replacement. Preserve every unspecified exported field and child row, and reject a candidate that differs from the normalized blueprint plus baseline even when its ZIP and CSV structure are valid.
- Do not change a base description only in `AR_PAYMENT_TERM`; mirror it into exactly one base-language `AR_PAYMENT_TERM_TRANSLATION` row and preserve non-base translations.
- Do not rename a payment term, move it to another reference data set, or delete an installment, translation, or discount by omission through this workflow.
- Do not upload a task-level Payment Terms ZIP from an offering-level or functional-area-level import page, and do not reuse a ZIP that previously failed or whose SHA-256 differs from the current handoff.
- Do not preview or build discounts until the discount basis is explicitly resolved, each discount is complete and unique, and no line has more than three discounts.
- Do not hide a known invalid value behind a missing-business-choice question. Report all offline-detectable value/range errors first, then ask only for still-relevant unresolved decisions.
- Do not build from template and baseline exports whose environment, Fusion release, metadata field contract, or CSV headers differ.
- Do not treat the orchestration-owned design confirmation as Core Data Loader candidate-specific approval, or Core Data Loader candidate-specific approval as permission to skip design confirmation.
- Do not treat a multi-task, functional-area, offering, failed, or stale export as an exact task-level build template.
- Do not use a direct payment-term REST write, SQL, UI automation, or a legacy task-local import route.
- Do not upload or initiate without a current Core Data Loader Task Hook envelope bound to the exact approved archive SHA-256.
- Do not reuse stale approval after any source, archive, environment, task identity, validation, or target change.
- Do not resubmit after a timeout, unknown outcome, or failed import; reconcile status first.
- Do not call the task complete on an accepted request or process status alone.
- Do not call the task complete until a fresh successful export passes the bundled candidate-to-persisted-state reconciliation.

## Portability

Resolve repository, project, attachments, environment, release, request IDs,
and CodeSearch series at runtime. Recorded absolute paths, sandbox hostnames,
request IDs, and source revisions are provenance only. This skill requires no
laptop-specific path, credential, token, browser state, or fixed environment.
