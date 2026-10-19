# Manage Import Maps Design Enforcement

## Source Evidence

| Source ID | Source | Used For |
|---|---|---|
| Developer-provided Manage Import Maps REST transformation requirements (2026-09-28) | REST-only transformation support and validation contract | Destination-child nesting, importMapFunctions validation, advisory syntax guidance, ReturnAttributeName construction, and SourceColumns construction. |
| git:9ec180c7496534f635941ca84b62f0625a4a6352 (2026-09-25) | Developer-approved LanguageCode remediation | Exact non-null LanguageCode preservation for destination children. |
| git:0ed0568d9a8e506c826d134dfb7607bc906939a2 (2026-09-25) | Developer-approved FSM import-route remediation | Unchanged expression preservation and stable-code destination checks on the FSM route. |

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 0 | Select import route | Run MIM.SELECT_IMPORT_ROUTE before route-specific validation; require an explicit REST Data Loader or FSM task-level ZIP route |
| 1 | Validate REST input structure | On the REST route, validate parent, source, destination, and transformation nesting; return MISSING when a transformation has no destination mapping |
| 2 | Apply create-only defaults | Default missing, null, or whitespace-only REST create fields; preserve explicit create values and omitted update values |
| 3 | Resolve missing ItemClassName | Only when the REST request is a create and ItemClassName is absent, null, or whitespace-only, derive it from the exact cached or freshly-read ROOT_ICC item-class response |
| 4 | Resolve standard lookup values | Use the named standard lookup type for every supplied or defaulted REST display value that lacks a code |
| 5 | Resolve destination metadata | Derive destination payload values and any non-null LanguageCode from one exact cached or freshly-read importMapAttributes item |
| 6 | Validate transformation functions | For each supplied REST transformation, validate the parsed ExpressionCode function through importMapFunctions; syntax differences produce FunctionSyntax and Examples advisories and do not block |
| 7 | Resolve transformation return attributes | Build ReturnAttributeName from the exact parent destination identity and append LanguageCode only when non-null |
| 8 | Derive transformation source columns | Build SourceColumns from the current source and all participating sources in supplied order, including the current source again in the suffix |
| 9 | Normalize source IgnoreFlag | Set IgnoreFlag to Y for source-only rows and N for mapped source rows |
| 10 | Gate Data Loader preview | Continue only with exact required lookup results and completed derivations; disclose but do not block for a FunctionSyntax advisory |
| 11 | Gate FSM return to Data Loader | On the FSM route, preserve the immutable ZIP and its expressions, report exact, unmatched, and DUMMY_TABLE-skipped destination rows, and return readiness to core.data-loader only when archive input is valid and no eligible destination row has multiple exact matches |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| At MIM.ENFORCE_LOOKUP_RESULTS: Delimiter is supplied or defaulted only as a display or input value on the REST route | Blocking | resolve_import_map_delimiter | The value has not resolved to exactly one LookupCode from ORA_EGI_IMP_MAP_DELIMITER | Run the required Standard lookup and map only its exact LookupCode | Yes |
| At MIM.ENFORCE_LOOKUP_RESULTS: FileType is supplied or defaulted only as a display or input value on the REST route | Blocking | resolve_import_map_file_type | The value has not resolved to exactly one LookupCode from ORA_EGI_IMP_MAP_FILE_TYPE | Run the required Standard lookup and map only its exact LookupCode | Yes |
| At MIM.ENFORCE_LOOKUP_RESULTS: DateFormat is supplied or defaulted only as a display or input value on the REST route | Blocking | resolve_import_map_date_format | The value has not resolved to exactly one LookupCode from DATE_FORMAT | Run the required Standard lookup and map only its exact LookupCode | Yes |
| At MIM.ENFORCE_LOOKUP_RESULTS: EncodingType is supplied or defaulted only as a display or input value on the REST route | Blocking | resolve_import_map_encoding_type | The value has not resolved to exactly one LookupCode from EGI_ENCODING_TYPE | Run the required Standard lookup and map only its exact LookupCode | Yes |
| At MIM.ENFORCE_LOOKUP_RESULTS: TimestampFormat is supplied or defaulted only as a display or input value on the REST route | Blocking | resolve_import_map_timestamp_format | The value has not resolved to exactly one LookupCode from EGI_TIME_STAMP | Run the required Standard lookup and map only its exact LookupCode | Yes |
| At MIM.ENFORCE_LOOKUP_RESULTS: the REST request is a create and ItemClassName is absent, null, or whitespace-only | Blocking | resolve_root_item_class | ItemClassName has not been filled from exactly one current ROOT_ICC item-class response with a nonblank ItemClass | GET or reuse the matching ROOT_ICC item-class response and map only ItemClass into ItemClassName | Yes |
| At MIM.ENFORCE_LOOKUP_RESULTS: A REST destination mapping is requested | Blocking |  | Its corresponding SourceColumn is missing | Supply the corresponding SourceColumn; do not submit a destination-only mapping | Yes |
| Before REST lookups: A transformation or expression is supplied without a destination mapping | Blocking |  | The transformation cannot be placed beneath a destination resource | Return MISSING and ask for the destination mapping; do not drop or sanitize the transformation | No |
| At MIM.ENFORCE_LOOKUP_RESULTS: A REST destination mapping is requested | Blocking | resolve_import_map_destination_attributes | Required destination values and any non-null LanguageCode do not come from one exact current importMapAttributes item | Re-resolve the destination from one matched item | Yes |
| At MIM.ENFORCE_LOOKUP_RESULTS: A REST transformation child is supplied | Blocking | resolve_import_map_transformation_function | ExpressionCode is blank, its parsed candidate matches no FunctionName exactly, or more than one exact match exists | Supply an ExpressionCode whose parsed function matches one current FunctionName; use the ordered REST-backed suggestions when available | Yes |
| At MIM.ENFORCE_LOOKUP_RESULTS: A REST transformation function resolves but ExpressionCode differs from FunctionSyntax after outer trimming | Advisory | resolve_import_map_transformation_function | None | Preserve ExpressionCode, show the authoritative FunctionSyntax and Examples, and continue to preview | No |
| At MIM.ENFORCE_LOOKUP_RESULTS: A REST transformation child is supplied | Blocking | resolve_import_map_transformation_return_attribute | ReturnAttributeName does not equal the exact parent destination's EntityName.AttributeGroupName.AttributeCode value with .LanguageCode appended only when LanguageCode is non-null | Replace ReturnAttributeName with the resolver output from the exact parent destination item | Yes |
| At MIM.ENFORCE_LOOKUP_RESULTS: A REST transformation destination has null LanguageCode | Blocking | resolve_import_map_transformation_return_attribute | ReturnAttributeName has a trailing separator or a fourth language component | Use exactly the three non-language destination components | Yes |
| At MIM.ENFORCE_LOOKUP_RESULTS: A REST transformation child is supplied | Blocking |  | SourceColumns does not equal current SourceColumn + $!$ + all participating source-column names joined by $&#124;$ in supplied order, including the current source again | Rebuild SourceColumns from the current REST request | Yes |
| At MIM.ENFORCE_LOOKUP_RESULTS: No REST transformation or expression is supplied | Blocking |  | A transformation child or transformation-only attribute was synthesized | Omit the unrequested transformation data | Yes |
| At MIM.ENFORCE_LOOKUP_RESULTS: A source child is prepared on the REST route | Blocking |  | IgnoreFlag does not equal N for a mapped source child or Y for a source-only child | Normalize the source payload from destination-child presence | Yes |
| At MIM.ENFORCE_LOOKUP_RESULTS: A lookup returns zero or multiple exact matches | Blocking |  | A required target value remains missing or ambiguous | Request a valid unambiguous input value; do not select the first result | Yes |
| At MIM.ENFORCE_LOOKUP_RESULTS: A previously previewed source value, lookup result, or derived transformation value changes | Blocking |  | The Data Loader preview and approval no longer describe the current source | Revalidate, rebuild the immutable archive, and obtain fresh approval | Yes |
| On the FSM task-level ZIP route | Blocking |  | REST transformation validation is invoked, expression data is removed or rewritten, or a different archive is handed off | Preserve the original immutable ZIP, including all transformation and expression records, for Fusion FSM semantic validation | No |
| At MIM.CHECK_FSM_READINESS: an FSM destination row's unchanged DestinationTable contains the exact case-sensitive substring DUMMY_TABLE | Advisory | validate_fsm_destination_attributes | None | Record the unchanged row as not_applicable with the skip reason; do not invoke importMapAttributes, assign a match count, or produce an unmatched warning | No |
| At MIM.CHECK_FSM_READINESS: an FSM destination row has one exact four-field code match | Advisory | validate_fsm_destination_attributes | None | Record the row as exact in the validation result and preserve the ZIP unchanged | No |
| At MIM.CHECK_FSM_READINESS: an FSM destination row has zero exact four-field code matches | Advisory | validate_fsm_destination_attributes | None | Record the row as unmatched with a warning, preserve it unchanged, and allow return to the core.data-loader Task Hook workflow | No |
| At MIM.CHECK_FSM_READINESS: an FSM destination row has multiple exact four-field code matches | Blocking | validate_fsm_destination_attributes | More than one importMapAttributes item matches the unchanged four-field code key | Stop before upload and report the unchanged key and match count; never choose a result | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_import_map_delimiter | Delimiter is supplied or defaulted without an explicit LookupCode on the REST route | Delimiter LookupCode from ORA_EGI_IMP_MAP_DELIMITER | ora_reference_lookups.md |
| resolve_import_map_file_type | FileType is supplied or defaulted without an explicit LookupCode on the REST route | FileType LookupCode from ORA_EGI_IMP_MAP_FILE_TYPE | ora_reference_lookups.md |
| resolve_import_map_date_format | DateFormat is supplied or defaulted without an explicit LookupCode on the REST route | DateFormat LookupCode from DATE_FORMAT | ora_reference_lookups.md |
| resolve_import_map_encoding_type | EncodingType is supplied or defaulted without an explicit LookupCode on the REST route | EncodingType LookupCode from EGI_ENCODING_TYPE | ora_reference_lookups.md |
| resolve_import_map_timestamp_format | TimestampFormat is supplied or defaulted without an explicit LookupCode on the REST route | TimestampFormat LookupCode from EGI_TIME_STAMP | ora_reference_lookups.md |
| resolve_root_item_class | The REST request is a create and ItemClassName is absent, null, or whitespace-only | ItemClassName from ItemClass in one exact ROOT_ICC item-class response | ora_reference_lookups.md |
| resolve_import_map_destination_attributes | A REST destination mapping is requested | Destination payload values and non-null LanguageCode from one exact current importMapAttributes item | ora_reference_lookups.md |
| resolve_import_map_transformation_function | A REST transformation child is supplied | Exact FunctionName validation and FunctionSyntax plus Examples advisory values | ora_reference_lookups.md |
| resolve_import_map_transformation_return_attribute | A REST transformation child is supplied beneath a resolved destination | ReturnAttributeName from the exact parent destination identity | ora_reference_lookups.md |
| validate_fsm_destination_attributes | The FSM ZIP contains a row with DestinationColumn; apply the documented DUMMY_TABLE eligibility check before any REST matching | DUMMY_TABLE skip reason for excluded rows or exact comparison of the unchanged four-field code key for eligible rows | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MIM.ENFORCE_LOOKUP_RESULTS | decision | 100 | design_enforcement | allowed->MIM.DONE;blocked->MIM.HANDLE_ISSUE | MIM.CHECK_LOOKUP_READINESS | stop | After REST validation, lookups, transformation derivations, and source normalization; disclose syntax advisories and block unresolved required values before Data Loader handoff and preview |
