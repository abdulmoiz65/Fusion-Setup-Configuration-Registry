---
skill_id: "core.fusion-api.ucm-rest-client"
name: "UCM REST Client"
description: "Calls Oracle Fusion UCM HTTP IdcService APIs using OAuth, including ping, search, metadata lookup, file check-in, and file download. Use when a workflow needs a UCM dDocName such as UCMFA00000000, needs to stage a local file without ERP SOAP uploadFileToUcm, or needs to inspect/download UCM content used by Import Management or Export Management."
layer: "core"
pillar: "Core"
type: "import"
execution_mode: "hybrid"
owner_team: "Central platform team"
version: "0.1.0"
inputs:
  - "fusion_environment_context"
  - "ucm_document_metadata"
  - "local_file"
  - "execution_options"
outputs:
  - "ucm_document_summary"
  - "ucm_document_name"
  - "download_path"
  - "diagnostics"
depends_on:
  - "core.auth.fusion-oauth-authentication"
uses_core:
  - "core.auth.fusion-oauth-authentication"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Connects to Oracle UCM HTTP IdcService endpoints when invoked."
  - "Uploads local files to UCM only when --execute is used."
  - "Downloads UCM document content to the local workspace when requested."
required_privileges:
  - "Fusion privileges to access UCM content in the target security group and document account"
---

# UCM REST Client

Use this core skill when a workflow needs to interact with Fusion UCM directly
through the HTTP IdcService endpoint instead of the ERP Integration Service SOAP
wrapper.

## Required Reference

Before changing service names, metadata fields, or CX Import hand-off behavior,
read:

- `references/oracle-ucm-http-idcservice.md`

## Boundary

This is not the CX Import Management API. It only stages, locates, inspects, and
downloads UCM documents. CX Import Management still consumes the resulting UCM
document name through `DataFiles[].InputFileContentId`.

For CX imports, the important returned value is usually `dDocName`, for example
`UCMFA06213998`. A numeric `dID`/document id is useful for UCM metadata lookup
but is not the same value as the CX import `InputFileContentId`.

Some Fusion environments do not accept OAuth bearer tokens directly on
`/cs/idcplg` and return the WebCenter Content sign-in page instead. In that
case, use `--auth-mode basic --prompt-password` with the Fusion username from
`fusionEnv.properties` or `--username`. If Basic auth also returns the sign-in
page, the pod is enforcing an interactive SSO cookie for `/cs/idcplg`; use the
ERP Integration Service SOAP path or another Oracle-supported server-side
content upload API for automation.

## Commands

Ping the UCM endpoint:

```bash
python3 core/fusion-api/ucm-rest-client/scripts/ucm_rest_client.py ping \
  --summary \
  --token-cache auto
```

Ping with Basic authentication when `/cs/idcplg` does not accept OAuth bearer
tokens:

```bash
python3 core/fusion-api/ucm-rest-client/scripts/ucm_rest_client.py ping \
  --auth-mode basic \
  --prompt-password \
  --summary
```

Upload a CSV to an Import Management document account:

```bash
python3 core/fusion-api/ucm-rest-client/scripts/ucm_rest_client.py upload \
  --file project/cx-test/accounts.csv \
  --auth-mode basic \
  --prompt-password \
  --document-account "crm/simplifiedAccount/import/" \
  --security-group FAFusionImportExport \
  --title accounts.csv \
  --execute \
  --summary \
  --token-cache auto
```

Fetch metadata for the uploaded UCM document:

```bash
python3 core/fusion-api/ucm-rest-client/scripts/ucm_rest_client.py info \
  --ddoc-name UCMFA00000001 \
  --summary \
  --token-cache auto
```

Search for recently staged documents:

```bash
python3 core/fusion-api/ucm-rest-client/scripts/ucm_rest_client.py search \
  --query-text "dSecurityGroup <matches> `FAFusionImportExport`" \
  --result-count 10 \
  --summary \
  --token-cache auto
```

Download the primary file:

```bash
python3 core/fusion-api/ucm-rest-client/scripts/ucm_rest_client.py download \
  --ddoc-name UCMFA00000001 \
  --output project/cx-test/downloaded/accounts.csv \
  --token-cache auto
```

Authenticated requests are restricted to HTTPS hosts configured by
`restBaseUrl` or `*_restBaseUrl` in `core/auth/fusionEnv.properties`; other
hosts and redirects to them are rejected before Basic or bearer credentials are
sent.
