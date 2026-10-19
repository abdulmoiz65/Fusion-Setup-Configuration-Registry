# Review and Submit Accounting Configuration Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Environment and project | Bind every external operation and durable receipt to one exact target and active project |
| 2 | Primary ledger identity | Resolve one exact PRIMARY ledger and retain its positive LedgerId and ChartOfAccountsId |
| 3 | Filtered options export | Create only the approved primary-ledger criterion, poll the same ProcessId, and download the current ZIP |
| 4 | Configuration and options | Select the exact configuration group and prove mandatory ledger options from export values |
| 5 | Runtime LOV identities | Resolve independent exact ledger, calendar, and COA triples for every populated payload group |
| 6 | Payload and approval | Assemble the exact envelope and ordered 40 parameters from ora_defaulting_rules.md, validate them, and obtain approval bound to the fingerprint |
| 7 | Original request reconciliation | On resume or uncertainty, track the same request identity before any new mutation is considered |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| execution_context | Exact Fusion environment and project | Yes | Always | Satisfied only when unambiguous | Configured environment and implementation project |  | Prevent cross-environment execution and lost audit state | Select one environment and project before external work | Environment identity; project ID |
| primary_ledger | Exact primary ledger | Yes | Always | Lookup | User primary ledger name | find_primary_ledger_by_exact_name | The export criterion and ESS configuration derivation require the primary LedgerId | Provide the exact primary ledger name | PRIMARY_LEDGER_ID; PRIMARY_LEDGER_NAME; PRIMARY_COA_ID; period set; period type |
| filtered_export | Current scoped Specify Ledger Options export | Yes | Building a new request | Verify | Approved GL_PRIMARY_LEDGER PRIMARY_LEDGER_ID criterion and returned FileContent | select_scoped_ledger_configuration | Runtime flags and retained earnings are export-owned and the configuration group must be current | Approve the exact export request and retain its ProcessId/checksum | Configuration rows; average flag; option fields; related candidates; checksum |
| primary_options | Primary ledger options | Yes | Building a new request | Verify | Exact scoped PRIMARY export row | validate_ledger_options_export | Review and Submit must not run before mandatory ledger options exist | Complete Retained Earnings Account and other required primary options | Primary options readiness |
| requested_secondary | Exact secondary ledger | Conditional | Requested scope is single-secondary | Lookup | Exact scoped SECONDARY row plus exact ledgersLOV | select_secondary_ledger_exact | SECONDARY_LEDGER mode needs one target and its parent primary | Provide the exact parent primary and target secondary names | Secondary export row; target identity |
| secondary_options | Secondary ledger options | Conditional | Requested scope is single-secondary | Verify | Exact scoped SECONDARY export row | validate_ledger_options_export | A single-secondary completion must not use incomplete target options | Complete the secondary options and obtain a fresh scoped export | Secondary options readiness |
| calendar_identity | Compatible calendar identity | Yes | Building a new request | Lookup | Export PeriodSetName/AccountedPeriodType plus accountingCalendarsLOV | resolve_ledger_calendar_exact | ESS needs a CalendarId that matches the ledger period contract | Resolve one compatible row per populated ledger group | PRIMARY_CAL_ID; SECONDARY_CAL_ID when applicable |
| coa_identity | Matching COA identity | Yes | Building a new request | Verify | ledgersLOV ChartOfAccountsId plus export code and chartOfAccountsLOV | verify_ledger_coa_exact | StructureInstanceId is not the job's COA parameter | Require one matching StructureInstanceNumber and code | PRIMARY_COA_ID; SECONDARY_COA_ID when applicable |
| exact_approval | Exact ESS approval | Yes | Execution intent is execute | Blocked until approved | Final preview and payload fingerprint |  | Accounting configuration completion is consequential and the POST is not safely replayable | Approve the unchanged environment, scope, and full payload immediately before submission | Approval receipt; payload fingerprint |
| original_request | Original ESS request identity | Conditional | request_id exists or submit result is uncertain | Verify | Submission checkpoint and singular ESS request GET |  | Duplicate submissions must be prevented | Resume the same request; never auto-resubmit | requestId; state; phase; ECID; terminal result |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact current local or live evidence proves the dependency | Continue to next declared step |
| Lookup | A documented read-only LOV can resolve the value | Read-only lookup only |
| Verify | Evidence exists and must be checked without changing it | Read-only or local validation only |
| Blocked until approved | A filtered export or ESS POST is ready but lacks exact immediate approval | No mutation |
| Blocked | Input, scope, options, cardinality, identity, or prior-request state is unresolved | No create or submit |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GLREV.DEPENDENCIES | decision | 20 | resolve_dependency | ready->GLREV.LOOKUPS;blocked->GLREV.RETURN_ISSUES | GLREV.VALIDATE | stop | Validated input exists |
