# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Mandatory preflight | Current `Algorithm_BO.xml` and current Service Mapping source XML are attached or explicitly provided with the same request; the algorithm name is correct, the absolute highest version has `ActiveFlag=Y`, and the Service Mapping context is `ARInterface` | Stop and request corrected current XML exports; do not use chat cache, prior project artifacts, remembered paths, or default assumptions | Ask the implementer to attach the current Manage Algorithms export and the current copied `ARInterface` Service Mapping source XML | Every advisory, mapping, validation, source-resolution, or use-case request handled by this companion | |
| Algorithm identity | `Algorithm_BO.xml` name equals `Subscription Management and Account Receivables Integration` | Reject the export and request the correct Manage Algorithms export | Validate the algorithm name before source analysis | Always | |
| Absolute highest version | All versions are read and the absolute highest `VersionNum` has `ActiveFlag=Y` | Reject the export as not In Progress; do not proceed by using an older active version | Ask for an In Progress algorithm export | Always | |
| Service Mapping context | Service Mapping source XML has `contextName="ARInterface"`; filename may vary | Stop and request the copied Subscription AR Integration source XML | Validate context before source analysis | Always | |
| Input type classification | Prompt is classified as Type 1, 2, 3, 4, or 5 from the primary algorithm Use-Case Resolution reference | Stop source recommendations until classified | Use the primary algorithm classifier, especially when invoked directly | Always | |
| Mapping outcome | Business rule and intended Accounts Receivables header or line outcome | Stop and request the expected AR result | Obtain a positive and negative example from the implementer | Always | |
| Target attribute | AR descriptive flexfield level, context, assigned table column, and source-type-compatible DFF family are confirmed | Stop and request the configured flexfield details | Confirm the flexfield code, context, Table Column assignment, and that character/date/number DFF family matches the source type from XML or describe | A custom AR attribute is mapped | |
| Source object and attribute | Source entity and source attribute are identified through the current export, implementer input, or one accepted describe-backed candidate | Stop and request source resolution | Scan current exposed attributes, run permitted describe for relevant objects, and require implementer selection or exact names | Always | |
| Describe runtime availability | Required describe calls either complete successfully or the runtime failure has been reported with the implementer's selected next path | Stop and disclose that describe is not working; ask whether to resolve the runtime environment connection and rerun describe, or proceed only with named unconfirmed assumptions for review | Report the failed describe family or URI and failure category when known | Any missing or objectless source requires describe | |
| Objectless source attribute | A source attribute or business term without an object has been checked across the current Service Mapping XML and permitted describe responses before object recommendation | Stop and request object resolution | Do not default to any context entity; show described candidates and require one implementer decision | Attribute is stated without `Subscription`, `Products`, `BillLines`, `Charges`, `ProductAssociations`, or another explicit source object | |
| Duplicate source labels across families | The source-resolution record identifies the functional owner and lists same-label alternatives | Stop and request owner/candidate selection | Prefer the explicitly stated object, otherwise the business-owning source family; do not select another family only because its cardinality is easier | Same or similar candidate labels appear in multiple described or exposed families | |
| Service access | Read and write access decision for the custom attribute | Stop and request the service-access requirement | Confirm the access setting for the selected entity | A custom attribute is added | |
| Advisory delivery | Proposed configuration and requested UI steps are shown in chat, with the same content persisted as an artifact | Return the complete proposal in chat before handoff | A mapping advisory is returned | |
| Source-resolution decision | Each requested source is accepted from the current export, supplied exactly by the implementer, or accepted as one named describe candidate | Stop and request an implementer decision | A requested source is used by Groovy | |
| Configuration handoff | Final selected sources, aliases, types, access, publication prerequisites, remaining UI actions, and the final source-target mapping table are recorded | Create the handoff after approved local Algorithm_BO.xml creation | Local algorithm artifact is created | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Data type compatibility | Require the custom Subscription attribute data type to match the Service Mapping attribute data type, and pass that type to the primary algorithm workflow for omitted-target DFF selection | A custom attribute is added or a target column is omitted | |
| DFF target family by source type | Recommend `ATTRIBUTE<n>` for string/varchar/character/display identifiers/codes/Boolean-as-code, `ATTRIBUTE_DATE<n>` for date/datetime, and `ATTRIBUTE_NUMBER<n>` for number/integer/long/decimal/numeric identifiers; use the matching `HEADER_` family for header scope | The AR target is omitted and a DFF target is suggested | Do not infer numeric solely from names ending in `Id`; require XML/describe type evidence or label the type assumption as unconfirmed |
| Custom attribute name | Require the _Custom suffix in the Service Mapping Attribute column | A custom descriptive-flexfield attribute is added | |
| Mapping level | Require an explicit header or line target; do not infer it from the source entity | The AR target is not stated | |
| Source mapping | Require a documented entity-to-view-object attribute mapping before recommending a change | A source attribute is custom | |
| Seeded service-mapping surface | Use a listed seeded object and attribute when the business logic needs it; request mapping confirmation for any attribute outside this inventory | A service-mapping object is referenced | |

## Seeded Service-Mapping Objects

| Object | Seeded Attributes | Use in Customization Enabled Service Mapping Advisory |
|---|---|---|
| BillLines | BillLineId, SubscriptionId, SubscriptionProductId, ChargeId, ProductAssociationId | Available when the stated business logic requires bill-line context |
| Charges | ChargeId, ProductAssociationId | Available when the stated business logic requires charge context |
| HeaderSalesCredits | SalesCreditId, SubscriptionId, SubscriptionProductId | Available when the stated business logic requires header sales-credit context |
| ProductSalesCredits | SalesCreditId, SubscriptionProductId | Available when the stated business logic requires product sales-credit context |
| Subscription | SubscriptionId | Available when the stated business logic requires subscription context |
| Products | SubscriptionId, SubscriptionProductId | Available when the stated business logic requires subscription-product context |
| ProductAssociations | ProductAssociationId | Available when the stated business logic requires product-association context |

These are user-confirmed seeded objects and attributes for Customization Enabled mode. Do not infer any additional object or attribute, and do not apply this inventory to PerformanceMode.

## Source Anchors

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/subscription-management/fasmq/create-and-manage-account-receivables-service-mappings.html | Subscription AR Integration purpose, custom-attribute requirements, and service-mapping steps |
| User-provided seeded service-mapping inventory | Available object and attribute surface for Customization Enabled advisory mappings |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SVC_AR_VALIDATE_INPUT | step | 1 | validate_input | valid->SVC_AR_CHECK_DEPENDENCIES;missing->SVC_AR_MISSING_INPUT | none | stop | Always |