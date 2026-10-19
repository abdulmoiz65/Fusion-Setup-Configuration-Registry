# Performance Templates Defaulting Rules

Sources: existing setup guidance and [REST resource and field guidance](../../performance-template-rest-source-contract.md). Verify UI defaults for the target release and environment.

Field names below include legacy entity/FSM names. Before constructing a REST
payload, translate only the source-confirmed names in the linked contract and
validate every field against live describe metadata. For example, REST uses
`AutoPopulateMatrixMgrFlag`, `UseCalculatedRatingsOnlyFlag`, and
`AvailableToUseFlag`. Never send a legacy heading directly as a REST key.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| `DateFrom` | Current date | A new template has no supplied start date | No | |
| `DateTo` | `4712-12-31` | A new template has no supplied end date | No | |
| `TemplateTypeCode` | `ORA_STANDARD` | A new template has no supplied template type | No | |
| `SetCode` | `COMMON` | A new FSM CSV template has no supplied set code; never send SetCode in the REST root payload | No | |
| `SetId` | `0` | A new FSM template has no supplied set ID; a REST payload may contain SetId only if target describe explicitly exposes it as writable | No | |
| `EnableSyncFlag` | `Y` when profile `ORA_HRA_PERFORMANCE_DOCUMENTS_AND_GOALS_REDWOOD_ENABLED` is `Y`; otherwise `N` when it is `N` | A new template is created | Yes; derive from the profile value | resolve_performance_documents_profile |
| Update payload attributes | Send changed writable fields and child create, update, or delete parts only | PATCH request | No | inspect_template_rest_metadata |
| Parent identifiers and child context | Use the view-link context from the owning REST accessor | Child create or change | No | read_template_by_id |
| Participant role minimum and maximum values | Reset role minimum to 0 and role maximum to null | SetRoleMinimumsFlag or SetRoleMaximumsFlag is false | No | |
| `AutoPopulateMmFlag`, `DefaultMatrixPcpnRoleId`, `SendRequestToMmFlag`, `WrkSeeMgrPcpnFlag` | `N`, `null`, `N`, `N` respectively | The selected process flow has `AssignPcpnsFlag=N` | Yes; derive from the selected process flow | resolve_active_process_flow |
| `UseCalcRatingsOnlyFlag` | `N` | The selected process flow explicitly returns `IncludeTalentReviewCalibFlag=N` | Yes; derive only from an observed process-flow value | resolve_active_process_flow |
| `AllowMgrSelectMmRoleFlag` | `Y` | Manager and matrix-manager roles exist, and the selected process flow has `MgrSelectPcpnsFlag=Y` and `AssignPcpnsFlag=Y` | Yes; derive from the selected process flow and role set | resolve_process_flow_role_context |
| `AllowWkrSelectMmRoleFlag` | `Y` | Worker and matrix-manager roles exist, and the selected process flow has `WkrSelectPcpnsFlag=Y` and `AssignPcpnsFlag=Y` | Yes; derive from the selected process flow and role set | resolve_process_flow_role_context |
| `UseCalcRatingsOnlyFlag` | `N` | `CalculateRatingsFlag=N` | Yes; clear calculated-ratings-only behavior | |
| `AllMmMgrTypeFlag` | `ORA_HRA_ALL_MANAGER_TYPES` | `AutoPopulateMmFlag=Y` | Yes; derive from matrix-manager auto-population | |
| `SendRequestToMmFlag`, `DefaultMatrixPcpnRoleId`, `MmManagerTypes`, `AllMmMgrTypeFlag` | `N`, `null`, `null`, `null` respectively | `AutoPopulateMmFlag=N` | Yes; clear incompatible matrix-manager settings | |
| Calculated-rating dependent fields | Clear calculated-only, section-calculation, manager-reason, and calculated-rating visibility values when `CalculateRatingsFlag=N` | `CalculateRatingsFlag=N` | No | |
| `AvailableToUse` | `Y` | A new template-period record is created | No | |
| `GoalAlgorithmTypeCode` | `ORA_GOALPLAN` when profile `ORA_HRA_PERFORMANCE_DOCUMENTS_AND_GOALS_REDWOOD_ENABLED` is `Y`; otherwise `ORA_NONE` when it is `N` | A new template-period record is created | Yes; derive from the profile value | resolve_performance_documents_profile |
| Period dates | Default from the selected review period | A review period is selected for a new editable period | Yes | resolve_review_period |

### FSM Root-Row Materialization

