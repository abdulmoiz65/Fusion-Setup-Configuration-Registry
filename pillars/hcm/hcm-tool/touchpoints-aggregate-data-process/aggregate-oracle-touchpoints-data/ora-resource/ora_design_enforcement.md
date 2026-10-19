# Aggregate Oracle Touchpoints Data Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm fixed ESS identity | Use only the source-confirmed job definition, EarHcmEss application, HRE product, and retries 0 |
| 2 | Bind ordered parameters | Bind worker count to submit.argument1 and selected run type to submit.argument2 as STRING values |
| 3 | Enforce date semantics | For one-off runs treat today as immediate execution; recurring requests use schedule.recurrences instead; never add a date business argument |
| 4 | Build immutable review | Show the complete target, defaults and overrides, both run-type choices, exact payload, polling settings, and audit destination |
| 5 | Bind approval | Accept approval only for the current immutable review immediately before submission |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A new ESS request is prepared | Error | | Job definition, application, product, or retries differs from the fixed contract | Restore the fixed source-confirmed ESS identity | Yes, before preview |
| Request parameters are prepared | Error | | Parameter count, order, name, type, worker range, or run type differs from the documented contract | Rebuild exactly two ordered STRING parameters | Yes, before preview |
| A one-off resolved run date is today | Error | | Payload contains startTime or a date business argument | Submit on demand and retain the date only in review and audit evidence | Yes, before preview |
| A one-off future run date is supplied | Error | | Timezone or exact startTime is absent from the review | Resolve one timestamp and rebuild the preview | Yes, before approval |
| Review is presented | Error | | The alternative run type is omitted or the selected run type is unclear | Show ORA_HRE_FULL_RUN and ORA_HRE_INCREMENTAL_RUN and mark the selected value | Yes, before approval |
| Submission is imminent | Error | | Approval is missing, stale, ambiguous, quoted, or applies to different inputs | Present the current immutable review and wait for a new affirmative response | No automatic fix |
| Implementation Full submission | Error | | Current parent full_ready_for_preview is not true, evidence is uninspected, task bindings are unsynchronized, or run type is not ORA_HRE_FULL_RUN | Return to the parent workflow; obtain readiness confirmation then separate exact Full approval | No automatic fix |
| Daily Incremental scheduling | Error | | Current parent daily_ready_for_preview is not true, Full evidence is not verified, or run type is not ORA_HRE_INCREMENTAL_RUN | Keep the schedule task blocked; user attestation cannot substitute for ESS success | No automatic fix |
| Daily schedule preview | Error | | Recurrence, timezone/offset behavior or end condition differs from the reviewed requirements, or start is past or before verified Full completion | Rebuild using references/daily-schedule.md; disclose DST limitations | Yes, before approval |
| Daily schedule completion | Error | | Exact recurring request and schedule have not been verified through core readback | Preserve request ID and report verification pending; never claim future runs succeeded | No automatic fix |
| Configuration changes after readiness or Full | Error | | Evidence or approval belongs to an earlier configuration revision or another target | Invalidate downstream readiness; never cancel or recreate an existing schedule automatically | No automatic fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| | No task-local live lookup is required for the fixed ESS contract | | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TPA.DESIGN_GATE | decision | 40 | design_enforcement | ready->TPA.APPROVAL_GATE;blocked->TPA.ERROR_HANDLER | TPA.APPLY_DEFAULTS | stop | Defaults and explicit overrides have been resolved |
