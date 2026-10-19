# Job Requisition Descriptive Flexfields Dependency Readiness

Confirm exact task context, target identity, fresh-export evidence for read-only inspection, supported FSM routing, reference authority, and change approval before handing work to validation or import workflows.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Exact task and catalog route | Confirm the Job Requisition Descriptive Flexfields task, Recruiting Configuration ownership, positive task sequence, CSV support, and FSM import mode |
| 2 | Fresh read-only segment export | For Inspect or list, use shared.setup-export.task-level-export for the exact task and selected environment; require downloaded FileContent and successful extraction |
| 3 | Exact exported DFF and scope | Resolve exactly one DFF root from the export and retain only the requested Global or named context rows |
| 4 | LOV or value-set authority | For a configuration change that specifies an LOV or value set, resolve the supplied reference through its authoritative contract |
| 5 | Mutation artifact and approval | For a mutation, validate the immutable FSM archive and bind explicit approval to its exact preview through Core Data Loader immediately before submission |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| exact_task_preflight | Exact task, offering, functional area, sequence, CSV support, and FSM route | Yes | Every request | Blocked until the generated task metadata and effective catalog match exactly | Generated task skill and effective catalog | | Prevents a generic Common DFF, another Recruiting task, or alternate transport from being substituted | Use the exact Job Requisition Descriptive Flexfields task under Recruiting Configuration | Task code; task name; offering; functional area; positive task sequence; catalog flags; import mode |
| segment_retrieval_export | Fresh downloaded task CSV segment export | Yes | Inspect or list current segments | Blocked until shared.setup-export.task-level-export downloads and extracts valid FileContent for the exact task and selected environment | Current exact-task CSV export | | Provides authoritative current segment rows without a direct DFF or REST read | Start one fresh exact-task export, download FileContent, and validate the ZIP before listing rows | Process ID; archive identity; extraction state; exported DFF root; segment rows |
| dff_target_identity | Exact exported DFF and requested scope | Yes | Every supported request | Satisfied only when exactly one DFF root and the requested scope resolve without substitution | Fresh exact-task export for Inspect; approved request for a change | | Prevents ambiguous or inferred DFF, context, or segment selection | For Inspect, use the exported DFF root and requested Global or named context scope; require a segment identity only for single-segment work | Requested operation; exact flexfield identity; scope; optional segment identity |
| dff_lov_value_set_contract | LOV or value-set authority | Conditional | A configuration change specifies an LOV or value set | Lookup | Approved reference contract | resolve_dff_reference_authority | Prevents use of an inferred value-set identifier or mapping | Supply the authoritative source, match rule, requested fields, and value mapping | Confirmed source; match rule; requested fields; value mapping |
| fsm_csv_route | Supported CSV and FSM route | Yes | Export or import | Satisfied only when the task flags and FSM import mode are confirmed | Generated task skill and effective catalog | | Prevents an alternate export or import path | Use task-level CSV export or Core Data Loader FSM import as applicable | Export/import capability |
| immutable_import_artifact | Validated immutable FSM CSV ZIP | Yes | Import or approved change submission | Blocked until the exact archive is validated and its bytes and checksum are frozen | Core Data Loader lifecycle | | Prevents an unvalidated or changed package from reaching Fusion | Validate and preview the exact archive through Core Data Loader | Archive path; task identity; package members; checksum |
| mutation_approval | Preview and explicit approval | Conditional | Before a mutation | APPROVAL_REQUIRED until approval is bound to the exact preview | Core Data Loader lifecycle | | Prevents an unapproved or stale mutation | Review the exact target and delta, then approve immediately before execution | Preview fingerprint; approval evidence |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| READY | Every applicable task, target, route, lookup, artifact, and approval requirement is satisfied | Only the selected workflow may continue |
| MISSING | A required operation, identity, scope, artifact, or approval is absent | No |
| BLOCKED | Catalog, lookup-contract, workflow, or verification readiness is unresolved | No |
| UNSUPPORTED | Another task, generic DFF task, alternate route, unrelated attribute, inferred context, or inferred segment is requested | No |
| AUTHORIZATION | Required Fusion task or Data Loader access is absent | No |
| APPROVAL_REQUIRED | A mutation lacks approval bound to the exact current preview | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JOB_REQ_DFF.RESOLVE_REFERENCES | step | 20 | resolve_dependency | resolved->JOB_REQ_DFF.CHECK_READINESS;missing->JOB_REQ_DFF.RETURN_ISSUES;ambiguous->JOB_REQ_DFF.RETURN_ISSUES;unsupported->JOB_REQ_DFF.RETURN_ISSUES | JOB_REQ_DFF.VALIDATE_INPUT | stop | Every supported request |
| JOB_REQ_DFF.CHECK_READINESS | decision | 30 | resolve_dependency | ready->JOB_REQ_DFF.ENFORCE_DESIGN;missing->JOB_REQ_DFF.RETURN_ISSUES;blocked->JOB_REQ_DFF.RETURN_ISSUES;authorization->JOB_REQ_DFF.RETURN_ISSUES;unsupported->JOB_REQ_DFF.RETURN_ISSUES | JOB_REQ_DFF.RESOLVE_REFERENCES | stop | Every supported request |
