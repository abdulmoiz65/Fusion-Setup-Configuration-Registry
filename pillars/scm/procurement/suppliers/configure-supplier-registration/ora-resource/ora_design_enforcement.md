# Configure Supplier Registration Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Flow scope | Select the prospective, spend authorized, or both registration flows in scope |
| 2 | Profile design | Configure only the documented profile components and their supported Enabled, Required, or Hidden state for each in-scope flow, observing component-specific restrictions |
| 3 | Registration controls | Set changed Internal Registration and Self Service Procurement defaults, source-specific supplier-identifier requirements, company-details or bank-account attachment requirements, and post-approval site assignments deliberately |
| 4 | External registration URL control | Treat external-registration URL encryption-key regeneration as a separately approved action because it expires existing registration URLs |
| 5 | Shared singleton coordination | When this task changes supplierOptions in the same runbook as the other shared tasks, require a fresh singleton lookup, exclusive field ownership, and serial execution. |
| 6 | Shared entity-configuration coordination | When Configure Supplier Profile Change Request also changes supplierEntityConfigurations, require a fresh entity lookup and exclusive attribute ownership. |
| 7 | Mutation route | Preview and apply changes through core.data-loader using the ordered registered business objects: supplierEntityConfigurations, then supplierOptions |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A registration flow is configured | Error |  | No prospective or spend-authorized flow is identified | State the business relationship for each intended flow | Yes |
| A profile component is configured | Error |  | The component state is absent, unsupported for that component, or attempts to change Organization Details or Contacts from this page | Use Enabled, Required, or Hidden only where the setup page permits it; use Enabled or Hidden for Qualifications Questionnaire, Enabled or Required for Contact User Account, and retain Organization Details and Contacts as displayed | Yes |
| An attachment rule is configured | Error |  | The attachment type or supported relationship scope is ambiguous | Identify company-details or bank-account attachments and the applicable relationship | Yes |
| External-registration URL encryption-key regeneration is requested | Error |  | Explicit approval to expire existing registration URLs is absent | Stop before the action and obtain explicit approval for the target environment and its URL impact | Yes |
| A shared supplierOptions runbook task is prepared | Error | read_registration_supplier_options | The lookup does not resolve exactly one current row, another participating task proposes a different final value for the same attribute, or the lookup predates an earlier successful shared task | Resolve the conflict, re-read the singleton, and prepare only this task's owned fields through its Data Loader REST route | Yes |
| A shared supplierEntityConfigurations row is prepared | Error | read_registration_entity_configurations | The proposed artifact includes profile-change attributes or was prepared from a row read before Configure Supplier Profile Change Request completed | Re-read the row and include only RegistrationProspectiveCode and RegistrationSpendAuthorizedCode through core.data-loader | Yes |
| A mutation is prepared | Error |  | The proposed write does not use the ordered registered Data Loader business objects | Use core.data-loader only; do not invoke an ADF REST create, update, PATCH, or custom action directly | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| read_registration_supplier_options | Before preparing a supplierOptions-backed registration setting in a shared runbook | SupplierOptionsConfigId and current task-owned supplierOptions values | ora_reference_lookups.md |
| read_registration_entity_configurations | Before preparing a registration entity configuration change in a shared runbook | SupplierProfileEntityId and current registration-owned entity values | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POZ.SR.ENFORCE_DESIGN | decision | 30 | design_enforcement | passed->POZ.SR.EXECUTION_GATE;blocked->POZ.SR.HANDLE_ERROR | POZ.SR.READ_ENTITY_CONFIGURATIONS | stop | Before Data Loader preview |
