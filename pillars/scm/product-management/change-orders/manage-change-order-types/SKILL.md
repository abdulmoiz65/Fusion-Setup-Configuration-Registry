---
skill_id: "scm.product-management.change-orders.manage-change-order-types"
name: "Manage Change Order Types Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Change Order Types under the Change Orders functional area."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Change Orders"
functional_area_code: "EGO_CHANGE_ORDERS"
task_code: "EGO_MANAGE_CHANGE_ORDER_TYPES"
task_name: "Manage Change Order Types"
parent_skill_id: "scm.product-management.change-orders"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM product management pillar team"
version: "0.1.6"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "attachment_category"
  - "attachment_category_association_start_date"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "attachment_category_resolution"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.apps-common"
  - "scm.product-management.items.manage-attachment-categories-for-product-management"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
state_updates:
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/change-orders/manage-change-order-types/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/change-orders/manage-change-order-types/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects: []
required_privileges: []
---

# Manage Change Order Types Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Change Order Types` under `Change Orders`.

## Setup Task Skill Contract

- task_code: `EGO_MANAGE_CHANGE_ORDER_TYPES`
- task_name: `Manage Change Order Types`
- parent_skill_id: `scm.product-management.change-orders`
- pillar: `SCM`
- offering: `Product Management`
- functional_area: `Change Orders`
- functional_area_code: `EGO_CHANGE_ORDERS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Change Order Types` under `Change Orders`.

## Setup Task Metadata

- Task name: `Manage Change Order Types`
- Task code: `EGO_MANAGE_CHANGE_ORDER_TYPES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Default Priority, Default Reason, and Lookup Dependencies

| Change type field | Standard Lookup | Lookup task |
|---|---|---|
| `PriorityCode` | `EGO_CHANGE_PRIORITIES` | [Manage Change Priorities](../manage-change-priorities.md) |
| `ReasonCode` | `EGO_CHANGE_REASONS` | [Manage Change Reasons](../manage-change-reasons.md) |

For each requested default assignment, resolve the exact `LookupCode` as an
enabled value through `core.fusion-api.apps-common` and its `lookups` workflow.
Do not call a lookup endpoint directly from this skill. If a code is missing,
create it through the mapped lookup task after that task's read preflight and
explicit approval; do not create it through the Change Order Types FSM ZIP.
Re-read every created code and require it to be enabled.

Resolve every requested priority and reason before exporting Change Order
Types. Once all requested lookup values are enabled, obtain one fresh export
and prepare one creation or update package that assigns all requested values.
If the user requests only lookup creation, do not associate it with a change
type. Stop if a code is absent, disabled, or ambiguous; never substitute a
similarly named code.

Clear a default only when the user explicitly requests removal. Confirm the
target field is nonblank in a fresh export, and clear only the explicitly
requested `PriorityCode`, `ReasonCode`, or both. This restriction applies to
lookup clearing, not to other independently valid changes in the package.
Process Start Date separately under the Change Type Header Dates rules;
neither operation requires nor blocks the other. Allow independently requested
changes and applicable defaults in the same package, while preserving unrelated
values and shared lookup definitions. Retain required dependent rows, validate the exact ZIP through
`core.data-loader`, then present the previous and blank values, ZIP contents,
and target environment for import
approval. If validation rejects the blank value, stop without upload or retry.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Change Orders`
- Setup task name: `Manage Change Order Types`
- Setup task code: `EGO_MANAGE_CHANGE_ORDER_TYPES`

## Fresh Export Recovery and Outcome Handoff

When a Manage Change Order Types export attempt returns no Process ID, ZIP, or process log, use this bounded recovery workflow after the active project's prerequisites have passed:

