# Time Categories Reference Lookups

## Source Basis

- Developer-provided Time Categories UI structure and screenshot, 2026-09-08.
- Developer-provided Time Categories FSM authoring input, 2026-09-08.
- Developer-provided Time Attribute and value-resolution workflow, 2026-10-05.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| verify_time_categories_fsm_package | A create or edit package is prepared | Fresh ORA_HWM_MANAGE_TIME_CATEGORIES export archive; for edit, user-provided Current Name | Local export archive | ASM_SETUP_CSV_METADATA.xml marker, task-scoped CSV, keys, changed-row scope, ZIP bytes, and for edit one exact Current Name row | Require a fresh same-task export with the exact-case marker and approved task scope; for edit require exactly one exported row whose current Name exactly matches Current Name | Validated FSM archive for core.data-loader; for edit the matching exported row and current values | Stop when a fresh export cannot be obtained or validated, or when Current Name matches zero or multiple exported rows |
| resolve_time_category_expression_time_attribute | A Time Attribute search term is supplied for a condition row | Time Attribute search term | GET {FA_HOST}/hcmRestApi/resources/11.13.18.05/timeAttributeFieldsLOV?onlyData=true&orderBy=DisplayName&q=Name LIKE '%{timeAttributeSearchTerm}%' OR DisplayName LIKE '%{timeAttributeSearchTerm}%'&fields=DisplayName,Name,TimeAttrributeFieldId&limit=25&offset=0 | DisplayName, Name, TimeAttrributeFieldId | Use a case-insensitive contains search; retrieve every page before evaluating match count. Retain one result, or require the user to choose the Name when several results remain. | Selected DisplayName, Name, and TimeAttrributeFieldId; populate both ORA_HWM_TCAT_EXPR_RESULT.TimeAtrbFldName and ORA_HWM_TCAT_EXPR_RESULT.RefrencedTimeAtrbName with the selected Name. | No result: request another Time Attribute search term. Multiple results: show every Name value and require the user to choose one. |
| resolve_time_category_time_attribute_data_source | Exactly one Time Attribute is selected | Selected TimeAttrributeFieldId | GET {FA_HOST}/hcmRestApi/resources/11.13.18.05/timeAttributeDataSources/{TimeAttrributeFieldId} without a fields query parameter | Entire returned data-source response | Verify returned TimeAttributeFieldId corresponds to selected TimeAttrributeFieldId. Stop when no data source is returned, the identity differs, or ImplementationType is blank. | TimeAttributeFieldId, Name, ParentTimeAttributeFieldId, AttributeType, ValueSetId, ValueSetCode, ValueDataType, Precision, Scale, MinimumValue, MinimumValueNumber, MinimumValueDate, MinimumValueTimestamp, MaximumValue, MaximumValueNumber, MaximumValueDate, MaximumValueTimestamp, DataSourceUsageId, UsageType, DataSourceId, DataSourceCode, and ImplementationType | Stop before preview and disclose the failed data-source condition. |
| resolve_time_category_specific_value | Value Type is Specific Value and ImplementationType is DEPENDENT_VALUE_SET, INDEPENDENT_VALUE_SET, TABLE_VALUE_SET, or VIEW_OBJECT | Selected TimeAttrributeFieldId and value search term | GET {FA_HOST}/hcmRestApi/resources/11.13.18.05/timeAttributeDataSources/{TimeAttrributeFieldId}/child/ValuesList?q=Value LIKE '%{valueSearchTerm}%'&fields=Code,Value,ValueChar,ValueDate,ValueNumber&limit=25&offset=0; omit q for a complete list | Code, Value, ValueChar, ValueDate, ValueNumber | Use a case-insensitive contains search; retrieve every page before evaluating match count. Code is the selection identifier; do not merge duplicate display values. | Selected Code, business display Value, and selection values; map them to every corresponding display and selection field required by the fresh export | No result: request another value search term. Multiple results: show every result and require Code. |
| search_existing_time_categories | A derived requirement needs a Time Category | Derived business terms and a fresh ORA_HWM_MANAGE_TIME_CATEGORIES export archive | Local export archive; use `ORA_HWM_TCAT_CMP.csv`, `ORA_HWM_TCAT_GRP_EXPR_RESULT.csv`, and `ORA_HWM_TCAT_EXPR_RESULT.csv` | Name, Description, Unit of Measure, Track Usage, and an ordered plain-language condition summary | Return an exact match when normalized supplied terms match the category name or every confirmed condition. Return close matches when at least two significant derived terms match the name, description, unit of measure, attribute label, or displayed condition value. Mark a category as delivered only when its Description explicitly identifies it as Delivered. | Exact and close matches, condition summaries, delivered status, and search evidence | Return no match when no category meets either rule; do not infer that a category is delivered from its name or identifier. |
| monitor_and_verify_approved_time_category_request | An approved Time Categories create, edit, import, or load is accepted | Accepted request identity, approved immutable artifact, Data Loader status route, authoritative export, and approved normalized configuration | Selected Data Loader status route and fresh Time Categories export | Request status, authoritative category parent, group expression, and ordered conditions | Monitor the same accepted request until terminal status. On terminal success, compare the fresh export with the approved configuration; classify absent, extra, reordered, unlinked, or mismatched conditions as mismatched. | Terminal status and read-back comparison evidence | Stop on failed, timed-out, partial, uncertain, or mismatched results; do not submit another load. |

