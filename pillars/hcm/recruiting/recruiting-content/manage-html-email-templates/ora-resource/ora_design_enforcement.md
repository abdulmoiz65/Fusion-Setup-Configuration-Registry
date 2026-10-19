# Manage HTML Email Templates Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Cross-environment archive gate | For a supplied cross-environment FSM package, compare it with a fresh target task-level FSM export. When it contains both existing and new templates, require an explicit choice to Replace existing templates or Import only new templates. Do not require this comparison for an individual create generated from the documented Basic, Blank, or MultiColumn mapping. |
| 2 | Dependent-CSV default gate | When the user does not provide dependent CSV files, generate the complete approved metadata and type-association CSV payload before package validation; never overwrite supplied files. |
| 3 | Design-metadata gate | For FSM import, require complete compatible DesignMetadata and matching parent, metadata, and type-association keys. |
| 4 | Preview and approval gate | Validate the immutable archive, bind approval to the exact target and SHA-256, and use only the routed task executor. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| FSM import with both target-existing and target-new templates | Error | | No explicit handling choice is supplied | Present the existing and new template names and request Replace existing templates or Import only new templates | Yes |
| Replace existing templates | Error | | The reviewed archive does not retain all supplied parent rows and their matching metadata and type-association rows | Preserve the complete supplied FSM package for import; do not alter exported parent values | Yes |
| Import only new templates | Error | | The reviewed archive retains a target-existing parent or orphaned metadata/type-association row | Retain each target-new parent and every matching dependent row; exclude every target-existing parent and matching dependent row | Yes |
| Individual template create | Error | | One or more of Name, Template Type, the applicable Campaign Purpose or Email Type, or Template is missing; Template is not Basic, Blank, or MultiColumn; or the type selection is incompatible with the selected Template Type | Collect the four UI fields, select a mapped Campaign Purpose or Email Type, and use the matching complete documented design-metadata baseline | Yes |
| Activate, deactivate, interactive design edit, or delete | Error | | The requested action is attempted through the task-level FSM export/import route | Provide a manual handoff to the Manage HTML Email Templates UI; do not automate browser/UI actions. The documented task CSV package does not expose a lifecycle status or delete operation. | No |
| Individual create without dependent CSV files | Error | | The selected Basic, Blank, or MultiColumn documented metadata is unavailable, reduced, or changed from the Complete UI-Created Baseline Mapping | Stop before preview; restore the matching complete documented metadata or select another documented template baseline | Yes |
| FSM import with supplied dependent CSV files | Error | | DesignMetadata is minimal, reduced, hand-built as a placeholder, incompatible, or has parent-key mismatch | Correct supplied files; do not overwrite them with defaults | Yes |
| Generated dependent CSV payload | Error | | Generated type-association row does not match the selected Campaign Purpose or Email Type, generated design metadata does not match the selected mapped source fingerprint, or generated parent codes do not match | Regenerate both dependent CSV files from the documented defaults | Yes |
| FSM import | Error | | Parent, metadata, and type-association MessageDesignCode values do not agree | Rebuild related rows from one selected source template | Yes |
| Any live mutation | Error | | Current preview, exact immutable artifact or selected record, or immediate approval is absent | Stop before the mutation | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HET.ENFORCE_DESIGN | decision | 40 | design_enforcement | passed->HET.EXECUTION_GATE;blocked->HET.HANDLE_ERROR | HET.APPLY_DEFAULTS | stop | Before routing a validated request to task-level FSM export or FSM Data Loader import |
