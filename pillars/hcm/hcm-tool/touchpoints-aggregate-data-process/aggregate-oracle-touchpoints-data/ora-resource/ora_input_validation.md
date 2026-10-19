# Aggregate Oracle Touchpoints Data Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Execution context | project_id, configured Fusion environment | Stop before preview | Select an initialized project with an active Run Book and configured Fusion environment | Every new submission | |
| Run date | run_date in YYYY-MM-DD | Apply the documented current-date default | Resolve once in the configured project or environment timezone | New one-off submission only | |
| Worker count | number_of_workers | Apply the documented default of 4 | Accept one integer from 1 through 20 | Every new submission | |
| Run type | run_type | Apply the documented default ORA_HRE_FULL_RUN | Accept ORA_HRE_FULL_RUN or ORA_HRE_INCREMENTAL_RUN | Every new submission | |
| Polling settings | wait_seconds and poll_interval | Use the core submitter defaults and show them in review | Require positive bounded integers; daily schedule creation uses wait_seconds 1 and poll_interval 1 with full-status for bounded readback | Every new submission | |
| Implementation context | operation_intent and parent workflow state/evaluation with matching project_id, environment and configuration_revision | Stop before implementation preview | Load the parent implementation workflow and its current persisted state; do not classify implementation work as standalone to bypass its gate | Implementation Full or daily scheduling | |
| Daily recurrence inputs | start date, daily time, named timezone, offset-bearing first occurrence, and explicit end/no-end decision | Stop before schedule preview | Resolve business schedule requirements using references/daily-schedule.md | Daily Incremental scheduling | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Project Run Book status is active and the configured environment is available | Valid | Continue to default resolution | |
| Project Run Book status is absent, pending, failed, or unknown | Blocked | Stop before any Fusion request and repair or activate the project Run Book | |
| Environment identity is unresolved | Blocked | Resolve the exact environment before preview; Fusion enforces ESS authorization on execution without a separate privilege probe | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Run date format | Accept one valid ISO date in YYYY-MM-DD; reject a malformed or past date | run_date is supplied | |
| Worker count type and range | Accept an integer from 1 through 20; reject zero, negative, fractional, nonnumeric, or greater values | number_of_workers is supplied | |
| Run type enum | Accept only ORA_HRE_FULL_RUN or ORA_HRE_INCREMENTAL_RUN | run_type is supplied | |
| Parameter count and order | Require exactly submit.argument1 followed by submit.argument2 | A payload is prepared | |
| Date exclusion | Reject a payload that sends run_date as submit.argument3 or any other business parameter | A payload is prepared | |
| Approval timing | Accept approval only after the exact current review and immediately before submission | A live submission is requested | |
| Operation classification | Accept implementation_full, daily_incremental_schedule, standalone_run or track_existing; classification must agree with the requested objective and persisted project scope | Every invocation | |
| Workflow evidence shape | Require same-context parent state, evidence references and readiness confirmation; daily scheduling additionally requires the Full request identity and terminal evidence | Implementation submission | |
| Recurrence shape | Exactly one schedule.recurrences entry with icalString FREQ=DAILY;INTERVAL=1; (including the final semicolon) and ISO startDate; optional explicit endDate; executePast false; no scheduleId or top-level startTime | Daily Incremental scheduling | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TPA.VALIDATE_INPUT | decision | 10 | validate_input | valid->TPA.RESOLVE_DEPENDENCIES;invalid->TPA.ERROR_HANDLER | none | stop | Every new Aggregate Oracle Touchpoints Data submission |
