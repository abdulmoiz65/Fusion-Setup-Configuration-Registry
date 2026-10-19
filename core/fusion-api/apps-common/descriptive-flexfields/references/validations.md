# DFF Context and Segment Validations

Apply these checks whenever the selected DFF setup task will create or update
global segments, contexts, or context-sensitive segments. Complete them before
building an FSM CSV import ZIP and repeat them against the final candidate ZIP,
including a user-supplied ZIP. Use the selected task's current export and
metadata as the authority for its CSV member names, headers, parent keys, and
available table columns. Do not infer an unsupported column or CSV field from
the examples below.

These are **FSCR preflight requirements** for this workflow. Oracle's generic
DFF import format marks some of these fields optional; that does not waive the
reviewed design requirements below. The user need not supply a separate *Data
Type* field. Resolve the type from the available description, value-set code,
or table column under the defaulting rules, then validate compatibility. Do
not add a `DataType` CSV header unless the selected task format declares one.

## Required global and context-sensitive segment information

For every segment being created or changed, resolve and review each item. An
unchanged value may be taken from an exact, current exported row; never guess
one from the segment label or a different DFF.

| Required item | Meaning and validation |
| --- | --- |
| `Name` | The segment's display name. Require nonblank text. |
| `SegmentCode` (Code) | The stable segment code. Require a nonblank code and match an update to exactly one existing segment in the intended DFF and context. |
| `SegmentIdentifier` (API Name) | The segment's API identifier. Require a nonblank, reviewed identifier for a new segment; preserve the existing identifier for an update unless the selected task's guidance explicitly supports changing it. |
| `ColumnName` (Table Column) | The application table column used to store the attribute value. Require a nonblank, supported column and confirm its availability and data type from the current DFF/task metadata. Character attributes use `ATTRIBUTE1`–`ATTRIBUTE30` (30 columns); Number attributes use `ATTRIBUTE_NUMBER1`–`ATTRIBUTE_NUMBER10` (10 columns); Date attributes use `ATTRIBUTE_DATE1`–`ATTRIBUTE_DATE5` (5 columns); Date Time attributes use `ATTRIBUTE_TIMESTAMP1`–`ATTRIBUTE_TIMESTAMP5` (5 columns). The column family can establish the Data Type when the user has not supplied one. Reject a column outside the range or inconsistent with a type resolved from another supplied input. Treat `Date` and `Date Time` as distinct types. These ranges do not establish that every column exists or is available in the selected table. |
| `ValueSetCode` (Value Set) | The code of the value set associated with the segment. Require the intended code in the reviewed segment design and validate every nonblank code through the Value Sets skill below. Do not treat a reference in another exported segment as proof that the value set is currently valid. |
| `Prompt` | The text shown to the user for the segment. Require nonblank text. |
| `DisplayType` | The display control selected for the segment. Require a nonblank lookup code from the primary or secondary list below, supported by the selected task's format and compatible with the attribute's Data Type and value set. |
| `SequenceNumber` | The segment's display order within its global or named context. Require a positive integer and check that it does not conflict with another segment in that same scope. |

For a context-sensitive segment, also require its exact parent `ContextCode`.
Match that code to one existing context or to a context in the same reviewed
candidate. Confirm the DFF code and application ID on the parent and segment
rows agree with the selected task. Include every additional field required by
the selected task's CSV contract, even when it is not listed in this design
table.

## Display type lookup codes

The lookup codes below describe how a DFF attribute (segment) appears to the
user. They are **display types**, distinct from the attribute's `Character`,
`Number`, `Date`, or `Date Time` Data Type. When the user has not supplied `DisplayType`,
present the primary choices below and request a selection. Also accept a
secondary code when the user explicitly supplies one. Preserve the selected
lookup code exactly; do not replace a secondary code with a primary one.

### Primary choices

| Lookup code | Meaning | Data Type restriction |
| --- | --- | --- |
| `TEXT_BOX` | Text Box | No additional restriction in this list. |
| `DATE_TIME` | Date/Time | Use only for a `Date` attribute. |
| `CHECKBOX` | Check Box | Use only for a `Number` attribute. |
| `TEXT_AREA` | Text Area | No additional restriction in this list. |
| `LOV` | List of Values | No additional restriction in this list. |
| `DROP_DOWN_LIST` | Drop-down List | No additional restriction in this list. |
| `POP_UP_LIST` | Pop-up List of Values | No additional restriction in this list. |
| `RADIO_BUTTON_GROUP` | Radio Button Group | No additional restriction in this list. |
| `STATIC_URL` | Static URL | No additional restriction in this list. |
| `INPUT_SEARCH` | Inline Search | No additional restriction in this list. |
| `HIDDEN` | Hidden | No additional restriction in this list. |

