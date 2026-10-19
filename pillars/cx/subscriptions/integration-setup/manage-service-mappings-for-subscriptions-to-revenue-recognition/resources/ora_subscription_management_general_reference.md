# Subscription Management General Reference - RMCS Mapping

## Use

Use general Subscription Management documentation to understand the business rule and its subscription, product, charge or revenue-output scope. Keep that business meaning separate from verified runtime source exposure and algorithm behavior.

## Source

The [existing mapping source catalogue](../ora-resource/ora_reference_lookups.md#source-catalogue) retains the supplied Subscription Management guide, the RMCS integration-only guide and physical data-model documentation with reviewed release boundaries. General documentation does not establish the current Service Mapping source, algorithm version, aliases, cardinalities, custom field exposure, service access or publication state.

## Companion resource mapping

| Need | RMCS resource | Ownership |
|---|---|---|
| Required attachments, integration identity and version eligibility | [Algorithm XML preflight](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_algorithm_xml_guidance.md#input-preflight) | Primary Algorithms |
| Source discovery, metadata/type compatibility, protected output schema and mapping/access checks | [Service Mapping Guidance](ora_service_mapping_guidance.md) | Service Mappings companion |
| Per-source acceptance, evidence and unresolved prerequisites | [Source-resolution record](ora_service_mapping_guidance.md#source-resolution-record) | Service Mappings companion |
| Optional describe acquisition and its execution gates | [Live lookups](../ora-resource/ora_reference_lookups.md#live-lookups) | Task ora-resource lookup owner |
| Use-case classification and request/return record | [Use-Case Resolution](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_use_case_resolution.md) | Primary Algorithms owns classification and continuation |
| Complete output/source configuration traceability | [Final traceability and configuration handoff](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_use_case_resolution.md#final-traceability-and-configuration-handoff) | One primary-owned schema; companion supplies source configuration facts |
| Physical source/target documentation and runtime distinction | [RMCS Data Model Reference](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_rmcs_data_model_reference.md) | Primary reference; runtime mapping remains separately verified |
| Function-backed sources, direct writes, inserts and skip behavior | [Groovy Function Guidance](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_groovy_function_guidance.md) | Primary Algorithms |

## Boundaries

This context/index file defines no execution route. Follow the owning resource for each operation; do not import Receivables-specific Groovy, context literals, aliases or publication procedures. Keep source resolution separate from the primary's approved local artifact work, and retain unresolved evidence in the companion return. No Fusion write is authorized by these resources.
