# Aggregate Oracle Touchpoints Data Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| run_date | Current date in the configured project or environment timezone, resolved once at preview creation | run_date is omitted for a one-off run | No; preserve an explicit valid date | |
| execution_mode | On demand with no startTime | A one-off resolved run_date is today | No; a future date follows the separately reviewed future-start rule | |
| number_of_workers | 4 | number_of_workers is omitted | No; preserve an explicit integer from 1 through 20 | |
| run_type | ORA_HRE_FULL_RUN | run_type is omitted for a one-off run | No; explicit values remain subject to the implementation-stage design gate | |
| retries | 0 | Every new submission | No | |
| wait_seconds | Core ESS submitter default | wait_seconds is omitted for a one-off run | No; preserve an explicit positive bounded override | |
| poll_interval | Core ESS submitter default | poll_interval is omitted | No; preserve an explicit positive bounded override | |

The immutable review must show both run-type options even when the full-run
default is applied. For standalone runs a user selection of Incremental rebuilds
the payload and invalidates approval. The implementation Full and daily schedule
stages lock their respective run types through design enforcement. Daily time,
timezone and end condition have no silent defaults; the daily contract requires
wait_seconds 1 and poll_interval 1 for bounded readback rather than waiting for
the repeating parent to terminate.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TPA.APPLY_DEFAULTS | step | 30 | apply_default | applied->TPA.DESIGN_GATE;blocked->TPA.ERROR_HANDLER | TPA.RESOLVE_DEPENDENCIES | stop | Dependencies are ready and one or more optional inputs are omitted |
