# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm task boundary | Keep the package to one approved hierarchy and its node tree. |
| 2 | Validate authoritative evidence | Confirm every node's exact master geography and immediate parent evidence. |
| 3 | Validate node links and identifiers | Confirm correlation codes and one identifier row per imported node. |
| 4 | Validate package representation | Use only the task-native FSM package representation. |
| 5 | Prepare immutable import preview | Bind the target environment and validated ZIP before seeking approval. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every package | Blocker | | More than one unrelated hierarchy or node tree is included | Retain only the approved hierarchy and nodes | Yes |
| Every node | Blocker | | A geography element, master identifier, parent relation, spelling, or accent variant is guessed or unresolved | Obtain authoritative evidence before packaging | Yes |
| Every child node | Blocker | | ParentGeoNodeCode does not identify the immediate parent node | Correct the package-local node link | Yes |
| Identifier coverage | Blocker | | An imported node has no matching identifier row or the identifier values disagree | Add or correct the identifier row | Yes |
| Package representation | Blocker | | XML, JUnit, or migration-batch content is used as an FSM CSV package | Use the matching task-native FSM route | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GHH.ENFORCE | decision | 40 | design_enforcement | passed->GHH.APPROVAL_GATE;blocked->GHH.DESIGN_ISSUES | GHH.DEFAULTS | stop | Dependency evidence and defaults are complete |
