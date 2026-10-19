# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required Name, Code, or Provider is missing for any requested record. | Stop before artifact generation and identify the record and missing field. |
| Name, Code, or Description exceeds its verified maximum length for any requested record. | Stop before artifact generation and identify the record and field limit. |
| The provider is unsupported for any requested record. | Stop before artifact generation. |
| A prohibited secret, token, credential, tenant value, customer configuration value, session value, or process metadata outside a required local FSM source or generated ZIP is supplied for a configuration preview or import artifact. | Redact the value and stop before artifact generation. Required non-secret process metadata may remain unchanged only inside the local ZIPs and must not be logged, quoted, committed, or persisted elsewhere. |
| A task-level export is explicitly requested. | Start the routed task-level export without a separate protected-data confirmation or approval. A possible, theoretical, or historical indication of protected content is not an error or blocker; do not refuse, substitute a template-only export, or redirect to manual Fusion. Required non-secret process metadata inside the local source or generated FSM ZIPs under the Empty-Export Metadata Replacement Contract is not a protected value for this rule; do not quote or log it. If the returned content includes any other protected value, do not persist or quote it; stop artifact processing and return a sanitized diagnostic. |
| A requested batch is empty, repeats a ConfigCode or ConfigName, contains an invalid record, or changes the requested record order. | Stop before package generation; correct the complete batch and regenerate one package. Do not submit an eligible subset. |
| A requested ConfigCode or ConfigName duplicates an existing exported source row. | Stop before package generation; leave the source export unchanged and require a distinct request. Do not copy or append the source row to a candidate. |
| A Code or Name collision is reported by Fusion after submission. | Preserve the per-record outcome and reconcile every requested record. Do not replay, rename, or add a duplicate row automatically; use a fresh target export before any new delta is proposed. |
| A provider-settings CSV is supplied or generated. | Stop; the verified package contains no provider-settings CSV. |
| XML parsing finds the exact null provider-metadata collection in a fresh target export. | Apply the Empty-Export Metadata Replacement Contract only when every precondition holds. Retain the source export, create a separate immutable package, and stop with Package contract if parsing, selection, replacement, or output validation fails. |
| The metadata-repair path is selected and the target collection is not the exact null form, or the constructed canonical mapping does not match the task-local rule. | Stop before package generation. Do not request a reference XML or invent substitute mapping values. |
| Target audit, immutable package review, or package SHA-256 is missing. | Do not hand off the import; return the request to preflight. |
| A controlled import passes preflight. | Hand off only to core.data-loader; do not construct or submit a direct FSM request or request a duplicate task-level approval from this resource flow. |
| A Data Loader import request is accepted. | Show a status card with the request or process reference, state Processing, and an explicit Check CAPTCHA import status action. Do not report success or poll automatically. |
| A Data Loader import status is Succeeded. | Show the request or process reference, final status, and loaded and failed counts when available. Offer an optional Verify CAPTCHA configuration action. If the user selects it, use the existing fresh task-level export and CAPTCHA.RECONCILE_EXPORT workflow; do not start that verification otherwise. |
| A multi-provider import completes with partial provider-row failures. | Preserve successful and failed provider-row evidence, reconcile every requested record, and do not retry automatically. |
| Post-import export does not reconcile every requested provider row's requested Code and Name, Provider ID, or Draft status. | Preserve sanitized diagnostics, do not retry automatically, and investigate before any further operation. |
| Fusion or the shared exporter denies required task-level export access, or Fusion or core.data-loader denies required task-level import access. | Stop, report the missing access, and do not change routes or retry. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A requested configuration record is missing, over length, unsupported, prohibited, or duplicates a Code or Name within the batch. | Correct the complete configuration batch and rerun validation, or use the explicit task-level export pathway when an export is requested. |
| Authorization | Fusion or the shared exporter denies required task-level export access, or Fusion or core.data-loader denies the requested task-level import operation. | Restore the required access; do not change routes. |
| Preflight blocker | A controlled multi-provider import lacks a fresh target audit, an allowed immutable package, its requested record set, or package SHA-256. | Return to preflight. |
| Import handoff | The controlled import has passed task-level preflight. | Hand off only to core.data-loader, which owns final execution approval. |
| Processing | Data Loader accepted the package but success is not verified. | Check CAPTCHA import status later. |
| Import succeeded | A Data Loader import status reports Succeeded. | Show the final status card and offer optional CAPTCHA configuration verification. Do not report the configuration as verified unless the user selects it and the fresh export reconciles every requested provider record. |
| Package contract | The package includes a provider-settings CSV, carries an existing source configuration row, does not match the verified multi-provider shape, has a requested Code or Name collision with the batch or fresh target export, alters source-export metadata beyond the exact null collection, or has an unverified canonical mapping, CSV header, requested record set, Draft row, or package SHA-256. | Rebuild one new package using the fresh target metadata, task-local canonical mapping when required, verified ordered provider-header CSV containing only requested rows, and generated package identity. |
| Reconciliation | A post-import export does not reconcile every requested provider record's requested Code and Name, Provider ID, and Draft status, or the import has partial provider-row failures. | Preserve per-record diagnostics and investigate; do not retry automatically. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input validation | The missing or invalid configuration field and the corrective action. |
| Authorization or preflight blocker | The blocked operation and the required access-restoration or preflight action, without exposing protected values. |
| Import handoff | Exact target, task code, requested record count, immutable package identity, and the one core.data-loader handoff boundary. |
| Data Loader accepted the package | A status card with Processing state, available request or process reference, an explicit Check CAPTCHA import status action, and the safe next action. |
| Data Loader import succeeded | A final status card with request or process reference and loaded and failed counts when available, plus an offered optional Verify CAPTCHA configuration action. |
| Package contract | The missing or prohibited package component, requested record count, and the verified multi-provider package boundary. |
| Reconciliation | Per-record expected and observed values, any Draft-state mismatch, and the safe investigation step. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Secret or credential input is supplied. | Do not log, persist, include, or generate the protected value. |
| Direct migration service access is requested. | Do not call an internal Fusion migration service. |
| A controlled import is not fully preflighted. | Do not submit or hand off the import. |
| A controlled import is fully preflighted. | Do not request a task-level approval or construct or submit a direct FSM request; hand off only to core.data-loader. |
| The null collection or constructed canonical mapping does not exactly match the metadata-repair rule. | Do not alter the source export, substitute a mapping, or submit an import. |
| Credential completion, validation, or activation is requested. | Do not perform the action through this skill. |
| Reconciliation fails or a write result is uncertain. | Do not retry automatically. |
| Only a hypothetical protected-value risk, stale blocker, or unrelated workspace note exists. | Do not preemptively refuse the requested task-level export, substitute a template-only export, redirect to manual Fusion, or request storage approval. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAPTCHA.GATE_EXPORT | decision | 15 | execution_gate | export_authorized->CAPTCHA.COMPLETE_EXPORT_HANDOFF | CAPTCHA.VALIDATE_INPUT | stop | An explicit task-level export request passed input validation. Hypothetical protected-content risk is not a gate failure. |
| CAPTCHA.COMPLETE_EXPORT_HANDOFF | terminal | 16 | terminal | none | CAPTCHA.GATE_EXPORT | stop | Return export_ready to the outer task workflow. The direct request authorizes the read-only export without a second confirmation or approval. |
| CAPTCHA.GATE_IMPORT | decision | 50 | execution_gate | ready_for_import_handoff->CAPTCHA.COMPLETE_IMPORT_HANDOFF;blocked_for_import_handoff->CAPTCHA.IMPORT_BLOCKED | CAPTCHA.ENFORCE_DESIGN | stop | A controlled multi-provider import passed task-level preflight. This task does not request approval. |
| CAPTCHA.HANDLE_INPUT_ERROR | step | 70 | error_handler | handled->CAPTCHA.RETURN_ISSUES | CAPTCHA.VALIDATE_INPUT | stop | Input validation is invalid. |
| CAPTCHA.HANDLE_DEPENDENCY_ERROR | step | 71 | error_handler | handled->CAPTCHA.RETURN_ISSUES | CAPTCHA.CHECK_DEPENDENCIES | stop | A dependency is unavailable or incomplete. |
| CAPTCHA.HANDLE_DESIGN_BLOCKER | step | 72 | error_handler | handled->CAPTCHA.RETURN_ISSUES | CAPTCHA.ENFORCE_DESIGN | stop | A design gate blocks progress. |
| CAPTCHA.HANDLE_RECONCILIATION_ERROR | step | 73 | error_handler | handled->CAPTCHA.RETURN_ISSUES | CAPTCHA.RECONCILE_EXPORT | stop | A post-import reconciliation does not match every requested provider record's requested Code and Name, Provider ID, or Draft status. |
| CAPTCHA.DONE_DRAFT_PREVIEW | terminal | 80 | terminal | none | CAPTCHA.ENFORCE_DESIGN | stop | A non-secret Draft preview is compliant. |
| CAPTCHA.IMPORT_BLOCKED | terminal | 81 | terminal | none | CAPTCHA.GATE_IMPORT | stop | Import preflight is incomplete. |
| CAPTCHA.COMPLETE_IMPORT_HANDOFF | terminal | 82 | terminal | none | CAPTCHA.GATE_IMPORT | stop | Import preflight is verified; hand off the one immutable multi-provider package only to core.data-loader, which owns final execution approval. |
| CAPTCHA.DONE_RECONCILED | terminal | 83 | terminal | none | CAPTCHA.RECONCILE_EXPORT | stop | The fresh post-import export reconciles the requested Code and Name, Provider ID, and Draft status for every requested provider record. |
| CAPTCHA.RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | An issue has been handled. |
