# Manage Communicate Info Design Enforcement

This executable design scope covers Campaign Management numbering only.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate generation method | Resolve the requested display value to one supported backing value |
| 2 | Preserve unrelated values | Keep the current starting value unless the user explicitly requests and validates a replacement |
| 3 | Review import scope | Confirm that the immutable FSM archive changes only the approved campaign-number values |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Campaign Number Generation Method is changed | Blocker |  | The requested value does not map to ORA_CAMP_GEN_METHOD_AUTO or ORA_CAMP_GEN_METHOD_MANUAL | Select Automatic or Manual | Yes |
| Only Campaign Number Generation Method is changed | Blocker |  | Campaign Number Starting Value differs from the readback baseline | Restore the baseline starting value before preparing the immutable archive | Yes |
| An FSM archive is prepared | Blocker |  | The archive changes an unrequested setting or does not contain the exported Manage Communicate Info metadata and CSV files | Rebuild the archive from the current task-level CSV export and apply only the approved change | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCI.ENFORCE_DESIGN | decision | 5 | design_enforcement | ready->MCI.EXECUTION_GATE;blocked->MCI.HANDLE_ERROR | MCI.CHECK_DEPENDENCIES | stop | Campaign-number input and dependency checks passed |
