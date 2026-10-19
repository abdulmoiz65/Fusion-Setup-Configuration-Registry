# Manage External Integrations Error Handling

Report the result for the selected path and one safe next action.

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | The request type, integration, or desired state is missing or conflicting | Correct the identified input and return the public document for the named integration when one is available |
| Status lookup incomplete | The GET fails, a setting row is missing or duplicated, or a value is not Y or N | Report Unknown for the affected integration, state the precise issue, and return the matching public Oracle document |
| Export blocker | The FSM task or routed export workflow is unavailable | Report the FSM export blocker and return the matching public Oracle document; do not substitute the document for the export route |
| Documentation gap | No public Oracle document covers the requested setting change | State the gap and do not execute an undocumented change |
| Security blocker | A secret is proposed for tracked input or output | Remove it and use the approved external secret store |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Current status result | Show Microsoft Teams and Slack separately as Enabled, Disabled, or Unknown; state that the result came from the live GET |
| Export result | Show the FSM task identity and the export artifact or process outcome |
| Setting-change request | Link the matching public Oracle document, state what it covers, and state that this skill did not change Fusion |
| Disable request | State when the public setup document does not provide a whole-integration disable procedure |
| Any error result | Link the matching public Oracle document for the named integration when one is available; state that it is guidance and does not replace the blocked GET or FSM export route |
| Blocked result | Show the failure class, affected path, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Status cannot be verified | Do not use the supplied ZIP or an earlier status as current evidence |
| A setting change is requested | Do not call updateSettingValues or submit an import from this skill |
| Export fails or is uncertain | Do not retry automatically or claim that an artifact was created |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MEI.RETURN_STATUS | terminal | 4 | terminal | none | MEI.EVALUATE_STATUS | stop | Return the live status result |
| MEI.RETURN_EXPORT_ROUTE | terminal | 6 | terminal | none | MEI.ROUTE_EXPORT | stop | Return the FSM export route or routed export result |
| MEI.RETURN_GUIDANCE | terminal | 8 | terminal | none | MEI.GUIDE_CHANGE | stop | Return the matching public Oracle document without changing Fusion |
| MEI.HANDLE_ERROR | step | 9 | error_handler | disclosed->MEI.RETURN_ISSUES | none | stop | Input, status, export, documentation, or security handling is required |
| MEI.RETURN_ISSUES | terminal | 10 | terminal | none | none | stop | A blocker or unknown result prevents successful completion |
