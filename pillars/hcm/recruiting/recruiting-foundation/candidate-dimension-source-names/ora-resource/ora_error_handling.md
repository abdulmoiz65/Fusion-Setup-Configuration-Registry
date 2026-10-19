# Error Handling

| Outcome | When it applies | Required response |
| --- | --- | --- |
| `MISSING` | No exact source identity is found after checking the applicable verified export or task UI. | Stop and request the exact identity. |
| `AMBIGUOUS_SOURCE` | More than one source matches the supplied identity. | Stop and request a unique identity. |
| `BLOCKED` | Required UI action, editability, access, or fresh evidence is not verified. | Stop; state what must be verified. |
| `TBD` | The requested behavior has no verified UI/export evidence. | Do not infer it; record it as TBD. |

Do not manufacture field-specific validation text or Oracle UI error codes. Report only messages observed in the verified UI/export evidence.

## Retrieval failures

A missing export dependency, unknown CSV support, authentication or privilege
failure, unavailable output path, export failure or timeout, or unverifiable
package returns `BLOCKED`. Preserve the failure stage, selected environment,
task code, original ProcessId when available, last observed status, artifact
references, and next action in the project run record. Report only observed
Fusion messages; never expose credentials or token-cache contents.

Do not return stale rows as fresh data or substitute a direct API, browser,
import, or another task. Export failures remain on the issue path and cannot
reach successful retrieval. Continue or retry only when subsequently requested
under the shared export skill's recovery contract.

## Rename failures

Missing dependencies or fresh export, ambiguous identity, invalid CSV/ZIP, a duplicate proposed default name, more than one changed cell, a Task Hook failure, or missing archive approval blocks import. Report the concrete failed stage. An absent exported row does not authorize a fabricated row or browser fallback. Uncertain export or import results require reconciliation of the original process, not automatic resubmission. Preserve the existing target profile and never disclose credentials.

## Add Row failures

Missing Name/URL/language, duplicate Name or URL, ambiguous baseline joins, changed headers, invalid source provenance, unsupported values, archive preservation failure, or a Task Hook error blocks creation. Return the exact validation finding. Preserve existing source data and leave failed validation without an upload. A successful Data Loader initiation is asynchronous, not proof that the new row exists. Reconcile a failed or uncertain original import before retrying; do not use an update or browser Save to bypass creation errors.


## Preview and import gate

For a mutation, present the selected environment, operation, exact source identity,
requested changes, applied defaults, baseline timestamp and candidate SHA-256 using
core.data-loader's normal report. Follow that skill's contextual approval rule:
approval of the exact validated archive or explicit same-request auto-approval.
An initial rename/Add Row instruction alone authorizes preparation and validation.
A materially changed request or archive requires a new preview and valid approval.

Core Data Loader owns Task Hook preview approval/integrity verification, UCM upload
and FSM initiation. Pass the exact approved archive, selected profile and verified
taskValidationEnvelope; never call import REST directly or switch to browser Save.
Return the loader's result, retain its original process identity, and reconcile
completion before claiming the source was changed. Retrieval and internal
validate_import perform no upload; a validation terminal is not a live success claim.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CDSN.READINESS_GATE | decision | 60 | execution_gate | ready->CDSN.DONE_VALIDATED;blocked->CDSN.HANDLE_ISSUES | CDSN.ENFORCE_DESIGN | stop | Return retrieval or validation findings; require the core Data Loader preview/approval lifecycle before mutation |
| CDSN.HANDLE_ISSUES | step | 70 | error_handler | disclosed->CDSN.RETURN_ISSUES | none | stop | A request, dependency, lookup, preservation, approval or process issue occurs |
| CDSN.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | A blocking issue is disclosed |
| CDSN.DONE_VALIDATED | terminal | 90 | terminal | none | CDSN.READINESS_GATE | stop | Return findings to the caller; this terminal never submits a load |
