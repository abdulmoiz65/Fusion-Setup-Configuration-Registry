# Manage Sales Stage Phase Codes Error Handling

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

Stop before any undocumented write, automatic retry, or interpretation of a
runtime opportunity field as setup metadata.

## Error Situations

| Situation | What Should Happen |
| --- | --- |
| Required phase-code input is missing or invalid | Stop before package preparation; identify the Lookup Code, Meaning, Enabled, sequence, or date issue and request a corrected row |
| Delete is requested or found in the package | Stop and report Delete as unsupported; do not infer deletion semantics. Offer a separately reviewed Disable or end-date Update only when the fresh export supports it |
| Fresh export, task identity and persisted Data Loader task context, ASM identity, member/header receipt, reviewed delta, state lock, unrelated-content receipt, final path, or reopened SHA-256 validation fails | Classify as package readiness, show every exact mismatch, and stop before Core Data Loader handoff |
| Accepted Data Loader initiation is followed by automatic polling, ProcessLog retrieval, result retrieval, or verification | Stop; accepted initiation is terminal for that request and those steps require a later explicit status or results request |

## Error Classifications

| Result Category | When Used | Next Action |
| --- | --- | --- |
| Input validation | A required phase-code identity or value is missing, invalid, or inconsistent with the requested operation | Correct the row and rerun validation before immutable-package handoff |
| Unsupported operation | Delete is requested or encoded without a proven task-specific semantic | Refuse Delete; require a new explicit Disable or end-date Update request before preparing another package |
| Package readiness | The baseline is not a fresh completed exact-target and release export, the task or ZIP contract differs, the reviewed state lock drifted, unrelated content changed, or reopened bytes do not match the recorded hash | Refresh the exact task export, rebuild only a reviewed Create, Update, or Disable delta, and rerun `verify_stage_phase_package_readiness` |

## Refusal Rules

| Situation | What Must Not Happen |
| --- | --- |
| Required phase-code fields, exact current-state evidence, or immutable package validation is missing | Do not hand off, save, import, retry, or claim that the target is unchanged; obtain the missing evidence and rebuild the immutable package |
| Delete is requested, encoded, or inferred from an omitted row | Do not delete or treat omission as deletion; require a separately reviewed supported lifecycle operation |
| A child FSM preview or approval is proposed before Core Data Loader handoff | Do not create, request, accept, or reuse it in this child; hand only the validated immutable package to Core Data Loader for its retained-session Task Hook preview and current contextual approval contract. Do not require a literal user keyword or add a separate child approval gate |
| Native FSM package-readiness has not returned ready for the exact immutable ZIP | Do not hand off, upload, initiate, or manufacture Data Loader-owned preview or approval evidence |

## Recovery, Fallback and Live Errors

| Situation | What Should Happen |
|---|---|
| Successful exact-task data export is header-only | Preserve actual successful status and recover the unchanged standard parent from fresh live metadata; omission is not absence/fallback |
| Parent/code GET fails or returns 401/403 | Classify auth/authz/transport/Fusion API, allow only core's one cache-token refresh and bounded read retry, then stop; never switch views or invent absence |
| Export failed/timed out or remains unusable after recovery | Retain exact target/task/lookup receipt, actual status/elapsed polling, classified failure and recovery outcomes; only exhaustion returns a candidate |
| Accepted import later fails or has no effect | On a later explicit results request retrieve Core Data Loader status/errors/ProcessLog, require all jobs terminal and fresh unchanged requested states before fallback; no automatic retry |
| Prior submission unknown/pending, diagnostics incomplete, scope drift or partial changes | Block switching; reconcile first. All-applied returns verified state without writing; partial results require a new reviewed remaining-change request |
| REST_FALLBACK needs unsupported DFF or compound Disable delta | Block instead of dropping requested fields or inventing payloads; retain its supported FSM route |
| Final fallback eligible but REST approval missing | Prepare an immutable exact preview and obtain separate approval immediately before execution; export/Data Loader approval is not reusable |
| REST row fails, is uncertain or verification fails | Stop at once, preserve successes and unattempted rows, reconcile safely without retry/rollback/another fallback; new writes need new preview and approval |
| Diagnostics or artifacts cannot be persisted | Classify artifact persistence, preserve safe temporary evidence and report intended project path; never expose credentials/tokens/private keys |

