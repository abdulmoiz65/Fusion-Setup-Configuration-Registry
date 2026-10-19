# Standard Coverage Design Enforcement

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | 1 | Verify prerequisites | Confirm the documented entitlement and functional prerequisites are ready. |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | 2 | Check identity | Use the documented read-only lookup for the exact CoverageName. |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | 3 | Establish readiness | Continue only when no existing exact-name coverage is returned and mandatory inputs are complete. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | 1 | Use Data Loader | Generate and validate the `subscriptionCoverageDefaults` source for the requested lifecycle operation. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | 2 | Choose the default level | Choose Global to apply the selected Standard Coverage to all customers, or Customer to apply it to one selected customer. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | 3 | Complete the level-specific selection | Select Default Level Value when Customer is selected. |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | 4 | Set effective dates | Enter the start date; leave the end date empty for an open-ended coverage. |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Creating or checking standard coverage readiness | Error | find_standard_coverage_by_exact_name | The exact name lookup returns more than one record, fails, or cannot be authorized | Resolve the identity or access issue before continuing | Yes |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Preparing a documented REST create request | Error | find_standard_coverage_by_exact_name | An exact CoverageName already exists | Review the existing coverage; do not treat the request as a create candidate | Yes |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | Preparing a documented REST create request | Error |  | DynamicMatrixClassName or StartDate is absent | Supply the entitlement type and start date documented for the create flow | Yes |
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | CoverageChargeDiscounts is supplied | Error |  | Required charge-discount reference values are incomplete | Supply the complete documented reference values or omit the optional charge-discount entry | Yes |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Creating or updating through Data Loader | Error |  | Default Level is not Global or Customer | Correct the Data Loader source before preflight | Yes |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Creating or updating a customer-specific Default Coverage through Data Loader | Error |  | Default Level Value is not selected | Select the customer in the Data Loader source before preflight | Yes |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Creating or updating through Data Loader | Error |  | Standard Coverage or start date is absent | Correct the Data Loader source before preflight | Yes |

## Design Lookup Requirements

| Task Code | Task Name | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|---|
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | find_standard_coverage_by_exact_name | Before readiness is returned for a named standard coverage | CoverageHeaderId, CoverageHeaderPuid, CoverageName, MatrixName, StartDate, EndDate, StandardCoverageYn | ora_reference_lookups.md |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_STANDARD_COVERAGE | Manage Standard Coverage | STDCOV.DESIGN_GATE | decision | 40 | design_enforcement | ready->STDCOV.READY_FOR_DOCUMENTED_CREATE;blocked->STDCOV.DESIGN_ISSUES | STDCOV.LOOKUP | stop | The exact-name lookup found no existing standard coverage |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.DESIGN_GATE | decision | 30 | design_enforcement | ready->DEFCOV.READY_FOR_DATA_LOADER;blocked->DEFCOV.DESIGN_ISSUES | DEFCOV.DEPENDENCIES | stop | Required Default Coverage values are ready for Data Loader preflight and approval |
