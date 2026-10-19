# Reporting Hierarchy Generation Dependency Readiness

Source: [Oracle Reporting Hierarchy Generation](https://docs.oracle.com/en/cloud/saas/sales/fauss/reporting-hierarchy-generation.html).

## Required Dependency Order

Discovery operations end after their read-only lookup. They do not require an
organization change, scheduled-process privilege, execution approval, or ESS
submission readiness.

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Organization hierarchy change | Run the scheduled process after a manager or organization change that requires reporting hierarchy updates. This applies only to `submit`. |
| 2 | Required privilege | Verify the submitting user has Application Implementation Consultant, Master Data Management Application Administrator, or Run Trading Community Resource Reporting Hierarchy Generation privilege. |
| 3 | Tree Code validation | Confirm the supplied Tree Structure Code and Tree Code exist as an exact pair through the configured Fusion connection's `fndTrees` REST response, passing `REST-Framework-Version: 9`. |
| 4 | Tree Version validation | Confirm the supplied Tree Version ID exists for the supplied Tree Structure Code and Tree Code through the configured Fusion connection's `fndTreeVersions` REST response, passing `REST-Framework-Version: 9`. Display Status, EffectiveStartDate, and EffectiveEndDate; classify as FUTURE when the start date is after the current validation date, INACTIVE only when both dates are before it, and ACTIVE otherwise. Require additional confirmation only for INACTIVE. |
| 5 | Explicit execution approval | Confirm the validated Tree Code and Tree Version and exact bound parameters before submitting. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| RH.DEP.HIERARCHY_CHANGE | Organization hierarchy readiness | Yes | `submit=true` | Verify | Current submit-request hierarchy context |  | Oracle requires the process after manager or organization hierarchy changes. | Confirm the hierarchy change and selected tree version in the current submit request; do not reuse discovery or prior-request values. | Tree Structure Code, Tree Code, Tree Version ID |
| RH.DEP.PRIVILEGE | Scheduled-process privilege | Yes | Before scheduling | Verify | Oracle-documented role or privilege |  | Oracle requires an authorized role or the Run Trading Community Resource Reporting Hierarchy Generation privilege. | Use an authorized implementation or master-data-management role, or obtain the required privilege. | Authorization confirmation |
| RH.DEP.TREE | Tree Code | Yes | Before `submit` scheduling | Verify | Current-submit Tree Structure Code and Tree Code | reporting_hierarchy_tree | The selected tree must exist through the configured Fusion connection. | Require an exact returned TreeStructureCode and TreeCode pair. If no exact match is returned, report it to the user and stop; do not substitute another tree. | Validated Tree Structure Code and Tree Code |
| RH.DEP.TREE_VERSION | Tree Version | Yes | Before `submit` scheduling | Verify | Current-submit Tree Structure Code, Tree Code, and Tree Version ID | reporting_hierarchy_tree_version | The selected version must exist for the selected tree through the configured Fusion connection. | Require exactly one returned TreeVersionId equal to the supplied value. Display Status, EffectiveStartDate, and EffectiveEndDate. Classify it as FUTURE when the start date is after the current validation date, INACTIVE only when both dates are before it, and ACTIVE otherwise. Require explicit confirmation only for INACTIVE. | Validated Tree Version ID, Status, EffectiveStartDate, EffectiveEndDate, and ACTIVE/FUTURE/INACTIVE classification; inactive-version confirmation when applicable |
| RH.DEP.EXECUTION_APPROVAL | Explicit execution approval | Yes | Before submitting a new ESS request | Satisfied | Explicit user approval |  | ESS submission has side effects. | Approve the configured job definition, application, and exact bound parameters. | Job definition ID, application, resolved request parameters |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required hierarchy context and privilege are confirmed. | No |
| Verify | A documented prerequisite must be confirmed, but no authoritative verification contract was supplied. | No |
| Blocked | A prerequisite is absent, cannot be confirmed, or is unauthorized. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| RH.DEPENDENCIES | decision | 6 | resolve_dependency | ready->RH.DESIGN;blocked->RETURN_ISSUES | RH.TREE_VERSION_LOOKUP | stop | Required submit parameters, validated Tree Code and Tree Version, and execution approval are present. |  |
