# Inventory Zones Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_inventory_zone_status | A status code or meaning is supplied. | StatusCode, StatusMeaning | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?finder=LookupTypeFinder;LookupType=ORA_INV_ZONE_STATUS&onlyData=true&fields=LookupCode,Meaning | LookupCode, Meaning | Trim whitespace and compare code and meaning case-insensitively for an exact match. When both are supplied, each must identify the same single row. | StatusCode: LookupCode | Block handoff and request a valid unambiguous status. |
| resolve_inventory_zone_activity_type | An activity type code or meaning is supplied. | FSM Activity Usages CSV: ActivityTypeCode as Meaning; REST/Data Loader: ActivityTypeCode, ActivityTypeMeaning | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?finder=LookupTypeFinder;LookupType=ORA_INV_ZONE_ACTIVITY_TYPES&onlyData=true&fields=LookupCode,Meaning | LookupCode, Meaning | Trim whitespace and compare code and meaning case-insensitively for an exact match. When both are supplied, each must identify the same single row. | REST/Data Loader ActivityTypeCode: LookupCode; FSM ActivityTypeCode: Meaning | Block handoff and request a valid unambiguous activity type. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A user supplies a backend code | Validate the code through its named resolver before Data Loader handoff. |
| A user supplies a display meaning | Resolve it through its named resolver and retain the returned code. |
| A user supplies code and meaning | Resolve both and block when they identify different rows. |
| An FSM Activity Usages CSV is prepared for REST/Data Loader | Treat FSM ActivityTypeCode as Meaning, resolve it, and write LookupCode to REST/Data Loader ActivityTypeCode. |
| REST/Data Loader data is prepared for FSM | Resolve the REST LookupCode when needed and write Meaning to FSM ActivityTypeCode. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| INV-ZONES.RESOLVE-STATUS | decision | 20 | reference_lookup | resolved->INV-ZONES.RESOLVE-ACTIVITY-TYPE;not_applicable->INV-ZONES.RESOLVE-ACTIVITY-TYPE;blocked->INV-ZONES.RETURN-ISSUES | INV-ZONES.VALIDATE-LOV-INPUTS | stop | A zone status code or meaning is supplied. |
| INV-ZONES.RESOLVE-ACTIVITY-TYPE | decision | 30 | reference_lookup | resolved->INV-ZONES.APPLY-START-DATE-DEFAULT;not_applicable->INV-ZONES.APPLY-START-DATE-DEFAULT;blocked->INV-ZONES.RETURN-ISSUES | INV-ZONES.RESOLVE-STATUS | stop | An activity type code or meaning is supplied. |
