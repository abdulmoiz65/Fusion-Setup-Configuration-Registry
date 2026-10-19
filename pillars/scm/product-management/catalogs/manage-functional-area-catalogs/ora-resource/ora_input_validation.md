# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Execution contract | Authorized execution route: FSM configuration package import through core.data-loader; action sequence: validate the same-task FSM package and metadata, validate required setup-data fields, default omitted REST-described catalog values, map each resolved catalog identity to the exact FSM CSV columns, validate user-provided functional-area values when a default functional-area assignment is requested, validate mapped CSV fields, bind the immutable package to the target environment, preview, obtain explicit approval, import, immediately persist the returned Data Loader Content ID and Request ID, retain the FSM migration ProcessId when Fusion returns one, monitor only the persisted tracking identifier, retrieve the corresponding ProcessLog when available, and validate the resulting catalog and any requested assignment; required setup-data fields: catalog identity as Catalog Code or Catalog Name with the supplied value copied into the missing counterpart when a catalog row is included; when absent, default ControlLevel to `1` and CatalogContentCode to `LEAF_ITEMS`, and default MultItemCatAssignFlag to `N` only when no default functional-area assignment is requested; a default functional-area assignment is optional and, when requested, requires Functional Area ID or Functional Area Name resolved through EGP_CATALOG_FUNCTIONAL_AREAS, a verified Catalog Code, and explicit `HierarchyEnabled` and `MultItemCatAssignFlag`. Prompt once for a public Oracle Functional Area Catalog Rules document reference; if the user declines or does not provide one, record `not_provided` and continue. When a default Category Code or Category Name is supplied, infer `DefaultCategoryRequired=Yes`; otherwise require an explicit `DefaultCategoryRequired` value. When category setup is requested or `DefaultCategoryRequired` is Yes, require Category Code and Category Name plus a verified catalog-category relationship Catalog Code and Category Code | Stop before preview or import only for missing required values or environment/package evidence | Select exactly one configured Fusion target environment. When the package was exported from that same environment, verify the source and target environment identity matches. When the source and target differ, verify release compatibility. | Manage Functional Area Catalogs is requested | |
| FSM import artifact | Validated same-task FSM configuration package containing the EGP_MANAGE_DEFAULT_CATALOGS FSM CSV export and exactly one ASM_SETUP_CSV_METADATA.xml file; export tracking receipt with TaskCode, ProcessId, submission time, source environment and initial status; intended target environment: exactly one configured Fusion target environment, with either matching source/target environment identity or, for a cross-environment migration, verified release compatibility | Stop before import | Export the exact task through shared.setup-export.task-level-export, persist the returned ProcessId immediately in the project task run record, then verify the package baseline | An FSM import is requested | verify_functional_area_catalogs_fsm_package |

## REST and UI Field Canonicalization

Accept the aliases below at intake, normalize them before FSM validation, and retain the supplied field name and value in the validation receipt. This is an input-normalization rule only; it does not authorize direct REST catalog creation or change the FSM-only execution route.

| Canonical FSM concept | Accepted REST or UI aliases | Accepted input values | Canonical FSM result | Safety rule |
|---|---|---|---|---|
| Control level | `ControlLevel`; `MasterControlledFlag`; `Controlled At` | FSM code: `1`/`2`; Boolean: `true`/`false` (also `Y`/`N`, `yes`/`no`); UI text: `Master Level` or `Organization Level` | `1`, `true`, or `Master Level` → `ControlLevel=1`; `2`, `false`, or `Organization Level` → `ControlLevel=2` | Validate the resulting code against the exported `EGP_CATALOG.csv` header and permitted values before package preview; stop on an unrecognized or conflicting alias value. |
| Multiple item-category assignments | `AllowItemToMultipleCategoriesFlag`; `Allow multiple item category assignments` | Boolean: `true`/`false` (also `Y`/`N`, `yes`/`no`, or `1`/`0`) | `true` → `MultItemCatAssignFlag=Y`; `false` → `MultItemCatAssignFlag=N` | Do not apply a default merely because the REST Describe metadata has one; preserve an explicit FSM value and stop on a conflict. |
| Catalog content | `CatalogContentCode`; `AssignItemsToLeafOnlyFlag`; `Assign items to leaf level categories only` | Canonical code, or Boolean: `true`/`false` (also `Y`/`N`, `yes`/`no`, or `1`/`0`) | `true` → `CatalogContentCode=LEAF_ITEMS`; `false` → `CatalogContentCode=ALL_ITEMS`; an explicit canonical code is retained | Canonicalize every non-omitted catalog row, then resolve the lookup collection once through `resolve_catalog_content_code` and validate each row against its cached result; stop on an unrecognized or conflicting alias value. |
| Category content | `CategoryContentCode`; `ItemsOnlyFlag`; `Restrict category to item assignment only` | Canonical code `ITEM_ONLY`/`MIXED`, or Boolean: `true`/`false` (also `Y`/`N` or `yes`/`no`) | `true`, `Y`, or `Yes` → `CategoryContentCode=ITEM_ONLY`; `false`, `N`, or `No` → `CategoryContentCode=MIXED`; an explicit canonical code is retained | Validate the resulting code against the exported `EGP_CATEGORY.csv` header and the supported values `ITEM_ONLY` or `MIXED`; stop on an unrecognized or conflicting alias value. |

