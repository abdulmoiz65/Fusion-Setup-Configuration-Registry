# Input Validation

Source: Oracle Financial Orchestration System Options documentation and Oracle SCM business-object reference.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Item validation organization | OrganizationName | Blocked | Provide one organization name, then resolve exactly one matching Item Validation Organization LOV record | Every System Options setup request | resolve_validation_organization |
| Implementation project scope | implementationProjectScopeConfirmation = true | Blocked | Confirm that the active implementation project includes Manufacturing and Supply Chain Materials Management, Supply Chain Financial Flows, and Financial Orchestration System Options | Every System Options setup request | |
| System Options record state | Zero or one Financial Orchestration System Options record | Blocked | Read the existing record state before preparing a change; update the one existing record, or create one only when no record exists | Every System Options setup request | find_system_options_record |
| Service-item handling | Configure service items for global purchase processing = true for a selected non-null Service Item; explicit `clearServiceItem = true` for a clear | Blocked | Enable processing before selecting an item from that organization's LOV; an explicit clear is allowed regardless of processing state | A Service Item is supplied, explicitly cleared, or the global procurement description-line flow requires service-item setup | resolve_service_item |
| Event-processing batch size | Maximum Number of Records per Batch | Blocked | Provide the number of supply chain event records Financial Orchestration should process per batch | Every System Options setup request | |
| Trade-processing options | Calculate tax for trade receipt accrual; Ignore bill only flows; Process referenced RMA without forward flow as unreferenced | Blocked | State the selected options and business rationale before preview | The corresponding trade, bill-only, or referenced-return scenario is in scope | |

## Service Item Guardrail

Evaluate **Configure service items for global purchase processing** as the
effective value after the requested change: use the explicitly supplied value
when present, otherwise the currently configured value.

| Requested Service Item action | Required effective processing option | Required evidence | Result when the requirement is not met |
|---|---|---|---|
| Set `ServiceItemId` to a non-null value | `GPOServiceItem = "Y"` | One Service Item selected from the LOV for the resolved Item Validation Organization | Block the payload; do not set a Service Item or implicitly enable processing. |
| Clear `ServiceItemId` (`null`) | Any effective `GPOServiceItem` value | An explicit user request to clear the Service Item | Allow the clear; an omitted Service Item is not a clear request. |
| Omit `ServiceItemId` | No Service Item action | None | Preserve the existing Service Item value. |

The guardrail applies equally to create and update payloads. A Service Item
must never be set while the effective processing option is `N`; an explicit
clear remains allowed whether that option is `Y` or `N`.

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Validation organization is missing or ambiguous | Blocked | Resolve exactly one organization | resolve_validation_organization |
| Non-null Service Item and effective `GPOServiceItem = "N"` | Blocked | Set `GPOServiceItem` to `Y` in the approved payload | |
| Non-null Service Item is absent from the resolved organization LOV | Blocked | Select one LOV row for that organization | resolve_service_item |
| Explicit Service Item clear | Continue | Set `ServiceItemId: null` | |
| System Options lookup returns more than one row | Blocked | Investigate the duplicate state | find_system_options_record |
| System Options lookup returns one row | Continue | Prepare an update for that row | find_system_options_record |
| System Options lookup returns zero rows | Continue | Prepare a create | find_system_options_record |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Supported option identity | Accept only the documented System Options fields: Item Validation Organization, service-item processing option, Service Item, Maximum Number of Records per Batch, Calculate tax for trade receipt accrual, Ignore bill only flows, and Process referenced RMA without forward flow as unreferenced | Every supplied value | |
| Configured business object identity | Use only financialOrchestrationSystemOptions with BO short name ORA_FOS_SYSTEM_OPTION in the ORA_FSCM_REST context | Every read, create, or update preparation request | |
| Single-record guard | Do not prepare a create when one System Options record exists; do not prepare an update when no record exists; stop if more than one record is returned | Every System Options setup request | find_system_options_record |
| Item validation organization purpose | Confirm that the selected organization is used for item validation against Financial Orchestration qualifiers | Item Validation Organization is supplied | resolve_validation_organization |
| Service item enablement | Accept a non-null Service Item only when the effective Configure service items for global purchase processing value is true; never enable it implicitly | A Service Item is supplied | |
| Service item clear | Accept `clearServiceItem = true` whether the effective Configure service items for global purchase processing value is true or false; prepare `ServiceItemId: null` only for that explicit clear request | A Service Item clear is explicitly requested | |
| Service item organization scope | Accept only a Service Item returned by the LOV query filtered with the resolved Item Validation Organization ID | Configure service items for global purchase processing is true | resolve_service_item |
| Payload scope | Include only fields explicitly supplied and approved for this request; preserve every unmentioned System Options field | Every create or update preview | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FOS.SO.VALIDATE_INPUT | step | 10 | validate_input | validated->FOS.SO.CHECK_DEPENDENCIES;blocked->FOS.SO.HANDLE_ISSUE | none | stop | Every request |
