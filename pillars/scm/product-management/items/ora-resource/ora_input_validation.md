# Manage Lifecycle Phases Import Validation

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | Lifecycle phase identity | PhaseName; PhaseCode is optional | Block import | Provide PhaseName; when PhaseCode is omitted, derive it only after the fresh live baseline is available | A Manage Lifecycle Phases import is requested | |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | Lifecycle phase type | PhaseType | Block import | Provide a PhaseType that resolves to an active standard lookup code for lookup type EGP_LIFECYCLE_PHASES | A Manage Lifecycle Phases import is requested | find_lifecycle_phase_type_standard_lookup |

## Field Validation

| Task Code | Task Name | Check | What Happens | Applies When | Resolver |
|---|---|---|---|---|---|
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | PhaseSeq range | When supplied, accept PhaseSeq only when it is a whole number from 1 through 999, inclusive; block a non-numeric, fractional, zero, negative, or out-of-range value | Only after the fresh live baseline is fetched | |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | Supplied PhaseSeq and PhaseType uniqueness | Require every supplied `(PhaseSeq, PhaseType)` pair to be unique within the provided input and absent from the same fresh live baseline; block matching pairs. A sequence used with a different PhaseType does not block the input. | Only after the fresh live baseline is fetched and before PhaseSeq defaulting | find_exported_lifecycle_phase_sequence_type_pairs |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | Resolved PhaseSeq and PhaseType validation | After defaulting, require every resolved `(PhaseSeq, PhaseType)` pair to be unique, with PhaseSeq a whole number from 1 through 999, and absent from the fresh populated base export. Recheck this pair immediately before the immutable import package is approved. | After PhaseSeq defaulting and immediately before approval | find_exported_lifecycle_phase_sequence_type_pairs |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | Fresh live baseline prerequisite | Require a fresh, populated Manage Lifecycle Phases export obtained through `shared.setup-export.task-level-export`; do not propose, default, or validate PhaseSeq or PhaseCode until it is available. Do not use a cached, template-only, or earlier workspace export. | After PhaseType resolves and before PhaseSeq or PhaseCode processing | fetch_live_lifecycle_phase_baseline |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | PhaseCode format | When supplied or derived, require 1–30 characters and only uppercase letters, numbers, and underscores (`^[A-Z0-9_]{1,30}$`). Explicit invalid codes block. | After the live baseline is fetched | find_exported_lifecycle_phase_codes |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | PhaseCode uniqueness | Require each supplied or derived code to be unique case-insensitively in both the fresh export and current input. An explicit duplicate blocks; a derived collision must be disambiguated before final validation. | After the live baseline is fetched and after defaulting | find_exported_lifecycle_phase_codes |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | PhaseName length | When supplied or derived, accept PhaseName only when it contains 1 through 80 characters | A Manage Lifecycle Phases import is requested | |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | PhaseType | Require PhaseType and accept only an active code or meaning resolved through standard lookup type EGP_LIFECYCLE_PHASES | A Manage Lifecycle Phases import is requested | find_lifecycle_phase_type_standard_lookup |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | LCP.VALIDATE_PROVIDED_INPUT | step | 1 | validate_input | valid->LCP.LOOKUP_PHASE_TYPE;invalid->RETURN_ISSUES | none | stop | Validate PhaseName and PhaseType identity before lookup; defer PhaseSeq and PhaseCode validation until the live baseline is fetched |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | LCP.FETCH_LIVE_SEQUENCE_BASELINE | decision | 3 | fetch_live_baseline | ready->LCP.DEFAULT_MISSING_VALUES;missing->RETURN_ISSUES | LCP.LOOKUP_PHASE_TYPE | stop | Require a fresh populated export through shared.setup-export.task-level-export before PhaseSeq or PhaseCode processing |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | LCP.VALIDATE_FINAL_VALUES | step | 5 | validate_input | valid->LCP.CHECK_TEMPLATE_ZIP;invalid->RETURN_ISSUES | LCP.DEFAULT_MISSING_VALUES | stop | Validate derived and supplied Manage Lifecycle Phases values after defaulting against the fresh live baseline |
# Manage Default Item Class Import Validation

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | User-provided import data | A non-empty user-provided record or table | Block import preparation | Provide the data to be converted | A Manage Default Item Class import is requested | |
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | FSM export/import template | A valid Manage Default Item Class FSM export/import template package and its CSV member | Block import preparation | Obtain the exact task template before mapping user data | A Manage Default Item Class import is requested | obtain_manage_default_item_class_template |

## Field Validation

| Task Code | Task Name | Check | What Happens | Applies When | Resolver |
|---|---|---|---|---|---|
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | Template-defined import columns and values | Compare every user-provided value to the exact column names, order, requiredness, and permitted values in the retrieved FSM template; do not add or infer fields | A valid task template is available | |
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | Import-format mapping | Map each user-provided phase to ORA_EGP_ITEM_CLASS_PHASE_ASSIGNMENT.csv: ItemClassCode=ROOT_ICC, PhaseCode=PhaseCode, PhaseType=PhaseType, PhaseName=PhaseName, PhaseSequence=PhaseSeq, and Inherited=N | A valid task template is available | |
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | Attachment-category CSV selection | Include ORA_ITEM_CLASS_ATTACH_CATEGORY.csv in the upload ZIP only when the user provides attachment categories to associate with ROOT_ICC; otherwise omit that CSV member | A valid task template is available and the upload ZIP is being prepared | |
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | Default item class code | Accept only ROOT_ICC for this task; replace an omitted value with ROOT_ICC and reject any other supplied value | A Manage Default Item Class import is requested | |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | DIC.VALIDATE_USER_INPUT | step | 1 | validate_input | valid->DIC.CHECK_FSM_TEMPLATE;invalid->RETURN_ISSUES | none | stop | A Manage Default Item Class import is requested |
