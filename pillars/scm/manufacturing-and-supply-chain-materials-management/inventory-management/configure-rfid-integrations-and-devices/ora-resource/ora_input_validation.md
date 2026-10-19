# RFID Integrations and Devices Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Integration or device type | DeviceTypeCode or Device Type display value | Block | Supply one supported code or display value | An integration or device record is supplied | resolve_rfid_device_type |
| Integration status | EnabledFlag or Status | Block | Supply Active, Inactive, true, false, Y, or N | An integration record is supplied | |
| Device status | EnabledFlag or Status | Default | Omit the value to use Boolean false; otherwise supply Active, Inactive, true, or false | A device record is supplied | |
| Process event type | EventTypeCode or Event Type display value | Block | Supply one exact active Event Type code or meaning | A processes child row is supplied | resolve_rfid_process_event_type |
| Process type | ProcessTypeCode or Process Type display value | Block | Supply one exact Process Type code or meaning | A processes child row is supplied | resolve_rfid_process_type |
| Process status | EnabledFlag or Status | Block | Supply Active, Inactive, true, or false | A processes child row is supplied | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Device Type mapping | Accept RFID Surface Read Point or RFID_SURFACE_READER and map to DeviceTypeCode RFID_SURFACE_READER. Accept RFID Cabinet or RFID_Cabinet and map to DeviceTypeCode RFID_Cabinet. Reject any other value. | Integration or device Device Type is supplied | resolve_rfid_device_type |
| Integration Status normalization | Normalize Active or true to EnabledFlag Y. Normalize Inactive or false to EnabledFlag N. Accept directly supplied Y or N after canonical validation. | An integration record is supplied | |
| Device Status normalization | Normalize Active or true to Boolean EnabledFlag true. Normalize Inactive or false to Boolean EnabledFlag false. Apply the Boolean value for both create and update Data Loader preparation; do not accept or emit Y or N for a device status. | A device record is supplied | |
| Process Status normalization | Normalize Active to EnabledFlag true and Inactive to EnabledFlag false. Accept Boolean true or false. The observed processes child payload remains Boolean; do not convert it to Y or N. | A processes child row is supplied | |
| Event Type resolution | Accept an exact Event Type meaning or LookupCode and fill EventTypeCode from LookupCode. If both are supplied, they must resolve to the same one record. | A processes child row is supplied | resolve_rfid_process_event_type |
| Process Type resolution | Accept an exact Process Type meaning or LookupCode and fill ProcessTypeCode from LookupCode. If both are supplied, they must resolve to the same one record. | A processes child row is supplied | resolve_rfid_process_type |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RFID.VALIDATE_INPUT | decision | 2 | validate_input | valid->RFID.PREFLIGHT_BOS;invalid->RFID.HANDLE_ERROR | RFID.DEFAULT_DEVICE_ENABLED_FLAG | stop | Validate the approved Device Type, Status, Event Type, and Process Type input representations before Data Loader handoff |
