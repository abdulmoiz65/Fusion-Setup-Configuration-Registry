# RFID Integrations and Devices Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Data Loader BO metadata | Run a fresh selected-environment metadata preflight before every load |
| 2 | Input resolution | Resolve approved Device Type and standard lookup values before Data Loader handoff |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| rfid_configurations_bo_metadata | inventoryRFIDConfigurations registration and metadata | Yes | Every Data Loader handoff involving integrations | Verify | Per-run Data Loader metadata preflight in the selected environment; external registration confirmation is user-provided provenance only | | Confirms current environment visibility and schema for the integrations BO | Run the metadata preflight for inventoryRFIDConfigurations. A prior successful run is not reusable readiness evidence. | Selected environment, inventoryRFIDConfigurations discriminator, metadata result |
| rfid_devices_bo_metadata | inventoryRFIDDevices registration, metadata, and Processes component visibility | Yes | Every Data Loader handoff involving devices or processes | Verify | Per-run Data Loader metadata preflight in the selected environment; external registration confirmation is user-provided provenance only | | Confirms current environment visibility and schema for the Devices BO and its processes child component | Run the metadata preflight for inventoryRFIDDevices and confirm its processes component. A failed or unavailable preflight blocks the load; do not fall back to direct REST execution. | Selected environment, inventoryRFIDDevices discriminator, processes component, metadata result |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Current selected-environment metadata preflight confirms the applicable BO and child component | Yes |
| Verify | A new load or environment requires fresh metadata evidence | Read-only check only |
| Unresolved | Metadata preflight is unavailable, fails, or does not expose the required BO or processes component | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RFID.PREFLIGHT_BOS | decision | 3 | resolve_dependency | ready->RFID.RESOLVE_DEVICE_TYPE;unresolved->RFID.HANDLE_ERROR | RFID.VALIDATE_INPUT | stop | Complete the fresh selected-environment Data Loader metadata preflight for every applicable registered BO |
