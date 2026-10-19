# Input Validation

This task skill validates operation routing and read identifiers. For import,
it binds the supplied file role, object, mode, volume, and activity order, then
delegates CSV source inspection and validation to `Import Trading Community
Data`, `core.data-loader`, and their declared dependencies. They may read,
inspect, decode, parse, classify, validate, hash, package, and otherwise process
the CSV as required by their existing contracts.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | operation=read or import; import may explicitly select create, create-or-update, or delete; a named supported read operation also selects read | Stop before external access only when intent cannot be determined | Use the user's stated read or import intent | Every run | |
| Fusion environment | Exactly one configured fusion_environment_context | Stop before authentication or external access | Select one configured target environment through the routed workflow | Every live run | |
| Read operation | read_operation=list, describe, inventory, hierarchy_detail, versions, nodes, or full_read after applicable defaulting | Stop before REST access | Select one supported read operation or use the unqualified-list default | Read operation | |
| List as-of date | Optional ISO date in YYYY-MM-DD form; defaults to the current date in the configured environment's execution context | Stop before REST access when a supplied value is invalid | Correct the supplied date or omit it to use the disclosed default | list | read_ui_aligned_hierarchy_inventory |
| Hierarchy identity for reads | Exact TreeStructureCode and TreeCode; list and inventory may omit TreeStructureCode | Stop before the hierarchy GET that requires the identity | Supply the exact values shown by Fusion or returned by list or inventory | hierarchy_detail, versions, nodes, or full_read | read_hierarchy_tree_exact |
| Version identity for reads | Exact TreeVersionId plus the hierarchy identity | Stop before node lookup | Select an identifier returned by the exact version lookup | nodes; full_read when nodes are requested | read_hierarchy_versions |
| Supplied hierarchy file | Explicit hierarchy_csv and/or hierarchy_node_csv; or exactly two unlabeled ordered_hierarchy_csvs, each resolving to a nonempty regular .csv | Stop before preview only when no supported usable file input was supplied | Supply one explicitly labeled path or two paths in header-then-member order | Import operation | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| List omits TreeStructureCode | Satisfied | Read every accessible tree and version, complete pagination, and apply the eligibility criteria without a client-side structure allowlist | read_ui_aligned_hierarchy_inventory |
| Inventory omits TreeStructureCode | Satisfied | Read every accessible tree and complete pagination without a client-side structure allowlist | read_hierarchy_tree_inventory |
| An exact hierarchy read has TreeStructureCode and TreeCode | Lookup | Require one exact pair match before following returned child links | read_hierarchy_tree_exact |
| Nodes are requested without TreeVersionId | Lookup | List versions and return candidates; do not select a version automatically | read_hierarchy_versions |
| hierarchy_csv is supplied | Satisfied | Route it to object Hierarchy and delegate source inspection and validation to the selected shared/Core workflow | |
| hierarchy_node_csv is supplied | Satisfied | Route it to object HierarchyNode and delegate source inspection and validation to the selected shared/Core workflow | |
| Exactly two unlabeled CSV paths are supplied | Satisfied | Route the first file to Hierarchy and the second file to HierarchyNode; show the mapping in preview and allow normal dependency processing | |
| Delete is requested for an unchanged supplied CSV | Satisfied | Route the exact object with DELETE_RECORD. Do not inspect or resolve row identities before upload; use Core Data Loader's immutable preview and approval, then let Fusion Import Management accept or reject the rows. | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Exact read identifiers | Trim surrounding whitespace, preserve case, and reject control characters or caller-supplied URL fragments | A read identifier is supplied | |
| List as-of date | Require a real calendar date in ISO YYYY-MM-DD form; compare it inclusively with EffectiveStartDate and EffectiveEndDate | A list as-of date is supplied or defaulted | read_ui_aligned_hierarchy_inventory |
| Returned read links | Follow only same-environment canonical or child links returned by the current lookup | Detail, nodes, labels, or data-source-parameter reads | read_hierarchy_tree_exact |
| Import file handoff | Require a supplied path and preserve its explicit file role and basename when handing it to the shared importer; delegate file eligibility and transport checks to the selected shared/Core workflow | A hierarchy import file is supplied | |
| Import CSV processing | Permit declared shared/Core dependencies to inspect and validate headers, rows, and bytes as required; do not create a task-specific validation blocker or treat dependency parsing as a conflict | Every supplied hierarchy import file | |
| Supplied delete row data | Do not inspect or validate PartyId, PartyNumber, parent identity, AsOfDate, or any other row field; Fusion Import Management evaluates the unchanged file after submission | Supplied `Hierarchy` or `HierarchyNode` with `DELETE_RECORD` | |
| Immutable preview digest | Require archiveSha256 from Core Data Loader's structured preflight response through the task-local bridge; do not treat its omission from rendered Markdown as missing and do not calculate a substitute digest | Before building the Task Hook preview | |

## Import Routing

| Supplied File Role | Create Only | Import, Create or Update | Delete | High Volume | Execution Order |
|---|---|---|---|---|---|
| hierarchy_csv | Object Hierarchy with CREATE_ONLY | Object Hierarchy with CREATE_RECORD | Object Hierarchy with DELETE_RECORD | YES | First for create/update; second for delete when both roles are supplied |
| hierarchy_node_csv | Object HierarchyNode with CREATE_ONLY | Object HierarchyNode with CREATE_RECORD | Object HierarchyNode with DELETE_RECORD | YES | Second for create/update; first for delete when both roles are supplied |
| exactly two unlabeled paths | First path maps to Hierarchy with CREATE_ONLY; second path maps to HierarchyNode with CREATE_ONLY | First path maps to Hierarchy with CREATE_RECORD; second path maps to HierarchyNode with CREATE_RECORD | First path maps to Hierarchy with DELETE_RECORD; second path maps to HierarchyNode with DELETE_RECORD | YES for each activity | Preserve role mapping; use header-then-member for create/update and member-then-header for delete |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MH.VALIDATE_REQUEST | decision | 1 | validate_input | read->MH.DEFAULT_READ_OPERATION;import->MH.DEFAULT_IMPORT_MODE;invalid->MH.ERROR | none | stop | Before every Manage Hierarchies operation |
| MH.ROUTE_CX_IMPORT | step | 5 | validate_input | resolved->MH.IMPORT_READY;unresolved->MH.ERROR | MH.DEFAULT_IMPORT_MODE | stop | Bind fixed hierarchy object, mode, volume, and order, then delegate source preflight and CSV processing to the shared/Core workflow |
