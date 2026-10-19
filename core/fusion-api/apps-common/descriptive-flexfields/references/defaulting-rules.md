# DFF Context and Attribute Defaulting Rules

In this reference, a DFF **attribute** and a DFF **segment** mean the same
configurable field. Field names such as `SegmentCode` retain the terminology
used by the import format.

Use these rules when preparing a DFF blueprint for a create or update request.
Apply a default only when the corresponding value is absent from the user's
request and cannot be preserved from an exact existing row for an update.
Preserve explicitly supplied field values, subject to the naming interpretation
below. Use the selected task's current export and metadata for storage columns
and sequence numbers; another DFF or an older
export is not a source of availability. Run
[mandatory validations](validations.md) on the resolved design and the final
candidate package before handing it to Data Loader.

## Global and context-sensitive segments

Interpret descriptive suffixes before deriving a new field's `Name`,
`SegmentCode`, and `SegmentIdentifier`. A standalone, trailing `Attribute` or
`Segment` identifies the kind of field, so `StartDate Attribute` and
`StartDate Segment` both resolve to `Name: StartDate`, `SegmentCode: StartDate`,
and `SegmentIdentifier: startDate`. A trailing type word such as `Number` may
also describe the Data Type rather than the name: `Age Number` resolves to
`Name: Age`, `SegmentCode: Age`, and `SegmentIdentifier: age`. Read the original
description for Data Type clues before removing a suffix. Remove only
descriptive words at the end, in that order when both occur; never remove a
word embedded in the meaningful name. For example, keep `Phone Number` when
`Number` is part of the field's meaning. If the intended name is unclear, or
the user explicitly requests a literal name containing the suffix, ask for
clarification rather than silently changing a supplied field value. Also ask
when separately supplied name and code values conflict. Preserve the exact
identity of an existing segment on update.

| Field | Default when omitted | Required evidence or stopping condition |
| --- | --- | --- |
| `SegmentCode` (Code) | Copy the resolved segment `Name` after applying the naming interpretation above. | If both name and code are absent, request one. Check the resulting code against the selected task's length, syntax, and uniqueness rules before using it. |
| `Name` | Copy the supplied `SegmentCode` after applying the naming interpretation above. | If both name and code are absent, request one. Do not rename an existing segment as a side effect of a different update. |
| `SegmentIdentifier` (API Name) | For a new attribute, derive lower camel case from the resolved `Name`: remove spaces, lowercase the initial letter of the first word, and uppercase the initial letter of each later word while preserving their remaining letters. For example, `StartDate` becomes `startDate` and `Age` becomes `age`; descriptive suffixes are not included. | Show the proposed API name for review. If punctuation, length, a reserved word, or a collision makes it invalid, stop and request an explicit API name; do not silently strip or truncate characters. Preserve an existing API name on update unless its change is explicitly supported and requested. |
| Data Type | First use the user's description: string, text, or alphanumeric means `Character`; numeric-only or number means `Number`; date alone means `Date`; and date together with time, date-time, or timestamp means `Date Time`. If no type is stated, infer it from `ValueSetCode`: `CHAR` or `CHARACTERS` means `Character`, `NUMBER` means `Number`, `DFF_DATE_TIME` or another clear `DATE_TIME`, `DATETIME`, or `TIMESTAMP` indicator means `Date Time`, and `DATE` alone means `Date`. If the value-set code gives no clear type, infer it from a user-supplied `ColumnName`: `ATTRIBUTE1`–`ATTRIBUTE30` means `Character`, `ATTRIBUTE_NUMBER1`–`ATTRIBUTE_NUMBER10` means `Number`, `ATTRIBUTE_DATE1`–`ATTRIBUTE_DATE5` means `Date`, and `ATTRIBUTE_TIMESTAMP1`–`ATTRIBUTE_TIMESTAMP5` means `Date Time`. | Check date-and-time wording and date-time value-set indicators before the date-only rule. Match a supplied column to one exact family and range; do not infer a type from a column outside those ranges. If the available type cues conflict, ask the user to correct the inputs instead of silently changing a supplied value. If no type can be resolved from the description, value set, or column, ask for the Data Type. A missing `ValueSetCode` still requires user input under its own rule. Data Type is a blueprint value, not necessarily a CSV header. |
| `ColumnName` (Table Column) | Select the column family for the resolved Data Type: Character uses `ATTRIBUTE1`–`ATTRIBUTE30` (30 columns), Number uses `ATTRIBUTE_NUMBER1`–`ATTRIBUTE_NUMBER10` (10 columns), Date uses `ATTRIBUTE_DATE1`–`ATTRIBUTE_DATE5` (5 columns), and Date Time uses `ATTRIBUTE_TIMESTAMP1`–`ATTRIBUTE_TIMESTAMP5` (5 columns). Within that family and the selected segment scope, find the highest numbered column already assigned to an existing or earlier proposed segment, then increment its number by one. If none is assigned, start at `1`. For example, if the last Character column is `ATTRIBUTE4`, assign `ATTRIBUTE5` to the next Character segment. | Read the current task-scoped export and registered columns; calculate the highest suffix numerically rather than from CSV row order. Include disabled and earlier proposed segments. For a global segment, consider global columns; for a context-sensitive segment, consider global columns and columns in its own context. Check any reuse across different contexts against the task contract. Confirm that the resulting column exists and is available in the selected table. If it exceeds `ATTRIBUTE30`, `ATTRIBUTE_NUMBER10`, `ATTRIBUTE_DATE5`, or `ATTRIBUTE_TIMESTAMP5`, or is otherwise unavailable, stop and request a column decision; do not wrap around, fill an earlier gap, invent a higher column, or reassign an existing segment silently. |
| `ValueSetCode` (Value Set) | No default. Keep the exact user-provided value-set code. | This field is required. If absent, ask the user for it and show `Pending user input` in the blueprint. |
| `Prompt` | Copy the resolved segment `Name`. | Show this default in the blueprint. Require a reviewed, nonblank prompt before package preparation. |
| `ShortPrompt` | Copy the resolved segment `Prompt` when `ShortPrompt` is absent. | Keep this default in the internal design and include it in the package only when the selected task format has a `ShortPrompt` field. Do not display `ShortPrompt` in the user-visible blueprint. |
| `DisplayType` | No default. Keep the exact user-provided display type. | Show `Pending user input` when absent. Validate it against the selected task format and the segment's data type. |
| `SequenceNumber` | In the selected scope, use the highest valid existing or already proposed sequence plus `10`. Use `10` when that scope has no segments. Global segments form one scope; each context-sensitive context forms its own scope. | Determine the maximum numerically, not from CSV row order. Include disabled rows and earlier proposed rows in the calculation, reject malformed sequence evidence, and recheck uniqueness before package preparation. |
| `MultirowUniqueKeyFlag` | Leave blank in every included context-sensitive segment row of the prepared ZIP when the task format declares this field. | Do not add the header to a member whose format omits it. If a multirow context requires a unique-key value, or an unrelated included row has a nonblank value, stop rather than changing it to force the blank default. |

