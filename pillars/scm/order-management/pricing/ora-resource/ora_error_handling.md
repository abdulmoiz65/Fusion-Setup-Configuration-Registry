# Manage Price Elements Error Handling

Source: Oracle Fusion Cloud SCM, Manage Pricing Elements (26B).

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| ORA_QP_MANAGE_PRICE_ELEMENTS | Manage Price Elements | Element Code duplicates an existing element | Stop and choose a unique code or use the existing suitable predefined element |
| ORA_QP_MANAGE_PRICE_ELEMENTS | Manage Price Elements | Active is cleared for a referenced element | Stop; retain Active until the referencing pricing entity no longer uses the element |
| ORA_QP_MANAGE_PRICE_ELEMENTS | Manage Price Elements | Used in Pricing Guidelines is enabled for Cost or Accrual | Stop; leave the option disabled |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| ORA_QP_MANAGE_PRICE_ELEMENTS | Manage Price Elements | Validation or design enforcement failed | Do not submit, retry, or mutate setup data |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICE_ELEMENTS | Manage Price Elements | QP.PE.READY | terminal | 3 | terminal | none | QP.PE.DESIGN | stop | Validation and design enforcement passed |
| ORA_QP_MANAGE_PRICE_ELEMENTS | Manage Price Elements | QP.PE.ISSUES | step | 4 | error_handler | resolved->RETURN_ISSUES | none | stop | Validation or design enforcement failed |
| ORA_QP_MANAGE_PRICE_ELEMENTS | Manage Price Elements | RETURN_ISSUES | terminal | 5 | terminal | none | QP.PE.ISSUES | stop | An issue was handled |

# Manage Pricing Bases Error Handling

Source: Oracle Fusion Cloud SCM, Manage Pricing Bases (25D); REST API for Oracle Fusion Cloud SCM, Get all pricing bases (26B).

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | Referenced price element is absent, inactive, or ambiguous | Stop and resolve the price element through Manage Price Elements before preparing the pricing basis. |
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | Existing pricing basis has the requested name | Stop and review the existing basis; use an approved update path instead of creating a duplicate. |
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | Usage is Tier Basis but required charge criteria are absent | Stop and provide the applicable charge criteria before import. |
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | A pricing-basis or price-element lookup fails | Stop before retrying, previewing, or importing; retain only sanitized diagnostics. |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | Validation, dependency, lookup, or design enforcement failed | Do not submit, retry, or mutate setup data. |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | QP.PB.READY | terminal | 7 | terminal | none | QP.PB.DESIGN | stop | Validation, dependency, lookup, and design enforcement passed |
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | QP.PB.ISSUES | step | 8 | error_handler | resolved->RETURN_ISSUES | none | stop | Validation, dependency, lookup, or design enforcement failed |
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | RETURN_ISSUES | terminal | 9 | terminal | none | QP.PB.ISSUES | stop | An issue was handled |

# Manage Pricing Parameters Error Handling

Source: Manage Pricing Parameters task metadata.

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | A read request does not use the parameterized core REST-client route, or a create/update request does not use Data Loader | Stop; explain that reads use `core.fusion-api.rest-api-client` at `/fscmRestApi/resources/11.13.18.05/qpParameters/{pricingParametersUniqID}/child/qpParameterValues` and require the parent identifier; create and update use `core.data-loader`. |
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | The prepared Data Loader source fails validation | Stop before preview or import; correct the reported Data Loader validation issues and revalidate. |
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | Registered business object, live-schema validation, immutable artifact preview, or current approval is missing | Stop before import; generate the missing evidence and approval. |

## Error Classifications

