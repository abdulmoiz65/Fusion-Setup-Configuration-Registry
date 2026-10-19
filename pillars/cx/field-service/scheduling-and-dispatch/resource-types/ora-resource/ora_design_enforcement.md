# Resource Types Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate workbook intake | Confirm the Resource Types worksheet, unique labels, and internally consistent selections before design review. |
| 2 | Validate operating model | Confirm each proposed type documents a distinct operating model and its routing, capacity, cost, tracking, or teamwork effect. |
| 3 | Validate organization and bucket boundary | Confirm Organization Units are used for hierarchy and buckets are used for intake, routing, booking, or quota. |
| 4 | Validate routing and quota enablement | For each work-performing field Resource Type, require routing assignment and quota management or a documented exception. |
| 5 | Validate bucket capacity scope | When bucket quota management or routing into sub-buckets is enabled, require the documented capacity, booking, or routing effect. |
| 6 | Validate cost policy | When cost or travel values are configured, require their dispatch, payroll, agreement, subcontractor, or regulatory basis. |
| 7 | Validate teamwork and sharing | When teamwork or sharing is enabled, require the collaboration rationale and privacy/regulatory assessment for contractor location sharing. |
| 8 | Validate load thresholds | When thresholds are configured, require the metric and its dispatcher-workload basis. |
| 9 | Validate duration learning | When duration learning is configured, require its eligibility, contribution, onboarding/atypical-resource, and exclusion-period rationale. |
| 10 | Validate change impact | When an existing Resource Type changes, require assigned-resource and existing-behavior impact assessment. |
| 11 | Validate contractor separation | When contractors and employees share a type, require proof that operating treatment does not differ or separate the types. |
| 12 | Release preview | Permit preview only when every applicable Error rule passes or is corrected. |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| RT.OPERATING_MODEL | A Resource Type is created or changed | Error | | The type does not represent a distinct operating model, or the business effect on routing, capacity, costs, tracking, or teamwork is undocumented | Create separate Resource Types only where operational behavior differs, such as employees versus contractors, different service models, or distinct capacity treatment | Yes, before preview |
| RT.ORGANIZATION_AND_BUCKET_BOUNDARY | Organization Units, groups, or buckets are selected for the Resource Type model | Error | | Buckets are used only as reporting hierarchy, or Organization Units are expected to manage activity intake, routing, booking, or quota | Use Organization Units for hierarchy, segmentation, reporting, and the resource tree. Use buckets for activity intake, routing, booking, and quota management | Yes, before preview |
| RT.ROUTING_AND_QUOTA_ENABLEMENT | A work-performing field Resource Type is prepared for rollout | Error | | Routing assignment or quota management is disabled without a documented operational reason | Normally enable routing assignment and quota management for work-performing field-resource types before rollout; validate representative assignment scenarios | Yes, before preview |
| RT.BUCKET_CAPACITY_SCOPE | Bucket quota management or routing into sub-buckets is proposed | Error | | The capacity area, booking allocation, or routing effect is undocumented | Enable bucket quota management only for defined capacity areas or booking allocations. Enable routing into sub-buckets only when that behavior is intentional | Yes, before preview |
| RT.COST_POLICY | Relative working-time costs, travel costs, or start/end travel allowances are configured | Error | | Values do not reflect the dispatch policy, payroll treatment, labor agreement, subcontractor terms, or local regulation | Set cost and allowance values from the documented dispatch and employment model; do not use arbitrary defaults | Yes, before preview |
| RT.TEAM_AND_SHARING | Team participation, team-holder capability, or shared inventory, skills, or location is proposed | Error | | The collaboration model is undocumented, or contractor location sharing has not been assessed for privacy and regulatory impact | Enable only the sharing and teamwork capabilities the operating model needs; separately assess contractor location-sharing risk | Yes, before preview |
| RT.LOAD_THRESHOLDS | Load thresholds are configured | Error | | The threshold metric does not match how dispatchers assess workload | Use activity count, work hours, or workday percentage according to the operational dispatch model; validate dispatcher interpretation before rollout | Yes, before preview |
| RT.DURATION_LEARNING | Resource-level duration learning, initial duration ratios, contribution rules, or learning exclusion periods are proposed | Error | | The model allows unrepresentative, onboarding, or atypical resources to distort duration statistics | Use individual learning only where individualized estimates add value. Use initial duration ratios for onboarding or atypical efficiency, and define exclusion periods and contribution rules | Yes, before preview |
| RT.CHANGE_IMPACT | An existing Resource Type is changed | Error | | The impact on assigned resources and existing behavior has not been assessed | Treat Resource Type changes as durable structural changes. Assess assigned-resource impact and do not assume all changes are retroactive | Yes, before preview |
| RT.CONTRACTOR_SEPARATION | Contractors and internal employees are modeled in the same Resource Type | Error | | Their cost, travel, tracking, capacity, teamwork, access, or routing treatment differs | Separate contractor and internal Resource Types when their operating treatment differs; combining them hides real routing and governance differences | Yes, before preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RT.CHECK_OPERATING_MODEL | decision | 2 | design_enforcement | passed->RT.CHECK_ORGANIZATION_AND_BUCKET_BOUNDARY;blocked->RT.RETURN_ISSUES | RT.VALIDATE_WORKBOOK | stop | A Resource Type is created or changed |
| RT.CHECK_ORGANIZATION_AND_BUCKET_BOUNDARY | decision | 3 | design_enforcement | passed->RT.CHECK_ROUTING_AND_QUOTA_ENABLEMENT;blocked->RT.RETURN_ISSUES | RT.CHECK_OPERATING_MODEL | stop | Organization Units, groups, or buckets are selected for the Resource Type model |
| RT.CHECK_ROUTING_AND_QUOTA_ENABLEMENT | decision | 4 | design_enforcement | passed->RT.CHECK_BUCKET_CAPACITY_SCOPE;blocked->RT.RETURN_ISSUES | RT.CHECK_ORGANIZATION_AND_BUCKET_BOUNDARY | stop | A work-performing field Resource Type is prepared for rollout |
| RT.CHECK_BUCKET_CAPACITY_SCOPE | decision | 5 | design_enforcement | passed->RT.CHECK_COST_POLICY;blocked->RT.RETURN_ISSUES | RT.CHECK_ROUTING_AND_QUOTA_ENABLEMENT | stop | Bucket quota management or routing into sub-buckets is proposed |
| RT.CHECK_COST_POLICY | decision | 6 | design_enforcement | passed->RT.CHECK_TEAM_AND_SHARING;blocked->RT.RETURN_ISSUES | RT.CHECK_BUCKET_CAPACITY_SCOPE | stop | Relative working-time costs, travel costs, or start/end travel allowances are configured |
| RT.CHECK_TEAM_AND_SHARING | decision | 7 | design_enforcement | passed->RT.CHECK_LOAD_THRESHOLDS;blocked->RT.RETURN_ISSUES | RT.CHECK_COST_POLICY | stop | Team participation, team-holder capability, or shared inventory, skills, or location is proposed |
| RT.CHECK_LOAD_THRESHOLDS | decision | 8 | design_enforcement | passed->RT.CHECK_DURATION_LEARNING;blocked->RT.RETURN_ISSUES | RT.CHECK_TEAM_AND_SHARING | stop | Load thresholds are configured |
| RT.CHECK_DURATION_LEARNING | decision | 9 | design_enforcement | passed->RT.CHECK_CHANGE_IMPACT;blocked->RT.RETURN_ISSUES | RT.CHECK_LOAD_THRESHOLDS | stop | Resource-level duration learning, initial duration ratios, contribution rules, or learning exclusion periods are proposed |
| RT.CHECK_CHANGE_IMPACT | decision | 10 | design_enforcement | passed->RT.CHECK_CONTRACTOR_SEPARATION;blocked->RT.RETURN_ISSUES | RT.CHECK_DURATION_LEARNING | stop | An existing Resource Type is changed |
| RT.CHECK_CONTRACTOR_SEPARATION | decision | 11 | design_enforcement | passed->RT.RETURN_SUCCESS;blocked->RT.RETURN_ISSUES | RT.CHECK_CHANGE_IMPACT | stop | Contractors and internal employees are modeled in the same Resource Type |
