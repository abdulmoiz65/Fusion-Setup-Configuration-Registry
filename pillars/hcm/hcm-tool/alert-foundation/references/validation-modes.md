# Alert Foundation validation modes (0.11.0)

Validation depth and submission style are independent choices. An unqualified
CREATE prompt means **simple validation, sequential submission**. Only explicit
`batch-create` selects one JSON batch for the whole workbook.

| Check or behavior | simple (default) | deep (explicit) |
|---|---|---|
| Mandatory fields, explicit booleans, supported operations | Local | Local |
| Included parent/child relationships, unique workbook keys | Local | Local |
| Payload shape, safe paths, known local field lengths | Local | Local |
| Live describe compatibility | Skipped | Required |
| Alert type/access, MIME, language, recipient channel | Literal codes; Fusion validates | Resolve against the target |
| Existing AlertCode duplicate search | Fusion validates | Required before approval |
| Environment, source digest, immutable payload approval | Required | Required |
| Submission response and independent create read-back | Required | Required |
| Automatic write retry or rollback | Never | Never |

Simple is intended for consumers who already know their business codes. It does
not translate labels, infer codes, fetch metadata, or prove that Fusion will
accept the request. Invalid business values are reported from Fusion after
approval. Known local lengths remain inexpensive checks; they are not refreshed
from the live service. Body remains literal input without content validation.

Deep executes the declared describe, LOV, language and duplicate resolvers.
The reader emits their request specifications but never executes them. The
assisted provider executes reached rules, follows pagination, checks exact
matches and current metadata, and records real evidence. Missing routes, access,
or ambiguous values block deep; never silently downgrade to simple. Deep does
not enable the deferred validateExpression action or file-based Body writes.

For simple CREATE, complete local ALERT.VALIDATE, record ALERT.LOOKUP outcome
`skipped_simple`, then execute the local dependency/design branches and approval.
Do not authenticate, run live preflight calls, or manufacture passed live evidence
before approval. Record the configured origin and existing role authorization
assumption locally; Fusion remains authoritative for authentication/authorization.

These CREATE shortcuts do not remove fresh exact-item identity, state,
ownership or destructive-operation safeguards for UPDATE, DISABLE, DELETE or
COPY. Those operations retain their existing declared read prerequisites.
Post-submission verification is also not a preflight check and remains required.

## User prompts

> Create Event Alerts from "<intake.xlsx>".

> Create Event Alerts from "<intake.xlsx>" with deep validation.

> Create Event Alerts from "<intake.xlsx>" in batch-create mode.

> Create Event Alerts from "<intake.xlsx>" in batch-create mode with deep validation.

The provider always uses the current project's configured Fusion environment
and seeks approval before writes. In batch-create, either validation mode yields
one entire-workbook work unit, one `Confirm Alert Batch <SHA256>` approval and
one POST. Sequential retains one work unit per included Alert hierarchy.

## Adapter and approval contract

Pass `--validation-mode simple|deep` to `read-alert-intake.py`; default is simple.
The canonical approval document contains both `validation_mode` and the exact
`validation_policy` from `scripts/alert_validation.py`. The execution adapter
uses the approved document, not a new command-line mode override.

Simple batch requires no live `--gate-evidence` file. Deep batch requires one,
bound to mode `deep`, environment, aggregate digest, and actual hashed gate
artifacts. Both validate the source hash, payload, configured origin and exact
approval before authenticating. Do not reuse pre-0.11.0 previews or approvals;
regenerate a preview after any mode, policy, source or request change.

One batch POST cannot enforce server stop-on-first-part-error. Inspect every
returned part, stop further writes on failure, preserve partial/uncertain
outcomes, and require separately approved recovery. No atomicity is assumed.
