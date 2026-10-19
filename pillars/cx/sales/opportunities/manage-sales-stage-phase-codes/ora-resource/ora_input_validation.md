# Manage Sales Stage Phase Codes Input Validation

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

Use these task-scoped rules for Manage Sales Stage Phase Codes under the
Opportunities functional area. The source basis is Oracle's
[Manage Sales Methods and Stages](https://docs.oracle.com/en/cloud/saas/sales/fadsi/manage-sales-methods-and-stages.html)
guidance plus current Standard Lookups REST contract plus a fresh same-target task export for the exact phase-code lookup
rows, CSV members, and headers used by this setup task.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
| --- | --- | --- | --- | --- | --- |
| Sales stage phase-code request | Operation and LookupCode; Create needs Meaning and Enabled Yes/No or EnabledFlag Y/N; Update needs a reviewed mutable delta; native FSM Disable sets Enabled=No or EnabledFlag=N and may include an explicitly requested EndDateActive only when the export supports it; Lookup_DFF is native-FSM-only under the exact exported contract | Block package preparation | Provide the exact code, reviewed fields and supported operation. Normalize friendly field names/flags into reviewed intent, never rename CSV headers or guess DFF serialization | SingleLookup or each reviewed Package Create, Update or Disable row |  |
| Immutable package readiness | Exact target/release/task identity, completed `MOO_MANAGE_SALES_STAGE_PHASE_CODES` export receipt, exact `TaskName`, ASM identity, exact member/header receipt, reviewed Create, Update, or Disable row delta and state lock, unrelated-content receipt, final `PackagePath`, reopened `PackageSha256`, and validation result; require persisted `TaskContextPath` plus positive `TaskSequence`, resolved to the exact skill path, `TaskCode`, `TaskName`, offering, and functional area | Block Core Data Loader handoff | Export the exact task again, rebuild only the reviewed supported delta, reopen and hash the final ZIP, validate persisted Data Loader task context, and never hand-author or synthesize task context | Native FSM mutation or Import handoff | verify_stage_phase_package_readiness |

| Request envelope | Operation, RequestMode, selected environment/release/project and fixed TaskCode=MOO_MANAGE_SALES_STAGE_PHASE_CODES, LookupType=MOO_STAGE_PHASE_CD | Block live reads and preview | Select SingleLookup for one code/Read/Inventory or Package for Export/Import and multiple reviewed rows; resolve exact task ownership | Every request |  |
| Live state and impact | Fresh exact parent, code absence for Create or existing mutable before-state for Update/Disable, timestamps, write/editability evidence, intended use and stage/reporting impact per row | Block mutation preparation | Resolve each exact code through standard lookup reads; an empty export is not absence. Retain reviewed pre-state and intended delta | Every mutation or changed Import row | resolve_stage_phase_code_state |
| Final fallback receipt | REST_FALLBACK; same-target/release/task/lookup/row classified failure, applicable CSV recovery exhaustion and complete prior-submission reconciliation | Block fallback; retain CSV or original blocker | Recover omitted parent first. Submitted imports require later explicit results request, all jobs terminal, status/errors/ProcessLog and fresh unchanged state | REST_FALLBACK Create, Update or Disable | verify_stage_phase_rest_fallback |
| REST execution preview | RestFallbackEligible=true, exact ordered method/endpoint/writable body/verification GET, before/after state, impact and immutable fingerprint with separate immediate approval | Block submission; preview preparation requires no approval | Build one reviewable Apps Common preview and obtain its own approval immediately before execution; no FSM approval reuse | REST_FALLBACK submission |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
| --- | --- | --- | --- |
| Operation is unsupported; code identity is blank; Create lacks Meaning or a reviewed enabled value; Update has no mutable delta; Disable does not resolve to EnabledFlag=N; supplied Enabled/EnabledFlag is invalid or conflicting; DisplaySequence is not a nonnegative integer; or StartDateActive exceeds EndDateActive | Reject before preparation; accept Enabled Yes/No or EnabledFlag Y/N only with an unambiguous reviewed mapping and keep exact CSV value conventions | Create, Update or Disable request or each changed Import row |  |
| Delete is requested or encoded in a package | Reject as unsupported because no task-specific deletion semantic is proven; offer a separately selected Disable or end-date Update only when the fresh export contains the required field | Every Delete request or package row | verify_stage_phase_package_readiness |
| Target, release, export completion, or exact task code/name is missing or inconsistent, or a persisted project context has a blank task-context path or nonpositive sequence | Reject handoff and refresh the exact task export or selected project context; missing or inconsistent task context blocks handoff; never hand-author or synthesize task context | Native FSM mutation or Import handoff | verify_stage_phase_package_readiness |
| ASM identity, members or exact CSV headers differ from the baseline; row-count differences exceed reviewed child changes and unchanged support-parent linkage; current state does not match the live lock; or unrelated content changed | Reject the complete package; permit only disclosed child deltas and unchanged parent support, never rewrite metadata/headers, infer deletion or submit a subset | Native FSM mutation or Import handoff | verify_stage_phase_package_readiness |
| Reopening `PackagePath` does not reproduce `PackageSha256`, or the path/hash refers to evidence for another package | Invalidate readiness and rebuild and revalidate the immutable package | Native FSM mutation or Import handoff | verify_stage_phase_package_readiness |

| LookupType or task code differs from the fixed standard task; a SetId/SetCode/ReferenceGroupName selector is supplied; RequestMode/route is incompatible; or REST is requested for Export/Import/Delete | Reject before lookup; this is standard lookup maintenance, not a set-enabled task. Supported reads are Inventory/Read, Export/Import use FSM and only Create/Update/Disable may use verified REST_FALLBACK | Every request |  |
| LookupCode contains path separators, control characters or whitespace, exceeds 30 characters; Meaning exceeds 80; Description exceeds 240; Tag exceeds 150; or a supplied date is not ISO YYYY-MM-DD | Reject the field without silent normalization; encode valid code keys as one path segment | A supplied code or mutable field |  |
| Successful exact-task full-data export is header-only | Validate successful process/metadata/member/header evidence, resolve parent and requested code state live, and apply the standard-parent support procedure; zero rows alone do not trigger fallback | FSM Create, Update, Disable, Export or Import preparation | verify_stage_phase_package_readiness |
| Changed child lacks exactly one unchanged in-package MOO_STAGE_PHASE_CD standard parent or its FND_APP_STANDARD_LOOKUP.LookupType join differs | Block handoff; retain/add the unchanged fresh live parent with blank added audit fields and preserve unrelated content | Every changed FSM child | verify_stage_phase_package_readiness |
| REST_FALLBACK lacks documented exhaustion, same-target evidence, complete reconciliation or unchanged row scope; CSV is repairable; input/catalog/auth/approval/workflow/context gaps exist; jobs are pending/uncertain/partial; or FSM-only was required | Reject before REST preview; no retry or guessed eligibility | REST_FALLBACK | verify_stage_phase_rest_fallback |
| REST body includes Lookup_DFF, SetId, SetCode, audit/parent/identity changes, unsupported fields, duplicate codes, or Disable deltas beyond EnabledFlag=N | Block fallback/submission; do not drop or reinterpret requested fields. DFF and compound Disable remain on their supported FSM route | REST_FALLBACK | verify_stage_phase_rest_fallback |
| Enabled=Yes/No must be sent to REST | Normalize only the reviewed intent to EnabledFlag=Y/N; keep exact current CSV header/value conventions for FSM | Supported Create/Update/Disable fields |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.STAGE_PHASE.VALIDATE | step | 1 | validate_input | valid->OPP.STAGE_PHASE.RESOLVE_PARENT;missing->OPP.STAGE_PHASE.RETURN_MISSING;invalid->OPP.STAGE_PHASE.RETURN_MISSING;failed->OPP.STAGE_PHASE.RETURN_FAILED | none | stop | Every Manage Sales Stage Phase Codes request: Inventory, Read, Create, Update, Disable, Export or Import. Apply required fields only to the selected operation; full-task Export needs no code, set or Data Loader context. Reject unsupported Delete and incompatible mode/route before resolution |
