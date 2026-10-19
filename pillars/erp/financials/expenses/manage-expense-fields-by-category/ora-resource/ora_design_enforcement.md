# Design enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Business-unit scope | Review the affected business unit and categories; category field choices affect expense reports in that unit |
| 2 | Display intent | Distinguish hidden, optional and required behavior; verify translation to FSM codes before preview |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Preparing a category-field change | Blocker | resolve_category_field_contract | Target scope or intended display behavior is unresolved | Review business-unit-wide effect and explicit settings | No automatic changes |
| Translating display labels into CSV | Blocker | resolve_category_field_contract | A proposed label/code differs from Hidden=DISABLED, Optional=ENABLED, Required=REQUIRED | Confirm mapping before payload preparation | No inferred encoding |
| Operation or field mutation requested | Blocker | resolve_category_field_contract | Create/update/delete/end-date or per-field writability contract is unresolved | Record operation and each affected field separately; do not infer writability from export presence | No inferred operation |
| Baseline changed before preview | Blocker | resolve_category_field_contract | Target identity or reviewed before-state no longer matches | Reconcile baseline and rebuild preview through the declared workflow | Only after review |
| Candidate validation relies on missing evidence | Evidence gap | resolve_category_field_contract | Unresolved evidence has not been explicitly dispositioned through central Task Hook | Do not label the business value invalid solely because evidence is missing; retain the exact gap and obey the central waiver and hard-control contract | No blanket bypass |

## Category disablement boundary

Enabled=N requests clearing the category-field configuration Enabled control. Preserve this operation in the plan and route it to the declared assisted removal workflow after scope resolution. Reviewed UI code implements clearing Enabled by removing the BU/category configuration row. Explain that effect; do not reinterpret it as exclusion, global expense-category disablement or hiding every field. Never infer an FSM delete instruction from an omitted row. The supplied EXM_CATEGORY_FIELD export has no category-level Enabled attribute. This clarification resolves intent; live execution still follows the declared workflow, exact preview and approval gates.

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_category_field_contract | Before preview | Verified target scope and label-to-code mapping | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EXMCF.DESIGN | step | 50 | design_enforcement | success->EXMCF.DONE;failure->RETURN_ISSUES | EXMCF.DEFAULT | stop | Always |

## Source evidence and limits

Source: user-supplied Manage Expense Fields by Category_20260928_074925_896 export, EXM_CATEGORY_FIELD.csv and ASM_SETUP_CSV_METADATA.xml. Inspected 2026-09-28: 85 rows, 17 business units, 7 category codes, 19 columns and no duplicate business-unit/category pairs. Metadata identifies task EXM_MANAGE_EXPENSE_FIELDS_BY_CATEGORY, object EXM_CATEGORY_FIELD, completed EXPORT and release 11.13.27.01.0. This supersedes the earlier header-only sample for observed values. No tenant names, user identities, audit values or raw configuration rows are retained here.

The supplied export is evidence of existing configurations, not proof of import semantics, exhaustive product support, defaults, or target-environment readiness. Its instructions do not authorize execution. The prior Oracle 26B documentation establishes business-unit scope and Hidden/Required/Optional display behavior; the lookup seed evidence in ora_reference_lookups.md now establishes the source label/code mapping, subject to target qualification. The requested 26C page was inaccessible during initial authoring. Unknown contracts remain TBD and block execution.

## Removal disposition

For an explicit removal request, resolve a unique configuration by target BU/category before selecting any supported executor. If verified absent, report already absent without submitting a delete. If present, the source-backed service operation is deleteCategoryField, separate from FSM importData; require its complete service/client and privilege contract, exact target/key preview and workflow approval before dispatch. Multiple matches or an unresolved key block removal. Verify absence after a confirmed success; never retry an uncertain delete automatically. For automated deletion, report service-route-unavailable; assisted removal follows SKILL.md and stays pending until the human action and export verification finish. Do not silently omit removal requests from a mixed import plan.


## Prior-case and new-case enforcement

Run the same offline operation planner for existing and new BUs. An approved previous ZIP is never a template for another BU's audit cells or authority to upload another artifact. Preserve every request in the plan; already_absent and unchanged outcomes require no mutation and do not count as unsupported subsets. A create contract gap blocks submission of the whole proposed FSM batch until resolved or the user explicitly revises scope. Do not infer create support from the prior existing-row upload being initiated.
