# Design Enforcement

For offline dynamic checks, apply the task's explicit non-blocking deferral policy from reference lookups. A known constraint violation still blocks. An unknown membership, use state or supplemental eligibility condition is not a proven violation: record deferred_to_fusion and continue normal approval/upload processing without claiming that check passed.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Protect identity/set/dates | Check name/set identity and dates using available evidence; missing offline set membership is deferred |
| 2 | Preserve in-use semantics | Block proven protected post-use mutations; unknown offline state is deferred |
| 3 | Enforce conditional groups | Burdening, sponsored, capitalization rules |
| 4 | Preserve child collections | Explicit translation/class-category diffs only |
| 5 | Protect route/package | FSM, exact package, preview, approval |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Create | Blocker | find_project_type | Duplicate name+set | Choose new identity or update | Yes |
| Update | Blocker | resolve_project_type_use | Protected field changes after use | Preserve field | No |
| Burdening | Blocker | resolve_project_type_references | Required schedule value missing, schedule proven invalid, null serialized BurdenAccountFlag after defaulting, or proven inconsistent accounting | Complete/correct options; an omitted create component choice defaults N and is not a missing user decision | Yes |
| Separate-item burdening | Blocker |  | Explicit BurdenAccountFlag Y or an explicit indirect destination request contradicts separate-item accounting | Explain that D creates burden items on the raw-cost project/task; clarify conflicting intent. Do not require the disabled component/destination fields or fabricate a destination | Yes |
| Same-item component expenditure items | Blocker | resolve_project_type_references | BurdenAmtDisplayMethod S with BurdenAccountFlag Y but no destination project, or a proven invalid destination | Supply the component destination project; Task Name is optional. Do not apply this requirement to D or BurdenAccountFlag N | Yes |
| Sponsored transition | Blocker | resolve_project_type_use | Re-enable burdening after prohibited in-use deselection | Preserve current state | No |
| Capitalization | Blocker | resolve_project_type_references | Required/conditional asset option invalid, including CipGroupingMethodCode EI with VendorInvoiceGroupingCode G | Resolve compatible treatment; preserve explicit M or N rather than forcing N | Yes |
| Class categories | Blocker | resolve_project_type_references | Duplicate/invalid category | Correct child rows | Yes |
| Capitalization enabled | Blocker | resolve_project_type_capital_cost | CapitalCostTypeCode missing, or B with TotalBurdenedJournalFlag N | Supply valid cost type and required accounting configuration; do not silently change cost type | Yes |
| Capitalization enabled or disabled | Blocker | resolve_project_type_asset_grouping | Grouping method missing when enabled, or nonnull when disabled | Apply the documented capitalization applicability | Yes |
| Capitalization disabled | Blocker | resolve_project_type_references | AssetAllocationMethod or CapitalEventProcessing differs from N; complete-asset, override-assignment, interest-override or automatic-asset flags differ from N; supplier grouping differs from G; capital cost type, grouping or interest schedule is nonnull; or automatic allocation differs from ALL_COSTS | Enforce the disabled-capitalization entity contract; preserve omitted update values and reject an inconsistent request rather than silently resetting it | Yes |
| Supplier treatment changes G to N, N to G, N to M, or M to N | Blocker | resolve_project_type_use | Transferred asset lines are proven to exist | Preserve treatment when transfer state proves restriction; otherwise defer unknown state; G to M and M to G are not covered by this specific restriction | No |
| Class-category assignment change | Blocker | resolve_project_type_use | Duplicate parent/category identity or changed assignment on an in-use type | Preserve protected assignment and correct duplicate identity | No |
| Translation rows supplied | Blocker | resolve_project_type_languages | Duplicate resolved language rows for one parent or mutation of insert-only Language identity | Preserve identity and require an explicit supported translation-row change | No |
| Dynamic reference or mode authority missing | Warning | resolve_project_type_references | None solely from missing offline data source, supplemental eligibility or seeded meanings for a proven control domain | State it has no data source where applicable; record non-blocking deferred_to_fusion and continue with supplied CSV-ready values | No data correction needed; do not invent values |
| Direct REST/delete | Blocker |  | No supported contract | Use FSM; do not delete | No |
| Import | Blocker | verify_project_type_package | Contract/approval invalid | Regenerate/approve | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_project_type | Create/update | Baseline/children | ora_reference_lookups.md |
| resolve_project_type_use | Protected changes | Use state | ora_reference_lookups.md |
| resolve_project_type_references | Referenced groups | Resolved IDs/codes | ora_reference_lookups.md |
| verify_project_type_package | Import | Contract/checksum | ora_reference_lookups.md |
| resolve_project_type_capital_cost | Capitalization choices | Canonical capital cost code | ora_reference_lookups.md |
| resolve_project_type_asset_grouping | Capitalization applicability | Canonical asset grouping code | ora_reference_lookups.md |
| resolve_project_type_supplier_grouping | Supplier treatment | Canonical combined control value | ora_reference_lookups.md |
| resolve_project_type_languages | Translation assignments | Canonical eligible language identities | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PTYPE.ENFORCE_DESIGN | decision | 7 | design_enforcement | pass->PTYPE.EXECUTION_GATE;blocked->PTYPE.RETURN_REFUSAL;failure->PTYPE.RETURN_ISSUES | PTYPE.RESOLVE_DEPENDENCIES | stop | Before import approval |

