---
skill_id: "router.project-objective-classifier"
name: "Project Objective Classifier"
description: "Classifies an implementation objective by pillar, offering, functional area, scope, geography, and delivery phase, with dependency-graph scope enrichment for pre-release and custom contexts."
layer: "router"
pillar: "Router"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "Central architecture or platform team"
version: "0.1.2"
inputs: 
  - "implementation_objective"
  - "business_requirements"
  - "project_scope"
  - "effective_offering_catalog"
  - "pre_release_catalogs"
  - "custom_catalogs"
  - "dependency_graph_sources"
outputs: 
  - "objective_classification"
  - "pillar_scope"
  - "offering_scope"
  - "functional_area_scope"
  - "dependent_task_scope"
  - "scope_diagnostics"
  - "token_usage_record"
uses_core:
  - "core.project-mgmt.project-state-manager"
  - "core.project-mgmt.artifact-registry-manager"
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
  - "objective"
  - "scope"
  - "skill_path"
workspace_outputs:
  - artifact_type: "objective"
    default_location: "project/{project_id}/artifacts/router/project-objective-classifier/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "scope"
    default_location: "project/{project_id}/artifacts/router/project-objective-classifier/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
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

# Project Objective Classifier

## Purpose

Classifies an implementation objective by pillar, offering, functional area, scope, geography, and delivery phase.

## When to Use

Use this router skill at the start of an implementation workflow or whenever the current workflow state must be reclassified, resequenced, or routed to the next responsible skill.

## Inputs

- `implementation_objective`
- `business_requirements`
- `project_scope`

## Outputs

- `objective_classification`
- `pillar_scope`
- `offering_scope`
- `functional_area_scope`

## Implementation Notes

Keep routing decisions explainable. Persist the selected skill IDs, confidence,
assumptions, catalog evidence, and human review points so downstream skills can
continue from the same context.

## Offering-Scope Resolution

For every classification, load the complete `offerings` object from
`knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`.
This effective catalog is authoritative for offering-scope resolution; do not
derive candidates from a release, pre-release, custom, or pillar catalog in
isolation.

Resolve `offering_scope` as follows:

1. Enumerate all effective offerings and match an explicitly supplied offering
   short code exactly. If a display name is supplied instead, match its
   normalized name exactly after case and whitespace normalization.
2. When the request supplies a functional-area short code, retain only
   offerings whose `functionalAreas` object contains that exact code.
3. When pillar scope is known, retain only offerings whose ownership is
   confirmed by `knowledge/setup-task-catalog/effective/pillars-offerings-mapping.json`.
4. Treat the remaining offering as resolved only when exactly one candidate
   remains. Do not select an offering based on a partial name, keyword match,
   or the functional area alone when it belongs to multiple offerings.
5. If there are no candidates or multiple candidates, persist the candidate
   codes and catalog path in the scope artifact, set `offering_scope` to
   pending, and ask for an offering short code or sufficient business context.

The scope artifact must record the resolved offering short code and display
name, the functional-area and pillar filters applied, the candidate offering
codes considered, the effective catalog path, confidence, assumptions, and any
required human review. Downstream skills must consume these resolved short
codes rather than re-resolving display names.

## Pre-Release and Custom Scope Enrichment

The effective catalog remains the authority for resolved offering and
functional-area identity. After resolving those contexts, determine whether
each selected offering or functional area is sourced from either of these
layers:

- `knowledge/setup-task-catalog/pre_release/`
- `knowledge/setup-task-catalog/custom/`

For a selected context with either provenance, read the applicable graphs under
`knowledge/dependency-graphs/` and derive the graph's in-scope dependent setup
tasks. Add a graph-derived task to `dependent_task_scope` only after it
resolves to exactly one valid task in
`knowledge/setup-task-catalog/effective/setupTasksAll.json` and that task is
present in the same resolved effective offering/functional-area context. A
graph node, label, edge, or source-layer task is never sufficient by itself.

Apply this process as follows:

1. Resolve a graph task ID as `task:<task-code>` by its suffix. For any other
   ID, require an exact match to one effective task code or task name; do not
   use fuzzy or label-only matching.
2. Follow only supported `depends-on` edges and only when the source task is in
   the selected context. Treat their targets as candidate dependent tasks.
3. Validate every candidate against the effective task catalog and effective
   hierarchy before adding it to scope. De-duplicate by effective task code.
4. Record each added task's graph path, node/edge identity, source provenance,
   and effective-catalog resolution evidence. Record invalid, ambiguous,
   out-of-scope, and missing graph candidates in `scope_diagnostics` and omit
   them from scope.

Dependency-graph enrichment is additive only: it cannot remove an explicitly
selected task, replace resolved offering or functional-area ownership, or turn
an unresolved offering scope into a resolved one. Missing or partial graphs do
not block classification; persist the diagnostic and require human review when
the dependent scope cannot be established.

## Preflight and Error Handling

Before persisting classification output, preflight the objective inputs, the
effective catalog, the selected pre-release/custom source catalogs, and every
selected dependency-graph path. Confirm that each graph task candidate can be
matched to one effective task and one resolved offering/functional-area context.
This classifier performs no Fusion calls or mutations.

Fail closed on ambiguous offering, functional-area, task, or graph-node
resolution. Classify such outcomes as `input_validation` or
`catalog_or_metadata_mismatch`, omit the unresolved dependent task, and persist
a diagnostic with the source path, candidate identities, and recommended human
review. Treat unreadable graphs or artifact-write failures as
`artifact_persistence` diagnostics; retain safe partial classification output
only when it clearly identifies what was not enriched. Do not retry malformed
catalog or graph input.

Diagnostics and scope artifacts must redact credentials, access tokens, token
caches, private keys, and customer-sensitive configuration values. Record only
catalog paths, stable task identifiers, graph node/edge identities, and safe
resolution evidence.
