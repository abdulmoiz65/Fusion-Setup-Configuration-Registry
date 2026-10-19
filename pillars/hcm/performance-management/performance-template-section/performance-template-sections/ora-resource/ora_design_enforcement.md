# Performance Template Sections Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---:|---|---|
| 1 | Select type-specific content behavior | Configure competency, goal, development-goal, questionnaire, summary, or final-feedback behavior consistent with the selected type |
| 2 | Complete rating design | Where ratings are used, align rating models, calculation rule, weights, rounding, mapping, and role visibility |
| 3 | Complete optional feature prerequisites | Meet the documented prerequisites for multiple competency sections, person-profile competencies, and Writing Assistant |
| 4 | Review disclosure and enforcement limits | Confirm role visibility and understand the documented limits of comment and justification enforcement for HDL updates |
| 5 | Enforce dependent-field invariants | Re-evaluate every applicable conditional relationship after normalization. A bypass request or residual contradiction blocks the run. |
| 6 | Protect direct REST operations | Reject derived fields, invalid conditional combinations, and changes that bypass in-use, authorization, or destructive-transition safeguards |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A competency section has a text field type | Blocker | | The type is unsupported in performance documents | Use a supported competency configuration | Yes |
| Multiple competency sections are used | Blocker | | Enhanced Talent Profile Management or its Competencies Template sections are unavailable | Enable the prerequisite and define the competency sections before adding them to the template | Yes |
| Calculated ratings are configured | Blocker | | Rating model, calculation rule, or template calculated-rating activation is incomplete | Complete the section and template settings before using calculated ratings | Yes |
| RateSectionFlag is Y | Blocker | | SectionRatingModelCode has no value | Set RateSectionFlag to N or select a compatible section rating model | Yes |
| RateSectionFlag is N | Blocker | | WeightSectionFlag or EnableMgrReasonFlag is not N, or SectionWeight or SectionMinWeight is not null | Set the flags to N and both weights to null | Yes |
| Any documented dependent-field rule applies | Blocker | | The normalized payload retains a contradictory value, or a request asks to bypass the rule. | Apply the required reset and re-evaluate all applicable relationships. If any invariant remains unsatisfied, stop before preview, approval, import, or mutation; no request or approval can waive it. | Yes, only by making the payload compliant |
| WeightSectionFlag is N | Blocker | | SectionWeight or SectionMinWeight is not null | Clear both weight fields before import | Yes |
| SectionWeight and SectionMinWeight are supplied | Blocker | | SectionWeight is less than SectionMinWeight | Correct the weights before import | Yes |
| A Goal or Development Goal section is synchronized | Blocker | | `ORA_HRA_SYNCHRONIZED_GOALS` is not confirmed Y | Confirm the profile option before applying synchronized-goal defaults | Yes |
| A competency section is configured | Blocker | resolve_competency_reference_section | ReferenceSectionName is absent, does not resolve to exactly one competency profile section, or ReferenceSectionId differs from the resolved SectionId | Resolve the reference and populate ReferenceSectionId from the returned SectionId | Yes |
| CalculationRuleCode is A, S, or B | Blocker | | EnableItemsFlag or RateItemFlag is not Y | Set both flags to Y; they cannot be overridden | Yes |
| RatingTypeCode is PER or PAP with RateItemFlag Y | Blocker | find_active_rating_model | PerfRatingModelCode has no value | Select a compatible performance rating model or use the section rating model | Yes |
| A new section is cloned from an exported comparator | Blocker | | A business or configuration value was inherited without an explicit user value or documented default | Clear the value to null, N for flags, or 0 for numeric amounts and counts; when WeightSectionFlag is N, clear SectionWeight and SectionMinWeight to null. Retain only structural, transport, relationship, and required translation fields from the comparator | Yes |
| SectionTypeCode is WFF or MFF | Blocker | | A non-excepted configuration field is populated or a Boolean field is not N | Retain only Name, Description, Comments, DateFrom, DateTo, StatusCode, and SectionTypeCode; clear other configuration fields and set Boolean fields to N | Yes |
| SectionTypeCode is QUESTIONNAIRE | Blocker | | A field outside Name, Description, Comments, DateFrom, DateTo, StatusCode, SectionTypeCode, IncludeQstnrScoreOsFlag, IncludeQstnrScoringFlag, WeightSectionFlag, SectionWeight, and SectionMinWeight is populated, or a non-excepted Boolean field is not N | Clear other configuration fields and set non-excepted Boolean fields to N | Yes |
| CalculationRuleCode is Fast Formula | Blocker | | FastFormulaId has no value | Create or select a Performance Rating Calculation formula, then populate FastFormulaId | Yes |
| Writing Assistant is enabled | Blocker | | The section is not Profile Content for competencies, or required tips and feedback suggestions are not uploaded | Configure the Profile Content section and load the competency data | Yes |
| Manager justification is enabled | Warning | | The design expects employees to view the manager justification | The justification is visible to management hierarchy, eligible HR specialists, and qualifying matrix managers, not employees | Yes |
| Comment character limits are configured | Warning | | The design relies on HDL to enforce limits | Use interactive performance-document evaluation tasks for enforcement; the documented limit is not enforced by HDL updates | Yes |
| A direct REST mutation is proposed | Blocker | resolve_section_describe | Payload includes derived meanings, InUseFlag, SectionDefnInUseFlag, or other non-updateable attributes | Use describe metadata to construct only the permitted operation payload | Yes |
| A direct REST update or delete is proposed | Blocker | resolve_section_by_id | The target is in use, immutable for the change, or caller lacks the required manage/delete permission | Stop before the mutation; correct the target or obtain the required authorized workflow and approval | No |
| Child items are supplied | Blocker | | Parent state does not permit children, ContentItemId is duplicated or inapplicable, or child values conflict with parent-governed rating models and flags | Remove invalid child rows or correct the parent configuration before submission | Yes |
| Dynamic Skills is selected | Blocker | | Redwood performance documents/goals or Skills Enrichment is disabled, or skills values violate the documented Dynamic Skills constraints | Enable the required features or select a supported type and values | Yes |
| LOV-backed configuration is supplied | Blocker | resolve_section_status | A supplied status, section type, calculation, decimal, mapping, item processing, or goal-plan evaluation value does not resolve through its documented LOV | Resolve every supplied value through its field-specific resolver and correct invalid codes | Yes |
| Rating or profile references are supplied | Blocker | find_active_rating_model | A rating model, rating level, profile type section, content type, or specified profile is outside its documented LOV scope | Resolve the reference through its field-specific resolver and correct the selection | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| HRA_SECTIONS.ENFORCE_DEPENDENT_FIELD_INVARIANTS | decision | 50 | design_enforcement | conforming->HRA_SECTIONS.ENFORCE_DESIGN;blocked->HRA_SECTIONS.HANDLE_ISSUES | HRA_SECTIONS.APPLY_DEFAULTS | continue | Every applicable dependent-field rule is normalized and compliant |
| HRA_SECTIONS.ENFORCE_DESIGN | decision | 60 | design_enforcement | conforming->HRA_SECTIONS.READINESS_GATE;blocked->HRA_SECTIONS.HANDLE_ISSUES | HRA_SECTIONS.ENFORCE_DEPENDENT_FIELD_INVARIANTS | continue | A section design or direct REST request is ready for final review |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_section_describe | A direct REST request is prepared | Permitted fields and updateability | ora_reference_lookups.md |
| resolve_section_by_id | A direct REST update or delete is proposed | Target identity, object version, current values, and in-use flags | ora_reference_lookups.md |
| resolve_section_status | A common-lookup configuration value is supplied | Validated Status code and Meaning | ora_reference_lookups.md |
| resolve_item_rating_type | Item processing values are supplied | Validated RatingType code and Meaning | ora_reference_lookups.md |
| resolve_goal_plan_evaluation_type | Synchronized Performance Goals is configured | Validated evaluation-type code and Meaning | ora_reference_lookups.md |
| find_active_rating_model | Rating model or level values are supplied | RatingModelId and effective model identity | ora_reference_lookups.md |
| resolve_competency_content_type | Profile Content values are supplied | Competency ContentTypeId | ora_reference_lookups.md |
| resolve_competency_reference_section | A competency section is configured | Effective competency profile-section identity | ora_reference_lookups.md |

## Source Material

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/considerations-for-creating-performance-template-sections.html | Supported section types, content behavior, and ratings |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/how-can-i-create-multiple-competency-type-sections.html | Multiple competency-section constraints |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/Chunk1140664948.html | Supplied Oracle documentation reference for the functional area |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/Chunk1276566370.html | Supplied Oracle documentation reference for the functional area |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/how-managers-can-justify-difference-in-manual-and-calculated-ratings.html | Manager-justification visibility and enforcement limitations |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/create-a-performance-template-section-for-profile-content.html | Profile Content section example |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/create-a-performance-template-section-for-performance-goals.html | Performance Goals section example |
