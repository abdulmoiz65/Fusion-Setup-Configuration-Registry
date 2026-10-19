# Dependency Readiness

## Source

| Source | Location | Used For |
|---|---|---|
| Oracle Cost Organization Relationship | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/cost-organization-relationship.html | Legal-entity, business-unit, inventory-organization, and primary-cost-book constraints |
| Oracle Create Cost Organization Relationships | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/create-cost-organization-relationships.html | Association setup inputs and ledger-derived fields |
| Oracle Important Points to Know Before Creating Cost Organization Relationships | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/important-points-to-know-before-creating-cost-organization-relationships.html | Readiness troubleshooting and immutability constraints |
| Cost Organization LOV lookup | /fscmRestApi/resources/11.13.18.05/costOrgsLOV?q=CostOrgName = "&lt;cost-org-name&gt;" | Exact Cost Organization identity and legal-entity lookup contract by name or code |
| Eligible Inventory Organization LOV lookup | /fscmRestApi/resources/11.13.18.05/eligibleInventoryOrgsLOV?q=OrganizationName = "&lt;inventory-org-name&gt;"; /fscmRestApi/resources/11.13.18.05/eligibleInventoryOrgsLOV?q=OrganizationCode = "&lt;inventory-org-code&gt;" | Exact Inventory Organization identity, classification, legal entity, master organization, business unit, and profit center business unit lookup contract by name or code |
| Legal Entity LOV lookup | /fscmRestApi/resources/11.13.18.05/legalEntitiesLOV?q=LegalEntityId = &lt;legal-entity-id&gt;; /fscmRestApi/resources/11.13.18.05/legalEntitiesLOV?q=Name = "&lt;legal-entity-name&gt;" | Exact Legal Entity identity and name lookup contract by ID or name |
| Set LOV lookup | /fscmRestApi/resources/11.13.18.05/setIdSets?q=SetCode = "&lt;set-code&gt;" | Exact Set identity, code, and name lookup contract by ID, code, or name |
| Cost Book LOV lookup | /fscmRestApi/resources/11.13.18.05/costBooksLOV?q=CostBookCode = "&lt;cost-book-code&gt;" | Exact Cost Book identity, code, and periodic-average-cost status lookup contract by ID or code |
| Oracle Fusion Cost Organization Cost Books LOV finder | /fscmRestApi/resources/11.13.18.05/costOrgBooksLOV?finder=findByCostOrganization;bindCostOrgId=&lt;cost-org-id&gt; | Read-only existing Cost Book association and primary-book status validation for a ledger-less Cost Book association |
| Ledger LOV lookup | /fscmRestApi/resources/11.13.18.05/ledgersLOV?q=Name = "&lt;ledger-name&gt;" | Exact Ledger identity, category, accounting-calendar name, and currency lookup contract by ID or name |
| Accounting Calendar LOV lookups | /fscmRestApi/resources/11.13.18.05/accountingCalendarsLOV?q=PeriodSetName = '&lt;period-set-name&gt;'&onlyData=true; /fscmRestApi/resources/11.13.18.05/accountingCalendarsLOV?q=UserPeriodSetName = '&lt;user-period-set-name&gt;'&onlyData=true | Exact Accounting Calendar identity and period metadata lookup contract by the user-declared period-set name or user period-set name |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Cost Organization | Define the Cost Organization before associating inventory organizations or cost books. |
| 2 | Item Validation Organization | Select an item master organization in the same legal entity as the Cost Organization. |
| 3 | Legal Entity | Resolve the shared Legal Entity name from the matching Cost Organization and Item Validation Organization LegalEntityId values. |
| 4 | Set Assignment | Resolve the Set and use its SetId as SetAssignmentId. |
| 5 | Cost Books | Resolve the Cost Book and use its CostBookId as CostBookIdentifier. |
| 6 | Ledger | Resolve the Ledger, its category, currency, and accounting-calendar name when the new association is ledger-backed. |
| 7 | Accounting Calendar | Resolve the accounting-calendar identity and period metadata from the Ledger PeriodSetName or another exact calendar identifier. |
| 8 | Existing Primary Cost Book | For a ledger-less association, read the Cost Organization's existing Cost Books and confirm one is primary before continuing. |
| 9 | Inventory Organizations | Confirm each inventory organization has a Profit Center Business Unit, shares the Cost Organization legal entity and item master organization, and is not already assigned elsewhere. |
| 10 | Cost Books and Ledgers | Associate at least one Cost Book with the primary ledger of the Cost Organization legal entity; add secondary, reporting, or ledger-less books only as needed. |
| 11 | Subledger Application Options | Run Update Subledger Application Options if the required ledger is not available for cost-book association. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| COR-COST-ORGANIZATION | Cost Organization | Yes | Always | Lookup | Fusion costOrgsLOV exact user-declared CostOrgName or CostOrgCode lookup | resolve_cost_organization_exact | The relationship is anchored to a Cost Organization and requires its resolved identity and legal entity. | Provide either an exact Cost Organization name or an exact Cost Organization code and declare which field it is; do not select a partial or first match. | CostOrgId, LegalEntityId, CostOrgCode, CostOrgName, EffectiveStartDate, EffectiveEndDate, Status |
| COR-ITEM-VALIDATION-ORGANIZATION | Item Validation Organization | Yes | Always | Lookup | Fusion costOrgItemValidationOrgsLOV exact user-declared OrganizationName or OrganizationCode lookup with ClassificationCode INV | resolve_item_validation_organization_exact | It provides the item setups and must share the Cost Organization legal entity. The lookup confirms the documented INV classification and returns LegalEntityId for that comparison. | Provide either an exact Item Validation Organization name or code and declare which field it is; require ClassificationCode INV and confirm the returned LegalEntityId matches the Cost Organization LegalEntityId. | OrganizationId, OrganizationName, OrganizationCode, MasterOrganizationId, BusinessUnitId, LegalEntityId |
| COR-LEGAL-ENTITY | Legal Entity | Yes | Always | Lookup | Fusion legalEntitiesLOV exact LegalEntityId or exact Name lookup | resolve_legal_entity_exact | The relationship requires the Legal Entity Name associated with the matching Cost Organization and Item Validation Organization LegalEntityId. | Use the resolved Cost Organization LegalEntityId; do not continue if it differs from the Item Validation Organization LegalEntityId. | LegalEntityId, Name |
| COR-SET-ASSIGNMENT | Set Assignment | Yes | Always | Lookup | Fusion setIdSets exact SetId, SetCode, or SetName lookup | resolve_set_exact | The relationship requires SetAssignmentId, which is the SetId returned by this lookup. | Provide an exact Set ID, code, or name; do not select a partial or first match. | SetAssignmentId from SetId, SetId, SetCode, SetName |
| COR-INVENTORY-ORGANIZATION | Inventory Organization | Yes | For every inventory organization association | Lookup | Fusion eligibleInventoryOrgsLOV exact OrganizationName or exact OrganizationCode lookup | resolve_inventory_organization_exact | An Inventory Organization can belong to only one Cost Organization and must meet legal-entity, business-unit, and item-master constraints. The lookup LegalEntityId is the legal entity associated with the Inventory Organization. | Provide either an exact Inventory Organization name or an exact Inventory Organization code; compare the resolved LegalEntityId with the Cost Organization legal entity; do not select a partial or first match. | InvOrgId from OrganizationId, OrganizationId, InvOrgParametersOrganizationId from OrganizationId, OrganizationCode, OrganizationName, ClassificationCode, LegalEntityId, MasterOrganizationId, BusinessUnitId, ProfitCenterBUId from ProfitCenterBusinessUnitId, Effective Start Date |
| COR-PRIMARY-COST-BOOK | Existing Primary Cost Book | Yes | A ledger-less Cost Book association is being created | Lookup | Fusion costOrgBooksLOV finder scoped by resolved CostOrgId | resolve_primary_cost_book_by_cost_organization | A Cost Organization must have a primary Cost Book associated with the primary ledger of its legal entity. | No additional input is required; the workflow validates the Cost Organization's existing associations. | Primary CostBookId, Primary CostBookCode, PrimaryBookFlag |
| COR-LEDGER | Ledger | Conditional | A ledger-backed Cost Book association is being created | Lookup | Fusion ledgersLOV exact LedgerId or exact Name lookup | resolve_ledger_exact | A primary Cost Book must use the primary Ledger of the Cost Organization legal entity. PeriodSetName is the Ledger accounting-calendar name. | Provide an exact Ledger ID or Ledger Name only for a ledger-backed association; do not select a partial or first match. | LedgerId, LedgerIdentifier from LedgerId, LedgerName from Name, LedgerCategory from LedgerCategoryCode, AccountingCalendarName from PeriodSetName, CurrencyCode |
| COR-ACCOUNTING-CALENDAR | Accounting Calendar | Yes | Always | Lookup | Fusion accountingCalendarsLOV exact user-declared PeriodSetName or UserPeriodSetName lookup | resolve_accounting_calendar_exact | The Ledger PeriodSetName refers to the Accounting Calendar and must resolve to the calendar and period metadata needed for the Cost Book association. | Declare whether the supplied value is PeriodSetName or UserPeriodSetName; do not select a partial or first match. | CalendarId, CalendarIdentifier from CalendarId, AccountingCalendarName from PeriodSetName, UserAccountingCalendarName from UserPeriodSetName, PeriodType, CalendarTypeCode, PeriodSetId, PeriodTypeId |
| COR-PERIOD-END-VALIDATION | Existing Period End Validation | Yes | Updating Cost Organization Book Relationships Period End Validations | Lookup | Fusion costOrgBookPeriodEndValidations query scoped by CostOrgId and CostBookId | resolve_existing_period_end_validations | A PATCH update is permitted only for a ValidationType already present for the resolved Cost Organization and Cost Book. | Provide CostOrgId, CostBookId, and one existing ValidationType; do not select a partial or first match. | ValidationType, PeriodPendingCloseFlag, PeriodCloseFlag, PeriodFinalCloseFlag, RenderPeriodPendingCloseFlag, DisablePeriodPendingCloseFlag, DisablePeriodCloseFlag, ValidationActionCode, Meaning |
| COR-LEDGER-AVAILABILITY | Required Ledger availability | Conditional | The required ledger is not listed for Cost Book association | Blocked | Scheduled Processes work area | | Oracle directs running Update Subledger Application Options before retrying ledger selection. | Run Update Subledger Application Options, verify ledger availability, then restart validation. | Ledger |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | All required organizations, Cost Books, and Ledger associations are already defined and comply with the documented constraints | Yes, lookup only |
| Blocked | A required organization, Cost Book, Ledger, or required organization assignment is missing or noncompliant | No |
| Blocked | The required Ledger is not listed for Cost Book association | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COR.CHECK_DEPENDENCIES | decision | 14 | resolve_dependency | ready->COR.RESOLVE_REFERENCE_DATA_SET_OBJECT;blocked->COR.HANDLE_ISSUE | COR.RESOLVE_INVENTORY_ORGANIZATION | stop | Creating or updating Cost Organization Relationships |
