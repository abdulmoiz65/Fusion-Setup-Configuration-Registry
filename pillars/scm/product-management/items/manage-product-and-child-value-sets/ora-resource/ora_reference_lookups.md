# Manage Product and Child Value Sets Reference Lookups

Oracle documents the Product Management flexfields metadata endpoint as a
read-only source for flexfield metadata and value-set configuration. This
lookup does not authorize a setup change.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_setup_task_identity | Before an FSM template export, setup-data validation, or import for this task | Expected TaskCode EGP_MANAGE_PRODUCT_VALUE_SETS and TaskName Manage Product and Child Value Sets | GET /fscmRestApi/resources/11.13.18.05/setupTasks?onlyData=true&totalResults=true&q=TaskCode='EGP_MANAGE_PRODUCT_VALUE_SETS'&limit=100; fallback GET with TaskName LIKE '%Manage Product and Child Value Sets%' | TaskCode, TaskName, AvailableFlag, CSVExportImportSupportedFlag, ExportImportSupportedFlag | Prefer one exact TaskCode match. If the code lookup has no match, require exactly one TaskName LIKE result whose returned TaskCode is EGP_MANAGE_PRODUCT_VALUE_SETS. Do not use TaskName equality. Do not filter the setupTasks response by Offering or Functional Area because this resource does not return those fields for this task; resolve that context from the selected task skill and catalog. | Resolved task code, task name, available flag, CSV export/import flag, export/import flag | Zero, many, unavailable, or unsupported results block. Do not infer a task code or substitute another task. |
| resolve_parent_independent_value_set | ValidationType is Subset or the request defines child SKU variants | ParentIndependentValueSetCode, ParentIndependentValueSetModule | GET /fscmRestApi/resources/11.13.18.05/productManagementFlexfieldsMetadata?expand=all | Product Management flexfield metadata and value-set configuration | Require exactly one configured parent whose value set code and module match the supplied identifiers and whose validation type is Independent | Parent independent value-set configuration receipt | Zero, many, module mismatch, or non-independent matches block; do not select a candidate |
| verify_imported_value_set | After Data Loader reports a completed import and functional verification is requested | Imported ValueSetCode, expected ValidationType, expected IndependentValueSetCode when Subset, and requested child values | GET /fscmRestApi/resources/11.13.18.05/valueSets?q=ValueSetCode='<exact code>'&expand=values&onlyData=true&limit=10 | ValueSetCode, ValidationType, ValueDataType, MaximumLength, IndependentValueSetCode, and expanded values Value, IndependentValue, Description, EnabledFlag, SortOrder | Require exactly one root value set with the exact code. For a Subset, require the expected parent code and ValidationType SUBSET. Compare every requested child value and independent-value mapping against the expanded values. Use this expanded root response when the child values endpoint is unavailable. | Sanitized post-import definition and value receipt | Zero or many root matches, a definition mismatch, or a missing/mismatched requested value fails functional verification. Do not retry or mutate data automatically. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Setup-task discovery | Resolve by exact task code first. When a name search is needed, use TaskName LIKE and retain only the exact expected code. |
| Missing contextual fields | Do not apply Offering or Functional Area response filters to setupTasks results; use the selected task skill and catalog context instead. |
| Phase 1 parent-only load | After task identity resolves, return resolved_parent_only when the immutable artifact contains only an INDEP parent and its values. Do not call the parent metadata lookup before the parent is created. |
| Phase 2 subset load | After task identity resolves, return resolved_subset when the immutable artifact contains a SUBSET child. Require the parent metadata lookup before the child load. |
| Parent validation | Use the documented read-only metadata endpoint and retain only a sanitized match receipt. |
| Unresolved parent | Stop. Do not fuzzy-match, select the first candidate, or create a parent value set. |
| Post-import functional validation | Only after the Data Loader status is Succeeded, use verify_imported_value_set. Confirm the exact child definition and each requested value mapping; report the resulting receipt without identifiers, credentials, or raw response data. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VSET.RESOLVE_TASK | step | 15 | reference_lookup | resolved_parent_only->VSET.ENFORCE_PARENT_DESIGN;resolved_subset->VSET.RESOLVE_PARENT;blocked->VSET.HANDLE_ERROR;failure->VSET.HANDLE_ERROR | VSET.VALIDATE_INPUT | stop | Before an FSM template export, setup-data validation, or import for this task |
| VSET.RESOLVE_PARENT | step | 20 | reference_lookup | resolved->VSET.CHECK_DEPENDENCIES;blocked->VSET.HANDLE_ERROR;failure->VSET.HANDLE_ERROR | VSET.RESOLVE_TASK | stop | A parent independent value set must be confirmed |
