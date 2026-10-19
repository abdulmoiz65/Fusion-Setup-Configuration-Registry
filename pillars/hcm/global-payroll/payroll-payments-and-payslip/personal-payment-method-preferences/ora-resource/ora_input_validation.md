# Personal Payment Method Preferences Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Search intent | Intent = SEARCH | Stop and request SEARCH | State that the request is for existing Payment Method Preferences | Existing-preference search is requested | |
| Creation-eligibility intent | Intent = CREATE | Stop and request CREATE | State that the request is to identify LDGs eligible for preference creation | Eligible-LDG search is requested | |
| Legislative data group identity | LegislativeDataGroupName | Stop and request the exact LDG name when a specific LDG is requested | Supply the LDG display name for exact resolution | A request is scoped to one LDG | find_ldg_by_exact_name |
| Preference mutation identity | LegislativeDataGroupId and deletion intent only when deletion is requested | Stop only for an unresolved LDG or a deletion request that cannot be classified | Resolve the LDG name, query the existing preference with Intent SEARCH, and set operation automatically: no preference = CREATE; exactly one preference = MERGE; requested deletion of an existing preference = DELETE | Create, update, or delete is requested | find_payment_method_preferences |
| Available Payment Methods | One or more OPM IDs or names | Stop and report every unresolved value | Resolve each supplied value in the selected LDG and preserve input order | Available Payment Methods is supplied | find_organization_payment_methods_by_ldg |
| Noneditable Payment Methods | One or more OPM IDs or names | Stop and report every unresolved value | Resolve each supplied value in the selected LDG and preserve input order | Noneditable Payment Methods is supplied | find_organization_payment_methods_by_ldg |
| Data Loader parent fields | PreferencesKey, operation, Content-Type, REST-Framework-Version, RestAction | Stop preparation | Populate operation from the SEARCH-derived decision; set RestAction to POST for CREATE, MERGE, and DELETE; populate Content-Type and REST-Framework-Version for every DAT parent row; resolve LegislativeDataGroupId and use that exact value as PreferencesKey | Any DAT file is prepared | find_payment_method_preferences |
| Data Loader attributesMap fields | For CREATE or MERGE: PreferencesKey, LegislativeDataGroupId, PaymentMethodsMaximumNumber, ValidationExclusionFlag, PaymentAmountTypes, OrgPaymentMethodsAvailableToWorker, OrgPaymentMethodsRestrictedForEdit, RestAction, and every optional attribute returned for MERGE. For DELETE: PreferencesKey, RestAction, and LegislativeDataGroupId. | Stop preparation | Always emit a populated attributesMap child row. Set RestAction to POST for CREATE, MERGE, and DELETE. For DELETE, LegislativeDataGroupId is the only business attribute required; populate it with the resolved ID, use that same ID as PreferencesKey, and leave all other child business attributes blank. For MERGE preserve every returned optional attribute unless a user-supplied value overrides it. Use comma-separated OPM IDs for the two OPM attributes when they apply. | Any CREATE, MERGE, or DELETE DAT file is prepared | find_payment_method_preferences |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An LDG name is supplied | The name must resolve to exactly one LDG | Stop on no match or multiple matches; otherwise retain LegislativeDataGroupId and LegislationCode | find_ldg_by_exact_name |
| Organization payment methods are supplied for available or noneditable selection | The LDG must already resolve | Resolve organization payment methods only in the resolved LDG context | find_organization_payment_methods_by_ldg |
| Intent is SEARCH or CREATE | The finder must be findByLegislativeDataGroupName with the matching Intent value | Stop and correct the finder or Intent before the read | find_payment_method_preferences |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Finder name and Intent pairing | Existing-preference reads require findByLegislativeDataGroupName and SEARCH; creation-eligibility reads require the same finder and CREATE | A Payment Method Preferences finder is requested | find_payment_method_preferences |
| LDG context for organization payment methods | Do not retrieve organization payment methods without a resolved LegislativeDataGroupId | An OPM lookup is requested | find_organization_payment_methods_by_ldg |
| Payment amount type | Accept A, P, or B only; present Amount, Percentage, or Both respectively | A payment amount type is supplied | resolve_payment_amount_type |
| Validation exclusion flag | Accept Y or N only; resolve a supplied Yes or No meaning before using the returned code | Exclude from 100% Validation is supplied | find_yes_no_lookup |
| Maximum Personal Payment Methods | Require a whole number containing digits only; reject decimals, signs, and nonnumeric text | Maximum Personal Payment Methods is supplied | |
| REST OPM response values | Split each fetched Available Payment Methods or Noneditable Payment Methods value on pipe, trim whitespace, reject an empty entry, resolve every remaining entry, remove duplicate IDs while preserving their first-occurrence order unless a future REST contract explicitly requires duplicates, and retain pipe-separated formatting for presentation | A multi-value OPM value is fetched through REST | find_organization_payment_methods_by_ldg |
| DAT OPM value conversion | Resolve the ordered user-provided OPM IDs, reject an empty, invalid, or ambiguous value, then join the IDs with a comma for OrgPaymentMethodsAvailableToWorker and OrgPaymentMethodsRestrictedForEdit. Do not use a pipe in DAT content. | User-provided OPM input is converted into DAT content | find_organization_payment_methods_by_ldg |
| User-facing labels | Present Available Payment Methods, Noneditable Payment Methods, Maximum Personal Payment Methods, Payment Amount Types, Exclude from 100% Validation, and Legislative Data Group; do not expose REST attribute names unless technical detail is explicitly requested | A preference is displayed | |
| Maximum Personal Payment Methods | Require a supplied whole-number value and leave its allowed range to the custom action’s server validation because no range is supplied | Create or update includes Maximum Personal Payment Methods | |
| Automatic operation selection | Never request or accept operation as an input. After resolving the LDG, run Intent SEARCH: set CREATE when no preference exists; set MERGE when exactly one preference exists; set DELETE only when the user requests deletion and exactly one preference exists. | A mutation is requested | find_payment_method_preferences |
| MERGE current-state acquisition | Run Intent SEARCH for the resolved LDG, obtain the one existing preference, and retain every attribute returned by that preference, including optional attributes, before constructing the payload or DAT row. | operation is automatically MERGE | find_payment_method_preferences |
| MERGE field selection | Populate every returned preference attribute, including optional attributes, in the payload or DAT row. Replace a returned value only when the user supplied a validated value for that attribute; retain every other just-read value. Also include every supplied custom-action-contract attribute. Reject a modified-fields-only payload and do not use a stale cached value. | operation is automatically MERGE | find_payment_method_preferences |
| Delete field selection | Set operation to DELETE only after SEARCH confirms that one preference exists for the resolved LDG. | Deletion is requested | find_payment_method_preferences |
| DAT parent construction | Always populate Content-Type and REST-Framework-Version; set parent PreferencesKey to the resolved LegislativeDataGroupId and populate the same value in the child PreferencesKey | Any DAT file is prepared | find_ldg_by_exact_name |
| DAT attributesMap completeness | Always emit an attributesMap child row. For DELETE, populate PreferencesKey and LegislativeDataGroupId with the resolved ID, set RestAction to POST, and leave all other child business attributes blank. For CREATE and MERGE, include all attributesMap values and do not emit a partial child row. RestAction is POST for every operation. Format OrgPaymentMethodsAvailableToWorker and OrgPaymentMethodsRestrictedForEdit as comma-separated OPM IDs when they apply. | Any CREATE, MERGE, or DELETE DAT file is prepared | find_ldg_by_exact_name |

