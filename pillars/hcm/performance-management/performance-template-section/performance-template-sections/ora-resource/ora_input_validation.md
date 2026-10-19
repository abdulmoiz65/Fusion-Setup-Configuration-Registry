# Performance Template Sections Input Validation

Validate configuration input and direct REST request shape before the task's selected execution workflow. This resource does not authorize a REST mutation.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Section identity | Name, section type, active status, and effective dates | Do not configure the section | Define the section identity and its period before saving it | Every section | |
| Rated or calculated section | Section rating model and calculation method | Do not enable calculated ratings | Select a compatible rating model and one documented method: Average, Sum, Band, or Fast Formula | Ratings are enabled or calculated | |
| Rated section | RateSectionFlag is N, or SectionRatingModelCode has a value | Do not create a rated section without a rating model | Set RateSectionFlag to N or select a compatible section rating model | RateSectionFlag is Y | |
| Fast Formula calculation | CalculationRuleCode is Fast Formula and FastFormulaId has a value | Do not configure the formula method | Create or select a Performance Rating Calculation formula, then populate FastFormulaId | CalculationRuleCode is Fast Formula | |
| Profile Content competency source | Documented profile-content source and item-processing choices | Do not use the section to evaluate unspecified competencies | Select the supported profile source or template content and complete applicable item processing | Section type is Profile Content | |
| Performance Goals synchronization | Evaluation type that identifies the goal plan | Do not enable synchronized goals | Select the evaluation type that maps the intended goal plan to the section | Section type is Performance Goals and synchronized goals are used | |
| Writing Assistant | Profile Content competency section plus uploaded feedback suggestions and development tips | Do not present Writing Assistant as ready | Configure the competency section and upload its documented data through the Profile Management spreadsheet flow | Writing Assistant is enabled | |
| REST root create or update | Name, Description, DateFrom, Status, SectionType, and only documented writable root attributes | Reject the request | Supply required values and remove derived, non-updateable, or display-only fields | A direct REST create or update request is prepared | resolve_section_describe |
| REST child item create or update | SectionDefinitionId and ContentItemId; item fields applicable to the parent section state | Reject the child request | Supply parent and content identities and remove read-only child attributes | templateSectionItems is present | resolve_section_describe |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| More than one competency section is planned | Enhanced Talent Profile Management and Competencies Templates are required | Stop design completion until the prerequisite capability and templates are available | |
| Person profile competencies are selected | The effective ProfileOptionValue from core.fusion-api.apps-common.profile-options via /fscmRestApi profileValues must be Y; the selected competency section needs an Item Value Set and an evaluator type visible to employees and managers | Correct the profile option or Profile Management competency-section setup | verify_person_profile_comp_section_option |
| Calculated ratings are enabled | Template Process settings must enable Calculate Ratings and choose eligible roles that can view calculated ratings | Complete template-level settings before treating the section calculation as usable | |
| A Goal or Development Goal section is synchronized | Profile option `ORA_HRA_SYNCHRONIZED_GOALS` must be confirmed Y before the synchronized-goal defaults are applied | Correct the profile option or set sync fields explicitly to their non-synchronized state | |
| A competency section is configured | ReferenceSectionName must resolve to exactly one valid competency profile section and populate ReferenceSectionId | Select the referenced competency section, resolve it, and use the returned SectionId | resolve_competency_reference_section |
| SectionRatingModelCode has no value | CalculationRuleCode, CalcMappingCode, DecimalPlaces, FastFormulaId, RoundingRuleCode, and MappingMethodCode must all be null | Clear the calculation-related values; do not apply calculation defaults | |
| RateSectionFlag is Y | SectionRatingModelCode must have a value | Select a compatible rating model or set RateSectionFlag to N | |
| CalculationRuleCode is Fast Formula | FastFormulaId must have a value | Stop the configuration until a Performance Rating Calculation formula is selected | |
| An existing section is updated or deleted | The exact SectionId must resolve and its in-use state must permit the intended action | Stop before the mutation path and correct the target or action | resolve_section_by_id |
| LOV-backed root values are supplied | Status, SectionType, CalculationRule, DecimalPlaces, MappingMetric, RoundingRule, and MappingMethod must resolve to exact LOV codes | Correct the code or remove the inapplicable value | resolve_section_status |
| Item processing values are supplied | RatingType and ItemCalculationType must resolve to exact LOV codes | Correct the code or remove the inapplicable value | resolve_item_rating_type |
| Goal-plan synchronization is configured | EvaluationType must resolve to an exact goal-plan evaluation-type code | Correct the evaluation type | resolve_goal_plan_evaluation_type |
| SectionWeight and SectionMinWeight are supplied with WeightSectionFlag=Y | SectionWeight must be greater than or equal to SectionMinWeight | Correct the two weights before import | |
| RatingTypeCode is PER or PAP and RateItemFlag is Y | PerfRatingModelCode must have a value | Select a compatible performance rating model or use the section rating model where `UseSecrtgForPerfrtgFlag` is Y | find_active_rating_model |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Section type is supported | Use Profile Content, Performance Goals, Development Goals, Questionnaire, Overall Summary, Worker Final Feedback, or Manager Final Feedback; competency text-field sections are not supported in performance documents | Every new section | |
| Rating type matches section type | Profile Content can use Proficiency, Performance, or Proficiency and Performance; Performance Goals and Development Goals use Performance | Content items are enabled | |
| Item calculation matches rating type | For Proficiency and Performance choose Proficiency, Performance, or Proficiency multiplied by Performance; default calculation methods for other rating types cannot be changed | Profile Content items use Proficiency and Performance | |
| Character-limit applicability is understood | Minimum and maximum limits apply to evaluation comments in worker self-evaluation, manager evaluation, and participant feedback; character count includes letters, numbers, and HTML tags | Comment limits are configured | |
| Root text and dates meet the REST contract | Name is at most 240 characters; Description and Comments are at most 4,000 characters; Name and DateFrom are required; reject a direct request that violates these rules | A REST root payload is supplied | |
| Rating-model and calculation fields are coherent | When SectionRatingModelCode is blank, CalculationRuleCode, CalcMappingCode, DecimalPlaces, FastFormulaId, RoundingRuleCode, and MappingMethodCode must be null; when CalculationRuleCode is Fast Formula, FastFormulaId is required | A direct REST root payload is supplied | |
| Rate section and rating model are coherent | RateSectionFlag defaults to N when omitted. If RateSectionFlag is Y, SectionRatingModelCode must have a value. | A new, regenerated, or direct REST root payload is prepared | |
| Unweighted section fields are coherent | If WeightSectionFlag is N, SectionWeight and SectionMinWeight must both be null/blank. | A new, regenerated, or direct REST root payload is prepared | |
| Rate section dependencies are coherent | If RateSectionFlag is N, WeightSectionFlag and EnableMgrReasonFlag must be N and SectionWeight and SectionMinWeight must be null/blank. | A new, regenerated, or direct REST root payload is prepared | |
| Calculation defaults match the rule | A uses ORA_NUMERIC_RATING/ORA_2/STD/NEAR; S, B, and ORA_FAST_FORMULA use ORA_POINTS_RANGE/ORA_2/STD/NEAR. Fast Formula requires FastFormulaId. | CalculationRuleCode has a value | |
| Non-formula calculation rules force item processing | A, S, and B require EnableItemsFlag=Y and RateItemFlag=Y; do not allow overrides. | CalculationRuleCode is A, S, or B | |
| Empty calculation rule clears dependent values | DecimalPlaces, RoundingRuleCode, CalcMappingCode, MappingMethodCode, FastFormulaId must be null and UseSecWeightsForCalc and EnableMgrReasonFlag must be N. | CalculationRuleCode has no value | |
| Disabled item processing clears dependent values | If EnableItemsFlag is N, ContentProfileFlag, AddItemsConfirmCritFlag, RateItemFlag, ShowMandatory, EnableChildItemsFlag, UseSpecContentItemFlag, EnableItemCommentsFlag, and LockEvalWhenGoalSetFlag must be N; SkillProgressCode and SkillTypeCode must be null. | A new or regenerated FSM CSV row is prepared | |
| Disabled item rating clears dependent values | If RateItemFlag is N, ShowTargetPerfRtg, ShowTargetProfLevel, and UseSecrtgForPerfrtgFlag must be N; RatingTypeCode, PerfRatingModelCode, and ItemCalculationCode must be null. | A new or regenerated FSM CSV row is prepared | |
| Goal, Development Goal, Competency, and Dynamic Skills item rules | Goal and Development Goal with rated items require PER. Competency and Dynamic Skills with rated items allow PER, PRO, or PAP and default PRO. Those types with enabled items require EnableItemCommentsFlag=Y. | Applicable section category | |
| Item-rating calculation and model are coherent | PRO forces ItemCalculationCode=PRO and clears performance-target/model fields; PER forces ItemCalculationCode=PER and ShowTargetProfLevel=N; PAP permits PER, PRO, or PAP and defaults PRO. PER or PAP requires PerfRatingModelCode. | RateItemFlag is Y | find_active_rating_model |
| Synchronized-goal defaults are coherent | Goal plus `ORA_HRA_SYNCHRONIZED_GOALS=Y` requires EnableSyncFlag=Y and EvaluationTypeCode=ORA_HRA_EVAL_TYPE_DEFAULT; Development Goal plus the option=Y requires EnableSyncFlag=Y. | Applicable section category | |
| Goal/content mapping is coherent | Goal=ContentTypeId 124; Development Goal=133; Competency=104; Dynamic Skills=134 and SkillProgressCode=ORA_ALL_SKILL. Other section categories require ContentTypeId null and ContentProfileFlag=N. | A new or regenerated FSM CSV row is prepared | |
| New-record source isolation | A comparable exported row may supply only CSV layout, required transport/relationship fields, formatting, and required translations. Every other value must be user-supplied or covered by a documented default; otherwise use null, N for flags, or 0 for numeric weights, amounts, and counts. | A new FSM CSV record is built from an exported comparator | |
| Overall Summary section comments default | Default EnableSectionCommentsFlag to Y only when SectionTypeCode is OS and the flag is omitted | A new or regenerated FSM CSV row is prepared | |
| Final Feedback field restriction | For SectionTypeCode WFF or MFF, only Name, Description, Comments, DateFrom, DateTo, StatusCode, and SectionTypeCode may retain business values. Every other configuration field must be null, and every Boolean field must be N. ViewInstanceName and the derived GroupingKey remain required FSM transport fields; system ID columns retain the exported null representation. | A new or regenerated FSM CSV row is prepared | |
| Questionnaire field restriction | For SectionTypeCode QUESTIONNAIRE, only Name, Description, Comments, DateFrom, DateTo, StatusCode, SectionTypeCode, IncludeQstnrScoreOsFlag, IncludeQstnrScoringFlag, WeightSectionFlag, SectionWeight, and SectionMinWeight may retain business values. Every other configuration field must be null, and every other Boolean field must be N. ViewInstanceName and the derived GroupingKey remain required FSM transport fields; system ID columns retain the exported null representation. | A new or regenerated FSM CSV row is prepared | |
| Direct REST payload excludes derived values | Do not post lookup meanings, InUseFlag, SectionDefnInUseFlag, or non-updateable attributes; reject the direct request when present | A REST root or child payload is supplied | resolve_section_describe |
| Child weights and relationships are coherent | SectionDefinitionId references the parent; ContentItemId is unique within the section; MinimumWeight is not greater than Weight; reject invalid child rows | A child item payload is supplied | |
| Flag and dependent-field values are applicable | Use boolean semantics for flags; reject dependent profile, content-item, worker-goal, or child values when their parent condition is false | A direct REST payload contains conditional flags or child rows | |
| LOV-backed root fields use valid codes | Resolve Status, SectionType, CalculationRule, DecimalPlaces, MappingMetric, RoundingRule, and MappingMethod using their individual LOV contracts; reject a code that does not resolve | A direct REST root payload supplies any of these fields | resolve_section_status |
| Item rating and calculation codes are valid | Resolve RatingType and ItemCalculationType using their individual LOV contracts; reject a code that does not resolve | Item processing is supplied | resolve_item_rating_type |
| Rating model and selected levels are compatible | The selected rating model must resolve in the effective rating-model LOV; a selected target level must resolve under that model | A section or child item supplies rating model or target level values | find_active_rating_model |
| Profile-content and specified-profile values are valid | Resolve competency content type, reference section, profile type section, and specified profile from their documented LOVs; reject values outside the returned scope | Profile Content configuration supplies these values | resolve_competency_reference_section |

