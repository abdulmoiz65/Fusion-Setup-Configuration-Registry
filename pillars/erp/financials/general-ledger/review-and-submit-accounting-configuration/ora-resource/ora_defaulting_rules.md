# Review and Submit Accounting Configuration Defaulting Rules

This file is the task-local source of truth for constructing the filtered
export request and the AccountingConfigSetup ESS request. Assemble from these
tables; do not copy a prior tenant payload or use a task-local script.

## Client and Job Contract

| Contract Field | Required Value or Route |
|---|---|
| Submit method and path | POST /ess/rest/scheduler/v1/requests |
| Track method and path | GET /ess/rest/scheduler/v1/requests/{requestId} |
| Job definition ID | JobDefinition://oracle/apps/ess/financials/generalLedger/ledgers/ledgerDefinitions/AccountingConfigSetup |
| Application | FscmEss |
| Product | GENERAL-LEDGER |
| Job definition application | GL |
| Job definition name | AccountingConfigSetup |
| Display name | Complete Accounting Configuration |
| Submit success | HTTP 201 with one positive numeric id; store that id as requestId |
| Direct standard REST capability | core/fusion-api/rest-api-client/scripts/fusion_rest_client.py accepts the ESS path with method POST and a JSON body file |
| Task execution route | core/fusion-api/ess-job-submitter/scripts/ess_job_submitter.py with payload-file; it submits once and tracks the singular request resource |
| FSM client disposition | core.fusion-api.fsm-rest-client delegates non-BOSS standard Fusion REST to core.fusion-api.rest-api-client; it is not a separate generic request executable |

The setup-task code is not the ESS job definition. Never derive or substitute
the job definition from GL_REVIEW_AND_SUBMIT_ACCOUNTING_CONFIGURATION.

## Filtered Export Request Contract

| JSON Path | Required Value | Value Source |
|---|---|---|
| TaskCode | GL_SPECIFY_LEDGER_OPTIONS | Fixed |
| SetupTaskCSVExportCriteria[0].TaskCode | GL_SPECIFY_LEDGER_OPTIONS | Fixed |
| SetupTaskCSVExportCriteria[0].BusinessObjectCode | GL_PRIMARY_LEDGER | Fixed |
| SetupTaskCSVExportCriteria[0].AttributeSet | Set1 | Fixed |
| SetupTaskCSVExportCriteria[0].AttributeName | PRIMARY_LEDGER_ID | Fixed |
| SetupTaskCSVExportCriteria[0].AttributeValue | Positive primary LedgerId serialized as a string | Exact PRIMARY ledgersLOV match |
| SetupTaskCSVExportProcess[0].TaskCode | GL_SPECIFY_LEDGER_OPTIONS | Fixed |

The request contains one criteria object and one process object. Reject extra
criteria, an SL ID in AttributeValue, or any caller override to a fixed value.

## Scenario Matrix

| Requested Scope | FROM_PAGE | Primary Parameter Group | Secondary Parameter Group | submit.argument14 | submit.argument15 | submit.argument16 |
|---|---|---|---|---|---|---|
| primary-only | REVIEW_SUBMIT | Populate from exact primary evidence | Seven empty strings; only valid when no SECONDARY or ALC candidate exists | PRIMARY_COA_ID | PRIMARY_CAL_ID | PRIMARY_COA_ID + literal X + PRIMARY_CAL_ID |
| configuration | REVIEW_SUBMIT | Populate from exact primary evidence | Seven empty strings; product resolves eligible relationships | PRIMARY_COA_ID | PRIMARY_CAL_ID | PRIMARY_COA_ID + literal X + PRIMARY_CAL_ID |
| primary-and-related | REVIEW_SUBMIT | Populate from exact primary evidence | Seven empty strings; require at least one related candidate but do not enumerate it | PRIMARY_COA_ID | PRIMARY_CAL_ID | PRIMARY_COA_ID + literal X + PRIMARY_CAL_ID |
| single-secondary | SECONDARY_LEDGER | Populate from exact parent primary evidence | Populate from one exact true SECONDARY row and its independent LOV evidence | SECONDARY_COA_ID | SECONDARY_CAL_ID | SECONDARY_COA_ID + literal X + SECONDARY_CAL_ID |

## Request Envelope Contract

| Envelope Field | Required Value | Override Rule |
|---|---|---|
| description | FDOS Review and Submit - followed by the exact primary ledger name | A caller may provide a nonblank audit description before preview; any change invalidates approval |
| jobDefinitionId | JobDefinition://oracle/apps/ess/financials/generalLedger/ledgers/ledgerDefinitions/AccountingConfigSetup | Never override |
| application | FscmEss | Never override |
| product | GENERAL-LEDGER | Never override |
| requestParameters | Exactly 40 parameter objects in the position order below | Never reorder, omit, duplicate, or append |

Each requestParameters item has exactly name, paramType, and value. Use the
declared paramType and serialize every value as a JSON string, including values
whose paramType is BOOLEAN. Do not add callbackSubscription or SYS_className.

## Request Parameter Contract

