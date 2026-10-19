# Learning Paths Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Group and definition integrity | Group rows by path and validate identity, explicit empty-Draft intent, sections, and unique activity membership |
| 2 | Graph integrity | Validate display and completion-access predecessors and reject dangling, self-referential, or cyclic edges |
| 3 | Validity and renewal | Validate begin, expiry, renewal, due, and reassignment combinations |
| 4 | Lifecycle and deletion safety | Require complete structure for activation, refresh usage for deletion, and freeze exact approved rows |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Empty Draft create | Blocker | | Empty Draft intent is not explicit or required parent identity is incomplete | Confirm empty Draft intent and complete the parent definition | Yes |
| A row adds or replaces an activity | Blocker | | Authoritative eligibility and relationship evidence is unavailable | Defer the row or provide an approved catalog-item resolver | Yes |
| Existing or proposed dependency graph | Blocker | resolve_learning_path_existing_graph | An edge is dangling, self-referential, duplicated, or creates a direct or indirect cycle | Correct the grouped graph before preview | Yes |
| Validity or renewal configuration | Blocker | | Required values are incomplete or incompatible | Correct the combined validity and renewal design | Yes |
| Activate | Blocker | resolve_learning_path_lifecycle_values | Structure is empty or incomplete, the graph is invalid, or the enabled target value and transition are unresolved | Complete and validate the structure, graph, and lifecycle transition | Yes |
| Retire | Blocker | resolve_learning_path_lifecycle_values | The enabled target value or transition is unresolved | Resolve the live value and transition | Yes |
| Parent delete | Blocker | resolve_learning_path_existing_graph | Current usage or learner-impact evidence does not prove deletion safe | Preserve the path or remove usage through its owning workflow | No |
| Copy | Blocker | | The raw Describe declares no copy action | Do not execute copy | No |
| Any approved row | Blocker | | Environment, grouping, row selection, manifest, or current-state fingerprint differs from preview | Rebuild the preview and obtain new approval | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_learning_path_existing_graph | Existing graph validation, update, activation, deletion, or reconciliation | Membership, order, edges, statuses, usage, metrics, and fingerprint | ora_reference_lookups.md |
| resolve_learning_path_lifecycle_values | Activation or retirement | Current status, enabled target status, and transition eligibility | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LPT.ENFORCE_DESIGN | decision | 5 | design_enforcement | passed->LPT.EXECUTION_GATE;blocked->LPT.HANDLE_ERROR | LPT.APPLY_DEFAULTS | stop | Validated grouped rows have completed their applicable dependencies, lookups, and defaults |
