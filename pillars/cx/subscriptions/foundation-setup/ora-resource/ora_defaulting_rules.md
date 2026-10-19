# Subscription Profile Defaulting Rules

Source: Oracle REST API, Get all subscription profiles.

## Standard Defaults

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | BillFirstPartialPeriodOption | ORA_PRORATE | Reviewing a REST profile representation that does not supply a value | Yes | |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | BillLastPartialPeriodOption | ORA_PRORATE | Reviewing a REST profile representation that does not supply a value | Yes | |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | EnableAdvBipTemplateFlag | false | Reviewing a REST profile representation that does not supply a value | Yes | |
| CUSTOM_MANAGE_SUBSCRIPTION_PROFILES | Manage Subscription Profiles | HeaderNumberingMethod | ORA_PUID | Reviewing a REST profile representation that does not supply a value | Yes | |
