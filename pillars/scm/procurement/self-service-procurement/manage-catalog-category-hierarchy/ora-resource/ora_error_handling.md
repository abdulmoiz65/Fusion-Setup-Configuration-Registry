# FSM Validation Handoff and Result Reporting

Task: POR_MANAGE_CATALOG_CATEGORY_HIERARCHY. Expected TYPE: SHOPPING. FSM CSV only; execution remains with the generated skill’s routed export, validation, and core.data-loader services. These resources perform local preparation and evidence assessment; they declare no product REST operation.

Source: user-approved rules derived from reviewed native FSM exports and import receipts (September 2026). Preventive safeguards below are authoring policy, not claims of tested Oracle rejection behavior.

Successful FSM tests cover browsing-category creation and purchasing-category relationships, including a new item placement and an unchanged existing relationship. A numeric-looking category name with a descriptive code was accepted. Name-only and other name/code failures do not establish matching precedence or a mandatory CategoryCode rule.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Local preparation passes | Return the exact prepared artifact and disclosures to the declared workflow. Local success is neither import authorization nor proof of Fusion acceptance |
| FSM returns an invalid/nonexistent category error | Preserve the server message and offending row identity in the allowed project diagnostics; do not infer mandatory code, matching precedence, item-master absence or a safe replacement identity |
| Terminal status and ProcessLog disagree or one is unavailable | Preserve both sources and classify the outcome as unresolved unless available authoritative evidence establishes the process result; disclose any client-status retrieval failure separately |
| Partial success or uncertain completion | Retain successful-object and failed-object results with an errors array; do not automatically replay the package or discard partial success |
| Authentication or transport failure | Delegate recovery to the core workflow; do not re-submit an import as an authentication probe |
| Process timeout or failed process | Preserve environment, task, process/request IDs, last status, elapsed wait and available logs; use the core next-check/retry path |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | CSV contract, identifier shape or proposed structural safeguard fails | Correct affected rows before handoff |
| catalog mismatch | Task, TYPE, metadata or selected native contract differs | Resolve the selected task/package mismatch |
| auth/authz | Authentication or privilege failure | Use the core authorized recovery policy |
| transport/environment | Communication or environment identity failure | Resolve environment evidence before continuing |
| Fusion API | Server request is rejected | Retain server diagnostics and use the declared workflow’s recovery path |
| process timeout | Polling expires without terminal result | Stop polling and provide the next-check path; do not submit a duplicate |
| process failed | FSM reports failed or partially failed processing | Preserve ProcessLog and partial results; correct the cause before any approved retry |
| artifact persistence | Required package, receipt or diagnostic cannot be saved | Stop and restore durable evidence before handoff or retry |
| approval blocker | Core workflow’s required approval is missing | Follow that workflow’s approval gate; add no duplicate task approval |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Core workflow handoff | Exact target environment, TaskCode, immutable import artifact, intended row delta, reference uncertainties and any possible reassignment; core owns preview/approval and submission |
| Validation report | Separate archive validation, task-rule validation, FSM processing and independent target readback; explicitly label skipped or unperformed stages |
| FSM processing report | Terminal process status and available logs, object counts separately from row counts, warnings, errors and partial successes; two passed objects do not mean two imported rows |
| Verification report | Distinguish server-reported processing success from independent export/UI verification; never claim readback when it was not performed |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing reference evidence | Do not invent an internal ID, silently translate codes, assert nonexistence or introduce a product REST route |
| Failed or uncertain mutation | Do not auto-replay an import; require core-supported idempotency or explicit retry authorization |
| Local success terminal | Do not label a completed preparation graph as a completed Fusion import |

The graph ends at preparation handoff. Post-execution reporting guidance is consumed by the routed workflow when results exist; no Task Node here submits or polls a Fusion job.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCH.HANDOFF | step | 50 | execution_gate | ready->RETURN_SUCCESS;blocked->RETURN_ISSUES | CCH.DESIGN | stop | Preparing disclosures and handing the artifact to the existing core workflow |
| RETURN_SUCCESS | terminal | 90 | terminal | none | CCH.HANDOFF | stop | Local preparation is complete; Fusion execution and verification remain with the routed workflow |
| RETURN_ISSUES | terminal | 100 | terminal | none | none | stop | A reached preparation check blocks handoff; return actionable issues |