### Secondary choices accepted when supplied

| Lookup code | Meaning |
| --- | --- |
| `COLOR` | Color |
| `DYNAMIC_URL` | Dynamic URL |
| `MULTI_SELECT_LOV` | Multiple Select List of Values |
| `RICH_TEXT_EDITOR` | Rich Text Editor |

Reject `DATE_TIME` for a `Character`, `Number`, or `Date Time` attribute, and
reject `CHECKBOX` for a `Character`, `Date`, or `Date Time` attribute. For every
code, also check
the selected task's supported display types and any applicable value-set
requirements. If the chosen code is unsupported or incompatible, report the
specific code and attribute; ask the user to select a valid display type
before package preparation.

## Required context information

A DFF may define multiple context values. Validate each new or updated context
separately; its context-sensitive segments must reference its exact
`ContextCode`.

| Required item | Meaning and validation |
| --- | --- |
| `Name` (Display Name) | The context name shown to users. Require nonblank text. |
| `ContextCode` (Code) | The stable code that identifies the context. Require a nonblank code; match an update to exactly one existing context, and reject a conflicting create. |
| `ContextIdentifier` (API Name) | The context's API identifier. Require a nonblank, reviewed identifier for a new context; preserve the existing identifier for an update unless the selected task's guidance explicitly supports changing it. |

Confirm that the context belongs to the selected DFF and application. Include
any further task-specific required CSV fields, such as its enabled state, from
the authoritative task format.

## Cross-row and package checks

1. **No repeated global segment:** Compare every proposed context-sensitive
   segment with the DFF's existing and proposed global segments. After trimming
   and case folding, a matching `SegmentCode`, `SegmentIdentifier`, or `Name`
   means the context-sensitive segment repeats a global segment. Block the
   candidate and report the conflicting rows; do not silently rename one.
   Check the selected task's column-allocation rules separately. Oracle may
   allow one storage column to serve segments in different contexts, so column
   equality alone does not establish that two segments repeat.
2. **Blank `MultirowUniqueKeyFlag`:** In the prepared context-sensitive segment
   CSV, where this header belongs to the selected task format, require a blank
   value in every included row before import. Do not insert the header into a
   member whose authoritative format omits it. If the target context is
   multirow and its contract requires a unique-key flag, stop and report the
   conflict rather than sending an invalid blank value. If an unrelated
   exported row has a nonblank flag, stop rather than clearing or dropping that
   row merely to make the package pass.
3. **Value-set definition:** For each distinct nonblank `ValueSetCode` in the
   requested segments, invoke `core.fusion-api.apps-common.value-sets` and use
   its read-only `valueSets` route through `core.fusion-api.rest-api-client`.
   Resolve the code to exactly one value set in the confirmed target Fusion
   environment; inspect the returned `ValueSetCode` and `ValueDataType`.
   Compare `ValueDataType` with the resolved segment data type and the selected
   column family. Missing, ambiguous, inaccessible, or incompatible results
   block package preparation. This is a definition check, not permission to
   create or change value-set values.
4. **Candidate integrity:** Validate the exact candidate ZIP against the
   current task export: correct DFF/application parent keys, context links,
   expected metadata member and CSV headers, and unchanged unrelated rows.
   Report each failed field, row, and evidence source. Do not repair the ZIP
   silently or send a failed candidate to `core.data-loader`.

Return a pass/block result for each check, the exact task and DFF identity,
the evidence used, and any missing design decision. Classify missing or
conflicting input as `input_validation`, a task-format or value-set mismatch
as `catalog_or_metadata_mismatch`, and an unavailable live lookup as
`auth/authz` or `transport/environment` as appropriate. Persist the safe
diagnostic in the active project workflow when it writes durable artifacts;
omit credentials, tokens, and sensitive row values.

After all DFF checks pass, hand the immutable ZIP and task context to
`core.data-loader` for its separate FSM source validation, Task Hook, preview,
and approval workflow. Do not upload, import, or deploy from this validation
reference.

## Oracle references

- [File Format for Importing Descriptive Flexfields](https://docs.oracle.com/en/cloud/saas/applications-common/26b/oaext/file-format-for-importing-descriptive-flexfields.html) documents the generic context and segment fields.
- [Get all value sets](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-servername-fscmrestapi-resources-11.13.18.05-valuesets-get.html) documents `ValueSetCode` and `ValueDataType`.
- [Overview of Descriptive Flexfields](https://docs.oracle.com/en/cloud/saas/applications-common/25c/facia/overview-of-descriptive-flexfields.html) explains context-sensitive segments and shared storage columns across contexts.
