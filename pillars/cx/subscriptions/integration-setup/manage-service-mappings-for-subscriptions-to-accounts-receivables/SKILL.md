---
skill_id: "cx.subscriptions.integration-setup.manage-service-mappings-for-subscriptions-to-accounts-receivables"
name: "Manage Service Mappings for Subscriptions to Accounts Receivables Advisory"
description: "Companion workflow for Service Mapping source XML, source attributes, describe metadata, view-object mappings, access, and publication prerequisites for Subscriptions-to-Accounts-Receivables. Returns mapping results to the primary Manage Algorithms skill."
layer: "pillar"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Integration Setup"
functional_area_code: "CUSTOM_INTEGRATION_SETUP"
task_code: "CUSTOM_MANAGE_SERVICE_MAPPINGS_FOR_SUBSCRIPTIONS_TO_ACCOUNTS_RECEIVABLES"
task_name: "Manage Service Mappings for Subscriptions to Accounts Receivables"
parent_skill_id: "cx.subscriptions.integration-setup"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
type: "advisory"
execution_mode: "advisory"
owner_team: "CX subscriptions pillar team"
version: "0.1.8"
inputs:
  - "business_requirement"
  - "service_mapping_source_xml"
  - "requested_source_attributes"
  - "implementation_project_context"
outputs:
  - "service_mapping_assessment"
  - "source_attribute_recommendations"
  - "source_resolution_record"
  - "service_mapping_configuration_handoff"
  - "mapping_prerequisites"
  - "validation_result"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "cx.subscriptions.integration-setup.manage-algorithms-for-subscriptions-to-accounts-receivables"
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
---

# Manage Service Mappings for Subscriptions to Accounts Receivables

## Purpose

Assess Service Mapping sources for the Subscription Management and Accounts Receivable integration, recommend confirmed source aliases and prerequisites, and return the result to the companion Manage Algorithms workflow without changing Fusion configuration.

## Ownership and return

This is the companion workflow for Service Mapping only. It owns Service Mapping source XML, entities, custom attributes, aligned REST describe metadata, `Pricing*` view objects, access, and publication prerequisites. It never edits the source XML or creates an import artifact.

After the mapping result is accepted or declined, return automatically to `cx.subscriptions.integration-setup.manage-algorithms-for-subscriptions-to-accounts-receivables`, passing confirmed sources, alternatives, assumptions, context, access, and publication prerequisites.

## Inputs and source XML

Run this mandatory preflight before every advisory, mapping, validation, source-resolution, or use-case request handled by this companion. Require the current `Algorithm_BO.xml` and current Service Mapping source XML in the same request; the Service Mapping filename may vary. If either XML is missing, stop immediately and ask the implementer to attach both current exports. Validate that `Algorithm_BO.xml` is for `Subscription Management and Account Receivables Integration`, read every version, and reject the request unless the absolute highest `VersionNum` has `ActiveFlag=Y`; do not continue by using an older active version. Validate that the Service Mapping source XML has `contextName="ARInterface"`; if it does not, stop and request the copied Subscription AR Integration source XML. Do not use chat cache, prior project artifacts, remembered file paths, or assumptions to pass this preflight.

When a customer use case involves general Subscription Management behavior, such as subscription lifecycle, products, pricing, billing, or Order Management-created subscriptions, read [Subscription Management General Reference](references/ora_subscription_management_general_reference.md) before an external documentation lookup. Use it for business context only; it does not replace current Service Mapping source, view-object, type, access, or publication confirmation.

For every advisory request handled by this companion, require the business requirement, current `Algorithm_BO.xml`, and current Service Mapping source XML as attachments or explicit file inputs in the same request. If either XML is absent from the current inputs, stop and ask the implementer to attach both current exports; do not proceed from chat cache, prior project artifacts, remembered paths, or default assumptions. Generic navigation or export-how-to questions may be answered without the XMLs, but no mapping recommendation, describe lookup, source-resolution record, or handoff may proceed until both current XMLs are supplied and pass preflight.

Validate `contextName="ARInterface"` before assessing an attached source XML. If it differs, inform the implementer and stop the assessment. To obtain it, instruct the implementer to use **Subscriptions Setup > Dynamic Matrix Configuration > Manage Algorithms > Actions > View Source XML**, copy the source to `servicemappingsource.xml`, and attach it with the business requirement.

## Source discovery and recommendations

Use describe coverage for **subscriptions**, **subscription products**, **bill lines**, **charges**, and **product associations** through covered levels. Treat matching `Pricing*` view objects and their REST describe resources as the same business source.

Use the Input Type 1-5 classification from the primary Manage Algorithms workflow, or classify the prompt with `../manage-algorithms-for-subscriptions-to-accounts-receivables/references/ora_use_case_resolution.md` when this companion is invoked directly. For Type 1, confirm whether the stated source is already exposed. For Type 2, describe only the stated source object when the source attribute is unclear or absent. For Type 3, scan all exposed entities, use Subscription general context, then describe every relevant source object before recommending an object. For Type 4, treat both source and target facts as unresolved until the primary workflow confirms the RA target recommendation and this companion confirms the source. For Type 5 with no source object, accept the primary workflow's generic-reference and official-docs discovery analysis, or perform it if invoked directly, then run environment describe for every relevant object family: subscriptions, subscriptionProducts, billLines, charges, and coveredLevels/ProductAssociations. Return candidates grouped by object fit and do not return control for Groovy drafting until the implementer confirms the named source.

