# Manage Legal Jurisdictions Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required input, length, flag, or date rule fails | Stop and identify the failing field and constraint. |
| Geography or lookup code has zero, many, disabled, or ineffective matches | Stop; disclose normalized input, request path, eligibility rule, and result count. |
| Legal Function has no unique enabled FunctionCode | Stop the function branch; do not write the display label to FunctionCode. |
| LOV discovery endpoint is unavailable, unauthorized, partial, or ambiguous | Return no partial list; identify the endpoint and its failure class. |
| Non-primary Territory or hierarchy value | Exclude the addressGeographies row from all choice, suggestion, and resolution sets when any required primary flag is false. Preserve raw evidence; never silently normalize an explicitly supplied alternate. |
| Required primary flag missing, null, or unrecognized | Re-read the affected identity or coherent hierarchy projection and its applicable primary flags; if eligibility remains unknown, stop choice delivery and resolution as a primary-flag metadata gap. Do not treat an unknown flag as false or true. |
| No primary-eligible candidate remains | Report no eligible primary Territory choices; do not fall back to excluded alternates or infer that the raw endpoint returned zero rows. |
| Endpoint candidate difference | Preserve valid rows from identity discovery and depth-appropriate addressGeographies enrichment, apply primary eligibility before deduplicating eligible rows by the visible row tuple, retain raw and exclusion receipts, and require a visible-row selection. |
| Territory auto-resolved before all required receipts complete | Classify as an orchestration failure. Return to Territory discovery; do not retrieve code LOVs, prepare a package, or create setup data. |
| Multiple Territory candidates but the response offers only one confirmation row or malformed columns | Classify as a Territory choice-delivery failure. Regenerate the full five-column table (first 50 plus complete Markdown artifact when needed) and require visible-row selection; do not continue. |
| Remaining LOV response is partial, uses first values, or is delimiter-separated | Classify as an orchestration failure. Re-page every required endpoint and return separate complete one-column `Choice` tables only after Territory Resolution Gate succeeds. |
| Remaining LOV table has a missing count, `<br>` values, only its first choice, or lacks its >50 complete-list artifact | Classify as `lov_delivery_failed`. Do not ask for selections or continue validation; re-retrieve and render all four required LOV tables. |
| Territory pages are retrieved but the choices are not delivered | Classify as an orchestration failure. Finish the requested identity search pagination and return up to 50 UI-style rows plus a complete Markdown table link when additional rows exist; do not ask for an internal identifier. |
| Equivalent jurisdiction exists | Report that it already exists and do not create duplicate setup data. |
| Existing jurisdiction differs | Show field-level requested-versus-existing differences and request an explicit update-versus-new decision. |
| Immutable field is changed | Reject the update and explain which field is immutable after creation. |
| Identifying rule conflicts | Show existing identifying jurisdictions for the geography and the expected Oracle clearing/automatic-identification effect. |
| Active-registration evidence is missing or positive | Block end dating or conflicting start-date changes. |
| Export metadata or a technical value outside the reusable default policy is unresolved | Stop before archive generation; classify as a technical lookup gap rather than using an import failure to discover it. Header-only templates and documented defaults are not a gap. |
| FSM geography carrier is unavailable from supported Territory endpoints | Record a readiness warning with the selected hierarchy and endpoint receipts. Continue package preparation, validation, and explicitly approved import submission; do not copy an existing jurisdiction row to fill the value. |
| CSV has a UTF-8 BOM or its header differs from the export | Stop before preflight; rebuild from the export header in UTF-8 without BOM. |
| A generated CSV data row has a different field count from its header, or its shared parent/child geography values differ | Classify as a package contract gap. Do not upload or initiate; rebuild from header-indexed values, CSV-parse every row, and require exact header/data cardinality before a new preview. |
| Final readiness fails | Stop before core.data-loader preview and list every missing member, column, value, source, or decision. |
| Import or verification later fails or the initiation receipt is incomplete | Preserve redacted package/process evidence. Before any retry, reconcile dataLoaderDataSets by the exact archive/data-set name, then retrieve errors and the FSM ProcessLog when a request exists; do not replay a mutation without the core.data-loader approval workflow. |
| FSM dataset counters report success but its ProcessLog contains `Completed with warnings`, `error`, `failed`, CSV parsing errors, or zero processed objects | Treat the import as failed or warning-blocked, not successful. Report the ProcessLog finding, do not claim the setup data was created, and require a corrected package plus a new approval before resubmission. |

## Unavailable Canonical Geography Mapping

For a valid create, apply the two-check policy in ora_reference_lookups.md:
exclude only geography/category uniqueness and identifying-impact prechecks as
not_applicable warnings. Do not ask for a waiver, infer a clean result, or defer
other errors. A failed request or incomplete response is not this exclusion.
If import rejects the geography/category combination, quote the reviewed log's
actual error; do not assert which geography resolved unless independently
verified. Preserve the failed result and require corrected preparation and the
normal approval path before retrying.

## Reviewed Log Outcome Evidence

Read the downloaded FSM ProcessLog before quoting success or failure. Use its
final outcome, processed-object summary, warning count, and actionable errors,
not its initial In progress line. Quote a short exact outcome or error line and
link the reviewed log using the task-local format below. A failure,
warning, parsing error, or zero processed objects blocks a success claim even
when dataset counters appear successful. Missing or unreadable logs mean the
outcome is unverified; do not invent a quotation. If counters lag a completed
log, refresh status once read-only and disclose any remaining discrepancy.

