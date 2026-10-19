# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Task-flow context | Establish PROJECT_PLAN and PLAN_TYPE for this task, then resolve parent planning amounts and the distinct child PlannedForCode before conditional controls. |
| 2 | Eligible plan type | Confirm the selected plan type is not seed data and is not attached where the source makes its controls read-only. |
| 3 | Applicable reference values | Resolve static choices through their local canonical tables. Resolve calendar before period profile, business unit and rates set before planning schedules, and known feature readiness before Output units. Unsupported reference/feature acquisition records a nonblocking warning, not a missing dependency. |
| 4 | Task-level FSM route | Authenticate, obtain and persist an export ProcessId, wait for completion, validate the returned ZIP, and retain its package schema through preview, approval, submission, and readback. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PJO.PPT.CONTEXT | Task-flow context | Yes | Any request | Verify | Task identity and current package context | | The task is PROJECT_PLAN at PLAN_TYPE level | Resolve parent planning amounts and distinct child scope before interpreting conditional fields | planTypeCode, PlanOptionLevelCode, PlannedForCode |
| PJO.PPT.ELIGIBILITY | Eligible plan type | Yes | Edit or option change | Verify | Current retained baseline and supported eligibility evidence; unavailable editability verification is disclosed | | Attached and seed-data conditions make source controls read-only | Block known protected changes; disclose unavailable editability checks without requiring a consultant UI visit | plan type eligibility |
| PJO.PPT.REFERENCES | Parent planning amounts | Yes | Create or change to parent planning amounts | Verify | Dedicated local resolver | resolve_plan_option | Canonical membership and project-plan applicability are separate checks | Resolve any unambiguous wording; non-default creation needs supported branch/package evidence | canonical PlanOptionCode |
| PJO.PPT.CHILD_SCOPE | Child planning amounts | Yes | Planning-options or currency child row | Verify | Dedicated local resolver | resolve_planned_for | Parent and child code domains differ | Resolve the parent first and preserve evidenced child relationships | PlannedForCode and matching currency parent key |
| PJO.PPT.PERIOD | Period profile and calendar | Conditional | Period Profile supplied or changed | Verify | Evidence selected by resolve_period_profile | resolve_period_profile | Profile choices depend on calendar G/P | Follow the resolver evidence boundary; unavailable target validation remains unresolved/nonblocking without a new lookup or evidence request | profile name, evidence basis and target-validation status |
| PJO.PPT.BUSINESS_UNIT | Business unit | Conditional | Rate schedule row supplied | Lookup | Dedicated dynamic resolver | resolve_business_unit | Rate assignments require canonical business-unit code and identity | Use the verified BU resolver; its canonical response name is source-proven to equal ShortCode in the same application language | ShortCode and internal BU identity |
| PJO.PPT.RATE_SET | Business-unit project rates set | Conditional | A rate schedule is supplied | Lookup | Dedicated live assignment resolver after BU resolution | resolve_business_unit_rate_set | Rate schedules must belong to the selected BU assigned or common project rates set | Resolve the assignment once per distinct BU before schedule matching | Internal assigned SetId |
| PJO.PPT.OUTPUT_UNITS | Output units feature | Conditional | Output units calculation requested | Verify | Feature readiness required by the dedicated resolver | resolve_percent_calc | An enabled lookup member does not prove feature availability | Use known readiness; unavailable feature validation is warning-only; do not silently downgrade the requested method | feature readiness |
| PJO.PPT.ROUTE | Task-level FSM route | Yes | Before any configuration change | Verify | Persisted export receipt, completed current task export, and task import support | resolve_task_level_fsm_route | The task supports CSV export/import; the completed current export supplies the package schema for the requested change | Authenticate before create. Persist the returned ProcessId before polling. If no ProcessId exists because authentication failed, reauthenticate and create the first export. If it exists, resume only that process. Validate the ZIP, obtain checksum-bound approval, then submit once through Data Loader | export ProcessId, valid current export ZIP, and approved preview |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | All supported applicable dependencies are satisfied; nonblocking unresolved warnings are retained | No |
| Unresolved | A supported reference/feature validation route is absent | No; record warning and continue the declared workflow |
| Blocked | Context, eligibility, current export, or approval is missing | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PJO.PPT.READINESS | step | 20 | resolve_dependency | ready->PJO.PPT.RESOLVE_LOVS;blocked->PJO.PPT.ROUTE_ISSUES | PJO.PPT.VALIDATE_INPUT | stop | Any validated request |
