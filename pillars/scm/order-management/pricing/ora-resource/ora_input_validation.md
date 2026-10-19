# Manage Price Elements Input Validation

Source: Oracle Fusion Cloud SCM, Manage Pricing Elements (26B).

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICE_ELEMENTS | Manage Price Elements | Price element definition | Element Code, Element Name, Type, Active | Block preview | Supply all four values | Creating a price element | |
| ORA_QP_MANAGE_PRICE_ELEMENTS | Manage Price Elements | Predefined-element review | Search result showing that no predefined element meets the requirement | Block preview | Search active predefined price elements before adding a row | Creating a price element | |

## Field Validation

| Task Code | Task Name | Check | What Happens | Applies When | Resolver |
|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICE_ELEMENTS | Manage Price Elements | Element Code is unique | Reject a code that duplicates an existing price element to avoid a conflict | Creating a price element | |
| ORA_QP_MANAGE_PRICE_ELEMENTS | Manage Price Elements | Active is selected | Permit the element to participate in Pricing calculations | Creating or activating a price element | |
| ORA_QP_MANAGE_PRICE_ELEMENTS | Manage Price Elements | Active is cleared only when not referenced | Reject deactivation when a pricing entity references the element | Deactivating a price element | |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICE_ELEMENTS | Manage Price Elements | QP.PE.VALIDATE | decision | 1 | validate_input | passed->QP.PE.DESIGN;failed->QP.PE.ISSUES | none | stop | Creating, updating, or deactivating a price element |

# Manage Pricing Bases Input Validation

Source: Oracle Fusion Cloud SCM, Manage Pricing Bases (25D); REST API for Oracle Fusion Cloud SCM, Get all pricing bases (26B).

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | Core pricing-basis definition | Name, PriceElementCode, Active | Block preview | Supply the basis name, referenced price-element code, and active value | Creating or importing a pricing basis | |
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | Tier-basis charge criteria | PriceType, ChargeType, ChargeSubtype; Frequency when the charge is recurring | Block preview | Supply the charge criteria that the tier basis includes or excludes | Usage is Tier Basis | |

## Field Validation

| Task Code | Task Name | Check | What Happens | Applies When | Resolver |
|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | Name length | Reject a Name longer than 80 characters | Creating or importing a pricing basis | |
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | PriceElementCode length | Reject a PriceElementCode longer than 30 characters | Creating or importing a pricing basis | |
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | Active value | Accept only Y or N; Y makes the pricing basis active and N makes it inactive | Creating, updating, or importing a pricing basis | |
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | Basis usage | Accept a value supported by the ORA_QP_BASIS_USAGES lookup; use the documented default only when the user leaves Usage blank | Creating or importing a pricing basis | |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | QP.PB.VALIDATE | decision | 1 | validate_input | passed->QP.PB.DEFAULT;failed->QP.PB.ISSUES | none | stop | Creating, updating, or importing a pricing basis |

# Manage Pricing Parameters Input Validation

Source: Manage Pricing Parameters task metadata.

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | Read-only Pricing Parameter Value lookup | Task code ORA_QP_MANAGE_PRICING_PARAMETERS, resolved `pricingParametersUniqID`, and `core.fusion-api.rest-api-client` path `/fscmRestApi/resources/11.13.18.05/qpParameters/{pricingParametersUniqID}/child/qpParameterValues` | Block read result | Resolve the parent Pricing Parameter identifier, then use the declared read-only core REST-client route. Do not upload or initiate a load | Reading Pricing Parameter values | |
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | Data Loader route | Task code ORA_QP_MANAGE_PRICING_PARAMETERS, registered `qpParameterValues` business object, and core Data Loader route | Block routing | Use `core.data-loader`; do not use FSM export/import as the default create/update route | Creating or updating Pricing Parameter values | |
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | Data Loader source validation | Prepared source accepted against the live `qpParameterValues` Data Loader schema | Block routing | Correct the reported Data Loader validation issues before continuing | Creating or updating Pricing Parameter values | |
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | Import-ready change set | Caller-selected create or update data, validated immutable Data Loader artifact, and explicit approval for that artifact | Block import | Validate and preview the Data Loader artifact, then obtain approval | Creating or updating Pricing Parameter values | |