## Lookup Execution Rules

## Time Attribute and Value Resolution Contract

The inputs are `timeAttributeSearchTerm`, `valueType`, and
`valueSearchTermOrValue`. The user may select a Time Attribute at any point.
Resolve or request a Value only when `valueType` is `Specific Value`.

1. Search `timeAttributeFieldsLOV` with the documented case-insensitive
   contains query, `limit=25`, and `offset=0`. Read `count`, `hasMore`,
   `limit`, and `offset` from each response. While `hasMore` is true, increase
   offset by the returned limit. Do not judge uniqueness from a partial page.
2. If the search has no results, ask for another Time Attribute search term.
   If it has one result, retain DisplayName, Name, and TimeAttrributeFieldId.
   If it has several results, show only the Name values and require the user to choose one.

   ```text
   Multiple Time Attributes matched "{timeAttributeSearchTerm}".

   {results table containing Name only}

   Which Name should be used?
   ```

3. Retrieve the selected attribute's data source without a `fields` query
   parameter. Preserve every returned field and at least inspect the fields
   listed by `resolve_time_category_time_attribute_data_source`. The spelling
   differs across services: `timeAttributeFieldsLOV` returns
   `TimeAttrributeFieldId`; `timeAttributeDataSources` returns
   `TimeAttributeFieldId`. Verify the two selected identities correspond.
4. When Value Type is not `Specific Value`, do not enable or request Value,
   do not use `valueSearchTermOrValue`, do not call ValuesList, and do not run
   FORMAT_VALUE_SET validation.
5. When Value Type is `Specific Value` and ImplementationType is
   `FORMAT_VALUE_SET`, do not call ValuesList. Validate the supplied value
   using AttributeType and every non-null Precision, Scale, MinimumValue,
   MinimumValueNumber, MinimumValueDate, MinimumValueTimestamp, MaximumValue,
   MaximumValueNumber, MaximumValueDate, and MaximumValueTimestamp returned by
   the data source. If it fails, show the supplied
   value, expected AttributeType, every violated non-null constraint, and the
   returned-metadata format requirement, then ask:

   ```text
   The value "{suppliedValue}" isn't valid for the Time Attribute
   "{DisplayName}".

   Expected attribute type: {AttributeType}

   Violated constraints:

   {violated constraints}

   Enter a value that satisfies the displayed type and constraints.
   ```

6. When Value Type is `Specific Value` and ImplementationType is
   DEPENDENT_VALUE_SET, INDEPENDENT_VALUE_SET, TABLE_VALUE_SET, or VIEW_OBJECT,
   call ValuesList. For a search, use the documented case-insensitive `Value`
   contains query; for a complete list omit `q`. Paginate every request before
   evaluating the result. A single result retains Code, Value, ValueChar,
   ValueDate, and ValueNumber. Several results must be displayed without
   combining duplicate Value fields, then ask which Code to use. A no-match
   result asks:

   ```text
   No values matched "{valueSearchTerm}" for the Time Attribute
   "{DisplayName}".

   Enter another value search term.
   ```

   For several results, use:

   ```text
   Multiple values matched "{valueSearchTerm}" for the Time Attribute
   "{DisplayName}".

   {results table containing Code, Value, ValueChar, ValueDate, and ValueNumber}

   Which Code should be used?
   ```

7. If Value Type is `Specific Value` and ImplementationType is blank or is not
   one of the documented types, stop before preview and ask:

   ```text
   ImplementationType "{ImplementationType}" does not have a documented
   Time Categories value-resolution contract.

   Provide the required value-resolution rules before continuing.
   ```

