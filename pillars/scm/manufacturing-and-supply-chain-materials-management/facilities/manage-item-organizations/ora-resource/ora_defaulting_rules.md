# Defaulting Rules

## Defaulting Order

| Sequence | What Must Happen |
|---|---|
| 1 | When both MasterOrganizationName and MasterOrganizationCode are not provided, default only MasterOrganizationName from OrganizationName. Do not default MasterOrganizationCode. |
| 2 | Resolve ItemGroupingCode when its value is not provided, using the resolved master organization identity. |
| 3 | Default ItemDefinitionOrganizationName only after the resolved ItemGroupingCode is ORA_RCS_IGB_DFTN and its value is not provided. |

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| MasterOrganizationName | OrganizationName | Both MasterOrganizationName and MasterOrganizationCode are not provided for a self-referencing item master | No |  |
| InventoryFlag | false | Value is not provided for an item organization | No |  |
| ItemGroupingCode | ORA_RCS_IGB_DFTN | Value is not provided and MasterOrganizationName equals the new OrganizationName, or the new organization self-references as its master item organization | No |  |
| ItemGroupingCode | ORA_RCS_IGB_RFRC | Value is not provided and the ORA_RCS_IGB_DFTN condition does not apply | No |  |
| ItemDefinitionOrganizationName | New OrganizationName | Value is not provided and the ItemGroupingCode resolved in defaulting sequence 1 is ORA_RCS_IGB_DFTN | No |  |
| All other fields | No default | A value is provided | No |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| MIO.APPLY_DEFAULTS | step | 1 | apply_default | defaulted->MIO.VALIDATE | none | stop | Creation request |
