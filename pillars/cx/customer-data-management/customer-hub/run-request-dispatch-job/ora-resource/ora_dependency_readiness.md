# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target environment | Resolve exactly one Fusion environment. |
| 2 | Scheduler identity | Apply the source-confirmed parent jobDefinitionId, CrmEss application, and ZCH product. |
| 3 | Job parameters | Resolve/default ordered submit.argument1 and submit.argument2 STRING values. |
| 4 | Schedule | Resolve on-demand execution or the complete recurring schedule. |
| 5 | Approval | Bind standalone approval to the immutable preview. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| RDJ.ENV | Fusion environment | Yes | New submission | Blocked until proven | Exactly one configured environment |  | Prevent cross-environment execution | Select one target | Environment identity |
| RDJ.IDENTITY | ESS technical identity | Yes | New submission | Fixed | Reviewed FusionApps RequestDispatchJob metadata |  | Prevent submission to an inferred or child process | Use only the fixed parent-job identity | RequestDispatchJob, CrmEss, and ZCH |
| RDJ.PARAMETERS | ESS user parameters | Yes | New submission | Satisfied after validation/defaulting | Screenshot-confirmed Scheduled Processes UI values and completed Process Details | resolve_refresh_metadata_policy | Reproduce supported UI choices and preserve Scheduler positions | Choose Refresh Metadata and optionally override the timeout | submit.argument1 and submit.argument2 STRING values |
| RDJ.SCHEDULE | Execution schedule | Yes | New submission | Blocked until selected | Explicit on-demand choice or exact bounded Oracle-supported recurrence rules, per-rule start/end values, IANA/Olson time zone, and optional inclusions/exclusions |  | Prevent an unintended or unbounded recurring process | Choose on-demand or provide the complete recurring schedule | Schedule object and continuing impact |
| RDJ.APPROVAL | Immutable preview approval | Yes | New submission | Blocked until approved | Preview fingerprint and later standalone approval |  | Prevent unreviewed processing of eligible requests | Approve the unchanged preview | Approval evidence |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RDJ.DEPENDENCIES | decision | 30 | resolve_dependency | satisfied->RDJ.ENFORCE;blocked->RDJ.ERROR | RDJ.DEFAULTS | stop | Resolve all new-submission dependencies. |
