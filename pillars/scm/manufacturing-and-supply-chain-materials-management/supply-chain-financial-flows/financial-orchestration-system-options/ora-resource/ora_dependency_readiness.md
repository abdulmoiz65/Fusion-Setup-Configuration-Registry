# Dependency Readiness

Source: Oracle Implement Supply Chain Financial Orchestration documentation and Oracle Financial Orchestration System Options business-object reference.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Implementation project scope | Include Manufacturing and Supply Chain Materials Management in the implementation project and open the System Options task from Supply Chain Financial Flows |
| 2 | Item validation organization | Resolve the selected validation organization before using it for qualifier-based item validation |
| 3 | Service item | Allow a selected Service Item only when the effective Configure service items for global purchase processing value is true; allow an explicit Service Item clear regardless of that value |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| implementation_project_scope | Manufacturing and Supply Chain Materials Management implementation project | Yes | Every System Options setup request | Verify | User confirmation of the active implementation project scope | | The System Options task is accessed from this offering and functional area | Confirm that the active project includes Manufacturing and Supply Chain Materials Management, Supply Chain Financial Flows, and Financial Orchestration System Options | implementationProjectScopeConfirmation: true |
| system_options_record | Financial Orchestration System Options record | Yes | Every System Options setup request | Lookup | ORA_FSCM_REST financialOrchestrationSystemOptions, BO short name ORA_FOS_SYSTEM_OPTION | find_system_options_record | Oracle documents that System Options contains only one row | Allow an update only when exactly one record exists; allow a create only when no record exists; stop if more than one record is returned | SystemOptionId: id |
| item_validation_organization | Item validation organization | Yes | Every System Options setup request | Lookup | financialOrchestrationItemOrganizationsLOV OrganizationName, OrganizationCode, OrganizationId | resolve_validation_organization | Financial Orchestration uses this organization to validate items according to qualifiers | Provide the intended organization name | validationOrganizationId: OrganizationId |
| service_item | Service item | Conditional | Effective `GPOServiceItem = "Y"`, a non-null Service Item is requested, and `clearServiceItem` is not true | Lookup | financialOrchestrationServiceItemsLOV filtered by the resolved OrganizationId | resolve_service_item | Financial Orchestration tasks use the service item for the applicable service-item flow | Select one item from the LOV returned for the resolved Item Validation Organization; never infer processing enablement | serviceItemId: InventoryItemId |
| target_rest_contract | Target Fusion REST endpoint | Yes | Every live lookup or change request | Verify | Configured Fusion REST base URL and documented `resources/latest` paths | | The tested LOV and System Options resources are served by the current REST resource contract | Do not use a different pod or a legacy `rest/rv` path | configuredRestBaseUrl; documentedResourcePath |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Project-scope gap | The implementation project does not include the required offering or task | No |
| Reference-resolution gap | The required validation organization or service item is absent, ambiguous, or unresolved | Lookup only when the documented contract is completed |
| Ready for separate workflow | Every applicable dependency is satisfied | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FOS.SO.CHECK_DEPENDENCIES | step | 20 | resolve_dependency | ready->FOS.SO.RESOLVE_RECORD;blocked->FOS.SO.HANDLE_ISSUE | FOS.SO.VALIDATE_INPUT | stop | After supplied System Options values pass input validation |
