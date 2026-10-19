# Time Allocations Input Validation

## Source Basis

- User-authorized Time Consumer Sets timeCategoriesLOV pattern with verified TcatCd mapping for Time Allocations, 5 October 2026.

- User-provided Generic FSM Baseline, received 5 October 2026.
- User-requested correction separating fresh-export discovery from import readiness, 5 October 2026.
- Developer-provided Time Allocation UI Skeleton.
- User-provided verified Time Attribute field lookup contract, received 5 October 2026.
- User-provided verified Time Attribute data-source and value validation contract, received 5 October 2026.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Allocation identity | Allocation Name | Block | For Create, provide the new Allocation Name; for Edit, provide the existing Allocation Name to identify the target. Edit restrictions are enforced in ora_design_enforcement.md | Always | |
| Effective period | Effective Start Date; Effective End Date | Block | Use the displayed fixed end date and provide or accept the start-date default | Create or edit | |
| Source allocation row | Processing Sequence; Allocation Type | Block | Add a row and choose an Allocation Type | Each Source row | |
| Hours allocation detail | Summation Level | Block | Choose Time Card or Day | Allocation Type is Hours | |
| Output row | Processing Sequence | Block | Add an Output-table row | Each Output row | |
| Hours output row | Hours | Block | Add a positive Hours value | Allocation Type is Hours | |
| Percentage output row | Percentage | Block | Add a Percentage value | Allocation Type is Percentage | |
| Time Attribute definition | Attribute Display Sequence; Time Attribute | Block | Provide a positive display sequence and select a Time Attribute | Adding a Time Attribute | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation is not Create or Edit | Reject the unsupported operation | Catalog-routed FSM CSV request | |
| Allocation Name is blank | Reject the request | Always | |
| Effective Start Date is blank | Apply the documented current-date default before preview | A user does not supply a start date | |
| Effective End Date is edited or differs from 12/31/4712 | Reject the change; it is read-only | Always | |
| Source Processing Sequence is blank | Default it from the Source-table row number | A Source row is added | |
| Processing Sequence duplicates another row in the same table | Reject the duplicate; Processing Sequence must be unique within each table | A Source or Output-table row is added or edited | |
| Allocation Type is not Equally, Percentage, or Hours | Reject the value | A Source row is added or edited | |
| Summation Level is supplied when Allocation Type is not Hours | Clear the value and disable the field | Allocation Type is Equally or Percentage | |
| Summation Level is blank or not Time Card or Day | Reject the row | Allocation Type is Hours | |
| Hours Processing Sequence is blank | Default it from the hours-table row number | A hours row is added | |
| Hours is not greater than 0 | Reject the row | A hours row is added or edited | |
| Percentage is blank | Reject the Output row | Allocation Type is Percentage | |
| Percentage is not a decimal number greater than 0 | Reject the Output row | Allocation Type is Percentage | |
| Percentage total is not 100 | Reject the Output-table rows | Allocation Type is Percentage | |
| Attribute Display Sequence is not greater than 0 | Reject the attribute definition | Adding a Time Attribute | |
| Time Attribute is blank | Reject the attribute definition | Adding a Time Attribute | |
| A source row supplies a Time Category | Require the verified category name and nonblank category code from resolve_time_category before preparing that row | A source allocation row supplies a Time Category | resolve_time_category |
| A Time Attribute is selected | Require one resolved Time Attribute returned by the documented full-list or search lookup | Adding a Time Attribute | resolve_time_attribute_field |
| A FORMAT_VALUE_SET Time Attribute column has a value | Validate the supplied value against AttributeType and every applicable non-null constraint returned by the data source: Precision, Scale, MinimumValue, MinimumValueNumber, MinimumValueDate, MinimumValueTimestamp, MaximumValue, MaximumValueNumber, MaximumValueDate, and MaximumValueTimestamp. Reject a value that cannot be interpreted as the returned AttributeType or violates a returned constraint. Identify the expected AttributeType and each violated constraint, then suggest a compliant form based only on the returned metadata. | A Time Attribute column is populated and ImplementationType is FORMAT_VALUE_SET | resolve_time_attribute_data_source |
| A selectable Time Attribute column has a value | Require one ValuesList row selected by Code. Preserve duplicate Value labels as separate choices. If the search returns multiple rows, show Code, Value, ValueChar, ValueDate, and ValueNumber for every match and ask the user to select the value to use. | A Time Attribute column is populated and ImplementationType is DEPENDENT_VALUE_SET, INDEPENDENT_VALUE_SET, TABLE_VALUE_SET, or VIEW_OBJECT | find_time_attribute_value |
| A selected Time Attribute has a blank or unsupported ImplementationType | Reject the value contract and stop before preview; do not infer how the value must be entered or resolved | A Time Attribute is selected | resolve_time_attribute_data_source |

## FSM Validation Stages

Business-input validation uses the field rules above, the existing defaults,
and the documented Time Attribute field, data-source, and value lookups. Do
not replace those contracts with blanket missing-dependency or missing-LOV
requirements.

The fresh same-task export is obtained after business validation through the
invoking workflow. CSV member names, headers, field mappings, and key or
relationship evidence are inspected at that stage, not requested as business
inputs before export. Export evidence must support the proposed mapping;
unknown semantics must not be inferred from labels alone.

Package and reconciliation evidence is checked before the Data Loader
handoff under ora_design_enforcement.md. A successful business-validation
result does not mean that an import package is ready.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TAL.VALIDATE_INPUT | decision | 10 | validate_input | valid->TAL.RESOLVE_TIME_CATEGORY;missing_or_invalid->TAL.HANDLE_INPUT_ISSUE | none | stop | A Time Allocations create or edit request is prepared |
| TAL.VALIDATE_TIME_ATTRIBUTE_VALUE | decision | 18 | evaluate_result | valid->TAL.APPLY_DEFAULTS;not_applicable->TAL.APPLY_DEFAULTS;missing_or_invalid->TAL.HANDLE_INPUT_ISSUE | TAL.RESOLVE_TIME_ATTRIBUTE_VALUE | stop | A selected Time Attribute data source has been resolved and any supplied value must be validated according to ImplementationType |
