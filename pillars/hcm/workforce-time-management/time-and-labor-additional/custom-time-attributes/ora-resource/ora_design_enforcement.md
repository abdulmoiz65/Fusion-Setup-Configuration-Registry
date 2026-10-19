# Custom Time Attributes Design Enforcement

## Source Basis

- User-provided Generic FSM Baseline for Custom Time Attributes, 5 October 2026.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate business prerequisites | Validate task-specific inputs, dependencies, and operation rules before export. |
| 2 | Obtain fresh same-task export | Use shared.setup-export.task-level-export for ORA_HWM_MANAGE_CUSTOM_TIME_ATTRIBUTES; stop if the export cannot be obtained or validated. |
| 3 | Populate scoped change | Populate only the approved task-specific change and preserve unrelated exported values. Scope approval is not import approval. |
| 4 | Validate package | Require exact-case ASM_SETUP_CSV_METADATA.xml, task-scoped object CSV members, valid keys, relationships, and approved row scope. |
| 5 | Route package | Route the validated FSM ZIP to core.data-loader only when evidence proves the declared FSM route. |
| 6 | Wait for preview | Wait for the immutable package preview from core.data-loader. |
| 7 | Complete Summary | Generate the business-only Complete Summary from verified structured values after validation, lookup resolution, and defaulting, before the provider-owned approval process. |
| 8 | Require approval | Obtain explicit approval for that current preview through core.data-loader; never reuse stale preview or approval evidence. |
| 9 | Import once | Submit once through the declared FSM route owned by core.data-loader. |
| 10 | Reconcile | Reconcile through the documented task read/export path and selectors; stop on failed, partial, timed-out, or uncertain import. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Classification is With dependent attributes | Error | | Dependent Time Attributes section is unavailable or child definitions omit the applicable attribute fields | Show the section; each dependent uses the parent field contract except Classification, Unit of Measure, and Attribute Category | Yes |
| Classification is Without dependent attributes | Error | | Dependent attributes are included | Hide the dependent section and stop for correction if children were supplied; do not silently discard them | No |
| Editing an existing parent Custom Time Attribute | Error | | The requested change includes Display Name, Name, Data Type, Classification, Attribute Category, or Value Location | Preserve those parent fields from the fresh export and remove them from the requested update; stop before preview until the requested scope contains only fields that can be changed | No |
| Editing an existing Dependent Time Attribute | Error | | The requested change includes Display Name, Name, Data Type, or Value Location | Preserve those child fields from the fresh export and remove them from the requested update; stop before preview until the requested scope contains only fields that can be changed | No |
| After fresh export, before package preparation | Error | resolve_filtered_data_source | Required filtered source remains deferred, missing, or ambiguous, and no explicit user confirmation of an export mismatch is recorded | Resolve from exported data before preview, or record the user's confirmed available-in-Fusion selection as an override and reconcile the link after import | No |
| After fresh export, before package preparation | Error | resolve_unfiltered_data_source | Required unfiltered source remains deferred, missing, or ambiguous, and no explicit user confirmation of an export mismatch is recorded | Resolve from exported data before preview, or record the user's confirmed available-in-Fusion selection as an override and reconcile the link after import | No |
| Parent attribute, after fresh export | Error | resolve_attribute_category | Required category remains deferred, missing, or ambiguous | Resolve from exported data before preview | No |
| New parent or dependent attribute, after fresh export | Error | resolve_value_location | Value Location is unresolved, occupied, or duplicated among new package rows | Use the resolved unused location before preview; preserve existing attribute locations | Yes |
| Preparing an FSM change | Error | | Unrelated exported values change or rows exceed approved scope | Preserve unrelated values and restrict changes to the approved scope | Yes |
| Catalog-routed FSM Create or Edit | Error | | Package is converted to an HCM Data Loader archive or direct Fusion REST mutation is proposed | Keep the FSM ZIP and route through core.data-loader | No |
| After fresh export | Error | | FSM evidence does not prove the expected route | Stop and rebuild from validated same-task evidence | Yes |
| Before submission | Error | | Current immutable preview approval is missing or stale | Obtain current approval through core.data-loader | No |
| After fresh export, before package preparation | Error | | Export evidence does not establish the required package mapping or operation semantics | Establish task-scoped CSV members, field mappings, keys, relationships, and operation semantics from validated export evidence; do not guess | No |
| Before import | Error | | The documented read/export path and selectors cannot identify the changed object and related rows | Establish the documented reconciliation read/export path and selectors for the changed object and related rows | No |
| After import with a confirmed export mismatch | Error | | The exported source link does not equal the user-confirmed requested source | Report the update as not applied; do not claim success or retry automatically | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_filtered_data_source | After fresh export for parent and dependent attributes | Verified exported filtered source representation and reference keys | ora_reference_lookups.md |
| resolve_unfiltered_data_source | After fresh export for parent and dependent attributes | Verified exported unfiltered source representation and reference keys | ora_reference_lookups.md |
| resolve_attribute_category | After fresh export for parent attributes | Verified exported category representation and reference keys | ora_reference_lookups.md |
| resolve_value_location | After fresh export for new parent and dependent attributes | Unused Value Location reserved for the new row | ora_reference_lookups.md |

## Task-Specific Contract Boundaries

The baseline defines orchestration, not a Custom Time Attributes field contract.
The field contract is in ora_input_validation.md and automatic population is in
ora_defaulting_rules.md. Both data-source selections and Attribute Category resolve from the fresh
same-task export through ora_reference_lookups.md. Value Location
mappings and unused-slot selection are documented in ora_defaulting_rules.md
and resolve_value_location; actual CSV members and columns still require
fresh-export verification. CSV members,
keys, relationships, and reconciliation selectors must be established at their
post-export gates. Do not borrow Time Allocation mappings or invent a writable REST route.
The user designated the fresh same-task export as the local lookup authority;
no live LOV request is required by these rules.

## Complete Summary Contract

Generate the Complete Summary only after validation, lookup resolution, and defaulting have produced verified structured values. Always generate it before the provider-owned approval process. Include every user-provided business value and every default actually applied. Omit blank, null, unused, and metadata-only values. Show populated child records only when they have values and use business labels only. Keep implementation-only values internally for validation and provider execution. Do not add warnings, diagnostics, or technical notes.

## Complete Summary

| Business Setting | Selected Value |
|---|---|
| <business label> | <verified business display value> |

## Defaults Applied

| Business Setting | Default Applied |
|---|---|
| <business label> | <verified default display value> |

## Display Value Rules

| Value Kind | Display Value |
|---|---|
| Resolved selection | Verified business display name |
| Identifier or code | Verified business meaning |
| Boolean setting | Selected, Not selected, Enabled, Disabled, Yes, or No as applicable |
| Lifecycle state | Business-friendly state such as Draft or Submitted |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CTA.COMPLETE_SUMMARY | step | 19 | design_enforcement | summary_ready->CTA.ENFORCE_FSM;summary_incomplete->CTA.HANDLE_ISSUE | CTA.APPLY_DEFAULTS | stop | A validated Custom Time Attribute proposal is ready for the provider-owned approval process |
| CTA.ENFORCE_FSM | decision | 20 | design_enforcement | compliant->CTA.RETURN_HANDOFF;blocked->CTA.HANDLE_ISSUE | CTA.COMPLETE_SUMMARY | stop | Apply the baseline gates at their stated stages; completion does not authorize a mutation |
