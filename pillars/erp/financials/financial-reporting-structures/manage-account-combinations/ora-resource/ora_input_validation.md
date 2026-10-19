# Manage Account Combinations Input Validation

Validate a local preparation candidate before any environment lookup, package handoff, or import approval. The candidate may be natural-language segment values, GlBulkComboInterface.csv, or GlBulkComboInterface.zip containing that CSV.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Candidate source | Natural-language segment vector, GlBulkComboInterface.csv, or GlBulkComboInterface.zip | Block preparation | Supply exactly one supported candidate source | Always |  |
| Chart of accounts | Position 1 from a CSV or ZIP, or a COA identifier embedded in natural-language input | Block preparation | Derive the identifier from the candidate; use code-first and name-fallback resolution for natural language | Always | resolve_chart_of_accounts_from_candidate |
| Segment vector | One through 30 ordered segment values | Block preparation | Use an accepted delimiter for natural language or populate positions 3 through 32 in CSV order | Natural-language candidate or CSV row |  |
| Import group | Import Group Identifier in position 38 | Generate a local yyyyMMddHHmmss value before CSV validation; do not ask the user for it | Use the user value when supplied; otherwise generate before CSV validation | Always |  |
| End marker | END in position 62 | Block preparation | Set the common row marker to END | CSV or ZIP candidate |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| CSV encoding and header | Require UTF-8 text without a header row; preserve valid quoted commas and blank fields | CSV candidate or ZIP member |  |
| ZIP member set | Require exactly one root member named GlBulkComboInterface.csv; reject additional, encrypted, absolute, drive-qualified, or traversal members | ZIP candidate |  |
| Package name | Require the supported Account Combinations package name GlBulkComboInterface.zip when creating or accepting a ZIP package | Package creation or ZIP candidate |  |
| Column count | Require exactly 62 columns in every nonblank row; reject a header, missing position, or populated overflow | CSV candidate or ZIP member |  |
| Chart of Accounts Code | Require a nonblank position 1 and require it equals the exact returned StructureInstanceCode from the candidate resolver | Every row | resolve_chart_of_accounts_from_candidate |
| Segment positions | Preserve positions 3 through 32 in order; accept one through 30 natural-language values, reject any segment value longer than 25 characters, and pad only the remaining physical positions with blanks | Every row |  |
| Flags | Enabled, Allow Posting, and Preserve Attributes may be blank; when populated each must be Y or N | Positions 2, 33, and 36 |  |
| Dates and numbers | Reject invalid dates, To Date earlier than From Date, and nonnumeric values in Attribute Number 1 through Attribute Number 5 | When positions 34, 35, or 55 through 59 are populated |  |
| Import group length | Require a nonblank value no longer than 18 characters | Position 38 |  |
| Common import group | Require the same Import Group Identifier on every row in the submitted CSV | Multirow candidate |  |
| End-of-record indicator | Require END at position 62 and require the same marker on every row | Every row |  |
| Natural-language delimiter | Accept a segment vector delimited by one nonempty repeated delimiter; do not split segment values on mixed or ambiguous delimiters | Natural-language candidate |  |

## FBDI Column Contract

| Position | Field | Mandatory |
|---|---|---|
| 1 | Chart of Accounts Code | Yes |
| 2 | Enabled | No |
| 3 | Segment1 | No |
| 4 | Segment2 | No |
| 5 | Segment3 | No |
| 6 | Segment4 | No |
| 7 | Segment5 | No |
| 8 | Segment6 | No |
| 9 | Segment7 | No |
| 10 | Segment8 | No |
| 11 | Segment9 | No |
| 12 | Segment10 | No |
| 13 | Segment11 | No |
| 14 | Segment12 | No |
| 15 | Segment13 | No |
| 16 | Segment14 | No |
| 17 | Segment15 | No |
| 18 | Segment16 | No |
| 19 | Segment17 | No |
| 20 | Segment18 | No |
| 21 | Segment19 | No |
| 22 | Segment20 | No |
| 23 | Segment21 | No |
| 24 | Segment22 | No |
| 25 | Segment23 | No |
| 26 | Segment24 | No |
| 27 | Segment25 | No |
| 28 | Segment26 | No |
| 29 | Segment27 | No |
| 30 | Segment28 | No |
| 31 | Segment29 | No |
| 32 | Segment30 | No |
| 33 | Allow Posting | No |
| 34 | From Date | No |
| 35 | To Date | No |
| 36 | Preserve Attributes | No |
| 37 | Alternate Account | No |
| 38 | Import Group Identifier | Yes |
| 39 | ATTRIBUTE_CATEGORY | No |
| 40 | ATTRIBUTE1 | No |
| 41 | ATTRIBUTE2 | No |
| 42 | ATTRIBUTE3 | No |
| 43 | ATTRIBUTE4 | No |
| 44 | ATTRIBUTE5 | No |
| 45 | ATTRIBUTE6 | No |
| 46 | ATTRIBUTE7 | No |
| 47 | ATTRIBUTE8 | No |
| 48 | ATTRIBUTE9 | No |
| 49 | ATTRIBUTE10 | No |
| 50 | Attribute Date 1 | No |
| 51 | Attribute Date 2 | No |
| 52 | Attribute Date 3 | No |
| 53 | Attribute Date 4 | No |
| 54 | Attribute Date 5 | No |
| 55 | Attribute Number 1 | No |
| 56 | Attribute Number 2 | No |
| 57 | Attribute Number 3 | No |
| 58 | Attribute Number 4 | No |
| 59 | Attribute Number 5 | No |
| 60 | Disabled By Feature | No |
| 61 | Cross-Validation Combination End Date | No |
| 62 | End-of-record indicator | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MAC-010-VALIDATE-INPUT | decision | 10 | validate_input | valid->MAC-020-RESOLVE-COA;invalid->MAC-070-HANDLE-ERROR | none | stop | Always |
