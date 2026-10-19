# Elements Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | LDG and legislation | Resolve one exact LDG in the target environment before selecting a questionnaire. |
| 2 | Template selectors and questions | Match resolved legislation, primary, optional secondary and category to one local questionnaire; present its questions. |
| 3 | User answers | Collect and confirm every applicable response; retain exact question codes and labels. |
| 4 | Routed HDL handoff | Use core.data-loader with active project Run Book and its own artifact, preview and approval gates. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| element_ldg | Unique target LDG and legislation | Yes | Before questionnaire selection | Lookup | Target Fusion LDG LOV | find_ldg_by_exact_name | Legislation must come from the selected LDG. | Provide exact LDG name; resolve ambiguity before proceeding. | LegislativeDataGroupName;LegislativeDataGroupId;legislationCode |
| element_questionnaire | Matching element-template questions | Yes | Before asking for answers | Lookup | Packaged local example catalog | find_element_questionnaire | RuleCode and Rule must come from the selected combination. | Supply another current catalog entry when no match exists. | Ordered RuleCode;Rule |
| loader_handoff | Active project route and live Data Loader preflight | Yes | Before any HDL submission | Required | Routed project workflow and core.data-loader live metadata validation | | Data Loader validates the compact DAT header and immutable import artifact before upload. | Stop if live metadata, task validation or the loader approval gate fails. | Validated immutable import artifact;runbook state |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Lookup ready | Required LDG and selectors are present. | Run the routed read-only LDG lookup. |
| Questionnaire ready | One local catalog combination matches. | Display questions and collect confirmation; no HDL submission yet. |
| Blocked | Missing or ambiguous LDG, no questionnaire match, or unconfirmed answers. | Stop the dependent step and report the exact gap. |
| HDL handoff ready | Confirmed answers and active Run Book are available. | Hand off to core.data-loader for live metadata preflight, exact-artifact approval and submission. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ELE.CHECK_DEPENDENCIES | decision | 3 | resolve_dependency | ready->ELE.RESOLVE_LDG;blocked->ELE.HANDLE_ERROR | ELE.APPLY_DEFAULTS | stop | Confirm LDG input and active project route permit the declared lookup; defer live DAT schema validation to core.data-loader. |
