# Test-only composite Item Catalog FSM batch

Use this route only for an explicit controlled-certification request whose exact
Fusion environment is confirmed as non-production. It reduces repeated prompts;
it does not weaken proposal, package, duplicate, Task Hook, target, or readback
gates.

The exact environment alias must contain an affirmative non-production marker:
`BRONZE`, `DEV`, `DEVELOPMENT`, `QA`, `SANDBOX`, `STAGE`, `STAGING`, `TEST`,
`TESTING`, or `UAT`. The runner rejects aliases containing `LIVE`, `PRD`,
`PROD`, or `PRODUCTION`, and fails closed for unknown aliases even when the
manifest labels them `test`.

## Ownership boundary

The pillar-local runner
`../../scripts/run_item_catalog_fsm_test_batch.py` owns only ordered orchestration,
test-target enforcement, fingerprint checks, fail-fast state, and project-local
receipts. It must not implement OAuth, UCM upload, Data Loader initiation, status
REST, task export, or application readback.

For every load, it invokes these existing routes unchanged:

1. `core/data-loader/scripts/upload_and_initiate.py` for the exact approved FSM
   ZIP and Task Validation envelope;
2. `core/data-loader/scripts/get_data_load_info.py --status-only` as a separate
   monitoring operation explicitly requested by the user in the composite batch
   authorization;
3. the Item Catalog skill for direct child readback, parent no-drift comparison,
   and duplicate-rerun blocking;
4. `shared.setup-export.task-level-export` for the fresh full Item Catalog export.

The Core Data Loader implementation and its default immediate-return behavior
remain unchanged.

## Two user checkpoints

1. Present one review proposal containing all child identities and exact parent
   catalogs. Obtain one response that confirms all values and resolves every
   catalog ambiguity. This is not package or execution authorization.
2. In a later message, present the exact target, release, ordered provider rows,
   authorization fingerprint, automatic monitoring/readback scope, and fail-fast
   policy. The user's response must explicitly request package preparation and
   include unambiguous `auto-approve` wording for only the listed test loads. It
   must also explicitly request terminal status and Item Catalog verification.

Checkpoint 2 is the separate package-preparation request required by the parent
FSM contract and the same-prompt Core Data Loader auto-approval for the identified
loads. It is not reusable session authorization. No per-package, per-status, or
per-readback confirmation is requested after it.

## Authorization manifest

Create a project-local fingerprint-input draft with
`manifest_stage: authorization`. It contains every field required by
`../../schemas/item-catalog-fsm-test-batch.schema.json` except the computed
`authorization_fingerprint`:

- exact test environment, task, and create-only FSM route;
- exact SHA-256 of the source-backed Item Catalog FSM provider registry;
- ordered unique context/load IDs;
- proposal and provider-row fingerprints;
- exactly one expected loaded row and zero failed rows per canary;
- `auto_approve`, terminal monitoring, domain verification, and fail-fast set to
  true;
- mutation retry, auto-correction, and provider promotion set to false;
- bounded polling, state, and diagnostic paths inside the project workspace.

Calculate the authorization fingerprint locally:

```text
python3.11 pillars/hcm/hcm-tool/profile-management-content-library-configuration/scripts/run_item_catalog_fsm_test_batch.py \
  --project-root project/<project_id> \
  --manifest <project-relative-authorization-manifest.json> \
  --expected-test-environment <exact-test-alias> \
  --print-authorization-fingerprint
```

Add the returned value as `authorization_fingerprint`; the resulting
authorization manifest must conform to the schema. Present that fingerprint at
checkpoint 2. Any change to the target,
release, provider registry, context order, proposal/provider rows, expected counts, safety policy,
polling, or state/diagnostic locations invalidates it.

## Execution manifest and dry run

After checkpoint 2, build one deterministic one-child package per context and
one approved Task Validation envelope per ZIP. Extend the same manifest with:

- `manifest_stage: execution`;
- project-relative ZIP and Task Validation envelope paths;
- exact SHA-256 values for both artifacts;
- an execution fingerprint over the authorization material and derived artifacts.

