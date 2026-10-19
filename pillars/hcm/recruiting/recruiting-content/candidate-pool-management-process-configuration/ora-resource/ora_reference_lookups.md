# Candidate Pool Package Reference Lookups

## Required lookups

| Resolver | Required evidence | Rule |
|---|---|---|
| export_candidate_pool_task_baseline | Completed, fresh, unscoped `ORA_IRC_CANDIDATE_POOL_PROCESS_CONFIGURATION` export | Stop if the export is foreign, scoped, stale, incomplete, or missing a selected `POOL` source graph. |
| check_pool_process_code_unique | Target process code and raw exported `ORA_IRC_LC.Code` values | Reject a case-insensitive match; create-only authoring never becomes update. |
| resolve_pool_phase_route | Requested phase/state-routing input plus source Pool process route and phase identity | Require exactly one reusable Pool route and every requested state-routing fragment. |
| generate_pool_setting_identifiers | Raw exported setting and setting-item dictionaries | Generate `SETTING_CODE_` and `SETTING_ITEM_CODE_` values only after the fresh Pool export proves each prefix plus 32-uppercase-hexadecimal pattern and no collision exists. |

## Task nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| POOL.EXPORT_BASELINE | decision | 20 | reference_lookup | exported->POOL.RESOLVE_IDENTITIES;failed->POOL.HANDLE_ISSUES | POOL.VALIDATE_INPUTS | stop | Before archive construction |
| POOL.RESOLVE_IDENTITIES | decision | 30 | reference_lookup | resolved->POOL.BUILD_ARCHIVE;blocked->POOL.HANDLE_ISSUES | POOL.EXPORT_BASELINE | stop | Before generating settings or routing rows |
