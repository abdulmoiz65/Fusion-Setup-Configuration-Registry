# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_existing_item_master_organizations | An item organization is being created | None; query the enterprise's existing active item organizations | /fscmRestApi/resources/11.13.18.05/inventoryOrganizations?finder=itemOrgs;Status=Active&fields=OrganizationId,OrganizationCode,OrganizationName,MasterOrganizationName,ItemDefinitionOrganizationName | OrganizationId, OrganizationCode, OrganizationName, MasterOrganizationName, ItemDefinitionOrganizationName | Retain existing self-master organizations where MasterOrganizationName equals OrganizationName. Do not query or match the organization being created, because it does not yet exist. | Existing item master IDs, codes, names, and count | Zero, one, and multiple matches are all valid lookup results. Pass the count and records to design enforcement; only a request failure is an error. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| MIO.FIND_EXISTING_ITEM_MASTERS | decision | 4 | reference_lookup | existing_none->MIO.ENFORCE;existing_one->MIO.ENFORCE;existing_multiple->MIO.ENFORCE;failed->MIO.HANDLE_ISSUE | MIO.DESIGN_GATE | stop | Creation |
