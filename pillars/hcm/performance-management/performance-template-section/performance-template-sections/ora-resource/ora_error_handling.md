# Performance Template Sections Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| SectionRatingModelCode has no value but a calculation-related field is populated | Stop before approval or import; set CalculationRuleCode, CalcMappingCode, DecimalPlaces, FastFormulaId, RoundingRuleCode, and MappingMethodCode to null. |
| A request, approval, or import artifact asks to bypass a dependent-field rule | Apply the documented reset if one exists, then re-evaluate all applicable invariants. Stop before preview, approval, import, or mutation if the payload remains contradictory; do not waive the rule. |
| CalculationRuleCode is Fast Formula but FastFormulaId has no value | Stop before approval or import; select a Performance Rating Calculation formula and populate FastFormulaId. |
| RateSectionFlag is Y but SectionRatingModelCode has no value | Stop before approval or import; set RateSectionFlag to N or select a compatible section rating model. |
| RateSectionFlag is N but weight or manager-reason fields retain rated-section values | Stop before approval or import; set WeightSectionFlag and EnableMgrReasonFlag to N and both section weights to null/blank. |
| WeightSectionFlag is N but SectionWeight or SectionMinWeight has a value | Stop before approval or import; clear both weight fields to null/blank. Fusion rejects 0 for either field when Weight Section is No. |
| SectionWeight is less than SectionMinWeight | Stop before approval or import; correct the weights so SectionWeight is greater than or equal to SectionMinWeight. |
| Goal or Development Goal synchronization is requested but `ORA_HRA_SYNCHRONIZED_GOALS` is not confirmed Y | Stop before approval or import; confirm the profile option or remove the synchronized-goal defaults. |
| A competency section has no ReferenceSectionName, an unresolved reference, or a mismatched ReferenceSectionId | Stop before approval or import; resolve the exact competency reference section and populate ReferenceSectionId with its returned SectionId. |
| CalculationRuleCode is A, S, or B but EnableItemsFlag or RateItemFlag is not Y | Stop before approval or import; set both fields to Y. |
| RateItemFlag is Y with RatingTypeCode PER or PAP but PerfRatingModelCode has no value | Stop before approval or import; select a compatible performance rating model or set it from SectionRatingModelCode when section-rating reuse is enabled. |
| A new record inherited a business or configuration value from an exported comparator | Stop before approval or import; retain only comparator structure, required transport/relationship fields, formatting, and required translations. Clear each unrequested and non-defaulted field to null, N for flags, or 0 for numeric amounts and counts; use null for SectionWeight and SectionMinWeight when WeightSectionFlag is N. |
| SectionTypeCode is WFF or MFF and a restricted field is populated | Stop before approval or import; retain only Name, Description, Comments, DateFrom, DateTo, StatusCode, and SectionTypeCode as business values, clear other configuration fields, and set Boolean fields to N. |
| SectionTypeCode is QUESTIONNAIRE and a restricted field is populated | Stop before approval or import; retain only Name, Description, Comments, DateFrom, DateTo, StatusCode, SectionTypeCode, IncludeQstnrScoreOsFlag, IncludeQstnrScoringFlag, WeightSectionFlag, SectionWeight, and SectionMinWeight as business values, clear other configuration fields, and set non-excepted Boolean fields to N. |
| An FSM CSV member uses blanket quoting | Stop before approval or import; remove quotes from headers and values that do not require CSV escaping, preserve quotes only for values containing a comma, double quote, carriage return, or line feed, then rebuild and revalidate the ZIP. |
| Unsupported competency text-field section is proposed | Do not configure it for a performance document; select a supported competency configuration |
| Calculated-rating prerequisites are incomplete | Do not represent the calculated rating as ready; complete the rating model, rule, and template activation settings |
| Multiple competency prerequisite is missing | Stop the multiple-section design until Enhanced Talent Profile Management and the required Competencies Templates are available |
| Writing Assistant data is absent | Do not claim that suggestions are available; upload and save the competency feedback suggestions and development tips |
| HDL update is expected to enforce comment limits or manual-versus-calculated justification | Explain that the supplied documentation does not enforce those controls for HDL updates |
| REST describe metadata is unavailable or does not support a submitted field | Stop before the mutation path; do not guess field updateability or post the field |
| REST target lookup returns no match or an in-use section for an update or delete | Stop before the mutation path and report the resolved target state |
| REST request fails entity, authorization, or payload validation | Preserve the returned validation category and correct the request; do not automatically retry a POST, PATCH, or DELETE |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Missing prerequisite | A required setup, model, formula, template, or uploaded content is unavailable | Complete the dependency and repeat the design review |
| Invalid configuration | The section type or selected processing behavior conflicts with documented support | Correct the section design |
| Enforcement limitation | The requested control is expected to be enforced through HDL | Use the documented interactive evaluation path or revise the expectation |
| Input validation | REST metadata, field, domain, or cross-field validation rejects the request | Correct the payload and restart the selected workflow from validation |
| Auth/authz | Caller lacks permission or the target is locked by authorization or in-use state | Stop and obtain the authorized path; do not retry the mutation automatically |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Design review result | The missing or invalid setting, its affected section type, and the documented corrective action |
| HDL limitation | That the documented comment-limit and manager-justification enforcement does not apply to HDL updates |
| Direct REST refusal | The rejected field or action, the resolved target state when available, and the safe corrective action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Direct REST execution is requested from this resource set | Do not treat these validation resources as a write contract or execute POST, PATCH, or DELETE; a selected task execution workflow, preview, and current explicit approval are required |
| A validated export/template exists for this CSV-enabled task | Use its unchanged layout and required parent/translation rows through `core.data-loader`; do not invent fields or relationship rows. |
| A prerequisite is missing | Do not treat the section design as complete or ready for calculated ratings or Writing Assistant |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| HRA_SECTIONS.READINESS_GATE | decision | 70 | execution_gate | ready->HRA_SECTIONS.DONE;not_ready->HRA_SECTIONS.HANDLE_ISSUES | HRA_SECTIONS.ENFORCE_DESIGN | continue | Design enforcement passed |
| HRA_SECTIONS.HANDLE_ISSUES | step | 80 | error_handler | reported->RETURN_ISSUES | none | stop | Any validation, dependency, invariant, design, readiness, or REST safeguard issue is found |
| HRA_SECTIONS.DONE | terminal | 90 | terminal | none | HRA_SECTIONS.READINESS_GATE | stop | The documentation-backed design review is complete |
| RETURN_ISSUES | terminal | 100 | terminal | none | none | stop | Issues have been disclosed for correction |

## Source Material

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/how-managers-can-justify-difference-in-manual-and-calculated-ratings.html | Justification enforcement limit for HDL updates |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/how-you-set-the-minimum-and-maximum-character-limits-for-evaluation-comments.html | Comment-limit enforcement limit for HDL updates |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/how-you-upload-writing-assistant-data-using-spreadsheets.html | Writing Assistant upload and save behavior |
| https://docs.oracle.com/en/cloud/saas/talent-management/faipm/how-you-set-up-writing-assistant-for-performance-documents.html | Writing Assistant prerequisites |
