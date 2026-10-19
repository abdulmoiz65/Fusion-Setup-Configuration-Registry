# FSM Category Hierarchy Design Rules

Task: POR_MANAGE_CATALOG_CATEGORY_HIERARCHY. Expected TYPE: SHOPPING. FSM CSV only; execution remains with the generated skill’s routed export, validation, and core.data-loader services. These resources perform local preparation and evidence assessment; they declare no product REST operation.

Source: user-approved rules derived from reviewed native FSM exports and import receipts (September 2026). Preventive safeguards below are authoring policy, not claims of tested Oracle rejection behavior.

Successful FSM tests cover browsing-category creation and purchasing-category relationships, including a new item placement and an unchanged existing relationship. A numeric-looking category name with a descriptive code was accepted. Name-only and other name/code failures do not establish matching precedence or a mandatory CategoryCode rule.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve task boundary | Apply this task’s TYPE and child-kind scope |
| 2 | Review identity and placement | Evaluate reconciliation needs and observed existing parents |
| 3 | Preview intended delta | Describe category creation separately from relationship changes and disclose evidence limits |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| New browsing category or relationship | Error | | A proposed browsing creation has no category row, or the request treats a relationship row as category creation | Use POR_BROWSE_CATEGORY.csv for browsing creation and POR_BROWSE_TREE.csv for placement; a relationship to an existing category need not recreate it | Only explicit requested corrections |
| TopCategoryFlag | Error | | Value is inconsistent with the task-specific guidance in this row | TopCategoryFlag denotes shopping featured-category behavior, not hierarchy root status. Preserve explicitly supplied blank, N or Y values; reject other values. ParentCategoryName and ChildCategoryName determine placement. | No silent flag changes |
| Existing parent evidence | Review | inspect_target_hierarchy_export | A different observed parent is present and the preview has not disclosed potential reassignment | Show existing and intended placement and carry the reviewed intent into the core approval workflow; do not impose an unverified universal one-parent constraint | No silent move or deletion |
| Cross-instance identity | Error | inspect_target_hierarchy_export | A known name/code discrepancy is being treated as equivalent without an explicit target mapping | Require reconciled target identity before import; identical names alone do not guarantee correct FSM resolution | User-supplied mapping only |
| Import package scope | Error | | Unrequested setup changes or missing native members are present | Include only intended data-row changes, retaining all native files, header-only CSVs and unchanged task metadata; do not reimport all exported setup unnecessarily | Remove rows only to implement the reviewed delta |
| Reimport versus new placement | Disclosure | inspect_target_hierarchy_export | Preview or report claims a new relationship when evidence shows an existing identical association | Label an unchanged association reimport separately; if baseline is unavailable label prior placement unverified | Correct the claim only |
| Test coverage | Disclosure | | Outcome is being generalized beyond the task-specific tested scope stated above | Preserve the scope of browsing, purchasing, agent or supplier assignment evidence in review output | Correct the claim only |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| inspect_target_hierarchy_export | Assessing target identity, prior placement or reimport claims; absent evidence remains unverified | Evidence status, provenance, matching rows and observed parents | ora_reference_lookups.md |

No identifier, purchasing flag or target mapping is automatically defaulted. A blank code remains blank unless the user supplies a reconciled value.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCH.DESIGN | step | 40 | design_enforcement | valid->CCH.HANDOFF;blocked->RETURN_ISSUES | CCH.DEPENDENCIES | stop | Reviewing the intended FSM delta |
