# Manage Strategic Values Design Enforcement

Apply these mandatory gates after parent-first identity resolution and the
route-aware package verifier. SingleLookup requires one exact set and, when
code-specific, one code state. Package Export remains full-task and set-less;
Package Create, Update, Disable, or Import validates each changed row's set,
state lock, delta, and impact independently. REST_FALLBACK validates the same
reviewed rows through fresh reads and its dedicated exhaustion verifier.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm request and fixed identity | Preserve RequestMode, MOO_SETID_STRATEGIC_VALUE, and MOO_MANAGE_STRATEGIC_VALUES; require an explicit Common-versus-different set decision and one exact resolved set for SingleLookup, no selector for full-task Export, and one exact set per changed package row |
| 2 | Compare operation with current state | For SingleLookup, permit Create only for a missing code and Read, Update, Disable, or Delete only for one existing code; for Package Create, Update, Disable, or Import, enforce the matching rule independently on every changed row |
| 3 | Enforce mutation route | Prefer FSM and applicable CSV recovery for Create, Update, or Disable; only verified final exhaustion permits REST_FALLBACK through Apps Common with separate preview approval. Delete retains its explicitly selected REST exception |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| SingleLookup | Blocker | resolve_strategic_value_reference_set | SetSelectionDecision is missing; Common Set was inferred or resolves to a non-Common set; SetId/SetCode is malformed, unknown, cross-environment, ambiguous, or conflicts with another selector, BU/organization assignment, confirmed request, fresh export, or package row; or the parent reference group is missing/inconsistent/pagination-incomplete | Ask whether Common Set should be used or require a different exact set; complete ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES when needed, then rerun parent-first read-only resolution without substituting a set | Yes |
| FSM Package Create, Update, Disable, or Import | Blocker | verify_strategic_value_fsm_package | Any changed row lacks the fixed lookup type, exact set/code identity, expected-state lock, permitted minimal delta, impact evidence, or complete package validation | Correct the specific row or package evidence; validate all changed rows atomically without forcing one set | Yes |
| Package Export | Blocker | verify_strategic_value_fsm_package | The request requires a set selector, code, row delta, state lock, or impact, or the completed baseline is narrowed below the exact full task | Export and validate the complete MOO_MANAGE_STRATEGIC_VALUES task for the exact target and release without inventing row scope | Yes |
| SingleLookup Create | Blocker | resolve_strategic_value_lookup_state | The exact LookupCode already exists in the resolved set | Change the operation to Update or choose a unique code | Yes |
| SingleLookup Read, Update, Disable, or Delete | Blocker | resolve_strategic_value_lookup_state | No exact LookupCode exists in the resolved set | Supply an existing code or use Create when appropriate | Yes |
| SingleLookup Update, Disable, or Delete | Blocker | resolve_strategic_value_lookup_state | The preview is not bound to the returned child item identifier or item link | Rebuild the preview from the exact returned item | Yes |
| FSM SingleLookup Create, Update, or Disable | Blocker | verify_strategic_value_fsm_package | The immutable package does not contain exactly the reviewed lookup-code change plus its unchanged parent linkage, or its baseline, task identity, metadata contract, state lock, delta, impact, or PackageSha256 is missing or stale | Build the exact-task package with one reviewed code change and its unchanged support parent; preserve unrelated baseline rows. Data Loader owns its later preview and approval lifecycle | Yes |
| FSM Create using a header-only data baseline | Blocker | verify_strategic_value_fsm_package | Successful exact-target/task export evidence or current metadata-derived schema is missing, or the omitted parent is not resolved live with unchanged fields, or code absence is inferred from the export | Validate the data export and apply the task skill's Header-Only FSM Baselines and Parent Linkage procedure; an empty export alone is not a blocker | Yes |
| Every changed FSM lookup-code row | Blocker | verify_strategic_value_fsm_package | FND_APP_SET_ENABLED_LOOKUP.LookupType has no matching LookupType in the package parent CSV, or the parent configuration or resolved SetCode is changed | Require a matching unchanged parent row in FND_APP_SET_ENABLED_LOOKUP.csv and the exact resolved child SetCode; never hand off a child-only package | Yes |
| FSM Package Create, Update, Disable, or Import | Blocker | verify_strategic_value_fsm_package | The package task code, baseline, immutable ZIP, metadata-derived files/headers, any per-row set/state/delta/impact, or PackageSha256 is missing, stale, cross-environment, or changed | Rebuild and atomically validate the exact task package; Data Loader owns its later preview and approval lifecycle | Yes |
| Every SingleLookup mutation | Blocker | resolve_strategic_value_lookup_state | Business ownership, affected field, downstream or historical impact, delivered/custom safety, minimal delta, or immediate expected-state re-read is missing | Complete impact review and re-read the exact code immediately before handoff | Yes |
| SingleLookup Delete | Blocker | resolve_strategic_value_lookup_state | FSM is selected, REST was not explicitly selected, metadata does not permit deletion, or impact evidence is incomplete | Use Disable or complete the documented REST exception and separate approval | Yes |
| Inventory or Read | Blocker | resolve_strategic_value_lookup_state | Read-only lookup resolution is being treated as mutation authorization | Return sanitized current state only | Yes |
| REST_FALLBACK Create, Update, or Disable | Blocker | verify_strategic_value_rest_fallback | RestFallbackEligible is not true; same-target failure/recovery evidence is missing; CSV is usable or repairable; prior submissions are running, uncertain, partially applied, or incompletely diagnosed; or the route bypasses input/catalog/auth/set/assignment/context/approval constraints | Exhaust applicable CSV recovery and reconcile every prior submission. Return verified state without a write if all rows are applied; partial results require a newly reviewed remaining-change request | Yes |
| Every REST_FALLBACK row | Blocker | resolve_strategic_value_lookup_state | Any row lacks exact task/lookup/set/code identity, fresh reviewed pre-state, operation/state compatibility, permitted minimal delta, write privileges, editability, impact, same-target canonical endpoint, or unique batch identity | Resolve and review each row before preview; never infer write authority from readable data, change parent/set assignments, or reinterpret Create as upsert | Yes |
| Every REST submission | Blocker | verify_strategic_value_rest_fallback | Exact method/endpoint/body/verification GET or immutable preview fingerprint changed, approval is missing/stale or borrowed from export/Data Loader, or a prior REST result is failed/uncertain/unverified | Prepare and approve a separate exact REST preview immediately before execution. Submit each displayed request once and stop on first failure/uncertainty; reconcile and obtain new approval before any further write. REST_DELETE follows its separate contract without the fallback verifier | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_manage_strategic_values_parent | Every request | Exact MOO_SETID_STRATEGIC_VALUE parent, returned nonblank ReferenceGroupName, task-scope and editability evidence, canonical parent link | ora_reference_lookups.md |
| resolve_strategic_value_reference_set | Before SingleLookup inventory, read, or preview | One exact SetId and SetCode, plus assignment evidence when a business unit was supplied | ora_reference_lookups.md |
| resolve_strategic_value_lookup_state | Before returning SingleLookup current state or previewing Create, Update, Disable, or Delete | Current code state and returned child item identifier or item link when present | ora_reference_lookups.md |
| verify_strategic_value_fsm_package | Before Package Export review or an FSM handoff | For Export, exact full-task baseline identity and receipt; for SingleLookup mutation, exactly one matching reviewed row; for Package mutation or Import, every changed row's exact set, state lock, delta, and impact | ora_reference_lookups.md |
| verify_strategic_value_rest_fallback | Before REST_FALLBACK preview | Documented final CSV exhaustion, same-target failure/recovery receipt, fresh per-row resolution, terminal/reconciled prior import evidence when submitted, unchanged reviewed pre-state, and RestFallbackEligible=true | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.STRATEGIC.DESIGN | decision | 8 | design_enforcement | pass->OPP.STRATEGIC.GATE;blocked->OPP.STRATEGIC.RETURN_MISSING;failed->OPP.STRATEGIC.RETURN_FAILED | OPP.STRATEGIC.VERIFY_PACKAGE | stop | Enforce explicit set scope, parent identity, per-row operation/state, immutable identity, impact and minimal deltas. FSM requires package readiness; REST_FALLBACK requires the dedicated verifier's eligible outcome, write privileges and a separate immutable preview; REST_DELETE retains its separate contract |
