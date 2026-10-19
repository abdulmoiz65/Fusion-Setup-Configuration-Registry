# Reference Lookups

## ADF REST Object Guidance

| Functional Activity | ADF REST Object | Guidance |
|---|---|---|
| Read internal profile-management entities | GET /fscmRestApi/resources/11.13.18.05/supplierEntityConfigurations | Resolve the applicable internal-profile entity and read SupplierProfileEntityId, SupplierProfileEntityCode, SupplierProfileEntity, and InternalChangeMgmtCode. |
| Read supplier-initiated profile-management entities | GET /fscmRestApi/resources/11.13.18.05/supplierEntityConfigurations | Resolve the applicable supplier-initiated entity and read SupplierProfileEntityId, SupplierProfileEntityCode, SupplierProfileEntity, SupplierInitiatedChangeMgmtProspectiveCode, and SupplierInitiatedChangeMgmtSpendAuthorizedCode. |
| Read profile-change attachment requirements | GET /fscmRestApi/resources/11.13.18.05/supplierOptions | Resolve the applicable SupplierOptionsConfigId and read InternalChangeBankAccAttachmentsRequiredFlag and SupplierPortalChangeBankAccAttachmentsRequiredFlag. |

## Shared Collection Ownership

| Collection | This Task Owns | Other Task Ownership | Shared-row Rule |
|---|---|---|---|
| supplierEntityConfigurations | InternalChangeMgmtCode, SupplierInitiatedChangeMgmtProspectiveCode, SupplierInitiatedChangeMgmtSpendAuthorizedCode | Configure Supplier Registration owns RegistrationProspectiveCode and RegistrationSpendAuthorizedCode | Re-read the current row after either task completes; prepare only this task's owned attributes in the Data Loader artifact. |
| supplierOptions | InternalChangeBankAccAttachmentsRequiredFlag, SupplierPortalChangeBankAccAttachmentsRequiredFlag | Configure Supplier Registration owns AutoCreateSiteAssignmentFlag, ExternalRegBankAccAttachmentsRequiredFlag, ExternalRegCompanyDetailsAttachmentsRequiredCode, ExternalRegSuccessMessage, ExternalRegSupplierIdRequiredFlag, ExternalRegWelcomeMessage, InternalRegSupplierBusRelationDefaultCode, InternalRegSupplierIdRequiredFlag, SourcingSupplierBusRelationDefaultCode, SourcingSupplierIdRequiredFlag, SSPSupplierBusRelationDefaultCode, and SSPSupplierIdRequiredFlag; Configure Supplier Notifications owns NotifyPriorToExpirationDays and ReminderFrequencyDays | Resolve exactly one shared singleton, run the tasks serially, re-read after either task completes, and prepare only this task's owned attributes in the Data Loader artifact. |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| read_internal_profile_entities | Before validating a profile-change configuration request | SupplierProfileEntityId | GET /fscmRestApi/resources/11.13.18.05/supplierEntityConfigurations | SupplierProfileEntityId, SupplierProfileEntityCode, SupplierProfileEntity, InternalChangeMgmtCode | Match the supplied SupplierProfileEntityId exactly once in the internal profile result when an internal entity is selected | Current entity configuration | Stop |
| read_supplier_initiated_profile_entities | Before validating a profile-change configuration request | SupplierProfileEntityId | GET /fscmRestApi/resources/11.13.18.05/supplierEntityConfigurations | SupplierProfileEntityId, SupplierProfileEntityCode, SupplierProfileEntity, SupplierInitiatedChangeMgmtProspectiveCode, SupplierInitiatedChangeMgmtSpendAuthorizedCode | Match the supplied SupplierProfileEntityId exactly once in the supplier-initiated profile result when a supplier-initiated entity is selected | Current entity configuration | Stop |
| read_profile_change_options | Before validating a profile-change configuration request and again after an earlier successful shared supplierOptions task | None | GET /fscmRestApi/resources/11.13.18.05/supplierOptions | SupplierOptionsConfigId, InternalChangeBankAccAttachmentsRequiredFlag, SupplierPortalChangeBankAccAttachmentsRequiredFlag | Return exactly one seeded Supplier Options configuration. | Resolved singleton key and current attachment requirement flags | Stop on zero rows or multiple rows; the seeded row must be corrected outside this task, and this task must not create a row. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup returns no matching entity or options record | Stop and request correction; do not infer an identifier or setting |
| A lookup returns more than one matching entity | Stop and require an unambiguous SupplierProfileEntityId |
| A shared supplierOptions task has completed before this task | Re-run read_profile_change_options before artifact preparation and retain only this task's approved field changes. |
| The Supplier Options lookup returns zero rows | Stop; treat the seeded singleton as missing and do not prepare a create or bootstrap operation. |
| Configure Supplier Registration completed first | Re-run read_internal_profile_entities and read_supplier_initiated_profile_entities before artifact preparation and retain only InternalChangeMgmtCode, SupplierInitiatedChangeMgmtProspectiveCode, and SupplierInitiatedChangeMgmtSpendAuthorizedCode. |
| Configure Supplier Registration completed first and this task changes supplierOptions | Re-run read_profile_change_options before artifact preparation and retain only InternalChangeBankAccAttachmentsRequiredFlag and SupplierPortalChangeBankAccAttachmentsRequiredFlag. |
| A lookup request fails | Preserve the sanitized failure evidence and stop before any configuration update |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PROFILECHG.REFRESH_INTERNAL_ENTITIES | step | 10 | reference_lookup | success->PROFILECHG.REFRESH_SUPPLIER_ENTITIES;failure->RETURN_ISSUES | none | stop | Always |
| PROFILECHG.REFRESH_SUPPLIER_ENTITIES | step | 20 | reference_lookup | success->PROFILECHG.REFRESH_OPTIONS;failure->RETURN_ISSUES | PROFILECHG.REFRESH_INTERNAL_ENTITIES | stop | Always |
| PROFILECHG.REFRESH_OPTIONS | step | 30 | reference_lookup | success->PROFILECHG.ENFORCE_SCOPE;failure->RETURN_ISSUES | PROFILECHG.REFRESH_SUPPLIER_ENTITIES | stop | Always |
