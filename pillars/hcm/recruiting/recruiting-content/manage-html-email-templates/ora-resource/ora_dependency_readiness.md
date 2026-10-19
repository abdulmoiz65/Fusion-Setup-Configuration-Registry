# Manage HTML Email Templates Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Authorized FSM task route | The selected operator and task-level FSM export or FSM import route must be available for the target environment. |
| 2 | Cross-environment archive handling choice | For a supplied cross-environment archive, compare parent MessageDesignCode values with a fresh target task-level FSM export. When both existing and new templates are present, require Replace existing templates or Import only new templates before preview. This does not apply to an individual create generated solely from a documented template mapping. |
| 3 | Dependent CSV baseline | When the user omits dependent CSV files for an individual create, use the selected Basic, Blank, or MultiColumn Complete UI-Created Baseline Mapping row to generate both dependent CSV files. |
| 4 | Immutable package review | The exact archive must pass validation, retain its reviewed SHA-256, and receive current approval before initiation. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| het_authorized_route | Authorized FSM task route | Yes | Task-level export or FSM import | Satisfied | Selected shared.setup-export.task-level-export or core.data-loader executor and target environment | | The supported FSM route must be available before an external operation. | Stop and use an authorized operator or route when access is unavailable. | None |
| het_target_identity | Cross-environment archive handling choice | Yes | FSM import of a supplied cross-environment archive | Satisfied | Fresh target task-level FSM export and explicit user choice | | Prevents accidental replacement or accidental omission in a cross-environment package. | Show the complete Existing template names list and New template names list. Then choose Replace existing templates or Import only new templates. | Existing template names; new template names; selected handling |
| het_dependent_csv_baseline | Complete dependent CSV baseline | Yes | FSM import when dependent CSV files are not provided | Satisfied | Selected Complete UI-Created Baseline Mapping row in ora_defaulting_rules.md | | A proper complete design-metadata structure is required for the imported template design. | Copy the selected Basic, Blank, or MultiColumn metadata unchanged from the documented mapping; set the parent code to MessageDesignCode and set TypeCode from the selected Campaign Purpose or Email Type mapping. | Complete metadata CSV; complete type CSV |
| het_supplied_dependent_csv | Supplied dependent CSV payload | Yes | FSM import when dependent CSV files are provided | Satisfied | User-provided metadata and type CSV files | | Supplied data must not be silently replaced. | Validate the supplied dependent files against the parent MessageDesignCode and selected template scope. | Matching metadata and type rows |
| het_current_approval | Current immutable preview approval | Yes | FSM import | Satisfied | User confirmation after exact preview | | FSM import mutates Fusion configuration. | Review target, operation, and immutable archive immediately before action. | Approval record; SHA-256 for import |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required evidence, selected route, and current approval are present | Continue through the declared workflow only |
| Blocked | Access, identity, complete design, preview, or approval is absent | No |
| Auth or authz | The selected operator cannot access the task or routed operation | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HET.CHECK_DEPENDENCIES | decision | 20 | resolve_dependency | ready->HET.APPLY_DEFAULTS;blocked->HET.HANDLE_ERROR | HET.VALIDATE_INPUT | stop | After input validation |
