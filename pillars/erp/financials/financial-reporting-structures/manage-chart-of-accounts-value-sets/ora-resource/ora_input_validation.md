# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve |
|---|---|---|---|
| Value-set identity | ValueSetCode or SegmentCode | Block | Derive ValueSetCode as SegmentCode_VS when SegmentCode is present |
| COA-driven value-set scope | COA identity; user-confirmed Company, Cost Center, Account, and Intercompany baseline or an explicit replacement design; and every additional user-designed segment with its business classification and requested MaximumLength | Block | Present the baseline as a proposal, ask the user to confirm or revise it and provide any additional segments, then collect the remaining requested segment design detail. Do not derive additional segments. |
| Required value-set attributes | ModuleId, ValidationType, ValueDataType, ValueSubtype, MaximumLength, UppercaseOnlyFlag, ZeroFillFlag, SecurityEnabledFlag | Block | Apply workbook constants and the approved environment-independent ModuleId, then report the source |
| Import contract | Complete same-task FSM CSV export and ASM_SETUP_CSV_METADATA.xml | Block | Obtain complete same-task export; template-only output is supplementary only |

## Field Validation

| Check | What Happens |
|---|---|
| COA name | Reject values longer than 30 characters. |
| Segment name | Reject values longer than 30 characters. |
| ValueSetCode | Reject values longer than 30 characters, including codes derived from SegmentCode. |
| ValueSetIdentifier length | Reject values longer than 30 characters after validating or deriving the identifier. |
| Segment length | If supplied, require MaximumLength to be a numeric integer from 1 through 150. If segment length and MaximumLength are both blank, default MaximumLength to 6 before package generation. Never replace an explicitly supplied valid length with the default. |
| Delimiter | Allow only exclamation mark, asterisk, plus sign, hyphen, period, colon, equals sign, caret, tilde, or vertical bar. |
| ModuleId | Require exactly 47110F64AC0B08E2E040449823C60DB6 for every General Ledger value-set import, regardless of target environment. Default a blank value to this identifier and reject a different value before package generation. |
| ValueSetIdentifier | If supplied, require an English letter first, followed only by letters or digits; if blank, derive an alphanumeric identifier from user-provided ValueSetCode when present, otherwise from SegmentName. Remove nonalphanumeric separators and capitalize the next alphabetic character after each separator. |
| Secured value set | When SecurityEnabledFlag is Y, require a nonblank DataSecurityObjectName. Do not apply this requirement when SecurityEnabledFlag is N. |
| Table-validated value set | When ValidationType indicates table validation, require FromClause, ValueColumnName, ValueColumnType, ValueColumnLength, and IdColumnName. Validate EnabledFlagColumnName, StartDateColumnName, EndDateColumnName, WhereClause, and OrderByClause when supplied; do not invent missing optional clauses. |
| Vague create request | Propose Company, Cost Center, Account, and Intercompany; ask for COA identity, confirmation or revision of the proposed set, segment lengths, and any additional user-designed segments. Do not create artifacts, value sets, or values before confirmation. |
| Derived candidate code | Treat SegmentCode_VS as a lookup candidate only. Require exactly one matching value set with compatible MaximumLength and format before reuse; otherwise retain the candidate for creation readiness without requesting a separate value-set creation confirmation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COAVS.VALIDATE | step | 2 | validate_input | valid->COAVS.READY | COAVS.COLLECT | stop | Always |