The authorization fingerprint deliberately excludes derived ZIP/envelope paths
and hashes; the execution fingerprint includes them. The runner still requires
the Task Validation preview to bind the exact package bytes, proposal fingerprint,
provider-row fingerprint, create operation, and FSM source type, so derived
artifacts cannot drift from the earlier business authorization.

Remove the old `execution_fingerprint`, if present, and calculate the derived
value from the otherwise complete execution manifest without performing an
external call:

```text
python3.11 pillars/hcm/hcm-tool/profile-management-content-library-configuration/scripts/run_item_catalog_fsm_test_batch.py \
  --project-root project/<project_id> \
  --manifest <project-relative-execution-manifest.json> \
  --expected-test-environment <exact-test-alias> \
  --print-execution-fingerprint
```

Write that result into the execution manifest. The manifest must now conform to
the schema; then run dry-run validation.

Run the no-side-effect validation before execution:

```text
python3.11 pillars/hcm/hcm-tool/profile-management-content-library-configuration/scripts/run_item_catalog_fsm_test_batch.py \
  --project-root project/<project_id> \
  --manifest <project-relative-execution-manifest.json> \
  --expected-test-environment <exact-test-alias> \
  --dry-run
```

Dry run must not authenticate, call Fusion, write state, upload, initiate,
monitor, verify, or promote a provider.

## Execution and resume

Only while acting on checkpoint 2 may the workflow pass the exact authorization
fingerprint to `--execute`. Require an explicit Fusion properties path and verify
that its `environment` equals both the manifest target and
`--expected-test-environment` before calling Core Data Loader.

The runner passes `auto` to shared Core authentication for both submission and
status commands, resolving to `~/.fusionaim/<profile-fingerprint>_token.json`.
`--token-cache` may select an external private file; checkout paths are rejected.
Shared authentication rejects symlinks, non-regular files, non-owner files and
unsafe file/directory permissions before using the cache. The pillar passes only
the path or sentinel to Core and never reads or persists cache contents. The
cache path is not batch authorization material and must not appear in a manifest
or project workspace.

The runner persists state before starting each upload. States
`submitting`, `submission_unknown`, `blocked`, `failed`, and `timed_out` never
resubmit. A status resume uses the existing request ID. A completed or blocked
batch is terminal and cannot start another load.

For FSM loads, Fusion `ObjectTotalCount` and `ObjectLoadedCount` report task
business objects rather than the one requested child row. After every reported
object has loaded, at least one object is present, and zero objects have failed,
the runner enters `awaiting_verification`. The manifest's `1/1/0`
`expected_counts` remains the business-change contract and is enforced by the
one-child package plus exact domain verification. The active Item Catalog
workflow performs its declared read-only checks and creates a receipt conforming to
`../../schemas/item-catalog-fsm-test-verification.schema.json`. Supplying that
project-relative receipt to the next `--execute` call is orchestration input, not
a new user approval. A verified receipt advances to the next canary; a blocked
receipt ends the batch.

The runner stores Core CLI Markdown and sanitized state only under the project
paths named in the manifest. Never persist tokens, authorization headers,
property values, endpoints, full existing rows, base64 payloads, or customer data.

## Stop behavior

Stop without asking to waive, correct, retry, skip, or roll back when:

- the target is production-like, unclassified, different from the configured
  environment, or changed from the authorization;
- a proposal/provider fingerprint, source SHA, Task Validation envelope, or
  execution fingerprint differs;
- a ZIP is not FSM or lacks exactly one metadata member;
- a load fails, reports zero objects, has any object failure, has incomplete
  object totals, status times out, or initiation has an unknown outcome;
- domain readback, parent no-drift, full export, or duplicate-rerun proof blocks.

Only the Core authentication service's one permitted cached-token refresh may
retry automatically. Never retry upload, initiation, import, export submission,
or another mutation.

## Lifecycle after the test

The exact batch authorization expires in terminal project state. It is not
rolled into another run and does not authorize provider promotion. Keep this
guarded capability in the pillar for future controlled test batches; remove only
the project-local batch artifacts according to normal project retention policy.

Passing verification may generate a review-only lifecycle promotion proposal.
Changing a provider from `certification-only` to `verified`, committing, pushing,
merging, or switching general-use routing remains a separate reviewed source
change.
