# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Read current configuration | Retrieve the applicable entity configuration and profile-change options before evaluating the requested setting |
| 2 | Enforce scope | Confirm that the selected profile-management scope and requested fields match |
| 3 | Shared entity-configuration coordination | When Configure Supplier Registration also changes supplierEntityConfigurations, require fresh entity lookups and exclusive attribute ownership. |
| 4 | Shared singleton coordination | When this task changes supplierOptions in the same runbook as the other shared tasks, require a fresh singleton lookup, exclusive field ownership, and serial execution. |
| 5 | Hold execution | Require the task's declared export, validation, and approval gates before an approved Data Loader route is used |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Internal profile management is configured | Error | | A requested entity is absent or the change includes a supplier-initiated code field | Configure only InternalChangeMgmtCode for the selected internal-profile entity | Yes |
| Supplier-initiated profile management is configured | Error | | A requested entity is absent or the change includes InternalChangeMgmtCode | Configure only SupplierInitiatedChangeMgmtProspectiveCode or SupplierInitiatedChangeMgmtSpendAuthorizedCode for the selected supplier-initiated entity | Yes |
| A bank-account attachment requirement is configured | Error | | The attachment flag does not match the selected profile-management scope | Use InternalChangeBankAccAttachmentsRequiredFlag for internal scope and SupplierPortalChangeBankAccAttachmentsRequiredFlag for supplier-initiated scope | Yes |
| A shared supplierEntityConfigurations row is prepared | Error | | The proposed artifact includes registration attributes or was prepared from a row read before Configure Supplier Registration completed | Re-read the row and include only InternalChangeMgmtCode, SupplierInitiatedChangeMgmtProspectiveCode, and SupplierInitiatedChangeMgmtSpendAuthorizedCode through core.data-loader | Yes |
| A shared supplierOptions runbook task is prepared | Error | read_profile_change_options | The lookup does not resolve exactly one current row, another participating task proposes a different final value for the same attribute, or the lookup predates an earlier successful shared task | Resolve the conflict, re-read the singleton, and prepare only this task's owned fields through core.data-loader | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| read_profile_change_options | Before preparing a supplierOptions-backed profile-change setting in a shared runbook | SupplierOptionsConfigId and current attachment requirement flags | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PROFILECHG.ENFORCE_SCOPE | decision | 40 | design_enforcement | compliant->PROFILECHG.COMPLETE;noncompliant->RETURN_ISSUES | PROFILECHG.REFRESH_OPTIONS | stop | A profile-change configuration request is being evaluated |
