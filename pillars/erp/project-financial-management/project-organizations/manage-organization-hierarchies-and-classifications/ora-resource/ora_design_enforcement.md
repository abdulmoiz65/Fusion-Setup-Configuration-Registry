# Manage Organization Hierarchies and Classifications Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm enterprise scope | Bind the change to one target, accountable owner, approved design, impact, window, and rollback expectation |
| 2 | Protect target state | Reconcile current hierarchy, classifications, and default hierarchy before update or import |
| 3 | Enforce valid selection | Require one resolved hierarchy type and at least one resolved classification |
| 4 | Protect non-None hierarchy | Require one valid tree, active version, and starting organization |
| 5 | Enforce route boundary | Limit import to target-template-backed behavior and report unproven replacement or removal as unsupported automation |
| 6 | Protect approval | Bind execution to one immutable preview and submit once |
| 7 | Keep follow-up separate | Route Maintain Project Organizations as its own scoped task when required |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Error | | Target, owner, approved outcome, impact, window, or rollback expectation is missing | Complete the approved enterprise scope | Yes |
| Update or import | Error | resolve_current_org_hierarchy_setup | Current target state is stale, ambiguous, or unreconciled | Refresh and reconcile target state | Yes |
| Every change | Error | resolve_allowed_hierarchy_type | Hierarchy type cannot be resolved to one valid value | Provide a clearer hierarchy outcome | Yes |
| Every change | Error | resolve_available_org_classifications | Selected classification set is empty or contains an unresolved or ambiguous value | Retain at least one resolved classification | Yes |
| Organization or department hierarchy | Error | resolve_default_org_hierarchy | Tree, active version, or starting organization is missing or invalid | Resolve one complete target combination | Yes |
| FSM import | Error | verify_org_hierarchy_fsm_package | Import would replace a different existing hierarchy type, remove classifications, or use unverified mappings | Narrow the import to proven behavior or return the affected operation as unsupported | Yes |
| FSM import | Error | verify_org_hierarchy_fsm_package | Template metadata, members, headers, translations, operation behavior, preview, or checksum is missing or changed | Refresh target evidence and generate a new preview | Yes |
| Direct REST, internal service, browser automation, or hand-built package is proposed | Error | | No supported customer contract is evidenced | Retain the target-template-gated FSM route or return unsupported | No |
| Hierarchy change requires maintenance | Error | resolve_current_org_hierarchy_setup | Maintain Project Organizations would be submitted without separate task scope and approval | Hand off to the separate setup task | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_current_org_hierarchy_setup | Update, import, hierarchy-change impact, and verification | Current hierarchy, classifications, default hierarchy, impact, verification | ora_reference_lookups.md |
| resolve_allowed_hierarchy_type | Every hierarchy decision | Desired hierarchy type | ora_reference_lookups.md |
| resolve_available_org_classifications | Every classification decision | Desired set, additions, removals, preserved values | ora_reference_lookups.md |
| resolve_default_org_hierarchy | Organization or department hierarchy | Tree, active version, starting organization | ora_reference_lookups.md |
| verify_org_hierarchy_fsm_package | FSM import | Target template contract, operation, members, row counts, checksum, process result | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OHCL.ENFORCE_DESIGN | decision | 8 | design_enforcement | pass->OHCL.EXECUTION_GATE;blocked->OHCL.HANDLE_ERROR;unsupported->OHCL.REFUSED | OHCL.APPLY_DEFAULTS | stop | Before controlled import approval |

## Refined Best-Practice Gate

The registry's design-enforcement node evaluates the controls distributed across this task's standard `ora-resource` files. Record `control_id`, `status` (`pass`, `fail`, `needs_input`, or `not_applicable`), evidence, and any approved exception for every applicable control. Recalculate source-snapshot population counts from the target.

- **BP-011 — Blocking control:** Require the same hierarchy type in HCM and Project Financial Management. When HCM is the enterprise hierarchy source, refuse a competing PFM structure unless an approved source-of-truth exception exists.
- **BP-012 — Blocking control:** Classify organizations narrowly: owning only for project/task owners; expenditure only for cost-incurring organizations; and asset, partner, manufacturing, business-unit, or project-unit classifications only when the operating model requires them.
- **BP-013 — Blocking control:** Do not derive expenditure eligibility automatically from owning eligibility; require independent decisions for the two roles.
