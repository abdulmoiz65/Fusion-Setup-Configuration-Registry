# Content Library Task-Node Execution

Read the selected child `SKILL.md` and its `ora-resource/ora_rule_registry.json`.
Select the entry matching the exact task code and name. Require task readiness
`ready` with no blocking reasons. Confirm `start_node` exists, each node ID is
unique, every prerequisite and transition names an existing node, and each
node's source row, file, and Rule ID still match the registry. Any mismatch
blocks execution until the task source and registry are reconciled.

Read the selected task's source rows and named resolver definitions before
using a node. Start at `start_node`; satisfy prerequisites, evaluate
`applies_when`, record the result, and follow only a declared transition. Stop
at a terminal node. Do not invent a missing lookup, default, outcome, or
cross-task step.

A ready registry does not authorize a Fusion write. Follow the child skill's
specified environment, privilege, package, preview, approval, executor, and
readback checks for the requested operation. Preserve sanitized evidence and
stop on an uncertain submission rather than replaying it.
