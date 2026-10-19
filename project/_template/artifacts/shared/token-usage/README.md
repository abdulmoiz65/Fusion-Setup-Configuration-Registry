# Token Usage Tracking

This folder is for estimated token usage records for implementation tasks that
write artifacts into `project/{project_id}`.

These records are operational estimates, not billing-grade usage metrics. Use
them to compare task patterns, understand context size, and identify expensive
artifact-generation workflows.

## When to Log

Create or update a token usage entry when a task writes one or more project
workspace artifacts, such as reports, exports, validation results, baselines,
configuration blueprints, or generated HTML/PDF files.

Logging is the default for any activity that updates `project/{project_id}`.
Repository scripts should call `core/project-mgmt/scripts/token_usage_logger.py`
after writing workspace artifacts. Manual or assisted workflows should append
the same table format before the activity is considered complete.

## Recommended Location

```text
project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md
```

If a task needs a more detailed record, add a task-specific file under:

```text
project/{project_id}/artifacts/shared/token-usage/current/
```

## Recommended Columns

| Column | Description |
|---|---|
| Activity Start Time | Activity start timestamp in ISO 8601 format, including timezone when known. Use the local project timezone unless the workflow records UTC. |
| Task | Short task name. |
| Trigger | User request or workflow that caused the task. |
| Number of Artifacts Written | Count of files created or updated under `project/{project_id}`. |
| Number of Files Read | Count of important local files or documentation pages used as context. |
| Estimated Input Tokens | Approximate tokens read from local files or tool outputs. |
| Estimated Output Tokens | Approximate tokens written into generated artifacts or final response. |
| Estimated Total Tokens | Sum of estimated input and output tokens. |
| Estimation Method | Example: `chars/4`, tokenizer, or manual estimate. |
| Notes | Caveats, excluded context, or why usage may be undercounted. |

If the exact artifact paths or source files matter for auditability, list them
in `Notes` or create a task-specific detail file under `current/`.

## Estimation Guidance

- Prefer a tokenizer when available.
- Otherwise use `characters / 4` as a simple approximation.
- Separate generated artifact tokens from conversational final-answer tokens
  when useful.
- State when estimates exclude model-internal reasoning, hidden system
  context, or tool metadata.
- If an older entry only has a date and the exact start time is unknown,
  preserve the date by normalizing to `T00:00:00` in the project timezone and
  note the limitation when useful.
