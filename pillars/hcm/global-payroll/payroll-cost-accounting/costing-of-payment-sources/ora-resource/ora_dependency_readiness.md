# Costing of Payment Sources HDL Dependency Readiness

## Authority Boundary

For this task, the authoritative local source is the user-supplied approved
current-task HDL input or its immutable approved HDL archive. It supports only
presence and consistency checks for supplied identities, dates, and account
values; it never establishes Fusion state. The self-contained search contracts
in ora_reference_lookups.md provide live source/LDG search authority. The
organization-method resolver
additionally establishes that method's code/ID pair and automatically binds it
to the source using the joined parent name and unique effective LOV result;
user confirmation is not relationship evidence. Payment Source Identity in
ora_reference_lookups.md establishes the source-level BaseOrgPayMethodName
mapping for PaymentSourceCode. The current lookups do not retrieve that child
base code. The Full Flexfield resolvers
separately verify the exact LDG structure assignment, runtime segment metadata and
component values; user input supplies desired accounts, not validation evidence.
Apply the task validation scope in ora_design_enforcement.md rather than adding
prerequisites beyond the rules below. Zap uses declared live PM history/detail
evidence for allocation, physical accounts and aligned CostInfo; user input is
not authoritative for the existing DELETE target set. Update uses
resolve_payment_source_update_state for live intervals, accounts and flags;
prior chat, a previous Create payload or user confirmation cannot replace it.
End Date uses resolve_payment_source_end_date_state for the last aligned interval
and the complete unchanged-history/account/flag baseline.

Search-only requests return before the HDL dependency node. Missing accounts,
HDL codes, or an import archive must not block the declared search calls.
The four checkbox-to-CostInfoV3 mappings are packaged in
ora_input_validation.md and apply directly during input validation.

