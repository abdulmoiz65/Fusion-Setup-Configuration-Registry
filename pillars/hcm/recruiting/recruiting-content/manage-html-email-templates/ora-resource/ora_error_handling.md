# Manage HTML Email Templates Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required template identity, type, or package member is missing | Stop before preview and request the exact missing value or archive member. |
| Dependent CSV files are absent | Generate both dependent CSV files from the approved baseline, validate matching MessageDesignCode values, and show the generated values in preview. |
| Supplied dependent CSV files are partial or invalid | Stop; do not overwrite user-supplied dependent files with defaults. |
| A cross-environment archive has both existing and new templates | Show the target-existing and target-new template names; stop before preview until the user chooses Replace existing templates or Import only new templates. |
| User chooses Import only new templates | Rebuild the reviewed archive with only target-new parent rows and their matching metadata and type-association rows; do not retain orphaned dependencies. |
| Activate, deactivate, interactive design edit, or delete is requested | Do not construct an FSM package or automate browser/UI actions. Explain that the documented task CSV package has no lifecycle status or delete operation and provide the manual Manage HTML Email Templates UI steps. |
| DesignMetadata is minimal, incomplete, or incompatible | Classify as design-metadata validation failure; preserve evidence, rebuild from a compatible complete source, preview again, and obtain new approval. |
| Task access or routed operation is unavailable | Classify as auth/authz and stop; use an authorized operator. |
| Export or import process fails | Preserve redacted process status/log when requested and do not retry a live operation automatically. |
| An approved import is accepted by Fusion | Report initiation immediately. Do not poll, retrieve results, run a reconciliation export, or list templates unless the user explicitly asks. |
| The user asks Check the import result, Did the import work?, Were the templates created?, Show import errors, or another plain-language result question | Resolve the most recent matching import request from the active task context and retrieve its result and available ProcessLog through the declared FSM/Data Loader route. Ask for the request ID only when no matching request is available or more than one is ambiguous. The same approval covers this read-only follow-up while the archive, target environment, and intended operation are unchanged. |
| Import results complete successfully with no errors | State that the selected templates were created. Do not run a target export unless the user explicitly asks for a listing or template-specific verification. |
| Archive changes after preview | Treat approval as stale; validate the changed archive and obtain fresh approval. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required values, member files, keys, cross-environment archive comparison, or import handling choice are invalid or missing | Correct the exact value or rebuild the archive. |
| Design metadata validation | Complete compatible design structure fails | Rebuild from compatible complete metadata and re-preview. |
| Auth or authz | Task or routed executor access is unavailable | Stop and route to the security owner. |
| Process failed | Export or import returns failed terminal state | Retrieve status/log when requested; do not replay automatically. |
| Approval blocker | Preview, immutable artifact identity, or immediate approval is missing or stale | Stop and obtain a current exact approval. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview | Target environment, template identity, requested action, selected source template when cloning, included member files, row scope, and SHA-256. |
| Mixed-archive handling choice | Complete Existing template names list, complete New template names list, and the two choices: Replace existing templates or Import only new templates. Do not show counts alone. |
| Mutation approval | Exact target, business effect, immutable import archive, and the current approval request. |
| Failure | Failure class, task code, stage, sanitized evidence, and one safe next action. |
| Accepted import | State that the import was initiated. Do not show a template list or run a reconciliation export by default. |
| Requested import result | Succeeded, In progress, or Failed; total, loaded, and failed counts; and every actionable ProcessLog diagnostic when errors are reported. Do not ask for another approval when the approved archive, target environment, and operation are unchanged. |
| Post-import semantic verification | Only when explicitly requested, run a fresh task-level FSM export and show re-exported template name, type/purpose, language, and complete design metadata from the task CSVs. |
| FSM list response | One row per exported MessageDesignCode with Name, Template Type, and the mapped Campaign Purpose or Email Type. Do not expose Template, Subject, Language, CSV codes, or raw metadata. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Incomplete or minimal design metadata | Do not submit merely because the ZIP is structurally valid. |
| Mixed existing/new archive without a handling choice | Do not preview, submit, or silently choose replacement or exclusion behavior. |
| Failed or uncertain mutation | Do not retry or create another record automatically. Retrieve the result when requested; require a fresh explicit approval for any retry, and reconcile with a fresh task-level export when the user requests verification or a retry is being considered. |
| Unsupported automated service contract | Do not infer a REST endpoint, payload, lookup, or UI route. Use only task-level FSM export and FSM Data Loader import. |
| Lifecycle or interactive design operation requested through FSM | Do not infer a status transition, delete record, or designer update from the CSV package. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HET.EXECUTION_GATE | decision | 50 | execution_gate | ready->HET.DONE;blocked->HET.HANDLE_ERROR | HET.ENFORCE_DESIGN | stop | The request is validated and ready to route to task-level FSM export or FSM Data Loader import |
| HET.HANDLE_ERROR | step | 60 | error_handler | handled->HET.RETURN_ISSUES | none | stop | Any validation, dependency, design, approval, export, import, or verification failure |
| HET.RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| HET.DONE | terminal | 80 | terminal | none | HET.EXECUTION_GATE | stop | All resource checks passed and the request is ready for task-level FSM export or FSM Data Loader import |

## Manual UI Lifecycle Handoff

For a delete request, provide these generic steps and do not open or control the Fusion UI:

1. Open **Setup and Maintenance** in Fusion.
2. Search for and open **Manage HTML Email Templates**.
3. Search for the template name supplied in the request.
4. Select the intended record, choose **Delete**, and confirm the deletion in Fusion.
5. If verification is needed, ask for a fresh template-list export after the user confirms the UI action is complete.
