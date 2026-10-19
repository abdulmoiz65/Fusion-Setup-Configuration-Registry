# Goal Management Approval Convention

Use this convention for Goal Management REST mutations, ESS submissions, and
other live operations whose owning workflow requires explicit approval. When a
request is routed through `core.data-loader`, its approval contract remains
authoritative.

## Approval Preview

Immediately before the live operation, show one current preview containing:

- the exact Fusion environment or hostname;
- the operation, target, and business effect;
- the exact payload, immutable import artifact, or ESS parameters, as applicable;
- the relevant current state, proposed state, and expected impact; and
- whether the approval covers one operation or a clearly enumerated batch.

Retain the complete SHA-256 fingerprint or structured approval envelope
internally to bind approval to the preview. Do not require the consultant to
copy or repeat a fingerprint, and do not expose an internal hash or artifact
path solely to collect approval. Show it only when the user explicitly requests
technical integrity details or when it is needed for a diagnostic.

Use this consultant-facing prompt by default:

> Reply `Approve`, `Yes`, or `Go ahead` to continue.

## Accepted Approval

Accept a clear contextual affirmative such as `approve`, `approved`, `yes`,
`go ahead`, `proceed`, or `submit it` when all of these conditions hold:

1. The response immediately follows the approval preview.
2. Exactly one unchanged preview is pending, or the response unambiguously
   identifies one pending operation or an explicitly combined batch.
3. The response is unconditional and contains no requested payload, target,
   environment, route, or sequencing change.

Do not require a fixed keyword. A request to create, update, activate, assign,
submit, or execute that precedes the final preview is not approval for the live
operation.

## Approval grouping versus transport

Keep approval cardinality separate from transport cardinality. “One approval,”
“approve all,” “single approval gate,” and similar language may select one
approval group for a fully enumerated ordered plan. They do not select an ADF
batch endpoint, a `parts` envelope, or any other HTTP transport. Resolve every
operation's current supported method, path, media type, concurrency contract,
and body shape independently after classifying the business operation.

When batch transport is unsupported but each item operation advertises PATCH,
render one approval group containing the ordered independent PATCH requests.
Disclose that the group is not transport-atomic, verify after every request,
and stop on the first failure or changed precondition. Never fall back from a
rejected batch to PATCH, or from PATCH to batch, without a newly resolved
preview and fresh approval. If any operation has no authoritative contract,
block the complete group before the first write.

## Invalidation and approval groups

Invalidate approval and produce a new preview when the environment, operation,
target identity, current state, payload, artifact, ESS parameters, expected
impact, or operation order changes. Reject negative, conditional, ambiguous,
stale, and different-preview responses.

Immediately before execution, recompute the canonical fingerprint from the
actual environment, route, operation, identity, payload or ordered steps and
preconditions. Comparing two cached hash strings is insufficient. Builders
snapshot caller input; runners use the exact preview and the applicable
`approval_is_current` helper. Re-read and compare state-dependent preconditions;
a changed target/state requires a new preview. For a Library Goal status update,
pass the fresh full `current_state` to `approval_is_current`; absent or changed
precondition values invalidate approval. For Library Goal verification,
pass current metadata (including localized availability meanings when resolved)
to `verify_created_goal`; compare every approved field and verify any declared
generated GoalId/GoalExternalId relationship before completion.

When several operations are pending, either:

- request approval for each labeled operation separately; or
- show one complete, ordered approval-group preview and request one approval
  for that exact plan. The preview must distinguish one transport request from
  multiple transport requests.

Never infer that approval for one operation authorizes a different mutation,
an automatic retry, a fallback route, or a later Run Book status change.
