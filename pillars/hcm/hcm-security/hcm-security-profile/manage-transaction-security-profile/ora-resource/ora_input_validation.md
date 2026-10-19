# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| View All selection | View All | Stop and request the View All setting | Supply whether View All is enabled | Always | |
| Security profile operation | Read, Add, Update | Stop and request a supported operation | Supply Read, Add, or Update; deletion is unsupported | Always | |
| Scoped profile family | Family | Stop and request Family | Supply a Family value | View All is not enabled | |
| Category for subcategory | Category | Stop and request Category | Supply Category or remove Subcategory | View All is not enabled and Subcategory is supplied | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| View All is enabled | Family, Category, and Subcategory are ignored | Continue without validating scoped values | |
| View All is not enabled and structural requirements pass | The supplied scoped values require a supported-combination check | Validate against the task-local catalog | validate_supported_transaction_security_combination |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Ignore scoped values for View All | Ignore Family, Category, and Subcategory even when supplied | View All is enabled | |
| Restrict security profile operation | Accept only Read, Add, or Update; reject Delete and any other operation | Always | |
| Require Family for scoped profile | Reject the request when Family is absent | View All is not enabled | |
| Require Category for profile creation | Reject an Add request that selects a Family but no Category | Operation is Add and View All is not enabled | |
| Resolve Category value | Resolve the supplied Category value or code to one Category Code for the selected Family; reject no match or more than one match | View All is not enabled and Category is supplied | resolve_category_code_by_value |
| Subcategory requires Category | Reject the request when Subcategory is supplied without Category | View All is not enabled | |
| Exclude Subcategory requires selection | Reject Exclude Subcategory when no Subcategory is selected | Exclude Subcategory is requested | |
| Resolve Subcategory value | Resolve each supplied Subcategory value or code to one Subcategory Code for the resolved Family and Category Code; do not resolve ALL | View All is not enabled and Subcategory is supplied other than ALL | resolve_subcategory_code_by_value |
| Expand ALL subcategory | Accept ALL in any letter case only when Family and Category match at least one catalog row; resolve every supported subcategory for that prefix | View All is not enabled and Subcategory is ALL in any letter case | validate_supported_transaction_security_combination |
| Validate comma-separated subcategory codes | Split the supplied value on commas, trim whitespace, and require every non-ALL code to match an exact Family, Category, Subcategory catalog row; reject empty or duplicate codes | View All is not enabled and multiple Subcategory values are supplied | validate_supported_transaction_security_combination |
| Validate supported combination or prefix | Accept Family when it matches at least one catalog row; accept resolved Family and Category Code when they match at least one row; accept ALL in any letter case as the sole subcategory value for a valid Family-and-Category prefix; otherwise require every resolved comma-separated Subcategory Code to match an exact tuple | View All is not enabled after structural validation | validate_supported_transaction_security_combination |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TSP.VALIDATE_INPUT | decision | 1 | validate_input | valid->TSP.RESOLVE_CATEGORY_CODE;invalid->RETURN_ISSUES | none | stop | Always |
