# Reporting Hierarchy Generation Design Enforcement

Source: [Oracle Reporting Hierarchy Generation](https://docs.oracle.com/en/cloud/saas/sales/fauss/reporting-hierarchy-generation.html).

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm hierarchy selection | Use the selected tree structure, tree code, and tree version for the hierarchy that must be generated. |
| 2 | Prevent parallel submission | Do not submit another instance while an existing Reporting Hierarchy Generation instance is running or blocked. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| `submit=true` | Error |  | Required parameter selections are missing, invalid, or excluded from approval. | Supply the documented hierarchy values and bind them to `submit.argument1` through `submit.argument3` before approval. | Yes |
| `submit=true` | Error | reporting_hierarchy_tree | The configured-connection `fndTrees` lookup does not return an exact match for the supplied Tree Structure Code and Tree Code. | Report the invalid tree selection to the user; provide a valid Tree Code for the selected Tree Structure Code before approval. | Yes |
| `submit=true` | Error | reporting_hierarchy_tree_version | The configured-connection `fndTreeVersions` lookup does not return exactly one TreeVersionId equal to the submitted version, or an INACTIVE version lacks explicit confirmation. Classify as FUTURE when EffectiveStartDate is after the current validation date, INACTIVE only when both EffectiveStartDate and EffectiveEndDate are before it, and ACTIVE otherwise. | Report Status, EffectiveStartDate, EffectiveEndDate, and the classification. Supply a valid Tree Version ID, or explicitly confirm use of an INACTIVE version; then confirm all three submitted parameter values before execution. | Yes |
| A scheduled-process instance is already active | Error |  | A second instance is submitted while the first instance remains in progress; Oracle documents subsequent instances as blocked until the first completes. | Wait for the active instance to complete before submitting another instance. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| reporting_hierarchy_tree | Before `submit` approval | Tree Structure Code, Tree Code | ora_reference_lookups.md |
| reporting_hierarchy_tree_version | Before `submit` approval | Tree Structure Code, Tree Code, Tree Version ID | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RH.DESIGN | decision | 7 | design_enforcement | pass->RH.DONE;blocked->RETURN_ISSUES | RH.DEPENDENCIES | stop | Submit dependencies, validated Tree Code and Tree Version, explicit approval, and self-incompatibility checks are resolved. |