| Task Code | Task Name | Result Category | When Used | Next Action |
|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | catalog_or_metadata_mismatch | The read request lacks a parent Pricing Parameter identifier or cannot use the declared parameterized REST-client path | Resolve `pricingParametersUniqID` and use `core.fusion-api.rest-api-client`; use the registered Data Loader workflow for create/update. |
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | input_validation | Required task metadata or setup-data validation is missing or fails | Correct the missing or invalid input before routing. |
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | input_validation | A create or update request lacks a registered business object, live-schema-validated source, immutable artifact preview, or current approval | Correct the missing requirement and regenerate the Data Loader preview. |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | Validation or route selection failed | Do not preview, upload, initiate an FSM package, or import setup data. |
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | Data Loader validation, artifact preview, or import approval failed | Do not submit, retry, or substitute a Data Loader artifact. |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | QP.PP.REST_GET | decision | 2 | execution_gate | retrieved->QP.PP.REST_GET_READY;failed->QP.PP.ISSUES | QP.PP.VALIDATE | stop | A read request retrieves Pricing Parameter Values through `core.fusion-api.rest-api-client` at `/fscmRestApi/resources/11.13.18.05/qpParameters/{pricingParametersUniqID}/child/qpParameterValues` |
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | QP.PP.REST_GET_READY | terminal | 3 | terminal | none | QP.PP.REST_GET | stop | The requested Pricing Parameter Value list is available for read output |
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | QP.PP.DATA_LOADER_VALIDATION | decision | 4 | execution_gate | validated->QP.PP.DATA_LOADER_IMPORT_READY;failed->QP.PP.ISSUES | QP.PP.VALIDATE | stop | A create or update has a live-schema-validated Data Loader source for `qpParameterValues` |
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | QP.PP.DATA_LOADER_IMPORT_READY | terminal | 5 | terminal | none | QP.PP.DATA_LOADER_VALIDATION | stop | The exact Data Loader artifact is previewed and awaiting explicit approval for `core.data-loader` |
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | QP.PP.ISSUES | step | 6 | error_handler | resolved->RETURN_ISSUES | none | stop | Validation, Data Loader preparation, or import readiness failed |
| ORA_QP_MANAGE_PRICING_PARAMETERS | Manage Pricing Parameters | RETURN_ISSUES | terminal | 7 | terminal | none | QP.PP.ISSUES | stop | An issue was handled |

# Manage Pricing Charge Definitions Error Handling

Source: Oracle Fusion Cloud SCM, Manage Pricing Charge Definitions (25C); Add Your Own Lookup to Charge Types (25D).

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | A suitable predefined definition exists | Stop creation and use or update the existing suitable definition through an approved path. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | The existing-definition review has no unique closest match | Do not infer a selection; ask the user to choose an existing definition or confirm creation of a new definition. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | An exact Price Type, Charge Type, and Charge Subtype combination exists | Stop before preview or import; disclose the conflicting definition code and name and require a different combination. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Required fields, a supplied code format, or recurring periodicity are invalid | Stop before preview or import; correct the charge-definition data and revalidate. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Charge Type or Charge Subtype is omitted | Retrieve enabled price types, charge types, and charge subtypes plus current charge definitions. Generate an exact Price Type, Charge Type, and Charge Subtype combination not present in the current definitions, then require user approval before source preparation. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | A supplied Charge Type or Charge Subtype is absent or disabled | Route creation or enablement of the exact supplied code through Manage Pricing Lookups, obtain lookup-write approval, and verify the code is enabled before rechecking the charge-definition combination. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | The Site value of `RCS_DEFAULT_UOM_CLASS_CODE_FOR_SVC_DURATION` is unavailable or blank and the recurring Price Periodicity UOM Class is omitted | Do not substitute a value; require the user to provide the periodicity UOM class. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | The user-supplied recurring Price Periodicity UOM Class equals the Site value of `RCS_DEFAULT_UOM_CLASS_CODE_FOR_SVC_DURATION` | Preserve the supplied value and issue an informational best-practice recommendation that it is the configured default. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Usage UOM Class has multiple eligible values | Do not substitute a value; require the user to provide the Usage UOM Class. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Custom charge type or subtype lookup verification is incomplete | Stop before preview or import; do not substitute an unverified lookup value. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Live Data Loader schema validation, immutable loader-source preview, or current approval is missing | Stop before import; generate the missing evidence and approval. |

## Error Classifications

| Task Code | Task Name | Result Category | When Used | Next Action |
|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | input_validation | Required definition attributes or code rules fail | Correct the input and revalidate. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | input_validation | A create request matches an existing Price Type, Charge Type, and Charge Subtype combination | Select a different combination and rerun the read-only conflict lookup before preview. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | input_validation | The business purpose is insufficient to recommend an omitted Charge Type or Charge Subtype, or the user does not confirm the proposal | Obtain a business-purpose description or explicit selection; do not prepare a source. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | catalog_or_metadata_mismatch | Custom lookup verification lacks a documented read-only contract | Complete the lookup prerequisite and author the authoritative resolver contract. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | approval_blocker | Current immutable ZIP preview or explicit approval is missing | Prepare the validated archive preview and obtain approval. |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Validation, dependency, lookup, or design enforcement failed | Do not preview, upload, submit, retry, or mutate setup data. |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | Data Loader validation, source preview, or approval failed | Do not submit or substitute a loader source. |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | QP.PCD.DATA_LOADER_VALIDATION | decision | 5 | execution_gate | validated->QP.PCD.DATA_LOADER_IMPORT_READY;failed->QP.PCD.ISSUES | QP.PCD.DESIGN | stop | A create or update has a live-schema-validated Data Loader source for pricingChargeDefinitions |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | QP.PCD.DATA_LOADER_IMPORT_READY | terminal | 6 | terminal | none | QP.PCD.DATA_LOADER_VALIDATION | stop | The exact Data Loader source is validated, previewed, and awaiting explicit approval for core.data-loader |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | QP.PCD.ISSUES | step | 7 | error_handler | resolved->QP.PCD.RETURN_ISSUES | none | stop | Validation, dependency, lookup, design enforcement, export, or import readiness failed |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | QP.PCD.RETURN_ISSUES | terminal | 8 | terminal | none | QP.PCD.ISSUES | stop | An issue was handled |


