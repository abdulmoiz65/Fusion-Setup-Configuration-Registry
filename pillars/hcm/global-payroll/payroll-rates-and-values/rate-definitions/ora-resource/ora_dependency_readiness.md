# Rate Definitions HDL Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target attribute metadata | Export Rate Definition and Rate Contributor Attributes from View Business Objects for the target release. |
| 2 | MERGE identity assessment | Confirm the effective-dated rate identity cannot update another rate definition; preserve source-system ownership when it is supplied. |
| 3 | Target setup references | Confirm the LDG, effective context, currency, periodicity, conversion formula, and category-specific source records. |
| 4 | Category prerequisites | Create and validate the compatible element, balance, rate, or value-by-criteria definition before using it as a contributor. |
| 5 | HDL artifact design | Link each contributor to the intended rate definition in the same LDG and effective context, then prepare the parent and contributor MERGE records. |
| 6 | Core Data Loader route | Use the owning core.data-loader workflow for live business-object discovery, template download, immutable artifact validation, approval, upload, initiation, and diagnostics. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| RATE.METADATA | Rate Definition and Rate Contributor attribute metadata | Yes | Every production HDL request | Verify | Current target RateDefinitionV2 Data Loader template | resolve_rate_definition_hdl_contract | The target template establishes supported attributes and child sections for the target release | Retrieve the template through core.data-loader before production preparation | Business-object ID, template content ID, supported parent and child attributes |
| RATE.IDENTITY | Rate-definition MERGE identity | Yes | Every RateDefinitionV2 MERGE record | Verify | Prepared immutable RateDefinitionV2 and RateContributorV2 records; source-system identifiers when supplied | validate_rate_definition_hdl_identity | MERGE parent and child rows must be internally unambiguous before the loader receives them | Provide the rate code, LDG, effective date, and deterministic sequence; preserve optional source-system identifiers when supplied | Confirmed parent key and update-safe child linkage |
| RATE.LDG | Legislative Data Group and effective context | Yes | Every parent and contributor record | Lookup | Target Fusion legislative-data-group LOV | resolve_legislative_data_group_by_exact_name | Rates and their references are LDG and effective-date scoped | Provide the target LDG and effective date; stop on no match or ambiguity | LegislativeDataGroupId, LegislativeDataGroupName, EffectiveStartDate |
| RATE.CATEGORY | Category-specific source setup | Yes | Every rate definition | Verify | Current target RateDefinitionV2 Data Loader template | resolve_rate_definition_hdl_contract | Element, Derived Rate, and Value by Criteria designs use different supported HDL attributes | Provide the category and its compatible source codes; do not substitute similarly named records | Category, ElementCode or derived contributors or value-by-criteria definition |
| RATE.ELEMENT | Compatible salary element and input value | Conditional | Category is Element | Verify | Current target Data Loader template and supplied element/input-value codes | resolve_rate_definition_hdl_contract | An Element rate requires the supported element, storage type, contributor-input, periodicity, currency, and conversion attributes | Confirm the element and input-value codes before loading; do not use a Hours x Rates element | ElementCode, ContributorInputValueCode, StorageType |
| RATE.CONTRIBUTORS | Contributor source records, linkage, and currency | Conditional | Category is Derived Rate or one or more contributors are supplied | Verify | Prepared HDL artifact and current target template | validate_rate_definition_hdl_identity | Contributors must link to the intended parent and use unique deterministic sequence numbers | Supply each contributor in deterministic order and validate all selected fields against the current target template | ContributorType, source identity, parent link, SequenceNumber, currency |
| RATE.ARTIFACT | HDL artifact and approval readiness | Yes | Before import | Verify | Prepared HDL artifact and request approval | | The artifact must contain the validated parent and contributor records, and live import requires immediate approval bound to the exact target and artifact | Present the exact target environment, immutable HDL artifact reference, and approval fingerprint | Artifact reference, target environment, approval fingerprint |
| RATE.LOADER_CONTRACT | HCM Data Loader execution contract | Yes | HDL preparation, validation, or import is requested | Verify | core.data-loader/references/fusion-zip-rest.md | resolve_rate_definition_hdl_contract | The core Data Loader contract owns live business-object discovery, template retrieval, immutable archive validation, UCM upload, load initiation, and diagnostics | Use the configured Fusion environment through core.data-loader; validate the target-discovered RateDefinitionV2 template before requesting approval or import | Business object ID, UCM template content ID, immutable archive reference, load request ID |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | A validated source value or immutable artifact reference is supplied | No lookup required; do not create a related object |
| Lookup | A documented read-only target lookup can resolve the value | Yes, read-only only |
| Verify | Target metadata, identity evidence, or configuration must be checked | Yes, only through the documented resolver contract |
| Blocked | A required value, unique match, metadata contract, loader contract, or approval is absent | No |
| Create with Approval | A separate approved workflow explicitly authorizes a missing related setup creation | No; outside this task resource unless separately routed |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RATE_DEFINITION.RESOLVE_DEPENDENCIES | decision | 30 | resolve_dependency | ready->RATE_DEFINITION.RESOLVE_REFERENCES;blocked->RATE_DEFINITION.HANDLE_DEPENDENCY_ERROR | RATE_DEFINITION.ASSESS_MERGE_IDENTITY | stop | Confirm target metadata, category-specific setup, contributor, artifact, and loader prerequisites before HDL preparation. |
