# Landed Cost Reference Types Design Enforcement

Source: User-supplied requirement that Landed Cost Reference Types use Data Loader only with the landedCostReferenceTypes business object.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Data Loader route | Confirm that core.data-loader is the only selected executor for the Landed Cost Reference Types load. |
| 2 | Registered business object | Use the registered landedCostReferenceTypes business object through core.data-loader. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A Landed Cost Reference Types load or delete is requested | Blocker | | The selected executor is not core.data-loader, or the registered business object is not landedCostReferenceTypes | Route the load or delete only through core.data-loader with the landedCostReferenceTypes business object. | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LANDED_COST_REFERENCE_TYPES.ENFORCE_DATA_LOADER_ROUTE | step | 50 | design_enforcement | compliant->LANDED_COST_REFERENCE_TYPES.EXECUTION_GATE;noncompliant->RETURN_ISSUES | LANDED_COST_REFERENCE_TYPES.CHECK_EXECUTION_CONTRACT | stop | Before preview or a live Landed Cost Reference Types load or delete. |
