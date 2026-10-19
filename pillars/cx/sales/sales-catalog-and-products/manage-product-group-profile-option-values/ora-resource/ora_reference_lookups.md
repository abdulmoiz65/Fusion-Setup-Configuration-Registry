# Reference Lookups

This resource owns read-only Inventory Organizations lookup mechanics for
`QSC_SALES_PRODUCTS_INVENTORY_ORG_ID`. It does not own the FSM export used to
list all organizations; that export is routed by the task guide. A code read
from ProfileOptions REST or an FSM export is never reported without its
Inventory Organizations name.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| get_sales_product_item_organization_name | A single QSC profile value code is read from ProfileOptions REST or from an FSM export and will be reported | Profile value code | /fscmRestApi/resources/11.13.18.05/inventoryOrganizations | OrganizationCode, OrganizationName | Match exactly one record whose OrganizationCode equals the profile value code | reported_item_organization: OrganizationCode, OrganizationName | Stop the report as unresolved; do not return a code-only organization result or substitute a name. Do not run this resolver when listing all valid organizations: the FSM CSV files already provide those names. |
| resolve_sales_product_item_master | A direct QSC request provides an organization code or name, or a QSC FSM import does, or a REST configured-value read returns V1 and validity is required | Proposed OrganizationCode and/or OrganizationName, or REST-returned V1 | /fscmRestApi/resources/11.13.18.05/inventoryOrganizations | OrganizationId, OrganizationCode, OrganizationName, MasterOrganizationCode, active-state field | When a value is supplied without identifying whether it is a code or name, match active master records where OrganizationCode or OrganizationName equals the value. If that yields multiple rows, ask which it is, then rerun against only that field. Match exactly one record where OrganizationCode equals MasterOrganizationCode. When both source values are supplied, they must match that same record. | resolved_item_organization: OrganizationCode, OrganizationName, MasterOrganizationCode, OrganizationId | Zero matches: identify or create the item master through Manage Item Organizations before retrying. A code/name conflict, multiple matches after the user identifies the field, or REST access/data-security failure blocks validation. |
| get_sales_product_item_organization_details | Organization details beyond the mandatory name are requested | Profile value code or resolved organization code and requested fields | /fscmRestApi/resources/11.13.18.05/inventoryOrganizations | OrganizationCode, OrganizationName, and only the additional requested fields | Match exactly one record whose OrganizationCode equals the resolved or reported code | requested_organization_details | Report no match or multiple matches without substituting a value. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| ProfileOptions REST or FSM export returns one QSC profile value code | Run get_sales_product_item_organization_name and report both OrganizationCode and OrganizationName. This is distinct from listing all valid organizations, for which the FSM CSV files already provide the names. |
| REST configured-value read returns V1 | Run get_sales_product_item_organization_name, then run resolve_sales_product_item_master before reporting V1 as valid. |
| QSC import or Site PATCH is requested | Run resolve_sales_product_item_master for the proposed code or name before the mutation or import. Use its resolved OrganizationCode as the profile value. |
| Details are requested | First run get_sales_product_item_organization_name, then run get_sales_product_item_organization_details when more fields are requested. Do not imply item-master validity unless it was separately validated. |
| A value supplied without identifying whether it is a code or name returns multiple rows | Ask the user whether the supplied value is an organization code or organization name, then rerun only that exact field match. |
| Name resolution or validation cannot establish exactly one required match after field selection | Stop the report, mutation, or import as applicable; do not substitute an FSM list, browser LOV, raw SQL result, or arbitrary code/name match. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QSC.PROFILE.VALUE_NAME | step | 2 | reference_lookup | resolved->QSC.PROFILE.REPORTED;unresolved->QSC.PROFILE.BLOCKED;failure->QSC.PROFILE.FAILED | QSC.PROFILE.INPUT | stop | Run when a QSC profile value from ProfileOptions REST or an FSM export is reported; resolve the returned OrganizationCode to OrganizationName |
| QSC.PROFILE.ITEM_ORGANIZATION | step | 4 | reference_lookup | resolved->QSC.PROFILE.DEPENDENCY;not_found->QSC.PROFILE.MASTER_ORG_MISSING;blocked->QSC.PROFILE.BLOCKED;failure->QSC.PROFILE.FAILED | QSC.PROFILE.INPUT | stop | Run only when a direct QSC request provides an organization for QSC_SALES_PRODUCTS_INVENTORY_ORG_ID; resolve the proposed item-master organization code or name before profile-value execution planning |
