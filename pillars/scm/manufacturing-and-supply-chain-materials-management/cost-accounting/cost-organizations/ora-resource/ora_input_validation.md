# Input Validation

## Source

- Oracle Fusion Cloud SCM, [Create a Cost Organization](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/create-a-cost-organization.html)
- Developer-provided non-Cost Organization LOV REST contract, /fscmRestApi/resources/11.13.18.05/nonCostOrganizationsLOV?q=Name = "&lt;cost organization name&gt;"&amp;limit=1
- User-verified Data Loader Status constraint: the loader supports only `A` (Active) and `I` (Inactive).


## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Creation option | Create New or Use an existing organization | Stop | Select one creation option before collecting attributes | Always | |
| Create New REST attributes | CostOrganizationCode, CostOrganizationName, LegalEntityName | Stop | Provide every listed REST attribute; Status is defaulted or normalized separately | Creation option is Create New | |
| Use an existing organization REST attributes | CopyExistingOrgFlag, CostOrganizationCode, CopyOrganizationName, CopyOrgClassificationCode, LegalEntityName | Stop | Provide CostOrganizationCode, CopyOrganizationName, and LegalEntityName; resolve CopyOrgClassificationCode and EffectiveStartDate from the existing organization lookup; Status is defaulted or normalized separately | Creation option is Use an existing organization | resolve_non_cost_organization_exact |
| Existing Cost Organization update | CostOrganizationCode and at least one of CostOrganizationName or Status | Stop | Provide the exact CostOrganizationCode and one or both permitted update fields. Do not supply any other update field. | Update an existing Cost Organization | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| LegalEntityName identifies a legal entity that was defined before cost organization creation | Continue to dependency readiness | Always | |
| CopyOrganizationName matches the existing organization name | Resolve the exact existing organization; require the returned Name to match, then use its ClassificationCode and EffectiveStartDate | Creation option is Use an existing organization | resolve_non_cost_organization_exact |
| Status is blank | Default Status to `A` | Create a cost organization | |
| Status is `Active` or `Inactive` | Normalize `Active` to `A` and `Inactive` to `I` before the Data Loader payload is created | Create a cost organization or an update supplies Status | |
| Status is `A` or `I` | Preserve the supplied value | Create a cost organization or an update supplies Status | |
| Status has any other value | Stop; provide `A`, `I`, `Active`, or `Inactive` | Create a cost organization or an update supplies Status | |
| Status represents an active cost organization | Continue; a Cost Organization must have Status `A` before the cost processor can cost its transactions | When transactions are intended to be costed | |
| Effective Start Date is blank, or every supplied value is a real `YYYY-MM-DD` calendar date | Continue to defaulting; reject `MM/DD/YYYY`, `YYYY/MM/DD`, timestamps, and invalid calendar dates before creating the Data Loader archive | Always | |
| User-supplied Effective Start Date differs from the resolved existing organization EffectiveStartDate | Disclose that the user-supplied date will not be used and request approval to use the resolved date before continuing | CopyExistingOrgFlag is true and EffectiveStartDate is supplied | resolve_non_cost_organization_exact |
| Update request includes a field other than CostOrganizationCode, CostOrganizationName, or Status | Stop; reject the update request before an archive or preview is created | Update an existing Cost Organization | |
| Existing Cost Organization update has neither CostOrganizationName nor Status | Stop; request one permitted update field | Update an existing Cost Organization | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| CopyExistingOrgFlag is true and CopyOrganizationName is supplied | Resolve the existing organization by exact Name and use the returned ClassificationCode and EffectiveStartDate | Continue to legal-entity dependency readiness | resolve_non_cost_organization_exact |
| CopyExistingOrgFlag is true and a supplied EffectiveStartDate differs from the resolved date | Await approval to replace the user-supplied date with the resolved existing organization EffectiveStartDate | Continue to legal-entity dependency readiness only after approval | resolve_non_cost_organization_exact |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCO.VALIDATE | decision | 1 | validate_input | valid_create->CCO.NORMALIZE_STATUS;valid_update->CCO.UPDATE_NORMALIZE_STATUS;invalid->CCO.HANDLE_ISSUE | none | stop | Create a cost organization or update an existing Cost Organization; only CostOrganizationName and Status are mutable during update |
