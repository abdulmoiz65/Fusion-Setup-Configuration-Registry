# Payroll Costing Value Sets Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Exact task package | Validate task identity, root business object, scope, all six CSV nodes, headers, and release before editing or importing |
| 2 | Target Payroll Costing module | Confirm an applicable target-environment ModuleId before authoring or modifying a root Value Set |
| 3 | Value Set parent and value references | Resolve Independent parents, target Value Set identity, and child-value parent references before authoring dependent structures or values |
| 4 | Security and protected status | Resolve applicable security-object and protection evidence before a security-related or any protected mutation |
| 5 | Table and View Object prerequisites | Validate a Table source before Table authoring; block Validation View Object authoring until its task contract is confirmed |
| 6 | Related Value Set prerequisites | Resolve two Independent members, all mappings, and pair orientation before enabling a new relationship |
| 7 | Cost Allocation KFF impact | Determine whether imported metadata or relationship changes affect a Cost Allocation KFF and retain redeployment verification when applicable |
| 8 | Shared FSM workflow outcomes | Require the declared shared export, validation, import, and post-import verification workflow results before reporting a completed setup operation |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PCVS.PACKAGE_CONTRACT | Exact task metadata and six-file package contract | Yes | Every package and task-level operation | Verify | Submitted package metadata and template evidence | inspect_task_csv_package_metadata | Prevents a package for another task, module, functional area, or business object from being used | Supply an exact task package with every CSV node retained, including header-only files | Task identity; root business object; module scope; release; file and header validation |
| PCVS.TARGET_MODULE | Applicable Payroll Costing ModuleId | Yes | Create or modify a root Value Set | Verify | Sanitized successful result from shared reference-data validation | verify_target_module_evidence | ModuleId is an environment and release-sensitive taxonomy identity, while moduleKey is the task scope | Provide target, release, ModuleId, and the passed validation evidence; do not copy the observed example blindly | ModuleId; target evidence reference |
| PCVS.PARENT_VALUE_SET | Independent parent and maintained-value parent | Conditional | Dependent, Subset, or child value authoring | Verify | Submitted rows and sanitized successful target-reference result | resolve_parent_value_set_reference | Dependent and Subset functional models rely on an Independent Value Set, and every child belongs to one parent | Provide a resolvable exact parent; import it in the package only when the confirmed contract supports that sequence | Parent ValueSetCode; IndependentValueSetCode; child-parent readiness |
| PCVS.SECURITY_PROTECTION | Security object and protected Value Set status | Conditional | SecurityEnabledFlag or DataSecurityObjectName is supplied, or an existing Value Set is modified | Verify | Sanitized successful target-reference result | verify_value_set_security_evidence | Protected Value Sets and their maintained values cannot be edited; security references need target evidence | Provide the protection and security validation result; stop a prohibited mutation | Protection status; security readiness |
| PCVS.TABLE_SOURCE | Table-validation source metadata | Conditional | Table validation is requested | Verify | Submitted validation-table row and sanitized successful reference-data result | verify_table_validation_source_evidence | Table validation relies on a valid source, columns, and optional restriction metadata | Validate the proposed source through the declared shared workflow; do not invent SQL or aliases | Table-source readiness; parent association |
| PCVS.RELATED_PAIR | Related Value Set members and mappings | Conditional | A relationship or mapping is created, updated, enabled, or disabled | Verify | Submitted related-set rows and sanitized successful target-reference result | resolve_related_value_pair | Payroll relationships require two Independent Value Sets; mappings must be complete before enabling a new relationship | Provide the exact pair, mappings, and orientation evidence; leave a new relationship disabled until ready | Resolved pair; mapping readiness; enable readiness |
| PCVS.KFF_REDEPLOYMENT | Affected Cost Allocation KFF redeployment result | Conditional | Imported Value Set metadata or related-set changes affect a Value Set used by a Cost Allocation KFF | Verify | Sanitized post-import verification result from the declared shared workflow | | Value Set imports can affect flexfield deployment and Payroll requires successful redeployment after related-set changes | Retain the affected KFF identity and a successful redeployment result before claiming completion | Affected KFF; redeployment result |
| PCVS.SHARED_WORKFLOW_RESULTS | Task-level FSM export, validation, import, and post-import results | Yes | A task-level export or import is requested | Verify | Sanitized records from shared.setup-export.task-level-export, shared.validation.setup-data-validator, shared.validation.reference-data-validator, and core.data-loader | | This resource supplies task knowledge; the shared skills own generic transport, import, approval, and process handling | Run the declared shared workflow and retain each sanitized result in the operation record | Dependency result; import process result; post-import verification result |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Every applicable dependency has one passed evidence result | Yes, evidence inspection only; generic execution remains with the declared shared workflow |
| Blocked | Required metadata, target evidence, parent, mapping, protection result, or KFF result is absent or fails | No |
| Not applicable | A conditional validation model, security feature, relationship, or KFF impact is not part of the request | No lookup needed |
| Unsupported | The request requires an unconfirmed stored code, View Object contract, delete behavior, direct REST mutation, alternate import, XML, HDL, or transactional costing | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| PCVS.CHECK_DEPENDENCIES | decision | 2 | resolve_dependency | ready->PCVS.ENFORCE_TASK_BOUNDARY;blocked->PCVS.FAILED | PCVS.VALIDATE_PACKAGE | stop | Every task-level CSV package, authoring, import, or verification request | |
