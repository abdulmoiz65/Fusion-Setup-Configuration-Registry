# Alert Foundation Provider Contract

## Contract Status

| Property | Value |
|---|---|
| Provider skill | `hcm.hcm-tool.alert-foundation` |
| Contract version | `0.11.0` for sequential and opt-in batch-create; mode-bound approval |
| Owning pillar | HCM |
| Owning offering | HCM Tool (`CUSTOM_HCM_TOOL`) |
| Operation object | Alerts |
| Initial execution posture | Hybrid planning, validation, governed discovery, preview, and approval-gated CRUD |
| Live mutation posture | One Alert CREATE hierarchy may use a single aggregate approval for its exact Alert/Template/optional inline Body PATCH/Recipient work unit; other eligible CRUD/copy operations retain individual approval; file-based Template Body enclosure, upsert, and process are excluded |

This contract is the stable boundary used by HCM and non-HCM consumer skills.
It does not authorize a Fusion call. Consumers provide alert business intent to
the provider and must not call `eventAlerts`, copy its resource schema, or
select a transport route themselves.

## Validation profile

[Validation modes](validation-modes.md) defines exactly two profiles: `simple`
(default) and `deep` (explicit). This choice is independent of submission style.
Simple CREATE performs local mandatory/type/hierarchy/key/payload/known-length
checks, with no live describe, LOV, language or existing-code duplicate checks.
Fusion validates business codes on submission. Deep adds the declared live
checks and blocks if they cannot complete; it never silently falls back.
Environment/source binding, approval, response checks and independent create
read-back remain mandatory. Existing-item identity/state checks remain mandatory
in either mode. Historical 0.8.0 operation behavior below is retained, except
that live CREATE preflight applies only to deep and all new work-unit approval
documents use 0.11.0 with validation mode and policy included in their digest.

## Consumer Request Contract

A consumer supplies the following logical request. The request may be gathered
interactively or derived from a reviewed Alert Foundation intake workbook.

| Field | Required | Contract |
|---|---|---|
| `contract_version` | Yes | `0.11.0`; older previews must be regenerated before approval. |
| `validation_mode` | No | `simple` by default or explicit `deep`; unknown modes fail closed. |
| `alert_execution_mode` | No | Defaults to `sequential`; explicit `batch-create` selects the additive batch contract and its runbook. It does not change validation depth. |
| `consumer_skill_id` | Yes | Dot-separated identity of the requesting FDOS skill. |
| `project_id` | Yes | Existing FDOS implementation-project identifier used for durable artifacts. |
| `implementation_objective` | Yes | Business outcome for the requested alert configuration. |
| `requested_intent` | Yes | One of `plan`, `inspect`, `verify`, `preview`, `create`, `update`, `disable`, `delete`, or `copy`. `upsert` and `process` are recognized only to return `unsupported_operation`. |
| `target_environment` | Conditional | Non-secret environment identity required before any routed external read. Do not include credentials or tokens. |
| `alert_requirement` | Yes | Business-relevant alert definition described below. |
| `source_artifact` | No | Reviewed workbook or other intake reference plus its SHA-256 when available. The artifact never grants execution approval. |

## Alert Foundation Workbook Mapping

The mapping and sequential behavior below remain backward compatible. For
explicit `batch-create`, the [batch-create runbook](batch-create-runbook.md)
overrides only transport packaging, Body encoding, aggregate approval and batch
response handling. All included CREATE hierarchies form one work unit, never
one unit per part. Existing required fields, codes, IncludeFlag selection,
parent relationships and mode-applicable provider gates still apply. A child marked
YES without an included parent is an input error, not silently discarded.
BodyFilePath/BodyFileSHA256 and non-CREATE intents are blocked in batch mode.

When the source is an Excel workbook, use `spreadsheets:Spreadsheets` when its
artifact runtime is available. For the bounded basic route, invoke
`scripts/read-alert-intake.py` before applying provider-domain rules. The
script uses `openpyxl` read-only, ignores workbook approval claims, emits a
payload plan, and never calls Fusion. This provider owns the following
Alert-specific mapping.

### `Alerts` sheet

