# Offline tools

`scripts/trees.py` uses only the Python standard library (Python 3.9+ with IANA
timezone data). It has no live execution path, credential import, network client
or output-file overwrite. It prints JSON to stdout. Keep sensitive inputs and
responses outside tracked/project storage; callers own safe artifact persistence.

## Plan intake

Top-level fields: operation, object, optional environment (HTTPS origin), versions,
associations, parameters, label_definitions, item_href, describe. `describe` is
optional offline metadata evidence; generic required fields are not blindly
mapped into payloads. The planner uses the explicit contract field allowlists,
and always omits generated TreeVersionId on creates. Target describe comparison
remains a workflow prerequisite, not an automatic grant of live support.

Operations: create_tree, create_version, create_association, create_parameter,
create_label, add_node, update_tree, update_version, update_label, update_parameter.
Conditional operations emit contract_blockers and exit 2. Unsupported combinations
raise a specific gap, emit no mutations and exit 2.

`object` uses exact REST field names from contracts.md. For create_tree only,
`versions` contains version objects with optional `nodes` arrays. Versions map to
FndTreeVersionVO only; no FndTreeNode is emitted in fndTrees. Tree creation
requires at least one `parameters` item; each maps to the tree-level
FndTreeDataSourceParamsVO child and must explicitly provide DataSourceId,
ParameterId and ParameterValue. Tree-label associations are not included in
fndTrees. A node's supplied PK values are source-member values, not generated
TreeNodeIds. The planner emits a source-member validation requirement for the
existing domain resolver selected from structure/data-source evidence. A node may have a planner-only
`node_ref`; a descendant names its parent with planner-only `parent_ref`. The
planner emits one addValueTreeNode template per requested node, including roots,
plus a post-create read-back requirement keyed to the generated action result.
It resolves named version IDs after fndTrees, roots use an empty parentTreeNodeId,
and children resolve parent node IDs in dependency order. Planner references and
validation IDs are never sent as generated Fusion IDs.
For Draft version creates, ChangedSinceValidation defaults to `"Y"` when omitted,
null or blank; LevelCount and NodeCount default to 0 when omitted or null.
ChangedSinceValidation must be a one-character string, while both counts must be
non-negative integers. Valid supplied values are preserved. These fields are
included in nested and standalone create payloads but are never defaulted on PATCH.
Standalone add_node uses the action's lower-camel-case fields and an existing
resolved parent/version. Supplied TreeVersionId is removed from version creates
with a notice, regardless of describe.required declarations.

For create_tree, the plan emits parameter_validation before every external
mutation: list and paginate fndTrees for exact TreeStructureCode matches, read
each matching tree's FndTreeDataSourceParamsVO child collection, normalize the
DataSourceId/ParameterId/ParameterValue tuples, and compare complete tuple
collections.
A match proceeds, no same-structure tree records `assumed_correct`, and existing
same-structure trees with no match persist the exception artifact and block all
creates. Every supplied node gets a source_member_validation_check requiring an
existing domain resolver selected from tree structure/data-source evidence. No
resolver or an unvalidated source record blocks every mutation. After a successful
node action, node_readback_checks selects the generated-ID endpoint from the
tree structure. For the three HCM structures it emits a collection path
(positionTreeNodesLOV, departmentTreeNodesLOV or organizationTreeNodesLOV) and
`{"q":"TreeNodeId={generated_tree_node_id}"}`. fndTreeNodes retains its generic
behavior for all other structures. The check records endpoint, query string,
generated ID, returned count, HTTP result, returned identity and verification
outcome while verifying tree/version, parent, source and applicable PK values.
For the three `PER_*` structures it never falls back to fndTreeNodes. A failed
read-back is diagnostic only; a parent action that returned a resolved ID still
permits its child action. Only a failed or uncertain create action stops
dependents.
For sequenced work that supplies DataSourceId, the planner also emits a read of
the resolved tree's FndTreeDataSourceParamsVO child collection after creation.
A missing/unreadable collection or unmatched source records `assumed_correct` and
does not change the completed pre-create parameter-tuple result.

PATCH takes item_href and environment, requires a canonical same-origin item and
rejects identity changes. Validate the merged existing record before executing.
No create defaults are applied to PATCH. The planner only accepts the documented
subset: extending an allowlist requires source evidence and tests.

```bash
python3 core/fusion-api/apps-common/trees/scripts/trees.py plan --input core/fusion-api/apps-common/trees/examples/compound.json --timezone America/New_York --dry-run
python3 core/fusion-api/apps-common/trees/scripts/trees.py plan --input core/fusion-api/apps-common/trees/examples/position-compound.json --timezone America/New_York --dry-run
python3 core/fusion-api/apps-common/trees/scripts/trees.py validate --input core/fusion-api/apps-common/trees/examples/final-graph.json
```

The payload_sha256 covers the initial mutation plus every sequenced-node template
and data-source check using canonical JSON. Approval must additionally bind the
environment and prerequisites. Dates
are frozen in the plan; --as-of is fixture-only and marks the plan accordingly.
CLI exit 0 means offline operation completed, not live authorization.

## Normalized validation model

See examples/final-graph.json. Booleans are JSON true/false, not Y/N strings.
Convert authoritative exported settings explicitly; never invent absent values.
`structure`: multiple_roots, multiple_active, restrict_set, restrict_date,
labeling (None, Level, Group, Depth). `sources` maps source IDs to max_depth
(-1 unlimited), duplicates, parent_sources, leaves, ranges, use_all, all_keys.
`all_keys` must represent a complete filtered source snapshot; otherwise omit it.

`version`: id (a local symbolic version key is allowed for a proposed graph),
start/end ISO dates, status. `nodes`: id (local symbol or actual node ID), version,
source, keys (ordered tuple), parent (symbol/ID or null), exists (verified source
existence), set_id, label, label_compatible, start/end source dates, type (single,
range, reference), reference_exists where applicable. Symbolic IDs are validation
references only and are never emitted as generated Fusion IDs.

Supply the complete proposed final nodes after additions/removals, not only the
changed rows. `other_active_versions` is a complete array of other active date
intervals. Model-level set_id and evidence booleans structure_audited,
parameters_complete, source_keys_resolved and ragged_skip_valid are verified
prerequisite assertions with artifact provenance in the accompanying workflow
record. The helper cannot verify those assertions or evaluate ADF source filters.

Every applicable unknown/failure blocks validation (exit 2). It reports named
Oracle checks separately from local integrity/prerequisite checks. It never claims
to have performed an Oracle audit. Results are readiness evidence, not activation.

## Reconcile

```text
python3 core/fusion-api/apps-common/trees/scripts/trees.py reconcile --input <saved-plan.json> --response <saved-response.json>
```

Captures generated version IDs from the initial creation response and node IDs
from each addValueTreeNode response. Missing or ambiguous IDs produce
partial_or_unverified and stop the sequence. Fetch omitted children with declared
scoped reads. Repeated source tuples need extra occurrence/parent evidence; the
helper refuses to guess.
Field read-back, audit, activation and flattening remain separate checks.

Exit 1: malformed input or file error. Exit 2: contract gap, unresolved checks or
partial/unverified response. All modes reject duplicate JSON keys.
