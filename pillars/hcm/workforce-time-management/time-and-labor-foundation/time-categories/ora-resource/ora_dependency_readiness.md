# Time Categories Dependency Readiness

## Source Basis

- Developer-provided Time Categories UI structure and screenshot, 2026-09-08.
- Developer-provided FSM baseline and task-operation guidance, 2026-09-08.
- Developer-provided Time Categories FSM authoring input, 2026-09-08.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Existing category identity | For edit, use the user-provided Current Name to match exactly one row in the fresh Time Categories export. |
| 2 | Existing-category search and selection | For a plain-language requirement, derive the business terms, search existing categories, and require the user's choice when more than one plausible category exists. |
| 3 | Condition expression | Validate populated-row operators, ordering, and balanced grouping. |
| 4 | Time Attribute and data-source resolution | Resolve the selected Time Attribute through the complete paginated search, retrieve its data source, and map the selected Name to both expression-result fields. |
| 5 | Specific Value resolution | Only when Value Type is Specific Value, validate FORMAT_VALUE_SET input or resolve an eligible ValuesList selection, then map it to every required display and selection field in the fresh export. |
| 6 | Export-shaped FSM package | Obtain and validate a fresh same-task export; retain its metadata, headers, keys, and unrelated rows while applying only approved changes. |

## Resolved Configuration Contract

Before rows are generated, create `TC.RESOLVED_CONFIGURATION`. It contains the
operation, category business fields, ordered condition clauses, user-supplied
values, applied defaults, and the export-derived task schema. Resolve every
business field by this precedence: explicit user requirement; request-derived
value; verified compatible-category evidence; documented default; focused user
decision. Compatible categories are evidence for unresolved business values,
not CSV row templates and not update targets.

The serializer owns technical linkage. It derives parent references, grouping
keys, display sequences, expression-group markers, and protocol constants from
the Time Categories task contract and the current export headers. In
particular, expression-row markers are a row-type contract, not values copied
from a matching category. If the export schema cannot support a required
contract field or its invariant is ambiguous, block package preparation.

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| existing_time_category | Existing category identity | Yes | Edit | Verify | User-provided Current Name and fresh Time Categories FSM export archive | verify_time_categories_fsm_package | An edit must target one existing category without assuming that the editable Name is its runtime identity | Provide the existing Time Category Name | Matching exported row and current values |
| existing_category_search | Existing-category search and selection | Yes | Plain-language requirement needs a Time Category | Lookup | Derived business terms and fresh Time Categories export | search_existing_time_categories | Prevent duplicate creation and require a user choice when multiple categories are plausible | Provide a selection or confirm that no suitable category exists | Search evidence and selected reuse or create decision |
| expression_result_time_attribute | Expression-result Time Attribute mapping | Yes | A condition row uses Time Attribute | Lookup | Time Attribute search term and selected TimeAttrributeFieldId | resolve_time_category_expression_time_attribute | The expression result requires the same selected resolved Name in TimeAtrbFldName and RefrencedTimeAtrbName | Provide a search term or select TimeAttrributeFieldId | Selected DisplayName, Name, TimeAttrributeFieldId, ORA_HWM_TCAT_EXPR_RESULT.TimeAtrbFldName, and ORA_HWM_TCAT_EXPR_RESULT.RefrencedTimeAtrbName |
| specific_value_resolution | Specific Value resolution | Conditional | Value Type is Specific Value | Lookup or Validate | Selected TimeAttrributeFieldId, ImplementationType, and value search term or supplied value | resolve_time_category_specific_value | Values must follow the documented data-source contract and populate every export-required display and selection field | Provide a value search term or supplied value | Resolved business display value, selection values, or a validated FORMAT_VALUE_SET value |
| fsm_package | Export-shaped FSM package | Yes | Create or edit | Verify | Fresh Time Categories FSM export archive | verify_time_categories_fsm_package | Preserves the declared FSM route and package structure while changing only approved records | No user-supplied archive is required; obtain a fresh same-task export | FSM marker, task-scoped CSV, keys, scope, ZIP evidence, and unchanged metadata, headers, and unrelated rows |
| final_completion | Task-authorized asynchronous status monitoring and category read-back verification | Yes | An approved Time Categories create, edit, import, or load is accepted | Verify | Accepted request identity, approved immutable artifact, Data Loader status route, authoritative Time Categories export, and approved normalized configuration | monitor_and_verify_approved_time_category_request | Submission acceptance alone does not prove that condition rows render as the approved category expression | Monitor the accepted request. On terminal success, refresh the Time Categories export and compare the persisted category; stop on a mismatch | Accepted request ID, terminal status, read-back evidence, verified category fields, verified condition expression, or mismatch evidence |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The dependency has documented authoritative evidence | No |
| Lookup | A documented selection or identity resolver is available | Read-only lookup only |
| Verify | Existing package evidence must be checked | No |
| Not Applicable | The dependency condition is false | No |
| Needs Input | A required business value is missing | No |
| Unresolved | The source, match rule, or result is TBD, unavailable, or ambiguous | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TC.DEPENDENCIES | step | 20 | resolve_dependency | ready->TC.VERIFY_FSM;not_applicable->TC.VERIFY_FSM;needs_input->TC.ERROR;unresolved->TC.ERROR | TC.VALIDATE | stop | Input validation has passed |
