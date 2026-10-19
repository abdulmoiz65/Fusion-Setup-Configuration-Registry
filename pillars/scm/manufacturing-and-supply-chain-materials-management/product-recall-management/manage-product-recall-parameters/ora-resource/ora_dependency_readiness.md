# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Product Recall Management access | The executor has the Manage Product Recall Parameters privilege and Data Loader can describe the selected business objects. |
| 2 | Referenced setup identities | Validate lookup codes through genericLookupsLOV; inventory organizations through the describe-backed `inventoryOrganizations` resource; subinventories through activeSubinventories; locators through activeLocators; business units through finBusinessUnitsLOV; ledgers through ledgersLOV; and owners/coordinators through publicWorkers. |
| 3 | Product recall lookups | Containment action codes are configured before a true BypassTaskFlag is used, where the configured business process requires them. |
| 4 | Immutable preview and approval | The Data Loader preview exists and the user explicitly approves its exact target, operations, and payload artifact. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| recall_parameters_privilege | Manage Product Recall Parameters access | Yes | Always | Verify | Assigned role and Data Loader describe result | describe_recall_parameter_business_objects | Oracle documents ENQ_MANAGE_PRODUCT_RECALL_PARAMETERS for manage access to the recall parameter resources | Provide an authorized implementation identity; stop if describe is denied | Supported business objects and methods |
| recall_reference_identities | Referenced lookup code, organization, subinventory, locator, cost center/location, business unit, ledger, owner, or coordinator | Conditional | A supplied row refers to the relevant identity | Lookup | Target-environment lookup result | resolve_inventory_organization | Every referenced identity must resolve exactly before a payload is shaped | Provide exact values and required parent context; use PersonNumber or another supported unique worker identifier for owner/coordinator validation | Resolved canonical values and IDs required by the current contract |
| recall_owner_coordinator | Active owner or coordinator worker | Conditional | recallContainmentTaskOwners supplies OwnerName | Lookup | publicWorkers lookup result | resolve_owner_or_coordinator_worker | A free-text owner name is not a safe unique identity | Provide PersonNumber or a target-describe-supported unique worker identifier | Sanitized identity confirmation and canonical display name |
| recall_financial_context | Business unit and ledger | Conditional | The selected Data Loader schema exposes a business-unit or ledger field | Lookup | finBusinessUnitsLOV and ledgersLOV lookup results | resolve_business_unit | Business-unit and ledger relationships must be exact and active when attributes are exposed | Provide an exact name or ID; reconcile a supplied ledger to the business unit's PrimaryLedgerId | BusinessUnitId, PrimaryLedgerId, LedgerId, CurrencyCode |
| recall_bypass_lookup | Containment action code lookup | Conditional | BypassTaskFlag is true and bypass count or disposal tasks are used | Verify | Product Recall Lookups configuration | | Oracle documentation requires this lookup when the bypass attribute is enabled | Confirm the required containment action codes exist before preview | Validation evidence |
| recall_import_approval | Data Loader preview approval | Yes | A live import is requested | Verify | Immutable preview artifact and explicit user approval | | REST import is a mutation and must be approved against the exact preview | Obtain explicit approval immediately before import; rerun preview after any change | Preview fingerprint and approval record |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The required access, identity, or approval evidence is present | Yes for documented read-only lookups; no create |
| Lookup | An exact display value must be resolved before preview | Yes for describe-backed read-only lookup only |
| Blocked | A required privilege, identity, lookup, or approval is missing or ambiguous | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RECALL.PARAMETERS.RESOLVE-DEPENDENCIES | decision | 25 | resolve_dependency | ready->RECALL.PARAMETERS.DESCRIBE-CONTRACT;blocked->RECALL.PARAMETERS.HANDLE-DEPENDENCY-ERROR | RECALL.PARAMETERS.LOOKUP-EXISTING | stop | A payload or operation is being prepared |
