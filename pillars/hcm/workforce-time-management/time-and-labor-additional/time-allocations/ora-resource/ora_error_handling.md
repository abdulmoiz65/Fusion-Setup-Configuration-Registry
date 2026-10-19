# Time Allocations Error Handling

## Source Basis

- User-authorized Time Consumer Sets timeCategoriesLOV pattern with verified TcatCd mapping for Time Allocations, 5 October 2026.

- User-provided Generic FSM Baseline, received 5 October 2026.
- User-requested correction separating fresh-export discovery from import readiness, 5 October 2026.
- Developer-provided Time Allocation UI Skeleton.
- User-provided verified Time Attribute data-source and value validation contract, received 5 October 2026.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Time Category lookup returns zero or multiple search matches, blank or ambiguous selected TcatCd, unavailable results, or incomplete pages | Mark the source-row category unresolved, show the supplied search term and result or specific failure, and stop before preview. Follow resolve_time_category for the no-result creation prompt or multiple-result selection. An unavailable or incomplete lookup is not evidence that the category does not exist. |
| An Edit requests a change to Allocation Name or Effective End Date | Explain that these fields cannot be updated after creation, identify the requested immutable field, and stop before preview. Ask the user to remove that change; do not silently drop it or convert the edit to a new allocation. |
| A required field or table value is absent | Identify the affected business field and stop before preview. |
| A conditional or numeric rule is violated | Explain the rule and request a corrected value. |
| A Time Attribute field or data source is not found, cannot be uniquely identified, or returns a blank or unsupported ImplementationType | Show the selected Time Attribute identity and the missing or unsupported result, then stop before preview. |
| A FORMAT_VALUE_SET value does not match AttributeType or violates a returned Precision, Scale, minimum, or maximum constraint | Show the expected AttributeType and every violated non-null constraint, then ask for a corrected value and suggest its required form from the returned metadata. |
| A ValuesList search returns no rows | Show the search term and ask the user for another value. |
| A ValuesList search returns multiple rows | Show Code, Value, ValueChar, ValueDate, and ValueNumber for every returned match and prompt the user to select one Code; do not select automatically or merge duplicate Value labels. |
| A ValuesList page fails or pagination cannot be completed | Preserve sanitized lookup diagnostics and stop; do not accept a partial result set or retry automatically. |
| After fresh-export inspection, required task-specific evidence remains unresolved | Stop before package preparation or import as applicable and identify the specific unresolved mapping, operation rule, key, relationship, or reconciliation selector. Absence of a not-yet-obtained export is not a business-input failure. |
| A fresh same-task export cannot be obtained or validated | Stop before package preparation or submission; preserve sanitized diagnostics. |
| FSM evidence does not prove the expected import route | Stop and rebuild through the declared fresh-export workflow. |
| Approval is missing or stale | Stop before submission; obtain explicit approval for the current immutable core.data-loader preview. |
| A later import or mutation fails, partially succeeds, times out, or is uncertain | Preserve sanitized diagnostics, reconcile current state through the task’s documented read/export path, and stop without automatic retry. If reconciliation cannot complete, retain the uncertain status and report that blocker. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required, conditional, enum, or numeric check fails | Correct the identified value and restart validation. |
| Design blocker | A UI branching or read-only rule is violated | Correct the configuration before preview. |
| Time Attribute lookup blocker | A field, data source, ImplementationType, or complete paginated ValuesList result cannot be resolved | Correct the Time Attribute or search input, then restart the lookup from its first page. |
| Time Attribute value selection | Multiple ValuesList rows match the search term | Review the displayed fields and select one Code. |
| Time Attribute format validation | A FORMAT_VALUE_SET value does not satisfy the returned type or non-null constraints | Enter a corrected value in the displayed AttributeType-compatible form. |
| Execution contract blocker | The current stage lacks required evidence after its declared discovery step | Resolve the specific gap and resume that stage; do not require package evidence before the fresh-export step. |
| Process uncertainty | A later operation has an unknown result | Reconcile current state and stop before any retry. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation or design failure | Affected business field, safe failure category, and one corrective action. |
| Multiple Time Attribute value matches | Search term and each returned Code, Value, ValueChar, ValueDate, and ValueNumber. |
| FORMAT_VALUE_SET validation failure | Supplied value, expected AttributeType, and each violated non-null Precision, Scale, minimum, or maximum constraint. |
| Contract blocker | The missing contract element and one safe next action. |
| Uncertain later operation | Operation, sanitized status or error, and required reconciliation step. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Time Category resolution is incomplete | Do not invent TcatCd, substitute TcatId, automatically select among multiple matches, collapse duplicate names, or treat a partial page as complete. |
| Time Attribute field or data-source resolution is incomplete | Do not infer TimeAttrributeFieldId, ImplementationType, AttributeType, or validation limits. |
| ValuesList returns multiple rows | Do not auto-select a row, discard duplicate display values, or use a partial first page as the complete result. |
| FORMAT_VALUE_SET validation fails | Do not accept the value or invent a replacement value outside the returned data-source constraints. |
| Package or reconciliation evidence is unresolved after export inspection | Do not invent a payload or claim import readiness; do not make a direct REST mutation. |
| A later import or mutation fails, partially succeeds, times out, or is uncertain | Do not retry automatically. |

## FSM Contract Gate

TAL.CHECK_EXECUTION_CONTRACT is the pre-export handoff gate. It checks that
business validation has passed, the operation is Create or Edit, and the
catalog routes this task through FSM CSV import. Return contract_ready for
that handoff; return contract_missing if the current-stage route or required
business evidence is absent. Do not require future export, package, preview,
or approval evidence at this gate.

TAL.RETURN_FSM_HANDOFF returns to the invoking workflow for the fresh same-task
export. It does not report package readiness or import success. After export,
the invoking workflow must apply the package-stage design rules before
core.data-loader handoff. Preview and submission approval remain owned by
core.data-loader; approval of this authoring change is not import approval.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TAL.CHECK_EXECUTION_CONTRACT | decision | 40 | execution_gate | contract_missing->TAL.RETURN_CONTRACT_BLOCKER;contract_ready->TAL.RETURN_FSM_HANDOFF | TAL.ENFORCE_DESIGN | stop | A business-validated Create or Edit request is ready for the catalog-routed FSM fresh-export workflow |
| TAL.HANDLE_INPUT_ISSUE | step | 80 | error_handler | handled->TAL.RETURN_ISSUES | none | stop | Required or field validation fails |
| TAL.HANDLE_DESIGN_ISSUE | step | 81 | error_handler | handled->TAL.RETURN_ISSUES | none | stop | A design rule blocks preview |
| TAL.RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | A blocking input or design issue has been disclosed |
| TAL.RETURN_CONTRACT_BLOCKER | terminal | 91 | terminal | none | TAL.CHECK_EXECUTION_CONTRACT | stop | The pre-export gate lacks required current-stage route or business evidence |
| TAL.RETURN_FSM_HANDOFF | terminal | 92 | terminal | none | TAL.CHECK_EXECUTION_CONTRACT | stop | Pre-export gates passed; return to the invoking workflow for fresh same-task export and subsequent package validation, not package readiness or import success |
