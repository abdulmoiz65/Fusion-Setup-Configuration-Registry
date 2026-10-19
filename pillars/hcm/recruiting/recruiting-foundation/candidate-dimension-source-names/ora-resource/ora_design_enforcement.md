# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm source identity | Resolve the requested operation against verified source evidence |
| 2 | Prepare only the requested delta | Rename one source-language cell or append one base row and one language row |
| 3 | Verify preservation | Compare the final candidate against the unchanged baseline before preview |
| 4 | Delegate validation and import | Use shared validation and core Data Loader including Task Hook, immutable preview and approval |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Retrieve | Blocker | resolve_source_export | Selected language is missing or ambiguous or an unmatched base row would be dropped | Require one translation per source; do not use the first match | No |
| Rename | Blocker | resolve_source_export | Current Name does not resolve to one source-language identity | Return NOT_FOUND or AMBIGUOUS_SOURCE; request URL/medium when needed | No |
| Rename | Blocker | resolve_source_export | Another source-language identity already has the proposed Name | Return ALREADY_EXISTS; preserve the other source | No |
| Rename no-op | Information | resolve_source_export | Exact source already has the requested Name | Return NO_CHANGE without a candidate or import | No |
| Add Row | Blocker | resolve_source_export | Proposed URL occurs across any medium, or Name occurs in SourceName/SourceDisplayName, using case-insensitive duplicate checks | Return ALREADY_EXISTS; never convert creation to update | No |
| Add Row | Blocker | resolve_source_export | Baseline schema or joins differ from the verified package contract | Resolve the schema before appending records | No |
| Before import | Blocker | resolve_source_export | Candidate changes an unrelated field, translation, archive member or baseline identity | Return PRESERVATION_FAILED and rebuild from the verified baseline | Yes |
| Any operation | Blocker | | Requested work changes another task, existing URL/sequence/medium, translation, or deletes a source | Stop at the supported boundary | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_source_export | Retrieve, rename, Add Row and internal validate_import | Verified package contract, unique identities, language rows and before-values | ora_reference_lookups.md |

## Prepare rename

Use a new candidate path and retain the fresh baseline and its SHA-256. Match the
exact current Name in the source-language translation joined to its unique base.
Apply supplied URL/medium disambiguation; never use Name as the join key. Replace
only SourceDisplayName in that row. Do not change SourceName, URL, medium, Sequence
or another language. Preserve all CSV bytes outside the target cell, including
quoting, BOM and line endings. Escape commas and quotes according to the exported
CSV representation; validate by parsing the result, not by line-based replacement.

## Prepare Add Row

Derive the candidate from the verified export, preserving original member metadata,
names, order and comment. Append exactly one row to each source CSV using its
existing header order and line ending. Use the explicit URL for base SourceUrlValue
and TL parent URL; use the documented direct-source defaults for both parent medium
fields. Set base SourceName and TL SourceName/SourceDisplayName to the requested Name,
and TL Language/SourceLang to the verified language. Leave unspecified nullable fields
blank as defined by defaulting rules. Do not allocate surrogate IDs, copy another
source's business fields, synthesize extra translations or edit XML metadata.

## Validate import

Apply shared setup-data and applicable reference validation, then core Data Loader's
normal FSM validation without approval/upload. Its Task Hook runs internal
validate_import on the existing baseline, final candidate and exact request.
Independently verify the following before building the immutable preview:

| Operation | Required comparison |
|---|---|
| Both | Valid ZIP CRCs; identical member names/order/comment and metadata; exact task/environment provenance; unchanged non-target members; new output path; final candidate SHA-256 |
| Rename | Same CSV headers, rows, order and identities; exactly one requested source-language SourceDisplayName changes; every other cell and translation is unchanged |
| Add Row | Original CSV bytes remain an unchanged prefix; exactly one new base and one requested-language row; appended values match the request and defaults; every other member unchanged |

Bind actual validation findings, before/after values and final archiveSha256 into
the core Data Loader Task Hook preview. Do not mark a result passed without checking
the final archive. Internal validate_import never exports, calls the loader recursively,
or uploads. Changed artifacts invalidate the preview and require revalidation.

## Post-import verification

Inspect the detailed FSM result for every business object, then obtain a fresh
task export to confirm the renamed Name or new Name/URL/language/sequence. Compare
all pre-existing source rows and translations with the baseline. A successful
initiation alone does not establish persistence or translation propagation.

For Add Row, the upload candidate must still contain exactly one new base row and
one requested-language row. Fusion may generate additional language rows for that
new identity after import. Record the actual server-generated rows separately;
verify the requested-language values and that all pre-existing rows are unchanged.
Do not synthesize translations in the candidate or treat blank generated display
names as verified translations. Unexpected changes to existing identities still
fail preservation checks.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CDSN.ENFORCE_DESIGN | step | 50 | design_enforcement | enforced->CDSN.READINESS_GATE;blocked->CDSN.HANDLE_ISSUES | CDSN.APPLY_DEFAULTS | stop | Apply operation-specific preservation rules; validate_import compares the existing final archive |
