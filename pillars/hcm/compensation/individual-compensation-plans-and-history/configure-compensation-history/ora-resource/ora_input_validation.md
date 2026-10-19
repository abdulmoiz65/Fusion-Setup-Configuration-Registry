# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Registered Compensation History business object | BusinessObject: compensationHistoryElements | Stop | Resolve the exact registered business object; do not substitute a similarly named object | Every request | resolve_compensation_history_business_object |
| Current Compensation History field contract | One or more supplied fields present in the current compensationHistoryElements template and attribute metadata | Stop | Read the current schema and submit only fields whose names and values conform to it | A validation, preview, import, create, or update request supplies configuration values | read_compensation_history_elements_schema |
| New-record mandatory fields | CmpHistoryId, CreationDate, and RestAction when the current schema retains their mandatory status for the selected operation | Stop | Supply the missing value in the source data; do not infer an identifier, date, or action | A new Compensation History element record is being prepared | read_compensation_history_elements_schema |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The registered business object has not resolved | Blocked | Stop before preview or import preparation | resolve_compensation_history_business_object |
| The current schema has not been read | Blocked | Stop before preview or import preparation | read_compensation_history_elements_schema |
| A supplied field is absent from the current schema or violates its data type, length, mandatory, lookup, or reference contract | Blocked | Correct the source data and revalidate | read_compensation_history_elements_schema |
| Every supplied field conforms to the current schema | Continue | Continue only through the task's established export/import workflow | read_compensation_history_elements_schema |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Exact field identity | Accept only fields returned by the current compensationHistoryElements template and attribute metadata | Every supplied value | read_compensation_history_elements_schema |
| Field shape | Validate supplied values against current data type, data length, mandatory status, lookup, and reference metadata | Every supplied value | read_compensation_history_elements_schema |
| Element and input value fields | Validate ElementName, LDGName, InputValue, ElementTypeId, and InputValueId only when they are present in the current schema | The request supplies any of these fields | read_compensation_history_elements_schema |
| History classification fields | Validate ReportingName, ProcessingType, Country, and HistoryCategory only when they are present in the current schema | The request supplies any of these fields | read_compensation_history_elements_schema |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCH.VALIDATE_INPUT | step | 30 | validate_input | valid->CCH.COMPLETE;invalid->CCH.HANDLE_ISSUE | CCH.READ_SCHEMA | stop | After the registered business object and current schema resolve |
