# HCM Exclusion Rules Dependency Readiness

The downloaded HCM Exclusion Rules export establishes the current-environment CSV baseline. Before preparing any future import package, obtain a fresh export and validate that it retains this object, view, and linkage contract. Preserve ASM_SETUP_CSV_METADATA.xml byte-for-byte; do not edit, regenerate, rename, or replace it.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Exclusion rule Name and existing children | Use the supplied Name or derive it from the functional definition; resolve it through exclusionRules with the ExclusionType-specific child collection expanded |
| 2 | Exclusion Type | Resolve the supplied exclusion type through `hcm.hcm-security.hcm-security-common.manage-common-lookups` using ORA_PER_EXCLUSION_TYPE |
| 3 | Exclusion value | Resolve a selected list or hierarchy value through its documented LOV resolver. For an attribute-based exclusion, resolve attribute metadata. Retain a supplied comparison value as literal free text unless the resolved attribute maps to ColumnName SET_ID; for that set-backed attribute, resolve the supplied SetName or SetCode through setIdSets and use its SetCode in AttributeSetCode and SetId in AttributeValue. |
| 4 | Attribute operator | For an attribute-based exclusion, resolve the supplied operator through `hcm.hcm-security.hcm-security-common.manage-common-lookups` using ORA_PER_EXCLUSION_OPERATORS |
| 5 | Current task export | Export a current target-environment template-only HCM Exclusion Rules package and retain its ASM_SETUP_CSV_METADATA.xml unchanged |
| 6 | CSV resolver layout | Resolve every CSV member, header array and order, row relationship, ViewInstanceName, GroupingKey pattern, and metadata node order from that current template-only export. Apply the documented criterion mappings: non-country list identifier to IdValue; country-list TerritoryCode to Value; attribute fields to FlexContext, ColumnName, TableName, Operator, and AttributeValue; Department Hierarchy or Department Tree values to TreeCode and TopNodeValue; Position Hierarchy or Supervisor Hierarchy top node to TopNodeValue. Use the supplied member-specific ViewInstanceName and new-row GroupingKey fallbacks only when the template omits them |
| 7 | CSV rows | Populate only members, fields, and criterion mappings resolved by the template layout and documented task mapping rules. Use the resolved or fallback ViewInstanceName. For each new row whose GroupingKey pattern is absent, generate a distinct uppercase 32-character hexadecimal GUID and use it as that row's GroupingKey. Retain ASM_SETUP_CSV_METADATA.xml byte-for-byte unchanged |
| 8 | Task-validation preview | Generate the final immutable CSV package, then build the core Data Loader task-validation preview for those exact archive bytes before requesting approval |
| 9 | Single approval | Obtain one explicit approval for the exact task-validation preview and immutable archive; do not request a separate package approval |
| 10 | Import and verification | Verify the approved task-validation envelope against the unchanged archive, then submit one approved task-level import through core.data-loader and verify the returned process log |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| exclusion_type_lookup | Exclusion Type | Yes | Creating or updating an exclusion rule | Lookup | `hcm.hcm-security.hcm-security-common.manage-common-lookups`; lookupType=ORA_PER_EXCLUSION_TYPE | resolve_exclusion_type_from_common_lookup | The supplied type must be a valid exclusion-type lookup code | Provide a valid exclusion type code | Exclusion Type and meaning |
| exclusion_rule_child_reconciliation | Exclusion rule parent and child rows | Yes | Creating or updating an exclusion rule | Lookup | exclusionRules; supplied or derived Name and selected ExclusionType | resolve_exclusion_rule_by_name_with_children | Existing parents and their type-specific children must be reconciled before CSV rows are prepared | Provide a Name and selected exclusion type; stop if same-name parents are ambiguous or have a different type | ExclusionRuleId, ExclusionRuleDetailId, and selected child rows |
| exclusion_value_lookup | Selected list or hierarchy value | Yes | A list or hierarchy exclusion criterion is configured | Verify | Documented individual LOV resource and display value for the selected exclusion type | resolve_hcm_exclusion_rule_csv_layout | The selected value must resolve to its mandated detail-row mapping: non-country list identifier to IdValue, country-list TerritoryCode to Value, Department Hierarchy or Department Tree TreeCode and top department to TreeCode and TopNodeValue, and Position Hierarchy or Supervisor Hierarchy top node to TopNodeValue | Provide the selected display value and any required disambiguator | IdValue, Value, TreeCode, or TopNodeValue as applicable |
| exclusion_rule_attribute_lookup | Attribute exclusion value | Yes | An attribute-based exclusion criterion is configured | Lookup | exclusionRuleAttributesLOV; selected attribute exclusion type; supplied AttributeDisplayName | resolve_exclusion_rule_attribute_from_lov | The selected attribute must resolve to its documented FlexfieldContextCode, ColumnName, and TableName mapping | Provide the attribute display name; if multiple results are returned, provide an exact attribute | FlexContext, ColumnName, and TableName |
| attribute_comparison_text | Attribute comparison value | Yes | An attribute-based exclusion criterion is configured and resolved attribute metadata does not map to ColumnName SET_ID | Verify | User-supplied free text | resolve_hcm_exclusion_rule_csv_layout | Attribute comparison values are free text and require no value-set or LOV validation; the detail row must retain it unchanged in AttributeValue | Provide nonempty comparison text; retain it unchanged in AttributeValue | AttributeValue |
| set_backed_attribute_value | Set-backed attribute comparison value | Yes | Resolved attribute metadata maps to ColumnName SET_ID | Lookup | Supplied SetName or SetCode; setIdSets | resolve_set_id_from_set_id_sets | A set-backed attribute compares a stored SetId, so the supplied set selector must resolve to one current SetId and SetCode before it can populate the detail row | Provide one exact SetName or SetCode; when both are supplied they must identify the same set | AttributeSetCode from SetCode; AttributeValue from SetId |
| attribute_operator_lookup | Operator Type | Yes | An attribute-based exclusion criterion is configured | Lookup | `hcm.hcm-security.hcm-security-common.manage-common-lookups`; lookupType=ORA_PER_EXCLUSION_OPERATORS | resolve_attribute_operator_from_common_lookup | The supplied operator must be a valid attribute-exclusion operator lookup code and populate Operator in the detail row | Provide a valid operator type code | Operator and meaning |
| hcm_exclusion_rule_csv_baseline | Current template-only task export and ASM metadata | Yes | Creating or updating an exclusion rule | Verify | Current target-environment HCM Exclusion Rules template-only export, unchanged ASM_SETUP_CSV_METADATA.xml, and documented task criterion mappings | resolve_hcm_exclusion_rule_csv_layout | The template defines the permitted members, headers, row relationships, ViewInstanceName values, GroupingKey patterns, and metadata node order; the task criterion mappings define the required detail fields; documented fallbacks apply only when a migration value or grouping pattern is absent | Export the task again and resolve its layout before preparing rows; preserve ASM_SETUP_CSV_METADATA.xml byte-for-byte. | Immutable layout context, criterion mappings, fallback decisions, generated new-row GroupingKeys, and metadata bytes |
| hcm_exclusion_rule_csv_package | Immutable supported CSV package | Yes | Preparing an exclusion-rule import | Verify | Required exclusion-rule attributes plus fresh validated template layout | resolve_hcm_exclusion_rule_csv_layout | A supported package can be generated only after every selected criterion is placed in its required detail field and the current template establishes the permitted members, headers, relationships, migration values, and metadata | Populate only the identified attributes and values through the resolver output and documented criterion mappings, then build the core Data Loader task-validation preview from the final archive | Immutable CSV ZIP preview and task-validation preview |
| exclusion_rule_child_idempotency | Existing child-row behavior | Yes | Preparing a list, attribute, or hierarchy exclusion detail row | Verify | Existing parent and selected child collection from exclusionRules | resolve_exclusion_rule_by_name_with_children | List rows are idempotent by child identity; attribute and hierarchy rows update the matching child row | Omit an already-present list child; use returned ExclusionRuleDtlId for an existing attribute or hierarchy child | Omitted list rows or existing ExclusionRuleDtlId for update rows |
| hcm_exclusion_rule_task_validation_approval | Single task-validation approval | Yes | Importing an exclusion-rule package | Verify | Final immutable archive and its core Data Loader task-validation preview | | One approval must cover the exact preview and final archive bytes | Request one approval only after the task-validation preview is available; do not request a separate package approval | Approved task-validation envelope |
| hcm_exclusion_rule_csv_mutation_route | Core Data Loader-only mutation route | Yes | Creating or updating an exclusion rule | Verify | Approved task-validation envelope, unchanged immutable archive, core.data-loader task-level import, and returned process log | | Exclusion-rule changes are permitted only through core.data-loader after the single task-validation approval and process-log verification | Do not use REST POST, PUT, or PATCH. Verify the approved envelope against the exact archive, run one core.data-loader import, and verify the result | Approved task-validation envelope and import process log |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Lookup | A supplied exclusion type, selected list or hierarchy value, attribute, or attribute operator requires resolution | Yes |
| Blocked | A required LOV returns no match or cannot be disambiguated | No |
| Satisfied | A current template-only export resolves unambiguous members, headers, mappings, row relationships, and metadata node order; ViewInstanceName and GroupingKey use template values or the documented fallback; ASM_SETUP_CSV_METADATA.xml is unchanged | No |
| Blocked | A required CSV member, header, mapping, row relationship, or metadata contract is missing, ambiguous, or inconsistent | No |
| Blocked | Required rule attributes, the fresh validated export, task-validation preview, single approval, approved envelope, or verification plan is missing | No |
| Ready | All CSV package and Core Data Loader import-route dependencies are satisfied | No |