## Field Validation

| Task Code | Task Name | Check | What Happens | Applies When | Resolver |
|---|---|---|---|---|---|

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | QP.PP.VALIDATE | decision | 1 | validate_input | read->QP.PP.REST_GET;create_or_update->QP.PP.DATA_LOADER_VALIDATION;failed->QP.PP.ISSUES | none | stop | Getting Pricing Parameter values through the parameterized core REST-client route and creating or updating through the Data Loader workflow |

# Manage Pricing Charge Definitions Input Validation

Source: Oracle Fusion Cloud SCM, Manage Pricing Charge Definitions (25C); Redwood: Create and Manage Pricing Charge Definitions (26C).

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Existing-definition review | Customer charge details and the active charge-definition set | Block preview | Reuse the closest matching active definition; otherwise retain the documented create outcome | Creating a charge definition | find_best_matching_charge_definition |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Core charge-definition attributes | Charge Definition Code; Name; Applies To; Price Type; Charge Type; Charge Subtype; Active; Setup Enabled | Block preview | For a new definition, require a valid, unique Charge Definition Code. For an update, resolve the supplied code to the existing active definition and retain its applicable attributes. | Creating or updating a charge definition | resolve_charge_definition_by_code |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Combination-uniqueness review | Price Type; Charge Type; Charge Subtype and the current charge-definition set | Block preview | Resolve the exact combination conflict before preparing a create source. | Creating a charge definition | find_charge_definition_combination_conflict |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Recurring-price attribute | User-supplied Price Periodicity UOM Class or the current Site value of `RCS_DEFAULT_UOM_CLASS_CODE_FOR_SVC_DURATION` | Block preview | When omitted, use the nonblank Site profile value. When supplied and it exactly matches that value, notify the user that it is the configured default and recommend retaining it as the best-practice choice. Otherwise preserve the supplied value. | Price Type is Recurring | resolve_recurring_frequency_uom_class |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Usage-price attribute | Usage UOM Class or one uniquely resolved eligible Usage UOM Class | Block preview | Default the uniquely resolved value; otherwise supply the Usage UOM Class. | Price Type is Usage | resolve_single_usage_uom_class |

## Field Validation

| Task Code | Task Name | Check | What Happens | Applies When | Resolver |
|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Code format | Reject a supplied code that is not uppercase alphabetic words separated only by underscores, includes QP, contains spaces, or exceeds 30 characters | A charge-definition code is supplied | |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Charge-definition code for create | Require a nonblank code with valid format and zero current matches; reject an omitted or duplicate code | Creating a charge definition | resolve_charge_definition_by_code |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Charge-definition code for update | Resolve the supplied code to exactly one active charge definition and fill its applicable Price Type, Charge Type, and Charge Subtype; reject no match or multiple matches | Updating a charge definition | resolve_charge_definition_by_code |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Price Type, Charge Type, and Charge Subtype combination | Reject a create when one or more existing definitions have the exact same three codes; require zero matches before preview | Creating a charge definition | find_charge_definition_combination_conflict |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Applies To | Accept only Price, Return, or Shipping | Creating or updating a charge definition | |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Recurring periodicity | Read the Site-level `RCS_DEFAULT_UOM_CLASS_CODE_FOR_SVC_DURATION` profile option. If the recurring-charge value is omitted, require a nonblank resolved profile value; if it is supplied and exactly matches the profile value, issue the configured-default best-practice recommendation without changing it. | Creating or updating a recurring charge definition | resolve_recurring_frequency_uom_class |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Usage UOM Class | Require Usage UOM Class when Price Type is Usage and more than one or no eligible value resolves | Creating or updating a usage charge definition | resolve_single_usage_uom_class |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Runtime availability | Require Active and Setup Enabled for the charge definition to be usable by Pricing at runtime | Creating, activating, or enabling a charge definition | |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | QP.PCD.VALIDATE | decision | 1 | validate_input | passed->QP.PCD.DEPENDENCY;failed->QP.PCD.ISSUES | none | stop | Creating or updating a pricing charge definition through the registered Data Loader REST workflow |


