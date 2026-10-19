# HCM Exclusion Rules Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Reconcile existing rule and child rows | Resolve the supplied or derived Name through exclusionRules with the ExclusionType-specific child collection expanded |
| 2 | Enforce attribute readiness | Identify the exclusion type, attribute mapping, operator, and supplied free-text comparison value before generating a package |
| 3 | Enforce supported package construction | Build the package only from the fresh validated HCM Exclusion Rules task export, preserve its supported metadata and parent-detail contract, apply the documented criterion-to-detail-field mappings, and leave unavailable optional values empty |
| 4 | Enforce one approval gate | Build the core Data Loader task-validation preview from the final immutable package, obtain one approval for that preview, then submit one core.data-loader task-level import and verify its returned process log |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| An attribute-based exclusion rule is prepared | Blocker | resolve_exclusion_rule_attribute_from_lov | The supplied attribute is not returned by exclusionRuleAttributesLOV for the selected exclusion type, the exact attribute mapping is unresolved, or the supplied comparison text is empty | Stop import, tell the user that the specified attribute cannot define the exclusion, and select a returned attribute with the appropriate exclusion type | Yes |
| An attribute-based exclusion rule is prepared and its resolved ColumnName is not SET_ID | Blocker |  | The supplied comparison text has been value-set or LOV validated, normalized, or replaced instead of retained as supplied free text | Retain the supplied nonempty comparison text unchanged in AttributeValue; do not run a value-set or LOV validation for it | Yes |
| An attribute-based exclusion rule is prepared | Blocker | resolve_attribute_operator_from_common_lookup | The operator is unresolved | Resolve the operator before generating the package | Yes |
| An attribute-based exclusion rule requires an exact comparison | Blocker | resolve_attribute_operator_from_common_lookup | The resolved operator is not Equals | Use the Equals operator for an exact attribute-value match | Yes |
| An attribute-based exclusion rule requires a partial comparison that begins with the supplied value | Blocker | resolve_attribute_operator_from_common_lookup | The resolved operator is not Starts With | Use the Starts With operator for a partial attribute-value match beginning with the supplied value | Yes |
| An attribute-based exclusion rule maps to ColumnName SET_ID | Blocker | resolve_set_id_from_set_id_sets | The supplied SetName or SetCode does not resolve to exactly one SetId and SetCode, both supplied selectors resolve to different rows, AttributeSetCode does not contain the returned SetCode, or AttributeValue does not contain the returned SetId | Resolve one exact current reference-data set through setIdSets; populate AttributeSetCode with its SetCode and AttributeValue with its SetId | Yes |
| A list exclusion child row is prepared | Blocker | resolve_exclusion_rule_by_name_with_children | A returned child has the same documented list identity but the package creates another detail row | Omit the duplicate child row from the package | Yes |
| An existing exclusion-rule parent is prepared | Blocker | resolve_exclusion_rule_by_name_with_children | The package omits the returned ExclusionRuleId from the parent row | Populate the returned ExclusionRuleId and reconcile only its selected child collection | Yes |
| An attribute or hierarchy exclusion child row is prepared | Blocker | resolve_exclusion_rule_by_name_with_children | A matching existing child is returned but ExclusionRuleDtlId is empty or the package creates another detail row | Populate the returned ExclusionRuleDtlId and update that child row | Yes |
| An HCM exclusion-rule CSV package is generated | Blocker |  | An unavailable optional field contains the literal #null marker instead of an empty value | Apply the Unavailable optional CSV value default and leave the field empty | Yes |
| An HCM exclusion-rule CSV package is generated or imported | Blocker | resolve_hcm_exclusion_rule_csv_layout | The package is not based on a current template-only export, differs from its resolved members, headers, mappings, row relationships, or metadata node order; uses a ViewInstanceName or GroupingKey that differs from the template output and applicable fallback; modifies metadata; or the core Data Loader task-validation preview and its single approval do not cover the exact archive | Re-export the task, rebuild only with identified attributes through the resolver output, use the documented fallbacks only when the template omits a migration value or grouping pattern, preserve ASM_SETUP_CSV_METADATA.xml byte-for-byte, build the task-validation preview, and obtain one approval for that exact archive | Yes |
| An HCM exclusion-rule CSV package is generated or imported | Blocker | resolve_hcm_exclusion_rule_csv_layout | A selected criterion is missing a required detail field or is populated in a different field: non-country list identifier in IdValue; country-list TerritoryCode in Value; attribute FlexContext, ColumnName, TableName, Operator, or AttributeValue; Department Hierarchy or Department Tree TreeCode or TopNodeValue; Position Hierarchy or Supervisor Hierarchy TopNodeValue | Correct the detail row only through the resolver output and documented task mapping rules; use Global Segment for FlexContext when the selected attribute is a global segment | Yes |
| Approval is requested for an exclusion-rule package | Blocker |  | The core Data Loader task-validation preview has not been built from the final immutable archive, or a separate package approval is requested | Build the task-validation preview first and request one approval only for that exact archive | Yes |
| An exclusion-rule create or update is requested | Blocker | | The requested route is direct REST POST, PUT, or PATCH, or does not use core.data-loader with returned-process-log verification | Use the approved immutable package and core.data-loader only | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_exclusion_type_from_common_lookup | An exclusion type is resolved | Validated exclusion type and meaning | ora_reference_lookups.md |
| resolve_exclusion_rule_attribute_from_lov | An attribute-based exclusion rule is prepared | FlexfieldContextCode, ColumnName, TableName, ExclusionType | ora_reference_lookups.md |
| resolve_attribute_operator_from_common_lookup | An attribute-based exclusion rule is prepared | Operator Type and meaning | ora_reference_lookups.md |
| resolve_set_id_from_set_id_sets | An attribute-based exclusion rule maps to ColumnName SET_ID | SetId and SetCode from supplied SetName or SetCode | ora_reference_lookups.md |
| resolve_hcm_exclusion_rule_csv_layout | An HCM exclusion-rule CSV package is generated or imported | Template-derived members, headers, mappings, row relationships, and metadata; template-derived or fallback ViewInstanceName values; template-derived or distinct generated new-row GroupingKeys | ora_reference_lookups.md |
| resolve_exclusion_rule_by_name_with_children | An exclusion rule is created or updated | ExclusionRuleId and type-specific existing child rows | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HCMEX.ENFORCE | decision | 40 | design_enforcement | compliant->HCMEX.CSV_READINESS;blocked->HCMEX.RETURN_ISSUES | HCMEX.RESOLVE_REFERENCES | stop | A validated HCM exclusion-rule configuration is being prepared for preview or CSV package generation |
