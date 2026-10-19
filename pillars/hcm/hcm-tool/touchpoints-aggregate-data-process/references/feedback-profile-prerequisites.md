# Automatic Feedback profile prerequisites

This contract applies to full Touchpoints implementation and any selected scope
containing Feedback. It implements the existing Requested Feedback Template
parent baseline through `core.fusion-api.apps-common.profile-options`.

## Required SITE values

- `HRA_REQUEST_FEEDBACK_ENABLED = Y`
- `ORA_HRA_REQ_FEEDBACK_REDWOOD_ENABLED = Y`

These are mandatory regardless of whether intake names them. Touchpoints profile
settings do not substitute for this baseline. Do not add the separate goals
profile unless explicitly in scope.

## Execution sequence

1. During authorized execution, before final task mapping, invoke
   `scripts/touchpoints_feedback_profiles.py --input <workflow-state.json>
   --live-read --base-url <exact-environment-url> --reference <provider-read-reference>`.
   This is the declared profile-provider read step. It uses only cached
   authentication and the shared core transport, and performs four exact GETs.
   A missing session requires the existing Chrome authentication handoff.
   No login, write, or stopped-run resume occurs inside this adapter.
2. Persist the returned normalized `state` as the workflow state using the
   existing artifact/state managers. Rerun the authoritative Run Book planner.
   Read errors are agent-owned technical failures, never requests for consultant
   profile evidence or manual setup. Independent work may continue.
3. Both verified Y values produce a no-change baseline and no new profile row.
   A non-Y, absent, or unknown value produces exactly one prerequisite row:
   `feedback_profile_prerequisites`, `Manage Administrator Profile Values`,
   `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`, Performance Management / Performance Management Common.
   It is a profile-provider handoff, with manual tracking task type, never a
   Data Loader operation. Canonical initial creation includes it in the same
   Run Book. An existing Run Book uses authorized core add/sequence operations.
4. The prerequisite requirements contain both codes, current evidence, desired
   SITE Y values and exact read requests. Delegate updates to the existing
   profile provider. Re-read before preview; skip already-Y profiles; preview
   each required POST/PATCH, obtain its exact-write approval, dispatch once and
   read back. Do not mutate through this read adapter. Provider identity,
   SITE flags, privileges and approval checks remain mandatory.
5. Refresh the normalized evidence after readback. Mark the remote prerequisite
   Completed through authorized core Run Book update, then refresh its snapshot.
   A bound prerequisite remains in the plan as verified Completed even when
   both values become Y; completion never silently removes a tracking row.
6. Sync contexts and handoffs. Feedback handoff includes its parent skill,
   `mandatory_profile_baseline`, provenance, values and the requirement to
   refresh before template mutation. The agent validates the baseline through
   the parent contract before entering the nested Feedback Templates workflow.
   Neither missing evidence nor an enabled profile authorizes a template write.

The planner automatically discovers this prerequisite even when a caller has
not supplied `dependent_tasks`. The reserved key and its requirements cannot be
overridden with supplied task requirements. Full scope keeps Touchpoints profile
work first and ESS last; focused Feedback scope includes only its actual
prerequisites and Feedback. This prerequisite gates Feedback rather than
unrelated Check-In work.

## Evidence and failure boundaries

`feedback_profile_evidence` must match project, environment and configuration
revision, identify the profile provider and SITE level, contain actor,
timestamp, reference, verification reference, and both literal configured
values. Effective user values, other environments, unknown fields and
consultant no-change assertions do not replace provider SITE readback.

This fixes the profile prerequisite and handover gap. It does **not** resolve
Feedback template POST capability or caller privilege evidence. Those are
separate checks in the owning template workflow; a profile read is not a
capability probe or a privilege grant. Keep unresolved checks as agent-owned
technical failures and attempt only the owning workflow's declared evidence
routes. Never set preflight booleans from these profile values, perform a trial
POST, or ask the consultant to justify an omitted technical flag.

## Local verification

Tests cover full/focused scope, enabled/disabled/absent/unknown values, exact
GETs, incomplete readback, changed environment, retained bound completion,
independent Check-In progress, handoff evidence and stopped-run protection.
Use `--dry-run` for offline planning; it never contacts Fusion.
