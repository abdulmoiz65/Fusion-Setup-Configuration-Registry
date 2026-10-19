# Time Rules Design Enforcement

Source: User-provided requirement to search for and reuse a functionally compatible Time Rule Template before proposing or creating a Time Rule, and to require explicit approval when a new template is needed.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Existing Time Rule check | Reuse a verified exact Time Rule when one exists |
| 2 | Derivable proposal | When exactly one close same-family Time Rule is found, use it internally to propose complete business values. Default the proposal to **Create new**; invite the user to change any value or explicitly request an update. Do not expose the source rule unless the user asks for provenance or a material value is ambiguous. |
| 3 | Prerequisite template search | For every non-exact create or update proposal, verify the supporting Time Rule Template from a current target-environment baseline before package preparation. Reuse a current verified template baseline when it already supports the selected source rule; otherwise export and evaluate the templates. |
| 4 | Compatibility decision | Compare functional configuration rather than TemplateName; reuse only one fully compatible verified template |
| 5 | Candidate recommendation | When fully compatible, multiple, or partial template candidates exist, display the source-backed candidates, functional match, and material differences before requesting a selection |
| 6 | Joint proposal | When no fully compatible template exists, display the complete proposed Time Rule Template and Time Rule together |
| 7 | Complete Summary | Generate the business-only Complete Summary from verified structured values after validation, lookup resolution, and defaulting, before the provider-owned approval process |
| 8 | Approval boundary | Obtain explicit approval bound to the displayed proposal before handing off either object for import |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A new Time Rule is being proposed or created | Error | find_compatible_time_rule_template | The current target-environment template export has not been searched | Refresh the Time Rule Templates setup-task export and evaluate compatibility | Yes, by completing the lookup |
| Exactly one derivable same-family Time Rule candidate exists | Error | find_behaviorally_equivalent_time_rule | A complete business-value proposal has not been shown, or an update is implied without an explicit user request | Use the candidate internally to propose values and defaults, state that the default operation is Create new, and invite value changes. Reveal source-rule provenance only on request or to resolve a material ambiguity. Never modify an existing rule unless the user explicitly requests Update existing. | Yes, by presenting the proposal or receiving an explicit update request |
| A template candidate has the requested name but its functional configuration differs | Error | find_compatible_time_rule_template | Any applicable formula, condition, input, output, summation, reporting, Time Category, result or payroll time-type, parameter, or effective-context characteristic is missing, conflicting, or unverified | Disclose the differences and obtain user direction; do not silently reuse the candidate | No automatic fix |
| Exactly one fully compatible verified template exists | Error | find_compatible_time_rule_template | The selected template and match explanation have not been displayed | Display TemplateName and the matched functional characteristics before using it in the Time Rule proposal | Yes |
| Multiple fully compatible or partial-only template candidates exist | Error | find_compatible_time_rule_template | The candidate recommendation, functional match evidence, and material differences have not been displayed before requesting a selection | Display every candidate with its match category, supported characteristics, differences, and confirmation needed; then request user direction | Yes, by completing the candidate disclosure |
| No fully compatible verified template exists | Error | find_compatible_time_rule_template | Either proposed object is incomplete, the relationship is unclear, or approval has not been explicitly given for the exact displayed proposal | Display all required template and rule details, explain their relationship, and request explicit approval | Yes, by revising and redisplaying the proposal |
| The proposal or target environment changes after approval | Error |  | The approval fingerprint no longer matches the intended imports | Invalidate approval, display the revised proposal, and ask again | Yes |
| A validated Time Rule Template proposal or validated Time Rule archive is ready for approval | Error |  | A business-only Complete Summary has not been generated from verified structured values, resolved display values, and defaults actually applied | Generate the Complete Summary and Defaults Applied sections before transitioning to the provider-owned approval process | Yes, by regenerating the summary from the verified result set |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_behaviorally_equivalent_time_rule | Exactly one derivable same-family candidate exists | Internal candidate identity and structural match; user-facing proposed values, defaults, and operation | ora_reference_lookups.md |
| find_compatible_time_rule_template | A non-exact create or update proposal needs template verification | Match category, TemplateName, matched characteristics, differences, and verification status | ora_reference_lookups.md |

## Proposal Disclosure Contract

