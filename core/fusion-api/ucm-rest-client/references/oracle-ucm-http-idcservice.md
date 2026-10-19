# Oracle UCM HTTP IdcService Notes

Fusion UCM exposes Oracle WebCenter Content services through the HTTP
IdcService endpoint, normally:

```text
{restBaseUrl}/cs/idcplg
```

The utility in this folder can call that endpoint with either:

- OAuth bearer authentication from `core/auth/fusion-oauth-authentication`
- Fusion Basic authentication supplied at runtime with `--auth-mode basic`

If a bearer-authenticated call returns the WebCenter Content sign-in HTML page,
the endpoint is reachable but did not accept the OAuth token for IdcService.
Try Basic authentication for that environment. If Basic authentication also
returns the sign-in page, the SaaS pod is enforcing an interactive SSO cookie
for `/cs/idcplg`; the HTTP IdcService endpoint is not usable as a headless UCM
upload API from this client.

## Services Used

- `PING_SERVER`: verifies endpoint and authentication.
- `CHECKIN_UNIVERSAL`: checks in a local file. The file part is sent as
  `primaryFile` by default.
- `DOC_INFO_BY_NAME`: returns document metadata for a UCM document name such as
  `UCMFA06213998`.
- `DOC_INFO`: returns document metadata for numeric `dID`.
- `GET_SEARCH_RESULTS`: searches UCM metadata.
- `GET_FILE`: downloads the primary file content.

## CX Import Management Link

CX Import Management `DataFiles[].InputFileContentId` expects the UCM document
name (`dDocName`) rather than the numeric document id (`dID`).

ERP Integration Service SOAP `uploadFileToUcm` can return only a numeric id in
some environments. That numeric id is not sufficient for CX Import Management
file import activities. Direct UCM check-in should return the `dDocName`, which
is the value to pass to CX import.

## Common Fields

Typical check-in fields for Fusion import/export staging are:

- `dDocTitle`: display title, usually the file name.
- `dDocType`: document type. The utility defaults to `Document`.
- `dSecurityGroup`: defaults to `FAFusionImportExport`.
- `dDocAccount`: UCM account, for example `crm/simplifiedAccount/import/`.
- `dDocAuthor`: optional author override.

Additional metadata can be supplied through repeated `--field Name=value`
arguments.

## Safety

The upload command performs a dry run unless `--execute` is supplied. Read-only
commands (`ping`, `info`, `search`) can be used to verify endpoint behavior
before checking in a file.

Do not store Fusion passwords in `fusionEnv.properties`. Prefer
`--prompt-password` for interactive runs or `--password-env` for automation.
