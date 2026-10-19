# Workstations Error Handling

## Source Evidence

| Source | Verified Fact | Source Anchor |
|---|---|---|
| Oracle Setup Task CSV Imports REST API | Task CSV import status values are `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`, `COMPLETED_WARNINGS`, and `COMPLETED_ERRORS`. `ProcessLog` contains processing details for each imported business object and can be downloaded from the import-process result. | [Get an import process result](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-11.13.18.05-setuptaskcsvimports-taskcode-child-setuptaskcsvimportprocess-processid-child-setuptaskcsvimportprocessresult-processid-get.html); [Get an import process log](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-setuptaskcsvimports-taskcode-child-setuptaskcsvimportprocess-processid-child-setuptaskcsvimportprocessresult-processid-enclosure-processlog-get.html) |

## Error Situations

| Situation | What Must Happen |
|---|---|
| A required create field is absent or violates a sourced length limit | Stop before FSM package assembly. Identify the exact missing or invalid field. |
| The organization is not confirmed as a manufacturing plant, or the Work Center cannot be confirmed as one existing parent Work Center in that organization | Stop. Do not select an organization or Work Center by position or invent a lookup result. |
| The requested Workstation code is known to be in use in the target organization | Stop. Require a new code or an approved FSM update contract. |
| An equipment-resource-instance association is inactive, not equipment type, belongs to another organization or Work Center, or is already associated with another Workstation | Stop the association. The primary Workstation may proceed only when its own validated FSM contract is complete. |
| Current Workstations FSM input details remain unknown | Stop before package assembly. Report which rule remains undocumented: remaining header requiredness, accepted date and Boolean literals, translation behavior, lookup mechanics, or package order. |
| A future approved FSM import reaches `COMPLETED` or `COMPLETED_WARNINGS` | Treat `COMPLETED` as success and `COMPLETED_WARNINGS` as success with warnings. Retrieve and retain `ProcessLog`; it contains processing details for each imported business object. |
| A future approved FSM import completes with errors | Treat `COMPLETED_ERRORS` as an issue outcome. Retrieve the process log; do not automatically resubmit the ZIP. |
| A future approved FSM import remains `NOT_STARTED` or `IN_PROGRESS` after the polling window | Stop polling and report the task code, process identifier, and last known status. Do not recheck the same process until a user explicitly asks to do so. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WORKSTATIONS.DONE | terminal | 30 | terminal | none | WORKSTATIONS.DESIGN_CREATE_CONTRACT | continue | The documented input and design checks pass. This terminal does not authorize FSM package assembly or a Fusion write. |
| WORKSTATIONS.RETURN_ISSUES | terminal | 40 | terminal | none | none | continue | A validation or design check fails, or a required FSM contract remains undocumented. |
