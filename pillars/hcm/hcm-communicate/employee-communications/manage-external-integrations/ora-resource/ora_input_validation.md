# Manage External Integrations Input Validation

Classify the request into one of three paths: current status, FSM export, or setting-change guidance. This skill covers only the Microsoft Teams and Slack integration flags.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Request type | Current status, export, or setting change | Clarify the requested outcome | Use the request and existing context | Every request | |
| Integration | Microsoft Teams, Slack, or both | Use both only for a status request; otherwise clarify | Match the integration named by the user | Status or setting-change request | |
| Desired state | Enable or disable | Clarify the intended state | Accept only an explicit enable or disable request | Setting-change request | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Status scope | Accept Microsoft Teams, Slack, or both | Current status is requested | |
| Export scope | Use task code ORA_IRC_EMP_EXT_INTEGRATIONS and task name Manage External Integrations | Export is requested | |
| Change scope | Accept enable or disable guidance for Microsoft Teams or Slack; do not execute a state change | A setting change is requested | |
| Credentials | Reject tokens, passwords, private keys, or other secrets from tracked files and output | Every request | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MEI.VALIDATE_INPUT | decision | 1 | validate_input | status->MEI.READ_STATUS;export->MEI.ROUTE_EXPORT;change->MEI.GUIDE_CHANGE;invalid->MEI.HANDLE_ERROR | none | stop | A Microsoft Teams or Slack external-integration request is supplied |
