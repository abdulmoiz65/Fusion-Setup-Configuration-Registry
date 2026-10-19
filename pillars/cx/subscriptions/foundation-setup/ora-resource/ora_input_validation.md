# Subscription Profile Input Validation

Source: Oracle REST API subscriptionProfiles describe metadata.

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | Profile identity | Profile Name | Stop profile-creation preparation | Provide the profile name in Subscription Management | Creating a subscription profile | |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | Billing period | Period Start and Period Type | Stop profile-creation preparation | Select both period values before continuing | Creating a subscription profile | |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | Existing validation identity | MessageName | Stop update preparation | Provide the existing validation MessageName | Updating a subscription validation record | |

## Field Validation

| Task Code | Task Name | Check | What Happens | Applies When | Resolver |
|---|---|---|---|---|---|
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | User-supplied attributes | Require only SubscriptionProfileName, PartialPeriodType, and PartialPeriodStart because they are marked inputRequired in the describe metadata; retain any additional supplied attributes unchanged | Creating a subscription profile | |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | Billing service level | Do not use Bill service at product level | Selecting Bill service | |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | Validation check identifier | Never pass QaCheckId; MessageName is the Data Loader key for updates. | Updating a subscription validation record | |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | Field types and mutability | MessageName, ValidationObject, and ErrorSeverity are strings with maximum length 30; EnabledFlag is boolean; MandatoryFlag has maximum length 1; MessageText is read-only | Preparing or reviewing a subscription validation record | |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | Notification-template creation fields | Require TemplateSetName, SenderEmailAddress, StartDate, and RestAction POST. Leave TemplateSetNumber, TemplateGuid, TemplateSetId, and ObjectVersionNumber blank because Fusion generates them on create. | Preparing a notification-template create source | |
| CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET | Event Notification Rules and Templates Set | Notification-template dates | Format StartDate and EndDate as YYYY-MM-DD, for example 2025-01-01. Do not use slash-formatted dates. | Preparing a notification-template create or update source | |
