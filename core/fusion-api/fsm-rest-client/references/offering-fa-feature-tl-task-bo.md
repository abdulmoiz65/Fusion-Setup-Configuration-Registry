---
name: offering-fa-feature-tl-task-bo
description: Fetch Oracle Fusion offering to functional-area-or-feature to task-list to task to business-object mappings. Use when the user asks for this end-to-end hierarchy with product, classification, and display-name path, as a preview or complete CSV export.
---

# Offering to Task to Business Object Map

Return these columns:

`OFFERING`, `FA_FEATURE`, `PRODUCT_FAMILY`, `PRODUCT`, `CLASSIFICATION`,
`TASK_LIST_NAME`, `TASK_NAME`, `BUSINESS_OBJECT_NAME`, and `PATH`.

Enumerate only `availableOfferings`; retrieve FA and feature hierarchy rows per
offering; resolve FA/feature metadata in `featureShortName in (...)` batches;
collect feature-to-task-list associations; expand task lists through batched
`taskListItems/$views/manageTaskListSearch` calls; and enrich tasks through one
bulk business-object request. Use each business object's nested manage-task
relationship; do not call an endpoint per task or task list. Where a task list
cannot be resolved in bulk, retain its association record as the task fallback.

Return a compact JSON preview by default. Only when the user explicitly asks
for the entire list, use `--all` and save a CSV. Retain and report the `errors`
array; never describe an export with errors as complete.

## API contract

All calls use the BOSS base URL and `boss_scope`.

| Purpose | Method and endpoint |
|---|---|
| Offering enumeration | `GET /api/boss/data/objects/ora/commonSetup/features/v1/features/$views/availableOfferings` |
| Functional-area hierarchy | `GET /api/boss/extraction/queries/ora/commonSetup/features/v1/availableFunctionalAreasByOffering?parentShortName={offering}` |
| Feature hierarchy | `GET /api/boss/extraction/queries/ora/commonSetup/features/v1/availableFeaturesByOffering?parentShortName={offering}` |
| FA/feature metadata | `GET /api/boss/data/objects/ora/commonSetup/features/v1/features` |
| Feature-to-task/list association | `GET /api/boss/extraction/queries/ora/commonSetup/features/v1/associatedTasksAndTaskListsByFeature?featureShortName={feature}` |
| Task-list id resolution fallback | `GET /api/boss/extraction/queries/ora/commonSetup/search/v1/$en/setupEntities` with `taskLists=TASKLIST` |
| Batched task-list expansion | `GET /api/boss/data/objects/ora/commonSetup/tasks/v1/taskListItems/$views/manageTaskListSearch?$filter=taskList.taskListId in ({taskListIds})` |
| Business-object names and manage-task associations | `GET /api/boss/data/objects/ora/commonSetup/businessObjects/v1/businessObjects` |

Fetch `availableOfferings` with `$limit` and `$offset` pagination so the full
offering list is included. The remaining collection endpoints also support
`$limit` and `$offset`.
Join a task to its business objects using the business object's nested
manage-task relationship. Product family and product come from FA/feature
metadata; no release enrichment is performed. Path values must use display names
and start with `/`, for example `/Compensation Management/Absence Management`.

## Execution

```bash
python3 core/fusion-api/fsm-rest-client/scripts/offering-fa-feature-tl-task-bo.py \
  --properties core/auth/fusionEnv.properties \
  --preview-limit 25
```

For a complete export:

```bash
python3 core/fusion-api/fsm-rest-client/scripts/offering-fa-feature-tl-task-bo.py \
  --properties core/auth/fusionEnv.properties \
  --all --project-id <project_id>
```

Use `--offering-short-name` to scope the mapping and `--output` for an explicit
CSV path. Use BOSS OAuth (`boss_scope`) and never print bearer tokens or
authorization headers. Review the API contract above before changing endpoint
behavior.

For a resumable full export, use `--offering-offset`, `--offering-limit`,
`--node-offset`, and `--node-limit` to write small CSV batches, then run
`scripts/merge_offering_fa_feature_tl_task_bo_batches.py` over the batch CSVs. This
is required where the execution host imposes short foreground job limits.
