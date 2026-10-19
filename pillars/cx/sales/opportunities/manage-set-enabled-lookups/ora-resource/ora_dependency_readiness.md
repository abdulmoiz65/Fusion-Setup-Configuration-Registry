# Manage Set Enabled Lookups Dependency and Package Readiness

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

Treat parent metadata, reference-set assignment, fresh export evidence, package
shape, row state, and execution ownership as mandatory route-aware
dependencies. This task doesn't create record-set assignments and doesn't
select or bypass a Core Data Loader execution adapter.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Exact target/task identity and persisted Data Loader task context | Bind one target environment/release to FND_MANAGE_SET_ENABLED_LOOKUPS and exact TaskName; retain persisted TaskContextPath plus positive TaskSequence resolved to the exact skill path, TaskCode, TaskName, offering, and functional area for the persisted Data Loader task context |
| 2 | Parent reference group | Resolve every affected lookup parent and preserve its returned nonblank ReferenceGroupName |
| 3 | Reference set and current state | Resolve every selected or changed row's exact set with the returned reference group, any requested business-unit assignment, and current code state |
| 4 | Fresh baseline | For Package Import or FSM Create, Update, or Disable, require a successful fresh same-target, same-release export of FND_MANAGE_SET_ENABLED_LOOKUPS |
| 5 | Package contract | Preserve exact ASM metadata, declared member paths, member names, header spelling and order, safe ZIP shape, and unrelated content |
| 6 | Row delta, impact, and state locks | Validate every changed row independently and prove the final package contains only reviewed Create, Update, or Disable changes |
| 7 | Immutable Data Loader handoff | Reopen the final ZIP, bind PackagePath and PackageSha256 to the task identity and persisted Data Loader task context and proposed delta, and let Core Data Loader own Task Hook validation, preview, standalone approval, upload, and accepted initiation |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| set_lookup_task_context | Exact target, FND task identity, and persisted Data Loader task context | Yes | Every Core Data Loader mutation handoff | Verify | Configured environment, setup-task catalog, and persisted project context |  | Prevent cross-environment or wrong-task execution by requiring exact context resolution | Select one target and exact task; supply persisted TaskContextPath, exact TaskName, and positive TaskSequence resolved to the exact skill path, TaskCode, offering, and functional area | Environment, release, SkillPath, TaskCode, TaskName, TaskContextPath, TaskSequence, Offering, FunctionalArea |
| set_lookup_parent_metadata | Current lookup parent metadata | Yes | Every lookup, export, package, or preview | Lookup | Apps Common set-enabled lookup parent GET | resolve_set_enabled_lookup_parent | Business-unit assignments are keyed by the parent's returned reference group, not an assumed lookup-type value | Resolve each affected parent and require nonblank ReferenceGroupName | Per-type parent identity, ReferenceGroupName, parent link, lookup timestamp |
| set_lookup_reference_scope | Explicit set decision, exact sets, and record-set assignments | Yes | Every request except Package Export with no row scope | Lookup | Explicit user choice plus Apps Common set and business-unit assignment GETs | resolve_lookup_reference_set | Set-enabled codes must remain in an exact set and requested BU assignments must already exist; Common Set is never inferred | Confirm Common Set or supply a different exact Set ID/Set Code per single request; preserve exported set identity for existing package rows and require an explicit choice for each new row | SetSelectionDecision, LookupType, ReferenceGroupName, SetId, SetCode, optional BUOrgId, prerequisite status |
| set_lookup_fresh_export | Fresh task baseline | Yes | Package Import or FSM Create, Update, or Disable | Blocked until verified | Completed shared.setup-export.task-level-export result and retained ZIP | verify_set_lookup_package_readiness | The exact current task contract and rows must anchor package authoring and state comparison | Export FND_MANAGE_SET_ENABLED_LOOKUPS again when target, release, task, state, or freshness can't be proven | ExportProcessId, target, release, task identity, completed status, ExportedAt, baseline path, baseline SHA-256 |
| set_lookup_package_contract | Exact baseline and final package contract | Yes | Package Import or FSM Create, Update, or Disable | Blocked until verified | Fresh baseline, final immutable ZIP, ASM_SETUP_CSV_METADATA.xml, and CSV members | verify_set_lookup_package_readiness | Prevent guessed members, normalized headers, unsafe ZIPs, task mismatch, or unrelated edits | Preserve metadata, members, headers, header order, unrelated rows, and baseline bytes outside the reviewed delta | Baseline and final member inventories, metadata identity, header fingerprints, row counts, PackagePath, PackageSha256 |
| set_lookup_row_delta | Per-row type, set, state lock, delta, and impact | Yes | Package Import or FSM Create, Update, or Disable | Blocked until every row passes | Baseline rows, fresh parent/set/code GET evidence, proposed package rows, and business review | verify_set_lookup_package_readiness | A combined package is safe only when every changed row is independently valid and reviewed | Correct every invalid row; don't submit a partial package or include a named-task lookup type | Per-row operation, LookupType, ReferenceGroupName, SetId, SetCode, LookupCode, before state or absent-create lock, after state, impact, lookup timestamp |
| set_lookup_loader_handoff | Immutable Core Data Loader handoff | Yes | FSM Create, Update, Disable, or Package Import ready for execution | Ready only for Data Loader preview | Final reopened ZIP, exact task identity, and persisted Data Loader task context | verify_set_lookup_package_readiness | Data Loader owns Task Hook validation, upload approval, routing, upload, initiation, and accepted-result reporting | Hand off PackagePath, PackageSha256, task identity, persisted Data Loader task context, delta, locks, and impact; wait for Data Loader's lifecycle | PackagePath, PackageSha256, task identity, persisted Data Loader task context, later Data Loader evidence and handoff status |

