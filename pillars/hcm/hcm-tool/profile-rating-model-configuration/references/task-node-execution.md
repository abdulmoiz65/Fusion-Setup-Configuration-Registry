# Profile Rating Model Task-Node Execution

Read this skill and `ora-resource/ora_rule_registry.json`. Select the exact
Profile Rating Models task code and name. Require readiness `ready` with no
blocking reasons. Confirm `start_node`, unique node IDs, valid prerequisites
and transitions, and a matching source row and Rule ID for each node. A
missing or stale source contract blocks validation and execution.

Read the selected source rows and resolver definitions before following the
graph. Start at `start_node`; check prerequisites, evaluate `applies_when`,
record the observed outcome, and follow only a declared transition. Stop at a
terminal node. Missing or ambiguous inputs and unsupported outcomes block the
path.

A ready registry provides rule order only. For an allowed creation route,
complete this skill's environment, privilege, payload, preview, approval,
executor, and readback checks. Record sanitized evidence. Verify an uncertain
submission before considering any retry.
