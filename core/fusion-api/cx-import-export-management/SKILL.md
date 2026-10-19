---
skill_id: "core.fusion-api.cx-import-export-management"
name: "CX Import Export Management"
description: "Creates, activates, checks, uploads files for, and downloads output from Oracle CX Sales and Fusion Service Import Management file import activities and Export Management bulk export activities. Use when a user provides CX data, a local CSV, a UCM content ID, an import object or mapping, an export object, export filters, or asks to upload to UCM, initiate, submit, monitor, poll, or download CX Import Management or Export Management jobs."
layer: "core"
pillar: "Core"
type: "import"
execution_mode: "hybrid"
owner_team: "Central platform team"
version: "0.1.0"
inputs:
  - "fusion_environment_context"
  - "cx_import_payload"
  - "cx_export_payload"
  - "local_import_file_or_ucm_content_id"
  - "execution_options"
  - "approved_import_id"
outputs:
  - "import_activity_summary"
  - "export_activity_summary"
  - "ucm_upload_summary"
  - "export_download_path"
  - "diagnostics"
  - "audit_summary"
  - "protected_import_preview"
depends_on:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.fusion-api.ucm-rest-client"
uses_core:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.fusion-api.ucm-rest-client"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Connects to Oracle CX REST APIs when invoked."
  - "Stores owner-private import approval records outside the repository under ~/.fusionaim/cx-import-approvals/."
  - "Uploads local import files to UCM through ERP Integration Service only after explicit execution approval."
  - "Creates or activates CX Import Management import jobs only after explicit execution approval."
  - "Creates or activates CX Export Management bulk export jobs only after explicit execution approval."
  - "Downloads export output files to the local workspace when requested."
required_privileges:
  - "Fusion CX privileges to create and monitor Import Management or Export Management jobs for the target object"
---

# CX Import Export Management

Use this core skill to submit Oracle CX Sales and Fusion Service Import
Management import activities and Export Management bulk export activities.

## Required Reference

Before changing payload behavior or troubleshooting field names, read:

- `references/oracle-cx-import-export-management.md`

## Key Boundary

Import Management accepts UCM document names, not CSV rows. Local CSV imports
must use `prepare-import` → `approve-import` → `execute-approved-import`.
Bare `create-import --execute` and `upload-ucm --execute` are disabled before
configuration or token access, including imports based only on a supplied UCM
content ID. The legacy commands remain available for payload previews.

## Approved Import Workflow

1. Complete the governing Data Loader/Task Hook source review, object-support,
   privilege, and task validation gates. Resolve the exact object's UCM account;
   never guess an account or substitute another object.
2. Run `prepare-import` with the exact local data CSVs and execution settings.
   It reads sources without transforming their contents, validates the fixed
   `core/auth/fusionEnv.properties` profile against the OAuth trust policy, and
   confirms `UcmAccount` through the exact object's live metadata. It makes no
   Fusion mutation. Repeat `--upload-file` for multiple data CSVs in upload order;
   mapping CSVs and existing-content-ID imports are not supported by this path.
3. Present the returned manifest, `approvalId`, and `reviewSha256` with the
   governing preview. The manifest binds ordered basenames and byte digests,
   canonical CSV-group SHA-256, normalized target/environment and OAuth profile,
   object, ImportMode, UCM account/transport, activity name, activation, and schedule.
   Obtain explicit approval for these exact values before issuing `approve-import`.
   An existing explicit approval of this same manifest satisfies this gate;
   do not ask twice for the same execution.
4. Call `approve-import --approval-id <id> --review-sha256 <reviewed-digest>`.
   This records the approving OS UID and a 15-minute expiry (maximum one hour).
   It cannot update or renew an existing approval. No Fusion call occurs.
5. Call `execute-approved-import --approval-id <id>` with the identical source
   list and settings. The adapter checks the protected record before token
   acquisition, reads each source once, compares every approved field, and
   atomically consumes the approval before authenticated traffic. It rereads
   only the fixed profile and exact object account metadata to confirm the
   target, failing on drift. It uploads the already verified in-memory bytes.
6. Persist the redacted receipt and any partial-success identifiers under the
   active project's artifacts. A failed/uncertain attempt spends the approval;
   reconcile the returned UCM and import IDs before requesting a new approval.
   Mutating requests are never automatically retried. Use `get-import` for
   subsequent status checks; submission is not proof of completed import.

