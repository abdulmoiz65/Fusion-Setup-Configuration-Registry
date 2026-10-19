# Manage Legal Reporting Unit Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Country text is ambiguous or any geography carrier is inconsistent | Stop and show type/use candidates and the one-receipt derivation diff; never select first row |
| STATE or other non-country territory is requested | Return Unsupported Scope before package creation; explain that non-country lookup works but blank-code import with full hierarchy is not yet validated |
| Explicit jurisdiction has multiple effective candidates | Show distinguishing details and ask the user to select; accept non-identifying candidates and reuse the selection |
| Selected jurisdiction name matches multiple importer-equivalent names | Stop with the name ambiguity; selecting an ID does not make a name-keyed CSV import unique |
| Jurisdiction is null | Skip jurisdiction/address lookups and create no new registration child; do not ask for a jurisdiction merely because the UI can default one |
| Registration details are supplied without jurisdiction | Ask for the intended jurisdiction or explicit removal of registration details; do not infer or discard them |
| Address matches multiple exported rows | Show the matching exported addresses and ask which one; duplicate import natural keys remain a blocker |
| Scoped export contains no suitable address | Block only the explicit registration branch, route prerequisite address setup, and refresh the export; never use an unrelated sample address |
| Scoped export has missing or unexpected entity roots, absent criteria metadata, or a wrong task/scope | Block baseline use even if the process succeeded; retain the ordered request/hash, ProcessId and requested-versus-observed scope sets. Reconcile the existing process before any authorized fresh request; never silently broaden scope or resubmit to poll |
| Main history is outside export scope | Expand scope to every sibling LRU and historical main period before permitting Y |
| Existing LRU differs | Show field-level requested-versus-existing differences and request explicit update-versus-new decision |
| Conditional child is partial or contains authority/function data | Reject before import; do not emit a partial child or function row |
| A broader export container is Completed with errors | Inspect the exact process log and archive. Accept evidence for this task only when every required object/member completed successfully with zero failed, warning, or partial rows and every failure is proven outside this task; otherwise block. |
| Import or verification fails | Preserve full tuple, package/process evidence, and partial successes; do not substitute or replay blindly |
| Final package readiness fails | Stop before Data Loader preview; disclose the exact missing or changed archive evidence and rerun the selected task SKILL.md local FSM package-preparation workflow |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required, length, flag, date, child-completeness, or carrier rule fails | Correct exact inputs |
| Parent not ready | Parent missing, mismatched, ineffective, or absent from package hierarchy | Resolve and include exact parent |
| Technical lookup gap | Resolver unavailable, zero/many, incompatible, or blocking | Correct evidence or target setup |
| Existing match | Equivalent LRU exists | Reuse and verify |
| Business decision | Existing definition differs or main choice is unresolved | Present field-level diff |
| Unsupported scope | Non-country geography, authority, or function requested | Restrict scope or implement future gated capability separately |
| Package contract gap | Current hierarchy, carrier, header, parent, or empty child is unproven | Refresh export and re-author |
| Auth or authz | Required privilege unavailable | Refresh approved cached authentication once for a read, then stop |
| Transport or environment | Network or service fails before side effect | Retry only known idempotent reads with bounds |
| Fusion API or process failed | Submission/child fails | Persist redacted logs/status; do not replay |
| Broader export contamination | A broader export failed outside this task while every required object/member has complete successful evidence | Scope strictly to this task, disclose the exception, and continue only after all baseline checks pass; otherwise classify as package contract gap and block |
| Process timeout | Nonterminal beyond wait | Do not resubmit; provide next-check path |
| Re-export mismatch | Terminal success differs semantically | Show exact tuple/relationship diff |
| Package readiness | Final archive identity, baseline, parent and child shape, country-only scope, preservation, semantic delta, ZIP, hash, inventory, diff, receipt, or unchanged-source evidence fails | Rebuild locally through the selected task SKILL.md workflow and revalidate the complete graph |

## Final Package Readiness Gate

