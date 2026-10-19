# Alert Foundation Mutation Runbook

## Scope

Contract 0.11.0 uses [simple/default or deep validation](validation-modes.md),
independent of sequential versus batch submission. Simple CREATE performs local
checks only; references below to live describe, LOVs and duplicate searches are
deep CREATE gates. Existing-item identity/state and post-write verification
requirements apply in both modes. No simple-mode live preflight is implied.

This document describes the default **sequential** route. An explicit
`batch-create` request must use [the batch-create runbook](batch-create-runbook.md)
for packaging, approval and execution. Do not apply sequential headers, per-Alert
approvals, separate child writes or Body PATCH operations to a batch work unit.

This runbook owns approved direct REST mutation processing for the Alert
Foundation provider. It does not replace the compiled `ora-resource` validation
and gating plan. It does not authorize a call by itself.

Supported mutation intents are create, update, disable, delete, and copy.
Upsert and `processAlert` are excluded. Parent and child writes remain separate
REST mutations. Version `0.8.0` may bind one approval to the exact ordered
Alert POST, Template POST, optional inline Body PATCH, and Recipient POST
operations in one Alert hierarchy; other writes retain individual previews and
approvals.
For a created template, retain `TemplateId` as the internal identity and use
the server-returned `TemplateCode` canonical key/URI for subsequent template
item and child paths.

## Execution Route

Use `core.fusion-api.rest-api-client` and its standard Fusion REST client. Use
the target environment configured through the shared OAuth flow and never
persist or display tokens, credentials, or authorization headers.

| Intent | Method and relative URI | Body |
|---|---|---|
| create | POST `/hcmRestApi/resources/11.13.18.05/eventAlerts` | Canonical reviewed parent JSON |
| update | PATCH the server-returned canonical item URI `/hcmRestApi/resources/11.13.18.05/eventAlerts/{canonicalKey}` | Canonical JSON containing only approved changed fields |
| inline Template Body | PATCH `/hcmRestApi/resources/11.13.18.05/eventAlerts/{alertCanonicalKey}/child/templates/{templateCanonicalKey}` | `{"Body": "<exact approved plain text>"}` |
| disable | PATCH the server-returned canonical item URI `/hcmRestApi/resources/11.13.18.05/eventAlerts/{canonicalKey}` | `{"EnabledFlag": false}` unless another approved field is explicitly included |
| delete | DELETE the server-returned canonical item URI `/hcmRestApi/resources/11.13.18.05/eventAlerts/{canonicalKey}` | No body |
| copy | POST `/hcmRestApi/resources/11.13.18.05/eventAlerts/{canonicalKey}/action/copyAlert` using the server-returned canonical key | Exact body required by the current compatible describe contract |

Send `REST-Framework-Version: 9` while the target describe contract requires it.
Never set `Upsert-Mode=true` in this provider version.

For inline plain-text template content, create the Template without `Body`,
verify the server-returned `TemplateCode`, then PATCH the exact Template item
with only the approved `Body` field. Version `0.8.0` accepts HTTP 200 from this
PATCH as the operation result. Record that independent stored-content read-back
is deferred; do not claim exact Body verification. Do not validate or transform
the Body content, and do not Base64-encode it.

Keep file-based content separate. `BodyFilePath` and `BodyFileSHA256` retain the
future raw-byte enclosure plan. When either file field is supplied, stop before
mutation because the shared REST client still has no reviewed raw-file route.
Never persist arbitrary Body content in diagnostics.

For a Template Recipient create, precompute its exact URI from the reviewed
`AlertCode` and `TemplateCode`, then require each create read-back to return
those same canonical keys before continuing. POST to
`/hcmRestApi/resources/11.13.18.05/eventAlerts/{alertCanonicalKey}/child/templates/{templateCanonicalKey}/child/recipients`
with only `RecipientCode`, `ChannelType`, and `ValueExpression`. In deep mode resolve
`ChannelType` from `ORA_HRC_ALERT_CHANNEL_TYPE`. Require `ValueExpression` and
apply the local maximum-length check. Live validation through the eventAlerts
`validateExpression` action is deferred in version `0.8.0`; do not call it and
do not make it a work-unit readiness gate.

## Single-Approval Create Work Unit

Define one work unit per included Alert hierarchy. It contains the parent Alert
CREATE followed by each Template CREATE, its optional inline Body PATCH, and
that Template's Recipient CREATE operations. The work unit is eligible only
when every URI can be formed exactly from reviewed `AlertCode`, `TemplateCode`,
and `RecipientCode` values and no file-based Body fields are populated.

Canonicalize each payload with sorted keys and compact separators. Record its
SHA-256. Then canonicalize one approval document containing the contract
version, execution mode, validation mode and policy, exact HTTPS Fusion origin, workbook SHA-256, ordered operations,
effects, exact verification GETs, and the following execution policy:

- Verify every mutation before the next write. Parent, Template, and Recipient
  creates use independent GET comparison; inline Body PATCH uses accepted HTTP
  200 response verification in version `0.8.0`.
- Stop on the first HTTP, verification, or canonical-key failure.
- Never retry or roll back a write automatically.
- Preserve and report verified earlier operations as partial success.

Compute one aggregate SHA-256 over that document and request exactly
`Confirm Alert Work Unit <SHA-256>` immediately before execution. Approval is
invalid after any change to validation mode/policy, environment, source digest, operation order,
method, URI, payload, effect, verification contract, or execution policy.

