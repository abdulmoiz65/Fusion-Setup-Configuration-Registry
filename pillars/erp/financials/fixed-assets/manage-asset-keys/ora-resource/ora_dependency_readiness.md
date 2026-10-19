# Dependency Readiness

## Batch Import Preparation

For a CSV or list of keys, resolve the target System Controls record and KEY#
structure once per structure and environment. Map enabled segments to their
exact current `ValueSetCode` and dependent-parent requirement, then use the
value-set skill's grouped workflow for distinct set codes and requested values
per returned parent link.

Detect duplicate physical ten-segment combinations within the input locally.

Use the paginated BOSS `assetKeys` resource to index exact records by structure
plus all ten physical segments and to build a separate collision index across
structures using all ten segments alone. If BOSS is unavailable, denied,
malformed, or cannot be paged completely, use one newly completed,
same-environment `FA_MANAGE_ASSET_KEY` setup-data export and its
`FA_ASSET_KEY.csv` instead. Do not mix a partial BOSS result with export rows.
A cross-structure collision is not an existing record in the selected
structure to update. Normalize unused physical columns to blank only after
deployed-structure mapping.

Only after the required dependency order has resolved and
`MAK.ENFORCE_DESIGN` has passed, enter `MAK.PREPARE_ARCHIVE`. At that node,
verify the ordered rule-result record before requesting this task's CSV template
or specification package through `shared.setup-export.task-level-export` in
template mode. The record must show successful input validation, reference
resolution, dependency checks, defaults, and design enforcement. Use the
template's verified members,
headers, row widths, and metadata as the package-shape source for the immutable
import artifact. Do not use the template as target-state or duplicate evidence. Inspect
`ASM_SETUP_CSV_METADATA.xml` and the CSV members to identify the Asset Key
combination object and its serialized keys; do not guess a filename, require an
unexported `CodeCombinationId`, or synthesize that ID. If the template package
cannot be downloaded or inspected unambiguously, stop before archive
preparation.

## Batch Evidence Lifecycle

Keep the System Controls, structure, value-set, selected duplicate-evidence
source, and batch fingerprints together. Partition mixed structures into
explicitly resolved batches.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---:|---|---|
| 1 | Asset Key System Controls | Use `resolve_asset_key_system_control` to establish the enterprise identity and obtain its exported AssetStructureInstanceCode. |
| 2 | KEY# structure | Use `discover_asset_key_kff_structure` to obtain a new KFF task export for this request and target environment, then resolve one enabled KEY# structure, its delimiter, displayed segments, requiredness, and value-set mappings. |
| 3 | KEY# combination mapping | Use `resolve_asset_key_kff_combination` to map supplied values to the selected instance and physical Segment1 through Segment10 columns. |
| 4 | KEY# segment values | Verify every mapped value and required dependent parent through current grouped evidence. |
| 5 | Existing combinations | Check the current same-environment BOSS `assetKeys` resource for an existing exact combination; when that read fails, use one current same-environment `FA_MANAGE_ASSET_KEY` setup-data export as the complete duplicate-evidence source. |
| 6 | Archive preparation | After `MAK.ENFORCE_DESIGN` passes, verify the ordered rule-result record, then obtain and inspect the task template/spec package. |
| 7 | Import route | Use the catalog-supported FSM route through core.data-loader after validation and its approval workflow. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| asset_key_system_control | Asset Key System Controls structure | Yes | Create or validate a key | Verify | Current enterprise identity and matching System Controls export | resolve_asset_key_system_control | Creation uses the System Controls-selected instance. | Resolve current System Controls export before KEY# discovery; require numeric identity only when the import contract requires it. | AssetStructureInstanceCode and contract-required identity |
| asset_key_kff_structure | KEY# structure | Yes | Create or validate a key | Verify | Current KEY# task export and the selected AssetStructureInstanceCode | discover_asset_key_kff_structure | The selected System Controls instance determines the deployed KEY# structure. | Resolve one enabled KEY# instance and its current metadata before mapping input values. | Delimiter, displayed segments, requiredness, and value sets |
| asset_key_kff_combination | KEY# combination mapping | Yes | Create or validate a key | Verify | Selected KEY# structure and supplied key code or labelled segments | resolve_asset_key_kff_combination | Creation must use the selected instance's physical mapping. | Map all supplied values to physical Segment1 through Segment10 before value-set validation. | Normalized segments and mapped value-set/value pairs |
| asset_key_segment_values | KEY# segment values | Yes | Create or validate a key | Verify | Current grouped value-set REST evidence with verified filters, pagination, visibility, and parent mapping | resolve_asset_key_segment_values | Configured segment values must be valid for the active structure. | Create or enable the exact prerequisite through Manage Fixed Assets Flexfield Value Sets, then re-verify. | ValueSetCode, Value, enabled/effective state, dependent parent |
| existing_asset_key | Existing Asset Key combination | Yes | Create, update, or delete request | Verify | Primary: complete exact BOSS Asset Keys result. Fallback: current same-target populated Asset Keys export when BOSS evidence is unavailable, incomplete, ambiguous, or lacks required fields. | resolve_existing_asset_key | Prevent duplicate creation and enforce persisted-key lifecycle boundaries. | Use an exact existing record only for date or enabled-state maintenance. | Combination identity, persisted state, enabled state, evidence source |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | All applicable mandatory dependencies resolve uniquely with current evidence. | Proceed to defaults and design validation. |
| Blocked | System Controls, structure, value, or dependent parent is absent or invalid. | Stop; use only the approved prerequisite task. |
| Ambiguous | More than one structure, mapping, or existing combination matches. | Stop for a precise business selection. |