# Manage Rounding Rules Input Validation

Sources: [Round Your Pricing (26C)](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faupr/round-your-pricing.html), [Types of Rounding Rules (26B)](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/faupr/types-of-rounding-rules.html), and the registered pricingRoundingRules Data Loader template inspected in this session. The 26C detail page was unavailable at authoring time.

This graph validates rounding-rule creation through core.data-loader. Data Loader owns field types, schema constraints, supported child sections and operation-specific validation. Apply the required groups to each new rule; do not impose a single-record or precision-only restriction. Updates, deletes and currency assignments are outside this create workflow. No project-specific values or defaults are embedded.

Rule inventory: QP.RR.VALIDATE, QP.RR.LOOKUP, QP.RR.DESIGN, QP.RR.READY, QP.RR.ISSUES, QP.RR.RETURN_ISSUES. IDs identify distinct nodes and are not allocated from row order.

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | Rounding rule definition | Name, RoundingRuleTypeCode, RoundValue, RoundingRuleDirectionCode or RoundingRuleDirection (direction name), ActiveFlag, SetupEnabledFlag | Block validation | Obtain the business choices applicable to the selected rule type; preserve explicit zero and false values; resolve a supplied direction name through resolve_rounding_direction_by_name; do not infer defaults | Creating rounding rules | resolve_rounding_direction_by_name |
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | Loader source contract | Final immutable archive validated by core.data-loader for pricingRoundingRules | Block validation | Complete live template validation and archive preparation first | Creating rounding rules | |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | QP.RR.VALIDATE | decision | 1 | validate_input | passed->QP.RR.LOOKUP;failed->QP.RR.ISSUES | none | stop | Every request |

# Manage Rounding Rule Assignments Input Validation

Sources: [Round Your Pricing (26C)](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faupr/round-your-pricing.html), [Manage Rounding Rules (26B)](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/faupr/manage-rounding-rules.html), and [Create and manage pricing rounding rule assignments (26D)](https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/order26d/26D-order-mgmt-wn-f50338.htm).

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | Currency-specific assignment | Currency; Rounding Rule | Block validation | Select the currency and a rounding rule that exists and is available for assignment | Creating or updating an assignment | verify_assignable_rounding_rule |

## Field Validation

| Task Code | Task Name | Check | What Happens | Applies When | Resolver |
|---|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | Assignment effect | Treat the selected rounding rule as applicable only to items that use the selected currency | Creating or updating an assignment | |
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | Description | Accept a description only when the redesigned assignment page exposes it; it is not required for the documented currency-to-rule assignment | Creating or updating an assignment | |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | QP.RRA.VALIDATE | decision | 1 | validate_input | passed->QP.RRA.LOOKUP;failed->QP.RRA.ISSUES | none | stop | Creating, updating, or deleting a rounding rule assignment |

# Manage Customer Pricing Definitions Input Validation

Source: Oracle Fusion Cloud SCM, Business Objects for Oracle Fusion Cloud SCM, CustomerPricingDefinition (26C).

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | Customer pricing definition | Name when AssignmentTypeCode is not ORA_QP_ALL; AssignmentTypeCode when supplied | Block preview | When Name is omitted and the resulting AssignmentTypeCode is ORA_QP_ALL, apply the documented Customer Pricing Definition for Validation default. When AssignmentTypeCode is omitted, apply the documented ORA_QP_ALL default before preparing a Data Loader source. | Creating or updating a customer pricing definition | |

## Field Validation

