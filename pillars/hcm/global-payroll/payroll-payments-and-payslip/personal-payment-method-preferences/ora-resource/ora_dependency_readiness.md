# Personal Payment Method Preferences Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Legislative data group | Resolve the requested LDG to one record before using LDG-scoped preference or OPM reads. |
| 2 | Payment Method Preferences finder | Use the documented finder and the intent that matches the requested read. |
| 3 | Organization payment methods | Resolve OPMs only for the resolved LDG when available or noneditable methods are being evaluated. |
| 4 | Preference design | Check the documented LDG-level limits, selectable/noneditable OPM choices, amount-type choice, and allocation rule before preview. |
| 5 | Automatic operation and current preference state | Run Intent SEARCH after LDG resolution. Set operation to CREATE when no preference exists, MERGE when one exists, or DELETE only for a requested deletion of one existing preference. For MERGE, retain every returned attribute, including optional attributes, before applying user overrides. |
| 6 | Custom action contract | Use the supplied Payment Method Preferences custom action only after validations, preview, and explicit approval are complete; set RestAction to POST regardless of the derived operation. |
| 7 | Describe metadata | Retrieve and retain the describe response before claiming field-level metadata beyond the supplied attribute mappings. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| legislative_data_group | Legislative data group | Yes | A specific LDG is requested or a preference is created, updated, or deleted | Lookup | Exact LegislativeDataGroupName | find_ldg_by_exact_name | Preferences are configured at the LDG level | Provide one exact LDG name | LegislativeDataGroupId, LegislationCode |
| payment_method_preference_finder | Payment Method Preferences finder | Yes | A search or creation-eligibility read is requested | Lookup | Intent and optional LegislativeDataGroupName | find_payment_method_preferences | The supplied contract requires the specified finder and Intent | State whether existing preferences or eligible LDGs are required | Preference records or eligible LDG records |
| organization_payment_methods | Organization payment methods | Conditional | Available or noneditable payment methods are selected or displayed | Lookup | Resolved LegislativeDataGroupId | find_organization_payment_methods_by_ldg | OPMs must be obtained in the LDG context | Provide an LDG name or ID first | Organization payment method IDs and names |
| yes_no_lookup | YES_NO common lookup | Conditional | A yes-or-no preference is entered or displayed | Lookup | LookupType YES_NO | find_yes_no_lookup | API payloads use the code and presentation uses the meaning | Provide Yes or No or the approved code | LookupCode, Meaning |
| payment_amount_type | Payment amount type | Conditional | Payment Amount Types is entered or displayed | Satisfied | A, P, or B from the developer-supplied Payment Amount Type Array | resolve_payment_amount_type | The user-facing meaning must correspond to the stored code | Provide Amount, Percentage, Both, or an approved code | PaymentAmountTypes code and presentation meaning |
| preference_operation_resolution | Existing LDG preference | Yes | A mutation is requested | Lookup | Resolved LDG name with Intent SEARCH | find_payment_method_preferences | Operation is derived, never supplied: no preference = CREATE; exactly one preference = MERGE; requested deletion of one existing preference = DELETE | Stop for an ambiguous result or a deletion request without an existing preference; do not ask the user for operation | Derived operation and existing-preference result |
| merge_latest_preference_state | Complete latest existing preference state | Yes | operation is automatically MERGE | Lookup | Resolved LDG name with Intent SEARCH | find_payment_method_preferences | MERGE must represent the complete latest state, not only fields requested for change | Stop if exactly one current preference cannot be returned; retain every returned attribute including optional attributes, overlay validated user values, and do not omit any returned field from the payload or DAT row | Every returned preference attribute, including LegislativeDataGroupId, PaymentMethodsMaximumNumber, ValidationExclusionFlag, PaymentAmountTypes, OrgPaymentMethodsAvailableToWorker, and OrgPaymentMethodsRestrictedForEdit |
| custom_action_write_contract | Payment Method Preferences custom action | Yes | Create, update, or delete is requested | Satisfied | Developer-supplied custom-action contract | | The supplied contract defines one POST custom action, media type, operation values, and attributesMap fields. Populate operation from preference_operation_resolution and set RestAction to POST regardless of whether operation is CREATE, MERGE, or DELETE. For MERGE, attributesMap must contain every listed and every optional returned attribute with its latest value unless the user supplied a validated override. | Use POST with application/vnd.oracle.adf.action+json at /hcmRestApi/resources/latest/paymentMethodOptions/action/paymentMethodOptionsOperation; do not add a second slash between latest and paymentMethodOptions. | operation, RestAction, attributesMap, LegislativeDataGroupId, PaymentMethodsMaximumNumber, ValidationExclusionFlag, PaymentAmountTypes, OrgPaymentMethodsAvailableToWorker, OrgPaymentMethodsRestrictedForEdit, every optional returned attribute |
| describe_metadata | Payment Method Preferences describe response | Conditional | Attribute metadata is requested | Blocked | /hcmRestApi/resources/latest/paymentMethodOptions/describe response | describe_payment_method_options | Required status, updateability, data types, lengths, precision, scale, defaults, nullability, and relationships must come from the live describe response | Supply a redacted describe response or an authorized Fusion environment | One row for every returned attribute and all server-provided metadata |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | A documented exact identifier or literal is already supplied | No |
| Lookup | A documented read-only resolver can uniquely resolve the value | Yes |
| Ambiguous | More than one reference record matches | No |
| Blocked | A required value, prerequisite, preview, approval, or server-validated contract detail is missing | No |
| Duplicate | An existing preference is returned for the selected LDG before create | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PPMP.RESOLVE_DEPENDENCIES | decision | 2 | resolve_dependency | preference_search->PPMP.LOOKUP_PREFERENCES;ldg_resolution->PPMP.LOOKUP_LDG;yes_no_resolution->PPMP.LOOKUP_YES_NO;blocked->RETURN_ISSUES | PPMP.VALIDATE_INPUT | stop | Always |

## Sources

- Oracle Fusion Cloud HCM, Configure Payment Method Preferences: https://docs.oracle.com/en/cloud/saas/human-resources/25a/faipb/configure-payment-method-preferences.html
- Developer-supplied Payment Method Preferences, LDG, OPM, and common-lookup REST routes.