1. Validate Fusion authentication or refresh it through the Fusion OAuth login capability, core.auth.fusion-oauth-authentication. If authentication fails, stop and report that failure before submitting another export.
2. Submit exactly one new read-only Manage Change Order Types setup-data export through shared.setup-export.task-level-export for EGO_MANAGE_CHANGE_ORDER_TYPES. Capture and persist the new attempt's Process ID, ZIP, and process log wherever available; identify explicitly which evidence was not returned.
3. If the retry returns none of those, stop and report a Fusion export-process issue with the environment, task code, attempt details, and missing evidence. Do not prepare an import package from stale exports, upload, import, or silently retry again.
4. If only a Process ID or process log is returned, use the shared export workflow's bounded status/log handling for that process. Neither is a substitute for a successful fresh setup-data ZIP. On failure or timeout, stop and disclose the process status and available evidence.
5. Choose the user handoff from the export outcome. When a fresh setup-data ZIP is available and validated, prepare the requested changes without intermediate confirmation, show the prepared import ZIP contents, and request explicit import approval. When export fails or produces no usable ZIP, request direction to restart export or restart runbook execution through the existing workflow. If runbook execution was interrupted, request direction to resume or restart it from its recorded state; do not replay completed imports or other mutations automatically. Do not offer import from stale or missing data.

## Base and Child Change Type Identification

Base Change Type is a mandatory input when creating a change type. Require the user to explicitly identify the base/source change type to copy, by name or code, in the request or established task context. If it is missing or blank, stop at input validation and show: "Base Change Type is missing from your request. Please provide the name or code of the change type to copy before I can create the new change type." Do not select a default, infer it from the new type's name, or reuse an unrelated prior selection. This is a missing-input request, not an intermediate confirmation gate. Do not prepare or submit the creation package until the supplied selection resolves to exactly one exported type. For an update, use the selected existing target's exported relationship; do not require the user to re-enter its base type. Lead with this missing-input message; do not replace it with a generic statement about mandatory base selection or dependency checks. Mention other missing inputs separately only when they are actually missing.

