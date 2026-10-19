# Material Statuses Dependency Readiness

## Source Evidence

| Source | Used For |
|---|---|
| Implementation owner confirmation | External BO registration is complete for inventoryMaterialStatuses |
| Live Data Loader metadata retrieval | Confirms Inventory Material Statuses, discriminator inventoryMaterialStatuses, parent and child metadata sections, and user keys |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Input normalization | Normalize supplied friendly 1/2 values before Data Loader preparation |
| 2 | Data Loader metadata visibility | Use the verified inventoryMaterialStatuses metadata contract before execution planning |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| inventory_material_statuses_bo | Data Loader business object metadata | Yes | Before core.data-loader prepares an import | Satisfied | Live metadata retrieval for inventoryMaterialStatuses |  | The registered BO and its parent and child metadata are visible in the configured environment | Use inventoryMaterialStatuses for Material Statuses data preparation | inventoryMaterialStatuses |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MSTAT.CHECK_READINESS | decision | 20 | resolve_dependency | ready->MSTAT.DATA_LOADER_HANDOFF;blocked->MSTAT.HANDLE_ERROR | MSTAT.VALIDATE_INPUT | stop | After input normalization and before handing data to core.data-loader |
