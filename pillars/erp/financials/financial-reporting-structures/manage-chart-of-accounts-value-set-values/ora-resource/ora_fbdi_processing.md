# Segment Values FBDI Processing Contract

Use this Markdown contract instead of local executable scripts. Apply every
step deterministically and stop the complete batch on any error.

## Contents

1. Canonical candidate
2. File intake algorithm
3. FBDI column order
4. Usage classification
5. Validation and defaulting algorithm
6. Package generation and verification
7. Data Loader handoff

## Canonical Candidate

Represent one request as:

```text
InputFormat: text | image | csv | zip
SourceRole: create_update_candidate
ValueSetCode: exact target code
ResolvedValueSetId: identifier returned by the exact parent lookup
MaximumLength: integer from 1 through 150 returned by the exact parent lookup
NaturalAccount: true | false | unknown
SegmentUsageEvidence: explicit_natural_account |
                      explicit_normal_segment |
                      not_supplied
Values[]:
  Value
  StartDate
  EndDate
  SummaryFlag
  EnabledFlag
  AccountType
  AllowPostingFlag
  AllowBudgetingFlag
  ThirdPartyControlAccount
  ReconcileFlag
  FinancialCategory
  Description
  AdditionalFBDIColumns
Provenance[]:
  rowIndex
  sourceFile or sourceImage
  sourceRow
  sourceColumnCount
```

Keep `AdditionalFBDIColumns` as an ordered field-name-to-value map. It may
contain only supported translated descriptions, `ATTRIBUTE1` through
`ATTRIBUTE50`, and `DATA_SOURCE`.

## File Intake Algorithm

For text, extract the exact Value Set Code and every visible/requested row in
input order. For an image, transcribe visible cells and preserve blanks; ask for
unreadable required cells rather than guessing.

For CSV and ZIP input:

1. Accept UTF-8 and remove an input UTF-8 BOM. Produce UTF-8 without a BOM.
2. For ZIP input, reject absolute paths, drive-qualified paths, `..` traversal,
   encrypted members, more than 50 files, a member over 10 MiB, total
   uncompressed content over 50 MiB, or a compression ratio over 100:1.
3. Prefer exactly one case-insensitive basename
   `GlSegmentValuesInterface.csv`. If absent, accept only one unambiguous CSV.
   Reject no CSV, multiple preferred members, or multiple other CSV files.
4. Ignore blank rows, a row whose first cell is `Segment Values`, a row
   containing `* Required`, and a header row beginning `Value Set Code,Value`.
5. Require 13 through 101 columns. Pad positions 14 through 101 with blanks
   when omitted. If more than 101 columns exist, allow only blank overflow
   cells and discard them; reject any populated overflow position.
6. Require Value Set Code in position 1 and Value in position 2.
7. Normalize positions 5, 6, 8, and 9 to `Y` or `N`. Accept only
   `Y/Yes/true/1` and `N/No/false/0`, case-insensitive.
8. Trim positions 3, 4, 7, 10, 11, and 12. Preserve Value and descriptions
   exactly except for the validations in `ora_input_validation.md`.
9. Require exactly one distinct Value Set Code per candidate.
10. Record source row and original column count for every data row.

An empty candidate is invalid. Treat an attached CSV or ZIP as a
`create_update_candidate` only when the user requests preparation or
create/update processing.

## FBDI Column Order

Write exactly 101 headerless columns in this order:

