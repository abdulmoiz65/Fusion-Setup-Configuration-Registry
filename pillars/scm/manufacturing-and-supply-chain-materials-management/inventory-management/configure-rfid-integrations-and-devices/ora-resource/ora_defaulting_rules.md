# RFID Integrations and Devices Defaulting Rules

## Default Rules

| Field | Default Value | Apply When | Override Behavior | Applies When | Source Evidence |
|---|---|---|---|---|---|
| Device EnabledFlag | Boolean false | A device-create record omits both EnabledFlag and Status | Preserve any explicit EnabledFlag Boolean or Status value; normalize the supplied value through Device Status normalization instead of applying the default. Do not default an update record. | Device create Data Loader preparation only | User-approved task rule. The Redwood device-create UI model defaults EnabledFlag to false. |
| Processes UnmapTagFlag | Boolean false | A processes child-create row omits UnmapTagFlag | Preserve an explicit UnmapTagFlag Boolean value. Do not default an update row. | Processes child create Data Loader preparation only | User-approved task rule. |

## Defaulting Rules

| Situation | What Happens |
|---|---|
| A device-create record omits both EnabledFlag and Status | Set EnabledFlag to Boolean false before input validation and Data Loader preparation. |
| A device record supplies EnabledFlag or Status | Do not replace the supplied value; continue with Device Status normalization. |
| A device-update record omits EnabledFlag and Status | Do not apply a default; preserve the omission for update handling. |
| A processes child-create row omits UnmapTagFlag | Set UnmapTagFlag to Boolean false before Data Loader preparation. |
| A processes child row supplies UnmapTagFlag | Do not replace the supplied Boolean value. |
| A processes child-update row omits UnmapTagFlag | Do not apply a default; preserve the omission for update handling. |
| An integration record or processes child row omits its status | Do not apply this device-only default; its required-status rule remains in force. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RFID.DEFAULT_DEVICE_ENABLED_FLAG | decision | 1 | apply_default | defaulted->RFID.VALIDATE_INPUT;preserved->RFID.VALIDATE_INPUT;failed->RFID.HANDLE_ERROR | none | stop | Apply Boolean false only for create records when a device omits both EnabledFlag and Status or a processes child row omits UnmapTagFlag; preserve explicit values, update omissions, and non-applicable records |
