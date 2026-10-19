# Shifts and Schedules REST Execution

## Route Selection

The default direction is `data_loader_execution`. It remains blocked until Core Data Loader establishes a supported import contract; this task has `CSVExportImportSupportedFlag=UNKNOWN`.

`ora_rest_execution` is an explicit alternative using the task-owned adapter and shared REST client. Its sequence is mandatory: create or resolve work schedules, create or resolve shifts, then create/update/delete work-schedule items. An item is never sent to a shift path.

## Machine-Readable Execution Contract

```json
{
  "schemaVersion": "1.1",
  "taskCode": "ORA_FFS_TS_SHIFTS_AND_SCHEDULES",
  "defaultDirection": "data_loader_execution",
  "executionDirections": {
    "data_loader_execution": {"orchestration": "core-data-loader", "executorSkill": "core.data-loader"},
    "ora_rest_execution": {"orchestration": "pillar-direct-rest", "executorSkill": "core.fusion-api.rest-api-client"}
  },
  "operations": [
    {"operationId": "work-schedule", "methods": ["GET", "PUT"], "pathTemplate": "/api/field-service/configuration/v1/workSchedules/{label}", "semantics": "upsert", "requiresExactPreview": true},
    {"operationId": "shift", "methods": ["GET", "PUT"], "pathTemplate": "/api/field-service/configuration/v1/shifts/{label}", "semantics": "upsert", "requiresExactPreview": true},
    {"operationId": "work-schedule-item", "methods": ["GET", "POST", "PUT", "DELETE"], "readPathTemplate": "/api/field-service/configuration/v1/workSchedules/{label}/items", "writePathTemplate": "/api/field-service/configuration/v1/workSchedules/{label}/items/{itemId}", "requiresCurrentState": true, "requiresExactPreview": true, "requiresExplicitApproval": true, "retryPolicy": "never", "verification": {"method": "GET", "pathTemplate": "/api/field-service/configuration/v1/workSchedules/{label}/items"}}
  ]
}
```

## Required REST Sequence

1. GET each work schedule by label. A 404 is a creation baseline; PUT the workbook parent with `If-None-Match: {label}`.
2. GET each shift by label. A 404 is a creation baseline; PUT the workbook parent with `If-None-Match: {label}`.
3. After the ordered parent requests are planned, GET `/api/field-service/configuration/v1/workSchedules/{label}/items`, construct item requests, and execute them after approval.
4. After every write, GET the resource or item collection and verify the exact changed values. Stop on the first failure.

## API Mapping

| Resource | Method | Relative path | Documented request fields |
|---|---|---|---|
| Work schedule | GET / PUT | `/api/field-service/configuration/v1/workSchedules/{label}` | `name`, `active` |
| Shift | GET / PUT | `/api/field-service/configuration/v1/shifts/{label}` | `name`, `active`, `type`, `points`, `workTimeStart`, `workTimeEnd` |
| Work-schedule item | GET / POST | `/api/field-service/configuration/v1/workSchedules/{label}/items` | `type`, `label`, `shiftType` for shift items, `startDate`, `endDate`, `recurrence`, `comments` |
| Work-schedule item | PUT / DELETE | `/api/field-service/configuration/v1/workSchedules/{label}/items/{itemId}` | Workbook `itemId` supplies the documented item identity plus the same item body fields |

The filled workbook retains implementor-friendly columns: `shiftLabel` maps to item `label`; `nonWorkingReasonLabel` maps to item `label`; `repeatType` and `repeatDays` map to `recurrence.type` and full weekday values in `recurrence.weekdays`. `itemId` is OFSC-generated for POST and is used only in PUT and DELETE paths.

Source: [API Structure - Configuration](https://confluence.oraclecorp.com/confluence/display/OFSCdev/API+Structure+-+Configuration), Work Schedules and Shifts v1 sections.
