# Manage External Integrations Design Enforcement

Keep the status, export, and setting-change paths separate.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Identify the path | Select status GET, FSM export, or public-document guidance |
| 2 | Enforce the boundary | Run only the operation allowed for that path |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Current status is requested | Blocker | get_communicate_integration_status | Status is inferred from an export, example, or earlier result instead of the GET | Run the documented GET and report each integration separately | Yes |
| Export is requested | Blocker | | The request is routed to a status GET, setting update, or core.data-loader import | Use shared.setup-export.task-level-export for the FSM task export | Yes |
| A setting change is requested | Blocker | | A live update or import is attempted, or the matching public Oracle document is omitted | Return the Microsoft Teams or Slack public setup document and state its coverage; do not mutate Fusion | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| get_communicate_integration_status | Before reporting a requested current Microsoft Teams or Slack status | One exact result for each requested setting code and its SettingValue | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MEI.GUIDE_CHANGE | decision | 7 | design_enforcement | guidance_ready->MEI.RETURN_GUIDANCE;blocked->MEI.HANDLE_ERROR | MEI.VALIDATE_INPUT | stop | An enable or disable request is supplied for Microsoft Teams or Slack |
