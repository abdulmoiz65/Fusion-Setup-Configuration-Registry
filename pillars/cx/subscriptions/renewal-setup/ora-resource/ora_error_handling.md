# Renewal Template Error Handling

## Error Handling Expectations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | Required renewal template details are missing or incompatible | Return the missing or incompatible values and stop before any REST payload preparation. |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | The RenewalTemplates describe request cannot be authorized or read | Stop and request authorized read-only access; do not infer REST attributes. |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | A renewal template update supplies RenewalTemplateId as its key | Stop before archive preparation. Replace it with the existing RenewalTemplateNumber and rebuild validation and approval for the corrected update artifact. |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | RETURN_SUCCESS | terminal | 40 | terminal | none | RT.ENFORCE_DESIGN | stop | All documented input and design checks pass |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Validation, describe access, or design enforcement is blocked or fails |