After the unchanged Data Loader status report, show one compact evidence block
for each final outcome or actionable error that was actually reviewed:

**Reviewed log:** [FSM Process Log](<actual-log-path>)
> <Short exact final outcome or actionable error line from the reviewed log>

Preserve the message wording subject to credential and sensitive-value redaction.
Do not dump the full log, invent a quote, or suppress failure/warning findings.
If no applicable log can be read, say that log verification is incomplete and
identify the API status as the available evidence. This task-local rule applies
only to Legal Jurisdiction status/outcome requests. Accepted initiation still
returns Data Loader's original In Progress report immediately without polling.

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required field, length, format, flag, or date validation fails | Correct the exact input |
| Technical lookup gap | Lookup is zero/many/unavailable or its supported contract is TBD | Resolve evidence; do not guess |
| Existing match | Equivalent definition exists | Reuse and verify |
| Business decision | Existing definition differs | Present field-level differences for a user decision |
| Design policy | Identifying, uniqueness, immutable-field, or active-registration rule fails | Correct the design or use a separately approved new definition |
| Package contract gap | Metadata, template, source evidence, technical default, or readiness entry is incomplete | Refresh export and revalidate |
| Auth or authz | Read-only source is unavailable due to privilege | Refresh approved read authentication once, then stop |
| Fusion API or process failed | A later central import/export process fails | Persist redacted status/log and do not replay blindly |

## First-Go Import Readiness Record

| Check | Required Evidence |
|---|---|
| Target and task | Exact target environment, release, task code XLE_MANAGE_LEGAL_JURISDICTIONS, and export timestamp |
| Required members | ASM_SETUP_CSV_METADATA.xml, XLE_JURISDICTION.csv, and ORA_XLE_JURISDICTION_DATA.csv, with archive paths and hashes |
| Parent columns | Exact exported XLE_JURISDICTION.csv header/order, including LegislativeCatCode, geography transient fields, Name, IdentifyingFlag, RegistrationCodeLe, RegistrationCodeEtb, RequiredEtbFlag, RequiredLeFlag, Active, effective dates, and JurisdictionCode |
| Child columns | Exact exported ORA_XLE_JURISDICTION_DATA.csv header/order: parent geography transients, FunctionCode, and RequiredFlag; each Legal Function row uses `RequiredFlag` defaulting to `Y`, with explicit valid user input taking precedence; header-only when no Legal Function is included |
| Encoding and row evidence | UTF-8 without BOM for every CSV; CSV-aware parse evidence that every data row has the exact header field count; exact parent/child shared-geography comparison; and the tested Legal Function child-row count from the validated archive because FSM process summaries can aggregate child rows under one business object |
| Columns and values | Every required column, supplied value, generated value, and defaulted technical value |
| Source evidence | Export/template location and fingerprint, read-only lookup receipt, Oracle documentation, or EDM reference for each non-user value |
| Existence result | Equivalent/different/absent result and requested-versus-existing comparison |
| Unresolved items | Each unresolved value marked as a business decision or technical lookup gap |
| Package approval status | Approved for central preview only when no technical lookup/default remains unresolved; this record is not approval for a live import |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before package generation | Resolved geography and codes, existence result, identifying impact, immutable-field check, date-impact result, and technical default sources |
| LOV discovery result | Resolved Territory, every required endpoint, retrieval timestamp, pagination/result counts, and display label/internal-code pairs; disclose that the list is available/enabled, not an inferred Territory-specific entitlement unless response metadata proves it |
| Guided clarification | Missing Territory returns the first bounded identity page and requests a Territory search term. A supplied Territory returns up to 50 merged UI-style search candidates in the same response; when additional rows exist, provide the total count and a linked complete Markdown choice table. After visible-row selection, return every remaining required LOV in one consolidated response and mark Legal Functions optional. |
| READY_FOR_DATA_LOADER_PREVIEW handoff | Complete readiness record, archive fingerprint, and statement that central Data Loader preview/import has not been created or approved |
| Failure | Failure class, environment, task code, stage, redacted evidence, and recommended action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Unresolved code/default | Do not generate or submit an FSM ZIP to discover a known technical value from a failure log. |
| UI label | Do not place a UI label into a code field without export/metadata evidence that it is accepted. |
| Existing equivalent | Do not create duplicate setup data. |
| Existing difference | Do not update or create a competing record until the user chooses. |
| Active registrations or incomplete clearance | Do not end date or alter a conflicting effective start date. |
| Live mutation | Do not upload, preview, or import; only core.data-loader may perform its later approval-governed operation. |
| Incomplete LOV discovery | Do not return a partial or stale set of selections as all valid values. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LJ.PACKAGE_PREVIEW_GATE | decision | 60 | execution_gate | ready->LJ.READY_FOR_DATA_LOADER_PREVIEW;blocked->LJ.HANDLE_ERROR;failure->LJ.HANDLE_ERROR | LJ.ENFORCE_DESIGN | stop | After final immutable FSM archive and readiness record are available |
| LJ.HANDLE_ERROR | step | 70 | error_handler | handled->LJ.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, defaulting, enforcement, or readiness failure |
| LJ.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| LJ.RETURN_LOVS | terminal | 85 | terminal | none | none | stop | Complete read-only Territory choice delivery or LOV discovery succeeded; no create, package, preview, or import action occurred |
| LJ.READY_FOR_DATA_LOADER_PREVIEW | terminal | 90 | terminal | none | LJ.PACKAGE_PREVIEW_GATE | stop | All task rules and first-go readiness checks passed; no preview or import has been created |
