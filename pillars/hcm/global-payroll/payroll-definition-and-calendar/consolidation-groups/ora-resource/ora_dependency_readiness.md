# Consolidation Groups Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Operation contract | Route Create and Update to HCM Data Loader; keep Search, Read One, and status monitoring read-only; stop unsupported Delete and FSM requests. |
| 2 | Legislative Data Group | Establish exactly one accessible LDG, use its exact returned Name for HDL, and preserve its Fusion ID and LegislationCode for read scope. |
| 3 | Create duplicate preflight | Before preparing or submitting Create, query the complete LDG-scoped collection and reject any exact Code or Name duplicate. |
| 4 | Update record identity | For Update, establish a user key or Fusion surrogate ID confirmed by target View Business Objects metadata. |
| 5 | Target business-object metadata | Confirm the target release when Update, Delete, or a shape outside the documented create MERGE contract is requested. |
| 6 | Authorization | Require authentication, appropriate functional access, Data Exchange or HDL access, and LDG data security. |
| 7 | Preview and approval | Before any upload or submission, show the archive shape, operation, key strategy, LDG reference, fields, business effect, and unresolved risks. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| legislative_data_group_id | Accessible Legislative Data Group by Fusion ID | Conditional | Search, Read One, Create, Update, or Payroll Definition reference selection receives LegislativeDataGroupId | Lookup | Supplied LegislativeDataGroupId | verify_legislative_data_group_by_id | Consolidation Groups are LDG-scoped and HDL uses the LDG user-key name | Provide the exact accessible LDG ID | LegislativeDataGroupName: Name; LegislativeDataGroupId: LegislativeDataGroupId; LegislationCode: LegislationCode |
| legislative_data_group_name | Accessible Legislative Data Group by exact name | Conditional | An LDG name is supplied instead of an ID | Lookup | Supplied exact LDG name and optional LegislationCode | find_legislative_data_group_by_exact_name | HDL requires the exact accessible LDG Name and access is security-dependent | Provide an exact name and legislation code when needed to disambiguate | LegislativeDataGroupName: Name; LegislativeDataGroupId: LegislativeDataGroupId; LegislationCode: LegislationCode |
| create_duplicate_identity | New Consolidation Group or Consolidation Set duplicate preflight | Yes | Create is prepared or submitted | Lookup | Resolved LegislativeDataGroupId, proposed ConsolidationSetCode, and proposed ConsolidationSetName | check_consolidation_group_duplicate_by_ldg | Name and Code are business identities that must be unique within the exact LDG before a new group is created | Provide one resolved LDG and both proposed values | DuplicatePreflight or existing ConsolidationSetId, Name, Code, LDG, and audit fields |
| target_hdl_metadata | Target Payroll Consolidation Group metadata | Conditional | Update, Delete, or a shape outside the documented create MERGE example is requested | Blocked | Target-environment View Business Objects export | | The supplied source doesn't include the target metadata needed to confirm update keys, additional actions, or additional attribute shapes | Export Payroll Consolidation Group metadata and supply the relevant action and attribute rows | Supported actions, required attributes, key hints, lengths, CLOB rules |
| hdl_create_contract | HCM Data Loader Create contract | Conditional | Create uses the documented MERGE shape | Satisfied | Developer-provided working DAT and cited Oracle guidance | | HCM Data Loader is the required mutation route and the verified user-key shape omits explicit integration keys | Prepare PayrollConsolidationGroup.dat with Name, exact LegislativeDataGroupName, Code, and optional ClobFiles content | Business object, file name, MERGE action, ConsolidationSetName, LegislativeDataGroupName, ConsolidationSetCode, optional Comments, archive shape |
| consolidation_group_search | LDG-scoped group collection | Conditional | Search is requested | Lookup | Resolved LegislativeDataGroupId and optional SearchTerm | search_consolidation_groups_by_ldg | The verified search contract is an internal read-only App UI collection | Provide LDG scope and optional keyword | Rows and paging state |
| existing_group_identity | Existing Consolidation Group | Conditional | Read One or Update precheck is requested | Lookup | Resolved LegislativeDataGroupId and ConsolidationSetId | find_consolidation_group_by_id_in_ldg | No dedicated read-one endpoint was confirmed and Update must preserve existing identity and Code | Provide the LDG and exact group ID; for Update, confirm the usable key through View Business Objects | ID, Name, Code, Comments, audit values, LDG ID |
| payroll_definition_group_reference | Eligible Payroll Definition group choices | Conditional | A group is selected in the Payroll Definition UI | Lookup | Resolved LegislativeDataGroupId and optional search text | list_consolidation_group_payroll_references_by_ldg | Generic Code is the selected ID and Meaning is display text | Select one returned pair | Code, Meaning, selected ConsolidationSetId mapping |
| hdl_data_set_status | HDL data-set status | Conditional | Monitor Load is requested | Lookup | Loader RequestId | get_hdl_data_set_status | Upload or submission success does not prove import and load completion | Provide the request ID and wait for terminal status | Data-set transfer, import, and load status |
| hdl_business_object_status | PayrollConsolidationGroup loader status | Conditional | Monitor Load is requested | Lookup | Loader RequestId | list_hdl_business_object_statuses | Task success depends on the target business object's terminal result | Review the PayrollConsolidationGroup child status and counts | Business-object import and load status, counts |
| hdl_data_set_messages | HDL data-set messages | Conditional | Monitor Load is requested or a loader phase fails | Lookup | Loader RequestId | list_hdl_data_set_messages | Record-specific messages are required for safe correction | Review and retain sanitized confirmed messages | Business-object and record message context |
| authorized_loader_access | Authorized HDL execution access | Conditional | A live upload, submission, or load is requested | Blocked | Target user authentication, privileges, Data Exchange or HDL access, and LDG data security | | This authoring resource does not establish credentials or grant mutation authority | Establish authorized access in the target environment before handoff to the loader workflow | Authorized environment and permitted business-object scope |
| delete_contract | Supported loader Delete action and keys | Conditional | Delete is requested | Unsupported | Target View Business Objects metadata was not supplied | | Delete support and its key contract are unconfirmed | Do not execute Delete until target metadata confirms the action and keys | Unsupported Delete operation |
| fsm_task_contract | Task-specific FSM import or export | Conditional | FSM Import or FSM Export is requested | Unsupported | General FSM guidance only | | No task-specific action, schema, keys, scope, status, or error contract was confirmed | Use HDL for supported Create or Update, or supply a verified FSM contract | Unsupported FSM operation |
| internal_mutation_contract | Internal Redwood mutation service | Conditional | payrollGeneric Create, Update, or Delete is requested | Unsupported | Developer-provided source explicitly prohibits this route | | Internal UI services are not the supported mutation mechanism | Use HCM Data Loader for supported Create or Update | Unsupported internal mutation |
| public_crud_contract | Dedicated supported public Consolidation Group CRUD | Conditional | Public REST CRUD is requested | Unsupported | No dedicated public resource was found in the supplied evidence | | The internal payrollGeneric service must not be presented as public CRUD | Use the documented HDL route or supply a supported public contract | Unsupported public CRUD |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Direct supplied evidence establishes the dependency within the documented scope | Continue; no dependency lookup or create is needed. |
| Lookup | A named read-only resolver must return one accessible result or a complete status collection | Run the documented lookup only; do not create related setup. |
| Blocked | Required target metadata, access, preview, approval, or safe key representation is missing | No; resolve the blocker first. |
| Unsupported | Supplied evidence does not establish the requested operation contract | No; stop without inventing behavior. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CG.RESOLVE_DEPENDENCIES | decision | 2 | resolve_dependency | ready->CG.RESOLVE_REFERENCES;blocked->CG.HANDLE_ERROR;unsupported->CG.HANDLE_ERROR | CG.VALIDATE_INPUT | stop | Validated request |

## Sources

- Developer-provided ConsolidationGroups.md, updated and reviewed 2026-08-13.
- Oracle Fusion Cloud HCM, How Data Is Loaded Using HCM Data Loader: https://docs.oracle.com/en/cloud/saas/human-resources/fahdl/how-data-is-loaded-using-hcm-data-loader.html
- Oracle Fusion Cloud HCM, Example of Loading Payroll Consolidation Group: https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/example-of-loading-payroll-consolidation-group.html
- Oracle Fusion Cloud HCM, Supported Key Types: https://docs.oracle.com/en/cloud/saas/human-resources/fahdl/supported-key-types.html
