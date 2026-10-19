# Payroll Flow Patterns Defaulting Rules

## Source Basis

- Oracle Help Center, Flow Pattern Components: https://docs.oracle.com/en/cloud/saas/human-resources/faupf/flow-pattern-components.html
- Oracle Help Center, Flow Pattern Parameters: https://docs.oracle.com/en/cloud/saas/human-resources/faupf/flow-pattern-parameters.html
- Oracle Help Center, Considerations to Configure Flow Connectors: https://docs.oracle.com/en/cloud/saas/human-resources/faupf/considerations-to-configure-flow-connectors.html
- Oracle REST API for Oracle Fusion Cloud HCM, Get all flow patterns: https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-flowpatterns-get.html
- Developer-provided FSCR DAT generation workflow received 22 September 2026 defines create-operation constants, temporary identifiers, and object-level defaults for processFlows DAT generation.
- Developer-provided FSCR Payroll Flow Patterns instruction received 25 September 2026 defines Flow Status to DefaultFlowFlag derivation and object-operation values.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| LDG Required | Yes | A new pattern is prepared and the developer has not explicitly selected global availability; confirm the current ProcessFlows representation before writing | No | inspect_process_flows_metadata |
| Connector Name | Flow Pattern name | A connector name is omitted and the pattern participates in connector rules | No | inspect_process_flows_metadata |
| Flow Status | Active | Flow Status isn't supplied as business input; do not include it in the Flow payload | No | derive_default_flow_flag |
| Schedule | As soon as possible | No explicit schedule is supplied | No | inspect_process_flows_metadata |
| OPERATION | CREATE | A new Flow, FlowTask, or FlowParameter record is created | No |  |
| OPERATION | UPDATE | An existing Flow, FlowTask, or FlowParameter record is updated | No |  |
| OPERATION | DELETE | An existing Flow, FlowTask, or FlowParameter record is deleted | No |  |
| Flow.FlowId | 101 | The single Flow record is generated | No |  |
| FlowTask.BaseFlowId | 101 | Every FlowTask record is generated | No |  |
| FlowParameter.BaseFlowId | 101 | Every FlowParameter record is generated | No |  |
| FlowTask.FlowTaskId | Start at 201 and increment by one | FlowTask records are generated in request order | No |  |
| FlowParameter.FlowParameterId | Start at 301 and increment by one | FlowParameter records are generated in request order | No |  |
| Flow.LdgRqdFlag | Y | The user does not supply LdgRqdFlag in a DAT create request | No |  |
| Flow.DefaultFlowFlag | Y | Flow Status is Active and mandatory Connector Status is Parameters Only | No | derive_default_flow_flag |
| Flow.DefaultFlowFlag | N | Flow Status is Active and mandatory Connector Status is Task Flow | No | derive_default_flow_flag |
| Flow.DefaultFlowFlag | H | Flow Status is Hidden | No | derive_default_flow_flag |
| Flow.DefaultFlowFlag | I | Flow Status is Inactive | No | derive_default_flow_flag |
| FlowTask.IgnorePreReq | Y | The user does not supply IgnorePreReq | No |  |
| FlowTask.VerifyFlag | N | The user does not supply VerifyFlag | No |  |
| FlowParameter.ContextParamFlag | N | The user does not supply ContextParamFlag | No |  |
| FlowParameter.DisplayFlag | Y | The user does not supply DisplayFlag | No |  |
| FlowParameter.ParamUsageType | INPUT | The user does not supply ParamUsageType | No |  |

Do not default mandatory Connector Status, task composition, Process after Error, flow or task parameter values, parameter bindings, owners, notifications, translations, connected flows, or Smart LOV selections. Those values express business behavior and require explicit source-backed input. Parameter Basis and Basis Value remain optional and are not defaulted.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PFP.APPLY_DEFAULTS | step | 40 | apply_default | applied->PFP.ENFORCE_DESIGN;not_applicable->PFP.ENFORCE_DESIGN;blocked->PFP.HANDLE_ERROR | PFP.CHECK_DEPENDENCIES | stop | Apply only documented defaults after required inputs and dependencies are resolved |
