# Configure Supplier Registration Reference Lookups

## ADF REST Object Guidance

| Functional Activity | ADF REST Object | Guidance |
|---|---|---|
| Read registration entity configuration | GET /fscmRestApi/resources/11.13.18.05/supplierEntityConfigurations | Resolve the applicable entity and read SupplierProfileEntityId, SupplierProfileEntityCode, SupplierProfileEntity, RegistrationProspectiveCode, and RegistrationSpendAuthorizedCode. |
| Read registration options | GET /fscmRestApi/resources/11.13.18.05/supplierOptions | Resolve the SupplierOptionsConfigId and read only the supplierOptions fields owned by this task. |

## Shared Collection Ownership

| Collection | This Task Owns | Other Task Ownership | Shared-row Rule |
|---|---|---|---|
| supplierEntityConfigurations | RegistrationProspectiveCode, RegistrationSpendAuthorizedCode | Configure Supplier Profile Change Request owns InternalChangeMgmtCode, SupplierInitiatedChangeMgmtProspectiveCode, and SupplierInitiatedChangeMgmtSpendAuthorizedCode | Re-read the current row after either task completes; prepare only this task's owned attributes in the Data Loader artifact. |
| supplierOptions | AutoCreateSiteAssignmentFlag, ExternalRegBankAccAttachmentsRequiredFlag, ExternalRegCompanyDetailsAttachmentsRequiredCode, ExternalRegSuccessMessage, ExternalRegSupplierIdRequiredFlag, ExternalRegWelcomeMessage, InternalRegSupplierBusRelationDefaultCode, InternalRegSupplierIdRequiredFlag, SourcingSupplierBusRelationDefaultCode, SourcingSupplierIdRequiredFlag, SSPSupplierBusRelationDefaultCode, SSPSupplierIdRequiredFlag | Configure Supplier Profile Change Request owns InternalChangeBankAccAttachmentsRequiredFlag and SupplierPortalChangeBankAccAttachmentsRequiredFlag; Configure Supplier Notifications owns NotifyPriorToExpirationDays and ReminderFrequencyDays | Resolve exactly one shared singleton, run the tasks serially, re-read after either task completes, and prepare only this task's owned attributes in the Data Loader artifact. |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| read_registration_supplier_options | Before preparing a supplierOptions-backed registration setting in a shared runbook | None | ADF REST GET Supplier Options collection | SupplierOptionsConfigId, AutoCreateSiteAssignmentFlag, ExternalRegBankAccAttachmentsRequiredFlag, ExternalRegCompanyDetailsAttachmentsRequiredCode, ExternalRegSuccessMessage, ExternalRegSupplierIdRequiredFlag, ExternalRegWelcomeMessage, InternalRegSupplierBusRelationDefaultCode, InternalRegSupplierIdRequiredFlag, SourcingSupplierBusRelationDefaultCode, SourcingSupplierIdRequiredFlag, SSPSupplierBusRelationDefaultCode, SSPSupplierIdRequiredFlag | Return exactly one seeded Supplier Options configuration. | Resolved singleton key and current registration-owned values | Stop on zero rows or multiple rows; the seeded row must be corrected outside this task, and this task must not create a row. |
| read_registration_entity_configurations | Before preparing a registration entity configuration change and after Configure Supplier Profile Change Request completes | SupplierProfileEntityId | GET /fscmRestApi/resources/11.13.18.05/supplierEntityConfigurations | SupplierProfileEntityId, SupplierProfileEntityCode, SupplierProfileEntity, RegistrationProspectiveCode, RegistrationSpendAuthorizedCode | Match the supplied SupplierProfileEntityId exactly once. | Current entity configuration and registration-owned values | Stop on zero rows or multiple rows; do not select or create a row. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| This task follows another successful shared supplierOptions task | Re-run the read-only lookup before artifact preparation and retain only this task's approved field changes. |
| Configure Supplier Profile Change Request completed first | Re-run read_registration_entity_configurations before artifact preparation and retain only RegistrationProspectiveCode and RegistrationSpendAuthorizedCode. |
| Configure Supplier Profile Change Request completed first and this task changes supplierOptions | Re-run read_registration_supplier_options before artifact preparation and retain only the registration-owned supplierOptions attributes. |
| The lookup resolves exactly one configuration | Use the returned configuration only as current-state evidence for the Data Loader artifact and post-load verification. |
| The lookup returns zero rows or multiple rows | Stop before Data Loader processing; treat the seeded singleton as missing or inconsistent, and do not introduce a bootstrap, create, or substitute-key path. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POZ.SR.READ_SHARED_SUPPLIER_OPTIONS | step | 25 | reference_lookup | resolved->POZ.SR.READ_ENTITY_CONFIGURATIONS;not_found->POZ.SR.HANDLE_ERROR;ambiguous->POZ.SR.HANDLE_ERROR;failure->POZ.SR.HANDLE_ERROR | POZ.SR.APPLY_DEFAULTS | stop | This task changes a supplierOptions-backed setting in a shared runbook |
| POZ.SR.READ_ENTITY_CONFIGURATIONS | step | 27 | reference_lookup | resolved->POZ.SR.ENFORCE_DESIGN;not_found->POZ.SR.HANDLE_ERROR;ambiguous->POZ.SR.HANDLE_ERROR;failure->POZ.SR.HANDLE_ERROR | POZ.SR.READ_SHARED_SUPPLIER_OPTIONS | stop | Before preparing a supplierEntityConfigurations change or after Configure Supplier Profile Change Request completes |
