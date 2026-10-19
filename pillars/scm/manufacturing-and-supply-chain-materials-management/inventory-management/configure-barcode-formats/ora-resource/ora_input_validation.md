# Configure Barcode Formats Input Validation

## Source Evidence

| Source | Used For |
|---|---|
| Redwood Barcode Formats child layout module | Client-side DateFormat syntax and blank-value behavior |
| Redwood Barcode Formats create and batch payload modules | Status is emitted as Y or N; switch-backed REST fields are emitted as native booleans |
| Configure Barcode Formats FSM export | Status and all corresponding switch fields use Y or N in CSV routes |
| User-approved scope | Required and conditional field validation remains owned by BO metadata, Data Loader, and Fusion |

## Scope Boundary

| Boundary | What Happens |
|---|---|
| BO metadata and Data Loader validation | Required fields, conditional fields, lengths, uniqueness, domains, and final record validation remain runtime-owned. |
| Local validation | Validate the sourced client-side DateFormat syntax and the approved code-or-meaning input contracts before Data Loader handoff. |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| DateFormat client syntax | Preserve a blank value. For a supplied value, compare case-insensitively and accept only dd, mm, mon, yyyy, yy, hh, and jjj tokens. Tokens may be concatenated; when separators are used, allow only slash or hyphen. Reject all other syntax. | A child DataIdentifierConfigurations DateFormat value is supplied |  |
| Field Code or Field Name representation | Accept a supplied FieldCode or FieldName only after it resolves to exactly one returned lookup row; normalize the resolved value to LookupCode in FieldCode for REST/Data Loader and FSM handoff. | A FieldCode or FieldName value is supplied | resolve_barcode_field_name |
| Data Length Type representation | Accept a supplied DataLengthType or DataLengthTypeName only after it resolves to exactly one returned lookup row; normalize the resolved value to LookupCode in DataLengthType for REST/Data Loader and FSM handoff. | A DataLengthType or DataLengthTypeName value is supplied | resolve_barcode_data_length_type |
| Data Type representation | Accept a supplied DataType or DataTypeName only after it resolves to exactly one returned lookup row; normalize the resolved value to LookupCode in DataType for REST/Data Loader and FSM handoff. | A DataType or DataTypeName value is supplied | resolve_barcode_data_type |
| Conflicting lookup representations | When code and meaning are both supplied for FieldCode and FieldName, DataLengthType and DataLengthTypeName, or DataType and DataTypeName, require both representations to resolve to the same lookup row. | Both representations are supplied for a selected lookup field |  |

## Route-Aware Switch And Status Normalization

Trim and compare every string representation case-insensitively. A native Boolean is equivalent to its `true` or `false` representation. Preserve an omitted field for approved defaulting or runtime-owned validation; do not infer a value for an unsupported representation.

| Field | Accepted Enabled Representations | Accepted Disabled Representations | REST/Data Loader Canonical Output | FSM Canonical Output | Applies When |
|---|---|---|---|---|---|
| Status | `true`, `yes`, `y`, `active` | `false`, `no`, `n`, `inactive` | `Y` when enabled; `N` when disabled | `Y` when enabled; `N` when disabled | Status is supplied for a barcode-format header |
| RetainPrefixFlag | `true`, `yes`, `y` | `false`, `no`, `n` | Boolean `true` when enabled; `false` when disabled | `Y` when enabled; `N` when disabled in RetainPrefixFlag | RetainPrefixFlag is supplied for a barcode-format header |
| IncludesCheckDigitFlag | `true`, `yes`, `y` | `false`, `no`, `n` | Boolean `true` when enabled; `false` when disabled in IncludesCheckDigitFlag | `Y` when enabled; `N` when disabled in IncludesCheckDigit | IncludesCheckDigitFlag is supplied for a barcode-format header |
| GroupSeparatorFlag | `true`, `yes`, `y` | `false`, `no`, `n` | Boolean `true` when enabled; `false` when disabled | `Y` when enabled; `N` when disabled in GroupSeparatorFlag | GroupSeparatorFlag is supplied for a child data-identifier row |
| MultiDataElementFlag | `true`, `yes`, `y` | `false`, `no`, `n` | Boolean `true` when enabled; `false` when disabled | `Y` when enabled; `N` when disabled in MultiDataElement | MultiDataElementFlag is supplied for a child data-identifier row |
| RetainDataIdentifierFlag | `true`, `yes`, `y` | `false`, `no`, `n` | Boolean `true` when enabled; `false` when disabled | `Y` when enabled; `N` when disabled in RetainDataIdentifier | RetainDataIdentifierFlag is supplied for a child data-identifier row |
| RetainDelimiterFlag | `true`, `yes`, `y` | `false`, `no`, `n` | Boolean `true` when enabled; `false` when disabled | `Y` when enabled; `N` when disabled in RetainDelimiter | RetainDelimiterFlag is supplied for a child data-identifier row |

| Normalization Rule | What Happens |
|---|---|
| Status canonical value | Normalize enabled representations to `Y` and disabled representations to `N` for both REST/Data Loader and FSM routes. |
| Switch canonical value | Normalize enabled and disabled representations to Boolean `true` and `false` for REST/Data Loader. For FSM generation, emit `Y` and `N` in the corresponding FSM column named above. |
| Unsupported representation | Stop before Data Loader handoff; do not coerce arbitrary text or defer the failure to BO metadata. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BCF.VALIDATE_DATE_FORMAT | step | 10 | validate_input | valid->BCF.NORMALIZE_BOOLEAN_FIELDS;invalid->BCF.HANDLE_ERROR | none | stop | Before normalization, defaulting, selected lookup resolution, or Data Loader preparation |
| BCF.NORMALIZE_BOOLEAN_FIELDS | step | 15 | evaluate_result | normalized->BCF.CHECK_READINESS;skipped->BCF.CHECK_READINESS;invalid->BCF.HANDLE_ERROR | BCF.VALIDATE_DATE_FORMAT | stop | A supplied Status or supported switch-backed field requires route-aware normalization before defaulting or Data Loader preparation |
