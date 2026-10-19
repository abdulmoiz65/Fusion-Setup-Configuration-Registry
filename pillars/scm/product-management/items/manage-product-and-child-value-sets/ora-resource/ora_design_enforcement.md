# Manage Product and Child Value Sets Design Enforcement

Product value sets define the allowed values for Product Hub attributes. Child
value sets support SKU variants through a subset of an independent value set.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Purpose gate | Confirm that the value set supports a constrained Product Hub attribute or a documented SKU-variant requirement |
| 2 | Definition gate | Confirm the code, module, validation type, and data type |
| 3 | Child gate | For a subset child, confirm the independent parent and its populated values |
| 4 | Readiness gate | Return validation readiness only; this skill has no write execution contract |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every value set request | Error | | The request lacks a defined Product Hub attribute purpose or SKU-variant purpose | Document the attribute or variant use before continuing | Yes |
| Every value set request | Error | | The validation type or value data type is outside Oracle's documented seeded values | Select a documented validation type and data type | Yes |
| ValidationType is Subset | Error | resolve_parent_independent_value_set | The parent is absent, ambiguous, belongs to a different supplied module, is not Independent, or has no intended variant values | Create or populate the independent parent, then revalidate the subset | Yes |
| Ready for setup execution | Error | | The request relies on this validation skill as a write contract | Route setup execution through the selected FSM workflow and its required preview and approval gates | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_parent_independent_value_set | ValidationType is Subset or a child SKU-variant value set is requested | Exact parent value-set code, module, validation type, and value configuration receipt | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VSET.ENFORCE_PARENT_DESIGN | decision | 25 | design_enforcement | passed->VSET.READY_FOR_EXECUTION;blocked->VSET.HANDLE_ERROR | VSET.RESOLVE_TASK | stop | Phase 1 creates only the independent parent and its values for the documented size-value subset relationship |
| VSET.ENFORCE_DESIGN | decision | 40 | design_enforcement | passed->VSET.READY_FOR_EXECUTION;blocked->VSET.HANDLE_ERROR | VSET.CHECK_DEPENDENCIES | stop | Before returning setup-validation readiness |
