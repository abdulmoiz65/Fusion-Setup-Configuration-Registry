---
skill_id: "core.data-loader.task-rest"
name: "Task REST Execution"
description: "Execute an explicitly requested task-declared Oracle Fusion REST operation after Task Validation."
layer: "core"
type: "support"
execution_mode: "hybrid"
owner_team: "Central platform team"
---

# Task REST Execution

This Skill is called only by `core/data-loader/task-hook` after it resolves an Ora Resource rule plan and only when the user explicitly requests a named Ora REST operation. It never calls Data Loader upload or initiation.

1. Use the selected task context supplied by Task Hook; do not resolve another task.
2. If `ora-resource/ora_rest_execution.md` exists, read only its matching task/operation section. Otherwise read the matching section in `ora-resource/ora_rest_documentation.md`. Never merge or fall back from an existing `ora_rest_execution.md`; an absent or invalid operation there fails closed.
3. Refuse absent, ambiguous, or disabled operations. Permit only `GET`, `POST`,
   or `PATCH` with a declared relative Fusion REST path.
4. Obtain Describe metadata when declared and map supplied input to a draft payload. Submit the draft payload and evaluated rule results to Task Hook `validate-ora-rest-payload`. Do not preview or execute while a rule is blocked. For `POST` or `PATCH`, show the validated exact payload and obtain explicit approval immediately before execution. Do not retry writes.
5. Invoke only the shared client:

   `python core/fusion-api/rest-api-client/scripts/fusion_rest_client.py <URL> --method <METHOD> --header REST-Framework-Version=9 [--body <JSON>]`

6. Return the REST result as terminal. Do not prepare, upload, or initiate a
   Data Loader upload artifact afterwards.