# Manage Rounding Rules Error Handling

Source: repository error-handling and core.data-loader approval contracts.

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | Invalid input or unsupported scope | Report the failed field or unsupported operation; stop before preview |
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | Lookup failure, duplicate or unresolved reuse review | Retain sanitized evidence and resolve the issue before preparing approval |
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | Loader or task validation fails | Stop; correct the source or rules, rebuild the immutable archive when changed, and rerun validation |
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | Upload or initiation outcome is uncertain | Preserve partial success and external identifiers through core.data-loader; do not retry without its allowed recovery and explicit approval |

## Disclosure Rules

| Task Code | Task Name | Gate | What Must Be Shown |
|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | QP.RR.READY | Validation readiness only; creation still requires the core.data-loader approval and submission workflow. No task node submits data. |
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | QP.RR.RETURN_ISSUES | Failure class, failed node, sanitized evidence and one corrective next action; no approval request while blocked |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | QP.RR.READY | terminal | 4 | terminal | none | QP.RR.DESIGN | stop | All validation and design checks passed |
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | QP.RR.ISSUES | step | 5 | error_handler | reported->QP.RR.RETURN_ISSUES | none | stop | A validation, lookup or design check failed |
| ORA_QP_MANAGE_ROUNDING_RULES | Manage Rounding Rules | QP.RR.RETURN_ISSUES | terminal | 6 | terminal | none | QP.RR.ISSUES | stop | Issues reported |

# Manage Rounding Rule Assignments Error Handling

Sources: [Create and manage pricing rounding rule assignments (26D)](https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/order26d/26D-order-mgmt-wn-f50338.htm) and repository execution-safety policy.

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | Currency or Rounding Rule is missing | Stop and request the missing selection. |
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | The selected rule is not eligible for assignment | Stop; correct the rule in Manage Rounding Rules before creating or updating the assignment. |
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | Rule or currency resolver fails, is ambiguous, or returns an ineligible value | Stop automated validation; do not substitute a guessed endpoint, identifier, rule, or currency. |
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | A live creation, update, or deletion outcome is uncertain | Preserve sanitized evidence and do not retry without the selected execution workflow and current approval. |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | Validation, lookup, dependency, or design enforcement failed | Do not preview, submit, retry, or mutate setup data. |
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | A declared read-only lookup does not reach a terminal exact eligible result | Do not claim that the user-provided Currency or Rounding Rule was verified, and do not prepare or submit the assignment. |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | QP.RRA.READY | terminal | 5 | terminal | none | QP.RRA.DESIGN | stop | All validation, dependency, and design checks passed |
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | QP.RRA.ISSUES | step | 6 | error_handler | reported->QP.RRA.RETURN_ISSUES | none | stop | Validation, lookup, dependency, or design enforcement failed |
| ORA_QP_MANAGE_ROUNDING_RULE_ASSIGNMENTS | Manage Rounding Rule Assignments | QP.RRA.RETURN_ISSUES | terminal | 7 | terminal | none | QP.RRA.ISSUES | stop | Issues reported |

# Manage Customer Pricing Definitions Error Handling

