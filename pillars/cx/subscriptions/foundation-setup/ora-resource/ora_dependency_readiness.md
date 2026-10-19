# Subscription Profile Dependency Readiness

Source: Oracle REST API subscriptionProfiles describe metadata and user-supplied creation policy.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Subscription Management access | Sign in as a setup user and open Subscription Management |
| 2 | Subscription configuration navigation | Open Subscription Configuration, then Manage Subscription Rules and Subscription Profiles when a profile needs further setup |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | SUBPROFILE.SETUP_ACCESS | Subscription Management setup-user access | Yes | Creating a subscription profile | Verify | Oracle setup UI | | The documented creation flow starts in Subscription Management | Sign in as a setup user before continuing | |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|---|
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | Missing | Required setup access is unavailable | No |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | Satisfied | Documented setup access and required selections are present | No |
