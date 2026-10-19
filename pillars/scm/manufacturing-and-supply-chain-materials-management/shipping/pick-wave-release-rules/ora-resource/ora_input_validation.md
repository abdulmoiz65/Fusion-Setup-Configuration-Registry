# Pick Wave Release Rules Input Validation

Source: Redwood Pick Wave Release Rules page and dynamic layout.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Rule identity | ReleaseRule; ShipFromOrganizationName or ShipFromOrganizationCode | Stop before preview | Request the missing field using its Data Loader label. | Creating a pick wave release rule | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|
| Checkbox flag normalization | Normalize Y, Yes, True, Checked, and selected to `true`. Normalize N, No, False, Unchecked, and blank to `false`. Preserve already-normalized lowercase `true` or `false`. | PriorReservationsFlag, IncludeAssignedLinesFlag, AutoPickConfirmFlag, AutoShipOnPickConfirmFlag, CreateShipmentsFlag, AppendShipmentsFlag, or AutomaticallyPackFlag is supplied | |
| Active and range-date timestamp normalization | Normalize a supplied Start Date, End Date, From Requested Date, From Scheduled Ship Date, To Requested Date, or To Scheduled Ship Date to the BO timestamp format `YYYY-MM-DDTHH:MI:SS.sss+hh:mm`. For example, `9/9/26 12:00 AM` becomes `2026-09-09T00:00:00.000+00:00`. Do not serialize these values as Excel date serials, date-only values, or timestamps without milliseconds. | StartDateActive, EndDateActive, FromRequestedDate, FromScheduledShipDate, ToRequestedDate, or ToScheduledShipDate is supplied | |
| Pick-from field omission | When Pick From Subinventory is null, blank, or not supplied, omit `PickFromSubinventory` and `PickFromLocator` from DAT `METADATA` and do not serialize empty placeholders. | Pick From Subinventory is not supplied | |
| Project number mapping | Map the friendly input field Project Number to `ProjectCostingProjectNumber`. Do not populate `ProjectCostingProjectName` from this input. When generating a DAT file, omit `ProjectCostingProjectName` from `METADATA` entirely; do not serialize it as an empty field. | Project Number is supplied | |
| Release status | Preserve the supplied ReleaseStatusCode. The Redwood create form defaults it to E when the UI supplies no value. Do not create a task-local default. | Creating a rule through a source that supplies the UI default | |
| Destination type | Preserve the supplied DestinationTypeCode. The Redwood create form defaults it to S when the UI supplies no value. Do not create a task-local default. | Creating a rule through a source that supplies the UI default | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PWR.VALIDATE_INPUT | step | 10 | validate_input | passed->PWR.RESOLVE_RELEASE_STATUS;failed->RETURN_ISSUES | none | stop | Creating or validating a pick wave release rule |
