# Performance Template Sections Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| CalculationRuleCode, CalcMappingCode, DecimalPlaces, FastFormulaId, RoundingRuleCode, MappingMethodCode | null | SectionRatingModelCode has no value. This rule takes precedence over calculation-related defaults. | Yes | |
| EnableSyncFlag; EvaluationTypeCode | Y; ORA_HRA_EVAL_TYPE_DEFAULT | The section is Goal (`SectionTypeCode=GOAL`) and profile option `ORA_HRA_SYNCHRONIZED_GOALS` is Y. | Yes | verify_synchronized_goals_profile_option |
| EnableSyncFlag | Y | The section is Development Goal (`SectionTypeCode=ORA_DEVGOAL`) and profile option `ORA_HRA_SYNCHRONIZED_GOALS` is Y. | Yes | verify_synchronized_goals_profile_option |
| ReferenceSectionId | resolved SectionId for the supplied ReferenceSectionName | The section is a competency section. | Yes | resolve_competency_reference_section |
| WeightSectionFlag; SectionWeight; SectionMinWeight; EnableMgrReasonFlag | N; null; null; N | `RateSectionFlag` is N. | Yes | |
| SectionWeight; SectionMinWeight | null; null | `WeightSectionFlag` is N. | Yes | |
| CalcMappingCode; DecimalPlaces; RoundingRuleCode; MappingMethodCode | ORA_NUMERIC_RATING; ORA_2; STD; NEAR | `CalculationRuleCode` is Average (`A`). | Yes | |
| CalcMappingCode; DecimalPlaces; RoundingRuleCode; MappingMethodCode | ORA_POINTS_RANGE; ORA_2; STD; NEAR | `CalculationRuleCode` is Sum (`S`), Band (`B`), or Fast Formula (`ORA_FAST_FORMULA`). | Yes | |
| EnableItemsFlag; RateItemFlag | Y; Y | `CalculationRuleCode` is Average (`A`), Sum (`S`), or Band (`B`). | Yes | |
| DecimalPlaces; RoundingRuleCode; CalcMappingCode; MappingMethodCode; FastFormulaId; UseSecWeightsForCalc; EnableMgrReasonFlag | null; null; null; null; null; N; N | `CalculationRuleCode` has no value. | Yes | |
| ContentProfileFlag; AddItemsConfirmCritFlag; RateItemFlag; ShowMandatory; EnableChildItemsFlag; UseSpecContentItemFlag; EnableItemCommentsFlag; SkillProgressCode; SkillTypeCode; LockEvalWhenGoalSetFlag | N; N; N; N; N; N; N; null; null; N | `EnableItemsFlag` is N. | Yes | |
| RateItemFlag; RatingTypeCode | N; null | The section is Goal, Development Goal, Competency, or Dynamic Skills and `EnableItemsFlag` is N. | Yes | |
| EnableItemCommentsFlag | Y | The section is Goal, Development Goal, Competency, or Dynamic Skills and `EnableItemsFlag` is Y. | Yes | |
| ShowTargetPerfRtg; ShowTargetProfLevel; RatingTypeCode; UseSecrtgForPerfrtgFlag; PerfRatingModelCode; ItemCalculationCode | N; N; null; N; null; null | `RateItemFlag` is N. | Yes | |
| RatingTypeCode | PER | The section is Goal or Development Goal and `RateItemFlag` is Y. | Yes | |
| RatingTypeCode | PRO | The section is Competency or Dynamic Skills and `RateItemFlag` is Y without a supplied valid type. Allowed values are PER, PRO, and PAP. | No | |
| ShowTargetPerfRtg; UseSecrtgForPerfrtgFlag; PerfRatingModelCode; ItemCalculationCode | N; N; null; PRO | `RatingTypeCode` is PRO. | Yes | |
| ItemCalculationCode; ShowTargetProfLevel | PER; N | `RatingTypeCode` is PER. | Yes | |
| ItemCalculationCode | PRO | `RatingTypeCode` is PAP and no item calculation is supplied. Allowed values are PER, PRO, and PAP. | No | |
| PerfRatingModelCode | SectionRatingModelCode | `RatingTypeCode` is PER or PAP, `RateItemFlag` is Y, and `UseSecrtgForPerfrtgFlag` is Y. | Yes | |
| SkillProgressCode | ORA_ALL_SKILL | The section is Dynamic Skills. | Yes | |
| UseWorkerGoalsFlag; UpdateGoalWeightsFlag | Y; Y | The section is Goal and `EnableSyncFlag` is Y. | Yes | |
| UseWorkerGoalsFlag; ExcludeInactiveItemsFlag; IncludeFutureItemsFlag | Y; Y; Y | The section is Development Goal and `EnableSyncFlag` is Y. | Yes | |
| ContentTypeId; ContentProfileFlag | 124; Y | The section is Goal. | Yes | |
| ContentTypeId; ContentProfileFlag | 133; Y | The section is Development Goal. | Yes | |
| ContentTypeId; ContentProfileFlag | 104; Y | The section is Competency. | Yes | |
| ContentTypeId; ContentProfileFlag | 134; Y | The section is Dynamic Skills. | Yes | |
| ContentTypeId; ContentProfileFlag | null; N | The section is not Goal, Development Goal, Competency, or Dynamic Skills. | Yes | |
| Status | A | A new performance section has no supplied status. | Yes | |
| RateSectionFlag | N | A new or regenerated FSM CSV row has no supplied rate-section value. | No | |
| DateFrom | Current date | A new performance section has no supplied DateFrom. | Yes | |
| DateTo | 4712-12-31 | A new performance section has no supplied DateTo. | Yes | |
| SectionType | REG | A direct REST create omits SectionType and no parent template context supplies a section type | Yes | |
| EnableSectionCommentsFlag | Y | SectionTypeCode is OS and EnableSectionCommentsFlag has no supplied value | No | |
| Overall Summary direct-REST inapplicable flags | N for EnableItemsFlag, ContentProfileFlag, FreeFormAllowedFlag, AddItemsConfirmCritFlag, RateItemFlag, UseSecrtgForPerfrtgFlag, ShowSectionWeight, ShowSectionMinWeight, ShowMandatory, ShowCritical, ShowDescription, ShowMeasurement, ShowDueDate, ShowReminderDate, ShowOwnedBy, ShowStatus, ShowPercentComplete, UseProfileFlag, UseSpecProfileFlag, UseWorkerGoalsFlag, UseSpecContentItemFlag, ShowTargetPerfRtg, and ShowTargetProfLevel; null for ContentTypeId, RatingTypeCode, PerfRatingModelId, ItemCalculationCode, ProfileTypeId, and ProfileId | SectionTypeCode is OS and a direct REST create or update is prepared | Yes | resolve_section_describe |
| Final Feedback configuration fields | null for CalculationRuleCode, CalcMappingCode, DecimalPlaces, FastFormulaId, RoundingRuleCode, MappingMethodCode, RatingTypeCode, ItemCalculationCode, SectionRatingModelCode, ContextName, PerfRatingModelCode, ProfileTypeCode, ProfileCode, ReferenceSectionName, ReferenceProfileTypeId, EvaluationTypeCode, SectionWeight, SectionMinWeight, SkillProgressCode, and SkillTypeCode; N for all Boolean fields, including RateSectionFlag, WeightSectionFlag, EnableItemsFlag, ContentProfileFlag, FreeFormAllowedFlag, AddItemsConfirmCritFlag, RateItemFlag, UseSecrtgForPerfrtgFlag, ShowTargetPerfRtg, ShowTargetProfLevel, ShowSectionWeight, ShowSectionMinWeight, ShowMandatory, ShowCritical, ShowDescription, ShowMeasurement, ShowDueDate, ShowReminderDate, ShowOwnedBy, ShowStatus, ShowPercentComplete, UseProfileFlag, UseSpecProfileFlag, UseWorkerGoalsFlag, UseSpecContentItemFlag, UseSecWeightsForCalc, EnableChildItemsFlag, ExcludeInactiveItemsFlag, IncludeFutureItemsFlag, UpdateGoalWeightsFlag, EnableItemCommentsFlag, EnableSectionCommentsFlag, EnableSyncFlag, IncludeQstnrScoreOsFlag, IncludeQstnrScoringFlag, EnableMgrReasonFlag, and LockEvalWhenGoalSetFlag | SectionTypeCode is WFF or MFF. Preserve only Name, Description, Comments, DateFrom, DateTo, StatusCode, and SectionTypeCode as business values. Retain ViewInstanceName and derived GroupingKey as required FSM transport fields; retain exported null representation for system ID columns. | Yes | |
| Questionnaire configuration fields | null for CalculationRuleCode, CalcMappingCode, DecimalPlaces, FastFormulaId, RoundingRuleCode, MappingMethodCode, RatingTypeCode, ItemCalculationCode, SectionRatingModelCode, ContextName, PerfRatingModelCode, ProfileTypeCode, ProfileCode, ReferenceSectionName, ReferenceProfileTypeId, EvaluationTypeCode, SkillProgressCode, and SkillTypeCode; N for all Boolean fields except IncludeQstnrScoreOsFlag, IncludeQstnrScoringFlag, and WeightSectionFlag. Preserve supplied values for IncludeQstnrScoreOsFlag, IncludeQstnrScoringFlag, WeightSectionFlag, SectionWeight, and SectionMinWeight only where consistent with the general `RateSectionFlag` rules. | SectionTypeCode is QUESTIONNAIRE. Preserve only Name, Description, Comments, DateFrom, DateTo, StatusCode, SectionTypeCode, and the five named questionnaire fields as business values. Retain ViewInstanceName and derived GroupingKey as required FSM transport fields; retain exported null representation for system ID columns. | Yes | |

