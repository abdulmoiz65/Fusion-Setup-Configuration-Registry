# Observed Setup-Assistant State Branches

Use this reference after every read-only assistant-status discovery request, including the immediate post-initialization lookup and an explicit status refresh. It records the response shape observed in the connected Fusion environment and limits this skill to behavior supported by the verified direct API contract. Treat assistant `Status` and Company Profile `IsDataExisting` as read-only values for discovery and branching. Use the same customer-facing status outcome for the same observed assistant state across both lookup paths, except that post-initialization `SETUP_NOT_DONE` continues to Company Profile input collection. The only permitted write is the governed final submission transition of assistant `Status` to `SUBMITTED`; never write `IsDataExisting` or make any other `Status` change.

## State Sources

| Source | Fields to use | Supported use case |
|---|---|---|
| Assistant | `Id`, `Name`, `Status` | Identify the selected assistant and determine overall completion state. |
| Company Profile | `Id`, `IsDataExisting`, `Addressline`, `BusinessUnit`, `CompanyName`, `CorporateCurrency`, `Country`, `EnterpriseName`, `LegalEntity`, `OfferingName`, `TaxRegNumber` | Assess existing-data state and update only the validated company-information fields. `Addressline` is Legal Address Address Line 1 only; do not use it to collect a complete postal address. `CompanyName` is the unique CPQ Company Identifier / CPQ Company Name; `EnterpriseName` is the Fusion Enterprise Name. Translate the returned state before showing it to the user. |
| CPQ Users | Collection presence and user ID | Reconcile requested administrators and prevent duplicates. In this Setup Assistant contract, every returned `CPQUsers` record represents a CPQ administrator. |
| CPQ Role Mappings | `Id`, `ResourceRoleName`, `RoleCommonNameCode` | Review seeded CPQ role mappings without changing them. |
| CPQ Starter Data Import | Child-record presence and ID | Report starter-data readiness only; do not import or alter starter data. |
| Setup Progress | `TaskCode`, `TaskName`, `TaskOrder`, `Active`, `TaskStatus`, `TaskStatusCode`, `ErrorMessage` | Monitor only CPQ-owned tasks and the Company Information prerequisite; provide sanitized task-level diagnostics. |
| Setup Assistant LOV | Country, Corporate Currency, Legal Entity, Business Unit lists | Retain the complete response internally and validate every selection before a Company Profile update. Ask for the required value first; only on an explicit customer request, show display values for the single relevant LOV category. |

## Branch Rules

