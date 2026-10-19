# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target environment metadata | Confirm the Payroll Balance Definition business object discriminator and successful live Data Loader schema validation. |
| 2 | LDG and existing balance assessment | Resolve the target LDG and assess whether an existing balance has the exact requested name. |
| 3 | Balance design values | Validate the category, UOM, currency condition, and dimensions for the target legislation when they are included. |
| 4 | Feed sources | Validate every element classification or element/input-value feed and its UOM compatibility. |
| 5 | HDL artifact design | Link children by BalanceId or BalanceCode with the same LDG, keep seeded and custom feed changes separate, and prepare the HDL file. |
| 6 | Approval gate | Bind explicit approval to the exact target environment and immutable HDL artifact before import. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| BAL.METADATA | Target business-object metadata | Yes | All HDL preparation | Verify | View Business Objects evidence and Core Data Loader live schema validation | resolve_balance_metadata | The import must use the release-specific business-object contract | Confirm the exact discriminator and successful live schema validation | Validated parent business-object contract |
| BAL.LDG | Legislative data group | Yes | All parent and child records | Lookup | Legislative data groups LOV | find_ldg_by_exact_name | All records must use the intended valid LDG | Provide an LDG name and resolve exactly one match | LegislativeDataGroupId, LegislativeDataGroupName, legislation context |
| BAL.EXISTING | Existing balance assessment | Yes | New or changed balance definition | Lookup | Public Balance Definition LOV endpoint and target evidence | find_balance_by_exact_name | Avoid creating a duplicate or unnecessary custom balance | Provide an exact balance name and target environment | Existing balance type ID, balance identity |
| BAL.DESIGN | Category, UOM, currency, and dimension design | Yes | Parent or DefinedBalance is included | Verify | Target LDG metadata and approved localization setup | resolve_balance_reference_values | Categories, dimensions, and contexts are predefined and localization-sensitive | Validate every selected value in the target LDG; do not reuse another LDG's values | Category code, UOM, currency requirement, dimension code |
| BAL.FEED | Feed source readiness | Conditional | A BalanceClassification or BalanceFeed is included | Verify | Target element, input-value, and classification authority | resolve_balance_reference_values | Feed sources must exist, be LDG-compatible, and match the balance UOM | Validate the exact classification or element/input-value source before HDL preparation | Classification code, element code, input value code, UOM compatibility |
| BAL.PARENT | Parent balance linkage | Yes | Any child record is included | Satisfied | Direct BalanceId, or BalanceCode with the same LDG, supplied by the user or resolved from the parent | | Child records can use BalanceId or the documented BalanceCode alternate key; source-system identifiers are optional | Provide the Balance Type ID or balance code with LDG | BalanceId or BalanceCode |
| BAL.SOURCE_REF | Source-system parent cross-reference | Conditional | BalanceId(SourceSystemId) is used instead of direct BalanceId | Verify | Supplied source-system identifiers and target metadata | resolve_balance_source_system_reference | The alternate linkage must resolve to the intended parent ID | Provide the source-system identifiers or use direct BalanceId | BalanceId |
| BAL.ARTIFACT | HDL split and approval readiness | Yes | Before import | Verify | Prepared HDL artifact and request approval | | Seeded and custom balance-feed updates must be separate, and live import requires immediate approval | Split files as necessary; present the exact target and immutable artifact for approval | Artifact reference, target environment, approval fingerprint |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | A direct BalanceId or other validated dependency value is supplied | No lookup required; do not create a related object |
| Lookup | A documented read-only lookup can resolve the value | Yes, read-only only |
| Verify | Target metadata or localization evidence must be checked | Yes, only through the documented resolver contract |
| Blocked | A required value, unique match, metadata contract, or approval is absent | No |
| Create with Approval | A separate approved workflow explicitly authorizes a missing related setup creation | No; outside this task resource unless separately routed |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BAL.RESOLVE_DEPENDENCIES | decision | 30 | resolve_dependency | ready->BAL.ENFORCE_DESIGN;blocked->BAL.HANDLE_DEPENDENCY_ERROR | BAL.LOOKUP_EXISTING | stop | A Balance Definitions HDL request passed input validation |
