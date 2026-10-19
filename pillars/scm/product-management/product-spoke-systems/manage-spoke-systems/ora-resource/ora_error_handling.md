# Manage Spoke Systems Error Handling

## Source and Scope

Source: developer questions about failed updates and differing source-system versus options self-link identities. The observed discrepancy is a diagnostic hypothesis, not proof of the outgoing loader URL. The authoring and Data Loader workflows require unresolved contracts to block and prohibit unapproved replay. No generic transport or retry implementation belongs here.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Source-system ID differs from the options self-link key | Report the identity distinction. Do not claim the CSV is incorrect solely because the numbers differ. Confirm the loader URL-key mapping before preparing another update. |
| Requested UI field is ambiguous | Stop before selecting a similarly named field in another section; request the owning section or resolve an authorized field contract. |
| Source contract is incomplete | Return the file, field, and unresolved requirement; no task readiness or successful update claim. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Proposed write to spokeSystems | Do not register or use spokeSystems as the updating business object; the developer scoped it to read-only identity lookup. |
| Failed or uncertain options mutation | Do not replay the update or bypass Data Loader with direct PATCH. Follow the invoking workflow's diagnosis and new approval requirements. |
| Missing reference contract | Do not substitute a guessed key, category, REST enum, or local authority. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MSS.HANDLE_ISSUE | step | 90 | error_handler | reported->RETURN_ISSUES | none | stop | Mandatory input validation returns failed |
| RETURN_ISSUES | terminal | 100 | terminal | none | none | stop | Return unresolved requirements and one safe next action |
| MSS.DONE | terminal | 40 | terminal | none | MSS.VALIDATE_INPUT | stop | Return mandatory-input validation success to the caller; this does not authorize a write or verify a Fusion update |
