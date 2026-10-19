# Event Action Design Enforcement

Source: developer-provided EventAction-HDL.md, Supported Actions, Localization Input Validations, and Supplied Sample Comparison. This file owns business-design gates; field shape and allowed values are in ora_input_validation.md.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Select the action purpose | Identify the process, action type, worker scope, and required submission behavior. |
| 2 | Confirm monitored change | Define an action-type Event Group and the intended triggering DateTrackedEvent records if association is required. |
| 3 | Select action-specific behavior | Apply only the DDF context and options relevant to time cards, HCM Rates, or late hires. |
| 4 | Settle source conflicts | Resolve DAT withdrawal warnings and public-example column differences against target metadata before preview. |
| 5 | Review localization | Treat the GB example as a sample, not a country rule; require target LDG and design evidence. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Event Action is expected to trigger from changes | Blocker | find_event_group_by_exact_code | No confirmed action-type Event Group, monitored event, or supported association component | Confirm group design and association in target before expecting notifications. | Yes |
| Criteria is requested | Blocker | find_hcm_group_by_name_or_id | Worker group is not unique or SourceCode versus HCMGroupCode remains unresolved | Confirm the intended group and target Criteria metadata; code-only input still needs a code mapping. | Yes |
| Time-card resubmission | Blocker | verify_event_action_metadata | Selected lookback, SYNC submission, ProcessMode, or AutoApprove conflicts with target-supported attributes | Use the documented time-card pattern only after target metadata review. | Yes |
| HCM Rates recalculation | Blocker | verify_event_action_metadata | DDF context, ProcessingType, or InformationCategory is not confirmed in target | Use ORA_HCM_RATES_RECALC context and a target-supported processing value; public Full example uses ORA_FULL. | Yes |
| Late-hire retropay | Blocker | verify_event_action_metadata | Flow switches, LDG, submission mode, or withdrawn fields are copied from a sample without deliberate design | Confirm the Evaluate Late Hires behavior and target release. | Yes |
| Supplied GB late-hire sample is reused | Blocker | verify_event_action_metadata | MESS and AutoApprove=Y are accepted as GB defaults without resolving public example differences | Obtain an explicit design choice and target validation. | Yes |
| Translation is requested | Blocker | | Language or translated text is absent, or parent action has not been prepared | Supply supported Language and localized EventActionName/Description after the parent action. | Yes |
| Any child row is linked | Blocker | | EventActionTypeCode is used as the configured EventActionCode | Use the actual parent action code in child and association rows. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_event_group_by_exact_code | An Event Group association is requested | Confirmed group identity and action-type scope | ora_reference_lookups.md |
| find_hcm_group_by_name_or_id | Worker-group Criteria is requested | Confirmed GroupName or GrpId; code mapping and target HDL column when required | ora_reference_lookups.md |
| verify_event_action_metadata | DDF fields, withdrawn fields, Criteria, or association are involved | Supported target columns and components | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EA.ENFORCE_DESIGN | step | 80 | design_enforcement | passed->EA.EXECUTION_GATE;blocked->EA.RETURN_ISSUES | EA.VERIFY_METADATA | stop | Any Event Action HDL request; evaluate Design Rules and source conflicts |
