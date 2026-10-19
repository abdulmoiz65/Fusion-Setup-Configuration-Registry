# Manage SMS Configuration Dependency Readiness

The supplied Manage SMS Configuration export and nested task metadata establish the supported parent-row FSM import contract. Keep only dependencies that affect provider creation. The parent-row import does not require active-provider readback, provider credentials, or provider tests. When activation is requested, successful creation is followed by a manual activation handoff in Manage SMS Configuration.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | FSM import contract | Confirm the task metadata and supplied export identify ORA_IRC_EMP_CAMP_SMS_CONFIG as an FSM CSV import |
| 2 | Provider-account readiness | Require provider-account readiness only when credentials or provider tests are requested |
| 3 | Post-creation activation handoff | When activation is requested, create the provider first; after successful creation, direct the user to Manage SMS Configuration to deactivate any currently active SMS configuration, activate the created configuration, and verify exactly one configuration is active |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| SMS-FSM-IMPORT-CONTRACT | Manage SMS Configuration FSM import contract | Yes | A provider-account CSV import is prepared | Satisfied | Nested task metadata plus the supplied Manage SMS Configuration export and ASM_SETUP_CSV_METADATA.xml | | Confirms the task code, exported parent-row schema, and FSM Data Loader route | Preserve the exported archive structure and route it through core Data Loader | TaskCode: ORA_IRC_EMP_CAMP_SMS_CONFIG; DataLoaderImportMode: FSM |
| SMS-PROVIDER-ACCOUNT-READINESS | External SMS provider account readiness | Conditional | Provider credentials or outbound or inbound tests are requested | Blocked | The supplied parent-row export contains no provider credential or test-readiness contract | | Provider tests require provider-account readiness beyond the parent-row create contract | Complete and review the provider-specific account details in Messaging Configuration; never persist provider secrets in FDOS artifacts | Provider identity and readiness evidence |
| SMS-POST-CREATE-ACTIVATION-HANDOFF | Post-creation activation handoff | Conditional | Provider activation is requested with provider creation | Satisfied | User-supplied workflow for the Manage SMS Configuration task | | The FSM archive creates the provider row but has no active-status field; activation must occur in the task after creation and exactly one SMS configuration may be active | After successful creation, go to Manage SMS Configuration, deactivate any currently active SMS configuration, activate the created configuration, and verify exactly one SMS configuration is active | Created AccountName |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The task metadata and export establish the FSM creation contract, and any requested activation uses the documented post-creation handoff | Yes, continue to the remaining preview and approval gates |
| Blocked | A conditional provider credential or test dependency applies but its required contract is absent | No; stop the requested credential or test action |
| Not Applicable | Credentials, provider tests, and activation are not requested | Yes, continue without adding an extra dependency step |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SMS.CHECK_DEPENDENCIES | decision | 3 | resolve_dependency | ready->SMS.ENFORCE_SINGLE_ACTIVE;blocked->SMS.HANDLE_ERROR | SMS.DEFAULT_PROVIDER_ID | stop | A validated and defaulted provider request is evaluated against only the dependencies applicable to its requested operation |
