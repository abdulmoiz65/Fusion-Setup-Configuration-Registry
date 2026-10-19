# Review and Submit Accounting Configuration Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| select_scoped_ledger_configuration | Filtered export ZIP is available | Exact primary ledger name; ZIP; ASM_SETUP_CSV_METADATA.xml; ORA_GL_PRIMARY_LEDGER_CONFIG.csv; GL_PRIMARY_LEDGER.csv | Require task GL_SPECIFY_LEDGER_OPTIONS, type EXPORT, terminal completed status, one exact configuration root, and ledger rows whose ORA_GL_PRIMARY_LEDGER_CONFIG.Name equals the primary name | Primary row; scoped rows; SECONDARY and ALC candidates; export checksum; process status | Stop with member, metadata, configuration, or row-cardinality diagnostics; never use an unrelated row |
| validate_ledger_options_export | A scoped primary or target secondary row is selected | RetEarnCcidSegments; FirstLedgerPeriodName; CurrencyCode; PeriodSetName; AccountedPeriodType; StructureInstanceCode; EnableAverageBalancesFlag | Require at least one retained-earnings segment, all named nonblank fields, and average flag Y or N | Ledger options readiness; primary average flag; secondary average flag when applicable | Block the ledger and route correction to its owning Specify Ledger Options task |
| select_secondary_ledger_exact | Requested scope is single-secondary | Exact primary name; exact secondary name; selected configuration rows | Match exactly one row under the primary configuration whose Name is exact and LedgerCategoryCode is SECONDARY | Secondary export row; secondary name; category | Zero or many is unresolved; ALC is invalid; stop without choosing another child |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_primary_ledger_by_exact_name | Primary ledger name is supplied | Exact case-sensitive primary name | /fscmRestApi/resources/11.13.18.05/ledgersLOV with q=Name='<exact name>', onlyData=true, limit=10 | LedgerId, Name, LedgerCategoryCode, ChartOfAccountsId, PeriodSetName, AccountedPeriodType | Exactly one row; Name exact; category PRIMARY; period set and type later equal export | PRIMARY_LEDGER_ID; PRIMARY_LEDGER_NAME; PRIMARY_COA_ID; PRIMARY_PERIOD_SET_NAME; PRIMARY_PERIOD_TYPE | Zero is not found; many is ambiguous; non-PRIMARY is wrong role; stop and show candidates safely |
| find_secondary_ledger_by_exact_name | Requested scope is single-secondary and scoped row is selected | Exact target secondary name | /fscmRestApi/resources/11.13.18.05/ledgersLOV with q=Name='<exact name>', onlyData=true, limit=10 | LedgerId, Name, LedgerCategoryCode, ChartOfAccountsId, PeriodSetName, AccountedPeriodType | Exactly one row; Name exact; category SECONDARY; period set and type equal export | SECONDARY_LEDGER_ID; SECONDARY_LEDGER_NAME; SECONDARY_COA_ID; SECONDARY_PERIOD_SET_NAME; SECONDARY_PERIOD_TYPE | Zero, many, or another category blocks the target; never use ALC or first result |
| resolve_ledger_calendar_exact | A primary or secondary payload group is populated | Export PeriodSetName; export AccountedPeriodType | /fscmRestApi/resources/11.13.18.05/accountingCalendarsLOV with q=PeriodSetName='<exact period set>', onlyData=true, limit=10 | CalendarId, PeriodSetName, PeriodType | Exactly one row with exact PeriodSetName and PeriodType equal to export AccountedPeriodType | PRIMARY_CAL_ID or SECONDARY_CAL_ID | Zero is incompatible/not found; many is ambiguous; stop without choosing by position |
| verify_ledger_coa_exact | A primary or secondary ledger LOV row is resolved | ledgersLOV ChartOfAccountsId; export StructureInstanceCode | /fscmRestApi/resources/11.13.18.05/chartOfAccountsLOV with q=StructureInstanceNumber=<ChartOfAccountsId>, onlyData=true, limit=10 | StructureInstanceNumber, StructureInstanceId, StructureInstanceCode | Exactly one row; StructureInstanceNumber equals ChartOfAccountsId and StructureInstanceCode equals export | Confirm payload COA ID from ChartOfAccountsId; retain StructureInstanceId only as non-payload evidence | Zero or many blocks; code mismatch blocks; never substitute StructureInstanceId |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| String literal contains an apostrophe or reserved URL character | Escape the Fusion query literal and use the core client's query encoding; never concatenate untrusted input into a URL |
| Exact response cardinality is one | Record endpoint path, source value, match count, mapped values, evidence time, and sanitized response fingerprint |
| Successful response cardinality is zero or many | Report not found or ambiguous separately and stop; never broaden, fuzzy-match, or select the first result |
| Cached-token GET returns 401 or 403 | Refresh an eligible cached token once, retry that read-only call once, then classify final 401/403 as auth/authz |
| GET returns 429, transient 5xx, timeout, or connection closure | Use only bounded read-only retry and record attempts/correlation evidence |
| Any client, JSON, schema, 400, final auth, or cross-source mismatch occurs | Stop with the actual failure; never translate it to not found |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GLREV.LOOKUPS | decision | 30 | reference_lookup | resolved->GLREV.DEFAULTS;blocked->GLREV.RETURN_ISSUES | GLREV.DEPENDENCIES | stop | Exact export and LOV resolution are required |
