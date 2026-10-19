# Review Period Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? |
|---|---|---|---|
| status | Current metadata-supported default, shown in preview | Only when the source omits status; if no proven default exists, resolve the intended status before preview | Preserve an explicit valid code; reject invalid codes rather than silently replacing them. No blanket inactive-first rule applies to Review Periods |
| omitted update fields | Preserve fresh stored values | Update | No |
| description | No default | Create/update | Preserve omission; do not invent consultant text |
| InUseFlag and concurrency | Fresh read-only state | Risky update/inactivate/delete | Never send guessed values |
| effective date | No default | Any operation | Never infer today |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| REVIEW_PERIODS.DEFAULTS | step | 50 | apply_default | complete->REVIEW_PERIODS.DESIGN | REVIEW_PERIODS.LOOKUPS | stop | Mutation lookups are resolved |