## Package Readiness Rules

| Check | Ready Condition | Blocked Condition |
|---|---|---|
| Target and freshness | Export is completed, retrievable, and demonstrably from the exact target, release, task, and current workflow; its baseline hasn't been superseded by a changed target or state lock | Wrong or ambiguous target/release/task, incomplete or failed export, unavailable bytes, or stale/unproven baseline |
| ZIP safety and metadata | Baseline and final ZIPs are readable and unencrypted with no unsafe or duplicate paths; each has exactly one case-sensitive ASM_SETUP_CSV_METADATA.xml member and exactly one FND_MANAGE_SET_ENABLED_LOOKUPS task identity | Unsafe, encrypted, corrupt, ambiguous, missing, duplicate, or wrong-task metadata |
| Members and headers | Final member inventory, logical paths, filenames, header spelling, and header order match the fresh export and its metadata exactly | Invented, missing, extra, renamed, or normalized member or header |
| Row scope | Every changed row belongs to MOO_SETID_ASSESS_OVRRIDE_RSN or MOO_SETID_REVN_CATEGORY; unchanged and unrelated rows are preserved byte-semantically | Named-task type, unknown type, unreviewed row, dropped unrelated row, or unexplained difference |
| Row operation | Each changed row is Create, Update, or Disable; Create proves absence, Update has an exact mutable delta, and Disable changes only EnabledFlag to N | Delete, silent upsert, duplicate Create, missing existing row, unsupported field, or operation/state mismatch |
| Per-row set and state lock | Parent ReferenceGroupName is returned and nonblank, every new row has an explicit set decision, set resolves exactly with that value, any requested BU assignment exists, and fresh current state matches the recorded lock immediately before handoff | Missing set choice, inferred Common Set, assumed reference group, unresolved set/assignment, stale state, ambiguous code, or before-state mismatch |
| Business impact | Every changed row records owner, intended use, historical-use assessment, affected Opportunity or Revenue behavior, and downstream consumer review | Missing, partial, or conflicting impact evidence |
| Immutable final artifact | Reopened final bytes reproduce PackageSha256 and match the exact task identity and persisted Data Loader task context, member/header receipt, row delta, state locks, and Data Loader handoff values | Artifact or context changes, hash mismatch, Task Hook archive mismatch, or stale approval |

Package readiness ends at an immutable handoff to Core Data Loader. Data Loader
must create its own Task Hook validation envelope and immutable upload preview.
After Data Loader's later contextual approval, an accepted initiation response is terminal
for that request; status, ProcessLog, and live verification require a later
explicit request.

## Dependency Classification

| Result Category | When Used | Can Continue? |
|---|---|---|
| Satisfied | All dependencies applicable to the selected read, REST, or Export route are verified | Yes |
| Ready for Data Loader preview | The exact package and handoff evidence pass, but Data Loader hasn't yet completed its preview and later approval | Handoff only; no upload authorization |
| Lookup | A documented read-only resolver must determine parent, set, assignment, or state | Read only until exact evidence returns |
| Blocked | Required identity, assignment, export, package, row, impact, state-lock, or hash evidence is absent or inconsistent, or a later Data Loader stage lacks the Task Hook or approval evidence that stage owns | No |

## Recovery and Fallback Readiness

| Check | Ready Condition | Blocked Condition |
|---|---|---|
| Omitted parent linkage | Completed full-data exact-task export may omit seeded rows; each reviewed child joins an existing exported or freshly resolved unchanged parent support row, with exact SetCode and preserved unrelated data | Invalid/template export, missing or conflicting live parent, child-only package, guessed schema/set, or unrelated row changes |
| Final CSV exhaustion | Applicable recovery is exhausted with a classified same-target receipt; every prior submitted import is terminal, fully diagnosed and every requested row unchanged or Create-absent | Repairable CSV, missing workflow/context/approval/auth/catalog/set facts, explicit FSM-only scope, unknown submissions, pending import, partial effects or concurrent state changes |
| REST_FALLBACK | Bypass native ZIP/context readiness only as fallback_candidate to verify_set_lookup_rest_fallback; fresh parent/set/state reads and unchanged intent still required | An arbitrary missing ZIP/context is treated as eligibility or export/Data Loader approval is reused |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.SET_LOOKUP.DEPENDENCY | step | 5 | resolve_dependency | satisfied->OPP.SET_LOOKUP.DESIGN;loader_preview_ready->OPP.SET_LOOKUP.DESIGN;fallback_required->OPP.SET_LOOKUP.RETURN_FALLBACK_REQUIRED;fallback_candidate->OPP.SET_LOOKUP.VERIFY_FALLBACK;missing->OPP.SET_LOOKUP.RETURN_MISSING;blocked->OPP.SET_LOOKUP.RETURN_MISSING;failed->OPP.SET_LOOKUP.RETURN_FAILED | OPP.SET_LOOKUP.RESOLVE_PARENT | stop | Validate route-specific exact task, parent/set/row state, impact and native immutable package, including omitted-parent recovery. Documented final CSV exhaustion alone returns fallback_required. REST_FALLBACK returns fallback_candidate to its dedicated verifier without ZIP/context; Export/Import stay FSM-only |
