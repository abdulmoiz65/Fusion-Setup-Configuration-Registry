# Routed execution and recovery

## Intake and offline planning

For implementation, enter through router/implementation-router/SKILL.md and
select this core skill explicitly. Consume prior project evidence before asking
for missing inputs. Record project, environment origin/release, exact scope,
source key mappings, structure flags, parameters and source timestamps.
Structure and source-record resolution must come from an already selected pillar
or project evidence route: the PDFs do not provide those lookup endpoints.

Run the offline helper and preserve the plan. It has no live option and does not
read environment properties. Tree creation requires explicit Data Source
Parameters. Before every external mutation, GET and fully paginate fndTrees,
filter exact TreeStructureCode matches, then read every resolved tree's
child/FndTreeDataSourceParamsVO. Normalize DataSourceId, ParameterId and
ParameterValue as trimmed NFC strings and compare the complete tuple collection.
A matching tree permits creation; no same-structure tree records assumed_correct
and permits it. Same-structure trees with no matching collection require a
persisted exception diagnostic and stop before every mutation. The initial
compound mutation contains only the tree and Draft version(s), plus those complete
parameters. Resolve TreeVersionId from the response,
then issue addValueTreeNode once for every requested node. Root actions use an
empty parentTreeNodeId; children wait for their parent TreeNodeId. A generic
describe-required TreeVersionId does not override the explicit create omission
policy.
For each Draft version create, resolve and freeze ChangedSinceValidation,
LevelCount and NodeCount before approval: blank/missing validation status becomes
`"Y"`, and missing/null counts become 0. Reject invalid explicit values. Do not
add or default these fields in PATCH.

Before the parameter comparison and every mutation, validate each supplied source
member value through the existing domain resolver selected from the tree
structure and DataSourceId evidence. The resolver must prove that the supplied
source record exists and is valid for the planned member key. Do not use
`fndTreeNodes` at this stage: a TreeNodeId identifies a node already created in a
tree, not the Position, Department, Organization, or other source record supplied
as a PK value. Record the selected resolver and its response evidence. If the
structure/data-source evidence does not identify an applicable existing resolver,
persist a catalog-mismatch artifact and stop rather than guessing an API.

## Declared read-only prerequisite step

Only after context is established, select
core.fusion-api.rest-api-client and its references/fusion-rest-api.md. That route
may invoke core.auth.fusion-oauth-authentication; no separate OAuth implementation.
Use the declared collections/finders/describe in contracts.md to establish exact
existing identities, absence of duplicates, target field support and item links.
Use a maximum of 100 pages per collection, 500 records per page if supported;
on exceeding the budget report incomplete lookup and require a narrower scope.
Do not substitute an unlisted endpoint or browser Fusion navigation for a gap.

Confirm environment identity without logging credential configuration. Do not
request privilege attestation or administrator evidence before a read or
mutation; the target environment is authoritative and may reject an unauthorized
request. Do not fabricate role names. Record an authorization error if it occurs.
For catalog-backed caller tasks check catalog flags and the declared route before
using this skill. Standalone core requests have no invented TaskCode.

## Validation and approval

Validate final structure/source relationships, all keys and parents, labels,
parameters, dates and existing-version membership. The normalized validator
reports unknowns; obtain evidence for any applicable unknown before mutation.
For PATCH merge the current record with the patch, validate that result and
review dependency impact. Do not apply create defaults to missing patch fields.
Ensure existing target versions are DRAFT; active edits are not enabled by this
package. If concurrent changes are possible, re-read immediately before execution
and invalidate the plan on relevant change; use server preconditions only where
supported. Revalidate defaults if the date changes, but never alter approved bytes.

Persist exact body and plan, mutation hash, target origin, contract evidence,
validation results and preconditions. No fixture-date override is executable.
Check the destination is inside the selected project and does not overwrite an
existing run. Present operation, effect and exact payload to the user. Obtain
explicit approval immediately before execution (including the shared client's
single cache-auth retry). Approval for a lookup or plan is not mutation approval.
Contract blockers cannot be waived by generic execution approval.

## Declared mutation step

Invoke only the existing client from repository root after all gates:

```text
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py <approved-relative-path> --method <approved-method> --body-file <approved-project-payload> --header <approved-content-type> --header <approved-accept> --timeout 60 --output <safe-response-path>
```

Arguments are separate argv values, not interpolated shell expressions. Headers
must match the operation matrix. Use the configured environment profile for the
approved origin; do not change credentials. Hash the body and request immediately
before execution and compare against approval. A helper preview alone is never
execution authorization. No generic live runner is bundled.

For a sequenced-node plan, execute the initial `fndTrees` POST once only after
the parameter and every node-validation artifact succeeded, reconcile
the returned tree/version identities, and perform the planned
FndTreeDataSourceParamsVO child read when a DataSourceId was supplied. Record a
matching source or the non-blocking `assumed_correct` outcome. This read does
not defer or replace the required pre-create parameter tuple validation.
Materialize each
subsequent addValueTreeNode body from its resolved `treeVersionId` and
`parentTreeNodeId`, preserve the planned dependency order, and execute each call
once. Resolve and retain every returned node ID before a dependent step. A failed
or uncertain step stops the remaining sequence; never replay the initial create.

