# Activity Types REST Execution

## Route Selection

Use `ora_rest_execution` as the default task direction. It is the only
executable route for this task because its declared mutation is `PUT`, while
`core.data-loader.task-rest` permits only `GET`, `POST`, and `PATCH`.
`core.data-loader.task-rest` remains an explicit fail-closed selection for
callers that require Core routing; it cannot be delegated or substituted for
this `PUT` operation.

| Requested direction | Result | Rule |
|---|---|---|
| Omitted or `ora_rest_execution` | Select the pillar-owned OFSC Metadata REST workflow: GET preflight, immutable preview, approval-bound PUT, then GET verification through the shared REST client | Default executable route |
| `core.data-loader.task-rest` | Block before preview | Core Task REST permits only GET, POST, and PATCH; it cannot execute this declared PUT and there is no fallback |
| Data Loader archive/import | Block | This task's CSV support is `UNKNOWN` and the package route is on hold |

## Machine-Readable Operation Contract

```json
{
  "schemaVersion": "1.0",
  "taskCode": "ORA_FFS_TS_ACTIVITY_TYPES",
  "defaultDirection": "ora_rest_execution",
  "executionDirections": {
    "core.data-loader.task-rest": {
      "orchestration": "core-task-rest-unsupported-put",
      "executorSkill": "core.data-loader.task-rest",
      "supported": false,
      "blocker": "Core Task REST permits only GET, POST, and PATCH; Activity Types requires PUT."
    },
    "ora_rest_execution": {
      "orchestration": "pillar-direct-rest",
      "executorSkill": "core.fusion-api.rest-api-client"
    }
  },
  "operations": [
    {
      "operationId": "put-activity-type",
      "method": "PUT",
      "pathTemplate": "/rest/ofscMetadata/v1/activityTypes/{label}",
      "requiredBodyFields": ["label", "active", "groupLabel", "defaultDuration", "translations"],
      "requiresCurrentState": true,
      "requiresExactPreview": true,
      "requiresExplicitApproval": true,
      "retryPolicy": "never",
      "verification": {
        "method": "GET",
        "pathTemplate": "/rest/ofscMetadata/v1/activityTypes/{label}"
      }
    }
  ]
}
```

## Execution Rules

1. Resolve active languages, the selected group, and every Activity Type by label using the OFSC Metadata API before mapping a payload. Require an active English label: base `en` or a regional English label such as `en-US`; accept the API's boolean or legacy string representation of `active`.
2. Treat a `404` Activity Type read as a create candidate. Treat a `200` as an update candidate and preserve approved optional fields not changed by the requested design. Stop on any other read result.
3. Build an immutable preview containing selected direction, environment identity, method, path, request body, current-state summary, field-level diff, and SHA-256 digest. Any direction, body, path, environment, or current-state change invalidates it.
4. Require explicit approval bound to that digest immediately before each `PUT`. Do not retry a `PUT`, substitute a write, delete, or roll back. A requested `core.data-loader.task-rest` direction stops before preview because its owned capability does not permit `PUT`; it never falls back automatically.
5. `ora_rest_execution` is a mutating route after its approval gate; its preflight GETs are not its terminal behavior. After each successful `PUT`, issue the declared `GET` verification and compare returned required fields with the approved request. Persist only redacted diagnostics and references under the project workspace. Do not fall back after a failure.

## OFSC Metadata Endpoints

| Action | Method | Relative path |
|---|---|---|
| Discover active languages | GET | `/rest/ofscMetadata/v1/languages` |
| Read group | GET | `/rest/ofscMetadata/v1/activityTypeGroups/{label}` |
| Read Activity Type | GET | `/rest/ofscMetadata/v1/activityTypes/{label}` |
| Create or update Activity Type | PUT | `/rest/ofscMetadata/v1/activityTypes/{label}` |

The shared REST client resolves these relative paths from the selected FSCR environment profile. Do not substitute a different endpoint family for this execution route.
