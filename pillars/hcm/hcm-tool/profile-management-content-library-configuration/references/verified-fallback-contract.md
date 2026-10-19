# Verified provider fallback exception

FSM is preferred. Original GROW-8154 Jira/FDD acceptance remains FSM-only.
The user's 2026-09-11 direction permits an explicitly selected, provider-specific
exception; it does not make HDL evidence FSM acceptance or approve a live load.
Record the selection in the project decision/run and retain both results separately.
Without that selection, or when strict FSM-only acceptance is requested, do not
select an HDL route. A known FSM limitation may justify offering the exception;
do not run a known failing import merely to demonstrate it again.

## Initial eligible route

Only enhanced-profile GOAL, using the checked-in
[CONTENT_ITEM_V2_HDL contract](../content-items/references/content-item-goal-hdl-provider.json),
is eligible. It must still be `verified`; release metadata is not a gate.
The complete request must consist of exactly one create-only item with
ContentItemCode, ContextName=GOAL, Name and DateFrom. Input date is YYYY-MM-DD;
the existing provider renders YYYY/MM/DD. Other historical HDL providers,
HSDL, generic DAT workarounds, REST/browser writes and internal services are not
enabled by this exception. Future providers require their own reviewed contract,
capability, lifecycle and readback evidence; read support alone is insufficient.

Preserve all supplied rows, translations, descriptions and relationships in the
complete review. If any requested part is unsupported, hold the complete load.
Never remove fields, split a full set silently, create dependencies or broaden
the four-field provider to make it fit. Rating/foundation/Profile Types changes,
employee data, updates, deletes, end-dates, migration and merging existing records
remain excluded. The provider's HDL MERGE syntax is constrained to creation by
fresh dual-key zero-match locks; it is not update authority.

## Selection and execution gates

1. Capture the complete supplied configuration and provenance, confirm mappings,
   and freeze its review fingerprint. Resolve the authenticated target, privileges,
   enhanced mode and the registered GOAL FSM companion-document
   limitation through the declared workflow. An auth, transport, evidence,
   duplicate or approval failure is never a reason to switch provider.
2. Require explicit exception selection and a recorded `not_submitted` mutation
   state for this exact request. No automatic failover after an accepted, partial,
   failed, timed-out or uncertain submission. Preserve its IDs/status/ProcessLog
   and use the owning status/diagnosis workflow; a retry needs a new reviewed
   decision and fresh exact evidence, not this fallback gate.
3. Obtain fresh complete unfiltered same-target Content Items FSM evidence through
   `shared.setup-export.task-level-export`, with its own export gates. Reopen all
   required members and compare integrity-validated seed evidence. Check literal
   ContextName+Name and the separate ContextName+ContentItemCode collision guard.
   Display every actual matched identifier and stop on any collision, including
   different rows matching the two keys. Do not normalize names or emit generic
   similarity warnings. Retain catalog-specific case semantics in their own route.
4. Run `prepare_goal_content_item_hdl_package.py inspect` locally,
   then prepare only from its fresh receipt and the complete approved review.
   Input and receipt schema 1.1 add exact reporting and bound fallback selection;
   the provider registry remains schema 1.0. Old project evidence is immutable,
   not silently upgraded or treated as fresh readiness.
5. The input includes the following `fallback_selection`, copied from the recorded
   task decision/history, never manufactured to pass validation:

   ```json
   {
     "policy": "verified-goal-hdl-exception-v1",
     "explicitly_selected": true,
     "fsm_limitation": "enhanced-goal-companion-document",
     "mutation_state": "not_submitted"
   }
   ```

   These declarations are not independent live-state evidence or approval. The
   owning Task Hook must verify them against the complete request, selected route,
   prior execution history and current target evidence. The helper binds them to
   the exact input/provider-row, receipt, proposal and readiness fingerprints.
   Missing, changed or inconsistent bindings block preparation/handoff.
6. Independently reopen the deterministic archive, validate the live ContentItem
   source/schema through Core Data Loader, and present the exact target, single
   row, provider, package hash and create-only effect in its immutable preview.
   Task Hook and `core.data-loader` approval/auto-approval rules remain authoritative.
   The helper returns `approval_state=not_requested`; a project exception, package
   confirmation or testing intent never supplies retained load approval.
7. Submit only through `core.data-loader`. Capture accepted IDs, terminal status
   and ProcessLog through its allowed status workflow. Independently compare a
   fresh complete same-target FSM readback to every approved field and recheck the
   duplicate lock. A successful HDL load is fallback evidence, not proof that the
   GOAL FSM import defect is fixed or that full-set FSM acceptance has passed.

Continue independent local intake, validation and documentation while any gate
is held. Report the missing gate and owner without broadening provider authority.
