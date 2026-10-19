# Manage Opportunity Revenue Categories Dependency Readiness

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

Treat the task export, immutable ZIP, and current-state evidence as mandatory
local package dependencies. This child validates them but does not create a
Data Loader preview, request approval, upload, or initiate an import.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
| --- | --- | --- |
| 1 | Fresh task baseline | Obtain a completed MOO_MANAGE_REVENUE_CATEGORIES export from the exact target and Fusion release |
| 2 | Exact task identity and persisted Data Loader task context | Bind TaskName Manage Opportunity Revenue Categories and TaskCode MOO_MANAGE_REVENUE_CATEGORIES; bind persisted TaskContextPath plus positive TaskSequence resolved to the exact skill path, TaskCode, TaskName, offering, and functional area for the persisted Data Loader task context |
| 3 | Package contract | Validate exactly one ASM_SETUP_CSV_METADATA.xml task identity plus the baseline's metadata-derived members, headers, header order, and safe ZIP shape |
| 4 | Standard-lookup parent-child closure | When changed child rows exist, require exactly one current MOO_REVN_CATEGORY parent carrier row in FND_APP_STANDARD_LOOKUP.csv and require every ORA_FND_APP_STANDARD_LOOKUP_CODE.csv row to reference it exactly |
| 5 | Reviewed change set | For every changed MOO_REVN_CATEGORY child row, validate operation, code, before-state or absent-create lock, minimal delta, and business impact while preserving all unrelated content and leaving the parent business metadata unchanged |
| 6 | Immutable final artifact | Reopen the final ZIP, recompute SHA-256, and require exact agreement with PackagePath, PackageSha256, task identity and persisted Data Loader task context, parent-child closure, and the reviewed change set |

## Package Readiness Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Blocking Condition | Values to Fill |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| revenue_category_fresh_export | Fresh exact-task export | Yes | SingleLookup Create, Update, or Disable; Package Import | Blocked until verified | Completed shared.setup-export.task-level-export result and retained baseline ZIP | verify_revenue_category_fsm_package | Export is missing, failed, incomplete, stale, cross-target, cross-release, or not exactly MOO_MANAGE_REVENUE_CATEGORIES | ExportProcessId, environment identity, FusionRelease, TaskCode, completed status, ExportedAt, BaselinePath, BaselineSha256 |
| revenue_category_task_context | Exact task identity and persisted Data Loader task context | Yes | SingleLookup Create, Update, or Disable; Package Import | Verify | Catalog-fixed task identity and persisted project context | verify_revenue_category_fsm_package | Prevent wrong-task execution by requiring exact context resolution | SkillPath, TaskCode, TaskName, TaskContextPath, TaskSequence, Offering, FunctionalArea |
| revenue_category_package_contract | Exact baseline and final ZIP contract with parent-child closure | Yes | SingleLookup Create, Update, or Disable; Package Import | Blocked until verified | Baseline and final ZIPs, ASM_SETUP_CSV_METADATA.xml, metadata-derived CSV members, and fresh verify_revenue_category_lookup_type evidence | verify_revenue_category_fsm_package | ZIP is unreadable, encrypted, path-unsafe, contains duplicate or unexpected ASM identity, changes required members or exact headers/order, has changed child rows with a header-only, missing, duplicate, stale, or mismatched MOO_REVN_CATEGORY parent row, has a child whose parent key differs, or cannot prove preservation | ASM identity, baseline/final member inventories, header fingerprints, parent and child row counts, ParentChildClosureVerified, parent state fingerprint, preservation receipt |
| revenue_category_row_delta | Reviewed standard-lookup row delta | Yes | SingleLookup Create, Update, or Disable; Package Import | Blocked until every row passes | Baseline rows, fresh exact Apps Common GET evidence, proposed final rows, and business review | verify_revenue_category_fsm_package | A changed row is not MOO_REVN_CATEGORY, has an unsupported operation or field, lacks exact code and state lock, conflicts with live state, lacks impact, or changes unrelated content | Per-row operation, LookupCode, before or absent state, after state, mutable delta, impact, lookup timestamp, preservation evidence |
| revenue_category_final_hash | Reopened immutable final ZIP | Yes | SingleLookup Create, Update, or Disable; Package Import | Blocked until verified | Final PackagePath reopened after authoring and hashed without mutation | verify_revenue_category_fsm_package | Recomputed SHA-256 differs from PackageSha256, the path or bytes changed, or the hash is not bound to the exact reviewed context | PackagePath, PackageSha256, recomputed SHA-256, validation timestamp |
| revenue_category_export_baseline | Completed full-task Export baseline | Yes | Package Export | Blocked until verified | Completed shared.setup-export.task-level-export result and retained ZIP | verify_revenue_category_fsm_package | Export is narrowed by LookupCode or row scope, is incomplete or failed, or target/release/task identity does not match | Exact target, FusionRelease, TaskCode, completed status, BaselinePath, BaselineSha256, members, headers |

## Atomic Verification Contract

- `SingleLookup` Create, Update, or Disable requires exactly one changed row
  matching the resolved LookupCode and fresh state.
- `Package` Import validates every changed row; one invalid row blocks the
  entire package, and no valid subset may be handed off under the same hash.
- Create requires a fresh exact absence lock. Update and Disable require one
  exact existing-state lock; Disable changes only `EnabledFlag` to `N`.
- A final package with changed child-code rows must contain exactly one
  `FND_APP_STANDARD_LOOKUP.csv` row for `MOO_REVN_CATEGORY`. Populate its
  business metadata from the fresh exact parent read, keep its system-audit
  fields blank, and require every child row's parent key to match it. Treat the
  parent as a required linkage carrier, not as a requested parent mutation.
- Preserve ASM metadata, member names, headers and order, unchanged rows, and
  all unrelated bytes or canonical row content outside the reviewed delta.
- Data Loader binds `finalData.archiveSha256` only after handoff when it creates
  its own Task Hook preview. Missing Data Loader approval before that preview is
  expected and is not a package-readiness blocker.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.REVENUE_CATEGORY.VERIFY_PACKAGE | step | 5 | resolve_dependency | ready->OPP.REVENUE_CATEGORY.DESIGN;not_applicable->OPP.REVENUE_CATEGORY.DESIGN;missing->OPP.REVENUE_CATEGORY.RETURN_MISSING;failed->OPP.REVENUE_CATEGORY.RETURN_FAILED | OPP.REVENUE_CATEGORY.LOOKUP_CODE | stop | Validate a complete full-task Export baseline, exactly one SingleLookup Create/Update/Disable row, or every changed Package Import row; Read is not_applicable |
