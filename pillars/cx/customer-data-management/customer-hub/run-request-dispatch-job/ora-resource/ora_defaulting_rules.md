# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Client retries | 0 | New submission | No |  |
| Submission handling | Submit only, capture requestId, then stop | New submission | No |  |
| Automatic replacement | Disabled | Timeout, transport failure, missing response, or failed process | No |  |
| Schedule | No default | User has not chosen on-demand or recurring execution | No; require an explicit choice |  |
| Recurrence rules | No default | Recurring execution | No; require one or more explicit Oracle-supported RFC 5445 RRULEs |  |
| Recurring start, end, time zone, inclusions, and exclusions | No default | Recurring execution | No; require explicit bounded values and preserve optional exceptions exactly |  |
| Generate past occurrences | false (`executePast=false`) | Recurring execution | No |  |
| Parent job identity | JobDefinition://oracle/apps/ess/cdm/hubBase/reqDispatcher/RequestDispatchJob; application CrmEss; product ZCH | New submission | No |  |
| Refresh Metadata | IF_NEEDED | User omits Refresh Metadata | Yes; ALWAYS, NEVER, or explicit blank/null are supported user choices |  |
| Dispatch Job Timeout | 120 | User omits Dispatch Job Timeout | Yes; preserve validated whole-number text exactly |  |
| Parameter shape | submit.argument1 followed by submit.argument2; both STRING | New submission | No |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RDJ.DEFAULTS | step | 25 | apply_default | applied->RDJ.DEPENDENCIES;failure->RDJ.ERROR | RDJ.VALIDATE | stop | Apply safe submission and retry defaults. |
