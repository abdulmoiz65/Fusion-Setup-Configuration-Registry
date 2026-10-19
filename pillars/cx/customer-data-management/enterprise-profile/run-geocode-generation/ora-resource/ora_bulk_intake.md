# Bulk Intake

## Accepted Bulk Inputs

| Input Format | What Must Be Provided | How Rows Are Processed |
|---|---|---|
| None | Not applicable | One ESS submission or one existing requestId is handled per skill run |

## Column Guidance

| Column Type | Allowed Fields | What Happens |
|---|---|---|
| Single structured request | fusion_environment_context, country or country_code, start_date, end_date, regenerate_geocode, batch_size, wait_seconds, poll_interval, project_id | Resolve the country when supplied, then validate and preview as one request |
| Array, CSV, spreadsheet, or table of requests | None | Reject before Fusion calls |

## Preview and Execution Rules

| Gate | Requirement |
|---|---|
| Catalog support | Do not route through FSM CSV export or import because CSVExportImportSupportedFlag is N |
| Submission count | Submit at most one new ESS request per direct execution instruction |
| Tracking | Resume the returned requestId instead of creating a replacement request |
