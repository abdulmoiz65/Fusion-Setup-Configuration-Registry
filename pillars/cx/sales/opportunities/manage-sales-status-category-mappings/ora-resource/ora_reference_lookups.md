# Manage Sales Status Category Mappings Package Resolver

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

Use this local resolver to inspect the retained fresh export and final package.
It performs no Fusion mutation and grants no upload approval.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| verify_status_category_mapping_package_readiness | A reviewed status-category mapping reaches immutable-package readiness | Exact target/release/task identity; completed export receipt; baseline and final ZIP paths and SHA-256 values; `TaskCode`; `TaskName`; ASM metadata; member inventories; exact headers; baseline and final mapping rows; reviewed row delta; immediate pre-handoff state evidence; persisted Data Loader task context and its resolved identities | Require one fresh completed export for exact `MOO_MANAGE_SALES_STATUS_CATEGORY_MAPPINGS` target/release and exact task name; require persisted Data Loader task context; validate safe ASM metadata, export-derived members/headers, reviewed four-flag delta/state lock, unchanged unrelated content, and reopened SHA-256 | Export receipt; task-context receipt; ASM identity; member/header receipt; row counts; exact category; before/after flags; reviewed delta; state-lock result; unrelated-content receipt; `PackagePath`; `PackageSha256`; `PackageValidationResult`; `HandoffStatus=READY_FOR_DATA_LOADER` | Stop on missing, ambiguous, stale, wrong-target/release/task, inconsistent persisted Data Loader task context, unsafe ZIP, structural difference, state drift, unrelated change, or hash mismatch; never hand-author or synthesize task context, repair the ZIP, request child approval, or submit a partial package |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| All readiness evidence matches one immutable package | Return the package receipt to `OPP.STATUS_MAPPING.PACKAGE`; handoff remains unapproved until Data Loader creates its own preview and later receives standalone `approve` |
| The final package changes after validation | Invalidate readiness, reopen and revalidate the new bytes, and require Data Loader to create a new preview after handoff |
| Export, package, task identity and persisted Data Loader task context, delta, or state evidence is missing or inconsistent | Return `MISSING`, `BLOCKED`, or `FAILED` with the exact discrepancy and no handoff |
