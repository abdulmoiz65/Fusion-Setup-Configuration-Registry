# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Change-management scope | Internal profile management or supplier-initiated profile management | Stop | Specify which profile-management scope is being configured | Always | |
| Entity configuration change | SupplierProfileEntityId and the code field permitted for the selected scope | Stop | Provide the target entity and its requested setting | An entity configuration is changing | |
| Bank-account attachment setting | InternalChangeBankAccAttachmentsRequiredFlag or SupplierPortalChangeBankAccAttachmentsRequiredFlag | Stop | Provide the flag for the selected scope | A bank-account attachment requirement is changing | |
| Shared supplierOptions coordination | Participating task field ownership and one final value for each overlapping supplierOptions attribute | Stop | Resolve any overlap before this task is prepared; execute the shared singleton tasks serially. | This task changes a supplierOptions-backed setting in a runbook that also includes Configure Supplier Registration or Configure Supplier Notifications | read_profile_change_options |
| Shared entity-configuration coordination | SupplierProfileEntityId and only profile-change-owned attributes | Stop | Re-read the shared entity configuration after Configure Supplier Registration if it completed first. | A profile-management entity configuration is changing in the same runbook | read_internal_profile_entities |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An internal profile entity setting is requested | Verify the entity exists in the internal profile configuration set | Stop on no match | read_internal_profile_entities |
| A supplier-initiated profile entity setting is requested | Verify the entity exists in the supplier-initiated profile configuration set | Stop on no match | read_supplier_initiated_profile_entities |
| A bank-account attachment setting is requested | Verify the current supplier options record is available | Stop on no match | read_profile_change_options |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Internal profile field scope | Accept only InternalChangeMgmtCode for the selected entity; reject supplier-initiated fields | Internal profile management | |
| Supplier-initiated profile field scope | Accept only SupplierInitiatedChangeMgmtProspectiveCode and SupplierInitiatedChangeMgmtSpendAuthorizedCode for the selected entity | Supplier-initiated profile management | |
| Attachment option scope | Accept the internal or supplier-portal attachment flag only for its matching profile-management scope | A bank-account attachment requirement is changing | |
| Shared singleton freshness | Require a fresh read-only supplierOptions lookup after every earlier successful shared-singleton task in the runbook; do not reuse a stale row or merge another task's unapproved fields. | This task changes a supplierOptions-backed setting in a shared runbook | read_profile_change_options |
| Seeded singleton operation | Accept only an update to the resolved existing supplierOptions row through this task's approved Data Loader route; reject a create, bootstrap, or delete request. | This task changes a supplierOptions-backed setting | read_profile_change_options |
| Shared entity attribute ownership | Accept only InternalChangeMgmtCode, SupplierInitiatedChangeMgmtProspectiveCode, and SupplierInitiatedChangeMgmtSpendAuthorizedCode for supplierEntityConfigurations; reject RegistrationProspectiveCode and RegistrationSpendAuthorizedCode. | A supplierEntityConfigurations change is supplied | |
| Shared supplierOptions attribute ownership | Accept only InternalChangeBankAccAttachmentsRequiredFlag and SupplierPortalChangeBankAccAttachmentsRequiredFlag; reject the Registration and Configure Supplier Notifications attributes. | A supplierOptions change is supplied | read_profile_change_options |
