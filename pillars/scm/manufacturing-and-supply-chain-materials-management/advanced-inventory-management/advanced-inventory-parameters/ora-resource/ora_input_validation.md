# Advanced Inventory Parameters Input Validation

## Local Validation Scope

First classify the source through `core.data-loader`. A ZIP with the exact member basename `ASM_SETUP_CSV_METADATA.xml` is a candidate FSM archive. The filename of a loose CSV, catalog support flags, or a caller-supplied route label alone does not establish this route. Use the FSM branch below for classified FSM archives; all parent-BO identity and effective-value rules in this file apply only to the REST-backed route. Reject explicit delete intent on either route.

## FSM Archive Validation

| Condition | Required handling |
| --- | --- |
| Source is classified as FSM | Use shared Data Loader package validation for Advanced Inventory Parameters. The observed CSV member is `ORA_INVENTORY_ADVANCED_INVENTORY_PARAMETER.csv`; a filename alone does not establish task compatibility. |
| FSM operation validation | Reject explicit delete requests or known delete settings. Delegate import-operation validation to the shared Data Loader workflow and honor its failures. Do not require an unverified task-specific import-operation marker or non-delete preflight certificate; an `EXPORT` process label alone is not grounds for rejection or proof of import behavior. |
| FSM columns require validation | Use the target environment's current native FSM export/metadata and the 78-attribute knowledge inventory in `SKILL.md`. Both 73-column pre-patch and 78-column patched exports have been observed. Do not enforce a fixed column count or populate missing columns. Preserve blanks, casing, flag values, category codes, and DFF columns. |
| A request uses a patch-dependent attribute | Include supplied values for the five optional fields when exposed by target-native FSM metadata; otherwise ignore/defer them without a patch blocker and report skipped requested values. Do not add absent columns or infer support from another environment. Shared validation still applies. |
| REST-only requirements are encountered | Do not require REST BO attributes, perform meaning resolution, inject the REST default, request `OrganizationId`, or require separate REST child-BO metadata. `OrganizationCode` is present in the observed FSM header; its operation-specific requiredness must be established from native metadata. |
| A field domain, conditional requirement, or DFF context is material but unverified | Obtain authoritative FSM metadata or validation evidence. Do not borrow REST rules or guess accepted values. If the applicable validation cannot be completed, block the load and report the missing evidence. |

After FSM validation, continue through `ADV_INV_PARAMS.CHECK_FSM_READINESS`. Do not enter the REST lookup, effective-value, or defaulting nodes.

## REST-backed Input Validation

Data Loader and Fusion own required-field, data-type, domain, and cross-field validation for the registered parent `advancedInventoryParameters` business object and its template child sections. This task-local scope establishes the supplied parent business identity before Data Loader handoff. The registered parent BO resolves its internal `OrganizationId` from the supplied `OrganizationCode`; callers do not supply that internal identifier.

| Input condition | Local handling | If blocked |
| --- | --- | --- |
| A parent `advancedInventoryParameters` row is supplied | Require exactly one nonblank `OrganizationCode` to identify the inventory organization. | Stop and request the target organization code. |
| An `InvAdvancedInvParamsDFF` child section is supplied | Include it through the parent template. The parent BO/Data Loader binding resolves the internal parent `OrganizationId`; do not require or compare it locally, and do not invoke a separate child BO. | Stop if the parent organization code is absent. |
| Create or update operation is not established | Establish the operation from the governed task context before applying operation-specific rules. Do not guess from an identifier or a failed read. | Stop and request the operation context. |
| Delete is requested for the parent or child, including a delete operation in source rows or artifacts | Reject the request before lookup, preview, or Data Loader handoff. Confirmation cannot override this restriction. | Return unsupported-operation issues. |
| Any other supplied field | Preserve it for the registered BO. Do not duplicate Data Loader or Fusion validation locally. | Data Loader/Fusion validates it. |

## Effective Values and Final Validation

Evaluate these rules after display-value resolution, independently for each organization. For create, use supplied and resolved values. For update, overlay all supplied and resolved changes together on verified current values; never check intermediate priority states. Omission preserves a current value; explicit null is an intentional supplied value and must not be replaced by a default. Use current values only as validation context, not as extra write fields.

