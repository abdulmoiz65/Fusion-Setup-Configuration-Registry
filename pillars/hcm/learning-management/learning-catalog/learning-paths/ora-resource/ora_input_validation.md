# Learning Paths Input Validation

Sources: OLC-116681 FDD v5 section OLC-120244 and the supplied raw
learningPaths Describe, reviewed 2026-09-22.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Request identity | target environment; requested operation; row identifier | Stop the affected row before preview | Supply one exact environment, operation, and row identity | All requests | |
| Path definition | learningItemNumber; title; ownership when applicable; visibility; lifecycle intent; validity and renewal values when supplied | Return row-specific missing fields | Complete the minimum parent definition | Create or parent update | |
| Empty Draft intent | explicit emptyDraftRequested value | Require an explicit choice | Confirm whether an empty Draft is intended or provide a section/activity manifest | Create without sections or activities | |
| Section and activity manifest | section number and status; section order and completion rule; activity number; elearn identifier or number; activity order, format, status, and section membership | Stop only the affected path group | Correct the grouped manifest; new or replaced activities also require authoritative eligibility evidence | Structure is supplied or activation is requested | |
| Dependency graph | section and activity display predecessors; completion-access predecessors | Stop graph validation for the affected path | Supply exact predecessor references from the same grouped manifest | Any predecessor is requested | resolve_learning_path_existing_graph |
| Existing path identity | exact learningItemNumber preferred, or learningItemId; current-state fingerprint | Stop the affected row before change | Resolve one exact path and follow its returned item link | Duplicate check, non-create operation, or reconciliation | resolve_learning_path_identity |
| Extensible attributes | WLF_LEARNING_ITEM or WLF_LI_SPECIALIZATION context plus target-confirmed segments | Stop extensibility processing | Refresh target metadata and resolve every supplied segment and value | DFF values are supplied | |
| Approval evidence | immutable grouped manifest and preview fingerprint with fresh explicit approval | Stop before mutation | Refresh all applicable evidence and obtain approval for the exact valid rows | Any live mutation | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A new or replaced activity lacks authoritative eligibility or relationship evidence | Blocked for that row | Preserve unaffected rows; obtain an approved catalog-item resolver before this activity mutation | |
| A dependency edge is dangling, self-referential, duplicated, or cyclic | Invalid | Correct the grouped graph and rebuild the preview | resolve_learning_path_existing_graph |
| An explicitly requested empty Draft has no sections or activities | Valid structure exception | Continue with parent Draft validation; activation remains blocked | |
| Activation has no complete section and activity structure | Invalid | Add and validate a non-empty structure before approval | |
| Existing graph, usage, path, or activity state changed after preview | Stale | Refresh evidence, rebuild the grouped manifest and preview, and obtain new approval | resolve_learning_path_existing_graph |
| A documented change request remains nonterminal | Pending | Poll only its processing status and process identifier within the timeout | resolve_learning_path_change_request |
| Activation or retirement is requested | Lookup required | Resolve an enabled status and an FDD-valid current-to-target transition | resolve_learning_path_lifecycle_values |
| Parent deletion is requested | Usage evidence required | Prove deletion safety from current where-used, metrics, assignments, and learner impact | resolve_learning_path_existing_graph |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Path number is present and unique | Reject missing values and exact-number collisions | Create | resolve_learning_path_identity |
| Rows for one path are grouped before validation | Reject cross-path section, activity, or predecessor references | Multi-row input | |
| Section and activity identities are unique within the grouped path | Reject duplicate or unowned entries | Structure is supplied | |
| Every predecessor target exists in the same approved manifest | Reject dangling references | Graph changes | |
| Display and completion-access graphs are acyclic | Reject direct and indirect cycles, including self-reference | Graph validation | |
| Validity, renewal, due, and reassignment values are internally compatible | Reject incomplete or incompatible combinations | Validity or renewal is configured | |
| Draft and activation are separate | Never treat create or update as implicit activation | Create, update, or activate | |
| Operation is supported | Permit create, update, status PATCH, parent/section/nested-activity delete, and section/nested-activity create or update; reject copy and user-facing upsert | Any mutation | |
| Approved row selection is unchanged | Invalidate approval when a row is corrected, excluded, added, removed, regrouped, or reordered | After preview | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LPT.VALIDATE_INPUT | decision | 1 | validate_input | valid->LPT.CHECK_DEPENDENCIES;invalid->LPT.HANDLE_ERROR | none | stop | One or more Learning Paths rows are normalized |
| LPT.EVALUATE_RESULT | decision | 7 | evaluate_result | verified->LPT.RETURN_SUCCESS;issues->LPT.HANDLE_ERROR | LPT.EXECUTION_GATE | stop | Validation or mutation evidence is reconciled with the approved rows, manifest, and preview |
