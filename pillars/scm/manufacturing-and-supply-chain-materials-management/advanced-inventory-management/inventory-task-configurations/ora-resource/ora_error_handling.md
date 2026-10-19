# Inventory Task Configurations Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| XLSX contains OrganizationId or OrganizationCode. | Clear both cells, retain OrganizationName, and rebuild the Data Loader source artifact. Do not upload or retry the invalid artifact unchanged. |
| An explicitly selected FSM CSV contains Y or N task-generation values. | Stop before upload. Rebuild the immutable FSM archive with the exact strings Yes or No; do not add REST child fields to the CSV. |
| Data Loader artifact is missing StatusCode, StartDate, or TaskGroupingLevel on an emitted activity usage. | Apply the canonical default when the field is absent; otherwise stop and request a supported value before handoff. |
| StartDate is not a YYYY-MM-DD value. | Stop before Data Loader handoff. Render the corrected calendar date in the XLSX and restart core Data Loader validation. |
| Default-zone lookup returns more than one row. | Stop before artifact preparation. Do not select the first result; resolve the duplicate default-zone data. |
| No default zone exists. | For REST Create, prepare one parent-root XLSX containing the default-zone parent row and its activityUsages rows. Populate child OrganizationName and derived ZoneName for ParentUserKeys resolution. This rule does not apply when FSM Import was explicitly selected. |
| Create is requested but a default zone already exists. | Stop before artifact preparation. Request an explicit Update operation; do not overwrite the existing configuration with a create artifact. |
| Update is requested but no default zone exists. | Stop before artifact preparation. Request an explicit Create operation; do not fabricate a parent identity or send a PATCH artifact. |
| Update result does not contain all five current activity usage types. | Stop before Data Loader handoff. Resolve the incomplete configuration or obtain an approved create/remediation plan; do not guess missing current values. |
| Required activityUsages parent identity is absent or incomplete. | Stop before XLSX artifact preparation. Do not add ParentIdentifier or manually source ZoneId. Correct OrganizationName or derived ZoneName, or remediate the BO ParentUserKeys registration. |
| An emitted activity usage has a missing or invalid TaskGroupingLevel. | Apply the canonical activity matrix and regenerate the source artifact. Core Data Loader validation and its final-artifact approval must restart. |
| OrganizationName does not resolve to exactly one accessible task-management organization. | Stop before Data Loader handoff and request an accessible organization name. |
| Organization or default-zone parent identity is missing for activityUsages. | Stop before Data Loader handoff and request the missing parent identity. |
| TaskGroupingLevel display value cannot be resolved to one allowed LookupCode. | Stop before Data Loader handoff; do not guess, fuzzy-match, or select the first result. |
| A conflicting TaskGroupingLevel meaning and code are supplied. | Stop and request one unambiguous value. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Lookup is missing, ambiguous, or failed. | Do not submit a Data Loader request or retry a mutation. |
| A task-local XLSX approval is requested before `core.data-loader` prepares its final immutable artifact. | Do not request it or dispatch a REST or import operation. Hand off only after task-local validation passes; `core.data-loader` owns the single approval to upload and initiate its final artifact. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| INV_TASK_CONFIG.DATALOADER_HANDOFF | terminal | 50 | terminal | none | INV_TASK_CONFIG.CHECK_PARENT_CHILD_READINESS | continue | Local validation, lookup, defaulting, and dependency checks have passed; hand off the prepared XLSX to `core.data-loader` for its normal approval and import workflow. No task-local approval or import call. |
| INV_TASK_CONFIG.FSM_DATALOADER_HANDOFF | terminal | 51 | terminal | none | INV_TASK_CONFIG.CHECK_FSM_READINESS | continue | FSM validation and readiness passed; hand off the unchanged FSM ZIP to `core.data-loader` for its normal approval and import workflow. No task-local approval or import call. |
| INV_TASK_CONFIG.RETURN_ISSUES | terminal | 90 | terminal | none | none | continue | Any task-local validation, lookup, defaulting, or dependency prerequisite is blocked or fails. |
