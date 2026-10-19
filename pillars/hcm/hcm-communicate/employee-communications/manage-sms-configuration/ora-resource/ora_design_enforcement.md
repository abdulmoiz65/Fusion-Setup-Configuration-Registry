# Manage SMS Configuration Design Enforcement

Only one SMS configuration may be active. The supplied parent CSV has no active-status field, so the import must not claim to set or verify active status. When activation is requested, successful provider creation must be followed by a manual activation handoff in Manage SMS Configuration.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve import scope | Do not represent the supplied parent CSV as setting or verifying provider active status |
| 2 | Activate after creation | After successful creation, go to Manage SMS Configuration and review the created configuration before activation |
| 3 | Enforce one active configuration | Deactivate any currently active SMS configuration before activating the created configuration, then verify exactly one SMS configuration is active |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A provider configuration import is prepared | Warning | | The import is presented as setting or verifying active status even though the supplied CSV has no active-status field | Limit the import claim to provider-account creation and return the post-creation activation handoff after success | Yes |
| Provider activation is requested after successful creation | Blocker | | Another SMS configuration would remain active when the created configuration is activated | In Manage SMS Configuration, deactivate the currently active configuration before activating the created configuration | Yes |
| The created configuration is activated | Blocker | | The task shows zero or more than one active SMS configuration | Correct the task state until exactly one SMS configuration is active | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SMS.ENFORCE_SINGLE_ACTIVE | decision | 4 | design_enforcement | passed->SMS.EXECUTION_GATE;disclosed->SMS.EXECUTION_GATE;blocked->SMS.HANDLE_ERROR | SMS.CHECK_DEPENDENCIES | stop | The import active-status boundary and the post-creation exactly-one-active handoff are reviewed |
