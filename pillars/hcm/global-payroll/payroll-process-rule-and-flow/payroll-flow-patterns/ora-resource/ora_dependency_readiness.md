# Payroll Flow Patterns Dependency Readiness

## Source Basis

- Oracle Help Center, Considerations to Create a Flow Pattern: https://docs.oracle.com/en/cloud/saas/human-resources/faupf/considerations-to-create-a-flow-pattern.html
- Oracle Help Center, Flow Pattern Components: https://docs.oracle.com/en/cloud/saas/human-resources/faupf/flow-pattern-components.html
- Oracle Help Center, Flow Pattern Parameters: https://docs.oracle.com/en/cloud/saas/human-resources/faupf/flow-pattern-parameters.html
- Oracle Help Center, How to Create a Smart List of Values for a Flow Parameter: https://docs.oracle.com/en/cloud/saas/human-resources/faupf/how-to-create-a-smart-list-of-values-for-a-flow-parameter.html
- Oracle Help Center, Considerations to Configure Flow Connectors: https://docs.oracle.com/en/cloud/saas/human-resources/faupf/considerations-to-configure-flow-connectors.html
- Developer-provided FSCR DAT generation workflow received 22 September 2026 defines parent-child identity, LDG, base-task, and parameter-reference readiness requirements.
- Developer-provided FSCR REST instruction received 22 September 2026 requires payrollFlowPatterns describe metadata before collection attributes or finders are treated as documented.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | ProcessFlows metadata | Retrieve the current registered Data Loader attributes, key fields, supported operations, and parent-child associations before mapping source data |
| 2 | Target pattern identity | Establish create candidacy or resolve exactly one existing user-defined pattern; copy a delivered pattern before modification |
| 3 | Legislative context and security | Confirm the intended LDG or global availability and the user's functional and data access for the pattern and any connected flows |
| 4 | Delivered task and process definitions | Confirm every automatic, report, and manual task used by the flow is available in the target context |
| 5 | Parameter reference setup | When Parameter Basis or Basis Value is supplied, confirm referenced lookups, value sets, Smart LOV definitions, and source flow or task parameters exist before dependent parameters; neither field is mandatory |
| 6 | Connected flow patterns | Resolve each connected pattern exactly and verify same-LDG and security requirements where applicable |
| 7 | DAT parent-child identity | Assign FlowId 101, link every FlowTask and FlowParameter through BaseFlowId 101, and verify unique child IDs before generation |
| 8 | payrollFlowPatterns REST metadata | Retrieve the complete describe response before interpreting collection fields, validations, references, finders, or finder attributes |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| process_flows_metadata | Registered ProcessFlows contract | Yes | Any mapping, preview, create, copy, or update | Lookup | Current core Data Loader metadata and generated sample | inspect_process_flows_metadata | Public functional documentation doesn't define the writable loader schema | Regenerate the ProcessFlows sample and metadata workbooks before mapping or import | Supported columns, keys, operations, types, lengths, requiredness, and associations |
| target_flow_pattern | Exact target payroll flow pattern | Conditional | Update, copy, connector selection, or reuse comparison | Lookup | Read-only flowPatterns result | find_payroll_flow_pattern_by_exact_name | Prevents creating against or changing the wrong flow pattern | Provide the exact displayed Flow Pattern name and LDG when names are not unique | Current parent identity and business configuration |
| legislative_context | Legislative Data Group and legislation | Conditional | LDG Required restricts the pattern or localized tasks are used | Verify | Supplied LDG context and current Fusion pattern results | list_payroll_flow_patterns_by_ldg | Flow availability, delivered content, security, and connector eligibility can be LDG-specific | Provide the target LDG and confirm access | Authorized LDG-scoped pattern choices and legislation |
| delivered_tasks | Available flow tasks and processes | Yes | Tasks are added or replaced | Blocked | Current ProcessFlows metadata plus target Fusion task availability; exact provider contract is not published in the supplied sources | inspect_process_flows_metadata | A pattern can contain only available automatic, report, and manual tasks | Resolve every task through current metadata before preview | Task identities, task action support, and associations |
| parameter_references | Lookup, value set, Smart LOV, flow parameter, task parameter, or context source | Conditional | A supplied Parameter Basis or Basis Value derives or validates a parameter value from another source | Verify | Current ProcessFlows metadata and existing referenced setup | inspect_process_flows_metadata | A supplied parameter source must be valid; Parameter Basis and Basis Value aren't mandatory | Complete the referenced setup only when the supplied design uses it | Lookup or value-set identity, source parameter, binding type, and basis value |
| connected_flows | Exact connected flow patterns | Conditional | Connector rules are configured | Lookup | Authorized read-only flowPatterns results | find_payroll_flow_pattern_by_exact_name | Connector rules automatically control which results are consolidated at run time | Provide every exact Connector Name and flow-pattern selection | Connected pattern identity and connector context |
| dat_legislative_data_group | Legislative Data Group identity | Conditional | Flow LdgRqdFlag is Y or a FlowParameter supplies Legislative Data Group | Lookup | User-supplied LDG name or valid ID | resolve_legislative_data_group_by_exact_name | The DAT must contain a resolved LegislativeDataGroupId and must not fabricate it | Provide the exact Legislative Data Group name when the ID is not supplied | LegislativeDataGroupId and LegislationCode |
| dat_base_task | Base task identity | Conditional | One or more FlowTask records are requested | Lookup | User-supplied task business value | resolve_base_task_id | Every generated FlowTask requires a resolved BaseTaskId | Provide the exact task value accepted by the documented task lookup | BaseTaskId |
| dat_parameter_lookup | Flow-parameter lookup identity | Conditional | ParamLookup is supplied by name or display value | Lookup | User-supplied lookup name or display value | resolve_flow_parameter_lookup | ParamLookup must use the documented response code or ID | Provide the exact lookup display name | ParamLookup |
| dat_parameter_value_set_lookup | Value Set Lookup identity | Conditional | Display Type is Value Set and Lookup is supplied by name or display value | Lookup | User-supplied Lookup value | resolve_flow_parameter_value_set_lookup | The Lookup field must use the documented ValueSetCode | Provide the exact ValueSetCode used as the Lookup name or display value | Lookup |
| dat_parent_child_links | Flow child foreign-key relationship | Yes | Any FlowTask or FlowParameter is generated | Satisfied | DAT generation rules set the single Flow FlowId and each child BaseFlowId to the string 101 |  | Prevents orphaned or cross-flow child records | Do not override generated parent or child linkage identifiers | FlowId and BaseFlowId |
| payroll_flow_patterns_describe | payrollFlowPatterns REST attribute and finder metadata | Yes | The payrollFlowPatterns collection or findByFilterCriteria finder is used | Lookup | GET payrollFlowPatterns describe response | inspect_payroll_flow_patterns_describe | Returned fields, types, requiredness, validations, formats, lengths, reference dependencies, finders, and finder attributes must not be inferred | Capture one complete authorized describe response before documenting or validating the collection | Complete attribute and finder contract |
| payroll_flow_patterns_filter | LDG-scoped Payroll Flow Patterns collection | Conditional | Payroll Flow Patterns are queried by LDG | Lookup | LegislativeDataGroupId and optional FlowName searchText | list_payroll_flow_patterns_by_filter | The finder requires an LDG and may be narrowed by FlowName | Supply the target ldgId and optional searchText | Complete authorized collection result |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The dependency is explicitly supplied and verified against current metadata or Fusion state | No further lookup is required |
| Lookup | A documented read-only resolver can determine the dependency | Yes, read-only lookup only |
| Verify | A supplied dependency must be confirmed before preview | Yes, read-only verification only |
| Blocked | The dependency is missing, ambiguous, unauthorized, or lacks a published resolver contract | No; request the missing business value or current metadata |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PFP.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | ready->PFP.APPLY_DEFAULTS;blocked->PFP.HANDLE_ERROR | PFP.RESOLVE_REFERENCES | stop | After applicable read-only lookups and ProcessFlows metadata resolution |
