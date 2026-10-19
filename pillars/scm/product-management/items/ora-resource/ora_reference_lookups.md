# Manage Lifecycle Phases Reference Lookups

## Local Lookups

| Task Code | Task Name | Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | find_valid_lifecycle_template_zip | After lifecycle-phase input fields pass validation and before import ZIP preparation | Current project workspace export directory | Select exactly one latest valid Manage Lifecycle Phases task CSV template package | template_zip_path; csv_member_name; package_metadata | No match: block import and export the template. Many matches: select the latest valid package and record its path. |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | fetch_live_lifecycle_phase_baseline | Immediately after PhaseType resolves and before proposing, defaulting, or validating PhaseSeq or PhaseCode | Run `shared.setup-export.task-level-export` for Manage Lifecycle Phases and require a fresh, successful, populated task export for this import run | Capture all existing PhaseSeq, PhaseType, and PhaseCode values from that exact export; reject cached, template-only, stale, empty, or wrong-task artifacts. This single baseline is mandatory for all subsequent sequence and code decisions. | live_baseline_export; existing_phase_sequence_type_pairs; existing_phase_codes | Missing or invalid baseline: block import. |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | find_exported_lifecycle_phase_sequence_type_pairs | Only after `fetch_live_lifecycle_phase_baseline` succeeds | The fresh live baseline and provided input records | Validate each supplied `(PhaseSeq, PhaseType)` pair against the baseline and current input. For a missing PhaseSeq, scan whole-number values 20 through 999 and allocate the lowest pair absent from the baseline and already allocated input rows; continue ascending for additional rows of the same PhaseType. Never propose a generic sequence. | existing_phase_sequence_type_pairs; available_phase_sequence | No available value, or a supplied duplicate pair: block import. A sequence used by a different PhaseType remains eligible. |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | find_exported_lifecycle_phase_codes | Only after `fetch_live_lifecycle_phase_baseline` succeeds | The fresh live baseline and provided input records | Compare codes case-insensitively against existing export rows and all current input rows. | existing_phase_codes; conflicting_phase_codes | An explicit duplicate or invalid code blocks; return derived-code collisions to the defaulting rule for suffix allocation. |

## Live Lookups

| Task Code | Task Name | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|---|
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | find_lifecycle_phase_type_standard_lookup | Before applying PhaseType to an import record | User-provided PhaseType; LookupType=EGP_LIFECYCLE_PHASES | /fscmRestApi/resources/11.13.18.05/standardLookups/EGP_LIFECYCLE_PHASES/child/lookupCodes | LookupCode; Meaning; enabled effective status | Match the supplied PhaseType exactly to one active LookupCode or Meaning | PhaseType lookup code | No match: block import and request a valid lookup value. Many matches: block import and request the exact LookupCode. |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | LCP.LOOKUP_PHASE_TYPE | decision | 2 | reference_lookup | valid->LCP.FETCH_LIVE_SEQUENCE_BASELINE;invalid->RETURN_ISSUES | LCP.VALIDATE_PROVIDED_INPUT | stop | A Manage Lifecycle Phases import is requested |
# Manage Default Item Class FSM Template Lookup

## Live Lookups

| Task Code | Task Name | Resolver | Runs When | Source Values | Service Path or URL | Query or Match Rule | Fields to Request | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|---|
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | obtain_manage_default_item_class_template | No valid task-specific template is supplied | Target FSM export/import capability and exact setup task name | TBD | Retrieve exactly one template package for Manage Default Item Class | Template package and CSV member metadata | template_package_path; csv_member_name; template_headers; package_metadata | No match: block and obtain the task template. Many matches: block until the exact current task template is identified. |

## Import Preparation Gate

Use the resolved template as the sole import-format contract. Convert the user-provided input into that template's CSV member without changing its header names, column order, package structure, or metadata. Map PhaseCode, PhaseType, PhaseName, and PhaseSeq from the reviewed DOCX to the identically named template columns; set EGP_ITEM_CLASS.ItemClassCode to ROOT_ICC and Inherited to N. Submit the reviewed, immutable package through `core.data-loader`; do not invoke an import adapter directly.
