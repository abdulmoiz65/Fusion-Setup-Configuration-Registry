# Advanced Inventory Parameters Error Handling

## Error Rules

OrganizationCode input, REST DFF readiness, and Redwood LPN diagnostics below concern the REST-backed route. For FSM, use the native package rules in `ora_input_validation.md` and `ora_dependency_readiness.md`; do not apply REST field requirements to FSM columns. The no-delete restriction applies to both routes.

| Condition | Classification | Required handling |
| --- | --- | --- |
| `OrganizationCode` is absent or blank | Input validation | Stop and request one unambiguous parent organization code. The BO/Data Loader resolves the internal `OrganizationId`; do not ask callers to provide it. |
| Parent-template DFF child-section visibility/metadata is unavailable | Readiness blocker | Do not prepare a separate child load. Report the missing parent-template verification evidence and let `core.data-loader` validate the child section when preparing the parent load. |
| Inventory Management prerequisite is not established | Dependency blocker | Stop and resolve prerequisite setup before Data Loader handoff. |
| Operation or effective-value validation rejects the request | Non-overridable validation blocker | Return the issues from `ora_input_validation.md`. Never seek approval to bypass the no-delete policy or hand a rejected request to Data Loader. |
| A request disables an already-enabled LPN configuration | Fusion/Data Loader validation | The Redwood UI invokes a Fusion validation operation before it clears dependent LPN settings. Do not emulate that operation locally; preserve the Fusion/Data Loader diagnostic and require its resolution before retrying. |
| Data Loader or Fusion rejects a non-local field | Data Loader or Fusion validation | Preserve the diagnostic and do not duplicate backend validation locally. |
| FSM marker is missing, malformed, ambiguous, or package task identity does not match | FSM package validation | Stop and request a valid task export package. Do not synthesize missing metadata or rename REST fields to make a package appear valid. |
| Shared FSM validation reports an operation or metadata failure | FSM validation blocker | Stop before approval/upload and report the concrete shared diagnostic. Reject explicit delete requests or known delete settings; do not add an independent non-delete evidence requirement. |
| FSM import reports errors | Native FSM diagnostic | Preserve the native diagnostic and use core.data-loader status/error reporting, including available FSM ProcessLogs when status is requested. Any changed archive requires fresh validation and approval. |

## Correction and Retry Guidance

| Failure | Next step |
| --- | --- |
| REST input or final priority validation | Identify the organization, affected fields, and diagnostic. Request corrected values or the specific missing current-value evidence from ora_input_validation.md. Re-resolve changed meanings and validate the final combined values. |
| Authentication or environment access | Report the failed environment/read stage without exposing credentials. Restore access before retrying; do not change source data or retry submission to resolve authentication. |
| Package structure or task identity | Request a valid complete export or the authoritative object-to-task mapping, naming the missing/mismatched metadata item. Do not invent or repair package metadata by guessing. |
| FSM operation validation | Resolve concrete shared-loader/Fusion operation diagnostics. Reject explicit delete requests or known delete settings. Do not request an unverified operation marker or non-delete preflight evidence merely because native metadata describes an `EXPORT` process. |
| Native business-field error | Preserve the Fusion/FSM field diagnostic and request a correction through the appropriate source preparation workflow. Do not infer a new local rule from a generic error. |

After source values, mappings, package bytes, operation, or environment change, rerun applicable validation and the normal immutable-artifact approval workflow. For an uncertain upload/initiation outcome, use the shared loader's reconciliation/status procedure before considering another submission; do not blindly resubmit.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| ADV_INV_PARAMS.DATALOADER_HANDOFF | terminal | 40 | terminal | none | ADV_INV_PARAMS.APPLY_CROSSDOCK_DUE_DATE_SORT_DEFAULT | continue | Local identity, readiness, applicable reference-lookup checks, and approved default evaluation have passed; hand off to `core.data-loader`. |
| ADV_INV_PARAMS.RETURN_ISSUES | terminal | 90 | terminal | none | none | continue | Local validation or readiness is blocked or fails. |
| ADV_INV_PARAMS.FSM_DATALOADER_HANDOFF | terminal | 41 | terminal | none | ADV_INV_PARAMS.CHECK_FSM_READINESS | continue | FSM validation and readiness passed; hand off to core.data-loader for its normal approval and import workflow. No task-local import call. |