| Check | Required Evidence |
|---|---|
| Target identity | Exact target environment and task identity for XLE_MANAGE_LEGAL_REPORTING_UNIT |
| Baseline | Fresh same-target, same-release, successful same-task FSM export; criteria-first serialized request/hash, ProcessId, exact requested numeric scope IDs in ASM and resolved parent identifiers in CSV, with child linkage checked per parent |
| Package structure | Current ASM metadata and exact expected member hierarchy |
| CSV contract | Exact headers, order, and encoding; exact unchanged legal-entity parent row; ORA_XLE_LEGAL_REPORTING_UNIT_REGISTRATION_FUNCTION.csv has zero new candidate rows and preserves any existing rows, or remains header-only if the baseline is empty |
| Semantic scope | Smallest supported country-only XLE_ETB_PROFILE.csv delta; null jurisdiction produces zero new registration rows; explicit resolved jurisdiction produces one complete authority-free registration child; no partial child |
| Preservation | Every unrelated row and untouched member is preserved |
| Forbidden values | No unsupported, physical, audit, ESS, object-version, authority, function, non-country geography, or service-owned value is introduced except a carrier explicitly authorized by the task rules |
| Archive validity | Final immutable archive is a valid ZIP |
| Fingerprint | SHA-256 of the exact final archive |
| Review evidence | Final member inventory and row/member semantic diff against the baseline |
| Receipt | Sanitized package-preparation receipt with no secrets or sensitive payload values |
| Freshness | No source, value, mapping, package, member, or hash changed after validation |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview | Parent, name, fixed country tuple, receipt-only GeographyIdentifierId, null or explicitly selected jurisdiction, registration branch, main history, authority nulls, zero new function rows, and fingerprint; record jurisdiction geography association as not checked without asking an extra confirmation |
| Failure | Failure class, environment, task code, stage, redacted evidence, external IDs, partial successes, and recommended action |
| Scoped export exception | Overall process state and ID, each failed object and detail from the exact process log, required-object states and row counters, archive fingerprint, and the task-scope decision |
| Verification | Terminal state, exact LRU/child natural keys, country tuple and matching transients, main flag/history, expected zero or one new registration, registration identifying behavior, zero new function rows, and zero unrelated mutations |
| READY_FOR_DATA_LOADER_PREVIEW handoff | State that this is validation and handoff only; the central Data Loader preview has not been created or approved |
| Archive change | Identify the change and require complete graph revalidation, local package preparation, and a new central preview |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Non-country input | Do not author a partial or guessed geography hierarchy or write GeographyId |
| Resolver or package gap | Do not guess from list order or fuzzy matching, or construct a child-only package. Reuse exported values only for the documented parent, preservation, and exact legal-address exceptions |
| Uncertain write | Do not replay until read-only reconciliation establishes side effects |
| Broader export ambiguity | Do not hide the overall error, ignore a failed object, or accept the archive when a required-object status/counter is failed, warning, partial, missing, or indeterminate |
| Package gate | Do not require, infer, record, or claim user approval; do not upload, initiate, or mutate Fusion |
| Approval-bound action | Only core.data-loader may create the later preview, obtain explicit approval, verify the exact archive hash, upload, and initiate |
| Final archive changed | Do not reuse the readiness result or a central preview; require complete revalidation and a new preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRU.PACKAGE_PREVIEW_GATE | decision | 60 | execution_gate | ready->LRU.READY_FOR_DATA_LOADER_PREVIEW;blocked->LRU.HANDLE_ERROR;failure->LRU.HANDLE_ERROR | LRU.ENFORCE_DESIGN | stop | After the task SKILL.md local workflow has produced the exact final immutable FSM ZIP and immediately before core.data-loader builds its preview |
| LRU.HANDLE_ERROR | step | 70 | error_handler | handled->LRU.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, default, enforcement, or package-readiness failure |
| LRU.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| LRU.READY_FOR_DATA_LOADER_PREVIEW | terminal | 90 | terminal | none | LRU.PACKAGE_PREVIEW_GATE | stop | All task rules and final-package readiness checks passed; the central Data Loader preview has not yet been created or approved |
