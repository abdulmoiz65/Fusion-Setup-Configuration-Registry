# Manage Inventory Organizations Reference Lookups

## Source Evidence

| Source | Used For |
|---|---|
| Oracle Fusion Cloud SCM REST API: Get all organizations, https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/fasrp/op-inventoryorganizations-get.html | Read-only collection endpoint, query support, and organization response fields |
| Oracle Fusion Cloud SCM REST API: Inventory Organizations Open List of Values REST Endpoints, https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/fasrp/api-scm-common-list-values-scm-common-inventory-organizations-open-list-values.html | Globally accessible organization LOV endpoint |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_inventory_organization_exact | A source organization must be identified for a copy request, or a proposed organization must be checked for a duplicate | OrganizationId, OrganizationCode, OrganizationName | /fscmRestApi/resources/11.13.18.05/inventoryOrganizations?fields=OrganizationId,OrganizationCode,OrganizationName,Status,InventoryFlag&onlyData=true&q=<exact OrganizationCode or OrganizationName expression> | OrganizationId, OrganizationCode, OrganizationName, Status, InventoryFlag | Use OrganizationId when supplied. Otherwise trim outer whitespace and require exactly one exact OrganizationCode or OrganizationName match; for a source copy, require InventoryFlag=true. For duplicate checking, any exact matching OrganizationCode or OrganizationName is a conflict. | OrganizationId: OrganizationId; OrganizationCode: OrganizationCode; OrganizationName: OrganizationName; Status: Status; InventoryFlag: InventoryFlag | For source copy, stop and request one unambiguous inventory organization. For duplicate checking, stop and request a distinct name or code. Do not fuzzy-match or select the first result. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Direct OrganizationId is provided for a source copy | Use the ID to retrieve and confirm the source organization before approving a copy workflow |
| OrganizationCode or OrganizationName is provided | Run the exact-match lookup before duplicate validation or source-copy selection |
| Lookup is unavailable, inaccessible, or returns an ambiguous source | Stop before any copy, create, or update operation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| INVORG.RESOLVE_EXISTING | decision | 20 | reference_lookup | resolved->INVORG.READY;not_required->INVORG.READY;blocked->INVORG.HANDLE_ERROR;failure->INVORG.HANDLE_ERROR | INVORG.VALIDATE_INPUT | stop | Resolve a source organization or check exact name/code conflicts when the request supplies an organization identifier |
