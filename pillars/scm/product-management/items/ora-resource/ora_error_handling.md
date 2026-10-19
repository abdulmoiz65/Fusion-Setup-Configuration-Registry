# Manage Lifecycle Phases Import Gate Outcomes

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | PhaseCode and PhaseName are both missing | Return issues and stop before import ZIP preparation |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | A fresh populated Manage Lifecycle Phases export from `shared.setup-export.task-level-export` is missing, stale, empty, template-only, or for another task | Return the export prerequisite issue and stop before proposing, defaulting, or validating PhaseSeq or PhaseCode |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | PhaseSeq is non-numeric, fractional, or outside the inclusive range 1 through 999; or its resolved `(PhaseSeq, PhaseType)` pair is duplicated in the input or already present in the required fresh live baseline | Return the invalid pair and allowed range, then stop before import ZIP preparation |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | No PhaseSeq remains available from 20 through 999 | Return issues and stop before import ZIP preparation |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | An explicit PhaseCode is invalid (not 1–30 uppercase letters, numbers, or underscores) or duplicates a code case-insensitively in the fresh live baseline or current input | Return the invalid or duplicate code and stop before import ZIP preparation |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | A derived PhaseCode cannot be made unique with a `_2`, `_3`, and so on suffix within 30 characters; or PhaseName violates its length rule | Return the field and allowed length, then stop before import ZIP preparation |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | PhaseType is missing or does not resolve to an active EGP_LIFECYCLE_PHASES standard lookup code | Return the invalid PhaseType and stop before import ZIP preparation |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | No valid task CSV template ZIP is available | Return issues and stop before import ZIP preparation or import submission |

## Error Classifications

| Task Code | Task Name | Result Category | When Used | Next Action |
|---|---|---|---|---|
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | MISSING | PhaseCode and PhaseName are both absent, PhaseType is absent, the fresh live baseline is unavailable, or no PhaseSeq remains available | Provide a phase identity and PhaseType, obtain the live export, or free a PhaseSeq in the baseline, then restart validation |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | INVALID | PhaseSeq is invalid; the resolved `(PhaseSeq, PhaseType)` pair is duplicated; an explicit PhaseCode is invalid or duplicates a code case-insensitively; PhaseName length is invalid; or PhaseType is not an active lookup value | Correct the invalid pair or value, regenerate derived values if needed, and restart validation |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | RETURN_ISSUES | terminal | 7 | terminal | none | none | stop | A required import gate fails |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | RETURN_SUCCESS | terminal | 8 | terminal | none | LCP.CHECK_TEMPLATE_ZIP | stop | All required import gates pass |
# Manage Default Item Class Import Gate Outcomes

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | User-provided data is absent or cannot be mapped to the retrieved template | Return the affected values and stop before import preparation |
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | No exact FSM export/import template package is available | Return issues and stop before conversion or import submission |
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | Template retrieval or import preparation has an unresolved contract | Classify as an approval blocker and stop; do not retry a live import or invent a template mapping |

## Error Classifications

| Task Code | Task Name | Result Category | When Used | Next Action |
|---|---|---|---|---|
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | MISSING | User input or the exact task template is absent | Provide the missing input or obtain the exact task template, then restart validation |
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | APPROVAL_BLOCKER | The source, mapping, or import contract remains TBD | Resolve the task template and mapping, rebuild the immutable preview, and obtain approval before using core.data-loader |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | DIC.PREPARE_IMPORT_DATA | step | 4 | execution_gate | ready->DIC.RETURN_SUCCESS;blocked->RETURN_ISSUES | DIC.APPLY_ROOT_ITEM_CLASS | stop | A Manage Default Item Class import is requested |
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | RETURN_ISSUES | terminal | 5 | terminal | none | none | stop | A Manage Default Item Class import gate fails |
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | DIC.RETURN_SUCCESS | terminal | 6 | terminal | none | DIC.PREPARE_IMPORT_DATA | stop | User data is mapped to the reviewed template and ready for core.data-loader validation |
