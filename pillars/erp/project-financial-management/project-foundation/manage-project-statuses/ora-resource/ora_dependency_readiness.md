# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Scope/baseline | Resolve target/task and current identity coverage, including seed exclusions |
| 2 | Capabilities/defaults | Check separate create/edit permissions; resolve create controls under the selected policy or inherited progress weight |
| 3 | Lifecycle/workflow/use | Resolve supplied requested targets; distinguish missing required targets from deferred downstream checks |
| 4 | Package/approval | Verify native template, proposed field/child diff, loader semantics and approved immutable checksum |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PSTATUS.SCOPE | Task/target | Yes | Every request | Verify | Catalog/context | verify_project_status_scope | Prevent cross-target work | Supply target | Scope |
| PSTATUS.IDENTITIES | Current names and stored codes | Yes | Create/update or named lifecycle/workflow targets | Lookup | Complete current same-target identity response | lookup_project_status_identities | Native export omits stored status codes and may exclude unmodified seeds | Use declared read-only LOV route; do not ask consultants to obtain codes from UI | Identity/code map and pagination scope |
| PSTATUS.BASELINE | Current status and child rows | Yes | Create/update/import | Lookup | Native export joined to the current identity map | find_project_status | Prevent unintended creates and preserve child collections | Obtain baseline through selected export workflow and disclose excluded seeds | Baseline, identity coverage |
| PSTATUS.CAP | Object/classification and field capabilities | Yes | Every write | Lookup | Task-local catalogs | resolve_status_capabilities | Separate creation from editing | Provide requested intent and fields | Canonical pair and editability |
| PSTATUS.CONTROLS | Project controls and basis | Conditional | PROJECT creation or controls supplied | Lookup | Exact current classification rows, or documented standard source rows for PROJECT create under prefer-current-else-standard | resolve_status_controls | Materialize explicit controls without confusing Allow and EnabledFlag; disclose unverified inheritance | Use the local create resolver; exact-inheritance and existing updates still need current values | Controls, policy, basis, inheritance verification and warnings |
| PSTATUS.WEIGHT | Inherited progress weight | Conditional | PROGRESS creation | Lookup | Supplied classification status | resolve_progress_weight | Preserve classification-derived reporting behavior | Supply verified inherited weight | Weight |
| PSTATUS.GRAPH | Lifecycle mode, native bridges, workflow targets and use findings | Conditional | Behavior changes | Lookup | Current identity/code map, local classification catalog and native graph evidence | resolve_status_graph | Prevent wrong S/U domains, missing child rows and guessed workflow codes | Resolve exact targets; unavailable bridge or required code blocks; downstream checks may be deferred | Stored codes, child keys, graph and warnings |
| PSTATUS.PACKAGE | FSM native and mutation contract | Yes | Import | Verify | Target template and exact package | verify_project_status_package | Loader safety | Preserve metadata, headers, field mapping and checksum | Contract |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required dependencies ready | Yes, within selected workflow and approval |
| Missing required evidence | Identity coverage, defaults unresolved under selected policy, requested target or template absent | No for affected write; read-only guidance can continue |
| Incomplete downstream graph evidence | Mappings beyond resolved requested targets are absent | Yes; disclose as deferred to Fusion validation, never passed |
| Conflict | Duplicate object/name, incompatible requested target or proven workflow recursion | No |
| Unsupported operation | Protected field, missing S-mode native bridge, direct setup REST, rename, delete, clear or child-removal contract unverified | No for that operation; disclose the exact object/classification and missing mechanism |
| Standard-source configuration | PROJECT create under prefer-current-else-standard with exact classification identity resolved but source parent excluded from export | Prepare explicit standard rows and disclose controls_basis=standard_source / inheritance_verified=false in the approved preview; do not mark current default parity passed |
| Workflow gap | Exact-inheritance PROJECT create lacks current classification controls and no declared lookup is available | Stop affected create; retain valid input and identify the missing read contract as catalog_or_metadata_mismatch. Do not make UI access or custom-status selection a consultant prerequisite |
| Warning | Ordinary lifecycle cycle or UI use warning | Preview with explicit disclosure; not an invented product refusal |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PSTATUS.RESOLVE_DEPENDENCIES | step | 7 | resolve_dependency | ready->PSTATUS.ENFORCE_DESIGN;missing->PSTATUS.RETURN_ISSUES;conflict->PSTATUS.RETURN_REFUSAL | PSTATUS.ROUTE_OPERATION | stop | Resolve only dependencies for the selected operation; whole-task export does not require status fixtures |
