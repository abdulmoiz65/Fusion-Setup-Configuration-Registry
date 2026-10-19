# Manage Positions Dependency Readiness

## Purpose

Defines the conditional Position target, fields, child objects, and workforce
references used by Manage Positions. Dependencies are evaluated only
for applicable operations and fields and are never created implicitly.

Shared reuse: `core.data-loader` owns loader preview, approval, import, and load-status processing; these rules supply only the Position dependency evidence required for that handoff.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Position resolver contract | Confirm the current positionsV2 describe mappings used by the requested operation |
| 2 | Position identity | Resolve the target or confirm that the proposed create identities are available |
| 3 | Current section values | Read requested sections and resolve an exact child target for update or delete |
| 4 | Position delete history | For effective-split delete, read every PositionHistoryDef page and derive the range from the immediately preceding row and selected non-first row |
| 5 | Business Unit | Resolve one active Business Unit for a supplied create or edit value |
| 6 | Department | Resolve one Department effective on the requested date |
| 7 | Job | Resolve one Job effective on the requested date |
| 8 | Location | Resolve one Location effective on the requested date when supplied |
| 9 | Position references | Resolve the Delegate Position and every Funding Position with each reference's own Business Unit |
| 10 | Valid grades | Resolve every GradeCode and GradeSetCode combination effective on the target date |
| 11 | Flexfield contexts | Resolve every populated DFF or EFF context and segment from the current polymorphic contract |
| 12 | Supplied field references | Resolve every other supplied lookup or foreign reference |
| 13 | Final mutation review | Apply every Position, child, dependency, effective-date, flexfield, key, type, and row-count rule to the final serialized DAT or ZIP before approval |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| position_contract | positionsV2 resolver contract | Conditional | The requested operation relies on Position fields or related LOV mappings | Verify | Current positionsV2 describe | inspect_positions_contract | Prevents guessed fields, child references, or source-to-target mappings | No user action unless the live contract is unavailable | Current describe-backed resolver mapping |
| position_identity | Existing Position or create-availability evidence | Conditional | Read, edit, delete, or create duplicate check | Lookup | Positions resource | find_manage_positions | Prevents an ambiguous target or duplicate create | Provide exact identity values or a bounded search fragment | Resolved Position identity or create-availability evidence |
| position_section_rows | Requested Position or child values and exact mutation target | Conditional | Get requests section values, or edit or delete requires current values or child identity | Lookup | Current positionsV2 parent and returned section links | read_position_section_rows | Supplies current values and prevents ambiguous child updates or deletes | Provide the section and a complete child key when one child row is targeted | Requested current values and exact parent or child keys |
| position_delete_history | Complete Position history and bounded split-delete range | Conditional | Effective-split delete | Lookup | All PositionHistoryDef pages | resolve_position_delete_history | Prevents deletion of the first split and derives the only permitted MERGE boundaries | Provide one exact non-first EffectiveStartDate | Predecessor EffectiveStartDate, selected EffectiveEndDate, FirstSplitFlag eligibility, and before/after evidence |
| edit_keys | Current parent and child edit keys | Conditional | An edit includes a Position or child row | Verify | Fresh current Position and child reads | read_position_section_rows | Prevents a blank-key edit from becoming an overlapping new effective row | Re-read the target row and carry its exact key; leave keys blank only for new child rows | Current parent business key and every edited child key |
| business_unit | Business Unit | Conditional | Create or edit supplies or changes Business Unit | Lookup | Current Business Unit LOV | resolve_position_business_unit | Keeps the Position attached to one active Business Unit | Provide one exact Business Unit name or ID | BusinessUnitName and BusinessUnitId |
| department | Department | Conditional | Create or edit supplies or changes Department | Lookup | Current Departments resource | resolve_position_department | Keeps the Position attached to one effective Department | Provide one exact Department name or ID and effective date | DepartmentName and DepartmentId |
| job | Job | Conditional | Create or edit supplies or changes Job | Lookup | Current Jobs LOV | resolve_position_job | Keeps the Position attached to one effective Job | Provide one exact Job name, code, or ID and effective date | JobName, JobCode, and JobId |
| location | Location | Conditional | Create or edit supplies or changes Location | Lookup | Current Locations LOV | resolve_position_location | Keeps a supplied Location exact and effective | Provide one exact Location name, code, or ID and effective date | LocationName, LocationCode, and LocationId |
| manager_assignment | Manager person and primary assignment | Conditional | Create, copy, or edit supplies a nonblank manager or supervisor reference; not applicable when manager fields are omitted or both references are explicitly cleared | Lookup | Current workersLov and the exact selected worker assignment when needed, as of Position EffectiveStartDate | resolve_position_manager_assignment | Prevents a new manager person from being paired with the previous manager assignment or a missing assignment number | Supply an exact manager business identity; choose an assignment only if eligible matches remain ambiguous | SupervisorPersonNumber, SupervisorAssignmentNumber, same-person AssignmentId evidence, effective date, and one exact eligible match |
| delegate_position | Delegate Position and its Business Unit | Conditional | A Position row supplies any DelegatePosition field | Lookup | Current Position and Business Unit resources | resolve_delegate_position | Prevents a delegate Position from being paired with the target Position's or source payload's unrelated Business Unit and prevents a display name from entering the numeric ID field | Provide one exact delegate Position code; discard copied Business Unit evidence when it conflicts | DelegatePositionCode, optional current DelegatePositionId, freshly resolved DelegatePositionBusinessUnitName, and numeric DelegatePositionBusinessUnitId |
| funding_position | Funding Position and its Business Unit | Conditional | A PositionFundingRelationship row is supplied | Lookup | Current Position and Business Unit resources | resolve_funding_position | Confirms that the funding Position and Business Unit identify the same effective Position and prevents a display name from entering the numeric ID field | Provide one exact funding Position code; discard copied Business Unit evidence when it conflicts | FundingPositionCode, optional current FundingPositionId, freshly resolved FundingPositionBusinessUnitName, and numeric FundingPositionBusinessUnitId |
| valid_grade | Grade and Grade Set | Conditional | A PositionGrade row is supplied | Lookup | Current PositionGrade describe-declared Grade reference | resolve_valid_grade | Prevents a GradeCode from being resolved without its Grade Set or outside its effective range | Provide one exact GradeCode and GradeSetCode | GradeCode, GradeSetCode, and optional current GradeId |
| flexfield_context | DFF or EFF context and populated segments | Conditional | A context-qualified segment is populated | Verify | Current Position or child polymorphic describe and returned context links | resolve_position_flexfield_context | Prevents a blank, stale, or mismatched FLEX selector and category | Provide one current context and supported segment value | Exact FLEX selector, EFF category when applicable, and current segment names |
| position_field_values | Supplied lookup, foreign reference, context, or segment | Conditional | Create or edit supplies a field governed by the current Position or child contract | Lookup | Current describe-declared LOV, returned child link, lookup type, or supported business key | resolve_position_field_value | Prevents display values, references, contexts, or segment values from being guessed | Provide one exact value and every dependent business-key component | Only current contract-declared target values |
| source_snapshot_counts | Complete source Position snapshot | Conditional | A Position is copied with one or more child sections | Verify | Paginated source Position reads as of the requested source date | read_position_section_rows | Detects a missing page, dropped child row, or invented empty child row | No user action unless the requested source scope is unclear | Row count for Position and every supported child section |
| final_create_copy_review | Final Position and child content with collected rule evidence | Conditional | A Position create or copy contains a child row | Verify | Final prepared loader content plus current read-only lookup and source-count evidence |  | Prevents submission when cross-row dates, FLEX selectors, dependent keys, duplicate checks, nonportable-field omission, or copy row-count parity is invalid | Correct the content or evidence and rerun every applicable rule before approval | All applicable Position rules passed for the unchanged final content |
| final_edit_payload_review | Final serialized edit content with fresh current-row and dependency evidence | Conditional | A Position edit is prepared | Verify | Final DAT or ZIP plus fresh Position, child, and resolver reads | read_position_section_rows | Detects conversion-time column shifts, display values in ID fields, missing flexfield declarations, missing existing-row keys, and effective-date overlaps before submission | Rebuild the source and repeat this review after every byte change | Every row classified as existing or new; current keys present only for existing rows; dependency types, flex declarations, contexts, and effective ranges match the unchanged serialized content |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every applicable dependency has exact authoritative evidence | No |
| Lookup | A documented resolver can resolve an applicable dependency | Read-only lookup only |
| Verify | Existing evidence must be confirmed without creating setup | No |
| Not Applicable | A dependency condition is false | No |
| Needs Input | A required selector or scope value is missing | No |
| Unresolved | Resolution returns no match, multiple matches, unavailable evidence, or an incompatible value | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POS.DEPENDENCIES | decision | 10 | resolve_dependency | ready->POS.DEFAULTS;not_required->POS.DEFAULTS;needs_input->POS.ERROR;unresolved->POS.ERROR | POS.FIELD_VALUES | stop | After Position and related-reference lookups and before defaulting |
