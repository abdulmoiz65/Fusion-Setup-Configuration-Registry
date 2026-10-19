# Manage Legal Addresses Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Country, layout, time-zone, or export resolver returns zero or many | Stop and show normalized inputs, request or filter, result counts, eligibility predicates, and candidates |
| Equivalent address exists | Return Existing Match and do not create a duplicate |
| Import completes with ValidatedFlag N and GeometryStatusCode DIRTY | Accept and disclose the unvalidated state; do not claim canonicalization |
| Import reports location, source-reference, or geography failure | Preserve package fingerprint and process evidence; do not retry with guessed values |
| Final package readiness fails | Stop before Data Loader preview; disclose the exact missing or changed archive evidence and rerun the selected task SKILL.md local FSM package-preparation workflow |
| A broader export container is Completed with errors | Inspect the exact process log and archive. Accept evidence for this task only when every required object/member completed successfully with zero failed, warning, or partial rows and every failure is proven outside this task; otherwise block. |
| Import status is nonterminal beyond the approved wait | Stop with environment, operation, task code, ProcessId, last status, elapsed time, and next-check path |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required, conditional, length, type, or layout rule fails | Correct the exact field and rerun preview |
| Catalog mismatch | Target metadata, header, layout, or resolver evidence conflicts | Refresh authoritative evidence and re-author |
| Auth or authz | Required identity or privilege is unavailable | Refresh approved cached authentication once for a read, then stop |
| Transport or environment | Network or target service fails before side effect | Retry only a known idempotent read with bounded backoff |
| Fusion API or process failed | Fusion rejects or a process reaches failed terminal state | Persist redacted status/log evidence and do not replay automatically |
| Broader export contamination | A broader export failed outside this task while every required object/member has complete successful evidence | Scope strictly to this task, disclose the exception, and continue only after all baseline checks pass; otherwise classify as package evidence failure and block |
| Process timeout | Import remains nonterminal beyond the approved wait | Do not resubmit; provide next-check path |
| Re-export mismatch | Terminal success does not produce the expected semantic row | Show expected-versus-actual natural-key and field differences |
| Package readiness | Final archive identity, baseline, shape, preservation, semantic delta, ZIP, hash, inventory, diff, receipt, or unchanged-source evidence fails | Rebuild locally through the selected task SKILL.md workflow and revalidate the complete graph |

## Final Package Readiness Gate

| Check | Required Evidence |
|---|---|
| Target identity | Exact target environment and task identity for XLE_MANAGE_LEGAL_ADDRESSES |
| Baseline | Fresh same-target, same-release, successful same-task FSM export receipt |
| Package structure | Current ASM metadata and exact expected member hierarchy |
| CSV contract | Exact headers, order, and encoding; only the reviewed XLE_LE_LEGAL_ADDRESS.csv row delta; required system blanks preserved |
| Semantic scope | Smallest supported legal-address create delta only, with documented CreatedByModule, new collision-checked OrigSystemReference, validation-status semantics, and country style/layout |
| Preservation | Every unrelated row and untouched member is preserved |
| Forbidden values | No unsupported, physical, audit, ESS, object-version, authority, function, or service-owned value is introduced except a carrier explicitly authorized by the task rules |
| Archive validity | Final immutable archive is a valid ZIP |
| Fingerprint | SHA-256 of the exact final archive |
| Review evidence | Final member inventory and row/member semantic diff against the baseline |
| Receipt | Sanitized package-preparation receipt with no secrets or sensitive payload values |
| Freshness | No source, value, mapping, package, member, or hash changed after validation |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview | Exact candidate identity, user components, resolved style, defaults, Generated/Null/System treatment, new source reference, and N/DIRTY meaning |
| Failure | Failure class, environment, task code, stage, safe redacted evidence, external IDs, and recommended action |
| Scoped export exception | Overall process state and ID, each failed object and detail from the exact process log, required-object states and row counters, archive fingerprint, and the task-scope decision |
| Verification | Terminal process state, exact re-exported natural key and components, validation status, and proof no unrelated row changed |
| READY_FOR_DATA_LOADER_PREVIEW handoff | State that this is validation and handoff only; the central Data Loader preview has not been created or approved |
| Archive change | Identify the change and require complete graph revalidation, local package preparation, and a new central preview |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing or ambiguous evidence | Do not guess, fuzzy-match, select the first row, or use exported business values beyond the exact legal-address exception |
| Uncertain or failed write | Do not retry automatically or submit a second package before read-only reconciliation |
| N/DIRTY result | Do not describe the address as geography-validated or canonicalized |
| Broader export ambiguity | Do not hide the overall error, ignore a failed object, or accept the archive when a required-object status/counter is failed, warning, partial, missing, or indeterminate |
| Package gate | Do not require, infer, record, or claim user approval; do not upload, initiate, or mutate Fusion |
| Approval-bound action | Only core.data-loader may create the later preview, obtain explicit approval, verify the exact archive hash, upload, and initiate |
| Final archive changed | Do not reuse the readiness result or a central preview; require complete revalidation and a new preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LA.PACKAGE_PREVIEW_GATE | decision | 60 | execution_gate | ready->LA.READY_FOR_DATA_LOADER_PREVIEW;blocked->LA.HANDLE_ERROR;failure->LA.HANDLE_ERROR | LA.ENFORCE_DESIGN | stop | After the task SKILL.md local workflow has produced the exact final immutable FSM ZIP and immediately before core.data-loader builds its preview |
| LA.HANDLE_ERROR | step | 70 | error_handler | handled->LA.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, default, enforcement, or package-readiness failure |
| LA.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| LA.READY_FOR_DATA_LOADER_PREVIEW | terminal | 90 | terminal | none | LA.PACKAGE_PREVIEW_GATE | stop | All task rules and final-package readiness checks passed; the central Data Loader preview has not yet been created or approved |
