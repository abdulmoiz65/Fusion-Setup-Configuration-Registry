# Renewal Template Design Enforcement

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|---|
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | 1 | Validate renewal economics | Confirm the selected price adjustment type has all required values and follows the documented no-price rule. |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | 2 | Validate renewal process criteria | Confirm customer acceptance and internal approval criteria are compatible with the selected renewal process. |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | Price adjustment type is Markdown or Markup | Error |  | Price adjustment basis or price adjustment value is absent. | Provide both the adjustment basis and value. | Yes |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | No price exists at renewal | Error |  | Price adjustment type, basis, and value are not Markup, Net Price, and 0 respectively. | Set price adjustment type to Markup, basis to Net Price, and value to 0. | Yes |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | Renewal process is Automatic and customer acceptance is required | Error |  | Internal approval criterion is supplied as an active requirement. | Use the documented Automatic plus Customer Acceptance configuration; configure event notification rules if automatic routing to the customer is needed. | Yes |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | Renewal process is Manual or Do not renew | Error |  | Customer acceptance or internal approval is treated as a required criterion. | Treat these criteria as not applicable for the selected process. | Yes |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | RT.ENFORCE_DESIGN | decision | 30 | design_enforcement | passed->RETURN_SUCCESS;issues->RETURN_ISSUES | RT.APPLY_DEFAULTS | stop | A renewal template create, update, or review request has completed schema validation |
