# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Identity/date invalid | Stop with work type, cardinality, and date conflict |
| Set assignment invalid | Identify original name/code input type, match/duplicate state, remaining count and consumers; a missing match must not change the searched field |
| Semantic/profile/use conflict | Stop with changed flag/type, profile state, affected consumers/transactions |
| Required consumer-impact handoff or workflow-selected source route missing | WTYPE_USE_EVIDENCE_MISSING, blocking=true; stop affected import preparation through the declared issues transition. Record the workflow gap and needed source coverage; do not ask for execution approval or acquire evidence through an undeclared route |
| Consumer-impact handoff stale, cross-target, mismatched, incomplete or untraceable | WTYPE_USE_EVIDENCE_INVALID, blocking=true; identify the failed contract check and return issues. Require a completed supported acquisition in a fresh run; never infer zero consumers or reuse old approval |
| Translation/DFF invalid | Stop with language/context/segment and metadata result |
| WTYPE_TRANSLATION_NAME_CONFLICT | blocking=true; identify affected translation rows, resolved language and conflicting work-type display identities. Return through WTYPE.RESOLVE_CHILDREN failure to WTYPE.RETURN_ISSUES before preview; do not rename, normalize, drop rows or request upload approval to bypass the collision |
| WTYPE_TRANSLATION_NAME_CHECK_INCOMPLETE | blocking=true; identify the missing or invalid required baseline/change/comparison evidence and return through WTYPE.RESOLVE_CHILDREN failure to WTYPE.RETURN_ISSUES. Restore evidence through the selected workflow; do not invent a comparison rule, run an undeclared lookup or downgrade to REFERENCE_UNRESOLVED |
| Complete supported LOV authority proves no match, or actual ambiguity remains | Identify CSV column and evidence; accept clarification in any language. Do not demand English or an exact display label; partial or parity-unverified absence is not proof of invalidity |
| Dynamic set collection incomplete or unavailable | Block membership validation; report retrieval/pagination failure separately from a proven invalid set. Do not invent a code or an active-date filter |
| Supplied set name matches exactly one distinct returned code | Derive SetCode and continue; do not ask for code clarification or code confirmation |
| Supplied set name matches multiple distinct returned codes | Show returned name/code/description candidates and ask which set is intended; never add a candidate solely because its code or description matches the input |
| Supplied set name has no match, but its text matches a code or description | Keep name-only resolution. Request a corrected name if no canonical code can be constructed; disclose any parity warning without declaring proven task invalidity. Do not use or ask to confirm the cross-field candidate |
| Explicit set code has no match, or explicit name and code disagree | Keep code-only resolution for the explicit code; request correction of the supplied field or conflicting pair, never a name fallback |
| Agent-generated SetCode lacks original name-resolution evidence | Recover the original set name from retained preparation context or clarify that name; the generated column does not prove explicit user code input. Never reread a Data Loader source to reconstruct intent |
| Target DFF authority or language import-eligibility parity missing | REFERENCE_UNRESOLVED, Warning, blocking=false; preserve proven supplied CSV representation, list skipped checks and needed evidence, continue all supported checks/preview without waiver. Do not infer validity from the blank template or stop the whole task |
| WTYPE_REFERENCE_MISSING | Complete scoped acquisition has zero matching identities; identify field and authority and ask for the intended reference |
| WTYPE_REFERENCE_AMBIGUOUS | Multiple candidate identities or conflicting segment mappings; show non-sensitive disambiguators and request the missing scope |
| WTYPE_REFERENCE_INCOMPATIBLE | Supported task authority proves identity incompatible, outside selected context, read-only or outside value constraints; identify the evidenced predicate. Installation/activation state alone does not prove translation-import incompatibility |
| WTYPE_REFERENCE_INACCESSIBLE | Authentication, authorization or transport failure; restore the declared read route, never report the reference absent |
| WTYPE_REFERENCE_INCOMPLETE | Failed page, missing required metadata, unfinished REST acquisition; retain request ID/stage and obtain complete evidence before preview |
| WTYPE_REFERENCE_CONTEXT | Target, identity, language, run or published metadata mismatch; reacquire in the intended scope |
| REFERENCE_UNRESOLVED | No supported DFF/reference membership authority or unverified task eligibility parity; Warning, blocking=false. Excludes required consumer-impact and translation-name collision evidence. Record field, preserved representation, skipped check and next evidence; continue supported checks only when required gates pass. Never fabricate codes/IDs or require developer tools/manual metadata/waiver |
| Package/import fails | Keep target, integrity and member/row evidence internal; report the actionable failure through Data Loader's prescribed output; no retry |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Identity/date/value failure | Correct input |
| Translation-name validation | Child resolver reports a collision or incomplete required collision evidence | Blocking; use input_validation for a proven collision or missing/invalid supplied evidence; preserve the original failure class for a failed supported baseline acquisition. No preview, waiver or automatic retry |
| Dependency | Required baseline/package or consumer-impact handoff/source operation missing | Blocking; stop affected import preparation, record failure_class=catalog_or_metadata_mismatch for an undeclared workflow source route, or input_validation for absent/invalid supplied evidence; preserve the original transport/auth/process failure class for a failed supported acquisition |
| REFERENCE_UNRESOLVED | Missing DFF/reference membership authority or unverified task parity without proven invalidity; excludes required consumer-impact evidence | Warning, blocking=false; preserve proven representation and continue remaining supported checks/preview |
| Conflict | Unsafe set-assignment removal, invalid child, or unsafe semantic/use impact | Correct/preserve |
| Unsupported | Delete/direct setup REST | Stop |
| Approval blocker | Submission requested without current Data Loader approval or with a missing/mismatched approved artifact or envelope | Stop before submission; use the loader's required validation/approval workflow; preparation alone is not approval |