## Export-Shaped FSM Package Preparation

For a create or edit, use the validated fresh export as the authoritative
baseline. Retain its exact metadata, declared members, headers, keys, row
layout, and unrelated records. Apply only the approved category parent,
expression-group, and ordered condition changes.

For each resolved Specific Value, map the returned business display Value to
every corresponding display field required by the fresh export and map the
returned selection value to every corresponding selection field. The current
export may require a `DisplayValue` field, but package preparation must derive
the required fields from the fresh export rather than treating one header as a
universal schema. A blank or mismatched required display or selection field
blocks preview and approval.

Validate the prepared package against the same fresh export and the Time
Categories task contract. Reject changed metadata, member names, headers, row
widths, unrelated rows, cross-file references, display sequences,
expression-group linkage, or a final-row operator. A failed result blocks
approval and import.

| Situation | What Happens |
|---|---|
| A Time Attribute selection is supplied | Run the Time Attribute search and data-source resolvers; do not proceed until both expression-result fields receive the selected resolved Name. |
| Value Type is Specific Value | Run the documented FORMAT_VALUE_SET validation or ValuesList resolver selected by ImplementationType. |
| Value Type is not Specific Value | Do not request or resolve Value, call ValuesList, or run FORMAT_VALUE_SET validation. |
| A fresh FSM export is required | Validate the local export archive, preserve its metadata and unrelated content, and apply only approved changes. |
| A requirement needs a Time Category | Run search_existing_time_categories before preparing a create package. Present exact and close matches with their business summaries. |
| Multiple plausible matches are returned | Request the user's selection. Do not select, edit, or create a category while the choice is unresolved. |
| One suitable existing category is selected | Reuse it and stop. Do not create a duplicate. |
| A delivered category is selected | Reuse it when suitable. Do not modify its definition. |

## Final Completion Read-Back

`monitor_and_verify_approved_time_category_request` runs after an approved
Time Categories create, edit, import, or load is accepted. Use the same
accepted request identity with the selected Data Loader status route. While it
is pending, running, In progress, or unavailable, continue status monitoring;
do not submit another load. On terminal success, obtain a fresh authoritative
Time Categories export and reconstruct the persisted category expression from
the parent, group-expression, and condition CSV objects.

Compare only supported approved values:

- category parent: name, description, Track Usage, and Unit of Measure;
- group expression: parent reference, group sequence, and group-row linkage;
- every condition, in order: time attribute, value type, explicitly supplied
  value, parentheses, operator, condition sequence, parent/group references,
  and row-type linkage marker.

Treat the category as verified only when the reconstructed export matches the
approved normalized configuration. A successful request with an absent,
extra, reordered, unlinked, or otherwise mismatched condition is
`mismatched`, not complete.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TC.VERIFY_FSM | step | 30 | reference_lookup | resolved->TC.RESOLVE_TIME_ATTRIBUTE;blocked->TC.ERROR;lookup_failure->TC.ERROR | TC.DEPENDENCIES | stop | A create or edit package requires fresh FSM export verification |
| TC.RESOLVE_TIME_ATTRIBUTE | decision | 35 | reference_lookup | resolved->TC.DEFAULTS;not_applicable->TC.DEFAULTS;blocked->TC.ERROR;lookup_failure->TC.ERROR | TC.VERIFY_FSM | stop | A condition row uses a Time Attribute |
| TC.SEARCH_EXISTING | step | 8 | reference_lookup | exact_match->TC.REUSE_EXISTING;close_match->TC.SELECT_EXISTING;no_match->TC.VALIDATE;lookup_failure->TC.ERROR | TC.INTAKE | stop | A derived requirement needs a Time Category. |
| TC.SELECT_EXISTING | decision | 9 | reference_lookup | reuse_selected->TC.REUSE_EXISTING;create_confirmed->TC.VALIDATE;selection_required->TC.RETURN_SELECTION;blocked->TC.ERROR | TC.SEARCH_EXISTING | stop | More than one plausible existing Time Category is returned. |
| TC.FINAL_COMPLETION | step | 95 | reference_lookup | verified->TC.FINAL_COMPLETION_SUCCESS;failed->TC.FINAL_COMPLETION_ERROR;timed_out->TC.FINAL_COMPLETION_ERROR;partial->TC.FINAL_COMPLETION_ERROR;uncertain->TC.FINAL_COMPLETION_ERROR;mismatched->TC.FINAL_COMPLETION_ERROR | TC.LOADER_READY | stop | An approved asynchronous Time Categories submission was accepted. |
