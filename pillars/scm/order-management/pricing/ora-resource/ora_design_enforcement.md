# Manage Price Elements Design Enforcement

Source: Oracle Fusion Cloud SCM, Manage Pricing Elements (26B), and Redwood: Create and Manage Price Elements (26C).

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Review predefined elements | Use a predefined price element when it meets the requirement to reduce maintenance |
| 2 | Review pricing-guideline eligibility | Do not enable Used in Pricing Guidelines for Cost or Accrual types |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICE_ELEMENTS | Manage Price Elements | Creating a price element | Blocking | | A predefined element was not reviewed before creating a new one | Use a predefined element when it meets the requirement | Yes |
| ORA_QP_MANAGE_PRICE_ELEMENTS | Manage Price Elements | Enabling Used in Pricing Guidelines | Blocking | | Type is Cost or Accrual | Leave Used in Pricing Guidelines disabled | Yes |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICE_ELEMENTS | Manage Price Elements | QP.PE.DESIGN | decision | 2 | design_enforcement | passed->QP.PE.READY;failed->QP.PE.ISSUES | QP.PE.VALIDATE | stop | Creating or updating a price element |

# Manage Pricing Bases Design Enforcement

Source: Oracle Fusion Cloud SCM, Manage Pricing Bases (25D); Adjust Price According to Predefined Attributes (26B).

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | 1 | Review existing pricing bases | Use a predefined pricing basis when it meets the requirement; create a new basis only when no suitable basis exists. |
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | 2 | Align usage and charge criteria | Use Adjustment Basis for a percent adjustment; define the price, charge, and frequency criteria needed for Tier Basis. |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | Creating or importing a pricing basis | Blocking | find_pricing_basis_by_exact_name | An existing suitable pricing basis has not been reviewed | Reuse a suitable predefined basis to reduce maintenance | Yes |
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | Usage is Tier Basis | Blocking | | Required included or excluded charge criteria are absent | Define the applicable price type, charge type, charge subtype, and frequency criteria before import | Yes |

## Design Lookup Requirements

| Task Code | Task Name | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | find_pricing_basis_by_exact_name | Creating or importing a pricing basis | Existing pricing-basis identifiers and comparable setup values | ora_reference_lookups.md |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | QP.PB.DESIGN | decision | 6 | design_enforcement | passed->QP.PB.READY;failed->QP.PB.ISSUES | QP.PB.BASIS_LOOKUP | stop | Creating or importing a pricing basis |

# Manage Pricing Charge Definitions Design Enforcement

Source: Oracle Fusion Cloud SCM, Manage Pricing Charge Definitions (25C); Redwood: Create and Manage Pricing Charge Definitions (26C).

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | 1 | Existing-definition reuse review | Prefer the closest matching active charge definition. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | 2 | Exact-combination review | Require that no existing charge definition has the same Price Type, Charge Type, and Charge Subtype. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | 3 | Historical-use protection | Clear Setup Enabled instead of deleting a definition that historical data still uses. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | 4 | Runtime availability | Keep Active and Setup Enabled selected when Pricing must use the definition at runtime. |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Creating a charge definition | Blocking | find_best_matching_charge_definition | Active definitions have not been reviewed for the closest match | Reuse the closest matching definition; create only when no suitable definition exists | Yes |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Creating a charge definition | Blocking | find_charge_definition_combination_conflict | One or more charge definitions already have the selected Price Type, Charge Type, and Charge Subtype | Select a combination with zero existing matches before preparing a create source | Yes |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Disabling a definition with historical use | Blocking | | The proposed action deletes or deactivates a definition that historical data still uses | Clear Setup Enabled and retain Active for historical records | Yes |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | A custom charge type or subtype is selected | Blocking | resolve_custom_charge_lookup | The documented lookup-code dependency has not been verified | Complete the custom pricing lookup setup before creating the charge definition | Yes |

## Design Lookup Requirements

| Task Code | Task Name | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | resolve_custom_charge_lookup | A custom charge type or subtype is selected | Enabled charge type and subtype lookup codes | ora_reference_lookups.md |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | find_best_matching_charge_definition | Creating a charge definition | Closest matching active charge definition | ora_reference_lookups.md |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | find_charge_definition_combination_conflict | Creating a charge definition | Existing definitions with the selected Price Type, Charge Type, and Charge Subtype | ora_reference_lookups.md |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | QP.PCD.DESIGN | decision | 4 | design_enforcement | passed->QP.PCD.DATA_LOADER_VALIDATION;failed->QP.PCD.ISSUES | QP.PCD.DEFAULT | stop | Creating or updating a pricing charge definition |


# Manage Rounding Rules Design Enforcement

