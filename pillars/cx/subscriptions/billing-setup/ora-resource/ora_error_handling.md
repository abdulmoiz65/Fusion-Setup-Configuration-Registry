# Manage Price Adjustments Error Handling

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | Category cannot be resolved, is ineligible, or has an ambiguous identity | Show the failed criterion and stop before preview or write |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | Specific-date rules are violated | Show the date, charge, accounting, or billing-design blocker and stop |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | A REST data-loader request is rejected or its outcome is uncertain | Preserve redacted diagnostics, reconcile with a read-only lookup, and do not retry automatically |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | Lookup-code Data Loader process reports Warning, Error, or Failed | Preserve the terminal-process diagnostics and run the exact lookup-code resolver. If one active record matches the approved code, meaning, sequence, and date data, classify the outcome as reconciled, do not retry the lookup upload, and continue with the priceAdjustmentCategories Data Loader stage. Otherwise stop before category creation |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | Category Data Loader process reports Warning, Error, or Failed | Preserve the terminal-process diagnostics and run the exact category resolver. If one record matches the approved category values, classify the outcome as reconciled and show every returned category attribute; otherwise stop and disclose the mismatch |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | A lookup-code or category Data Loader process is intermediate or times out | Poll status every 30 seconds for no more than 20 minutes. An intermediate process cannot start its dependent stage or be reported as complete. A timeout remains blocked until an exact record can be reconciled; do not submit a duplicate upload |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | Lookup code or category sequence collides, or a requested between-placement has intervening records | Present the complete affected inventory, collision, and sequence information and request customer confirmation; do not derive or submit a category sequence |
| CUSTOM_MANAGE_PRICE_ADJUSTMENT_VARIABLES | Manage Price Adjustment Variables | Variable identity is ambiguous, a required value is missing, or documented field limits are exceeded | Show the affected variable or value field and stop before preview or write |
| CUSTOM_MANAGE_PRICE_ADJUSTMENT_VARIABLES | Manage Price Adjustment Variables | A deletion is requested for an existing variable | Refuse the deletion because the documented behavior permits update but not deletion |
| CUSTOM_MANAGE_PRICE_ADJUSTMENT_VARIABLES | Manage Price Adjustment Variables | A REST data-loader request is rejected or its outcome is uncertain | Poll the Data Loader request every 30 seconds through a terminal state. Report data-set status and total, loaded, and failed counts. For a Warning or Error, report the affected object or row, stage, actionable message, and corrective action; reconcile through the read-only variable lookup and do not retry automatically |
| CUSTOM_MANAGE_MILESTONE_TEMPLATES_FOR_BILLING_AND_REVENUE_RECOGNITION | Manage Milestone Templates for Billing and Revenue Recognition | The milestone-name or milestone-source lookup type, code, or meaning cannot be resolved | Report the unresolved prerequisite and stop before Data Loader artifact preparation. Do not infer a lookup type or code. |
| CUSTOM_MANAGE_MILESTONE_TEMPLATES_FOR_BILLING_AND_REVENUE_RECOGNITION | Manage Milestone Templates for Billing and Revenue Recognition | Product eligibility or milestone percentage is missing or incompatible | Report the documented eligibility condition or missing milestone percentage and stop before preview. |
| CUSTOM_MANAGE_MILESTONE_TEMPLATES_FOR_BILLING_AND_REVENUE_RECOGNITION | Manage Milestone Templates for Billing and Revenue Recognition | A milestoneTemplates Data Loader request is rejected or its result is uncertain | Preserve redacted diagnostics, obtain status only when requested, and do not retry the import automatically. |
| CUSTOM_MANAGE_MILESTONE_TEMPLATES_FOR_BILLING_AND_REVENUE_RECOGNITION | Manage Milestone Templates for Billing and Revenue Recognition | The read-only milestone template collection request is unauthorized or fails | Report the authorization or transport failure and stop. Do not substitute a Data Loader import or infer environment data. |
| CUSTOM_MANAGE_MILESTONE_TEMPLATES_FOR_BILLING_AND_REVENUE_RECOGNITION | Manage Milestone Templates for Billing and Revenue Recognition | The milestone-template describe request lacks a Name, Source, or Event Type choice-list mapping | Report the unresolved code and stop. Do not infer a display meaning. |

