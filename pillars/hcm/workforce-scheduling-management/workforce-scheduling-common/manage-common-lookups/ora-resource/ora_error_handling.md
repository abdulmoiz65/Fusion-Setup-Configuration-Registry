# Manage Common Lookups Error Handling

## Source Basis

- Workforce Scheduling Common Applications provider-dependency contract, user-provided 18 August 2026

## Error Situations

| Situation | What Should Happen |
|---|---|
| The consuming task does not supply an exact lookupType | Stop before the provider lookup and request the exact product identifier from the consuming task. |
| The provider cannot resolve the supplied lookupType, returns ambiguous state, or reports a validation gap | Stop before recommending or applying a change, disclose the provider gap, and request corrected provider evidence. |
| The requested state already matches the provider recommendation | Return the evidence and make no change. |
| A provider-owned change lacks current user confirmation | Stop before the provider executes the change. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCL.HANDLE_ISSUES | step | 30 | error_handler | handled->MCL.RETURN_ISSUES | none | stop | A provider dependency, identifier, validation, or approval gate is blocked |
| MCL.RETURN_ISSUES | terminal | 40 | terminal | none | none | stop | A blocked provider dependency has been disclosed with a safe next action |
| MCL.READY | terminal | 50 | terminal | none | MCL.ENFORCE_PROVIDER_OWNERSHIP | stop | Provider evidence supports a recommendation; any provider-owned mutation still needs user confirmation |
