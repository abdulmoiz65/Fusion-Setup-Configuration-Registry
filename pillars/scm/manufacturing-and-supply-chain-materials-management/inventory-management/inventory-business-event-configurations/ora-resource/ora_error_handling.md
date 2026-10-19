# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Event type or event name is missing | Identify the missing field group and stop before lookup or Data Loader handoff. |
| Event type or event name lookup has zero, multiple, or conflicting matches | Return the supplied values and request one exact code or meaning for the applicable lookup type, then stop. |
| Event lookup cannot be read | Report a sanitized authentication, authorization, transport, or Fusion API diagnostic and stop without retrying automatically. |
| Business unit or inventory organization foundation is missing or not established | Identify the missing Fusion setup dependency and stop before event configuration. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Event type or event name input is absent | Provide the missing code or meaning and restart validation. |
| LOOKUP | A live lookup returns zero, multiple, conflicting, or unreadable results | Provide an exact permitted value or correct the read-access issue, then restart validation. |
| FOUNDATION | The required business unit or inventory organization setup is missing or not established | Complete the required Fusion setup data, then restart validation. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Validation, lookup, or foundation readiness fails | Do not configure the event until the prerequisite Fusion setup data is complete. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IBEC.RETURN_SUCCESS | terminal | 50 | terminal | none | IBEC.CONFIRM_FUSION_DATA_FOUNDATION | stop | Input validation, both event lookups, and Fusion data foundation readiness succeed |
| RETURN_ISSUES | terminal | 60 | terminal | none | none | stop | Input validation, lookup, or foundation readiness identifies a blocker |