| Returned state | Use case | Required behavior |
|---|---|---|
| Assistant status is complete | Status assessment | Report completion and offer this ready-to-use next prompt: `Publish Adaptive Search for oraclecpqo_transaction and oraclecpqo_transactionLine.` Do not submit again. |
| Assistant status is `SETUP_NOT_DONE` before initialization | Setup entry | Obtain initialization approval, initialize once, then rediscover before assessing Company Profile data. |
| Assistant status is complete before initialization | Setup entry | Report completion and stop; do not initialize. |
| Assistant status is `IN_PROGRESS`, `ERROR`, or unknown before initialization | Setup entry | Report the matching customer-facing status outcome and stop; do not initialize. |
| Assistant status is `SETUP_NOT_DONE` after initialization | Post-initialization discovery | Continue to Company Profile input collection. Do not initialize again. |
| Assistant status is `IN_PROGRESS` | Status assessment | Show: “CPQ Setup Assistant is still processing. You can monitor the Run Setup Assistant process in the Schedule Processes UI.” Stop without collecting data or mutating setup. |
| Assistant status is `ERROR` | Status assessment | Show: “CPQ Setup Assistant encountered an error at [affected CPQ setup step]. Review the logs for the Run Setup Assistant ESS job in the Schedule Processes UI. If the issue cannot be resolved, log an Oracle Service Request (SR).” Replace the bracketed step only with the affected task returned by CPQ progress; otherwise say that the affected step could not be determined safely. Stop without mutation. |
| Assistant status is `COMPLETED` | Status assessment | Show: “CPQ setup is already complete.” Then offer this ready-to-use next prompt: `Publish Adaptive Search for oraclecpqo_transaction and oraclecpqo_transactionLine.` Take no further action. |
| Assistant status is unknown | Status assessment | Show: “CPQ setup status could not be determined safely.” Stop before mutation and collect read-only diagnostics. |
| Company Profile `IsDataExisting` is `DOESNT_EXIST` after CPQ initialization | CPQ company setup | Show: “CPQ setup is not done. Continue by providing company details.” If enterprise name, CPQ company identifier, address, country, corporate currency, or applicable tax registration number is already populated, disclose the current values (redacting tax registration number) and ask the user whether to retain or update them before collecting anything else. Collect only missing required values and requested changes. Do not collect Legal Entity or Business Unit; Company Profile Setup creates them. |
| Company Profile `IsDataExisting` is `EXISTS` | Existing-enterprise reconciliation | Show the enterprise name as read-only. Do not collect address or country. Show eligible Legal Entity display values upfront and require a selection from that list; require CPQ company identifier and Business Unit selection. Allow a discovered currency to be updated; require a currency when it is absent. |
| Company Profile `IsDataExisting` is `EXISTS_WITH_BU` | Existing-enterprise reconciliation | Apply the `EXISTS` flow, including the upfront Legal Entity display list and required CPQ company identifier, but show the discovered Business Unit as read-only and do not allow it to be updated. |
| Company Profile has partial or inconsistent enterprise/business-unit data | Company-data reconciliation | Show: “Company setup is incomplete or inconsistent. Resolve the enterprise and business-unit setup before continuing.” Do not infer missing values or PATCH the profile. |
| Company Profile `IsDataExisting` is `PARTIAL` | Existing-data-state reconciliation | Show: “Partial setups are completed and hence unable to proceed.” Stop before collecting changes or PATCH. |
| Company Profile `IsDataExisting` is `ESSJOBALREADYSCHEDULED` | LDAP-job reconciliation | Show: “A Retrieve Latest LDAP Changes or Send Pending LDAP Requests job is active. You must cancel the existing jobs before continuing with Setup Assistant.” Stop before collecting changes or PATCH. |
| Company Profile reports CPQ processing already in progress | Background-job reconciliation | Show: “CPQ background processing is still running. You can monitor the Run Setup Assistant process in the Schedule Processes UI.” Do not initialize or submit again. |
| `CompanyProfiles` is absent, empty, or ambiguous | Company-information configuration | Stop before PATCH; do not construct a Company Profile URL. |
| `CPQUsers` is empty | CPQ-administrator provisioning | When a legal entity and business unit are available, first ask whether the current logged-in user should be an administrator, then ask whether additional administrators should be added. Collect and validate each requested user's details, require at least one approved administrator, create each approved user, then rediscover. |
| `CPQUsers` already contains one or more records and no addition is requested | CPQ-administrator verification | Treat the existing administrator requirement as satisfied because Setup Assistant `CPQUsers` records are CPQ administrators. Do not create a duplicate; reconcile the existing user state before submission. |
| A requested administrator already exists as a CPQ administrator | Duplicate prevention | Show: “This person is already a CPQ administrator.” Do not create or update the user. |
| A requested administrator already exists with another resource role | Role-conflict handling | Show: “This person already has a different resource role. Review role assignment before changing CPQ setup.” Do not create a duplicate. |
| A requested administrator exists but cannot be reconciled to a resource record | User reconciliation | Show: “An existing user record could not be reconciled to a CPQ resource. Investigate the user and resource records before retrying.” |
| Role mappings are present | Role review | Report the mappings as seeded read-only evidence; no role-mapping mutation is in scope. |
| Starter-data-import child is present | Starter-data assessment | Report presence only; no starter-data write is in scope. |
| Starter-data processing is running | Starter-data monitoring | Show: “CPQ starter-data import is running. Wait and refresh status; do not resubmit.” |
| Starter-data processing completes | Starter-data monitoring | Show: “CPQ starter-data import completed.” Continue with remaining CPQ progress checks. |
| Starter-data processing fails | Starter-data failure | Show a sanitized diagnostic and: “CPQ starter-data import did not complete. Review the diagnostic and resolve the cause before an approved rerun.” Do not resubmit automatically. |
| A CPQ-owned progress task or the Company Information prerequisite is not complete | Progress monitoring | Report the CPQ-relevant task state; do not report CPQ completion. |
| Setup Progress returns an error message | Failure triage | Return the affected CPQ setup step in plain language when returned, plus a sanitized diagnostic. Direct the user to the `Run Setup Assistant` ESS job logs in the Schedule Processes UI; if log review does not resolve the issue, advise logging an Oracle Service Request (SR). Reconcile through reads and do not resubmit automatically. |

## Company-Selection Flow

After initialization and discovery, retrieve the Setup Assistant LOV data before asking for company choices, but retain the complete response internally. Ask the customer for each required value. If the customer explicitly asks for possible values, show only the display values for the requested category (Country, Corporate Currency, Legal Entity, or Business Unit). Do not show the complete response, other LOV categories, identifiers, or record metadata.

