# AutoInvoice Grouping Rule Design Enforcement

<!-- fscr-supported-operations: create, update -->
<!-- fscr-update-fields: AR_AI_GROUPING_RULE::Description, AR_AI_GROUPING_RULE::EndDate, AR_AI_GROUPING_RULE::LineOrderingRuleName, AR_AI_GROUPING_RULE::StartDate -->
<!-- fscr-create-fields: AR_AI_GROUPING_RULE::Description, AR_AI_GROUPING_RULE::EndDate, AR_AI_GROUPING_RULE::LineOrderingRuleName, AR_AI_GROUPING_RULE::Name, AR_AI_GROUPING_RULE::StartDate, ORA_AR_AI_GRP_TXN_TYPE::AR_AI_GROUPING_RULE.Name, ORA_AR_AI_GRP_TXN_TYPE::Class11, ORA_AR_AI_GRP_TXN_REQUEST::AR_AI_GROUPING_RULE.Name, ORA_AR_AI_GRP_TXN_REQUEST::FromColumnName, ORA_AR_AI_GRP_TXN_REQUEST::ORA_AR_AI_GRP_TXN_TYPE.Class11 -->

Sources: SRC-ORACLE-GROUPING-ATTR, SRC-CODE-GROUPBY-CHOICE-VVO, SRC-CODE-PRIMARY-EO, SRC-CODE-CLASS-EO, SRC-CODE-GROUPBY-EO.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate business intent | Identify the requested grouping rule, transaction class and optional grouping characteristics. |
| 2 | Check conditional fields | Resolve deployed DFF rules and consolidated-billing intent before using those fields. |
| 3 | Preview gate | Route the candidate through Run Book and Data Loader's candidate-bound preview and approval contract. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? | Source IDs |
|---|---|---|---|---|---|---|
| A DFF context or segment is supplied without verified prerequisites or eligible exact-field update acceptance | Error | | Deployed context, enabled segments or requiredness have not been verified | Omit DFF fields or inspect pod configuration before preview | No automatic fix | SRC-CODE-PRIMARY-EO, SRC-CODE-CLASS-EO, SRC-CODE-GROUPBY-EO |
| ConsBillingUseFlag is supplied without verified prerequisites or eligible exact-field update acceptance | Error | | Accepted code and applicability remain unverified | Omit field until source and pod behavior are established | No automatic fix | SRC-CODE-PRIMARY-EO |
| Consolidated-billing characteristic is requested | Error | resolve_grouping_column_name | Target pod has not confirmed the opt-in and characteristic | Verify feature and exact UI choice before preview | No automatic fix | SRC-CODE-GROUPBY-CHOICE-VVO, SRC-CODE-GROUPBY-SEED |
| Physical delete is requested | Error | | No source-backed deletion contract exists | Use only a separately verified lifecycle action | No automatic fix | SRC-CODE-AMIMPL |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_grouping_column_name | A consolidated-billing characteristic is requested | Exact FromColumnName and target-pod feature availability | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AIGR.ENFORCE | step | 3 | design_enforcement | pass->AIGR.GATE;blocked->AIGR.ISSUES | AIGR.DEPENDENCIES | stop | Before preview |

## Existing-record update and evidence-gap policy

For an existing-record update, resolve exactly one root by unchanged Name from a fresh same-task export. Description, StartDate, EndDate and LineOrderingRuleName have source-backed root-field update contracts. Description is limited to 80 characters; StartDate remains required, EndDate must not precede StartDate, and a supplied line-ordering name must resolve exactly. Preserve every unrequested root/child value. Other non-key update fields remain evidence_unresolved; apply known validations and offer the exact-operation/exact-field governed application-validation choice when only eligible field-contract or resolver uncertainty remains. Record the accepted uncertainty and warning in the blueprint and candidate-bound preview. Keys, audit fields, malformed packages, unresolved target identity, proven-invalid values, source-proven unsupported operations and missing authorization are not overrideable. Retain normal Run Book/Data Loader routing, candidate-specific approval, one submission, diagnostics and fresh-export reconciliation.

Sources: SRC-CODE-AMIMPL, SRC-CODE-PRIMARY-VO, SRC-CODE-PRIMARY-EO; installed Builder loader-validation policy.