The approval authority is the current OS account's fixed private store at
`~/.fusionaim/cx-import-approvals/` (directory 0700, records 0600, no symlink
traversal). Workspace JSON previews are review copies, never authorization
sources. Approval IDs are random and cannot select arbitrary files; a separate
atomic consumption record blocks replay and concurrent execution. No signing
key, tokens, or source content is stored in approval records. This boundary
protects against edited project artifacts; it does not protect against a
compromised approving OS account or modified trusted FSCR code.

## Commands

Prepare the exact import for review (read-only Fusion metadata lookup):

```bash
python3 core/fusion-api/cx-import-export-management/scripts/cx_import_export_job.py prepare-import \
  --name "Account import" \
  --object-code Account \
  --import-mode CREATE_RECORD \
  --upload-file accounts.csv \
  --ucm-document-account 'crm$/import$' \
  --activate YES \
  --schedule ONE_TIME_IMMEDIATE
```

After explicit approval of the returned manifest:

```bash
python3 core/fusion-api/cx-import-export-management/scripts/cx_import_export_job.py approve-import \
  --approval-id <id> --review-sha256 <reviewed-digest>

python3 core/fusion-api/cx-import-export-management/scripts/cx_import_export_job.py execute-approved-import \
  --approval-id <id> \
  --name "Account import" \
  --object-code Account \
  --import-mode CREATE_RECORD \
  --upload-file accounts.csv \
  --ucm-document-account 'crm$/import$' \
  --activate YES \
  --schedule ONE_TIME_IMMEDIATE
```

Export and import-mapping creation retain their explicit `--execute` gate and
require preview and user approval. Export status, bounded polling, and download
commands retain their existing behavior.

Create an import mapping with columns in one REST call:

```bash
python3 core/fusion-api/cx-import-export-management/scripts/cx_import_export_job.py create-import-mapping \
  --name "Account import map" \
  --object-code Account \
  --column "OrganizationName=OrganizationName:Codex Account" \
  --column "Country=Country:GB" \
  --execute \
  --token-cache auto
```

Create and activate a bulk export activity:

```bash
python3 core/fusion-api/cx-import-export-management/scripts/cx_import_export_job.py create-export \
  --name "Account export" \
  --export-object Account \
  --export-column-names "PartyNumber,OrganizationName" \
  --export-filter-criteria "PartyNumber IS NOT NULL" \
  --activate YES \
  --wait-seconds 600 \
  --execute \
  --token-cache auto
```

Create, activate, poll, and download an export in one command:

```bash
python3 core/fusion-api/cx-import-export-management/scripts/cx_import_export_job.py create-export \
  --name "Account export" \
  --export-object Account \
  --activate YES \
  --execute \
  --wait-seconds 600 \
  --poll-interval 30 \
  --download-output project/{project_id}/exports/cx/account-export.zip \
  --token-cache auto
```

Download the completed export output:

```bash
python3 core/fusion-api/cx-import-export-management/scripts/cx_import_export_job.py download-export \
  --bulk-export-job-id 300000000000002 \
  --download-output project/{project_id}/exports/cx/account-export.zip \
  --token-cache auto
```

Use a full Oracle payload file when the request needs fields not exposed as
first-class CLI flags:

```bash
python3 core/fusion-api/cx-import-export-management/scripts/cx_import_export_job.py create-export \
  --payload-file export-payload.json \
  --execute \
  --token-cache auto
```

Check status:

```bash
python3 core/fusion-api/cx-import-export-management/scripts/cx_import_export_job.py get-import \
  --import-activity-id 300000000000001 \
  --token-cache auto
```

```bash
python3 core/fusion-api/cx-import-export-management/scripts/cx_import_export_job.py get-export \
  --bulk-export-job-id 300000000000002 \
  --token-cache auto
```

## Safety Rules

1. Never print access tokens, refresh tokens, client secrets, or token-cache
   contents.
2. Use `execute-approved-import` for import/UCM writes; `--execute` gates only
   export and import-mapping creation.
3. Do not infer `ObjectCode`, `ImportMapping`, or `ExportObject` when several CX
   objects could match the user's request; ask for the exact object code.
4. For import jobs, do not submit without either `ObjectCode` or `ImportMapping`.
5. For import jobs, stage only the bytes verified against the protected approval;
   existing `InputFileContentId` values alone cannot establish byte integrity.
6. Do not print base64 file payloads or SOAP envelopes because they contain the
   uploaded file content.
7. Bind import credentials and requests to the selected standard Fusion
   `restBaseUrl` origin; reject redirects to other configured service origins.

## Final Response

Report the target operation, endpoint, job name, UCM content ID when uploaded,
returned job identifier, whether the job was activated, export download path
when downloaded, and the last polled status if polling was requested.
