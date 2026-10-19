# Manage Cost Factors Input Validation

Sources: User-provided Manage Cost Factors business-rule content from Confluence page 14988929751; user-authorized inspection of the Redwood Manage Cost Factors page on 2026-09-01; live Data Loader attribute-details workbook generated on 2026-09-04.

## Route Scope

The Redwood UI and the Data Loader have separate validation contracts. Do not
apply page defaults, Status behavior, inline-row controls, or page-access rules
to a Data Loader workbook unless the current live Data Loader template exposes
the corresponding attribute.

## Data Loader Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Cost factor identity | `CostFactorName` and `CostFactorCode` | Reject the archive before preview | Provide a nonblank name of no more than 80 characters and a nonblank code of no more than 30 characters | Creating a Cost Factor through Data Loader |  |
| Pricing-basis relationship | Either `PricingBasisCode` or the live-generated `PricingBasis` foreign user-key column; derive the code from `PricingBasis` through Foreign Key Set 1, and when both are supplied require the provided code to match | Reject a missing, unmapped, invalid, or mismatched relationship before preview | Preserve the foreign-key columns generated for `supplierNegotiationCostFactors`; validate through Data Loader Foreign Key Set 1 and do not infer values outside that mapping | Creating a Cost Factor through Data Loader |  |

## Data Loader Field Validation

| Attribute | Metadata evidence | Data Loader rule |
|---|---|---|
| `CostFactorCode` | Mandatory; maximum length 30 | Require a nonblank code and validate uniqueness with the live archive and Fusion response. |
| `CostFactorName` | Mandatory; maximum length 80 | Require a nonblank name. |
| `CostFactorDescription` | Optional; maximum length 240 | Permit an omitted description; validate the supplied value when present. |
| `PricingBasisCode` | Foreign key; maximum length 30; alternative `PricingBasis` | Require this field or `PricingBasis`; when `PricingBasis` is supplied, derive its code through Foreign Key Set 1, and when both are supplied require the provided code to match. |
| `PricingBasis` | Foreign user key; maximum length 80; alternative `PricingBasisCode` | Require this field or `PricingBasisCode`; derive the code through Foreign Key Set 1, and when both are supplied require the provided code to match. |
| Any additional attribute | Operation-specific live template | Do not require it solely because it is mandatory in generic metadata. The current generated workbook and live archive validation are authoritative. |

## Redwood UI Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Cost factor identity | Cost Factor and Code | Reject the change before Apply | Provide a nonblank Cost Factor and Code | Creating a cost factor | |

## Redwood UI Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The user does not have PON_MANAGE_SUPPLIER_NEGOTIATION_COST_FACTOR | Blocked | Obtain or confirm the required internal-user page-access privilege before managing cost factors | |

## Redwood UI Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Cost Factor is present, unique, and within length | Cost Factor is required, must contain no more than 80 characters, and must be unique. Treat uniqueness as case-insensitive; if it already exists at Apply, display FND_CMN_OBJECT_NAME_EXISTS and require a different value | Creating or editing a cost factor | |
| Code is present, unique, and within length | Code is required, must contain no more than 30 characters, and must be unique. Treat uniqueness as case-insensitive; if it already exists at Apply, display FND_CMN_OBJECT_NAME_EXISTS and require a different value | Creating a cost factor | |
| Description is optional and within length | Allow a free-text description of no more than 240 characters; the BR specifies no uniqueness requirement | Creating or editing a cost factor | |
| Pricing Basis is present and valid | Require Pricing Basis when applying a row. Accept Fixed amount, Percentage of line price, or Per unit | Creating or editing a cost factor | |
| Status is present and valid | Require Status when applying a row. Accept Inactive or Active | Creating or editing a cost factor | |
| Search text is optional | Accept one combined search text value for a cost factor, code, or description. Do not require separate Cost Factor, Description, Code, or Status search fields | Searching cost factors | |

## Data Loader Task Node

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COST_FACTOR.CLASSIFY_OPERATION | decision | 5 | evaluate_result | data_load->COST_FACTOR.VERIFY_DATA_LOADER_RESOURCE;read_lookup->COST_FACTOR.LOOKUP_COST_FACTOR;unsupported->RETURN_ISSUES | none | stop | A Manage Cost Factors request is received. |
| COST_FACTOR.VALIDATE_DATA_LOADER_INPUT | step | 20 | validate_input | valid->COST_FACTOR.REQUIRE_PREVIEW_READY;invalid->RETURN_ISSUES | COST_FACTOR.VERIFY_DATA_LOADER_RESOURCE | stop | A Cost Factor source workbook is ready for Data Loader preview |
