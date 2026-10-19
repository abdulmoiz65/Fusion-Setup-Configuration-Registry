---
name: tasks-bo
description: Return Oracle Fusion setup-task-to-business-object relations. Use when the user asks for tasks_bo relations, task business objects, or a task-to-business-object CSV export.
---

# Task to Business Object Relations

Return `PRODUCT`, `TASK_NAME`, `TASK_SHORT_NAME`,
`BUSINESS_OBJECT_SHORT_NAME`, and `BUSINESS_OBJECT_NAME`, in that order.

Use read-only BOSS OAuth with `boss_scope` in `core/auth/fusionEnv.properties`
and `.fusionaim_boss_token.json`. Call the direct relationship resource:

```text
GET /api/boss/data/objects/ora/commonSetup/tasks/v1/taskBusinessObjects
```

This resource returns each relation with nested `task` and `businessObject`
objects. Use `$limit` and `$offset`; return 25 rows by default. Only on an
explicit request for the entire list, write a CSV.

```bash
python3 core/fusion-api/fsm-rest-client/scripts/tasks-bo.py \
  --properties core/auth/fusionEnv.properties --preview-limit 25 --verbose

python3 core/fusion-api/fsm-rest-client/scripts/tasks-bo.py \
  --properties core/auth/fusionEnv.properties --all --project-id <project_id> --verbose
```

`--verbose` reports progress after each relationship page and CSV creation.
