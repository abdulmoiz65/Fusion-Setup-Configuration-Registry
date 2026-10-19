# Manage Email Profiles Dependency Readiness

Source: Confluence page 21768014830 and current FSM export evidence.

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| MEP-BASELINE | Current task CSV export | Yes | A profile is created | Verify | shared.setup-export.task-level-export output | | Prevent duplicate and stale create | Export current task CSV | Export ZIP and ConfigName rows |
| MEP-ARCHIVE | Immutable FSM create archive | Yes | A profile is created | Verify | Current export metadata plus new profile row | | Binds submission to one approved change | Validate ZIP and record SHA-256 | Archive path and SHA-256 |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MEP.CHECK_DEPENDENCIES | decision | 2 | resolve_dependency | ready->MEP.ENFORCE_DESIGN;blocked->MEP.HANDLE_ERROR | MEP.VALIDATE_INPUT | stop | A sender-profile request has valid inputs |
