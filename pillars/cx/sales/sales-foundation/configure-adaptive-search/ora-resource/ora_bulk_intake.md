# Adaptive Search Publish Bulk Intake

## Accepted Bulk Inputs

| Input Format | What Must Be Provided | How Rows Are Processed |
|---|---|---|
| JSON string array | One exact object display name per element | Validate and submit as one atomic selective-publish selection |
| Plain table | One Object column | Normalize into one object selection; do not issue one publish per row |

## Column Guidance

| Column Type | Allowed Fields | What Happens |
|---|---|---|
| Required | Object | Display names are validated through localizedName and mapped internally to the REST entities array, except recognized CPQ aliases which add both direct CPQ entity names without catalog validation |
| Unsupported | Scheduling, credential, hostname, or arbitrary payload columns | Reject before preview |

## Preview and Execution Rules

| Gate | Requirement |
|---|---|
| Empty selection | Reject; never translate an empty input into a publish request |
| Validation | Report all invalid and duplicate object rows before preview; show up to three nearest suggestions for each invalid value, without exposing the full catalog |
| Atomic execution | Submit at most one POST for the approved object set |
| Retry | Never repeat the POST automatically after transport failure, timeout, or ambiguous submission result |
