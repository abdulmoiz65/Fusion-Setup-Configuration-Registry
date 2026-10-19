# Local VX Build and Deployment

## Build contract

Build only after Extension validation succeeds. The selected Extension
workspace must already contain its pinned Oracle Visual Builder tooling under
`node_modules`. This workflow never installs packages.

Use:

```bash
node scripts/build_vx.js \
  --repo <extension-workspace> \
  --version '$vb_snapshot_<timestamp>' \
  --expected-head <reviewed-commit> \
  --require-clean \
  --json
```

The builder supports both `extension1/sources/extension.json` and
`extension1/sources/vb-extension.json`. It validates generated output paths,
rejects symlinks, runs the target repository's pinned `vb-process-local` and
`vb-package` tasks, and confirms the source commit did not change during the
build.

## Deployment preflight

Before upload, present and approve:

- environment name and Fusion host from `core/auth/fusionEnv.properties`;
- `POST /fscmRestApi/vx/v2/extensions`;
- archive path, extension ID, snapshot version, size, and SHA-256;
- approved Extension page artifacts or complete Redwood routes.

Use:

```bash
node scripts/deploy_express_mode.js \
  --repo <extension-workspace> \
  --vx <validated-archive.vx> \
  --target-route '<complete-redwood-url>' \
  --token-cache <local-gitignored-token-cache.json> \
  --project-root project/{project_id}/artifacts/shared/extensibility/vblens-express-mode/current/reports \
  --confirm-deploy \
  --json
```

The shared script reads environment identity from the standard properties file
and delegates the raw archive stream to `scripts/upload_vx.js`. The uploader
accepts only the fixed Fusion VX endpoint and an unexpired local OAuth file
cache created by `core/auth/fusion-oauth-authentication`. It sends exactly one
request and never retries or polls. Rebuild a missing or expired cache through
the core OAuth login workflow before requesting deployment approval.

All normal JSON REST calls, including JSON POST calls, use
`scripts/fscr_rest_client.js`, which invokes the existing central
`fusion_rest_client.py` command.

## Snapshot URL contract

Generate URLs only after Fusion accepts the upload and either the response or
archive supplies a valid `$vb_` selector. Preserve every approved route query
pair and fragment. Add or replace only `vbdt:preferExtensionVersion`. Every
derived route uses the `fscmUI` Redwood shell. Do not open the URL.
