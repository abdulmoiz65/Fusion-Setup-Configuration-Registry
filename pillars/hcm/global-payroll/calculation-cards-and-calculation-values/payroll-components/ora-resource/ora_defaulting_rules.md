# Payroll Components Defaulting Rules

Apply defaults only after the operation, LDG, and required business references
are resolved. Bind each applied default into the internal approval-bound Task
Hook preview and immutable plan; `core/data-loader` owns the user-facing report.
A default never supplies consent and never carries from an earlier Create
operation.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| UseAllTaxUnits | Lowercase string true | Parent Create | No; an explicit false or specific-tax-unit request is unsupported rather than overwritten | |
| Sequence | Integer 1 | Reference Child Create and the user omitted sequence | No; preserve an explicit positive integer | |
| NavigationUse | Lowercase string false | Reference Child Create and Display in Overview was omitted | No; bind No to task validation while core owns user-facing output | |
| UsageType | T | Wage Basis Rule Reference is selected | Yes only by changing the business journey selection before Task Hook validation | map_reference_journey |
| UsageType | C | Calculation Factor Reference is selected | Yes only by changing the business journey selection before Task Hook validation | map_reference_journey |
| DeductionTypeId | Exact current parent ID | Reference Child Create | No; route-owned and internal | find_payroll_component |
| LegislativeDataGroupId | Exact current parent LDG ID | Reference Child Create | No; route-owned and internal | find_payroll_component |
| ContextId | Exact selected context ID | Reference Child Create | No; resolve from the business label | find_reference_context |
| SourceSystemId | Fresh collision-resistant DAT-safe operation identifier of at most 100 characters | Reference Child Create after Source System Owner selection | No; allocate once for this operation and retain internally with the resolved owner | resolve_active_source_owner |

## No-Default Inputs

Do not invent or inherit a Deduction Code, Component Name, Display Sequence,
LDG, Component Group, parent, reference journey, context, source owner, specific
tax reporting unit, date, ID, link, object version, or approval. If a required
user-owned value is absent, remain in `collecting` or `resolving` and return
`NEEDS_INPUT` after the applicable read-only lookup.

## Application Rules

| Situation | What Happens |
|---|---|
| A new Create command begins | Allocate new operation state, re-resolve every reference, and recompute defaults. |
| A default depends on an unresolved or ambiguous parent | Do not apply it; return the lookup classification. |
| An internally resolved child parent ID or LDG conflicts with the active parent | Return CATALOG_MISMATCH; never ask the user to reconcile raw IDs. |
| Core supplied an already prepared immutable archive for Task Hook validation | Do not rewrite it; require every declared default and derived value to be present exactly, or return CATALOG_MISMATCH for fresh core preparation. |
| A default or selected value changes after Task Hook validation | Rebuild through core/data-loader, invalidate the prior envelope and approval, and rerun task validation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PCOMP.APPLY_DEFAULTS | decision | 4 | apply_default | applied->PCOMP.VALIDATE_NATIVE_CONTRACT;not_required->PCOMP.VALIDATE_NATIVE_CONTRACT;read_only->PCOMP.EXECUTION_GATE;invalid->PCOMP.HANDLE_ERROR | PCOMP.RESOLVE_REFERENCES | stop | Input and references are ready; read-only requests require no defaults and bypass Create contract validation |
