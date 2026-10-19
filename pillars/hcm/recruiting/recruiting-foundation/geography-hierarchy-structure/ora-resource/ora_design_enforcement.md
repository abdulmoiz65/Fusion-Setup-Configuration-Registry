# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm task boundary | Keep the request to one country's allowed level mapping. |
| 2 | Validate package representation | Use only the task-native FSM package representation. |
| 3 | Preserve approved controls | Preserve control values unless approved evidence changes them. |
| 4 | Prepare immutable import preview | Bind the target environment and validated ZIP before seeking approval. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every package | Blocker | | More than one country, Postal Code, or an unsupported level mapping is present | Reduce the package to the approved country and supported levels | Yes |
| Level-three mapping | Blocker | | Level two is blank | Populate the approved level-two mapping or remove level three | Yes |
| Existing country update | Blocker | | Control values changed without approved design evidence | Restore exported controls or obtain approved evidence | Yes |
| Package representation | Blocker | | XML, JUnit, or migration-batch content is used as an FSM CSV package | Use the matching task-native FSM route | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GHS.ENFORCE | decision | 40 | design_enforcement | passed->GHS.APPROVAL_GATE;blocked->GHS.DESIGN_ISSUES | GHS.DEFAULTS | stop | Dependency evidence and defaults are complete |
