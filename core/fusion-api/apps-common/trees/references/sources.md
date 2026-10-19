# Evidence and conflicts

Authoring review: 2026-09-13. Classification: Oracle Internal for internal-source
contract evidence; public Oracle functional guidance is identified separately.
Original files remain outside this skill. No internal URL is retained. This
register and the local contract tables contain the required extracted knowledge;
no additional internal page is needed as a bundled runtime reference PDF.

## Sources

| ID | Title / version | Local knowledge and source locator |
| --- | --- | --- |
| P1 | Trees Management - Rest Services; supplied PDF, 113 physical pages; filename export stamp 250826 (not proof of API release) | contracts.md; pp. 3–5 tree, 6–11 nested creation, 47–48 versions, 55–57 parameters/associations, 58–60 node actions, 61–70 label describe/create. Contract paths specify 11.13.18.05. |
| P2 | Trees Usecases and Respective Rest Urls; supplied PDF, 10 physical pages | contracts.md; pp. 1–4 tree, 5 associations/parameters, 6 versions, 7–8 node actions/finders, 9–10 labels. |
| I1 | Trees Management - Rest Services; revision 65, updated 2024-12-06 | Consulted during authoring; agrees with P1 nested-root example. No additional unique retained reference needed. |
| I2 | Tree Audit Validations | Consulted during research; historical rule typos superseded by current public detailed audit guidance. |
| I3 | Trees Node Operation Support and Related links | Historical navigation/active-edit note; not an executable contract. |
| I4 | Trees FAQ and Common Errors | Historical developer/database repair notes; no SaaS repair execution adopted. |
| U1 | Explicit user creation/default requirements, 2026-09-13, 2026-09-16, 2026-09-17 and 2026-09-18 conversations | trees.md, workflow and planner: generated version IDs omitted, date defaults, compound sequencing, Draft creation defaults, parameter tuple comparison, separate source-member validation, and generated-node read-back mapping. User authority, not a claim of Oracle source wording. |
| O1 | Implementing Applications, Chapter 19 Trees, 26C | trees.md functional/validation summary. 25D starting page reviewed; 26D page could not be retrieved, so 26C is latest confirmed accessible edition. |

O1 topics reviewed: Overview of Trees; Tree Structures; Guidelines for Managing
Tree Structures; Guidelines for Defining the Tree Structure; How Trees and Data
Sources Work Together; Guidelines for Specifying Data Sources for Tree Structures;
Tree Labels; Tree Nodes; Guidelines for Managing Trees and Tree Versions; Tree
Structure Audit Results; Tree Version Audit Results; Copy, Audit, and Flatten
Tree Versions Using a Scheduled Process. Full public URLs are unnecessary at
runtime; maintainer discovery can use docs.oracle.com with exact guide/topic
names and release. The release label is provenance, not a hardcoded runtime URL.

## Dispositions

| Conflict or requirement | Disposition / confidence / live prerequisite |
| --- | --- |
| TreeVersionId mandatory in generic metadata | U1 create-only exception: omit and capture response; high-confidence explicit requirement. Existing-version actions still require identity. |
| Date defaults | U1: current plan date and 4712-12-31 only when absent; high-confidence explicit requirement. No PATCH defaults. |
| Draft validation/count defaults | U1: ChangedSinceValidation defaults to `"Y"` when omitted/null/blank; LevelCount and NodeCount default to 0 when omitted/null. Values are validated and preserved on create, never defaulted on PATCH. |
| Position-tree parameters and node lookup order | U1: a tree create needs complete parameter tuples. Compare them to every existing exact-structure tree before mutation; a mismatch blocks and no tree records assumed_correct. Validate source-member keys before mutation with the applicable existing source resolver. Validate generated node IDs after successful actions with the explicit HCM/FSCM endpoint mapping, without an HCM fallback to fndTreeNodes. |
| ACTIVE/Active samples | P1 also says uppercase status; U1 defaults DRAFT. No claim REST activation audits automatically. |
| Nested payload malformed brackets | P1 pp. 10–11 supplies historic tree/version/root/association/parameter shape. U1 supersedes its node nesting: serialize only tree/Draft version in fndTrees, with parameters only when explicitly complete. |
| Nested descendants with generated parent IDs | P1 and I1 show only root, no temporary-ID or recursive mechanism. U1 requires all nodes, including roots, through addValueTreeNode after TreeVersionId resolution in parent dependency order. |
| Nested Label meaning | FndTreeLabelVO creates association with TreeLabelId, not a new fndLabels definition. Compound definition creation unresolved. |
| Repeated pk1EndValue in update action | P2's legacy sample is malformed, but target `fndTreeNodeOperations/describe` confirms `updateTreeNode` and its `parentTreeNodeId` action parameter. U1 (2026-09-22) establishes reparenting through that parameter after resolving the generated node IDs from the structure-selected LOV. Do not copy the malformed duplicate field. |
| fndLabels vs fndTreeLabels definition path | P1 label describe/create points at fndLabels, P2 creation differs. Provisional fndLabels preview only; target evidence required for execution. |
| fscmRestApi vs fndSetupApi | Requests and response links disagree. Do not follow cross-service links automatically; require target contract evidence. |
| fndLabels/fndLabels repetition | P2 singular resource reads corroborate intended resource, but base path remains subject to confirmation. No duplicated path emitted. |
| Node deletion path | P2 includes action/deleteTreeNode; P1 omits action suffix. Delete is blocked, not silently corrected. |
| Item <tree-code> | P1 responses show encoded composite keys. Use exact identity and verified canonical links, not handmade keys. |
| Parameter response fndTreeDataSources | P1 request uses fndTreeDataSourceParams; response link differs. Verify target link/resource before use; never substitute automatically. |
| Empty association/parameter update sections | No complete write contract; target evidence needed. Creation evidence exists independently. |
| Read parameter child marked Patch | P2 explicitly supplies GET; no-body read is GET, not a mutation. |
| One-root/one-active overview simplification | Detailed O1 validators condition on structure flags; those conditions govern. |
| Internal date and active-version validator typos | O1 coverage examples and detailed flags govern; do not copy historical contradictory wording. |
| Structure endpoints, exact privileges, ESS job IDs | Not established. Use the routed structure evidence or manual handoff; do not ask for privilege attestation or guess identifiers. |
| Atomicity, direct PATCH transitions, automatic audit/flattening | Not established by creation examples; separate verification/outcomes required. |

## Capability status

Offline planner, defaults, validation and ID reconciliation are executable and
tested locally. Tree/Draft-version compound creation followed by dependency-ordered
root and descendant node actions, plus standalone version/node/association/parameter operations are
available through the gated shared-client workflow, subject to target contract
and explicit approval. A Draft version may be cloned with SourceTreeVersionId;
its copied nodes can be reparented through updateTreeNode using ParentTreeNodeId
after structure-selected LOV resolution. No live Fusion behavior has been
tested. Label definitions, delete operations, structures and automated
audit/activation/flattening remain conditional or blocked as described above.
