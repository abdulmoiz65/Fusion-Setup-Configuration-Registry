# Reporting Hierarchy Generation Reference Lookups

Source: Manage Resources Reporting Hierarchy Generation runtime-readiness guidance and [Oracle Reporting Hierarchy Generation](https://docs.oracle.com/en/cloud/saas/sales/fauss/reporting-hierarchy-generation.html).

## REST Header Requirement

Every lookup in this file must be delegated through
`core.fusion-api.rest-api-client` with:

```text
REST-Framework-Version: 9
```

The header applies to every page of a paginated lookup. Preserve the core
client's OAuth authorization and `Accept` headers.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| reporting_hierarchy_tree_codes | A user asks for valid Tree Codes before submitting | Current-request TreeStructureCode | /fscmRestApi/resources/11.13.18.05/fndTreeVersions?q=TreeStructureCode='<tree_structure_code>' | TreeCode, TreeVersionId, Status, EffectiveStartDate, EffectiveEndDate | Retrieve every page, discard blank TreeCode values, and deduplicate exact TreeCode values. | Tree Code candidates only | Return an empty candidate list when no valid Tree Code is returned. Do not infer, select, or bind a Tree Code or Tree Version ID. |
| reporting_hierarchy_tree_version_candidates | A user asks for valid Tree Version IDs after selecting a Tree Code | Current-request TreeStructureCode and TreeCode | /fscmRestApi/resources/11.13.18.05/fndTreeVersions?q=TreeStructureCode='<tree_structure_code>' AND TreeCode='<tree_code>' | TreeVersionId, Status, EffectiveStartDate, EffectiveEndDate | Retrieve every page and return every nonblank TreeVersionId with its status, dates, and calculated classification. | Tree Version candidates and candidate-selection status | Return an empty candidate list when no version is returned. Label a sole current-effective candidate as recommended, but do not select, retain, or submit it. |
| reporting_hierarchy_tree | Before ESS submission for every new request | Current-request TreeStructureCode and TreeCode | /fscmRestApi/resources/11.13.18.05/fndTrees?q=TreeStructureCode='<tree_structure_code>' AND TreeCode='<tree_code>' | TreeStructureCode, TreeCode | At least one returned row must exactly match both current-request values. | Validated Tree Structure Code and Tree Code | Stop ESS submission and report the lookup result. Do not infer, default, or substitute a tree code. |
| reporting_hierarchy_tree_version | After the Tree Code check and before ESS submission | Current-request TreeStructureCode, TreeCode, and TreeVersionId | /fscmRestApi/resources/11.13.18.05/fndTreeVersions?q=TreeStructureCode='<tree_structure_code>' AND TreeCode='<tree_code>' | TreeVersionId, Status, EffectiveStartDate, EffectiveEndDate | Exactly one returned TreeVersionId must equal the supplied TreeVersionId. Classify it as FUTURE when EffectiveStartDate is after the current validation date; INACTIVE only when both EffectiveStartDate and EffectiveEndDate are before it; ACTIVE otherwise. | Validated Tree Version ID, Status, EffectiveStartDate, EffectiveEndDate, and ACTIVE/FUTURE/INACTIVE classification | Stop and report the lookup result when no exact version matches. Always display the status and dates. Require explicit confirmation only when the calculated classification is INACTIVE. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The Tree Code lookup is requested | Use the configured Fusion connection's `fndTrees` REST resource with the supplied TreeStructureCode and TreeCode. Accept only an exact pair match in the response. |
| Tree Code discovery is requested | Use `fndTreeVersions` with only the supplied TreeStructureCode. Follow every response page, deduplicate returned nonblank TreeCode values, and present Tree Codes only. Do not show, select, or save Tree Version IDs. |
| Tree Version discovery is requested | Use `fndTreeVersions` with the supplied TreeStructureCode and TreeCode. Follow every response page and present each returned TreeVersionId with Status, EffectiveStartDate, EffectiveEndDate, and calculated classification. A recommendation is informational only and is not a submission value. |
| The Tree Code lookup returns no exact match | Stop before ESS submission and report that the supplied Tree Code is not valid for the supplied Tree Structure Code. |
| The Tree Code lookup fails or returns an incomplete response | Stop before ESS submission and report the lookup outcome; do not treat it as a valid tree. |
| The Tree Version lookup is requested | Query `fndTreeVersions` through the configured Fusion connection using the supplied TreeStructureCode and TreeCode, then compare returned TreeVersionId values with the supplied TreeVersionId. Display Status, EffectiveStartDate, and EffectiveEndDate for the exact match. |
| The Tree Version lookup returns no exact version match | Stop before ESS submission and report that the supplied Tree Version ID is not valid for the selected Tree Structure Code and Tree Code. |
| The exact Tree Version is active | Classify as ACTIVE when EffectiveStartDate is on/before the current validation date and EffectiveEndDate is blank or on/after it. Display the Fusion Status separately. The final execution approval must confirm all three submitted parameter values. |
| The exact Tree Version is future | Classify as FUTURE when EffectiveStartDate is after the current validation date. Report Status, EffectiveStartDate, and EffectiveEndDate, then continue to the final approval gate. |
| The exact Tree Version is inactive | Classify as INACTIVE only when both EffectiveStartDate and EffectiveEndDate are before the current validation date. Report Status, EffectiveStartDate, EffectiveEndDate, and the ended-effective-period condition; require explicit confirmation to use it. The final execution approval must still confirm all three submitted parameter values. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver | Request Path or URL |
|---|---|---|---|---|---|---|---|---|---|
| RH.TREE_CODE_DISCOVERY | decision | 2 | reference_lookup | resolved->RH.DONE_TREE_CODE_DISCOVERY;unresolved->RETURN_ISSUES | RH.VALIDATE | stop | The user asks for valid Tree Codes and supplies a Tree Structure Code. | reporting_hierarchy_tree_codes | /fscmRestApi/resources/11.13.18.05/fndTreeVersions?q=TreeStructureCode='<tree_structure_code>' |
| RH.TREE_VERSION_DISCOVERY | decision | 3 | reference_lookup | resolved->RH.DONE_TREE_VERSION_DISCOVERY;unresolved->RETURN_ISSUES | RH.VALIDATE | stop | The user asks for valid Tree Version IDs and supplies a Tree Structure Code and Tree Code. | reporting_hierarchy_tree_version_candidates | /fscmRestApi/resources/11.13.18.05/fndTreeVersions?q=TreeStructureCode='<tree_structure_code>' AND TreeCode='<tree_code>' |
| RH.TREE_LOOKUP | decision | 4 | reference_lookup | resolved->RH.TREE_VERSION_LOOKUP;unresolved->RETURN_ISSUES | RH.VALIDATE | stop | The current Tree Structure Code and Tree Code require configured-connection validation before ESS submission. | reporting_hierarchy_tree | /fscmRestApi/resources/11.13.18.05/fndTrees?q=TreeStructureCode='<tree_structure_code>' AND TreeCode='<tree_code>' |
| RH.TREE_VERSION_LOOKUP | decision | 5 | reference_lookup | active->RH.DEPENDENCIES;future->RH.DEPENDENCIES;inactive-confirmed->RH.DEPENDENCIES;inactive-unconfirmed->RETURN_ISSUES;unresolved->RETURN_ISSUES | RH.TREE_LOOKUP | stop | The current Tree Version ID requires configured-connection validation before ESS submission. | reporting_hierarchy_tree_version | /fscmRestApi/resources/11.13.18.05/fndTreeVersions?q=TreeStructureCode='<tree_structure_code>' AND TreeCode='<tree_code>' |
