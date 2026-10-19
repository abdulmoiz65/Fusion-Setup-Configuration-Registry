# Cost Component Mapping Groups Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Verify set access | Confirm the mapping group is created only for a set the user can manage |
| 2 | Advise on the default cost component mapping | When it is absent from the supplied Data Loader workbook, show the readiness message; place it first only when it is included in the request |
| 3 | Protect predefined component inventory treatment | Do not attempt to edit the predefined component Include in Inventory setting |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A mapping group is created | Error | resolve_accessible_set | SetName cannot be confirmed as accessible to the current user | Use a set the user can manage | Yes |
| A non-default child mapping is prepared | Information | read_predefined_component_mappings | The current group has no mapped default predefined component | Display the default-component readiness message; allow the otherwise valid mapping to proceed | Yes |
| A predefined component mapping is prepared | Error | | The request attempts to set or edit Include in Inventory | Do not edit this setting; it is always Yes except for nonrecoverable tax, for which it is No | Yes |
| A mapping group is updated or deleted | Error | read_mapping_group | isUsedInCostProfile=Y | Reject the parent PATCH or DELETE request | No |
| A mapping group is deleted | Information | read_mapping_group | Component-code or cost-element child mappings still exist | Disclose the children, then submit the parent-only DELETE. Prepare a separate child cleanup only if Fusion rejects that parent operation because of the remaining children. | Yes |
| A landed-cost-management mapping is updated | Error | check_capitalization_control | CapitalizationFlag is changed when isUsedinCTC=Y | Treat CapitalizationFlag as read-only | No |
| A child mapping is created or updated | Error | validate_destination_set_scope | DestSetName is neither the mapping group's set nor Common Set | Use the mapping group's set or Common Set | Yes |
| A cost-element mapping is created or updated | Error | validate_cost_element_source_set_scope | SourceSetName is not returned by the group-set-specific UI source-set lookup | For a Common mapping group use the `q=null` list; otherwise use Common Set or another source set returned after excluding the mapping group’s own set | Yes |
| A cost-element mapping is created or updated | Error | resolve_source_cost_element_for_set | A Common Set source element is not resolved through the Common Set PROFIT_IN_INVENTORY finder, or a non-Common source/destination has conflicting type evidence | Use the PII finder for Common Set sources; otherwise resolve each element through its applicable set-specific lookup and stop on a type conflict | Yes |
| A default predefined component mapping is absent | Information | | The default component is unmapped | Show: The default cost component is unmapped. Define mapping for the default cost component to avoid cost processor errors. Do not block an otherwise valid package. | Yes |
| A retry is prepared from a previously accepted row | Error | | The retry substitutes a generic material element or loses a resolved source, destination, display, type, or flag value | Preserve the accepted template-compatible values and reject a substitute that is not valid for the source mapping type | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_accessible_set | Before preview of a mapping group create request | Confirmed accessible SetName | ora_reference_lookups.md |
| read_mapping_group | Before parent update or delete | isUsedInCostProfile | ora_reference_lookups.md |
| check_capitalization_control | Before changing CapitalizationFlag | isUsedinCTC | ora_reference_lookups.md |
| validate_destination_set_scope | Before creating or updating a child mapping | ComponentMappingGroupSetId, DestSetName | ora_reference_lookups.md |
| validate_cost_element_source_set_scope | Before creating or updating a cost-element mapping | ComponentMappingGroupSetId, SourceSetName | ora_reference_lookups.md |
| resolve_source_cost_element_for_set | Before creating or updating a cost-element mapping | SourceSetName, validated SourceSetId, SourceCostElementCode or Meaning, source type | ora_reference_lookups.md |
| read_predefined_component_mappings | Before a non-default child mapping create, for readiness information only | Default predefined mapping indicator | ora_reference_lookups.md |
| resolve_profit_in_inventory_element | Before a PII-specific source or destination validation | Element side, set ID, CostElementCode, CostElementId | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCM.DESIGN_ENFORCEMENT | step | 50 | design_enforcement | compliant->CCM.EXECUTION_GATE;blocked->RETURN_ISSUES | CCM.DEPENDENCY_READINESS | stop | A mapping-group create request has passed input and dependency checks |
