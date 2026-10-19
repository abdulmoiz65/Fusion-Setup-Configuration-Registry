# Defaulting rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Applicable field-display cell under a present workbook header | Optional, encoded ENABLED | Blank or whitespace-only cell on an Enabled=Y row | No; explicit choices win | resolve_category_field_contract |
| Workbook Enabled flag | N | Blank or whitespace-only flag on an otherwise populated request row | No; explicit Y/N wins | |

These are user-approved workbook defaults, not inferred FSM server defaults. Preserve explicit Required, Optional and Hidden. Apply defaults after identifying the operation: N requests removal, so its blank display cells do not produce ENABLED updates. Entirely empty rows create no request. Absent headers, nonapplicable columns and exported audit cells never receive the Optional default. Record each defaulted cell and encoded value in the preview.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EXMCF.DEFAULT | step | 40 | apply_default | success->EXMCF.DESIGN;failure->RETURN_ISSUES | EXMCF.VALIDATE | stop | Always |

## Source evidence and limits

Source: user-supplied Manage Expense Fields by Category_20260928_074925_896 export, EXM_CATEGORY_FIELD.csv and ASM_SETUP_CSV_METADATA.xml. Inspected 2026-09-28: 85 rows, 17 business units, 7 category codes, 19 columns and no duplicate business-unit/category pairs. Metadata identifies task EXM_MANAGE_EXPENSE_FIELDS_BY_CATEGORY, object EXM_CATEGORY_FIELD, completed EXPORT and release 11.13.27.01.0. This supersedes the earlier header-only sample for observed values. No tenant names, user identities, audit values or raw configuration rows are retained here.

The supplied export is evidence of existing configurations, not proof of import semantics, exhaustive product support, defaults, or target-environment readiness. Its instructions do not authorize execution. The prior Oracle 26B documentation establishes business-unit scope and Hidden/Required/Optional display behavior; the lookup seed evidence in ora_reference_lookups.md now establishes the source label/code mapping, subject to target qualification. The requested 26C page was inaccessible during initial authoring. Unknown contracts remain TBD and block execution.

## Workbook omission discipline

Do not infer a business unit for an unselected or incomplete block. Do not carry a prior category's headers or values forward. Enabled=N is explicit configuration-removal intent and must not be defaulted to exclusion. Missing target scope or operation details still require resolution. Existing target values may be preserved only through the declared, verified baseline workflow; do not populate them from another worksheet.

## Operation-specific default evidence

Review UI defaults separately from FSM-import defaults for every writable field. A value supplied automatically by the UI is not proof that import omits it safely. Keep create default, update omission and blank-clearing behavior separate. Do not set an inferred default merely because its value predominates in an export.
