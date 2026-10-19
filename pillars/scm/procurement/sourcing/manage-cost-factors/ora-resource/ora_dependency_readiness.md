# Manage Cost Factors Dependency Readiness

Sources: User-provided Manage Cost Factors business-rule content from Confluence page 14988929751; confirmed Data Loader business object `supplierNegotiationCostFactors`; live Data Loader attribute-details workbook generated on 2026-09-04.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Data Loader business-object and foreign-key metadata | Resolve `supplierNegotiationCostFactors` and its pricing-basis foreign-key attributes through `core.data-loader` live metadata validation before preparing a Cost Factor archive |
| 2 | Internal-user page access privilege | Confirm that the user holds PON_MANAGE_SUPPLIER_NEGOTIATION_COST_FACTOR before managing Cost Factors in the interactive Redwood page |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| COST_FACTOR.DATA_LOADER_RESOURCE | `supplierNegotiationCostFactors` with `PricingBasisCode` / `PricingBasis` foreign-key metadata | Yes | A Data Loader archive is prepared or submitted | Ready per run | `businessObject` in this task's `SKILL.md`, resolved by the live `core.data-loader` metadata validator |  | It is the confirmed registered business object and pricing-basis relationship for Cost Factors | Resolve the object and preserve the live-generated foreign-key columns; stop if live metadata validation fails | The live metadata result for the current archive |
| COST_FACTOR.MANAGE_PRIVILEGE | PON_MANAGE_SUPPLIER_NEGOTIATION_COST_FACTOR | Yes | The interactive Redwood page is used | Separate UI gate | Fusion security role-assignment evidence for the interactive user |  | The BR requires this internal-user page-access privilege for page use | Provide evidence that the interactive user has the privilege, or request the appropriate access | Current interactive-user access evidence, only for UI work |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Data Loader dependency blocker | `supplierNegotiationCostFactors` or its pricing-basis foreign-key metadata cannot be resolved by live Data Loader metadata validation | No |
| Authorization blocker | The interactive Redwood page is used and the required page-access privilege is not confirmed | No for the UI route |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COST_FACTOR.VERIFY_DATA_LOADER_RESOURCE | decision | 10 | resolve_dependency | satisfied->COST_FACTOR.VALIDATE_DATA_LOADER_INPUT;blocked->RETURN_ISSUES | none | stop | A Data Loader operation is requested; the separate UI privilege gate applies only to interactive-page work |
