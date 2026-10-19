# Selection Criteria Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Read identity | A positive decimal SelectionId, a nonblank RequisitioningBUName, or both for a consistency check | Block the read | Supply at least one supported exact identity | Before a GET request | find_selection_criteria_by_identity |
| Selection criteria review | Source Type, Party Type, and Lowest Price preference | Mark the review incomplete | Supply the intended criteria before a design review | Reviewing a planned criterion | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| At least one supported read identity is supplied and every supplied value passes field validation | Continue | Resolve the current criterion with the documented read-only REST lookup; if both are supplied, check that the item GET returns the exact supplied BU name | find_selection_criteria_by_identity |
| No identity is supplied, either value fails field validation, or the two supplied identities do not identify the same criterion | Block | Correct the identity or mismatch; do not select a returned record by position | find_selection_criteria_by_identity |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| SelectionId | Require ASCII decimal digits only and a value greater than zero; reject signs, whitespace, path separators, and other characters before building the item path | SelectionId is used for the read | find_selection_criteria_by_identity |
| Requisitioning BU name | Require a nonblank exact business-unit name without control characters; preserve apostrophes and other printable characters for the lookup rule rather than altering or fuzzy-matching the name | RequisitioningBUName is supplied for the read or consistency check | find_selection_criteria_by_identity |
| Source Type preference | Accept Local, regional, GPO; Regional, local, GPO; or None as documented business choices | Reviewing a planned criterion | |
| Party Type preference | Accept Manufacturer, Distributor, or None as documented business choices | Reviewing a planned criterion | |
| Lowest Price preference | Treat the value as a Boolean preference; false means price is not considered | Reviewing a planned criterion | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPSEL.VALIDATE_INPUT | step | 10 | validate_input | valid->EPPSEL.RESOLVE_CRITERIA;invalid->EPPSEL.HANDLE_ERROR | none | stop | Before a read-only criteria review |

## Oracle Sources

- [Oracle Procurement 26C: Selection Criteria for External Purchase Prices](https://docs.oracle.com/en/cloud/saas/procurement/26c/oaprc/selection-criteria-for-external-purchase-prices.html) — selection scope and source-type, party-type, and lowest-price choices.
- [Oracle Procurement REST API: Get all selection criteria](https://docs.oracle.com/en/cloud/saas/procurement/25d/fapra/op-externalpurchasepricesselectioncriteria-get.html) — field names and Boolean `LowestPriceFlag` type.
