# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| OAuth authentication or authorization fails | Stop and report the authentication or privilege blocker without revealing credentials or tokens. |
| Unauthenticated CPQ deployment-version lookup returns `404` | Show: “CPQ is not dpeloyed in this instance and hence cannot proceed with Setups now.” Stop before initialization or any Setup Assistant call. |
| A read-only assistant lookup fails | Stop before mutation and report only a business-safe failure summary. Persist any endpoint or transport-status detail solely in the internal sanitized diagnostics artifact. |
| Initialize, company-profile update, user creation, or submission fails | Do not retry automatically; retain the safe diagnostic and verify current state before any further action. |
| Company Profile reports an unfamiliar existing-data value | Do not expose the raw value. Show that the company setup state cannot be determined safely, then stop before PATCH until the state is reconciled. |
| Company Profile reports `IsDataExisting` as `DOESNT_EXIST` after CPQ initialization | Continue with CPQ company setup. Collect enterprise name, currency, country, Legal Address Address Line 1 only, and CPQ company identifier; do not collect a complete address, city, state/province, postal or PIN code, additional address lines, Legal Entity, or Business Unit. |
| Company Profile reports `IsDataExisting` as `PARTIAL` | Stop before collecting changes or PATCH. Show: “Partial setups are completed and hence unable to proceed.” |
| Company Profile reports `IsDataExisting` as `ESSJOBALREADYSCHEDULED` | Stop before collecting changes or PATCH. Show: “A Retrieve Latest LDAP Changes or Send Pending LDAP Requests job is active. You must cancel the existing jobs before continuing with Setup Assistant.” |
| A requested CPQ user is already present | Do not create a duplicate. Report whether the user is already a CPQ administrator or requires role-assignment investigation; continue only with other validated, approved administrators. |
| Submission outcome is uncertain | Use the one immediate read-only setup-progress lookup to reconcile; do not submit a second request. |
| Immediate setup-progress lookup is indeterminate | Persist sanitized diagnostics and show: “CPQ setup status could not be determined safely.” End without mutation or inference; a later read requires an explicit user request. |

## Partial-Execution Recovery

When a company-profile update or administrator creation fails or is uncertain before submission, stop mutations and preserve the consumed approval and pending marker. Use `inspect-child-outcome` for read-only observations classified as `matches_approved`, `not_observed`, or `uncertain`. Absence is not proof that the original job cannot apply later. Persist only sanitized diagnostics and one safe next action.

Ordinary full reconciliation can advance only an exactly identified successful job whose complete expected state is verified. `recover-prewrite` can release only a proven zero-write attempt; it never restores the nonce, and fresh evidence and approval are required. There is no automated remaining-work resume for partial or uncertain writes. Resolve the original job through the supported operational process; safe retry requires a separately verified finality/idempotency contract. New approval alone is insufficient.

If submission was accepted or is uncertain, do not enter the pre-submission recovery flow and never submit again. Perform the one immediate read-only status retrieval, then use only user-triggered read-only status refreshes. If a retrieval reports an error, stop and report the sanitized diagnostic and one safe next action.

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Auth/Authz | OAuth token or required privilege is rejected | Reauthenticate or obtain the required role, then revalidate readiness. |
| Approval Blocker | Execution is requested with missing or stale stage approval | Stop execution; complete required validation and present the exact current guard preview before requesting approval. Missing approval alone does not block preapproval validation or preview. |
| Catalog Mismatch | Current initialization registration/template is incompatible, or required action evidence is unavailable | Record the specific missing or incompatible contract element and whether it is confirmed or indeterminate. Apply the initialization registration reference; do not infer a missing action from absent optional fields or invent a replacement route. |
| Approval Blocker | Automatic review rejects an assisted-evaluation preview | Preserve the rejection and stated reason. Check the recorded node evaluations and evidence against Task Hook's supported assisted route. Correct missing evidence or inaccurate results locally; do not fabricate passed results, bypass review, or retry an unchanged rejected action. |
| Fusion API | A documented API call returns an error | Report the sanitized diagnostic and stop. |
| Indeterminate Submission | Oracle may have accepted a submission but completion is not verified | Reconcile via read-only progress lookup; never replay automatically. |
| Partial Execution | A pre-submission mutation failed or is uncertain | Inspect read-only, persist sanitized observations, retain pending markers, and resolve the original job without replay. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before execution | Target environment, intended configuration effect, redacted change summary, and required approval action. |
| Failed or indeterminate operation | Failure category, safe diagnostic summary, verified side effects, and one safe next action. |

Do not show raw internal status values, task codes, job names, or implementation constants. Translate state through `references/observed-state-branches.md`; retain a raw value only in protected support diagnostics when policy permits.

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Approval is absent, stale, or for another environment | Do not invoke a POST or PATCH. |
| Submission outcome is uncertain | Do not automatically retry or create a duplicate CPQ setup request. |
| Credentials, tokens, client secrets, or customer payloads are present | Do not persist or disclose them in resources, diagnostics, or run records. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CPQ.INITIALIZATION_EXECUTION_GATE | decision | 11 | execution_gate | ready->CPQ.INITIALIZATION_READY;blocked->CPQ.RETURN_ISSUES;failure->CPQ.FAILED | CPQ.INITIALIZATION_BINDING_READINESS | stop | Confirm the initialization readiness record is complete for Task Hook preview and CPQ guard manifest construction with approval pending. Missing current-stage approval alone is not a readiness failure; it blocks guard execution. This gate does not invoke or authorize initialization. |
| CPQ.CONFIGURATION_EXECUTION_GATE | decision | 12 | execution_gate | ready->CPQ.CONFIGURATION_READY;blocked->CPQ.RETURN_ISSUES;failure->CPQ.FAILED | CPQ.CONFIGURATION_BINDING_READINESS | stop | Confirm the configuration readiness record and required prior-stage reconciliation are complete for Task Hook preview and CPQ guard manifest construction with approval pending. Missing current-stage approval alone is not a readiness failure; it blocks guard execution. This gate does not invoke or authorize a Company Profile update, administrator creation, or submission. |
| CPQ.STATUS_REPORTED | terminal | 13 | terminal | none | CPQ.READ_STATUS_ONLY | continue | A user-requested, single authenticated read-only status response was reported; no configuration action or runtime handoff is authorized. |
| CPQ.INITIALIZATION_READY | terminal | 14 | terminal | none | CPQ.INITIALIZATION_EXECUTION_GATE | continue | Initialization readiness was handed off as a redacted immutable record to Core Data Loader. The terminal does not execute or authorize initialization. |
| CPQ.CONFIGURATION_READY | terminal | 15 | terminal | none | CPQ.CONFIGURATION_EXECUTION_GATE | continue | Configuration readiness was handed off as a redacted immutable record to Core Data Loader. The terminal does not execute or authorize Company Profile, administrator, or submission mutations. |
| CPQ.RETURN_ISSUES | terminal | 16 | terminal | none | none | continue | Preflight, authenticated read-only discovery, dependency readiness, approval, or handoff evidence is blocked. |
| CPQ.FAILED | terminal | 17 | terminal | none | none | continue | An authenticated read-only API request or verification step fails. |


For paginated reconciliation, an invalid, repeated or incomplete page is a
verification blocker: retain the pending marker and do not submit. A recovery
snapshot persistence failure is an artifact-persistence blocker before approval
consumption and upload. Historical operations may use the retained attempt ID
only after matching the original consumed ledger record and approval fingerprint.
Retain evidence for outstanding/dependent workflows, including accepted final
submissions requiring later inspection; do not clear records as a retry mechanism.
