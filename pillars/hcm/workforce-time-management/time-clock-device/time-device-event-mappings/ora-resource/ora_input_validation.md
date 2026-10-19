# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Event mapping identity | Name | Stop before preview | Provide a mapping name | Create, or Update after one existing mapping is selected | |
| Required event selection | DeviceSupplierCode, SupplierDeviceEventCode, ApplicationEventCode | Stop before preview | Select all three values from their documented LOVs | Create, or Update after one existing mapping is selected | |
| Event attribute row | TimeAttributeFieldId | Block only the incomplete row | Select a time attribute or remove the optional row | One or more Event Attribute Details are supplied | |
| Parent-child local correlation | MappingId on the parent and every new Event Attribute Detail row | Block preview and upload | For a create, generate one unique numeric local MappingId and repeat it in every new Event Attribute Detail row. For an update, use only the persisted MappingId returned by Fusion on the parent and every child row. | Create or update with Event Attribute Details | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| DeviceSupplierCode changes | SupplierDeviceEventCode is cleared | Refresh the supplier-event provider and require a new selection | resolve_supplier_device_events |
| TimeAttributeFieldId changes | DisplayValue and StringValue are cleared | Resolve the selected attribute data source before selecting a replacement value | resolve_time_attribute_default_values |
| ApplicationEventCode is IN | Use the In event attribute map | Add or edit optional child rows for the IN event | |
| ApplicationEventCode is OUT | Use the Out event attribute map | Add or edit optional child rows for the OUT event | |
| ApplicationEventCode is OUT/IN | Use both event attribute maps | Add or edit optional child rows for both events | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Device supplier is a valid supplier LOV value and is not ORA_HWM_WEBCLOCK | Reject the selection when it is absent from the supplier LOV or is excluded | DeviceSupplierCode is supplied | resolve_device_suppliers |
| Supplier device event belongs to the selected supplier | Reject the selection when it does not match the selected supplier prefix | SupplierDeviceEventCode is supplied | resolve_supplier_device_events |
| Application event is a valid application-event LOV value | Reject the selection when it is absent from the application-event LOV | ApplicationEventCode is supplied | resolve_application_events |
| Mapping code is optional | Allow MappingCode to be omitted; derive no substitute value when it is blank | Create, or Update after one existing mapping is selected | |
| Description is optional | Allow the field to be omitted | Always | |
| Parent mapping REST action | Require POST only when creating a mapping and PATCH only when editing one verified existing mapping; reject UPDATE and any other parent action | Create or Update | |
| Event Attribute Detail REST action | Validate the child action against its own verified child lifecycle; never copy, derive, or infer it from the parent mapping REST action | An Event Attribute Detail row is supplied | |
| Time attribute is selected for every child row | Reject the incomplete row; Default Value remains optional | An Event Attribute Detail row is supplied | resolve_time_attributes |
| Default value is valid for the selected time attribute data source when that attribute is LOV-backed | Reject the dependent value and retain the row for correction | DisplayValue is supplied | resolve_time_attribute_default_values |
| Child event code matches the active event attribute map | Set EventCode to IN for the IN map, OUT for the OUT map, and retain the applicable code for each row when both maps are active | An Event Attribute Detail row is supplied | |
| New Event Attribute Detail MappingId | Require a nonblank numeric value that exactly equals the parent MappingId; for create, treat the repeated values as DAT-local correlations rather than persisted Fusion IDs | Create with Event Attribute Details | |
| Update MappingId | Accept only the persisted MappingId returned by the verified Fusion parent read and require every new or existing Event Attribute Detail row to use that exact parent value; do not generate, replace, or infer an ID | Update with Event Attribute Details | |
| MappingDetailId is supplied | Retain it only for an existing Event Attribute Detail row; do not assign or copy a MappingDetailId to a new child row | Update of an existing Event Attribute Detail | |
| Search attribute is supported | Reject an unknown, technical-only, or unsupported parent or child-resource attribute; do not silently ignore it | A user supplies a search criterion | search_time_device_mappings_by_criteria |
| Complete Summary source values are verified structured business values | Generate the summary only after completed input validation, applicable lookup resolution, and defaulting. Include every verified business value explicitly supplied by the user and every default that was actually applied. | Before the provider-owned approval process | |
| Complete Summary display scope | Omit blank, null, unused, metadata-only, and internal execution values. Show populated child records using business labels only; do not render an empty child section. | A Complete Summary is generated | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TDEM.VALIDATE_MAPPING | step | 10 | validate_input | valid->TDEM.SEARCH_TIME_DEVICE_MAPPINGS;invalid->TDEM.INPUT_ISSUES | none | stop | Search, Create, or Update |
| TDEM.VALIDATE_CHILD_ROWS | step | 60 | validate_input | valid->TDEM.GENERATE_COMPLETE_SUMMARY;invalid->TDEM.INPUT_ISSUES | TDEM.LOOKUP_DEFAULT_VALUES | stop | One or more Event Attribute Details are supplied |
