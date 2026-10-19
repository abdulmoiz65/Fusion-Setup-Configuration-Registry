# Cost Component Mapping Groups Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Accessible set | Confirm that the mapping group SetName is a set the user can manage |
| 2 | Resolved workbook values | Resolve parent, source, destination, display, type, and flag values before creating the workbook; use the required SetId and RestAction from the generated template |
| 3 | Mapping group and children | For a master-details create, prepare the parent and all requested child mappings in one validated workbook using the parent surrogate keys; for a child-only change, identify the existing parent by ComponentGroupId |
| 4 | Component-code mappings | Validate predefined and landed cost component mappings against the parent set and link them to a new parent through `ComponentGroupCode` and `SetName`, or to an existing parent by ComponentGroupId |
| 5 | Cost-element mappings | Validate source-to-destination cost element mappings and link them through the same new-parent surrogate keys, or to an existing parent by ComponentGroupId |
| 6 | ComponentSource-error fallback | After the documented ComponentSource-missing dataset failure is reconciled, prepare a fresh parent-update package, a predefined-component child package, and a combined landed-cost plus cost-element child package. Initiate and verify the parent first; after its success, the two independently approved child packages may be initiated in parallel. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| accessible_set | Mapping group set choice | Yes | Creating a mapping group | Lookup | Costing sets LOV matching the UI selector | resolve_accessible_set | Mapping groups are defined at set level; the selected name must be available in the current UI choice list | Select exactly one returned SetName; Fusion validates final authorization on POST | Confirmed SetId, SetName |
| parent_mapping_group | Parent mapping-group identity | Yes | Creating component-code or component-element child mappings | Satisfied | Existing parent response, or the new parent row's `ComponentGroupCode` and `SetName` | | A child-only change requires ComponentGroupId; a master-details create uses the template's parent surrogate keys | For a new parent, retain blank child ComponentGroupId and populate the exact parent ComponentGroupCode and SetName; otherwise retain the existing ComponentGroupId | ComponentGroupId or ComponentGroupCode and SetName |
| existing_landed_cost_mapping | Duplicate landed-cost mapping preflight | Yes | Before a landed-cost-management Data Loader import | Lookup | Read-only child mapping lookup | check_existing_landed_cost_mapping | A returned row means the mapping already exists | Do not submit the package when the preflight returns a row | Existing mapping indicator |
| existing_predefined_component_mapping | Duplicate predefined component mapping preflight | Yes | Before a predefined component Data Loader import | Lookup | Read-only child mapping lookup | check_existing_predefined_component_mapping | A returned row means the predefined source component is already mapped | Do not submit the package when the preflight returns a row | Existing mapping indicator |
| existing_cost_element_mapping | Duplicate cost-element mapping preflight | Yes | Before a cost-element Data Loader import | Lookup | Read-only child mapping lookup | check_existing_cost_element_mapping | A returned row means the source-to-destination element mapping already exists | Do not submit the package when the preflight returns a row | Existing mapping indicator |
| default_predefined_component_mapping | Default cost component mapping | No — advisory | Before any non-default child row, after a mapping-group result, and after parent create | Lookup | Predefined child mapping read | check_default_predefined_component_mapping | A default component should be mapped to avoid cost processor errors | Show the default-component message; do not block an otherwise valid package | Default predefined mapping indicator |
| capitalization_editability | CapitalizationFlag editability | Yes | Before changing CapitalizationFlag for a landed-cost-management mapping | Lookup | Read-only child mapping lookup | check_capitalization_control | A returned isUsedinCTC=Y row makes CapitalizationFlag read-only | Do not submit a capitalization change when the lookup returns a row | CapitalizationFlag editability |
| child_mapping_validation | Child-row validation | Yes | Preparing a master-details Data Loader package | Satisfied | Generated Data Loader workbook and current template validation | | The Data Loader package validates component-code and cost-element rows with their parent mapping group | Correct every invalid child row before generating the ZIP | Validated child rows |
| default_predefined_component_mapping | Default cost component mapping | No — advisory | Preparing a non-default child row | Satisfied | Generated Data Loader workbook | | A default component should be mapped to avoid cost processor errors | Show the default-component readiness message when the supplied workbook does not contain the default component; do not block an otherwise valid package | Default predefined mapping indicator |
| capitalization_editability | CapitalizationFlag editability | Yes | Preparing a landed-cost-management mapping row | Satisfied | Generated Data Loader workbook and current template validation | | CapitalizationFlag must comply with the template and the parent mapping context | Correct the row when template validation rejects the value | Validated CapitalizationFlag |
| cost_set_value | Cost set identity | Yes | A payload needs a set identifier or display value | Lookup | Costing sets LOV | resolve_cost_set | Set IDs and display values must be resolved before create or update | Select exactly one valid cost set | SetId, SetName |
| predefined_source_component | Predefined source component | Yes | Creating a predefined component mapping | Lookup | Cost components LOV | resolve_predefined_source_component | The source component must be active and unmapped for the selected group | Select exactly one active unmapped predefined component | SourceComponentCode, SourceCostComponentId, SourceSetName |
| landed_source_component | Landed-cost-management source component | Yes | Creating or updating a landed-cost-management mapping | Lookup | Cost components LOV | resolve_landed_cost_source_component | The source component must be active in the selected set | Select exactly one active landed-cost-management component | SourceComponentCode, SourceCostComponentId |
| destination_cost_element | Destination cost element | Yes | Creating or updating a mapping with a destination cost element | Lookup | Cost elements LOV | resolve_cost_element_for_set | The destination element must be eligible in the selected set | Select exactly one eligible cost element | CostElementCode, CostElementId |
| component_source_error_fallback | Three-request split fallback | Conditional | A combined child package was classified RECONCILED_PARTIAL for the exact ComponentSource-missing dataset message | Lookup | Completed Data Loader dataset diagnostic, submitted DAT, and exact child readback | reconcile_component_source_failure_effects | The observed service behavior requires independently executable, complete packages rather than a repeated combined-child request | Prepare three fresh immutable artifacts. Verify the parent request first, then submit the predefined child package and the combined landed-cost plus cost-element package only with their own approvals; those two child requests may run in parallel after parent success. | Parent update artifact, predefined child artifact, landed-cost and cost-element child artifact |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | The UI-selectable set and either an existing parent ComponentGroupId or a complete new-parent surrogate link are confirmed, and required Data Loader validation has passed | Yes, subject to the documented task execution contract |
| Blocked | The set cannot be resolved, a requested child mapping has neither an existing parent ID nor complete new-parent surrogate keys, a duplicate exists, or a required source or destination cannot be resolved | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCM.DEPENDENCY_READINESS | step | 40 | resolve_dependency | ready->CCM.DESIGN_ENFORCEMENT;blocked->RETURN_ISSUES | CCM.LOOKUP_ACCESSIBLE_SET | stop | A create request has completed the required set-access check |
