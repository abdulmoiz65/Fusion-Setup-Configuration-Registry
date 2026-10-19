# Manage Legal Entity Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Country, address, entity, or PSU resolver is zero, unresolved, inactive, ineffective, or unavailable | Stop the dependent work and disclose safe input/filter details, eligibility predicates, result counts, and candidates; use the owning resolver's correction/refinement path |
| Country lookup has multiple results, including language variants | Present the country values and languages for explicit refinement; do not select a first row or hardcode a language; require a unique effective result before continuing |
| Identifying-jurisdiction input is missing | Ask for the intended name or search text; reuse input already present in the request and do not ask again unnecessarily |
| Jurisdiction search has zero eligible results | Explain missing, nonidentifying, or out-of-date matches and request corrected input or configuration; do not fabricate a jurisdiction |
| Jurisdiction search has multiple eligible results | Present the distinguishing details required by the resolver and ask the user to select; hold dependent work until resolved, then verify exact-name import uniqueness |
| Selected jurisdiction has a duplicate exact Name | Report name-based import ambiguity even if only one record is eligible; selection of an ID alone cannot fix it. Stop unless the current import contract demonstrably supports unambiguous selection |
| Country or jurisdiction response is partial, malformed, or contains invalid dates | Classify as a lookup/validation failure and retain the failed stage; a failed or incomplete lookup is not a zero-match result. Do not proceed using partial candidates |
| Root-only or partial aggregate is proposed | Return Package Contract Gap and require all three explicit children before preview |
| Authority or function input is supplied | Return Unsupported Scope; do not populate guessed or exported authority/function values |
| Child import under an existing parent omits the current parent row | Return Parent Not Ready; include the exact unchanged parent row required by hierarchy without copying unrelated child values |
| A broader export container is Completed with errors | Inspect the exact process log and archive. Accept evidence for this task only when every required object/member completed successfully with zero failed, warning, or partial rows and every failure is proven outside this task; otherwise block. |
| Import submission or any child fails | Persist process/log evidence and partial-success details; never automatically replay |
| Terminal success re-export lacks any expected persistent child | Return Re-export Mismatch; insert-only transients may clear, but persistent children and registration numbers must exist exactly once |
| Final package readiness fails | Stop before Data Loader preview; disclose the exact missing or changed archive evidence and rerun the selected task SKILL.md local FSM package-preparation workflow |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required, length, flag, date, or aggregate-cardinality rule fails | Correct the exact input or row set |
| Parent not ready | Existing or earlier approved parent evidence is absent or mismatched | Resolve parent and package hierarchy |
| Technical lookup gap | Resolver is unavailable, partial, malformed, incompatible, or cannot resolve after its documented refinement/selection path | Correct evidence or target setup; do not guess |
| Existing match | Equivalent natural key and definition already exist | Reuse or verify; do not create |
| Business decision | Existing object differs, optional design is unresolved, or eligible jurisdiction/country-language candidates require user choice | Present differences or candidate details and request the missing selection; revalidate the selected result before continuing |
| Package contract gap | Current shape, hierarchy, carrier, default, or child behavior is unproven | Refresh export and re-author |
| Auth or authz | Export, lookup, or import privilege is unavailable | Refresh approved cached authentication once for a read, then stop |
| Transport or environment | Network or target service fails before a side effect | Retry only a known idempotent read with bounds |
| Fusion API or process failed | Submission fails or any object/child reaches failed terminal state | Persist redacted logs/status and do not replay |
| Broader export contamination | A broader export failed outside this task while every required object/member has complete successful evidence | Scope strictly to this task, disclose the exception, and continue only after all baseline checks pass; otherwise classify as package contract gap and block |
| Process timeout | Process remains nonterminal beyond approved wait | Do not resubmit; provide next-check path |
| Re-export mismatch | Terminal success differs semantically from expected aggregate | Show exact row/relationship diff |
| Package readiness | Final archive identity, baseline, six-member shape, parent and empty-child preservation, semantic delta, ZIP, hash, inventory, diff, receipt, or unchanged-source evidence fails | Rebuild locally through the selected task SKILL.md workflow and revalidate the complete graph |

