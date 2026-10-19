# Inventory Task Configurations Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_inventory_organization_by_name | OrganizationName is supplied and OrganizationId or OrganizationCode is required internally. | Supplied OrganizationName. | `/fscmRestApi/resources/11.13.18.05/inventoryAccessibleOrganizations` | OrganizationId, OrganizationCode, OrganizationName | Require exactly one trim and case-insensitive exact OrganizationName match after the finder and q filters are applied. | OrganizationName: parent and child XLSX rows; OrganizationCode: ZoneName derivation. OrganizationId is lookup-only and neither OrganizationId nor OrganizationCode is passed in the XLSX. | Stop Data Loader handoff on a read failure, no exact match, multiple exact matches, or conflicting supplied identity values. |
| resolve_default_zone_by_organization_id | OrganizationId is resolved before parent-root XLSX preparation. | Resolved OrganizationId. | `/fscmRestApi/resources/11.13.18.05/inventoryZoneTaskConfigurations` | OrganizationId, ZoneName, DefaultZone, activityUsages: ActivityTypeCode, TasksEnabled, TaskGroupingLevel, ZoneActivityUsageId | Require exactly zero or one default-zone row. Create requires zero; Update requires one. Do not select items[0] when more than one row is returned. | Create/Update route decision. For Update only, current activity values are used to preserve unspecified settings; identifiers remain BO-managed and are not filled in the XLSX. | Stop on a read failure, more than one default-zone row, a Create request with an existing default zone, or an Update request without one. |
| resolve_activity_task_grouping_level | A display Meaning is supplied for TaskGroupingLevel on CC or PC activity usage. | Supplied Meaning and ActivityTypeCode. | `/fscmRestApi/resources/11.13.18.05:9/standardLookupsLOV` | LookupCode, Meaning | Require exactly one trim and case-insensitive exact Meaning match within the activity-specific allowed codes. | TaskGroupingLevel: LookupCode | Stop Data Loader handoff on a read failure, no exact match, multiple exact matches, or a conflicting supplied LookupCode. |

## Request Parameters

| Resolver | Query parameters |
|---|---|
| resolve_inventory_organization_by_name | `fields=OrganizationId,OrganizationCode,OrganizationName`; `finder=getAccessibleOrgsByPrivilege;Privilege=INV_MANAGE_SUBINVENTORY_DATA`; `limit=2000`; `offset=0`; `onlyData=true`; `orderBy=OrganizationName`; `q=advancedInvParams.TaskManagementAllowedFlag=true and OrganizationName='<escaped supplied OrganizationName>'` |
| resolve_default_zone_by_organization_id | `expand=activityUsages`; `q=OrganizationId=<OrganizationId> and DefaultZone='Y'`; `onlyData=true` |
| resolve_activity_task_grouping_level | `finder=LookupTypeFinder;LookupType=ORA_INV_ZONE_ACTIVITY_GROUPING`; `onlyData=true`; `orderBy=Meaning`; `q=<activity-specific Redwood filter>` |

## Request Headers

| Resolver | Header |
|---|---|
| resolve_inventory_organization_by_name | `REST-Framework-Version: 9` |
| resolve_default_zone_by_organization_id | `REST-Framework-Version: 9` |

## Lookup Execution Rules

The reference lookup paths use the selected task environment; do not embed a pod host or runtime-specific base URL. `core.fusion-api.rest-api-client` supplies the environment base URL from `core/auth/fusionEnv.properties`, sends each documented request header, and serializes the documented query parameters with URL encoding, including the supplied OrganizationName.

The canonical activity defaults and fixed grouping values are defined in `ora_defaulting_rules.md`. Redwood uses `standardLookupsLOV` with `finder=LookupTypeFinder;LookupType=ORA_INV_ZONE_ACTIVITY_GROUPING`, `onlyData=true`, and `orderBy=Meaning` as follows:

| ActivityTypeCode | Complete `q` parameter | Lookup behavior |
|---|---|---|
| PICK | `LookupCode = 'PICKSLIP'` | Fixed default; no user lookup is needed. |
| DEL | `LookupCode IN ( 'DELIVERY_CART' )` | Fixed default; no user lookup is needed. |
| CC | `LookupCode IN ( 'CC_HEADER', 'SUB', 'ZONE' )` | Resolve a supplied display value. |
| PC | `LookupCode IN ( 'PC_HEADER' , 'SUB', 'ZONE' )` | Resolve a supplied display value. |
| PAR | None | Fixed `ZONE`; no lookup is needed. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| INV_TASK_CONFIG.RESOLVE_INVENTORY_ORGANIZATION | step | 15 | reference_lookup | resolved->INV_TASK_CONFIG.RESOLVE_DEFAULT_ZONE;blocked->INV_TASK_CONFIG.RETURN_ISSUES;failure->INV_TASK_CONFIG.RETURN_ISSUES | INV_TASK_CONFIG.VALIDATE_CONDITIONAL_ATTRIBUTES | stop | OrganizationName is supplied for the task configuration. |
| INV_TASK_CONFIG.RESOLVE_DEFAULT_ZONE | step | 20 | reference_lookup | found->INV_TASK_CONFIG.RESOLVE_TASK_GROUPING;missing->INV_TASK_CONFIG.RESOLVE_TASK_GROUPING;blocked->INV_TASK_CONFIG.RETURN_ISSUES;failure->INV_TASK_CONFIG.RETURN_ISSUES | INV_TASK_CONFIG.RESOLVE_INVENTORY_ORGANIZATION | stop | OrganizationId is resolved and the default-zone create-or-update route must be selected. |
| INV_TASK_CONFIG.RESOLVE_TASK_GROUPING | step | 25 | reference_lookup | resolved->INV_TASK_CONFIG.APPLY_ACTIVITY_DEFAULTS;not-applicable->INV_TASK_CONFIG.APPLY_ACTIVITY_DEFAULTS;blocked->INV_TASK_CONFIG.RETURN_ISSUES;failure->INV_TASK_CONFIG.RETURN_ISSUES | INV_TASK_CONFIG.RESOLVE_DEFAULT_ZONE | stop | A supplied TaskGroupingLevel meaning requires resolution; code-only input continues without lookup. |
