# Subscription Profile Reference Lookups

Source: Oracle REST API, Get all subscription profiles and subscription-profile describe metadata.

The collection lookup shows the subscription profiles defined in the selected
Fusion environment.

## Live Lookups

| Task Code | Task Name | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | list_subscription_profiles | Subscription profiles are listed or an exact supplied profile name is reviewed | Optional SubscriptionProfileName, limit, offset, fields, q, finder, or onlyData. When fields is not supplied, use the default display fields. | GET /crmRestApi/resources/11.13.18.05/subscriptionProfiles | Default display fields: SubscriptionProfilePuid, SubscriptionProfileName, BillService, InvoicingRuleId, TransactionTypeName, BillingFrequency, BillingDateCode, BillingOffsetDays, BillingSystem, AccountingRuleName, PaymentTermsName, PartialPeriodType, PartialPeriodStart | Use q with SubscriptionProfileName when an exact name is supplied; otherwise return the requested collection page. Use finder PrimaryKey only with SubscriptionProfileId. A caller-supplied fields value replaces the default display fields. | PUID from SubscriptionProfilePuid; Name from SubscriptionProfileName; Bill Service from BillService; Invoicing Rule from InvoicingRuleId; Transaction Type from TransactionTypeName; Billing Frequency from BillingFrequency; Billing Date from BillingDateCode; Day or Offset from BillingOffsetDays; Billing System from BillingSystem; Accounting Rule from AccountingRuleName; Payment Terms from PaymentTermsName; Period Type from PartialPeriodType; Period Start from PartialPeriodStart | Return an empty result when no row matches; stop on an ambiguous exact-name result or API failure |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | resolve_subscription_profile_bill_service | A returned subscription-profile row has a nonblank BillService code | SubscriptionProfilePuid, BillService | GET /crmRestApi/resources/11.13.18.05/subscriptionProfiles/{SubscriptionProfilePuid}/lov/BillServiceLookupPVA?fields=LookupCode,Meaning | LookupCode, Meaning | Require exactly one item whose LookupCode equals the profile BillService code. The describe metadata maps LookupCode to BillService and declares Meaning as the display attribute. | Bill Service code from LookupCode; Bill Service display value from Meaning | Skip the lookup when BillService is blank; otherwise stop on no match, multiple matches, or an API failure |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | list_subscription_validations | Subscription validations are listed or reviewed | Optional fields, limit, offset, and allRows | GET /crmRestApi/resources/latest/subscriptionValidations | Default UI fields: ValObjMeaning, MessageText, SeverityMeaning, EnabledFlag | When allRows is absent or false, request offset 0 and limit 25. When allRows is true, follow collection pages until hasMore is false. A caller-supplied fields value replaces the default UI fields. | Object from ValObjMeaning; Message from MessageText; Severity from SeverityMeaning; Enabled from EnabledFlag | Return an empty result when no rows are present; stop on API failure |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | list_notification_templates | Notification templates are listed | None | GET {{baseUrl}}/crmRestApi/resources/latest/notificationTemplates | All fields returned by the collection response | Return the accessible collection without inferring filters or field mappings not supplied in the endpoint contract. | Accessible notification-template records and collection pagination metadata when returned | Return an empty result when no rows are present; stop on API failure |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | show_notification_template_detail | Details are requested for one identified notification template | Exact TemplateSetNumber, supplied by the requester or returned by list_notification_templates | GET {{baseUrl}}/crmRestApi/resources/latest/notificationTemplates/{TemplateSetNumber}?onlyData=true&expand=NotificationTmplEvents,NotificationTmplEvents.NotificationTmplMessages,NotificationTmplEvents.NotificationTmplMessages.NotificationTmplAttachments | Parent template fields plus NotificationTmplEvents, NotificationTmplMessages, and NotificationTmplAttachments | Use the exact TemplateSetNumber as the URL path segment. Do not add filters, fields, expansions, or mutations beyond this declared request. | Return the parent template and its event, message, and attachment children in the Detail Display Format below. | Stop when the TemplateSetNumber is absent, ambiguous, or the detail request fails. |

## Lookup Execution Rules

| Task Code | Task Name | Situation | What Happens |
|---|---|---|---|
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | A profile collection request has more results | Return count, hasMore, limit, and offset so the next page can be requested |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | A REST request uses both fields and expand | Use fields; the documented REST API gives fields precedence |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | A profile collection request omits fields | Use the default display fields and present them as the PUID and UI-aligned columns defined in the lookup output mapping |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | A returned profile has a nonblank BillService code | Resolve the BillService code through resolve_subscription_profile_bill_service and display Meaning instead of the code |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | A validation collection request does not explicitly request all rows | Return the first 25 rows and report count, hasMore, limit, and offset |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | A validation collection request explicitly requests all rows | Follow every page and return all rows |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | A validation collection request omits fields | Use the default UI columns Object, Message, Severity, and Enabled |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | A notification-template collection request is made | Use GET {{baseUrl}}/crmRestApi/resources/latest/notificationTemplates without adding undocumented filters, fields, or mutations |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | A notification-template detail request is made | Use show_notification_template_detail only with one exact TemplateSetNumber and render the response with the Detail Display Format. |

## Detail Display Format

For a notification-template detail request, render the returned parent and each
child level as separate Markdown tables in this order. Use the labels and
column order below to mirror the Event Notification Rules and Templates Set
page. Render null or blank values as `—`; do not display technical IDs,
GUIDs, audit fields, links, or opaque change indicators unless the requester
explicitly asks for them.

### Template

| Template Name | Description | Sender Email Address | Start Date | End Date |
|---|---|---|---|---|

### Condition

| Event | Days Before Subscription Start Date | Applicable For | Notification Type | Customer Acceptance Required | Communication Channel |
|---|---|---|---|---|---|

### Message: {EventCodeName}

Render one table for each returned event that has messages.

| Free-Form | Language | Message Template | Message Subject | Start Date | End Date |
|---|---|---|---|---|---|

### Message Attachments: {MessageTemplate}

Render one table for each returned message that has attachments.

| Subscription Contract Layout Template | Attachment Name | Start Date | End Date | Default |
|---|---|---|---|---|

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | SUBPROFILE.LIST | step | 10 | reference_lookup | returned->SUBPROFILE.BILL_SERVICE;empty->SUBPROFILE.EMPTY;issues->SUBPROFILE.ISSUES | none | stop | Listing subscription profiles or reviewing an exact supplied profile name |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | SUBPROFILE.BILL_SERVICE | step | 15 | reference_lookup | resolved->SUBPROFILE.DONE;skipped->SUBPROFILE.DONE;issues->SUBPROFILE.ISSUES | SUBPROFILE.LIST | stop | Resolving the Bill Service display value for each returned profile with a nonblank BillService code |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | SUBVALID.LIST | step | 10 | reference_lookup | returned->SUBVALID.DONE;empty->SUBVALID.EMPTY;issues->SUBVALID.ISSUES | none | stop | Listing or reviewing subscription validations |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | NOTIFICATION.LIST | step | 10 | reference_lookup | returned->NOTIFICATION.DONE;detail_requested->NOTIFICATION.DETAIL;empty->NOTIFICATION.EMPTY;issues->NOTIFICATION.ISSUES | none | stop | Listing notification templates |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | NOTIFICATION.DETAIL | step | 15 | reference_lookup | returned->NOTIFICATION.DETAIL_DONE;issues->NOTIFICATION.ISSUES | NOTIFICATION.LIST | stop | Showing details for one identified notification template and its children |
