# Configure Legislations for Human Resources Readiness

This file owns task identity and execution prerequisites, not filter logic,
HTTP requests, or approval. Evaluate each mandatory dependency only at its declared stage; business
selection precedes dependent lookups. A metadata mismatch cannot be waived by choosing a different task.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Task identity and executable rules | Read core/fusion-dev/fusionapps-resource-authoring/references/ora-resource-task-node-execution-guide.md, the enclosing manifest, ora_rule_registry.json, the validated execution plan, and every reachable source anchor in the six ora_* Markdown resources; resolve them to the intended Human Resources task |
| 2 | Selected operation | The invoking workflow explicitly selects Search, Create, Delete, or Verify Delete for this task |
| 3 | Environment and client readiness | The configured environment and restBaseUrl match the selected workflow, and the governed client can authenticate; the lookup resource path is already declared by the skill |
| 4 | Create legislation selection | Complete resolve_available_legislation_for_create before any rule-specific lookup; this is shared context for all Create sections |
| 5 | Create rule values | Resolve live rule/currency/mapping candidates, apply omissions, validate required business inputs and return prepared logical values |
| 6 | Load or verification context | Task Hook receives Data Loader's final preflight and archive; Verify Delete receives the successful load outcome and its original selection context |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CLHR-IDENTITY | Human Resources task manifest and route | Yes | Manifest, registry, or invoking task does not identify PAY_CONFIGURE_LEGISLATIONS_FOR_HUMAN_RESOURCES / Configure Legislations for Human Resources; or the selected Delete route lacks dataloader_import_mode=REST and businessObject=deleteInstalledLegislation | Blocked | Enclosing manifest, compiled registry, and selected workflow compared with the effective setup-task catalog | | Nested compilation and Task Hook must use this exact task rather than Payroll | Correct the owning metadata or selected context and recompile; do not relabel only the registry | Confirmed task identity and selected route |
| CLHR-RULE-PLAN | Validated task graph and source anchors | Yes | The execution guide or a reachable source anchor is unread, the planner does not return planned with readiness ready, or the registry differs from its source tables | Blocked | Standard compiler and build_rule_execution_plan.py for this nested task | | A compiled graph alone does not satisfy environment, authentication, or proxy prerequisites | Load the execution guide and owning resources, validate the current graph without overrides, and evaluate the runtime dependencies | Validated plan and loaded source anchors |
| CLHR-WORKFLOW | Selected governed operation | Yes | No active workflow has selected this task and the requested operation | Blocked | Invoking workflow's selected task and the operation/intent rules in ora_input_validation.md | | An endpoint or source capture is evidence, not a workflow | Reach the selected operation through router.implementation-router before invoking its resolver | Selected task, operation, execution_intent, and phase |
| CLHR-PROJECT | Active project for durable artifacts | Yes | Durable Create/Delete preparation or task-run persistence has no selected project workspace | Blocked | Router project context and core.project-mgmt.project-workspace-initializer | | Prepared files and selection evidence must remain bound to their implementation project | Have the owning project workflow initialize draft-impl-project-<YYYY-MM-DD> from project/_template when needed and inform the user before resuming; keep configuration and credentials out of artifacts | Active project and safe task artifact location |
| CLHR-RUNBOOK | Active Run Book before loader submission | Yes | The owning workflow is routing a Fusion mutation but project runbook_control.status is not active | Blocked | Router Initial Run Book Gate and core.runbook | | Task readiness cannot bypass the project's submission prerequisites | Return to the owning project/Run Book workflow; local DAT preparation alone does not grant submission authorization | Active Run Book context before submission |
| CLHR-ENVIRONMENT | Configured Fusion environment | Yes | Configured environment identity or restBaseUrl is missing, invalid, or inconsistent with the selected workflow | Blocked | Selected environment configuration validated by the core authentication and REST-client skills | | Requests must target the configured environment; the skill already owns the fixed lookup path | Resolve the actual environment configuration issue; do not ask the user for a collection path, resource version, or browser-captured route | Validated environment identity and configured restBaseUrl host |
| CLHR-AUTH | Governed client readiness | Yes | Governed authentication is unavailable or required resource access is rejected | Blocked | core.fusion-api.rest-api-client, core.auth.fusion-oauth-authentication, and core.data-loader for approved loads | | Lookups require read access to installed legislations; an approved load requires Data Loader, UCM upload, and legislation deletion privileges | Resolve authentication or authorization through the selected core workflow; never copy cookies or credentials from a capture | Client authentication/access outcome without secret values |
| CLHR-PREFLIGHT | Task Hook's final archive | Yes | phase=validate_artifact and Data Loader preflight, its matching immutable archive, or original target/environment context is missing or inconsistent | Blocked | core.data-loader persisted preflight and selected task context | | Task rules must validate the same bytes that will be approved and uploaded | Return to Data Loader source validation before Task Hook; do not construct an envelope by hand | Final artifact and matching preflight |
| CLHR-VERIFY-CONTEXT | Previous deletion outcome | Yes | Verify Delete lacks successful load status with zero failures, exact original code, or the same confirmed environment and read-access context | Blocked | core.data-loader status workflow and retained deletion selection | | An accepted initiation or a different visibility context cannot prove deletion | Obtain the requested status and original selection first; if visibility cannot be confirmed, report verification as inconclusive | Successful load and original target/environment binding |
| CLHR-CREATE-SELECTION | Available legislation | Yes | First Create business step, before dependent rules | Lookup | Live available-legislation collection in selected environment | resolve_available_legislation_for_create | A supplied country name/code is not sufficient authority | Select one returned legislation; supplied exact identity is reused | Shared selection and eligibility evidence |
| CLHR-CREATE-RULE | Payroll Relationship Rule choices | Yes | After selected legCode for normal preparation or requested payroll-rule options | Lookup | Current rule choices | resolve_payroll_relationship_rule | Explicit rule and omission candidate must exist | Choose a current Meaning or allow documented omission default | Valid rule/default candidate |
| CLHR-CREATE-TRU | Deduction Card TRU choices | Yes | After selected legCode for normal preparation or requested TRU options | Lookup | Current TRU choices | resolve_deduction_card_tru_rule | Required user choice has no default | Choose a current Meaning | Valid TRU choice or options |
| CLHR-CREATE-CURRENCY | Default currency candidate | Conditional | Normal preparation after selection when no override supplied; not options-only | Lookup | Selected legislation default | resolve_default_currency | Do not infer currency from geography | Resolve the sole default candidate | Default currency candidate |
| CLHR-CREATE-CURRENCY-OVERRIDE | Currency choices | Conditional | Explicit currency input or request for options | Lookup | Current currency choices | resolve_currency_override | Explicit values must be validated | Select an exact current code/name | Valid override or options |
| CLHR-CREATE-MAPPINGS | Default mapping candidates | Conditional | Normal preparation with mapping omitted or edits starting from defaults; not options-only | Lookup | Current default relationship mappings | resolve_default_relationship_mappings | Do not hardcode environment-specific IDs | Use defaults or provide row edits | Ordered default candidates |
| CLHR-CREATE-PERSON-TYPES | System Person Type choices | Conditional | Changed/new person-type value or request for options | Lookup | Current selected-legislation choices | resolve_system_person_type_options | Default crosswalk is not an allowlist | Choose a live person-type label/code | Valid per-row person code |
| CLHR-CREATE-RELATIONSHIP-TYPES | Payroll Relationship Type choices | Conditional | Changed/new relationship-type value or request for options | Lookup | Current selected-legislation choices | resolve_payroll_relationship_type_options | IDs and Process in Payroll come from one live row | Choose a live relationship-type label | Valid per-row relationship ID and read-only flag |

These stage dependencies execute in the Create branch, not in the common
pre-lookup readiness node. Missing required user values are collected after
selection and option discovery. An active Run Book or loader artifact is not
a prerequisite for this explicitly scoped read-only preparation stage.

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Correct task identity and all applicable mandatory dependencies are satisfied | Declared lookups only; mutations remain owned by Data Loader |
| Task identity blocker | Manifest or registry identifies another task or lacks the selected route | No |
| Workflow blocker | Caller has not reached the selected operation | No |
| Rule-plan blocker | Required execution guide/source anchors are missing or the current graph is not planned and ready | No |
| Project or Run Book blocker | The applicable project artifact or mutation-submission prerequisite is unmet | No |
| Environment blocker | Configured environment identity or restBaseUrl is missing, invalid, or inconsistent with the selected workflow | No |
| Auth/authz blocker | Governed authentication or resource access is unavailable | No |
| Artifact or verification context blocker | Applicable preflight or successful-load context is missing or inconsistent | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CLHR.CHECK_READINESS | step | 2 | resolve_dependency | ready->CLHR.SELECT_OPERATION;blocked->CLHR.ERROR | CLHR.VALIDATE_INPUT | stop | Every request; evaluate only applicable prerequisites without making external calls |