## Final Package Readiness Gate

| Check | Required Evidence |
|---|---|
| Target identity | Exact target environment and task identity for XLE_MANAGE_LEGAL_ENTITY |
| Baseline | Fresh same-target, same-release, successful same-task FSM export receipt |
| Package structure | Current ASM metadata and exact entity-tree hierarchy with all six expected CSV members |
| CSV contract | Exact headers, order, and encoding; all required unchanged parent rows preserved; existing registration-function rows preserved unchanged with zero candidate function rows; a function member remains header-only only when already header-only in the baseline |
| Semantic scope | Smallest supported UI-equivalent aggregate only: legal-entity root, same-name main LRU, identifying entity registration, and identifying main-LRU registration |
| Country and jurisdiction references | Resolved territory/primary country evidence and selected eligible jurisdiction, complete lookup pages, unambiguous exact import Name, consistent CSV mappings, and disclosed country-association/GeographyElement1 limits; no country GeographyId prerequisite |
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
| Preview | Four-row aggregate, exact natural keys, resolvers, selected jurisdiction and its registration codes, defaults, null/system fields, authority/function zero-candidate-row scope, unchanged existing function rows, hierarchy, and fingerprint. Disclose that jurisdiction-to-country association was not independently verified and GeographyElement1 equals GeographyName by the agreed country derivation, not by an endpoint-returned value or universal invariant |
| Failure | Failure class, environment, task code, stage, safe redacted evidence, external IDs, partial successes, and recommended action |
| Scoped export exception | Overall process state and ID, each failed object and detail from the exact process log, required-object states and row counters, archive fingerprint, and the task-scope decision |
| Verification | Terminal state, each persistent child exactly once, both registration numbers, country mapping, natural-key address, and no unrelated mutation |
| READY_FOR_DATA_LOADER_PREVIEW handoff | State that this is validation and handoff only; the central Data Loader preview has not been created or approved |
| Archive change | Identify the change and require complete graph revalidation, local package preparation, and a new central preview |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing child or unresolved reference | Do not rely on UI automation, list order, export fallback, or guessed physical IDs. The declared jurisdiction name search and explicit eligible selection are permitted; a search fragment itself is never the resolved import Name |
| Missing country GeographyId | Do not require it from addressGeographies, substitute GeographyIdentifierId, or treat the selected jurisdiction's GeographyId as independent proof of the LE country |
| Duplicate jurisdiction import Name | Do not bypass ambiguity with user selection, eligibility filtering, or an invented ID column in the CREATE package |
| Authority/function request | Do not use exported tuples or the enabled lookup code as jurisdiction permission |
| Uncertain write | Do not replay until read-only reconciliation establishes whether side effects occurred |
| Broader export ambiguity | Do not hide the overall error, ignore a failed object, or accept the archive when a required-object status/counter is failed, warning, partial, missing, or indeterminate |
| Package gate | Do not require, infer, record, or claim user approval; do not upload, initiate, or mutate Fusion |
| Approval-bound action | Only core.data-loader may create the later preview, obtain explicit approval, verify the exact archive hash, upload, and initiate |
| Final archive changed | Do not reuse the readiness result or a central preview; require complete revalidation and a new preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LE.PACKAGE_PREVIEW_GATE | decision | 60 | execution_gate | ready->LE.READY_FOR_DATA_LOADER_PREVIEW;blocked->LE.HANDLE_ERROR;failure->LE.HANDLE_ERROR | LE.ENFORCE_DESIGN | stop | After the task SKILL.md local workflow has produced the exact final immutable FSM ZIP and immediately before core.data-loader builds its preview |
| LE.HANDLE_ERROR | step | 70 | error_handler | handled->LE.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, default, enforcement, or package-readiness failure |
| LE.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| LE.READY_FOR_DATA_LOADER_PREVIEW | terminal | 90 | terminal | none | LE.PACKAGE_PREVIEW_GATE | stop | All task rules and final-package readiness checks passed; the central Data Loader preview has not yet been created or approved |
