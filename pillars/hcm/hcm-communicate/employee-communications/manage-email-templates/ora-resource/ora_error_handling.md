# Manage Email Templates Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| OAuth configuration or privilege is missing | Stop before the Fusion call and route to the designated OAuth or security owner |
| Task-level FSM export process fails | Retrieve and preserve the sanitized process log; do not replay automatically |
| FSM import that creates a template fails or has an uncertain outcome | Preserve the sanitized import process log and do not submit the archive again until the target state is verified and a new immutable execution cycle starts |
| FSM status-transition import for one or more templates fails or has an uncertain outcome | Preserve the sanitized import process log; do not retry the archive; obtain fresh export evidence for every requested template and start a new immutable execution cycle before any further action |
| Express template is absent from the export | Record the evidence gap; create a representative Express template manually and request a fresh export |
| New Campaign metadata differs from the selected hardcoded editor default | Block import preview and use the matching complete value from `ora_defaulting_rules.md`; do not substitute values from a target export |
| Generated MessageDesignCode conflicts with the target export | Generate a new nonce against the same preflight export, rebuild all linked CSV rows with the replacement key, and repeat the conflict check before preview; do not re-export solely for this retry |
| Existing target templates conflict | Present existing and new names and obtain an explicit replace or new-only choice |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Auth/authz | OAuth configuration or task privilege is missing | Stop and route to the designated OAuth or security owner |
| Process failed | Task-level FSM export process fails | Preserve the sanitized process log; retry only through a new execution cycle |
| Process failed | FSM import creation process fails or has an uncertain outcome | Verify target state before considering a new immutable archive and execution cycle |
| Process failed | FSM status-transition import for one or more templates fails or has an uncertain outcome | Verify every requested target by fresh export; do not retry the archive without a new execution cycle |
| Catalog/evidence gap | Express evidence is absent from the export | Obtain a representative Express export before validation or import design decisions |
| Input validation | Metadata or linked parent rows are incompatible | Correct the candidate package and rerun validation |
| Execution blocker | Existing target templates conflict or the core Data Loader execution gate is incomplete | Obtain the explicit replace/new-only choice or complete the core Data Loader execution gate |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before FSM export | Task code, target environment, privilege readiness, and requested read-only evidence |
| Before FSM import | Immutable validated archive, exact target environment, intended operation, and the Core Data Loader execution-gate result for the exact archive |
| After successful Campaign template FSM creation or archive import | Import process identifier and terminal status, followed by fresh task-level export evidence. Then ask the requester to open **Setup and Maintenance → HCM Communicate → Employee Communications → Manage Email Templates** to review and design the template content manually. |
| After FSM status transitions | Import process identifier and terminal status, followed by fresh task-level export evidence of every transitioned template or a sanitized failure record |
| Export process failure | Process identifier, last status, elapsed wait, sanitized process log reference, and safe next action |
| Evidence gap | Missing Express template type or metadata baseline and the manual/export action required to resolve it |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Express DesignTypeCode or editor-specific metadata is absent | Do not infer it from Campaign data or claim Express migration or validation |
| HTML Campaign metadata uses blank design metadata with US/Y language settings | Do not replace it with Basic, Advanced, or target-template metadata |
| UI-only action is requested | Do not automate UI creation, editing, deletion, or sending through FDOS. Creating a Campaign template or changing only an existing Campaign template's status through a validated FSM import is not a UI-only action |
| FSM process fails or outcome is uncertain | Do not retry automatically or report success |
| Import is considered | Do not import without a validated archive and the Core Data Loader execution gate; do not request task-level confirmation for a name/key check, generated-code retry, or individual rows in the same immutable archive |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HCMET.EXECUTION_GATE | decision | 40 | execution_gate | ready->HCMET.DONE;blocked->HCMET.RETURN_ISSUES | HCMET.ENFORCE_DESIGN | stop | Validated request is limited to a declared FSM route |
| HCMET.RETURN_ISSUES | terminal | 50 | terminal | none | none | stop | Any blocking issue prevents safe completion |
| HCMET.DONE | terminal | 60 | terminal | none | HCMET.EXECUTION_GATE | stop | All required checks pass for the declared route |
