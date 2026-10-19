# Reference Lookups

## Source

- Oracle Fusion Cloud SCM, [Business Objects for Oracle Fusion Cloud SCM](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/fabsm/bo_oraScmCoreCostMgmtSetup_AnalysisCode.html)
- Approved Cost Analysis Groups parent-resolution contract.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| get_analysis_group | A child-only request is received, or the master-first fallback is selected after the live template rejects create-together code linkage | AnalysisGroupCode | `GET /fscmRestApi/resources/11.13.18.05/costAccountingCostAnalysisGroups?q=AnalysisGroupCode=<AnalysisGroupCode>` | `AnalysisGroupCode`, `analysisGroupId` | Match exactly one group whose `AnalysisGroupCode` equals the supplied value | Resolved `analysisGroupId` | No match, multiple matches, or a blank/missing `analysisGroupId` blocks the existing-master or fallback child load |
| get_cost_analysis_group_codes | A Cost Analysis Code record is added without creating the Cost Analysis Group master in the same source | Resolved `analysisGroupId`, AnalysisGroupCode | First call `get_analysis_group`; then retrieve every Cost Analysis Code in the resolved group using the registered Cost Analysis Code collection returned by the matching group response or its confirmed live metadata | AnalysisCode, analysisGroupId, defaultAnalysisCodeIndicator | Retrieve every Cost Analysis Code belonging to the one resolved parent and confirm every returned `analysisGroupId` equals the resolved parent ID | Existing Cost Analysis Code and default indicator values for exact-one-default validation | No existing Cost Analysis Codes is an empty set; a partial, unreadable, or unresolved response blocks the request |

## Execution Ownership

Execute `get_analysis_group` and `get_cost_analysis_group_codes` through
`core.fusion-api.rest-api-client`. This resource owns the read-only selection,
match, and output-mapping rules. The core client owns OAuth, GET transport,
the permitted cached-token refresh, and redacted diagnostics. Do not implement
HTTP, Authorization headers, or retry logic in this pillar resource.

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A master and children are requested together | Generate the live create template. Use one parent row plus child rows linked by the same unique `AnalysisGroupCode` when accepted. No parent lookup is required before this one-archive create. |
| A Cost Analysis Code-only load is requested | Run `get_analysis_group`, then `get_cost_analysis_group_codes`, before evaluating the default-code invariant. Build the Data Loader source with one resolved parent row plus all proposed Cost Analysis Code rows. |
| The lookup returns no match, multiple matches, or no parent ID | Stop before Data Loader artifact preparation and ask the functional user to verify `AnalysisGroupCode`. |
| The Cost Analysis Code collection cannot be resolved completely | Stop before Data Loader artifact preparation. |

For a create-together load, child source rows use the same unique
`AnalysisGroupCode` as the parent and do not require a pre-existing
`AnalysisGroupId`. For an existing master or master-first fallback, every child
source row must include the resolved `AnalysisGroupId` and the source must
include one matching parent row.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAG.RESOLVE_PARENT | decision | 2 | reference_lookup | resolved->CAG.ENFORCE_DESIGN;blocked->CAG.HANDLE_ISSUE | CAG.VALIDATE_INPUT | stop | Child analysis-code rows target an existing master, or the master-first fallback was selected after live-template validation. |
