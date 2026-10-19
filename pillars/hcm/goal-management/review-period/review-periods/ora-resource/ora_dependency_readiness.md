# Review Period Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 0 | Parent Run Book execution control | Match the approved plan fingerprint and prove this is the earliest incomplete applicable task |
| 1 | Exact Review Period identity | Resolve zero or one target according to operation |
| 2 | Usage evidence | Re-read Goal Plan and other exposed references for risky changes |
| 3 | Management metadata | Confirm current UI/runtime or approved OpenAPI action paths and operations; never assume a public management collection |
| 4 | Status LOV | Resolve current Active/Inactive codes before any status-bearing mutation |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| RP.RUNBOOK_CONTROL | Parent Run Book execution control | Yes | Any Run Book task execution | Validate | `hcm.goal-management` controlled next-task resolver | resolve_controlled_next_task | Prevents direct entry into a later task | Complete or mark every earlier task Not Applicable and show the next-task preview | Approved plan fingerprint, exact task identity, sequence, execution-control fingerprint |
| RP.IDENTITY | Review Period identity | Conditional | Existing-object operation | Lookup | reviewPeriodsLOV or management GET | review_period_lookup | Prevents ambiguous writes | Supply an exact name or returned ID | ReviewPeriodId and current state |
| RP.USAGE | Downstream usage | Conditional | Date change, inactivation, or delete | Verify | Current exposed references | review_period_usage_lookup | Protects dependent Goal Plans | Resolve every reference before approval | Usage count and references |
| RP.METADATA | Management action contract | Conditional | Mutation | Verify | Authenticated current UI/runtime metadata or approved OpenAPI | review_period_describe | Prevents invented public endpoints and operations | Use guided FSM/UI when unavailable | Relative action/item path, writable attributes, operations, concurrency |
| RP.STATUS_LOOKUP | Current status choices | Conditional | Create, update with status, or inactivate | Lookup | Current public Apps Common ACTIVE_INACTIVE result | review_period_status_lookup | Validates submitted status code and supports the documented `A` fallback | Resolve current enabled/effective codes and meanings; do not use a VBCS service alias or cached tenant value | Allowed status code/meaning pairs |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Identity, usage, and metadata satisfy the selected operation | Yes for lookup; create only after approval |
| Missing | No existing target for get/update/inactivate/delete | Lookup only |
| Blocked | Ambiguous target, unsupported metadata, or unsafe usage | Lookup only |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| REVIEW_PERIODS.DEPENDENCIES | step | 30 | resolve_dependency | ready->REVIEW_PERIODS.LOOKUPS;missing->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.VALIDATE | stop | A Review Period mutation is requested |
