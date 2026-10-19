# Manage Sales Methods and Sales Stages Package Lookups

## FSM Task Identity Policy

Require exact task code/name, selected task `SKILL.md`, target environment, and
immutable archive SHA-256 throughout review, export, package preparation, and
validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  `TaskCode`, `TaskName`, offering, and functional area.

The persisted context may come from a project setup-task plan without creating
an Oracle Run Book. Never hand-author, infer, or synthesize it solely to satisfy
Data Loader.

Use the fresh exact-task export as the baseline authority and reopen the final
immutable package before Core Data Loader handoff. This local resolver performs
no Fusion mutation and creates no approval.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| verify_sales_methods_final_package | The design is reviewed and a final FSM package is ready for executable handoff | Explicit SetSelectionDecision, with user-confirmed Common Set or a different exact SetId/SetCode; exact target and release; MOO_MANAGE_SALES_METHODS_AND_SALES_STAGES export receipt; fixed TaskCode and exact TaskName; selected skill path; persisted TaskContextPath and positive TaskSequence; final package path and recorded SHA-256; ASM metadata; exported and final members and headers; reviewed method and stage delta; latest current-state lock; dependency and unrelated-row preservation evidence | Require explicit user confirmation for Common Set or one different exact set identity; never derive Common Set from a product default or absent selector. Then require a fresh completed exact-target, exact-release, exact-task export; reopen the final immutable ZIP; require TaskName equal to Manage Sales Methods and Sales Stages, exactly one ASM ObjectShortName equal to MOO_MANAGE_SALES_METHODS_AND_SALES_STAGES, the complete exported member graph, exact filename/header spelling and order, only the reviewed method/stage delta, nonblank PhaseCd on every stage, unique nonblank StageNumber on create rows, unchanged current-state lock, preserved dependency and unrelated rows, and a recomputed SHA-256 equal to the recorded value. Resolve the persisted project context and require it to match the selected skill path, TaskCode, TaskName, offering, and functional area | Executable package receipt containing SetSelectionDecision, SetId, SetCode, target, release, skill path, TaskCode, TaskName, TaskContextPath, TaskSequence, resolved context identities, baseline export identity, ASM ObjectShortName identity, member/header fingerprints, reviewed delta, state lock, preservation result, immutable final path, reopened SHA-256, and handoff-ready status | Stop when set choice is missing or Common Set was inferred, or on any stale, cross-target, wrong-release, wrong-task, task-context, ASM, member, header, row, PhaseCd, StageNumber, delta, state-lock, preservation, path, or hash mismatch; never hand-author or synthesize task context, repair, partially hand off, or request child approval |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Final package passes every exact baseline, task-context, shape, row, lock, preservation, and hash check | Return handoff-ready evidence to the execution gate; Core Data Loader owns Task Hook preview and later standalone approve |
| Final package task identity differs from the fresh baseline, or persisted task context is missing or inconsistent | Stop before handoff and rebuild from a fresh exact-task export or refresh the project planning artifacts; never hand-author context values |
| SetId/SetCode is malformed, conflicts with the explicit decision or fresh baseline, confirmed Common Set maps to a non-Common set, or the package row uses another environment's set | Stop before handoff, disclose the sanitized set mismatch, and require a corrected explicit choice and rebuilt exact-target package; never substitute a set |
| The final ZIP changes after validation | Invalidate the receipt and reopened SHA-256; rerun the package-readiness resolver |
