---
skill_id: "shared.implementation-planning.task-dependency-resolver"
name: "Task Dependency Resolver"
description: "Derives ordered Oracle Fusion setup-task sequences from effective catalogs and effective-catalog-validated dependency-graph enrichment for pre-release and custom tasks."
layer: "shared"
pillar: "Common"
type: "planning"
execution_mode: "assisted"
owner_team: "Shared enablement team with pillar review"
version: "0.1.4"
inputs: 
  - "implementation_objective"
  - "project_context"
  - "pillar_scope"
  - "offering_scope"
  - "functional_area_scope"
  - "catalog_sources"
  - "dependency_graph_sources"
outputs: 
  - "recommendations"
  - "work_products"
  - "review_points"
  - "token_usage_record"
  - "setup_task_sequence"
  - "sequence_diagnostics"
depends_on:
  - "router.project-objective-classifier"
uses_core:
  - "core.fusion-api.fsm-rest-client"
  - "core.project-mgmt.project-state-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.artifact-version-manager"
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
  - "design_decisions"
  - "configuration_blueprints"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/shared/implementation-planning/{skill-name}/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/shared/implementation-planning/{skill-name}/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
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

# Task Dependency Resolver

## Purpose

Provides cross-pillar task dependency resolver guidance for Oracle Fusion Cloud implementations.

## When to Use

Use this shared skill when the implementation activity applies across multiple pillars or should be standardized before being specialized by ERP, HCM, SCM, CX, or common setup areas.

Use it after `router.project-objective-classifier` has produced
`offering_scope` and `functional_area_scope` for the implementation project.

## Inputs

- `implementation_objective`
- `project_context`
- `pillar_scope`
- `offering_scope`
- `functional_area_scope`

## Outputs

- `recommendations`
- `work_products`
- `review_points`

## Setup Task Sequence Construction

Read [dependency-graph enrichment](references/dependency-graph-enrichment.md)
before constructing a sequence. The graph is an enrichment source, never a
replacement for effective catalog and never a blocking prerequisite.

1. Read the offering and functional-area short codes from the
   `offering_scope` and `functional_area_scope` outputs of
   `router.project-objective-classifier`. Validate every pair; fail closed on a
   missing or ambiguous offering/functional-area pairing.
2. Build the release-task baseline from
   `knowledge/setup-task-catalog/release/offering-functional-area-task-catalog.json`.
   Use catalog task membership and its available sequence metadata for the
   selected contexts. The release catalog is the primary source of task
   identity and task order. Retain every catalog task occurrence, including
   repeated task codes or names. Treat an occurrence as distinct by its
   offering, functional area, and stable task-list item identifier; preserve
   its own catalog sequence in `setup_task_sequence`.
3. Identify selected pre-release and custom candidates from
   `knowledge/setup-task-catalog/pre_release/setupTasks_supplement.json` and
   `knowledge/setup-task-catalog/custom/setupTasksAll.json`. Resolve their
   offering and functional-area ownership through the effective hierarchy only
   for context matching. Before a candidate can enter the task sequence,
   resolve it to exactly one valid task in
   `knowledge/setup-task-catalog/effective/setupTasksAll.json` and confirm the
   same effective offering/functional-area context. Do not silently reclassify
   or retain a task whose effective identity or ownership is absent or
   ambiguous.
4. Enrich the baseline with matching dependency-graph nodes and edges as
   described in the reference. The graph may add task membership only for
   selected pre-release/custom candidates that pass the final effective-catalog
   validation in step 4. It may add ordering and `depends_on` links for any
   selected task that resolves unambiguously to a graph node. Keep effective
   task records authoritative for task code, name, and catalog context.
5. For a valid pre-release/custom task that lacks catalog sequence
   metadata, derive its logical sequence from graph `taskCallSequence`
   `callOrder`, task-level `dependsOn`, and supported graph `depends-on` edges.
   Apply a stable topological ordering after those relationships are mapped.
   When no valid dependency information exists to resolve the missing sequence,
   place the task at the end of its containing functional area. Order multiple
   such tasks by effective task code for a deterministic fallback; do not use
   graph-file order. Assign each task a sequence number and adjust subsequent
   tasks' sequence numbers accordingly. Retain these tasks in the ordered
   `setup_task_sequence` with `sequence_source: functional_area_tail` and a
   `sequence_fallback` diagnostic recording the effective task code, source
   layer, offering and functional area, graph paths examined, and fallback
   reason. Missing sequence metadata alone must not exclude an otherwise valid
   pre-release/custom task.
6. Combine catalog and graph prerequisite relationships, then perform a
   stable topological ordering. Preserve release order for unrelated release
   tasks and graph node `callOrder` for unrelated graph-enriched tasks. Retain
   the functional-area tail placement from step 6 while respecting all valid
   prerequisite relationships. Assign consecutive positive integer `sequence`
   values from 1 across the final ordered result, renumbering subsequent tasks
   after insertions. Verify that every selected, effective-catalog-validated
   pre-release/custom task is included with a valid sequence. Preserve original
   catalog sequence values and graph ordering as provenance. Persist the
   ordered result as the `setup_task_sequence` workspace artifact at
   `project/{project_id}/artifacts/shared/implementation-planning/task-dependency-resolver/current/setup-task-sequence.json`,
   including per-task `sequence_source`, effective-catalog validation evidence,
   dependency provenance, and diagnostics. Retain repeated catalog task
   occurrences as separate sequence entries with their respective sequence
   values and stable task-list item identifiers.

If task sequence resolution fails, classify the result as a catalog mismatch or
scope-validation outcome and request scope review rather than creating a
partial release baseline. A missing, invalid, partial,
or non-matching dependency graph is not a blocker: retain the effective catalog
sequence, omit only the affected graph enrichment, and record a graph
diagnostic.

## Implementation Notes

Keep outputs reusable by pillar skills. Where the guidance depends on a specific offering, country, or release, capture that condition in the work product rather than hardcoding it in the generic shared method.
