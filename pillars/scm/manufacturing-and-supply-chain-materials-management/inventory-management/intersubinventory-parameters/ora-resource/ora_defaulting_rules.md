# Intersubinventory Parameters Defaulting Rules

## Source Evidence

| Source | Used For |
|---|---|
| Redwood `onAddNewSubinventoryParameter.js` | Create defaults for `StartDate`, `ReceiptRoutingCode`, and `ManualReceiptExpenseFlag` |
| Redwood `FormDestTypeChangeChain.js`, `FormTransferTypeChangeChain.js`, and `FormReceiptRoutingChangeEventChain.js` | Conditions that retain, assign, or clear the receipt-routing value |
| Redwood create payload shaping | `ManualReceiptExpenseFlag` is omitted for inventory destinations |

## Approved Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| `StartDate` | Current date in `YYYY-MM-DD` | Create operation and `StartDate` is omitted or blank | No; preserve a supplied nonblank date |  |
| Receipt Routing code | `1` | Create, receipt routing applies, neither `ReceiptRoutingCode` nor `ReceiptRouting` is supplied, and the selected route's field is omitted or blank | No; preserve a supplied or resolved value |  |
| `ManualReceiptExpenseFlag` | `false` | Create operation, effective `DestinationTypeCode` is `EXPENSE`, and the flag is omitted or blank | No; preserve a supplied canonical boolean |  |

## Defaulting Behavior

| Situation | What Happens |
|---|---|
| Operation is update | Do not add create defaults; preserve existing values and supplied changes |
| Destination type is inventory | Omit `ManualReceiptExpenseFlag`; do not default it |
| Inventory transfer type is `1` | Receipt routing does not apply; preserve a blank routing field and reject a conflicting supplied routing value |
| Expense destination has `ManualReceiptExpenseFlag` false | Receipt routing does not apply; preserve a blank routing field and reject a conflicting supplied routing value |
| Receipt routing applies and a code or meaning was supplied | Preserve the supplied or resolved code; do not replace it with `1` |
| Receipt routing default `1` is applied | Treat `1` as the sourced Redwood create constant; it is not user input and is not passed backward through the earlier resolver node |
| FSM route is selected and routing applies without explicit input | Emit sourced default code `1` in FSM column `ReceiptRouting`; do not emit REST field `ReceiptRoutingCode` |
| Operation is unknown | Stop and establish create or update context before applying a default |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ISP.APPLY_DEFAULTS | step | 60 | apply_default | defaulted->ISP.VALIDATE_EFFECTIVE_VALUES;not-applicable->ISP.VALIDATE_EFFECTIVE_VALUES;blocked->ISP.HANDLE_ERROR | ISP.RESOLVE_RECEIPT_ROUTING | stop | After approved lookup resolution; apply only the sourced create defaults without overriding explicit input |
