# Time Rule Templates Design Enforcement

Source: User-provided requirement to reuse an existing functionally compatible Time Rule Template, treat creates and updates as FSM setup-data CSV imports through core.data-loader, and display and explicitly approve an immutable Data Loader preview before import.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Current-environment search | Search the refreshed target Fusion environment export before proposing or creating a template |
| 2 | Functional comparison | Compare the parent, inputs, usages, formula, and behavior; never match by TemplateName alone |
| 3 | Exact-match decision | Display every fully compatible verified template and ask whether the user wants to reuse one or create a new template |
| 4 | Create or proposal disclosure | For a confirmed create, display the normalized requested configuration. If no match exists, display the complete template proposal and its dependent Time Rule relationship |
| 5 | FSM CSV route | Prepare the minimal Time Rule Templates CSV ZIP and validate it through core.data-loader; do not require or invent a direct REST create or update endpoint |
| 6 | Complete Summary | Generate the business-only Complete Summary and Defaults Applied details from verified values and defaults actually applied |
| 7 | Validated package link | Display a clickable link to the exact validated FSM ZIP outside the business summary |
| 8 | Approval boundary | Obtain explicit approval bound to the exact displayed proposal, target environment, linked archive SHA-256, and core.data-loader preview before import handoff |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any new Time Rule Template is proposed or created | Error | find_compatible_time_rule_template | The current target-environment export has not been searched | Refresh the setup-task export and evaluate compatibility | Yes, by completing the lookup |
| A candidate name matches but functional configuration differs | Error | find_compatible_time_rule_template | Any applicable formula, condition, input, output, summation, reporting, Time Category, result or payroll time-type, parameter, or effective-context characteristic is missing, conflicting, or unverified | Disclose every difference and obtain user direction; do not silently reuse it | No automatic fix |
| One or more fully compatible verified templates exist | Error | find_compatible_time_rule_template | Every match and the choice to reuse or create have not been displayed | Display every template and its functional match, then ask whether the user still wants a new template | Yes |
| The user confirms a create from exact matches | Error | find_compatible_time_rule_template | The normalized requested configuration is incomplete | Build every supported row from normalized intent against the fresh schema; do not select or copy a source record | Yes |
| No fully compatible verified template exists | Error | find_compatible_time_rule_template | The proposal is incomplete, its dependent Time Rule relationship is unclear, or exact approval is absent | Complete and display the proposal, then request explicit approval | Yes |
| A Time Rule Template create or update is prepared | Error |  | The execution route bypasses core.data-loader, the FSM CSV ZIP is not immutable and validated, or the Data Loader preview does not identify TaskCode ORA_HWM_MANAGE_RULE_TEMPLATES | Route the exact CSV package through core.data-loader validation and preview before approval | Yes |
| No direct REST create or update endpoint is documented | Error |  | The workflow treats the missing REST endpoint as a blocker even though FSM CSV import is supported | Continue through the supported core.data-loader FSM CSV route; do not invent a direct REST write | Yes |
| The proposal or target environment changes after approval | Error |  | The approval fingerprint differs from the intended import | Invalidate approval, redisplay the revised proposal, and ask again | Yes |
| A Time Rule Templates archive is ready for approval | Error |  | A clickable link does not identify the exact validated FSM ZIP | Show the link outside the business proposal before asking for approval | Yes, by rebuilding, validating, and linking the exact ZIP |
| A validated Time Rule Templates archive is ready for approval | Error |  | The business-only Complete Summary and Defaults Applied details are absent, incomplete, or expose technical package data | Generate the summary from verified business values and defaults actually applied before linking the package or requesting approval | Yes, by regenerating the summary from the validated configuration |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_compatible_time_rule_template | Before any proposal or creation | Match category, TemplateName, matched characteristics, differences, and verification status | ora_reference_lookups.md |
| query_common_application_lookups | Before proposing a lookup-dependent Time Rule Template configuration | Current lookup state, product-recommended comparison evidence, and provider gap | ora_reference_lookups.md |
| query_common_application_value_sets | Before proposing a value-set-dependent Time Rule Template configuration | Current value-set state, product-recommended comparison evidence, and provider gap | ora_reference_lookups.md |

## Common Applications Provider Best Practices

