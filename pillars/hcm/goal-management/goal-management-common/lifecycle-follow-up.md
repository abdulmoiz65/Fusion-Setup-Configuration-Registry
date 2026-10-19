# Creation status and activation follow-up

Apply to newly created Performance and Development Library Goals, Goal Plans,
and Review Periods. Preserve each owning skill's create defaults, supported
operations, inactive-first rules, approval gates, and fresh-read verification.

- Explicit inactive intent: retain inactive; do not repeatedly request activation.
- Explicit active intent: retain that desired outcome even if creation must be
  inactive first. Preview the separate activation through the existing route.
- Status omitted: disclose the create status at task review. If created inactive,
  offer activation of only the successfully created objects as the recommended
  follow-up, or allow the consultant to confirm retaining them inactive. Missing
  status is not a creation blocker and does not authorize automatic activation.
- A requested downstream dependency requiring active status implies active
  intent (for example, a created Review Period needed by a Goal Plan). Include
  the required activation in the task review and existing approval workflow.
  An explicit inactive instruction conflicting with that dependency requires
  clarification; never silently override it.

Scope activation to the exact identities and verified successful creates from
this run, including partial successes. Never activate older matches, skipped
duplicates, or every object in a library. Use only an existing supported route;
this guidance grants no new write authority.

Report creation and lifecycle readiness separately. For unspecified status with
no required active dependency, report creation complete with an optional
activation follow-up, not BLOCKED. Do not silently close the lifecycle decision:
show the choice in the handoff and retain it in the task's existing operations
or follow-up record. Required activation remains outstanding until verified;
inactive creation alone does not complete an explicitly or implicitly active
outcome. Preserve the existing task ordering and approval conventions.

For each Performance or Development Library Goal create task, persist one
task-level lifecycle follow-up JSON before the task review or Run Book completion
update. Include `type_code`, `source_status_intent` (`omitted`, `active`, or
`inactive`), `activation_choice`, `handoff_choice_text`, and `verified_creates`
with the exact name, type, status, successful-create provenance, and fresh
verification reference for every goal created in this run. Validate it with
`python pillars/hcm/goal-management/goal-management-common/scripts/library_goal_lifecycle_handoff.py
<follow-up.json>`; a failed check prevents the handoff, not the successful create.
If status was omitted and a goal is inactive, use `pending` until the consultant
chooses activation or retention, and present both options in the same task
review. A pending optional choice does not prevent marking creation complete.
Do not include pre-existing or skipped duplicate goals.