Accept current-value evidence from an already verified Data Loader/BO read, a read-only result obtained through an approved existing lookup contract, or a user-provided current export/read response whose target environment and OrganizationCode can be established. Record its environment, organization, retrieval time, and source reference in normal validation context. Do not reuse evidence after a known intervening change, across environments, or across organizations. If evidence is stale or identity cannot be established, request a refreshed result containing only the fields needed below. This guidance does not introduce an endpoint, a local OrganizationId lookup, or a new artifact requirement.

On update, evaluate Cross-Dock conditional requirements only when its enable flag, category, demand days, or sort code/meaning changes. Evaluate the Put-away enabled/required-priority rule only when its enable flag or a priority changes. When a priority changes, obtain all remaining priority slots and check the final combined set, even if Put-away is disabled. When any of the five feature flags changes to a disabled value or is explicitly cleared, establish the resulting state of the other flags as needed for delete protection; a verified enabled flag proves the all-disabled condition is false. If the supplied changes enable a flag, they already rule out an all-disabled result. Explicit delete intent is always rejected. An unrelated update does not require Cross-Dock, Put-away, or feature-flag context. Unknown required context blocks only the affected validation; request the specific missing fields.

| Condition | Required handling |
| --- | --- |
| Effective Cross-Dock is enabled | Require nonblank `CrossDockItemCategoryName`, whole-number `CrossDockDemandDueDays` greater than or equal to zero, and a due-date-sort code. Only a create request that omits both sort code and meaning may defer the code to the approved default. |
| Effective Put-away Suggestions is enabled | Require at least one nonblank effective priority code after resolution. |
| Priority codes are supplied or resolved | Check all four effective priority slots, including unchanged slots on update. Reject duplicate nonblank codes and `ORA_RCV_KANBAN` or `ORA_RCV_DOCUMENT`. Run this check even when no display meanings were supplied and even when Put-away is disabled. |
| All five effective feature flags are disabled | Block handoff under the no-delete policy. The five fields are `LPNEnabledFlag`, `CrossDockEnabledFlag`, `PutAwaySuggestionsEnabledFlag`, `TaskManagementAllowedFlag`, and `OutboundLoadCreationAllowedFlag`. Missing or unknown flags are not evidence of disablement. |
| Flag representations are needed to evaluate a rule | Use the confirmed BO/Data Loader representation. Do not apply JavaScript truthiness to strings or guess meanings such as `Yeah`. If a supplied representation is unverified, request the canonical value. No friendly-value normalization is introduced here. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| ADV_INV_PARAMS.CLASSIFY_IMPORT_ROUTE | step | 5 | validate_input | rest->ADV_INV_PARAMS.VALIDATE_PARENT_IDENTITY;fsm->ADV_INV_PARAMS.VALIDATE_FSM_ARCHIVE;blocked->ADV_INV_PARAMS.RETURN_ISSUES | none | stop | Every request; use core.data-loader source classification and reject explicit delete intent before selecting the route. |
| ADV_INV_PARAMS.VALIDATE_FSM_ARCHIVE | step | 11 | validate_input | validated->ADV_INV_PARAMS.CHECK_FSM_READINESS;blocked->ADV_INV_PARAMS.RETURN_ISSUES | ADV_INV_PARAMS.CLASSIFY_IMPORT_ROUTE | stop | Classified FSM archive; verify task identity, reject explicit or known delete operations, and apply shared package validation. |
| ADV_INV_PARAMS.VALIDATE_PARENT_IDENTITY | step | 10 | validate_input | normalized->ADV_INV_PARAMS.CHECK_READINESS;blocked->ADV_INV_PARAMS.RETURN_ISSUES | ADV_INV_PARAMS.CLASSIFY_IMPORT_ROUTE | stop | REST-backed requests only; establish operation and organization identity and reject delete operations. |
| ADV_INV_PARAMS.VALIDATE_EFFECTIVE_VALUES | step | 32 | validate_input | validated->ADV_INV_PARAMS.APPLY_CROSSDOCK_DUE_DATE_SORT_DEFAULT;blocked->ADV_INV_PARAMS.RETURN_ISSUES | ADV_INV_PARAMS.RESOLVE_REFERENCE_LOOKUPS | stop | Every request after applicable lookup resolution, including code-only requests; evaluate effective values and conditional requirements. |
