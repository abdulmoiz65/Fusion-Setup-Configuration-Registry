# Lot Expiration Actions Reference Lookups

## Source Evidence

| Source | Used For |
|---|---|
| Redwood `InventoryLotExpirationActionsVO/metadata-rules.json` | `AutomatedActionCode` and `ExpirationActionStatusId` are unconditionally hidden by the active default metadata rule. |
| Redwood `lot-expiration-actions-page-chains/getall_standardLookupsLOVFetch.js` and `getall_materialStatusesFetch.js` | The page declares lookup service aliases, but no complete verified Fusion REST URL was provided or approved for task-local resolution. |
| User decision | Author only `ActionDisabledCode` normalization at this stage. |

## Lookup Decision

| Candidate | Decision | Reason |
|---|---|---|
| `AutomatedActionCode` | Not selected | Hidden UI field; no approved complete REST resolver contract. |
| `ExpirationActionStatusId` | Not selected | Hidden UI field; no approved complete REST resolver contract. |
| `ActionDisabledCode` | Not applicable | Checkbox normalization is local input handling, not a reference lookup. |

No local or live lookup resolver is defined for this task. Data Loader receives canonical `ActionDisabledCode` values after the approved normalization.
