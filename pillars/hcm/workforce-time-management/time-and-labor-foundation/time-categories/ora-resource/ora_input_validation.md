# Time Categories Input Validation

## Source Basis

- Developer-provided Time Categories UI structure and screenshot, 2026-09-08.
- Developer-provided FSM baseline and task-operation guidance, 2026-09-08.
- Developer-provided Time Categories FSM authoring input, 2026-09-08.
- Developer-provided business-only Complete Summary requirements, 2026-09-09.

## Complete Summary Input Contract

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Verified summary source | Use only populated structured business values that completed input validation, applicable lookup resolution, and defaulting or preservation | A Complete Summary is prepared | |
| User selections | Include every verified business value explicitly supplied by the user | Every Complete Summary | |
| Applied defaults | Include every default that was actually applied in a separate Defaults Applied section | Every Complete Summary | |
| Blank and metadata values | Omit blank, null, unused, and metadata-only values | Every Complete Summary | |
| Populated children | Show populated child records using business labels only; do not render an empty child section | A child record has values | |
| Summary readiness | Always generate the Complete Summary before the provider-owned approval process | A create or edit request is ready for provider approval | |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | create or edit | Block | Provide one supported operation | Every request | |
| Time Category name | Name | Block | Provide a nonblank unique name | Create or edit | |
| Existing category identity | Current Name | Block | Provide the existing Time Category Name before supplying any edited Name | Edit | verify_time_categories_fsm_package |
| Condition row minimum | Time Attribute and Value Type | Block | Complete both fields for every added Category Conditions row | A condition row is added | |
| Expression-result Time Attribute mapping | Time Attribute search term or selected TimeAttrributeFieldId | Block | Resolve the selected attribute through the documented paginated search and data-source lookup | A condition row uses Time Attribute | resolve_time_category_expression_time_attribute |
| Specific Value | Value search term or supplied value, plus all export-required resolved display and selection fields | Block | Resolve ValuesList selections or validate FORMAT_VALUE_SET values only when Value Type is Specific Value; map each resolved value to every matching field required by the fresh export | Value Type is Specific Value | resolve_time_category_specific_value |
| Existing-category decision | Search evidence and, when multiple candidates exist, the user's selected category or confirmed no-suitable-category decision | Block | Search existing categories and request a selection when needed | A plain-language requirement needs a Time Category | search_existing_time_categories |
| Explicit update intent | An explicit request to update the named existing category | Block | Obtain explicit update intent; a search, reuse, or read request is not update intent | Edit | |

## Requirement Classification

| Result | Use When | Next Action |
|---|---|---|
| category_required | The requirement identifies a population of time entries that must be included, excluded, filtered, transferred, displayed, totaled, attested, or evaluated by a category | Derive the population and business purpose, then search existing categories |
| not_required | The requirement concerns a Time and Labor object without a category-based population decision | Return without creating or updating a Time Category |
| clarification_required | The requirement cannot reliably establish whether a category is needed | Ask whether the requested outcome depends on selecting a population of time entries |

Before an existing-category search, retain the original requirement, category
need, intended time-entry population, business purpose, candidate business
terms, and any explicit unit of measure or condition logic. Do not infer an
attribute value or condition operator from a similarly named category.

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An edit request supplies Current Name | Require the fresh Time Categories export to contain exactly one matching current Name | Continue only with the matching exported row as the edit target | verify_time_categories_fsm_package |
| A Time Attribute is supplied | Require the selected attribute's data source and resolved expression-result Name before package preparation | Retain the selected Name for both expression-result fields | resolve_time_category_expression_time_attribute |
| Value Type is Specific Value | Require a value selection or a valid FORMAT_VALUE_SET value | Apply the documented ImplementationType branch | resolve_time_category_specific_value |
| A Specific Value is ready for package preparation | Require every export-required display and selection field to contain its corresponding resolved value | Block preview when any required field is blank or mismatched | resolve_time_category_specific_value |
| Value Type is not Specific Value | Do not require, request, or resolve Value | Ignore valueSearchTermOrValue | |
| A create or edit request is ready for package preparation | Fresh same-task FSM export is required | Obtain and validate a fresh Time Categories export | verify_time_categories_fsm_package |
| A create or edit request is ready for provider approval | Require a Complete Summary formed only from verified structured business values | Generate the summary before the provider-owned approval process | |
| A plain-language requirement has no suitable existing category | Require confirmation of the proposed category definition before package preparation | Retain only confirmed attributes, values, and condition logic | search_existing_time_categories |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name is blank | Reject the request | Create or edit | |
| Current Name is blank | Reject the request | Edit | |
| Name is not unique | Reject the request | Create or edit | |
| Track Usage is changed | Reject the requested change | Edit | |
| Unit of Measure is supplied | Accept only Days, Hours, or Units | Create or edit | |
| Time Attribute is supplied | Require a selected attribute from the complete paginated result set and a matching nonblank ImplementationType data source | Create or edit | resolve_time_category_expression_time_attribute |
| Value Type is Specific Value | Validate the supplied value against AttributeType and non-null constraints for FORMAT_VALUE_SET, or resolve ValuesList by Code for documented selectable value sets; populate every corresponding display and selection field required by the fresh export | Create or edit | resolve_time_category_specific_value |
| A required resolved display or selection field is blank or mismatched | Reject the package before preview | Create or edit | resolve_time_category_specific_value |
| Value Type is not Specific Value | Reject any attempt to resolve or validate Value | Create or edit | |
| Added condition row omits Time Attribute or Value Type | Reject the row | Create or edit | |
| Condition expression has unbalanced parentheses | Reject the expression | Multiple condition rows use grouping | |
| Operator is absent between populated condition rows or present on the final row | Reject the expression | Multiple populated condition rows | |
| Unsupported field is supplied | Reject the field | Create or edit | |
| An edit follows a category search or reuse request | Reject the edit | An existing category is found but no explicit update is requested | |
| A condition has an operator after the final populated row | Reject the expression | One or more condition rows | |
| A condition supplies an unknown value field | Reject the condition | Create or edit | |

## Normalized Condition Contract

Represent each populated condition as an ordered object with `time_attribute`,
`value_type`, optional `values` map, optional `left_parenthesis_count`, optional
`right_parenthesis_count`, and optional `operator_after`. `operator_after`
belongs to the current row and must be blank on the final row. The compiler may
accept a task-supported value field such as a character, date, identifier, or
timestamp only when it is supplied explicitly in `values` using its supported
field name. It must not obtain it by copying an existing category row.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TC.INTAKE | decision | 5 | validate_input | category_required->TC.SEARCH_EXISTING;not_required->TC.RETURN_NOT_REQUIRED;clarification_required->TC.RETURN_CLARIFICATION | none | stop | A plain-language Time and Labor requirement is supplied |
| TC.VALIDATE | step | 10 | validate_input | valid->TC.DEPENDENCIES;missing->TC.ERROR;invalid->TC.ERROR | none | stop | A Time Categories create or edit request is prepared |
