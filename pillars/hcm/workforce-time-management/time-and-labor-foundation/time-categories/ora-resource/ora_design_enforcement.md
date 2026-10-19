# Time Categories Design Enforcement

## Source Basis

- Developer-provided Time Categories UI structure, screenshot, and task behavior, 2026-09-08.
- Developer-provided FSM baseline, 2026-09-08.
- Developer-provided Time Categories FSM authoring input, 2026-09-08.
- Developer-provided business-only Complete Summary requirements, 2026-09-09.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm operation | Allow create or edit only. |
| 2 | Validate category details | Enforce Name uniqueness and edit restrictions. |
| 3 | Validate expression | Permit no condition rows; otherwise enforce completed rows, operator placement, order, and balanced grouping. |
| 4 | Resolve Time Attribute and data source | Search all Time Attribute pages, require a user selection for multiple results, retrieve the selected data source, and map the selected Name to both expression-result fields. |
| 5 | Resolve Specific Value | Only when Value Type is Specific Value, validate FORMAT_VALUE_SET input or resolve a documented ValuesList selection by Code. |
| 6 | Validate advanced condition | Treat Rule Name as optional and independent of Category Conditions. |
| 7 | Prepare export-shaped FSM package | Use the fresh export as the package baseline. Preserve its metadata, declared members, headers, keys, and unrelated rows; apply only the approved parent, group, and condition changes. |
| 8 | Validate FSM source | Validate the prepared package against the same fresh export and task-specific field rules before handoff. |
| 9 | Generate Complete Summary | Always generate exactly one business-only Complete Summary from verified structured fields after validation, lookup resolution, and defaulting or preservation. |
| 10 | Complete import preflight | Complete Core Data Loader validation, persist the immutable preflight artifact, and complete Task Hook validation for the exact ZIP. |
| 11 | Present validated package | Display one clickable link to the exact FSM ZIP package that passed validation outside the business-only Complete Summary. |
| 12 | Gate provider approval | Request one approval immediately before upload and import, after every validation gate passes. |
| 13 | Reuse before create | Search existing Time Categories from the derived requirement, reuse a suitable selected category, and create only after no suitable category is confirmed. |
| 14 | Protect delivered and downstream configuration | Never modify a delivered category. Do not create or update downstream consumer sets, layouts, balance definitions, attestations, or profiles in this task. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Error | | The requested operation is delete or unsupported | Use create or edit only | No |
| Create or edit | Error | | Name is blank or not unique | Supply a unique Name | Yes |
| Edit | Error | verify_time_categories_fsm_package | Current Name does not match exactly one row in the fresh export | Provide the existing Time Category Name and refresh the export | Yes |
| Edit | Error | | Track Usage is changed | Preserve the existing Track Usage value | Yes |
| A condition row is added | Error | | Time Attribute or Value Type is missing | Complete the row before save | Yes |
| A condition row uses Time Attribute | Error | resolve_time_category_expression_time_attribute | The selected Time Attribute was not resolved from all pages, its data source is absent or mismatched, ImplementationType is blank, or the expression-result fields are absent, differ, or do not contain the selected Name | Complete Time Attribute and data-source resolution before preview | Yes |
| Value Type is Specific Value | Error | resolve_time_category_specific_value | FORMAT_VALUE_SET validation failed, ValuesList was not resolved through all pages, or an undocumented ImplementationType was accepted | Correct the value or provide documented value-resolution rules | Yes |
| Value Type is Specific Value | Error | resolve_time_category_specific_value | An export-required display or selection field is blank, or does not contain the resolved value | Populate every export-required resolved field before preview | Yes |
| Multiple populated condition rows | Error | | Operators are missing between rows, present on the final row, grouping is unbalanced, or row order is not preserved | Correct the logical expression without reordering unrelated rows | Yes |
| Value Type is not Specific Value | Error | | Value was enabled, requested, resolved, validated, or ValuesList was called | Omit Value processing | Yes |
| A Time Categories FSM package is authored | Error | verify_time_categories_fsm_package | Any declared CSV business object has a mismatched header, row width, reference, expression group, populated display-sequence ordering, or terminal operator | Rebuild from the normalized configuration and the fresh export contract; preserve literal `0`, blank, and `#null` values only when the contract or requested business value requires them | Yes |
| Create or edit | Error | verify_time_categories_fsm_package | Fresh FSM export evidence or package validation is missing | Obtain and validate a fresh same-task export | Yes |
| A validated request is ready for provider-owned approval | Error | | A clickable link to the exact validated FSM ZIP is absent, or it points to a different package | Display the link to the immutable validated package outside the Complete Summary, then request approval | Yes |
| A validated request is ready for provider-owned approval | Error | | Complete Summary is absent; contains a blank, metadata-only, technical, identifier, code, key, opaque link, request detail, fingerprint, diagnostic, or warning; omits a verified user selection or actually applied default; or uses a technical label where a verified business label is available | Generate the exact business-only summary format below, then transition to the provider-owned approval process without changing provider execution or approval ownership | Yes |
| A create is requested from a plain-language requirement | Error | search_existing_time_categories | Existing-category search was not completed, an exact match was ignored, or a close match has not been presented for selection | Complete the search and reuse a suitable selected category; create only after no suitable category is confirmed | Yes |
| A delivered category is selected | Error | search_existing_time_categories | The requested operation is edit | Reuse the delivered category or select a different non-delivered category; do not modify delivered definitions | No |
| An existing category is updated | Error | verify_time_categories_fsm_package | The user has not explicitly requested the update or has not received the downstream-impact warning | Obtain explicit update intent after warning that rules, consumer sets, layouts, balances, and attestations can be affected | Yes |
| Any Time Categories request | Error | | The proposed work creates or updates a consumer set, layout, balance definition, attestation, or profile | Remove downstream-object actions; this task is limited to the Time Category and its approved conditions | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_time_categories_fsm_package | Create or edit | Fresh FSM marker, task-scoped CSV, keys, scope, and ZIP evidence; for edit one exact Current Name row | ora_reference_lookups.md |
| resolve_time_category_expression_time_attribute | A condition row uses Time Attribute | Selected DisplayName, Name, TimeAttrributeFieldId, matching TimeAttributeFieldId data source, and one Name mapped to both expression-result fields | ora_reference_lookups.md |
| resolve_time_category_specific_value | Value Type is Specific Value | Valid FORMAT_VALUE_SET value or selected ValuesList Code and returned value fields | ora_reference_lookups.md |
| search_existing_time_categories | A create is proposed from a plain-language requirement or a delivered category is targeted for edit | Existing-category search evidence, selected reuse or confirmed no-suitable-category decision, and delivered status | ora_reference_lookups.md |

## Required Complete Summary Format

Generate exactly this business-only structure after validation, lookup resolution,
and defaulting or preservation. Add a populated child section only when it has
business values; do not render empty child sections.

```md
## Complete Summary
| Business Setting | Selected Value |
|---|---|
| <business label> | <verified business display value> |

## Defaults Applied
| Business Setting | Default Applied |
|---|---|
| <business label> | <verified default display value> |
```

The summary must include every verified user-provided business value and every
actually applied default. Display identifiers as resolved business display
names, codes as verified business meanings, and booleans as Selected or Not
selected, Enabled or Disabled, or Yes or No. Display internal statuses using a
verified business-friendly status such as Draft or Submitted. Keep technical
values internally for validation and provider execution.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TC.ENFORCE | step | 50 | design_enforcement | passed->TC.ROUTE;not_applicable->TC.ROUTE;blocked->TC.ERROR | TC.DEFAULTS | stop | Validation, lookup resolution, defaults, preservation, and Complete Summary generation have completed |