## Terminology and Precedence

The import header is `SectionTypeCode`. In these rules, Goal maps to `GOAL` and Development Goal maps to `ORA_DEVGOAL`. Competency and Dynamic Skills are semantic section categories; resolve their supported section-type code through the section-type LOV before generating an import. `CalculationMappingCode` and `UseSectionWeightsForCalculationFlag` in a business request map to CSV headers `CalcMappingCode` and `UseSecWeightsForCalc`.

Apply type-specific Worker/Manager Final Feedback and Questionnaire restrictions first. Apply the general rate-section, calculation, item-processing, and content rules next. A more-specific rule in this resource overrides a general default. `RateSectionFlag=N` forces `WeightSectionFlag=N`, `SectionWeight=null`, `SectionMinWeight=null`, and `EnableMgrReasonFlag=N`; independently, `WeightSectionFlag=N` always forces both weight fields to null.

Every conditional relationship in this resource is a non-bypassable data
invariant. An instruction, approval, import artifact, or user request cannot
retain a contradictory value. Apply the required normalization, then stop
before preview, approval, import, or mutation if any invariant remains unsatisfied.

## New-Record Source Isolation

When a new FSM record is based on a comparable exported row, use that row only for CSV layout, required transport and relationship fields, effective-date/key formatting, and required translation lineage. Do not inherit its business or configuration values.

Populate a new business/configuration field only when the user explicitly supplied it or a documented defaulting rule in this resource applies. Otherwise set the field to null; use `N` for a Boolean flag and `0` for a numeric amount or count. For section weights, the specific rule takes precedence: set SectionWeight and SectionMinWeight to null whenever WeightSectionFlag is N. This applies to every inherited setting, including section weighting, synchronization, models, calculation options, item processing, profile/content choices, visibility fields, and comments. Do not use a comparator's populated value as an implied default.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| HRA_SECTIONS.APPLY_DEFAULTS | step | 40 | apply_default | applied->HRA_SECTIONS.ENFORCE_DEPENDENT_FIELD_INVARIANTS | HRA_SECTIONS.CHECK_DEPENDENCIES | continue | Dependencies are ready and documented defaults apply |

## Source Material

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/calculated-ratings.html | Calculated-rating behavior and rollup context |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/guidelines-for-setting-up-calculated-ratings-in-performance.html | Decimal, rounding, mapping, and default settings |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/how-performance-ratings-using-the-average-method-are-calculated.html | Average-method calculation examples and weighting context |