## Value-Set Handoff Rule

When a missing or disabled KEY# segment value is delegated to Manage Fixed
Assets Flexfield Value Sets, follow that skill's scoped existing-definition
export procedure before preparing the prerequisite artifact. For a confirmed
missing segment value required by a new Asset Key, pass `EnabledFlag=Y` to the
owning Value Sets workflow. This does not change the Asset Key combination's
separate `EnabledFlag` choice. Export only the resolved `ValueSetCode`
definition; do not use an unfiltered value-set data
export for this handoff. This is the exclusive Asset Key value-set route:
do not invoke `core.fusion-api.apps-common.value-sets` from Manage Asset Keys
or accept its direct REST output as readiness evidence. The delegated workflow
must send `REST-Framework-Version: 2` and use only the `values` and
`validationTable` links returned by the matched root response. Never construct
a child URL from `ValueSetCode`, a returned identifier, or any other ID.

## Ownership Boundary

This file owns dependency availability, prerequisite handoff, continuation, and
stop conditions. `ora_reference_lookups.md` owns evidence authority, resolver
mechanics, and the mandatory delegated value-set route. Input shape and field
validation belong to `ora_input_validation.md`; defaults belong to
`ora_defaulting_rules.md`; package/design safeguards belong to
`ora_design_enforcement.md`; and disclosure, recovery, and execution-boundary
handling belong to `ora_error_handling.md`.

## Prerequisite Continuation

Persist the parent fingerprint, segments, target, requested defaults, and
recovery stage for prerequisite work. Honor existing prerequisite authorization
and ask once only when it is absent. Route only confirmed component changes
through Manage Fixed Assets Flexfield Value Sets; resolve ambiguous or
unverified evidence before proposing a change.

After verified prerequisite completion, automatically resume fresh structure,
value-set, and duplicate checks for the retained parent batch. Approval for a
prerequisite does not approve the later Asset Keys artifact or import.

For an unchanged batch, resolve each exact KEY# value set and dependent-parent
relationship once, then reuse the indexed current evidence across matching
rows. Incomplete retrieval is unverified, not missing. After a prerequisite
change, refresh the structure, all value-set evidence, and duplicate evidence
before resuming the retained parent request. Do not reuse a prior import
approval.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---:|---:|---|---|---|---|---|
| MAK.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | ready->MAK.RESOLVE_OPERATION;blocked_or_ambiguous->MAK.HANDLE_DEPENDENCY | MAK.RESOLVE_REFERENCES | stop | Evaluate applicable dependencies from current reference findings before defaults and design. |
