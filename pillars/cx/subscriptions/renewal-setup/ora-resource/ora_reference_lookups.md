# Renewal Template Reference Lookups

## Live Lookups

| Task Code | Task Name | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | describe_renewal_templates | Before REST payload preparation or validation | none | {{baseUrl}}/crmRestApi/resources/latest/renewalTemplates/describe | RenewalTemplateNumber string max 30; RenewalTemplateName string max 150; DaysBeforeExpiry integer; MinRenewalDuration integer; RenewalDuration integer; RenewalDurationPeriod string max 30; RenewalProcess string max 30; CoTerminate string max 30; RenewalLevel string max 30; ConsolidateYn string max 30; choice-list mappings for renewal period, renewal process, coterminate, renewal level, and consolidation | Use the authenticated describe response for the exact RenewalTemplates resource. | Renewal Template Number: RenewalTemplateNumber; Template Name: RenewalTemplateName; Days Before Expiration: DaysBeforeExpiry; Minimum Renewal Duration: MinRenewalDuration; Renewal Duration: RenewalDuration; Renewal Period: RenewalDurationPeriod; Renewal Process: RenewalProcess; Coterminate: CoTerminate; Renewal Level: RenewalLevel; Consolidate subscriptions: ConsolidateYn | Stop and obtain authorized read-only describe access. Do not infer REST attributes. |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | resolve_coterminate_option | Before preparing a renewal template whose Coterminate value is supplied as a business label or code | Coterminate meaning or lookup code | /crmRestApi/resources/latest/fndStaticLookups?fields=LookupCode,Meaning&finder=LookupTypeIsActiveEnabledFinder;BindLookupType=ORA_OSS_CO_TERM&onlyData=true | LookupCode; Meaning | Match the supplied Coterminate meaning or code to exactly one active enabled ORA_OSS_CO_TERM lookup. | CoTerminate: LookupCode | Stop and ask for one valid value. Active values are NO for Do not coterminate and LATEST_END_DATE for Latest end date. |

## Lookup Execution Rules

| Task Code | Task Name | Situation | What Happens |
|---|---|---|---|
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | The describe request is unauthorized or the response cannot be read | Stop before REST payload preparation. Do not infer the schema. |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | The supplied Coterminate value does not resolve to one active enabled lookup | Stop before loader-artifact preparation and request a valid Coterminate code or meaning. |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | RT.DESCRIBE_SCHEMA | decision | 20 | reference_lookup | resolved->RT.RESOLVE_COTERMINATE;blocked->RETURN_ISSUES;failed->RETURN_ISSUES | RT.VALIDATE_INPUT | stop | A REST operation is planned |
| CUSTOM_MANAGE_RENEWAL_TEMPLATES | Manage Renewal Templates | RT.RESOLVE_COTERMINATE | decision | 22 | reference_lookup | resolved->RT.APPLY_DEFAULTS;blocked->RETURN_ISSUES;failed->RETURN_ISSUES | RT.DESCRIBE_SCHEMA | stop | A renewal template request supplies a Coterminate value |
