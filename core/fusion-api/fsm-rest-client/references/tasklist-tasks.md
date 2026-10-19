---
name: tasklist-tasks
description: Return Oracle Fusion task-list items, including nested task lists and tasks. Use when the user asks for taskListItems, task-list contents, or a task-list-item CSV export.
---

# Task List Items

Return these columns in order: `PRODUCT`, `TASK_LIST_NAME`,
`TASK_LIST_SHORT_NAME`, `DISPLAY_SEQUENCE`, `ITEM_TYPE_CODE`,
`ITEM_TASK_LIST_NAME`, `ITEM_TASK_LIST_SHORT_NAME`, `ITEM_TASK_NAME`,
`ITEM_TASK_SHORT_NAME`.

Use read-only BOSS OAuth with `boss_scope` in `core/auth/fusionEnv.properties`
and the `.fusionaim_boss_token.json` cache. Never use the default `scope` token
or print credentials.

| Purpose | Method and endpoint |
|---|---|
| Enumerate task lists | `GET /api/boss/extraction/queries/ora/commonSetup/search/v1/$en/setupEntities` with `taskLists=TASKLIST` |
| Retrieve task-list items in batches | `GET /api/boss/data/objects/ora/commonSetup/tasks/v1/taskListItems/$views/manageTaskListSearch?$filter=taskList.taskListId in ({taskListIds})` |

Pass `$limit` and `$offset` for paged responses. Batch up to 100 task-list IDs
per `in (...)` filter to reduce API calls. Return 25 rows by default. Only when
the user explicitly asks for every item, generate a CSV.

Pass `--verbose` to receive a stderr update after task-list enumeration, each
item batch, and CSV creation. In preview mode, retrieve only one 25-task-list
`setupEntities` page before the first batched item request.

```bash
python3 core/fusion-api/fsm-rest-client/scripts/tasklist-tasks.py \
  --properties core/auth/fusionEnv.properties --preview-limit 25

python3 core/fusion-api/fsm-rest-client/scripts/tasklist-tasks.py \
  --properties core/auth/fusionEnv.properties --all --project-id <project_id>
```

Use `--output <path>` for an explicit local CSV destination. Report errors and
never call an export complete when any task-list request failed.