When an alias and its canonical FSM field are both supplied, normalize both and require the same result. Treat a mismatch as `input_validation`; do not choose one field by precedence. Do not accept `CatalogId`, `CreationDateTime`, `LastUpdateDateTime`, `HierarchyEnabledFlag`, or `DefaultCategoryName` as catalog-create input: they are server-managed or non-updatable in the inspected REST Describe metadata and are not FSM canonical inputs.

## Dependency-Aware Validation

When `MultItemCatAssignFlag` and its REST/UI aliases are blank, default it to `N` only when no default functional-area assignment is requested. For a requested functional-area assignment, require the user-provided documented value. Preserve an explicit normalized `Y` or `N` value and stop on a conflicting or unsupported alias value.

For every catalog row, preserve an explicit normalized `HierarchyEnabled` value. When it is omitted, default `EGP_CATALOG.csv.HierarchyEnabled=Y` from the active `itemCatalogs/describe` metadata's `HierarchyEnabledFlag.defaultValue=true`. For requested functional-area assignments, require `MultItemCatAssignFlag`; prompt once for the applicable public Oracle Functional Area Catalog Rules documentation reference and record either the supplied reference or `not_provided` without blocking. When a default Category Code or Category Name is supplied, infer `DefaultCategoryRequired=Yes`; require an explicit `DefaultCategoryRequired` value only when neither default-category identity is supplied.

When `EGP_CATALOG.csv.ControlLevel` and its REST/UI aliases are blank, default it to `1` (Master Level). Preserve an explicit normalized `1` or `2` value and stop on a conflicting or unsupported alias value.

When `EGP_CATALOG.csv.CatalogContentCode` and its REST/UI aliases are blank, default that catalog row to `LEAF_ITEMS`. After all non-omitted catalog rows are canonicalized and defaulted, call `resolve_catalog_content_code` once and validate every row's resulting code against the complete cached lookup receipt before package preparation.

When `EGP_CATEGORY.csv.StartDateActive` is blank or not supplied, ask the user: `Category StartDateActive was not provided. May I use today's date, or would you like to provide another date?` Do not populate the field until the user confirms today's date or supplies a different valid date.

When `EGP_CATEGORY.csv.SummaryFlag` or `EGP_CATEGORY.csv.SupplierEnabledFlag` is blank or not supplied, populate each with `Y`; preserve any explicit user-provided value.

## Subsequent-run baseline reconciliation

Before preparing any subsequent runbook package, inspect the persisted baseline ZIP for the requested catalog and category identities. If the baseline contains catalog or category rows that were successfully imported by the preceding run, tell the user which rows were found and ask:

First ask:

> This is a subsequent runbook execution. Should I perform a fresh FSM baseline export before preparing the package?

If the user chooses `yes`, run `shared.setup-export.task-level-export`, wait for the export result, persist the refreshed baseline ZIP and export Process ID, and inspect the refreshed rows. If the export is incomplete or fails, stop before package preparation. If the user chooses `no`, use the persisted baseline and disclose its path and last-refresh status.

When matching rows are found, ask separately:

> The baseline contains rows previously imported by the last runbook execution. Should I merge those baseline rows into the next package, or ignore the baseline rows and use only the newly supplied rows?

Accept only an explicit `merge` or `ignore` choice. Before executing the merge algorithm, obtain a separate explicit confirmation:

> I found matching baseline rows. Do you confirm merging them into the next package?

On confirmed `merge`, retain and reconcile the matching baseline catalog, category, and catalog-category relationship rows with the new rows, resolving exact duplicate identities without creating duplicates. On `ignore`, exclude the matching baseline data rows while preserving the required CSV headers and metadata. Stop before package preparation if the user has not selected or confirmed the choice. Never silently refresh, merge, or discard baseline data.

### Required merge/reconciliation algorithm

When `merge` is selected, materialize the result in the next candidate archive; identity comparison alone is insufficient:

