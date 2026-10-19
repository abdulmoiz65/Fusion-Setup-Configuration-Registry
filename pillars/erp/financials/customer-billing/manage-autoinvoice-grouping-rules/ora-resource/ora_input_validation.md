# AutoInvoice Grouping Rule Input Validation

<!-- fscr-supported-operations: create, update -->
<!-- fscr-update-fields: AR_AI_GROUPING_RULE::Description, AR_AI_GROUPING_RULE::EndDate, AR_AI_GROUPING_RULE::LineOrderingRuleName, AR_AI_GROUPING_RULE::StartDate -->
<!-- fscr-create-fields: AR_AI_GROUPING_RULE::Description, AR_AI_GROUPING_RULE::EndDate, AR_AI_GROUPING_RULE::LineOrderingRuleName, AR_AI_GROUPING_RULE::Name, AR_AI_GROUPING_RULE::StartDate, ORA_AR_AI_GRP_TXN_TYPE::AR_AI_GROUPING_RULE.Name, ORA_AR_AI_GRP_TXN_TYPE::Class11, ORA_AR_AI_GRP_TXN_REQUEST::AR_AI_GROUPING_RULE.Name, ORA_AR_AI_GRP_TXN_REQUEST::FromColumnName, ORA_AR_AI_GRP_TXN_REQUEST::ORA_AR_AI_GRP_TXN_TYPE.Class11 -->

Scope: AR_MANAGE_AUTOINVOICE_GROUPING_RULES. Validate the exact same-task FSM CSV package before handing it to Data Loader. Sources: SRC-FSM-PACKAGE, SRC-CODE-PRIMARY-EO, SRC-CODE-CLASS-EO, SRC-CODE-GROUPBY-EO, SRC-CODE-CLASS-SEED.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Grouping rule identity | AR_AI_GROUPING_RULE.Name | Block candidate | Ask for a unique rule name of at most 40 characters that does not begin ORA_ | Create | |
| Effective start | AR_AI_GROUPING_RULE.StartDate | Block candidate | Ask for an explicit start date; the UI default does not prove an import default | Create | |
| Transaction class | ORA_AR_AI_GRP_TXN_TYPE.Class11 | Block child row | Ask for Credit Memo, Debit Memo or Invoice; normalize to C, D or I | Each class child row | resolve_grouping_transaction_class |
| Optional characteristic | ORA_AR_AI_GRP_TXN_REQUEST.FromColumnName | Block child row | Ask for a characteristic confirmed in the target environment | Each group-by child row | resolve_grouping_column_name |
| Same-task package | Exported metadata and three task CSV members | Block candidate | Obtain a fresh export of this exact FSM task and preserve its member headers and relationships | Every candidate | |

## Field Validation

| Check | What Happens | Applies When | Resolver | Source IDs |
|---|---|---|---|---|
| Name length and reserved prefix | Reject more than 40 characters and customer-created names beginning ORA_; require uniqueness | Create | | SRC-CODE-PRIMARY-EO |
| Description length | Reject more than 80 characters | When supplied | | SRC-CODE-PRIMARY-EO |
| Date order | Reject EndDate earlier than StartDate | When EndDate supplied | | SRC-CODE-PRIMARY-EO |
| Transaction class | Normalize case-insensitive Credit Memo, Debit Memo and Invoice to C, D and I; reject other values and duplicate classes within one rule | Each class child row | resolve_grouping_transaction_class | SRC-CODE-CLASS-EDIT-UIVO, SRC-CODE-CLASS-LOOKUP-VVO, SRC-CODE-CLASS-SEED, SRC-CODE-CLASS-EO |
| Group-by duplicate | Reject a repeated resolved characteristic within one transaction class | Each group-by child row | resolve_grouping_column_name | SRC-CODE-GROUPBY-EO |
| DFF segments | Respect 30-character contexts and 150-character segments; verify deployed context and segment rules; eligible update uncertainty follows the exact-field policy below | Only when DFF supplied | | SRC-CODE-PRIMARY-EO, SRC-CODE-CLASS-EO, SRC-CODE-GROUPBY-EO |
| Consolidated-billing flag | One-character storage is known; verify accepted codes and applicability; eligible update uncertainty follows the exact-field policy below | Only when ConsBillingUseFlag supplied | | SRC-CODE-PRIMARY-EO |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AIGR.VALIDATE | step | 1 | validate_input | valid->AIGR.DEPENDENCIES;invalid->AIGR.ISSUES | none | stop | Every request |

## Existing-record update and evidence-gap policy

For an existing-record update, resolve exactly one root by unchanged Name from a fresh same-task export. Description, StartDate, EndDate and LineOrderingRuleName have source-backed root-field update contracts. Description is limited to 80 characters; StartDate remains required, EndDate must not precede StartDate, and a supplied line-ordering name must resolve exactly. Preserve every unrequested root/child value. Other non-key update fields remain evidence_unresolved; apply known validations and offer the exact-operation/exact-field governed application-validation choice when only eligible field-contract or resolver uncertainty remains. Record the accepted uncertainty and warning in the blueprint and candidate-bound preview. Keys, audit fields, malformed packages, unresolved target identity, proven-invalid values, source-proven unsupported operations and missing authorization are not overrideable. Retain normal Run Book/Data Loader routing, candidate-specific approval, one submission, diagnostics and fresh-export reconciliation.

Sources: SRC-CODE-AMIMPL, SRC-CODE-PRIMARY-VO, SRC-CODE-PRIMARY-EO; installed Builder loader-validation policy.

## Custom entity validation evidence

When consolidated-invoices opt-in is enabled, `TransactionRequestGroupingRuleEOImpl.validateEntity` rejects a non-Invoice class when ConsBillingUseFlag is Y (`AR_CONS_BILL_TRAN_CLS_NOT_ALOW`), and rejects grouping-column IDs 14, 15, 16, 22, 46, 47 and 180 when the flag is unchecked (`AR_CONS_BILL_GROUP_NOT_ALLOW_U`). Resolve names to IDs and verify the environment feature state before assessing these conditions. Unknown state is not proof of either branch. Source: SRC-CODE-PRIMARY-EOIMPL, lines 798–868. These known-invalid combinations cannot be overridden. The flag test does not establish a closed Y/N value domain.
