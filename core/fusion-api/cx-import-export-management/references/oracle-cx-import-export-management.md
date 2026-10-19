# Oracle CX Import and Export Management REST Reference

This reference captures the minimum Oracle REST API details needed by
`core.fusion-api.cx-import-export-management`.

## Import Management

Official endpoint:

- Create file import activity:
  `POST /crmRestApi/resources/11.13.18.05/importActivities`
  Source: https://docs.oracle.com/en/cloud/saas/sales/faaps/op-importactivities-post.html
- Create file import activity data file:
  `POST /crmRestApi/resources/11.13.18.05/importActivities/{ImportActivityId}/child/DataFiles`
  Source: https://docs.oracle.com/en/cloud/saas/sales/faaps/op-importactivities-importactivityid-child-datafiles-post.html
- Get file import activity:
  `GET /crmRestApi/resources/11.13.18.05/importActivities/{ImportActivityId}`
  Source: https://docs.oracle.com/en/cloud/saas/sales/faaps/op-importactivities-importactivityid-get.html

Important payload fields:

| Field | Meaning |
| --- | --- |
| `Name` | Import job name. Required by Oracle. |
| `ObjectCode` | Object being imported, such as `Account`, `Contact`, or `Opportunity`. |
| `ImportMapping` | Existing mapping number. Oracle requires either mapping number or object code for practical import creation. |
| `DataFiles` | Array of source file references. |
| `DataFiles[].FileName` | Source CSV file name. |
| `DataFiles[].InputFileContentId` | UCM document name for the source CSV file, for example `UCMFA06213998`. |
| `ImportMode` | Common values include `CREATE_ONLY`, `CREATE_RECORD`, and `DELETE_RECORD`. |
| `Activate` | `YES` activates/queues the job; `NO` saves without activation. |
| `Schedule` | Default immediate one-time scheduling is `ONE_TIME_IMMEDIATE`. |

Returned identifier:

- `ImportActivityId`

Status and report fields may appear on the activity or data-file child,
including `Status`, `ReadFromFile`, `LoadedSuccessfully`, `ErrorsReported`,
`Warnings`, `ErrorReportContentId`, `ExceptionReportContentId`, and
`SuccessReportContentId`.

## UCM Upload for Import Files

CX Import Management references source files by UCM document name. In a
successful UI-created Account import, `DataFiles[].InputFileContentId` was in
the `UCMFA06213998` format and the import completed with records read and
loaded. Numeric values returned by generic ERP Integration Service upload calls
were accepted by the REST `DataFiles` child but later failed during
`PREPARING_IMPORT_DATA` because CX Import Management could not resolve the file
from content management.

Repository grounding and limitation:

- This pod exposes the ERP Integration Service REST resource at
  `{restBaseUrl}/fscmRestApi/resources/11.13.18.05/erpintegrations`. The
  resource name is lower-case `erpintegrations`.
- The REST create operation accepts fields including `OperationName`,
  `DocumentContent`, `FileName`, `ContentType`, `FileType`, `DocumentAccount`,
  and `Comments`.
- Use `OperationName=uploadFileToUCM` to upload through REST. The documented
  REST payload uses a file type value such as `csv` or `zip` in `ContentType`,
  not a MIME type such as `text/csv`.
- In this pod, successful ERP Integration REST upload returned numeric
  `DocumentId` only, for example `6207050`, not a `UCMFA...` document name.
  The `getDocumentIdsForFilePrefix` finder also returns numeric document ids.
- Use UCM GenericSoapPort
  `{restBaseUrl}/idcws/GenericSoapPort` with `IdcService=GET_SEARCH_RESULTS`
  and query text `dID <matches> \`{DocumentId}\`` to resolve the numeric id to
  `dDocName`. This was verified on this pod: `DocumentId=6207050` resolved to
  `dDocName=UCMFA06214121`.
- SOAP
  `uploadFileToUcm` on `{restBaseUrl}/fscmService/ErpIntegrationService`
  remains a fallback.
- For CX Import Management, do not assume the SOAP `uploadFileToUcm` `<result>`
  or REST `DocumentId` numeric value is valid for `InputFileContentId`. Resolve
  or capture the UCM document name (`UCM...`) before submitting the import.