| Task Code | Task Name | Check | What Happens | Applies When | Resolver |
|---|---|---|---|---|---|
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | Name | When Name is blank and the resulting AssignmentTypeCode is ORA_QP_ALL, apply the Customer Pricing Definition for Validation default. Otherwise reject a blank name because Oracle documents Name as non-nullable. | Creating or updating a customer pricing definition | |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | Assignment type | Validate a supplied AssignmentTypeCode, or the ORA_QP_ALL default when omitted, against lookup type ORA_QP_CUST_PRICING_ASSN_TYPES through registered Data Loader source review | Creating or updating a customer pricing definition | |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | Global assignment type uniqueness | When the resulting AssignmentTypeCode is ORA_QP_ALL, run the read-only uniqueness lookup. For a create with exactly one existing global definition, prompt to reuse it; for an update, exclude the current resolved primary identifier and require no other global definition. | Creating or updating with AssignmentTypeCode ORA_QP_ALL | ensure_single_global_customer_pricing_definition |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | Pricing strategy | Require PricingStrategyId when AssignmentTypeCode is not 'ORA_QP_ALL' because the business object maps it to the Pricing Strategy identifier | Creating or updating a customer pricing definition | |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | Pricing Strategy child association | Resolve the global parent with AssignmentTypeCode ORA_QP_ALL. If none exists, prepare its separate validated create load, then rerun association resolution after the create succeeds. Resolve the entity type to exactly one supported child collection, and require AssociationStartDate in YYYY-MM-DDTHH:MI:SS.sss+hh:mm format; reject multiple, ambiguous, unsupported, or mismatched values | Associating any entity under a Pricing Strategy | resolve_global_customer_pricing_definition_for_association |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | CPD.VALIDATE | decision | 1 | validate_input | child_association->CPD.RESOLVE_PARENT_PRICING_STRATEGY;passed->CPD.APPLY_DEFAULTS;failed->CPD.ISSUES | none | stop | Creating or updating a customer pricing definition through the registered Data Loader REST workflow |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | CPD.OFFER_REUSE_GLOBAL_DEFINITION | decision | 5 | evaluate_result | accepted->CPD.READY_REUSE;declined->CPD.ISSUES | CPD.CHECK_GLOBAL_ASSIGNMENT | stop | A create request with AssignmentTypeCode ORA_QP_ALL finds exactly one existing global customer pricing definition; prompt the user to use that resolved definition without changing it |

# Manage Pricing Messages Input Validation

Source: the developer-provided parent Pricing SKILL.md workflow and corresponding flat task metadata. Fusion records and operation support remain live authorities; the final immutable source and preflight evidence are supplied by core.data-loader. These rules authorize no Fusion write.

Rule inventory: QP.PM.VALIDATE, QP.PM.LOOKUP, QP.PM.DESIGN, QP.PM.READY, QP.PM.ISSUES, QP.PM.RETURN_ISSUES.

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | Selected environment and request | Active project context; selected environment origin; exact request intent | Block validation | Resolve the selected workflow and environment; never accept an example URL as token-host authority | Every request |  |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | Existing message change | Exact existing message selector; requested MessageText; text-only, add-one-token, or remove-one-token intent; explicit removal intent when deleting | Block validation | Obtain missing request values; do not infer a removal from a text edit | Preparing a message change |  |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | Immutable Data Loader artifact | Final immutable pricingMessages archive; Data Loader validated template, key, operation and mapping evidence; stage child-add, child-delete, or parent-text | Block validation | Complete core.data-loader conversion and preflight before invoking Task Hook; one stage per archive | Preparing a message change |  |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | Token selection | Exact TokenName when an association changes | Block validation | Obtain one requested token; derive identifiers through the declared live lookup | Adding or removing one association |  |

## Field Validation

| Task Code | Task Name | Check | What Happens | Applies When | Resolver |
|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | Source shape | Require nonblank request values and well-formed stage data; preserve explicit false values; Data Loader owns type, key, template and DAT/ZIP validation | Every request |  |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | Request scope | Inventory cannot authorize a load. For writes permit only an existing-message text update or one explicitly requested existing-token association change; reject parent or definition creation/deletion | Every request |  |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | QP.PM.VALIDATE | decision | 1 | validate_input | passed->QP.PM.LOOKUP;failed->QP.PM.ISSUES | none | stop | Every selected task request |
