# Consumption Rules Error Handling

## Task-Specific Handling

| Condition | Classification | Action |
|---|---|---|
| `OwningPartySite` is supplied without `OwningParty` or `ProcurementBU` | input validation | Stop before Data Loader handoff and request the missing companion value or values. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CONSUMPTIONRULES.DATALOADER_HANDOFF | terminal | 50 | terminal | none | CONSUMPTIONRULES.CHECK_DEPENDENCIES | continue | The approved dependency passes; hand off the source to `core.data-loader`, which owns LOV and backend validation. |
| CONSUMPTIONRULES.RETURN_ISSUES | terminal | 90 | terminal | none | CONSUMPTIONRULES.VALIDATE_OWNING_PARTY_CONTEXT | continue | The approved dependency is incomplete. |
