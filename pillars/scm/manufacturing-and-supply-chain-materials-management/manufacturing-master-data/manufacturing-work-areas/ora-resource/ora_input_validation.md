# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Task identity | Manufacturing Work Areas and ORA_REDWOOD_MANUFACTURING_WORK_AREAS | Stop | Select the matching Setup and Maintenance task. | Every request | |
| Existing inventory organization | Target organization code that can be confirmed in Fusion | Stop | Resolve it with `verify_inventory_organization` before preparing a work-area request. | Every request | verify_inventory_organization |
| Work-area creation values | Work Area Name and Work Area Code; Inactive Date is optional | Stop before source preparation | Provide Name and Code; correct Inactive Date when supplied. | Creating a work area | |
| FSM setup-data artifact | FSM export or import source accepted by the core Data Loader workflow | Stop before import | Prepare and validate the source through core.data-loader; do not invent an FSM file layout from this guidance. | Before FSM import | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The task identity, inventory organization, applicable creation values, and Data Loader source are supplied | Satisfied | Continue to reference lookup, dependency, and design checks. | verify_inventory_organization |
| The target plant cannot be identified or confirmed, or required creation values are absent | Blocked | Correct the request before preparing an FSM artifact. | |
| The FSM artifact is absent or has not passed core.data-loader validation | Blocked | Prepare or correct the source through core.data-loader. | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Existing organization | Accept the request only when `verify_inventory_organization` returns exactly one organization. | Every request | verify_inventory_organization |
| Work Area Name and Code | Require both values for a create request. | Creating a work area | |
| Inactive Date | Allow blank; when supplied, require a date later than the current date. | Creating or updating a work area | |
| FSM contract | Use only the source structure accepted by core.data-loader and the selected FSM workflow. | Before import | |
| Import operation | Keep create, edit, and delete intent explicit; do not infer an operation or claim an undocumented FSM action is supported. | Every request | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WA.VALIDATE | step | 1 | validate_input | ok->WA.DEPENDENCIES;failure->WA.FAILED | none | stop | Every Manufacturing Work Areas request |
