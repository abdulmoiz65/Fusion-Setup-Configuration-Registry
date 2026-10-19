# Manage Ledger Sets Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Task identity and inputs | Establish selected environment, setup access, Name/ShortName shape and requested members; use the packaged create contract. |
| 2 | Header and candidate identities | Resolve the selected structure/calendar/period tuple and each intended member. |
| 3 | Template, scoped structure and conditional state | Validate the current template and acquire the resolved primary ledger's scoped export through the declared shared export steps. COA export is conditional on a named required structural gap. Existing membership is required only for nested members or affected update/review facts. |
| 4 | Relationship and DFF evidence | Supply these only when classification or requested flexfield changes require them. |
| 5 | Core execution handoff | Complete validation of immutable bytes, then use the existing Data Loader approval/execution route. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| task_package | Current task package and prepared candidate | Yes | FSM writes | Verify | Explicitly designated source/candidate files | inspect_ledger_set_package | Loader must receive a task-specific immutable archive | Use current template for shape; acquire populated baseline only for facts that need it | Headers, XML contract, digest, exact row graph |
| technical_create_profile | Packaged explicit create contract | Yes | FSM create | Verify | MLS_FSM_CREATE_V1 in ora_defaulting_rules.md and current template | resolve_ledger_set_create_profile | Initialization must be explicit and field/type compatible | Apply built-in rules; report concrete differences rather than missing project qualification | Profile ID, field dispositions and compatibility result |
| unique_ledger_set_name | Current exact-name precheck | Yes | All | Lookup | Both declared current ledger/name LOV sources | find_ledger_set_by_exact_name | Create must stop for an observed existing L or S identity | Run fresh checks; zero successful results mean no conflict observed in the queried scope | Identity/conflicts, paging status and scope disclosure |
| unique_short_name | Independent current short-name precheck | Conditional | FSM create supplies or derives ShortName | Lookup | Declared current short-name LOV | find_ledger_set_by_exact_short_name | Name and ShortName checks are independent | Check the derived or supplied value; conflict requires another short name | Checked short identity, conflicts and scope disclosure |
| accounting_structure | Member COA/calendar/period tuple | Yes | Create or structural/membership update | Verify | Member LOV and current designated evidence for nested members | find_ledger_by_exact_name | Labels alone do not prove structure compatibility | Resolve each effective member; use the separate COA/calendar dependencies for import keys | Member identifiers and tuples |
| coa_import_keys | Selected enabled COA and import instance code | Yes | Create or supported structure update | Lookup | Current documented chartOfAccountsLOV | resolve_ledger_set_chart_of_accounts | Import code is different from the display name and structure instance ID | Resolve the user's chart directly and compare its StructureInstanceNumber to member ChartOfAccountsId | Name, StructureInstanceCode, StructureInstanceNumber and separate StructureInstanceId |
| calendar_import_keys | Selected calendar display/internal keys and period type | Yes | Create or supported calendar update | Lookup | Current documented accountingCalendarsLOV | resolve_ledger_set_accounting_calendar | Internal calendar name cannot be guessed from the display name | Resolve the selected calendar directly and compare every member's period tuple | CalendarId, PeriodSetName, UserPeriodSetName, PeriodType |
| balancing_column | Selected COA balancing segment column | Conditional | Candidate requires BalSegColumnName | Lookup | Documented member ledger structural lookup | resolve_ledger_set_balancing_segment_column | A sampled SEGMENT1 value is not a universal default | Resolve the balancing column from exact compatible effective-member evidence | BalSegColumnName |
| structural_create_profile | Fresh allowlisted shared structural values | Yes | FSM create | Verify | Current ledger-scoped Manage Primary Ledgers export, declared lookups and packaged field dispositions; conditional COA evidence for a named required gap | resolve_ledger_set_structural_profile | Members establish compatibility; supplied or resolved chart and selected calendar establish import keys | Extract only the exact primary row's structural values; apply packaged omissions and do not copy primary accounting options. No mandatory COA export or historical set profile | Scope/identity receipt, balancing pair, supported management pair or omission, compatible reference keys and named required gaps |
| conditional_coa_metadata | Unresolved required structural value or role | Conditional | Named required gap remains after scoped export/lookups/packaged rules, or no valid primary anchor exists | Verify | Separately approved current COA structure-instance export | resolve_ledger_set_structural_profile | Extra export must address a concrete gap | Explain the exact field/key and additional scope before export approval; optional base-profile omissions do not trigger it | Exact selected-instance role joins for the missing value |
| existing_assignments | Direct and flattened membership | Yes | Update/review or nested member | Verify | Current FSCR task export, declared endpoint results or an already configured declared FSCR report adapter output | inspect_ledger_set_evidence | An assignment delta requires a complete baseline | Obtain direct membership and expand nested members through the framework; missing required facts block without a UI fallback | Existing header, membership and default; distinguish derived expansion from independent flattened evidence |
| currency_eligibility | Monetary classification currency | Conditional | Nonblank classification | Lookup | Documented currency LOV and designated currency eligibility evidence | resolve_ledger_set_currency | Classified members need an exact currency | Supply exact currency code and current enabled facts | Resolved currency |
| gaap_relationships | Primary and secondary ledger family/level | Conditional | GAAP view | Verify | Designated authorized relationship evidence | inspect_ledger_set_evidence | Category/name alone does not establish family or conversion level | Obtain relationship evidence for each secondary and primary | Primary root, eligible secondary relationships |
| dff_configuration | Deployed context and segment schema | Conditional | DFF supplied or tenant requires it | Verify | Designated deployed flexfield evidence | inspect_ledger_set_evidence | Segment names/value sets differ by tenant | Supply deployed context mapping, requiredness and allowed values | DFF contract |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Framework evidence gap | Required facts are absent from the declared endpoints/exports and no configured declared FSCR metadata/report adapter supplies them | Stop the affected operation as missing_framework_evidence; no UI access, ad hoc SQL or invented endpoint |
| Satisfied | Exact identities and complete designated evidence resolve | Applicable read-only resolver only |
| Lookup | The documented key/source is available but unresolved | Applicable read-only resolver only |
| Blocked | Missing, partial, stale, mismatched or unauthorized dependency evidence | No implicit dependent-object creation |

