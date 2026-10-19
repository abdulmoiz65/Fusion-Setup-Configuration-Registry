# Manage Person Name Formats Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_manage_person_name_formats | Read is requested, or an exact target is needed before create, edit, or delete | Legislation code, country, format code, or person name format display name | /hcmRestApi/resources/{version}/nameFormats | Country, legislation, format type, scope, and ordered components | Match exact format codes with FormatName and display names with FormatNameMeaning. For an explicitly requested display-name contains search, use q=FormatNameMeaning like '%term%' and replace term with the escaped caller value. Use CountryName or LegislationCode for country scope; page results and require one exact format and component target for edit or delete. | Functional format values; retain runtime IDs only for the current run | Return read rows; stop on zero or multiple exact targets |
| resolve_name_format_component_token | Create or edit supplies ordered component or separator labels | Exact ordered labels, country or legislation, scope, and format type | Current /hcmRestApi/resources/{version}/nameFormats, current NameFormat Data Loader metadata, and the `PER_NAME_SUB_FORMAT_COMPONENTS` common lookup | Component labels, literal characters, stored mask tokens, FormatName, LegislationCode, and UserFormatChoice | Require one proven token for every requested label in the applicable contract; never derive abbreviations from label text. Use the proven literal mappings below; for any other literal character, require one exact current separator token. For `<$preferred$$fallback$>`, resolve both core attributes independently and retain their supplied order. | Ordered tokens used to build FormatMask | Stop when any token is missing or ambiguous. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| An exact target or token is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A collection is requested | Use bounded limit and offset pagination and follow hasMore or the next page only to the declared bound. |

## Proven Literal Token Mappings

The `PER_NAME_SUB_FORMAT_COMPONENTS` lookup proves the following literal
separator mappings. Use the stored token form in `FormatMask`; never emit the
literal character as raw mask content.

| Literal meaning | Stored token |
| --- | --- |
| double quote (`"`) | `$QUO$` |
| opening parenthesis (`(`) | `$OPE$` |
| closing parenthesis (`)`) | `$CLO$` |
| comma (`,`) | `$COM$` |
| period (`.`) | `$DOT$` |
| slash (`/`) | `$SLA$` |
| colon (`:`) | `$COL$` |
| semicolon (`;`) | `$SEM$` |
| at sign (`@`) | `$ATT$` |
| whitespace | `$SPA$` |

Treat this table as a known contract, but re-resolve the lookup when Fusion
reports a schema or token error, or when the selected environment is known to
use a different current lookup value.

## Read Response Presentation

For each Name Format returned to a user, return only a `Human-readable layout`
value. Decode the complete returned `FormatMask`, including its current proven
component and separator tokens in stored order. Keep `FormatMask` as internal
lookup and validation evidence, but do not include it in the user-facing
response.

| Stored token | Human-readable rendering |
|---|---|
| `$FIR$` | First Name |
| `$KNA$` | Known As |
| `$PNA$` | Prefix |
| `$LAS$` | Last Name |
| `$MID$` | Middle Name |
| `$TIT$` | Title |
| `$SUF$` | Suffix |
| `$SPA$` | space |
| `$COM$` | comma |
| `$OPE$` | opening parenthesis |
| `$CLO$` | closing parenthesis |
| `$QUO$` | double quote |
| `$DOT$` | period |
| `$SLA$` | slash |
| `$COL$` | colon |
| `$SEM$` | semicolon |
| `$ATT$` | at sign |

Render separators from the mask naturally: `$SPA$` is one space and
`$COM$$SPA$` is comma plus one space. Do not flatten a layout into a
comma-separated component list. If a returned component or separator token is
not proven by current metadata or this table, show that token verbatim in the
human-readable layout and label it `unresolved`; never derive a label from its
abbreviation.

Render `<$preferred$$fallback$>` as `Preferred (or Fallback)`, preserving the
stored order. The angle brackets are a replacement component, not literal
output. If either nested token is unresolved, render that token verbatim and
label the replacement component `unresolved`.

Example output:

| Format name | Human-readable layout |
|---|---|
| `DISPLAY_NAME` | First Name Preferred Name Last Name |
| `LIST_NAME` | Last Name, First Name |

## Confirmed Create Response

After a Name Format create is confirmed, always present the created record in
this form. Use the authoritative `nameFormats` read when a status or
reconciliation workflow authorizes that read. If the caller confirms creation
in the UI without requesting a read, return the confirmed submitted values and
label the source accordingly.

| Field | User-facing value |
|---|---|
| Format name | `FormatName` |
| Scope | Global or Local |
| Legislation or country | Returned legislation/country, when applicable |
| Human-readable layout | Fully rendered component and separator sequence |

Do not include the raw `FormatMask`, runtime identifiers, loader request IDs,
or the DAT source row in this confirmation response.

## Confirmed Delete Response

After a Name Format delete is confirmed, state: `The Name Format was deleted successfully.` Then identify the deleted record by Format name, Scope, and
Legislation or country. Confirm through an authorized post-load status/read
workflow or the caller's UI confirmation. An accepted asynchronous Data Loader
initiation is not confirmation that the record was deleted.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PNF.READ | decision | 3 | reference_lookup | resolved->PNF.DEFAULTS;list_returned->PNF.DEFAULTS;not_found->PNF.ERROR;ambiguous->PNF.ERROR;failed->PNF.ERROR | PNF.DEPENDENCY | stop | Read is requested, or an exact target is required before create, edit, or delete |
