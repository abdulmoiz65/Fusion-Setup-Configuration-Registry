# FSM Category Hierarchy Dependencies

Task: POR_MANAGE_CATALOG_CATEGORY_HIERARCHY. Expected TYPE: SHOPPING. FSM CSV only; execution remains with the generated skill’s routed export, validation, and core.data-loader services. These resources perform local preparation and evidence assessment; they declare no product REST operation.

Source: user-approved rules derived from reviewed native FSM exports and import receipts (September 2026). Preventive safeguards below are authoring policy, not claims of tested Oracle rejection behavior.

Successful FSM tests cover browsing-category creation and purchasing-category relationships, including a new item placement and an unchanged existing relationship. A numeric-looking category name with a descriptive code was accepted. Name-only and other name/code failures do not establish matching precedence or a mandatory CategoryCode rule.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Selected task package | Complete local contract checks before using any rows as reference evidence |
| 2 | Parent and child evidence | Consume the local evidence assessment and distinguish same-package browsing creation from existing target references |
| 3 | Routed execution prerequisites | Leave environment, privileges, catalog flags, package validation and approval checks to the declared core workflow |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PARENT_REFERENCE | Intended browsing parent | Yes | Every relationship | Assess as supplied-in-package, observed, unverified or ambiguous | Intended rows and supplied target export evidence | inspect_target_hierarchy_export | Placement refers to a browsing parent; snapshot absence cannot establish nonexistence | A new browsing parent needs a corresponding category row; retain uncertainty about existing parents for FSM validation | Evidence status only |
| CHILD_REFERENCE | Intended browsing or purchasing child | Yes | Every relationship | Assess as supplied-in-package, observed, unverified or ambiguous | Intended rows and supplied target export evidence | inspect_target_hierarchy_export | Creating a browse row does not create an item-master category | Use category rows for new browsing children; preserve supplied purchasing identity for server validation | Evidence status only |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Locally supported | Intended browse category is in the package or reference is observed in attributed target evidence | No additional external operation; evidence is not live existence validation |
| Unverified | Snapshot or matching row is absent, stale or scope-limited | No exploratory lookup or auto-create; disclose and continue only to the declared FSM validation workflow |
| Reconciliation required | Supplied target evidence conflicts with requested identity | Stop preparation until an explicit mapping or corrected input is supplied; never auto-create a purchasing category |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCH.DEPENDENCIES | step | 30 | resolve_dependency | assessed->CCH.DESIGN;conflict->RETURN_ISSUES | CCH.EVIDENCE | stop | Classifying reference evidence before preview |
