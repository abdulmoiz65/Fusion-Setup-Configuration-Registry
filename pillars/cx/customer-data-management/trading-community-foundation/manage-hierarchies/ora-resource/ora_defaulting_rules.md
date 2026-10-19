# Defaulting Rules

Default read presentation and job routing. Never derive an import mode from
supplied CSV content.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| read_operation | list | The user asks to list or show hierarchies without naming a technical read operation | No; preserve explicit describe, inventory, hierarchy_detail, versions, nodes, or full_read | read_ui_aligned_hierarchy_inventory |
| as_of_date | Current date in the configured environment's execution context | read_operation=list and the user does not supply an as-of date | No; preserve a valid explicit ISO date and always disclose the effective date used | read_ui_aligned_hierarchy_inventory |
| ImportMode | CREATE_RECORD | The user supplies a Hierarchy or HierarchyNode CSV and asks to import without choosing create-only, create-or-update, or delete | No; preserve an explicit CREATE_ONLY, CREATE_RECORD, or DELETE_RECORD choice | |
| high-volume | YES | Every Hierarchy or HierarchyNode CX Import activity | No | |

An explicit literal delete is not defaulted: normalize it to `DELETE_RECORD`
and delegate immutable preview, approval, submission, and Fusion result handling
to `Import Trading Community Data`.

Do not silently default an explicit request for all headers, raw inventory,
inactive/future/expired hierarchies, or empty hierarchies to `list`; route that
request to `inventory` and state that no version or node eligibility filter was
applied.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MH.DEFAULT_READ_OPERATION | step | 2 | apply_default | resolved->MH.READ_HIERARCHY;unresolved->MH.ERROR | MH.VALIDATE_REQUEST | stop | Preserve a supported explicit read operation or default an unqualified list or show request to list with a disclosed as-of date |
| MH.DEFAULT_IMPORT_MODE | step | 3 | apply_default | resolved->MH.ROUTE_CX_IMPORT;unresolved->MH.ERROR | MH.VALIDATE_REQUEST | stop | A supplied hierarchy import is requested |
