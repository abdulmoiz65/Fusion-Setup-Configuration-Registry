# Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| validate_supported_transaction_security_combination | View All is not enabled after structural validation | Family, Category, Subcategory | If only Family is supplied, match at least one row by FAMILY. If Family and Category are supplied, match at least one row by FAMILY and CATEGORY_CODE. Split comma-separated Subcategory values, trim whitespace, and require each non-ALL value to match an exact FAMILY, CATEGORY_CODE, SUBCATEGORY_CODE row. If ALL in any letter case is the sole value, match at least one row by FAMILY and CATEGORY_CODE and return every supported SUBCATEGORY_CODE for that prefix. Reject ALL when mixed with another code, as well as empty or duplicate codes. | Validated Family, Category, Subcategory; validated Subcategory Codes; expanded Subcategory Codes for ALL | Reject the request when the supplied Family, Family and Category, ALL prefix, or any supplied subcategory code has no catalog match |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_category_code_by_value | View All is not enabled and Category is supplied | Family, Category value or code | /hcmRestApi/resources/11.13.18.05/transactionSecurityProfiles/action/fetchCategoriesByFamily | Returned category value and corresponding category code | For the supplied Family, accept one exact returned Category value or Category Code and map it to the corresponding Category Code | Category Code | Stop and request an unambiguous Category value or code |
| resolve_subcategory_code_by_value | View All is not enabled, resolved Category Code is available, and Subcategory is supplied other than ALL | Family, resolved Category Code, each comma-separated Subcategory value or code | /hcmRestApi/resources/11.13.18.05/transactionSecurityProfiles/action/fetchSubcategoriesByFamilyAndCategory | Returned subcategory value and corresponding subcategory code | For the resolved Family and Category Code, accept one exact returned Subcategory value or Subcategory Code for each supplied list item and map it to the corresponding Subcategory Code | Subcategory Codes | Stop and identify each unmatched or ambiguous Subcategory value or code |

## Supported Combination Catalog

| FAMILY | CATEGORY_CODE | SUBCATEGORY_CODE |
|---|---|---|
| HCM | PER | ADDPERS |
| HCM | WLF | ASSIGNMENT |
| HCM | WLF | CATALOG |
| SCM | CJM | CUST_PROGRAM |
| HCM | CEL | RR |
| FIN | AP | Financing Program Offer |
| HCM | HRR | HRA |
| SCM | CJM | SPECIAL_PRICE_AGREEMENT |
| HCM | CMP | SAL |
| FIN | IBY | External Bank Account Approval |
| FIN | AGIS | Intercompany Approval |
| PRC | POR |  |
| HCM | CMP | IC |
| HCM | CMP | WFC |
| HCM | ANC | DON |
| SCM | CJM | CUST_MANUAL_ADJUST |
| FIN | EXM | Expense Approval |
| FIN | AP | Account Coding |
| HCM | PER | AOR |
| HCM | PER | EMPL |
| FIN | AP | Holds Resolution |
| HCM | CHK |  |
| SCM | RCV | RcvReceipts |
| HCM | HRR | HRT |
| FIN | FA | Asset Retirement Approval |
| HCM | PER | HMO |
| AISTUDIO |  |  |
| HCM | HRR | HRG |
| HCM | PER | IRC |
| HCM | PER | PERS |
| FIN | AR | Credit Memo Approval |
| PRC | PON |  |
| SCM | CJM | CUST_CLAIM |
| HCM | TestCategory | TestSubcategory |
| HCM | HWM | OTL |
| HCM | ANC | ABS |
| PRJ | PJB |  |
| HCM | PER | WFS |
| FIN | AP | Invoice Approval |
| PRJ | PJC |  |
| HCM | HRR | HRR |
| FIN | XLA | Subledger Accounting Entry Approval |
| FIN | FA | Asset Adjustment Approval |
| HCM | IRC | REQS |
| HCM | PER | DORS |
| HCM | PER | HCM_APPROVAL_DELEGATION |
| HCM | PER | DOR |
| CRM |  |  |
| HCM |  |  |
| HCM | IRC | OFRS |
| FIN | FA | Asset Addition Approval |
| FIN | AP | Bank Account Transfer Approval |
| FIN | GL | Journal Approval |
| SCM | INV |  |
| FIN | XLA | Subledger Entry Approval |
| PRJ | PJO |  |
| HCM | IRC | OROPM |
| PRC | PO |  |
| PRJ | PJF |  |
| HCM | HWM | HTS |
| SCM | RCV | SelfScvReceipts |
| HCM | ANC | DIS |
| PRJ | PJE | Project Change Request Approval |
| FIN | FA | Asset Mass Transaction |
| FIN | FLA | Lease Approval |
| FIN | IBY | Payment Approval |
| SCM |  |  |
| HCM | HRR | HRD |
| AI |  |  |
| HCM | HWM | ABS |
| HCM | HHR | HhrVolunteering |
| FIN | FA | Asset Transfer Approval |
| FIN | AP | Dynamic Discount Campaign Offer |
| HCM | PER | SCHD |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Category value is supplied | Resolve it to Category Code using fetchCategoriesByFamily before catalog validation |
| Subcategory value is supplied | Resolve each value to Subcategory Code using fetchSubcategoriesByFamilyAndCategory after Category Code resolution and before catalog validation |
| Supported combination catalog is available | Validate the supplied Family, resolved Family and Category Code, or exact tuple against the task-local catalog |
| Supported family or family-category prefix has at least one match | Continue with the validated supplied values; do not fill omitted values |
| Subcategory is ALL in any letter case and the family-category prefix has at least one match | Continue and expand to every supported subcategory code for the matching prefix |
| Comma-separated subcategory codes are supplied | Split and trim each code; continue only when every non-ALL code exactly matches the selected Family and Category |
| ALL is mixed with another subcategory code, or the list contains an empty or duplicate code | Return a blocking validation issue; do not expand or select values |
| Every supplied subcategory code has an exact match | Continue with the validated combination list |
| Supplied family, family-category prefix, ALL prefix, or any subcategory code has no match | Return a blocking validation issue; do not select a value automatically |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TSP.RESOLVE_CATEGORY_CODE | decision | 2 | reference_lookup | resolved->TSP.RESOLVE_SUBCATEGORY_CODE;not-required->TSP.DONE_FAMILY_ONLY;no-match->RETURN_ISSUES;ambiguous->RETURN_ISSUES | TSP.VALIDATE_INPUT | stop | View All is not enabled after input validation |
| TSP.RESOLVE_SUBCATEGORY_CODE | decision | 3 | reference_lookup | resolved-or-not-required->TSP.DONE_SCOPED;no-match->RETURN_ISSUES;ambiguous->RETURN_ISSUES | TSP.RESOLVE_CATEGORY_CODE | stop | View All is not enabled after Category Code resolution |
