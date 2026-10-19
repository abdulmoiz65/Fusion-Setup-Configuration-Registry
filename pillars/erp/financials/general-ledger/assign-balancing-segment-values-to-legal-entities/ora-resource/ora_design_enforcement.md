# Assign Balancing Segment Values to Legal Entities Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm task boundary | Restrict the delta to legal-entity balancing-value assignments in the selected ledger scope |
| 2 | Confirm carrier path | Prefer a new populated ledger-scoped export; allow a current template carrier only after a classified eligible populated-export failure |
| 3 | Confirm parent readiness | Require the legal entity to be an existing confirmed parent in the scoped accounting configuration; template structure alone is insufficient |
| 4 | Confirm assignment design | Require exact current value-set and value evidence and detect existing legal-entity or direct-ledger ownership from current business-state evidence |
| 5 | Confirm field contract | Derive every technical field, blank, and date serialization before authoring; do not use a failed import as discovery |
| 6 | Enforce smallest delta | Change only approved assignment rows; preserve populated closure or add only evidence-backed dependency closure required by a template carrier |
| 7 | Preview and approve | Show exact semantic and raw row changes, carrier mode, fallback evidence when applicable, checksums, and exclusions before import |
| 8 | Make submission recoverable | Bind a unique DataSetName and pre-submit task-process baseline to the approved ZIP, then run the existing Data Loader adapter with at least a 300-second outer command budget |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Always | Error | Current-run task carrier | No new populated ledger-scoped export was attempted, or the selected populated/template carrier is stale, unsafe, wrong-task, wrong-release, incomplete, or structurally invalid | Submit the exact populated export first; select a current same-task template only after a classified eligible carrier failure | Yes, before authoring |
| Template fallback is requested | Error | Populated-export failure classification | The failure is not proven to be a size limit, 413, completed-with-warning or incomplete carrier, transient 429 or 5xx, timeout, or result-download/transport failure | Correct invalid criteria, authentication, authorization, identity, business, corruption, or cancellation issues instead of falling back | No automatic fallback |
| Template fallback is selected | Error | Current fallback business-state evidence | The template is being used as proof of parent readiness, balancing value-set role, no existing assignment, or no direct-ledger conflict; or the separate evidence is stale or incomplete | Obtain supported current read-only evidence covering the exact parent and both assignment ownership paths; otherwise stop | Yes, before authoring |
| Always | Error | Exact legal-entity parent | The legal entity is absent, not confirmed, ambiguous, or belongs to a different selected scope | Complete the owning ledger/legal-entity configuration first, then re-export | Yes, through the owning setup workflow |
| Every requested row | Error | Exact ledger balancing value set and value | Ledger BalSegValueSetCode is missing or ambiguous; a supplied code disagrees; value exceeds MaximumLength; or exact value is missing, disabled, or ineffective | Correct the scope or input, or complete the owning setup and retry read-only validation | Yes, before authoring |
| Every requested row | Error | Existing assignment state | The exact value is assigned to a different legal entity or directly to the ledger in the same accounting context | Resolve ownership deliberately in the owning UI and confirm posted-use constraints; do not imply reassignment from a create request | No automatic fix |
| Exact assignment already exists | Information | Existing assignment state | No supported business field changes | Return no-op with current target and dates; do not submit an empty or metadata-only import | Not required |
| Explicit date update | Error | Existing assignment and row contract | Existing row is not unique, dates are invalid, or requested interval conflicts with eligibility | Correct the exact row or dates and rebuild the preview | Yes, before import |
| Deletion or reassignment is requested | Error | Current assignment state and accountable lifecycle evidence | Posted journals, final subledger accounting, or other use can prevent safe removal; this create/update baseline lacks a portable proof contract | Use the named task UI and assignment report with the required accounting review, then re-export | No automatic delete |
| Package delta exists | Error | Exact carrier diff and parser-based CSV check | A business row outside ORA_LEGAL_ENTITY_BAL_SEG_VAL_DEF.csv changes, a dependency row is added without exact current-state proof, an unrelated row, header, alias, manifest, or member order changes, or a changed CSV does not parse into the expected header and field-count records | Rebuild from the exact carrier with only the owned assignment delta and, in template fallback mode, the minimum evidence-backed manifest-required dependency closure; use a CSV serializer and verify actual record boundaries in the final ZIP | Yes, before preview |
| Any technical default lacks proof | Error | Current export, manifest, or documented read-only metadata | A technical value is guessed, copied from an unrelated row, or left to failed-import discovery | Refresh authoritative evidence; block before the first live import | Yes, before preview |
| Approved package is ready for Data Loader | Error | Submission recovery anchor | The ZIP basename is not unique to this attempt, differs from fileName or dataSetName, exceeds 200 characters, is not approval-bound, lacks a pre-submit task-process baseline, or the caller can terminate before 300 seconds | Regenerate and preview a uniquely named package, capture the baseline immediately before submission, and extend the caller budget before the first write | Yes, before import |

## Assignment Ownership Rules

| Rule | Contract |
|---|---|
| Legal entity before ledger | Complete legal-entity balancing-value assignments before assigning remaining values directly to the ledger |
| Exclusive ownership | In the selected accounting context, one exact value cannot be owned simultaneously by another legal entity and by the ledger |
| Existing parent only | This task may create or update an assignment child; it must not synthesize a ledger, legal entity, journal-configuration parent, chart of accounts, value set, or segment value |
| Explicit mutation | Existing-row dates change only when the user explicitly requests the change; create intent does not imply deletion or reassignment |
| Scope fidelity | Every parent and child key must trace to the same exact environment, release, task carrier, ledger scope, legal entity, and current evidence bundle |

