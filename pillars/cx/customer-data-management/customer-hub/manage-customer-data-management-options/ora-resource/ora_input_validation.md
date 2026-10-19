# Input Validation

Validate the fixed task, closed profile-option inventory, SITE scope, stored values, and immutable FSM package before preview or execution.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | operation=export, prepare_import, import, validate, status, view, or update_one | Stop before preview or external action | Select one supported operation | Every run | |
| Fixed task identity | task_name=Manage Customer Data Management Options and task_code=ORA_ZCH_MANAGE_CUSTOMER_DATA_MANAGEMENT_OPTIONS | Stop before preview | Use the enclosing catalog-backed identity; never accept an override | Every run | |
| Fusion environment | fusion_environment_context | Stop before authentication or external action | Select exactly one configured target | Export, import, status, view, or update_one | |
| Closed option request | Exact profile code from Supported Stored Values and one requested stored value | Stop before change preview | Select one or more inventory members and their exact stored values | Prepare_import, import, view, or update_one | read_cdm_option_definition |
| SITE eligibility | LevelName=SITE, LevelValue=SITE, EnabledFlag=Y, and UpdateableFlag=Y for a change | Stop before change preview | Read the exact profile definition, level, and configured SITE value | View, prepare_import, import, or update_one | read_cdm_option_definition |
| FSM baseline | Original setup_data_zip_path and lowercase 64-character setup_data_zip_sha256 | Stop before package edit or import preview | Export the exact task and preserve its bytes | Prepare_import or import | |
| Editable package row | Existing FND_APP_PROFILE_VALUE.csv row matching exact code, application id, SITE, and SITE | Do not synthesize a row | Report export_content_discrepancy or use update_one | Prepare_import or import | read_cdm_option_definition |
| Exact approval | Approval bound to environment, task, code or ZIP hash, current value, proposed value, and validation evidence | Stop before mutation | Display a fresh exact preview and obtain approval through the selected executor | Import or update_one | |

## Supported Stored Values

