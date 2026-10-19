# Manage Positions Design Enforcement

## Purpose

Defines the mandatory Position contract, identity, effective-reference,
source-scope, and loader-key design gates evaluated before preview or routing.
It does not perform lookups, apply defaults, or create missing setup.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm contract and identity | Confirm the current contract, then resolve one target or confirm create name and supplied code availability. |
| 2 | Read current content | Read requested sections and resolve an exact child target when required. |
| 3 | Validate context | Confirm YYYY/MM/DD effective context. |
| 4 | Resolve dependencies | Resolve Business Unit, Department, Job, Location, and every other supplied lookup or foreign reference exactly. |
| 5 | Validate final mutation artifact | Match dependency evidence, effective dates, flexfield declarations and selectors, row intent, parent-child keys, field types, and source row counts to the final DAT or ZIP. |
| 6 | Limit mutation scope | Keep only the base Position row and child objects explicitly modified by the user. |
| 7 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| CONTRACT | Every request | Blocking | inspect_positions_contract | The live positionsV2 describe contract is unavailable or its resolver mapping is unusable | Restore the live contract; never guess a childRef or mapping | Lookup fix |
| IDENTITY | Read, edit, or delete | Blocking | find_manage_positions | Identity is absent, unresolved, or ambiguous | Supply one exact PositionCode or PositionName | Input fix |
| CREATE_UNIQUENESS | Create | Blocking | find_manage_positions | Exact PositionName or supplied PositionCode already exists, or a required check is ambiguous | Supply a unique name and code when required | Input fix |
| POSITION_CODE | Create omits PositionCode | Blocking | inspect_positions_contract | Automatic code generation is not confirmed | Supply PositionCode | Input fix |
| BUSINESS_UNIT | Create or edit | Blocking | resolve_position_business_unit | The Business Unit is unresolved, inactive, or ambiguous | Supply one exact active Business Unit | Lookup fix |
| DEPARTMENT | Create or edit | Blocking | resolve_position_department | The Department is unresolved, inactive, ambiguous, or not effective on the requested date | Supply one exact effective Department | Lookup fix |
| JOB | Create or edit | Blocking | resolve_position_job | The Job is unresolved, inactive, ambiguous, or not effective on the requested date | Supply one exact effective Job | Lookup fix |
| LOCATION | Create or edit supplies a Location | Blocking | resolve_position_location | The Location is unresolved, inactive, ambiguous, or not effective on the requested date | Supply one exact effective Location | Lookup fix |
| SUPPORTED_CONTENT | Every request | Blocking | inspect_positions_contract | A section or field is not present in the current Position contract | Remove the unsupported content or use one exact current technical name or unique display label | Input fix |
| FIELD_VALUE | Create or edit supplies a lookup, foreign reference, context, or segment | Blocking | resolve_position_field_value | The value or any dependent key is unresolved, inactive, ineffective, unsupported, or ambiguous | Supply one exact supported value and complete business key | Lookup fix |
| CHILD_TARGET | Get requests one child row, or edit or delete targets a child | Blocking | read_position_section_rows | The complete child key is absent or resolves to zero or multiple current rows | Supply one complete current child business key | Input fix |
| CHILD_LINKAGE | A child mutation is included | Blocking | read_position_section_rows | The child row does not identify the same exact Position and effective context, or depends on an invented surrogate identifier | Use the current supported parent business key and effective context | Input fix |
| EDIT_KEYS | A Position or child row is edited | Blocking | read_position_section_rows | The parent Position key or any edited child key is blank, stale, ambiguous, or absent; a blank key would be interpreted as a new effective row | Re-read the current target and include its exact parent and child keys; use a blank key only for a new child row | Input or payload fix |
| ACTION_REASON_UPDATE | An effective-dated Position update is authored | Blocking |  | ActionReasonCode was copied from a create/correct payload, defaulted, or supplied without an explicit user request | Omit ActionReasonCode. Include it only when the user explicitly provides an update-appropriate reason. | Input or payload fix |
| CREATE_COPY_KEYS | A Position is created or copied | Blocking | inspect_positions_contract | Prepared content populates a new parent or child surrogate identifier, GUID, WHO column, or source-system key, or a foreign-reference ID lacks fresh exact-match evidence | Omit nonportable fields and resolve target-environment references again | Input or lookup fix |
| COPY_COMPLETENESS | A Position is copied with child objects | Blocking | read_position_section_rows | Final section row counts differ from the complete paginated source snapshot | Restore missing rows, remove invented rows, or repeat the source read | Input or lookup fix |
| CHILD_EFFECTIVE_RANGE | A create or copy contains a date-effective child row | Blocking |  | A child begins before the Position, ends after it, or ends before it begins | Rebase or correct the child effective range | Input fix |
| EVALUATION_DATE | A PositionEvaluation row is created or copied | Blocking |  | DateEvaluated is before Position.EffectiveStartDate or after Position.EffectiveEndDate | Rebase an earlier copied date to the target start or supply a valid date | Input fix |
| DELEGATE_POSITION_KEY | Any DelegatePosition field is populated | Blocking | resolve_delegate_position | DelegatePositionCode and its Business Unit fields do not resolve to the same one effective Position or do not match final dependency evidence | Use the exact delegate Position and its own Business Unit | Lookup fix |
| DELEGATE_POSITION_PAYLOAD_TYPE | Any DelegatePosition field is populated | Blocking | resolve_delegate_position | DelegatePositionBusinessUnitId is blank, nonnumeric, or contains the Business Unit display name, or the name and ID were not freshly resolved from the same delegate Position | Rebuild the row with the resolved numeric Business Unit ID and display name in their separate columns | Lookup or payload fix |
| FUNDING_POSITION_KEY | A PositionFundingRelationship row is supplied | Blocking | resolve_funding_position | FundingPositionCode and its Business Unit fields do not resolve to the same one effective Position or do not match final dependency evidence | Use the exact funding Position and its own Business Unit | Lookup fix |
| FUNDING_POSITION_PAYLOAD_TYPE | A PositionFundingRelationship row is supplied | Blocking | resolve_funding_position | FundingPositionBusinessUnitId is blank, nonnumeric, or contains the Business Unit display name, or the name and ID were not freshly resolved from the same funding Position | Rebuild the row with the resolved numeric Business Unit ID and display name in their separate columns | Lookup or payload fix |
| VALID_GRADE_KEY | A PositionGrade row is supplied | Blocking | resolve_valid_grade | GradeSetCode and GradeCode do not resolve together exactly once on the target date or do not match final dependency evidence | Supply one complete effective Grade business key | Lookup fix |
| FLEXFIELD_CONTEXT | A context-qualified segment is populated | Blocking | resolve_position_flexfield_context | The FLEX selector is blank or differs from the segment context, multiple contexts are populated in one row, the context or segment is absent from current describe, or EFF category is not POS_EIT/POS_LEG as applicable | Use one current context per row and its exact selector, segments, and EFF category | Input or lookup fix |
| FLEXFIELD_DECLARATION | A qualified DFF or EFF segment is populated in loader content | Blocking | resolve_position_flexfield_context | The matching `FLEX:FLEX_CODE` declaration is absent from the `METADATA` line or its row value is blank or differs from the segment context | Rebuild the metadata and row with the explicit resolved FLEX selector | Payload fix |
| FINAL_EDIT_PAYLOAD_REVIEW | A Position edit is prepared | Blocking | read_position_section_rows | The unchanged final DAT or ZIP was not inspected by METADATA header name; an existing row lacks its fresh key; a new row carries an existing-row key; an ID/name pair has the wrong type, column, or resolver value; a qualified segment lacks its exact flex declaration or context; or an effective range would overlap | Re-read the affected rows and dependencies, rebuild the source, and rerun the complete serialized edit review before preview | Input, lookup, or payload fix |
| FINAL_CREATE_COPY_REVIEW | A Position create or copy contains any child row | Blocking |  | Any applicable Position input, dependency, reference, defaulting, effective-date, flexfield, parent-child, duplicate, or copy-completeness rule is not passed for the unchanged final prepared content | Correct the content or evidence and restart the applicable rules before approval | Input or lookup fix |
| DELETE_TARGET | Delete | Blocking | read_position_section_rows | The Position or requested child is not resolved exactly once, required child or effective-split context is absent, or the request implies a REST write | Resolve one exact target and route deletion through core.data-loader | Input fix |
| DELETE_MODE | Delete targets the Position parent | Blocking |  | Zap versus effective-split intent is absent or ambiguous | Require the user to choose the destructive scope; never infer zap | Input fix |
| ZAP_DELETE | Zap delete | Blocking | find_manage_positions | The exact logical Position is unresolved, the artifact uses MERGE, contains child rows, or mixes DELETE and MERGE for that Position | Author one Position DELETE row using its resolved supported business key and disclose complete logical-object purge | Input or payload fix |
| DATE_EFFECTIVE_SPLIT_DELETE | Effective-split delete | Blocking | resolve_position_delete_history | The selected row is the first split, has no predecessor, is unresolved or ambiguous, or the final artifact does not use `SET PURGE_FUTURE_CHANGES Y` plus one Position MERGE whose start is the predecessor start and whose end is the selected row end | Rebuild the bounded MERGE from complete fresh Position history; never use DELETE for a split | Lookup or payload fix |
| MODIFIED_SECTIONS | Create, edit, or delete | Blocking |  | The mutation contains a child-object row when the user supplied no values for that child object | Keep the base Position row and only child-object rows explicitly modified by the user | Input fix |

