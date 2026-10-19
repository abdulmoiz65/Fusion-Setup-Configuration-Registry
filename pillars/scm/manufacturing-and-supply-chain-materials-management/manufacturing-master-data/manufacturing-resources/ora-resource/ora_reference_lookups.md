# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_parent_resource | ResourceId | ResourceId | /fscmRestApi/resources/11.13.18.05/productionResources/{ResourceId} | ResourceId, OrganizationId, OrganizationCode, ResourceType, AutomationEquipmentFlag, InactiveDate | Match the exact ResourceId | ResourceId, OrganizationId, ResourceType, AutomationEquipmentFlag, InactiveDate | Stop when the resource does not exist or does not match the required parent type. |
| resolve_work_center_by_id | PrimaryWorkCenterId is supplied | PrimaryWorkCenterId | /fscmRestApi/resources/11.13.18.05/workCenters/{WorkCenterId} | WorkCenterId and returned work-center identity | Match the exact WorkCenterId | PrimaryWorkCenterId | Stop when the work center does not exist. The service validation remains authoritative for its assignment to the resource. |
| resolve_equipment_asset_by_id | AssetId is supplied | AssetId | /fscmRestApi/resources/11.13.18.05/installedBaseAssets/{AssetId} | AssetId and returned asset identity | Match the exact AssetId | AssetId | Stop when the asset does not exist. The service validation remains authoritative for plant, work-center, and active-association eligibility. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A rule is enforced by the productionResources service but has no independent lookup endpoint | Use core.data-loader validation; do not infer or call an alternate API. |
| More than one candidate is returned | Stop and ask for a unique identifier. |
| No candidate is returned | Stop and ask for a valid identifier. |
