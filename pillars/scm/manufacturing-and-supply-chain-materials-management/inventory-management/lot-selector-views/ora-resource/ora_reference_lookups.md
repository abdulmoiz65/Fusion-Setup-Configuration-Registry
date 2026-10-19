# Lot Selector Views Reference Lookups

## Source Evidence

| Source | Used For |
|---|---|
| Redwood Configure Views lookup action chains | Confirms lookup types, Meaning display values, and LookupCode backend values. |
| Configured cptcyaeqy read-only verification | Confirms the complete standardLookupsLOV URL and visible LookupCode and Meaning results for both lookup types. |
| User approval | Selects both resolver contracts for task-local authoring. |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_inventory_search_view_application | Application or ApplicationCode is supplied | Application display Meaning, ApplicationCode LookupCode, or both | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?finder=LookupTypeFinder;LookupType=ORA_INV_SV_APPLICATION&onlyData=true&fields=LookupCode,Meaning | LookupCode, Meaning | Trim each supplied representation and compare case-insensitively and exactly against LookupCode and Meaning; if both are supplied, require one same returned row. | ApplicationCode: LookupCode; retain Meaning. | Stop on no match, ambiguity, or representations resolving to different rows. |
| resolve_inventory_search_view_task_flow | Task Flow or TaskFlow is supplied | Task Flow display Meaning, TaskFlow LookupCode, or both | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?finder=LookupTypeFinder;LookupType=ORA_INV_SV_TASKFLOWS&onlyData=true&fields=LookupCode,Meaning | LookupCode, Meaning | Trim each supplied representation and compare case-insensitively and exactly against LookupCode and Meaning; if both are supplied, require one same returned row. | TaskFlow: LookupCode; retain Meaning. | Stop on no match, ambiguity, or representations resolving to different rows. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A code or friendly value is supplied | Run the resolver documented for that field; validate a directly supplied code through the same resolver. |
| Lookup returns one exact row | Fill the documented canonical code and retain the returned system values. |
| Code and friendly value are both supplied | Continue only when both resolve to the same row. |
| Lookup returns no or multiple exact rows | Stop and request a valid unambiguous value; never fuzzy-match or select the first result. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LSV.RESOLVE_APPLICATION | step | 30 | reference_lookup | resolved->LSV.RESOLVE_TASK_FLOW;skipped->LSV.RESOLVE_TASK_FLOW;blocked->LSV.HANDLE_ERROR | LSV.NORMALIZE_INPUT | stop | Application or ApplicationCode is supplied. |
| LSV.RESOLVE_TASK_FLOW | step | 40 | reference_lookup | resolved->LSV.CHECK_METADATA;skipped->LSV.CHECK_METADATA;blocked->LSV.HANDLE_ERROR | LSV.RESOLVE_APPLICATION | stop | Task Flow or TaskFlow is supplied. |
