# Manage SMS Configuration Defaulting Rules

The user supplied the task-specific default policy. When values are blank, default the provider to TWILIO, Message Length Limit to 1600, and the provider identifier consistently with the resulting provider. Do not override explicit values; an explicitly supplied conflicting provider identifier is an input-validation error.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ProviderCode | TWILIO | ProviderCode is blank | No | |
| MessageMaxLength | 1600 | Message Length Limit is blank | No | |
| CommProviderId | 1 | ProviderCode is TWILIO and CommProviderId is blank | No | |
| CommProviderId | 2 | ProviderCode is SYNIVERSE and CommProviderId is blank | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SMS.DEFAULT_PROVIDER_ID | step | 2 | apply_default | defaulted->SMS.CHECK_DEPENDENCIES;unchanged->SMS.CHECK_DEPENDENCIES | SMS.VALIDATE_INPUT | stop | A validated request continues; default blank ProviderCode to TWILIO, blank MessageMaxLength to 1600, and blank CommProviderId consistently with the resulting provider; otherwise pass through explicit values unchanged |