For a new-template FSM archive, write `SetId=0` and `SetCode=COMMON`
explicitly in the `HRA_TEMPLATE.csv` row. Do not rely on runtime defaulting
for either column, even when the create-request default is the same. Preserve
an explicitly supplied, resolved non-common set only when the requested
template is deliberately scoped to that set.

## Period Child Defaults

For a REST create of a period eligibility-profile association, set
`TalentObjectType=TEMPLATE_PERIOD`, bind `TalentObjectId` to the owning period,
and set `ColumnValue` to that fresh period's exact `ShortName`. This is a
required owner-key value, not an optional copied attribute. Never preserve a null `ColumnValue`
from a source/read projection, and never derive it from the
customary name or eligibility-profile name.

## Template Section Defaults

A template section is created from an existing Section Definition. Inherit its supported attributes first, then apply only the overrides below. In these rules, `GOALS` is the goal section type and `ORA_DEVGOAL` is the development-goal section type.

For every REST section create, map the selected Section Definition's `SectionType`
to the template-section payload's `SectionTypeCode`; do not omit
`SectionTypeCode` merely because `SectionDefId` is present. Resolve that exact
code through `HRA_SECTION_TYPE` before preview. Apply the corresponding REST
field-name mappings for other inherited definition values (for example,
`RatingType` to `RatingTypeCode` and `PerformanceRatingModelId` to
`PerfRatingModelId`) rather than copying provider attribute names blindly.

