# Subscription Profile Error Handling

Source: Oracle REST API, Get all subscription profiles.

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | The subscription-profile GET request fails | Stop, preserve a redacted status and error summary, and do not retry automatically |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | The Bill Service lookup request fails or does not return exactly one matching LookupCode | Stop, preserve a redacted status and error summary, and do not substitute a label |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | An exact profile-name lookup returns multiple rows | Stop and request a disambiguating identifier, such as SubscriptionProfilePuid |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | A direct REST create contract is requested | Block the direct REST write and use the default core.data-loader route for the registered subscriptionProfiles business object |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | The subscription-validations GET request fails | Stop, preserve a redacted status and error summary, and do not retry automatically |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | The notification-templates GET request fails | Stop, preserve a redacted status and error summary, and do not retry automatically |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | The notification-template detail GET request fails, or TemplateSetNumber is missing or ambiguous | Stop, preserve a redacted status and error summary, and request one exact TemplateSetNumber; do not retry automatically |

## Error Classifications

| Task Code | Task Name | Result Category | When Used | Next Action |
|---|---|---|---|---|
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | Lookup failed | GET request cannot be completed | Report the redacted failure and stop |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | Bill Service lookup unresolved | A nonblank BillService code has no unique matching LookupCode | Report the unresolved code and stop |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | Ambiguous | Exact name resolves to multiple profiles | Request SubscriptionProfilePuid |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | Direct REST write blocked | A create, update, or delete request attempts to use a direct REST payload | Use core.data-loader and its immutable preview and approval workflow |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | Lookup failed | GET request cannot be completed | Report the redacted failure and stop |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | Lookup failed | GET request cannot be completed | Report the redacted failure and stop |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | Detail lookup blocked | TemplateSetNumber is missing or does not identify exactly one template | Request the exact TemplateSetNumber and stop |

## Disclosure Rules

| Task Code | Task Name | Gate | What Must Be Shown |
|---|---|---|---|
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | Profile lookup result | PUID, name, default or selected requested fields, count, hasMore, limit, and offset |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | Validation lookup result | Object, message, severity, enabled, count, hasMore, limit, and offset; show the first 25 rows unless all rows were explicitly requested |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | Notification-template lookup result | Accessible notification-template records and collection pagination metadata when returned |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | Notification-template detail lookup result | Template, Condition, Message, and Message Attachments tables in the Detail Display Format; show blank values as — and omit technical IDs, GUIDs, audit fields, links, and opaque change indicators unless explicitly requested |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | Writable REST behavior is not documented by the supplied source | Do not create a direct REST payload, mutation node, or retry policy; use core.data-loader for creation or import |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | Writable REST behavior is not documented by the supplied source | Do not create a direct REST payload, mutation node, or retry policy; use the approved Data Loader workflow for updates only |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | A create operation is requested | Do not prepare, validate, or submit a create source; explain that subscription-validation creates are not allowed |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | A delete operation is requested | Do not prepare, validate, or submit a delete source; explain that subscription-validation deletes are not allowed |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | Writable REST behavior is not documented by the supplied source | Do not create a direct REST payload, mutation node, or retry policy; use core.data-loader for creation or import |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | SUBPROFILE.DONE | terminal | 20 | terminal | none | SUBPROFILE.BILL_SERVICE | stop | The profile lookup returned one or more rows and their Bill Service values were resolved or skipped when blank |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | SUBPROFILE.EMPTY | terminal | 30 | terminal | none | SUBPROFILE.LIST | stop | The profile lookup returned no rows |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | SUBPROFILE.ISSUES | terminal | 40 | terminal | none | none | stop | The profile lookup failed or an exact name was ambiguous |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | SUBVALID.DONE | terminal | 20 | terminal | none | SUBVALID.LIST | stop | The validation lookup returned one or more rows |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | SUBVALID.EMPTY | terminal | 30 | terminal | none | SUBVALID.LIST | stop | The validation lookup returned no rows |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | SUBVALID.ISSUES | terminal | 40 | terminal | none | none | stop | The validation lookup failed |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | NOTIFICATION.DONE | terminal | 20 | terminal | none | NOTIFICATION.LIST | stop | The notification-template lookup returned one or more rows |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | NOTIFICATION.DETAIL_DONE | terminal | 25 | terminal | none | NOTIFICATION.DETAIL | stop | The notification-template detail lookup returned the identified template and its children |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | NOTIFICATION.EMPTY | terminal | 30 | terminal | none | NOTIFICATION.LIST | stop | The notification-template lookup returned no rows |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | NOTIFICATION.ISSUES | terminal | 40 | terminal | none | none | stop | The notification-template lookup failed |
