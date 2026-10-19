# Manage Cost Factors Error Handling

Sources: User-provided Manage Cost Factors business-rule content from Confluence page 14988929751; user-authorized inspection of the Redwood Manage Cost Factors page on 2026-09-01; confirmed Data Loader business object `supplierNegotiationCostFactors`; live Data Loader attribute-details workbook generated on 2026-09-04.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Cost Factor or Code duplicates an existing value at Apply | Display FND_CMN_OBJECT_NAME_EXISTS and require a unique value. Treat the uniqueness check as case-insensitive. |
| Cost Factor or Code is blank at Apply | Do not commit the inline-row change; require the missing value. |
| Pricing Basis or Status is blank or invalid at Apply | Do not commit the inline-row change; require a valid value. |
| Attribute validation fails during Apply | Do not commit the inline-row change until the relevant attribute and component rules pass. |
| The required internal-user page-access privilege is unavailable | Block the task and request PON_MANAGE_SUPPLIER_NEGOTIATION_COST_FACTOR access. |
| A Data Loader Cost Factor create is requested | Resolve `supplierNegotiationCostFactors` and the pricing-basis foreign-key columns through `core.data-loader`, then validate the immutable workbook archive before preview. |
| A direct REST write or another unsupported integration route is requested | Do not construct or submit it; route the request through `core.data-loader` for `supplierNegotiationCostFactors`. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation failure | A required, overlength, duplicate, or invalid field is detected | Correct the field and apply the inline row again. |
| Authorization blocker | The required page-access privilege is absent or unconfirmed | Obtain or confirm the required access before proceeding. |
| Data Loader contract blocker | Live metadata cannot resolve `supplierNegotiationCostFactors` or the pricing-basis foreign-key relationship, the prepared archive fails validation, or the request attempts to bypass `core.data-loader` | Correct the object, source, or route and create a new immutable approval preview. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Duplicate identity | The affected Cost Factor or Code and the FND_CMN_OBJECT_NAME_EXISTS outcome without exposing unrelated records |
| Validation failure | The field or component that must be corrected before the inline row can be applied |
| Authorization blocker | The required privilege name and the fact that current-user access is unconfirmed or unavailable |
| Data Loader contract blocker | The unresolved business object or foreign-key relationship, invalid archive, unsupported direct-write route, or missing approval for the immutable archive |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A request bypasses `core.data-loader` or live metadata cannot resolve `supplierNegotiationCostFactors` and its pricing-basis foreign-key relationship | Do not construct or submit a live integration request. |
| A duplicate, missing, overlength, or invalid field is detected | Do not apply the Cost Factors inline row. |
| Required page access is unavailable | Do not attempt to manage cost factors with another user's access or bypass the privilege check. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | What Should Happen |
|---|---|---|---|---|---|---|---|---|
| COST_FACTOR.REQUIRE_PREVIEW_READY | decision | 30 | execution_gate | ready->COST_FACTOR.RETURN_PREVIEW_READY;blocked->RETURN_ISSUES | COST_FACTOR.VALIDATE_DATA_LOADER_INPUT | stop | A Data Loader Cost Factor archive has passed source validation and is about to enter preview | Continue only when `supplierNegotiationCostFactors` and its pricing-basis foreign-key metadata were resolved by live metadata and the final archive is immutable and valid. Do not require upload approval at this stage. |
| COST_FACTOR.RETURN_PREVIEW_READY | terminal | 40 | terminal | none | COST_FACTOR.REQUIRE_PREVIEW_READY | stop | The immutable archive is ready for preview | Return the validated archive to the Task Hook preview lifecycle. Require the separate approval only after preview creation and immediately before `core.data-loader` submission. |
| COST_FACTOR.RETURN_LOOKUP_RESULT | terminal | 45 | terminal | none | COST_FACTOR.LOOKUP_COST_FACTOR | stop | A Cost Factor lookup returned exactly one Cost Factor. | Return the documented Cost Factor fields without exposing internal IDs. |
| RETURN_ISSUES | terminal | 60 | terminal | none | none | stop | A dependency, defaulting, validation, or execution-gate node reports a blocking outcome | Return the blocking issue and the required corrective action without attempting a live change. |
