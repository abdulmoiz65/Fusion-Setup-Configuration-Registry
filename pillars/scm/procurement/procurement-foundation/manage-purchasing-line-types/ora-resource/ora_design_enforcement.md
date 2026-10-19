# Design Enforcement

Apply these gates before any preview. They define a valid line-type design and do not authorize a direct REST write.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm readiness | Confirm offering, implementation-role, and privilege readiness. |
| 2 | Validate request | Apply only the client-side request contract; the Data Loader or REST execution resolves existing records and references. |
| 3 | Apply defaults | Apply only documented defaults and preserve supplied values unless a rule below blocks them. |
| 4 | Enforce design | Apply immutable-field, credit-line, purchase-basis, and seeded-data restrictions. |
| 5 | Preview and approval | Prepare the selected create or update outcome for the task's separate approval workflow. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any create | Error | | LineTypeCode starts with ORA_ | Choose a nonreserved code; duplicate detection is performed by the Data Loader business object or REST execution | Yes |
| Create with CreditLineFlag true | Error | | ProductTypeCode is not SERVICES, PurchaseBasisCode is not SERVICES, DefaultMatchApprovalLevelCode is not 2-Way, DefaultInvoiceMatchOptionCode is not P, or DefaultReceiptCloseTolerancePercent is not 100 | Omit the field to use the documented default or supply the required credit-line value | Yes |
| Create with PurchaseBasisCode SERVICES or CreditLineFlag true | Error | | DefaultUOMCode is supplied | Omit DefaultUOMCode | Yes |
| Create or update with CreditLineFlag false | Error | | DefaultMatchApprovalLevelCode is outside 2-Way or 3-Way for SERVICES, or outside 2-Way, 3-Way, or 4-Way for GOODS | Select a level permitted by the purchase basis | Yes |
| Create or update with CreditLineFlag false | Error | | DefaultReceiptCloseTolerancePercent is outside 0 through 100 | Supply a value in the documented range or omit it | Yes |
| Update | Info | | Existing-record identity, immutable fields, seed status, and reference values cannot be established client-side | Retain the supplied update request; the Data Loader business object or REST execution accepts or rejects the server-side change | No client-side substitution |
| DFF is supplied | Error | | The supplied DFF row lacks a parent `LineTypeCode` linkage | Provide the parent linkage; the Data Loader business object validates DFF attributes, context, and deployed segment acceptance | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| Data Loader business object or explicitly selected REST execution | Every update | Existing record, immutable-field state, seed status, and reference values | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PLT.ENFORCE_DESIGN | decision | 40 | design_enforcement | create_ready->PLT.READY_FOR_APPROVAL;update_ready->PLT.READY_FOR_APPROVAL;blocked->RETURN_ISSUES | PLT.APPLY_DEFAULTS | stop | Every validated create or update request |