The following identity/account-setup order applies to Create/Update only.
Zap follows its separate history, detail, dependency and approval nodes; it does
not require runtime KFF or account-segment validation for identity-only deletes.
End Date follows its own state, preserved-flag and component validation,
freshness and single combined-archive approval nodes; it does not rewrite or revalidate accounts.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Payment-source setup and Update state | Resolve source/parent identity first. Update then resolves its complete history and account/CostInfo baseline before checking derived dates and the resulting account set; Create keeps its existing input checks. |
| 2 | Full Flexfield validation and source assembly | For account writes, resolve the LDG structure, runtime metadata and every supplied account's component values through the Full Flexfield resolvers. Assemble PM rows from validated_full_kff_accounts and the current template; a user's confirmation does not satisfy these lookups. |
| 3 | Archive validation and approval | Validate the immutable archive through core.data-loader and obtain approval bound to the exact environment and operation. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| payment_source_search | Payment-source candidate resolution | Conditional | Display-name or filter discovery requested before Create/Update | Lookup | Live PaymentSourcesSearchVO result from the current search pass | search_payment_sources | User-facing filters can find candidate rows before the user is asked for HDL-only values | Consume the selected search result; request one distinguishing filter only if identity remains ambiguous | selected_search_record |
| organization_payment_method_identity | Organization payment method code and selected-source association | Conditional | Any supported operation consumes parent identity, including Create, Update, End Date, full Zap and code-enriched Search; child-only recovery and status/approval resumes retain their declared boundaries | Lookup | Key-validated source join plus complete same-LDG/date organization-method LOV result | resolve_organization_payment_method_code | Resolve method identity and relationship automatically before consuming parent keys, including when keys were supplied | Consume validated relationship evidence without user confirmation. Missing or ambiguous evidence blocks; input assertions or approval cannot replace the resolver | resolved_org_payment_method;organization_payment_method_code;parent_binding_status;parent_binding_evidence |
| payment_source_identity | Payment source and organization payment method HDL identity | Yes | Every supported Create, Update or End Date request, after any requested search | Required | Approved current-task HDL input, including an available source-level base code under Payment Source Identity in ora_reference_lookups.md, plus the bound organization-method resolver result when discovery ran | | PM records require the source and parent identities separately; each code belongs to its own record | Consume the mapped source code when available and ask only for an absent business value or report the missing retrieval contract. Do not request reference attachments or ask again for resolved source or bound parent codes | payment_source_code;organization_payment_method_code |
| update_state | Existing PM allocation, aligned CostInfo and complete account state | Yes | Every effective-dated Update, including flags-only changes | Lookup | Complete identity-bound live PM history/detail and automatic parent binding | resolve_payment_source_update_state | Resolves the containing interval and unchanged values before applying the business delta; preserves earlier and later periods | Consume the live baseline, not user certification. Stop on ambiguity, old-value conflict or an unsupported same-start correction | update_baseline;update_selected_interval;update_end_date;update_existing_accounts;update_current_flags;update_comparison_facts |
| end_date_state | Last aligned period and preserved scope | Yes | End Date preparation, freshness and final verification | Lookup | Complete source-bound PM history/detail from the active environment | resolve_payment_source_end_date_state | Proves exact last start, aligned initial CostInfo and complete preserved account/flag/history baseline | Resolve automatically; a failed or partial prior import must be reconciled before a new preparation, not converted into a separate-object continuation | end_date_baseline;end_date_selected_interval;end_date_current_end;end_date_cost_info;end_date_comparison_facts |
| end_date_loader_contract | Combined MERGE archive and date-effectivity capability | Yes | End Date when F differs from E; skip for verified no change | Required | core.data-loader source/schema validation and Date Effectivity capability evidence for both components | | Require component-specific support for ReplaceLastEffectiveEndDate; it is special metadata outside ordinary attribute lists. Validate both components in one immutable two-member archive through core.data-loader | Include CostInfo with preserved flags and CostAllocation together. Do not split the import, require CostInfo to be closed in a prior load, bypass a validator, or remove the special attribute. Missing/negative capability still blocks automated handoff | end_date_template_validation;end_date_component_capability;end_date_archive_preflight |
| full_kff_ldg | LDG Cost Allocation structure assignment | Yes | Create or effective-dated Update renders accounts, including unchanged carry-forward rows | Lookup | Exact live LDG result bound to the selected source context | resolve_payment_source_kff_ldg | The assigned flex number determines the account structure | Resolve it automatically; stop if missing or inconsistent, not for user certification | kff_ldg_context;cost_allocation_id_flex_number |
| full_kff_metadata | Full Flexfield runtime structure | Yes | Create or effective-dated Update renders accounts | Lookup | Live runtime descriptor for the resolved LDG flex number | resolve_payment_source_full_kff | Account titles, order, delimiter and LOV bindings are environment-specific | Use returned metadata; do not ask the user to approve guessed segment positions | runtime_segment_definitions;runtime_lov_contracts;runtime_delimiter |
| account_rows | Full Flexfield account identity and values | Yes | Create or effective-dated Update renders accounts | Lookup | Live runtime metadata and declared LOV results for requested values and preserved Update components, enriched by fixed defaults | validate_payment_source_full_kff_values | CASH, CLRNG and LBLTY require complete validated accounts; a user's approval is not value-validation evidence | Consume validated_full_kff_accounts and existing defaults. Resolve unchanged Update components from the live baseline rather than asking the user to repeat them | validated_full_kff_accounts;full_kff_validation_evidence |
| hdl_archive | Immutable validated HDL archive and current approval | Yes | At the execution gate before import handoff; not the earlier input/default/dependency pass | Blocked until approved | core.data-loader validation result | | A loader handoff is a side effect; preparing the preview is not. | Complete preparation first, then approve the exact preview immediately before submission. Do not demand approval before the archive and preview exist | archive_fingerprint;approval_fingerprint |
| zap_history | Complete logical allocation history | Yes | New full Zap; recovery uses original sealed history plus current reconciliation | Lookup | Live PM history for the selected source/LDG/environment | query_payment_source_costing_history | Selector date must not hide earlier or later splits | Resolve all pages and one exact allocation | zap_history;sealed_history_keys |
| zap_details | All physical accounts and aligned CostInfo | Yes | New full Zap; recovery uses original sealed details plus current reconciliation | Lookup | Live detail bound to every sealed history tuple | query_payment_source_costing_details | Three objects must be deleted explicitly; there is no cascade | Require all details, aligned dates and independent IDs; no supplied account target dictionaries | zap_parents;zap_accounts;zap_cost_info_targets;sealed_detail_evidence |
| zap_loader_contract | DELETE capability, keys and cross-object dependency processing | Yes | Zap | Required | core.data-loader source/schema and Task Hook validation for the current target environment | | CostInfoId plus the child PaymentMethodId has completed a PM DELETE with successful loader and read-back verification; each new target still requires current published metadata and operation validation | Validate the authored identity-only sources and all included components, requiring the published child PaymentMethodId for CostInfoV3 before approval. A recovery requires the prior core.data-loader per-object/row results, immutable original scope and PM CostInfo-Only Recovery checks; missing evidence blocks. Stop if the loader cannot validate DELETE support, key sufficiency or dependency handling; do not trial-run against Fusion | zap_template_validation;zap_dependency_validation |
| zap_handoff | One approved immutable destructive import | Yes | Final Zap submission or resumed status, not pre-approval preparation | Required | core.data-loader persisted preflight and immutable archive, Task Hook preview and approval, then accepted handoff result | | Prevents approval bypass and uncertain destructive retries | Bind one destructive approval to all periods, components, exact environment and archive bytes; use the loader's authoritative gate only | preflight_envelope;task_preview;archive_fingerprint;approval_fingerprint;ContentId;RequestId |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Search resolution | User-facing filters can resolve candidates through the declared live lookups | Yes, declared read-only search only; no Create |
| Ready | Every required input and prerequisite is confirmed. | No |
| Missing prerequisite | A required setup or source value is absent. | No |
| Approval required | The archive is valid but has not received current approval. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CPS.HDL.CHECK_DEPENDENCIES | decision | 20 | resolve_dependency | ready->CPS.HDL.ENFORCE_ROUTE;blocked->CPS.HDL.HANDLE_ERROR | CPS.HDL.VALIDATE_FULL_KFF | stop | After inputs/defaults, resulting payment-account presence and applicable Full Flexfield checks pass. Update requires its live baseline and validation of all rendered carry-forward accounts; only a proven permitted empty account set skips KFF. Evaluate only the declared dependencies within task scope |
| CPS.ZAP.CHECK_DEPENDENCIES | decision | 21 | resolve_dependency | ready->CPS.ZAP.ENFORCE;blocked->CPS.HDL.HANDLE_ERROR | CPS.ZAP.VALIDATE_SOURCE | stop | Evaluate only Zap dependencies and the shared immutable-archive requirement. Complete source/schema and Task Hook preparation before the final loader approval; skip Create/Update account-write dependencies |
| CPS.END_DATE.CHECK_DEPENDENCIES | decision | 24 | resolve_dependency | ready->CPS.END_DATE.ENFORCE;blocked->CPS.HDL.HANDLE_ERROR | CPS.END_DATE.APPLY_DEFAULTS | stop | Evaluate End Date identity, baseline and both components' loader/date-effectivity support for one combined archive. For F=E skip template/capability/upload. No prior CostInfo-only load or intermediate date difference is required |
