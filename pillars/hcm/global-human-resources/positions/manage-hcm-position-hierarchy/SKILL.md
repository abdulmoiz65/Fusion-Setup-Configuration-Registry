---
skill_id: "hcm.global-human-resources.positions.manage-hcm-position-hierarchy"
name: "Manage HCM Position Hierarchy Setup Task Guidance"
description: "Reads an effective HCM position hierarchy and performs approved hierarchy relationship changes through core.data-loader using the Position Hierarchy business object."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Positions"
functional_area_code: "ORA_POSITIONS"
task_code: "ORA_PER_MANAGE_HCM_POSITION_HIERARCHY"
task_name: "Manage HCM Position Hierarchy"
parent_skill_id: "hcm.global-human-resources.positions"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "HDL"
businessObject: "Position Hierarchy"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "HCM global human resources pillar team"
version: "0.2.1"
inputs:
  - "operation"
  - "ancestor_position"
  - "selected_position"
  - "destination_parent_position"
  - "effective_start_date"
  - "position_details"
  - "move_children_option"
  - "project_context"
outputs:
  - "hierarchy_tree"
  - "hierarchy_scope"
  - "position_hierarchy_xlsx"
  - "setup_data_routing"
  - "operation_run_state"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "hcm.global-human-resources.positions.manage-positions"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
uses_core:
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/positions/manage-hcm-position-hierarchy/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/positions/manage-hcm-position-hierarchy/current/"
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
oracle_supplied_guidance_files:
  - purpose: "Operation, identity, effective-date, row-shape, and source-key validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Hierarchy configuration, Position, access, metadata, and loader readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Ancestor, descendant, Position, relationship, and verification reads"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "As-of-date and workbook-value defaults"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Cycle, stale-state, workbook, approval, and verification blockers"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "CRUD routing, loader failure handling, reconciliation, and retry restrictions"
    location: "ora-resource/ora_error_handling.md"
oracle_supplied_guidance_status: "Authored for REST reads and core.data-loader Position Hierarchy mutations"
side_effects:
  - "Reads effective Position and hierarchy data from the confirmed Fusion environment."
  - "Authors a Position Hierarchy XLSX from live Data Loader metadata."
  - "After an immutable preview and explicit approval, core.data-loader can upload and initiate the approved load."
  - "New-child and duplicate actions combine a Manage Positions-authored Position XLSX with the Position Hierarchy XLSX in one approved core.data-loader ZIP."
  - "Position edit and Position delete actions may delegate a separate approved Position load to Manage Positions."
required_privileges:
  - "Access to positionsLov and positionsV2; Position Searches access when descendant or cycle evidence is required"
  - "Manage HCM Position Hierarchy privilege"
  - "HCM Data Loader upload and load privileges"
  - "Manage Positions privileges for delegated Position create, edit, or delete"
---

# Manage HCM Position Hierarchy Setup Task Guidance

## Purpose

View an effective HCM position hierarchy from a selected ancestor and manage
its parent-child relationships without a state-changing direct REST call.
Reads use Fusion REST resources. Every create, edit, move, remove, or delete
mutation uses `core.data-loader`; underlying Position CRUD is delegated to
`hcm.global-human-resources.positions.manage-positions`, which also uses
`core.data-loader`.

## Task Overview

Use this task to plan and govern `Manage HCM Position Hierarchy` configuration in Global Human Resources.