Source: Oracle Fusion Cloud SCM, Business Objects for Oracle Fusion Cloud SCM, CustomerPricingDefinition (26C).

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | Name, assignment type, or pricing strategy is missing | When Name is omitted for an ORA_QP_ALL definition, apply the Customer Pricing Definition for Validation default. Otherwise stop before preview or import and obtain the missing value. |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | A create request finds exactly one existing ORA_QP_ALL definition | Prompt the user to use the resolved definition. If accepted, return it without creating, updating, or repurposing it; if declined, stop without mutation. |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | Global assignment uniqueness lookup finds multiple ORA_QP_ALL definitions, is ambiguous, incomplete, or fails | Stop before preview or import. Do not create, overwrite, or repurpose a global definition. |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | A Pricing Strategy child association finds zero global customer pricing definitions with AssignmentTypeCode ORA_QP_ALL | Prepare the separate validated global-definition create load with documented defaults. After the create succeeds, rerun association resolution; do not fabricate PricingStrategyId. |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | A Pricing Strategy child association finds multiple global definitions, a blank resolved PricingStrategyId, or a conflicting supplied ID | Stop before preview or import. Do not substitute or overwrite PricingStrategyId; correct the conflict, then rerun lookup and validation. |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | Data Loader source fails live-schema validation or lacks current approval | Stop before import; correct the source, revalidate it, and obtain approval for the exact immutable artifact. |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | Validation or Data Loader preparation failed | Do not preview, upload, initiate, retry, or mutate setup data. |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | CPD.PREPARE_GLOBAL_FOR_ASSOCIATION | terminal | 6 | terminal | none | CPD.RESOLVE_PARENT_PRICING_STRATEGY | stop | An association request found no global ORA_QP_ALL definition; prepare its separate validated create load, submit it with approval, then rerun association resolution |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | CPD.READY_CREATE | terminal | 7 | terminal | none | CPD.CHECK_GLOBAL_ASSIGNMENT | stop | Customer pricing definition inputs are valid, child PricingStrategyId values are derived when needed, defaults are applied, and global assignment uniqueness is confirmed for the separately approved Data Loader workflow |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | CPD.READY_REUSE | terminal | 8 | terminal | none | CPD.OFFER_REUSE_GLOBAL_DEFINITION | stop | The user accepted reuse of the exactly one resolved global customer pricing definition; return it without a create or update |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | CPD.ISSUES | step | 9 | error_handler | resolved->CPD.RETURN_ISSUES | none | stop | Validation, parent lookup, global uniqueness check, reuse decision, defaulting, or Data Loader preparation failed |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | CPD.RETURN_ISSUES | terminal | 10 | terminal | none | CPD.ISSUES | stop | An issue was handled |

# Manage Pricing Messages Error Handling

Source: the developer-provided parent Pricing SKILL.md workflow and corresponding flat task metadata. Fusion records and operation support remain live authorities; the final immutable source and preflight evidence are supplied by core.data-loader. These rules authorize no Fusion write.

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | Input, identity, lookup, operation mapping, template or task validation fails | Stop before preview or execution; classify input_validation or catalog_or_metadata_mismatch and return the missing fact or safe correction |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | Read-only auth, transport or Fusion API failure | Use the core client failure contract; one cached-token refresh only; retain redacted status, stage, failure class and next action; do not claim an incomplete inventory is complete |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | A child load succeeds, fails or is uncertain | Successful initiation is terminal for that user request. On a later status request require verified zero-failure completion and correct child state before separately preparing the parent stage; stop on partial or uncertain results without retry or compensation |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | A parent load is initiated | Return the exact core.data-loader initiation report and stop. Verify exact requested text and unchanged unrelated fields only on a later explicit status request |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | Any required rule failed, was skipped or is unavailable | Do not preview, upload, submit, use direct REST writes, invent an adapter, silently waive a safety rule or retry an uncertain load |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | Sensitive evidence | Never print or persist credentials, cache contents, authorization headers or customer-sensitive message text; persist only permitted redacted project evidence |

## Disclosure Rules

| Task Code | Task Name | Gate | What Must Be Shown |
|---|---|---|---|
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | QP.PM.READY | Task validation readiness only. Inventory completion is read-only; a message load still needs core.data-loader preview and approval of the exact artifact. A task node never submits data. |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | QP.PM.RETURN_ISSUES | Failure class, failed node, sanitized evidence and one corrective next action; no approval prompt while blocked |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | QP.PM.READY | terminal | 4 | terminal | none | QP.PM.DESIGN | stop | Applicable task validation passed; hand off to the selected core workflow only |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | QP.PM.ISSUES | step | 5 | error_handler | reported->QP.PM.RETURN_ISSUES | none | stop | A required task check failed |
| ORA_QP_MANAGE_PRICING_MESSAGES | Manage Pricing Messages | QP.PM.RETURN_ISSUES | terminal | 6 | terminal | none | QP.PM.ISSUES | stop | Return blocking issues without execution |
