# Review and Submit Accounting Configuration Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Accounting-configuration scope | Exact primary ledger name; requested scope | Stop before any lookup or export | Ask for the exact primary ledger name and one supported scope | Always | find_primary_ledger_by_exact_name |
| Single-secondary scope | Exact parent primary ledger name; exact secondary ledger name | Stop before payload construction | Ask for both names; a secondary name alone cannot derive the accounting configuration | Requested scope is single-secondary | select_secondary_ledger_exact |
| Fusion execution context | Exact environment; project ID; preview or execute intent | Stop before external operation | Resolve one configured environment and active implementation project | Always |  |
| Current filtered export | GL_SPECIFY_LEDGER_OPTIONS export filtered by the resolved primary LedgerId | Stop before readiness evaluation | Preview and approve the exact filtered export request, then download its terminal result | Building a new request | select_scoped_ledger_configuration |
| Mandatory ledger options | Retained Earnings Account; First Opened Period; currency; period set; period type; COA code; average-balance flag | Return the ledger to its owning setup task | Correct Specify Ledger Options and obtain a fresh identical-scope export | Every ledger that the selected mode validates | validate_ledger_options_export |
| LOV evidence | Exact ledger, compatible calendar, and matching COA response | Stop before payload construction | Run the documented read-only LOVs and require exact cardinality and cross-source equality | Building a new request | resolve_ledger_calendar_exact |
| Exact execution approval | Approval bound to environment, export checksum, LOV evidence, scope, full payload, and payload fingerprint | Stop before ESS POST | Show the final preview and obtain explicit approval immediately before submission | Execution intent is execute |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Primary name resolves to exactly one PRIMARY ledger | Satisfied | Use its LedgerId only for the filtered export criterion | find_primary_ledger_by_exact_name |
| Primary lookup resolves zero, many, or a non-PRIMARY category | Blocked | Correct the exact name or environment; never select the first or fuzzy result | find_primary_ledger_by_exact_name |
| Filtered export has one matching configuration root and one matching PRIMARY row | Satisfied | Validate scope rows and ledger options | select_scoped_ledger_configuration |
| Any required option is blank or average-balance flag is outside Y or N | Blocked | Correct the owning primary or secondary Specify Ledger Options task and re-export | validate_ledger_options_export |
| Requested scope is primary-only and any SECONDARY or ALC candidate exists | Blocked | Use configuration or primary-and-related, or prove a different supported product route | select_scoped_ledger_configuration |
| Requested scope is primary-and-related and no related candidate exists | Blocked | Use primary-only or configuration | select_scoped_ledger_configuration |
| Requested scope is single-secondary and exact scoped row is absent, duplicated, or not SECONDARY | Blocked | Correct the parent/target names or complete the secondary-ledger setup first | select_secondary_ledger_exact |
| Calendar and COA identities agree between export and LOVs | Satisfied | Build the deterministic request | resolve_ledger_calendar_exact |
| Existing positive request ID is supplied with a matching checkpoint | Resume | Track the existing request only; do not export or submit another request |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Ledger name normalization | Trim outer whitespace only; blank is missing; preserve case and internal whitespace | Always |  |
| Requested scope enumeration | Accept only primary-only, configuration, primary-and-related, or single-secondary | Always |  |
| Export identity | Require metadata ObjectShortName GL_SPECIFY_LEDGER_OPTIONS, ProcessType EXPORT, and terminal completed status | Export is supplied | select_scoped_ledger_configuration |
| Export members | Require ASM_SETUP_CSV_METADATA.xml, ORA_GL_PRIMARY_LEDGER_CONFIG.csv, and GL_PRIMARY_LEDGER.csv | Export is supplied | select_scoped_ledger_configuration |
| Export row ownership | Select rows only when ORA_GL_PRIMARY_LEDGER_CONFIG.Name equals the exact primary ledger name | Export is supplied | select_scoped_ledger_configuration |
| Retained Earnings Account | Require physical field RetEarnCcidSegments to contain at least one nonblank segment; never look for a guessed RetEarningsAccount header | Every validated ledger | validate_ledger_options_export |
| Other mandatory options | Require nonblank FirstLedgerPeriodName, CurrencyCode, PeriodSetName, AccountedPeriodType, and StructureInstanceCode; require EnableAverageBalancesFlag Y or N | Every validated ledger | validate_ledger_options_export |
| Primary ledger cardinality | Require exactly one scoped PRIMARY row whose Name equals the requested primary and no second PRIMARY row in the configuration | Always | select_scoped_ledger_configuration |
| Secondary ledger cardinality | Require exactly one exact-name scoped SECONDARY row; reject ALC | Requested scope is single-secondary | select_secondary_ledger_exact |
| Integer identities | Require positive decimal LedgerId, ChartOfAccountsId, and CalendarId; serialize them as strings | Building the payload |  |
| COA identity | Require ledgersLOV.ChartOfAccountsId to equal chartOfAccountsLOV.StructureInstanceNumber; never use StructureInstanceId | Each primary or secondary LOV triple | verify_ledger_coa_exact |
| Calendar compatibility | Require PeriodSetName equality and calendar PeriodType equality with export AccountedPeriodType | Each primary or secondary LOV triple | resolve_ledger_calendar_exact |
| Approval fingerprint | Invalidate approval when environment, scope, export, LOV evidence, parameter, or payload changes | Immediately before ESS POST |  |

## ESS Payload Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Envelope fields | Require exactly description, jobDefinitionId, application, product, and requestParameters using the fixed values in ora_defaulting_rules.md | Payload preview is built |  |
| Parameter object shape | Require exactly name, paramType, and value for every item; value must be a JSON string | Every requestParameters item |  |
| Parameter count and order | Require exactly 40 unique parameter names in positions 1 through 40 from ora_defaulting_rules.md | Payload preview is built |  |
| Boolean parameter encoding | Require paramType BOOLEAN with string value false at positions 28 and 29 and string value true at position 33 | Payload preview is built |  |
| REVIEW_SUBMIT secondary group | Require positions 10 through 16 to exist with empty-string values | Requested scope is primary-only, configuration, or primary-and-related |  |
| SECONDARY_LEDGER groups | Require positions 3 through 16 to use independently validated primary and exact secondary evidence | Requested scope is single-secondary | select_secondary_ledger_exact |
| Display triple | Require positions 38 and 39 to use the scenario target and position 40 to equal position 38 + literal X + position 39 | Every payload |  |
| Forbidden fields | Reject callbackSubscription, SYS_className, an SL array, a caller-supplied child list, and any uncontracted envelope or parameter field | Every payload |  |
| Evidence freshness | Require the payload values to be built from the current scoped export and current exact LOV responses, not copied from an earlier request | Every new submission |  |
| Payload fingerprint | Require SHA-256 over canonical UTF-8 JSON with sorted object keys and compact separators | Before approval |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GLREV.VALIDATE | decision | 10 | validate_input | valid->GLREV.DEPENDENCIES;invalid->GLREV.RETURN_ISSUES | none | stop | Always |
