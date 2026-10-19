# Manage Lifecycle Phases Template Package Readiness

## Required Dependency Order

| Task Code | Task Name | Sequence | Dependency | What Must Happen |
|---|---|---|---|---|
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | 3 | Fresh populated live lifecycle-phase export | After PhaseType resolves, run `shared.setup-export.task-level-export` for Manage Lifecycle Phases and require a fresh successful populated export before proposing, defaulting, or validating PhaseSeq or PhaseCode |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | 6 | Valid task CSV template ZIP | Resolve a valid Manage Lifecycle Phases template package before preparing or submitting an import ZIP |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | lcp_live_sequence_baseline | Fresh populated Manage Lifecycle Phases export | Yes | Immediately after PhaseType resolves and before PhaseSeq or PhaseCode is proposed, defaulted, or validated | Verify | A new `shared.setup-export.task-level-export` result for the exact Manage Lifecycle Phases task | fetch_live_lifecycle_phase_baseline | It is the authoritative current source for PhaseSeq/PhaseType pairs and PhaseCode uniqueness | Run the task-level export and wait for a successful populated result; do not reuse a cached, template-only, stale, or wrong-task export | export_receipt; live_baseline_export; existing_phase_sequence_type_pairs; existing_phase_codes |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | lcp_template_zip | Valid task CSV template ZIP | Yes | After lifecycle-phase values pass final validation and before import ZIP preparation | Verify | Current project workspace export directory | find_valid_lifecycle_template_zip | The template defines the valid CSV member name, column order, and package metadata | Export the Manage Lifecycle Phases template, then retry preparation | template_zip_path; csv_member_name; package_metadata |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|---|
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | Satisfied | A valid template ZIP is found | Yes |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | Satisfied | A fresh populated live baseline is found for this import run | Yes |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | Blocked | The live baseline is missing, stale, empty, template-only, or for another task; or no valid template ZIP is found | No |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | LCP.FETCH_LIVE_SEQUENCE_BASELINE | decision | 3 | fetch_live_baseline | ready->LCP.DEFAULT_MISSING_VALUES;missing->RETURN_ISSUES | LCP.LOOKUP_PHASE_TYPE | stop | Require a fresh populated live export through shared.setup-export.task-level-export before PhaseSeq or PhaseCode processing |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | LCP.CHECK_TEMPLATE_ZIP | decision | 6 | resolve_dependency | valid->RETURN_SUCCESS;missing->RETURN_ISSUES | LCP.VALIDATE_FINAL_VALUES | stop | A Manage Lifecycle Phases import is requested |
# Manage Default Item Class Template Package Readiness

## Required Dependency Order

| Task Code | Task Name | Sequence | Dependency | What Must Happen |
|---|---|---|---|---|
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | 2 | Valid FSM export/import template | Obtain the exact Manage Default Item Class template package before converting input or submitting an import |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | default_item_class_fsm_template | Valid Manage Default Item Class FSM export/import template | Yes | After user input passes validation and before conversion to import data | Verify | Downloaded task-specific FSM template package under project/default-item-class-test/exports | obtain_manage_default_item_class_template | The template defines the CSV member, headers, column order, and required import format | Download or provide the exact task template, then restart conversion | template_package_path; csv_member_name; template_headers; package_metadata |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|---|
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | Satisfied | A valid task-specific FSM template package is available | Yes |
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | Blocked | The template package is missing, ambiguous, or does not identify this setup task | No |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | DIC.CHECK_FSM_TEMPLATE | decision | 2 | resolve_dependency | valid->DIC.APPLY_ROOT_ITEM_CLASS;missing->RETURN_ISSUES | DIC.VALIDATE_USER_INPUT | stop | A Manage Default Item Class import is requested |
