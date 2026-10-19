# RFID Integrations and Devices Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_rfid_device_type | Integration or Device Type is supplied as a display value or code | RFID Surface Read Point, RFID_SURFACE_READER, RFID Cabinet, RFID_Cabinet | Trim and compare case-insensitively for exact display or exact code. RFID Surface Read Point maps to RFID_SURFACE_READER; RFID Cabinet maps to RFID_Cabinet. | DeviceTypeCode: mapped code | Stop on no match, ambiguity, or conflicting display and code values. Do not fuzzy match. |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_rfid_process_event_type | A processes child row supplies Event Type meaning, code, or both | Event Type meaning, EventTypeCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?finder=LookupTypeFinder;LookupType=ORA_INV_RFID_EVENT_TYPES&onlyData=true&q=Meaning!='List' | LookupCode, Meaning, LookupType, Description | Trim and compare case-insensitively for exact Meaning or LookupCode. When both are supplied, both must identify the same single row. | EventTypeCode: LookupCode | Stop on no match, multiple matches, or conflicting code and meaning. Do not use List. |
| resolve_rfid_process_type | A processes child row supplies Process Type meaning, code, or both | Process Type meaning, ProcessTypeCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?finder=LookupTypeFinder;LookupType=ORA_INV_RFID_PROCESS_TYPES&onlyData=true | LookupCode, Meaning, LookupType, Description | Trim and compare case-insensitively for exact Meaning or LookupCode. When both are supplied, both must identify the same single row. | ProcessTypeCode: LookupCode | Stop on no match, multiple matches, or conflicting code and meaning. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A directly supplied Device Type code is used | Validate it through resolve_rfid_device_type before Data Loader handoff. |
| A directly supplied Event Type or Process Type code is used | Validate it through its named standard lookup resolver before Data Loader handoff. |
| A standard lookup call fails or returns malformed data | Stop with a Fusion API or transport/environment diagnostic; do not substitute a browser, direct REST write, or guessed value. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RFID.RESOLVE_DEVICE_TYPE | decision | 4 | reference_lookup | resolved->RFID.RESOLVE_EVENT_TYPE;no_processes->RFID.COMPLETE_PARENT;failed->RFID.HANDLE_ERROR | RFID.PREFLIGHT_BOS | stop | Resolve Device Type with resolve_rfid_device_type and continue to process resolution only when a processes child row is supplied |
| RFID.RESOLVE_EVENT_TYPE | decision | 5 | reference_lookup | resolved->RFID.RESOLVE_PROCESS_TYPE;failed->RFID.HANDLE_ERROR | RFID.RESOLVE_DEVICE_TYPE | stop | Resolve the Event Type for each supplied processes child row through resolve_rfid_process_event_type |
| RFID.RESOLVE_PROCESS_TYPE | decision | 6 | reference_lookup | resolved->RFID.COMPLETE_PROCESS;failed->RFID.HANDLE_ERROR | RFID.RESOLVE_EVENT_TYPE | stop | Resolve the Process Type for each supplied processes child row through resolve_rfid_process_type |
