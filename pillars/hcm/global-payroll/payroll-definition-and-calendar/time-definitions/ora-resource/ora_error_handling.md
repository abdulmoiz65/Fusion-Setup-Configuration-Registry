# Payroll Time Definition Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required parent or child identity or documented type-dependent input is missing | Name operation, component, row/key, field, and supplied value; stop before DAT construction. |
| Direct parent business value or UsageType is unfamiliar | Preserve the trimmed value and continue; do not require an allowlist override or substitute a lookup code. |
| Local task context is absent | Bootstrap and validate it from exact active-project, catalog, and nested-skill values without separate approval. |
| Existing task context conflicts | Stop and identify the exact conflicting field; never overwrite silently. |
| LDG or true reference has no unique same-LDG match | Report not found, ambiguity, inconsistency, or cross-LDG scope; never choose the first row. |
| Parent create key exists | Stop before upload and disclose the business key and candidate count. |
| Parent delete key is absent or ambiguous | Stop before DELETE construction and disclose supplied code or DefinitionName plus LDG; when a name resolves, derive the DAT code from ShortName and never request or display TimeDefinitionId. |
| Parent delete has exported usage rows | Report every exact UsageType meaning as cascade-delete impact and continue to the single parent DELETE preview; do not require or emit child DELETE rows. |
| Parent delete has dependent time definitions | Report dependent natural keys and BaseTimeDefinitionCode or PeriodTimeDefinitionCode reference fields that equal the target DefinitionName; stop before approval. |
| Parent delete has an explicitly exposed delivered or protected marker | Report that protected result without exposing internal IDs; stop before approval. |
| Parent delete ownership or unrelated cross-consumer resolver is unavailable | Record the unresolved limitation, disclose it in the preview, continue to normal approval when verified task-export checks pass, and let Fusion Data Loader enforce referential integrity. |
| Usage assignment already exists | Report that the exact child natural key is already assigned and do not upload a redundant MERGE. |
| Usage removal target is absent or ambiguous | Report the exact child natural key derived from parent ShortName and do not upload DELETE. |
| Usage export unqualified code equals joined parent DefinitionName | Disclose usage export display-name projection, retain the joined parent ShortName as the HDL TimeDefinitionCode, and continue through child validation, immutable preview, and approval. |
| Usage export unqualified code identifies a different or unreconcilable parent | Stop before child DAT construction and report conflicting identity evidence. |
| Fresh export has zero usage candidates immediately after a create | Do not report the usage absent or stop immediately. First evaluate exact immutable DAT plus successful terminal ProcessId evidence or authenticated exact read-back from the same target, task, and LDG. Continue only on fully matching qualified evidence and disclose task export visibility lag. |
| Recent HDL evidence is preview-only, initiated-only, failed, warning-only without confirmed row success, unknown-status, cross-target, or conflicting | Stop before child DAT construction; do not infer a parent or usage key from that evidence. |
| Parent business-field update is requested | State that the field is registered as not updatable; never delete and recreate to emulate an edit. |
| Export is failed, truncated, unusable, inconsistent, or explicitly relevant warning exists | Stop before preview and report the first concrete evidence failure; do not use fallback identity logic. |
| Export is COMPLETED_WARNINGS or optional warning details are unavailable without relevant failure | Disclose and continue when required structure and cardinality are usable. |
| DAT construction completes | Continue through live BO/template validation, task-rule preview, fingerprinting, and one approval request; do not return done. |
| Live schema validation fails | Report exact component, operation, header or attribute mismatch, field, value, and stage; do not upload. |
| Preview changes after approval | Invalidate approval, rebuild preview/fingerprint, and request fresh approval. |
| User declines approval | Make no upload or submission and disclose the not-approved result. |
| Authentication or authorization fails | Stop on missing session, inaccessible task/LDG, 401, 403, or Data Loader denial; approval cannot bypass denial. |
| Data Loader rejects a row | Return operation, component, natural key, field, supplied value, source stage, and first concrete loader message. |
| Initiation succeeds | Report accepted initiation immediately; do not poll unless status or verification is subsequently requested. |
| Mutation response is uncertain | Do not retry automatically; reconcile through safe reads first. |
| Process fails | Report ProcessId, terminal status, row counts, and first concrete failing stage or row message. |
| Read-back differs | Report initiation, process result, and verification separately. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required value, DAT safety, date/number, paired key, child meaning, or documented type-shape rule fails | Correct the field and restart continuous preflight |
| Project context | Existing task context is ambiguous, incomplete, or conflicting | Correct or safely extend it; never overwrite silently |
| Reference resolution | LDG, parent/child key, base, or period reference has wrong cardinality or scope | Supply exact business identity or refresh documented evidence |
| Parent delete safety | Exported base or period dependency or explicitly exposed protected ownership blocks deletion; exported usage rows are disclosed cascade impact | Correct the dependent definition or stop for the protected target; review exact usage meanings that will be cascade-deleted |
| Unsupported parent update | Registered parent attribute is not updatable | Do not emulate through delete and recreate; use verified child maintenance only when applicable |
| Authorization | Authentication, task access, LDG scope, approval, or Fusion enforcement fails | Correct access and restart from safe preflight stage |
| Contract gap | Field limit, localization, existing-environment cycle, or another execution-critical behavior remains TBD | Obtain source evidence for the affected operation; unavailable parent-delete ownership and unrelated cross-consumer resolvers remain disclosed nonblocking limitations |
| Data Loader failure | Upload, initiation, HDL processing, or downstream process reports an error | Correct first concrete failure before a fresh approved submission |
| Verification mismatch | Read-back cannot confirm intended state | Reconcile through supported read-only evidence |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Parent create preview | Operation, LDG, code, name, supplied values, exact immutable MERGE DAT, fingerprint, candidate count, schema result, and nonblocking warnings. |
| Parent delete preview | Supplied code or DefinitionName, resolved ShortName DAT code, target DefinitionName for dependency checks, LDG, exact parent count, usage count, every exact UsageType meaning that will be cascade-deleted, dependent-definition count, any explicitly exposed protected result, unavailable ownership or cross-consumer limitations, the single natural-key parent DELETE DAT with no child DELETE rows, fingerprint, and warnings; never show TimeDefinitionId. |
| Usage assignment preview | Supplied parent code or DefinitionName, resolved ShortName child code, LDG, exact UsageType meaning, zero-child evidence, any usage export display-name projection warning, child MERGE DAT, fingerprint, and schema result; never show internal IDs. |
| Usage removal preview | Supplied parent code or DefinitionName, resolved ShortName child code, LDG, exact UsageType meaning, one-child evidence, any usage export display-name projection warning, child DELETE DAT, fingerprint, and schema result; never show internal IDs. |
| Export-lag usage preview | Exact parent and child natural key from qualified successful DAT or authenticated read-back, successful terminal ProcessId or read-back evidence, task export visibility-lag warning, child DAT, fingerprint, and schema result; never show internal IDs. |
| Local context bootstrap | Local context path and sequence without credentials or protected target IDs. |
| Approval | Environment, operation, business natural key, exact DAT display, and fingerprint. |
| Submission | Distinguish approved, uploaded, and initiated states without claiming terminal completion. |
| Status or verification | When requested, report terminal status, counts, first concrete errors, and read-back separately. |
| Privacy | Never disclose credentials, tokens, cookies, environment secrets, or internal IDs used only for resolution. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Mutation request | Do not use direct mutation REST or payrollTimeDefinitionsLOV; use core.data-loader, HDL, and PayrollTimeDefinition. |
| Business-value validation | Do not require direct parent values or UsageType to appear in examples, exports, existing rows, or lookup evidence. |
| Missing bootstrappable context | Do not ask for separate approval to create reversible local task context. |
| DAT created | Do not terminate or ask the user to initiate remaining read-only preflights before schema validation and approval. |
| Parent delete | Do not require, substitute, display, or expose TimeDefinitionId in DAT or preview, and do not require or emit TimeDefinitionUsage DELETE rows for complete parent deletion. |
| Usage child | Do not require or expose TimeDefinitionId or TimeDefinitionUsageId, substitute UsageTypeCode, or invent an allowlist. |
| Parent update | Do not emit a parent-field MERGE or simulate update through delete/recreate. |
| Unapproved operation | Do not upload or initiate before fresh approval for exact immutable preview. |
| Changed content | Do not submit modified bytes under earlier approval. |
| Uncertain response | Do not automatically retry. |
| HDL code lookup | Do not query payrollTimeDefinitionsLOV by TimeDefinitionCode or use SQL, fuzzy, name-only, or first-row substitutes. Resolve a supplied DefinitionName only through the exact task export with LDG, then derive the code from ShortName. |
| Export-lag fallback | Do not treat a zero-row export as authoritative absence immediately after create. Do not accept preview-only, initiated-only, failed, unknown-status, cross-target, or conflicting evidence as a usage key. |

