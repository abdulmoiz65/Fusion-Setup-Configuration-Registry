# Defaulting Rules

## Source Precedence

| Sequence | Source | Use |
|---|---|---|
| 1 | Complete same-task FSM CSV export and ASM_SETUP_CSV_METADATA.xml | Reuse populated technical values, internal codes, column names, and accepted value forms |
| 2 | Supported read-only Fusion metadata | Resolve target-specific identifiers or lookups absent from the full export |
| 3 | COA Attributes workbook | Apply required, derived, constant, and fallback default rules |
| 4 | Oracle functional and EDM documentation | Resolve documented semantics only |

Template-only exports may supplement the complete export for file shape, but must not replace the complete export.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Source |
|---|---|---|---|---|
| ValueSetCode | SegmentCode_VS | Value-set code is blank | No | COA Attributes workbook: Value Sets row 2 |
| ModuleId | 47110F64AC0B08E2E040449823C60DB6 | Always | Yes | Approved General Ledger value-set module identifier; use this same value in every environment |
| ValueSetIdentifier | Alphanumeric identifier derived from user-provided ValueSetCode when present; otherwise derive from SegmentName | User leaves it blank | Yes | User instruction; COA Attributes workbook: Value Sets row 3 identifies this as nonrequired |
| Description | Segment name or documented business description | User leaves it blank | Yes | COA Attributes workbook: Value Sets row 4 derived |
| ValidationType | INDEP | User leaves it blank | No | COA Attributes workbook: Value Sets row 5 |
| ValueDataType | VARCHAR2 | User leaves it blank | No | COA Attributes workbook: Value Sets row 6 |
| ValueSubtype | TEXT | User leaves it blank | No | COA Attributes workbook: Value Sets row 7 |
| MaximumLength | 6 | User leaves segment length or MaximumLength blank | No | User-provided default-length rule; COA Attributes workbook: Value Sets row 8 |
| UppercaseOnlyFlag | N | User leaves it blank | Yes | COA Attributes workbook: Value Sets row 11 |
| ZeroFillFlag | N | User leaves it blank | Yes | COA Attributes workbook: Value Sets row 12 |
| SecurityEnabledFlag | N | User leaves it blank | Yes | COA Attributes workbook: Value Sets row 13 |
| Optional min/max, precision, scale, security object, audit, and independent-value-set fields | blank | User leaves them blank and full export does not establish a value | No | COA Attributes workbook: Value Sets rows 9–10 and 14–28 |
| Baseline segment design | Company, Cost Center, Account, and Intercompany | User makes a vague COA-creation request with no structural details; present as a proposal and wait for confirmation | No | User-provided vague-request rule |

## Identifier Derivation

| Source Value | Derived ValueSetIdentifier | Rule |
|---|---|---|
| test-1-coa | Test1Coa | Remove nonalphanumeric separators and capitalize the next alphabetic character after each separator; capitalize the first alphabetic character for user-provided ValueSetCode sources |
| tst1 coa | tst1Coa | Remove the space and capitalize the next alphabetic character |
| test1@coa | test1Coa | Remove the special character and capitalize the next alphabetic character |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COAVS.DEFAULT | step | 5 | apply_default | complete->COAVS.BULK | COAVS.LOOKUP | stop | Object absent |