## Disclosure Rules

| Task Code | Task Name | Gate | What Must Be Shown |
|---|---|---|---|
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | Before any mutation through Data Loader | Exact category identity, resolved configuration flags, intended business effect, and the immutable preview requiring approval |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | Before lookup-code creation and before category creation | One combined business confirmation for the lookup and category values; header-only standardLookups parent and lookupCodes child-data source structure; retrieved Fusion values; Oracle-documented defaults and meanings; lookup-code process status and exact-code reconciliation; full category and Price Element sequence inventory; the immutable archive approval required by the Data Loader workflow |
| CUSTOM_MANAGE_PRICE_ADJUSTMENT_VARIABLES | Manage Price Adjustment Variables | Before any mutation through Data Loader | Exact variable identity, resolved existing state, intended value changes, and the immutable preview requiring approval |
| CUSTOM_MANAGE_MILESTONE_TEMPLATES_FOR_BILLING_AND_REVENUE_RECOGNITION | Manage Milestone Templates for Billing and Revenue Recognition | Before any mutation through Data Loader | Exact milestone template identity, resolved milestone-name and milestone-source values, product eligibility, milestone percentages, and the immutable preview requiring approval. |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | Category eligibility, ordering, or approval is unresolved | Do not submit or replay a create, update, or import operation |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | Mandatory values, default-value confirmation, lookup-code verification, collision decision, or sequence placement is unresolved | Do not create or update a lookup code or Price Adjustment Category |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | A direct REST POST or PATCH is proposed for a lookup code or category | Do not invoke the direct REST mutation; route the create or update through Data Loader |
| CUSTOM_MANAGE_PRICE_ADJUSTMENT_VARIABLES | Manage Price Adjustment Variables | Variable identity, date-effective value contract, or approval is unresolved | Do not submit or replay a create, update, or import operation |
| CUSTOM_MANAGE_MILESTONE_TEMPLATES_FOR_BILLING_AND_REVENUE_RECOGNITION | Manage Milestone Templates for Billing and Revenue Recognition | Lookup prerequisites, product eligibility, milestone percentage, live Data Loader metadata, or approval is unresolved | Do not prepare, submit, retry, or replay a milestoneTemplates import. |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | PA.DONE | terminal | 90 | terminal | none | PA.ENFORCE | stop | All validation and design checks pass |
| CUSTOM_MANAGE_PRICE_ADJUSTMENTS | Manage Price Adjustments | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any validation, lookup, or design check produces issues |
| CUSTOM_MANAGE_PRICE_ADJUSTMENT_VARIABLES | Manage Price Adjustment Variables | PAV.DONE | terminal | 90 | terminal | none | PAV.ENFORCE | stop | All validation and design checks pass |
| CUSTOM_MANAGE_PRICE_ADJUSTMENT_VARIABLES | Manage Price Adjustment Variables | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any validation, lookup, or design check produces issues |
| CUSTOM_MANAGE_MILESTONE_TEMPLATES_FOR_BILLING_AND_REVENUE_RECOGNITION | Manage Milestone Templates for Billing and Revenue Recognition | MT.DONE | terminal | 90 | terminal | none | MT.ENFORCE | stop | All milestone template validation and design checks pass |
| CUSTOM_MANAGE_MILESTONE_TEMPLATES_FOR_BILLING_AND_REVENUE_RECOGNITION | Manage Milestone Templates for Billing and Revenue Recognition | MT.LIST_DONE | terminal | 91 | terminal | none | MT.LIST_TEMPLATES | stop | The read-only milestone template list is returned |
| CUSTOM_MANAGE_MILESTONE_TEMPLATES_FOR_BILLING_AND_REVENUE_RECOGNITION | Manage Milestone Templates for Billing and Revenue Recognition | MT.DESCRIBE_DONE | terminal | 92 | terminal | none | MT.DESCRIBE_LOOKUPS | stop | The milestone Name, Source, and Event Type lookup meanings are resolved |
| CUSTOM_MANAGE_MILESTONE_TEMPLATES_FOR_BILLING_AND_REVENUE_RECOGNITION | Manage Milestone Templates for Billing and Revenue Recognition | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any milestone template validation, lookup, dependency, or design check produces issues |
