# Event Group Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target and metadata | Identify environment and LDG; obtain current EventGroup Attributes export before production mapping. |
| 2 | Existing setup | Check predefined or existing groups and overlapping monitored changes. |
| 3 | Purpose-specific setup | Confirm consuming element and time definition when proration consumption is requested, retroactive process when outcome testing is requested, and existing action or qualifiers only when those Action components are requested. |
| 4 | HDL handoff | Use the declared HCM Data Loader workflow only after payload, target, preview, and approval checks. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| EVENT_GROUP_LDG | Target legislative data group | Yes | Every group | Lookup | Target legislativeDataGroupsLOV through core.fusion-api.rest-api-client | resolve_event_group_ldg | Parent and children need compatible legislative scope. | Supply target environment and LDG; resolve one exact live match. | Confirmed LegislativeDataGroupName and LegislativeDataGroupId |
| EVENT_GROUP_METADATA | Current EventGroup metadata | Yes | Production preparation | Lookup | Target EventGroup attribute-details export through core.data-loader; named Common Lookups through core.fusion-api.apps-common.lookups | verify_event_group_metadata | Template inventory omits mandatory flags, lengths, types, and complete legal values. | Resolve target schema and enabled, effective lookup codes. | Confirmed component attributes and supported technical values |
| EVENT_GROUP_EXISTING | Existing or predefined group | Yes | New or amend intent | Lookup | Target payrollEventGroups REST resource; merged resource contract in ora_reference_lookups.md | find_existing_event_group | Overlapping triggers can change payroll outcomes. | Check scoped code/name identity; compare trigger scope only when monitored events are requested. | Existing group identity or confirmed absence |
| EVENT_GROUP_ACTION | Existing Event Action | Conditional | EventGroupAction association is requested | Lookup | Target payrollEventActions REST resource; merged resource contract in ora_reference_lookups.md | resolve_event_group_action | EventGroupAction references an existing action; the parent alone does not. | Supply intended action code or ID and effective context only for an association. | Confirmed EventActionCode or EventActionId |
| EVENT_GROUP_TIME | Applicable time definition | Conditional | A time definition is explicitly supplied or required by the consuming design | Lookup | Target payrollTimeDefinitionsLOV through core.fusion-api.rest-api-client; contract in ora_reference_lookups.md | resolve_event_group_time_definition | Group and consuming element need compatible time rules. | Supply the exact DefinitionName or numeric TimeDefinitionId and confirm LDG/type/usage applicability. The LOV cannot derive an HDL code. | Confirmed numeric TimeDefinitionId with name, type and LDG evidence |
| EVENT_GROUP_QUALIFIER | Supported qualifier | Conditional | EventValueQualifier is used | Lookup | Target qualifier metadata; access contract TBD | verify_event_group_qualifier | Qualifier name and value must fit the event. | Confirm the qualifier domain and selected value. | Confirmed QualifierName and QualifierValue |
| EVENT_GROUP_FORMULA | Supported formula reference | Conditional | FormulaCode or FormulaId is proposed | Lookup | Target component and formula metadata; access contract TBD | resolve_event_group_formula | Public EventGroup guidance does not confirm formula behavior. | Confirm component support before mapping a formula. | Confirmed formula key if supported |
| EVENT_GROUP_HDL_ROUTE | HCM Data Loader workflow | Yes | Any Fusion load | Verify | core/data-loader/SKILL.md; HCM EventGroup DAT at ZIP root; exact immutable artifact, selected environment and CUSTOM_EVENT_GROUP Task Hook context | | core.data-loader owns import validation, Task Hook, preview and approval before UCM upload/initiation. | Complete loader source/schema/archive validation first, then this task's read-only checks against the same artifact; return to the loader for its single approval gate. | Selected target, EventGroup business object, immutable validated ZIP, completed task checks and retained loader preview |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The required target-release values and contracts are confirmed. | Only the workflow-selected and approved operation may run. |
| Lookup | An authoritative value still needs resolution. | No create action. |
| Verify | A defined contract requires runtime evidence for the selected target and artifact. | Only its routed validation may run; upload remains subject to the loader gate. |
| Blocked | A required value, contract, metadata export, or loader gate is absent. | No. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EVENT_GROUP.DEPENDENCY_GATE | decision | 4 | resolve_dependency | ready->EVENT_GROUP.DESIGN_GATE;blocked->EVENT_GROUP.RETURN_ISSUES | EVENT_GROUP.RESOLVE_REFERENCES | stop | Confirm target metadata, existing setup, applicable purpose-specific dependencies, and the declared HDL handoff. |

## Source

- Developer-supplied EventGroups-HDL.md: Required inputs and prerequisites; Reference Attribute Information; HDL operation and payload structure; Unresolved Items.
- User-supplied Event Groups REST TDD and OraReview upload 3: exact source references and deployment limitations are recorded in ora_reference_lookups.md.
- Repository mandatory import workflow: core/data-loader/SKILL.md, Execute a data-loading request and Task Hook routing. Its approval workflow is authoritative for this handoff.
