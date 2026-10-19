# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Protect identity/immutables | Exact schedule and immutable set/type/currency remain valid |
| 2 | Select route/references | Require route coverage for writes; complete supported reference checks and carry explicit unresolved warnings |
| 3 | Validate lines | Keys, dates, values/UOM, overlap, and precedence pass |
| 4 | Protect active use/delete | Used fields/consumers are safe; destructive intent explicit |
| 5 | Protect preview/approval | Route, IDs, payload/package, diff, and checksum are immutable |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Create/update/copy | Blocker | find_rate_schedule | Duplicate/ambiguous or immutable-header change | Correct identity/create replacement | Yes |
| Route | Blocker | verify_rate_route | Method/field/child/DFF coverage incomplete or route changed | Select complete route and re-preview | Yes |
| References | Blocker | resolve_rate_references | Complete supported authority proves no match, actual ambiguity, inactive status where applicable, or dependency incompatibility | Resolve user intent in any language to one eligible canonical member | Yes |
| Missing LOV authority/parity | Warning | record_unresolved_rate_reference | None; blocking=false; do not reinterpret as missing dependency or design violation | Preserve proven representation, disclose skipped check and continue remaining supported checks/preview without waiver | No invented replacement |
| Same-key effective intervals | Blocker | resolve_rate_lines | Requested/current intervals overlap including a shared endpoint for the same fully qualified subtype key | End the prior interval before the new start or correct the requested range; preserve differently qualified keys | Yes |
| Delete schedule header | Blocker | find_rate_schedule | Current header contains one or more rate schedule lines, even with zero consumers | Report the observed PJF-2235397 via ora_error_handling.md; no automatic child deletion or cascade | No automatic correction |
| Delete individual line | Blocker | resolve_rate_use | No supported line-delete operation/eligibility evidence, disabled/unavailable UI action, or protected use | Return the exact operation/eligibility gap; do not infer eligibility from a toolbar or from zero consumers alone | No automatic cascade |
| Delete/protected mutation | Blocker | resolve_rate_use | No stable ID, active consumers, or field immutable while used | End-date/preserve or resolve use | Yes |
| Execution | Blocker | verify_rate_route | Preview/approval stale or route mismatch | Rebuild/reapprove | Yes |
| REST request contract | Blocker | verify_rate_route | Any field is supported only by GET evidence, belongs to another endpoint/subtype, is unknown, or has been rejected by this target operation | Correct endpoint/shape and prove per-field request support before preview | Yes |
| Staged REST create | Blocker | verify_rate_route | Header and child are not both validated and included in the approved plan, or parent-ID binding/partial-success behavior is absent | Preview the complete ordered call set and bind the returned parent ID explicitly | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_rate_schedule | Create/update/copy/delete | Stable identity/full baseline | ora_reference_lookups.md |
| verify_rate_route | Every write | Methods/fields/children/DFF or FSM contract | ora_reference_lookups.md |
| resolve_rate_references | Header/line values | Effective stable IDs/dependencies | ora_reference_lookups.md |
| resolve_rate_lines | Line changes | Canonical keys/intervals/values | ora_reference_lookups.md |
| resolve_rate_use | Protected mutation/delete | Consumer counts/protection | ora_reference_lookups.md |
| record_unresolved_rate_reference | Missing supported LOV authority/parity | Proven representation, skipped check, warning and next evidence | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RATE.ENFORCE_DESIGN | decision | 8 | design_enforcement | pass->RATE.EXECUTION_GATE;warning->RATE.EXECUTION_GATE;blocked->RATE.RETURN_REFUSAL;failure->RATE.RETURN_ISSUES | RATE.RESOLVE_DEPENDENCIES | stop | After every supported check, with unresolved warnings preserved |

## Refined Best-Practice Gate

This node evaluates only this file's design policies; input, default, lookup, dependency and error behavior each have their own owning node/file. Record control_id, status (pass, fail, needs_input, warning, or not_applicable), evidence, and any approved exception for every applicable policy. Missing LOV authority is an explicit nonblocking warning, not a failed blocking control or a research-waiver requirement. The following BP controls are FSCR design/operational guidance, not messages emitted by Oracle. Never invent a UI or service rejection to justify them.

- **BP-071 — Advisory:** Recommend job schedules for broad labor populations. Preserve the user's selected Person schedule; individual actual cost, union/local arrangements, specialist rates, payroll costing and planning intent are context, not new mandatory inputs or an automatic type replacement.
- **BP-072 — Conditional FSCR history policy:** When established consumer protection or an explicit project history-preservation policy applies, end-date the old line and create a new effective line instead of overwriting protected history. The UI accepted changing an unused historical Resource Class fixture from 10 to 12; a past date alone is not an Oracle immutability error. Otherwise recommend preserving history and disclose the impact in preview; do not invent active use.
- **BP-073 — Blocking control:** Use the least-specific valid employee key: person only for invariant rates, person plus job for role variation, and person plus job plus organization only when organization changes cost.
- **BP-075 — Advisory:** Record ownership when supplied. It is not a Fusion payload field or required setup input; absence does not block validation, preview or creation, or trigger clarification. Execution approval belongs to the selected core workflow.
- **BP-076 — Advisory:** Record purpose when supplied or evident from the schedule name, description, or business request. Purpose is not a Fusion payload field or required setup input; do not request a separate confirmation or block validation, preview, or creation when it is absent. Recommend reviewing rate derivation before reusing a schedule across costing, billing, planning, budget, forecast, or transfer-price contexts.
- **BP-077 — Blocking control:** Reject a supplied nonlabor refinement only when complete supported authority proves incompatibility. Missing resource/organization authority or unverified parity is REFERENCE_UNRESOLVED, Warning, blocking=false; absent optional qualifiers do not fail this policy. Lookup mechanics stay in ora_reference_lookups.md.
- **BP-078 — Blocking control:** Use resource-class schedules for high-level planning only and do not substitute them for actual-costing controls.

Header deletion with children and consumer protection are distinct checks. The blocked header deletion did not remove any data. Empty-header deletion and actual line deletion were not executed in the recorded UI run. Toolbar presence, selected-row state, enabled state and operation eligibility are separate evidence; the user's observation that some lines lack Delete remains unresolved. Never claim that toolbar placement explains that restriction.
