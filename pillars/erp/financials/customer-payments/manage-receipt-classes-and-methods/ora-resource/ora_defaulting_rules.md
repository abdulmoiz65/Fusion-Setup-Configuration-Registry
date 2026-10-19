# Manage Receipt Classes and Methods Defaulting Rules

## Defaulting policy

Business behavior is never defaulted merely because a value is common in the current export. Missing processing, accounting, bank, currency, lifecycle, confirmation, remittance, clearance, payment-channel, or error-recovery decisions remain questions or blockers.

## Default rules

| Rule | Applies When | Default | Rationale | Override |
|---|---|---|---|---|
| Operation | The prompt explicitly says create, add, update, end-date, or verify | Normalize the explicit verb only | A name collision does not authorize changing an existing setup. | A new explicit customer instruction. |
| Omitted update fields | Updating an exactly resolved baseline row | Preserve the baseline value and every unmentioned child/sibling row | Omission is not a clear instruction. | Explicit supported clear or replacement instruction. |
| Explicit blank | A customer explicitly requests clearing a clearable optional field | Represent clear only after schema and operation support are proven | Prevents accidental data loss. | A supplied replacement value. |
| Audit columns | Any generated candidate row | Blank CreatedBy, CreationDate, LastUpdatedBy, LastUpdateDate, and LastUpdateLogin | These values are service-owned; baseline values remain read-only evidence. | No override without recorded controlled import evidence. |
| Internal IDs and versions | Create row | Leave generated identifiers, object versions, request IDs, and opaque keys blank unless the exact template contract requires an established parent key | Portable setup uses business identities. | Proven template/runtime requirement only. |
| Dates | A date is supplied by the request or copied from current-export/context evidence | Normalize valid `YYYY-MM-DD` and source-export `YYYY/MM/DD` to `YYYY-MM-DD`; serialize every populated candidate date in that canonical form before opening the ZIP | Fusion exports may use slashes while its CSV import rejects that representation; pre-ZIP normalization prevents an immutable invalid archive. | Explicit corrected date; ambiguous or unparseable dates are blocked. |
| Boolean wording | Prompt unambiguously says yes/no, enabled/disabled, or equivalent | Normalize to business true/false, then serialize to Y/N only for a proven Y/N field | Avoids guessing codes for non-boolean enums. | Explicit customer correction. |
| Bulk scope | One row is invalid or ambiguous | Block the complete package; report row-level results | Never silently produce a partial implementation. | Corrected complete request. |

## Values that must not be defaulted

| Area | Required explicit or target-derived value |
|---|---|
| Receipt class | Name, creation method, confirmation behavior, remittance behavior, clearance behavior |
| Receipt method | Name, parent class, start date, and every applicable automatic/bills-receivable choice |
| Method account | BU, bank account, currency, start date, primary choice, override behavior, and applicable GL accounts |
| Card error mapping | Transaction category, error code, primary action, and applicable subsequent action/days |
| Lifecycle | Update versus create, end date, rename, move, delete, and mixed-operation intent |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RCM.DEFAULTS | step | 40 | apply_default | applied->RCM.ENFORCE;blocked->RCM.BLOCKED | RCM.LOOKUP_ERROR | stop | All lookup nodes have resolved or produced an explicit no-op pass. |
