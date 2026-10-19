# Performance Template Sections Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---:|---|---|
| 1 | Profile Management and rating models | Make required competency templates, profile options, and rating models available before selecting them in a section |
| 2 | Goal or development-goal source | Establish the goal plan, evaluation type, or development-goal inclusion policy before configuring the matching section |
| 3 | Calculated-rating design | Select calculation, rounding, mapping, and visibility settings for sections that use calculated ratings |
| 4 | Writing Assistant content | Upload competency feedback suggestions and development tips before relying on Writing Assistant |
| 5 | REST request metadata | Read the resource describe metadata and, for updates or deletes, resolve the target section before taking a mutation path |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| HRA_SECTIONS.RATING_MODEL | Profile Rating Model | Conditional | RateSectionFlag is Y or a section is calculated | Required | Profile Management setup | | A rating model is required for a rated section and to enable calculated ratings | Select a compatible section rating model before enabling rating or configuring the calculation rule | Rating model |
| HRA_SECTIONS.FAST_FORMULA | Performance Rating Calculation Fast Formula | Conditional | CalculationRuleCode is Fast Formula | Required | Manage Fast Formulas setup | | FastFormulaId is required to calculate the section rating | Create and select the formula before enabling the method | FastFormulaId |
| HRA_SECTIONS.MULTI_COMPETENCY | Enhanced Talent Profile Management and Competencies Template | Conditional | Multiple competency-type sections are needed | Required | Enhanced Talent Profile Management | | Multiple competency sections rely on competency sections defined from Competencies Templates | Enable the prerequisite and define the required competency sections | Competency section names |
| HRA_SECTIONS.PERSON_PROFILE_COMP_SECTION_OPTION | Person profile competency section profile option | Conditional | Person profile competencies are selected | Required | core.fusion-api.apps-common.profile-options via /fscmRestApi profileValues | verify_person_profile_comp_section_option | The option enables person-profile competency sections | Confirm the returned ProfileOptionValue is Y before configuring person profile competencies | Confirmed effective ProfileOptionValue |
| HRA_SECTIONS.WRITING_ASSISTANT | Feedback suggestions and development tips | Conditional | Writing Assistant is enabled for managers | Required | Profile Management Item Catalog spreadsheet flow | | Writing Assistant suggestions are associated with competencies and proficiency levels | Upload and save the required data before rollout | Competencies, feedback suggestions, development tips |
| HRA_SECTIONS.REST_METADATA | REST describe metadata | Yes | A direct REST create, update, delete, or child-item request is proposed | Lookup | GET /latest/talentPerformanceTemplateSections/describe | resolve_section_describe | Describe metadata is authoritative for less-common field updateability | Resolve permitted fields before preparing the request | Writable attributes and updateability |
| HRA_SECTIONS.EXISTING_SECTION | Existing section identity and in-use state | Conditional | A direct REST update or delete is proposed | Lookup | GET /latest/talentPerformanceTemplateSections/{SectionId} | resolve_section_by_id | In-use state, object version, and current values constrain safe change and deletion | Resolve the exact target and stop if it is in use or cannot be changed | SectionId, ObjectVersionNumber, InUseFlag, SectionDefnInUseFlag, Status, SectionType |
| HRA_SECTIONS.CONFIGURATION_LOVS | Section configuration lookup values | Conditional | Root fields use Status, SectionType, CalculationRule, DecimalPlaces, MappingMetric, RoundingRule, or MappingMethod | Lookup | core.fusion-api.apps-common.lookups via /fscmRestApi selected lookup view | resolve_section_status | The caller must use supported codes rather than display meanings | Resolve each supplied code with its field-specific resolver through the core skill | Validated code and meaning |
| HRA_SECTIONS.ITEM_LOVS | Item-processing lookup values | Conditional | RatingType or ItemCalculationType is supplied | Lookup | core.fusion-api.apps-common.lookups via /fscmRestApi selected lookup view | resolve_item_rating_type | Item processing requires valid type and calculation codes | Resolve each supplied code with its field-specific resolver through the core skill | Validated code and meaning |
| HRA_SECTIONS.GOAL_PLAN_EVALUATION | Goal-plan evaluation type | Conditional | Synchronized Performance Goals uses EvaluationType | Lookup | core.fusion-api.apps-common.lookups via /fscmRestApi selected lookup view | resolve_goal_plan_evaluation_type | The evaluation type determines the eligible goal-plan mapping | Resolve the supplied evaluation type through the core skill | Validated evaluation-type code and meaning |
| HRA_SECTIONS.SYNCHRONIZED_GOALS_OPTION | Synchronized Goals profile option | Conditional | Goal or Development Goal synchronization is requested | Required | core.fusion-api.apps-common.profile-options via /fscmRestApi profileValues | verify_synchronized_goals_profile_option | The effective option controls whether the synchronized-goal defaults can be applied | Confirm the returned ProfileOptionValue is Y before applying the synchronized-goal defaults | Confirmed effective ProfileOptionValue |
| HRA_SECTIONS.RATING_MODEL_LEVEL | Rating model and rating levels | Conditional | Section or child item supplies rating model or target rating level | Lookup | Supplied talentRatingModels and ratingLevelsLOV endpoints | find_active_rating_model | Selected model and level must be valid in the effective model scope | Resolve the model, then resolve the level for that model | RatingModelId and valid rating level |
| HRA_SECTIONS.PROFILE_CONTENT_LOVS | Competency content, reference section, profile type section, and specified profile | Conditional | Profile Content fields are supplied | Lookup | Supplied contentTypesLOV, profileTypeSectionsLOV, and profilesLov endpoints | resolve_competency_reference_section | Profile-content values must be valid for the selected content and subscriber scope | Resolve content type first, then resolve the competency reference section and populate ReferenceSectionId from its SectionId; resolve profile type section or profile as applicable | ContentTypeId, ReferenceSectionId, SubscriberCode, ProfileId |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Required | A documented prerequisite must be available before the section configuration can be considered complete | No |
| Conditional | The prerequisite applies only to the selected section design | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| HRA_SECTIONS.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | ready->HRA_SECTIONS.APPLY_DEFAULTS;missing->HRA_SECTIONS.HANDLE_ISSUES | HRA_SECTIONS.REFERENCE_LOOKUPS | continue | Reference lookups completed |
