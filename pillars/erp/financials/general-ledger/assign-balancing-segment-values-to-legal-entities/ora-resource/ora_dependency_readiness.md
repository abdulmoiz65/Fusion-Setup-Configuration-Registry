# Assign Balancing Segment Values to Legal Entities Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target identity | Confirm environment, release, task code, and resolve the exact PRIMARY ledger to its canonical Name and LedgerId |
| 2 | Current task package | First submit and validate a new populated same-task FSM CSV export filtered by the exact LedgerId; use a current same-task template carrier only after a classified eligible populated-export failure |
| 3 | Existing parent context | Resolve the exact confirmed legal entity and ledger parent row already present in the accounting configuration; a template carrier alone is not parent or ownership evidence |
| 4 | Value metadata | Derive the ledger's balancing value-set code, then resolve its maximum length and every requested value's enabled and effective state through read-only metadata |
| 5 | Assignment state | Inspect the current populated task export, or supported current read-only Fusion evidence during a template fallback, for exact existing assignments and cross-target conflicts before selecting create, explicit update, or no-op |
| 6 | Package and approval | Preserve the package graph, apply the smallest supported row delta, validate it, preview it, and obtain checksum-bound approval before import |
| 7 | Submission recovery anchor | Before the first Data Loader write, bind a unique approval-visible ZIP basename, final checksum, submitter, UTC start time, task code, SourceType FSM, and the current task import-process baseline; allow at least 300 seconds for the adapter command to return |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| target_context | Exact environment, release, task, and PRIMARY-ledger scope | Yes | Always | Lookup | User input and current project context | resolve_primary_ledger_scope_for_export | Prevents cross-environment or cross-ledger authoring and provides the filter value required by Fusion task CSV export | Supply or confirm the exact primary-ledger name or ID | Environment; release; task code; canonical LedgerName; LedgerId |
| scoped_package | Current validated task carrier for this execution | Yes | Always | Blocked until validated | Primary: populated setupTaskCSVExports with exact task criteria; fallback: current same-task setupTaskCSVTemplateExports after a classified eligible carrier failure | select_validated_legal_entity_bsv_package | Supplies the supported physical package contract without reusing a stale carrier; only the populated primary path also supplies current parent and ownership rows | Attempt a new export filtered by GL_PRIMARY_LEDGER / PRIMARY_LEDGER_ID / {LedgerId}; if it has an eligible carrier failure, obtain a current template and the separate current business-state evidence | Carrier ZIP; checksum; primary or fallback mode; populated-export failure receipt when applicable; process provenance; member inventory; headers; manifest graph; scope receipt when populated |
| fallback_state_evidence | Current exact parent and assignment-state evidence independent of the template | Yes | Template fallback is selected | Lookup | Supported current read-only Fusion task UI, assignment report, or documented metadata receipts that cover the exact ledger and legal entity | resolve_template_fallback_business_state | A template proves schema only and cannot establish current parent readiness, another legal-entity owner, or direct-ledger ownership | Obtain current evidence for the exact ledger, legal entity, value set, and every requested value; if the evidence cannot cover both ownership paths, stop | Canonical parent identity and technical fields; ledger balancing value set; requested-owner rows; other-legal-entity rows; direct-ledger rows; evidence timestamp and scope |
| legal_entity_parent | Existing confirmed legal entity in the scoped configuration | Yes | Always | Lookup | Current populated task export, or the validated current fallback business-state evidence bundle | resolve_legal_entity_parent_row | An assignment child cannot safely synthesize its parent accounting configuration | Provide the exact legal-entity identifier or name and retain current evidence | LegalEntityIdentifier; ObjectName; ledger; parent technical fields |
| row_contract | Current assignment physical contract | Yes | Always | Lookup | Selected carrier header and ASM manifest; fallback also requires reviewed same-release same-role field evidence | derive_assignment_row_contract | Prevents guessing headers, types, field order, date serialization, and technical defaults | Refresh the carrier or business-state evidence if the contract cannot be proven | Header/order; data types; date format; parent linkage; population classes |
| balancing_role | Exact ledger balancing value set | Yes | Always | Lookup | Current scoped primary or secondary ledger alias | derive_scoped_balancing_value_set | Prevents accepting a real but unrelated value set and supplies the required technical FlexValueSetCode | If a code is supplied, it must match the exact ledger-derived code | ValueSetCode; balancing column; structure instance; key-flexfield receipt |
| value_set | Exact current value set | Yes | Always | Lookup | Ledger-derived code validated through Fusion Value Sets REST resource | resolve_value_set_exact | Establishes authoritative identity and MaximumLength before row generation | No separate code is required when ledger metadata resolves exactly | ValueSetId; ValueSetCode; MaximumLength; data and validation types |
| segment_values | Exact enabled and effective values | Yes | Every requested row | Lookup | Fusion Value Set Values child resource | verify_balancing_value_exact | Prevents assigning nonexistent, disabled, expired, future-ineligible, or wrong-set values | Correct or activate invalid values through their owning setup task | Value; enabled state; effectivity; summary/detail flags |
| assignment_state | Current exact assignment state | Yes | Every requested row | Verify | Current populated assignment members, or validated current fallback evidence covering legal-entity and direct-ledger owners | inspect_existing_assignment | Selects create, explicit update, or no-op without relying on failed import discovery | Review existing target and dates; do not request deletion implicitly | Existing row; current owner; current dates; row count; intended disposition; evidence source and timestamp |
| preview_approval | Accountable checksum-bound package approval | Yes | A nonempty delta is ready | Blocked until explicit approval | Final preview and approval receipt |  | The task changes legal-entity ownership of balancing values and downstream accounting attribution | Approve the exact final preview; any change invalidates approval | Approval identity; timestamp; final checksum |
| submission_recovery_anchor | Recoverable identity for the one approved Data Loader submission | Yes | Immediately before the first approved Data Loader write | Blocked until captured | Final approved archive plus current user, UTC clock, and read-only task import-process collection | prepare_fsm_submission_recovery_anchor | Prevents a caller timeout from leaving an untraceable write or causing an unsafe duplicate submission | Use a unique ZIP basename no longer than 200 characters and capture the exact task process baseline before calling Data Loader | DataSetName; archive checksum; CreatedBy; submission window start; TaskCode; SourceType; prior ProcessIds; command timeout budget |