## CSV Resolver Layout

| CSV Object | Parent Identity Field | ViewInstanceName | GroupingKey | Resolver Requirement |
|---|---|---|---|---|
| ORA_PER_HCM_EXCLUSION_RULE.csv | Template-resolved relationship field or fields | Template-derived value; otherwise ExclusionRuleMigration | Template-derived pattern; otherwise a distinct generated uppercase 32-character hexadecimal GUID for each new row | Use only the resolver output for members, columns, identity fields, and row ordering; use the supplied fallback only when the template omits the migration value or grouping pattern |
| ORA_PER_HCM_EXCLUSION_RULE_DETAIL.csv | Template-resolved relationship field or fields | Template-derived value; otherwise ExclusionRuleDetailMigration | Template-derived pattern; otherwise a distinct generated uppercase 32-character hexadecimal GUID for each new row | Use only the resolver output for members, columns, identity fields, and row ordering; use the supplied fallback only when the template omits the migration value or grouping pattern |

## ASM Metadata Preservation Rules

| Rule | What Must Happen |
|---|---|
| Source artifact | Use ASM_SETUP_CSV_METADATA.xml from a fresh exported HCM Exclusion Rules task package |
| Immutability | Preserve ASM_SETUP_CSV_METADATA.xml byte-for-byte; do not edit, regenerate, rename, replace, or merge it |
| Batch and object order | Preserve the template-derived metadata node order and CSV-member order; do not exchange, add, or omit members |
| ViewInstanceName | Use the ViewInstanceName resolved for each member from the current template. If absent, use ExclusionRuleMigration for ORA_PER_HCM_EXCLUSION_RULE.csv or ExclusionRuleDetailMigration for ORA_PER_HCM_EXCLUSION_RULE_DETAIL.csv |
| Row relationships | Use only the parent-child or other row relationships resolved from the current template; do not infer linkage fields or values |
| GroupingKey | Use the pattern resolved for each generated row from the current template. If absent, generate one distinct uppercase 32-character hexadecimal GUID for each new row and use it as that row's GroupingKey; do not reuse, copy, or mix values across rows |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HCMEX.CSV_READINESS | decision | 50 | resolve_dependency | ready->HCMEX.READY;blocked->HCMEX.RETURN_ISSUES | HCMEX.ENFORCE | stop | A supported HCM exclusion-rule CSV package is being generated or imported |
