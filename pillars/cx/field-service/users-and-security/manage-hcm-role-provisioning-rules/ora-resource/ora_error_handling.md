# Error Handling

## Stop Conditions

Stop and return the shared workflow's redacted failure classification when the
shared workflow rejects an input, dependency, environment, authorization,
archive, approval, import, or process result. Do not retry export, upload,
import, overwrite, or a failed job from this pillar task. Do not expose tokens,
credentials, private keys, customer security configuration, or unredacted
payloads.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HRPRFS.EXECUTION_GATE | decision | 4 | execution_gate | ready->HRPRFS.READY;blocked->HRPRFS.BLOCKED | HRPRFS.ENFORCE_DELEGATION | stop | Before the shared workflow returns an immutable approval preview. |
| HRPRFS.READY | terminal | 5 | terminal | none | HRPRFS.EXECUTION_GATE | continue | The pillar delegation checks passed; the shared workflow owns the next action. |
| HRPRFS.BLOCKED | terminal | 6 | terminal | none | none | continue | A delegation prerequisite is missing or failed. |
