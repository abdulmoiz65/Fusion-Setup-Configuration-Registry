# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Device supplier | Select a permitted supplier before selecting its supplier device event |
| 2 | Supplier device event | Resolve the event using the selected supplier as the filter |
| 3 | Application event | Select the Oracle application event that controls the visible event attribute map or maps |
| 4 | Time attribute | For each optional Event Attribute Detail row, select the time attribute before selecting a default value |
| 5 | Default value | Select only a value supported by the selected time attribute data source when the attribute is LOV-backed |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| TDEM.DEVICE_SUPPLIER | Device supplier | Yes | Always | Lookup | ORA_HWM_TCD_SUPPLIERS common lookup | resolve_device_suppliers | Supplier device events are dependent on the supplier | Select a supplier before continuing | DeviceSupplierCode |
| TDEM.SUPPLIER_EVENT | Supplier device event | Yes | Always | Lookup | ORA_HWM_TCD_SUPPLIER_EVENTS common lookup filtered by selected supplier | resolve_supplier_device_events | The selected event must belong to the selected supplier | Re-select the supplier event after changing the supplier | SupplierDeviceEventCode |
| TDEM.APPLICATION_EVENT | Application event | Yes | Always | Lookup | ORA_HWM_TCD_EVENTS common lookup | resolve_application_events | The application event determines which event attribute map or maps apply | Select IN, OUT, or OUT/IN as applicable | ApplicationEventCode |
| TDEM.TIME_ATTRIBUTE | Time attribute | Yes | An Event Attribute Detail row is supplied | Lookup | timeAttributeFieldsLOV | resolve_time_attributes | Each child row maps one time attribute | Select a time attribute for every retained row | TimeAttrFieldIdRW |
| TDEM.DEFAULT_VALUE | Default value | Conditional | A default value is supplied for an LOV-backed time attribute | Lookup | Selected attribute data source and ValuesList | resolve_time_attribute_default_values | The dependent value is driven by the selected time attribute | Clear the value and select an allowed replacement after changing the time attribute | DisplayValueRW |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The required value is present and resolves to exactly one permitted LOV entry | Yes |
| Blocked | A required value is missing, excluded, or has no matching dependent LOV value | No |
| Needs correction | A parent value changed and its dependent selection was cleared | Yes |
