# Input Validation

Validate the fixed Customer Hub task identity, site-only profile request, whole-task FSM archive, and exact approval before any Fusion side effect.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | operation=export, import, migrate, validate, view, manual_update, update, or status | Stop before preview or live action | Select one supported operation | Every run | |
| Fixed task identity | task_name=Manage Customer Hub Profile Options and task_code=ZCH_MANAGE_CUSTOMER_HUB_PROFILE_OPTIONS | Stop before preview | Use the enclosing catalog-backed task identity; never accept an override | Every run | |
| Fusion environment | fusion_environment_context | Stop before authentication, preview, or status lookup | Select exactly one configured target environment | Live export, import, update, or status | |
| Durable context | project_id and persisted task_context inside that project | Stop before preview | Select the implementation project and matching task context | Export, import, migrate, or status | |
| Profile request | Exact profile_option_code from the enclosing skill inventory and profile_level=SITE | Stop before view, manual guidance, preview, or update | Select one supported option and use its documented site level | View, manual_update, or update | read_customer_hub_profile_definition |
| Site value change | Current value, proposed_profile_value, profile_level_key=SITE, and enabled/updatable evidence | Stop before update preview | Read the exact definition and configured SITE record | Update | read_customer_hub_profile_definition |
| Whole-task package | setup_data_zip_path and lowercase 64-character setup_data_zip_sha256 | Stop before preview | Supply one exact-task FSM ZIP and hash its exact bytes | Validate, import, or migrate target phase | |
| Package content | One case-sensitive ASM_SETUP_CSV_METADATA.xml member and FND_APP_PROFILE_VALUE.csv when profile values change | Stop before preview | Use an FSM archive produced for this task and preserve required members | Import or migrate target phase | |
| Import approval | Approval matching Core Data Loader's exact immutable import preview and Task Hook validation envelope | Stop before import submission | Let Core Data Loader build, display, approve, and verify the import preview | Live import | |
| Direct update approval | Approval matching target environment, option code, SITE key, current value, proposed value, and guardrails | Stop before profile-value mutation | Display the exact preview and obtain fresh explicit approval | Live update | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Exact option is in the primary or guarded inventory and its definition confirms SiteLevelEnabled and SiteLevelUpdatable | Satisfied | Continue with view, guidance, or exact update preview | read_customer_hub_profile_definition |
| Requested level is product or user, or the definition is missing, ambiguous, disabled, or not updatable at SITE | Blocked | Correct the request or stop; do not choose another level | read_customer_hub_profile_definition |
| Requested value is exposed by the current definition or is one of the explicitly documented primary values | Satisfied | Preserve the value exactly in the preview | read_customer_hub_profile_definition |
| Requested value is not confirmed by documentation or the current definition | Blocked | Resolve an authoritative value; do not infer or normalize it | read_customer_hub_profile_definition |
| ZIP has a valid signature, exactly one case-sensitive ASM_SETUP_CSV_METADATA.xml, and one exact task identity | Satisfied | Preserve bytes and bind ZIP path and SHA-256 into the preview | |
| ZIP is loose CSV, changed after hashing, encrypted, ambiguous, unsafe, or has missing or mismatched metadata | Blocked | Supply a safe complete FSM archive and restart validation | |
| Preview identity, environment, artifact or change, and validation evidence match approval | Authorized | Execute once through the declared core route | |
| Any preview-bound value changes after approval | Blocked | Revalidate and obtain fresh exact approval | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Profile task membership | Reject a code outside the enclosing primary and guarded inventories; report target inventory disagreement as catalog_or_metadata_mismatch | View, manual_update, update, export validation, import, or migrate | |
| Site-only level | Require profile_level=SITE and profile_level_key=SITE; reject product and user levels | View configured value or update | read_customer_hub_profile_definition |
| Task override | Reject any task name or code other than the fixed Customer Hub profile-options task | Every run | |
| Export scope | Require a complete, unfiltered, non-template export through shared.setup-export.task-level-export | Export | |
| Documented default | Apply a documented default only when the user explicitly requests it and the current definition agrees | Default requested | read_customer_hub_profile_definition |
| Guarded option | Require its option-specific warning and current definition facts in the preview | Any guarded option explicitly listed in the task skill | read_customer_hub_profile_definition |
| ZIP signature and metadata | Require a valid ZIP, exactly one ASM_SETUP_CSV_METADATA.xml member, and one matching TaskCode | Package validation | |
| Immutable bytes | Do not extract, normalize, or repack the submitted archive after its final SHA-256 is calculated | Import validation through submission | |
| Execution ownership | Require core.fusion-api.apps-common for direct profile-value access and core.data-loader for FSM import | Live update or import | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CHP.VALIDATE_CONTEXT | step | 1 | validate_input | valid->CHP.READ_PROFILE_OPTION;invalid->CHP.ERROR | none | stop | Before operation review, immutable preview, or status continuation |
