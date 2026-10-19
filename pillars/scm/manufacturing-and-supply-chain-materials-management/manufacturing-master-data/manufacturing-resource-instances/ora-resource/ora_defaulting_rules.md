# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| PrimaryWorkCenterId | Derived from the exact verified work-center code | The code is supplied and the ID is absent | No | verify_primary_work_center_assignment |
| AssetId | Derived from AssetNumber | The asset number is supplied and the ID is absent for EQUIPMENT | No | verify_equipment_asset |
| EquipmentIdentifier and EquipmentInstanceName | Derived from AssetNumber | A valid AssetId is supplied and either value is absent for EQUIPMENT | No | verify_equipment_asset |
| PrimaryWorkCenterId | Derived from the eligible asset work center | A valid AssetId is supplied, the ID is absent, and the asset work center is assigned to the parent resource | No | verify_equipment_asset |
| PartyId | Exact PartyId mapping in reviewed LaborEligibilityEvidence | The registry identifier is supplied and PartyId is absent for LABOR; validate MRINST.PERSON first | No | |
| PartyId | Derived from one exact laborResourceInstancesLOV PartyName match | Person, Person Name, or Party Name is supplied and PartyId and RegistryId are absent for LABOR | No | resolve_labor_party_by_name |
| LaborIdentifier and LaborInstanceName | Values explicitly present in reviewed LaborEligibilityEvidence | MRINST.PERSON passes and either value is absent for LABOR | No | |
| PrimaryResourceFlag | N | An inactive date is supplied for a LABOR instance | No |  |

Do not overwrite supplied values. Any derived primary work center must still pass verify_primary_work_center_assignment; any conflicting value blocks. Derivation evidence must precede final required-field validation.
