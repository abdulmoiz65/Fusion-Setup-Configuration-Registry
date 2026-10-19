# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 0 | Mandatory preflight | Attach or explicitly provide the current `Algorithm_BO.xml` and current `ARInterface` Service Mapping source XML in the same request before any advisory, mapping, validation, source-resolution, or use-case work; reject unless the algorithm name is correct, the absolute highest version has `ActiveFlag=Y`, and the Service Mapping context is `ARInterface` |
| 1 | AR descriptive flexfield | Create and deploy the required header or line descriptive flexfield, then record its context and Table Column assignment |
| 2 | Subscription custom attribute | Create and publish the required custom attribute in an active sandbox when a new source attribute is required |
| 3 | Subscription AR Integration mapping | Add the custom entity attribute, map it to the view object attribute, and set read and write access |
| 4 | Published Service Mapping | Publish every new source attribute mapping before returning the completed mapping result |
| 5 | Test subscription | Populate the custom attribute, activate the subscription, and use the documented Receivables interface flow to verify the result |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| current_exports | Current `Algorithm_BO.xml` and current Service Mapping source XML | Yes | Any advisory, mapping, validation, source-resolution, or use-case request is handled | Verify | Current request attachments or explicit file inputs | | The mapping advisory must reflect the active algorithm contract and current exposed Service Mapping source, not cached state | Attach both current exports with the request | Algorithm export and Service Mapping source XML |
| algorithm_identity_and_version | Correct algorithm name and editable absolute highest version | Yes | Any request is handled | Verify | Current `Algorithm_BO.xml` | | The companion must not recommend mapping for the wrong integration or an algorithm that is not In Progress | Provide `Subscription Management and Account Receivables Integration` where the absolute highest `VersionNum` has `ActiveFlag=Y` | Algorithm name, all versions, highest version ActiveFlag |
| input_type_classification | Type 1, 2, 3, 4, or 5 is identified | Yes | Source recommendation or handoff is prepared | Verify | Business requirement and primary algorithm Use-Case Resolution reference | | The source-discovery path depends on whether target, source object, and source attribute are known | Classify before describe or recommendation | Input type |
| ar_descriptive_flexfield | AR header or line descriptive flexfield | Yes | A custom AR target attribute is mapped | Verify | Oracle setup and task documentation | | The mapping needs the configured AR context and table column | Provide the flexfield code, context, and Table Column assignment | Target context and column |
| subscription_custom_attribute | Subscription custom attribute | Conditional | The required source value is not a delivered source attribute | Verify | Oracle setup and task documentation | | The mapping needs a published Subscription Management source attribute | Provide the sandbox, entity, attribute, and data type | Source entity and attribute |
| subscription_ar_integration_mapping | Subscription AR Integration mapping | Yes | Any custom attribute is mapped | Verify | Oracle setup and task documentation | | The source must be mapped to the view object and exposed through the service | Provide the entity, _Custom attribute, view object mapping, and service access | Mapping definition |
| describe_runtime_path | Runtime describe availability or implementer-selected fallback | Conditional | A required source is missing from the current export or the source object is unknown | Verify | Permitted describe result or implementer choice after failure disclosure | | Describe must either validate the candidate or the implementer must knowingly choose a review-only assumption path | Resolve the runtime environment connection and rerun describe, or accept named unconfirmed assumptions for review | Failed describe family or URI and chosen path |
| published_service_mapping_changes | Published Service Mapping changes | Yes | New source attributes are used by the requested mapping | Verify | Implementer confirmation | | The returned source alias cannot be used until its mapping is published | Publish the required Service Mapping changes before returning the result | Published source attributes |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Advisory blocker | Preflight, flexfield, custom attribute, input type, or mapping detail is not confirmed | No |
| Ready for implementer review | The required mapping details are supplied and consistent | No |

## Source Anchors

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/subscription-management/fasmq/create-and-manage-account-receivables-service-mappings.html | Flexfield, sandbox, service-mapping, and verification prerequisites |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SVC_AR_CHECK_DEPENDENCIES | step | 2 | resolve_dependency | ready->SVC_AR_ENFORCE_DESIGN;blocked->SVC_AR_BLOCKED | SVC_AR_VALIDATE_INPUT | stop | Input validation is valid |