## Refined Best-Practice Gate

The registry's design-enforcement node evaluates the controls distributed across this task's standard `ora-resource` files. Record `control_id`, `status` (`pass`, `fail`, `needs_input`, or `not_applicable`), evidence, and any approved exception for every applicable control.

- **BP-028 — Readiness recommendation:** Keep project types purpose-based and flag known near-duplicates for review. Consider classifications, templates, organizations and transaction controls for other variation. A different name is still subject to the exact name/set duplicate gate; do not require proof of fundamental differentiation or an extra rationale to create an otherwise valid requested type.
- **BP-030 — Blocking control:** Every burden-enabled type requires a compatible default cost burden schedule and a resolved project/task override setting. Preserve explicit choices. On create, an omitted CostSchOverrideFlag resolves to N through Standard Defaults; disclose that default in the immutable preview. On update, preserve the baseline value when omitted. The resolved setting satisfies this control before preview; omission alone is not a needs_input condition. Loading still requires the selected executor's approval of the exact preview and artifact. Disable overrides where uniform internal costing is required.
- **BP-031 — Readiness recommendation:** Review burden-code expenditure-type mappings before downstream costing/accounting use. Missing mapping evidence does not block creating the project type. Keep the two modes distinct: S plus BurdenAccountFlag Y sends component items to an indirect destination; D creates separate burden items on the raw-cost project/task and does not require that destination or component checkbox.
- **BP-034 — Blocking control:** For sponsored types, treat award and award-project burden defaults as the primary governance point and do not assume ordinary project/task override behavior applies.

## Required Design Evidence

- **BP-029 — Required evidence:** Record intended inherited financial behavior from the requested flags, method, schedule and override choices plus disclosed create defaults; no separate design document is required for a task-scoped create. Once a type is used by a project, protect its immutable semantics and use retirement/versioning rather than mutation.
- **BP-032 — Required evidence:** For capitalization-enabled types, document raw-versus-burdened CIP, asset grouping, asset-definition requirement, supplier-invoice treatment, and capitalized-interest policy.

## Source and Policy Classification

See [Source Evidence Index](ora_reference_lookups.md#source-evidence-index). SRC-EO/SRC-EOIMPL support unique identity, protected-use, capitalization consistency, EI/G rejection and the four transferred-asset transition restrictions. SRC-DOC supports the broad schedule, override, capitalization and classification decisions.

BP-028 through BP-035 are FSCR design/evidence controls, not statements that Oracle enforces every control as an application constraint. BP-030 and BP-032 follow SRC-DOC's decision guidance. BP-028, BP-031 and BP-033 are non-blocking readiness recommendations: record missing evidence as readiness_not_assessed, not needs_input or deferred_to_fusion. Do not require a policy exception merely to create the type, invent Oracle API requirements, or claim operational readiness from package review alone. SRC-DOC and SRC-UI-SEPARATE distinguish separate-item burdening from same-item component routing.