## Execution Boundary

This current-strict graph prepares and gates parent create/delete and usage assignment/removal through separate approval nodes. After approval, each success terminal authorizes only one unchanged core.data-loader HDL submission with businessObject PayrollTimeDefinition. Parent update is unsupported. Data Loader owns upload and initiation; status and read-back occur only when later requested.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TD.CREATE_PREVIEW | step | 140 | execution_gate | prepared->TD.CREATE_APPROVAL;blocked->TD.ERROR_HANDLE | TD.VALIDATE_CREATE_DAT | stop | Build immutable parent-create preview and bind fingerprint |
| TD.DELETE_PREVIEW | step | 145 | execution_gate | prepared->TD.DELETE_APPROVAL;blocked->TD.ERROR_HANDLE | TD.VALIDATE_DELETE_DAT | stop | Build immutable parent-delete preview with exact cascade usage meanings, verified blocking impact checks, disclosed nonblocking limitations, and no IDs |
| TD.USAGE_ASSIGN_PREVIEW | step | 150 | execution_gate | prepared->TD.USAGE_ASSIGN_APPROVAL;blocked->TD.ERROR_HANDLE | TD.VALIDATE_USAGE_ASSIGN_DAT | stop | Build immutable child-MERGE preview with preserved UsageType meaning and no IDs |
| TD.USAGE_REMOVE_PREVIEW | step | 155 | execution_gate | prepared->TD.USAGE_REMOVE_APPROVAL;blocked->TD.ERROR_HANDLE | TD.VALIDATE_USAGE_REMOVE_DAT | stop | Build immutable child-DELETE preview with preserved UsageType meaning and no IDs |
| TD.CREATE_APPROVAL | decision | 160 | execution_gate | approved->TD.DONE_CREATE;declined->TD.ERROR_HANDLE;stale->TD.ERROR_HANDLE | TD.CREATE_PREVIEW | stop | Request fresh approval for exact parent-create preview |
| TD.DELETE_APPROVAL | decision | 165 | execution_gate | approved->TD.DONE_DELETE;declined->TD.ERROR_HANDLE;stale->TD.ERROR_HANDLE | TD.DELETE_PREVIEW | stop | Request fresh approval for exact parent-delete preview |
| TD.USAGE_ASSIGN_APPROVAL | decision | 170 | execution_gate | approved->TD.DONE_USAGE_ASSIGN;declined->TD.ERROR_HANDLE;stale->TD.ERROR_HANDLE | TD.USAGE_ASSIGN_PREVIEW | stop | Request fresh approval for exact usage-assignment preview |
| TD.USAGE_REMOVE_APPROVAL | decision | 175 | execution_gate | approved->TD.DONE_USAGE_REMOVE;declined->TD.ERROR_HANDLE;stale->TD.ERROR_HANDLE | TD.USAGE_REMOVE_PREVIEW | stop | Request fresh approval for exact usage-removal preview |
| TD.DONE_CREATE | terminal | 180 | terminal | none | TD.CREATE_APPROVAL | stop | Exact parent-create DAT is approved for one Data Loader submission |
| TD.DONE_DELETE | terminal | 185 | terminal | none | TD.DELETE_APPROVAL | stop | Exact parent-delete DAT is approved for one Data Loader submission |
| TD.DONE_USAGE_ASSIGN | terminal | 190 | terminal | none | TD.USAGE_ASSIGN_APPROVAL | stop | Exact usage MERGE DAT is approved for one Data Loader submission |
| TD.DONE_USAGE_REMOVE | terminal | 195 | terminal | none | TD.USAGE_REMOVE_APPROVAL | stop | Exact usage DELETE DAT is approved for one Data Loader submission |
| TD.ERROR_HANDLE | step | 200 | error_handler | disclosed->TD.DONE_ISSUES | none | continue | Any failed, declined, stale, unsupported, unsafe, uncertain, or incomplete result |
| TD.DONE_ISSUES | terminal | 210 | terminal | none | TD.ERROR_HANDLE | stop | Blocking or declined result disclosed and no live submission authorized |
