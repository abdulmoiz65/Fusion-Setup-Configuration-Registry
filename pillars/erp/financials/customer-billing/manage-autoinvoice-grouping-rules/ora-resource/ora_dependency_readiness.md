# AutoInvoice Grouping Rule Dependency Readiness

Sources: SRC-CODE-AMIMPL, SRC-CODE-ORDER-VO, SRC-CODE-GROUPBY-COLUMN-VO, SRC-CODE-GROUPBY-CHOICE-VVO, SRC-CODE-CLASS-SEED.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Line ordering rule | If LineOrderingRuleName is supplied, its exact name must exist in RA_LINE_ORDERING_RULES in the target pod. |
| 2 | Transaction class | Normalize to the system GROUPING_TRX_TYPE code before constructing each class child row. |
| 3 | Group-by characteristic | If a group-by child is requested, verify its exact FromColumnName and target-pod availability. |
| 4 | Deployed DFF configuration | If any DFF field is requested, resolve context and segment rules before preview; for an existing-record update, eligible unresolved evidence may use the exact-field application-validation policy in ora_input_validation.md. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill | Source IDs |
|---|---|---|---|---|---|---|---|---|---|---|
| ordering_rule_name | Existing AutoInvoice line ordering rule | Conditional | LineOrderingRuleName supplied | Lookup | RA_LINE_ORDERING_RULES through FSM import alternate key; no public preflight GET established | find_line_ordering_rule_by_name | Import removes the root row and reports an error when the name is absent | Supply the exact name from this environment | OrderingRuleId is filled by FSM import | SRC-CODE-AMIMPL, SRC-CODE-ORDER-VO |
| transaction_class | Grouping transaction class | Yes | Each class child row | Lookup | GROUPING_TRX_TYPE system seed | resolve_grouping_transaction_class | Class1 is required and duplicate class is rejected | Choose Credit Memo, Debit Memo or Invoice | Class11 code C, D or I | SRC-CODE-CLASS-SEED, SRC-CODE-CLASS-EO |
| grouping_column | Optional grouping characteristic | Conditional | Group-by child row requested | Lookup | RA_GROUP_BY_COLUMNS seed and target-pod state through FSM import | resolve_grouping_column_name | Import removes the child row and reports an error when the exact name is absent | Supply a characteristic available in this environment | ColumnId is filled by FSM import | SRC-CODE-AMIMPL, SRC-CODE-GROUPBY-SEED, SRC-CODE-GROUPBY-COLUMN-VO |
| grouping_dff_context | Deployed grouping-rule DFF | Conditional | DFF context or segment supplied | Evidence unresolved | Target-pod descriptive flexfield setup, not yet inspected | | Context and required segment rules vary by environment | Confirm the deployed context and segments, omit DFF values, or for eligible update uncertainty use the exact-field application-validation policy in ora_input_validation.md | Only verified values or the exact update fields covered by informed acceptance; no inferred defaults | SRC-CODE-PRIMARY-EO, SRC-ORACLE-GROUPING-EDM |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact reference and conditional configuration are verified | Read-only lookup only; create remains under Data Loader |
| Evidence unresolved with informed update acceptance | Only eligible non-key update-field uncertainty is covered by the exact-operation/exact-field policy in ora_input_validation.md | Apply known validations and disclose the accepted uncertainty in the candidate-bound preview; import remains under Run Book and Data Loader |
| Blocked | Reference proven missing or ambiguous, known-invalid values, or unresolved deployed DFF rules without eligible exact-field update acceptance | Stop before candidate preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AIGR.DEPENDENCIES | step | 2 | resolve_dependency | ready->AIGR.ENFORCE;blocked->AIGR.ISSUES | AIGR.VALIDATE | stop | After input validation |
