# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Mapping outcome evidence | Classify the validated XML as an evidenced existing mapping, source-and-target availability without assignment evidence, a mapping gap, or a metadata or compatibility blocker |
| 2 | Subscription integration feature | Obtain implementation evidence that the Order Management to Subscription Management processing feature is enabled before relying on a test line |
| 3 | Mapping grouping impact | Identify whether the recommended mapping affects documented subscription grouping attributes and state the intended outcome |
| 4 | Duration and pricing compatibility | Obtain configuration evidence when the recommendation affects service duration, rate plan, or pricing context |
| 5 | Fulfillment orchestration | Obtain implementation evidence that Order Management fulfillment completes before the Subscription Management interface |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| OMSUBMAP.FEATURE_OPT_IN | Integrate Order Management with Subscription Management to Process Subscriptions | Yes | A recommendation will be tested with an Order Management line | Verify | User-supplied implementation evidence |  | The integration applies to order lines created after feature opt-in | Supply feature state and post-opt-in test-line evidence | Feature state and test-line applicability |
| OMSUBMAP.GROUPING_CONTEXT | Inbound subscription grouping context | Conditional | The recommendation can affect customer, product or offering, bill-to or ship-to, rate plan or pricing context, or subscription dates | Verify | User-supplied mapping and grouping evidence |  | A mapping recommendation must preserve an intentional grouping outcome | Identify affected grouping attributes and intended outcome | Affected attributes and intended grouping outcome |
| OMSUBMAP.DURATION_PRICING | Service-duration and price-periodicity UOM compatibility | Conditional | The recommendation affects service duration, rate plan, or pricing context | Verify | User-supplied configuration evidence |  | Incompatible UOM classes can invalidate the design | Supply service-duration UOM class, time mappings, and price-periodicity UOM class | UOM compatibility evidence |
| OMSUBMAP.FULFILLMENT_ORCHESTRATION | Subscription fulfillment orchestration | Yes | Every recommendation that relies on the FOM-to-OSS interface | Verify | User-supplied orchestration evidence |  | The interface must not be assessed as sending an item before fulfillment | Supply process identity and fulfillment-before-interface evidence | Orchestration evidence |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Verify | The requirement is supported only by implementation evidence supplied with the request | No: do not substitute a database query, browser shortcut, or undocumented REST call |
| Blocked | Required evidence is missing, contradictory, or incompatible | No: return the missing evidence and stop the assessment |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OMSUBMAP.RESOLVE.DEPENDENCIES | decision | 3 | resolve_dependency | satisfied->OMSUBMAP.ENFORCE.DESIGN;blocked->OMSUBMAP.RETURN.ISSUES | OMSUBMAP.DESCRIBE.METADATA | stop | XML mapping outcome and every required describe lookup passed |

## Sources

- Oracle Fusion Cloud Subscription Management, Using Subscription Management, Create Subscriptions from Order Management: https://docs.oracle.com/en/cloud/saas/subscription-management/fasum/using-subscription-management.pdf
- Oracle Fusion Cloud Order Management, Integrate Order Management with Subscription Management: https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faiom/integrate-order-management-with-subscription-management.html
