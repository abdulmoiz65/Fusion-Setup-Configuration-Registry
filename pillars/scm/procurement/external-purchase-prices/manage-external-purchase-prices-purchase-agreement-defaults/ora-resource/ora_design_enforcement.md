# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Choose scope | Use All Business Units for common defaults; use a specific active requisitioning BU only for an intended override |
| 2 | Review defaults | Confirm each changed value is appropriate for BPAs created from external purchase prices |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Specific-BU setup | Blocker | | BU identity is blank or ambiguous | Supply one exact requisitioning BU identity | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPPAD.ENFORCE_DESIGN | decision | 4 | design_enforcement | passed->EPPPAD.EXECUTION_GATE;blocked->EPPPAD.HANDLE_ISSUES | EPPPAD.APPLY_DEFAULTS | stop | Every request |
