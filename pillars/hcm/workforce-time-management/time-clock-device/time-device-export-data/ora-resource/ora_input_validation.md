# Time Device Export Data Input Validation

## Source Basis

- Time Profiles Technical Design Document for FSCR, Confluence page 21722044713, read 2026-09-23.
- Developer-provided Time Device Export Data field definitions and create-payload reference, 2026-09-23.
- Developer-provided business-only Complete Summary requirements, 2026-09-23.

## Complete Summary Input Contract

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Verified summary source | Generate the summary only from populated structured business values that completed validation, applicable lookup resolution, and defaulting or preservation | A Complete Summary is prepared | |
| User selections | Include every verified user-provided business value | Every Complete Summary | |
| Applied defaults | Include every user-facing default that was actually applied in a separate Defaults Applied section | Every Complete Summary | |
| Blank and metadata values | Omit blank, null, unused, and metadata-only values | Every Complete Summary | |
| Populated children | Show populated child records using business labels only; do not render an empty child section | A child record has values | |
| Summary readiness | Always generate and display the Complete Summary and Defaults Applied immediately before requesting provider-owned approval | A create or update request is ready for provider approval | |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Export data identity | Name | Block the create or provider update request | Provide a non-empty Name | Create or provider update preparation | |
| Search criteria | At least one user-provided business attribute | Block the search request | Provide one or more business attributes to evaluate | Search or update selection | search_time_device_export_data_by_criteria |
| Summary readiness | Complete Summary and Defaults Applied | Block provider approval | Generate the required business-only summary from verified structured values | Create or update | |

## Creation Intake Disclosure

Before preparing a new Time Device Export Data definition, show every supported
configuration field below. Mark only `Name` as required. Do not present a
subset of optional fields as the complete creation input set.

| Configuration Field | Required | Input Type |
|---|---|---|
| Name | Yes | Text |
| Description | No | Text |
| Start Date | No | Date |
| Number Of Days in Period | No | Text |
| Number Of Objects in Batch | No | Text |
| First Name | No | Checkbox |
| Last Name | No | Checkbox |
| Badge ID | No | Checkbox |
| Payroll Time Types | No | Checkbox |
| Schedule | No | Checkbox |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name is mandatory | Reject a missing or empty Name | Create or provider update preparation | |
| Description is optional | Accept Description when supplied; omit it when not supplied | Always | |
| Start Date is optional | Accept Start Date in a user-provided date format when supplied; omit it when not supplied | Always | |
| Start Date normalization | Normalize a supplied, unambiguous Start Date to YYYY-MM-DD and write that exact value to `TcdExpStartDate` in every generated Data Loader source before validation or submission | Start Date is supplied | |
| Ambiguous or unresolvable Start Date | Block provider handoff and request an unambiguous date | Start Date cannot be normalized safely | |
| Number Of Days in Period is optional | Accept the supplied textbox value; omit it when not supplied | Always | |
| Number Of Objects in Batch is optional | Accept the supplied textbox value; omit it when not supplied | Always | |
| First Name is optional | Accept First Name as an optional checkbox selection | Always | |
| Last Name is optional | Accept Last Name as an optional checkbox selection | Always | |
| Badge ID is optional | Accept Badge ID as an optional checkbox selection | Always | |
| Payroll Time Types is optional | Accept Payroll Time Types as an optional checkbox selection | Always | |
| Schedule is optional | Accept Schedule as an optional checkbox selection | Always | |

## Provider Field Mapping

| Business Field | Provider Field | Value Handling |
|---|---|---|
| Name | Name | Required business value |
| Description | Description | Optional business value |
| Start Date | TcdExpStartDate | Optional business value; write the validated YYYY-MM-DD value to generated Data Loader sources |
| Number Of Days in Period | TcdExpDuration | Optional supplied textbox value |
| Number Of Objects in Batch | TcdExportBatchSize | Optional supplied textbox value |
| First Name | FirstNameFlag | Optional checkbox selection |
| Last Name | LastNameFlag | Optional checkbox selection |
| Badge ID | PersonBadgeIdFlag | Optional checkbox selection |
| Payroll Time Types | PayTimeTypesFlag | Optional checkbox selection |
| Schedule | ScheduleFlag | Optional checkbox selection |

## Preservation Rules

| Rule | What Happens | Applies When |
|---|---|---|
| Supplied business values | Preserve every supplied field value through validation for the provider-owned create or update flow | A field is supplied |
| Omitted optional fields | Keep an omitted optional field absent from the provider request; do not substitute a value or send an explicit not-selected value | A field is not supplied |
| Start Date representation | Preserve the user-provided Start Date for business interaction and use its validated normalized YYYY-MM-DD representation in the provider request and every generated Data Loader source | Start Date is supplied |
| Unspecified format and range rules | Do not invent a date format, numeric range, or checkbox dependency that is not documented in the supplied field definitions or the design | A supplied optional field is evaluated |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A search or update is requested | Require at least one user-provided business attribute and evaluate every supplied attribute as a conjunctive criterion | Retrieve every page, show all matching candidates, and request a selection when multiple candidates match | search_time_device_export_data_by_criteria |
| A new Time Device Export Data definition is prepared | Check exact Name, then case-insensitive partial Name, then every supplied non-Name attribute when neither Name check finds a match | If a match is found, present it and wait for the user's use-existing or create-new choice | search_time_device_export_data_by_criteria |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TDEDEXPORT_VALIDATE_INPUT | step | 1 | validate_input | valid->TDEDEXPORT_SEARCH_EXPORT_DATA;invalid->TDEDEXPORT_INPUT_BLOCKED | none | stop | Always |
