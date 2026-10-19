# Alert Foundation batch-create (0.11.0)

## Scope and user prompt

> Create Event Alerts from "<intake.xlsx>" in batch-create mode. Prepare one work unit containing all included Alert hierarchies and seek one approval before submission.

Unqualified prompts continue to select sequential mode. Batch is a transport
choice, independent of [simple/default or deep validation](validation-modes.md).
Simple CREATE skips live preflight; deep requires declared checks. Do not submit a test call to establish
compatibility. No core, authentication or catalog changes are needed for this
route; the HCM Tool adapter reuses the shared authentication and REST transport.

## One workbook, one work unit, one approval, one POST

1. Execute the compiled Alerts task plan built with `--setup-task Alerts` and
   its reached source rules. Use the
   current project's configured Fusion origin. For offline payload preparation:

   ```text
   python pillars/hcm/hcm-tool/alert-foundation/scripts/read-alert-intake.py "<intake.xlsx>" --execution-mode batch-create --target-environment https://<fusion-host> --project-id <active-project-id> --attempt-id <new-attempt-uuid> --output <preview.json>
   ```

2. Stop on any intake error. All included Alerts, Templates and Recipients must
   be CREATE with valid parent relationships. Retain existing code requirements;
   optional server-generated Template/Recipient codes are not an intake feature
   in this release. Reject duplicate codes within the same parent, unsupported
   entities, file-based Body plans and mixed-intent workbooks. Empty or absent
   inline Body is omitted. Nonblank Body is literal workbook text, converted to
   UTF-8 and Base64 exactly once, even if it already looks like Base64. Do not
   interpret HTML or validate expressions inside Body.

3. `preview.work_units` contains exactly **one** aggregate wrapper. Its
   `approval_document.request.payload.parts` contains one entry per included
   Alert, with nested `templates` and `recipients`. Preserve selected workbook
   order; never split, chunk or silently fall back to sequential execution.
   The whole request uses:

   | Property | Exact value |
   |---|---|
   | Method | POST |
   | Endpoint | Approved Fusion origin + `/hcmRestApi/resources/latest` |
   | Content-Type | `application/vnd.oracle.adf.batch+json` |
   | REST-Framework-Version | `4` |
   | Part path / operation | `/eventAlerts` / `create` |

   These are JSON batch parts, not MIME multipart uploads. Each part has a stable
   `createAlertN` id. The sequential adapter continues to reject this root path
   and uses version 9. Batch cannot accept arbitrary root endpoints, custom
   headers, actions, update/delete parts, or Upsert-Mode.

4. In simple mode, complete local input/hierarchy/payload checks and bind the
   configured environment and authorization assumption. Record the live lookup
   branch as skipped_simple; do not call Fusion or require live gate evidence.
   In deep mode, complete the identity, authorization-assumption, compatible metadata,
   lookup, language and duplicate gates through the declared provider read route.
   For batch compatibility, use the selected batch version 4 against the declared
   eventAlerts describe resource; require the needed nested fields/children and
   retain reviewed batch-route evidence. Stop on an unsupported target contract.
   Prepare local gate evidence from the **actual** reached checks, never from
   workbook READY cells or placeholder assertions. Evidence JSON contains:

   ```json
   {
     "validation_mode": "deep",
     "work_unit_sha256": "<aggregate SHA256>",
     "target_environment": "https://<fusion-host>",
     "status": "ready_for_approval",
     "gates": {
       "ALERT.VALIDATE": {"status": "passed", "artifact": "<absolute evidence file>", "sha256": "<uppercase file SHA256>"},
       "ALERT.LOOKUP": {"status": "passed", "artifact": "<absolute evidence file>", "sha256": "<uppercase file SHA256>"},
       "ALERT.DEPENDENCY": {"status": "passed", "artifact": "<absolute evidence file>", "sha256": "<uppercase file SHA256>"},
       "ALERT.DESIGN": {"status": "passed", "artifact": "<absolute evidence file>", "sha256": "<uppercase file SHA256>"}
     }
   }
   ```

   The adapter checks bindings, statuses and artifact hashes, not the truth of
   an arbitrary caller's assertions. The assisted provider workflow owns actual
   gate execution and evidence review. Never manufacture passed records to unlock
   the adapter. Re-evaluate stale evidence; a hash is not proof of live freshness.

