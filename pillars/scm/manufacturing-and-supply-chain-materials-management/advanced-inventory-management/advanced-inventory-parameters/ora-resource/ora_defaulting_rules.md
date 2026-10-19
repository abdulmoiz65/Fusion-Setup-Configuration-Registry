# Advanced Inventory Parameters Defaulting Rules

Applies only to the REST-backed BO route. FSM archives bypass this resource and retain their exported values, including blanks; do not inject `A` into an FSM CSV.

## Source Evidence

| Source | Used For |
| --- | --- |
| Redwood `FormPassValueToPageChain.js` | When `CrossDockEnabledFlag` becomes enabled, the UI assigns the existing `CrossDockDueDateSort` or code `A` to the Cross-Dock payload. |

## Approved Default

| Field | Default Value | Applies When | Override User Value? | Resolver |
| --- | --- | --- | --- | --- |
| `CrossDockDueDateSort` | `A` | Confirmed create operation with `CrossDockEnabledFlag` explicitly enabled, and both `CrossDockDueDateSort` and `CrossDockDueDateSortMeaning` absent from supplied inputs. | No. Preserve supplied codes, resolved meanings, explicit nulls, and blanks; do not treat supplied empty values as omitted. | resolve_advanced_inventory_crossdock_due_date_sort |

## Defaulting Behavior

| Input Shape | What Happens |
| --- | --- |
| Cross-Dock is not explicitly enabled | Do not apply a default. |
| Cross-Dock is enabled and a due-date-sort meaning is supplied | Resolve the meaning first; preserve its resolved code. |
| Cross-Dock is enabled and a due-date-sort code is supplied | Preserve the supplied code. |
| Create: Cross-Dock is enabled and both code and meaning are omitted | Set `CrossDockDueDateSort` to `A`. |
| Update: code and meaning are omitted | Do not add a write value; preserve the existing value. If current context is needed for validation and unavailable, stop and request it. |
| A code or meaning is explicitly null or blank | Preserve the explicit input for validation; do not default it to `A`. |
| Operation is unknown | Stop and establish create/update context before defaulting. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| ADV_INV_PARAMS.APPLY_CROSSDOCK_DUE_DATE_SORT_DEFAULT | step | 35 | apply_default | defaulted->ADV_INV_PARAMS.DATALOADER_HANDOFF;not-applicable->ADV_INV_PARAMS.DATALOADER_HANDOFF;blocked->ADV_INV_PARAMS.RETURN_ISSUES | ADV_INV_PARAMS.VALIDATE_EFFECTIVE_VALUES | stop | Evaluate the create-only default after effective-value validation. |
