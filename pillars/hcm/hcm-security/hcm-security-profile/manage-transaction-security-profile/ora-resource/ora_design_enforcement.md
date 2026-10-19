# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Select transaction scope | Select the appropriate product Family and Category for the transactions users may manage |
| 2 | Refine scope | Optionally select subcategories; selected subcategories include only those transactions unless Exclude Subcategory is selected |
| 3 | Complete access configuration | Assign the profile to data roles, assign roles to users, and enable transaction security before claiming that restrictions are effective |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Creating a scoped profile | Error | resolve_category_code_by_value | Family is selected without a Category | Select the category of transactions users should manage | Yes |
| Selecting a subcategory | Error | resolve_subcategory_code_by_value | The selected subcategory is not resolved for the selected Family and Category | Select a valid subcategory, or select all supported subcategories when appropriate | Yes |
| Exclude Subcategory is selected | Error | none | No subcategory is selected | Select the subcategory that users must not manage | Yes |
| Reporting restricted Transaction Console access | Error | TBD | Profile assignment, data-role assignment, user assignment, or transaction-security enablement is unverified | Complete and verify every documented access-configuration step | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_category_code_by_value | A Category value or code is supplied | Category Code | ora_reference_lookups.md |
| resolve_subcategory_code_by_value | A Subcategory value or code is supplied | Subcategory Codes | ora_reference_lookups.md |
