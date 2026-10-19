# Event Action Error Handling

Source: developer-provided EventAction-HDL.md, Error Responses and Troubleshooting, Validation Checklist, and Limitations. Diagnostic actions below do not supply literal Oracle error codes.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required action identity, type, dates, or submission value is missing | Stop before DAT preparation and identify exact missing fields. |
| LDG, Event Group, HCM group, or action type has zero or multiple target matches | Stop; report field and value, match count, and the target context without selecting a candidate. |
| Target metadata disagrees with public examples or supplied DAT | Stop; identify component, attribute, release, and discrepancy. Request current Attributes export. |
| Generated task metadata names Event Action and HDL, but target registration or current attributes are unconfirmed | Stop execution planning; confirm the registered business object and selected core data-loader contract before any import. |
| DAT import fails | Preserve sanitized import diagnostics; inspect ZIP/DAT name, delimiters, METADATA columns, and target schema. |
| HDL load row fails | Preserve row-specific error and external request/process identifier if available; correct only after classifying the failure. |
| No expected Event Action notification appears | Inspect group association, monitored events, worker Criteria, effective dates, and notification pages. |
| Manual action remains unprocessed | Inspect Process Event Actions flow selection, schedule, report, and warnings/errors. |
| A live HDL submission outcome is uncertain | Stop before retry; reconcile status and target setup through the approved data-loader workflow. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Missing, malformed, or inconsistent request fields | Correct the specified fields and revalidate. |
| catalog_or_metadata_mismatch | Withdrawn, unknown, or conflicting object attributes and values | Export target Attributes metadata and revise the mapping. |
| auth_authz | HDL or business-object access denied | Verify target privileges through the approved workflow. |
| transport_environment | Connection or target environment unavailable | Verify environment identity and connection; do not retry a possibly submitted mutation blindly. |
| fusion_api | Fusion rejects DAT import or HDL load | Capture row/process diagnostics and inspect exact reported cause. |
| process_timeout | HDL or related process has not completed in the allowed wait | Report request/process ID, last status, elapsed wait, and next check. |
| process_failed | Fusion process reports failure | Preserve ProcessLog/status if available and report failed rows. |
| artifact_persistence | DAT, result, or diagnostic could not be saved | Stop and restore artifact integrity. |
| approval_blocker | Exact preview, environment, artifact, or required approval is absent | Complete the selected data-loader workflow gate. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before live HDL import | Target environment, operation, immutable DAT/ZIP artifact, selected action identity, mapping, validation result, and the selected data-loader approval gate. |
| On failure | Stage, class, sanitized message, environment, artifact reference, row/process ID when available, partial successes, and safe next action. |
| On timeout | Environment, operation, TaskCode or job, ProcessId/requestId, last status, elapsed wait, and next-check route. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Lookup path or target metadata is TBD | No inferred REST lookup, browser shortcut, or claim of executable readiness. |
| Public sample conflicts with supplied DAT | No silent choice of one source, sample LDG, internal ID, or withdrawn field. |
| No approved live execution step is selected | No direct REST, OAuth, browser, or HDL submission from these resource tables. |
| Mutation outcome is uncertain | No automatic replay of POST, import, loader, or process operation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EA.EXECUTION_GATE | decision | 90 | execution_gate | ready->EA.RETURN_READY;blocked->EA.RETURN_ISSUES | EA.ENFORCE_DESIGN | stop | Check current target metadata, confirmed lookups, registered Event Action business object, exact immutable HDL artifact, approved core data-loader execution contract, and approval; writable route details are TBD |
| EA.RETURN_READY | terminal | 100 | terminal | none | EA.EXECUTION_GATE | stop | Return validated readiness only; no Fusion mutation is performed by this registry |
| EA.RETURN_ISSUES | terminal | 110 | terminal | none | none | stop | Return missing or failed validation, lookup, design, or execution-gate evidence |
