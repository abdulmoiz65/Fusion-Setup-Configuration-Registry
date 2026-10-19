# Selection Criteria Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm scope | Choose all requisitioning BUs only for a common policy; choose one exact requisitioning BU for an intentional override |
| 2 | Apply source-type preference | Decide whether Local, regional, GPO; Regional, local, GPO; or None reflects the intended sourcing priority |
| 3 | Apply party-type preference | Evaluate Manufacturer, Distributor, or None only after source type |
| 4 | Apply price preference | Evaluate Lowest Price only after source type and party type |
| 5 | Review outcome | If eligible prices remain tied after the configured criteria, expect the latest external purchase price line to be selected |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A specific-BU criterion is reviewed | Blocker | find_selection_criteria_by_identity | The requisitioning BU identity is blank, ambiguous, or the GET result does not exactly match it | Supply one exact requisitioning BU identity and rerun the read-only lookup | Yes |
| Source Type is configured | Blocker | | The selected value is outside the documented Local, regional, GPO; Regional, local, GPO; or None choices | Select one documented source-type preference; use None only when source type must not influence selection | Yes |
| Party Type is configured | Blocker | | The selected value is outside Manufacturer, Distributor, or None | Select one documented party-type preference; this criterion is evaluated after source type | Yes |
| Lowest Price is configured | Blocker | | The preference is not represented as a Boolean choice | Specify whether lowest price should be considered; it is evaluated after source type and party type | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_selection_criteria_by_identity | A current criterion or specific-BU identity must be verified | Criterion identity, scope indicators, source type, party type, lowest-price flag, and last-update timestamp | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPSEL.ENFORCE_DESIGN | decision | 50 | design_enforcement | passed->EPPSEL.RETURN_READ_RESULT;blocked->EPPSEL.HANDLE_ERROR | EPPSEL.APPLY_DEFAULTS | stop | A resolved or planned criterion is reviewed |

## Oracle Source

- [Oracle Procurement 26C: Selection Criteria for External Purchase Prices](https://docs.oracle.com/en/cloud/saas/procurement/26c/oaprc/selection-criteria-for-external-purchase-prices.html) — all-BU or specific-BU scope; source-type and party-type choices; source, party, and lowest-price precedence; latest eligible-line tie break.
