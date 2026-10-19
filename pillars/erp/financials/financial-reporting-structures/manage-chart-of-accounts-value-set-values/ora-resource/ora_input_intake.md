# Value Set Value Input Intake

## Accepted Input Formats

| Input Format | Required Content | Handling |
|---|---|---|
| Natural-language text | Value Set Code and one or more values with Summary, Allow Posting, and Allow Budgeting flags | Normalize all rows in input order |
| Image | Visible value rows and headers | Transcribe visible cells; ask once for unreadable required cells and never infer them |
| CSV | Headerless segment-value rows with 13 through 101 columns | Parse locally into the canonical candidate |
| ZIP | One unambiguous `GlSegmentValuesInterface.csv` | Inspect safely and parse locally; `GlSegmentHierInterface.csv` isn't required |

## Dependency Inputs

| Field | Mandatory | Purpose | Rule |
|---|---|---|---|
| ValueSetCode | Yes | Identify the target value set | Require an exact nonblank code |
| Values[] | Yes | Hold every requested value row | Require at least one row and preserve order |
| Value | Every row | Identify the segment value | Require nonblank and unique within the submitted batch |
| Description | Every row | Describe the segment value | Require nonblank; map to `DESCRIPTION_US` |
| SummaryFlag | Every row | Identify summary values | Require explicit Y/N or an unambiguous equivalent |
| AllowPostingFlag | Every row | Control posting | Require explicit Y/N or an unambiguous equivalent |
| AllowBudgetingFlag | Every row | Control budgeting | Require explicit Y/N or an unambiguous equivalent |
| EnabledFlag | Conditional | Control enabled status | Default to Y for text; require file column 6 for CSV/ZIP |
| MaximumLength | Before package generation | Validate value length | Resolve from the exact parent Value Sets GET |
| NaturalAccountUsage | Conditional | Establish whether AccountType is required | Use established Structure Instance context in an end-to-end plan; otherwise accept only an explicit standalone user declaration |
| AccountType | Conditional | Supply Natural Account classification | Require a user-reviewed value for every row only when NaturalAccountUsage is proved or declared; otherwise preserve, validate, and normalize when supplied |
| Execute | Conditional | Distinguish preview from live side effect | Explicit create, update, import, upload, or execute wording requests Data Loader execution after approval |

## Body Field Rules

| Situation | Handling |
|---|---|
| Batch-wide flag | Copy it to every row only when the wording is unambiguous |
| Image cell is unreadable | Report the row/column and ask one consolidated question |
| No exact parent ValueSetCode match | Report that the code doesn't exist and stop before package work |
| Parent lookup has invalid MaximumLength | Report a catalog mismatch and stop; don't default or ask the user to guess it |
| End-to-end Structure Instance context proves Natural Account usage | Require AccountType for every row; suggest from Description only when unambiguous and obtain user acceptance or correction |
| Standalone run with an explicit Natural Account declaration | Require AccountType for every row; suggest from Description only when unambiguous and obtain user acceptance or correction |
| No proof or declaration of Natural Account usage | Leave AccountType blank unless explicitly supplied; don't infer usage from a value set name, value, or description |
| Existing versus new value | Never precheck it; submit the supplied row through Data Loader and report its outcome, with per-value create/update status unavailable unless returned |
| User supplies only a file | Validate and preview; don't upload until live intent is explicit |
| Multiple Value Set Codes | Reject; this skill processes one target value set per run |
| Request to check individual values | This skill doesn't perform value-existence lookups; explain that Data Loader determines the create/update outcome |
| Create/update wording with values | Prepare the FBDI candidate; never query child values before or after handoff |
