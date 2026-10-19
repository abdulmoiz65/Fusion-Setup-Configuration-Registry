# Reporting Hierarchy Generation Input Validation

Source: [Oracle Reporting Hierarchy Generation](https://docs.oracle.com/en/cloud/saas/sales/fauss/reporting-hierarchy-generation.html).

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Tree Code discovery | Tree Structure Code only; `submit` omitted or `false` | Block | Collect the Tree Structure Code only. Do not collect or bind a Tree Version ID. | Every Tree Code discovery request |  |
| Tree Version discovery | Tree Structure Code and Tree Code; no Tree Version ID; `submit` omitted or `false` | Block | Collect the Tree Structure Code and Tree Code only. Do not collect or bind a Tree Version ID. | Every Tree Version discovery request |  |
| Submission parameters | `submit=true` plus Tree Structure Code, Tree Code, and Tree Version ID supplied together in the current execution request, or carried together from one verified Manage Resources CX Import handoff | Block | For a direct submission, collect all three values and explicit submit intent. For a verified handoff, use only its exact carried triple and do not request the values again. | Every scheduled-process request |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Submit intent | Accept `submit=true` only when all three ESS business values are present. Omitted or `false` is read-only and cannot transition to ESS submission. | Every request |  |
| Tree Structure Code | Accept only RESOURCE_ORG_TREE_STRUCTURE or PARTNER_ORG_TREE_STRUCTURE. Require it for discovery and submission; accept an exact verified ResourceUser CX Import completion handoff for `submit=true`. | Every request |  |
| Tree Code | Do not require it for Tree Code discovery. Require GLOBAL_SALES_MARKETING for an internal direct Tree Version discovery or `submit=true` request, or a non-empty caller-confirmed partner tree code. A verified ResourceUser CX Import completion handoff supplies its exact carried code. The submit path requires a later exact-pair `fndTrees` lookup. | Tree Version discovery or `submit=true` | reporting_hierarchy_tree |
| Tree Version ID | Do not accept or bind it for discovery. Require a non-empty direct value or carried handoff value for `submit=true`. A later `fndTreeVersions` validation lookup must return exactly one matching TreeVersionId. Display its Status, EffectiveStartDate, and EffectiveEndDate and classify it as FUTURE, INACTIVE, or ACTIVE. Require explicit confirmation only for an `INACTIVE` submit value. | `submit=true` | reporting_hierarchy_tree_version |
| ESS parameter binding | Use submit.argument1, submit.argument2, and submit.argument3 as STRING in that order only for `submit=true`; do not use scheduled-process display labels as REST parameter names. | All submit business values are present |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RH.VALIDATE | decision | 1 | validate_input | tree-structure-only->RH.TREE_CODE_DISCOVERY;tree-code-provided->RH.TREE_VERSION_DISCOVERY;explicit-submit->RH.TREE_LOOKUP;invalid->RETURN_ISSUES | none | stop | A Reporting Hierarchy Generation request is received. |
