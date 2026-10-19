# Frozen create submission

Use only after cap_create_handoff has returned an exact unapproved preview and
the user later approves that load. The one approval is core.data-loader's approval;
there is no additional generic plan approval. Do not use synthetic test fixtures,
raw retrieval readiness or a prior request to manufacture executable evidence.

## Supported continuation

cap_create_submission.submit_create requires project_root, preview_path,
approved_preview_sha256 and approve_upload=True. The SHA identifies the complete
reviewed preview, including its preparation binding; it is not a signature or a
substitute for actual user consent. Keep the digest in the approval context.

The wrapper verifies the frozen CAP operation, inputs, evidence and binding;
shared preflight and ZIP hashes; canonical task; and configured target/Run Book
against the project binding. It calls public Task Hook approve_data_load_preview
and verify_approved_data_load_archive, persists the exact returned envelope,
claims an exclusive durable target-plus-ZIP attempt marker, and invokes unchanged
upload_approved_preflight once. It has no HTTP client, URL override, direct product
POST, custom multipart encoder, schema fallback or core patch.

After approval, do not reread original DAT/evidence/task context, regenerate the
ZIP, refresh live metadata/duplicate checks or rerun Task Hook rules. Those facts
are frozen in the approved preview. Current environment and Run Book integrity
remain mandatory. Changed frozen artifacts/context require fresh preparation and
approval, not repair of the approved artifact in place.

## Project-local create configuration

Create preparation automatically creates `config/cap-data-loader.properties`
inside the selected project using the shared guard's active Run Book identity.
It contains only a comment and `runID`, not authentication settings. Existing
matching content is reused; conflicting content or symlinks are rejected without
overwriting. The configured environment, saved task binding and identity evidence
must still match. No new Fusion Run Book is created by this step.

Both shared preflight (`--run-config`) and submission (`run_config_path`) receive
that explicit file. Its project-relative path and SHA-256 are frozen in the
preview alongside the project state and saved binding. Submission refuses missing
or changed configuration instead of recreating it. Unsubmitted older previews
require fresh preparation and approval; never replay completed/uncertain loads.
This change is create-only: read/list and existing update routes are unchanged.
The shared default properties file is neither read for create runID nor edited.

## Submission failures

An exclusive marker under project/state/runs/cap-create-submissions is retained
on success, rejection, error or interruption. Copying the same ZIP/preview into
another directory does not permit automatic replay. Do not remove that marker
to retry; first reconcile effects and obtain the user's specific retry decision.
The wrapper does not implement a retry route.

Shared core owns its documented explicit-rejection recovery, including its
optional Run Book parameter fallback for action error27503 with the same uploaded
ContentId. The pillar adds no automatic retry after uncertain upload/initiation.

Accepted initiation means submitted, not CAP-created/processed. If saving the
receipt fails, preserve/report the known returned result and retain recovery
artifacts. Do not misreport no effects. Shared initiation Markdown is returned
unchanged; local persistence warnings precede it separately. No automatic status
polling. For the separately requested status/readback stage, use existing shared
monitoring and CAP exact read routes. ORA_NEEDS_PROCESSING is pending; null is
unverified. Contributor-state inspection remains limited by its supported route.

After accepted initiation and verified receipt, only the internal shared
preflight and approved Task Hook envelopes are retired. The approved ZIP, CAP
preview, durable attempt marker and sanitized receipt remain for reconciliation.
