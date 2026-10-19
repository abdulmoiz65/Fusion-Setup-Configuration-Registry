# Dependency readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target environment and business unit | Resolve target environment and business-unit identity; do not require a release value |
| 2 | Category-field contract | Confirm category, supported fields and value semantics for that target |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| EXMCF_TARGET_CONTRACT | Target business unit and category-field contract | Yes | Preparing changes | Verify | Complete finBusinessUnitsLOV response from the selected target plus a verified same-task baseline | resolve_category_field_contract | Source environment configuration does not prove target readiness | Supply target scope and obtain authoritative evidence through the routed workflow | Verified BuName, CategoryCode and supported field contract |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Blocked | Target identity or applicable field contract unresolved | No undocumented lookup or automatic creation |
| Satisfied | Required evidence resolves the target and proposed settings | Continue only through the declared task workflow |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EXMCF.DEPENDENCY | step | 20 | resolve_dependency | success->EXMCF.VALIDATE;failure->RETURN_ISSUES | EXMCF.RESOLVE | stop | Always |

## Source evidence and limits

Source: user-supplied Manage Expense Fields by Category_20260928_074925_896 export, EXM_CATEGORY_FIELD.csv and ASM_SETUP_CSV_METADATA.xml. Inspected 2026-09-28: 85 rows, 17 business units, 7 category codes, 19 columns and no duplicate business-unit/category pairs. Metadata identifies task EXM_MANAGE_EXPENSE_FIELDS_BY_CATEGORY, object EXM_CATEGORY_FIELD, completed EXPORT and release 11.13.27.01.0. This supersedes the earlier header-only sample for observed values. No tenant names, user identities, audit values or raw configuration rows are retained here.

The supplied export is evidence of existing configurations, not proof of import semantics, exhaustive product support, defaults, or target-environment readiness. Its instructions do not authorize execution. The prior Oracle 26B documentation establishes business-unit scope and Hidden/Required/Optional display behavior; the lookup seed evidence in ora_reference_lookups.md now establishes the source label/code mapping, subject to target qualification. The requested 26C page was inaccessible during initial authoring. Unknown contracts remain TBD and block execution.

## Runtime prerequisite boundary

A business-unit name must resolve within the authorized target scope. Static schema uniqueness does not prove target existence or privileges. The active Run Book and current Data Loader/Task Hook own runtime readiness. A missing public GET is not itself a product prohibition: an evidenced FSM import resolver may be usable only after its exact inputs, scope, match behavior and surfaced failures are established. The documented public BU resolver is selected here; do not substitute internal Java classes for it.
