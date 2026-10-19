# Time Slots REST Execution

The Time Slots direct-REST workflow uses the implementation API below. The
public metadata endpoint is discovery-only; it is not the create or update
route.

```json
{
  "schemaVersion": "1.0",
  "taskCode": "ORA_FFS_TS_TIME_SLOTS",
  "defaultDirection": "core.data-loader.task-rest",
  "executionDirections": {
    "core.data-loader.task-rest": {"orchestration": "core-task-rest", "executorSkill": "core.data-loader.task-rest"},
    "ora_rest_execution": {"orchestration": "pillar-direct-rest", "executorSkill": "core.fusion-api.rest-api-client"}
  },
  "operations": [
    {"operationId": "put-time-slot", "method": "PUT", "pathTemplate": "/api/field-service/configuration/v1/timeSlots/{itemId}", "identityRule": "itemId is the workbook Time Slot Label. Every request sends FS-IDENTIFY-BY: label. A 404 read is a create candidate and sends If-None-Match: {label}; a 200 read is an update candidate and omits If-None-Match to avoid a create-only conflict.", "requiredBodyFields": ["label", "name", "active", "timeStart", "timeEnd"], "requiresCurrentState": true, "requiresExactPreview": true, "requiresExplicitApproval": true, "retryPolicy": "never", "verification": {"method": "GET", "pathTemplate": "/api/field-service/configuration/v1/timeSlots/{itemId}"}}
  ]
}
```

| Action | Method | Relative path |
|---|---|---|
| Public documented list | GET | `/rest/ofscMetadata/v1/timeSlots` |
| Implementation search | GET | `/api/field-service/configuration/v1/timeSlots/` |
| Implementation read | GET | `/api/field-service/configuration/v1/timeSlots/{itemId}` |
| Implementation create | PUT | `/api/field-service/configuration/v1/timeSlots/{itemId}` |
| Implementation update | PUT | `/api/field-service/configuration/v1/timeSlots/{itemId}` |

The writable item body is exactly `label`, `name`, `active`, `timeStart`, and
`timeEnd`. `isAllDay` is present in the documented response but not the
documented request body, so it is not sent. The label is both the item identity
and a required payload field. Every PUT sends `FS-IDENTIFY-BY: label` and
`If-None-Match: {label}` only for a 404 create candidate. Omit
`If-None-Match` for a 200 update candidate; otherwise the implementation API
returns `409 Conflict` because the label already exists. Do not send POST,
PATCH, DELETE, or a metadata v1 item write.

Activity Types and Capacity Categories remain validation/design inputs only;
this task does not call their association APIs. Warehouse Visits has no mapped
writable field and is rejected.
