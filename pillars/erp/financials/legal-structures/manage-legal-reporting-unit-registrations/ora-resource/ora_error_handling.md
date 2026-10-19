# Manage Legal Reporting Unit Registrations Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Parent LRU belongs to another entity | Return Input Validation and block before jurisdiction lookup |
| Parent, jurisdiction, address, or conflict resolver returns zero/many/incompatible/unavailable | Stop and disclose normalized inputs, request/filter, eligibility predicates, result counts, and candidates |
| Jurisdiction resolves IdentifyingFlag true | Compare existing identifying registrations and block a duplicate |
| Authority or function is supplied | Return Unsupported Scope; do not populate guessed or exported values |
| Enabled function code resolves | Disclose that XLE_JUR_FUNCTIONS permission and authority/site dependency are still unproven; candidate remains blocked |
| Child package omits entity or LRU current parent row | Return Parent Not Ready and require both exact unchanged parents required by hierarchy |
| A broader export container is Completed with errors | Inspect the exact process log and archive. Accept evidence for this task only when every required object/member completed successfully with zero failed, warning, or partial rows and every failure is proven outside this task; otherwise block. |
| Import or verification fails | Preserve parent/child package, process, and re-export evidence; do not retry blindly |
| Final package readiness fails | Stop before Data Loader preview; disclose the exact missing or changed archive evidence and rerun the selected task SKILL.md local FSM package-preparation workflow |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required, ownership, length, date, authority, or function rule fails | Correct/remove exact input |
| Parent not ready | Parent missing, mismatched, ineffective, or absent from hierarchy | Resolve/include exact parents |
| Technical lookup gap | Resolver fails, is zero/many, incompatible, or incomplete | Correct evidence or target setup |
| Existing match | Equivalent definition exists | Reuse and verify |
| Business decision | Existing definition differs, sibling collision exists, or identifying state conflicts | Present field-level diff |
| Unsupported scope | Authority or function branch requested | Remove branch or implement future gated capabilities separately |
| Package contract gap | Current shape, hierarchy, parent, header, empty child, or carrier is unproven | Refresh export and re-author |
| Auth or authz | Required privilege unavailable | Refresh approved cached authentication once for a read, then stop |
| Transport or environment | Network/service fails before side effect | Retry only known idempotent reads with bounds |
| Fusion API or process failed | Submission or child process fails | Persist redacted log/status and do not replay |
| Broader export contamination | A broader export failed outside this task while every required object/member has complete successful evidence | Scope strictly to this task, disclose the exception, and continue only after all baseline checks pass; otherwise classify as package contract gap and block |
| Process timeout | Nonterminal beyond wait | Do not resubmit; provide next-check path |
| Re-export mismatch | Terminal success differs from expected child | Show exact semantic diff |
| Package readiness | Final archive identity, baseline, two-parent and child shape, preservation, semantic delta, ZIP, hash, inventory, diff, receipt, or unchanged-source evidence fails | Rebuild locally through the selected task SKILL.md workflow and revalidate the complete graph |

## Final Package Readiness Gate

| Check | Required Evidence |
|---|---|
| Target identity | Exact target environment and task identity for XLE_MANAGE_LEGAL_REPORTING_UNIT_REGISTRATIONS |
| Baseline | Fresh same-target, same-release, successful same-task FSM export receipt |
| Package structure | Current ASM metadata and exact expected member hierarchy |
| CSV contract | Exact headers, order, and encoding; exact unchanged legal-entity and legal-reporting-unit parent rows; ORA_XLE_LEGAL_REPORTING_UNIT_REGISTRATION_FUNCTION.csv header-only with zero candidate rows |
| Semantic scope | Smallest supported LRU-registration delta only in ORA_XLE_LEGAL_REPORTING_UNIT_REGISTRATION.csv |
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
| Preview | Both parent natural keys, ownership, jurisdiction/address receipts, complete definition, authority nulls, zero function rows, unchanged parents, and fingerprint |
| Failure | Failure class, environment, task code, stage, redacted evidence, external IDs, and recommended action |
| Scoped export exception | Overall process state and ID, each failed object and detail from the exact process log, required-object states and row counters, archive fingerprint, and the task-scope decision |
| Verification | Terminal state, exact child keys and definition, preserved empty function file, and proof no unrelated mutation occurred |
| READY_FOR_DATA_LOADER_PREVIEW handoff | State that this is validation and handoff only; the central Data Loader preview has not been created or approved |
| Archive change | Identify the change and require complete graph revalidation, local package preparation, and a new central preview |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Parent or resolver gap | Do not resolve LRU globally, fuzzy-match, select first row, infer physical IDs, or use export CREATE values beyond the address exception |
| Authority/function request | Do not treat tax-authority data, exported tuple, or enabled code as the missing jurisdiction/site contract |
| Uncertain write | Do not replay until read-only reconciliation establishes side effects |
| Broader export ambiguity | Do not hide the overall error, ignore a failed object, or accept the archive when a required-object status/counter is failed, warning, partial, missing, or indeterminate |
| Package gate | Do not require, infer, record, or claim user approval; do not upload, initiate, or mutate Fusion |
| Approval-bound action | Only core.data-loader may create the later preview, obtain explicit approval, verify the exact archive hash, upload, and initiate |
| Final archive changed | Do not reuse the readiness result or a central preview; require complete revalidation and a new preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRUR.PACKAGE_PREVIEW_GATE | decision | 60 | execution_gate | ready->LRUR.READY_FOR_DATA_LOADER_PREVIEW;blocked->LRUR.HANDLE_ERROR;failure->LRUR.HANDLE_ERROR | LRUR.ENFORCE_DESIGN | stop | After the task SKILL.md local workflow has produced the exact final immutable FSM ZIP and immediately before core.data-loader builds its preview |
| LRUR.HANDLE_ERROR | step | 70 | error_handler | handled->LRUR.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, default, enforcement, or package-readiness failure |
| LRUR.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| LRUR.READY_FOR_DATA_LOADER_PREVIEW | terminal | 90 | terminal | none | LRUR.PACKAGE_PREVIEW_GATE | stop | All task rules and final-package readiness checks passed; the central Data Loader preview has not yet been created or approved |
