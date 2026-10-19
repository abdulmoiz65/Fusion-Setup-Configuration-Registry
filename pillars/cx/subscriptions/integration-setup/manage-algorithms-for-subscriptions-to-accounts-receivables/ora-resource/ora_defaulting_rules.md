# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| CustomizationFlag default expression | False | No custom algorithm behavior is required | Yes | |
| CustomizationFlag default expression | True | A reviewed custom change to Subscription Management and Accounts Receivables Integration is required | Yes | |
| FlexContext | Omit | AttributeContext is Standard | No | |
| RA target column and context | Resolve the column from the public Oracle `RA_INTERFACE_LINES_ALL` reference and the context from the current interface contract | A Receivables target is selected | No | |
| Missing RA target recommendation | Check documented Standard columns by business meaning and source type; when no direct Standard match exists, suggest a DFF slot from the appropriate source-type family using XML `attributeType` or companion describe type: `ATTRIBUTE<n>` for string/varchar/character and Boolean-as-code, `ATTRIBUTE_DATE<n>` for date/datetime, and `ATTRIBUTE_NUMBER<n>` for number/integer/long/decimal/numeric identifiers. Do not infer numeric solely from names ending in `Id`; require type evidence or mark the type assumption unconfirmed. Start at segment 1 or after the highest used same-type-family slot in the active algorithm and current Service Mapping XML | The scenario supplies a source value but no Receivables target column | No | RA target reference, companion source-resolution record, and current interface contract |
| Named assumptions | Evidence-backed source or target recommendations only | The implementer explicitly says to go with assumptions | No | Use-Case Resolution; companion source-resolution record; deployed DFF details |
| TransactionInterfaceHeaderDff AttributeName | Strip only the leading `HEADER_` prefix from a confirmed `HEADER_ATTRIBUTE*` physical column (`HEADER_ATTRIBUTE5` -> `ATTRIBUTE5`) | The insert context is confirmed as `TransactionInterfaceHeaderDff` | No | Current interface contract |
| FlexContext for skip control | Omit | The confirmed `SkipBillLines` control is used | No | |
| TransactionType for skip control | Required. Use the resolved transaction-class expression from the current Service Mapping XML when the skip applies to both invoice and credit memo lines; use the matching confirmed literal or guarded resolved expression when the skip is invoice-only or credit-memo-only | The confirmed `SkipBillLines` control is used | No | Current Service Mapping XML |
| TransactionType for both invoice and credit memo mappings | Resolved transaction-class expression from the current Service Mapping XML, such as the BillLines attribute mapped to `TransactionClass` | The same normal AR insert applies to both invoice and credit memo lines | No | Current Service Mapping XML |
| Transaction condition for invoice-only or credit-memo-only mappings | `if` / `else if` using the resolved transaction-class expression | A normal AR insert applies only to INV or only to CM | No | Current Service Mapping XML |
| TransactionInterfaceLineDff FlexContext | Subscriptions Context | The subscription was created in Subscription Management | No | |
| TransactionInterfaceLineDff FlexContext | ORA_DOO_ORIGIN_SUBSCRIPTIONS | The subscription was created from Order Management | No | |
| TransactionInterfaceLineDff internal reservation | Reject `INTERFACE_LINE_ATTRIBUTE<n>` when `n` is in `1..4` | The subscription was created in Subscription Management and uses `Subscriptions Context` | No | Request a different deployed target |
| TransactionInterfaceLineDff internal reservation | Reject `INTERFACE_LINE_ATTRIBUTE<n>` when `n` is in `1..8` | The subscription was created from Order Management and uses `ORA_DOO_ORIGIN_SUBSCRIPTIONS` | No | Request a different deployed target |
| Regular line DFF AttributeContext | TransactionLineDff | The current interface contract identifies the `ATTRIBUTE<n>`, `ATTRIBUTE_DATE<n>`, or `ATTRIBUTE_NUMBER<n>` pattern as a line DFF | No | Current interface contract |
| TransactionLineDff or TransactionInterfaceHeaderDff FlexContext | Confirm the deployed context; do not default it | A DFF segment is selected | No | Current interface contract or deployed Receivables DFF setup |
| Date target AttributeValue | `toDate(<date_expression>)` | The confirmed physical Receivables target has RA catalog data type `DATE` | No | Groovy Function Guidance |

## Source Anchors

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/subscription-management/fasmq/create-and-manage-account-receivables-service-mappings.html | Delivered CustomizationFlag default and the documented value required for customization |
| https://docs.oracle.com/en/cloud/saas/financials/26b/oedmf/rainterfacelinesall-26242.html | Primary RA interface-line column catalog |
| User-provided Algorithm Groovy contract | Context defaults and omission rules |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ALG_AR_APPLY_DEFAULT | step | 4 | apply_default | applied->ALG_AR_ENFORCE_DESIGN;not_applicable->ALG_AR_ENFORCE_DESIGN | ALG_AR_CHECK_DEPENDENCIES | stop | Dependencies are ready |