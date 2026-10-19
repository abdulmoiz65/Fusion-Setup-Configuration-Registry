# Renewal Template Input Validation

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | Template identity | RenewalTemplateName for create; RenewalTemplateNumber for update | Stop | Provide a template name of no more than 150 characters for create, or the existing Renewal Template Number for update. | Creating or updating a renewal template | describe_renewal_templates |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | Required REST attributes | RenewalTemplateName; DaysBeforeExpiry; MinRenewalDuration; RenewalDuration; RenewalDurationPeriod; RenewalProcess; CoTerminate; RenewalLevel | Stop | Provide values for every required input attribute. | Creating a renewal template | describe_renewal_templates |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | Optional consolidation preference | ConsolidateYn | Continue | Leave unset when consolidation is not selected. | Creating a renewal template |  |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | Price adjustment details | PriceAdjustmentBasis; PriceAdjustmentPercent | Stop | Provide both values. | PriceAdjustmentType is Markdown or Markup |  |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | Renewal acceptance criteria | Customer acceptance required; internal approval required | Stop | Provide the criteria allowed for the selected renewal process. | Renewal process is Automatic |  |

## Field Validation

| Task Code | Task Name | Check | What Happens | Applies When | Resolver |
|---|---|---|---|---|---|
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | REST attribute mapping | Accept documented input only when it maps to a describe-backed RenewalTemplates attribute; reject read-only audit attributes. | A REST operation is planned | describe_renewal_templates |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | Update business key | Require RenewalTemplateNumber for every update. Reject RenewalTemplateId as an update key and do not put it in the Data Loader update payload. | Updating a renewal template | describe_renewal_templates |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | Coterminate lookup mapping | Resolve a supplied Coterminate label or code to the active LookupCode before loader-artifact preparation. | A renewal template request supplies a Coterminate value | resolve_coterminate_option |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | RT.VALIDATE_INPUT | step | 10 | validate_input | valid->RT.DESCRIBE_SCHEMA;invalid->RETURN_ISSUES | none | stop | A renewal template create, update, or review request is prepared |
