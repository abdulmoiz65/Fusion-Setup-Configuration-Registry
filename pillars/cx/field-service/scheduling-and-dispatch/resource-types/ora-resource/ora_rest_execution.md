# Resource Types REST Execution

## Route Selection

`core.data-loader.task-rest` is the default direction. It owns whether the Core
Task REST route can execute the declared `PUT`. If it rejects `PUT`, stop and
require an explicit `ora_rest_execution` selection. Never fall back between
directions.

| Requested direction | Result |
|---|---|
| Omitted or `core.data-loader.task-rest` | Delegate only to the Core Task REST executor. Block when it does not permit `PUT`. |
| `ora_rest_execution` | Use the Field Service shared orchestration and this task adapter for preflight, immutable preview, approval-bound PUT, and GET verification. |

## Machine-Readable Operation Contract

```json
{
  "schemaVersion": "1.0",
  "taskCode": "ORA_FFS_TS_RESOURCE_TYPES",
  "defaultDirection": "core.data-loader.task-rest",
  "executionDirections": {
    "core.data-loader.task-rest": {"orchestration": "core-task-rest", "executorSkill": "core.data-loader.task-rest"},
    "ora_rest_execution": {"orchestration": "pillar-direct-rest", "executorSkill": "core.fusion-api.rest-api-client"}
  },
  "operations": [
    {"operationId": "put-resource-type", "method": "PUT", "pathTemplate": "/api/field-service/configuration/v1/resourceTypes/{label}", "requiredBodyFields": ["name", "active", "role", "translations"], "requiresCurrentState": true, "requiresExactPreview": true, "requiresExplicitApproval": true, "retryPolicy": "never", "verification": {"method": "GET", "pathTemplate": "/api/field-service/configuration/v1/resourceTypes/{label}"}}
  ]
}
```

## OFSC Metadata Endpoints

| Action | Logical OFSC Metadata path | Actual path |
|---|---|---|
| List Resource Types | GET `/rest/ofscMetadata/v1/resourceTypes` | `/api/field-service/configuration/v1/resourceTypes` |
| Read Resource Type | GET `/rest/ofscMetadata/v1/resourceTypes/{label}` | `/api/field-service/configuration/v1/resourceTypes/{label}` |
| Create or update Resource Type | PUT `/rest/ofscMetadata/v1/resourceTypes/{label}` | `/api/field-service/configuration/v1/resourceTypes/{label}` |

The Core REST client must receive the actual `/api/field-service/configuration/v1/`
paths because it does not rewrite logical OFSC Metadata aliases. Authenticate only
with `core.auth.fusion-oauth-authentication` through that client; do not use browser
automation or a separate HTTP client.

## Execution Rules

1. Read the workbook in free format. Require its `Resource Types` sheet, unique non-empty labels, unambiguous Active values, and applicable RT design-rule evidence; do not require an implementation template.
2. Require an active English language from the metadata language collection: `en` or `en-*`, including `en-US`.
3. The documented v1 PUT contract accepts only `active`, `name`, `role`, and `translations`. For a new Resource Type, send `If-None-Match: {label}` and use only that public body shape. Optional capabilities, load thresholds, cost, travel, and statistic fields have no confirmed public PUT mapping for this endpoint: retain their current values and block a workbook that requests a change. Do not send invented `capabilities` fields or inferred nested baselines.
4. GET the Resource Types collection and then GET each requested label. Only an actual `HTTP 404` response means a create candidate; text such as OAuth or browser output containing `404` is an error, not a create candidate.
5. Build an immutable preview with environment identity, selected route, method, logical path, request body, current-state baseline, and SHA-256 checksum.
6. Require explicit approval matching that exact checksum immediately before ordered PUT execution. Never retry a PUT automatically and never change routes after a failure.
7. After every successful PUT, GET and compare the approved fields. Account for bounded read-after-write delay with up to eight GET-only confirmation attempts, three seconds apart; never retry the PUT. If the final read-back still differs, stop immediately; do not send any later PUT or auto-rollback.
8. Persist only redacted diagnostics and run evidence under `project/{project_id}`. Never persist credentials, OAuth tokens, or customer payloads.

## Synthetic API Test Fixture

For endpoint contract testing only, the runner accepts `--test-payload-file`. It must
contain exactly one PUT to an `fscr_test_` label and a body containing exactly the
documented fields. This route is not workbook authoring and must never target a
customer Resource Type. It follows the same preview, checksum approval, no-retry,
and GET verification gates.
