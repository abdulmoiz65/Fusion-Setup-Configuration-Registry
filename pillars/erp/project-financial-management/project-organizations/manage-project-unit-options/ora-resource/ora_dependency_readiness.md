# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Project Organizations setup scope | Task codes and target environment must be explicit |
| 2 | Classified project unit | The organization hierarchy/classification setup must expose one project unit |
| 3 | Related business-unit additions | Preserve the exact requested names for Fusion FSM import validation; removals need usage/deletability evidence |
| 4 | Reference data set | Use resolve_reference_set to resolve the default set against the completed current-target REST collection |
| 5 | Numbering feature and determinant | Current feature ownership and determinant state must be known before numbering defaults or changes |
| 6 | Reporting-options row | The project unit must have exactly one complete `PJF_REPORTING_SETUP` row; a missing row requires a customer-approved same-task correction |
| 7 | Fresh export and package template | Same-task option state and exact import contracts must be current and target-validated |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PUOPT.SCOPE | Project Organizations scope | Yes | Every request | Verify | Catalog metadata and project context | verify_project_unit_options_scope | Prevents cross-task or cross-environment writes | Supply target and retain catalog codes | OfferingCode, FunctionalAreaCode, TaskCode, TargetEnvironment |
| PUOPT.PROJECT_UNIT | Existing classified project unit and current options | Yes | Every write or import | Lookup | setup_data_artifacts.current_export | find_project_unit_options | Options cannot exist without exactly one project unit | Export current task data | ProjectUnitId, Identity, CurrentOptions |
| PUOPT.SET | Target default reference set | Conditional | Default set name or explicitly labeled set code is supplied, or an option row is created | Lookup | Completed current-target set REST collection from resolve_reference_set | resolve_reference_set | Default set controls reference-data sharing | Resolve ordinary input by name and reuse the returned canonical code | SetCode, SetName, ResolutionBasis |
| PUOPT.BUSINESS_UNITS | Related business units | Conditional | Relationships change | Input validation | Requested names and, for removals, relationship-usage evidence | resolve_project_business_units | Fusion owns validation of relationship eligibility during the FSM import | Include exact additions in the preview; retain usage evidence for removal | Name, FusionValidationDeferred, IsDeletable for removals |
| PUOPT.NUMBERING | Numbering feature and determinant state | Conditional | Numbering changes or missing determinant | Verify | setup_data_artifacts.numbering_feature_status and current export | verify_project_unit_options_package | Feature ownership changes which setup owns numbering and when defaults apply | Supply current feature and determinant evidence | FeatureEnabled, DeterminantExists, Method, Type, NextNumber, Prefix |
| PUOPT.REPORTING | Complete project-unit reporting setup | Yes | New project unit, missing reporting row, or downstream Project Plan Type/Project Template use | Lookup | Fresh same-task export member `PJF_REPORTING_SETUP.csv` | find_project_unit_options | A project unit with implementation and BU rows but no reporting row can fail downstream plan-type initialization | Resolve explicit choices and default omissions per ora_defaulting_rules.md; disclose the complete row in the existing approval preview; import the missing row and verify it by a fresh export | ReportingRowExists, commitment statuses, PlanamtAllocMethod |
| PUOPT.PACKAGE | FSM package contract | Yes | Import preview | Verify | setup_data_artifacts.package_template and generated package | verify_project_unit_options_package | Data Loader requires exact same-task members and headers | Validate the task template and preserve checksum | PackageFiles, HeaderMaps, RowCounts, PackageChecksum |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Project unit, complete reporting row, conditional set/BUs/numbering, current export, and package are ready | Yes |
| Missing runtime artifact | A required target-pod artifact is absent | No; collect it |
| Identity or usage conflict | Project unit/set/BU is ambiguous, reporting row is absent/incomplete, numbering conflicts, or relationship cannot be removed | No; correct identity/reporting setup or preserve current state |
| Unsupported operation | Project-unit delete, direct REST option write, or set-assignment mutation is requested | No; return refusal and correct route |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PUOPT.RESOLVE_DEPENDENCIES | step | 7 | resolve_dependency | ready->PUOPT.ENFORCE_DESIGN;missing->PUOPT.RETURN_ISSUES;conflict->PUOPT.RETURN_ISSUES | PUOPT.ROUTE_OPERATION | stop | Before validation completes or an FSM package preview is produced |
## Related Business Unit Validation

Project Accounting eligibility for additions is validated by Fusion when the approved FSM package is imported. Preserve any returned Fusion error with the package checksum and row identity; do not retry automatically. Removal remains blocked without current usage and deletability evidence.
