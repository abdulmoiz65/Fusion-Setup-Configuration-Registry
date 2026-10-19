# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| CostedFlag | N | Creating a resource and CostedFlag is omitted | Yes |  |
| OrganizationId | Derived from OrganizationCode | OrganizationId is omitted and OrganizationCode is supplied | Yes |  |
| DefaultExpenditureTypeId | Derived from DefaultExpenditureTypeName | The ID is omitted and a name is supplied | Yes |  |
| PrimaryWorkCenterId | Derived from PrimaryWorkCenterCode | The ID is omitted and a code is supplied for a valid instance | Yes |  |
| PartyId, LaborIdentifier, LaborInstanceName | Derived from RegistryId or party data where documented | Creating a labor instance with the applicable alternate identifier | Yes |  |
| AssetId, EquipmentIdentifier, EquipmentInstanceName, PrimaryWorkCenterId | Derived from AssetNumber or asset data where documented | Creating an eligible equipment instance with the applicable alternate identifier | Yes | resolve_equipment_asset_by_id |
