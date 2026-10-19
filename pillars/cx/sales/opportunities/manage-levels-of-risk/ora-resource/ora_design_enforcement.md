# Manage Levels of Risk Design Enforcement

Apply these mandatory gates after parent-first identity resolution and the
route-aware package verifier. SingleLookup requires one exact set and, when
code-specific, one code state. Package Export remains full-task and set-less;
Package Create, Update, Disable, or Import validates each changed row's set,
state lock, delta, and impact independently.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm request and fixed identity | Preserve RequestMode, MOO_SETID_RISK_LEVEL, and MOO_MANAGE_LEVELS_OF_RISK; require an explicit Common-versus-different set decision and one exact resolved set for SingleLookup, no selector for full-task Export, and one exact set per changed package row |
| 2 | Compare operation with current state | For SingleLookup, permit Create only for a missing code and Read, Update, Disable, or Delete only for one existing code; for Package Create, Update, Disable, or Import, enforce the matching rule independently on every changed row |
| 3 | Enforce mutation route | Use FSM for Create, Update, or Disable; require an explicitly selected and separately approved REST exception for Delete |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| SingleLookup | Blocker | resolve_risk_reference_set | SetSelectionDecision is missing; Common Set was inferred or resolves to a non-Common set; SetId/SetCode is malformed, unknown, cross-environment, ambiguous, or conflicts with another selector, BU/organization assignment, confirmed request, fresh export, or package row; or the parent reference group is missing/inconsistent/pagination-incomplete | Ask whether Common Set should be used or require a different exact set; complete ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES when needed, then rerun parent-first read-only resolution without substituting a set | Yes |
| Package Create, Update, Disable, or Import | Blocker | verify_risk_fsm_package | Any changed row lacks the fixed lookup type, exact set/code identity, expected-state lock, permitted minimal delta, impact evidence, or complete package validation | Correct the specific row or package evidence; validate all changed rows atomically without forcing one set | Yes |
| Package Export | Blocker | verify_risk_fsm_package | The request requires a set selector, code, row delta, state lock, or impact, or the completed baseline is narrowed below the exact full task | Export and validate the complete MOO_MANAGE_LEVELS_OF_RISK task for the exact target and release without inventing row scope | Yes |
| SingleLookup Create | Blocker | resolve_risk_lookup_state | The exact LookupCode already exists in the resolved set | Change the operation to Update or choose a unique code | Yes |
| SingleLookup Read, Update, Disable, or Delete | Blocker | resolve_risk_lookup_state | No exact LookupCode exists in the resolved set | Supply an existing code or use Create when appropriate | Yes |
| SingleLookup Update, Disable, or Delete | Blocker | resolve_risk_lookup_state | The preview is not bound to the returned child item identifier or item link | Rebuild the preview from the exact returned item | Yes |
| SingleLookup Create, Update, or Disable | Blocker | verify_risk_fsm_package | The immutable package does not contain exactly the reviewed set/code row, or its baseline, task identity, metadata contract, state lock, delta, impact, or PackageSha256 is missing or stale | Rebuild the one-row exact task package and hand it to Data Loader; Data Loader owns its later preview and approval lifecycle | Yes |
| Package Create, Update, Disable, or Import | Blocker | verify_risk_fsm_package | The package task code, baseline, immutable ZIP, metadata-derived files/headers, any per-row set/state/delta/impact, or PackageSha256 is missing, stale, cross-environment, or changed | Rebuild and atomically validate the exact task package; Data Loader owns its later preview and approval lifecycle | Yes |
| Every SingleLookup mutation | Blocker | resolve_risk_lookup_state | Business ownership, affected field, downstream or historical impact, delivered/custom safety, minimal delta, or immediate expected-state re-read is missing | Complete impact review and re-read the exact code immediately before handoff | Yes |
| SingleLookup Delete | Blocker | resolve_risk_lookup_state | FSM is selected, REST was not explicitly selected, metadata does not permit deletion, or impact evidence is incomplete | Use Disable or complete the documented REST exception and separate approval | Yes |
| Inventory or Read | Blocker | resolve_risk_lookup_state | Read-only lookup resolution is being treated as mutation authorization | Return sanitized current state only | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_manage_levels_of_risk_parent | Every request | Exact MOO_SETID_RISK_LEVEL parent, returned nonblank ReferenceGroupName, task-scope and editability evidence, canonical parent link | ora_reference_lookups.md |
| resolve_risk_reference_set | Before SingleLookup inventory, read, or preview | One exact SetId and SetCode, plus assignment evidence when a business unit was supplied | ora_reference_lookups.md |
| resolve_risk_lookup_state | Before returning SingleLookup current state or previewing Create, Update, Disable, or Delete | Current code state and returned child item identifier or item link when present | ora_reference_lookups.md |
| verify_risk_fsm_package | Before Package Export review or an FSM handoff | For Export, exact full-task baseline identity and receipt; for SingleLookup mutation, exactly one matching reviewed row; for Package mutation or Import, every changed row's exact set, state lock, delta, and impact | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.RISK.DESIGN | decision | 7 | design_enforcement | pass->OPP.RISK.GATE;blocked->OPP.RISK.RETURN_MISSING;failed->OPP.RISK.RETURN_FAILED | OPP.RISK.VERIFY_PACKAGE | stop | Enforce the explicit Common-versus-different set decision, RequestMode-aware parent identity, SingleLookup or per-row operation/state rules, immutable identifiers, business impact, minimal delta, fixed task routing, and REST-delete-only policy after package verification |
