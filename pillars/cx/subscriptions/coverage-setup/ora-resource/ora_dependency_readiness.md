# Standard Coverage Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Entitlement configuration | Configure an entitlement type when the coverage requires entitlement association. A matrix name is optional in the current Standard Coverage REST create contract. |
| 2 | Standard coverage definition | Provide the coverage name, description, start date, and entitlement type. |
| 3 | Optional charge discount | When a charge discount is included, provide its service activity, billing type, adjustment type and amount, pricing basis, and business process. |

## Default Coverage Dependency Order

| Task Code | Task Name | Sequence | Dependency | What Must Happen |
|---|---|---|---|---|
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | 1 | Data Loader template | Resolve the registered `subscriptionCoverageDefaults` template for the requested operation. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | 2 | Default level selection | Select Global for all customers or Customer for one selected customer. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | 3 | Standard Coverage selection | Select the Standard Coverage to apply. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | 4 | Effective dates | Enter the start date. Enter an end date only for a time-bounded coverage. |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.ENTITLEMENT | Subscription entitlement type | Yes | Preparing a documented REST create request | Satisfied when DynamicMatrixClassName is supplied; otherwise Blocked | Supplied request value |  | The current Standard Coverage REST create contract requires an entitlement type but does not mark MatrixName as required | Supply the Subscription Entitlements type; provide MatrixName only when an entitlement matrix must be associated | DynamicMatrixClassName |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.CONFIGURATION | Coverage configuration prerequisites | Yes | Creating a standard coverage through the Subscription Configuration work area | Satisfied when the required business-process, service-activity, time-zone, severity, billing-type, price-list, adjustment-type, adjustment-basis, and entitlement-type setup is available; otherwise Blocked | Implementation evidence |  | Oracle lists these prerequisites before standard coverage templates are created | Complete or verify the prerequisite setup before continuing | Prerequisite readiness evidence |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.CHARGE_DISCOUNT | Charge-discount reference data | Conditional | CoverageChargeDiscounts is supplied | Satisfied when the supplied values are available; otherwise Blocked | Supplied request values and prerequisite setup evidence |  | The documented REST example associates each discount with service activity, billing type, adjustment type, pricing basis, and business process | Supply each matching reference value or omit the optional charge-discount row | CoverageChargeDiscounts values |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.DATA_LOADER_TEMPLATE | Registered Data Loader template | Yes | Creating, updating, or deleting a Default Coverage | Satisfied when live metadata resolves `subscriptionCoverageDefaults`; otherwise Blocked | Core Data Loader metadata lookup |  | The operation must use the Data Loader schema returned by the target environment | Resolve the template and use the operation-specific sample; do not fall back to UI or direct REST | Registered template and operation |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.STANDARD_COVERAGE | Standard Coverage selection | Yes | Creating or updating a Default Coverage | Satisfied when a Standard Coverage is selected in the Data Loader source; otherwise Blocked | Approved Data Loader source |  | Oracle requires selecting a Standard Coverage for both Global and Customer levels | Select the Standard Coverage to apply | Selected Standard Coverage |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|---|
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Satisfied | All mandatory dependency values and prerequisite evidence are present | No |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Blocked | A required entitlement, prerequisite, or charge-discount value is absent | No |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Satisfied | A Standard Coverage is selected and the chosen level has its required values | No |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Blocked | The required Standard Coverage or customer selection is absent | No |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.DEPENDENCIES | decision | 20 | resolve_dependency | satisfied->STDCOV.LOOKUP;blocked->STDCOV.DEPENDENCY_ISSUES | STDCOV.VALIDATE | stop | After required Standard Coverage inputs are valid |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.DEPENDENCIES | decision | 20 | resolve_dependency | satisfied->DEFCOV.DESIGN_GATE;blocked->DEFCOV.DEPENDENCY_ISSUES | DEFCOV.VALIDATE | stop | After Default Coverage setup inputs are valid |
