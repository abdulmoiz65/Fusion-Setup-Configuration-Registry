# API contracts and operation matrix

All paths below are relative to the configured Fusion origin. The contract prefix
is `/fscmRestApi/resources/11.13.18.05/` (not the documentation release number).
Ordinary resources use JSON Accept/Content-Type. Node actions use
`application/vnd.oracle.adf.action+json` Content-Type and
`application/vnd.oracle.adf.actionresult+json` Accept.

This is a conservative writable subset from the supplied contracts, not a claim
that every metadata attribute can be changed. `scripts/trees.py` rejects unknown
fields. Obtain target metadata through the workflow before mutation. A missing
or ambiguous contract is a blocker; describe-required TreeVersionId on create
is the explicit user exception.

| Operation | Method and suffix | Writable fields / response | Prerequisite and verification |
| --- | --- | --- | --- |
| Create tree | POST fndTrees | TreeStructureCode, TreeCode, TreeName, Draft FndTreeVersionVO, and required explicit FndTreeDataSourceParamsVO tuples. Draft versions include ChangedSinceValidation, LevelCount and NodeCount after defaulting/validation. Response tree identity and version IDs. | Before POST, match normalized parameter tuples against existing same-structure tree children; resolve every returned TreeVersionId before any node action. |
| Create version | POST fndTreeVersions | TreeStructureCode, TreeCode, TreeVersionName, dates, DRAFT, ChangedSinceValidation, LevelCount and NodeCount; optional Description. Returned TreeVersionId. | Existing tree or compound create; omit generated ID; verify name, dates, status and returned values. |
| Add single node | POST fndTreeNodeOperations/action/addValueTreeNode | treeStructureCode, treeCode, treeVersionId, parentTreeNodeId, dataSourceId, pk1Value…pk5Value. Result is generated node ID. | Before POST, validate supplied source member keys through the applicable existing domain resolver selected from tree structure/data-source evidence. After POST, use the structure-selected generated-ID read-back endpoint. |
| Create association | POST fndTreeLabels | TreeStructureCode, TreeCode, DataSourceId, TreeLabelId. | Existing compatible label definition; verify association. |
| Create parameter | POST fndTreeDataSourceParams | TreeStructureCode, TreeCode, DataSourceId, ParameterId, ParameterValue. | Registered source parameter/type; read value back. |
| Create label definition | POST fndLabels (provisional) | TreeStructureCode, DataSourceId, LabelName, LabelShortName, dates, optional Description/SetId; returned LabelId. | Base-path conflict: require target contract confirmation before execution; verify label. |
| Update tree | PATCH canonical fndTrees item | TreeName, Description, SetId after evidence of mutability. | Resolve full identity, preview old/new values and dependency impact; read back. |
| Update version | PATCH canonical fndTreeVersions item | TreeVersionName, Description, dates; DRAFT only with evidence of transition. | Merge existing dates before validation; no date defaults; re-audit needed. |
| Update definition/parameter | PATCH canonical item | Definition name/short name/description/dates/set; parameter value. | Incomplete/conflicting contract: target writable evidence required; blocked until supplied. |
| Reparent or update a node | POST fndTreeNodeOperations/action/updateTreeNode | treeStructureCode, treeCode, treeVersionId, treeNodeId and ParentTreeNodeId; include dataSourceId and source-key fields only when the target action metadata or requested change requires them. | Resolve the generated node and destination-parent IDs through the structure-selected node lookup; verify the new parent through that same lookup. |
| Delete node | POST .../action/deleteTreeNode in usecase PDF | treeStructureCode, treeCode, treeVersionId, treeNodeId. | Blocked conflicting path; explicit destructive scope and target evidence needed. |
| Copy version and reparent a node | POST fndTreeVersions with SourceTreeVersionId, then POST fndTreeNodeOperations/action/updateTreeNode | The new Draft version includes SourceTreeVersionId; updateTreeNode supplies the copied node and copied destination-parent IDs. | Resolve copied node IDs from the applicable HCM LOV for PER_POS/PER_DEPT/PER_ORG, scoped to the created tree/version; verify the final parent there. |
| Audit/activate/flatten | No established REST/ESS route | See functional handoff. | Never imply success from HTTP creation. |

## Tree and version creation

The management PDF physical pages 10–11 establishes this shape:

```json
{
  "TreeStructureCode": "SYNTHETIC_STRUCTURE",
  "TreeCode": "DEMO_TREE",
  "TreeName": "Demo tree",
  "FndTreeVersionVO": [{
    "TreeStructureCode": "SYNTHETIC_STRUCTURE",
    "TreeCode": "DEMO_TREE",
    "TreeVersionName": "DEMO_VERSION",
    "Status": "DRAFT",
    "EffectiveStartDate": "2026-09-13",
    "EffectiveEndDate": "4712-12-31",
    "ChangedSinceValidation": "Y",
    "LevelCount": 0,
    "NodeCount": 0
  }],
  "FndTreeDataSourceParamsVO": [{
    "DataSourceId": "SYNTHETIC_SOURCE",
    "ParameterId": "SYNTHETIC_PARAMETER",
    "ParameterValue": "SYNTHETIC_VALUE"
  }]
}
```