| Position | Name | Param Type | Value Source or Fixed Value |
|---|---|---|---|
| 1 | EXT_PortletContainerWebModule | STRING | ORA_FSCM_UI |
| 2 | FROM_PAGE | STRING | Scenario Matrix |
| 3 | PRIMARY_AVERAGE_FLAG | STRING | Primary export EnableAverageBalancesFlag |
| 4 | PRIMARY_CAL_ID | STRING | Compatible primary accountingCalendarsLOV CalendarId |
| 5 | PRIMARY_COA_ID | STRING | Primary ledgersLOV ChartOfAccountsId, equal to COA LOV StructureInstanceNumber; never StructureInstanceId |
| 6 | PRIMARY_LEDGER_ID | STRING | Primary ledgersLOV LedgerId |
| 7 | PRIMARY_LEDGER_NAME | STRING | Exact primary export and ledgersLOV Name |
| 8 | PRIMARY_PERIOD_SET_NAME | STRING | Exact primary export and ledgersLOV PeriodSetName |
| 9 | PRIMARY_PERIOD_TYPE | STRING | Exact primary export and ledgersLOV AccountedPeriodType |
| 10 | SECONDARY_AVERAGE_FLAG | STRING | Exact secondary export EnableAverageBalancesFlag for single-secondary; otherwise empty string |
| 11 | SECONDARY_CAL_ID | STRING | Compatible secondary accountingCalendarsLOV CalendarId for single-secondary; otherwise empty string |
| 12 | SECONDARY_COA_ID | STRING | Secondary ledgersLOV ChartOfAccountsId, equal to COA LOV StructureInstanceNumber and never StructureInstanceId, for single-secondary; otherwise empty string |
| 13 | SECONDARY_LEDGER_ID | STRING | Secondary ledgersLOV LedgerId for single-secondary; otherwise empty string |
| 14 | SECONDARY_LEDGER_NAME | STRING | Exact secondary export and ledgersLOV Name for single-secondary; otherwise empty string |
| 15 | SECONDARY_PERIOD_SET_NAME | STRING | Exact secondary export and ledgersLOV PeriodSetName for single-secondary; otherwise empty string |
| 16 | SECONDARY_PERIOD_TYPE | STRING | Exact secondary export and ledgersLOV AccountedPeriodType for single-secondary; otherwise empty string |
| 17 | TENANT_NAME | STRING | GLOBAL |
| 18 | TENANT_UUID | STRING | 00000000-0000-0000-0000-000000000000 |
| 19 | aflogLevel | STRING | N |
| 20 | completionText | STRING | Empty string |
| 21 | cpAsynchJobWrapper | STRING | oracle.apps.fnd.applcp.request.exec.AsyncExecutableWrapper |
| 22 | cpJavaJobWrapper | STRING | oracle.apps.fnd.applcp.request.exec.ExecutableWrapper |
| 23 | cpSqlFileFlag | STRING | F |
| 24 | currentSubRequestId | STRING | 0 |
| 25 | filePersistenceMode | STRING | content |
| 26 | jobDefinitionApplication | STRING | GL |
| 27 | jobDefinitionName | STRING | AccountingConfigSetup |
| 28 | jobExecutesVirusScanOnLogFiles | BOOLEAN | false serialized as a string |
| 29 | jobExecutesVirusScanOnOutputFiles | BOOLEAN | false serialized as a string |
| 30 | jobPackageName | STRING | /oracle/apps/ess/financials/generalLedger/ledgers/ledgerDefinitions |
| 31 | logLevel | STRING | 1 |
| 32 | numberOfArgs | STRING | 18 |
| 33 | oracle.apps.fnd.applcp.invokeIncrementProcIfPresent | BOOLEAN | true serialized as a string |
| 34 | parentRequest | STRING | 0 |
| 35 | requestStepPath | STRING | Empty string |
| 36 | shadowClassName | STRING | oracle.apps.financials.generalLedger.ledgers.ledgerDefinitions.ess.program.AccountingConfigSetup |
| 37 | srsFlag | STRING | N |
| 38 | submit.argument14 | STRING | Scenario Matrix target COA ID |
| 39 | submit.argument15 | STRING | Scenario Matrix target calendar ID |
| 40 | submit.argument16 | STRING | Position 38 value + literal X + position 39 value, with no whitespace |

## Assembly and Fingerprint Rules

| Sequence | Assembly Rule | Failure Behavior |
|---|---|---|
| 1 | Build the five-field envelope from Request Envelope Contract | Stop on missing, extra, or overridden fixed envelope fields |
| 2 | Select exactly one row from Scenario Matrix using requested scope | Stop on unsupported or ambiguous scope |
| 3 | Append positions 1 through 40 in ascending order using fresh export and LOV evidence | Stop on missing source value, duplicate name, wrong type, wrong order, or count other than 40 |
| 4 | For REVIEW_SUBMIT, keep positions 10 through 16 present with empty-string values | Stop if related ledgers are enumerated or any secondary value is populated |
| 5 | For SECONDARY_LEDGER, populate both primary and secondary groups and use the secondary display triple at positions 38 through 40 | Stop if the parent group, exact target, or independent target LOV evidence is absent |
| 6 | Canonicalize the completed envelope with sorted object keys, UTF-8, and compact separators, then calculate SHA-256 | Treat any payload or fingerprint change as invalidating approval |

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| description | FDOS Review and Submit - followed by exact primary ledger name | Caller did not supply an audit description | Yes, before preview only |  |
| FROM_PAGE | REVIEW_SUBMIT | Requested scope is primary-only, configuration, or primary-and-related | No |  |
| FROM_PAGE | SECONDARY_LEDGER | Requested scope is single-secondary | No |  |
| Positions 10 through 16 | Empty string | FROM_PAGE is REVIEW_SUBMIT | No; related ledgers are product-resolved |  |
| Approval | No default | Every mutating external step | No; require exact immediate approval |  |
| Retry count | Zero automatic POST retries | Every filtered export, ESS submit, and verification export | No |  |
| Optional secondary name | No default | Scope is not single-secondary | No; reject a supplied value outside single-secondary |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GLREV.DEFAULTS | step | 40 | apply_default | applied->GLREV.ENFORCE | GLREV.LOOKUPS | stop | Exact resolved values are available |
