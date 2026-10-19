# Event Group HDL Input Validation

Validate against the current target-pod EventGroup Attributes export. The supplied template inventory does not establish mandatory flags, lengths, data types, all legal values, or release-specific schema changes.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Group identity | EventGroupName and EventGroupType; EventGroupCode optional | Block load preparation if name or type is missing or the type is outside Proration, Action, and Retroactive | Accept exactly Proration, Action, or Retroactive as the business type. Treat Action as the Event Action group described by Oracle documentation. Default a missing code to the exact name, then validate the HDL fields against target metadata. | Every group | verify_event_group_metadata |
| Proration period | Calendar Year, Financial Year, Past Period Adjustment, or Payroll Period | Block Proration group preparation if the period is missing or outside these four values | Require one of the four named business values for a Proration group; resolve its target-pod ProrationType mapping before rendering HDL. | EventGroupType is Proration | verify_event_group_metadata |
| Target scope | Environment, LegislativeDataGroupName or LegislativeDataGroupId | Block load preparation if the target or LDG is missing | Identify the target and resolve one compatible LDG. Do not require an effective date for a parent-only EventGroup: the supplied parent template has no effective-date attribute. | Every group | resolve_event_group_ldg |
| Operation | New or amend intent and resolved EventGroupCode | Block load preparation | State the intent; apply the code default when needed before checking existing setup. | Every group | find_existing_event_group |
| Monitored event | DatedObjectName or DatedTableId, UpdateType, ColumnName when applicable | Block event mapping | Select supported technical names from target-release metadata. | Every DateTrackedEvent | verify_event_group_metadata |
| Proration consumer context | Consuming recurring element, proration points, applicable time definition and proration style | Block element-association preparation | Confirm consuming element setup and applicable values when the request includes proration consumption or outcome testing. | Element association or payroll outcome testing is requested | resolve_event_group_time_definition |
| Event Action context | Existing EventActionCode or EventActionId; conditions and hierarchy when required | Block association preparation | Identify the action and define the intended conditions. A parent-only Action group does not require an association. | EventGroupAction association is requested | resolve_event_group_action |
| Current HDL schema | Target-pod EventGroup Attributes export | Block production file preparation | Export current Attributes from View Business Objects; confirm required fields, types, lengths, and legal values. | Production load | verify_event_group_metadata |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| LDG or current component metadata is unresolved | Blocked | Resolve the exact target-release authority. | resolve_event_group_ldg |
| A requested EventGroupAction references an unconfirmed Event Action | Blocked | Resolve one existing effective action. | resolve_event_group_action |
| A proration time definition is used but unconfirmed | Blocked | Resolve one applicable definition. | resolve_event_group_time_definition |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Parent identity | Child records must retain the selected EventGroupCode and compatible LDG and effective context. | Any child component | |
| Parent-only group | Permit EventGroup without DateTrackedEvent. Do not require or manufacture a monitored source, column, update type, EventValueChange, EventValueQualifier, EventGroupAction, formula, or child effective dates when none is requested. Evaluate child-specific rules only for supplied child components. | No monitored event or child component is requested | |
| Parent-only as-of date | Retain a requested as-of date as design context; do not render it as an EventGroup parent attribute or invent an effective-dated child. Explain that parent-only HDL cannot establish the requested start date from the supplied schema. | An as-of date is supplied for a parent-only group | |
| Event Group type domain | Accept only Proration, Action, or Retroactive as business input. Action is the Event Action group category. Reject any other business value before technical-code lookup. | Every group | |
| Proration period domain | Accept only Calendar Year, Financial Year, Past Period Adjustment, or Payroll Period. Reject any other value before target-pod mapping. Require one of these values when the group type is Proration. | Proration period is supplied or EventGroupType is Proration | |
| Proration period versus time definition | Map the Payroll Period business label to ProrationType using PAY_PRORATION_PERIOD_TYPE. Do not put its code in TimeDefinitionId: target metadata types that field as Number and references PayrollTimeDefinition. TimeDefinitionCode is the separate string user key for a supplied time definition. | Proration period or time definition is supplied | verify_event_group_metadata |
| Parent-first order | Place EventGroup before DateTrackedEvent and other child records in the DAT. | HDL mapping includes children | |
| Source field support | Confirm DatedObjectName, ColumnName, UpdateType, EventGroupType, and ProrationType in target-release metadata. The accepted business labels above do not establish HDL technical codes, field lengths, or target support. | Technical values are populated | verify_event_group_metadata |
| DT_INSERT column | ColumnName must be blank. | UpdateType is DT_INSERT | |
| Dates | Use YYYY/MM/DD and a nonconflicting effective range; object-specific constraints are TBD. | Effective dates are populated | |
| Condition sequence | Sequence must express the intended hierarchy; a parent sequence or ID must refer to an existing parent condition. | EventValueChange is used | |
| ValidEvent | Accept Y or N only. | EventValueChange has ValidEvent | |
| Value condition | FromValue and ToValue must fit the monitored column; the documented wildcard is &lt;ANY_VALUE&gt;. | EventValueChange has values | verify_event_group_metadata |
| Qualifier | Verify predefined QualifierName and its permitted QualifierValue; other value domains are TBD. | EventValueQualifier is used | verify_event_group_qualifier |
| Formula | Confirm that the component supports FormulaCode or FormulaId before mapping either attribute. | A formula is proposed | resolve_event_group_formula |
| User keys | Use documented user keys with MERGE where appropriate; use internal IDs only with an approved extraction or migration design. | HDL mapping | |
| HDL package shape | Use EventGroup.dat at the root of a ZIP submitted through Data Exchange > Import and Load Data; verify component and attribute spelling against the current View Business Objects export. | Any proposed HDL package | verify_event_group_metadata |
| Sample placeholders and cross-record keys | Reject unresolved angle-bracket placeholders, an unfinished EventActionCode, or child EventGroupCode and LDG values that do not identify the intended parent. Sample2-EventGroup.dat contains these illustrative defects and cannot be loaded unchanged. | A sample is adapted into an HDL file | |