After each successful addValueTreeNode action, substitute its returned generated
TreeNodeId into exactly one selected read-back endpoint:

| TreeStructureCode | Post-create validation request |
| --- | --- |
| `PER_POS_TREE_STRUCTURE` | `GET /hcmRestApi/resources/11.13.18.05/positionTreeNodesLOV` with `{"q":"TreeNodeId={generated_tree_node_id}"}` |
| `PER_DEPT_TREE_STRUCTURE` | `GET /hcmRestApi/resources/11.13.18.05/departmentTreeNodesLOV` with `{"q":"TreeNodeId={generated_tree_node_id}"}` |
| `PER_ORG_TREE_STRUCTURE` | `GET /hcmRestApi/resources/11.13.18.05/organizationTreeNodesLOV` with `{"q":"TreeNodeId={generated_tree_node_id}"}` |
| Any other structure | `/fscmRestApi/resources/11.13.18.05/fndTreeNodes/{TreeNodeId}` |

Record the selected endpoint, query string, generated ID, returned count, HTTP
result, returned identity and verification outcome. The HCM collection query
must return exactly one record whose TreeNodeId matches the generated ID. Require
the returned node to match the intended
tree/version, parent, DataSourceId and all applicable PK values. This is
creation verification, not source-member validation. A failed read-back records
a verification diagnostic and does not retry the successful node action. Do not
fall back to fndTreeNodes for the three `PER_*` structures. Continue a dependent
action when its parent action succeeded and returned a resolved node ID; stop it
only when its parent's create action failed or is uncertain.

## Verification and persistence

Run reconcile on saved JSON response, then scoped GET read-back through the same
client. Missing inline children require child reads, not another POST. Match each
requested child by unambiguous full identity; multiple matching keys need explicit
node occurrence/parent evidence. Capture generated version/node/label IDs and
canonical links separately from source keys. Compare dates, status, keys, parents,
labels and parameter values to the request. Verify absence of unintended children
when a complete requested hierarchy was specified. HTTP success and identity
reconciliation are not field verification or audit.

Use separate creation, verification, audit, activation and flattening outcomes.
A manual audit handoff is incomplete until operator evidence is supplied. Do not
claim this skill executed that handoff. Save partial successes and errors.

Runtime locations:
- project/{project_id}/artifacts/core/trees/{run_id}/ for plans, validation,
  redacted response summaries, ID maps and diagnostics.
- project/{project_id}/state/runs/{run_id}.json, conforming to skill-run.schema.json.
- Register durable artifacts with schemas/project-artifact.schema.json and update
  applicable project validation/report state using existing project conventions.
- Append token usage to artifacts/shared/token-usage/current/token-usage-log.md:
  start time, skill ID, task/trigger, files read/written, estimated input/output/
  total tokens, estimation method and notes. Label chars/4 estimates explicitly.

If no implementation project exists, use project/_template and the repository's
draft-impl-project-<YYYY-MM-DD> convention, inform the user and offer renaming. No
project or token log is created merely for authoring this reusable package.

Never store credentials, token caches, real customer data or production-sensitive
values in project/tracked files. If an actual payload contains such values, hold
it in an approved local untracked temporary location and store only a hash,
redacted summary and safe reference in the project. Apply the same rule to raw
responses; do not place secrets in diagnostic output.

## Failure handling

| Class | Action |
| --- | --- |
| input_validation | Correct missing/invalid input before side effects. |
| catalog_or_metadata_mismatch | Stop affected operation; record conflict and required evidence. |
| auth_expired_or_invalid | Shared cache client refreshes once on rejected auth; no extra loop. |
| authorization_or_privilege | Stop when Fusion rejects the request for authorization; do not preflight by asking for privilege evidence. |
| transport_or_environment | Retry read-only known transient failure once after 2 seconds; no mutation transport retry. |
| fusion_api_error | Save redacted HTTP status, path, message, external IDs and ECID when available. |
| process_timeout | Stop after configured deadline; report operation, environment, ID, last status, elapsed and next check. |
| process_failed | Preserve successes and retrieve available status/log through declared route. |
| artifact_persistence | Stop before mutation if approval artifacts cannot be retained; safe temporary diagnostics if necessary. |
| approval_blocker | Await exact mutation/overwrite/destructive retry approval. |

Client timeout is 60 seconds. No job polling is currently implemented; separately
routed jobs must specify finite polling bounds. Unknown POST/PATCH outcome means
reconcile through scoped GET before deciding whether to retry. Never infer atomic
rollback from a compound failure. Return nonzero for partial/incomplete outcomes.
Preserve IDs for completed children. Any compensating deletion requires its own
established contract and explicit scope/approval; no automatic rollback.

Diagnostics: status, stage, failure_class, message, recommended_action, environment,
skill_id, artifact_refs, endpoint, external IDs, elapsed/last status when relevant,
and errors array for partial results. Redact secrets and sensitive source values.