5. Before requesting final approval, complete Fusion login and prove authentication readiness. A
   noninteractive batch may use only an unexpired cached token: do not open a
   browser, refresh, or begin a POST. If this fails, stop as `not_submitted`.
   Generate a new UUID attempt id and recovery context for every initial or
   recovery plan. Present one concise summary (target, source digest, attempt id,
   recovery context, part/Alert/Template/Recipient
   counts, Body encoding, exact headers, no retries, verification limits), with
   the complete immutable document available for review. Request exactly one
   approval: `Confirm Alert Batch <aggregate SHA256>`. The digest binds execution mode,
   validation mode and policy,
   source workbook, target, method, URI, headers, ordered parts and nested payloads,
   payload digest and execution/verification policy. Existing sequential approval
   phrases cannot authorize this route. Attempt id and recovery context are in
   the digest, so an earlier phrase cannot authorize a recovery POST. Any change requires a fresh preview and
   approval. Do not ask for additional approval per part or child.

6. After approval, persist the unchanged sole wrapper as `<batch-work-unit.json>`.
   Invoke the existing adapter once:

   ```text
   python pillars/hcm/hcm-tool/alert-foundation/scripts/execute-alert-mutation.py <batch-work-unit.json> --execution-mode batch-create --cached-token-only --receipt-output project/<active-project-id>/state/runs/alert-receipts/<new-attempt-uuid>.json --source-workbook "<intake.xlsx>" --approval-phrase "Confirm Alert Batch <aggregate SHA256>"
   ```

   This is the simple-mode invocation. For a deep preview, pass
   `--validation-mode deep` to the reader in step 1 and add
   `--gate-evidence <gates.json>` to the execution invocation above.
   Standard adapter authentication options remain available. It validates the
   approval, source hash, deep-only gate references and configured origin before one
   cached-token readiness check and one shared `request_bytes` POST. The adapter
   atomically reserves the new receipt after approval validation, then fsyncs
   `approval_validated` before authentication, `authentication_ready` after the
   cached token, `request_started` before POST, and `response_received` after
   any HTTP response. A pre-existing, mismatched, changed, or completed receipt
   blocks authentication and dispatch. `--receipt-output` must exactly match
   the safe project-owned `execution_receipt_reference` embedded in the approved
   work unit; it resolves from the repository root, never the process directory.
   An alternate, absolute, or traversal path is refused. There is no
   automatic POST retry, including after 401/403, timeout or uncertain outcome.
   Never use the generic retrying REST CLI as a substitute for this adapter.

7. Inspect every returned part by id, not array position. Reject missing,
   duplicate or unexpected ids; part errors; wrong codes, fields, counts or
   canonical origins/paths. Require internal IDs and compare nested children by
   their codes. HTTP 200 alone is not success. Sanitized results retain reported
   identities but do not persist raw response text, encoded Body or credentials.
   On any error, stop further writes and reconcile **all** submitted parts through
   the declared read route before proposing recovery. A pre-dispatch failure is
   `not_submitted`; after `request_started` with no response it is
   `outcome_unknown`. The atomic sanitized receipt records `approval_validated`,
   `authentication_ready`, `request_started`, and `response_received` and
   refuses overwrite. Never replay the batch or
   issue compensating DELETEs automatically.

8. A matching response returns `submitted_pending_verification`, not completed.
   Perform the existing independent canonical GET comparisons for every returned
   Alert, Template and Recipient through the declared core read route. Body is
   excluded from field comparison and stored-content verification stays deferred.
   Record completed only after required reads pass, with that Body limitation.
   Persist the durable Alert skill-run record only through:

   ```text
   python -B pillars/hcm/hcm-tool/alert-foundation/scripts/skill_run_persistence.py --input-stdin --output <new-run-record.json>
   ```

   The record must contain the schema-permitted `token_usage` object. Its
   estimates and log reference must match the project token-usage log. The helper validates it against
   `schemas/skill-run.schema.json`, writes it atomically, and refuses to replace
   an existing run record. The record must use only schema-permitted fields and
   must not contain `$schema`, an empty key, or `external_ids`.
   Adapter exit 0 means submission/response checks passed; it does not mean final
   business verification completed. Exit 2 is local validation failure; exit 3
   is auth, submission or response-verification failure. Retain partial evidence
   and a newly approved recovery plan if necessary.

## Evidence and limitations

The implementation follows the user's September 10 standalone curl evidence:
single and two-part creation, explicit Template/Recipient codes, version 4 and
the latest root endpoint. The single-part UI displayed decoded message text.
These tests do not establish rollback, atomicity, maximum part count, server
stop-on-first-error or independent stored Body verification. Once one POST is
submitted, the client cannot stop subsequent server parts. Do not promise those
behaviors or silently chunk a large workbook; obtain a new reviewed work unit
if the target imposes a batch-size limit.

Persist previews, sanitized results, gate evidence, diagnostics, run record and
token-usage entry under the current project according to its existing policies.
Use synthetic fixtures in Git; exclude generated outputs and environment data.
