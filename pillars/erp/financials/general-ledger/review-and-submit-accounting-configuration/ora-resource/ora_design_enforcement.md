# Review and Submit Accounting Configuration Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Bind scope | Resolve one exact primary-ledger accounting configuration and one supported requested scope |
| 2 | Prove options readiness | Validate retained earnings and every other mandatory export field for all ledgers required by the mode |
| 3 | Prove runtime identities | Cross-check export values against exact ledger, calendar, and COA LOV results |
| 4 | Enforce product scope semantics | Keep REVIEW_SUBMIT configuration-wide and SECONDARY_LEDGER bound to one exact true secondary |
| 5 | Freeze exact preview | Render full payload, related candidates, irreversible effect, and fingerprint |
| 6 | Require accountable approval | Obtain approval immediately before the unchanged ESS POST |
| 7 | Prevent duplicate mutation | Submit once and reconcile the original request before any new submission is considered |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Always | Error | find_primary_ledger_by_exact_name | Primary name does not resolve exactly once as PRIMARY in the target environment | Correct the exact name/environment | Yes, input only |
| Building a new request | Error | select_scoped_ledger_configuration | Export task, type, terminal status, required members, configuration root, or PRIMARY row is missing or ambiguous | Obtain a fresh approved filtered export and use only its exact configuration group | Yes, new export with approval |
| Any validated ledger | Error | validate_ledger_options_export | RetEarnCcidSegments is blank, FirstLedgerPeriodName or a foundational identity is blank, or average flag is invalid | Complete the owning Specify Ledger Options task and re-export | Yes, owning workflow |
| A non-Standard accounting method was requested for a newly FDoS-created ledger | Error | validate_ledger_options_export | The requested method handoff is incomplete or an identical-scope re-export does not verify it | Complete the correct primary- or secondary-ledger UI handoff; readiness remains blocked until re-export | Yes, owning UI workflow |
| Requested scope is primary-only | Error | select_scoped_ledger_configuration | Any SECONDARY or ALC candidate row exists and relationship-level eligibility cannot be proven absent from this export | Use configuration/primary-and-related or a separately documented narrower product route | No automatic reinterpretation |
| Requested scope is configuration or primary-and-related | Warning | select_scoped_ledger_configuration | Caller expects only true SL rows or a selected child subset | Disclose that the job may include eligible SECONDARY and ALC relationships and does not accept a child array | Yes, correct scope choice |
| Requested scope is single-secondary | Error | select_secondary_ledger_exact | Target is absent, duplicated, outside the parent group, or category ALC/PRIMARY | Provide one exact SECONDARY under the exact primary | Yes, input/setup correction |
| Calendar or COA is resolved | Error | resolve_ledger_calendar_exact | Export and LOV period/COA identities disagree or caller uses StructureInstanceId | Use the exact compatible CalendarId and ChartOfAccountsId/StructureInstanceNumber | Yes, rebuild from evidence |
| Payload is ready | Error |  | Caller changes fixed job definition, wrappers, tenant constants, argument count, order, or source mapping | Reassemble from the exact contract in ora_defaulting_rules.md and revalidate | No manual payload editing |
| Approval is requested | Error |  | Environment, scope, export checksum, LOV evidence, full payload, fingerprint, or irreversible effect is absent | Show the complete preview and bind a new approval | Yes, preview only |
| Prior POST is failed, timed out, or indeterminate | Error |  | Automatic retry or replacement submission is proposed | Reconcile and track the original identity; require new preview/approval for any later POST | No blind retry |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_primary_ledger_by_exact_name | Always | Primary LedgerId, ChartOfAccountsId, category, period set, and period type | ora_reference_lookups.md |
| select_scoped_ledger_configuration | Building a new request | Exact configuration root, scoped rows, related candidates, metadata status, and checksum | ora_reference_lookups.md |
| validate_ledger_options_export | Each ledger required by mode | Retained earnings, first period, currency, period identities, COA code, and average flag | ora_reference_lookups.md |
| select_secondary_ledger_exact | Requested scope is single-secondary | Exact SECONDARY row under the exact primary | ora_reference_lookups.md |
| resolve_ledger_calendar_exact | Each populated ledger group | Compatible CalendarId | ora_reference_lookups.md |
| verify_ledger_coa_exact | Each populated ledger group | ChartOfAccountsId equals StructureInstanceNumber and code agrees | ora_reference_lookups.md |

## Execution Route Contract

| Capability | Repository Evidence | Required Task Use |
|---|---|---|
| FSM REST client | core.fusion-api.fsm-rest-client explicitly delegates standard non-BOSS Fusion REST calls to core.fusion-api.rest-api-client and does not expose a generic fsm_rest_client executable | Do not invent or add a task-local FSM client; follow the delegated standard REST route |
| Generic Fusion REST client | fusion_rest_client.py accepts relative Fusion endpoints, POST, and JSON body-file input, so it can technically call /ess/rest/scheduler/v1/requests | Use for documented standard REST operations only when the active workflow selects it; it does not replace ESS-specific checkpoint and polling behavior |
| ESS job submitter | ess_job_submitter.py accepts the complete payload-file, submits to the Scheduler endpoint, returns requestId, polls the singular request, and supports request-id resume | Required executor for the approved AccountingConfigSetup request |
| Filtered setup export | shared.setup-export.task-level-export owns the approved export creation, ProcessId polling, FileContent download, and ProcessLog retrieval | Do not replace it with exploratory browser or an untracked direct POST |
| Payload construction | SKILL.md plus the exact tables in this ora-resource package own all input, lookup, default, mapping, validation, and error behavior | Build in memory or transient untracked storage; no task-local references, scripts, tests, payload templates, or copied tenant payloads |

## Contract Disposition

| Contract | Status | Consequence |
|---|---|---|
| GL-03 | Closed | PRIMARY, SECONDARY, and ALC rows are classified by exact category without treating ALC as SL |
| GL-07 | Closed by this reviewed task contract | Exact filtered export, LOV mapping, deterministic payload, approval, single-submit, polling, recovery, and post-submit verification are defined |
| GL-09 | Closed | Optional ledger options remain owned by their setup tasks; this task validates required readiness without defaulting optional design |
| GL-12 | Closed | Posting-cutoff policy remains owned by Specify Ledger Options and is not invented during submission |
| GL-13 | Closed | Custom journal conversion rules remain owning-task/UI work and must be re-exported before submission |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GLREV.ENFORCE | decision | 50 | design_enforcement | passed->GLREV.ERROR_POLICY;blocked->GLREV.ERROR_POLICY | GLREV.DEFAULTS | stop | Defaults and exact evidence are available |
