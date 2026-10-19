# Manage Legal Entity Registrations Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Parent, jurisdiction, address, or collision resolver returns zero, many, incompatible, or unavailable | Stop and show normalized inputs, request/filter, eligibility predicates, result counts, and candidates |
| Authority or function is supplied | Return Unsupported Scope; keep authority values null and function file empty; do not reuse exported tuples |
| Function code resolves successfully | Disclose that code/meaning is enabled but jurisdiction permission and authority/site dependency remain unproven; candidate stays blocked |
| Existing registration differs | Show field-level requested-versus-existing differences and request an explicit update-versus-new decision |
| Child package omits current parent row | Return Parent Not Ready and require the exact unchanged parent row required by hierarchy |
| A broader export container is Completed with errors | Inspect the exact process log and archive. Accept evidence for this task only when every required object/member completed successfully with zero failed, warning, or partial rows and every failure is proven outside this task; otherwise block. |
| Import or verification fails | Preserve package/process/re-export evidence and never retry the parent or child blindly |
| Final package readiness fails | Stop before Data Loader preview; disclose the exact missing or changed archive evidence and rerun the selected task SKILL.md local FSM package-preparation workflow |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required, length, date, type, authority, or function rule fails | Correct or remove the exact input |
| Parent not ready | Parent is missing, mismatched, ineffective, or absent from required package hierarchy | Resolve and include exact parent |
| Technical lookup gap | Resolver fails, is zero/many, incompatible, or incomplete | Correct evidence or target setup; do not guess |
| Existing match | Equivalent definition exists | Reuse and verify |
| Business decision | Existing definition differs or identifying state conflicts | Present field-level diff |
| Unsupported scope | Authority or function branch is requested | Remove branch or implement future gated capabilities separately |
| Package contract gap | Current shape, hierarchy, header, empty child, or carrier is unproven | Refresh export and re-author |
| Auth or authz | Required privilege is unavailable | Refresh approved cached authentication once for a read, then stop |
| Transport or environment | Network or target service fails before a side effect | Retry only known idempotent reads with bounds |
| Fusion API or process failed | Submission or child process fails | Persist redacted log/status and do not replay |
| Broader export contamination | A broader export failed outside this task while every required object/member has complete successful evidence | Scope strictly to this task, disclose the exception, and continue only after all baseline checks pass; otherwise classify as package contract gap and block |
| Process timeout | Process remains nonterminal beyond wait | Do not resubmit; provide next-check path |
| Re-export mismatch | Terminal success differs from expected child definition | Show exact semantic diff |
| Package readiness | Final archive identity, baseline, parent and child shape, preservation, semantic delta, ZIP, hash, inventory, diff, receipt, or unchanged-source evidence fails | Rebuild locally through the selected task SKILL.md workflow and revalidate the complete graph |

## Final Package Readiness Gate

| Check | Required Evidence |
|---|---|
| Target identity | Exact target environment and task identity for XLE_MANAGE_LEGAL_ENTITY_REGISTRATIONS |
| Baseline | Fresh same-target, same-release, successful same-task FSM export receipt |
| Package structure | Current ASM metadata and exact expected member hierarchy |
| CSV contract | Exact headers, order, and encoding; exact unchanged legal-entity parent row; ORA_XLE_LEGAL_ENTITY_REGISTRATION_FUNCTION.csv header-only with zero candidate rows |
| Semantic scope | Smallest supported registration delta only in XLE_REGISTRATION.csv |
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
| Preview | Parent natural key, jurisdiction/address receipts, complete registration definition, authority nulls, zero function rows, unchanged parent, and fingerprint |
| Failure | Failure class, environment, task code, stage, redacted evidence, external IDs, and recommended action |
| Scoped export exception | Overall process state and ID, each failed object and detail from the exact process log, required-object states and row counters, archive fingerprint, and the task-scope decision |
| Verification | Terminal state, exact child natural keys and values, preserved empty function file, and proof no unrelated mutation occurred |
| READY_FOR_DATA_LOADER_PREVIEW handoff | State that this is validation and handoff only; the central Data Loader preview has not been created or approved |
| Archive change | Identify the change and require complete graph revalidation, local package preparation, and a new central preview |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing or ambiguous evidence | Do not fuzzy-match, select first row, infer physical IDs, or use export business values beyond the address exception |
| Authority/function request | Do not treat a tax authority, exported tuple, or enabled function code as the missing permission/site contract |
| Uncertain write | Do not replay until read-only reconciliation establishes side effects |
| Broader export ambiguity | Do not hide the overall error, ignore a failed object, or accept the archive when a required-object status/counter is failed, warning, partial, missing, or indeterminate |
| Package gate | Do not require, infer, record, or claim user approval; do not upload, initiate, or mutate Fusion |
| Approval-bound action | Only core.data-loader may create the later preview, obtain explicit approval, verify the exact archive hash, upload, and initiate |
| Final archive changed | Do not reuse the readiness result or a central preview; require complete revalidation and a new preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LER.PACKAGE_PREVIEW_GATE | decision | 60 | execution_gate | ready->LER.READY_FOR_DATA_LOADER_PREVIEW;blocked->LER.HANDLE_ERROR;failure->LER.HANDLE_ERROR | LER.ENFORCE_DESIGN | stop | After the task SKILL.md local workflow has produced the exact final immutable FSM ZIP and immediately before core.data-loader builds its preview |
| LER.HANDLE_ERROR | step | 70 | error_handler | handled->LER.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, default, enforcement, or package-readiness failure |
| LER.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| LER.READY_FOR_DATA_LOADER_PREVIEW | terminal | 90 | terminal | none | LER.PACKAGE_PREVIEW_GATE | stop | All task rules and final-package readiness checks passed; the central Data Loader preview has not yet been created or approved |