| FSM CSV escaping | When creating or regenerating a CSV member, write headers and ordinary values without double quotes. Add double quotes only for an individual value containing a comma, double quote, carriage return, or line feed; double embedded quotes. Reject blanket-quoted CSV members. | FSM CSV import is prepared or revalidated | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| HRA_SECTIONS.VALIDATE_CONFIG | decision | 10 | validate_input | valid->HRA_SECTIONS.REFERENCE_LOOKUPS;invalid->HRA_SECTIONS.HANDLE_ISSUES | none | continue | A Performance Template Sections configuration is being designed or reviewed |

## Source Material

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/considerations-for-creating-performance-template-sections.html | Section types, ratings, content, and source options |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/how-can-i-create-multiple-competency-type-sections.html | Multiple competency-section prerequisite and setup |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/populate-performance-documents-with-person-profile-competencies.html | Person-profile competency prerequisites |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/guidelines-for-setting-up-calculated-ratings-in-performance.html | Calculated-rating inputs |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/how-you-use-fast-formulas-in-performance-documents.html | Fast Formula prerequisites |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/options-for-item-processing-in-a-performance-template-section.html | Item-processing validation |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/how-you-set-the-minimum-and-maximum-character-limits-for-evaluation-comments.html | Evaluation-comment limits |