| POSITION_CONFIGURATION | Create or edit | Warning |  | FTE, synchronization, or budgeting settings are requested without confirming their intended use and prerequisites | Confirm the intended setting and required position status before change | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| inspect_positions_contract | Every request | Describe-backed technical names, child references, and source-to-target mappings | ora_reference_lookups.md |
| find_manage_positions | Read, edit, delete, or create uniqueness check | Exact identity, duplicate-check result, effective range, and current values | ora_reference_lookups.md |
| read_position_section_rows | Get, or edit or delete requires current section values or child identity | Requested current section values and exact parent or child keys | ora_reference_lookups.md |
| resolve_position_delete_history | Effective-split delete | Complete ordered history, non-first eligibility, predecessor start, selected-row end, and verification evidence | ora_reference_lookups.md |
| resolve_position_business_unit | Create or edit | One exact active Business Unit identity | ora_reference_lookups.md |
| resolve_position_department | Create or edit | One exact Department effective on the requested date | ora_reference_lookups.md |
| resolve_position_job | Create or edit | One exact Job effective on the requested date | ora_reference_lookups.md |
| resolve_position_location | Create or edit when Location is supplied | One exact Location effective on the requested date | ora_reference_lookups.md |
| resolve_delegate_position | Create or edit supplies any DelegatePosition field | One exact effective delegate Position and its own Business Unit | ora_reference_lookups.md |
| resolve_funding_position | A funding relationship is created or copied | One exact effective funding Position and its own Business Unit | ora_reference_lookups.md |
| resolve_valid_grade | A valid-grade row is created or copied | One exact GradeSetCode and GradeCode effective on the target date | ora_reference_lookups.md |
| resolve_position_flexfield_context | A context-qualified segment is populated | One current context, exact selector, segment contract, and EFF category when applicable | ora_reference_lookups.md |
| resolve_position_field_value | Create or edit supplies another lookup, foreign reference, context, or segment | Exact current contract-declared target value or complete supported business key | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POS.DESIGN | decision | 12 | design_enforcement | passed->POS.ROUTE;not_required->POS.ROUTE;blocked->POS.ERROR | POS.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
