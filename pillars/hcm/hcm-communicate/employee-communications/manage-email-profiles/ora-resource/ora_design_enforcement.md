# Manage Email Profiles Design Enforcement

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A profile is created | Blocker | | Baseline has an exact ConfigName match or archive changes more than one new row | Rebuild from current export with a unique name | Yes |
| A profile is deleted | Blocker | | The current export does not resolve exactly one target row or the archive changes fields other than ObjectStatus | Rebuild from current export and set only ObjectStatus to ORA_DELETED | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MEP.ENFORCE_DESIGN | decision | 3 | design_enforcement | passed->MEP.EXECUTION_GATE;blocked->MEP.HANDLE_ERROR | MEP.CHECK_DEPENDENCIES | stop | An immutable sender-profile archive is evaluated |
