# Goal Management Profile Options Error Handling

## Source Basis

The enclosing SKILL.md defines validation_gap and PROVIDER_SKILL_UNAVAILABLE.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Semantic catalog is absent or malformed | Report the catalog contract failure and restore the resource; do not guess a code/value or silently bypass resolution. |
| Intent is unresolved, ambiguous, neutral, or contradictory | Ask the targeted consultant question produced by intake before provider lookup. |
| Provider capability is unavailable | Return PROVIDER_SKILL_UNAVAILABLE and stop; do not implement a local replacement. |
| Tenant identity, level, or value cannot be validated | Return validation_gap with the provider's sanitized diagnostics and a correction path. |
| Provider read fails | Preserve the provider failure classification and next action; follow only its documented recovery policy. |
| Update approval or execution evidence is missing | Stop at the owning value-maintenance workflow; never infer approval from this task's ready terminal or retry an uncertain write. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPO.HANDLE_ISSUES | step | 30 | error_handler | handled->MPO.RETURN_ISSUES | none | stop | Input, provider, or ownership validation is blocked |
| MPO.RETURN_ISSUES | terminal | 40 | terminal | none | none | stop | Return the disclosed blocker and safe next action |
| MPO.READY | terminal | 50 | terminal | none | MPO.ENFORCE_OWNERSHIP | stop | Return validated read evidence or update handoff readiness; no mutation has been authorized or executed by this task |
