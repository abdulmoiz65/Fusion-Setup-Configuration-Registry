# Elements Input Validation

## Scope

Validate the input contract for a Payroll Element Details HDL create. Source: developer-provided `Elements-HDL.md`, its example DAT header, and its nine-question catalog. Input validation does not choose a template, resolve a reference, or submit HDL.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Element identity | ElementName; ReportingName; optional Description | Ask for a missing name. | Use the compact supplied HDL header; core.data-loader validates it against live target metadata before upload. | Create | |
| Legislative context | LegislativeDataGroupName | Stop before questionnaire selection. | Ask for the exact target LDG name. | Create | find_ldg_by_exact_name |
| Template selectors | PrimaryClassificationName; Category; optional SecondaryClassificationName | Ask for primary or category; keep omitted secondary blank. | User supplies selectors valid for the target LDG. | Create | find_element_questionnaire |
| Effective start | ElementStartDate | Ask for the effective start date. | Normalize the user date to the target HDL format after checking metadata. | Create | |
| Questionnaire answers | One confirmed Response for every question in the selected template | Display each selected question and ask for missing answers or explicit confirmation. | Preserve exact RuleCode and Rule from the selected questionnaire; do not treat stored example Response as confirmed. | After questionnaire match | find_element_questionnaire |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Before resolving LDG | LDG name, primary classification, category, element name and effective date are present. | Continue to dependency check, or return exact missing fields. | |
| After questionnaire match | Nine answers are required for the one supplied US Information / blank secondary / Standard example. Other combinations have no supplied questions. | Display all matched questions in stored order, collect answers and confirm them. | find_element_questionnaire |
| Before HDL submission | Core.data-loader validates the final DAT against live business-object metadata and the selected task rules. | Stop on a live schema or task-validation failure; do not require a separate user-supplied metadata export. | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| SecondaryClassificationName omitted | Represent as an explicit empty value; never substitute another classification. | Create | |
| ElementStartDate | Require a real effective date. The supplied DAT demonstrates YYYY/MM/DD; accepted target format and date-effective restrictions require target metadata. | Create | |
| ElementName | US-specific guidance in the source states a 50-character maximum and warns against a secondary-classification name in some cases. Validate country applicability before enforcing this rule elsewhere. | US create | |
| Questionnaire cardinality | Require exactly one confirmed answer per applicable question and reject extra rules from another template. | After questionnaire match | find_element_questionnaire |
| Questionnaire answer values | Preserve the user-confirmed values exactly. The local catalog gives examples but no complete allowed-value list; do not claim that this preflight proves Fusion will accept them. | Before HDL preparation | |
| Source keys, GUID and optional full-header IDs | Use the compact supplied HDL header for this create; omit optional full-header identifiers unless live Data Loader metadata requires a different supported form. | Create | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ELE.VALIDATE_INPUT | decision | 1 | validate_input | valid->ELE.APPLY_DEFAULTS;missing->ELE.HANDLE_ERROR;invalid->ELE.HANDLE_ERROR | none | stop | Validate create request identity, LDG, primary classification, category and effective date. |
| ELE.VALIDATE_RESPONSES | decision | 6 | validate_input | confirmed->ELE.CHECK_DESIGN;missing->ELE.HANDLE_ERROR;invalid->ELE.HANDLE_ERROR | ELE.FIND_QUESTIONNAIRE | stop | Show all selected questions and require one confirmed response for each; preserve those values for the loader. |