| UI-observed condition | Customer interaction | Validation and write behavior |
|---|---|---|
| `DOESNT_EXIST` with no populated configurable Company Profile fields | Ask for enterprise name, CPQ company identifier, Legal Address Address Line 1, country, and corporate currency. | Enterprise name, CPQ company identifier, Address Line 1, country, and corporate currency are required. Address Line 1 must be a single street, building, premises, or locality line, not a complete address. Do not collect city, state/province, postal or PIN code, country text, or additional address lines. Country and currency must be selected from their LOV lists. Do not collect Legal Entity or Business Unit; Company Profile Setup creates them. |
| `DOESNT_EXIST` with one or more populated configurable Company Profile fields | Show each returned value, redacting tax registration number, and ask whether to retain it or provide an update before collecting any missing required values. | A retained value satisfies the corresponding required field. A retained country or currency must be in the current LOV list; otherwise require a replacement. Validate requested changes and PATCH only changed fields. Do not collect Legal Entity or Business Unit; Company Profile Setup creates them. |
| `EXISTS` | Show enterprise name as read-only. Do not ask for address or country. Show eligible Legal Entity display values upfront, then require CPQ company identifier and selection of Legal Entity and Business Unit. | CPQ company identifier is required and must pass its UI validation. Accept Legal Entity and Business Unit only from the current LOV lists. Allow currency to be updated when present; require it when absent. |
| `EXISTS_WITH_BU` | Apply the `EXISTS` flow, including the upfront Legal Entity display list and required CPQ company identifier, but show the discovered Business Unit as read-only. | Do not offer a Business Unit replacement. CPQ company identifier is required and must pass its UI validation. Accept Legal Entity and currency only from the current LOV lists. |
| New company setup with Brazil selected as country | Ask for tax registration number in addition to the new-company fields. | Tax registration number is required only for this country branch. |
| Partial or inconsistent company setup | Explain the issue and stop. | Do not show a selection list as a workaround and do not PATCH the profile. |

Validate only changed fields and send only those changes. Before PATCH, show the selected legal entity, business unit, company fields, and redacted administrator details in the exact change summary; require explicit approval for that exact summary.

## CPQ Administrator Input Rules

For an initial CPQ setup, first ask whether the current logged-in user should be created as a CPQ administrator. If yes, collect that user's first name, last name, and valid email address; do not assume session identity details. Then ask whether additional administrators should be added and, if yes, collect first name, last name, and valid email address for each. Require at least one existing `CPQUsers` record or one approved, validated proposed administrator. Do not accept duplicate email addresses within the requested administrator list or an email already returned by CPQ user discovery. If an existing `CPQUsers` record satisfies the requirement and no addition is requested, do not create a user; reconcile the existing state before submission. For a later setup iteration, retain discovered administrators unless the customer explicitly requests a supported change.

## Customer-Facing Status Messages

Do not display raw status values, task codes, job names, or implementation constants. The sole approved exception is the customer-facing label `Run Setup Assistant` in the post-submission tracking guidance below. Use these messages in execution output; retain raw values only in a protected diagnostic record when needed for support.

| Condition | Message to show | Next action |
|---|---|---|
| All CPQ-owned progress tasks are complete | “CPQ Setup Assistant is complete.” Then offer this ready-to-use next prompt: `Publish Adaptive Search for oraclecpqo_transaction and oraclecpqo_transactionLine.` | No submission or rerun. |
| One or more CPQ-owned tasks are incomplete | “CPQ setup is not complete yet.” | Show the named CPQ task and its safe next action. Do not poll, submit, or resubmit automatically. |
| Assistant was initialized and is awaiting configuration | “CPQ setup has been initialized and is ready for company profile and administrator configuration.” | Rediscover, validate, then request approval for any change. |
| Setup submission or a CPQ background task is in progress | “CPQ Setup Assistant is still processing. It typically completes in approximately 12–15 minutes.” | The user can track progress in the Schedule Processes UI by monitoring the `Run Setup Assistant` process. Do not poll, submit, or resubmit automatically. |
| Setup reports an error | “CPQ Setup Assistant encountered an error at [affected CPQ setup step]. Review the logs for the Run Setup Assistant ESS job in the Schedule Processes UI. If the issue cannot be resolved, log an Oracle Service Request (SR).” | Replace the bracketed step only with the affected task returned by CPQ progress; otherwise say that the affected step could not be determined safely. Show a sanitized diagnostic, reconcile state, and do not submit or resubmit. |
| Status request times out or fails, or returned state is missing, contradictory, or unknown | “CPQ setup status could not be determined safely.” | Stop mutations, retain sanitized diagnostics when available, do not infer completion, and require a new user-triggered read-only status refresh. |

## CPQ Progress Scope

Use these returned task codes when assessing CPQ Setup Assistant progress:

| Scope | Task code | Task name |
|---|---|---|
| Company Profile prerequisite | `SA_COMPANY_INFORMATION` | Company Information |
| CPQ administrator | `SA_CPQ_ADMIN_USERS` | Application Administrators |
| CPQ starter data | `SA_CPQ_REFDATA_IMPORT` | Import of Starter Data |
| CPQ resource roles | `SA_CPQ_RESOURCE_ROLES` | Resource Roles and Role Mappings |

Do not use accounting calendar, geographies, sales hierarchy, sales catalog, generic resource roles, opportunities, competitors, sales setup users, forecasting, or adaptive search as CPQ Setup Assistant completion criteria. Those are Sales Setup Assistant progress tasks returned by the shared response.