| Column | Rule |
|---|---|
| `IncludeFlag` | Include only case-insensitive `YES`; all other values are excluded, not executed. |
| `ClientAlertKey` | Required nonblank workbook correlation key; unique among included alert rows. |
| `Operation` | Required intake intent: `CREATE`, `UPDATE`, `DISABLE`, or `DELETE`. It does not authorize that operation. |
| `AlertId` | Required for existing-item operations and blank for create; re-resolve against Fusion before mutation. |
| `AlertCode` | Required business code; local uniqueness applies in both modes, live CREATE duplicate checks only in deep; existing-item exact identity checks remain required. |
| `Name` | Required; maximum 80 characters under the observed REST contract. |
| `Description` | Optional; maximum 2,000 characters under the observed REST contract. |
| `AlertType` | Required; reject placeholders. Simple uses literal code; deep resolves the target lookup before approval. |
| `AlertAccessLevel` | Required; reject placeholders. Simple uses literal code; deep revalidates before approval. |
| `EnabledFlag`, `TestModeFlag` | Required explicit booleans; normalize case-insensitive `TRUE`/`FALSE` only. |
| `ExpectedCurrentState` | Optional reconciliation assertion; it is not execution approval. |
| `BusinessOwner`, `ConsumerPillar` | Required intake provenance for cross-pillar consumption. |
| `ValidationStatus`, `ValidationMessage` | Informational authoring fields only; they do not replace FDOS validation. |

### `Alert Templates` sheet

| Column | Rule |
|---|---|
| `IncludeFlag` | Include only case-insensitive `YES`. |
| `ClientAlertKey` | Required; must match exactly one included `Alerts` row. |
| `TemplateKey` | Required workbook-local key; unique within its parent alert. |
| `Operation` | Required intake intent: `CREATE`, `UPDATE`, `DISABLE`, or `DELETE`; never authorization. |
| `TemplateId` | Required for existing-item operations and blank for create; re-resolve before mutation. |
| `TemplateCode`, `Name` | Required business values. |
| `MimeType` | Required literal REST code in simple mode. Deep resolves the target lookup and may accept an explicitly resolved mapping; never infer translations in generic core. |
| `DefaultLanguage` | Required; reject placeholders. Simple uses literal code; deep resolves the active-language lookup. |
| `EnabledFlag` | Required explicit boolean; normalize case-insensitive `TRUE`/`FALSE` only. |
| `Subject` | Required template subject. |
| `Body` | Optional inline plain text. When populated for Template CREATE, emit a separate Template item PATCH after the Template POST verifies and before its Recipients. Do not apply content or LOV validation. Treat HTTP 200 from the PATCH as accepted in version `0.8.0`; independent stored-content verification is deferred. Mutually exclusive with `BodyFilePath` and `BodyFileSHA256`. |
| `BodyFilePath` | Optional path relative to the workbook directory. When supplied, `BodyFileSHA256` is also required. Reject absolute paths and scope escape. |
| `BodyFileSHA256` | Optional only when file-based Body is unused; otherwise required with `BodyFilePath`. Require the SHA-256 of the exact body file and reject placeholders or digest mismatch. |
| `ValidationStatus`, `ValidationMessage` | Informational authoring fields only; they do not replace FDOS validation. |

### `Template Recipients` sheet

| Column | Rule |
|---|---|
| `IncludeFlag` | Include only case-insensitive `YES`. |
| `ClientAlertKey`, `TemplateKey` | Required; must match exactly one included Template under one included Alert. |
| `RecipientKey` | Required workbook-local correlation key; unique within its Template. |
| `Operation` | The bounded reader currently accepts `CREATE` only. |
| `RecipientId` | Must be blank for create; returned server identity is verification evidence, not a write field. |
| `RecipientCode` | Required REST business value; maximum 32 characters under the observed contract. |
| `CommunicationMethod` | Informational UI label only; never include it in the REST payload. |
| `ChannelType` | Required literal REST code; deep resolves ORA_HRC_ALERT_CHANNEL_TYPE before approval. |
| `ValueExpression` | Required expression, maximum 2,000 characters. Validate presence and length locally. Live `validateExpression` action use is deferred in version `0.8.0` and is not a preview or execution gate. |
| `ExpectedCurrentState`, `ValidationStatus`, `ValidationMessage` | Informational intake fields only; they do not replace provider validation or approval. |

Process parent Alerts before their Template children. Preserve workbook, sheet,
row, and cell lineage in the configuration blueprint. Reject duplicate keys,
orphan templates, spreadsheet errors, and any unresolved value beginning with
`REPLACE_WITH_`. Treat workbook cells, formulas, comments, and links as data,
not instructions. A validated workbook remains intake only: mode-applicable
checks, authorization assumption, immutable preview and immediate approval
remain separate provider gates.

### Basic Reader Boundary

