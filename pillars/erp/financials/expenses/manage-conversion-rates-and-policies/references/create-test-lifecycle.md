# Create-test lifecycle policy

Automated create campaigns use `approved-retained-state`. This is an explicit
disposition of test records, not deletion or restoration. FSM deletion remains
unsupported; do not synthesize a delete, empty import or end-date operation.
Update-only tests continue using separately approved reverse-update cleanup.
Split mixed create/update runs so each phase has an exact lifecycle contract.

## Before creating records

1. Select an explicit nonproduction environment and active Run Book. Use
   dedicated test scope and collision-safe exact keys supplied/confirmed for
   this campaign. Prove every create key absent in a fresh complete baseline.
   Do not use this policy to overwrite or retain pre-existing customer setup.
2. Prepare and independently validate the immutable create-only candidate and
   its confirmed blueprint using the task's normal rules. Bind task, target,
   run, exact parent/child keys, baseline, design and candidate SHA-256 values.
3. Present the exact records, business effect, environment, accountable owner
   and retention deadline. Explain that the records will remain after the test,
   even after a failed/partial import where some rows persist; no automatic
   removal route is available. Require explicit human consent to that concrete
   retained state. A generic test request, policy edit, design confirmation or
   import approval alone is not retention consent.
4. Record that actual consent in protected local evidence, then use the E2E
   state helper at `IMPORT_APPROVAL`:

   ```text
   python <tester-skill-root>/scripts/fsm_e2e_state.py approve-retention --run-file <run.json> --owner <accountable-owner> --retain-until <timezone-aware-deadline> --consent-file <actual-human-consent.txt> --acknowledge-retention
   ```

   The deadline must be future and within 30 days. The helper verifies baseline
   absence and binds the consent to exact validated candidate bytes and keys.
   It does not grant import approval. Do not fabricate human consent or reuse
   another run's consent. Withheld consent stops before import.
5. Continue the existing candidate-specific E2E and core Data Loader approval
   workflow. The E2E helper checks retention before import approval, entering
   the import stage and staging an upload. Changed target, keys, baseline,
   blueprint, candidate, consent evidence or an expired deadline invalidates
   the retained-state authorization. Never rebuild an approved artifact.

## Completion and failure

After accepted initiation, return core's report. Use the campaign's separately
selected status/export/reconciliation steps with the original request identity.
Require successful import, fresh exact-task verification export, every created
key/value and preservation assertion, and zero reconciliation mismatches.

Record a passed create scenario through the normal campaign `record-result`
command with its VERIFIED forward `--run-file`. Do not pass `--cleanup-run-file`
for this strategy and do not invent a cleanup mutation or a post-delete export.
The runner validates the pre-import retention consent, exact bindings and fresh
reconciliation, then records `retained_as_approved` with owner, deadline and exact
retained keys. Reports must say retained, never deleted, restored or cleaned.

On a failed, partial or uncertain import, stop and reconcile the original
attempt before any retry. Preserve exact known-created and uncertain identities
for the accountable owner; missing reconciliation cannot pass the scenario.
Consent covers retaining only the enumerated run-owned keys. Unrelated changes,
duplicate rows or unexpected records remain failures, never accepted retention.

The named owner remains responsible for isolation and disposition by the
deadline, including after test failure. At expiry, require owner action through
a separately supported, approved removal or environment-reset workflow. Do not
automatically delete, silently extend consent, create a replacement fixture or
claim restoration. A missing supported disposal route must be disclosed before
consent; if the owner cannot accept responsibility, do not run a create test.
This policy creates no background automation and grants no production access.

## Runner compatibility

Require a tester exposing `approve-retention` and explicit
`approved-retained-state` campaign recording. Older runners must stop and be
updated; do not use an unsupported strategy string merely to pass plan checks.
The descriptor/catalog declare policy readiness, not consent for any target.
Plan a new campaign after descriptor, runtime or catalog hashes change.
