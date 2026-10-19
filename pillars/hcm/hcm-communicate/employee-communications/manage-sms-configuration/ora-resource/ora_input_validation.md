# Manage SMS Configuration Input Validation

Manage SMS Configuration FSM Task — ORA_IRC_EMP_CAMP_SMS_CONFIG.

The supplied HCM Communicate export contains the parent object ORA_IRC_EMP_CAMP_SMS_CONFIG with ProviderCode, AccountName, AccountDescription, MessageMaxLength, CommProviderId, and CommAccountType. It confirms TWILIO with CommProviderId 1, SYNIVERSE with CommProviderId 2, and ORA_HCM_COMMUNICATE as the task scope. One exported row has a blank AccountDescription, so description is optional for this validation contract.

## Exported CSV Schema

| Object | CSV Fields and Metadata Types | Source Boundary |
|---|---|---|
| ORA_IRC_EMP_CAMP_SMS_CONFIG | ProviderCode string; AccountName string; AccountDescription string; MessageMaxLength int; CommProviderId long; CommAccountType string | Validate only the supplied parent-row contract; do not infer active status, child-request configuration, tests, footer settings, credentials, or provider lifecycle state from this CSV |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Provider account row | ProviderCode after defaulting; AccountName; MessageMaxLength after defaulting; CommProviderId after conditional defaulting; CommAccountType | Stop import preparation for the affected row | Supply the missing value or allow the documented provider, message-length, and provider-identifier defaults to apply | A provider account row is prepared | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| ProviderCode is blank | Ready | Set ProviderCode to TWILIO through the defaulting rule | |
| MessageMaxLength is blank | Ready | Set MessageMaxLength to 1600 through the defaulting rule | |
| ProviderCode is TWILIO and CommProviderId is blank | Ready | Set CommProviderId to 1 through the conditional default | |
| ProviderCode is SYNIVERSE and CommProviderId is blank | Ready | Set CommProviderId to 2 through the conditional default | |
| ProviderCode is TWILIO and a supplied CommProviderId is not 1 | Blocked | Correct CommProviderId to 1 or remove it so the default can apply | |
| ProviderCode is SYNIVERSE and a supplied CommProviderId is not 2 | Blocked | Correct CommProviderId to 2 or remove it so the default can apply | |
| Required provider account values are present and valid | Ready | Continue to dependency readiness for the requested operation | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| ProviderCode | Accept TWILIO or SYNIVERSE | A provider account row is prepared | |
| AccountName | Require a nonblank value | A provider account row is prepared | |
| AccountDescription | Accept blank or supplied text | A provider account row is prepared | |
| MessageMaxLength | Require a non-negative whole number using the exported int shape | A provider account row is prepared | |
| CommProviderId | Require the exported long shape after defaulting; use 1 only with TWILIO and 2 only with SYNIVERSE | A provider account row is prepared | |
| CommAccountType | Require ORA_HCM_COMMUNICATE | A provider account row is prepared | |

## Post-Action Validation

| Action | Source-Backed Check | If Evidence Is Missing or Fails | Next Action |
|---|---|---|---|
| Provider creation through FSM import | Treat the successful Data Loader creation result as completion of the import | Report the failed, timed-out, or uncertain process result and stop | When activation was requested, output: Creation succeeded. Go to Manage SMS Configuration, open the created configuration, deactivate any currently active SMS configuration, activate the created configuration, and verify exactly one SMS configuration is active |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SMS.VALIDATE_INPUT | decision | 1 | validate_input | valid->SMS.DEFAULT_PROVIDER_ID;invalid->SMS.HANDLE_ERROR | none | stop | A parent provider-account CSV row is reviewed |
| SMS.EVALUATE_RESULT | decision | 6 | evaluate_result | successful->SMS.RETURN_SUCCESS;failed_or_uncertain->SMS.HANDLE_ERROR | SMS.EXECUTION_GATE | stop | The Data Loader provider-creation process reaches a terminal or uncertain status |
