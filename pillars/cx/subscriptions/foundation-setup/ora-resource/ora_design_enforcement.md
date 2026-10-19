# Subscription Profile Design Enforcement

Source: Oracle REST API subscriptionProfiles describe metadata and user-supplied creation policy.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Navigate to Subscription Profiles | Open Subscription Management, Subscription Configuration, Manage Subscription Rules, Subscription Profiles, then Create |
| 2 | Define the profile | Enter the input-required profile name, period start, and period type; retain additional supplied attributes without requiring optional values |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | Selecting Bill service | Blocking | | Bill service is selected at product level | Restrict Bill service to subscription-header use | No |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | Preparing a Data Loader update | Blocking | | QaCheckId is supplied or MessageName is blank | Omit QaCheckId and use MessageName as the update key | No |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | Preparing a Data Loader create | Blocking | | The requested operation is create | Create operations are not permitted for subscription validations | No |
| CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS | Manage Subscription Validations | Preparing a Data Loader delete | Blocking | | The requested operation is delete | Delete operations are not permitted for subscription validations | No |
