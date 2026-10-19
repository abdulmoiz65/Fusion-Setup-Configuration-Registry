# FSM Category Hierarchy Input Validation

Task: POR_MANAGE_CATALOG_CATEGORY_HIERARCHY. Expected TYPE: SHOPPING. FSM CSV only; execution remains with the generated skill’s routed export, validation, and core.data-loader services. These resources perform local preparation and evidence assessment; they declare no product REST operation.

Source: user-approved rules derived from reviewed native FSM exports and import receipts (September 2026). Preventive safeguards below are authoring policy, not claims of tested Oracle rejection behavior.

Successful FSM tests cover browsing-category creation and purchasing-category relationships, including a new item placement and an unchanged existing relationship. A numeric-looking category name with a descriptive code was accepted. Name-only and other name/code failures do not establish matching precedence or a mandatory CategoryCode rule.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Native package contract | Selected-task exported ZIP or template, exact task metadata, CSV members and headers | Stop package preparation | Supply the selected task’s native export through the routed workflow | Preparing an import | |
| Browsing category identity | CategoryName and TYPE | Reject the affected row | Supply a nonblank name and SHOPPING | POR_BROWSE_CATEGORY.csv data rows | |
| Relationship identity | ParentCategoryName, ChildCategoryName, TYPE, PurchasingCatFlag | Reject the affected row | Supply nonblank parent and child names, SHOPPING, and the intended child kind | POR_BROWSE_TREE.csv data rows | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Exact identifier strings | Preserve CategoryName, CategoryCode, parent and child names as strings, including leading zeros, spaces, punctuation and case; never swap, trim, case-fold or derive identifiers from their appearance | Reading, comparing or writing supplied values | |
| Native CSV shape | Require selected-task filenames, exact header spelling and order, valid CSV quoting and equal header/data row widths; reject duplicate archive member names and unsafe member paths | Preparing an import | |
| Task and TYPE isolation | Require metadata ObjectShortName POR_MANAGE_CATALOG_CATEGORY_HIERARCHY; require SHOPPING in every data-row TYPE and POR_BROWSE_CATEGORY.TYPE; reject mixed types or another task’s metadata | All package members | |
| Relationship child kind | Require Y for a user-declared purchasing/item child and N for a browsing child; do not infer child kind from a numeric-looking name | POR_BROWSE_TREE.csv data rows | |
| CategoryCode supplied or blank | Preserve the supplied value exactly; blank alone is not evidence of invalid input or a reason to fabricate a code | POR_BROWSE_TREE.csv data rows | |
| Proposed structural safeguards | Reject self-parenting, cycles in the supplied browsing relationships and conflicting duplicates for the same TYPE, parent, child and purchasing flag; compare all remaining fields to detect a conflict | Locally supplied relationships; this does not prove the full target graph is acyclic | |
| Translation structure | Preserve the native translation headers and supplied language/source-language values; do not invent translations or language codes | POR_BROWSE_CATEGORY_TRANSLATION.csv | |

## Native Headers

Use these reviewed headers as a baseline. If a newly selected export differs, stop for contract review; do not force an older header onto it.

- POR_BROWSE_TREE.csv: PurchasingCatFlag, ChildCategoryName, TYPE, TopCategoryFlag, ParentCategoryName, CategoryCode.
- POR_BROWSE_CATEGORY.csv: CategoryName, TYPE, CategoryDescription, ImageUrl.
- POR_BROWSE_CATEGORY_TRANSLATION.csv: POR_BROWSE_CATEGORY.CategoryName, POR_BROWSE_CATEGORY.TYPE, CategoryName, CategoryDescription, Language, SourceLang.
- ASM_SETUP_CSV_METADATA.xml: preserve the selected task’s native metadata and object scopes.

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Local input checks pass | Package structure is locally valid; references and Fusion acceptance are not established | Assess supplied target evidence and dependency readiness | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCH.INPUT | step | 10 | validate_input | valid->CCH.EVIDENCE;invalid->RETURN_ISSUES | none | stop | Preparing the task’s FSM CSV import |