Submit each approved operation exactly once. After each POST, GET the approved
item URI, compare every approved payload field, and confirm the returned
canonical key equals the supplied code. After an inline Body PATCH, require
HTTP 200 before continuing; do not perform an unsupported Body read-back. Stop
before the next mutation on any mismatch or unaccepted response. A recovery,
retry, or compensating DELETE is a new mutation and requires a new immutable
preview and approval.

## Mandatory Sequence

1. Build the Alerts task execution plan with `--setup-task Alerts` and require
   `status: planned` with task readiness `ready`.
2. Complete every reached validation, lookup, dependency, and design node.
3. Bind the configured environment locally. Deep CREATE resolves compatible
   metadata and proves zero exact AlertCode matches using declared reads. An
   existing-item mutation must prove exactly one AlertId, capture the
   server-returned canonical item key/URI, and verify expected state. Do not
   assume the numeric AlertId is the item URI key.
4. For an eligible hierarchy create, build and fingerprint the complete work
   unit described above and obtain its one aggregate approval. For every other
   mutation, canonicalize the payload or explicit no-body DELETE, present its
   individual immutable preview, and obtain individual approval.
5. Before final batch approval, complete Fusion login and require authentication readiness. Batch
   noninteractive dispatch uses only a valid cached token and fails before the
   request when the token is absent or expired. Bind a unique attempt id and
   recovery context into each batch approval digest; a recovery needs a new
   preview and phrase. Submit each approved operation exactly once through the shared REST client.
   Do not automatically retry POST, PATCH, DELETE, or copy after any uncertain
   result.
6. Verify creates through the approved canonical item URI and, when AlertCode
   is available, `findByAlertCode`. For inline Body PATCH, accept only HTTP 200
   and record that independent read-back is deferred. DELETE verification
   requires a not-found result for the exact canonical item and no unexpected
   finder match.
7. Persist a redacted project run record with the preview fingerprint, outcome,
   and verification result only through:

   ```text
   python -B pillars/hcm/hcm-tool/alert-foundation/scripts/skill_run_persistence.py --input-stdin --output <new-run-record.json>
   ```

   The record must contain the schema-permitted `token_usage` object, whose
   estimates and log reference must match the project token-usage log. The helper validates the record against `schemas/skill-run.schema.json`,
   writes atomically, and refuses to overwrite an existing record. Use only
   schema-permitted fields; never include `$schema`, an empty key, or
   `external_ids`. Keep safe external request identifiers in sanitized technical
   evidence or permitted `notes`. Never persist the OAuth cache, authorization
   header, or sensitive template body.
   For batch execution also persist a sanitized, atomic, no-overwrite execution
   receipt. The adapter reserves it after approval validation before authentication
   and fsyncs each transition. It contains only `approval_validated`, `authentication_ready`,
   `request_started`, and `response_received`; before dispatch is
   `not_submitted`, while a started request with no response is `outcome_unknown`.
   Do not automatically retry a POST in either case. A pre-existing or completed
   receipt blocks authentication and dispatch, preventing same-work-unit replay.
   The receipt is the project-owned path
   `project/<project-id>/state/runs/alert-receipts/<attempt-id>.json` embedded
   in the immutable batch approval. The adapter resolves it from repository
   root; the CLI `--receipt-output` must match it exactly and cannot be substituted.

## Authorization Assumption

The product owner states that the executing identity's role/privilege grants
the described eventAlerts CRUD methods when it grants access to the resource.
This is a declared delivery assumption, not a conclusion inferred from GET.
The target environment remains authoritative: a persistent 401 or 403 after
the shared client's single refresh attempt stops execution as an auth/authz
failure.

## Operation-Specific Gates

| Operation | Additional gate |
|---|---|
| create | Require unique AlertCode, explicit AlertType, AlertAccessLevel, EnabledFlag, and TestModeFlag; do not include children in the initial parent request |
| update | Require exact AlertId plus server-returned canonical key/URI, fresh current state, and only explicitly approved changes |
| disable | Require exact AlertId plus canonical key/URI and current EnabledFlag; treat as a state-changing PATCH |
| delete | Require exact AlertId plus canonical key/URI, fresh current state, explicit destructive-effect disclosure, and delete-specific approval |
| copy | Require current describe action contract, exact source AlertId and canonical key/URI, exact action body, duplicate prevention for the copied identity, and copy-specific approval |
| hierarchy create work unit | Require one parent CREATE hierarchy, exact precomputed canonical paths, optional inline Body PATCH operations, no file-based Body input, applicable preflights, one aggregate approval fingerprint, ordered single submissions, and verification after each operation |
| template create | Require the approved parent `AlertCode` canonical key, omit `Body`, submit one Template POST, and verify the returned Template canonical key before a Body PATCH or child mutation |
| inline Template Body | Require a verified Template create, exact Template item URI, plain-text `Body` payload, and aggregate approval; submit one PATCH, accept HTTP 200, and disclose that independent Body read-back is deferred |
| template recipient create | Require approved parent and Template canonical keys, exact channel lookup in deep mode, locally validated expression presence and length, one Recipient POST, and independent read-back |

## Stop Conditions

Stop before submission for a deep-mode incompatible describe or invalid lookup value,
ambiguous identity, unexpected current state, missing method/action contract,
uncertain access-level ownership, stale preview, changed digest, absent exact
approval, changed work-unit content, canonical-key mismatch, or unsupported
upsert/process intent. During a work unit, stop after the first failed or
unverified operation and report partial success without cleanup writes.
