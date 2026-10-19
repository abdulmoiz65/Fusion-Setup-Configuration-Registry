# Value Set Value Defaulting Rules

## Standard Defaults

| Field | Default | Applies When | Override Explicit Input? |
|---|---|---|---|
| EnabledFlag | Y | Natural-language input omits it | No |
| ThirdPartyControlAccount | N | Natural Account usage is proved or declared, or a row with AccountType supplied omits it | No |
| ReconcileFlag | N | Natural Account usage is proved or declared, or a row with AccountType supplied omits it | No |
| STATUS_CODE | NEW | FBDI control-file load | System constant; not a CSV column |
| OBJECT_VERSION_NUMBER | 1 | FBDI control-file load | System constant; not a CSV column |
| LOAD_REQUEST_ID and audit fields | Loader assigned | FBDI load | System assigned; not CSV columns |
| Is Validated | Blank | Every generated CSV row | Yes; never trust workbook validation state as import data |

CSV and ZIP input must contain Enabled Flag in position 6; don't silently
default a missing file field. Preserve explicit valid Natural Account control
and reconcile values.

## Never Default

| Field | Reason |
|---|---|
| ValueSetCode | Selects the import target |
| Value | Identifies the requested member |
| SummaryFlag | Business behavior |
| AllowPostingFlag | Business behavior |
| AllowBudgetingFlag | Business behavior |
| AccountType | Financial classification for Natural Account values |
| MaximumLength | Authoritative constraint returned by the exact parent Value Sets lookup |
| StartDate and EndDate | Effective-dating decision |
| FinancialCategory | Reporting classification |

Defaulting occurs only in the locally prepared candidate before FBDI package
generation. Report every applied default in the preview.
