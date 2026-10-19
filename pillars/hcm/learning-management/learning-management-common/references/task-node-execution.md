# Learning Task-Node Execution

Read the selected Learning task's `SKILL.md` or flat task metadata, then run
`pillars/hcm/learning-management/learning-management-common/scripts/rule_plan.py`
for its exact functional area and task. Require `status: planned`,
`plan.validation.status: ready`, and task readiness `ready`. The local planner
checks task identity, graph edges, and the source row for each node. An
incomplete or stale graph blocks execution; correct its source and registry
before retrying.

Read every reachable node's `ora-resource` source row and any named resolver
contract before acting. For a flat task, use only rows matching its exact task
code and name. Start at `start_node`; check prerequisites, apply the node's
`applies_when` condition, record the observed outcome, and follow only its
declared transition. Stop at a terminal node. Missing or ambiguous input,
identity, source guidance, or outcome blocks that path.

A ready graph supplies rule order, not permission for an external call. Use the
selected task's declared client and operation after its environment, privilege,
payload, preview, and approval checks. Record sanitized evidence and external
IDs in the project run. Never replay an uncertain mutation; verify its result
through the task's declared readback route.
