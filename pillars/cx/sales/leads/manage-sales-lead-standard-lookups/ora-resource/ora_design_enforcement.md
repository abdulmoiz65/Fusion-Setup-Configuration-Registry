# Design Enforcement

## Mandatory Gates

| Gate | Pass Condition | Block Condition |
|---|---|---|
| Inventory completeness | Every documented/export-only standard candidate has resolved, not_found, or lookup_error status and complete paginated codes | Export-only or silently incomplete inventory |
| Task scope | Exact type resolves at standardLookups and is not a Set ID type | Set-enabled type, fuzzy identity, or wrong lookup category |
| Parent boundary | Existing parent is read-only and only its lookupCodes child is mutated | Lookup type create/update/delete or parent-field write |
| Exact identity | LookupType and LookupCode are case-sensitive, safe path keys and returned identities agree | Ambiguous, mismatched, or guessed key |
| CRUD selection | Absent code plus AddCode selects POST; existing code plus Update/Disable selects PATCH; safe existing code plus Remove selects DELETE | Upsert hides state, wrong method for state, or missing target |
| Minimal body | POST contains identity, Meaning, and approved mutable fields; PATCH contains only changed mutable fields; DELETE has no body | Audit, parent, key mutation, module, ownership, translation, BOSS, or unsupported fields |
| Duplicate/state lock | AddCode remains absent; existing-code fingerprint remains unchanged immediately before execution | Duplicate appeared, row changed, or target disappeared |
| Effective dates | Start date is not after end date and inactive effect is disclosed | Invalid or undisclosed availability state |
| Meaning/translation | Translation inventory and language impact are disclosed for Meaning changes | Base meaning is changed as though language-neutral or translations are written |
| Display sequence | Omitted or a positive integer; collisions are disclosed | Invalid integer or UI ordering guarantee |
| Delete safety | Positive customer-created evidence and reference-impact disclosure exist | Delivered/seeded/uncertain ownership or undisclosed impact |
| Approval binding | Complete preview digest matches environment, method, endpoint, identity, state, and body/delete effect | Vague, stale, or route-mismatched approval |
| Mutation route | Every code mutation uses core.fusion-api.apps-common | FSM, Data Loader, setup import, browser, curl, or task-local HTTP |
| Verification | Exact post-call code read confirms approved fields or deletion | HTTP acceptance alone or skipped read-back |
| Bulk behavior | Unique ordered targets execute sequentially and stop on first failure | Parallel writes, duplicate targets, continue-after-failure, or rollback promise |

## Additional Rules

- Export omission never blocks Apps Common lookup-code CRUD.
- Routine AddCode and non-impactful UpdateCode do not require a business owner,
  affected-field narrative, historical-use assessment, or downstream-consumer
  list.
- Require impact evidence only for DisableCode, RemoveCode, Meaning changes, or
  another change that can affect availability or existing references.
- Translation writes and lookup type mutations remain unsupported.
- Never retry or compensate for a write automatically.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SLL.DESIGN | decision | 5 | design_enforcement | pass->SLL.EXECUTION_GATE;fail->SLL.RETURN_ISSUES | SLL.ROUTE | stop | Enforce complete read evidence, standard-task scope, exact identity, deterministic code CRUD method, minimal request, duplicate/current-state lock, conditional impact/delete safety, approval binding, Apps Common routing, and verification |
