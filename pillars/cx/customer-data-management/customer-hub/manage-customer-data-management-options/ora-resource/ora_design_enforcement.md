# Design Enforcement

Enforce the closed task inventory, SITE scope, exact stored codes, cross-option consistency, immutable FSM package, and executor-owned approval.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Fix task and option inventory | Reject task overrides and arbitrary profile codes |
| 2 | Verify SITE state | Read exact definition, level eligibility, current value, and application id |
| 3 | Resolve stored value | Use active lookup code or documented numeric contract; never use UI text as CSV data |
| 4 | Validate option combination | Enforce source-tracking, scope, Groovy, and threshold dependencies |
| 5 | Bind mutation route | Edit only an existing FSM row or update one exact SITE value through Apps Common |
| 6 | Bind exact approval | Invalidate approval after any target, value, package, hash, or evidence change |
| 7 | Verify outcome | Re-export or re-read every affected SITE value and run Validate Setup |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every run | Error | | Task identity or requested code differs from the enclosing closed inventory | Restore the fixed task and choose a supported setting | Yes |
| Any option change | Error | read_cdm_option_definition | SITE is disabled, non-updatable, ambiguous, or the current value is stale | Re-read target state and rebuild preview | Yes |
| Lookup-backed change | Error | resolve_cdm_option_lookup_code | Proposed token is not one exact active code | Select the exact active stored code, not its UI meaning | Yes |
| Source-confidence attribute selection | Error | read_cdm_option_definition | ZCH_ENABLE_SURVIVORSHIP is not Y in the resulting option set | Enable source tracking in the same reviewed change set | Yes |
| Disable source tracking after enablement | Error | read_cdm_option_definition | Current or historical target evidence shows ZCH_ENABLE_SURVIVORSHIP was enabled | Do not disable source tracking | No |
| ORA_ZCH_MERGE_SCOPE=CDM_HV | Error | read_cdm_option_definition | Master, attribute, or agreement selection invokes business or Groovy rules | Choose a compatible optimized selection method | Yes |
| ZCH_GROOVY_RULE=Y | Error | read_cdm_option_definition | ZCH_SETATTRIBUTE_TYPE=ORA_ZCH_RULE | Choose only one compatible rule source | Yes |
| Link automation change | Error | read_cdm_option_definition | Link threshold is changed without a compatible link resolution design | Review resolution type and link behavior together | Yes |
| Merge automation change | Error | read_cdm_option_definition | Merge threshold is changed without a compatible merge resolution design | Review resolution type and merge behavior together | Yes |
| Prepare_import or import | Error | | Requested code has no existing exact SITE row in FND_APP_PROFILE_VALUE.csv | Report export_content_discrepancy; use update_one after live verification | Yes |
| Import | Error | | ZIP bytes, hash, task metadata, changed rows, target, or Core Data Loader envelope differs from approval | Restart validation and approval | Yes |
| Update_one | Error | read_cdm_option_definition | Exact target, current value, proposed stored value, SITE key, or approval is missing or stale | Rebuild the exact direct-update preview | Yes |
| Any uncertain write or accepted process | Error | | Another mutation is proposed before read-only reconciliation | Verify the existing outcome first | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| read_cdm_option_definition | Every view, option change, default request, or changed FSM profile row | Exact definition, application id, SITE eligibility, current value, SITE key, and SqlValidation | ora_reference_lookups.md |
| resolve_cdm_option_lookup_code | Every lookup-backed categorical change | Exact active stored code and UI meaning | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CDMO.DESIGN_GATE | decision | 6 | design_enforcement | pass->CDMO.VALIDATED;fail->CDMO.ERROR | CDMO.APPLY_DEFAULT | stop | Before package preview, direct-update preview, approved execution, or outcome reporting |
