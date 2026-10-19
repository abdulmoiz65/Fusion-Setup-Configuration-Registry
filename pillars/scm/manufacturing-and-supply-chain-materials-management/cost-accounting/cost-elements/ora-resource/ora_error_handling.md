# Error Handling

## Source

- Oracle Fusion Cloud SCM, [Manage Cost Elements and Analysis Groups](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/manage-cost-elements-and-analysis-groups.html)
- Oracle Fusion Cloud SCM, [How Cost Components, Cost Elements, and Cost Component Groups Work Together](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/how-cost-components-cost-elements-and-cost-component-groups-work.html)

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required Cost Element fields are missing | Stop and request only the missing CostElementCode, Cost Element Type meaning, or Cost Element Set name. CostElementDescription is optional. |
| Cost Element Type lookup is no-match, ambiguous, or returns an excluded code | Stop; request an eligible CST_COST_ELEMENT_TYPES Meaning. Do not accept a supplied LookupCode. |
| Fusion reports that Cost Element Type is invalid | Correct the parent rows so CostElementType contains the uniquely resolved CST_COST_ELEMENT_TYPES LookupCode, not the user-supplied display Meaning; revalidate before a new approval and upload. |
| Cost Element Set lookup is no-match or ambiguous | Stop; request a unique existing Cost Element Set name. |
| Profit In Inventory lacks a uniquely resolved Inventory Organization | Stop; request a corrected Inventory Organization name. |
| Profit In Inventory does not use the Common Cost Element Set | Stop; resolve and select Common before preview. |
| Analysis Group or Analysis Code is not already present | Stop; create the prerequisite separately and retry only after it exists. |
| Analysis Group and Analysis Code mapping is duplicated | Stop; do not create a duplicate mapping for the Cost Element. |
| A child association add uses RestAction CREATE or MERGE | Stop; regenerate the child row with RestAction POST. |
| Fusion reports an orphan Cost Element Analysis Group child or missing PARENT key | Classify as a payload-contract failure. For a combined create, regenerate the single DAT with matching parent and child CostElementCode and CostElementSetId; do not supply a guessed CostElementId. For an existing parent, use its exact resolved CostElementId in an association-only DAT. |
| A child association removal has no exact ElementAnalysisGroupId | Stop; read the nested child collection and resolve one existing mapping before preparing RestAction DELETE. |
| A request changes an existing Cost Element code, type, or Cost Element Set | Stop; these parent values are immutable after creation. Create a suitable separate Cost Element if a different value is needed. |
| An Analysis Group association is edited or removed while the parent is referenced by a Cost Component Group or Cost Profile | Continue with the child-mapping change; do not treat the parent reference as a blocker. |
| Fusion rejects a parent Cost Element delete because of child mappings, references, or usage | Retain the Cost Element and disclose the Fusion dependency error; do not retry automatically. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required Cost Element values are missing or an arbitrary CostElementType code is supplied | Correct the input, then revalidate. |
| Reference lookup | A type, set, or conditional organization does not resolve uniquely | Correct the display value, then revalidate. |
| Dependency readiness | An Analysis Group or Analysis Code prerequisite is absent | Complete the prerequisite setup separately. |
| Child mapping resolution | A requested association removal has zero or multiple matching child rows | Correct the association selection and resolve exactly one ElementAnalysisGroupId. |
| Design enforcement | Profit In Inventory does not use the Common Cost Element Set, or an association duplicates an existing Analysis Group and Analysis Code mapping | Correct the set or association before preview. |
| Immutable parent attribute | A request changes an existing Cost Element code, type, or Cost Element Set | Keep the immutable parent values and create a separate Cost Element when needed. |
| Fusion parent deletion | Fusion rejects the parent delete because of child mappings, references, or usage | Retain the Cost Element and resolve the returned dependency error before a new request. |
| Parent-child payload contract | A combined create emits a child without the parent alternate key | Correct the parent and child values, then regenerate and revalidate through core.data-loader. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Lookup failure | The user-supplied display value, matching count category, and correction required; never expose a selected first result. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Type, set, or organization resolution is incomplete | Do not invent, fuzzy-match, or use a first result for LookupCode, SetId, or OrganizationId. |
| Analysis prerequisite is absent | Do not create the Analysis Group or Analysis Code as part of this workflow. |
| A child association add uses CREATE or MERGE | Do not upload or initiate; prepare a new child row using POST. |
| An association removal has no unique ElementAnalysisGroupId | Do not use AnalysisGroupCode or AnalysisCode as a substitute delete key. |
| Profit In Inventory is not in the Common Cost Element Set | Do not prepare a payload or preview. |
| A request changes CostElementCode, CostElementType, or CostElementSetId after creation | Do not prepare an update payload for those immutable parent values. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCE.READY_FOR_DATA_LOADER | terminal | 7 | terminal | none | CCE.PREVIEW_GATE | stop | All validation, lookup, dependency, and design gates pass; hand off to core.data-loader preview |
| CCE.HANDLE_ISSUE | step | 8 | error_handler | disclosed->RETURN_ISSUES | none | stop | A prior node reports invalid, blocked, or failed |
| RETURN_ISSUES | terminal | 9 | terminal | none | CCE.HANDLE_ISSUE | stop | Error disclosure is complete |