Use the Base Change Type Mapping in [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md#base-change-type-mapping), transcribed from the user-provided Base Type vs Copied From.docx, to resolve the selected source name/internal code and its CopiedFrom value. The required creation input Base Change Type means the source selected for copying; it is distinct from that source's CopiedFrom value. For example, Engineering Change Order selects ORA_ENG_CO and retains CopiedFrom ENG_CO; Commercialization Change Order selects ECO and retains CopiedFrom ECO. Do not replace CopiedFrom with the selected source's internal code or derive it by stripping a prefix.

Read `CopiedFrom` from the exported `EGO_CHANGE_HEADER_TYPE` content for every reference to a base or child change type in lookups, copying, updates, validation, and package previews. Compare `CopiedFrom` with the current change type's corresponding identity in that exported content:

- If `CopiedFrom` identifies the current change type itself, classify it as a base change type.
- If `CopiedFrom` identifies a different change type, classify the current type as a child of the base change type identified by `CopiedFrom`.

This comparison identifies the change type's base/child relationship; it does not classify workflow statuses.

## Conditional Attachment-Category Workflow

When creating a change order type, first check whether the input supplies an
`attachment_category`. If it is absent, do not create, look up, or associate an
attachment category; continue with the normal change-order-type creation flow.

When an attachment category is supplied, complete this dependency before
preparing or importing the change-order-type package:

Default an omitted or blank Entity Name to `EGO_ENGINEERING_CHANGES_B` before attachment-category validation or delegation. Pass that value explicitly to Manage Attachment Categories for Product Management; do not ask the user for it or report a missing-entity-input error. This default is specific to Manage Change Order Types. If a different entity is explicitly supplied, report the mismatch rather than silently replacing it.

Explicitly request a fresh **setup-data export**, not a template/spec export, through the delegated attachment workflow. Resolve the requested category and its association to `EGO_ENGINEERING_CHANGES_B` from that export. Use entity export criteria only when supported by the selected workflow; otherwise inspect the returned data for that entity without inventing a filter or endpoint. Defaulting the entity supplies lookup context, not proof of an existing association. Missing or incomplete export evidence must not be treated as a missing category or association. A category absent from the entity-scoped results is not necessarily absent from the system; distinguish an existing category lacking the association from a nonexistent category before proposing creation.

1. Route the request to
   `scm.product-management.items.manage-attachment-categories-for-product-management`
   (Manage Attachment Categories for Product Management under **Product
   Management → Items**). Resolve the supplied Category Name as an exact,
   unambiguous category for entity `EGO_ENGINEERING_CHANGES_B`.
2. If the category already exists, reuse it. If it does not exist, invoke that
   skill to create it with exactly these inputs: Category Name, User Name,
   Description, and Entity Name `EGO_ENGINEERING_CHANGES_B`. Do not substitute
   a similar category or a category for another entity.
3. Require successful category creation or successful reuse resolution before
   proceeding. For creation, retain the returned category identity and success
   evidence from the attachment-category workflow.
4. Use a supplied `attachment_category_association_start_date` when present.
   When it is absent, default the association Start Date to the current date at
   package preparation, using the format evidenced by the supplied export (for
   example, `YYYY/MM/DD`). Record whether the date was supplied or defaulted in
   the package preview. Never reuse an unrelated association date.
5. Add the resolved category and its nonblank Start Date to the Change Policy
   for the change order type in the same validated Change Order Types package.
   For an existing category, this step ensures it is associated with the Change
   Policy; for a newly created category, it performs that association after
   creation.
6. Before requesting import approval, validate that the exact resolved category
   and its nonblank Start Date are present in the target Change Policy
   association and in the ZIP being shown for approval. Do not submit a
   change-order-type creation package when a requested category cannot be
   associated or the applied date is invalid.

If category lookup, category creation, association Start Date derivation or validation, or
Change Policy association validation fails, return a structured failure
identifying the category name, entity, failed stage, and recommended action.
Stop before Change Order Types import; do not create a change order type without
its requested attachment-category association. After import, reconcile the
association as a requested change and report it as processed only when the
import evidence confirms it.

## Import Package Scope and Row Preservation

Apply the Header Attribute Import Rules below as an explicit exception to row preservation for both creation and update packages.

- Build each import package from the exported rows for the selected source or target change type, including all related rows across dependent files. Retain unchanged dependent rows so an update does not fail because required entities are missing; do not build a package containing only changed rows.
- For new change order type creation, copy all rows belonging to the selected source change type and all related dependent rows into the import package. Apply the user-requested changes and the identity changes required for the new type, including unique Route and route-step identifiers. Update dependent references consistently to point to the copied entities, and preserve all other source values.
- When copying a child change type, retain the source row's `CopiedFrom` value. Do not substitute the source `TypeInternalName`; for example, a copy of `ORA_CR` must use `CopiedFrom: CR`, not `CopiedFrom: ORA_CR`.
- For an existing change order type update, copy all rows belonging to the target change type and all related dependent rows from the export package into the import package. Apply only the user-requested changes and retain existing identifiers, relationships, and all other unchanged values.
- Scope update packages to the target change type and its related dependencies only. Do not include unrelated change types or their dependent rows merely because they appear in the same export. Retaining all dependent rows means retaining all rows related to the selected type, not every row in every exported file.
- Before ZIP preparation, validate that all selected-type rows and required dependent rows have been retained except for the required child-type header-attribute exclusions below, references remain consistent, unrelated types are excluded, and differences from the export are limited to the requested changes, those exclusions, and, for creation, the required identity and reference changes.
- When a requested attachment category is resolved, retain or add the exact Change Policy association row required by the supplied export format. Its `StartDate` must be nonblank and match the supplied effective date or the recorded current-date default. Treat a missing, ambiguous, mismatched, or undated association as a blocking package-validation failure.

### Internal Workflow Reconstruction

For every creation or workflow update, build one canonical target workflow from the selected fresh-export baseline plus explicit requested edits. Never concatenate untouched copied workflow rows with separately generated target rows, or use a previously prepared import as the baseline for regeneration.

Resolve the source-to-target status and route mapping before emitting dependent rows using `resolve_change_type_workflow_mapping` in [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md). Sequence numbers are positions, not stable status identities: inserting an approval stage can move Scheduled and Completed. A split or renamed stage requires a request-backed mapping, not a nearest-sequence or route-name guess.

Apply that mapping consistently to routes, route steps, route people, workflow controls, and evidenced workflow-template references. For creation, allocate new route identities and remap each step's complete parent key. Preserve step activity and step sequence unless explicitly changed; the supplied CSV identifies steps within their route, so do not invent a global step-ID column or globally renumber steps. For updates, preserve retained entity identities while updating relationships required by an explicit workflow edit.

Enforce the canonical design rules on the actual final ZIP, not just an in-memory table or staging directory. Every step must resolve to exactly one target route under the same type and status; every route-person row must resolve to exactly one target step. Reconcile all required baseline dependencies and requested additions after remapping. Regeneration with the same baseline, requested edits, and identity map must produce the same logical rows without appending duplicates. Keep these routine mechanics internal.

### Internal Workflow-Control Uniqueness

For creation and update packages, emit exactly one ORA_EGO_WORKFLOW_STATUS_CONTROL row per target change type, target workflow status, and action. Use the exported columns and relationships to establish those identities; do not guess key-column names.

- Remap copied source controls through the same status mapping used for routes before evaluating uniqueness. Construct each target status's controls once from its mapped baseline and overlay only explicit requested edits; never retain the old source-sequence block alongside the remapped block. Apply requested control changes to the matching retained row instead of appending another target row for the same status/action.
- Add a new control row only when its target status/action key is absent. Preserve every distinct required control and its unchanged values; row preservation does not require retaining duplicate representations of the same control.
- Collapse exact duplicates after remapping. For differing rows with the same target key, apply only explicitly requested value changes to the authoritative exported baseline. If conflicting values remain unresolved, stop package validation rather than selecting the first or last row arbitrarily.
- Validate uniqueness after all copying, remapping, and requested edits, and again against the final ZIP member before import approval. Duplicate keys or unresolved status/action identities block upload and import.
- Keep this preparation and validation internal. Do not announce deduplication, key checks, or workflow-control row handling in routine plans, progress messages, previews, or summaries. If validation cannot complete, report the actionable failure without claiming success; retain technical details in diagnostics.

### Rejection-Reason

- For an association or update, input will be Lookup Code or Rejection Reason Code, also it may be Meaning or Rejection Reason consider any one of these as the rejection-reason selector.
- Input can have change type selector and multiple rejection reason in case if multiple rejection reason association or update.
- When Lookup Code or Rejection Reason Code is provided, use it directly in the change-type ZIP.
- When Meaning or Rejection Reason is provided, export the Manage Workflow Rejection Reasons data to resolve its Lookup Code, then use that code in the change-type ZIP. If no unique code is found, stop and ask for a valid rejection reason.
- If provided reason already exists in the change type it can be updated.
- To associate or update a rejection reason, add the rejection reason selector and optional Sequence Number to the change type. To update an existing association, identify it by Lookup Code; only its Sequence Number can be changed.
- Rejection Reason, Inherited, Enabled, Start Date, and End Date are informational at the change-type level and cannot be updated. Reject a request to change any of them and Sequence number is updatable.
- Removing a rejection reason from a change type is unsupported. Direct the user to remove the row in the Change Order Type UI; do not prepare or submit a rejection-reason deletion ZIP.

### Required Role Code

When a creation or update request adds or changes a role assignment, require an explicit Role Code in the request or established task context. A role display name alone is not sufficient. If the code is missing or blank, stop validation for the requested assignment and show: "Role Code is missing from your request. Please provide the Role Code for the role you want to assign." Do not guess a code from a display name or substitute another role. Do not prepare or submit the affected assignment until the code is provided. If no role change is requested, preserve the exported role values without asking the user to re-enter them. Requests to remove a creator continue to follow the unsupported-removal guidance below.

### Creator Removal

- When the user requests removal of a creator from a change type, show: "Removing a creator from a change type through this import workflow is unsupported. Please remove the creator row in the Change Order Type UI."
- Do not prepare or submit a creator-deletion ZIP, or omit the creator row to attempt deletion. Retain the existing creator rows in any package for other requested changes and disclose creator removal as not processed, requiring the UI action above.

## Scheduled Status Restriction

Before creation or update import approval, review all workflow statuses in the resulting target package, including unchanged statuses copied from the export. If the target's CopiedFrom is CR, DCR, PR, or CA, Scheduled status is not allowed. This includes Change Request, Deviation Change Request, Problem Report, Corrective Action, and their copied child types; determine the family from the exported relationship and Base Change Type Mapping, not the target's display name.

If any workflow step resolves to Scheduled using the exported status identity or meaning, stop validation before upload/import and show: "Scheduled status is not supported for change type '{change_type}' (base family '{family}'). Remove Scheduled from the requested workflow before importing." Identify the affected workflow step. Do not silently remove a copied status or bypass this rule because the row is unchanged. This specific restriction is mandatory even while general workflow-policy decisions remain deferred.

## Change Type Header Dates

For creation and update packages, convert any user-provided Change Type header Start Date or End Date to the format evidenced by the corresponding date fields in the fresh exported CSV. Preserve the supplied date's meaning; do not assume a generic date format. If header Start Date is not provided, use the current date at package preparation in that same format, rather than copying the exported Start Date. This is an explicit exception to unchanged-value preservation. If End Date is not provided, preserve its exported value, including a blank value.

If a supplied date is ambiguous or invalid, or the exported date format cannot be established, report the specific issue before preparing the affected fields. Show the applied header dates in the package preview and identify a defaulted Start Date. These rules apply only to Change Type header dates, not rejection-reason informational dates or attachment-category association dates, which retain their separate rules.

## Item Effectivity Field Rules

Apply these rules when preparing either a new change type or an update:

- If the user does not request an item-effectivity change, retain the exported EffectiveImmediatelyFlag and EffectivityIncrementDays values unchanged.
- If the user explicitly requests the change order to be effective immediately, set EffectiveImmediatelyFlag to Y. Preserve EffectivityIncrementDays unless separately requested; do not implicitly clear or reset it.
- If the user explicitly provides item-effectivity days greater than zero, set EffectiveImmediatelyFlag to N and EffectivityIncrementDays to the supplied number of days.
- Do not infer an immediate-effectivity request from a supplied zero or from an omitted day value. If the request combines immediate effectivity with positive days, clarify the conflicting intent before changing these fields.

## Header Attribute Import Rules

- Header attributes Customer, Supplier, Manufacturer, and Source can be modified only on base change types. Apply this restriction during import package preparation as well.
- Determine whether the target change type is a base or child using `CopiedFrom` in `EGO_CHANGE_HEADER_TYPE`, as described above. For creation, apply the rule to the resulting new change type's relationship, not merely to the source type's relationship.
- When the target is a base change type, apply header-attribute changes requested by the user and preserve other unchanged header-attribute values.
- When the target is a child change type, omit header-attribute rows from the import package, including unchanged rows copied from the export, to avoid an `EGO_ATTR_DISPLAY_CONFIG_U2` violation. Retain the other related dependent rows under the row-preservation rules above.
- If the user requests header-attribute changes on a child change type, explain that those changes can be applied only to its base change type. Do not silently modify or add the base change type to the child-type import package.
- Validate the header-attribute inclusion or exclusion internally before ZIP preparation. Routine exclusion of child-type header-attribute rows is a technical implementation detail; do not announce it in user-facing plans, progress messages, previews, or summaries. If an explicitly requested header-attribute change cannot be applied, explain the unapplied business change and base-type restriction without describing row-exclusion mechanics.

## Validation, ZIP Preparation, and Import Approval

Do not ask for confirmation during validation or ZIP preparation. Complete the supported validation and prepare the import ZIP without an intermediate approval gate. Before any import, show the prepared ZIP contents, including its member paths and the configuration rows or files to be imported, then obtain explicit approval for that exact prepared ZIP and target environment. Do not import if the ZIP changes after it is shown; revalidate, show the replacement ZIP contents, and obtain new explicit approval.

## Post-Import Log Review and Request Reconciliation

After every completed import, use the active core.data-loader workflow to retrieve and review the job status, import logs, and available row-level results, including when the job reports Success or Succeeded. A successful job status alone does not prove that the user's requested changes were processed; warnings may identify skipped or rejected changes.

Reconcile every requested change against the approved package and the import results. Follow the post-import disclosure rules in ora-resource/ora_error_handling.md and report each request as processed, not processed, partially processed, or unverified. Include changes excluded before submission as not submitted; do not count unchanged retained dependency rows as fulfilled user requests. Cite the relevant log evidence and include warnings or errors with their affected type, entity, or row and recommended next action.

Present the Fusion job status separately from the request outcome. If logs are missing or do not establish whether a change was applied, mark it unverified rather than successful. Retain the actual downloaded import log file or files alongside the reconciliation summary under the active project's task artifact directory, using a distinct run/job subfolder so later imports do not overwrite earlier evidence. A log reference or summary alone is not sufficient. Redact credentials and sensitive payloads before workspace persistence while preserving diagnostic warnings, errors, and processing outcomes; identify any redaction. Link the retained log files from the summary and final response, and record the job/process identifier and submitted package reference. If log retrieval or persistence fails, disclose the failure and do not claim that the log was retained. Do not automatically retry an import to address warnings or errors; use the existing preparation, validation, preview, and approval workflow for any corrective import.

## Best Practices

### Manage Change Order Type

- When copying a base change type, create a new Route and new route steps with unique identifiers; never reuse the base type's Route or route-step identifiers, because Fusion rejects duplicate unique identifiers.
- Use an Oracle predefined change type as the baseline, and create enterprise-specific change types by copying the appropriate predefined type.
- Keep the seeded change-type hierarchy and shared parent configuration stable; use **All Change Types** only for hierarchy and inherited flexfield configuration, not for creating changes.
- Select the predefined type that matches the business purpose—such as Engineering Change Order, Commercialization Change Order, Change Order without Revision Control, or Change Request.
- Define only approved workflow statuses for each change type, with a sequence appropriate to its business purpose. Scheduled is prohibited for CR, DCR, PR, and CA families; include scheduling only where supported.
- Include interim approval statuses only when a genuine staged-review requirement exists; avoid workflow steps that do not add a clear control or decision.
- Use a consistent change-order number generation method, priority, reason, effective-date policy, cancellation behavior, and assignee model. Avoid uncontrolled changes after production use begins.
- Treat a new default priority or reason as a cross-task dependency: create it
  through its mapped lookup task first, then associate its verified enabled
  code through this task. Lookup creation and Change Type import are independent
  mutations with separate approvals.
- Treat removal of a default priority or reason as a type-only update. Never
  delete or disable the shared lookup code; proceed only if the exact
  blank-field package passes Fusion validation and receives import approval.

### Manage Change Policy

- Define the Change Policy at the change-type level before users create or import change orders.
- Use a consistent, enterprise-approved number-generation method for each change type: Sequence Generated, Rule Generated, or User-Defined.
- For sequence-generated numbers, define and govern the prefix, starting number, increment, and suffix; prevent overlapping sequences across change types and environments.
- For rule-generated numbers, associate a tested rule set with the correct change type and validate uniqueness, required inputs, exception handling, and import behavior.
- Use user-defined numbers only when an external or regulatory identifier must be retained; establish uniqueness and format controls before enabling manual entry.
- Do not change a number-generation method without impact assessment. Existing change-order numbers remain unchanged, but new records will follow the new method.
- Set a default item effective-date policy that reflects the normal implementation lead time, while allowing authorized users to adjust the affected-object effective date before submission when needed.
- Remember that the affected item’s effective date determines production effectivity; the policy setting supplies the default for change lines.
- Define a clear cancellation policy, including when a scheduled change can be canceled and whether the change should automatically complete after all applicable lines are completed or canceled.
- Configure comments as Required when traceability or audit justification is needed, Optional when context is useful but not mandatory, and Not Applicable only when comments provide no business value.
- Establish a default assignee and, where required, an assignee role for every active change type. This is particularly important for supplier-initiated changes to avoid unowned or stalled workflows.
- Grant controlled access to modify assignees. Ensure authorized creators, requesters, or workflow participants can reassign work when the current assignee is unavailable.
- Set approved default priorities and reasons that support consistent triage, reporting, approval routing, and analytics. Review and retire unused values under change control.
- Associate only the attachment categories required for the change type, such as engineering evidence, regulatory documentation, impact analysis, or approval support.
- When a creation request names an attachment category, use the conditional attachment-category workflow above: reuse an existing exact category or create it through Manage Attachment Categories for Product Management with entity `EGO_ENGINEERING_CHANGES_B`, then verify its Change Policy association and explicit effective Start Date before importing the change order type.
- Configure standardized rejection reasons so approvers provide actionable, reportable feedback when rejecting a workflow.
- Review policy changes for their impact on active change orders, approvals, notifications, integrations, reports, audit requirements, and downstream applications.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `attachment_category_resolution`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `scm.product-management.change-orders` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