1. Match catalog rows by `CatalogCode` and `CategorySetName`, category rows by `CategoryCode`, and relationship rows by `CatalogCode + CategoryCode`.
2. For each matching row, copy every nonblank baseline field into the current row only when the current field is blank.
3. Preserve every nonblank value explicitly supplied in the current run, including user-entered flags and dates.
4. If both rows contain different nonblank values for the same field, report a reconciliation conflict and stop for user resolution; never overwrite silently.
5. Add unmatched current rows, retain only the matching baseline rows requested by the merge choice, remove exact duplicates, preserve CSV headers and `ASM_SETUP_CSV_METADATA.xml`, rebuild the ZIP, and recompute its SHA-256.
6. Show the field-level changes and conflicts in the preview. Approval applies to the rebuilt archive, not the pre-merge archive.

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The execution contract is not documented | BLOCKED | Do not prepare, preview, or import setup data; obtain task-specific Oracle guidance | |
| A catalog row, category rows, or both are absent | APPROVAL_REQUIRED | Present the omitted rows and obtain explicit approval before package preparation | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Authorized execution route | Route the approved task data through an FSM configuration package import | Manage Functional Area Catalogs is requested | |
| FSM action sequence | Validate package and metadata, validate required fields, bind the immutable package through core.data-loader, preview, obtain approval, import, persist the returned Content ID and Request ID immediately, retain a returned FSM migration ProcessId, monitor and retrieve ProcessLog only through persisted identifiers, and validate the resulting catalog assignment | Manage Functional Area Catalogs is requested | |
| Catalog | Accept Catalog Code or Catalog Name for a catalog row. Each value must be no more than 30 characters. When exactly one is supplied, copy its value into the missing counterpart only when the copied value also satisfies the 30-character limit. When both are supplied, preserve both approved values. When both are absent, request explicit approval to omit only the catalog row. | A catalog record is supplied or the catalog row is omitted | |
| Catalog and category code length | Require Catalog Code and Category Code to contain at most 30 characters. Stop before package preparation when either code exceeds the limit; never truncate or silently normalize it. | A catalog or category identity is supplied | |
| FSM catalog identity mapping | For every non-omitted EGP_CATALOG.csv row, require CatalogCode to be nonblank and equal to the resolved Catalog Code, and CategorySetName to be nonblank and equal to the resolved Catalog Name. Stop when either CSV field is blank or differs from its resolved value. | Before package preview or import | |
| Control level | When ControlLevel and its REST/UI aliases are blank, default `ControlLevel=1` (Master Level). Otherwise normalize Master Level or true to `1`, and Organization Level or false to `2`; preserve an explicit `1` or `2`. Stop on any other value or a conflicting alias, and validate the resulting code against the exported FSM contract. | A catalog row is prepared for an FSM package | |
| Multiple item-category assignments | When MultItemCatAssignFlag and its REST/UI aliases are blank, default `MultItemCatAssignFlag=N` only when no default functional-area assignment is requested. Otherwise map AllowItemToMultipleCategoriesFlag or UI Allow multiple item category assignments as true → `Y` and false → `N`; preserve an explicit `Y` or `N`, and stop on a conflict or unsupported value. | A catalog row is prepared for an FSM package | |
| Catalog content code | For each catalog row, when CatalogContentCode and its REST/UI aliases are blank, default `CatalogContentCode=LEAF_ITEMS`. Otherwise map AssignItemsToLeafOnlyFlag or UI Assign items to leaf level categories only as `true` → `LEAF_ITEMS` and `false` → `ALL_ITEMS`. Retrieve the complete `EGP_CATALOG_CONTENT_CODE` collection once after all rows are canonicalized, then resolve every row's resulting code to exactly one enabled, effective cached lookup row. | A catalog row is prepared for an FSM package | resolve_catalog_content_code |
| Category content code | When supplied, require canonical `CategoryContentCode` to be exactly `ITEM_ONLY` or `MIXED`. Map REST `ItemsOnlyFlag` or UI `Restrict category to item assignment only` as `true`, `Y`, or `Yes` → `ITEM_ONLY`, and `false`, `N`, or `No` → `MIXED`; retain an explicit canonical code only when it agrees with every supplied alias. Validate the final code against the exported EGP_CATEGORY.csv header before preview. | A category row is prepared for an FSM package | |
| Functional-area catalog parameters | Require user-provided `MultItemCatAssignFlag`. Prompt once for a public Oracle Functional Area Catalog Rules document reference; accept a supplied reference or record `not_provided` and continue. Infer `DefaultCategoryRequired=Yes` when the input supplies a default Category Code or Category Name; otherwise require user-provided `DefaultCategoryRequired`. Preserve explicit `HierarchyEnabled`; otherwise default it to `Y` from current REST Describe metadata. | A catalog is created or assigned to a functional area | |
| No functional-area assignment | Omit the default functional-area assignment CSV row, skip functional-area lookup and rule enforcement, and continue with catalog-category reference validation. | The user explicitly states that no functional-area assignment is requested | |
| Dependent catalog reference | For every category or default functional-area assignment row, require its Catalog Code or Catalog Name to match exactly one candidate EGP_CATALOG.csv row, or, when that catalog row is not in the candidate CSV, exactly one matching catalog row in the validated baseline ZIP. | A category or default functional-area assignment row references a catalog | verify_referenced_baseline_catalog |
| Category | Accept Category Code or Category Name. Category Code must be no more than 30 characters. When exactly one is supplied, disclose that the missing counterpart will default to the supplied value and allow the user to provide a different approved counterpart. When both are supplied, preserve both approved values. | A category record is supplied or either category field is supplied | |
| Category omission | When both Category Code and Category Name are absent, present that category and catalog-category data rows will be omitted while the same-task exported category CSV members and exact headers remain. Require explicit approval only when the user-provided `DefaultCategoryRequired` value is No. When it is Yes, stop and ask the user to provide Category Code or Category Name; do not omit the category rows. | No category setup is requested | |
| Functional-area required default category | When `DefaultCategoryRequired` is user-provided or inferred as Yes, require the supplied Category Code or Category Name. After the category identity is resolved, require its code in EGP_CATALOG.csv.CategoryCode and retain the matching category and catalog-category rows. Do not choose or default a category. | A catalog is created or assigned to a functional area that requires a default category | |
| Valid category relationship | Require Catalog Code and Category Code | A category is associated with a catalog | |
| Category-to-valid-category completeness | Require exactly one matching `ORA_EGP_VALID_CATALOG_CATEGORY.csv` row for every included `EGP_CATEGORY.csv` row, matched only by the unique `CategoryCode`. Do not use catalog context for matching. Reject orphan, duplicate, blank, or mismatched relationship rows; stop before preview or import and report the missing or invalid relationship. | Category setup is included | |
| Parent-category relationship mapping | When the input supplies a parent category, populate the matching valid-category row's `ParentCategoryCode` with the exact supplied parent code; require that the parent category is also included or is verifiably present in the target environment. Stop before preview or import on a missing, blank, self-referencing, or unresolved parent. | A category input includes `parent category` | |
| Default functional-area assignment | Accept Functional Area ID or Functional Area Name. When only the name is supplied, resolve Functional Area ID through EGP_CATALOG_FUNCTIONAL_AREAS; when both are supplied, require that they identify the same lookup entry. Require the resolved Functional Area ID and Catalog Code in the package row. | A catalog is assigned as the default for a functional area | resolve_catalog_functional_area_id |
| FSM artifact contents | Require the validated same-task package, EGP_MANAGE_DEFAULT_CATALOGS FSM CSV export, exactly one ASM_SETUP_CSV_METADATA.xml file, and a successful export-process receipt | An FSM import is requested | verify_functional_area_catalogs_fsm_package |
| FSM export tracking | Require a sanitized project task run record with the returned ProcessId before polling starts; use that exact ProcessId for every status, ZIP, or ProcessLog retrieval | An FSM export is submitted | verify_functional_area_catalogs_fsm_package |
| FSM import tracking | Require a sanitized project task run record with the exact archive fingerprint, submission time, returned Content ID, returned Request ID, and any returned FSM migration ProcessId immediately after an accepted import response. Query status and retrieve ProcessLog only through those persisted identifiers. | An FSM import is submitted | |
| FSM target environment | Require exactly one configured Fusion target environment. Accept a package exported from that same verified environment; otherwise verify the package source and target are release compatible. | An FSM import is requested | verify_functional_area_catalogs_fsm_package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CATALOGS.VALIDATE-INPUT | step | 10 | validate_input | complete->CATALOGS.CANONICALIZE-INPUT;omission_approval_required->CATALOGS.ROW-OMISSION-APPROVAL;incomplete->RETURN_ISSUES | none | stop | Manage Functional Area Catalogs is requested |
| CATALOGS.CANONICALIZE-INPUT | step | 13 | validate_input | canonicalized->CATALOGS.DEFAULT-CATALOG-IDENTITY;conflict->RETURN_ISSUES;unresolved->RETURN_ISSUES | CATALOGS.VALIDATE-INPUT | stop | A supplied REST or UI alias maps to an FSM catalog field |
| CATALOGS.VALIDATE-FSM-CATALOG-CSV | step | 20 | validate_input | valid->CATALOGS.VERIFY-FSM-PACKAGE;invalid->RETURN_ISSUES | CATALOGS.VERIFY-REFERENCED-BASELINE-CATALOG | stop | A non-omitted EGP_CATALOG.csv row is prepared for an FSM package |
