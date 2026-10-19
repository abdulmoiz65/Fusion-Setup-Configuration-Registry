# Renewal Template Defaulting Rules

## Standard Defaults

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | RenewalTemplateId | Server default expression | Creating a renewal template without an identifier | No | describe_renewal_templates |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | RenewalTemplateNumber | Server default expression | Creating a renewal template without a template number | No | describe_renewal_templates |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | RT.APPLY_DEFAULTS | step | 25 | apply_default | applied->RT.ENFORCE_DESIGN;not_applicable->RT.ENFORCE_DESIGN;failed->RETURN_ISSUES | RT.RESOLVE_COTERMINATE | stop | A create request has completed schema validation |