## Evaluation Scenarios

| ID | Request | Expected Result |
|---|---|---|
| PPMP-E01 | Show all Payment Method Preferences | Use the SEARCH finder without an LDG filter and show resolved user-facing values. |
| PPMP-E02 | Show the preference for a named LDG | Resolve exactly one LDG, then use the SEARCH finder for that LDG. |
| PPMP-E03 | Show complete preference details as a hierarchy | Resolve only missing display values, reuse cached results, and render the hierarchy template. |
| PPMP-E04 | Show LDGs eligible for preference creation | Use the documented finder with Intent CREATE. |
| PPMP-E05 | Create using LDG and OPM names when no preference exists | Resolve names, validate LDG context, SEARCH for the LDG, set operation to CREATE, then require the mutation gate. |
| PPMP-E06 | Create using IDs | Validate supplied IDs and codes, check for duplicates, then require the mutation gate. |
| PPMP-E07 | Mutation when a preference exists | SEARCH the preference, set operation to MERGE, and retain all returned attributes before applying user overrides. |
| PPMP-E08 | Update Maximum Personal Payment Methods | Require a whole number and preserve the existing LDG association. |
| PPMP-E09 | Update Available Payment Methods using multiple names | Resolve every OPM in the LDG, preserve order, and reject the entire request if any value fails. |
| PPMP-E10 | Generate DAT Noneditable Payment Methods using comma-separated IDs | Reject empty entries, deduplicate while preserving first occurrence, validate LDG context, retain order, and join IDs with a comma. |
| PPMP-E11 | Set Payment Amount Types to Amount | Store A and display Amount. |
| PPMP-E12 | Set Payment Amount Types to Percentage | Store P and display Percentage. |
| PPMP-E13 | Set Payment Amount Types to Both | Store B and display Both. |
| PPMP-E14 | Set Exclude from 100% Validation to Yes | Resolve and store Y; display the resolved Yes meaning. |
| PPMP-E15 | Set Exclude from 100% Validation to No | Resolve and store N; display the resolved No meaning. |
| PPMP-E16 | Delete using an LDG name | Resolve the LDG, confirm the preference exists, then require the mutation gate. |
| PPMP-E17 | Use an unresolved LDG name | Return the required no-match error. |
| PPMP-E18 | Use an ambiguous LDG name | Return the required multiple-matches error. |
| PPMP-E19 | Use an unresolved OPM | Return the required no-match error and stop. |
| PPMP-E20 | Use an OPM belonging to another LDG | Return the invalid-LDG-context error and stop. |
| PPMP-E21 | Use an invalid Yes or No value | Return the invalid-lookup error with Y and N as supported values. |
| PPMP-E22 | Use an invalid Payment Amount Type | Return the invalid-lookup error with A, P, and B as supported values. |
| PPMP-E23 | Use a decimal Maximum Personal Payment Methods value | Return the invalid-whole-number error. |
| PPMP-E24 | Display denormalized names and meanings | Do not make a redundant reference request. |
| PPMP-E25 | Display multiple OPM values | Preserve the original validated order in the user-facing output. |
| PPMP-E26 | Existing preference changes only Payment Amount Types | SEARCH the existing preference first; set operation to MERGE; send the updated PaymentAmountTypes with every other returned attribute, including optional attributes, preserved at its latest value. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PPMP.VALIDATE_INPUT | step | 1 | validate_input | valid->PPMP.RESOLVE_DEPENDENCIES;invalid->RETURN_ISSUES | none | stop | Always |

## Sources

- Oracle Fusion Cloud HCM, Configure Payment Method Preferences: https://docs.oracle.com/en/cloud/saas/human-resources/25a/faipb/configure-payment-method-preferences.html
- Developer-supplied Payment Method Preferences REST routes and finder contract.