## Dependency Classification

| Result Category | When Used | Can Continue? |
|---|---|---|
| Satisfied | Exact current evidence is present and eligible | Yes |
| Lookup | Business input exists but authoritative identity, eligibility, or technical metadata is unresolved | Read-only lookup only |
| Preserve | Package member or row exists only for dependency closure | Preserve without authoring |
| No-op | The exact assignment already exists and no explicit supported field change was requested | Report current state; do not submit an empty or metadata-only import |
| Blocked | Scope, package, parent, contract, value metadata, conflict decision, or approval is missing, stale, failed, or ambiguous | No |

## Package Acquisition and Shape

| Rule | Contract |
|---|---|
| Acquisition order | For every create or update execution, first resolve the exact PRIMARY LedgerId. Because the high-level task exporter has no criteria argument, use `core.fusion-api.rest-api-client` to POST `setupTaskCSVExports` with TaskCode `GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEGAL_ENTITIES`, one `SetupTaskCSVExportCriteria` row for GL_PRIMARY_LEDGER / Set1 / PRIMARY_LEDGER_ID / {LedgerId}, and one `SetupTaskCSVExportProcess` row. Require a positive returned ProcessId, then use the existing `shared.setup-export.task-level-export` result helper to poll and download that process. The missing high-level CLI option is not a blocker or fallback trigger. If safe process or HTTP/client evidence from this criteria-bearing attempt proves an eligible size, 413, incomplete-carrier, transient 429 or 5xx, timeout, or download/transport failure after bounded read-only handling, invoke the shared skill with template-only mode for the same task. Never fall back for invalid criteria, 400, final 401 or 403, missing privilege, unresolved identity, business conflict, corrupt downloaded content, or user cancellation |
| Freshness | Bind either the populated process receipt or the fallback failure receipt plus template process receipt to this run. In primary mode confirm environment, release, task, COMPLETED state, zero export errors, retrievable bytes, checksum, actual headers, manifest graph, and one exact PRIMARY_LEDGER_ID scope row. In fallback mode confirm the current same-task template process, retrievable bytes, checksum, required members, headers, and manifest, then separately bind current parent and ownership receipts. Reuse is allowed only within this same execution while the carrier checksum, evidence receipts, and all inputs remain unchanged |
| Required CSV members | `GL_LEDGER.csv`, `GL_SECONDARY_LEDGER.csv`, `ORA_GL_JOURNAL_CONFIG_DETAIL.csv`, `GL_LEDGER_SEG_VAL_ASSIGNMENT.csv`, `ORA_GL_LEDGER_RELATIONSHIP.csv`, `ORA_LEGAL_ENTITY_BAL_SEG_VAL_DEF.csv`, `ORA_GL_JOUNAL_CONVERSION_RULES.csv`, `ORA_PRIMARY_BALANCING_SEGMENT_VALUE_CONVERSION_RULES.csv`, `ORA_GL_PRIMARY_LEDGER_CONFIG.csv`, and `GL_PRIMARY_LEDGER.csv` |
| Required manifest | Preserve `ASM_SETUP_CSV_METADATA.xml`, including Oracle member names, logical paths, field graph, node order, task/release metadata, and header order |
| Task-owned member | Only ORA_LEGAL_ENTITY_BAL_SEG_VAL_DEF.csv assignment rows are eligible for a business delta. In fallback mode, populate only manifest-required dependency rows whose values are proven equal to current Fusion state; they are closure, not requested setup changes |
| Dependency closure | In primary mode preserve all other members, rows, aliases, actual headers, and header-only members unchanged. In fallback mode preserve the current template members and manifest, and add only the minimum evidence-backed dependency rows required by its graph |
| Size and serialization | Keep the ZIP and CSV members within current Oracle FSM limits and preserve the selected carrier's quoting, encoding, line-ending tolerance, and date format. Reject an incomplete populated package. A verified eligible carrier failure permits one current template export, but the template never substitutes for current parent or ownership evidence |
| Post-import verification | First submit another new populated export with the identical ledger criterion after the import reaches a terminal state. If the same eligible carrier failure recurs, verify through supported current read-only task UI, assignment report, or documented metadata that proves the exact expected owner and dates; otherwise mark verification incomplete. Never treat the pre-import package or import status alone as business-state verification |

## Source Basis

| Source | Use |
|---|---|
| Oracle Setup and Maintenance CSV export and import guidance | Export-first carrier, package preservation, validation, import monitoring, and verification |
| Oracle Setup Task CSV Exports REST API | `SetupTaskCSVExportCriteria` request fields and task export process/result retrieval |
| Oracle General Ledger setup guidance | Legal entities receive balancing values before values are assigned directly to a ledger |
| Current task catalog | Confirms export/import and CSV export/import support for the task |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ABSV.DEPENDENCIES | decision | 20 | resolve_dependency | ready->ABSV.LOOKUPS;blocked->ABSV.RETURN_ISSUES | ABSV.VALIDATE | stop | Validated intake exists |
