# Manage Receipt Classes and Methods Error Handling

## Error classifications

| Category | Examples | Required response |
|---|---|---|
| Input ambiguity | Missing operation, class/method name, date, processing behavior, account, currency, recovery action, or a customer date whose month/day order cannot be proven | Ask one consolidated business-language question and do not generate a ZIP. For an ambiguous date, identify the object/field and request an exact `YYYY-MM-DD` calendar date; never guess. |
| Source package | Wrong task, incomplete process, unsafe ZIP, mixed environment/release, member/header/metadata mismatch | Stop and list the exact invalid evidence. |
| Reference or dependency | Missing/ambiguous parent, BU, bank account, payment setup, accounting combination, or current-state match | Stop before preview and request target-valid evidence. |
| Design conflict | Incompatible creation/remittance/clearance/payment choices, duplicate, invalid dates, multiple primaries, or uncovered currency | Show the failed rule and corrective choice; do not weaken the rule. |
| Unsupported operation | Delete, rename, reparent, or another lifecycle action that cannot be represented as a task-owned create or exact update | Refuse candidate generation and preserve current state. Operation count, mixed entities, and multiple parents are not blockers. |
| Candidate validation | Audit value populated, noncanonical or invalid date, row dropped, required ancestor context missing/changed, task scope changed, hierarchy broken, non-deterministic build, or unresolved warning | Quarantine the candidate; never import or reuse it. Date failures must occur before ZIP creation when the adapter owns the build. |
| Process warning | Fusion reports a skipped child row, missing parent row, or any unresolved warning | Treat the process as failed even when zero rows are marked failed; preserve logs, verify partial persistence, repair, and generate a fresh candidate. |
| Loader pre-submit | Core Data Loader or Task Hook rejects the ZIP, task identity, or validation envelope | Capture the validation finding and immutable archive identity; do not upload or submit. |
| Fusion process | Import process warns, fails, or does not complete successfully | Capture process ID, status, logs, diagnostics, and check fresh state before any repair. |
| Persisted mismatch | Fresh export differs from the confirmed requirement or candidate | Mark unverified, preserve evidence, diagnose the owning layer, and require a fresh attempt. |

## Refusal and retry rules

| Situation | What must not happen |
|---|---|
| Any node is blocked, unresolved, invalid, failed, incomplete, or unapproved | Do not generate or submit a candidate. |
| Business design changes after confirmation | Do not reuse the confirmation; regenerate the consolidated flow preview and require a new standalone confirm. |
| Evidence or candidate bytes change while business design is unchanged | Keep the flow confirmation only when task, environment, release/schema compatibility, and stable business-design SHA-256 still match; repeat phase-local build, validation, determinism, and immutable-candidate approval checks. |
| Live import lacks separate approval | Do not upload or submit. |
| A package was rejected or its process failed | Do not resubmit or mutate that ZIP; preserve it as immutable evidence. |
| Partial persistence is possible | Do not generate the next attempt until a fresh current export is reconciled. |
| Resolver or CodeSearch evidence is unavailable | Do not fabricate evidence or silently infer a contract. |
| Credentials are supplied | Never place them in repository files, artifacts, reports, commands, ZIPs, or logs. |

## Disclosure requirements

| Gate | Required disclosure |
|---|---|
| Clarification | Exact unresolved business choices, grouped into the smallest useful question. |
| Final design confirmation | Environment, release, task code/name, every operation and phase, hierarchy, values, preserved state, dependencies, warnings, row counts, evidence hashes, and stable business-design hash. |
| Candidate handoff | Candidate path, SHA-256, blueprint, source hashes, member inventory, populated-row summary, validation result, and explicit offline-only status. |
| Import approval | Target environment, exact task, candidate filename/SHA-256, requested changes, and confirmation that the candidate passed independent validation. |
| Process result | Process name/ID, terminal status, row counts, warnings/errors, logs/diagnostics, and whether fresh-state verification passed. |

## Completion rule

Static generation is complete only when the rule registry and execution plan compile, all applicable nodes pass, the candidate is independently valid and deterministic, and the result is labeled locally validated rather than imported. Live completion requires a successful controlled process and fresh-export reconciliation of every requested class, method, account, and error-mapping value.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RCM.EXECUTION_GATE | decision | 60 | execution_gate | ready->RCM.READY;blocked->RCM.BLOCKED | RCM.ENFORCE | stop | Design enforcement passed; static mode may hand off a validated candidate, while live mode additionally requires controlled confirmation and approval. |
| RCM.READY | terminal | 70 | terminal | none | RCM.EXECUTION_GATE | stop | All applicable static rules passed and the requested output is ready for the next controlled stage. |
| RCM.BLOCKED | terminal | 999 | terminal | none | none | stop | Any preceding node returns invalid, blocked, unresolved, failed, incomplete, unsafe, unsupported, unconfirmed, or unapproved. |