| Proposed Object | What Must Be Shown |
|---|---|
| Time Rule Template | TemplateName, Description, Classification or Rule Type, TemplateType, ProcessType, FormulaName and FormulaId, RuleExecType, RunSummationLevel, RunTbbLevel, effective dates, inputs and parameter requirements, outputs and usages, Time Category handling, and result or payroll time-type behavior |
| Time Rule | RuleName, RuleType, selected or proposed TemplateName, condition and threshold, calculation behavior, Time Category, inputs, outputs, execution behavior, summation and reporting levels, effective context, and intended operation |
| Proposed values from a close configuration | Proposed business values and applied defaults, with **Create new** as the default operation. Invite the user to change values or explicitly request an update. Show source-rule provenance only on request or when needed to resolve a material ambiguity. |
| Relationship and approval | Explain how the Time Rule uses the template; show the target Fusion environment and proposal fingerprint; state that neither object will be created or imported until explicit approval is received |

## Complete Summary Contract

Generate the Complete Summary only after validation, lookup resolution, and defaulting have produced verified structured values. Always generate it before the provider-owned approval process. Include every user-provided business value and every default actually applied. Omit blank, null, unused, and metadata-only values. Show populated child records only when they have values and use business labels only. Keep implementation-only values internally for validation and provider execution. Do not add warnings, diagnostics, or technical notes.

Use this exact user-facing structure:

## Complete Summary

| Business Setting | Selected Value |
|---|---|
| <business label> | <verified business display value> |

## Defaults Applied

| Business Setting | Default Applied |
|---|---|
| <business label> | <verified default display value> |

## Display Value Rules

| Value Kind | Display Value |
|---|---|
| Resolved selection | Verified business display name |
| Verified business meaning | Business-friendly meaning |
| Selected setting | Selected, Not selected, Enabled, Disabled, Yes, or No as applicable |
| Lifecycle state | Business-friendly state such as Draft or Submitted |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TIMERULE.CHECK_TEMPLATE_REUSE | decision | 4 | design_enforcement | compliant->TIMERULE.CREATE_DEPENDENCY;noncompliant->TIMERULE.TEMPLATE_SELECTION_REQUIRED | TIMERULE.FIND_TEMPLATE | stop | Exactly one fully compatible template candidate was found |
| TIMERULE.PRESENT_DERIVABLE_RULE | step | 2 | design_enforcement | proposed_create_new->TIMERULE.FIND_TEMPLATE;update_existing_requested->TIMERULE.FIND_TEMPLATE | TIMERULE.FIND_MATCH | stop | Exactly one derivable same-family Time Rule candidate was found |
| TIMERULE.PREPARE_TEMPLATE_PROPOSAL | decision | 5 | design_enforcement | proposal_complete->TIMERULE.TEMPLATE_COMPLETE_SUMMARY;proposal_incomplete->TIMERULE.TEMPLATE_PROPOSAL_ERROR | TIMERULE.FIND_TEMPLATE | stop | No fully compatible template was found |
| TIMERULE.TEMPLATE_COMPLETE_SUMMARY | step | 6 | design_enforcement | summary_ready->TIMERULE.TEMPLATE_APPROVAL_GATE;summary_incomplete->TIMERULE.TEMPLATE_PROPOSAL_ERROR | TIMERULE.PREPARE_TEMPLATE_PROPOSAL | stop | A complete joint Time Rule Template and Time Rule proposal is ready for the provider-owned approval process |
| TIMERULE.RULE_COMPLETE_SUMMARY | step | 9 | design_enforcement | summary_ready->TIMERULE.CREATION_HANDOFF_READY;summary_incomplete->TIMERULE.DEPENDENCY_ERROR | TIMERULE.CREATE_DEPENDENCY | stop | A verified template and validated immutable Time Rule archive are ready for the provider-owned approval process |
| TIMERULE.PRESENT_TEMPLATE_CANDIDATES | decision | 10 | design_enforcement | candidates_disclosed->TIMERULE.TEMPLATE_SELECTION_REQUIRED;evidence_incomplete->TIMERULE.TEMPLATE_CANDIDATE_DISCLOSURE_REQUIRED | TIMERULE.FIND_TEMPLATE | stop | Multiple fully compatible or partial-only template candidates were found |