For a context-sensitive segment, carry the exact resolved parent `ContextCode`
into the blueprint and the package. Apply these segment defaults separately
within each context. A value set or data type alone does not determine the
context or a storage column.

## DFF contexts

A DFF can have several context values, each with its own context-sensitive
segments. Apply these rules to a new context only after identifying the DFF
and application. Preserve exact existing context identities on an update.

| Field | Default when omitted | Required evidence or stopping condition |
| --- | --- | --- |
| `ContextCode` (Code) | Copy the resolved context `Name` exactly. | If both name and code are absent, request one. Validate the derived code against the selected task's length, syntax, and uniqueness rules. |
| `Name` (Display Name) | Copy the supplied `ContextCode` exactly. | If both name and code are absent, request one. Do not rename an existing context merely to fill another field. |
| `ContextIdentifier` (API Name) | For a new context, derive CamelCase from the resolved `Name`: remove spaces and uppercase the initial letter of each word while preserving the remaining letters. For example, `Home Address` becomes `HomeAddress`. | Show the proposed API name for review. Stop for invalid characters, excessive length, reserved words, or collisions; do not silently alter the generated name. Preserve an existing API name on update unless its change is explicitly supported and requested. |

## User-visible blueprint and handoff

Before package preparation, show one row per context and segment with the
resolved field values other than `ShortPrompt`. Always include the resolved
`ColumnName` (Table Column) for each segment, or mark it `Pending resolution`
with the reason when it cannot yet be assigned. Label each displayed value
`User supplied`, `Preserved from current export`, `Defaulted`,
`Pending resolution`, or `Pending user input`; for a default, state its source
rule and the evidence used for column and sequence selection. For Data Type
inferred from a value-set code or column name, show that value as the source of
the default. Include the DFF and application identity, parent context, the
selected task, and the target environment. Show `MultirowUniqueKeyFlag` as
blank when applicable. Display
the same resolved values in the calling project's DFF blueprint, then present
the blueprint to the user. A pending field, invalid API name, unavailable
column, or failed validation blocks the import ZIP; do not
fill it with a guess or treat displaying the blueprint as approval to upload.

These are workflow defaults, not universal Oracle field defaults. Oracle's
[DFF import format](https://docs.oracle.com/en/cloud/saas/applications-common/26b/oaext/file-format-for-importing-descriptive-flexfields.html)
requires `ColumnName` to match an application column, and its
[flexfield API naming guidance](https://docs.oracle.com/en/cloud/saas/applications-common/25c/facia/naming-conventions-for-flexfield-apis.html)
restricts API names and cautions against changing them after creation.
