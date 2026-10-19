# Payroll Flow Patterns Design Enforcement

## Functional Knowledge Summary

Payroll flow patterns define reusable orchestration for automatic payroll processes, reports, and manual verification tasks. A submitted flow is an instance of a predefined or user-defined pattern. User-defined patterns can be created from scratch or copied from delivered patterns; delivered patterns aren't edited in place. The pattern owns task composition, activity and task-group presentation, owners, notifications, Process after Error behavior, the directed task sequence, parameters and bindings, connector rules, and security context.

Flow and task parameters must be designed together. Display behavior, format, usage, sequence, and any supplied basis or basis value determine what the submitter enters, what Fusion derives, and how one task passes output to another. Parameter Basis and Basis Value are optional. Positive Number and UCM formats carry specific validation and file-upload semantics. Smart LOV behavior depends on configured lookup type PAY_FLOWPARAMETER_VO.

Flow connectors persist reusable consolidation rules on the pattern, whereas linked flows are selected during flow submission. Task Flow connector status is required when connected-flow results must contribute to processing; Parameters Only doesn't provide that result-consolidation behavior. Flow sequencing must account for tasks that lock earlier payroll results. Multilingual user-defined names are maintained after migration through the Translation Editor.

The public flowPatterns REST resource supports read-only discovery and payroll-flow submission. It does not publish the writable setup schema for ProcessFlows. All Payroll Flow Patterns setup mutations must therefore use core.data-loader with current registered ProcessFlows metadata; direct REST setup mutation is prohibited.

## Source Basis