Compare every requested business meaning with existing custom attributes in the current source XML and show both the matching exposed attributes and the missing items. When an exposed attribute matches the entity and meaning, ask whether it is the intended source and return its `attributeType` for downstream target selection. If a source attribute or business term is stated without a source object, scan current exposed attributes across all ARInterface context entities, then run the permitted read-only describe checks across the relevant Subscriptions AR source objects before recommending an object. Use the general Subscription reference only to classify the business term and explain fit; do not use it instead of describe. For every missing item whose business object is known, use that object's aligned read-only describe to search exact and semantically close, queryable scalar candidates. When describe or the current export returns the same or semantically similar candidate under more than one source family, apply a functional-owner tie-breaker before recommending a default: prefer the explicitly stated object; if no object was stated, prefer the source family that owns the business concept by functional responsibility; list copied, denormalized, or convenience fields from other families as alternatives, not as the default. If the functional owner cannot be determined, stop and request the source object or implementer selection. Present the candidate source name, object, type, queryability, compatible mapping type, and the DFF target type family that the primary algorithm workflow should use if the Receivables target is omitted: character for string/varchar/display identifiers/codes/Boolean-as-code, date for date/datetime, and number for number/integer/long/decimal/numeric identifiers. A name ending in `Id` is not enough by itself; recommend a number DFF family only when describe or XML confirms a numeric type. Then require one implementer decision: select a candidate, provide an exact source name, or explicitly accept one named recommended default. A recommended default must name one returned candidate and explain its match; never invent an alias, view-object attribute, type, context, or flex context. If describe cannot run because the runtime environment connection, OAuth/authentication, privileges, transport, or describe endpoint is unavailable, stop and tell the implementer describe is not working. Ask whether to resolve the runtime environment connection and rerun describe, or proceed only with named unconfirmed assumptions for review. If describe runs but is ambiguous or does not return a viable candidate, stop and request the source object and attribute from the implementer.

After each source decision, return a source-resolution record that identifies whether it came from the export, an implementer-provided name, or an accepted named default candidate. Then recommend the smallest mapping change: entity, proposed `_Custom` alias, compatible type, aligned `Pricing*` view object, underlying attribute, and read/write service access. Show the custom-object form, for example `Subscription.LegacyContractNumber_Custom`, while keeping the actual alias dependent on the confirmed source. Mark uncreated, unexposed, or unpublished attributes as prerequisites. Do not return control for Groovy drafting until every required source has a decision.

Present the proposed configuration and Manage Service Mappings UI steps directly in the chat response. Persist the same assessment and steps under the implementation project for traceability, but do not require the implementer to open an artifact to review them. Return the confirmed result to the primary Manage Algorithms skill, which then drafts the Groovy. "Go with assumptions" means only named, evidence-backed source recommendations may be reviewed; it never bypasses preflight, source-resolution records, service access, publication prerequisites, deployed DFF or target-context confirmation, Groovy approval, or XML approval. After that skill creates an approved local `Algorithm_BO.xml`, provide and persist a Service Mapping configuration handoff containing the final selected sources, aliases, entity-to-view-object mappings, data types, access, publication prerequisites, and implementer configuration steps. Include a table with source object, source attribute, Service Mapping alias, target `RA_INTERFACE_LINES_ALL` column when supplied by the primary workflow, `ARInterface.insert` `AttributeName`, `AttributeContext`, `FlexContext`, transaction scope, and confirmed-or-assumed status. Do not edit the exported source XML.

Offer documented Manage Service Mappings UI steps when the implementer asks. Do not create, edit, publish, or return a revised `servicemappingsource.xml`.

## Describe-only REST boundary

Use only the following describe requests. Filter returned attribute names for exact or relevant matches and inspect the returned type whenever a compatible Service Mapping data type must be suggested.

| Service Mapping object | Describe URI |
|---|---|
| `PricingSubscriptions` | `/crmRestApi/resources/11.13.18.05/subscriptions/describe` |
| `PricingProducts` | `/crmRestApi/resources/11.13.18.05/subscriptionProducts/describe` |
| `PricingARAssociations` | `/crmRestApi/resources/11.13.18.05/subscriptionProducts/describe?partialDescription=coveredLevels` |
| `PricingBillLines` | `/crmRestApi/resources/11.13.18.05/subscriptionProducts/describe?partialDescription=billLines` |
| `PricingCharges` | `/crmRestApi/resources/11.13.18.05/subscriptionProducts/describe?partialDescription=charges` |

Describe is the only permitted REST read. Do not create, POST, invoke an action, use a general resource GET request, PUT, PATCH, or DELETE. A describe response supports only a probable-match recommendation; require implementer confirmation before returning a source to Manage Algorithms.

When a permitted describe request fails for runtime-environment reasons, do not replace it with assumptions automatically. Report the failed describe family or URI, classify the failure as connection, authentication, privilege, transport, or endpoint unavailable when possible, and ask the implementer to choose between fixing the runtime environment connection and rerunning describe or continuing only with named unconfirmed assumptions for review. Return to the primary Manage Algorithms workflow only after that choice is recorded.
