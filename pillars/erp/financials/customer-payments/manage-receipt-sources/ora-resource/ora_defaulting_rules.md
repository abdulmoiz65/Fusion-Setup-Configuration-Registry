# Manage Receipt Sources Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Operation | Normalize only an explicit create, update, end-date, or verify; never infer lifecycle intent from whether a name currently exists | Every request | Yes, only by a new explicit instruction |  |
| Description | Blank only after the customer confirms no description | Create | Yes |  |
| EndDateActive | Blank | Create without a bounded active period | Yes |  |
| DFF fields | Blank AttributeCategory and Attribute1 through Attribute15 | No DFF value is requested | No implicit DFF population |  |
| Audit fields | Blank CreatedBy, CreationDate, LastUpdateDate, LastUpdateLogin, and LastUpdatedBy | Every candidate row | No |  |
| Omitted update fields | Preserve the exact current baseline value | Update or end-date | Yes, only by an explicit requested change |  |
| Onboarding fields | Blank on create; preserve on update or end-date | Every candidate row | No customer override |  |
| Natural-language dates | Normalize to ISO YYYY-MM-DD in the blueprint; serialize using the exact template convention at build time | A date is provided | Yes, by explicit corrected date |  |

## Values with no business default

| Field | Required behavior |
|---|---|
| BUName | Ask or resolve exactly; never choose COMMON, the first row, or the most frequent BU. |
| Name | Ask for the customer-owned name; never generate or copy one. |
| Type1 | Ask Manual or Automatic when the prompt does not establish it. |
| AutoBatchNumbering | Ask Manual or Automatic; do not infer from source type or row frequency. |
| LastBatchNum | Require an explicit whole number on create or safely preserve the baseline on update when numbering remains automatic. |
| StartDateActive | Require an explicit date for create; never assume today. |
| ReceiptMethodName and ReceiptClassName | Resolve exactly when applicable; never choose the first method under a class. |
| BankAccountName | Require exact target evidence and compatibility when applicable. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RS.DEFAULTS | step | 40 | apply_default | applied->RS.ENFORCE;needs_input->RS.NEEDS_INPUT | RS.LOOKUP_BANK | stop | All applicable confirmed lookups resolved or produced an explicit no-op pass. |
