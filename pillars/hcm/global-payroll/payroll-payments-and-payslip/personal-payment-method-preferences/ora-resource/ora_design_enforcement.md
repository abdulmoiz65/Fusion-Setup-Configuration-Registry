# Personal Payment Method Preferences Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve LDG | Select one valid LDG because the preference applies at the LDG level. |
| 2 | Resolve OPMs | Select available and noneditable OPMs only from the resolved LDG. |
| 3 | Apply preference limits | Check the employee payment-method maximum, amount-type choice, and allocation treatment. |
| 4 | Check presentation behavior | When multiple selected OPMs share a payment type, present the OPM selection list behavior described by Oracle. |
| 5 | Confirm custom-action boundary | Derive operation from SEARCH, set RestAction to POST regardless of operation, confirm resolved values, preview, and explicit approval before a separately authorized executor uses the supplied custom action. For MERGE, refresh the existing preference and verify the payload or DAT row contains the complete latest state, including optional attributes. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A preference is created, viewed, or changed | Error | find_ldg_by_exact_name | LDG is absent, unresolved, or ambiguous | Select one valid LDG before evaluating the preference | Yes |
| Available or noneditable payment methods are selected | Error | find_organization_payment_methods_by_ldg | An OPM is not in the selected LDG or cannot be uniquely resolved | Use only OPMs returned for the resolved LDG | Yes |
| Employees can choose multiple OPMs with the same payment type | Error | find_organization_payment_methods_by_ldg | The user-facing design does not expose the OPM list implied by the documented configuration | Present an OPM selection list rather than only the payment-type list | Yes |
| Payment amount type is unset | Warning | | No explicit value is supplied | Apply the documented Both default and show it to the requester | Yes |
| A payment method is noneditable and allocation validation is configured | Error | find_yes_no_lookup | The yes-or-no treatment for exclusion from 100% validation is unresolved | Resolve and present the chosen YES_NO meaning before preview | Yes |
| Available Payment Methods or Noneditable Payment Methods contains one or more entries | Error | find_organization_payment_methods_by_ldg | Any supplied OPM is unresolved, ambiguous, outside the selected LDG, or removed from the ordered list | Resolve every value in LDG context; retain REST response formatting as pipe-separated and use comma-separated validated IDs only when generating DAT content | Yes |
| A pipe-separated OPM value is fetched through REST | Error | find_organization_payment_methods_by_ldg | The value has an empty entry or a duplicate that has not been normalized under the stated first-occurrence rule | Reject empty entries; remove duplicate IDs while retaining first-occurrence order unless the REST contract explicitly requires duplicates; retain pipe-separated formatting for REST presentation | Yes |
| DAT content is generated for either OPM attribute | Error | find_organization_payment_methods_by_ldg | OrgPaymentMethodsAvailableToWorker or OrgPaymentMethodsRestrictedForEdit contains a pipe delimiter or an unvalidated ID | Use the validated ordered OPM IDs joined with commas; apply this delimiter only to DAT content | Yes |
| A mutation is prepared | Error | find_payment_method_preferences | operation was supplied rather than derived, the result is ambiguous, or the LDG is unresolved | Resolve the LDG and SEARCH it. Set CREATE for no preference, MERGE for one preference, and DELETE only when deletion was requested for one existing preference. | Yes |
| operation is CREATE | Error | find_payment_method_preferences | SEARCH did not confirm that no preference exists or a reference is unresolved | Use CREATE only after SEARCH returns no preference and all supplied validations pass | Yes |
| operation is MERGE | Error | find_payment_method_preferences | The LDG association would change, the current preference is absent or ambiguous, an optional returned attribute is omitted, a value is stale, or a changed field is unresolved | Run SEARCH immediately before construction. Use LegislativeDataGroupId as immutable identity; populate every returned attribute, including optional attributes, and overlay only validated user values. | Yes |
| Deletion is requested | Error | find_payment_method_preferences | No preference exists for the resolved LDG | Return a not-found validation message and do not invoke the custom action | No |
| operation is DELETE | Error | find_payment_method_preferences | The attributesMap child row is absent, or its LegislativeDataGroupId does not equal the resolved preference identity | Emit one attributesMap DELETE row. Populate PreferencesKey and LegislativeDataGroupId with the resolved ID, set RestAction to POST, and leave all other child business attributes blank. | Yes |
| A mutation is prepared for a separately authorized executor | Error | | The path, HTTP method, media type, or RestAction differs from the developer-supplied custom-action contract | Use HTTP POST, RestAction POST for CREATE, MERGE, and DELETE, application/vnd.oracle.adf.action+json, and /hcmRestApi/resources/latest/paymentMethodOptions/action/paymentMethodOptionsOperation exactly | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_ldg_by_exact_name | An LDG name is supplied | LegislativeDataGroupId, LegislationCode | ora_reference_lookups.md |
| find_organization_payment_methods_by_ldg | OPM selection or display is required | Organization payment method IDs and names | ora_reference_lookups.md |
| find_yes_no_lookup | Exclusion from 100% validation is set or displayed | LookupCode, Meaning | ora_reference_lookups.md |
| resolve_payment_amount_type | Payment Amount Types is set or displayed | PaymentAmountTypes code, user-facing meaning | ora_reference_lookups.md |
| find_payment_method_preferences | A mutation is prepared | Derived operation and, for MERGE, every latest returned attribute including optional attributes | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PPMP.ENFORCE_DESIGN | decision | 8 | design_enforcement | pass->PPMP.EXECUTION_GATE;blocked->RETURN_ISSUES | PPMP.APPLY_DEFAULTS | stop | Any preference request |

## Sources

- Oracle Fusion Cloud HCM, Configure Payment Method Preferences: https://docs.oracle.com/en/cloud/saas/human-resources/25a/faipb/configure-payment-method-preferences.html

## Data Loader Execution Enforcement

This section governs execution without removing or changing the preceding reference material.

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any actual create, import, or load | Error | | A direct CRUD endpoint or custom action is selected as the execution route | Use core.data-loader with the paymentMethodOptions business object. | Yes |
| Any actual create, import, or load | Error | | The Data Loader business object is not paymentMethodOptions | Correct the business object before sample generation, preview, or approval. | Yes |

## Execution Policy Source

- Developer instruction: retain documented instructions for reference; perform actual data create, import, and load through the documented business object.