| Provider Dependency | Business Scenario | When to Use It | Recommended Configuration | Rationale | Prerequisites | Invocation Order | Validation | Exceptions | Source |
|---|---|---|---|---|---|---|---|---|---|
| Application Lookup Foundation Skill | A Time Rule Template depends on lookup-controlled behavior | Before proposing a create or update that uses a lookup | Route through `hcm.workforce-time-management.time-and-labor-common.manage-common-lookups` with each exact applicable `lookupType` from authorized evidence | Common Applications owns lookup resolution and CRUD; this skill must not duplicate it | Complete normalized request and exact runtime lookup type; scope labels are not identifiers | 1 | Show provider current state beside the product-recommended state and retain provider evidence | If an applicable lookup type is missing, unsupported, or ambiguous, return an unresolved provider gap and do not propose the dependent change | User-provided implementation contract |
| Application Value Set Foundation Skill | A Time Rule Template depends on value-set-controlled behavior | Before proposing a create or update that uses a value set | Route through `hcm.workforce-time-management.time-and-labor-common.manage-value-sets` with each exact applicable `ValueSetCode` from authorized evidence | Common Applications owns value-set resolution and CRUD; this skill must not duplicate it | Complete normalized request and exact runtime value-set code; scope labels are not identifiers | 2 | Show provider current state beside the product-recommended state and retain provider evidence | If an applicable value-set code is missing, unsupported, or ambiguous, return an unresolved provider gap and do not propose the dependent change | User-provided implementation contract |

## Provider Enforcement Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A Time Rule Template proposal depends on a Common Applications lookup or value set | Error | applicable provider resolver | The applicable provider was not invoked, its current state was not compared with the product-recommended state, or evidence is absent | Invoke each applicable read-only pillar route and show the comparison before proposing the dependent configuration | Yes, by completing the read-only provider checks |
| A provider route needs an exact identifier | Error | applicable provider resolver | An applicable `lookupType` or `ValueSetCode` is missing, unsupported, or ambiguous | Resolve the exact identifier from authorized product or current-environment evidence; otherwise return the provider gap without inventing one | No automatic fix |
| A requested implementation outcome requires a dependent configuration change | Error | query_common_application_lookups; query_common_application_value_sets | The outcome is not required or the exact proposed change has not been explicitly confirmed by the user | Preserve provider ownership and request confirmation before handing the change to the owning execution workflow | No automatic fix |

## Proposal Disclosure Contract

| Proposed Object | What Must Be Shown |
|---|---|
| Time Rule Template | TemplateName, Description, Classification or Rule Type, TemplateType, ProcessType, FormulaName and FormulaId, RuleExecType, RunSummationLevel, RunTbbLevel, effective dates, ordered inputs and parameter requirements, ordered outputs and usages, Time Category handling, and result or payroll time-type behavior |
| Dependent Time Rule | RuleName, RuleType, condition and calculation behavior, Time Category, inputs, outputs, execution behavior, summation and reporting levels, effective context, and how it references the proposed template |
| Approval | Target Fusion environment, intended create or update operation, proposal fingerprint, immutable CSV archive path and SHA-256, core.data-loader validation result and preview, and an explicit statement that neither the template nor the rule will be imported before approval |

## Complete Summary Contract

After package validation and before the package link or approval, always show
exactly these business-only sections:

## Complete Summary

| Business Setting | Selected Value |
|---|---|

## Defaults Applied

| Business Setting | Default Applied |
|---|---|

The `Complete Summary` includes every verified user-provided business value.
The `Defaults Applied` section includes every default actually applied while
normalizing the request or building the validated package. Use business labels
and friendly values such as `Selected`, `Not selected`, `Enabled`, `Disabled`,
`Yes`, `No`, `Draft`, or `Submitted`, as applicable. Show populated child
sections only when they have values. Omit blank, null, unused, and
metadata-only values. Do not add warnings, diagnostics, technical notes, CSV
column names, identifiers, archive paths, hashes, or package details.

## Package-Link Approval Gate

After the Complete Summary and before approval, show a clickable link to the
exact immutable FSM ZIP outside the business summary. The linked file must be
the one passed to Data Loader. If any field, relationship, or ZIP member
changes, rebuild, validate, regenerate the summary, and link a new ZIP before
seeking approval.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TIMETMPLT.PROPOSAL_GATE | decision | 3 | design_enforcement | proposal_complete->TIMETMPLT.CREATE_DEPENDENCY;proposal_incomplete->TIMETMPLT.PROPOSAL_ERROR | TIMETMPLT.FIND_MATCH | stop | A user-confirmed exact-match create, no fully compatible template, or an existing template update is requested |
| TIMETMPLT.COMPLETE_SUMMARY | step | 5 | design_enforcement | summary_ready->TIMETMPLT.PRESENT_VALIDATED_PACKAGE;summary_incomplete->TIMETMPLT.DEPENDENCY_ERROR | TIMETMPLT.CREATE_DEPENDENCY | stop | The validated configuration must be shown in a business-only Complete Summary and Defaults Applied section before package linking or approval |
| TIMETMPLT.PRESENT_VALIDATED_PACKAGE | step | 6 | design_enforcement | package_linked->TIMETMPLT.APPROVAL_GATE;package_missing->TIMETMPLT.DEPENDENCY_ERROR | TIMETMPLT.COMPLETE_SUMMARY | stop | The exact validated FSM ZIP must be linked outside the business summary before approval |
