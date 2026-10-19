# Library Goal create body handoff

For a REST create, use the task's `scripts/library_goal_payload.py` after the
existing route, execution-control, tenant-metadata, and duplicate checks pass.
This is a local payload check, not a new execution route or approval mechanism.

1. Prepare with `--metadata <current-metadata.json> --payload <source.json>
   --environment <selected-environment> --request-path <resolved-collection-path>
   --preview-output <new-preview.json> --prepared-output <new-prepared.json>`.
   Preserve the original source. Present the generated preview, including the
   materialized `TypeCode`, `StatusCode`, and `Visible`, for explicit approval.
2. Retain the approved preview's `sha256` in the existing approval record.
   The workflow supplies this digest internally; do not ask the user to copy it.
   A digest alone is not evidence of user approval.
3. Immediately before the declared core REST execution step, run the same
   helper with `--metadata <current-metadata.json> --payload <new-prepared.json>
   --environment <selected-environment> --request-path <resolved-collection-path>
   --approved-preview <new-preview.json> --approved-fingerprint <approved-digest>
   --submission-output <new-submission.json>`.
   Preserve any validated duplicate-risk/active-create flags from the preview.
   This mode validates the body as-is: it must not add missing fields or silently
   repair an approved payload. Failure blocks POST and requires correction and,
   for changed bound values, fresh preview/approval.
4. Pass **only** the returned `body_file` to the existing core REST client's
   `--body-file`, with the same resolved environment and POST collection path.
   Never use the original input file, reconstruct JSON, or edit the output
   between validation and transport. If anything changes, repeat the check.
   This pillar guard does not modify or intercept the shared REST client.
5. Keep the existing post-create fresh-read verification. No automatic retry or
   replacement create is authorized by this handoff.

Use new versioned artifact paths under the task's existing project workspace;
outputs refuse overwrite. On an artifact-write error, do not submit any partial
output. Correct the destination and regenerate a complete pair of artifacts.
