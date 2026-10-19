# Payment Terms Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Current task template and data export | Establish exact task identity from either the explicit selected-task metadata shape or the task-object UI-export shape, plus successful process state, CSV members, columns, keys, package order, release, and source context from current artifacts. |
| 2 | Reference data set | Resolve one exact set before duplicate, update, or end-date evaluation. |
| 3 | Existing payment term and full child state | Resolve exact current header, line, translation, and discount state for update/end-date; detect duplicate create requests and establish values that must be preserved. |
| 4 | Billing cycle | Resolve one supported cycle when balance-forward behavior is requested. |
| 5 | Receivables System Options | Verify the target setting when discount on partial payment is requested. |
| 6 | Conditional business choices and required header defaults | For split terms resolve print lead days and tax/freight allocation. For one-line creates apply and disclose First Installment (`INCLUDE`) because the entity field is mandatory and the only line is the first. For discount rows resolve the discount basis; for creates without discount rows apply and disclose Invoice Amount (`I`). Do not proceed while any material business choice is implicit. |
| 7 | Semantic candidate validation | Independently reconstruct expected rows from the normalized blueprint plus current baseline and require the candidate to match exactly; ZIP/CSV structure alone is insufficient. |
| 8 | Final local-design confirmation | After all values resolve, show the complete business preview, translated descriptions, and update deltas, then require the orchestration-owned design confirmation bound to its design SHA-256 before generating an offline candidate. |
| 8a | Batch atomicity | For 2 through 100 requested operations, require every distinct parent design and dependency to resolve before preview; one failed operation blocks the complete candidate. |
| 9 | Core Data Loader Task Hook | For an intended import only, after the exact immutable FSM archive is prepared, require a validation envelope bound to its SHA-256 before approval and upload. Offline prepare and review stop before this dependency. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PT.DEP.PACKAGE | Current Payment Terms FSM contract | Yes | Every importable request or offline package review | Verify | Attached exact task-level template ZIP for build, attached candidate ZIP for review, current data export when required, and exact ASM_SETUP_CSV_METADATA.xml | inspect_payment_term_package | Prevents invented columns, ordering, keys, failed exports, cross-task archives, and mixed-target packages | Use a successful task-level template for build; require template and baseline from the same environment/release with identical entity, field/type, and CSV contracts | Task identity and identity shape, selected migration tasks when present, process status/type, environment, release, entity files, field/type contract, node path/order, source context |
| PT.DEP.SPLIT | Split-term print/allocation choices | Conditional | More than one payment line exists | Verify | Customer business response recorded in the normalized blueprint |  | Fusion requires positive print lead days for split terms, and tax/freight allocation changes transaction behavior | Provide positive whole-number print lead days and choose allocate across installments or include in the first installment | PrintingLeadDays, FirstInstallmentCode |
| PT.DEP.INSTALLMENT_OPTION | Required header tax/freight option | Yes | Every candidate header | Verify or Lookup | Product-backed `INCLUDE` for a one-line create; otherwise customer response or exact current exported value | inspect_payment_term_package | PaymentTermEO requires FirstInstallmentCode even when a term contains only one installment | Review the disclosed one-line default; for a split term choose how to handle tax and freight | FirstInstallmentCode |
| PT.DEP.DISCOUNT_BASIS | Required header discount calculation basis | Yes | Every candidate header | Verify or Lookup | Product-backed Invoice Amount (`I`) for create without discount rows; otherwise customer response or exact current exported value mapped to supported lookup values | inspect_payment_term_package | PaymentTermEO requires a non-null value even when no discount child rows exist; with discounts it determines which invoice amounts receive the discount | Review the disclosed Invoice Amount default when no discounts exist; otherwise choose Invoice Amount, Lines Only, Lines and Tax excluding Freight, or Lines/Freight/Tax | CalcDiscountOnLinesFlag |
| PT.DEP.SET | Reference data set | Yes | Every create, update, end-date, or persisted-state verification | Lookup | Distinct SetCode values and approved display or business-unit mappings in the current task export handed into task context | resolve_payment_term_set | Prevents cross-set ambiguity and unusable terms | Identify the owning business set when zero or multiple matches remain; current choices must be shown | SetCode, display identity, resolution source, match count |
| PT.DEP.EXISTING | Existing payment term | Conditional | Update, end-date, or duplicate-create check | Lookup | Current four-entity Payment Terms export handed into task context | find_payment_term_exact | Establishes action, immutable Name+set identity, current translatable description, schedules, and values that must be preserved | Provide exact Name and set when no unique match exists; use a supported separate workflow for rename, set move, or child removal | Current header plus line, translation, and discount state |
| PT.DEP.BASE_TEXT | Base-language text row | Conditional | Description is created or updated | Verify | Exactly one current or proposed translation row where Language equals SourceLang | inspect_payment_term_package | Prevents a successful header-only import from leaving the visible translated description unchanged or blank | Resolve the base business language and use the same Description in the header and base row | Header Description, base Language/SourceLang/Description |
| PT.DEP.SEMANTIC | Candidate intent match | Yes | Candidate ZIP generation or review with baseline and blueprint | Verify | Candidate rows plus independently prepared baseline/blueprint rows | inspect_payment_term_package | Prevents a structurally valid ZIP from silently omitting requested values or clearing preserved data | Correct the candidate or normalized request; never waive the mismatch | Exact header, line, translation, and discount row equality |
| PT.DEP.BILLING | Billing cycle | Conditional | Balance-forward behavior is requested | Lookup | Current AR_BALANCE_FORWARD_BILL_CYCLE export handed into task context | resolve_billing_cycle | Balance-forward payment terms require a supported cycle | Provide or export one exact billing cycle | CycleName |
| PT.DEP.PARTIAL | Receivables System Options | Conditional | PartialDiscountFlag is enabled | Verify | Current AR_MANAGE_RECEIVABLES_SYSTEM_OPTIONS export handed into task context | verify_partial_discount_option | Oracle requires the corresponding system option for discounts on partial payments | Export and verify the option in the intended target | partial_discount_option_enabled |
| PT.DEP.DESIGN_CONFIRM | Final local-design confirmation | Yes | Before offline candidate ZIP generation | Verify | Bundled helper preview plus standalone orchestration-owned design confirmation |  | Prevents a ZIP from being created from misunderstood or stale normalized values | Review the complete business summary, before/after changes, preserved-state count, and translated descriptions; provide the orchestration-owned design confirmation only when it is correct | Design SHA-256, template SHA-256, baseline SHA-256, confirmed state |
| PT.DEP.BATCH | Atomic operation set | Conditional | Request contains more than one create, update, or end-date | Verify | Complete normalized operations list and current evidence for every target | inspect_payment_term_package | Prevents partial execution, invented bulk values, duplicate targets, and confirmation of an incomplete request | Resolve all operations, require distinct Name plus SetCode identities, and keep the package at 100 operations or fewer | Operation count, operation IDs, action counts, resolved identities, per-operation readiness |
| PT.DEP.TASK_HOOK | Core Data Loader Task Hook authorization | Yes | Before an FSM import upload; not applicable to offline prepare or review | Verify | Core Data Loader immutable preview and validation envelope |  | Binds task validation and approval to the exact archive | Let Core Data Loader rebuild the preview after any change | Approved archive SHA-256 and current validation envelope |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required evidence or value is already current and exact | Yes |
| Lookup | One documented read-only local resolution can fill the value | Yes |
| Verify | Current evidence must be checked without changing Fusion setup | Yes |
| Blocked | Required evidence, exact match, Task Hook envelope, or approval is absent or ambiguous | No |

## Customer Clarification Outcomes

| Evidence State | Required Outcome | Customer Message Contract |
|---|---|---|
| Exactly one current match | Satisfied | State the resolved business value and source; do not ask a redundant question. |
| No current match | Blocked | State what was supplied, explain why the dependency is needed, show bounded current choices when available, and ask one business question. |
| Multiple current matches | Blocked | Show distinct display names and codes and ask the customer to choose; do not rank or silently select. |
| Evidence absent or stale in offline mode | Blocked | Request the current local artifact and state that no environment call was made. |
| Evidence absent or stale in live mode | Verify | Route a fresh read-only export through the owning workflow before asking the customer for a value the system can resolve. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PT.DEPENDENCIES | decision | 20 | resolve_dependency | ready->PT.LOOKUP_PACKAGE;blocked->PT.BLOCKED | PT.VALIDATE | stop | Input validation passed |
