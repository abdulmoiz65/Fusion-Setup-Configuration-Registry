# Payroll Flow Patterns Input Validation

## Source Basis

- Oracle Help Center, Introduction to Payroll Flow Patterns: https://docs.oracle.com/en/cloud/saas/human-resources/faupf/payroll-flow-patterns.html
- Oracle Help Center, Flow Pattern Components: https://docs.oracle.com/en/cloud/saas/human-resources/faupf/flow-pattern-components.html
- Oracle Help Center, Flow Pattern Parameters: https://docs.oracle.com/en/cloud/saas/human-resources/faupf/flow-pattern-parameters.html
- Oracle Help Center, Positive Number Validation for Check Numbers: https://docs.oracle.com/en/cloud/saas/human-resources/faupf/positive-number-validation-for-check-numbers.html
- Oracle Help Center, Flow Submission Support for UCM File Upload: https://docs.oracle.com/en/cloud/saas/human-resources/faupf/flow-submission-support-for-ucm-file-upload.html
- Oracle Help Center, Considerations to Create a Flow Pattern: https://docs.oracle.com/en/cloud/saas/human-resources/faupf/considerations-to-create-a-flow-pattern.html
- Oracle REST API for Oracle Fusion Cloud HCM, Flow Patterns REST endpoints and response metadata: https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-flow-patterns.html
- Developer instruction received 16 September 2026: all setup mutations use core Data Loader with registered business object ProcessFlows.
- Developer instruction received 22 September 2026: reference and List of Values inputs must resolve names or display values to exactly one valid code or ID before create, update, or import; valid supplied codes or IDs are reused without an additional lookup.
- Developer-provided FSCR DAT generation workflow received 22 September 2026 defines the create-only processFlows, Flow, FlowTask, and FlowParameter input and validation contract.
- Developer-provided FSCR REST instruction received 22 September 2026 defines the payrollFlowPatterns describe endpoint and the findByFilterCriteria finder inputs.
- Developer-provided FSCR Payroll Flow Patterns instruction received 25 September 2026 defines mandatory Connector Status, Flow Status to DefaultFlowFlag derivation, object-operation values, and REST-managed task sequencing.
- Developer instruction received 7 October 2026: keep ProcessFlows as the registered business object name, but use processFlows for the top-level DAT discriminator and processFlows.dat for the DAT filename.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Create, copy, or update a user-defined payroll flow pattern; validation-only request | Block artifact preparation | Ask for one exact business operation | Every request |  |
| Flow pattern identity | Exact Flow Pattern name; exact current FlowId retained privately for an existing pattern | Block update and exact-match validation | Resolve the exact name through the read-only flow-pattern lookup; never infer an update target from a similar name | Update or copy | find_payroll_flow_pattern_by_exact_name |
| Basic information | Flow Pattern name, Description when required, Connector Status, LDG Required choice, and Legislative Data Group when the design is LDG-specific | Block preview | Request the missing business-facing values; derive Flow Status and DefaultFlowFlag from Connector Status under the documented derivation rule | Create, copy, or update | inspect_process_flows_metadata |
| Flow composition | Requested activities, task groups, automatic or manual tasks, owners, notification choices, and Process after Error behavior | Do not block | Preserve supplied composition and ownership choices when present; do not require owner, notification, or Process after Error choices solely to create a FlowTask | Create, copy, or structural update | inspect_process_flows_metadata |
| Task sequence | Optional task-order, concurrency, or join details when the caller needs to express them | Do not block | Do not require a complete task sequence, Start Flow, End Flow, or following-task relationships; the REST service manages task association and sequencing | Create, copy, or task-sequence update | inspect_process_flows_metadata |
| Flow and task parameters | Parameter name, display option, display format, usage, and sequence; Parameter Basis, Basis Value, and lookup or value-set selection only when supplied or needed by the design | Block only the affected supplied parameter | Supply every required business value; do not require Parameter Basis or Basis Value when neither is supplied | A parameter is added or changed | inspect_process_flows_metadata |
| Connector design | Mandatory Connector Status; Connector Name and exact connected flow patterns when connector rules are configured | Block preview | Supply Connector Status at flow level and resolve connected-flow details only when configured | Create, copy, or update | find_payroll_flow_pattern_by_exact_name |
| Translation plan | Installed languages, translated flow names, and optional translated descriptions | Keep translation outside the initial import | Migrate the flow first, then maintain translations in the destination by the documented Translation Editor workflow | User-defined or overridden flow names require multilingual search |  |
| Mutation artifact route | Current ProcessFlows Data Loader sample, attribute-details workbook, key-fields workbook, and immutable validated import artifact | Block preview | Generate current metadata and the sample through core.data-loader; do not hand-author a direct REST mutation payload | Create, copy, or update | inspect_process_flows_metadata |
| Reference or LOV identity | A valid code or ID; or a reference name or display value with a documented field-specific resolver | Block the affected create, update, or import row | Use the field-specific read-only resolver in ora_reference_lookups.md; do not place an unresolved name in a code or ID field | Any create, update, or import containing a reference or LOV attribute |  |
| DAT create scope | Exactly one Flow and zero or more requested FlowTask and FlowParameter records | Block DAT generation | Request the missing Flow details or reject a request containing more than one Flow | The processFlows DAT generation workflow is invoked |  |
| Flow record attributes | OPERATION, FlowId, FlowName, BaseFlowName, LdgRqdFlag, mandatory Connector Status, and derived DefaultFlowFlag; LegislativeDataGroupId when LdgRqdFlag is Y; Description only when supplied | Return a validation error and no partial DAT content | Supply Connector Status, derive DefaultFlowFlag from it and Flow Status, and resolve LegislativeDataGroupId when required | A Flow record is generated | resolve_legislative_data_group_by_exact_name |
| FlowTask record attributes | OPERATION and the current metadata-required identifiers and fields | Return a validation error and no partial DAT content | Derive or resolve only fields required by the current ProcessFlows metadata | Each requested FlowTask record | resolve_base_task_id |
| FlowParameter record attributes | OPERATION and the current metadata-required identifiers and fields; Parameter Basis and Basis Value are optional | Return a validation error and no partial DAT content | Do not require Parameter Basis or Basis Value unless the supplied design uses them; resolve every supplied reference value | Each requested FlowParameter record | inspect_process_flows_metadata |
| payrollFlowPatterns describe metadata | One complete describe response containing every returned attribute and finder definition with data type, requiredness, validation, accepted values, format, length restriction, reference or LOV dependency, finder name, and finder attributes | Block metadata-backed validation and field documentation | Retrieve the supplied payrollFlowPatterns describe endpoint and retain the complete response contract | Before the payrollFlowPatterns collection or finder response is interpreted | inspect_payroll_flow_patterns_describe |
| findByFilterCriteria finder inputs | LegislativeDataGroupId; optional FlowName searchText | Block the finder request when LegislativeDataGroupId is absent | Supply the target LDG ID; add FlowName only when search text is provided | GET payrollFlowPatterns through findByFilterCriteria | list_payroll_flow_patterns_by_filter |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A predefined pattern is selected for modification | Direct editing is not permitted | Copy the delivered pattern, rename the copy, and apply changes only to the user-defined copy | find_payroll_flow_pattern_by_exact_name |
| LDG Required restricts the pattern to an LDG | Require an exact authorized LDG context and legislation | Resolve the target context before preparing the import artifact | inspect_process_flows_metadata |
| A task parameter is bound to another flow or task parameter | Require the source parameter to exist and be available before the dependent parameter | Correct parameter sequence and binding before preview | inspect_process_flows_metadata |
| A connector references another flow | Require one exact accessible connected pattern; connected predefined flows must be in the same LDG | Resolve the connected pattern and verify required flow security | find_payroll_flow_pattern_by_exact_name |
| A flow parameter uses a Smart LOV | Require an enabled lookup code under lookup type PAY_FLOWPARAMETER_VO and the intended value-object mapping | Complete the prerequisite lookup configuration before import | inspect_process_flows_metadata |
| The import schema or key semantics differ from the current ProcessFlows metadata | The artifact is stale or unsupported | Regenerate the Data Loader sample and remap source data before preview | inspect_process_flows_metadata |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Flow Pattern name is absent | Block the row and request a business-facing name | Create or copy |  |
| A predefined flow is targeted for an in-place edit | Reject the operation and require a user-defined copy | Update | find_payroll_flow_pattern_by_exact_name |
| Connector Status is absent | Reject the Flow record because Connector Status is mandatory at flow level | Create or update | resolve_connector_status |
| Flow Status and Connector Status are available | Do not pass Flow Status in the Flow payload. Default missing Flow Status to Active and derive DefaultFlowFlag: Parameters Only plus Active = Y; Task Flow plus Active = N; Hidden = H; Inactive = I | Create or update | derive_default_flow_flag |
| LDG Required is supplied | Accept only a current value confirmed by ProcessFlows metadata; do not equate the public read-side codes Y, B, and N with writable loader values without metadata confirmation | Create or update | inspect_process_flows_metadata |
| Display is supplied for a parameter | Require the intended behavior: Mandatory, optional display, or hidden-derived value | Parameter maintenance | inspect_process_flows_metadata |
| Display Format is Positive Number | Require a non-decimal positive whole number with no letters, special characters, or comma separators | Start Check Number or End Check Number on a user-defined Generate Check Payments task |  |
| Display Format is UCM | Permit it only for a flow that uploads data; require the submitted value to be the UCM Content ID generated by the upload | File-upload flow parameter |  |
| Parameter sequence is supplied | Require each dependency source to have a lower sequence than the parameter that depends on it; hidden parameters are processed after required or dependent inputs | Parameter maintenance |  |
| Parameter Basis or Basis Value is supplied | Validate the supplied value against the design and current metadata. Do not require either attribute when it is not supplied | Parameter maintenance | inspect_process_flows_metadata |
| Process after Error is selected | Require an explicit business decision that subsequent processing may continue after the predecessor errors; never enable it implicitly | Task maintenance |  |
| A technical field is included in the Data Loader artifact | Require the field, operation support, requiredness, type, length, key role, and parent-child mapping to be present in the current ProcessFlows metadata | Every import artifact | inspect_process_flows_metadata |
| A direct REST create, update, or delete is proposed | Reject the route; prepare the change only through core.data-loader | Every mutation |  |
| OPERATION is populated | Require CREATE for a new record, UPDATE for an existing record update, and DELETE for an existing record deletion | Every Flow, FlowTask, and FlowParameter record |  |
| DAT top-level identity is prepared | Require processFlows as the top-level business object discriminator and processFlows.dat as the DAT filename; reject ProcessFlows in either case-sensitive position | Every Payroll Flow Patterns DAT artifact | inspect_process_flows_metadata |
| DAT object hierarchy differs from one Flow parent with FlowTask and FlowParameter children | Reject the request and report the invalid object relationship | processFlows DAT generation |  |
| DAT output contains an attribute absent from current business-object metadata | Reject the attribute and block generation until the current ProcessFlows metadata supports it | Every generated Flow, FlowTask, and FlowParameter record | inspect_process_flows_metadata |
| DAT scalar value is not a string | Reject the value unless current ProcessFlows metadata explicitly requires another data type | Every generated attribute | inspect_process_flows_metadata |
| FlowId or a child BaseFlowId differs from 101 | Reject generation; FlowId and every child BaseFlowId must be the string 101 | DAT create request |  |
| FlowTaskId allocation is invalid | Reject generation unless IDs are unique strings beginning at 201 and incrementing by one in request order | One or more FlowTask records are requested |  |
| FlowParameterId allocation is invalid | Reject generation unless IDs are unique strings beginning at 301 and incrementing by one in request order | One or more FlowParameter records are requested |  |
| BaseFlowName, BaseFlowTaskName, or BaseFlowParameterName is generated | Trim the corresponding name, convert all characters to uppercase, replace each sequence of one or more spaces with one underscore, and reject any derived value that differs | A Flow, FlowTask, or FlowParameter record is generated |  |
| LdgRqdFlag, DefaultFlowFlag, IgnorePreReq, VerifyFlag, ContextParamFlag, or DisplayFlag is populated | Accept only Y or N | The applicable object is generated |  |
| ParamDispType or ParamUsageType is populated | Require a value supported by current ProcessFlows business-object metadata | A FlowParameter record is generated | inspect_process_flows_metadata |
| ParamSequence is populated | Require a numeric value that is unique among all FlowParameter records in the same Flow | A FlowParameter record is generated |  |
| LegislativeDataGroupId is absent or unresolved while LdgRqdFlag is Y | Return a validation error and generate no partial DAT content | A Flow record is generated with LdgRqdFlag Y | resolve_legislative_data_group_by_exact_name |
| DAT validation succeeds | Return only the JSON DAT object with Flow, FlowTask, and FlowParameter arrays; include no Markdown, explanations, comments, or unsupported attributes | processFlows DAT generation |  |
| payrollFlowPatterns attribute metadata is absent from the describe response | Treat the attribute contract as undocumented; do not infer its data type, requiredness, accepted values, format, length, or reference or LOV dependency | REST metadata capture or response validation | inspect_payroll_flow_patterns_describe |
| A finder name or finder attribute is absent from the describe response | Reject its use as undocumented until a complete describe response confirms it | Any payrollFlowPatterns finder invocation | inspect_payroll_flow_patterns_describe |
| findByFilterCriteria is invoked without LegislativeDataGroupId | Block the request and ask for ldgId | GET payrollFlowPatterns | list_payroll_flow_patterns_by_filter |
| FlowName searchText is absent | Invoke findByFilterCriteria with LegislativeDataGroupId only; do not invent a FlowName filter | GET payrollFlowPatterns | list_payroll_flow_patterns_by_filter |
| Display Type is Value Set and Lookup is supplied | Require exactly one exact ValueSetCode match from the documented module-scoped valueSets endpoint and place ValueSetCode in Lookup | FlowParameter create, update, or import | resolve_flow_parameter_value_set_lookup |

