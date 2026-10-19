# Standard Coverage Input Validation

## Source Basis

- [Oracle Fusion Cloud Subscription Management: Create Standard Coverage](https://docs.oracle.com/en/cloud/saas/subscription-management/fadsm/create-standard-coverage.html)
- [Oracle Sales and Fusion Service REST API: Create and Update Standard Coverages Using REST API](https://docs.oracle.com/en/cloud/saas/sales/faaps/UC_Create_and_Update_Standard_Coverages_Using_REST_API.html)
- [Oracle Sales and Fusion Service REST API: Get a standard coverage](https://docs.oracle.com/en/cloud/saas/sales/faaps/op-subscriptioncoverageheaders-coverageheaderpuid-get.html)
- [Oracle Service Contracts User Guide: Setting Up Standard Coverage and Subscription Templates](https://docs.oracle.com/cd/E18727_01/doc.121/e13458/T378239T378261.htm) is supplemental historical guidance; it does not define the current REST contract.
- Developer-provided read-only collection endpoint: {{baseUrl}}/crmRestApi/resources/latest/subscriptionCoverageHeaders?q=StandardCoverageYn=Y.
- Developer-provided read-only entitlement-rule endpoint: {{baseUrl}}/fscmRestApi/resources/latest/pricingMatrixes/{MatrixId}/child/rules/{RuleId}.
- [Oracle Fusion Cloud Service: How do I create default coverages?](https://docs.oracle.com/en/cloud/saas/fusion-service/faiec/create-default-coverages.html)
- Developer-provided read-only default-coverage endpoint: {{baseUrl}}/crmRestApi/resources/latest/subscriptionCoverageDefaults.

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Standard coverage identity | CoverageName | Stop before readiness evaluation | Provide the template name | Creating or checking a standard coverage | find_standard_coverage_by_exact_name |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Core coverage definition | CoverageDescription, StartDate, DynamicMatrixClassName | Stop before readiness evaluation | Provide the template description, start date, and entitlement type | Preparing a documented REST create request |  |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Charge-discount details | ServiceActivityName, BillingTypeMeaning, AdjustmentTypeMeaning, AdjustmentAmount, PricingBasisName, BusinessProcessMeaning | Stop the affected charge-discount preparation | Provide the complete documented charge-discount values or omit the optional charge-discount entry | CoverageChargeDiscounts is supplied |  |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Entitlement-rule detail identity | CoverageName and RuleId | Stop the related detail request | Provide the exact coverage name and entitlement RuleId | Retrieving one entitlement rule associated with a Standard Coverage | get_entitlement_rule_by_matrix_and_rule_id |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Default coverage definition | Default Level, Standard Coverage, Start Date; optional End Date | Stop Data Loader preflight | Provide the selected level, standard coverage, and start date; supply an end date only for a time-bounded coverage | Creating or updating a Default Coverage through Data Loader |  |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Customer default identity | Default Level Value | Stop Data Loader preflight | Select the customer in Default Level Value | Default Level is Customer |  |

## Field Validation

| Task Code | Task Name | Check | What Happens | Applies When | Resolver |
|---|---|---|---|---|---|
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Coverage name length | Reject a CoverageName longer than 150 characters | CoverageName is supplied |  |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Coverage description length | Reject a CoverageDescription longer than 1000 characters | CoverageDescription is supplied |  |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Coverage date shape | Require StartDate and optional EndDate in the Oracle date format | A create or update request includes dates |  |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Standard Coverage collection request | Do not require CoverageName when listing records filtered by StandardCoverageYn=Y | Listing Standard Coverages in the configured Fusion environment | list_standard_coverages |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Coverage detail request | Require CoverageName; MatrixId is resolved from the matching coverage and RuleId identifies the requested entitlement rule | Retrieving detailed Standard Coverage data and one entitlement rule | find_standard_coverage_detail_by_exact_name |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | Schedule item request identity | Reject an item lookup without SchedulePuid; a collection request may instead omit SchedulePuid and supply optional limit and offset | Retrieving a single availability schedule | find_coverage_schedule_by_puid |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | Exception item request identity | Reject an item lookup without ExceptionPuid; a collection request may instead omit ExceptionPuid and supply optional limit and offset | Retrieving a single availability exception | find_coverage_exception_by_puid |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | Schedule documented-create contract | Mark documented-create readiness incomplete when TimezoneCode is missing | Preparing a future schedule create request |  |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | Exception availability documented-create contract | Mark documented-create readiness incomplete when ObjectCode or ObjectId is missing for a SubscriptionCoverageAvailability entry | Preparing a future exception create request with availability entries |  |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Default Level | Accept only Global or Customer | Creating or updating through Data Loader |  |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Customer default selection | Require Default Level Value when Default Level is Customer | Creating or updating a customer-specific Default Coverage through Data Loader |  |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Date normalization | Normalize an unambiguous valid supplied date to YYYY-MM-DD. Ask only when a non-ISO numeric date has two leading components that could both be a month; do not guess its day/month order | Creating or updating through Data Loader |  |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | End Date | Allow an empty End Date | Creating or updating through Data Loader |  |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Default Coverage collection request | Do not require a selection value when listing Default Coverages | Listing Default Coverages in the configured Fusion environment | list_default_coverages |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.VALIDATE | decision | 10 | validate_input | list->STDCOV.LIST;details->STDCOV.DETAIL_FIND;valid->STDCOV.DEPENDENCIES;invalid->STDCOV.INPUT_ISSUES | none | stop | Any Standard Coverage planning, validation, documented-create readiness, collection-listing, or related-detail request |
| CUSTOM_MANAGE_AVAILABILITY | Manage Availability | AVAIL.VALIDATE | decision | 10 | validate_input | schedule_list->AVAIL.SCHEDULE_LIST;schedule_item->AVAIL.SCHEDULE_LOOKUP;exception_list->AVAIL.EXCEPTION_LIST;exception_item->AVAIL.EXCEPTION_LOOKUP;issues->AVAIL.ISSUES | none | stop | Any Manage Availability read-only schedule or exception request |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.VALIDATE | decision | 10 | validate_input | create->DEFCOV.DEPENDENCIES;update->DEFCOV.DEPENDENCIES;delete->DEFCOV.DEPENDENCIES;list->DEFCOV.LIST;resolve_default->DEFCOV.RESOLVE_DEFAULTS;invalid->DEFCOV.INPUT_ISSUES | none | stop | Any Default Coverage Data Loader lifecycle, collection-listing, or default-resolution request |
