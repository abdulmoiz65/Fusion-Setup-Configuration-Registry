# Input Validation

Use the six task business objects only through the task's `core.data-loader` REST route. The public REST reference is the source for service shape; Fusion remains the final validator.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Global recall parameters | One or more requested changes to TimeFrameForTrackingRecall, BypassTaskFlag, TimeFenceForAutoWithdrawal, TimeFenceForAutoClosure, or AutoCloseInTransitTasksFlag | Stop before a singleton lookup or import | Ask the user which supported values must change; do not accept or invent ParameterValueId from user input | recallGlobalParams is supplied | find_existing_recall_global_params |
| Item validation organization | ItemValidationOrganizationName | Stop before a singleton lookup or import | Ask the user for the replacement organization name; do not accept or invent ParameterValueId from user input | recallItemValidationOrganizations is supplied | find_existing_recall_item_validation_organization |
| Participating inventory organization | InventoryOrganizationName | Stop the affected row | Provide one exact inventory organization name per row; provide no rows only when all inventory organizations must participate | recallInventoryOrganizations is supplied | resolve_inventory_organization |
| Containment task owner | OrganizationName, OwnerName, exactly one of SubinventoryName or CostCenterDescription, ActiveFlag | Stop the affected row | Supply the organization, owner, active state, and one mapping dimension | recallContainmentTaskOwners is supplied | resolve_owner_or_coordinator_worker |
| Traceability grouping | InventoryOrganizationName, ProductTraceabilityGrouping | Stop the affected row | Supply one inventory organization and a documented grouping value | recallProductTraceabilityGroupings is supplied | resolve_inventory_organization |
| Recall subinventory | InventoryOrganizationName, Subinventory, PickSubinventoryFlag; StockLocator when the selected subinventory is locator controlled | Stop the affected row | Supply the inventory organization, quarantine subinventory, pick flag, and locator if applicable | recallSubinventories is supplied | resolve_active_subinventory |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Singleton update intent | When the corresponding singleton already exists, require the user to provide the values to update; do not create a second record | recallGlobalParams or recallItemValidationOrganizations is supplied | find_existing_recall_parameter_rows |
| Singleton cardinality and key | Reject more than one source row or more than one existing singleton row. When exactly one existing row is found, require its server-returned ParameterValueId in the Data Loader update record | recallGlobalParams or recallItemValidationOrganizations is supplied | find_existing_recall_parameter_rows |
| Participating-organization semantics | Treat zero supplied and existing rows as all inventory organizations participating; when any rows are supplied or retained, treat only those organizations as participants | recallInventoryOrganizations is in scope | find_existing_recall_parameter_rows |
| Lookup code | Require an exact active generic lookup code; a supplied meaning alone must resolve to exactly one code | A lookup code is supplied or required by the selected configuration | resolve_generic_lookup_code |
| Inventory organization | Require exactly one active target inventory organization for every supplied InventoryOrganizationName or OrganizationName | An inventory-organization field is supplied | resolve_inventory_organization |
| Subinventory and locator | Require an exact active subinventory for its resolved inventory organization and, if a locator is supplied or required, an exact active locator for that organization and subinventory | recallSubinventories or a subinventory owner mapping is supplied | resolve_active_subinventory |
| Owner or coordinator | Require one exact public worker identity before using OwnerName as a containment task owner or coordinator | recallContainmentTaskOwners is supplied | resolve_owner_or_coordinator_worker |
| Business unit and ledger | Require one exact active business unit and, where a ledger is supplied or derived, one exact ledger | A business-unit or ledger context is supplied by the Data Loader schema | resolve_business_unit |
| Owner mapping dimension | Reject a row with both SubinventoryName and CostCenterDescription, or with neither | recallContainmentTaskOwners is supplied | resolve_cost_center_or_location |
| Owner mapping lifecycle | Reject a delete request; an existing mapping may only be deactivated by setting ActiveFlag to false | recallContainmentTaskOwners is supplied | find_existing_recall_parameter_rows |
| Traceability grouping value | Reject a value other than Subinventory, Location, or Inventory Organization | recallProductTraceabilityGroupings is supplied | |
| Recall subinventory suitability | Block preview when supplied evidence does not confirm a quantity-tracked, non-reservable subinventory; require StockLocator when it is locator controlled | recallSubinventories is supplied | |
| In-transit auto-close dependency | Block a true AutoCloseInTransitTasksFlag unless BypassTaskFlag is true | AutoCloseInTransitTasksFlag is true | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RECALL.PARAMETERS.VALIDATE-INPUT | decision | 10 | validate_input | valid->RECALL.PARAMETERS.LOOKUP-EXISTING;invalid->RECALL.PARAMETERS.HANDLE-INPUT-ERROR | none | stop | A create, update, deactivate, or participating-organization scope change is requested |