## Package Preservation Rules

| Area | Required Behavior |
|---|---|
| Task-owned member | Preserve the actual 16-column `ORA_LEGAL_ENTITY_BAL_SEG_VAL_DEF.csv` header and all unrelated rows; add or update only approved exact semantic keys |
| Parent member | Preserve ORA_GL_JOURNAL_CONFIG_DETAIL.csv unchanged in populated mode. In template fallback mode, include only the exact manifest-required parent closure proven equal to current Fusion state; it is not a requested mutation target |
| Direct-ledger assignments | Preserve `GL_LEDGER_SEG_VAL_ASSIGNMENT.csv` unchanged and use it only for conflict detection |
| Other CSV members | Retain every member, actual header, row, alias, and header-only state exactly as the selected populated or template carrier requires; populate template dependency closure only when its values are proven |
| Manifest | Preserve ASM_SETUP_CSV_METADATA.xml byte and semantic content from the selected current carrier; do not regenerate it |
| Scope metadata | In populated mode require one manifest scope row for GL_PRIMARY_LEDGER whose PRIMARY_LEDGER_ID code equals the resolved LedgerId. In template mode bind the separately resolved LedgerId and current business-state receipt because the template does not prove ledger scope |
| Archive safety | Reject absolute paths, traversal paths, duplicate unsafe member names, unexpected executable content, or missing members before extraction or import |
| Size and dates | Enforce current Oracle FSM size limits and exact export-derived CSV date serialization |

## Preview and Approval Contract

| Preview Item | Required Evidence |
|---|---|
| Identity | Environment, release, task code and name, exact ledger scope, legal entity, carrier mode, current-run export process provenance, fallback failure and template provenance when applicable, and carrier checksum |
| Resolution | Resolver, source, exact filter or key, page completion, match count, canonical result, eligibility, and transport/auth state |
| Defaults | Field-by-field classification as user-supplied, resolver-derived, export-derived, intentional blank, preserved, or service-owned |
| Delta | Exact create, update, no-op, and delete counts; old and new semantic keys and dates; unrelated-row and member change count |
| Package | Member inventory; actual headers; manifest validation; carrier and final checksums; archive size and safety checks; populated-versus-template mode; dependency-closure diff |
| Boundary | No ledger activation, Review and Submit, period opening, value-set creation, value creation, direct-ledger assignment, deletion, or implicit reassignment |
| Approval | Explicit accountable approval bound to the final checksum and unique DataSetName; any input, lookup, package, filename, or diff change invalidates approval |
| Recovery anchor | Unique DataSetName no longer than 200 characters; CreatedBy; UTC submission-window start; TaskCode; SourceType FSM; pre-submit task ProcessIds; adapter command budget of at least 300 seconds |

## Execution Boundary

| Operation | Contract |
|---|---|
| Export | For each create or update execution, use `core.fusion-api.rest-api-client` to POST the populated `setupTaskCSVExports` request with SetupTaskCSVExportCriteria for GL_PRIMARY_LEDGER / Set1 / PRIMARY_LEDGER_ID / {LedgerId}; then pass its positive ProcessId to the existing `shared.setup-export.task-level-export` result poll/download helper. Do not block merely because the high-level exporter lacks a criteria switch, and do not submit an unscoped export. If classified safe evidence from the criteria-bearing attempt proves an eligible carrier failure after bounded read-only handling, invoke the shared skill in template-only mode for the same environment, release, and task. Never use template mode for excluded failures or as current business-state proof; reuse the selected carrier only within its unchanged evidence- and checksum-bound execution |
| Validation | Use the shared setup-data and reference-data validators before approval |
| Import | Route the approved exact FSM CSV ZIP through `core.data-loader` once. Use its exact ZIP basename as both fileName and dataSetName, allow at least 300 seconds for the adapter command, and keep waiting on the same invocation when the host yields; this resource does not invent another import implementation |
| Monitoring | Track the original import process identity to terminal state and retrieve safe process log and object-level error details |
| Identifier-free timeout recovery | If the one adapter invocation ends without ContentId or RequestId, do not retry. Resolve the exact DataSetName through the Data Loader dataset collection; if that endpoint is unavailable, compare the exact task import-process collection with the pre-submit baseline. Resume monitoring only when exactly one identity is recovered |
| Verification | First submit a new populated export of the identical task and ledger scope after import. If the same eligible carrier failure recurs, verify in the task UI or Balancing Segment Value Assignment Report only when it proves the exact expected ownership and dates with no unrelated changes; otherwise report verification incomplete and do not claim success |

## Source Basis

| Source | Use |
|---|---|
| Oracle General Ledger implementation guidance | Assignment order, legal-entity versus direct-ledger ownership, and task behavior |
| Oracle Setup and Maintenance CSV guidance | Package preservation, validation, approval, import monitoring, and verification |
| Oracle Enterprise Data Model | Relationship semantics and effectivity meaning only; no SQL or database execution logic |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ABSV.ENFORCE | decision | 50 | design_enforcement | pass->ABSV.ERROR_POLICY;blocked->ABSV.RETURN_ISSUES | ABSV.DEFAULTS | stop | A complete proposed delta or no-op decision exists |