- https://docs.oracle.com/en/cloud/saas/human-resources/faupf/payroll-flow-patterns.html
- https://docs.oracle.com/en/cloud/saas/human-resources/faupf/flow-pattern-components.html
- https://docs.oracle.com/en/cloud/saas/human-resources/faupf/flow-pattern-parameters.html
- https://docs.oracle.com/en/cloud/saas/human-resources/faupf/positive-number-validation-for-check-numbers.html
- https://docs.oracle.com/en/cloud/saas/human-resources/faupf/flow-submission-support-for-ucm-file-upload.html
- https://docs.oracle.com/en/cloud/saas/human-resources/faupf/sequencing-rules-for-flows-and-locked-tasks.html
- https://docs.oracle.com/en/cloud/saas/human-resources/faupf/traslate-payroll-flow-names.html
- https://docs.oracle.com/en/cloud/saas/human-resources/faupf/considerations-to-create-a-flow-pattern.html
- https://docs.oracle.com/en/cloud/saas/human-resources/faupf/examples-of-editing-flow-patterns.html
- https://docs.oracle.com/en/cloud/saas/human-resources/faupf/examples-of-adding-a-new-parameter-to-a-payroll-flow.html
- https://docs.oracle.com/en/cloud/saas/human-resources/faupf/how-to-create-a-smart-list-of-values-for-a-flow-parameter.html
- https://docs.oracle.com/en/cloud/saas/human-resources/faupf/considerations-to-configure-flow-connectors.html
- https://docs.oracle.com/en/cloud/saas/human-resources/faupf/examples-of-flow-pattern-connectors-and-rules.html
- https://docs.oracle.com/en/cloud/saas/human-resources/faupf/options-to-link-flows.html
- https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-flow-patterns.html

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm supported operation | Keep the request within user-defined pattern create, copy, update, and validation scope |
| 2 | Resolve writable metadata | Retrieve current ProcessFlows Data Loader metadata and key fields |
| 3 | Validate composition | Confirm requested tasks, activities, owners, and error-continuation choices; do not require Start Flow, End Flow, or a complete task sequence because REST manages them |
| 4 | Validate parameter design | Confirm display, format, usage, and any supplied binding, basis, basis value, lookup, and value-set behavior |
| 5 | Validate connectors and security | Confirm connector semantics, exact connected flows, LDG scope, and access |
| 6 | Build Data Loader preview | Prepare an immutable core Data Loader artifact and require its normal approval gate before import |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any setup mutation is requested | Error | inspect_process_flows_metadata | A direct REST setup write, hand-authored payload, or non-Data Loader route is proposed | Use core.data-loader with ProcessFlows and current generated metadata | Yes |
| A delivered pattern is selected | Error | find_payroll_flow_pattern_by_exact_name | The request edits the delivered pattern in place | Copy and rename the delivered pattern, then modify the user-defined copy | Yes |
| A flow composition is prepared | Error | inspect_process_flows_metadata | A requested task or composition attribute isn't supported by current ProcessFlows metadata | Correct the requested composition; do not require Start Flow, End Flow, or a complete task sequence because REST manages task association and sequencing | Yes |
| Process after Error is enabled | Error |  | The continuation is not an explicit business decision or bypasses a required manual checkpoint | Disable it or document the intended continuation and recovery behavior | Yes |
| Tasks use results of earlier payroll processing | Error |  | The sequence ignores documented locks or permits corrective action while a downstream task holds a lock | Reorder or roll back the locking process according to the documented payroll flow | Yes |
| A parameter depends on another parameter | Error | inspect_process_flows_metadata | A supplied basis or basis value references an absent source | Correct the supplied binding and validate it against current metadata; do not require Parameter Basis or Basis Value when absent | Yes |
| Check-number parameters are configured | Error |  | Start or End Check Number isn't Positive Number format or accepts non-whole-number content | Use Positive Number format and reject decimals, letters, special characters, and comma separators | Yes |
| UCM display format is configured | Error |  | The flow isn't an upload flow or the parameter isn't intended to carry the generated UCM Content ID | Restrict UCM format to data-upload flows and map the generated content ID | Yes |
| Smart LOV is configured | Error | inspect_process_flows_metadata | The lookup isn't an enabled PAY_FLOWPARAMETER_VO code or doesn't return the intended value object | Complete and verify the common lookup before preview | Yes |
| Connected flows are configured | Error | find_payroll_flow_pattern_by_exact_name | Connector Status is Parameters Only, a connected pattern is unresolved, same-LDG rules fail, or required security is absent | Use Task Flow and verified accessible connector names | Yes |
| A Flow record is prepared | Error | resolve_connector_status | Connector Status is absent or invalid | Supply mandatory Connector Status at flow level; derive DefaultFlowFlag from Connector Status and Flow Status and do not pass Flow Status in the Flow payload | Yes |
| A flow is linked during submission | Error |  | Pattern-level connector behavior is incorrectly modeled as a submission-time linked flow, or two in-progress flows are combined | Keep reusable connector rules on the pattern; link only supported completed or insertable flows during submission | Yes |
| Translated names are required | Error |  | Translation is attempted before migration or a user-defined flow lacks needed installed-language translations | Migrate first, then translate the flow name and optional description in the destination | Yes |
| A new task parameter was delivered after a user-defined pattern was created | Error |  | The parameter is assumed to appear automatically | Remove and re-add the affected task or create a fresh copy of the delivered pattern, then restore sequence and parameter design | Yes |
| An import artifact is prepared | Error | inspect_process_flows_metadata | Any column, key, type, requiredness, association, or operation support is inferred from UI wording or public read-side REST attributes | Map only current registered ProcessFlows metadata | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| inspect_process_flows_metadata | Every mapping, preview, create, copy, or update | Current supported columns, key fields, types, lengths, requiredness, operation support, and parent-child associations | ora_reference_lookups.md |
| resolve_connector_status | Every Flow record | One valid mandatory Connector Status code and meaning | ora_reference_lookups.md |
| find_payroll_flow_pattern_by_exact_name | Existing-pattern update, delivered-pattern copy, reuse comparison, or connector selection | Exact current business identity, LDG context, status, base-flow context, and connector context | ora_reference_lookups.md |
| find_payroll_flow_pattern_by_id | Complete current parent and parameter comparison | Current parent and flowParameters children | ora_reference_lookups.md |
| list_payroll_flow_patterns_by_ldg | LDG-scoped selection or connector design | Complete authorized pattern choices for the LDG | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PFP.ENFORCE_DESIGN | decision | 50 | design_enforcement | passed->PFP.EXECUTION_GATE;blocked->PFP.HANDLE_ERROR | PFP.APPLY_DEFAULTS | stop | Before a ProcessFlows Data Loader preview or import artifact is treated as ready |
