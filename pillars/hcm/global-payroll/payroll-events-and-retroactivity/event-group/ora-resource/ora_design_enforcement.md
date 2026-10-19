# Event Group Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Choose purpose | Require Proration, Action, or Retroactive as the business type; for Proration, require Calendar Year, Financial Year, Past Period Adjustment, or Payroll Period. Action denotes the Event Action group category. |
| 2 | Review existing setup | Reuse a suitable predefined group and avoid unexamined overlap. |
| 3 | Define monitored changes | Select source object, column, update type, effective context, and needed condition hierarchy. |
| 4 | Confirm consumer and test | Identify the element, retroactive flow, or Event Action and its expected controlled outcome. |
| 5 | Gate production preparation | Use current target metadata and the approved HDL route. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every group | Blocker | find_existing_event_group | A proposed group duplicates or overlaps an existing trigger without a documented reason. | Reuse a suitable predefined group or define the distinct need. | Yes |
| Every group | Blocker | verify_event_group_metadata | Technical codes, source object, column, or update type are copied from a sample without target-release verification. | Confirm every technical value from current metadata. | Yes |
| Every group | Blocker | | Event Group type is missing or is not Proration, Action, or Retroactive. | Select one of the three allowed business types before HDL mapping. | Yes |
| Proration group | Blocker | | Proration Period is missing or is not Calendar Year, Financial Year, Past Period Adjustment, or Payroll Period. | Select one of the four allowed periods before resolving its target-pod ProrationType value. | Yes |
| Proration group with Payroll Period | Blocker | verify_event_group_metadata | The Payroll Period lookup code is placed in TimeDefinitionId or TimeDefinitionCode instead of ProrationType. | Put the verified period code in ProrationType. Populate a time-definition field only for a separately resolved PayrollTimeDefinition. | Yes |
| Element association or payroll outcome testing is requested for a Proration group | Blocker | resolve_event_group_time_definition | Consuming recurring element, proration points, time definition, or style is absent or incompatible. | Enable proration on the element and associate the selected group; test an in-period change. | Yes |
| Parent-only group | Verify | | A DateTrackedEvent is absent. | Permit parent-only creation; define monitored changes later if the group must trigger proration. | Yes |
| Retroactive group | Blocker | | Expected notification and approved retroactive payroll flow are undefined. | Define a backdated-change test and expected retroactive result. | Yes |
| EventGroupAction association or action outcome testing is requested | Blocker | resolve_event_group_action | The existing action, its effective context, or manual/automatic submission behavior is undefined. | Confirm action association, notification, and submission path. Parent-only Action creation does not require an existing action. | Yes |
| EventGroupAction is proposed | Blocker | resolve_event_group_action | An event-action type code is used as EventActionCode without confirming the configured action's own code. | Resolve one existing action and use its confirmed EventActionCode or EventActionId. | Yes |
| EventValueQualifier is included | Blocker | verify_event_group_qualifier | Qualifier, sequence, or parent-condition hierarchy is inconsistent or unsupported. | Use only required conditions and verify hierarchy and qualifier domain. | Yes |
| DateTrackedEvent without value condition | Verify | | The requirement needs value filtering but the event would monitor every matching change. | Add a supported value-change condition only when the action requirement needs it. | Yes |
| Proration or Retroactive group | Blocker | | EventValueChange, EventValueQualifier, or EventGroupAction is included. | Remove Event Action-only child components. | Yes |
| Every load | Blocker | | An undocumented REST substitute, guessed internal ID, or unapproved upload route is proposed. | Use documented user keys and the declared HDL workflow. | Yes |
| Country-specific design | Blocker | verify_event_group_metadata | A country-only schema, technical-code, or label change is assumed from the reference. | Check current country guidance and target LDG metadata; do not invent localization differences. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_existing_event_group | Before accepting new or amend design | Existing identity or confirmed absence | ora_reference_lookups.md |
| verify_event_group_metadata | Before accepting technical values or production file | Current schema and supported values | ora_reference_lookups.md |
| resolve_event_group_time_definition | When proration uses a time definition | Compatible definition | ora_reference_lookups.md |
| resolve_event_group_action | When an EventGroupAction association or action outcome test is requested | Existing effective action | ora_reference_lookups.md |
| verify_event_group_qualifier | When qualifiers are selected | Supported name and value | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EVENT_GROUP.DESIGN_GATE | decision | 5 | design_enforcement | pass->EVENT_GROUP.EXECUTION_GATE;blocked->EVENT_GROUP.RETURN_ISSUES | EVENT_GROUP.DEPENDENCY_GATE | stop | Enforce purpose, selected component scope, applicable consumer behavior, localization verification, and HDL route. |

## Source

- Developer-supplied EventGroups-HDL.md: Supported use cases; Setup and validation; Limitations; Localization Input Validations; Standard Instructions.
- User clarification on 2026-10-01: a DateTrackedEvent is not mandatory for parent-only Event Group creation.
- User instruction on 2026-10-01: constrain business types and Proration Period values to the enumerated choices in Input Validation.
- Developer-supplied EventGroups-HDL.md: Limitations distinguish action-type codes from an existing EventActionCode; Localization Summary identifies no verified country-specific label or schema changes.
