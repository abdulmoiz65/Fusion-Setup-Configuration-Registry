# Offline Task Rule Planning

Use the Expenses-local planner when a selected nested setup
task requires a planned, ready graph before runtime validation or candidate
preparation. This is an offline check of an existing compiled v3 registry. It
does not compile, regenerate, evaluate business rules, authenticate, read Fusion,
prepare an import, create approval state, or authorize an external operation.

```bash
python3 pillars/erp/financials/expenses/scripts/plan_task_rules.py \
  --skill-path <nested-task-folder> \
  --task-name "<exact-task-name>" --task-code "<exact-task-code>"
```

The folder and its `SKILL.md` must resolve inside this repository's `pillars/erp/financials/expenses/`.
The selected manifest and registry must agree on exact task name and code. Flat
tasks and registry versions other than nested v3 are unsupported by this command;
do not substitute another task or silently relax the check.

## Required planning gate

Read this guide, the selected task manifest, its six owning `ora-resource/`
guidance files, the compiled registry, and the returned plan before evaluating
any rule. The planner verifies:

- Exact task identity, unique node IDs and sequences, valid supported actions,
  a valid start, terminal shape, existing transition/prerequisite targets,
  reachability, terminal paths, and acyclic prerequisites.
- Task and node readiness without unresolved blockers or a readiness override.
- Task-local source files, exact source headings and lines, complete source node
  inventory, and agreement of source node rows with the compiled graph.

Require `status: planned` and `plan.validation.status: ready`. Otherwise stop at
the reported planning error and obtain an authoring correction through the
development workflow. Never repair or recompile rules during a customer run.
Planning failure is a catalog/metadata validation failure; it is not an approval
prompt. The command reports JSON errors with status, failure class and message,
and returns nonzero. It
does not write a run record; the owning task records sanitized diagnostics under
its existing project workflow. Missing local files are artifact/input failures.

The returned source digests identify the manifest, registry, and rule Markdown
checked in this run. Replan if any of these files change before consumption.
Source rows and resolver definitions remain the authority for rule details.
Graph readiness alone never establishes live dependency state, target
qualification, payload validity, successful import, or permission to mutate.

## Consuming the full task graph

Start at `start_node`. Before each node, require every declared prerequisite to
have succeeded in this run and evaluate `applies_when`. Read the node's owning
source section and, when applicable, its named resolver definition. Confirm the
source facts agree with the intended action. Missing or inconsistent source or
resolver guidance blocks execution; never invent a lookup, default, outcome, or
replacement route. Perform only the selected workflow's declared operation.

Record the node, sanitized evidence and observed outcome, then follow exactly
the declared transition. Stop on an unrecognized outcome or at a terminal; do
not execute nodes in sequence order regardless of their transitions. Preserve
the selected task's stricter readiness and qualification requirements.

Keep the task's existing preconditions, operation order, persistence, redaction,
diagnostics, retry limits, and approval/verification gates. Planning does not
select a live execution route or permit a read, export, import or browser action.
For an uncertain mutation, reconcile through the selected read-only workflow
before considering another submission. On resume, recheck changed evidence and
approval validity through the owning workflow.

## Later Data Loader validation

When the task reaches its declared Data Loader handoff, use `core.data-loader`
and its Task Hook `data-load` route after final-artifact preflight, following
[Task Rule Registry Execution](../../../../../core/data-loader/references/task-rule-registry-execution.md). Evaluate the
applicable read-only rules against that exact artifact before preview and
candidate-bound approval. The offline plan neither replaces that evaluation nor
allows Task Hook to restart intake, export, construction, approval, or import.
Any applicable waiver remains subject to the task's existing policy; this
planning command offers no override. A task requiring ready rules without an
override retains that requirement.

Return the exact task identity, planning/validation status, current or terminal
node and action, completed path and outcomes, sanitized facts and evidence,
blockers, verified side effects, one safe next action, and resume context under
the selected task's existing reporting contract. Do not claim runtime success
from a successful offline plan.
