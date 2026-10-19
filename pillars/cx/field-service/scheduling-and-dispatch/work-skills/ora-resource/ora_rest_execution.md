# Work Skills REST Execution

## Route Selection

Use `core.data-loader.task-rest` by default. It owns the default Task REST
operation. If it does not permit `PUT`, stop and require an explicit
`ora_rest_execution` request. Never select the other route automatically.

| Requested direction | Result |
|---|---|
| Omitted or `core.data-loader.task-rest` | Delegate only to Core Task REST; block if its operation contract rejects PUT |
| `ora_rest_execution` | Use the task-owned OFSC Metadata read, immutable-preview, approval-bound PUT, and GET verification workflow |

## Machine-Readable Operation Contract

```json
{
  "schemaVersion": "1.0",
  "taskCode": "ORA_FFS_TS_WORK_SKILLS",
  "defaultDirection": "core.data-loader.task-rest",
  "executionDirections": {
    "core.data-loader.task-rest": {
      "orchestration": "core-task-rest",
      "executorSkill": "core.data-loader.task-rest"
    },
    "ora_rest_execution": {
      "orchestration": "pillar-direct-rest",
      "executorSkill": "core.fusion-api.rest-api-client"
    }
  },
  "operations": [
    {
      "operationId": "put-work-skill",
      "method": "PUT",
      "pathTemplate": "/rest/ofscMetadata/v1/workSkills/{label}",
      "requiredBodyFields": ["name", "active", "sharing", "translations"],
      "requiresCurrentState": false,
      "requiresExactPreview": true,
      "requiresExplicitApproval": true,
      "retryPolicy": "never",
      "verification": {
        "method": "GET",
        "pathTemplate": "/rest/ofscMetadata/v1/workSkills/{label}"
      }
    },
    {
      "operationId": "put-work-skill-group",
      "method": "PUT",
      "pathTemplate": "/rest/ofscMetadata/v1/workSkillGroups/{label}",
      "requiredBodyFields": ["active", "assignToResource", "addToCapacityCategory", "translations", "workSkills"],
      "requiresCurrentState": false,
      "requiresExactPreview": true,
      "requiresExplicitApproval": true,
      "retryPolicy": "never",
      "verification": {
        "method": "GET",
        "pathTemplate": "/rest/ofscMetadata/v1/workSkillGroups/{label}"
      }
    }
  ]
}
```

## Free-Format Workbook and Write Rules

1. Read any `.xlsx` worksheet containing the specified field/value pairs. Do not require the implementation template. Require Work Skill Label, English Name, Active, and Sharing of the skill in teamwork for Work Skills. For groups, require a Work Skill Group Label, English Name, Active, and at least one member row with Work Skill Label and Ratio. `Assign to Resource` and `Add to Capacity Category` default to false unless explicitly enabled.
2. Require Active to be unambiguous. The source contract demonstrates the API value `maximal` for sharing; do not translate other UI display values to undocumented API enums.
4. Authenticate through `core.auth.fusion-oauth-authentication`; use the shared Core REST client. Require an active English language label of `en` or `en-*` before mapping a request.
4. Build an immutable preview with environment identity, route, method, path, body, current-state baseline (or explicit absence), and SHA-256 checksum. Require explicit approval of that exact checksum before every PUT.
5. Issue Work Skill PUTs first and Work Skill Group PUTs second, each in displayed workbook order. The Configuration API declares both PUTs as upserts, so a missing GET baseline is a creation candidate; do not retry PUT, fall back to the other route, or delete. Every group member must be included in the workbook or already exist in the target environment. GET-verify each successful PUT.
7. Persist only redacted diagnostics and run evidence under `project/{project_id}`. Never persist credentials, tokens, private keys, or customer payloads there.

## OFSC Metadata Endpoints

| Action | Method | Relative path |
|---|---|---|
| List Work Skills | GET | `/rest/ofscMetadata/v1/workSkills/` |
| Read Work Skill | GET | `/rest/ofscMetadata/v1/workSkills/{label}` |
| Update Work Skill | PUT | `/rest/ofscMetadata/v1/workSkills/{label}` |
| Delete Work Skill | DELETE | `/rest/ofscMetadata/v1/workSkills/{label}` |
| List Work Skill Groups | GET | `/rest/ofscMetadata/v1/workSkillGroups/` |
| Read Work Skill Group | GET | `/rest/ofscMetadata/v1/workSkillGroups/{label}` |
| Update Work Skill Group | PUT | `/rest/ofscMetadata/v1/workSkillGroups/{label}` |
| Delete Work Skill Group | DELETE | `/rest/ofscMetadata/v1/workSkillGroups/{label}` |
| List instance languages | GET | `/rest/ofscMetadata/v1/languages` |
