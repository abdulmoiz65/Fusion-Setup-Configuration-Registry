# Event Action Dependency Readiness

Source: developer-provided EventAction-HDL.md, Required Inputs and Prerequisites, Reference Attribute Information, and Validation Checklist. Resolver contracts are owned by ora_reference_lookups.md.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Current Event Action metadata | Confirm target release, attributes, DDF contexts, withdrawn fields, and supported keys before file preparation. |
| 2 | Event Action type and LDG | Confirm the type exists in target and resolve the LDG where the selected action requires one. |
| 3 | Event Group and monitored events | For a requested association, confirm an effective action-type Event Group watching the intended change. |
| 4 | HCM group | For Criteria, confirm one group and the accepted Criteria column. |
| 5 | Translation language | If translation is requested, confirm language support in target metadata; resolver contract is TBD. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| event_action_metadata | Current business-object attributes | Yes | Every HDL request | Lookup | core.data-loader Event Action attribute-details workflow; payrollEventActions describe separately checks REST shape | verify_event_action_metadata | Supplied DAT warns about withdrawal and differs from public examples. | Obtain current Event Action and relevant child attribute details through the declared workflow. | Confirmed fields, components, contexts, and keys |
| event_action_type | Available action type | Yes | Every HDL request | Blocked | Published HDL EventActionTypeCode list; target type-code authority TBD | verify_event_action_type | Published codes may differ from target availability; the reviewed REST response exposes a type ID without code mapping. | Supply intended type and target authority that proves its code is available. | Confirmed EventActionTypeCode |
| ldg | Legislative Data Group | Conditional | LDG-specific action | Lookup | Target legislativeDataGroupsLOV REST resource | find_ldg_by_exact_name | LDG-specific actions must use the intended target context. | Supply LDG name or validated ID. | LegislativeDataGroupName or LegislativeDataGroupId |
| event_group | Action-type Event Group | Conditional | Association requested | Lookup | Target unlisted payrollEventGroups REST resource; verify deployment and HDL key mapping | find_event_group_by_exact_code | Association must point to the intended monitored group. | Supply EventGroupCode and confirm group design. | EventGroupCode or EventGroupId |
| hcm_group | HCM worker group | Conditional | Criteria requested | Lookup | Target hcmGroupsLOV returns GroupName and GrpId; code-to-ID mapping remains unresolved | find_hcm_group_by_name_or_id | Criteria limits workers and the accepted HDL column is unresolved. | Supply exact GroupName or GrpId; code-only input needs separate authoritative mapping. | Confirmed GroupName or GrpId; HDL Criteria field only after target mapping |
| translation_language | Supported language | Conditional | Translation requested | Blocked | TBD | | Supplied translation header has Language, but no language domain or lookup contract. | Provide target language evidence before authoring translation. | Language |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | A target value and applicable attribute are already confirmed. | No new lookup needed. |
| Lookup | Exactly one approved read-only resolver contract is available. | Yes, read-only lookup only. |
| Blocked | Required metadata, authority, path, or unique match is missing. | No; obtain evidence and update resource contract. |
| Not applicable | The conditional component is omitted by design. | No. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EA.CHECK_DEPENDENCIES | step | 20 | resolve_dependency | ready->EA.LOOKUP_LDG;blocked->EA.RETURN_ISSUES | EA.VALIDATE_INPUT | stop | Any Event Action HDL request; evaluate Dependency Rules, including conditional dependencies |