Classify failures as input validation, catalog mismatch, auth/authz,
transport/environment, Fusion API, process timeout/failed, approval blocker or
artifact persistence. Retain stage, actual status, safe external IDs, artifact
refs and one next action. Redact credentials, tokens, OAuth state, cookies and
private keys from all output. Delete stays unsupported.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.STAGE_PHASE.GATE | decision | 7 | execution_gate | handoff_ready->OPP.STAGE_PHASE.RETURN_READY;accepted_initiation->OPP.STAGE_PHASE.RETURN_ACCEPTED;rest_approved->OPP.STAGE_PHASE.RETURN_REST_READY;read_only->OPP.STAGE_PHASE.RETURN_READ;export_ready->OPP.STAGE_PHASE.RETURN_EXPORT_READY;missing->OPP.STAGE_PHASE.RETURN_MISSING;failed->OPP.STAGE_PHASE.RETURN_FAILED | OPP.STAGE_PHASE.DESIGN | stop | Native FSM hands a validated immutable package to Data Loader without child approval and ends at accepted initiation. Final REST_FALLBACK needs dedicated eligible result and immediate separate exact-preview approval; submit/verify once per row. Read/Export returns no mutation authorization |
| OPP.STAGE_PHASE.RETURN_READY | terminal | 8 | terminal | none | OPP.STAGE_PHASE.GATE | continue | Native unchanged CSV, exact task/context/hash and parent-child/state/impact evidence ready for Data Loader Task Hook/preview; no upload approval or execution has occurred |
| OPP.STAGE_PHASE.RETURN_ACCEPTED | terminal | 9 | terminal | none | OPP.STAGE_PHASE.GATE | continue | Data Loader accepted initiation; end without automatic status/log/live verification until later explicit request |
| OPP.STAGE_PHASE.RETURN_MISSING | terminal | 10 | terminal | none | none | continue | Required identity, input, state, package/context, exhaustion/reconciliation or separate REST approval is missing; no write authorized |
| OPP.STAGE_PHASE.RETURN_FAILED | terminal | 11 | terminal | none | none | continue | Validation, resolution, readiness, execution or verification failed; no retry or implicit route switch |
| OPP.STAGE_PHASE.RETURN_REST_READY | terminal | 12 | terminal | none | OPP.STAGE_PHASE.GATE | continue | Eligible ordered REST_FALLBACK requests separately approved for Apps Common; submit once, verify immediately and stop at first failure/uncertainty |
| OPP.STAGE_PHASE.RETURN_FALLBACK_REQUIRED | terminal | 13 | terminal | none | OPP.STAGE_PHASE.PACKAGE | continue | Applicable CSV recovery exhausted with classified same-target receipt and fully reconciled unchanged prior submissions; RestFallbackEligible=false. Router resumes unchanged request once with fresh standard parent/code reads; no REST write approval implied |
| OPP.STAGE_PHASE.RETURN_VERIFIED | terminal | 14 | terminal | none | OPP.STAGE_PHASE.VERIFY_FALLBACK | continue | All requested values confirmed applied by fresh exact reads and no pending/uncertain jobs; return verified result without another mutation |
| OPP.STAGE_PHASE.RETURN_READ | terminal | 15 | terminal | none | OPP.STAGE_PHASE.GATE | continue | Read/Inventory complete with exact parent/code identities, timestamps and full pagination; no mutation |
| OPP.STAGE_PHASE.RETURN_EXPORT_READY | terminal | 16 | terminal | none | OPP.STAGE_PHASE.GATE | continue | Fresh exact full-task Export baseline valid for review, including header-only seeded omission; no code delta or import approval implied |