Sources: [Manage Rounding Rules (26B)](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/faupr/manage-rounding-rules.html), the user request to create a new rule, and repository fail-closed overwrite policy. Naming examples in [Round Your Pricing (26C)](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faupr/round-your-pricing.html) contain spaces; retain explicit user spelling rather than silently replacing spaces.

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | 1 | Review existing rules | Evaluate complete lookup results before preview |
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | 2 | Preserve requested behavior | Check runtime and assignment flags against the user's choices |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | Creating rounding rules | Error | find_rounding_rules_for_create | Any exact-name match or incomplete lookup | Review the existing rule; do not turn a create into an update | No |
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | An equivalent active, setup-enabled rule exists | Review | find_rounding_rules_for_create | Reuse decision is unresolved | Prefer reuse; obtain an explicit reason before creating an equivalent rule | No automatic changes |
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | Creating rounding rules | Error | | Prepared flags or rounding choices differ from the user's choices | Active controls runtime availability; Setup Enabled controls availability for assignment. Preserve explicitly disabled choices. | No automatic changes |


## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | QP.RR.DESIGN | decision | 3 | design_enforcement | passed->QP.RR.READY;failed->QP.RR.ISSUES | QP.RR.LOOKUP | stop | Creating rounding rules |

## Design Lookup Requirements

| Task Code | Task Name | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | find_rounding_rules_for_create | Creating rounding rules | exact_name_matches; equivalent_rules; collection_complete | ora_reference_lookups.md |

# Manage Rounding Rule Assignments Design Enforcement

Sources: [Manage Rounding Rules (26B)](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/faupr/manage-rounding-rules.html), [Round Your Pricing (26C)](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faupr/round-your-pricing.html), and [Create and manage pricing rounding rule assignments (26D)](https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/order26d/26D-order-mgmt-wn-f50338.htm).

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | 1 | Confirm prerequisite rule | Confirm the selected rounding rule exists and remains eligible for currency assignment. |
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | 2 | Confirm currency scope | Confirm the requested currency is the intended scope for runtime pricing. |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | Creating or updating an assignment | Error | verify_assignable_rounding_rule | The selected rounding rule does not exist or is not Setup Enabled for assignment | Create or reactivate an eligible rounding rule in Manage Rounding Rules before assigning it | Yes |
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | Creating or updating an assignment | Error | verify_currency_for_rounding_assignment | The selected currency cannot be resolved through an authoritative contract | Confirm the currency through the documented setup experience before proceeding | Yes |
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | Any assignment | Review | | The intended runtime impact on items using the selected currency has not been reviewed | Confirm the rule is appropriate for every item priced in that currency | Yes |

## Design Lookup Requirements

| Task Code | Task Name | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | verify_assignable_rounding_rule | Creating or updating an assignment | Rounding Rule; Setup Enabled status | ora_reference_lookups.md |
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | verify_currency_for_rounding_assignment | Creating or updating an assignment | Currency | ora_reference_lookups.md |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | QP.RRA.DESIGN | decision | 4 | design_enforcement | passed->QP.RRA.READY;failed->QP.RRA.ISSUES | QP.RRA.DEPENDENCY | stop | Creating or updating a rounding rule assignment |

# Manage Pricing Messages Design Enforcement

Source: the developer-provided parent Pricing SKILL.md workflow and corresponding flat task metadata. Fusion records and operation support remain live authorities; the final immutable source and preflight evidence are supplied by core.data-loader. These rules authorize no Fusion write.

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | 1 | Validate permitted effect | Evaluate the task-scoped Design Rules after the declared live lookups; a ready result permits only the core workflow handoff |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | Every request | Blocking | resolve_pricing_message_and_tokens | A GET request is being used to authorize a load, or parent/definition creation or deletion is requested | Stop; preserve the supported existing-record and read-only boundaries | No |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | Adding an association | Blocking | resolve_pricing_message_token_definition | The requested token is not uniquely eligible in the parent pricing entity or is already attached | Stop; do not create a definition or duplicate an association | No |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | Removing an association | Blocking | resolve_pricing_message_and_tokens | Removal intent is not explicit, the unique child key or parent differs from the live record, or final MessageText still references the removed token | Stop; preserve all other associations and the shared definition | No |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | Every message change | Blocking |  | Final immutable artifact lacks validated operation-specific mappings, target keys, current usable child template when needed, or update-only parent mapping; it includes a parent DELETE, definition write or unrelated row | Stop before approval; core.data-loader must validate the exact bytes and mappings. Child registration or sample synthesis alone is insufficient | No |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | Parent text stage following a child load | Blocking | resolve_pricing_message_and_tokens | No separately requested status confirmation of zero-failure child completion exists, expected child state is absent, unrelated associations changed, or parent identity/text changed since preflight | Stop; reconcile through the selected status/read workflow. Prepare and validate the parent stage separately before its own approval | No |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | Every message change | Blocking |  | Task Hook skipped this task, any task resource is unavailable, or rules have not passed for the final immutable archive | Stop before approval and submission; do not treat skipped validation as success for this task | No |

## Design Lookup Requirements

| Task Code | Task Name | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | resolve_pricing_message_and_tokens | Every message inventory or change; repeat before the next separately validated parent stage | Verified parent identity, current text, pricing entity, complete token collection and child keys | ora_reference_lookups.md |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | resolve_pricing_message_token_definition | Adding one missing existing-token association | Verified existing token attribute identity and eligibility | ora_reference_lookups.md |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | QP.PM.DESIGN | decision | 3 | design_enforcement | passed->QP.PM.READY;failed->QP.PM.ISSUES | QP.PM.LOOKUP | stop | Every selected task request; evaluate only applicable rules |