| Position | FBDI field |
|---:|---|
| 1 | `VALUE_SET_CODE` |
| 2 | `VALUE` |
| 3 | `START_DATE_ACTIVE` |
| 4 | `END_DATE_ACTIVE` |
| 5 | `SUMMARY_FLAG` |
| 6 | `ENABLED_FLAG` |
| 7 | `ACCOUNT_TYPE` |
| 8 | `ALLOW_POSTING_FLAG` |
| 9 | `ALLOW_BUDGETING_FLAG` |
| 10 | `THIRD_PARTY_CTRL_ACCOUNT` |
| 11 | `RECONCILE_FLAG` |
| 12 | `FINANCIAL_CATEGORY` |
| 13 | `DESCRIPTION_US` |
| 14 | `DESCRIPTION_AR` |
| 15 | `DESCRIPTION_CS` |
| 16 | `DESCRIPTION_D` |
| 17 | `DESCRIPTION_DK` |
| 18 | `DESCRIPTION_E` |
| 19 | `DESCRIPTION_EL` |
| 20 | `DESCRIPTION_ESA` |
| 21 | `DESCRIPTION_F` |
| 22 | `DESCRIPTION_FRC` |
| 23 | `DESCRIPTION_HR` |
| 24 | `DESCRIPTION_HU` |
| 25 | `DESCRIPTION_I` |
| 26 | `DESCRIPTION_IS` |
| 27 | `DESCRIPTION_IW` |
| 28 | `DESCRIPTION_JA` |
| 29 | `DESCRIPTION_KO` |
| 30 | `DESCRIPTION_NL` |
| 31 | `DESCRIPTION_LT` |
| 32 | `DESCRIPTION_PL` |
| 33 | `DESCRIPTION_PT` |
| 34 | `DESCRIPTION_PTB` |
| 35 | `DESCRIPTION_N` |
| 36 | `DESCRIPTION_RO` |
| 37 | `DESCRIPTION_RU` |
| 38 | `DESCRIPTION_S` |
| 39 | `DESCRIPTION_SF` |
| 40 | `DESCRIPTION_SK` |
| 41 | `DESCRIPTION_SL` |
| 42 | `DESCRIPTION_TH` |
| 43 | `DESCRIPTION_TR` |
| 44 | `DESCRIPTION_ZHS` |
| 45 | `DESCRIPTION_ZHT` |
| 46-95 | `ATTRIBUTE1` through `ATTRIBUTE50`, in numeric order |
| 96 | `DATA_SOURCE` |
| 97 | `DESCRIPTION_UK` |
| 98 | `DESCRIPTION_ET` |
| 99 | `DESCRIPTION_LV` |
| 100 | `DESCRIPTION_VN` |
| 101 | `IS_VALIDATED`; always blank |

Map canonical `Description` to `DESCRIPTION_US`. Canonical fields override the
same fields found in `AdditionalFBDIColumns`. Never write `VALUE_SET_CODE` or
`IS_VALIDATED` from `AdditionalFBDIColumns`.

The loader control file, not this CSV, supplies:

- `STATUS_CODE=NEW`
- `OBJECT_VERSION_NUMBER=1`
- `LOAD_REQUEST_ID`
- Creation and update audit columns

## Usage Context

Resolve import usage without Fusion value access:

1. In an end-to-end plan, an established Chart of Accounts Structure Instance
   context that assigns the target value set to Natural Account yields
   `NaturalAccount=true` and evidence `structure_instance_proved`.
2. In a standalone task run, an explicit user declaration that the value set is
   Natural Account yields `NaturalAccount=true` and evidence
   `standalone_declared`.
3. Otherwise set `NaturalAccount=false` and evidence `not_proved_or_declared`.
   Do not infer usage from a value set name, value, description, or a supplied
   Account Type.

Never download or query values for this decision. Don't classify a supplied
value as create or update before submission. The primary ESS outcome returned
by the authorized FBDI Loader is the server-side authority for the overall
import.

## Validation and Defaulting Algorithm

Run a base pass before Fusion access, followed by a classified pass after
segment usage is resolved:

1. Require one nonblank Value Set Code, at least one row,
   a nonblank Description for every row, and object-shaped rows.
2. Require Summary, Allow Posting, and Allow Budgeting for every row. Normalize
   accepted Boolean equivalents to `Y/N`.
3. Reject a row when Summary is `Y` and either Allow Posting or Allow Budgeting
   is `Y`. Require both flags to be `N` for a summary value; never silently
   override an explicit conflicting flag.
4. For text and image input, default omitted Enabled Flag to `Y`; for CSV/ZIP,
   require position 6. Record each default.
5. Normalize dates from `YYYY-MM-DD` or `YYYY/MM/DD` to `YYYY/MM/DD`. Reject an
   impossible date or End Date before Start Date.
