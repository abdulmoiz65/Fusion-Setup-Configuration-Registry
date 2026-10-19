# Dependency-Graph Enrichment

## Purpose

Use `knowledge/dependency-graphs/*.json` to add sequencing information for
selected setup tasks and to add selected pre-release/custom tasks when that
information is absent from the release catalog and FSM task-discovery result.
This is a non-blocking overlay: release catalog data remains the primary
sequence source, FSM data remains the secondary discovery source, and the
effective catalog is the final task-inclusion authority.

## Inputs and Eligibility

Read these sources in order:

1. `knowledge/setup-task-catalog/release/offering-functional-area-task-catalog.json`
2. `knowledge/setup-task-catalog/pre_release/setupTasks_supplement.json`
3. `knowledge/setup-task-catalog/custom/setupTasksAll.json`
4. The effective offering-functional-area hierarchy, used only to resolve
   pre-release/custom ownership context.
5. Every graph selected from `knowledge/dependency-graphs/*.json`.

Use a graph task for ordering, dependency enrichment, or graph-derived
membership only when all of the following are true:

- Its resolved offering and functional area are within the requested scope.
- The graph node contains exactly one matching task identity after resolution.
- That identity resolves to exactly one valid task in
  `knowledge/setup-task-catalog/effective/setupTasksAll.json` and is present in
  the same effective offering/functional-area context.

The graph may introduce task membership only when the task code is present in
the pre-release supplement or custom task catalog *and* passes the final
effective-catalog validation above. A task already present in the release
baseline or FSM result remains in that source's membership, but its graph order
and graph dependencies may be added as supplemental provenance.

Do not add an out-of-scope graph node merely because an edge references it. If
an edge points to an unresolved or out-of-scope node, retain the in-scope task
and record an unresolved graph prerequisite diagnostic.

## Node Mapping and Intra-Functional-Area Order

Graph nodes represent FSCR setup-skill scope. Their `taskCallSequence` array is
the canonical graph sequence for the node; use its ordered `callOrder` entries
and task IDs. If that array is unavailable, use `children` only when every
child has an unambiguous task identity and `callOrder`. A graph node that has
neither representation contributes no tasks.

Map each graph task ID to its catalog task code. For `task:<code>` IDs, the
suffix is the task code. For other graph task IDs, require an exact match to an
effective catalog task code or task name; never infer from a label. Use the
resolved effective task ownership context to build the
functional-area-to-task mapping. Within each functional area, preserve
ascending graph `callOrder`; retain a task's explicit `dependsOn` relations as
graph-internal prerequisites.

Catalog task occurrences are distinct when their offering, functional area, or
stable task-list item identifier differs. Retain every such occurrence in
`setup_task_sequence`, even when task code or name repeats, and preserve its
own sequence. When a graph task resolves to a repeated code, attach its graph
ordering and dependency provenance only to the matching effective-catalog
occurrence; diagnose and skip an ambiguous mapping.

For a pre-release/custom task that has no catalog or FSM sequence metadata,
use the graph `callOrder`, task-level `dependsOn`, and mapped `depends-on`
edges to derive its logical sequence before the stable topological sort. Graph
file order is not a sequence. If no valid graph dependency information remains
after effective-catalog validation, append the task to the end of its containing
functional area. Order multiple fallback tasks by effective task code, assign
sequence numbers, and renumber subsequent tasks accordingly. Retain every such
valid task in `setup_task_sequence`; set its `sequence_source` to
`functional_area_tail` and emit a `sequence_fallback` diagnostic with its
effective task code, source layer, offering and functional area, graph paths
examined, and fallback reason. This fallback also applies when no graph is
available. Missing sequence metadata alone is not grounds for exclusion.

Graph nodes do not override release/FSM ownership, display name, or task code.
They add pre-release/custom task membership where eligible, plus supplemental
order and dependency provenance for any matching selected task.

## Edge Mapping

An edge with `relationship: "depends-on"` means its `from` node depends on its
`to` node. For nodes with ordered task lists, map that node-level dependency to
a task-level relation from the first `from` task to the terminal `to` task(s).
For direct task nodes, use the node's single task. Retain the source graph file,
edge tuple, and mapping method in dependency provenance.

Skip and diagnose edges with an unsupported relationship, missing endpoint,
ambiguous endpoint task mapping, or cycle. Never guess a task pairing.

## Merge and Failure Rules

- The release baseline wins for release task identity and unrelated ordering.
- FSM discovery supplements a missing release task set; it does not override a
  valid release sequence merely because its response order differs.
- Graph enrichment may add ordering and dependencies for any matching selected
  task. It may add graph-derived task membership only for pre-release/custom
  tasks; it cannot remove release/FSM tasks or dependencies.
- De-duplicate only duplicate source representations of the same catalog task
  occurrence, identified by offering, functional area, and stable task-list
  item identifier. Do not de-duplicate repeated catalog tasks merely because
  their task code or name matches. De-duplicate dependencies by source and
  occurrence-aware `(from_occurrence, to_occurrence, relationship)` identity.
- If the graph is absent, invalid JSON, lacks `nodes`/`edges`, contains
  duplicates, has invalid endpoint references, or produces a cycle, preserve
  the release/FSM sequence and persist a `dependency_graph` diagnostic with the
  skipped graph path and reason.
- If only part of a graph is resolvable, use the resolvable portion and emit a
  diagnostic for every skipped node or edge. Omit every graph-derived task that
  lacks a final valid effective-catalog resolution. Do not make graph
  completeness an approval or execution blocker.

After combining the valid prerequisite relationships, retain functional-area
tail placement for fallback tasks and apply the stable topological ordering.
Assign consecutive positive integer `sequence` values from 1 across the final
result, including all selected, effective-catalog-validated pre-release/custom
tasks. Renumber subsequent tasks after insertions and preserve original
catalog/FSM sequence values and graph ordering as provenance.

The persisted `setup_task_sequence` must identify `sequence_source` (`release`,
`fsm`, `dependency_graph`, or `functional_area_tail`), the source catalog layer,
effective-catalog validation evidence, prerequisite provenance, and graph and
fallback diagnostics so downstream task-map and Run Book workflows can explain
the result. Each entry must include its offering, functional area, and stable
task-list item identifier so repeated catalog tasks remain distinct and retain
their respective sequences. Persist it as `setup-task-sequence.json` under the
skill's declared workspace output location.
