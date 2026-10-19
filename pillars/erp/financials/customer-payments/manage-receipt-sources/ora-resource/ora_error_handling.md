# Manage Receipt Sources Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required business choice is absent, ambiguous, or invalid | Ask one consolidated business-language question that identifies the affected record and acceptable correction; retain resolved values, re-evaluate after the answer, and ask again if needed. |
| Source package is wrong, unsafe, stale, failed, or incompatible | Explain the exact violated evidence rule, obtain or request corrected exact-task evidence, and resume from validation. |
| BU, target, method/class, bank compatibility, or DFF mapping is unresolved | Attempt the documented read-only resolution, then request the smallest authoritative target evidence still missing and resume after it is supplied. |
| Valid update or end-date is requested | Preserve omitted baseline values, validate the changed fields, and continue through preview, confirmation, build, and approval gates. |
| Rename, BU move, or hard delete is requested | Explain that this CSV route cannot perform that exact operation and ask whether end-date, replacement create, verify, or the named separate product workflow satisfies the intent. Continue with the explicitly selected supported route. |
| Candidate fails audit, schema, preservation, scope, or determinism checks | Quarantine it; never import or reuse it. |
| A ZIP is created before orchestration-owned design confirmation | Mark the attempt failed, preserve the ZIP as evidence, quarantine its SHA, and start a fresh attempt after a new preview and confirmation. Never validate it into eligibility or import it. |
| Fusion rejects the ZIP before submit | Capture the alert and page state; do not submit. |
| Process warns, skips, fails, times out, or has unknown status | Preserve process identity and diagnostics; do not resubmit automatically. |
| Fresh export differs from confirmed requirements | Mark the run unverified and diagnose the owning layer before a fresh attempt. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Needs input | Required business input, approval, evidence, or correction is absent. | Ask one clear question, retain resolved state, and re-evaluate after the answer. |
| Needs alternative | Rename, BU move, hard delete, or another operation outside the documented create/update contract is requested. | Explain the exact boundary and ask the customer to select an evidenced supported alternative; never translate intent silently. |
| Failed | Contract, candidate, process, or reconciliation validation fails. | Preserve evidence, repair the owner, and create a fresh attempt. |
| Ready | All applicable static rules pass. | Continue only to the next governed preview or validation stage. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Clarification | Exact unresolved business choices and valid distinctions. |
| Design confirmation | Environment/release evidence, task, operations, keys, values, preserved state, dependencies, blockers, warnings, row counts, source hashes, and design hash. |
| Candidate handoff | Candidate path, SHA-256, blueprint, source hashes, members, row summary, validation result, and offline-only status. |
| Import approval | Target, exact task, candidate filename/hash, requested changes, and independent validation status. |
| Process result | Process identity/status, row counts, warnings/errors, logs/diagnostics, and fresh-state verification result. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Any applicable rule is unresolved, invalid, failed, incomplete, or unconfirmed | Do not generate a candidate yet; ask or perform the next concrete resolution step and resume afterward. |
| Standalone design confirmation has not been recorded for the exact design and source hashes | Do not invoke build, validate, determinism, or rollback; do not create, stage, or hand off a ZIP. |
| A pre-confirmation ZIP exists | Do not reuse, rename, rebuild in place, authorize, upload, or import it; preserve it as immutable failed-attempt evidence and reject its SHA. |
| Candidate or source changes after confirmation | Do not reuse confirmation; generate a new preview. |
| Live submission lacks Data Loader's current approval | Do not upload or submit. |
| A candidate was rejected or its process failed | Do not resubmit or mutate the failed ZIP. |
| Partial persistence is possible | Do not create a new attempt until a fresh export is reconciled. |
| Resolver or source evidence is unavailable | Do not fabricate it or silently weaken the rule. |
| Credentials are supplied | Never persist them in repository files, artifacts, commands, ZIPs, or logs. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RS.EXECUTION_GATE | decision | 60 | execution_gate | create_ready->RS.READY_CREATE;update_ready->RS.READY_UPDATE;end_date_ready->RS.READY_END_DATE;no_op_ready->RS.READY_NOOP;needs_input->RS.NEEDS_INPUT;unsafe->RS.SAFETY_HOLD | RS.ENFORCE | stop | Design enforcement passed and the governing implementation orchestration recorded orchestration-owned design confirmation for the exact design and source hashes; only then may static mode build and hand off a validated candidate, while live mode also requires later Core Data Loader candidate-specific approval. |
| RS.READY_CREATE | terminal | 70 | terminal | none | RS.EXECUTION_GATE | stop | A create design passed every applicable static rule and is ready for the next governed stage. |
| RS.READY_UPDATE | terminal | 71 | terminal | none | RS.EXECUTION_GATE | stop | An update design passed every applicable static rule and is ready for the next governed stage. |
| RS.READY_END_DATE | terminal | 72 | terminal | none | RS.EXECUTION_GATE | stop | An end-date design passed every applicable static rule and is ready for the next governed stage. |
| RS.READY_NOOP | terminal | 73 | terminal | none | RS.EXECUTION_GATE | stop | Verification found no requested change; no mutation candidate is needed. |
| RS.NEEDS_INPUT | terminal | 90 | terminal | none | none | stop | Ask the smallest useful follow-up, retain resolved state, and restart at RS.VALIDATE after the answer or corrected evidence. |
| RS.SAFETY_HOLD | terminal | 999 | terminal | none | none | stop | A non-business safety or external condition prevents mutation. Explain the concrete recovery action, retain the design, and resume when the condition is corrected. |