6. Apply every rule and lexicon in `ora_input_validation.md`.
7. Reject duplicate Value strings within the candidate using exact comparison.
8. Require an exact resolved parent Value Set Code and REST Maximum Length from
   1 through 150; reject any Value whose character count exceeds it.
9. When `NaturalAccount=true`, require Account Type for every row. Suggest a
   type from Description only when its meaning is unambiguous, and require the
   user to accept or correct every suggestion. Ask for an explicit type for
   each unresolved row; do not build a package until all types are reviewed.
10. When `NaturalAccount=false`, leave Account Type blank unless explicitly
   supplied; validate and normalize any supplied type.
11. Normalize every supplied or reviewed Account Type:
   `Asset/A -> A`, `Liability/L -> L`, `Expense/E -> E`,
   `Owner's Equity/Owners Equity/Equity/O -> O`, and `Revenue/R -> R`.
12. When NaturalAccount is true or Account Type is supplied, default omitted
    Third Party Control Account and Reconcile Flag to `N` after the whole batch
    is otherwise valid. Otherwise leave all three fields blank. Preserve
    explicit valid values.
13. Accept Third Party Control Account only as `N`, `Y`, `R`, `CUSTOMER`, or
    `SUPPLIER`. Normalize Reconcile Flag to `Y/N`.
14. Do not create a prepared candidate or package unless every row passes.

Return validation results with status, phase, Value Set Code, classification,
Maximum Length, row count, error count, defaults, and per-row errors containing
rule ID, field, and message.

## Package Generation and Verification

Create the package only from the requested prepared rows.

1. Reconfirm exact resolved Value Set Code and ID, REST Maximum Length from 1
   through 150, proved/declared-or-not Natural Account context, at least one
   row, and required prepared
   fields `Value`, `SummaryFlag`, `EnabledFlag`, `AllowPostingFlag`, and
   `AllowBudgetingFlag`.
2. Allocate 101 blank cells per row and map fields by the table above.
3. Serialize with standard CSV quoting and LF record endings as UTF-8 without a
   BOM. Do not write a header.
4. Name the CSV `GlSegmentValuesInterface.csv`.
5. Create `glsegmentvaluesandhierarchy.zip` containing that one root member.
   Do not include `GlSegmentHierInterface.csv`.
6. When the available ZIP tool supports reproducible metadata, use timestamp
   `1980-01-01 00:00:00`, DEFLATE compression, and file mode `0600`.
7. Reopen the ZIP. Require the exact one-member list and byte-for-byte equality
   between the member and source CSV.
8. Reparse every CSV row and require exactly 101 columns.
9. Compute SHA-256 for both CSV and ZIP after finalization.

For a user-supplied `create_update_candidate` ZIP, reuse its exact bytes as a validated
fast path only when the conditions in `ora_bulk_intake.md` all pass. Set
`packageMode=reused_user_zip`. If any field must be normalized, defaulted,
padded, cleared, or changed, rebuild the package and set
`packageMode=rebuilt`.

The package report must include status, package mode, Value Set Code, row count,
column count, artifact paths, member list, `hierarchyCsvIncluded=false`, CSV
hash, ZIP hash, values, and these technical defaults:

```text
STATUS_CODE: NEW (control-file constant)
OBJECT_VERSION_NUMBER: 1 (control-file constant)
LOAD_REQUEST_ID: assigned by Load Interface File for Import
auditColumns: assigned by the loader
IS_VALIDATED: blank workbook-only marker
```

## Data Loader Handoff

After package verification and exact-preview approval, hand the immutable ZIP
to `core.data-loader`. Do not upload to UCM, call ERP Integrations, submit ESS,
or poll jobs directly from this pillar. Data Loader owns validation, immutable
preview, approval, import selection, submission, monitoring, and returned outcome.

Treat the Data Loader result as an overall outcome, not row-level evidence.
Report supplied values as submitted and mark created, updated, unchanged,
rejected, and not-processed counts unavailable unless Data Loader returns them.
On timeout, terminal non-success, or uncertain submission, report the Data
Loader result without a supplemental lookup. Never resubmit automatically.
