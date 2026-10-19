---
name: fa-feature-tl-tasks
description: Return Oracle Fusion FA/feature-to-task-list-or-task rows with product, classification, and release versions. Use when the user asks for the FA_FEATURE_TL_Tasks report, a feature task-list/task mapping, or its complete CSV export.
---

# FA_FEATURE_TL_Tasks

Return exactly these columns, in this order: `PRODUCT`, `FILTER_NAME`,
`CLASSIFICATION`, `AVAILABLE_RELEASE_VERSION`, `EXPIRATION_RELEASE_VERSION`,
`TASK_LIST_NAME`, `TASK_NAME`.

`FILTER_NAME` is the feature display name. Map a source classification of
`LICENSE` to `Functional Area`; map a blank source classification to `Feature`.
A row can contain a task list, a standalone task, or both, exactly as Fusion
returns it; do not expand task lists into their member tasks. Preserve absent
values as blank CSV cells.

## API contract and authentication

Use read-only BOSS calls and obtain OAuth with `boss_scope` from
`core/auth/fusionEnv.properties`. Keep the BOSS token in
`.fusionaim_boss_token.json`; never use the default `scope` token or print
bearer tokens/authorization headers.

| Purpose | Method and endpoint |
|---|---|
| Feature metadata | `GET /api/boss/data/objects/ora/commonSetup/features/v1/features` |
| Feature task-list/task associations | `GET /api/boss/extraction/queries/ora/commonSetup/features/v1/associatedTasksAndTaskListsByFeature?featureShortName={featureShortName}` |

Pass `$limit` and `$offset` to collection requests. Retry once with a fresh
`boss_scope` token after a 401 or 403 response.

## Execution

Return the first 25 records by default:

```bash
python3 core/fusion-api/fsm-rest-client/scripts/fa-feature-tl-tasks.py \
  --properties core/auth/fusionEnv.properties --preview-limit 25
```

Only when the user explicitly requests the entire list, generate a CSV:

```bash
python3 core/fusion-api/fsm-rest-client/scripts/fa-feature-tl-tasks.py \
  --properties core/auth/fusionEnv.properties --all --project-id <project_id>
```

Use `--output <path>` instead of `--project-id` for an explicit local CSV
destination. Report the CSV path, row count, API-call count, and errors; never
describe an export with errors as complete.

Pass `--verbose` for updates after feature retrieval, each feature-association
request, and CSV creation. The association endpoint accepts one feature code per
request, so it is not batched.