Creation readiness is satisfied by compatible current template bytes, packaged explicit rules, completed fresh negative identity prechecks, fresh member/reference results and validated structural values from the primary-ledger-scoped export with explicit field dispositions. A separate COA export is not a standard dependency; it addresses only a named required gap. There is no dependency on another project, a full Manage Ledger Sets export, a controlled-test receipt or a global inventory certificate. Extra nested membership, GAAP relationship, requested default and required/requested DFF evidence remains conditional. The stricter tenant-wide duplicate policy applies only when explicitly selected; known access restrictions and incomplete/failed reads always block the affected check. Preparation readiness does not assert Oracle import acceptance.

## Evidence Scope

| Situation | What Happens |
|---|---|
| Compatible multiple members | A scoped primary export may include family rows, but returned rows do not become requested assignments. Resolve every intended member independently; include only the requested direct relationships in the candidate. |
| Nested member | Obtain current direct membership and classification of the selected set and every reachable nested set before validating the proposed final graph. The structural anchor is a resolved eligible primary family, not the nested set's display name. |
| No DFF source | Block only the required/requested DFF operation and identify the missing deployed mapping/value-set contract. A successful blank optional-DFF create does not establish a segment-write contract. |
| Missing selected calendar display name | Treat this as an unresolved business selection under the declared calendar resolver, not a reason to export all ledger sets or ask for historical evidence. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MLS.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | ready->MLS.APPLY_DEFAULTS;blocked->MLS.HANDLE_ERROR | MLS.RESOLVE_REFERENCES | stop | Evaluate operation-specific dependencies using declared FSCR endpoint/export evidence; missing framework facts block without UI fallback, invented endpoints or implicit dependent-object creation. |
