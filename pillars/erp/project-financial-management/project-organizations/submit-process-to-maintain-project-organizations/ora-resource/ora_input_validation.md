# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Target environment | TargetEnvironment, configured environment and restBaseUrl | Block execution | Select the target configuration | Every request | verify_maintain_project_organizations_scope |
| Durable receipt | Distinct unused --output and companion .accepted.json paths | Block execution | Allocate task-local receipt paths | Every request | verify_ess_execution |
| Approval | Explicit approval of exact target and fixed payload | Block submission | Show the complete payload and target and obtain approval | Submit | verify_ess_approval |
| Existing request | Positive integer requestId | Block resume | Supply the previously returned request ID | Resume | track_existing_ess_request |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| operation is submit or resume; requestId selects resume when operation is omitted | Reject unsupported operations and conflicting submit plus requestId | Every request | |
| task code matches PJF_SUBMIT_PROCESS_TO_DENORMALIZE_ORGANIZATION_HIERARCHY | Reject wrong task scope | Every request | verify_maintain_project_organizations_scope |
| Payload uses only jobDefinitionId, application, product with the fixed values | Fill omitted fixed fields; reject overrides, additional fields, schedules and retries | Every request | |
| requestParameters is absent and no --parameter is supplied | Reject even empty or null requestParameters | Every request | |
| requestId is a positive integer, excluding boolean values | Reject invalid identity; never submit a replacement | Resume | |
| Approval is approved=true, operation=submit, exact environment/restBaseUrl and canonical payload_sha256 | Block absent, declined, stale or mismatched approval before authentication | Submit | verify_ess_approval |
| Wait seconds and poll interval are positive | Reject disabled or invalid polling settings | Execution | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| requestId supplied | Lookup | Resume only the supplied request; no submission approval is needed | track_existing_ess_request |
| No requestId supplied | Satisfied | Prepare the fixed payload and require approval | |
| Prior attempt failed, timed out or is uncertain | Blocked | Preserve evidence; resume known ID or reconcile uncertain submission through the active workflow; never automatically replay | |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPO.VALIDATE_INPUT | step | 1 | validate_input | valid->MPO.APPLY_DEFAULTS;invalid->MPO.RETURN_ISSUES;unsupported->MPO.RETURN_REFUSAL | none | stop | Every Submit Process to Maintain Project Organizations request |