## Business-to-REST Mapping Requirements

The public flowPatterns REST resource is a read and submission model, not the writable setup contract for ProcessFlows. Use these attributes for read-only comparison only. Resolve every writable Data Loader column from current registered metadata.

| Business Concept | Public Read-Side Attribute | Public Contract | Writable ProcessFlows Mapping |
|---|---|---|---|
| Flow pattern name | FlowPattern | Required, read only, maximum length 250 | Resolve from current ProcessFlows metadata |
| Description | Description | Read only, maximum length 250 | Resolve from current ProcessFlows metadata |
| Flow identifier | FlowId | Read-only integer identifier | Use only as current metadata permits; never invent |
| Base flow | BaseFlowId and BaseFlowName | Read-only inheritance identity | Resolve copy semantics from current ProcessFlows metadata |
| Flow status | FlowStatus | Do not pass in the Flow payload; default to Active when absent and derive DefaultFlowFlag with Connector Status | Use the documented DefaultFlowFlag derivation; verify writable columns against current ProcessFlows metadata |
| LDG requirement | LDGRequired | Read-only values Y, B, and N; documented default Y | Resolve writable value from current ProcessFlows metadata |
| Legislative context | LegislativeDataGroupId and LegislationCode | LDG identifier and country code | Resolve key and validation rules from current ProcessFlows metadata |
| Connector | ConnectorName and ConnectorStatus | Read-only connector tag and connector behavior | Resolve writable attributes from current ProcessFlows metadata |
| Flow parameter | FlowParameter and BaseFlowParameterName | Display name and base parameter code | Resolve parent-child columns and keys from current ProcessFlows metadata |
| Parameter presentation | Display and DisplayFormat | Display values Y, M, N; documented formats include date, lists, number, text, UCM, and value set | Resolve loader values from current ProcessFlows metadata |
| Parameter derivation | ParameterBasis and BasisValue | Binding type and its associated source or constant | Resolve loader values and dependency keys from current ProcessFlows metadata |
| Parameter order and direction | Sequence and Usage | UI processing order and input/output usage | Resolve loader values from current ProcessFlows metadata |
| Tasks, activities, owners, notifications, and sequence graph | Not exposed by the cited flowPatterns response schema | Functional behavior is documented in Payroll Flow Patterns pages | Resolve child objects, keys, and associations from current ProcessFlows metadata |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PFP.VALIDATE_INPUT | decision | 10 | validate_input | passed->PFP.RESOLVE_REFERENCES;missing->PFP.HANDLE_ERROR;invalid->PFP.HANDLE_ERROR | none | stop | Every Payroll Flow Patterns request before lookup, dependency resolution, or artifact preparation |
