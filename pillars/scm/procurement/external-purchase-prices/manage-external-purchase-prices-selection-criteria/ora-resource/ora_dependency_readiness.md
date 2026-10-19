# Selection Criteria Dependency Readiness

## Read Dependency

This node consumes only the result of `find_selection_criteria_by_identity` from `ora_reference_lookups.md`. It makes no additional Fusion request. Require the preceding lookup to have resolved one exact criterion and retain its returned scope fields as observed facts. Do not infer all-BU scope from a blank or absent field.

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|
| resolved_criterion | One exact current criterion | Yes | After the declared GET resolves a criterion | Check returned evidence | `find_selection_criteria_by_identity` result | find_selection_criteria_by_identity | The review must be based on the criterion actually returned for the supplied identity | If the lookup is not exact and complete, follow its blocker or not-found transition; do not choose a different record | Returned criterion and its scope fields |

## Boundary for Other Readiness

Procurement/BPA readiness matters when relying on a criterion for downstream purchase-agreement behavior, but this read-only route has no declared verification method for it. Do not assert that readiness or make it a blocker for reviewing the current criterion.

The manifest names the view privilege required for the live read. This route has no role-assignment or BU-access verification API. The declared GET is the only access check: classify an authentication or authorization failure through `ora_error_handling.md`; a successful GET establishes access only to the returned record, not an independently verified grant.

## Dependency Classification

| Result Category | When Used | Can Continue Review? |
|---|---|---|
| Ready | The preceding lookup resolved one exact, complete criterion | Yes; use only the returned facts |
| Blocked | Lookup evidence is missing, incomplete, or inconsistent | No; follow the lookup's blocker or not-found outcome |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPSEL.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | ready->EPPSEL.APPLY_DEFAULTS;blocked->EPPSEL.HANDLE_ERROR | EPPSEL.RESOLVE_CRITERIA | stop | After a criterion is resolved for review |

## Oracle Sources

- [Oracle Procurement 26C: How do I set up Oracle External Purchase Prices?](https://docs.oracle.com/en/cloud/saas/procurement/26c/faepp/how-do-i-set-up-oracle-external-purchase-prices.pdf) — downstream Procurement/BPA context and selection-criteria scope.
- [Oracle Procurement security reference: Purchase Pricing Manager](https://docs.oracle.com/en/cloud/saas/procurement/26b/oapcm/Purchase_Pricing_Manager_job_roles.html) — names the View External Purchase Prices Selection Criteria privilege; this task does not independently inspect grants.
