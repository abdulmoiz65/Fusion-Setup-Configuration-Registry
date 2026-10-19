# Repeating Time Periods Dependency Readiness

## Source Basis

- Generic FSM Baseline, developer-provided text, used only for the FSM CSV create or edit flow and failure boundaries.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Task inputs and operation rules | Validate task-specific inputs, dependencies, and supported operation rules. |
| 2 | Fresh same-task export and edit identity | Obtain and validate a fresh export for Repeating Time Periods; for edit, match Current Name to exactly one exported row. |
| 3 | Functional-match decision | For create, find and show every exact functional match, then obtain the user's explicit decision to continue with a new period. |
| 4 | Parent CSV contract | Apply the confirmed ORA_HWM_RP_TM_PERIOD parent-row mappings; do not infer its remaining create or edit behavior. |
| 5 | Delta-only change | Use the fresh export only as the mapping and validation baseline. Support every task-scoped CSV member in that export, sending only rows for the approved created or updated periods in each member; do not include unrelated exported periods. |
| 6 | FSM archive validation | Validate exact-case ASM_SETUP_CSV_METADATA.xml, the task-scoped object CSV, valid keys, and approved row scope. |
| 7 | Business-only Complete Summary | After validation, lookup resolution, and defaulting, generate and present the Complete Summary from verified structured UI fields only. |
| 8 | Immutable preview and provider-owned approval | Continue from the Complete Summary to core.data-loader, wait for the immutable package preview, and obtain explicit approval for that current preview. |
| 9 | Import and reconciliation | Import once through the declared FSM route; for edit, reconcile against the exactly matched Current Name row in a fresh same-task export. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| fresh_same_task_export | Fresh Repeating Time Periods export | Yes | A create or edit FSM package is prepared | Verify | Generic FSM Baseline | verify_repeating_time_periods_fsm_export | The FSM ZIP must be based on a fresh export for the same setup task | Obtain a new same-task export and stop if it cannot be obtained or validated | Validated fresh export artifact |
| existing_repeating_time_period | Existing repeating time period identity | Yes | Edit | Verify | User-provided Current Name and fresh Repeating Time Periods FSM export | verify_repeating_time_periods_fsm_export | An edit must target exactly one existing repeating time period without assuming the editable Name is its runtime identity | Provide the existing Repeating Time Period Current Name | Exactly one matching exported row and its current values |
| functional_match_decision | Exact functional matches | Yes | Create | Verify | Validated requested UI configuration and fresh Repeating Time Periods FSM export | find_functionally_matching_repeating_periods | Existing periods with the same functional configuration must be shown before a new period is created | Review every matching period and state whether to create a new period | Every matching period and the user's explicit continue-or-cancel decision |
| known_parent_csv_mappings | Confirmed ORA_HWM_RP_TM_PERIOD mappings | Yes | A create or edit FSM package is prepared | Satisfied | Fresh Repeating Time Periods FSM export and user-confirmed mapping |  | All exported parent rows use ORA_HWM_RP_TM_PERIOD with ViewInstanceName RepeatingTimePeriodMigration. For Create, PeriodCd is uppercase Name preserving characters and is the import key; GroupingKey equals PeriodCd. For Edit, retain the exact existing PeriodCd and GroupingKey even when Name changes. UI Sample Start Date maps to ReferenceDate; selected usages map to Y; and unselected usages map to N in the current UI-created rows. | For Create, require a PeriodCd absent from the fresh export. For Edit, target and retain the exact existing PeriodCd. | ORA_HWM_RP_TM_PERIOD; ViewInstanceName; Name; PeriodCd; GroupingKey; ReferenceDate; TimeEntryUsage; ApprovalUsage; AccrualUsage; OvertimeUsage; BalanceUsage; AttendanceTrackingUsage |
| known_parent_period_definition_mappings | Confirmed parent period-definition mappings | Yes | A create or edit FSM package is prepared | Satisfied | Fresh Repeating Time Periods FSM export |  | Daily rows use PeriodClass DAILY and PeriodType FIXED_DAYS; Monthly rows use MONTHLY, CALENDAR_MONTH, and MonthType CALMONTH; Semimonthly rows use SEMI-MONTHLY and SIMI_MONTH; Weekly rows use WEEKLY and FIXED_WEEKS. One day and More than one day use OneOrMany ONEDAY and MORETHANONE. One week, Biweekly, and More than two weeks use WeekType ONEWEEK, BiWEEK, and MORETHANWEEK. Multiple carries observed day or week quantities. | Preserve the matching observed field combination; leave nonapplicable definition fields blank | PeriodClass; PeriodType; MonthType; OneOrMany; WeekType; Multiple |
| supported_period_definition_combinations | Supported create definitions | Yes | Create FSM package | Satisfied | User-provided support rule, UI skeleton, and fresh export |  | Support Daily One day, Daily More than one day, Monthly Calendar month, Semimonthly, Weekly One week, Weekly Biweekly, and Weekly More than two weeks. | Build the matching confirmed parent-row representation and required conditional inputs for the selected definition. | PeriodClass; PeriodType; MonthType; OneOrMany; WeekType; Multiple; ReferenceDate |
| known_parent_blank_fields | Confirmed blank parent fields | Yes | Create FSM package for every Period Type | Satisfied | Fresh Repeating Time Periods FSM export, user direction, and successful controlled import |  | ModuleId, PeriodLength, RuleUsage, and RepeatingTmPeriodId are blank in all exported parent rows. Populate PeriodStartDate blank for every Period Type as directed. | Use blank values | ModuleId; PeriodLength; RuleUsage; RepeatingTmPeriodId; PeriodStartDate |
| edit_field_preservation | Edit field scope | Yes | Edit FSM package | Satisfied | User-provided edit rule and matched fresh-export row | verify_repeating_time_periods_fsm_export | Only Name and Description are updateable. PeriodCd and every other parent or translation field must retain its exported value. | Copy the matched exported rows; alter only Name and/or Description and preserve PeriodCd and GroupingKey exactly. | Name; Description; PeriodCd; GroupingKey; all other exported fields |
| supported_fsm_csv_members | Exported task-scoped CSV members | Yes | A create or edit FSM package is prepared | Verify | User-provided support rule and fresh export | verify_repeating_time_periods_fsm_export | Every task-scoped CSV member in the fresh export must be supported. | Enumerate every CSV member other than ASM_SETUP_CSV_METADATA.xml and prepare only the rows for the approved periods in each member. | Supported CSV-member list and scoped rows |
| approved_change_scope | Approved task-specific delta | Yes | A create or edit FSM package is prepared | Verify | User-provided change scope and fresh export |  | The FSM payload must contain only approved created or updated Repeating Time Period rows in every supported task-scoped CSV member. The fresh export is a baseline and is not copied wholesale into the import payload. | Identify the created or updated periods and exclude all unrelated exported periods | Approved rows in every supported CSV member |
| validated_fsm_archive | Validated FSM archive | Yes | Before preview or import | Verify | Generic FSM Baseline |  | The archive must retain exact-case ASM_SETUP_CSV_METADATA.xml, the task-scoped object CSV, valid keys, and approved row scope | Rebuild the ZIP and stop when any required evidence is absent | Immutable validated ZIP |
| complete_summary | Business-only Complete Summary | Yes | Before the provider-owned approval process | Verify | Verified structured UI fields after validation, lookup resolution, and defaulting |  | The provider-owned approval process must receive a complete business-only summary containing only UI-exposed values, without technical values or empty sections | Generate Complete Summary and Defaults Applied only when defaults were actually applied | Complete Summary with every populated UI value and applied default |
| current_preview_approval | Current immutable preview approval | Yes | Before import submission | Verify | Generic FSM Baseline |  | Preview and approval evidence cannot be stale | Wait for the immutable preview and obtain explicit approval for that exact preview | Current preview and approval evidence |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required FSM evidence is present and valid | No |
| Verify | A fresh export, archive, preview, approval, or reconciliation evidence must be checked | No |
| Blocked | A task-specific FSM contract or required FSM evidence is absent or invalid | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RTP.CHECK_FSM_READINESS | decision | 40 | resolve_dependency | ready->RTP.ENFORCE_FSM_SAFETY;blocked->RTP.BLOCKED | RTP.CHECK_FUNCTIONAL_MATCHES | stop | A Repeating Time Periods create or edit request is prepared through FSM CSV import |
