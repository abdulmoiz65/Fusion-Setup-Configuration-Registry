# Work Zones REST Execution

## Route Selection

`ora_rest_execution` is the default and only supported direction. No route may fall back to Data Loader or a different endpoint family.

## Machine-Readable Operation Contract

```json
{
  "schemaVersion": "1.0",
  "taskCode": "ORA_FFS_TS_WORK_ZONES",
  "defaultDirection": "ora_rest_execution",
  "executionDirections": {
    "ora_rest_execution": {
      "orchestration": "pillar-direct-rest",
      "executorSkill": "core.fusion-api.rest-api-client"
    }
  },
  "operations": [
    {
      "operationId": "create-work-zone",
      "method": "POST",
      "pathTemplate": "/rest/ofscMetadata/v1/workZones",
      "requiredBodyFields": ["workZoneLabel", "workZoneName", "status", "keys"],
      "requiresCurrentState": true,
      "requiresExactPreview": true,
      "requiresExplicitApproval": true,
      "retryPolicy": "never",
      "verification": {
        "method": "GET",
        "pathTemplate": "/rest/ofscMetadata/v1/workZones/{workZoneLabel}"
      }
    },
    {
      "operationId": "replace-work-zone",
      "method": "PUT",
      "pathTemplate": "/rest/ofscMetadata/v1/workZones/{workZoneLabel}",
      "requiredBodyFields": ["workZoneLabel", "workZoneName", "status", "keys"],
      "requiresCurrentState": true,
      "requiresExactPreview": true,
      "requiresExplicitApproval": true,
      "retryPolicy": "never",
      "verification": {
        "method": "GET",
        "pathTemplate": "/rest/ofscMetadata/v1/workZones/{workZoneLabel}"
      }
    }
  ]
}
```

## Execution Rules

1. Read the supplied `.xlsx` in free format. Locate a `Work Zones` worksheet and a populated header row for `Work Zone Name`, `Work Zone Label`, `Status`, and `Work Zone Key`; do not require an implementation template.
2. Validate a nonblank selected environment identity first. Then validate required labels/names, active or inactive status, unique case-insensitive keys, the documented 50-character maximum for each key, and the task-local `WZ.ENFORCE_DESIGN` evidence gate. `travelArea` is deprecated as of OFSC 26B, is not required, and must be omitted. The adapter may send only documented `shapes` and `translations` optional fields; it must not send `organization`.
3. Authenticate only through `core.auth.fusion-oauth-authentication` and use the Core REST client after all local gates pass. Resolve each current Work Zone with `GET /rest/ofscMetadata/v1/workZones/{workZoneLabel}` for the immutable preview. A structured HTTP 404 selects `POST /rest/ofscMetadata/v1/workZones` to create the absent Work Zone. A found baseline selects singular `PUT /rest/ofscMetadata/v1/workZones/{workZoneLabel}` to replace it.
4. Create an immutable preview in memory containing environment identity, selected route, method, path, body, current-state baseline (or absent baseline), and SHA-256 checksum. Persist only its redacted run evidence under `project/{project_id}`; never persist credentials, tokens, or customer request bodies.
5. Require explicit approval equal to the fresh checksum before each ordered POST or PUT. Never retry a live write. After each successful write, use bounded GET-only read-back polling to compare approved fields. On the first write or verification failure, stop all remaining requests, retain only an allowlisted diagnostic (`HTTP` status, error code, or field), and require a fresh continuation preview. Do not fall back between execution directions.

## OFSC Metadata Endpoints

| Action | Method | Relative path |
|---|---|---|
| Read Work Zone | GET | `/rest/ofscMetadata/v1/workZones/{workZoneLabel}` |
| Create Work Zone | POST | `/rest/ofscMetadata/v1/workZones` |
| Replace Work Zone | PUT | `/rest/ofscMetadata/v1/workZones/{workZoneLabel}` |
