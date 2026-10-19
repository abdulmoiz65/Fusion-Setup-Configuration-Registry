# Gig Descriptive Flexfields Design Enforcement

For copy, update, and disable, ask only for Segment Name when missing, then validate a fresh exact-task export for this request; if unavailable or empty, use the qualified Global fallback proposal instead of stopping; label older evidence UNVERIFIED. For new create, use a validated matching package or export fresh when absent. Follow the required-values table, confirmation, optional-values table, confirmation sequence in ../SKILL.md.

Global create, copy, update, and disable may use the [verified fallback export contract](ora_gig_global_segment_archive_contract.md), after a selected-environment exact-task export attempt fails, times out, or returns unusable rows. Confirm the complete design and disclose unavailable current-state checks as `UNVERIFIED`. Verification and context-sensitive work require a validated populated current-definition package. Global copy/update/disable use the confirmed fallback rules when fresh evidence is unavailable. Standalone list/inspect still requires a fresh export.

Apply these task-local gates before any configuration preview, deployment, or FSM import handoff for `IRC_MP_GIGS_DFF`.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm target | Match the exact Gig task, DFF, application, and Global or verified existing Gig-context scope |
| 2 | Resolve retrieval state | For copy, update, and disable, ask only for Segment Name when missing, then validate a fresh exact-task export for this request; if unavailable or empty, use the qualified Global fallback proposal instead of stopping; label older evidence UNVERIFIED. For new create, use a validated matching package or export fresh when absent. Follow the required-values table, confirmation, optional-values table, confirmation sequence in ../SKILL.md. Preserve the supported scope and exact-identity guards. |
| 3 | Collect and enforce design | Ask for the name first when missing. Apply the name-based design rules in ../SKILL.md using the validated package or qualified new-Global fallback, preserve supplied/confirmed source types, clarify ambiguous names, present type-compatible values as one proposal, obtain confirmation or changes, and validate uniqueness, storage, sequence, contexts, data, value-set, display, runtime, and optional settings |
| 4 | Enforce execution route | Build and validate a proven Gig FSM package without starting another export; never inherit Referral package behavior |
| 5 | Bind approval | Present the exact target and delta or immutable checksum, then obtain current approval immediately before mutation |
| 6 | Submit and monitor | For an approved create, update, or copy import, suppress the acceptance report, monitor the accepted request to terminal state, download and read the ProcessLog, and return only the final success or error result without retrying submission |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Error | | Task, sequence, parent task list, DFF, application, or business object differs from the supported identity | Return the exact missing or unsupported identity | No |
| Inspect/list request | Error | resolve_gig_dff_segments_from_task_export | A fresh exact Gig task export is absent, malformed, belongs to another task/DFF/application, or its context rows cannot be joined uniquely | Run a new routed export, validate it, and return Global plus all exact Gig-context segments grouped by scope | No |
| PlanCreate, PlanUpdate, or copy reaches analysis or artifact preparation | Error | verify_gig_dff_current_definition | An identifier, storage assignment, sequence, source property, or other current value required for safe construction is unavailable or ambiguous after validating this request's fresh export for copy/update/disable, or the matching package/export route for new create | Ask for the missing value or return BLOCKED; do not substitute another DFF or artifact | No |
| A context-sensitive segment is requested | Error | verify_gig_context_identity | The exact existing Gig context code and label are not uniquely verified | Use Global only or resolve the exact existing context | No |
| Any request | Error | | EMPLOYEE_REFERRAL, AGENCY_REFERRAL, another Referral identity, context creation, rename, deletion, or substitution is proposed | Keep Referral identities out of Gig DFF and preserve existing context lifecycle | No |
| PlanCreate or PlanUpdate | Error | verify_gig_dff_current_definition | Segment identity or business purpose duplicates or overlaps an existing Gig segment | Present the conflict and require an explicit design revision | Yes, before approval |
| PlanCreate | Error | verify_gig_dff_current_definition | Storage is occupied, sequence is not positive and unused, or identifier validity is not proven | Select compatible available values and require confirmation | Yes, before approval |
| Existing value set is used | Error | verify_gig_value_set_compatibility | The value set is absent, ambiguous, disabled, or incompatible with data, display, runtime use | Select one exact compatible value set | Yes, before approval |
| New value set is proposed | Error | | Value Set Code, Module, Validation Type, or Value Data Type is missing or incompatible | Complete the separate value-set design and owning workflow | Yes, before segment approval |
| PlanDisable | Error | verify_gig_dff_current_definition | Exact segment, impact, current usage, rollback, or approval is missing | Limit retirement to reversible disable of one exact segment | Yes, before approval |
| Copy source is omitted | Error | | Source Segment Name is missing or ambiguous | Ask only for source Segment Name, then export fresh and resolve it; request a selection only if ambiguous; use the qualified Global fallback if the fresh export is unavailable or empty | No |
| FSM import is proposed | Error | | Exact Gig members, filenames, headers, parents, translations, metadata, encoding, builder, or checksum validation are unproven | Return ARTIFACT_PREPARATION; never copy or infer Referral structure | No |
| Any mutation is ready | Error | | Exact preview is absent, approval is missing or stale, or immutable bytes changed | Re-preview and obtain new approval | Yes, by re-previewing |
| Approved create, update, or copy import was accepted | Error | | Completion monitoring, terminal status reconciliation, or ProcessLog review is omitted | Continue through core.data-loader task-scoped completion monitoring; do not retry or resubmit | No |
| Mutation failed or is uncertain before an accepted request ID exists | Error | | Automatic replay, replacement, or resubmission is proposed | Return the known failed or uncertain result and stop | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_gig_dff_segments_from_task_export | Inspect/list, or copy or duplicate without a source segment | Exact export identity; Global segments; exact Gig contexts and their segments; user-facing properties | ora_reference_lookups.md |
| verify_gig_dff_current_definition | Current state, uniqueness, storage, sequence, update preservation, disable, or verification is evaluated | Fresh validated exact-task export for this copy/update/disable request; validated matching package for new create or verification | ora_reference_lookups.md |
| verify_gig_context_identity | A context-sensitive segment is requested | Exact existing context code, label, and enabled state | ora_reference_lookups.md |
| verify_gig_value_set_compatibility | An existing value set is selected | Exact value-set identity, data type, validation type, module, enabled state, and compatibility | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GIG_DFF.ENFORCE_DESIGN | decision | 40 | design_enforcement | passed->GIG_DFF.APPROVAL_GATE;blocked->GIG_DFF.RETURN_ISSUES;conflict->GIG_DFF.RETURN_ISSUES;unsupported->GIG_DFF.RETURN_ISSUES | GIG_DFF.CHECK_READINESS | stop | Every supported request |