- **Task identity:** `ORA_PER_MANAGE_HCM_POSITION_HIERARCHY` — Manage HCM Position Hierarchy.
- **Scope:** HCM → Global Human Resources → Positions.
- **Declared routing:** this task uses read-only Fusion REST resources for hierarchy views and `core.data-loader` for approved changes; it does not authorize direct REST mutations.
- **Read next:** [ownership boundary](#ownership-boundary), [supported operations](#supported-operations), and [conditional resource read order](#conditional-resource-read-order). Those sections are authoritative for the operation route, approvals, and resources to load.

## What a Position Hierarchy Is

An HCM position hierarchy is the effective-dated graph formed by each
Position's relationship to its parent Position. A hierarchy node is a Position;
the `PositionHierarchy` record is only the edge from one existing child to one
existing parent. The child is identified by `BusinessUnitName` plus
`PositionCode`, and the parent by `ParentBusinessUnitName` plus
`ParentPositionCode`. Surrogate Position IDs or explicit source keys are valid
alternatives when the live template and `core.data-loader` key rules permit
them.

The relationship can drive assignment-manager synchronization. A hierarchy
change can therefore affect the manager inherited by assignments, and the
`Synchronize Person Assignments from Position` process may be required after
the load. HCM Data Loader automatically triggers hierarchy flattening unless
the submitted DAT explicitly disables that process; this task never adds such
a disabling instruction.

## Ownership Boundary

| Concern | Owner and route |
|---|---|
| Resolve an ancestor or parent reference | `positionsLov` REST read |
| Read descendants | Redwood `positionSearches` read operation and local tree construction |
| Resolve effective Position details, current parent, or verification | `positionsV2` REST read |
| Add, change, move, or end-date a parent-child relationship | `core.data-loader`, Business Object `Position Hierarchy` |
| Create, duplicate, edit, inactivate, or delete a Position | Manage Positions through `core.data-loader`, Business Object `Position` |
| Direct REST POST, PATCH, DELETE, upsert, or ADF batch mutation | Unsupported |

`positionSearches` uses POST as a search operation; it is read-only task
behavior and is not a CRUD mutation. Call only the declared POST; it has no
`describe` operation.

## Supported Operations

| Operation | Business effect | Execution route |
|---|---|---|
| `view_hierarchy` | Show one ancestor and all validated descendants as of one date | REST reads only |
| `build_hierarchy` | Add one relationship row for every non-root existing Position | One Position Hierarchy XLSX load |
| `add_existing_child` | Link an existing Position directly beneath an existing parent | One Position Hierarchy row |
| `move_position` with children | Change the selected Position's parent; its child relationships remain unchanged | One Position Hierarchy row |
| `move_position` without children | Move the selected Position and reparent each direct child to the original parent | One Position Hierarchy XLSX containing all affected rows |
| `remove_from_hierarchy` | End-date the selected relationship and, when needed, move its direct children to the grandparent | One Position Hierarchy XLSX containing all affected rows |
| `create_child_position` | Create a new Position and link it to the selected parent | One combined ZIP containing Position.dat and PositionHierarchy.dat |
| `duplicate_position` | Create a sanitized copy with a new name/code and link it | One combined ZIP containing Position.dat and PositionHierarchy.dat |
| `edit_position` | Change Position attributes; include a Position Hierarchy load only when the parent changes | Manage Positions, plus relationship load when applicable |
| `delete_position` | Delete a Position only when it has no incumbents and no child Positions | Manage Positions through `core.data-loader` |

Deleting or end-dating a `PositionHierarchy` relationship never deletes the
underlying Position. Do not translate `remove_from_hierarchy` into
`delete_position`, or the reverse.

## Conditional Resource Read Order

1. For a Position create or edit with no parent relationship change, delegate directly to Manage Positions; do not read hierarchy resources or generate hierarchy data.
2. Read `ora-resource/ora_input_validation.md` for every hierarchy request.
3. Read `ora-resource/ora_dependency_readiness.md` before a hierarchy read or mutation.
4. Read `ora-resource/ora_reference_lookups.md` whenever a Position or relationship must resolve or be verified.
5. Read `ora-resource/ora_defaulting_rules.md` only when the view date or optional workbook values are absent.
6. Read `ora-resource/ora_design_enforcement.md` before authoring or previewing a mutation workbook.
7. Read `ora-resource/ora_error_handling.md` before routing a mutation and whenever execution is not conclusively verified.
8. Read `core/data-loader/SKILL.md` and its selected references before generating, previewing, or loading an XLSX.

## Hierarchy Read Algorithm

1. Require a Position name or code and resolve one `asOfDate`; default only a
   read-only view to today's date.
2. Call `GET /hcmRestApi/resources/latest/positionsLov` with
   `effectiveDate={asOfDate}`,
   `fields=PositionId%2CPositionName%2CPositionCode%2CJobName%2CDepartmentName%2CBusinessUnitId%2CDepartmentId`,
   `finder=findByWord%3BActiveStatus%3DA%2CFilterAttributes%3DPositionName%20PositionCode%20JobName%20DepartmentName%2CSearchTerms%3D{urlEncodedPositionTerm}`,
   `onlyData=true`, `limit=25`, and `offset=0`.
3. Use the sole row or require the user to choose from at most the first five
   candidates. Extract the selected row's exact `PositionCode`.
4. POST to `/hcmRestApi/redwood/11.13.18.05/positionSearches` with
   `{"filters":[{"name":"AncestorPositionCode","terms":["<resolved PositionCode>"]},{"name":"EffectiveDate","value":"<asOfDate>"}]}`.
   Follow every supported result page.
5. Create the root from the selected `positionsLov` row even when the search
   response omits it. Index descendants by `PositionId`, join them with
   `ParentPositionId`, and use a unique parent name/code only when an ID is
   absent.
6. Reject duplicate IDs, incomplete pagination, cycles, multiple parents,
   unresolved parents, and disconnected descendants. Never infer a parent from
   response order.
7. Render through four descendant levels and name every continuation node.
   Retain the full validated graph for mutation checks.

## Position Hierarchy XLSX Contract

At runtime, generate the editable sample from live metadata with
`core.data-loader` for Business Object `Position Hierarchy`. Preserve its
single `PositionHierarchy` sheet and all live headers. The confirmed template
contains these relationship fields:

- `EffectiveStartDate` and `EffectiveEndDate`
- child keys: `PositionCode` with `BusinessUnitName` or `BusinessUnitId`, or
  `PositionId`
- parent keys: `ParentPositionCode` with `ParentBusinessUnitName` or
  `ParentBusinessUnitId`, or `ParentPositionId`
- optional explicit source keys: `SourceSystemOwner` and `SourceSystemId`
- Fusion-managed identity: `PositionHierarchyId` or `GUID`

Prefer the documented name-based user-key pairs. When a Business Unit ID is
supplied, resolve it to the same current Business Unit and reject conflicts
with a supplied name. Leave surrogate IDs and GUID blank when user keys resolve
uniquely. Accept a supplied `PositionHierarchyId` or `GUID` only when it exactly
matches the current relationship read; otherwise stop. Do not invent source
keys, copy them from an example, or provide only one member of the source-key
pair. Use `YYYY/MM/DD` in Data Loader cells.

Every Position referenced in a relationship row must either already exist in
the target environment or be created by `Position.dat` in the same combined
ZIP. The Position must be effective for the complete requested relationship
range when `PositionHierarchy.dat` is processed. Set the relationship end date
no later than the first applicable child or parent effective-row end date.
Display `4712/12/31` as `End Of Time` to the user.

## XLSX Row Algorithms

| Intent | Rows to author on `PositionHierarchy` |
|---|---|
| Build a hierarchy | One row per non-root Position, ordered by depth from the root. Fill child Business Unit/code, parent Business Unit/code, effective start, and bounded effective end. |
| Add an existing child | One row for the child and selected parent beginning on the approved effective date. |
| Move with children | One row for the selected Position and destination parent. Do not add rows for its direct children, so their parent remains the selected Position. |
| Move without children | First row: selected Position to destination parent. Additional row per snapshotted direct child: child to the selected Position's original parent. Use one approved effective date for all rows. |
| Remove from hierarchy, leaf | If the removal date is later than the earliest relationship start, use MERGE and end-date it on the prior day. If both dates match, use DELETE for the complete relationship. |
| Remove from hierarchy, with children | Apply the same relationship-removal rule and add one reparent row per direct child to the selected Position's original parent. |

For a move, require the user to choose `with_children` or `without_children`;
never infer it. For a removal with children, the grandparent is the automatic
destination. A root without a parent relationship cannot use this removal
algorithm. Resolve the complete relationship history through `positionsV2`.
Reject a removal date before its earliest start; use `MERGE` when it is later
and `DELETE|PositionHierarchy` only when it matches that earliest start.

A multi-row XLSX is one review and one load, but HCM Data Loader row processing
is not treated as transactional. Record the intended result for every row,
verify all affected relationships after completion, and never retry an
uncertain or partially successful load automatically.

## Create, Duplicate, Edit, and Delete Sequence

`PositionHierarchy` cannot itself create a Position. For
`create_child_position` or `duplicate_position`:

1. Snapshot the intended parent and prove the new Position name/code are unique.
2. Have Manage Positions author and validate a live-metadata `Position.xlsx`,
   including `JobId` or `JobCode` with `JobSetCode`, and `LocationId` or
   `LocationCode` with `LocationSetCode`; do not submit it independently.
3. Author `PositionHierarchy.xlsx` with the same Business Unit and Position
   code as the new Position and the selected parent's confirmed keys.
4. Pass both XLSX sources as separate `--ide-file` inputs to one
   `core.data-loader` invocation; do not use a positional source or preview
   either workbook separately. Require one immutable combined ZIP containing
   `Position.dat` and `PositionHierarchy.dat`.
5. Show one combined preview and fingerprint, obtain one standalone `approve`,
   and submit the unchanged ZIP once. HCM Data Loader processes referenced
   business objects before the objects that reference them, so Position is
   loaded before Position Hierarchy.
   Supersede any accidental standalone preview and rerun the combined preview
   in the same turn; do not report it as a blocker.
6. Verify both results: the new Position exists with the approved attributes
   and its hierarchy relationship resolves to the approved parent. Treat a
   successful Position with a failed hierarchy relationship as partial
   completion; do not automatically retry or delete the Position.

Position attribute edits and Position deletes follow Manage Positions. A
Position delete requires a fresh hierarchy check proving zero child Positions
and an authorized incumbent check proving zero incumbents. If either exists,
move or remove dependencies first and require a new delete preview later.

A Position create or edit with no parent relationship add or change follows
Manage Positions only. Do not resolve a hierarchy parent or create
PositionHierarchy data for that request.

## Deterministic Mutation Sequence

Use this order for every relationship mutation:

1. Intake one supported operation, exact Position selectors, effective date,
   and move mode when applicable.
2. Bind one authenticated environment; never derive it from a supplied link.
3. When Core Data Loader requires task context, select the matching active Run
   Book task and derive its context; do not require a separately persisted
   local context artifact.
4. Resolve each parent reference through `positionsLov`, then resolve effective
   Position details and current relationships through `positionsV2`.
5. Read `positionSearches` only when descendants or cycle evidence is required;
   reject no-ops, cycles, stale identities, range gaps, and incomplete graphs.
6. Generate a fresh live-metadata Position Hierarchy XLSX and fill exactly the
   rows required by the applicable algorithm.
7. Show environment alias, operation, effective range, each affected child,
   old parent, new parent, workbook identity, immutable fingerprint, and
   verification assertions.
8. Invoke `core.data-loader` without upload approval to validate the exact
   source and produce its immutable preview. Stop for a later standalone
   `approve` message.
9. After approval, revalidate the unchanged source and current hierarchy. Any
   changed identity, parent, child set, date range, source bytes, or fingerprint
   invalidates approval.
10. Let `core.data-loader` upload and initiate the approved load once. Do not
   call a product CRUD REST endpoint as fallback.
11. Monitor and classify the Data Loader result using the core skill. On a
    failed, partial, timed-out, or uncertain result, refresh state and stop
    before any retry.
12. Refresh affected Positions through `positionsV2`; repeat `positionSearches`
    only when the operation required graph evidence.

## Preflight, Failure, and Redaction

Before a read, preview, or mutation handoff, complete the applicable input,
dependency, lookup, defaulting, and design checks in the task-local
`ora-resource/` guidance. On any failure, classify it through
`ora_error_handling.md`, preserve only the required sanitized diagnostics, and
stop before retry or route substitution. Never print or persist credentials,
tokens, raw payloads, restricted incumbent data, or protected identifiers.

## Refusal Rules

- Do not issue a state-changing direct REST call, ADF batch, or browser write.
- Do not submit a new-child or duplicate hierarchy relationship without its
  new Position either already verified in Fusion or supplied as Position.dat
  in the same dependency-ordered combined ZIP.
- Do not delete a Position through the Position Hierarchy business object.
- Do not purge a date-effective relationship when end-dating satisfies the
  request. A physical Data Loader DELETE is irreversible, is not supported for
  every component, and requires a separately confirmed live delete contract.
- Do not mix `MERGE` and `DELETE` for the same record in one data file.
- Do not infer source keys, parent direction, move mode, mutation date, or an
  unresolved Position.
- Do not claim success from load acceptance or completion alone; require fresh
  hierarchy verification.

## Uniform Authoring and Read Contract

- Interpret each supplied business attribute within its intended parent or child section using the current operation-specific Data Loader metadata and REST `describe`. Match the exact technical name first, then an exact normalized display label or declared alias, then one unique case-, space-, and punctuation-insensitive match. If multiple fields remain plausible, show their business labels and ask the user to choose; if none match, report the field as unsupported. Never guess or copy a value between fields.
- For create or edit, map only resolved user values to the exact business-object section, resolve references through declared task resolvers, preserve omitted existing values, and author only requested or operation-required rows and fields through the existing mutation route.
- Determine mandatory input only from current operation-specific metadata and operation-required business identity. Never require or populate a nonmandatory field merely because it appears in a template, example, or response. EFF or Additional Information contexts and segments are always optional and must never be requested as a prerequisite; emit an EFF row only when the user explicitly requests that change, using only its resolved context, identity, changed values, and any fields current metadata requires for that included row.
- Never hard-code a business value from an example. Apply a fixed default only when the task defaulting rules and current metadata confirm it for the exact operation; otherwise omit an optional field or ask only when current metadata marks it required. Fixed technical discriminators are allowed only where the task contract requires them to identify the exact business-object section.
- For a normal read, present business-facing labels and values. Do not show WHO or history columns such as `CreatedBy`, `CreationDate`, `LastUpdatedBy`, `LastUpdateDate`, or `LastUpdateLogin`, or primary/surrogate identifiers, unless the user explicitly asks for them; retain identifiers internally for linking and mutation.
- When the user asks for complete details, read the exact parent without a restrictive field projection, expand every task-supported child or EFF collection by following server-returned links, paginate every collection, and return all current business attributes and child values after the same WHO/ID filtering. State when no supported child collection exists or none is returned; never invent a child path.

## Implementation Notes

Use the parent functional-area skill for broader Positions sequencing. Track
token usage only when this task writes project artifacts or skill-run records.
