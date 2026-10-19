# Configure Supplier Registration Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Registration-flow scope | Prospective Supplier, Spend Authorized Supplier, or both | Block preview | Identify the business relationships whose registration pages are being configured | Always |  |
| Profile-component choice | For each in-scope flow, component name and a supported state: Enabled, Required, or Hidden, subject to component-specific restrictions | Block preview | Specify the intended state for Organization Details, Contacts, Contact User Account, Addresses, Business Classifications, Bank Accounts, Products and Services, or Qualifications Questionnaire | A profile component is configured |  |
| Registration-source default | Internal Registration or Self Service Procurement source and default business relationship | Block preview | Provide Prospective Supplier or Spend Authorized Supplier for each changed source default | An internal-registration or Self Service Procurement default is configured |  |
| Shared supplierOptions coordination | Participating task field ownership and one final value for each overlapping supplierOptions attribute | Block preview | Resolve any overlap before this task is prepared; execute the shared singleton tasks serially. | This task changes a supplierOptions-backed setting in a runbook that also includes Configure Supplier Profile Change Request or Configure Supplier Notifications | read_registration_supplier_options |
| Shared entity-configuration coordination | SupplierProfileEntityId and only registration-owned attributes | Block preview | Re-read the shared entity configuration after Configure Supplier Profile Change Request if it completed first. | A registration entity configuration is changing in the same runbook | read_registration_entity_configurations |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Profile component state | For most editable components, accept Enabled, Required, or Hidden. For Qualifications Questionnaire, accept Enabled or Hidden only. For Contact User Account, accept Enabled or Required only. Organization Details and Contacts are read-only on this setup page; retain their displayed state and do not include them in a change payload. | A component state is supplied |  |
| Registration-source default | Accept only Prospective Supplier or Spend Authorized Supplier for Internal Registration and Self Service Procurement defaults. | A source default is supplied |  |
| Supplier identifier requirement | Require an explicit Yes or No decision independently for External Registration, Internal Registration, and Self Service Procurement. The option requires at least one of D-U-N-S Number, Taxpayer ID, or Tax Registration Number. | An identifier option is configured |  |
| Attachment requirement | Require the attachment type and intended flow. Company-details attachments support prospective, spend authorized, or both; bank-account attachments are an External Registration control. | An attachment requirement is configured |  |
| Site assignment behavior | Require an explicit automatic or manual site-assignment choice | Post-approval behavior is configured |  |
| Registration URL encryption key | Require an explicit approved Yes or No decision before regenerating the external-registration URL encryption key. | URL regeneration is requested |  |
| Shared singleton freshness | Require a fresh read-only supplierOptions lookup after every earlier successful shared-singleton task in the runbook; do not reuse a stale row or merge another task's unapproved fields. | This task changes a supplierOptions-backed setting in a shared runbook | read_registration_supplier_options |
| Seeded singleton operation | Accept only an update to the resolved existing supplierOptions row through this task's approved Data Loader route; reject a create, bootstrap, or delete request. | This task changes a supplierOptions-backed setting | read_registration_supplier_options |
| Shared entity attribute ownership | Accept only RegistrationProspectiveCode and RegistrationSpendAuthorizedCode for supplierEntityConfigurations; reject InternalChangeMgmtCode, SupplierInitiatedChangeMgmtProspectiveCode, and SupplierInitiatedChangeMgmtSpendAuthorizedCode. | A supplierEntityConfigurations change is supplied | read_registration_entity_configurations |
| Shared supplierOptions attribute ownership | Accept only AutoCreateSiteAssignmentFlag, ExternalRegBankAccAttachmentsRequiredFlag, ExternalRegCompanyDetailsAttachmentsRequiredCode, ExternalRegSuccessMessage, ExternalRegSupplierIdRequiredFlag, ExternalRegWelcomeMessage, InternalRegSupplierBusRelationDefaultCode, InternalRegSupplierIdRequiredFlag, SourcingSupplierBusRelationDefaultCode, SourcingSupplierIdRequiredFlag, SSPSupplierBusRelationDefaultCode, and SSPSupplierIdRequiredFlag; reject the Profile Change Request and Configure Supplier Notifications attributes. | A supplierOptions change is supplied | read_registration_supplier_options |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POZ.SR.VALIDATE_INPUT | step | 10 | validate_input | valid->POZ.SR.APPLY_DEFAULTS;invalid->POZ.SR.HANDLE_ERROR | none | stop | Before Data Loader preview |
