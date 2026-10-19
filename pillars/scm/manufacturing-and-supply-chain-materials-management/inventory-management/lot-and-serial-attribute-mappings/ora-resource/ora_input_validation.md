# Lot and Serial Attribute Mappings Input Validation

## Source Evidence

| Source | Used For |
|---|---|
| Redwood attributeFormTemplate | The Attribute Mapping Details radio options bind Lot and Serial labels to DescriptiveFlexfieldName values. |
| Redwood levelTemplate | The Level radio options bind Item and Category labels to ContextColumnName values. |
| User approval | Apply the sourced friendly-value mappings before Data Loader handoff. |

## Scope Boundary

| Boundary | What Happens |
|---|---|
| Backend-owned validation | Data Loader and Fusion own required fields, uniqueness, lengths, server-side domains, and final field enforcement. |
| Local validation ownership | Normalize only the approved Attribute Mapping Details and Level labels to their observed canonical backend values. |
| REST execution | Do not create direct REST write guidance; core.data-loader owns execution for Inventory Descriptive Flexfield Context Mappings. |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Attribute Mapping Details representation | Attribute Mapping Details as Lot or Serial, or DescriptiveFlexfieldName as INV_LOT_ATTRIBUTES or INV_SERIAL_ATTRIBUTES | Preserve a blank when neither representation is supplied. | Supply Lot, Serial, INV_LOT_ATTRIBUTES, or INV_SERIAL_ATTRIBUTES. | Attribute Mapping Details or DescriptiveFlexfieldName is supplied. |  |
| Level representation | Level as Item or Category, or ContextColumnName as ITEM or CATEGORY | Preserve a blank when neither representation is supplied. | Supply Item, Category, ITEM, or CATEGORY. | Level or ContextColumnName is supplied. |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Attribute Mapping Details is Lot | Fill DescriptiveFlexfieldName with INV_LOT_ATTRIBUTES. | Pass the canonical value to Data Loader. |  |
| Attribute Mapping Details is Serial | Fill DescriptiveFlexfieldName with INV_SERIAL_ATTRIBUTES. | Pass the canonical value to Data Loader. |  |
| DescriptiveFlexfieldName is already INV_LOT_ATTRIBUTES or INV_SERIAL_ATTRIBUTES | Preserve the supplied canonical value. | Pass the canonical value to Data Loader. |  |
| Level is Item | Fill ContextColumnName with ITEM. | Pass the canonical value to Data Loader. |  |
| Level is Category | Fill ContextColumnName with CATEGORY. | Pass the canonical value to Data Loader. |  |
| ContextColumnName is already ITEM or CATEGORY | Preserve the supplied canonical value. | Pass the canonical value to Data Loader. |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Attribute Mapping Details normalization | Convert Lot to INV_LOT_ATTRIBUTES and Serial to INV_SERIAL_ATTRIBUTES; preserve canonical values. | Before Data Loader handoff. |  |
| Level normalization | Convert Item to ITEM and Category to CATEGORY; preserve canonical values. | Before Data Loader handoff. |  |
| Unsupported Attribute Mapping Details representation | Reject a supplied value other than Lot, Serial, INV_LOT_ATTRIBUTES, or INV_SERIAL_ATTRIBUTES. | Attribute Mapping Details or DescriptiveFlexfieldName is supplied. |  |
| Unsupported Level representation | Reject a supplied value other than Item, Category, ITEM, or CATEGORY. | Level or ContextColumnName is supplied. |  |
| Conflicting representations | Reject a friendly value and canonical value that represent different options for the same backend field. | Both representations are supplied for Attribute Mapping Details or Level. |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LSAM.NORMALIZE_RADIO_VALUES | step | 10 | validate_input | valid->LSAM.CHECK_DEPENDENCIES;invalid->LSAM.HANDLE_ERROR | LSAM.APPLY_ORGANIZATION_DEFAULT | stop | Before Data Loader task validation or import preparation. |