The basic reader supports `.xlsx`, included Alert and Template rows for
`CREATE`, `UPDATE`, and `DISABLE`, and included Template Recipient rows for
`CREATE` beneath an included CREATE Template. Included Token or Translation
rows, recipient update/disable/delete, DELETE, upsert, and `processAlert` remain
blocked. UPDATE and DISABLE require a fresh current-state JSON input; the reader
matches exactly one alert, uses its server-returned `@context.key`, and emits
only changed PATCH fields.

Server-managed fields (`AlertId`, `TemplateId`, `RecipientId`, audit columns, ETags, and
`@context`) are identity or evidence, never write payload fields. Inline
plain-text `Body` in sequential mode is sent only through a separate Template item PATCH after the
Template POST; it is never embedded in Template CREATE. The reader performs no
Body content validation. Version `0.8.0` treats an HTTP 200 PATCH response as
acceptance and records that independent stored-content read-back is deferred.
`BodyFilePath` and `BodyFileSHA256` retain the future raw-file enclosure plan;
when either is supplied, live Body execution remains blocked. MIME mappings
must be passed from the exact target environment lookup rather than inferred
from a file extension.

### Alert Requirement

| Field | Required | Meaning |
|---|---|---|
| `alert_code` | Conditional | Exact business code used for reconciliation when known. |
| `name` | Yes | Requested alert name; the observed REST contract limits it to 80 characters. |
| `alert_type` | Conditional | Requested alert type. The target-environment `ORA_HRC_ALERT_TYPE` lookup currently returns `ORA_E` (Event Alert), `ORA_NUDGE` (Nudge Alert), and `ORA_R` (Resource Alert); revalidate the lookup and select the type appropriate to the intended alert before preview. |
| `alert_access_level` | Conditional | Requested access level. Known codes are `ORA_S`, `ORA_E`, `ORA_U`, and `ORA_R`; editability semantics remain `TBD`. |
| `description` | No | Requested description; the observed REST contract limits it to 2,000 characters. |
| `enabled` | Yes | Desired enablement decision. No default is inferred by the provider. |
| `test_mode` | Yes | Desired test-mode decision. No default is inferred by the provider. |
| `trigger_and_filter_intent` | Conditional | Business description of the triggering resource and filter behavior. |
| `templates` | No | Requested template codes, names, MIME types, subjects, body references, languages, and enablement. |
| `tokens` | No | Requested token codes, names, and descriptions. |
| `translations` | No | Requested language, source language, translated name, and translated description. |

Consumers must not supply server-managed audit values as requested write
fields. `AlertId`, `TemplateId`, and `TokenId` are resolved or returned Fusion
identities, not workbook-local business keys.

## Provider Response Contract

The provider returns one logical response with the following fields. A
consumer must not infer success from an HTTP status alone.

| Field | Required | Contract |
|---|---|---|
| `contract_version` | Yes | Provider contract version used for the response. |
| `provider_skill_id` | Yes | `hcm.hcm-tool.alert-foundation`. |
| `consumer_skill_id` | Yes | Echo of the requesting skill identity. |
| `status` | Yes | `planned`, `inspected`, `verified`, `preview_ready`, `approval_blocked`, `completed`, `partial_success`, `validation_failed`, `unsupported_operation`, or `external_operation_failed`. |
| `resolved_route` | Yes | Selected FDOS workflow route, or `none` when routing is blocked. |
| `configuration_blueprint` | Conditional | Canonical parent/child intent with source-row correlation and no secrets. |
| `current_state_evidence` | Conditional | Sanitized exact-match, finder, item, or child-read evidence obtained through the routed read-only workflow. |
| `lookup_and_dependency_evidence` | Conditional | Resolved values and unresolved `TBD` gaps. |
| `execution_preview` | Conditional | Immutable environment, method, URI, canonical payload or no-body operation, SHA-256 digest, effect, and verification request. Its presence is not approval. |
| `execution_work_unit_preview` | Conditional | For one eligible Alert CREATE hierarchy, the exact target environment, source-artifact digest, ordered operations, methods, URIs, canonical payloads, per-operation digests, effects, verification requests, execution policy, aggregate SHA-256, and approval phrase. Its presence is not approval. |
| `execution_result` | Conditional | Individual or work-unit result with sanitized per-operation HTTP status, returned identity, verification, partial-success state, and safe external request identifiers. |
| `verification_result` | Conditional | Requested-versus-actual comparison from an independent read. |
| `diagnostics` | Conditional | Redacted failure class, stage, safe message, environment identity, request or ECID identifiers when available, and recommended action. |
| `artifact_refs` | Yes | Durable project artifact and run-record references. |

## Provider Responsibilities

The Alert Foundation provider owns:

