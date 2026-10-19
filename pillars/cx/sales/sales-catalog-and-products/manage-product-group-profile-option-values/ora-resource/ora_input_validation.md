# Input Validation

This resource owns input shape for direct QSC value-change and removal requests. FSM-only
profile options bypass this resource. QSC FSM imports use the documented
proposed-value preflight before `core.data-loader` accepts the package.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Direct QSC value change | User asks to attach, assign, use, change, or replace a Sales Products Item Organization; profile_option_code=QSC_SALES_PRODUCTS_INVENTORY_ORG_ID; profile_level=Site; proposed_value and/or item_organization | Stop before preview | Provide the exact profile code, Site level, and one intended organization code or name; when both are supplied, they must identify the same organization | A direct QSC profile-value change is requested | resolve_sales_product_item_master |
| Direct QSC removal | User asks to clear, detach, remove, or delete the Sales Products Item Organization; profile_option_code=QSC_SALES_PRODUCTS_INVENTORY_ORG_ID; profile_level=Site | Stop before preview | Provide the exact profile code and Site level. Do not request a proposed organization. | A direct QSC Site-child removal is requested | |
| Complete valid-organization list | User asks for all valid Sales Products Item Organizations; target environment and approval for a read-only Manage Item Organizations FSM export | Stop before export | Explain why the complete list needs the target-environment export and ask the user for approval. | A complete valid-organization list is requested | |
| QSC FSM import value | An FSM import is explicitly requested; profile_option_code=QSC_SALES_PRODUCTS_INVENTORY_ORG_ID; immutable package with the proposed organization code or name | Stop before import approval | Identify the QSC profile row and its intended organization code or name; when both are present, they must identify the same organization | A QSC FSM import is requested | resolve_sales_product_item_master |
| Reported QSC value | User asks to view the configured value, or a QSC value from an FSM export is being reported; profile value code | Stop before reporting a code-only result | Retrieve the exact Inventory Organizations name for the profile value code | A QSC profile value is reported to the user | get_sales_product_item_organization_name |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Request intent | Classify the user's words as viewing the configured value, providing or changing an organization, removing an organization, or an explicitly requested FSM action. Do not require a fixed action word. | Always | |
| Complete-list approval | Do not run the Manage Item Organizations FSM export until the user explicitly approves the read-only export in the target environment. | User asks for all valid Sales Products Item Organizations | |
| Direct profile code | Require exactly QSC_SALES_PRODUCTS_INVENTORY_ORG_ID | Direct value-change or removal request | |
| Profile level | Require Site | Direct value-change or removal request | |
| Proposed organization identity | Accept one exact organization code or name. When a value is supplied without identifying whether it is a code or name and it matches multiple rows, ask the user which it is before rerunning the exact field match. When both are supplied, require one exact matching record; do not choose an organization | Direct value-change or QSC FSM import request | resolve_sales_product_item_master |
| Reported organization identity | Require an exact Inventory Organizations name lookup for a code returned by ProfileOptions REST or FSM export | Request to view the configured value or report a QSC FSM-export value | get_sales_product_item_organization_name |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QSC.PROFILE.INPUT | decision | 1 | validate_input | report->QSC.PROFILE.VALUE_NAME;value_change->QSC.PROFILE.ITEM_ORGANIZATION;removal->QSC.PROFILE.UNSET_EXECUTION_GATE;invalid->QSC.PROFILE.BLOCKED | none | stop | Run when QSC_SALES_PRODUCTS_INVENTORY_ORG_ID is selected; classify the request intent, then validate a returned profile-value code for reporting, the Site level and proposed item-master code or name for a value change, or the Site level for a removal |