The date above is a fixture, never a runtime default. The planner deliberately
does not include `FndTreeNode` in any fndTrees payload, even though the historic
example contains one. POST fndTrees creates only tree and Draft version(s), then
every requested node uses addValueTreeNode after TreeVersionId is resolved. A
root sends `parentTreeNodeId: ""`; a child sends its resolved parent TreeNodeId.
Wait for every node response before materializing a dependent child. Multiple
roots still require the applicable structure setting.

Omit unrequested optional arrays. Include FndTreeDataSourceParamsVO only when
DataSourceId, ParameterId and ParameterValue are explicitly provided and valid;
tree creation requires at least one such tuple. Do not
include FndTreeLabelVO in fndTrees creation; create associations separately.
Do not invent a version just to populate an optional array; report a tree-only
create as incomplete lifecycle setup until a version exists. Omit TreeVersionId;
never manufacture TreeNodeId. For Draft version creates, include the validated
ChangedSinceValidation/LevelCount/NodeCount values derived by the planner. Do
not add other sample derived/read-only fields such as Depth or ChildCount unless
target create metadata provides an explicit valid create contract and values. Do
not treat business source keys as generated TreeNodeIds.

FndTreeLabelVO associates a label; it does not create a definition with LabelName
or LabelShortName. New definitions in a compound request remain an explicit gap.
All parent bindings, including roots, use the documented sequenced
addValueTreeNode route after generated version IDs are resolved.
A single HTTP mutation has no established atomicity guarantee in these sources.

## Pre-mutation reads

For a tree create, list and fully paginate fndTrees, filter exact
TreeStructureCode matches, then read each resolved item's
`child/FndTreeDataSourceParamsVO`. Compare normalized complete parameter tuples:
DataSourceId, ParameterId, ParameterValue. A matching collection proceeds; no
same-structure trees produces an assumed_correct artifact; a same-structure
result without a match produces an exception diagnostic and stops.

For every requested node, validate the supplied source member PK values before
POST through the relevant existing domain resolver selected using structure and
DataSourceId evidence. The resolver must be able to establish the source record's
existence; do not infer an endpoint from a value's format. Missing source routing
or an unresolved record blocks mutation. After a node action succeeds, substitute
its returned generated TreeNodeId in this exact read-back mapping and compare the
returned tree/version, parent, source and all applicable PK values:

| TreeStructureCode | Post-create validation request |
| --- | --- |
| `PER_POS_TREE_STRUCTURE` | `GET /hcmRestApi/resources/11.13.18.05/positionTreeNodesLOV` with `{"q":"TreeNodeId={generated_tree_node_id}"}` |
| `PER_DEPT_TREE_STRUCTURE` | `GET /hcmRestApi/resources/11.13.18.05/departmentTreeNodesLOV` with `{"q":"TreeNodeId={generated_tree_node_id}"}` |
| `PER_ORG_TREE_STRUCTURE` | `GET /hcmRestApi/resources/11.13.18.05/organizationTreeNodesLOV` with `{"q":"TreeNodeId={generated_tree_node_id}"}` |
| Any other structure | `/fscmRestApi/resources/11.13.18.05/fndTreeNodes/{TreeNodeId}` |

There is no fndTreeNodes fallback for the three `PER_*` structures. Record the
selected endpoint, query string, generated ID, returned count, HTTP result,
returned identity and verification outcome. The HCM collection query must return
exactly one record with the generated TreeNodeId. A read-back failure is a
verification diagnostic: do not replay the
node action and do not stop a dependent action whose parent create result is
known. A failed or uncertain create result still stops dependents.

## Reads and identity

GET collections: fndTrees, fndTreeVersions, fndTreeNodes, fndTreeLabels,
fndTreeDataSourceParams, fndLabels. GET `resource/describe` verifies advertised
fields/actions, not permissions or behavioral correctness. An empty describe
response is not proof of support. fndLabels retains its base-path verification gap.

Documented finder names (case-sensitive):

| Resource | finder value |
| --- | --- |
| fndTreeVersions | AllVersionsRowFinder;TreeCode=…,TreeStructureCode=… |
| fndTreeNodes | TreeVersionIdRowFinder;TreeVersionId=… |
| fndTreeNodes | TSCodeAndTCodeRowFinder;TreeCode=…,TreeStructureCode=… |
| fndTreeNodes | Pk1StartValueRowFinder;Pk1StartValue=… (also Pk2 through Pk5) |
| fndTreeLabels | DataSourceBasedTreeLabelRowFinder;DataSourceId=…,TreeCode=…,TreeStructureCode=… |
| fndTreeDataSourceParams | TreeDataSourceParamsRowFinder;DataSourceId=…,TreeCode=…,TreeStructureCode=… |
| fndLabels | TreeStructureCodeRowFinder;TreeStructureCode=… |

Pass finder strings through repeated shared-client --query arguments, not shell
interpolation. Reject unresolved reserved finder delimiters until escaping is
confirmed. Page using limit/offset and hasMore, with a finite page budget; an
incomplete scan cannot establish absence or uniqueness. Use collection results
and exact full identity matches; a prefix result is insufficient. Never use a
business code as a URL item key simply because an example says <tree-code>.

Use canonical/self item links only after same-origin and expected resource-path
validation. Reject credentials, redirects to other origins, unsafe paths and
unexpected base-path changes. Follow documented children of the resolved tree:
`child/FndTreeVersionVO`, `child/FndTreeLabelVO`,
`child/FndTreeDataSourceParamsVO`; nodes under the resolved version use
`child/FndTreeNode`. Response links may disagree with historical request paths;
record the disagreement rather than following a different service automatically.