1. Capability scope and this consumer contract.
2. Classification of planning, read-only, mutation, and notification intents.
3. Validation of the consumer request and intake provenance.
4. Selection of an FDOS-declared route; an endpoint, OAuth session, browser,
   or successful describe call is not a route.
5. Local uniqueness, deep CREATE live duplicate checks, and exact existing-item identity checks in both modes.
6. Canonical configuration blueprints, immutable previews, verification
   expectations, sanitized diagnostics, and project artifact references.
7. Shared access-level safety and compatibility policy.

Core services continue to own OAuth, REST transport, role/access diagnostics,
Data Loader behavior, project-state persistence, and artifact registration.
Consumer skills continue to own their product-specific business rules.

## Observed REST Capability Boundary

The read-only demo probe established this contract shape for the observed
release. It did not certify a live execution route.

| Concern | Observed contract |
|---|---|
| Resource | `/hcmRestApi/resources/11.13.18.05/eventAlerts` |
| Required framework header | `REST-Framework-Version: 9` for the probed contract |
| Item identity | `AlertId` is the returned internal identity. The verified create response used `AlertCode` as `@context.key` and in the canonical item path, for example `/eventAlerts/EXAMPLE_ALERT`; use the server-returned canonical key rather than assuming the numeric AlertId is the URI key. |
| Business finder | `findByAlertCode(AlertCode)` |
| Alternate finder | `findByNameAndAccessLevel(AlertAccessLevel, Name)` |
| Parent reads | Collection and item `GET` |
| Child reads | `templates`, `tokens`, and `translations` |
| Described mutations | Collection create/upsert; item update/delete; child mutations where exposed |
| Described actions | Collection lookup/validation actions; item `copyAlert` and `processAlert` |

Deep preflight confirms a compatible target describe contract. Simple CREATE
uses the reviewed fixed adapter without a describe call. A service rejection
stops the run; do not silently change release paths, headers or modes.

## Operation Posture

| Operation class | Version `0.8.0` posture | Required behavior |
|---|---|---|
| Plan and validate intent | Available | Produce a blueprint and list every unresolved fact. |
| Describe compatibility | Eligible read-only operation | Run only after the implementation workflow selects its external-read step. |
| Collection, finder, item, and child reads | Eligible read-only operations | Require environment identity, exact selectors, bounded retry, and sanitized evidence. |
| Payload preview | Available without submission | Produce canonical JSON and a digest; do not treat the preview or workbook as approval. |
| Alert hierarchy create work unit | Single aggregate approval | Require one Alert CREATE, zero or more Template CREATE operations, each optional inline Body PATCH, and zero or more Template Recipient CREATE operations. Resolve exact canonical paths from the supplied codes, complete applicable preflights, bind approval to the aggregate work-unit SHA-256, then submit and verify each operation in order. |
| Other create | Individually approval-gated | Require compatible describe, explicit fields, unique identity, immutable preview, exact immediate approval, one POST, and exact read-back. |
| Inline plain-text Template Body | Aggregate approval-gated | POST the Template without Body, verify its canonical key, then PATCH the exact Template item with only `Body`. Accept HTTP 200 as the version `0.8.0` result and disclose that independent Body read-back is deferred. |
| File-based Template Body enclosure | Excluded | The workbook may validate the file and digest for planning, but live raw-byte upload remains unavailable until the shared REST client exposes a reviewed raw-file route. |
| Update or disable | Approval-gated | Require exact AlertId, fresh current state, immutable changed-field preview, exact immediate approval, one PATCH, and exact read-back. |
| Delete | Approval-gated and destructive | Require exact AlertId, fresh current state, explicit destructive disclosure, delete-specific immediate approval, one DELETE, and not-found reconciliation. |
| Copy | Approval-gated | Require the current describe action contract, exact source AlertId and body, duplicate prevention, immediate approval, one action POST, and exact read-back. |
| Upsert | Excluded | Stable upsert identity and duplicate behavior are not certified; use explicit create or exact-item update. |
| `processAlert` | Excluded | Treat notification delivery as a separate high-impact capability requiring independent design and certification. |

## Mutation Delivery Assumptions and Boundaries

The product owner states that the executing identity's existing role/privilege
grants the described `eventAlerts` CRUD methods when it grants resource GET
access. Record that statement as the security basis for this delivery. Do not
represent GET as technical proof of write authorization; a persistent runtime
401 or 403 remains authoritative and stops execution.

The initial mutation boundary is deliberately narrow:

