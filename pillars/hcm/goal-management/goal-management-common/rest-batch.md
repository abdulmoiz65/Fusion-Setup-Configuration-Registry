# Explicit Goal Management REST batch

This opt-in transport supplements existing object workflows. It is not HDL batch
upload, FSM CSV import, or ESS assignment. Existing specialized batching is unchanged.

## Selection

Run `goal-management-common/scripts/goal_management_route_selector.py`. Positive explicit REST +
batch intent selects `route=rest`, `transportIntent=adf_batch`. Multiple records,
“bulk”, and one approval alone do not select it. HDL requests retain the loader
route. Conflicting REST/HDL instructions stop for clarification. Normalize source
documents first, then reselect with the same intent. No new HTTP/auth client is used.

## Preparation and execution

1. Complete project/runbook checks and the owning object skill's existing REST
   preparation: privileges, current contracts, lookups, writable fields, duplicates,
   fresh identity, dependencies, and lifecycle validation. Reuse its validated
   entity body. Activation is its existing status update. Do not borrow worker
   `developmentGoals` or transaction-context bodies for Library Goal setup.
2. Only when the route selector returns `transportIntent=adf_batch`, call
   `goal-management-common/scripts/resolve_goal_management_batch_contract.py`. For parent CRUD on
   `reviewPeriods`, `libraryGoals`, and `goalPlans`, it combines the maintained
   capability registry with the current collection/item method advertised by
   describe. It ignores `batchEnabled` on unrelated custom actions. Standard REST,
   HDL, FSM, and intake routes bypass this resolver unchanged. Unsupported paths or
   absent current CRUD methods stop without a live mutation probe.
3. Call `goal-management-common/scripts/goal_management_rest_batch.py:resolve_and_build_preview`
   with intent, batch_root, operations, current runtime metadata, and a reviewed
   positive max_parts limit. The resolver supplies `batch_enabled`, operation
   evidence, transaction context, and the exact combination contract. Each operation
   supplies id, operation(create/update/delete), relative path, existing payload,
   resolved identity, fresh before values, validated=true,
   dependencies_verified=true, dependencies, and any exact `ifMatch` established by
   the owning workflow. These are internal inputs, not questions for business users.
   Object builders remain responsible for business validation.
4. Independent Goal Plans, Review Periods, and Library Goals can share a batch
   when their contracts allow it. performanceGoalsV2 uses only the existing
   Goal Plan template-goal contract. Children retain their advertised paths and
   required parent parts. No arbitrary custom actions or ESS in this CRUD adapter.
5. Prepare one dependency-ready stage at a time. Create Review Periods, verify IDs,
   then prepare dependent plans; verify created plans before children/activation.
   Preserve maximum-enforcement verification and Primary-plan constraints. No
   guessed IDs, generated-ID interpolation, create-plus-later-activation merging,
   or silent splitting. Oversized batches require an explicit staged plan.
6. Persist the immutable preview/fingerprint through existing project services.
   Present environment, exact parts, identities, old/requested values, dependencies,
   and transaction boundary. Obtain explicit approval immediately before execution.
   Re-read preconditions; stale state requires a rebuilt preview and new approval.
   Call assert_approved with the stored approved fingerprint.
7. Submit the exact request once through the owning workflow's existing
   core.fusion-api.rest-api-client and auth. POST to the resolved HCM resource root
   with application/vnd.oracle.adf.batch+json. Never append /$batch. Never execute
   directly from this helper, bypass a workflow gate, or infer live approval from
   repository-edit approval.
8. Re-read every affected object/child through the owning skill, including protected
   fields. Call reconcile with HTTP status, response, and verified_after keyed by
   part ID containing matches and actual after values. Persist the per-part audit,
   fingerprint, environment, timestamp, response/diagnostic references and available
   ECID in the active project. Redact diagnostics; no credentials or customer data
   in tracked source files. Missing response parts are not successful.

## Failure boundaries

### Enforced combination contract

The builder now requires `combination_contract`: `batch_root`, a nonempty
`transaction_context`, an `evidence` reference for the combined pattern, `pattern`,
and the exact ordered `parts` list of `{id, path, operation}`. Each operation's
contract must carry that same transaction context. Do not synthesize capability
evidence from the fact that individual endpoints exist. Missing evidence blocks
preparation. The combination contract is included in the approval fingerprint.

Each operation must explicitly provide `dependencies` (empty for independent
work). A dependency is `{part_id, verified, evidence}` from a previously verified
stage. Any dependency on a part in the current batch is rejected, even if marked
verified. Cross-part `$ref`, `${...}`, and `{{...}}` payload placeholders are
rejected. No automatic staging, guessed identifiers, or silent request splitting.

The local eligible patterns are deliberately narrow. For `independent_setup`,
the maintained registry establishes ADF batch eligibility while the resolver
requires the current tenant to advertise the corresponding ordinary CRUD method:

- `independent_setup`: parent creates or item updates/deletes for Goal Plans,
  Review Periods, and Library Goals, including independent create+update mixes.
- `template_goal`: only the existing `performanceGoalsV2` create/update contract;
  cannot be mixed with unrelated setup parts.
- `document_association`: each child create/delete must have one matching Goal
  Plan update. Every member carries `required_group: {id, parts}` with the same
  complete ordered group part IDs. Missing/reordered members, unrelated parts,
  and mismatched parent IDs are rejected.

Other child routes and specialized combinations remain on their owning skill's
existing route until an evidenced pattern and regression tests are added. These
restrictions affect only the new explicit batch adapter, not existing workflows.
Resolvers must derive dependencies and current CRUD evidence from actual business
intent and runtime reads. Caller-supplied booleans or an unrelated action's
`batchEnabled` value are not capability evidence.

Standard ADF batch failures roll back that batch, not earlier stages. Errors,
missing/duplicate IDs, timeout, and HTTP success without verified reads stop for
review. Never automatically replay mutations, compensate, or switch to HDL or
individual REST. Preserve earlier verified stages; diagnose and obtain fresh
approval for any retry. Activation does not include ESS assignment. Deletion
retains exact-target approval; one approval is not transport capability evidence.

Classify input/path/size errors as input validation, unsupported contracts as
catalog mismatch, changed approvals as approval blocker, and live failures with
the existing auth/authz, transport/environment, or Fusion API categories. Retain
the exact request identity on timeout; no automatic retry.

Reference: [Oracle ADF batch requests](https://docs.oracle.com/en/middleware/developer-tools/adf/12.2.1.4/develop/consuming-adf-restful-web-services.html).
