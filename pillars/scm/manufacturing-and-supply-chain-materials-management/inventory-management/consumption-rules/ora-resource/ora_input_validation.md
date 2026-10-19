# Consumption Rules Input Validation

## Source Evidence

| Source | Used For |
|---|---|
| User-approved task-local rule | `OwningPartySite` requires `OwningParty` and `ProcurementBU` in the same source record. |

## Scope Boundary

Data Loader and Fusion own LOV resolution, required-field enforcement, field
formats, domain validation, and relationship validation. This resource adds
only the approved input-completeness dependency.

## Dependency-Aware Validation

| Check | What Happens | Applies When | If It Fails |
|---|---|---|---|
| Owning Party Site context | Require nonblank `OwningParty` and `ProcurementBU` alongside `OwningPartySite`. | `OwningPartySite` is supplied. | Stop before Data Loader handoff and request the missing companion value or values. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CONSUMPTIONRULES.VALIDATE_OWNING_PARTY_CONTEXT | decision | 10 | validate_input | valid->CONSUMPTIONRULES.CHECK_DEPENDENCIES;invalid->CONSUMPTIONRULES.RETURN_ISSUES | none | stop | Every request. Apply the dependency only when `OwningPartySite` is supplied. |
