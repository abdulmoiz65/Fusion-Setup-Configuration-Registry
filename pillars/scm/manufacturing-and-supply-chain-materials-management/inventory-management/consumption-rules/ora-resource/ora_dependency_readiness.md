# Consumption Rules Dependency Readiness

## Source Evidence

| Source | Used For |
|---|---|
| User-approved task-local rule | An `OwningPartySite` source value requires the related Fusion data context: `OwningParty` and `ProcurementBU`. |
| User-provided BO registration record | Provenance only: `inventoryConsumptionRules` was reported as registered. It is not runtime readiness evidence. |
| Per-run Data Loader metadata preflight | Runtime evidence for the selected environment and `inventoryConsumptionRules` discriminator; a prior successful preflight cannot be reused. |

## Dependency Rules

| Dependency | Mandatory | Applies When | Status | Value Source | User Guidance |
|---|---|---|---|---|---|
| Owning Party Site Fusion data context | Conditional | `OwningPartySite` is supplied | Ready only when the preceding input gate confirms both companion values | Source record | Supply `OwningParty` and `ProcurementBU` for the same source record; Data Loader and Fusion validate the supplied values. |
| Data Loader metadata preflight | Yes | Before each Data Loader handoff | Per-run verification required | Selected environment and `inventoryConsumptionRules` discriminator | Run the metadata preflight for this environment. Record its environment, BO discriminator, timestamp, and result. A failed or unavailable preflight blocks the handoff; do not use direct REST. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CONSUMPTIONRULES.CHECK_DEPENDENCIES | decision | 20 | resolve_dependency | ready->CONSUMPTIONRULES.DATALOADER_HANDOFF;blocked->CONSUMPTIONRULES.RETURN_ISSUES | CONSUMPTIONRULES.VALIDATE_OWNING_PARTY_CONTEXT | stop | Every request after the Owning Party Site input gate and after a successful per-run `inventoryConsumptionRules` metadata preflight for the selected environment. |