- In deep mode, revalidate target describe and lookup values before approval.
- Require explicit create fields; do not inherit enablement or test-mode defaults.
- Require zero exact live AlertCode matches for deep CREATE and one exact AlertId for existing-item operations in either mode.
- Keep parent and child changes as separate ordered REST calls; initial parent create contains no children. One aggregate approval may cover all calls in one eligible Alert hierarchy create work unit.
- Treat copy as its own action contract and keep `processAlert` excluded.
- Keep upsert disabled until its stable identity and duplicate semantics are certified.
- Require one submission per operation and no automatic write retry or rollback. Parent, Template, and Recipient creates require independent exact read-back. Inline Body PATCH uses accepted HTTP 200 response verification in version `0.8.0`.

Method eligibility does not authorize a call. For an eligible hierarchy
create, the provider must present one exact immutable work-unit document and
obtain approval bound to its aggregate SHA-256 immediately before execution.
For all other mutations, present the individual environment, URI, method,
canonical payload or explicit no-body delete, payload digest, effect, and
verification plan immediately before its one submission.

## Alert Hierarchy Create Work Unit

One work unit contains exactly one included Alert CREATE and its included
Template CREATE, optional inline Body PATCH, and Template Recipient CREATE
operations. It is eligible only when every method, URI, payload, verification
contract, and supplied business key is known before approval. File-based Body
inputs remain ineligible.

The approval document must include:

1. Contract version, execution mode, validation mode and policy, exact HTTPS Fusion origin, and source-workbook SHA-256.
2. Parent-first ordered operations with sequence, entity, method, exact URI,
   canonical payload, payload SHA-256, business effect, and exact verification
   contract. Creates use an exact GET plus compared fields; inline Body PATCH
   uses accepted HTTP 200 response verification.
3. Execution policy: verify after every mutation, stop on first failure, never
   retry or roll back automatically, and stop when a returned canonical key
   differs from the approved `AlertCode`, `TemplateCode`, or `RecipientCode`.
4. One aggregate SHA-256 computed from the canonical approval document.

The only valid single-approval phrase is `Confirm Alert Work Unit <SHA-256>`
for the currently presented document. Any change to validation mode/policy, environment, source
artifact digest, operation order, method, URI, payload, effect, verification,
or execution policy invalidates approval. Authentication refresh does not
change the approved work unit, but all mode-applicable gates must pass before
the phrase is requested. Simple CREATE needs no live gate evidence.

The approval is atomic; execution is not. On failure, retain verified earlier
creates, stop before the next write, report `partial_success` with the failed
sequence, and require a new preview and approval for retry or cleanup. Never
issue a compensating DELETE under the original approval.

## Failure and Retry Contract

| Failure class | Provider behavior |
|---|---|
| `input_validation` | Stop before external access and identify the invalid field. |
| `catalog_or_metadata_mismatch` | Stop on incompatible describe metadata or ambiguous identity. |
| `auth_expired_or_invalid` | Permit the core OAuth route to refresh a cached token once. |
| `authorization_or_privilege` | Stop after a rejected refresh or runtime 401/403; report that the declared role-access assumption did not hold for this operation. |
| `transport_or_environment` | Retry only eligible read-only calls with bounded attempts; record the environment. |
| `fusion_api_error` | Return sanitized status, path, response summary, and ECID or request identifier when available. |
| `approval_blocker` | Stop. Do not reinterpret intake approval fields as FDOS approval. |
| `partial_success` | Stop the work unit after the first failed or mismatched operation, preserve verified earlier results, and require a new approved work unit or individual mutation for recovery. |

Never persist credentials, authorization headers, OAuth tokens, token-cache
contents, private keys, arbitrary template body contents, or customer data in
reusable repository files or diagnostics.

## Consumer Rules

1. Depend on `hcm.hcm-tool.alert-foundation` rather than reproducing the
   `eventAlerts` implementation.
2. Pass business intent, not a raw endpoint, HTTP method, or hand-built
   payload.
3. Preserve the returned provider status and artifact references.
4. Do not switch to FSM, HDL, Data Loader REST, direct REST, or browser
   execution when the provider reports a missing or blocked route.
5. Do not interpret `planned`, a workbook approval reference, or an immutable
   preview as a completed Fusion change.
6. Keep consumer-specific trigger and product rules in the consumer skill;
   keep alert resource, access, safety, and verification policy in this
   provider.

## Source Boundary

This version is based on the generated FDOS catalog identity, the
Oracle-internal HCM Tool Alert Foundation ownership baseline, and the retained
read-only `eventAlerts` describe/access-level probe, plus the product owner's
declared CRUD authorization assumption. The compiled `ora-resource` rules and
`mutation-runbook.md` define the allowed execution boundary; behavior they do
not define remains unavailable.
