# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Resource identity | OrganizationId or OrganizationCode; ResourceType; ResourceName; ResourceCode; UomCode | Block preview | Supply the missing values; OrganizationCode may derive OrganizationId through the documented REST validation path | Creating or updating a production resource |  |
| Costing | CostedFlag; DefaultExpenditureTypeId or DefaultExpenditureTypeName when costing applies | Use N only when CostedFlag is omitted; otherwise block invalid values | Use Y or N for CostedFlag and provide a valid expenditure type when needed | Creating or updating a costed resource |  |
| Labor instance | LaborInstanceCode; LaborInstanceName; optional PartyId or RegistryId; optional PrimaryWorkCenterId or PrimaryWorkCenterCode | Block the child request | Supply values valid for a LABOR parent resource | Creating or updating a labor instance | resolve_parent_resource |
| Equipment instance | EquipmentInstanceCode; EquipmentInstanceName; optional AssetId or AssetNumber; optional PrimaryWorkCenterId or PrimaryWorkCenterCode | Block the child request | Supply values valid for an EQUIPMENT parent resource | Creating or updating an equipment instance | resolve_parent_resource |
| Automation program file | ProgramFileId or ProgramFileName | Block the child request | Supply one program-file identifier for an automation-enabled equipment resource | Creating a program-file association | resolve_parent_resource |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| ResourceType is LABOR and HcmSchedulingGroupCode is supplied | Plant HCM scheduling must be enabled and the scheduling group must be valid | Stop if the service validation fails |  |
| AutomationEquipmentFlag is Y | ResourceType must be EQUIPMENT and plant robotics must be enabled | Stop until the service validation passes |  |
| A primary work center is supplied for an instance | The work center must be assigned to the parent resource | Stop until the association is valid | resolve_work_center_by_id |
| An equipment asset is supplied | The asset must be eligible for the plant and work-center context and not already actively associated | Stop until a valid asset is supplied | resolve_equipment_asset_by_id |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| ResourceType | Accept only a valid ORA_WIS_RESOURCE_TYPE value; normalize to uppercase before persistence | Create or update |  |
| ResourceClassCode | Require an active ORA_WIS_RESOURCE_CLASS value when supplied | Create or update |  |
| ResourceCode and ResourceName | Require uniqueness within OrganizationId | Create or update |  |
| UomCode | Require a valid unit of measure; do not change it after work-center assignment or resource-rate use | Create or update |  |
| InactiveDate | Require a future date; an instance cannot end after its parent resource | Deactivation or update |  |
| Client-generated IDs | Do not send ResourceId, LaborInstanceId, EquipmentInstanceId, or EquipmentProgramFileId on create | Create |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MFGRES.VALIDATE_INPUT | decision | 1 | validate_input | valid->MFGRES.DEPENDENCIES;invalid->MFGRES.BLOCKED | none | stop | A Manufacturing Resources create, update, child-instance, or program-file request is prepared. |