| Field | Default or override | Applies When |
|---|---|---|
| `AddItemsConfirmCritFlag` | `N` | Add-items confirmation criteria are not enabled. |
| `CalculationRuleCode`, `FastFormulaId`, `DecimalPlaces`, `RoundingRuleCode`, `CalcMappingCode`, `MappingMethodCode`, `ItemCalculationCode` | `null` | `CalculateRatingsFlag=N`. |
| `EnableItemCommentsFlag`, `EnableSectionCommentsFlag` | `N` | The respective inherited value is `null`. |
| `UseSpecProfileFlag`, `ProfileId` | `N`, `null` | Profile V2 is enabled. |
| `RateSectionFlag` | `N` | `UseCalcRatingsOnlyFlag=Y`. |
| `ShowSectionMinWeight`, `ShowSectionWeight`, `ShowMandatory`, `UseSpecContentItemFlag` | `N`, `N`, `N`, `N` | Section type is `GOALS` or `ORA_DEVGOAL` and `EnableSyncFlag=Y`. |
| `ShowSectionMinWeight` | `N` | Section type is `REG` or `ORA_DYNAMIC_SKILLS` and `EnableSyncFlag=Y`. |
| `EnableMgrReasonFlag` | `N` | Any of `RateSectionFlag`, `ShowMgrCalcRatingFlag`, manager-evaluates-worker condition, `SectionRatingModelCode`, or `CalculationRuleCode` is `N`, absent, or unresolved. |
| `EnableMgrReasonFlag`, `UseSecrtgForPerfrtgFlag`, `RateSectionFlag`, calculation fields, `UseSecWeightsForCalc` | `N`, `N`, `N`, `null`, `N` respectively | No section rating model exists, or `CalculateRatingsFlag=N`. |
| `PerfRatingModelCode` | Equal to `SectionRatingModelCode` | `UseSecrtgForPerfrtgFlag=Y`. |
| `CalculationRuleCode` | `null` when `CalculateRatingsFlag=N`; otherwise `A` | `RateSectionFlag=Y`. |
| Role-action `SectionRatingsRequiredCode`, `EnableMgrReasonFlag` | `NOT_ALLOWED`, `N` | `RateSectionFlag=N` or is absent. |
| Worker role-action `ShareRatingsFlag`; manager role-action `UpdateProfileFlag` | `N`; `null` respectively | Both `RateSectionFlag=N` and `RateItemFlag=N`. |
| Role-action `SectionRatingsRequiredCode` | `OPTIONAL_WITH_WARNING` | `RateSectionFlag=Y`. |
| `UseSecWeightsForCalc`, `CalcMappingCode` | `N`, `ORA_POINTS_RANGE` | A calculation rule is selected. |
| `CalcMappingCode`, `UseSecWeightsForCalc` | `ORA_NUMERIC_RATING`; `Y` only when an `OS` section has at least one weighted section | `CalculationRuleCode=A`. |
| `DecimalPlaces`, `RoundingRuleCode`, `MappingMethodCode` | `ORA_2`, `STD`, `NEAR` when blank | A calculation rule is selected. |
| `FastFormulaId` | `null` | Calculation rule is not `ORA_FAST_FORMULA`. |
| `WeightSectionFlag`, `SectionWeight`, `SectionMinimumWeight` | `N`, `null`, `null` | `CalculationRuleCode=S` or `B`. |
| `ShowSectionWeight`, `ShowSectionMinWeight` | `N`, `N` | `CalculationRuleCode=S`. |
| `EnableItemsFlag`, `RateItemFlag` | `Y`, `Y` | `CalculationRuleCode` is `A`, `S`, or `B` and section type is `REG`, `GOALS`, `ORA_DEVGOAL`, or `ORA_DYNAMIC_SKILLS`. |
| Calculation display and mapping fields; `UseSecWeightsForCalc`; `EnableMgrReasonFlag` | Clear calculation fields; `N`; `N` | No calculation rule is selected. |
| `ContentTypeId`, `ContentProfileFlag` | `124`, `Y` for `GOALS`; `133`, `Y` for `ORA_DEVGOAL`; `104`, `Y` for `REG`; `134`, `Y` for `ORA_DYNAMIC_SKILLS`; otherwise `null`, `N` | The section type is resolved. |
| Content-profile, item, skill, goal, and profile-dependent fields | Clear or set to `N`: `ContentProfileFlag`, `AddItemsConfirmCritFlag`, `RateItemFlag`, `ShowMandatory`, `EnableChildItemsFlag`, `UseSpecContentItemFlag`, `EnableItemCommentsFlag`, `SkillProgressCode`, `SkillTypeCode`, `LockEvalWhenGoalSetFlag`, `ShowDescription`, `UseProfileFlag`, `UseSpecProfileFlag`, `UseWritingAssistantFlag` | `EnableItemsFlag=N`. |
| `ShowDescription`, `AddItemsConfirmCritFlag`, `EnableItemCommentsFlag` | `Y`, `Y`, `Y` | `EnableItemsFlag=Y` and section type is `GOALS`, `ORA_DEVGOAL`, `REG`, or `ORA_DYNAMIC_SKILLS`. |
| `SkillProgressCode` | `ORA_ALL_SKILL` | Section type is `ORA_DYNAMIC_SKILLS`. |
| `UseWorkerGoalsFlag`, `UpdateGoalWeightsFlag`; period `GoalAlgorithmTypeCode` | `Y`, `Y`; `ORA_GOALPLAN` for every period without documents | Section type is `GOALS` and `EnableSyncFlag=Y`. |
| `UseWorkerGoalsFlag`, `IncludeFutureItemsFlag`, `ExcludeInactiveItemsFlag`; period `GoalAlgorithmTypeCode` | `Y`, `Y`, `Y`; `ORA_GOALPLAN` for every period without documents | Section type is `ORA_DEVGOAL` and `EnableSyncFlag=Y`. |
| Profile presentation fields | `ShowDescription=N`, `UseProfileFlag=N`, `UseSpecProfileFlag=N`, `UseWritingAssistantFlag=N` | `ContentProfileFlag=N`. |
| Profile/content/goal fields | `UseProfileFlag=N`, `UseSpecProfileFlag=N`, `UseSpecContentItemFlag=N`, `UseWritingAssistantFlag=N`, `UseWorkerGoalsFlag=N` | `ContentTypeId` is blank or invalid. |
| `ProfileTypeCode`; worker role-action profile values | `null`; `UpdateProfileFlag=N`, `PersonProfileTypeId=null`, `QualifierSetId=null`, `QualifierId=null` | `UseProfileFlag=N` or is absent. |
| `ProfileId` | `null` | `UseSpecProfileFlag=N` or is absent. |
| `IncludeFutureItemsFlag`, `ExcludeInactiveItemsFlag`, `UpdateGoalWeightsFlag` | `N`, `N`, `N` | `UseWorkerGoalsFlag=N` or is absent. |
| Rating/display fields | Clear `RatingTypeCode`, `PerfRatingModelCode`, `ItemCalculationCode`; set `ShowTargetPerfRtg=N`, `ShowTargetProfLevel=N`, `ShowSectionWeight=N`, `ShowSectionMinWeight=N`, `UseSecrtgForPerfrtgFlag=N` | `RateItemFlag=N` or is absent. |
| `LockEvalWhenGoalSetFlag` | `N` | `RateItemFlag=N` or absent and `EnableItemCommentsFlag=N` or absent. |
| `RatingTypeCode` | `PER` for `GOALS` or `ORA_DEVGOAL`; otherwise `PRO` | `RateItemFlag=Y`. |
| `RatingTypeCode`, `UseSecrtgForPerfrtgFlag`, `PerfRatingModelCode`, `ItemCalculationCode` | `PRO`, `N`, `null`, `PRO` | `EnableChildItemsFlag=Y`. |
| `UseSecrtgForPerfrtgFlag`, `PerfRatingModelCode`, `ItemCalculationCode`, target display | `N`, `null`, `PRO` when calculation is enabled otherwise `null`, `ShowTargetPerfRtg=N` | `RatingTypeCode=PRO`. |
| `UseSecrtgForPerfrtgFlag`, `PerfRatingModelCode`, `ItemCalculationCode`, target display | `N`, `null`, `PER` when calculation is enabled otherwise `null`, `ShowTargetProfLevel=N` | `RatingTypeCode=PER`. |
| `ItemCalculationCode` | `PXP` | `RatingTypeCode=PAP`. |
| `PerfRatingModelCode` | Equal to `SectionRatingModelCode` when `UseSecrtgForPerfrtgFlag=Y`; otherwise `null` | Section-rating performance behavior is resolved. |
| `IncludeQstnrScoreOsFlag`, `WeightSectionFlag`, `SectionWeight`, `SectionMinimumWeight` | `N`, `N`, `null`, `null` | Section type is `QUESTIONNAIRE` and `IncludeQstnrScoringFlag=N` or absent. |

