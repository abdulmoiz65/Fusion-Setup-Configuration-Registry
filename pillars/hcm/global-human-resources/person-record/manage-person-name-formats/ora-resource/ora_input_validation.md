# Manage Person Name Formats Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Person Name Formats.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, or delete | Block | Provide one supported operation | Every request |  |
| Format scope | Country or legislation, scope, and format type | Block | Provide one complete format scope | Every request | find_manage_person_name_formats |
| Existing format selector | Exact format code or display name within the resolved scope | Block | Provide one exact selector | edit or delete | find_manage_person_name_formats |
| Create components | Ordered component or separator labels | Block | Provide the intended ordered layout | create | resolve_name_format_component_token |
| Create source identity | `SourceSystemId` and `SourceSystemOwner`, including blanks | Default | Write both fields as blank unless the caller supplies nonblank values; preserve blanks through live Data Loader validation | create |  |
| Edit changes | Exact format and at least one supported component or field change | Block | Provide the target and intended change | edit | find_manage_person_name_formats |
| Delete target | One exact format or component target | Block | Provide the exact component selector; do not select the full container | delete | find_manage_person_name_formats |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A required format scope or target does not resolve exactly once | Missing | Correct the scope or selector | find_manage_person_name_formats |
| A country or legislation, scope, and format-type combination already exists for create | Invalid | Stop the duplicate create | find_manage_person_name_formats |
| A component or separator label has no unique proven token | Unsupported | Correct the label or restore the current token contract | resolve_name_format_component_token |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Effective range | Reject an end date earlier than its start date | Both dates are supplied |  |
| Component uniqueness | Reject duplicate component selections | Components are supplied |  |
| Component order | Reject an order incompatible with the applicable person name style | Components are supplied | resolve_name_format_component_token |
| Supported shape | Reject unsupported fields or source shapes | A mutation source is prepared |  |
| FormatMask source | Build FormatMask only from proven stored tokens; reject display labels as tokens | create or edit supplies components | resolve_name_format_component_token |
| Replacement component | Accept `<$preferred$$fallback$>` only when it contains exactly two proven core name-component tokens, in preferred-then-fallback order. Reject nested `<...>` groups, punctuation, separators, and non-token text inside the group. | A FormatMask supplies a replacement component | resolve_name_format_component_token |
| Layout literal mapping | Map whitespace to `$SPA$`, comma to `$COM$`, `(` to `$OPE$`, `)` to `$CLO$`, `"` to `$QUO$`, `.` to `$DOT$`, `/` to `$SLA$`, `:` to `$COL$`, `;` to `$SEM$`, and `@` to `$ATT$`. Reject any other literal character that has no unique current token. | A human-readable layout is supplied | resolve_name_format_component_token |
| FormatMask grouping | Use a backslash before each vertical-bar delimiter: one delimiter at outer boundaries and two adjacent delimiters between layout groups; concatenate tokens within each group | FormatMask is built |  |
| FormatMask escaping | Require a backslash before every vertical-bar delimiter in the source value. A leading quote is not an escape | FormatMask is supplied or built |  |
| Blank source identity | By default, write and preserve blank `SourceSystemId` and `SourceSystemOwner` values; reject any source that replaces them with inferred values or fails current live Data Loader validation | Create source has blank source identity fields |  |
| Identity selection | Prefer an accepted source-system identity or the unique natural scope key (`FormatName`, `LegislationCode`, `UserFormatChoice`) over `NameFormatId`. Include `NameFormatId` only when current live Data Loader template validation proves the selected operation requires it. | An update or delete source is prepared |  |
| Delete-row cardinality | Reject a `DELETE` record with more or fewer attribute values than its current `METADATA` definition. Count only values after the instruction and component discriminator; escaped `FormatMask` pipes are not field separators. | A delete source is prepared |  |

For every update or delete row, resolve the format exactly once, then generate
the smallest identity accepted by the current live contract. The preferred order
is: explicitly supplied source-system identity, unique natural scope key, then
the primary `NameFormatId` only when validation requires it. Do not invent a
source-system identity, reuse an ID from a stale read, or add `NameFormatId`
merely as a precaution.

For a delete, preserve the complete current metadata shape even when mutable
attributes are blank. `DELETE` and `NameFormat` are control fields and do not
count as attributes. With the current header
`METADATA|NameFormat|FormatName|LegislationCode|UserFormatChoice|FormatMask|SourceSystemId|SourceSystemOwner`,
the exact France local Order Name row is
`DELETE|NameFormat|ORDER_NAME|FR|L|||`. It has six attribute values: Order
Name, FR, L, and blank FormatMask, SourceSystemId, and SourceSystemOwner.
`DELETE|NameFormat|ORDER_NAME|FR|L||||` is invalid because its fourth trailing
delimiter introduces a seventh attribute value. Validate this cardinality
before creating the immutable ZIP preview.

For a layout of Last Name, space, First Name, comma, space, Title, use the
stored mask `|$LAS$$SPA$||$FIR$$COM$$SPA$||$TIT$|`. In a Data Loader source,
escape the stored pipe delimiters as
`\|$LAS$$SPA$\|\|$FIR$$COM$$SPA$\|\|$TIT$\|`; do not omit the double-pipe
layout-group separators.

For a replacement component, enclose the preferred and fallback tokens in angle
brackets. For example, Last Name, space, First Name, comma, space, Title with
Prefix as the replacement value uses the stored mask
`|$LAS$$SPA$||$FIR$$COM$$SPA$<$TIT$$PNA$>|`. Its Data Loader source is
`\|$LAS$$SPA$\|\|$FIR$$COM$$SPA$<$TIT$$PNA$>\|`. The comma and space are
outside the replacement component; the component itself contains only Title
then Prefix.

For global `LIST_NAME` requested as `Prefix Lastname`, normalize `Lastname` to
the Last Name component and map the separating whitespace to `$SPA$`. The
stored mask is `|$PNA$$SPA$||$LAS$|`; the escaped Data Loader source is
`\|$PNA$$SPA$\|\|$LAS$\|`. A comma maps to `$COM$`. For any other supplied
literal character, resolve its exact current separator token first; do not emit
the character as raw mask text or guess a token abbreviation.

The current `PER_NAME_SUB_FORMAT_COMPONENTS` contract also proves parentheses,
double quote, period, slash, colon, semicolon, and at sign. Map them to
`$OPE$`, `$CLO$`, `$QUO$`, `$DOT$`, `$SLA$`, `$COL$`, `$SEM$`, and `$ATT$`,
respectively. For example, `LastName (FirstName)` uses
`|$LAS$$SPA$||$OPE$$FIR$$CLO$|`. Any literal absent from this contract remains
an expected validation rejection until it resolves exactly.

The raw mask and Data Loader field separators both use pipes. Keep the raw
stored mask only as evidence, and serialize every literal mask pipe as `\|` in
the DAT field so it is not interpreted as an attribute separator. Local schema
validation does not prove Fusion's runtime interpretation of the `MERGE` value;
submission still requires a freshly validated immutable preview and approval.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PNF.VALIDATE | decision | 1 | validate_input | valid->PNF.DEPENDENCY;missing->PNF.ERROR;invalid->PNF.ERROR;unsupported->PNF.ERROR | none | stop | Every Manage Person Name Formats request |