Operational fields used by the script:

| Field | Meaning |
| --- | --- |
| `OperationName` | ERP Integration REST operation. Defaults to `uploadFileToUcm`. |
| `DocumentContent` / `Content` | Base64 encoded file bytes. REST uses `DocumentContent`; SOAP uses `Content`. |
| `FileName` | File name visible in UCM. |
| `ContentType` | MIME type such as `text/csv`. |
| `FileType` | File extension/type, such as `csv`. |
| `DocumentTitle` | UCM document title. |
| `DocumentSecurityGroup` | Defaults to `FAFusionImportExport`. |
| `DocumentAccount` | UCM account. Must be supplied by the user/project. |

The UCM document account is not guessed by the skill. Ask for the customer or
project standard, for example a CX Import Management account value, before
executing an upload.

## Import Mapping

Oracle's standard REST import flow creates an import map before activating the
import activity:

1. `POST /crmRestApi/resources/11.13.18.05/importMappings`
2. Add mapping columns under `ImportMappingColumns`
3. Activate the import with `ImportMapping` and `DataFiles[].InputFileContentId`

On this pod, creating the mapping and its `ImportMappingColumns` as a nested
payload in one `POST /importMappings` call succeeded. Creating the map first and
then posting to the returned child collection URL returned `404`, despite the
child link being advertised in the response.

Example nested payload:

```json
{
  "Name": "Account import map",
  "ObjectCode": "Account",
  "ImportMappingColumns": [
    {
      "ColumnHeader": "OrganizationName",
      "ExampleValue": "Codex Account",
      "AttributeCode": "OrganizationName"
    },
    {
      "ColumnHeader": "Country",
      "ExampleValue": "GB",
      "AttributeCode": "Country"
    }
  ]
}
```

## Export Management

Official endpoint:

- Create bulk export activity:
  `POST /crmRestApi/resources/11.13.18.05/bulkExportActivities`
  Source: https://docs.oracle.com/en/cloud/saas/sales/faaps/op-bulkexportactivities-post.html
- Get bulk export activity:
  `GET /crmRestApi/resources/11.13.18.05/bulkExportActivities/{BulkExportJobId}`
  Source: https://docs.oracle.com/en/cloud/saas/sales/faaps/op-bulkexportactivities-bulkexportjobid-get.html

Important payload fields:

| Field | Meaning |
| --- | --- |
| `Name` | Export job name. Required by Oracle. |
| `ExportObject` | Object code being exported. Required by Oracle. |
| `ExportColumnNames` | Comma-separated columns to export. |
| `ExportFilterCriteria` | Object filter criteria for selected records. |
| `ExportMapping` | Existing export mapping. |
| `ExportFileName` | Name of exported file uploaded to the repository. |
| `Activate` | `YES` activates/queues the job; `NO` saves without activation. |
| `ScheduleModeCd` | Default one-time scheduling is `ONETIME`. |
| `ScheduleTypeCd` | Default immediate scheduling is `IMMEDIATE`. |

Returned identifier:

- `BulkExportJobId`

Download guidance:

- `ExportFileURL` is intended for browser download.
- For programmatic download, follow the `/enclosure/ExportFileContents` link
  returned by the export activity after the job completes.
- This skill can directly call
  `/crmRestApi/resources/11.13.18.05/bulkExportActivities/{BulkExportJobId}/enclosure/ExportFileContents`
  for export output and
  `/crmRestApi/resources/11.13.18.05/bulkExportActivities/{BulkExportJobId}/enclosure/ErrorReportFileContents`
  for export error output.

## Operational Notes

- Use `core.auth.fusion-oauth-authentication` for OAuth token acquisition.
- Use the same `restBaseUrl` configured in `core/auth/fusionEnv.properties`.
- Use `crmRestApi`, not `fscmRestApi`, for these CX endpoints.
- UCM GenericSoapPort accepted the same OAuth bearer token on this pod, even
  though `/cs/idcplg` redirected to the WebCenter/IDCS sign-in page.
- Submit mutating requests only after the user confirms the target pod and job.