## Supplied Template Attribute Inventory

This inventory is reported by EventGroups-HDL.md from EventGroup.dat and Template-EventGroup.dat. It is an aid to metadata review, not a production field dictionary.

| Component | Attributes Reported in Template |
|---|---|
| EventGroup | EventGroupId, EventGroupCode, EventGroupName, EventGroupType, ProrationType, LegislativeDataGroupId, TimeDefinitionId, LegislativeDataGroupName, TimeDefinitionCode, GUID, SourceSystemOwner, SourceSystemId, Description, SourceRefTableName, SourceRef001–SourceRef010 |
| DateTrackedEvent | DatetrackedEventId, EventGroupId, DatedTableId, ColumnName, UpdateType, LegislativeDataGroupId, ProrationStyle, EventGroupCode, LegislativeDataGroupName, DatedObjectName, GUID, SourceSystemId, SourceSystemOwner, SourceRefTableName, SourceRef001–SourceRef010 |
| EventValueChange | EventValueChangeId, EffectiveStartDate, EffectiveEndDate, DatetrackedEventId, Sequence, ValidEvent, LegislativeDataGroupId, FromValue, ToValue, EventGroupCode, LegislativeDataGroupName, DatedObjectName, ColumnName, UpdateType, ParentEvtValChgId, GUID, SourceSystemId, SourceSystemOwner, FormulaId, EventGroupId, ParentEvtValChangeSequence, FormulaCode, DatedTableId, SourceRefTableName, SourceRef001–SourceRef010 |
| EventValueQualifier | EventValueQualId, EffectiveStartDate, EffectiveEndDate, EventQualifierId, EventValueChangeId, QualifierName, QualifierValue, SourceSystemOwner, SourceSystemId, GUID, LegislativeDataGroupName, DatetrackedEventId, EventGroupId, DatedTableId, ColumnName, UpdateType, EventGroupCode, DatedObjectName, Sequence, LegislativeDataGroupId, SourceRefTableName, SourceRef001–SourceRef010 |
| EventGroupAction | EffectiveEndDate, EffectiveStartDate, EventActionId, EventGroupActionId, EventGroupId, GUID, SourceSystemId, SourceSystemOwner, EventGroupCode, EventActionCode, LegislativeDataGroupName, LegislativeDataGroupId, SourceRefTableName, SourceRef001–SourceRef010 |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EVENT_GROUP.VALIDATE_INPUT | step | 1 | validate_input | valid->EVENT_GROUP.DEFAULT_CODE;blocked->EVENT_GROUP.RETURN_ISSUES | none | stop | Validate selected Event Group intent, required input groups, component shape, and source-supported field constraints. |

## Source

- Developer-supplied EventGroups-HDL.md: HDL Attribute Metadata Output; Required inputs and prerequisites; Standard Instructions; Specific Object-Level Validations; Field-Level Validations.
- User clarification on 2026-10-01: EventGroupCode may default to the name, and a DateTrackedEvent is optional for parent-only creation.
- User clarification on 2026-10-05 reaffirms that an omitted EventGroupCode defaults to the exact EventGroupName and DateTrackedEvent is not mandatory. These are normal parent-only rules, not a waiver of required parent validation or loader approval.
- User instruction on 2026-10-01: Event Group type is restricted to Proration, Action, or Retroactive; Proration Period is restricted to Calendar Year, Financial Year, Past Period Adjustment, or Payroll Period.
- Target-pod EventGroup attribute-details export on 2026-10-01: TimeDefinitionId is a numeric PayrollTimeDefinition foreign key; TimeDefinitionCode is a string user key; ProrationType uses PAY_PRORATION_PERIOD_TYPE.
- Developer-supplied EventGroups-HDL.md: Supplied HDL Samples and HDL operation and payload structure identify Sample2-EventGroup.dat as incomplete and document the DAT-in-ZIP layout.
