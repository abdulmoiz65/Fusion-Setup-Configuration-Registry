# Manage Sales Stage Phase Codes Design Enforcement

These rules preserve documented Sales behavior and prevent unrelated runtime
product-line concepts from being treated as setup metadata.

## Enforcement Order

| Sequence | Step | What Must Happen |
| --- | --- | --- |
| 1 | Validate phase-code design | Use lookup-code rows under the fixed MOO_STAGE_PHASE_CD lookup type and validate the requested identity, enabled state, sequence, and effective dates |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
| --- | --- | --- | --- | --- | --- |
| Creating, updating, or disabling a sales stage phase code | Blocker |  | The request targets a lookup type other than `MOO_STAGE_PHASE_CD`, reuses a Lookup Code for a new record, has no intended field change for an update, Disable does not set Enabled to No, or has an invalid enabled, sequence, or effective-date design | Use the fixed `MOO_STAGE_PHASE_CD` lookup type, retain one unique Lookup Code per phase, and correct the requested row before package preparation | Yes |
| Delete | Blocker |  | No task-specific source proves a safe deletion semantic for `MOO_STAGE_PHASE_CD` | Mark Delete unsupported; ask the requester to select Disable or an end-date Update when the fresh export supports it, then review that new delta | No |

| Every mutation or changed Import row | Blocker | resolve_stage_phase_code_state | Fresh Create absence or exact existing Update/Disable state, parent editability/security, catalog identity, write privileges, minimal delta or stage/reporting impact is missing; requested identity changes | Resolve each exact standard code and review intended fields/impact before preview; adding a phase code does not assign it to sales stages | Yes |
| Native FSM changed children | Blocker | verify_stage_phase_package_readiness | Safe exact-task export/schema, unchanged standard parent closure, fresh child state, exact persisted context or reopened immutable hash is missing/conflicting | Recover omitted parent with fresh unchanged live fields and validate every child join; preserve unrelated content and retain Data Loader's approval lifecycle | Yes |
| REST_FALLBACK | Blocker | verify_stage_phase_rest_fallback | Dedicated eligible outcome or fully representable reviewed delta is missing; CSV repairable; prior submissions pending/uncertain/partial/incompletely diagnosed; input/auth/catalog/context/approval/FSM-only constraints bypassed | Exhaust CSV recovery and reconcile all prior submissions; then fresh standard parent/code reads and a separate immutable REST preview | Yes |
| REST submission | Blocker | resolve_stage_phase_code_state | Preview/approval is missing/stale/borrowed from FSM, endpoint is not the same-target returned child or fixed collection, body writes parent/audit/set/identity fields, or prior REST row failed/uncertain/unverified | Prepare and approve one exact ordered REST preview immediately before execution; create-only POST with Upsert-Mode=false or minimal PATCH, verify once, stop at first failure/uncertainty | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_stage_phase_parent | Every request | Exact standard parent/catalog identity, unchanged business fields, editability/security and canonical link | ora_reference_lookups.md |
| resolve_stage_phase_code_state | Before reads or mutation preview | Fresh exact per-code state/absence, links, timestamps and full Inventory pagination | ora_reference_lookups.md |
| verify_stage_phase_package_readiness | Native FSM/Export readiness | Safe current export contract, standard-parent closure, per-child delta/state/impact, context and reopened hash for handoff | ora_reference_lookups.md |
| verify_stage_phase_rest_fallback | Before final fallback preview | Same-target exhausted/reconciled receipt, fresh parent/code reads and eligible outcome | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.STAGE_PHASE.DESIGN | decision | 6 | design_enforcement | pass->OPP.STAGE_PHASE.GATE;blocked->OPP.STAGE_PHASE.RETURN_MISSING;failed->OPP.STAGE_PHASE.RETURN_FAILED | OPP.STAGE_PHASE.PACKAGE | stop | Enforce exact standard lookup identity, operation/state, impact and native CSV readiness or dedicated final-fallback eligibility before route-owned preview/approval |
