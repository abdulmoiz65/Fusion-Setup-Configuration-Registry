# Item-by-item Learning setup inventory

Use this contract for broad Learning setup/review or a requested list of needed,
configured and missing settings. Deliver the inventory before a change proposal;
do not substitute totals, generic recommendations or only the proposed delta.
For a narrow task, cover its requested items without expanding to every area.

## Coverage and evidence

For an offering-wide request, retain the functional-area coverage from
[offering-wide intake](setup-capability-handoffs.md#offering-wide-intake-and-response)
alongside the detailed Common inventory and references to child work products.
Use coverage entries to identify assessed, partially assessed, not assessed or
excluded areas with reasons. Include unavailable/deferred areas as handoffs;
do not mark them assessed from taxonomy membership or turn the overview into
proof that every task has a live reader. This does not expand Common's executor
scope or require a new artifact schema.

Reuse accepted scope and answers. Expand the selected task guidance into named
items: profile codes/levels; applicable lookup types (and exact values when
reviewing a value-level gap); DFFs/contexts/segments; their value sets; indexes,
attributes and views; audit objects; and named security, CAP, defaults,
background-process and Talent-profile handoffs. Account for C1–C8 and relevant
non-FSM foundations in a broad assessment, even where no reader is available.
Keep conditional or excluded items visible with a reason. The manifest's
`required_setup_tasks` is catalog membership, not a mandate to configure all
tasks. Guided profile/lookup lists are a starting scope, not all possible
Learning settings: add applicable on-demand items from the task guidance.

Read through the selected workflow only. Keep successful independent reads
when another fails. Record exact environment, scope, observation time, reader,
completeness and evidence reference for each item. A report assembled later
retains those observation times; generation time is not a fresh pod read.
When a fresh assessment is requested, reread through permitted routes; do not
present previous runs as current evidence. After writes, reconcile the same
key/level/target using the latest successful readback without altering the old
baseline. A failed read or uncertain write cannot prove absence or success.

Record identities at the level actually assessed. A profile definition does
not prove a Site value exists, lookup counts do not prove vocabulary fits, and
saved DFF/index settings do not prove deployment, ingestion or persona behavior.
Do not invent custom value sets or mandatory flexfields without a requirement.
If names are unresolved, label a documented purpose as such, not a pod name.

## Required row contract

Persist `learning-setup-inventory.json` and `learning-setup-inventory.md` in a
new run/version under the Common project artifact path. Validate JSON using
[the local inventory schema](setup-inventory.schema.json). This is an assessment
format, not an import payload, new core schema or new executor.

Each stable `key` includes category, exact identity and level/target/context.
Include code (null only when unresolved), name/purpose, applicability and basis,
current value or safe summary, expected value/requirement, accepted decision,
fit/gap, next action, owner and approval state. Retain source/evidence references.
Keep these dimensions separate:

| Dimension | Meaning |
| --- | --- |
| Requirement | Required for agreed scope, conditional, optional, future scope or excluded; state the condition and source, not a universal product prerequisite. |
| Evidence | `observed`, `confirmed_absent`, or `not_validated`. Confirmed absence requires a complete, successful exact-scope read; a 404/denial/timeout/incomplete collection alone is not absence. |
| Fit | `meets_decision`, `review_needed`, `gap`, `unknown`, or `not_applicable`. Configured does not mean fit-for-purpose. A confirmed gap needs an applicable known requirement and evidence; unread items remain unknown. |
| Action | `keep`, `propose_change`, `input_required`, `verify`, `defer`, or `exclude`. Optional decisions and technical evidence gaps do not authorize changes. |
| Approval/execution | `not_requested`, `required`, `approved`, `completed_verified`, or `uncertain`; link approval/result evidence where relevant. Assessment approval is not permission to mutate. |

Observed null, N, zero and disabled values remain observed values, not synonyms
for missing. For an unread item use null plus `not_validated`; for a redacted
value keep an explicit safe summary and redaction marker. Editability and
protection are separate from configured state. A non-updatable mismatch needs
owner review, never a force update. Preserve optional unknown decisions without
overwriting an observed value or calling it unconfigured.

## User-facing delivery and continuation

Lead with coverage and evidence dates, then provide the full grouped report
without another request. Show code, name/purpose, applicability, configured
value/scope, needed value or decision, status, next action and approval per row.
Summarize observed, confirmed-absent and not-validated counts separately from
required, optional, future and excluded counts. Do not count every unknown as
missing or every configured row as ready. Include exact value-level evidence
when making a lookup/value-set change proposal; type counts alone are not enough.

List confirmed gaps separately from unresolved checks. Ask short, specific
questions only for missing applicable business information, with an example
reply where useful. For unavailable routes, name the owner and specific evidence
needed; preserve the technical restriction while continuing independent work.
Do not ask the user to supply guessed endpoints or waive technical safeguards.

Use the inventory to build the subsequent proposal. Recommend only supported,
applicable changes and ask for approval of the exact ready delta through the
existing provider gate. No changes is a valid result. Record completed changes
separately so the next run does not ask to approve or replay them. Calendar UI,
end-to-end acceptance and overall setup readiness remain separate from profile
readback. Preserve existing Run Book scope and approvals.

Persist sanitized outputs only in the ignored project workspace, register them,
update run/state references and log token estimates through existing project
services. No tenant-specific output belongs in reusable skill files.