### Questionnaire Role-Action Defaults

When `IncludeQstnrScoringFlag=Y`, apply score-visibility defaults using the corresponding questionnaire-view flag. A disabled view flag clears its matching score-view code. Disabling `ViewPcpnQstnrFlag` also sets `ViewPcpnNameFlag=N` and `ViewPcpnRoleFlag=N`.

| User role type | Default behavior when scoring is enabled |
|---|---|
| `MANAGER` | Set `ViewMgrQstnrScoresFlag=ORA_YES_IMMEDIATELY` and `ViewOwnQstnrScoresFlag=null`; set worker and participant score-view codes to `Y` only when their corresponding view flags are `Y`. |
| `WORKER` | Start with `ViewMgrQstnrScoresFlag=ORA_YES_IMMEDIATELY` and `ViewOwnQstnrScoresFlag=null`. When `ViewMgrQstnrFlag=Y`, default manager score view to `N`; change it to `Y` when worker calculated ratings are shown and the questionnaire score contributes to the overall summary. Apply the same `N` then conditional `Y` rule to participant score view using `ViewPcpnQstnrFlag` and manager calculated ratings. |
| `PARTICIPANT` | Set manager, worker, and participant score-view codes to `null`, and `ViewOwnQstnrScoresFlag=ORA_NO`; change own score view to `ORA_YES_IMMEDIATELY` when participant calculated ratings are shown and the score contributes to the overall summary. |


