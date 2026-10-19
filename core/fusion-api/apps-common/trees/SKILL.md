---
skill_id: "core.fusion-api.apps-common.trees"
name: "Apps Common Trees"
description: "Plan and execute controlled tree and Draft-version creation plus dependency-ordered node actions, labels and parameters for Oracle Fusion Trees."
layer: "core"
pillar: "Core"
type: "import"
execution_mode: "hybrid"
owner_team: "Central platform team"
version: "0.6.1"
inputs: ["fusion_environment_context", "project_id", "tree_request", "structure_and_source_evidence"]
outputs: ["operation_plan", "validation_result", "execution_result", "generated_id_map", "diagnostics"]
depends_on: ["core.fusion-api.rest-api-client", "core.auth.fusion-oauth-authentication"]
uses_core: ["core.fusion-api.rest-api-client", "core.auth.fusion-oauth-authentication"]
persists_project_state: true
state_updates: ["validation_results", "reports", "token_usage_records"]
workspace_outputs:
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/core/trees/{run_id}/"
    versioning_policy: "append-only"
applicability:
  industries: ["All"]
  countries: ["All"]
  fusion_releases: ["26C functional guidance; REST contract 11.13.18.05, subject to target verification"]
side_effects: ["Approved REST mutations", "Routed read-only REST calls and shared OAuth authentication", "Project run and artifact persistence"]
required_privileges: []
---

# Apps Common Trees

Reviewer: Apps Common Trees owner and Central platform REST/security reviewers.
Use through the implementation router for implementation requests. Authoring
this package does not authorize any Fusion calls.

## Purpose

Provide a controlled, project-persisted technical workflow for finding,
validating and mutating Oracle Fusion Trees through the shared REST client. The
workflow plans exact payloads, applies only established API contracts, and
records validation, generated-ID and diagnostic evidence.

## Load the applicable references

- [Contracts](references/contracts.md): resource/action selection and nested payloads.
- [Functional rules](references/trees.md): structures, sources, dates, labels and validators.
- [Workflow](references/workflow.md): prerequisites, execution gates, persistence and recovery.
- [Offline tooling](references/tooling.md): planning, validation and response reconciliation.
- [Evidence and conflicts](references/sources.md): authority, exceptions and unsupported cases.

## Mandatory behavior

1. Resolve project, environment, request and available structure/source evidence.
   No project is required merely to author this skill. Runtime durable work uses
   the selected project or the repository's draft-project convention.
2. Plan offline, then perform only the prerequisite reads declared in the
   workflow. For a tree create, supplied Data Source Parameters are required and
   must match an existing same-structure tree or receive a recorded no-tree
   assumed-correct result. Before any mutation, validate each supplied source
   member value through the relevant existing domain resolver selected from the
   tree structure and data-source evidence. Do not use `fndTreeNodes` to prove a
   proposed member exists. Missing structure metadata or an applicable resolver
   blocks dependent work; do not ask for
   advance privilege confirmation—Fusion enforces access when the request runs.
3. POST fndTrees creates only the tree, its Draft FndTreeVersionVO and the
   validated FndTreeDataSourceParamsVO collection. Never include FndTreeNode,
   including a root. Resolve TreeVersionId from that response, then add every
   requested root/child through ordered
   addValueTreeNode calls. Roots use an empty parentTreeNodeId; each child waits
   for its parent's returned TreeNodeId.
4. Omit TreeVersionId on creates even if describe marks it mandatory. Capture
   returned IDs. Default missing create dates independently to the plan's current
   date and 4712-12-31. Draft creates also default ChangedSinceValidation to Y
   and LevelCount/NodeCount to 0 under the documented omission rules. Never
   default PATCH. New versions default to DRAFT.
5. Validate the proposed final graph and structure-dependent rules. The offline
   helper is not a substitute for live prerequisite evidence or Oracle audit.
6. Persist and present exact environment, request, payload hash, defaults and
   effect before explicit approval immediately preceding mutation. Read the
   shared REST client instructions and use that client; no alternate adapter.
7. Include required supplied Data Source Parameters in the fndTrees body only
   when each has DataSourceId, ParameterId and ParameterValue, and the recorded
   pre-create comparison has matched or established assumed_correct because no
   same-structure tree exists. After each successful node action, read back the
   returned generated TreeNodeId through the endpoint selected by TreeStructureCode.
   The three HCM Tree Nodes LOV reads are collection queries with
   `q=TreeNodeId={generated_tree_node_id}`; `fndTreeNodes` retains its generic
   behavior for other structures. Verify its version, parent, source and
   PK values. A failed read-back records a verification diagnostic without
   retrying the successful action or stopping known-successful dependencies.
   Reconcile response/read-back identities and effects; persist partial results.
   Audit, activation and flattening are separate outcomes and currently manual
   handoffs, not implied REST success.

## Preflight

Before a live call, validate the offline plan, resolved environment, exact
identities, structure/source evidence, parameter comparison, source-member
checks, target contract, final graph and durable artifact destination. Present
the immutable request payload and operation plan, then obtain explicit approval
immediately before the first mutation. A missing, ambiguous or unpersistable
preflight result blocks the affected operation.
8. To roll forward a Draft version while retaining its graph, create the new
   version with SourceTreeVersionId. For a reparent request, resolve the copied
   node and copied destination-parent generated IDs through the structure-selected
   lookup, then call updateTreeNode with parentTreeNodeId. The HCM LOV result
   must be scoped to the requested tree/version; a business-object ID can occur
   in more than one tree/version. Do not use fndTreeNodes for these three HCM
   structures.

## Errors and recovery

Apply [workflow failure handling](references/workflow.md#failure-handling).
Classify failures, redact sensitive details, preserve successful IDs, and stop
on uncertain mutation outcomes. No automatic destructive rollback or mutation
transport retry. The shared client's one cache-auth retry must be included in
execution approval; do not add another retry loop.

## Offline quick start

From repository root:

```bash
python3 core/fusion-api/apps-common/trees/scripts/trees.py plan --input core/fusion-api/apps-common/trees/examples/compound.json --timezone America/New_York --dry-run
python3 -m unittest discover -s core/fusion-api/apps-common/trees/tests -v
```

The helper has no live mode, credential imports or HTTP implementation. The
skill executes approved calls through the existing core client as documented.
