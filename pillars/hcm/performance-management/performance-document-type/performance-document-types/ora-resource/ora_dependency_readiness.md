# Performance Document Types Dependency Readiness

Source: Oracle Fusion Cloud Talent Management, Overview of Performance Document Types.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Performance document type | Create a document type before associating it with a performance template or goal plan. |
| 2 | Performance template | Select a performance document type on the General tab of every performance template. |
| 3 | Interim evaluation document period | Select at least one document type for a template configured to use interim evaluations. |
| 4 | Goal plan | Associate document types with a goal plan to make that goal plan available in performance documents. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PERFORMANCE_DOCUMENT_TYPES.TEMPLATE_DATE_COVERAGE | Performance template date coverage | Yes | The document type will be used in a performance template | Verify | Target performance template | | The document type From Date must be the same as or before the template From Date, and its To Date must be the same as or later than the template To Date. | Confirm each target template date range and align the document type dates. | Document Type From Date, Document Type To Date |
| PERFORMANCE_DOCUMENT_TYPES.TEMPLATE_ASSOCIATION | Performance template association | Yes | Creating or configuring a performance template | Verify | Target performance template | | Every performance template must include a performance document type on its General tab. | Select the applicable document type on the template General tab. | Performance Document Type |
| PERFORMANCE_DOCUMENT_TYPES.INTERIM_DOCUMENT_PERIOD | Interim evaluation document period association | Conditional | The performance template uses interim evaluations | Verify | Target performance template document period | | At least one document type must be associated with the document period to determine which interim ratings and comments appear later. | Select one or more document types and review periods on the template Document Periods tab. | Performance Document Types, Review Periods |
| PERFORMANCE_DOCUMENT_TYPES.GOAL_PLAN_ASSOCIATION | Goal plan association | Conditional | A goal plan must be available in performance documents | Verify | Target goal plan | | A goal plan requires associated document types; the document type and review period determine which goal plans are added to the performance document. | Associate the document type with the goal plan and select the applicable review period. | Performance Document Type, Review Period |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Verify | Template dates, template association, interim document periods, or goal-plan association must be confirmed. | No; the supplied documentation does not define a lookup or creation contract. |
| Blocked | A required documented relationship is absent or a date range is invalid. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_DOCUMENT_TYPES.DEPENDENCIES | decision | 30 | resolve_dependency | ready->PERFORMANCE_DOCUMENT_TYPES.DEFAULTS;missing->PERFORMANCE_DOCUMENT_TYPES.STOP_DEPENDENCY | PERFORMANCE_DOCUMENT_TYPES.LOOKUP_CURRENT | stop | Document type inputs are valid and a template, interim evaluation, or goal-plan relationship applies. |