## Template Role Action Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| `ItemRatingsRequiredCode`, `ItemCommentsRequiredCode`, `AllowNotRatedItemFlag` | `OPTIONAL_WITH_WARNING`, `OPTIONAL_WITH_WARNING`, `N` respectively | A new template-role-action record is created | No | |
| `ItemRatingsRequiredCode` | `NOT_ALLOWED` | Section type is `ORA_DYNAMIC_SKILLS` and user role type is `PARTICIPANT` | Yes; derive from section and role | resolve_template_section_role_context |
| `SectionRatingsRequiredCode` | `NOT_ALLOWED` | Section type is `OS`, `REG`, `GOALS`, `ORA_DEVGOAL`, or `ORA_DYNAMIC_SKILLS`, and `RateSectionFlag=N` | Yes; derive from section settings | resolve_template_section |
| `SectionRatingsRequiredCode` | `NOT_ALLOWED` | `UseCalcRatingsOnlyFlag=Y` | Yes; calculated-ratings-only takes precedence | |
| `SectionRatingsRequiredCode` | `OPTIONAL_WITH_WARNING` | `UseCalcRatingsOnlyFlag=N` | Yes; derive from template settings | |
| `SectionCommentsRequiredCode` | `OPTIONAL_WITH_WARNING` | Section type is `OS`, `REG`, `GOALS`, `ORA_DEVGOAL`, or `ORA_DYNAMIC_SKILLS` | Yes; derive from section type | resolve_template_section |
| `SectionCommentsRequiredCode` | `OPTIONAL_WITH_WARNING` | Section type is `WFF` and user role type is `WORKER`, or section type is `MFF` and user role type is `MANAGER` | Yes; derive from section and role | resolve_template_section_role_context |
| `ShareRatingsFlag`, `ShareCommentsFlag` | `N`, `N` respectively | User role type is `MANAGER` | Yes; derive from role type | resolve_performance_role |
| `UpdateProfileFlag` | `Y` | User role type is `MANAGER`, section type is `REG` or `ORA_DYNAMIC_SKILLS`, and `ProfileTypeCode=PERSON` | Yes; derive from section and profile type | resolve_template_section |
| `UpdateProfileFlag` | `N` | User role type is `MANAGER` and either section type is not one of `REG`, `ORA_DYNAMIC_SKILLS`, or `ProfileTypeCode` is not `PERSON` | Yes; derive from section and profile type | resolve_template_section |
| `ViewMgrQstnrScoresFlag`, `ViewOwnQstnrScoresFlag`, `ViewPcpnQstnrScoresFlag`, `ViewWkrQstnrScoresFlag` | `ORA_YES_IMMEDIATELY`, `null`, `Y` when `ViewPcpnQstnrFlag=Y`, `Y` when `ViewWrkQstnrFlag=Y` respectively | User role type is `MANAGER`, section type is `QUESTIONNAIRE`, and `IncludeQstnrScoringFlag=Y` | Yes; derive from questionnaire and section settings | resolve_template_section |
| `ViewMgrQstnrScoresFlag`, `ViewOwnQstnrScoresFlag`, `ViewPcpnQstnrScoresFlag`, `ViewWkrQstnrScoresFlag` | `null`, `null`, `null`, `null` respectively | User role type is `MANAGER`, section type is `QUESTIONNAIRE`, and `IncludeQstnrScoringFlag=N` | Yes; derive from questionnaire and section settings | resolve_template_section |
| `ShareRatingsFlag`, `ShareCommentsFlag` | `Y`, `Y` respectively | User role type is `WORKER` and section type is `OS`, `REG`, `GOALS`, `ORA_DEVGOAL`, or `ORA_DYNAMIC_SKILLS` | Yes; derive from role and section type | resolve_template_section_role_context |
| `ShareRatingsFlag`, `ShareCommentsFlag` | `N`, `N` respectively | User role type is `WORKER` and section type is `QUESTIONNAIRE` | Yes; derive from role and section type | resolve_template_section_role_context |
| `ViewWkrQstnrScoresFlag`, `ViewMgrQstnrScoresFlag`, `ViewPcpnQstnrScoresFlag` | `ORA_YES_IMMEDIATELY`, `N`, `N` respectively | User role type is `WORKER`, section type is `QUESTIONNAIRE`, and `IncludeQstnrScoringFlag=Y` | Yes; derive from questionnaire and section settings | resolve_template_section_role_context |
| `ShareRatingsFlag`, `ShareCommentsFlag` | `N`, `N` respectively | User role type is `PARTICIPANT` and section type is `OS`, `REG`, `GOALS`, `ORA_DEVGOAL`, or `ORA_DYNAMIC_SKILLS` | Yes; derive from role and section type | resolve_template_section_role_context |
| `ViewOwnQstnrScoresFlag`, `ViewWkrQstnrScoresFlag` | `ORA_NO`, `ORA_YES_IMMEDIATELY` respectively | User role type is `PARTICIPANT`, section type is `QUESTIONNAIRE`, and `IncludeQstnrScoringFlag=Y` | Yes; derive from questionnaire and section settings | resolve_template_section_role_context |

## Defaulting Order

For a new template, first apply the unset root defaults. Then resolve the Redwood profile, selected process flow, and selected role set before applying dependent defaults. Resolve each template section and its user role before applying template-role-action defaults. When more than one rule sets `UseCalcRatingsOnlyFlag`, `N` is the required result. Do not retain a conflicting value for a field controlled by a selected profile, process-flow flag, matrix-manager auto-population setting, section, or user role.

Do not convert an unavailable process-flow compatibility flag into a false value; absence is unknown, not `N`. When the target omits `IncludeTalentReviewCalibFlag`, preserve an explicit `UseCalcRatingsOnlyFlag=Y`, apply every dependent reset in this table, validate against the live template Describe allowlist, and continue through the normal immutable preview and approval flow. Treat a definite Fusion validation rejection as authoritative and do not retry it blindly; an ambiguous response requires read reconciliation before any new effect is prepared.

Every dependent relationship in this resource is a non-bypassable data
invariant. An instruction, approval, import artifact, or user request cannot
retain a contradictory value. Apply the documented reset, then stop before
preview, approval, import, or mutation if any invariant remains unsatisfied.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PT.APPLY_PAYLOAD_DEFAULTS | step | 50 | apply_default | applied->PT.ENFORCE_DEPENDENT_FIELD_INVARIANTS | PT.RESOLVE_REST_DEPENDENCIES | stop | Create or change a template or child; preserve omitted PATCH fields and record no applicable defaults for delete |