## Disclosure Rules

For a Data Loader import, complete read-only task validation through Task Hook's
data-load route for the final immutable archive and verified persisted preflight.
Return ordered ruleResults before build-data-load-preview. Retain before/after
fields, child diffs, consumer impact, unresolved warnings and integrity evidence
internally. Do not display hashes, detailed previews or approval objects, or
create task-local copies of loader artifacts. Follow Task Hook's prescribed
validation-result persistence and pass its taskValidationEnvelope unchanged.

The task graph, including EXECUTION_GATE and RETURN_SUCCESS, completes before
upload approval; it checks validation/preparation, not the loader's later
approval. The declined graph outcome is reserved for a declined preparation
request. Data Loader alone owns approval, approved-archive verification and
submission. Accepted initiation ends the request without automatic polling,
log retrieval, re-export or saved loader result/failure artifacts. Later status
or verification requires an explicit request through the supported workflow.

| Gate | What Must Be Shown |
|---|---|
| Validation | Actionable validation issues; distinguish proven errors, unresolved warnings and skipped checks; retain detailed task evidence internally and never claim unperformed checks passed |
| Preview | Data Loader's prescribed approval-required report verbatim after task validation passes; retain the Task Hook preview internally; blockers receive no approval question and task validation adds no second approval |
| Result | Data Loader's prescribed accepted-submission or failure output; accepted submission is not verified completion. Report fresh-export/LOV and consumer checks only after the subsequent requested verification workflow completes; keep integrity values internal |

## Refusal Rules

Apply the existing set-removal design gate: zero remaining assignments alone is not a blocker. An explicitly requested final-assignment removal may proceed to Data Loader preview only when required consumer-impact evidence establishes safety and the target package contract supports the removal. Data Loader approval remains required before submission.

| Situation | What Must Not Happen |
|---|---|
| Required consumer-impact evidence unresolved | Do not import, show an approval question, waive the dependency through approval, manufacture a source contract, or request a manual snapshot as a workaround |
| Ambiguous identity or optional reference metadata unknown | Do not guess; unavailable DFF/reference membership authority alone stays nonblocking, while actual ambiguity or missing payload representation needs clarification |
| Set-assignment removal with unsafe downstream impact or unsatisfied required consumer-impact evidence | Do not import |
| Direct setup REST/delete | Do not infer support |
| Template/approval absent | Do not import |
| Failure | Do not retry/claim success |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WTYPE.EXECUTION_GATE | decision | 8 | execution_gate | ready->WTYPE.RETURN_SUCCESS;warning->WTYPE.RETURN_SUCCESS;not_ready->WTYPE.RETURN_ISSUES;declined->WTYPE.RETURN_REFUSAL | WTYPE.ENFORCE_DESIGN | stop | Return supported validation only with required impact evidence satisfied or not applicable; warnings and approval never clear a missing dependency |
| WTYPE.RETURN_SUCCESS | terminal | 9 | terminal | none | WTYPE.EXECUTION_GATE | continue | Supported validation/preparation complete before loader approval; return retained warnings and skipped checks without authorizing submission or claiming full reference validation |
| WTYPE.RETURN_ISSUES | terminal | 10 | terminal | none | none | continue | Correctable issue |
| WTYPE.RETURN_REFUSAL | terminal | 11 | terminal | none | none | continue | Unsupported/unsafe/declined action |
