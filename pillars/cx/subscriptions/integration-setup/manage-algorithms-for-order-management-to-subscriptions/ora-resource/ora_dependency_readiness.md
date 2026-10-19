# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Service Mapping assessment | Validate the companion assessment and its mapping_status before deciding whether an Algorithm is needed; resolve every mapping-information placeholder before preparing an approval-ready draft. A complete plan with `service_mapping_validation_skipped=true` may proceed only as the explicitly labelled provisional path |
| 2 | Algorithm necessity | Determine whether the assessment evidences an existing direct mapping, a Service Mapping prerequisite, or an Algorithm candidate |
| 3 | Safe algorithm version | Confirm the latest nonprotected active version, or the next unused active version when none exists, only when a reviewable draft or artifact is requested |
| 4 | Subscription integration feature | Obtain implementation evidence before relying on a test line |
| 5 | Duration and pricing compatibility | Obtain configuration evidence when the change affects duration, rate plan, or pricing context |
| 6 | Fulfillment orchestration | Obtain implementation evidence that fulfillment completes before the interface |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| OMSUBALGO.MAPPING_ASSESSMENT | Validated service_mapping_assessment | Yes | Every FOM-to-OSS algorithm recommendation or change request | Verify | Companion task output supplied as an Algorithm input | resolve_service_mapping_assessment | Algorithm logic must not infer an unconfirmed mapping, source attribute, target, or assignment | Supply a validated assessment covering the requested outcome | Context, source and target evidence, permissions, direct-assignment evidence, metadata status, mapping_status, algorithm_recommendation, assumptions, prerequisites |
| OMSUBALGO.ALGORITHM_BO_VERSION | FOM-to-OSS Algorithm_BO XML and safe target | Conditional | A reviewable draft or local artifact is requested | Verify | User-supplied Algorithm_BO.xml |  | Edit the latest nonprotected active version, or create the next unused version with ActiveFlag Y | User may ensure an active version exists | Algorithm identity, active target, and new version when needed |
| OMSUBALGO.FEATURE_OPT_IN | Subscription processing feature | Yes | A change will be tested with an Order Management line | Verify | User-supplied implementation evidence |  | Integration behavior applies only to lines created after opt-in | Supply feature state and post-opt-in test-line evidence | Feature state and test-line applicability |
| OMSUBALGO.DURATION_PRICING | Service-duration and price-periodicity UOM compatibility | Conditional | The change affects duration, rate plan, or pricing context | Verify | User-supplied configuration evidence |  | Incompatible UOM classes can invalidate behavior | Supply UOM compatibility evidence | UOM classes and time mappings |
| OMSUBALGO.FULFILLMENT_ORCHESTRATION | Subscription fulfillment orchestration | Yes | The change relies on the FOM-to-OSS interface | Verify | User-supplied orchestration evidence |  | Interface processing must not precede fulfillment | Supply fulfillment-before-interface evidence | Process identity and orchestration evidence |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Input version blocker | The BO is malformed, has another identity, would change Version 0 or 1, or cannot derive the next numeric version when no active version exists | No: request a valid export |
| Assessment blocker | An algorithm recommendation or change lacks a validated applicable companion assessment | No: request the assessment; do not infer mapping facts |
| Mapping prerequisite | The assessment reports a mapping gap, metadata blocker, or type incompatibility | No: return the Service Mapping prerequisite and mapping-information request. A complete exact mapping-gap plan with an explicitly approved `service_mapping_validation_skipped=true` marker may proceed only to the labelled provisional draft; otherwise an approval-ready draft requires the companion task's revalidated response |
| Verify | Implementation evidence is required before testing or final design review | No: do not substitute unsupported lookup or create operations |
| Blocked | Required evidence is missing, contradictory, or incompatible | No: stop and return the missing evidence |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OMSUBALGO.RESOLVE.MAPPING.ASSESSMENT | decision | 2 | resolve_dependency | ready->OMSUBALGO.RESOLVE.DEPENDENCIES;blocked->OMSUBALGO.RETURN.ISSUES | OMSUBALGO.VALIDATE.REQUEST | stop | Input validation passed |
| OMSUBALGO.RESOLVE.DEPENDENCIES | decision | 3 | resolve_dependency | satisfied->OMSUBALGO.ENFORCE.DESIGN;blocked->OMSUBALGO.RETURN.ISSUES | OMSUBALGO.RESOLVE.MAPPING.ASSESSMENT | stop | The mapping assessment is validated and all conditionally applicable dependencies are satisfied |

## Sources

- User-approved FOM-to-OSS operating model: Algorithm recommendations and changes consume a validated Service Mapping assessment before determining whether an Algorithm is needed.
- Oracle Fusion Cloud Subscription Management, Using Subscription Management, Create Subscriptions from Order Management: https://docs.oracle.com/en/cloud/saas/subscription-management/fasum/using-subscription-management.pdf
