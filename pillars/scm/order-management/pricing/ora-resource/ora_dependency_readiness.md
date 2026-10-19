# Manage Pricing Bases Dependency Readiness

Source: Oracle Fusion Cloud SCM, Roadmap to Manage Oracle Fusion Pricing (26B); Manage Pricing Bases (25D).

## Required Dependency Order

| Task Code | Task Name | Sequence | Dependency | What Must Happen |
|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | 1 | Price Elements | Complete Manage Price Elements and resolve the active price element before creating or importing a pricing basis that references it. |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | PB.PRICE_ELEMENT | Price Element | Yes | Creating or importing a pricing basis | Verify | User-provided PriceElementCode, verified through the Price Elements REST resource | find_price_element_by_exact_code | Each pricing basis references a price element to calculate the adjustment | Provide the exact active price-element code; complete Manage Price Elements first when it does not exist | PriceElementCode; PriceElementName |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | Blocked | The price element is absent, inactive, or ambiguous | Lookup only; do not create or activate the dependency from this task |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | QP.PB.DEPENDENCY | decision | 4 | resolve_dependency | ready->QP.PB.BASIS_LOOKUP;missing->QP.PB.ISSUES;failed->QP.PB.ISSUES | QP.PB.PRICE_ELEMENT_LOOKUP | stop | A pricing basis references a price element |

# Manage Pricing Charge Definitions Dependency Readiness

Source: Oracle Fusion Cloud SCM, Add Your Own Lookup to Charge Types (25D); Manage Pricing Charge Definitions (25C).

## Required Dependency Order

| Task Code | Task Name | Sequence | Dependency | What Must Happen |
|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | 1 | Pricing lookup codes | For a custom charge type or subtype, first add enabled lookup codes in Manage Pricing Lookups before creating the charge definition. |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | PCD.CUSTOM_LOOKUPS | Charge type and charge subtype lookup codes | Conditional | A custom charge type or charge subtype is selected | Verify | Apps Common standard lookup route for ORA_QP_CHARGE_TYPES and ORA_QP_CHARGE_SUBTYPES | resolve_custom_charge_lookup | A custom charge definition must reference the charge type and subtype added to the documented Pricing lookups | Complete and verify the enabled lookup codes in ORA_QP_CHARGE_TYPES and ORA_QP_CHARGE_SUBTYPES before preparing the charge definition | ChargeType; ChargeSubtype |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | PCD.MISSING_LOOKUP_PROPOSAL | Missing charge type or subtype | Conditional | Creating a new charge definition with either field omitted | Generate | Enabled Pricing price-type, charge-type, and charge-subtype lookups plus current charge definitions | generate_unused_charge_combination | A generated combination must not duplicate an exact current Price Type, Charge Type, and Charge Subtype combination | Present one enabled unused three-code combination and obtain approval before source preparation. | Proposed PriceType; ChargeType; ChargeSubtype; approval |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Blocked | A custom charge type or subtype has not been confirmed as enabled | Lookup contract TBD; do not create or enable lookup codes from this task |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Blocked | An omitted Charge Type or Charge Subtype has no confirmed recommendation or its draft-new lookup is not enabled | Recommendation and lookup only; do not select, create, or enable a lookup from this task |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | QP.PCD.DEPENDENCY | decision | 2 | resolve_dependency | ready->QP.PCD.DEFAULT;blocked->QP.PCD.ISSUES;failed->QP.PCD.ISSUES | QP.PCD.VALIDATE | stop | Creating or updating a pricing charge definition |

# Manage Rounding Rule Assignments Dependency Readiness

Sources: [Manage Rounding Rules (26B)](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/faupr/manage-rounding-rules.html) and [Round Your Pricing (26C)](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faupr/round-your-pricing.html).

## Required Dependency Order

| Task Code | Task Name | Sequence | Dependency | What Must Happen |
|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | 1 | Rounding Rule | Create or identify the rounding rule before assigning it to a currency. |
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | 2 | Assignment-eligible rule | Confirm that the selected rule remains Setup Enabled; an unavailable rule cannot be assigned to a currency. |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | RRA.ROUNDING_RULE | Existing rounding rule | Yes | Creating or updating an assignment | Verify | `pricingRoundingRules` collection: exact Name, ActiveFlag=true, SetupEnabledFlag=true | verify_assignable_rounding_rule | Oracle requires a rounding rule to exist before it can be assigned to a currency | Select the intended rule, then resolve the exact active, setup-enabled record | RoundingRuleId; canonical Name; eligibility receipt |
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | RRA.CURRENCY | Existing currency | Yes | Creating or updating an assignment | Verify | `currenciesLOV` collection: exact CurrencyCode, enabled, monetary, and effective | verify_currency_for_rounding_assignment | Pricing uses the assignment only for items that use the selected currency | Select the intended currency, then resolve the exact eligible currency record | CurrencyCode; Name; eligibility receipt |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | Blocked | The rounding rule or currency cannot be uniquely verified | Lookup only; do not create a rounding rule or currency from this task |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | QP.RRA.DEPENDENCY | decision | 3 | resolve_dependency | ready->QP.RRA.DESIGN;blocked->QP.RRA.ISSUES;failed->QP.RRA.ISSUES | QP.RRA.LOOKUP | stop | Creating or updating a rounding rule assignment |