| Profile Option Code | Accepted Stored Value | Validation |
|---|---|---|
| ORA_ZCQ_ENABLE_REALTIME_KEYGEN | Y or N | Require active YES_NO lookup code |
| ZCQ_BATCH_KEYGEN_NUMJOBS | Positive integer | Oracle publishes no maximum; require target acceptance |
| ZCQ_BATCH_MATCH_NUMJOBS | Positive integer | Oracle publishes no maximum; require target acceptance |
| ORA_ZCQ_MAX_CANDIDATES | Positive integer | Documented default is 20 |
| ORA_ZCQ_BATCHMATCH_DEBUG_LEVEL | DEBUG or INFO | Match exact stored token |
| ORA_ZCQ_CONVERTER_FINEST_LOGGING | Y or N | Require active YES_NO lookup code |
| ORA_ZCH_MERGE_MAX_REQUEST_LIMIT | Positive integer or blank | Documented default is 10; preserve blank exactly |
| ORA_ZCH_OPTIMIZE_LOAD | Y or N | Y is optimized; N is standard |
| ORA_ZCH_MERGE_REQUEST_BATCH_SIZE_LIMIT | Positive integer or blank | Documented default is 100; preserve blank exactly |
| ORA_ZCH_MERGE_SCOPE | ALL, CDM, CRM, or CDM_HV | Require active ORA_ZCH_MERGE_SCOPE_LOOKUP code |
| ZCH_REQUEST_NOTIFICATIONS | ORA_ZCH_NOTIFICATION_DEF_YES, ORA_ZCH_NOTIFICATION_DEF_NO, or ORA_ZCH_NOTIFICATION_DISABLED | Require active ORA_ZCH_NOTIFICATION_OPTION code |
| ZCH_AUTO_MERGE_THRESHOLD | Integer from 0 through 101 | 101 disables automerge |
| ZCA_MERGE_REQUEST | Y or N | Require active YES_NO lookup code |
| ZCH_DEDUP_REQUEST_TYPE_OPTION | MERGE, CHOICE, LINK, or LINK_DUP | Require active ZCH_DEDUP_REQUEST_TYPE_OPTION code |
| ORA_ZCH_DS_MERGE_REQUESTS | ZCH_PROCESS_WITHOUT_APPROVAL or ZCH_SUBMIT_FOR_APPROVAL | Require active ZCH_EUM_REQUEST_OPTION code |
| ZCH_USER_MERGE_REQUESTS | ZCH_PROCESS_WITHOUT_APPROVAL or ZCH_SUBMIT_FOR_APPROVAL | Require active ZCH_EUM_REQUEST_OPTION code |
| ZCH_AGREEMENT_TYPE | ORA_ZCH_DEFAULT, ORA_ZCH_GROOVY, or ORA_ZCH_RULE | Require active ORA_ZCH_AGREEMENT_LOOKUP code |
| ZCH_SETATTRIBUTE_TYPE | ORA_ZCH_NONE, ORA_ZCH_SC_OLDEST, ORA_ZCH_SC_NEWEST, or ORA_ZCH_RULE | Require active ORA_ZCH_SETATTRIBUTE_LOOKUP code |
| ZCH_ENABLE_SURVIVORSHIP | Y or N | Block N after Y has ever been enabled |
| ORA_ZCH_SETMASTER_TYPE | RULE, OLDEST, NEWEST, ANY, or ORA_ZCH_GROOVY | Require active ORA_ZCH_SETMASTER_LOOKUP code |
| ORA_ZCH_MERGE_IDENTICAL | Y or N | Require active YES_NO lookup code |
| ZCH_GROOVY_RULE | Y or N | Require active YES_NO lookup code |
| ORA_ZCH_LINK_SETMAIN_TYPE | ANY, NEWEST, OLDEST, ORA_ZCH_GROOVY, or ORA_ZCH_QUALITY_SCORE | Require active ORA_ZCH_LINK_SETMAIN_LOOKUP code |
| ZCH_AUTO_LINK_THRESHOLD | Integer from 0 through 101 | 101 disables autolink |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Exact code is in the closed inventory and live definition confirms SITE enabled and updatable | Satisfied | Continue with value validation | read_cdm_option_definition |
| Lookup-backed value resolves to one active exact lookup code | Satisfied | Preserve the stored code exactly | resolve_cdm_option_lookup_code |
| Numeric value meets the documented local shape and the live definition has no lookup contract | Satisfied | Preserve the numeric string exactly | read_cdm_option_definition |
| Definition, level, lookup code, or existing FSM row is missing or ambiguous | Blocked | Stop; do not infer a value, level, or row | read_cdm_option_definition |
| ZIP metadata and exact task identity match and the ZIP hash still matches | Satisfied | Build the immutable before/after preview | |
| Preview-bound fact changes after approval | Blocked | Revalidate and obtain fresh executor-owned approval | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Inventory membership | Reject every code outside Supported Stored Values | Every option request or changed CSV row | |
| Stored code, not display label | Reject UI text when it is not the exact accepted stored token | Every categorical change | resolve_cdm_option_lookup_code |
| SITE only | Reject product, user, or inferred levels | View, prepare_import, import, or update_one | read_cdm_option_definition |
| Existing-row edit | Change only ProfileOptionValue; preserve identity, audit columns, headers, encoding, unrelated rows, and member names | Prepare_import | |
| Blank handling | Accept blank only for the two documented job-limit options and preserve its exact exported representation | Prepare_import or update_one | read_cdm_option_definition |
| Package safety | Require one safe ASM_SETUP_CSV_METADATA.xml; reject absolute paths, traversal, encryption, duplicate members, loose CSV, and task mismatch | Prepare_import or import | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CDMO.VALIDATE_CONTEXT | step | 1 | validate_input | valid->CDMO.READ_PROFILE_OPTION;invalid->CDMO.ERROR | none | stop | Before operation review, package preview, direct-update preview, or status continuation |
