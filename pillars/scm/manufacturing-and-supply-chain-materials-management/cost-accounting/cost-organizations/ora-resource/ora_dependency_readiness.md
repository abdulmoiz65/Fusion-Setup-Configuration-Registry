# Dependency Readiness

## Source

- Oracle Fusion Cloud SCM, [Create a Cost Organization](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/create-a-cost-organization.html)


## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Existing organization | When CopyExistingOrgFlag is true, resolve the exact existing organization before deriving its classification and effective start date. |
| 2 | Legal entity | Define the legal entity before creating the cost organization. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CCO-EXISTING-ORGANIZATION | Existing organization | Yes | CopyExistingOrgFlag is true | Lookup | Fusion nonCostOrganizationsLOV exact Name lookup | resolve_non_cost_organization_exact | The copied organization supplies the classification and effective start date. | Provide one exact CopyOrganizationName. | OrganizationId, CopyOrganizationName, CopyOrgClassificationCode, EffectiveStartDate |
| CCO-LEGAL-ENTITY | Legal entity | Yes | Always | Verify | Previously defined legal entity | | A legal entity must be associated with the cost organization and defined first. | Provide LegalEntityName for a legal entity already defined in Fusion. | LegalEntityName |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | CopyExistingOrgFlag is true and the exact existing organization was resolved | Yes, lookup only |
| Ready | LegalEntityName names a previously defined legal entity | No |
| Blocked | CopyExistingOrgFlag is true and the existing organization did not resolve exactly | No |
| Blocked | LegalEntityName is absent or the named legal entity has not been defined | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCO.DEPENDENCIES | decision | 5 | resolve_dependency | ready->CCO.DEFAULT_EFFECTIVE_DATE;blocked->CCO.HANDLE_ISSUE | CCO.CONFIRM_EFFECTIVE_START_DATE_OVERRIDE | stop | Create a cost organization |
