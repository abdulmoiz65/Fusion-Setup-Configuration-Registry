# Performance Templates REST Execution

This task-local contract declares the executable REST route for Performance
Templates. It supplements, but does not replace, the FSM CSV import route.
The machine-readable authority is `ora_rest_execution.json`.

## Supported operations

All twelve Describe contexts support collection `GET`, item `GET`, collection
`POST` create, and item `PATCH` update when the same target Describe declares
that action. Child contexts also support item `DELETE` when the target Describe
declares it. Reject root standard `DELETE` when the target Describe omits that
item action; use the declared custom delete route. The root custom actions `getFastFormulaList`,
`findByAdvancedSearchQuery`, `deletePerformanceTemplate`,
`duplicatePerformanceTemplate`, and `submitEssRequestForTemplate` are supported
only with the method, parameters, and mutation classification in the JSON
contract. `upsert` remains explicitly unsupported.

The root create route requires `roles` as a declared nested create child and
also permits `alerts` for non-Anytime templates when a selected process flow
supplies task-alert defaults. Template alerts are unavailable for
`ORA_ANYTIME`, even when the REST child resource accepts a row. Direct alert
mutations must bind the fresh parent template type as
`parent_template_type_code`; the executable contract rejects `ORA_ANYTIME`
creates and updates before preview and includes the context in the approval
binding. A fresh-ETag delete is permitted only to remove an exact unsupported
alert row already present on an Anytime template.
Each row is validated against its target child Describe; the parent-managed
`TemplateDefnId` is omitted because Fusion assigns it from the new root in the
same request. This deep-create payload is a new mutation artifact and requires
its own exact approval. Do not treat an earlier root-only approval as authority
for nested role or alert writes.

An existing-template request that adds a template role and gives it section
participation is not a supported split REST mutation. The role create is
validated against section participation before the server-generated
`TmplRoleId` is available to the separate role-action child route. Do not send
the isolated role create as a probe. Obtain the user's exact section choice,
then use the task's validated FSM archive workflow for the complete role and
role-action graph and verify saved state after terminal success.

Deleting a template role and its last section role action is supported only by
the task-declared `atomic_role_delete` ADF REST batch after all root references
and period questionnaires for that role have been removed or replaced and
verified. Resolve the current process flow and its tasks before preview. When
it requires participant selection or feedback, require an explicit compatible
replacement-flow choice; never clear a flow required by existing periods or
guess its replacement. Supply one fresh raw ETag for
each exact child. The wrapper serializes each guard as a one-value `ifMatch`
array and preserves raw commas in ADF composite keys. It accepts exactly one role-action DELETE and one
template-role DELETE for the same template, rejects wildcard guards and extra
parts, and sends them in one all-or-none batch transaction. Do not issue the
two child DELETE requests separately. Do not use an FSM archive with omitted
rows for deletion: FSM import merges supplied rows and omission does not prove
that an existing row was removed. Verify exact absence of both children and
preservation of the template and sibling graph after the batch response.

Eligibility-profile child creates must include the create-only owner identity
required by the target resource. The wrapper binds `TalentObjectType` to
`TEMPLATE` or `TEMPLATE_PERIOD` for the selected scope and requires
`TalentObjectId` to match the applicable numeric parent identity. It rejects a
missing, mismatched, or cross-parent owner before producing a preview.
Eligibility-profile item routes use the scalar
`TalentEligibilityProfileObjectId` returned by the target PrimaryKey finder;
other nested item routes retain their declared composite keys. A scalar key
does not relax concurrency: eligibility PATCH and DELETE still require the
fresh non-wildcard HTTP ETag from the exact item response. Stop before preview
when the provider does not return one.

Use `scripts/performance_template_rest.py`. The wrapper validates the selected
scope, action, parent identity, item identity, target action, payload field
names, field mutability, required create fields, and custom-action parameters
against the supplied target Describe bytes. It rejects a target environment
other than the one named by the request specification and properties file.

Every item `PATCH` or `DELETE` specification must provide the fresh item ETag
as `if_match`. The immutable preview sends it as `If-Match` and binds it with
the other headers. A stale preview therefore fails the server precondition
instead of silently overwriting or deleting a concurrently changed row.

## Preview and approval

`preview` is offline and makes no network request. It writes an immutable JSON
preview containing the exact relative path, method, query, required headers,
canonical compact JSON body, payload digest, Describe digest, contract digest,
and request-binding digest. A mutation preview is not approval.

For one live mutation, obtain a later explicit approval that names the exact
`preview_sha256`, target environment, method, and path. Do not manufacture or
reconstruct this approval. `execute` reloads the preview and approval, verifies
all digests and binding fields, obtains OAuth through the shared authentication
service, and calls `rest_client_common.request_bytes` exactly once. It never
automatically replays `POST`, `PATCH`, or `DELETE` after an authentication, transport, or
uncertain response.

Read-only `GET` and the two read-only POST actions may execute without mutation
approval, but still require a validated preview. Every request includes
`REST-Framework-Version: 9`. Payload-bearing operations use the resource item
media type; custom actions use the ADF action media type.

The advanced-search action accepts server sort rows only for `Name`, `DateFrom`,
or `DateTo`, with `asc` or `desc` direction. Reject derived display fields and
unknown sort keys during preview rather than sending an unsupported sort.

## Verification and failure boundary

A successful write response is submission evidence, not sufficient acceptance
evidence. Build and execute a fresh exact-identity `GET` preview, then compare
all requested fields and preserved parent/child state. For child or custom delete,
verify exact absence and the intended child graph only. For duplicate, verify
new identities and the selected periods while confirming that the source is
unchanged. For ESS submission, retain the request identifier and monitor only
through a separately declared status workflow; never call submission again on
timeout.

An authentication response, transport failure, timeout, malformed response, or
lost connection after a write is an uncertain outcome. Reconcile with a safe
read and require a new exact preview and approval before any further write.
