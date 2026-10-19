# Deterministic Touchpoints orchestration

## Authority and scope

When Feedback is selected, [automatic Feedback profile prerequisites](feedback-profile-prerequisites.md)
governs mandatory discovery, provider readback and parent-to-template handover.
Do not rely on externally supplied dependent-task rows to introduce this baseline.

Classify the business objective once and persist `scope` with its source.
Full implementation uses profiles, Check-In, Feedback, surveys, nudges,
readiness, Full aggregation and daily Incremental scheduling. Selected-task
scope uses only the selected tasks and their source-backed unmet prerequisites.
Never add aggregation merely to seed a selected configuration Run Book.
Retain scope through follow-up answers; an actual scope amendment needs an
explicit decision. Different ordering of the same selected keys is not an amendment.

The ordered output of `touchpoints_runbook.py` is the authority for presentation,
provisioning and owner execution. Catalog identity and Run Book display labels
are separate fields on the same task. Do not maintain a second handwritten plan.

## Prerequisites and order

Owner intake may add `dependent_tasks`, an array of objects with:

- `key`: unique key distinct from the eight baseline keys.
- `name`, `owner_skill_id`, `execution_route`, `source_reference`.
- `required_by`: consumers that actually require the task.
- `depends_on`: explicit predecessor keys, default empty.
- `disposition`, `missing_inputs`, `evidence`, and `requirements` when available.
- `catalog_identity` with task_code/task_name/offering/functional_area for a
  catalog-backed task, mandatory for a Data Loader context.

Routes are profile-provider, data-loader, rest or manual-ui. Only prerequisites
reachable from selected consumers are included. Examples are unmet Requested
Feedback profile setup, or an eligible custom questionnaire for General Feedback.
Never add a custom questionnaire for Performance Goal Feedback; its owning skill
requires the seeded questionnaire. A satisfied prerequisite stays evidence and
does not need another configure task.

The planner validates references and cycles and orders profiles first, owner
prerequisites before consumers, configuration before readiness, and ESS last.
Daily Incremental scheduling is part of the ESS owner handoff and has its own
manual tracking row. If both ESS tasks are selected, Full precedes Incremental scheduling. Actual
Run Book sequences must match this order for every scope. No-gap repairs still
use core.runbook authorization. A selected profile plus ESS request cannot
become ESS-ready until the selected profile work is verified.

## Creation and context synchronization

Resolve every `creation_tasks[].catalog_identity` through the existing canonical
initializer/catalog resolver before initial creation. Requirements still missing
for a task do not remove its catalog identity or execution context. The scoped
`touchpoints_creation_plan.py` adapter consumes this exact canonical plan and
the authoritative configuration plan. It assigns REST-only Feedback a supported
manual tracking task type rather than the shared generator's Data Loader default.
It rejects extra or missing identities. Persist its reviewed output as the
project Run Book creation plan before the existing core creation step; identities
remain canonical. Other `manual_tracking_tasks` use authorized core add-task
operations after creation. All rows belong to the same Run Book.

The adapter performs no external operation. For a selected scope containing
only uncatalogued manual activities, core's current initial-creation contract
requires a catalog-backed task. Report that core capability gap as a technical
limitation. Do not expand scope, fabricate an action code, or ask the customer
to justify an unrelated aggregation task.

After provisioning and after any task-sequence repair, execute:

```bash
python3.12 scripts/touchpoints_orchestrator.py --project-root project/{project_id} --sync-context
```

This checks the active Run Book, complete snapshot, all selected bindings and
catalog identities; then synchronizes generated Data Loader/ESS task contexts
and creates `owner-handoffs.json` for every row. REST tasks remain REST handoffs.
The initial creation plan is not rewritten during synchronization. Existing
owned contexts are regenerated on a verified sequence change; changed task IDs
require reconciliation. Unrelated contexts are preserved, and collisions fail.
The historical `sync_checkin_task_context.py` command now uses the same complete
plan; it is no longer a Check-In-only repair.

For a new project without a snapshot, generate the plan first, provision the
Run Book, refresh all tasks and synchronize. A local sync failure is agent-owned
repair work. Never ask the customer to manufacture a task context. `--dry-run`
reports a needed sync without writing. A stopped/paused run selects no next task.

## Execution controller and questions

Read `plan.execution.next_task`, delegate to its owning skill, verify the result,
persist its evidence and synchronize the named Run Book row through authorized
core operations. Re-run the orchestrator after each outcome. Independent ready
configuration tasks may proceed when another task awaits input or fails. ESS
waits for all its predecessors; daily scheduling additionally waits for verified
Full success. Preserve pending/unknown external-operation records and reconcile
read-only before any retry. Exact previews and approvals remain owner-managed.

`task_outcomes` maps keys to owner diagnostics, e.g.
`{"feedback":{"issue":{"kind":"route_capability","source_reference":"owner diagnostic"}}}`.
The controller reports these states distinctly:

| Outcome | Customer question |
|---|---|
| ready | None; continue owner preflight |
| awaiting_business_input | Ask the missing business choice |
| awaiting_write_approval | Show the completed exact owner preview and ask once |
| awaiting_dependencies | Continue independent work |
| technical_failure | Resolve declared technical evidence or report the owner limitation |
| unsupported_route | Report the unsupported operation; no invented fallback |
| completed / not_applicable | Reuse valid outcome evidence |

Issue kinds business_input and write_approval permit a user question. Governance
permits one only with `explicit_policy_reference`. Privilege and route-capability
issues are technical. The agent reads configured target identity, declared
metadata/contracts, valid retained same-target history and fresh declared GETs;
it never asks the customer for ordinary technical evidence. A GET alone does not
prove POST permission. The Feedback owner's mandatory checks cannot be removed
inside Touchpoints: unresolved evidence is a provider skill limitation, not
permission to set true flags, probe with a write or substitute the UI.

Approval pending is a normal checkpoint, not a technical failure. The controller
never converts a generic implementation approval into an exact write approval,
and never asks again when an existing approval still covers the exact request.

## Regression checks

Test full and selected scopes, reversed input order, prerequisite closure and
cycles, profile-first and ESS-last sequence checks, typed REST creation,
task-by-task continuation, stopped runs, uncertain writes, context generation,
sequence repair, unrelated-context collisions and technical-question policy.
No live tenant calls are needed for these orchestration tests.

## Scoped ESS coordination

For full/daily owner work, follow the nested task's daily-schedule contract and
scripts/touchpoints_ess_handoff.py. The helper imports unchanged core submission
and read/wait functions, supplies explicit readback fields, and persists identity
before monitoring. It never substitutes a REST client or changes core. Readiness
and owner metadata are not approval. Keep separate approvals for Full and daily,
and synchronize completion through the existing authorized core.runbook route.
A verified daily_schedule record resolves its checkpoint; uncertain/missing
readback never does. Do not select a verified schedule for another creation.
