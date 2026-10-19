# Configure Barcode Formats Reference Lookups

## Source Evidence

| Source | Used For |
|---|---|
| Redwood Barcode Formats page and child dynamic layout | Lookup types, Meaning display key, implementation fields, and VBC service use |
| Redwood service catalog | Fusion REST base path and REST-Framework-Version 9 service configuration |
| User-approved resolver contracts | Read-only resolver scope, exact-match behavior, and canonical LookupCode mapping for REST/Data Loader and FSM routes |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_barcode_field_name | A child FieldCode code or FieldName meaning is supplied | Supplied LookupCode or Meaning for FieldCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?fields=LookupCode,Meaning&onlyData=true&q=LookupType='ORA_INV_BARCODE_FIELDS' | LookupCode, Meaning | Trim each supplied representation and compare case-insensitively and exactly against both LookupCode and Meaning. When code and meaning are both supplied, both must resolve to one row. | FieldCode: LookupCode; retain returned LookupCode and Meaning as validation evidence | Stop on no match, ambiguity, or representations resolving to different rows. |
| resolve_barcode_data_length_type | A child DataLengthType code or DataLengthTypeName meaning is supplied | Supplied LookupCode or Meaning for DataLengthType | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?fields=LookupCode,Meaning&onlyData=true&q=LookupType='ORA_INV_BARCODE_FIELD_LEN_TYPE' | LookupCode, Meaning | Trim each supplied representation and compare case-insensitively and exactly against both LookupCode and Meaning. When code and meaning are both supplied, both must resolve to one row. | DataLengthType: LookupCode; retain returned LookupCode and Meaning as validation evidence | Stop on no match, ambiguity, or representations resolving to different rows. |
| resolve_barcode_data_type | A child DataType code or DataTypeName meaning is supplied | Supplied LookupCode or Meaning for DataType | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?fields=LookupCode,Meaning&onlyData=true&q=LookupType='ORA_INV_BARCODE_FLD_DATA_TYPE' | LookupCode, Meaning | Trim each supplied representation and compare case-insensitively and exactly against both LookupCode and Meaning. When code and meaning are both supplied, both must resolve to one row. | DataType: LookupCode; retain returned LookupCode and Meaning as validation evidence | Stop on no match, ambiguity, or representations resolving to different rows. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A selected child LOV field has a supplied code or meaning | Run only its documented resolver; do not trust a supplied code without validation and do not fuzzy-match, contains-match, guess, or select the first candidate. |
| Lookup returns one exact row | Preserve the canonical LookupCode in FieldCode, DataLengthType, or DataType for REST/Data Loader and FSM handoff; retain returned LookupCode and Meaning as validation evidence. |
| Code and meaning are both supplied | Accept them only when both representations match the same returned row. |
| Lookup returns no or multiple exact rows | Stop and request a valid, unambiguous LookupCode or Meaning. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BCF.RESOLVE_FIELD_NAME | step | 40 | reference_lookup | resolved->BCF.RESOLVE_DATA_LENGTH_TYPE;skipped->BCF.RESOLVE_DATA_LENGTH_TYPE;blocked->BCF.HANDLE_ERROR | BCF.APPLY_DEFAULTS | stop | A FieldCode code or FieldName meaning is supplied |
| BCF.RESOLVE_DATA_LENGTH_TYPE | step | 50 | reference_lookup | resolved->BCF.RESOLVE_DATA_TYPE;skipped->BCF.RESOLVE_DATA_TYPE;blocked->BCF.HANDLE_ERROR | BCF.RESOLVE_FIELD_NAME | stop | A DataLengthType code or DataLengthTypeName meaning is supplied |
| BCF.RESOLVE_DATA_TYPE | step | 60 | reference_lookup | resolved->BCF.DATA_LOADER_HANDOFF;skipped->BCF.DATA_LOADER_HANDOFF;blocked->BCF.HANDLE_ERROR | BCF.RESOLVE_DATA_LENGTH_TYPE | stop | A DataType code or DataTypeName meaning is supplied |
