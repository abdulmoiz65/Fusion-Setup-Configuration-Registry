# Configure Planning Analytics Level-Attribute Validation

## Purpose

Validate level-attribute creation inputs against the Fusion-supported names for the selected level. Runbooks own batch assembly and writes through core.data-loader; these rules return validation results only.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CPA.VALIDATE_ITEM_ATTRIBUTE | decision | 50 | validate_input | pass->CPA.ITEM_ATTRIBUTE_VALIDATED;invalid->CPA.LOOKUP_FAILURE;unresolved->CPA.LOOKUP_FAILURE | CPA.LOOKUP_ITEM_ATTRIBUTE_NAMES | stop | Validate candidate AttributeName and any supplied DbDataType for LevelId 1 using the completed find_item_level_attribute_names result |
| CPA.VALIDATE_ORGANIZATION_ATTRIBUTE | decision | 51 | validate_input | pass->CPA.ORGANIZATION_ATTRIBUTE_VALIDATED;invalid->CPA.LOOKUP_FAILURE;unresolved->CPA.LOOKUP_FAILURE | CPA.LOOKUP_ORGANIZATION_ATTRIBUTE_NAMES | stop | Validate candidate AttributeName and any supplied DbDataType for LevelId 40 using the completed find_organization_level_attribute_names result |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Item level supported attribute name | Accept only a positive supported-name result; an invalid or unresolved result blocks creation. This validates an input enum against Fusion, not a local allowlist. | A level attribute is being created or its name validated for LevelId 1 | find_item_level_attribute_names |
| Organization level supported attribute name | Accept only a positive supported-name result; an invalid or unresolved result blocks creation. This validates an input enum against Fusion, not a local allowlist. | A level attribute is being created or its name validated for LevelId 40 | find_organization_level_attribute_names |
| Item level datatype consistency | When DbDataType is supplied, require an integer equal to the expected DbDataType returned by the named resolver. A conflicting value returns invalid and reports supplied and expected values; missing or malformed lookup datatype evidence returns unresolved. Never overwrite the supplied value. | LevelId 1 name validation passed and DbDataType is supplied | find_item_level_attribute_names |
| Organization level datatype consistency | When DbDataType is supplied, require an integer equal to the expected DbDataType returned by the named resolver. A conflicting value returns invalid and reports supplied and expected values; missing or malformed lookup datatype evidence returns unresolved. Never overwrite the supplied value. | LevelId 40 name validation passed and DbDataType is supplied | find_organization_level_attribute_names |

## Supplied Input Contract

The developer's create example contains a parts array with id, operation=create, path and payload; its child path targets planningLevels/1/child/LevelAttributes. The payload supplies AttributeName as a string, DbDataType as an integer, and Label as a string. The example values GLOBAL_ATTRIBUTE_DATE5, 3 and test are illustrative, not defaults or a general datatype mapping. The name-list lookups now provide the matched name and datatype mapping defined in ora_reference_lookups.md. Preserve supplied values; do not infer datatype from attribute-name suffixes or silently replace a conflicting user value. The source does not establish additional required fields, an exhaustive datatype enum, or label limits. Payload construction and submission remain owned by the selected runbook and core.data-loader.

## Supported Level Scope

The supplied responses resolve the item and organization name-list mappings. Creation-name validation is supported for LevelIds 1 and 40 through their respective resolvers. Other LevelIds have no supplied supported-name endpoint and must not reuse either mapping by assumption.

## Validation Outcomes

A pass requires a valid supported name and, when DbDataType is supplied, a matching integer datatype. An absent supplied datatype is not defaulted here; return the lookup's expected value for the owning Data Loader input/schema workflow. These rules do not waive its required-field checks. Invalid names and datatype conflicts return invalid; incomplete or ambiguous lookup evidence returns unresolved. Each validation branch has its own success terminal.
